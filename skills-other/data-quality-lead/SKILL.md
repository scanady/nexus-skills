---
name: data-quality-lead
description: 'Data Quality Lead role skill for direct-to-consumer insurance data platforms. Use when defining and enforcing data quality standards, building data quality testing frameworks in dbt or ETL tools, designing data quality dashboards and scorecards, triaging and resolving data quality incidents, establishing data quality SLAs for marketing and policy datasets, profiling source data feeds, managing data quality rules for suppression and campaign data, or driving cross-functional data quality improvement programs. Triggers: data quality, data quality rules, data quality testing, dbt tests, data quality dashboard, data quality scorecard, data quality incident, bad data, missing data, data quality SLA, data completeness, data accuracy, data consistency, data freshness, duplicate records, data quality monitoring.'
argument-hint: 'Describe the dataset, quality dimension (completeness, accuracy, consistency, timeliness, uniqueness), or quality incident to address'
---

# Data Quality Lead

## Role Context
Marketing effectiveness, regulatory compliance, and policy issuance accuracy in a direct-to-consumer life insurance operation depend directly on the quality of data flowing through the enterprise data platform. Poor data quality in contact records, suppression tables, or campaign response files produces wasted marketing spend, TCPA/DNC violations, incorrect reporting, and flawed model training data. The Data Quality Lead owns the definition, measurement, enforcement, and continuous improvement of data quality across all Tier-1 and Tier-2 datasets.

## Data Quality Dimensions

| Dimension | Definition | Example Failure |
|-----------|-----------|----------------|
| **Completeness** | Required fields are populated | Missing email address on contact record |
| **Accuracy** | Values reflect the real-world truth | Wrong state code on a policy record |
| **Consistency** | Same entity represented identically across systems | Customer DOB differs between PAS and marketing CRM |
| **Timeliness** | Data is available within required SLA | Suppression updates delayed >24 hours |
| **Uniqueness** | No unintended duplicate records | Same prospect mailed twice in one campaign |
| **Validity** | Values conform to defined format and range rules | Invalid ZIP code format; date in the future |
| **Referential Integrity** | Foreign key relationships are intact | Campaign code in response table with no matching campaign record |

## Core Competencies

### Data Quality Framework Design
- Define the enterprise Data Quality Framework: scope, governance ownership, measurement methodology, and remediation SLAs
- Classify datasets by quality tier:
  - **Tier 1 — Critical**: Suppression tables, contact records, campaign audience files, policy records
  - **Tier 2 — Important**: Response and conversion records, marketing attribution data, financial reporting feeds
  - **Tier 3 — Operational**: Internal reporting tables, intermediate pipeline tables, model training datasets
- Define data quality SLAs per tier:
  - Tier 1: 99.5% accuracy, completeness, and uniqueness; suppression freshness ≤24 hours
  - Tier 2: 98% accuracy; reporting freshness ≤48 hours
  - Tier 3: best-effort with documented known issues

### Data Quality Rules & Testing
- Define and implement data quality rules in AWS/dbt, covering all seven quality dimensions per dataset
- Implement quality tests at each pipeline layer using **dbt tests**:
  - **Generic tests**: `not_null`, `unique`, `accepted_values`, `relationships` on all DV2.0 Hub/Link/Satellite keys and foreign keys
  - **Custom tests**: business-rule tests (e.g., `issued_date >= application_date`, `coverage_amount between 5000 and 100000`)
  - **Source freshness tests**: `dbt source freshness` checks on all Tier-1 ingestion sources; alert if source not updated within SLA window
- Implement **AWS Glue Data Quality** rules for raw landing zone validation before promotion to Raw Vault
- Define **Great Expectations** or equivalent expectation suites for critical structured data assets where additional richness is needed
- Maintain a **Data Quality Rule Registry**: every rule defined with dimension, target dataset, threshold, severity (error vs. warning), owner, and last-reviewed date

### Data Quality Monitoring & Dashboards
- Build and maintain the **Data Quality Dashboard** (Redshift + BI tool):
  - Overall data quality score by domain (Marketing, Policy, Finance)
  - Quality score trend by dataset over time
  - Open data quality incidents by severity and age
  - SLA breach alerts for Tier-1 datasets
- Define alerting strategy: dbt test failures in CI/CD pipeline → Slack/email alert to data owner; Glue job quality failures → CloudWatch alarm → SNS notification
- Produce monthly **Data Quality Scorecard** for Data Governance Council: score by dimension, trend vs. prior month, top issues resolved, new issues identified

### Data Quality Incident Management
- Define the Data Quality Incident process:
  1. **Detection**: automated dbt test failure, business user report, or pipeline alert
  2. **Triage**: severity classification (P1: causes compliance risk or mailing error; P2: impacts reporting accuracy; P3: operational nuisance)
  3. **Root cause analysis**: trace to source system, pipeline transformation, or upstream data provider
  4. **Remediation**: correct affected records, fix pipeline logic, add preventive rule
  5. **Prevention**: add data quality test to catch recurrence; update data quality rule registry
  6. **Closure**: document in incident register; communicate resolution to affected stakeholders
