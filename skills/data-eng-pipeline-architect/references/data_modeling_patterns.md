# Data Modeling Patterns

Reference guide for warehouse + lakehouse data modeling decisions.

---

## Choosing a Modeling Approach

| Situation | Recommended approach |
|-----------|---------------------|
| BI / analytics on structured data | Star schema (Kimball) |
| Storage-constrained or complex normalization needed | Snowflake schema |
| Multi-source, auditability, schema flexibility | Data Vault 2.0 |
| Single consumer, fast query, wide denormalization OK | One Big Table (OBT) |
| Lakehouse with multiple consumers + quality layers | Medallion (Bronze/Silver/Gold) |

---

## Star Schema (Kimball)

Most common analytics model. Central fact table surrounded by denormalized dimension tables.

**Fact table:** measures + foreign keys to dimensions. One row per event/transaction.

```sql
-- Fact: one row per order line
CREATE TABLE fct_order_lines (
    order_line_key  BIGINT PRIMARY KEY,
    order_date_key  INT REFERENCES dim_date(date_key),
    customer_key    INT REFERENCES dim_customer(customer_key),
    product_key     INT REFERENCES dim_product(product_key),
    quantity        INT,
    unit_price      NUMERIC(10,2),
    discount_amount NUMERIC(10,2),
    net_revenue     NUMERIC(10,2)
);
```

**Grain statement required:** always declare the grain before building a fact table.
Example: "One row per order line item per order."

**Dimension table:** descriptive attributes, denormalized for query speed.
No joins within dimensions — flatten into the dim table.

**Best for:** Tableau / Power BI / Looker queries. Simple, predictable join patterns.

---

## Snowflake Schema

Normalized version of star schema. Dimension tables reference sub-dimension tables.

```
fct_orders → dim_product → dim_product_category → dim_department
```

**When to use:** Storage cost matters. Dimension hierarchy is deep and frequently queried at sub-levels.

**Trade-off:** More joins = slower BI queries. Use views to pre-join for consumers.

---

## Data Vault 2.0

Audit-friendly, source-agnostic modeling for enterprise data warehouses.

Three object types:

| Type | Purpose | Example |
|------|---------|---------|
| **Hub** | Business key + metadata | hub_customer (customer_bk, load_date, source) |
| **Link** | Relationship between hubs | link_order_customer (order_hk, customer_hk) |
| **Satellite** | Descriptive attributes, versioned | sat_customer_crm (customer_hk, name, email, load_date, end_date) |

All history preserved. No hard deletes. Source system tracked on every row.

**When to use:** Multiple source systems feeding same entity. Auditability required. Schema changes frequent.

**Cons:** Complex joins, verbose SQL. Requires tooling (dbt vault packages, AutomateDV).

---

## Slowly Changing Dimensions (SCD)

| Type | Behavior | Use when |
|------|---------|---------|
| **Type 1** | Overwrite — no history | Corrections, non-historical attributes (phone number) |
| **Type 2** | New row per change — full history | Most dimensions (customer address, product price) |
| **Type 3** | Add "previous value" column | Only need current + one prior (rare) |
| **Type 4** | History in separate audit table | High-churn dims with large rows |
| **Type 6** | Type 1 + 2 + 3 hybrid | Need current value fast AND full history |

**Type 2 implementation pattern:**

```sql
-- Mark previous record inactive on change
UPDATE dim_customer
SET is_current = false, effective_end = CURRENT_DATE
WHERE customer_bk = :bk AND is_current = true;

-- Insert new current version
INSERT INTO dim_customer (customer_bk, name, email, effective_start, effective_end, is_current)
VALUES (:bk, :name, :email, CURRENT_DATE, '9999-12-31', true);
```

**Surrogate key required** for Type 2 dims — natural key alone is not unique across versions.

---

## Medallion Layer Contracts

Define schema + quality rules at each layer boundary.

| Layer | Schema | Quality rules |
|-------|--------|--------------|
| Bronze | Inferred / as-source | No rules — raw fidelity |
| Silver | Declared DDL, version-controlled | No nulls on PK, no dups on natural key, type-cast all columns |
| Gold | Declared DDL, version-controlled | Row count SLA, freshness SLA, no nulls on metric columns |

Enforce Silver + Gold contracts via dbt schema tests:

```yaml
# dbt schema.yml
models:
  - name: silver_customers
    columns:
      - name: customer_id
        tests: [not_null, unique]
      - name: email
        tests: [not_null]
```

Fail CI if Silver/Gold tests fail. Never promote broken data to Gold.

---

## One Big Table (OBT)

Fully denormalized single table — all dims pre-joined into one wide table.

**When:** Single known consumer with stable, wide query patterns. Columnar storage makes width cheap.

**Cons:** Data duplication. Multiple consumers with different needs = multiple OBTs or misfit queries.

Build OBT in Gold layer from Silver star schema. Don't model OBT at Silver — keep flexibility.

---

## Naming Conventions

| Object | Prefix | Example |
|--------|--------|---------|
| Fact table | `fct_` | `fct_orders`, `fct_pageviews` |
| Dimension | `dim_` | `dim_customer`, `dim_date` |
| Staging (Bronze) | `stg_` | `stg_salesforce_accounts` |
| Intermediate | `int_` | `int_orders_with_customer` |
| Gold / mart | none or `_mart` | `orders_summary`, `sales_mart` |

Consistent naming enables discovery and prevents model collision in large dbt projects.

---

## Date Dimension

Always build a date dimension table. Never compute calendar logic in fact queries.

Minimum columns: `date_key (INT YYYYMMDD)`, `full_date`, `year`, `quarter`, `month`, `week`, `day_of_week`, `is_weekend`, `is_holiday`, `fiscal_year`, `fiscal_quarter`.

Populate 10 years past + 3 years future. Static — no pipeline needed after initial load.
