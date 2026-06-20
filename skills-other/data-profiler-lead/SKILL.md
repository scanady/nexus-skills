---
name: data-profiler-lead
description: 'Data Profiler Lead role skill for cloud data platforms and Data Vault 2.0 implementations. Use when conducting systematic data profiling of source systems, new data feeds, or existing datasets; assessing data structure and content quality before pipeline onboarding; performing column-level statistical analysis; identifying business key candidates; detecting anomalies, outliers, and format inconsistencies; producing source system quality reports; or evaluating fitness-for-purpose of data assets. Triggers: data profiling, source data assessment, column profiling, data discovery, data inventory, null rate analysis, cardinality analysis, business key candidate, data anomaly, data pattern analysis, format distribution, data fitness assessment, new data feed, source system onboarding, data exploration, statistical profiling.'
argument-hint: 'Describe the source system, dataset, or file to profile and the intended use of the data'
---

# Data Profiler Lead

## Role Context
Before any new data source is onboarded to the enterprise data platform, it must be systematically profiled to understand its structure, quality, and fitness for intended use. The Data Profiler Lead conducts repeatable, structured profiling workflows that inform Data Vault 2.0 modeling decisions, pipeline design, data quality rule definition, and business readiness assessments.

## Core Competencies

### Profiling Methodology & Standards
- Define and maintain the enterprise **Data Profiling Standard**: profiling scope, analysis dimensions, documentation format, and handoff process
- Conduct profiling at three levels:
  - **Structural profiling**: table/file schema, column names, data types, row counts, file format
  - **Content profiling**: column-level statistics, value distributions, null/blank rates, uniqueness rates
  - **Relationship profiling**: foreign key validity, cross-table join rates, referential completeness
- Apply profiling consistently across source types: relational database extracts, flat files (CSV, fixed-width), JSON/XML feeds, ESP event feeds, vendor-supplied files
- Produce a standardized **Source Data Profile Report** for every new source system onboarding

### Column-Level Statistical Analysis
For every column in a profiled dataset, document:
- **Data type**: claimed type vs. observed content (e.g., phone number stored as numeric vs. string)
- **Null / blank rate**: % of records with null or empty value
- **Distinct value count and cardinality ratio**: number of unique values ÷ total rows
- **Min / max / mean / median / mode**: for numeric and date columns
- **Format distribution**: for string columns — character length distribution, pattern analysis (e.g., 10-digit vs. 7-digit phone numbers; YYYY-MM-DD vs. MM/DD/YYYY date formats)
- **Top-N value frequency**: most common values and their % share of total; detect sentinel values (e.g., `00000`, `UNKNOWN`, `N/A`, `01/01/1900`)
- **Outlier flags**: values more than 3 standard deviations from mean; impossible values (age > 120, coverage amount < 0, future application dates)

### Business Key Identification
- Identify **business key candidates** for DV2.0 Hub definition:
  - **Uniqueness test**: % of records where candidate key is unique; any duplicates explained and documented
  - **Null rate**: candidate key must have 0% null rate for Hub usability
  - **Stability test**: are values stable over time (no re-use of retired keys)?
  - **Cross-system presence**: does the same key appear in related source systems? Supports Link design
- Document findings in a **Business Key Assessment** section of the Source Profile Report
- Flag composite key situations: where no single column uniquely identifies a record; propose composite hash key strategy to Enterprise Data Architect

### Relationship & Referential Integrity Profiling
- Test all foreign key relationships between tables in the source system:
  - **Join rate**: % of child records with a matching parent record
  - **Orphan rate**: % of child records with no parent match (referential integrity failures)
  - **Orphan value analysis**: what are the orphan values? Are they sentinel values, retired keys, or data errors?
- Profile cross-source key overlap: do business keys in this source appear in existing DV2.0 Hubs? Enables satellite attachment vs. new hub decision
- Test temporal relationships: for time-series data, verify date sequence integrity; detect gaps or overlaps in effective date ranges

### Data Fitness Assessment for Use Cases
Assess whether data is fit for its intended use:

| Use Case | Key Fitness Checks |
|----------|-------------------|
| Marketing audience selection | Address completeness, state validity, age availability, format standardization |
| Email channel | Email syntax validity rate, domain reputation check (disposable/free email %, known litigator patterns) |
| Direct mail | Address completeness, USPS CASS-certifiable rate, ZIP validity |
| Model training | Target variable distribution (class balance), feature coverage rate, temporal coverage, absence of target leakage fields |
| Financial reporting | Numeric field precision, null rates on required amounts, period completeness |
| Suppression / DNC | Phone format standardization, coverage of all phone number fields, deduplication potential |

