# Data Reconciliation

Load when you must prove that migrated data equals the source, find the differences, and repair them. Use it for the verify phase of any plan from `scripts/migration_planner.py`. Pair with `zero-downtime-techniques.md` for the methods that create the data.

## Contents

1. [What reconciliation proves](#1-what-reconciliation-proves)
2. [Kinds of difference](#2-kinds-of-difference)
3. [Detection ladder](#3-detection-ladder)
4. [Handling a moving source](#4-handling-a-moving-source)
5. [Repair](#5-repair)
6. [Scheduling and exit criteria](#6-scheduling-and-exit-criteria)
7. [Metrics and alerts](#7-metrics-and-alerts)
8. [Scale](#8-scale)

## 1. What reconciliation proves

Reconciliation answers one question: for every record the business cares about, do source and target agree? It does not prove the target is correct. It proves the target equals a source you already trust.

Four rules:

1. **Read-only first.** Detection never changes data. Repair is a separate, logged step.
2. **Repeatable.** Run the same check twice and get the same answer on unchanged data.
3. **Idempotent repair.** Applying a repair twice leaves the same state.
4. **Evidence kept.** Store every run's inputs, counts, and diffs. An audit asks for them months later.

## 2. Kinds of difference

| Kind | Example | Usual cause | Repair |
|---|---|---|---|
| Missing in target | Row exists in source only. | Failed secondary write, backfill gap, filter bug. | Upsert from source. |
| Extra in target | Row exists in target only. | Missed delete, test data, duplicate key mapping. | Review, then delete or keep by rule. |
| Field mismatch | Same key, different value. | Type conversion, rounding, encoding, truncation, timezone. | Fix the transform, then re-copy. |
| Orphan | Child row has no parent. | Load order, partial copy, deferred constraint. | Copy the parent, or remove the child by rule. |
| Temporal | Target is older than source. | Lag, lost update, out-of-order replay. | Re-sync by version. |
| Drift | Schema or enum differs. | Release changed one side only. | Align the schema, then compare again. |

Fix the cause, not only the rows. A repair loop that runs forever hides a defect in the writer.

## 3. Detection ladder

Climb from cheap to costly. Stop at the first rung that gives the confidence the table's risk needs. Critical tables go to the top.

| Rung | Check | Cost | Catches | Misses |
|---|---|---|---|---|
| 1 | Row counts | Very low | Large gaps, failed loads. | Offsetting extra and missing rows. Any field error. |
| 2 | Aggregates per column (sum, min, max, null count, distinct count) | Low | Truncation, rounding, null mapping. | Swapped values with equal totals. |
| 3 | Per-range checksums | Medium | Any field change inside a key range. | Which row differs. |
| 4 | Keyed delta (anti-join) | High | The exact missing, extra, and changed rows. | Nothing the keys cover. |
| 5 | Business-query comparison | Medium | Wrong derived results, broken joins, semantic errors. | Rows no query touches. |

### Rung 1 and 2: counts and aggregates

Compare under the same filter on both sides. Account for soft deletes, archived partitions, and rows written after the snapshot.

```sql
-- run on both sides, diff the output
SELECT count(*) AS n,
       count(email) AS non_null_email,
       count(DISTINCT customer_id) AS customers,
       sum(total_cents) AS total_cents,
       min(created_at) AS first_at, max(created_at) AS last_at
FROM orders
WHERE created_at < :cutoff;   -- the same fixed cutoff on both sides
```

Set a tolerance only where the business accepts one (for example, a session table). Use zero for money and identity data.

### Rung 3: range checksums

Hash each key range on both sides, then compare hashes. Drill into only the ranges that differ. This turns a billion-row compare into a few thousand hash compares.

```sql
-- PostgreSQL: one hash per 100k-id bucket
SELECT id / 100000 AS bucket,
       count(*) AS n,
       md5(string_agg(id::text || '|' || coalesce(email, '') || '|' || total_cents::text,
                      ',' ORDER BY id)) AS digest
FROM orders GROUP BY 1 ORDER BY 1;
```

Rules for a hash that compares across engines:

- Normalize before hashing: trim, a fixed text encoding (UTF-8), a fixed timestamp format in UTC, a fixed decimal scale, one representation of NULL (`''` and NULL must not collide, so write a marker such as `\N`).
- Hash only the columns the target owns and should equal. Exclude columns that legitimately differ (surrogate ids, `migrated_at`).
- Use an order-independent combine only if row order can differ. Prefer an ordered `string_agg` by key.
- Use a strong digest (SHA-256) for audit evidence. MD5 is fine for drift detection inside the team.

When a range differs, split it in half and compare again until the range holds a few hundred rows, then run rung 4 on that range.

### Rung 4: keyed delta

```sql
-- missing in target / extra in target / changed; run per differing range
SELECT 'missing_in_target' AS issue, s.id
FROM src.orders s LEFT JOIN tgt.orders t USING (id)
WHERE t.id IS NULL AND s.id BETWEEN :lo AND :hi
UNION ALL
SELECT 'extra_in_target', t.id
FROM tgt.orders t LEFT JOIN src.orders s USING (id)
WHERE s.id IS NULL AND t.id BETWEEN :lo AND :hi
UNION ALL
SELECT 'field_mismatch', s.id
FROM src.orders s JOIN tgt.orders t USING (id)
WHERE s.id BETWEEN :lo AND :hi
  AND (s.email IS DISTINCT FROM t.email OR s.total_cents <> t.total_cents);
```

Use `IS DISTINCT FROM` so NULL compares correctly. Across two servers, pull both sides into a scratch schema first. A cross-server anti-join over the network is slow and fragile.

### Rung 5: business queries

Pick 10 to 20 queries the business already trusts. Run each on both sides and compare results.

- Revenue by day and by product for the last 90 days.
- Active accounts by plan.
- Open balance per customer for the top 1,000 customers.
- A join across the tables that changed shape (for example, orders to addresses).
- Edge sets: oldest accounts, largest accounts, rows with NULL in migrated columns, rows with non-ASCII text.

This rung finds errors that row compare cannot: a join that fans out, a status mapped to the wrong code, or a currency stored in the wrong unit.

## 4. Handling a moving source

If the source changes during the check, a naive compare reports false differences. Use one of these.

| Technique | How | Use when |
|---|---|---|
| Fixed cutoff | Compare only rows with `updated_at < cutoff`, where the cutoff is older than the max replication lag. | Rows carry a reliable timestamp. |
| Version compare | Compare `version` or `updated_at` per key. Report a lag difference only if target is older by more than the lag budget. | Rows are updated in place. |
| Snapshot read | Read both sides from a consistent snapshot or replica at a known log position. | The engine supports it. |
| Quiesced window | Pause writers briefly and compare. | Last check before cutover. |
| Recheck | Re-test every reported difference after a delay. Only report a difference that persists. | Always, as a filter on any other technique. |

A difference that shrinks between runs is lag. A difference that persists or grows is a defect.

## 5. Repair

### Policy

| Class | Action |
|---|---|
| Missing in target, clear source row | Automatic upsert from source. |
| Field mismatch with a known transform bug | Fix the transform. Re-copy the affected range. |
| Extra in target | Manual review. Delete only by an approved rule. |
| Orphans | Repair the parent first. Then re-run the child check. |
| Anything touching money, identity, or regulated data | Manual review with two approvers. |

### Safe repair job

```python
def repair(keys, source, target, audit):
    for batch in chunks(keys, 500):
        rows = source.fetch(batch)                       # source is the authority
        with target.transaction():
            for row in rows:
                before = target.get(row.id)
                if before is not None and before.version > row.version:
                    audit.log("skip_newer_target", row.id)   # never overwrite newer data
                    continue
                target.upsert(row)
                audit.log("repaired", row.id, before=before, after=row)
        throttle()
```

Properties to keep:
- **Source wins** unless the target row is newer by version.
- **Idempotent**: an upsert by key. A rerun changes nothing.
- **Audited**: every change records before and after.
- **Bounded**: a cap on rows per run. A cap that trips means a defect, so stop and look.
- **Dry run**: print what would change before the first live run.

### Review queue

Write each unresolved difference with: table, key, both values, first seen, last seen, suspected cause, owner, decision. Review daily during the verify phase. A decision is one of `repair`, `accept` (with reason and approver), or `defect` (with ticket).

## 6. Scheduling and exit criteria

| Stage | Cadence | Scope |
|---|---|---|
| During backfill | After each table | Counts and aggregates. |
| Dual-write soak | Hourly | Counts, aggregates, sampled keyed delta on recent rows. |
| Verify window | Daily | Full ladder on critical tables. Rungs 1-3 elsewhere. Business queries. |
| Just before cutover | Once, in a quiesced window or at lag zero | Full keyed delta on critical tables. |
| After cutover | Daily until contract | Rungs 1-3 plus business queries. |

Exit criteria for the verify phase (put them in the plan before you start):

- Critical tables: zero unexplained differences for N consecutive daily runs (pick N of at least 3).
- Other tables: differences below the tolerance the owner signed.
- Every accepted difference has a reason and an approver.
- Review queue is empty.
- Repair job has not needed to run in the last N runs.

Do not move readers while a critical table has an open difference.

## 7. Metrics and alerts

| Metric | Alert |
|---|---|
| Difference count per table per run | Critical table above 0. Others above tolerance. |
| Difference trend across runs | Not falling for 3 runs. |
| Repair queue depth and oldest age | Age above the soak limit. |
| Replication or dual-write lag | Above the lag budget. |
| Run duration | Above 2x the previous run, or the run misses its window. |
| Run did not execute | Any missed schedule. A silent check is a failed check. |

Report per run: start, end, snapshot or cutoff used, rung reached, counts by difference kind, repairs applied, items in review, and the pass or fail verdict against the exit criteria. Keep each report. It is the evidence behind the cutover decision.

## 8. Scale

- **Partition the work** by key range or hash bucket. Run ranges in parallel, with a cap that protects the source.
- **Use replicas** for reads. Do not run a full compare on the primary.
- **Compare incrementally**: after the first full pass, check only ranges changed since the last pass (use change timestamps, or the CDC stream's changed keys).
- **Sample for non-critical tables**: a random sample of N keys (a few thousand) finds a defect rate above roughly 0.1% with high confidence. A sample cannot prove zero. Use full compare where zero is the requirement.
- **Push work to the database**: hash and aggregate in SQL on each side, and move only digests across the network.
- **Time-box**: a compare that cannot finish inside the window needs a smaller range or a replica, not a longer window.

### Sample size check

If the true defect rate is `p`, a random sample of `n` keys misses every defect with probability `(1 - p)^n`. For `p = 0.1%` and `n = 3000`, the miss chance is about 5%. State this limit in the report whenever you sample.
