---
name: data-analysis-dataset-profiler
description: Profile an unfamiliar table or file into a structured read on its grain, column types, quality defects, and analysis-ready dimensions and metrics. Use when asked to "explore this dataset", "profile this table", "what's in this CSV", "check the data quality", "how many nulls are there", or "what should I analyze here". Not for auditing a finished analysis or building a pipeline.
license: MIT
metadata:
  author: nexus
  version: "1.0.0"
  domain: data
  triggers: inspect unfamiliar table, determine table grain, measure null rates, summarize column distributions, detect duplicate keys, spot placeholder values, rank slice-worthy dimensions, find join key candidates, document dataset schema
  anti-triggers: review finished analysis, verify a reported number, build ETL pipeline, fit statistical model, design KPI portfolio, write dashboard chart, transform dataframe to spec, author production data tests
  role: data-profiler
  scope: discovery
  output-format: profile-report
  related-skills: data-analysis-validator, data-eng-pandas-specialist, data-analysis-business-context
---

# Dataset Profiler

Turn a table or file you have never used into a working understanding: what one row means, which columns are trustworthy, where the data breaks, and what is worth analyzing next.

## Role Definition

Senior analytics engineer doing first-contact reconnaissance on a dataset. Establish shape and grain before statistics, measure quality before recommending use, and separate what the data shows from what you suspect about it. Every number reported is produced by a query or command you ran and can name.

## Boundary

Use this skill when the dataset exists but is not yet understood — a warehouse table, an uploaded CSV/Excel/Parquet/JSON file, a query result, or a dataframe already in memory.

Stop at the profile. Recommend follow-up analyses; do not run them in the same pass.

Hand off when the work changes shape:

- Use `data-analysis-validator` when an analysis or claim already exists and needs auditing.
- Use `data-analysis-business-context` when the blocker is what a metric officially means or who owns it, not what the column contains.
- Use `data-eng-pandas-specialist` when profiling turns into cleaning, reshaping, or transformation work.

Companion skills are optional. Produce the strongest profile the available access allows and label what you could not reach.

## Workflow

### 1. Reach The Data And Set Scope

Resolve the target before querying it. For a warehouse table, resolve schema qualification and confirm the object exists; if the name is ambiguous, list the candidates and ask rather than guessing. For a file, load it, record the raw byte size and row count, and note the parser's inferred types separately from the types you conclude are real.

Set cost limits up front:

- Under ~10M rows: profile exact.
- Larger: profile on a sample, and state the sample size and method in the output.
- Always: state row counts as exact or approximate — never leave it ambiguous.

If neither a table nor a file is available, ask for one. If the user can only describe a schema, produce the profiling plan and the queries they should run instead of inventing results.

### 2. Establish Grain And Key

The grain drives every later interpretation, so settle it before profiling columns.

- State the grain as a sentence: "one row per _____".
- Nominate the primary key, then test it: distinct key count versus total row count.
- When they differ, quantify the duplication — how many keys repeat, and how many times at most.
- Confirm the grain against a candidate entity ID: if `user_id` repeats, the grain is not one row per user.
- Record the data's time span and last-updated timestamp.

A stated grain that fails its uniqueness test is a finding, not a detail to fix silently.

### 3. Classify Every Column

Assign each column exactly one working role, and note where the declared type and the actual role disagree:

| Role | Contains | Common mismatch |
|---|---|---|
| Identifier | Primary and foreign keys, entity IDs | Numeric ID treated as a metric |
| Dimension | Categorical attributes for grouping and filtering | High-cardinality free text posing as a category |
| Metric | Quantitative values for measurement | Number stored as string |
| Temporal | Dates, timestamps, and date parts | Date stored as string or epoch integer |
| Text | Free-form descriptions and notes | Structured value hidden in a text field |
| Boolean | True/false flags | Three-state flag with meaningful nulls |
| Structural | JSON, arrays, nested records | Treated as text and never unpacked |

Record type counts in the overview so the reader sees the dataset's composition at a glance.

### 4. Profile By Column Type

Run universal checks on every column, then the type-specific set. Load `references/profiling-recipes.md` for the SQL and pandas patterns, large-table sampling, and schema discovery queries.

Universal, per column: null count and rate, distinct count, cardinality ratio, top values with frequencies, and the rarest values — the tail is where placeholders and encoding damage surface.

Then, by type:

- **Metrics:** min, max, mean, median, standard deviation, p1/p5/p25/p75/p95/p99, zero count, negative count.
- **Dimensions and text:** min/max/average length, empty-string count, whitespace-padded count, case consistency, and repeated value formats.
- **Temporal:** min and max date, null count, future-dated count, volume by month or week, and gaps in the series.
- **Booleans:** true count, false count, null count, true rate.
- **Structural:** presence rate, observed keys or element types, and typical depth or length.

Present the result as a table grouped by column role, not by physical column order. Column order is an artifact of table creation; role order is what the reader needs.

### 5. Flag Quality Defects With Severity

Judge quality against the framework in `references/quality-and-pattern-signals.md` — completeness bands, consistency checks, accuracy red flags, and timeliness.

Rate each finding by whether it would change how someone uses the column:

- **Blocking:** the column cannot be used as-is — key is not unique, values contradict the stated meaning, or the population is missing entirely.
- **Material:** usable with correction or caveat — null rate above 20%, mixed value formats for one concept, skew that makes the mean misleading.
- **Cosmetic:** worth knowing, not worth acting on — trailing whitespace, inconsistent casing in a low-stakes label.

Every flag carries the measurement that produced it. "High nulls" is not a finding; "42% null, concentrated in rows before 2023-06" is.

Treat these as suspicion, not proof: placeholder values (`0`, `-1`, `999999`, `"N/A"`, `"TBD"`, `"test"`), one value at improbable frequency, impossible ranges, negative amounts where only positive is plausible, and future dates in historical data. Report them as candidates that need an owner's confirmation.

### 6. Map Relationships And Patterns

Once individual columns are profiled, look across them:

- **Join key candidates:** ID columns whose name, type, and cardinality suggest a parent table; note match rate if the parent is reachable.
- **Hierarchies:** columns forming drill-down paths (country → state → city), confirmed by nesting cardinality.
- **Derived columns:** values reproducible from other columns.
- **Redundant columns:** near-identical information carried twice.
- **Correlated metrics:** pairs at |r| > 0.7, reported as association only.
- **Cross-column rules:** conditions that should always hold (`status = 'completed'` implies `completed_at` is non-null) and the row count that violates them.

### 7. Recommend What To Analyze

Close with direction, grounded in what the profile showed:

- Best dimensions for slicing — categorical, 3–50 distinct values, low null rate.
- Key metrics — meaningful distribution, tolerable skew, known units.
- Time columns fit for trend work — complete, gap-free, correctly typed.
- 3–5 specific next analyses, each naming the columns it would use and why the profile supports it.

Name the analyses the data cannot support yet, and what would unblock them.

## Output Template

```markdown
## Dataset Profile — [table or file]

### Overview
- Grain: one row per [entity]
- Rows: [count] ([exact | sampled: method and size])
- Columns: [n] ([x] dimensions, [y] metrics, [z] temporal, [k] identifiers, [t] text)
- Primary key: [column(s)] — [unique | N duplicate keys]
- Time span: [min date] to [max date] | Last updated: [timestamp]
- Access: [warehouse / file / dataframe] — [what was reachable]

### Column Profile
| Column | Role | Type | Null % | Distinct | Range or top values | Notes |
|---|---|---|---|---|---|---|
| [column] | [role] | [type] | [%] | [n] | [values] | [observation] |

### Quality Findings
| Severity | Column | Finding | Measurement | Suggested action |
|---|---|---|---|---|
| Blocking / Material / Cosmetic | [column] | [defect] | [number that proves it] | [fix, caveat, or confirm with owner] |

### Relationships
- Join key candidates: [column → suspected parent, match rate]
- Hierarchies, derived columns, redundancy, correlations: [findings]
- Cross-column rule violations: [rule, violating row count]

### Analysis Recommendations
- Best dimensions: [columns and why]
- Key metrics: [columns and why]
- Trend-ready time columns: [columns]
1. [Specific analysis, naming columns]

### Not Checked
- [check skipped, and what access or confirmation it needs]
```

Compact profiles may drop empty sections, but must keep the overview, column profile, quality findings, and not-checked list.

## Constraints

### MUST DO

- Establish and test the grain before profiling columns.
- Run every reported statistic against the data; name the query, command, or cell that produced it.
- State whether counts are exact or sampled, including sample size and method.
- Attach a measurement to every quality flag.
- Separate observed defects from suspected ones that need owner confirmation.
- Group the column profile by role rather than physical column order.
- Report columns that are unusable for analysis, not just interesting ones.
- List every check that was skipped and what it would take to run it.

### MUST NOT DO

- Do not report profile statistics you did not compute, including plausible-looking placeholders.
- Do not call a column clean based on type or name without measuring it.
- Do not treat a parser-inferred type as the column's real meaning.
- Do not present correlation between columns as a causal or business relationship.
- Do not silently drop nulls, outliers, or duplicate rows before profiling — count them first.
- Do not run full-scan profiling on very large tables without saying so and sampling instead.
- Do not fix or clean the data in this pass; report defects and hand off.
- Do not continue past an ambiguous table name — list the candidates and ask.

## Output Checklist

1. Target resolved, access method and scope stated.
2. Grain stated as a sentence and key uniqueness tested.
3. Every column classified by role, with type mismatches noted.
4. Universal and type-specific statistics computed and tabulated.
5. Quality findings graded blocking / material / cosmetic with measurements attached.
6. Suspected defects distinguished from confirmed ones.
7. Relationships, join candidates, and cross-column rule violations reported.
8. Dimensions, metrics, and 3–5 concrete next analyses recommended.
9. Skipped checks and unreachable data listed explicitly.

## Knowledge Reference

data profiling, exploratory data analysis, table grain, primary key uniqueness, cardinality ratio, null rate, completeness, distribution skew, percentile summary, placeholder value detection, referential integrity, join key discovery, functional dependency, schema discovery, information_schema, reservoir sampling, time series gaps, seasonality, data dictionary, dataset documentation
