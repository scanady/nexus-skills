# DataOps Best Practices

Reference guide for CI/CD, data contracts, testing, observability, and deployment for data pipelines.

---

## CI/CD for Data Pipelines

All pipeline code — SQL, Python, dbt models, DAG definitions — treated as software.

**Required pipeline stages:**

```
PR opened → lint → unit tests → integration tests → review → merge → deploy
```

**Lint:** SQL linting (sqlfluff), Python linting (ruff), dbt project validation (`dbt parse`).

**Unit tests:** Test transformation logic without live database. Mock source data.

**Integration tests:** Run against staging environment with representative data sample.
Never run integration tests against production — use separate schema or dev warehouse.

**Deployment via PR only.** No manual changes to production DAGs or dbt models.

**dbt CI pattern:**

```bash
# In CI pipeline (GitHub Actions / GitLab CI)
dbt compile --target ci
dbt test --target ci --select state:modified+
dbt run --target ci --select state:modified+
```

Only test + run changed models and their dependents (`state:modified+`). Avoid full project re-run in CI.

---

## Data Contracts

Formal agreement between data producer and consumer: schema, quality, SLA, ownership.

Define contracts **before** building pipelines. Consumers depend on contracts, not on implementation details.

**Minimal contract definition:**

```yaml
# data-contract.yml
dataset: silver_orders
owner: data-platform-team
grain: one row per order
schedule: daily 06:00 UTC
sla:
  freshness: 2 hours after schedule
  row_count_min: 1000
schema:
  - name: order_id
    type: STRING
    nullable: false
    unique: true
  - name: customer_id
    type: STRING
    nullable: false
  - name: order_total
    type: NUMERIC
    nullable: false
quality_rules:
  - order_total >= 0
  - status IN ('pending', 'confirmed', 'shipped', 'cancelled')
```

**Contract enforcement:** run contract validation on every load. Fail load + alert on breach.

Tools: [Data Contract CLI](https://datacontract.com/), dbt schema tests, Great Expectations.

---

## Testing Pyramid for Data

| Layer | What | Tools | Run when |
|-------|------|-------|---------|
| **Unit** | Transform logic, SQL functions | pytest + mock data, dbt unit tests | Every commit |
| **Integration** | Pipeline end-to-end on sample data | dbt + staging DB | On PR |
| **Contract** | Output schema + quality vs contract | dbt tests, Great Expectations | On PR + post-deploy |
| **Regression** | Row count + metric delta vs baseline | Custom SQL assertions | Post-deploy |

Unit tests for dbt (dbt 1.8+):

```yaml
# dbt unit test definition
unit_tests:
  - name: test_net_revenue_calculation
    model: fct_order_lines
    given:
      - input: ref('stg_orders')
        rows:
          - {order_id: 'A1', gross: 100.00, discount: 10.00}
    expect:
      rows:
        - {order_id: 'A1', net_revenue: 90.00}
```

---

## Observability

Monitor four signals on every pipeline output:

| Signal | What to track | Alert threshold |
|--------|-------------|----------------|
| **Freshness** | Time since last successful load | > 2× expected schedule interval |
| **Volume** | Row count vs 7-day rolling average | < 50% or > 300% of average |
| **Schema drift** | Column added/removed/type changed | Any change on Silver/Gold tables |
| **Quality** | Null rate, dup rate, constraint violations | Any fail-severity check |

**Data lineage:** track source → target column mapping for every transform.
Tools: dbt docs + exposure graph, OpenLineage + Marquez, Atlan, DataHub.

**Alerting stack:**
- Airflow SLA callbacks → PagerDuty / Opsgenie for pipeline failure
- dbt test failures → Slack alert with test name + failing rows
- Volume anomalies → dashboard alert + Slack notification

Bake observability in at build time — not as a retrofit.

---

## Data Catalog

Register every new dataset before consumers can use it.

Minimum metadata per dataset:

- **Owner** (team + individual)
- **Grain** (what does one row represent)
- **Schedule + SLA** (when refreshed, how fresh guaranteed)
- **Upstream sources** (lineage)
- **Known consumers** (downstream dashboards, models, apps)
- **PII flag** (does it contain personal data)

Tools: dbt docs (lightweight), DataHub (self-hosted), Atlan, Alation.

---

## Deployment Strategies

### Blue/Green for Pipelines

Run new pipeline version in parallel with existing. Compare output row counts + key metrics. Cut over consumers once validated.

Useful for: major schema changes, complete pipeline rewrites.

**Pattern:**
1. Deploy new pipeline writing to `_v2` table
2. Run both for 2–3 cycles
3. Validate `_v2` output matches (or intentionally differs from) `_v1`
4. Update consumer references to `_v2`
5. Decommission `_v1` pipeline + table

### Incremental Schema Changes

Safe order for schema changes to avoid downstream breaks:

1. Add new columns (backward-compatible)
2. Backfill new columns in existing data
3. Update contracts + consumers to use new columns
4. Drop old columns **last** (only after all consumers migrated)

Never drop or rename a column without confirming zero consumers first.

### Feature Flags for Data

Use dbt variables or Airflow Variables to gate new logic:

```sql
-- dbt model: conditionally use new revenue logic
{% if var('use_new_revenue_logic', false) %}
    {{ new_revenue_calc() }}
{% else %}
    {{ legacy_revenue_calc() }}
{% endif %}
```

Enable per-environment before cutting over production.

---

## Incident Management for Data

**Severity levels:**

| Severity | Condition | Response SLA |
|----------|-----------|-------------|
| P1 | Gold table stale > 4h during business hours | 30 min |
| P2 | Silver quality check failing, Gold unaffected | 2 hours |
| P3 | Non-critical pipeline delayed | Next business day |

**Runbook per pipeline** — document:
- What it does + who uses it
- How to check status
- Common failure modes + resolution steps
- How to trigger manual backfill
- Escalation contact

Store runbooks in the same repo as pipeline code. Keep them current on refactors.
