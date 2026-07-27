# Profiling Recipes

Query and code patterns for producing profile statistics. Load the sections matching your access path and column types. SQL is written for standard ANSI syntax with engine notes where dialects diverge.

## Cost Control Before Anything Runs

| Table size | Approach | Note in output |
|---|---|---|
| < 10M rows | Full scan, exact statistics | "exact" |
| 10M–1B rows | Sample for distributions, exact for row count and key uniqueness | Sample size and method |
| > 1B rows, or billed by bytes scanned | Sample everything; restrict to a recent partition | Sample size, method, partition filter |

Sampling clauses by engine:

```sql
-- BigQuery: system sampling
SELECT * FROM `project.dataset.table` TABLESAMPLE SYSTEM (1 PERCENT);

-- Snowflake: row (Bernoulli) sampling, reproducible with a seed
SELECT * FROM table SAMPLE BERNOULLI (1) REPEATABLE (42);

-- PostgreSQL: block sampling, fast but clustered
SELECT * FROM table TABLESAMPLE SYSTEM (1);

-- Portable fallback: hash the key so the sample is stable across runs
SELECT * FROM table WHERE MOD(ABS(FARM_FINGERPRINT(CAST(id AS STRING))), 100) = 0;
```

Block sampling is fast but correlates with physical layout — if rows were loaded in date order, a block sample skews toward a date range. Prefer row or hash sampling when the profile drives a decision.

Partition-pruning first, sampling second: an unfiltered sample on a partitioned table can still scan every partition's metadata and cost more than expected.

## Grain And Key Verification

```sql
-- Row count vs. distinct key count: equality proves uniqueness at that grain
SELECT
  COUNT(*)                       AS rows,
  COUNT(DISTINCT candidate_key)  AS distinct_keys,
  COUNT(*) - COUNT(DISTINCT candidate_key) AS excess_rows
FROM table;

-- Compound key check
SELECT COUNT(*) AS rows, COUNT(DISTINCT CONCAT(col_a, '|', col_b)) AS distinct_pairs
FROM table;

-- Which keys duplicate, and how badly
SELECT candidate_key, COUNT(*) AS copies
FROM table
GROUP BY candidate_key
HAVING COUNT(*) > 1
ORDER BY copies DESC
LIMIT 20;
```

Concatenate compound keys with a separator that cannot appear in the values; `'a|b'` and `'ab|'` collide without one. Nulls in a candidate key are excluded from `COUNT(DISTINCT ...)` — count them separately or the key looks more unique than it is.

## Universal Column Statistics

```sql
-- One column, all universal stats
SELECT
  COUNT(*)                                        AS total_rows,
  COUNT(col)                                      AS non_null,
  COUNT(*) - COUNT(col)                           AS nulls,
  ROUND(1.0 * (COUNT(*) - COUNT(col)) / COUNT(*), 4) AS null_rate,
  COUNT(DISTINCT col)                             AS distinct_values,
  ROUND(1.0 * COUNT(DISTINCT col) / NULLIF(COUNT(col), 0), 4) AS cardinality_ratio
FROM table;

-- Top and bottom values in one pass; the tail exposes placeholders
SELECT col, COUNT(*) AS freq
FROM table
GROUP BY col
ORDER BY freq DESC
LIMIT 10;
-- repeat with ORDER BY freq ASC for the rare tail
```

Cardinality ratio reads as: near 1.0 means identifier-like, near 0 means categorical. A `user_id` at 0.02 means the grain is not one row per user, or the ID is being reused.

For wide tables, generate the per-column SQL from the information schema rather than hand-writing dozens of blocks — see Schema Discovery below.

## Numeric Columns

```sql
SELECT
  MIN(m) AS min_val,
  MAX(m) AS max_val,
  AVG(m) AS mean_val,
  STDDEV(m) AS sd,
  APPROX_QUANTILES(m, 100)[OFFSET(1)]  AS p1,
  APPROX_QUANTILES(m, 100)[OFFSET(25)] AS p25,
  APPROX_QUANTILES(m, 100)[OFFSET(50)] AS median,
  APPROX_QUANTILES(m, 100)[OFFSET(75)] AS p75,
  APPROX_QUANTILES(m, 100)[OFFSET(99)] AS p99,
  COUNTIF(m = 0)  AS zeros,
  COUNTIF(m < 0)  AS negatives
FROM table;
```

Dialect swaps: PostgreSQL uses `PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY m)`; Snowflake uses `APPROX_PERCENTILE(m, 0.5)`; `COUNTIF(x)` becomes `SUM(CASE WHEN x THEN 1 ELSE 0 END)` where unsupported.

Read the shape from mean versus median: mean far above median means a right tail; mean equal to median with a large standard deviation suggests bimodality worth a histogram. A histogram in fixed-width buckets settles it:

```sql
SELECT FLOOR(m / 100) * 100 AS bucket, COUNT(*) AS freq
FROM table GROUP BY bucket ORDER BY bucket;
```

## String Columns

```sql
SELECT
  MIN(LENGTH(s)) AS min_len,
  MAX(LENGTH(s)) AS max_len,
  AVG(LENGTH(s)) AS avg_len,
  COUNTIF(s = '')                        AS empty_strings,
  COUNTIF(s <> TRIM(s))                  AS padded_values,
  COUNTIF(s = LOWER(s)) AS all_lower,
  COUNTIF(s = UPPER(s)) AS all_upper
FROM table;
```

Empty string and null are different states and often mean different things — count both and say which the column uses.

