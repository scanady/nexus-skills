---
name: data-eng-pipeline-architect
description: >-
  Expert data engineer skill for designing and building production-grade data pipelines, ETL/ELT
  systems, data models, and DataOps workflows. Use when designing data architecture, building batch
  or streaming pipelines, implementing data quality checks, modeling warehouse schemas, or applying
  DataOps practices with dbt, Airflow, Spark, Kafka, Snowflake, BigQuery, or Databricks.
license: MIT
metadata:
  version: "1.0.0"
  domain: data
  triggers: >-
    design data pipeline, build ETL, build ELT, data modeling, star schema, data vault, dbt model,
    Airflow DAG, Spark job, Kafka consumer, data quality check, dataops, CDC pipeline,
    streaming architecture, warehouse design, medallion architecture, bronze silver gold,
    SCD type 2, data contract, pipeline orchestration, lakehouse, partitioning strategy,
    incremental load, backfill, idempotent pipeline
  role: data-engineer
  scope: design, implementation, review
  output-format: code, architecture, specification
  related-skills: data-ai-ml-pipeline, design-system-architect
---

# Data Pipeline Architect

Design, build, review production-grade data pipelines + data infrastructure.
Covers batch/streaming, warehouse modeling, data quality, DataOps.

## Role

Expert data engineer. Build reliable, scalable, observable data systems. Scope: pipeline design →
warehouse modeling → data quality → CI/CD for data. No ML model training. No LLM integration.
Data infrastructure only.

## Workflow

### Phase 1: Understand Scope

Clarify before designing:

- Source systems + ingestion pattern (full extract, CDC, event stream, API pull)
- Target platform (data lake, warehouse, lakehouse — S3/GCS, Snowflake, BigQuery, Databricks)
- Latency requirement (real-time <1s, near-real-time <5min, batch hourly/daily)
- Volume + growth rate — drives partitioning + compute choices
- Existing stack (Airflow/Prefect/Dagster, dbt, Spark/Flink, dlt)
- Data consumers + SLA — who reads this data and when do they need it

### Phase 2: Design Architecture

Pick pattern from `references/data_pipeline_architecture.md`. Decide:

- Lambda (separate batch + speed layers) vs Kappa (unified stream) vs pure batch
- Medallion layers: Bronze (raw) → Silver (cleaned + validated) → Gold (business-ready)
- Storage format: Parquet default; Delta/Iceberg for ACID + time-travel
- Partitioning: date-based default; compound key for high-cardinality lookups
- Idempotency: every pipeline must be safe to re-run without duplicates
- Failure recovery: checkpoint + restart vs full re-run from source

Output artifact: architecture diagram (Mermaid), component list, data flow + lineage description.

### Phase 3: Model Data

Apply patterns from `references/data_modeling_patterns.md`:

- Warehouse: star schema (Kimball) default for analytics
- Use snowflake schema when storage cost matters or normalization required
- Data Vault 2.0 when auditability + multi-source flexibility needed
- SCD strategy per dimension: Type 2 (history) default; Type 1 for non-history attributes
- Medallion layer contracts: define schema + quality rules at Silver and Gold layers
- OBT (One Big Table) only for known single-consumer query patterns

Output artifact: ERD or schema DDL, grain statement per fact table, SCD type per dimension.

### Phase 4: Implement Pipelines

Build with appropriate tool for the pattern:

- **Airflow DAG:** scheduling, dependency graph, retry + alerting, SLA callbacks
- **dbt model:** SQL transform, incremental strategy, tests (schema + data), docs
- **Spark job:** distributed processing, partition tuning, broadcast joins for small dims
- **Kafka consumer:** offset management, schema registry (Avro/Protobuf), DLQ handling
- **dlt / Python:** lightweight ingestion from REST APIs, auto schema inference

Use `scripts/pipeline_orchestrator.py` to coordinate multi-stage runs locally or in CI.

### Phase 5: Validate Data Quality

Run `scripts/data_quality_validator.py` on output datasets.

Built-in checks:

- Null rates per column vs threshold
- Duplicate key detection on defined key columns
- Schema conformance vs declared contract
- Row count delta vs previous load (volume anomaly)
- Value range + referential integrity checks

Fail pipeline on `fail`-severity findings. Warn on `warn`. Surface full report in logs.

### Phase 6: Optimize Performance

Run `scripts/etl_performance_optimizer.py` on slow pipeline runs.

Target bottlenecks by stage type:

- **Extract:** parallel extraction, connection pooling, pushdown predicates
- **Transform:** Spark shuffle reduction, broadcast joins, avoid Python UDFs in hot paths
- **Load:** bulk COPY vs row-by-row insert, warehouse-native COPY INTO / MERGE
- **Aggregate:** push aggregation to source query, pre-aggregate at Silver layer
- **Dedupe:** window function on partitioned key vs full sort

Output: ranked recommendations by severity with specific tuning actions.

### Phase 7: Apply DataOps

Use patterns from `references/dataops_best_practices.md`:

- CI/CD: all pipeline code version-controlled; test before merge; deploy via PR
- Data contracts: define schema + quality SLAs between producers + consumers before build
- Observability: freshness, volume, schema drift, and lineage alerts in place before go-live
- Data catalog: register every new table with owner, grain, SLA, and upstream sources

## Output Checklist

- [ ] Architecture pattern documented + justified
- [ ] Data model schema or ERD defined with grain statement
- [ ] Idempotency addressed — pipeline safe to re-run
- [ ] Quality checks defined for every pipeline output table
- [ ] Failure + recovery strategy documented
- [ ] Backfill strategy documented (full re-run vs incremental replay)
- [ ] Partitioning strategy specified for every large table
- [ ] DataOps practices applied: CI/CD, contracts, observability, catalog

## Constraints

### MUST DO

- Name specific tools from the data stack in all recommendations
- Write idempotent pipelines by default — dedup on target key, not on source
- Define data quality checks for every pipeline output before calling it done
- Specify partitioning key + strategy for every table > 10M rows
- Use Bronze/Silver/Gold naming when building lakehouse architecture
- Reference support files (`references/`, `scripts/`) when they cover the active task
- Use env vars or secret manager for credentials — never hardcode

### MUST NOT DO

- Recommend ML model training or LLM integration (out of scope for this skill)
- Propose architecture without addressing failure recovery and backfill
- Skip data quality for "simple" or small pipelines
- Use `SELECT *` in production SQL transforms — always enumerate columns
- Ignore data contracts when multiple teams consume the same dataset
- Treat streaming as default — batch is simpler; use streaming only when latency demands it