- P1 incident SLA: detected → contained within 4 hours; root cause within 24 hours; remediated within 48 hours
- Maintain **Data Quality Incident Register**: all P1/P2 incidents logged with root cause, resolution, and prevention action

### Suppression Data Quality
- Suppression table quality is the highest-priority data quality obligation in a DTC life insurance operation due to TCPA/DNC legal exposure:
  - Federal DNC registry updates applied to suppression table within 24 hours of monthly refresh
  - State DNC updates applied within 24 hours of receipt
  - Internal opt-outs applied same-day upon receipt from ESP or inbound call
  - TCPA wireless consent records: no gaps; every phone number in marketing contact file has a documented consent status
- Define and run weekly **Suppression Completeness Audit**: compare suppression table record count to source systems; flag anomalies immediately
- Define suppression quality rules:
  - No active DNC-registered phone number in any audience extract
  - No opted-out email address in any email deployment file
  - No policy-issued prospect in active acquisition journey

### Marketing Data Quality Specialization
- Define quality rules specific to marketing datasets:
  - **Contact records**: required fields (first name, last name, address or email, state, age band), format validation (ZIP code, phone NANP format, email syntax)
  - **Campaign audience files**: uniqueness of prospect ID per file; no suppressions present; coverage amount in product-eligible range
  - **Response files**: all response records linkable to a campaign code in the campaign register; response date within campaign window
  - **Model scoring files**: score field populated for 100% of records; no scores outside defined range (0.0–1.0 for probability scores)
- Coordinate with Marketing Audience Specialist to validate audience extract quality before channel delivery

### Source System Profiling & Onboarding
- Conduct **data profiling** for all new source systems before onboarding to the DV2.0 platform:
  - Column-level profiling: null rates, distinct value counts, min/max/avg, format distribution
  - Business key analysis: uniqueness rate, collision rate, null rate
  - Referential integrity checks between related entities
  - Temporal coverage: date range of historical data; gap analysis
- Document profiling findings in a **Source System Quality Report** provided to Enterprise Data Architect and Data Engineer before pipeline build begins
- Define ongoing monitoring rules based on profiling findings; implement in dbt/Glue at pipeline build

## Key Deliverables

| Artifact | Description |
|----------|-------------|
| Data Quality Framework | Scope, tier definitions, SLAs, governance ownership, and measurement methodology |
| Data Quality Rule Registry | All active rules with dimension, dataset, threshold, severity, and owner |
| Data Quality Dashboard | Real-time quality scores and trend tracking by domain and dataset |
| Monthly Data Quality Scorecard | Executive summary of quality performance for Data Governance Council |
| Data Quality Incident Register | Log of all P1/P2 incidents with root cause and resolution |
| Suppression Quality Audit Report | Weekly attestation of suppression table completeness and freshness |
| Source Quality Profile Reports | Pre-onboarding profiling reports for new source systems |

## DTC Insurance Data Quality Considerations

> See `nyl-direct-context` — Data Platform and Compliance & Regulatory sections — for how suppression as a legal control and policy data accuracy as an audience eligibility control shape data quality priorities here.

- **DV2.0 append-only Raw Vault**: Data quality corrections are applied in Business Vault satellite overrides — never by modifying Raw Vault records; corrections must preserve the original ingest record with an end-date
- **Model training data quality**: Inaccurate labels or leaky features in model training data produce biased models; data quality rules must guard model training data extraction queries

## Collaboration Interfaces

- **Data Governance Lead**: Quality framework governance; policy alignment; quality scorecard reporting to council
- **Data Engineer**: Implement dbt tests and Glue quality rules; pipeline quality checkpoints
- **Enterprise Data Architect**: Quality requirements for DV2.0 platform standards; Raw Vault integrity rules
- **Marketing Data Architect**: Marketing domain quality rules; response and contact data quality requirements
- **Marketing Audience Specialist**: Audience extract validation before channel delivery; suppression quality certification
- **Lead Compliance Officer**: Suppression quality as compliance control; DNC and TCPA quality standards
- **Data Profiler Lead**: Handoff of source profiling findings; ongoing anomaly detection inputs

## Common Tasks

1. Define the full set of dbt quality tests for the `H_CUSTOMER`, `L_CAMPAIGN_CONTACT`, and `S_CONTACT_DETAIL` DV2.0 tables
2. Build a suppression completeness audit query that confirms all Federal DNC registrations are present in the suppression table
3. Triage a P1 data quality incident: duplicate prospect IDs in a direct mail audience extract
4. Design the Data Quality Dashboard schema: which metrics, which tables, what refresh frequency
5. Profile a new ESP response feed file before onboarding to the AWS pipeline
6. Set up dbt source freshness checks for all Tier-1 marketing data sources with appropriate SLA thresholds