Format consistency by pattern collapse — replace digits with `9` and letters with `A`, then count the resulting shapes. Few shapes means a structured field; many means free text:

```sql
SELECT REGEXP_REPLACE(REGEXP_REPLACE(s, r'[0-9]', '9'), r'[A-Za-z]', 'A') AS shape,
       COUNT(*) AS freq
FROM table GROUP BY shape ORDER BY freq DESC LIMIT 20;
```

Case-variant duplicates hide category counts — `COUNT(DISTINCT s)` versus `COUNT(DISTINCT LOWER(TRIM(s)))` differing means the same category exists under multiple spellings.

## Date And Timestamp Columns

```sql
SELECT
  MIN(d) AS earliest,
  MAX(d) AS latest,
  COUNTIF(d IS NULL)          AS null_dates,
  COUNTIF(d > CURRENT_DATE()) AS future_dates,
  COUNT(DISTINCT DATE_TRUNC(d, MONTH)) AS months_covered
FROM table;

-- Volume by period; a gap or a cliff at the end signals a broken load
SELECT DATE_TRUNC(d, DAY) AS day, COUNT(*) AS rows
FROM table GROUP BY day ORDER BY day DESC LIMIT 60;
```

Find true gaps by joining against a generated calendar rather than eyeballing the series:

```sql
WITH cal AS (SELECT day FROM UNNEST(GENERATE_DATE_ARRAY('2023-01-01', CURRENT_DATE())) AS day)
SELECT cal.day
FROM cal LEFT JOIN (SELECT DISTINCT DATE(d) AS day FROM table) t USING (day)
WHERE t.day IS NULL
ORDER BY cal.day;
```

Check timezone before reading any date statistic: a UTC-stored timestamp reported in local time shifts day boundaries and can invent an empty first or last day.

## Cross-Column Checks

```sql
-- Rule violation count: state implies timestamp
SELECT COUNTIF(status = 'completed' AND completed_at IS NULL) AS violations FROM table;

-- Join key match rate against a suspected parent
SELECT
  COUNT(*)                                AS child_rows,
  COUNTIF(p.id IS NULL)                   AS unmatched,
  ROUND(1.0 * COUNTIF(p.id IS NULL) / COUNT(*), 4) AS orphan_rate
FROM child c LEFT JOIN parent p ON c.parent_id = p.id;

-- Functional dependency: does a determine b? Any group above 1 breaks it.
SELECT a, COUNT(DISTINCT b) AS b_values
FROM table GROUP BY a HAVING COUNT(DISTINCT b) > 1 LIMIT 20;
```

## Pandas Equivalents

```python
import pandas as pd

df = pd.read_csv(path)          # low_memory=False when dtype warnings appear
df.info(memory_usage="deep")    # shape, dtypes, non-null counts, real memory

# Universal per-column frame
profile = pd.DataFrame({
    "dtype": df.dtypes.astype(str),
    "nulls": df.isna().sum(),
    "null_rate": df.isna().mean().round(4),
    "distinct": df.nunique(dropna=True),
    "cardinality_ratio": (df.nunique() / df.notna().sum()).round(4),
})

df.describe(include="number").T          # numeric summary
df.describe(include="object").T          # top value, frequency, distinct
df["col"].value_counts(dropna=False).head(10)
df["col"].value_counts().tail(10)        # rare tail: placeholders live here

# Key uniqueness
len(df) == df["candidate_key"].nunique()
df[df.duplicated("candidate_key", keep=False)].sort_values("candidate_key")

# String hygiene
s = df["col"].dropna().astype(str)
(s != s.str.strip()).sum()               # padded values
s.str.lower().nunique() < s.nunique()    # case-variant duplicates

# Correlation among metrics
df.select_dtypes("number").corr(numeric_only=True)
```

Read dates with `parse_dates=[...]` rather than letting them stay object dtype — every temporal statistic is wrong until the column is a real datetime.

For files that do not fit in memory, chunk and aggregate: `pd.read_csv(path, chunksize=500_000)`, accumulating counts per chunk. Parquet is cheaper still — read only the columns being profiled via `pd.read_parquet(path, columns=[...])`.

## Schema Discovery

```sql
-- PostgreSQL / most engines: tables in a schema
SELECT table_name, table_type
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;

-- Column inventory with declared types and nullability
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'my_table'
ORDER BY ordinal_position;

-- PostgreSQL: physical size, largest first
SELECT relname, pg_size_pretty(pg_total_relation_size(relid)) AS size
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC
LIMIT 20;

-- BigQuery: rows and bytes without scanning the table
SELECT table_id, row_count, size_bytes
FROM `project.dataset.__TABLES__`
ORDER BY size_bytes DESC;

-- Snowflake: same, from the account metadata
SELECT table_name, row_count, bytes
FROM information_schema.tables
WHERE table_schema = 'PUBLIC'
ORDER BY bytes DESC;
```

Metadata row counts are maintained by the engine and can lag recent loads. When the number matters, confirm with `COUNT(*)` and say which source it came from.

Declared nullability is a constraint, not evidence — a `NOT NULL` column can still be 90% empty strings.

## Lineage Orientation

When the dataset is one table in an unfamiliar environment, work backward from consumption:

1. Start at the tables that dashboards and reports read.
2. Trace upstream to their sources; view definitions and dbt models name their inputs directly.
3. Separate the layers you find — raw, staging, mart — since quality expectations differ by layer.
4. Mark where each transformation filters, enriches, deduplicates, or aggregates.
5. Note which layer the profiled table sits in: defects in a mart usually originate upstream, and profiling the mart alone will not locate them.
