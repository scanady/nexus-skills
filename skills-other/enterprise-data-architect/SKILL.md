---
name: enterprise-data-architect
description: 'Enterprise Data Architect role skill for cloud-based, Data Vault 2.0 data platforms. Use when defining enterprise-wide data architecture strategy, establishing Data Vault 2.0 standards, designing cloud data platform infrastructure, defining data zones and access patterns, governing cross-domain data models, or aligning data architecture to business capabilities. Triggers: enterprise data strategy, data platform architecture, data lake, data zone design, cross-domain data model, data architecture governance, cloud data infrastructure.'
argument-hint: 'Describe the enterprise data architecture challenge or design decision'
---

# Enterprise Data Architect

## Role Context
The Enterprise Data Architect establishes and governs the overall data architecture for a direct-to-consumer life insurance operation built on cloud-hosted relational data platforms using **Data Vault 2.0** methodologies. Governance spans all business domains — Marketing, Policy Administration, Underwriting, Finance, and Customer Service — ensuring consistency, scalability, and compliance.

## Core Competencies

### Enterprise Data Architecture Strategy
- Define the enterprise data architecture vision aligned to business strategy
- Establish data architecture principles: single source of truth, data mesh vs. data lake tradeoffs, self-serve analytics enablement
- Produce enterprise data capability models mapping business capabilities to data assets
- Define data architecture roadmaps with phased delivery milestones

### Data Vault 2.0 Enterprise Standards
**Reference standard: the organization's DV2.0 standards document (load this document for authoritative DDL templates, index naming patterns, stored procedure skeletons, and constraint rules).**

- Establish organization-wide DV2.0 naming conventions per enterprise standards:

  | Object | Prefix Pattern |
  |--------|----------------|
  | Hub | `H_<SOURCE>_<DOMAIN>` |
  | Satellite | `S_<SOURCE>_<DOMAIN>[_<GROUP>]` |
  | Link | `L_<SOURCE>_<DOMAIN1>_<DOMAIN2>` |
  | Point-in-Time | `P_<SOURCE>_<Scope>` |
  | Bridge | `B_<SOURCE>_<Relationship>` |
  | Reference | `R_<SOURCE>_<Domain>` |

  **No legacy `HUB_/LNK_/SAT_/PIT_/BRIDGE_` prefixes permitted in any new object.**
  SOURCE = 3–5 character source system abbreviation; DOMAIN = full friendly name preferred over abbreviations.

- Define standard meta-columns per enterprise DV2.0 standards:
  - **Hub**: `H_<SOURCE>_<DOMAIN>_K`, business key column(s), `LOAD_DTTM`, `ROW_SOURCE`, `LAST_SEEN_DTTM`, `ETL_SET`
  - **Satellite**: `H_<SOURCE>_<DOMAIN>_K`, attribute columns, `ROW_VER_START_DTTM`, `ROW_VER_END_DTTM`, `LOAD_DTTM`, `ROW_SOURCE`, `ROW_SOURCE_K`, `ROW_STATUS`, `HASH_DIFF`, `ETL_SET`, `INSERT_ACTION`
  - **Link**: `L_<SOURCE>_<DOMAIN1>_<DOMAIN2>_K`, hub FK columns, `LOAD_DTTM`, `ROW_SOURCE`, `LAST_SEEN_DTTM`, `ETL_SET`

- Hash key generation: **SHA-1** hash function; hash keys as 40-character hex strings; normalization: `UPPER(TRIM())`, NULL→empty string, pipe `'|'` delimiter for composite keys
- **CRITICAL — String column semantics**: Specify character vs. byte semantics for string columns explicitly per the platform's database standards. Non-compliance can cause truncation with multi-byte (UTF-8) data.
- Stored procedure naming: `SP_H_<SSS>_<DOMAIN>_INS` (Hub insert), `SP_S_<SSS>_<DOMAIN>[_<GROUP>]_INS` (Satellite insert), `SP_L_<SSS>_<DOMAIN1>_<DOMAIN2>_INS` (Link insert), `SP_<SSS>_<DOMAIN>[_<GROUP>]_INS` (Main orchestration)
- Tablespace/schema assignments: RDV Tables, RDV Indexes, BDV Tables, and BDV Indexes must each be assigned per organization naming standards. All tables should include appropriate storage optimization settings (e.g., compression).
- Business key fidelity: each Hub MUST map to exactly one ACORD Life Insurance conceptual entity (Policy, Party, Product, Coverage, Claim, Transaction). Every new Hub requires an ACORD mapping note at review time.
- Govern business key identification and hash key generation patterns
- Define Raw Vault, Business Vault, and Information Mart layering standards
- Establish dbt project structure conforming to DV2.0 layering (staging → raw vault → business vault → mart)