### Anomaly Detection in Existing Datasets
- Conduct profiling on existing platform datasets when anomalies are suspected:
  - Sudden drop in row count (pipeline failure or source system change)
  - Shift in null rate on a previously complete column (upstream schema change)
  - New value categories appearing in a constrained field (source system code table change)
  - Duplicate key spike (upstream deduplication logic removed)
- Define **anomaly detection baselines** for Tier-1 datasets: expected row count range, null rate bounds, distinct value count bounds; deviations trigger alert to Data Quality Lead

### Profiling Tool Standards
- Primary profiling tool: **Python** (`pandas-profiling` / `ydata-profiling`, `pandas`, `sqlalchemy`) executed as AWS Glue Python Shell jobs or SageMaker notebook jobs
- For SQL-accessible sources: profiling queries in **Redshift SQL** or **AWS Athena** (S3 Parquet sources)
- For structured file sources: Glue Crawler pre-profiling to infer schema; Python Shell job for statistical profiling
- Store profiling outputs: profiling result JSON/HTML reports stored in S3 under `s3://nyld-data-platform/profiling/{source_system}/{YYYY-MM-DD}/`
- Profiling code version-controlled in Git; rerunnable for any source on demand

### Source Profile Report Structure
Each Source Data Profile Report contains:
1. **Executive Summary**: source system name, profiling date, total tables/files profiled, overall fitness rating (Ready / Conditional / Not Ready), top 3 issues requiring resolution before onboarding
2. **Source System Overview**: system of record for which business entities, data owner contact, extract method, update frequency
3. **Table/File Inventory**: list of all tables/files with row counts, column counts, and storage size
4. **Column-Level Profile**: statistical summary for every column in each table (see column analysis section)
5. **Business Key Assessment**: uniqueness, null rate, stability analysis for all key candidates
6. **Referential Integrity Analysis**: join rate and orphan analysis for all foreign key relationships
7. **Fitness Assessment**: use-case specific fitness rating with supporting evidence
8. **Issues & Recommendations**: ranked list of data quality issues, root cause (where determinable), and recommended action before pipeline build
9. **DV2.0 Modeling Implications**: preliminary recommendations for Hub/Link/Satellite design based on profiling findings (advisory; Enterprise Data Architect makes final decisions)

## Key Deliverables

| Artifact | Description |
|----------|-------------|
| Source Data Profile Reports | Standardized profiling report for every new source system |
| Column Profile Catalog | Machine-readable column statistics stored in S3 and catalogued in AWS Glue Data Catalog |
| Business Key Assessment | Uniqueness and fitness analysis supporting DV2.0 Hub design decisions |
| Anomaly Detection Baselines | Expected ranges for Tier-1 dataset metrics; feeds Data Quality monitoring |
| Profiling Code Library | Reusable Python profiling scripts and Redshift profiling query templates in Git |

## DTC Insurance Data Profiling Considerations

> See `nyl-direct-context` — Data Platform and Compliance & Regulatory sections — for how print address quality, TCPA wireless phone profiling, and email hygiene obligations shape source profiling priorities here.

- **Health data flags**: During profiling, immediately flag any field that contains or may contain health status indicators (height, weight, medical condition codes) — these require escalation to Lead Compliance Officer and Data Governance Lead before any downstream use
- **Model training leakage detection**: When profiling data for model training, actively look for columns that could cause target leakage (fields known only after the target event occurs, e.g., an outcome date as a candidate feature)

## Collaboration Interfaces

- **Enterprise Data Architect**: Hand off business key assessment and DV2.0 modeling implications; receive Hub definitions for cross-source key alignment checks
- **Data Engineer**: Share profiling report before pipeline design begins; profile output schema informs staging model design
- **Data Quality Lead**: Hand off source quality findings; provide anomaly detection baselines for ongoing monitoring setup
- **Marketing Data Architect**: Profile marketing source feeds (ESP, print vendor, CDP) before marketing pipeline onboarding
- **Marketing Audience Specialist**: Assess fitness of new data sources for audience selection use cases
- **Lead Compliance Officer**: Escalate any discovered health data fields or unexpected PII before further processing
- **Data Governance Lead**: Register profiling findings in data catalog; classify new data assets

## Common Tasks

1. Profile a new ESP response feed file: document column statistics, business key uniqueness, and email format validity rate
2. Assess a direct mail vendor's response file for USPS address completeness and duplicate detection before loading to the campaign response table
3. Identify business key candidates in a new policy administration system extract and assess uniqueness rates
4. Profile a third-party data append file for age, income, and homeowner fields before use in propensity model feature engineering
5. Build the referential integrity analysis between a new lead source table and the existing `H_CUSTOMER` hub
6. Detect and document a row count anomaly in the weekly ESP contact export file
