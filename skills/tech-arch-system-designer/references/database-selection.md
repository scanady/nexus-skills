# Database Selection

## Type Decision Table

| Type | Examples | Pick When |
|---|---|---|
| Relational | PostgreSQL, MySQL | ACID transactions, complex joins, structured schema |
| Document | MongoDB, Firestore | Flexible/nested schemas, rapid iteration |
| Key-Value | Redis, DynamoDB | Caching, sessions, rate limiting, high-throughput simple reads |
| Time-Series | TimescaleDB, InfluxDB | Metrics, IoT, event logs, financial ticks |
| Graph | Neo4j, Neptune | Deep relationship traversal, social networks, recommendation |
| Search | Elasticsearch, Meilisearch | Full-text search, log analytics |

## Relational (PostgreSQL recommended)

Pick for: financial data, referential integrity, complex queries, structured predictable schema.

PostgreSQL vs. MySQL:
- PostgreSQL: richer JSON (JSONB), full-text search built-in, better extension ecosystem — prefer unless team is deeply MySQL-invested
- MySQL: fine for standard CRUD, large community, slightly simpler ops

Avoid relational when: schema changes constantly, horizontal shard is required from day one, simple key-value access only.

## Document

Pick for: flexible schemas, content management, nested hierarchical data, fast prototyping.
Avoid for: multi-document ACID transactions, heavy relational queries, strict schema enforcement.

Firestore: serverless, scales to zero, best for mobile/web apps with Google ecosystem.
MongoDB: self-hosted or Atlas, richer query language, better for complex aggregations.

## Key-Value

Redis: in-memory, microsecond latency. Use for caching, pub/sub, distributed locks, sessions, rate limiting counters.
DynamoDB: serverless key-value/document hybrid, infinite scale, single-digit ms. Use when schema is simple and scale is the primary concern.

Avoid for: relational queries, large blobs (>1 MB), complex filtering.

## Time-Series

TimescaleDB: PostgreSQL extension — SQL interface + time-optimized storage. Good if team already uses Postgres.
InfluxDB: dedicated time-series, optimized ingest and retention policies. Better for pure metrics/IoT at high volume.

## Graph

Use only when relationship traversal is the primary access pattern. Not for occasional joins — relational handles that. 
Worth the overhead for: social graphs, fraud detection networks, knowledge graphs, recommendation engines.

## Search

Elasticsearch: full-text search + log analytics + aggregations. High operational overhead.
Meilisearch: simpler, faster to stand up, good for product/content search. Less powerful aggregations.

Use a dedicated search engine alongside primary DB — don't use it as a source of truth.

## Decision Matrix

| Primary Need | Recommended |
|---|---|
| ACID transactions | PostgreSQL |
| Flexible evolving schema | MongoDB |
| Sub-ms reads, caching | Redis |
| Serverless scale, simple access | DynamoDB |
| Time-based metrics | TimescaleDB or InfluxDB |
| Relationship traversal | Neo4j |
| Full-text search | Elasticsearch or Meilisearch |

## Multi-Database Strategy

Most non-trivial systems use multiple:
- PostgreSQL → source of truth for business data
- Redis → cache + sessions
- Elasticsearch → search layer synced from primary

Write an ADR for each store. Justify the complexity cost.