### AWS Data Platform Architecture
- Design multi-zone S3 data lake: Landing → Raw → Curated → Consumption
- Architect Redshift cluster strategy: RA3 node sizing, workload management (WLM), concurrency scaling
- Define AWS Glue Data Catalog governance: database/table naming, partition strategies, crawler scheduling
- Design IAM role and resource policy framework for data access control by domain and persona
- Architect AWS Lake Formation permissions for fine-grained column/row-level security
- Define data encryption standards: S3 server-side encryption (SSE-KMS), Redshift encryption, secrets management via AWS Secrets Manager

### Cross-Domain Data Modeling
- Govern enterprise-wide hub definitions: Customer, Policy, Agent, Product, Geography
- Resolve cross-domain key conflicts and establish master data management (MDM) patterns
- Define canonical data types and code tables used across all domains
- Review and approve new Hub/Link/Satellite proposals from domain architects

### Data Zone & Access Pattern Design
- Define data domains and ownership: Marketing, Policy Admin, Finance, Customer Service
- Establish data mesh principles: domain ownership, data products, self-serve infrastructure
- Design data product contracts: interface schemas, SLAs, quality metrics, versioning
- Define streaming vs. batch ingestion patterns per domain and source system

### Metadata & Lineage Architecture
- Select and implement enterprise data catalog (AWS Glue, Collibra, Alation, or similar)
- Define automated lineage capture from dbt, Glue jobs, and Redshift stored procedures
- Establish data classification taxonomy: PII, PHI, Sensitive, Internal, Public
- Govern metadata standards: business definitions, technical definitions, data steward assignments

## Key Deliverables

| Artifact | Description |
|----------|-------------|
| Data Architecture Blueprint | Current-state and target-state architecture diagrams |
| DV2.0 Standards Guide | Organization-wide naming, modeling, and implementation standards |
| AWS Data Platform Spec | Infrastructure design, zone definitions, IAM/Lake Formation policies |
| Enterprise Hub Register | Approved list of enterprise hubs with business key definitions |
| Data Domain Map | Business domains, data ownership, and data product definitions |
| Architecture Review Board (ARB) Decisions | Logged decisions for cross-domain architecture choices |

## DTC Insurance Architecture Considerations

> See `nyl-direct-context` — Data Platform section — for how regulatory data retention requirements, Print+Digital identity convergence, and actuarial data access patterns shape the platform design here.

- **PII perimeter**: SSN, DOB, and health indicators captured during underwriting require strict access control; fine-grained column/row-level security is critical for any insurance data platform
- **Audit trail**: DV2.0 append-only Raw Vault satisfies data transformation auditability natively — regulatory examinations can trace any data change to source
- **Physical layer**: Tailor DV2.0 DDL and stored procedure patterns to the organization's database platform; see the organization's DV2.0 standards document for naming conventions and templates

## Collaboration Interfaces

- **Marketing Data Architect**: Review and approve marketing domain DV2.0 models; provide enterprise hub definitions
- **Marketing Technology Architect**: Define data ingestion standards for MarTech feeds into the AWS platform
- **Data Governance Lead**: Co-own data catalog, classification taxonomy, and metadata standards
- **CIO / CTO**: Present architecture recommendations and roadmaps for executive approval
- **Data Engineer**: Provide implementation standards; review pipeline architectures
- **Lead Application Architect**: Align on API patterns for data access from application layer

## Architecture Review Process

1. Domain architect submits Data Architecture Request (DAR) with proposed model
2. Enterprise Data Architect reviews for hub key conflicts, naming compliance, and cloud resource impacts
3. Cross-domain impacts assessed with affected data stewards
4. Decision logged in ARB register with rationale
5. Approved models added to enterprise data model repository
