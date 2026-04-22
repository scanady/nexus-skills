# Data Pipeline Architecture

Reference guide for choosing + designing pipeline architecture patterns.

---

## Architecture Patterns

### Batch (ETL / ELT)

Run on schedule. Load full or incremental snapshots.

**When:** Latency > 1 hour acceptable. Source can be queried in bulk. Simpler ops.

**ELT preferred** over ETL when target warehouse has compute (Snowflake, BigQuery, Databricks):
load raw → transform in SQL via dbt.

Incremental load strategies:
- `WHERE updated_at > last_run_watermark` — simple, requires reliable updated_at
- CDC (see below) — reliable even without updated_at column
- Full replace on small dimensions — simplest; safe for tables < 1M rows

### Lambda Architecture

Separate batch layer (high accuracy, high latency) + speed layer (low latency, eventual correction).
Batch layer periodically overwrites speed layer results.

**When:** Need real-time approximate counts + periodic accurate recomputation (e.g., dashboards).

**Cons:** Two codepaths to maintain. Prefer Kappa if streaming infra already in place.

### Kappa Architecture

Single streaming layer for all data. Replay from durable log (Kafka) to recompute.

**When:** Event-driven source. Latency SLA < 5 min. Kafka or Kinesis already in stack.

**Cons:** Streaming infra cost. Harder backfill + debugging than batch. Overkill for daily analytics.

### Medallion / Lakehouse (Bronze → Silver → Gold)

Three-layer storage model:

| Layer | Content | Quality | Format |
|-------|---------|---------|--------|
| Bronze | Raw ingest, no transformation | None | As-is (JSON, CSV, Parquet) |
| Silver | Cleaned, typed, deduplicated | Schema enforced, nulls handled | Parquet / Delta / Iceberg |
| Gold | Business-ready aggregations, joins | Quality SLA met | Parquet / Delta |

Bronze: never delete, never transform — preserve source fidelity.
Silver: apply schema, cast types, filter invalid rows, deduplicate on natural key.
Gold: aggregate, join dims, compute business metrics — query-optimized for consumers.

---

## Change Data Capture (CDC)

Capture row-level inserts/updates/deletes from source DB without full table scans.

**Approaches:**

| Method | How | Latency | Source Impact |
|--------|-----|---------|--------------|
| Log-based CDC | Read DB transaction log (Debezium, AWS DMS) | Seconds | Minimal |
| Query-based CDC | Poll `WHERE updated_at > watermark` | Minutes | Read load on source |
| Trigger-based CDC | DB triggers write to audit table | Seconds | Write overhead |

Log-based CDC preferred for production. Requires source DB with binlog/WAL enabled.

**Target handling for CDC events:**
- Insert → INSERT if key not exists
- Update → UPDATE by natural key
- Delete → soft delete (set `is_deleted = true`) or hard delete by key

Use MERGE (UPSERT) in warehouse for CDC targets. Avoid separate INSERT + DELETE passes.

---

## Idempotency

Every pipeline must produce identical output when run multiple times on same input.

Techniques:
- **Write-replace:** overwrite target partition instead of appending (`INSERT OVERWRITE PARTITION`)
- **MERGE / UPSERT:** match on natural key, update or insert — safe to re-run
- **Dedup on load:** apply `ROW_NUMBER() OVER (PARTITION BY key ORDER BY updated_at DESC)` at Silver
- **Watermark tracking:** store last successful run watermark; re-run from same watermark on failure

Never use append-only without dedup logic — re-runs create duplicates.

---

## Partitioning Strategy

| Table type | Partition key | Rationale |
|------------|--------------|-----------|
| Event / fact | Date (`event_date`) | Prune by time range in queries |
| Large dimension | Hashed key bucket | Even distribution, fast lookup |
| CDC target | Natural key range | Fast MERGE scan |
| Aggregated gold | Date + entity key | Serves dashboards efficiently |

Over-partitioning (too many small files) is as bad as under-partitioning. Target 100MB–1GB per partition file after compaction.

Run compaction (OPTIMIZE / VACUUM) on Delta/Iceberg tables weekly.

---

## Failure Recovery + Backfill

Design before first deployment:

**Checkpointing:** Record last successful partition/watermark in a state table. Resume from last checkpoint on failure — don't re-run from beginning.

**Backfill approach by pattern:**

| Pattern | Backfill method |
|---------|----------------|
| Batch incremental | Re-run with `start_date` / `end_date` parameters |
| CDC | Replay Kafka topic from offset or re-snapshot source |
| Streaming | Replay from Kafka offset or S3 raw archive (Bronze) |
| Full replace | Re-run from scratch — no backfill needed |

Always test backfill before production. Backfill should produce same result as forward run.

---

## Storage Formats

| Format | Use when |
|--------|---------|
| Parquet | Default. Columnar, splittable, good compression. |
| Delta Lake | Need ACID, time-travel, MERGE, schema evolution on Databricks/Spark. |
| Apache Iceberg | Multi-engine ACID (Spark + Trino + Flink). Cloud-native lakehouse. |
| Avro | Row-based, schema evolution, good for Kafka serialization. |
| ORC | Hive-optimized; prefer Parquet unless Hive-native ecosystem. |

---

## Observability Hooks

Instrument every pipeline at these points:

- **Row count** logged at each stage (extract count, load count — compare for data loss)
- **Duration** per stage (detect slow stages early)
- **Watermark** recorded after success (enables resume + audit)
- **Error + retry** events emitted to monitoring (PagerDuty / Slack alert on failure)
- **Schema change** detection at Bronze ingestion (alert before Silver breaks)
