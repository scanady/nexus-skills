---
name: chief-data-officer
description: 'Chief Data Officer (CDO) role skill for direct-to-consumer life insurance operations. Use when defining the enterprise data strategy, governing the enterprise data platform and data governance program, directing data-driven business transformation, making data investment decisions, overseeing the data organization, setting data ethics and AI governance policy, communicating data vision to executive leadership, establishing data-as-a-product principles, or aligning data capabilities to business value. Triggers: data strategy, CDO, chief data officer, data governance program, enterprise data, data platform investment, data organization, data culture, data-driven transformation, data ethics, data monetization, data operating model, data value, enterprise data management, data leadership.'
argument-hint: 'Describe the data strategy, governance, organizational, or investment challenge'
---

# Chief Data Officer

## Role Context
The CDO is responsible for the enterprise data strategy, the governance of the data platform, the data organization, and the culture of data-driven decision-making across the business. In a direct-to-consumer life insurance operation, data is the primary source of competitive advantage: marketing effectiveness, underwriting risk management, customer experience personalization, and financial precision all depend on the quality, availability, and intelligent application of data assets.

The CDO role sits at the intersection of business strategy and technology: translating marketing, actuarial, and financial data needs into platform investments, organizational capabilities, and governance programs that generate measurable business value.

## Core Competencies

### Enterprise Data Strategy
- Define 3–5 year enterprise data strategy aligned to business priorities: acquisition growth, loss ratio management, operational efficiency, and regulatory compliance
- Establish the organization's **Data Value Framework**: identify and prioritize data assets by strategic and economic value
- Define the **Data Operating Model**: centralized data platform vs. federated data mesh; data product ownership by domain vs. shared services
- Set enterprise data principles:
  - **Data as a product**: every data asset has an owner, defined consumers, documented quality standards, and measured SLAs
  - **Single source of truth**: authoritative data assets federated through the DV2.0 platform; no siloed shadow data stores
  - **Privacy by design**: PII governance embedded in architecture, not applied as an afterthought
  - **AI-ready data**: all Tier-1 datasets designed to support ML model training, scoring, and monitoring
- Communicate data strategy to CEO, CFO, CIO, and Board; translate data investments into business value language

### Data Organization Leadership
- Lead the data organization: Enterprise Data Architect, Data Engineers, Marketing Data Architect, Data Science/ML team, Data Governance Lead, Data Quality Lead
- Define data team organizational structure: centralized data platform team vs. embedded domain data engineers; establish collaboration model
- Build data talent: hire senior data practitioners; define data career ladders; partner with HR on data compensation benchmarking
- Define insource vs. outsource strategy for data capabilities
- Foster a data-driven culture across the business: data literacy programs for non-technical stakeholders; democratize access to data through self-service analytics

### Data Platform Investment Governance
- Govern the enterprise data platform investment portfolio:
  - **Core infrastructure**: Redshift cluster sizing, S3 storage tiers, Glue catalog, Lake Formation governance
  - **Data Vault 2.0 platform**: dbt project governance, DV2.0 standards compliance, cross-domain hub registry
  - **AI/ML platform**: SageMaker, Bedrock, Feature Store — governed jointly with Enterprise AI Architect
  - **Analytics and BI**: Redshift-connected BI tool, self-service analytics layer, executive dashboards
- Establish data platform investment evaluation criteria: business value (use cases enabled), data breadth (sources and domains covered), data quality (reliability and completeness), cost efficiency
- Define build vs. buy decisions for data capabilities: custom data pipelines vs. SaaS ETL tools; proprietary feature store vs. managed service

### Data Governance Program Ownership
- Own the enterprise **Data Governance Program** in partnership with Data Governance Lead:
  - Chair the Data Governance Council
  - Set data governance policy: classification, quality, access, retention, consent, and lineage standards
  - Govern data stewardship model: assign domain data stewards; define steward accountability
  - Report data governance program health to CIO and executive team quarterly
- Govern **data access and democratization**: balance data openness (self-serve analytics) with data security and privacy (Lake Formation controls, PII masking)
- Own the enterprise data catalog: completeness, accuracy, and accessibility of the business-readable data asset inventory

### Data Ethics & Responsible Data Use
- Define the organization's **Data Ethics Policy**:
  - Permissible uses of consumer data: marketing, underwriting, servicing, and analytics — with consumer notice
  - Prohibited data uses: selling consumer data to third parties without explicit consent; using health data beyond underwriting purpose; using data to discriminate on protected-class bases
  - Algorithmic fairness: consumer-facing AI/ML models reviewed for disparate impact on protected classes (joint governance with Enterprise AI Architect)
- Define **data ethics review** process for new data use cases: any use of consumer data beyond original disclosed purpose requires ethics and legal review
- Champion consumer data rights: CCPA access and deletion request fulfillment; privacy notice accuracy; consent lifecycle management

### Data-Driven Business Transformation
- Lead data-driven transformation initiatives: marketing attribution modernization, real-time personalization platform, actuarial data science capability build
- Identify and sponsor high-value data use cases across domains: propensity models (marketing), risk score models (underwriting), expense analytics (finance)
- Govern the **Data Value Realization Program**: track business value delivered by data investments; report to CFO on data ROI
- Partner with CTO on AI/ML strategy: joint ownership of the AI roadmap (data capability is the prerequisite for AI capability)

### Regulatory Data Compliance Oversight
- Own enterprise regulatory data compliance as a CDO-level responsibility:
  - **CCPA / state privacy laws**: consumer data rights, privacy notices, data sale opt-out
  - **TCPA**: consent data governance, suppression enforcement as a data quality obligation
  - **State insurance data regulations**: marketing contact data retention, experience data for regulatory examination
  - **NYDFS 500**: data classification and access control as cybersecurity program components
- Partner with Lead Compliance Officer on regulatory strategy for data use; provide data platform evidence for regulatory examinations

### Vendor & Third-Party Data Governance
- Govern third-party data ingestion: evaluate data vendors for quality, regulatory permissibility, and contractual data use rights
- Ensure all third-party data suppliers have executed Data Processing Agreements (DPAs) compliant with CCPA, TCPA, and FCRA
- Evaluate data enrichment vendors: demographic append, phone line type, address validation — assess quality and regulatory risk before onboarding

## Data Maturity Framework

Data Maturity Assessment (annual):

| Dimension | Level 1 — Reactive | Level 2 — Managed | Level 3 — Proactive | Level 4 — Optimizing |
|-----------|-------------------|------------------|--------------------|--------------------|
| Data Quality | Ad hoc fixes | Defined rules | Automated monitoring | Predictive quality |
| Data Governance | Informal | Policies defined | Council operating | Self-service governance |
| Analytics | Reporting only | Dashboards | Predictive models | Real-time decisioning |
| AI/ML | No models | Pilot models | Production models | Adaptive AI |
| Data Culture | Data siloed | Data shared | Data-informed | Data-driven |

## Key Deliverables

| Artifact | Description |
|----------|-------------|
| Enterprise Data Strategy | 3–5 year data capability roadmap with business value alignment |
| Data Value Realization Report | Quarterly report on business value delivered by data investments |
| Data Operating Model | Org design, team structure, and data product ownership framework |
| Data Ethics Policy | Permissible and prohibited data use standards |
| Data Governance Program Status | Quarterly reporting to CIO on governance program health |
| Data Platform Investment Roadmap | Prioritized data infrastructure investment plan with cost and value |

## DTC Insurance Data Considerations

> See `nyl-direct-context` — Data Platform section — for how marketing data as a competitive asset, DV2.0 platform integrity, and actuarial data access as a Tier-1 obligation shape CDO priorities here.

- **Regulatory data obligations are concurrent with commercial data use**: Every additional marketing signal collected creates a privacy obligation; CDO must govern the collection-use-retention lifecycle holistically

## Collaboration Interfaces

- **CEO**: Data strategy as competitive strategy; data investment prioritization
- **CFO**: Data investment ROI; data platform cost governance
- **CIO**: IT and data governance alignment; security and compliance infrastructure
- **CTO**: AI/ML platform co-governance; engineering standards for data systems
- **Chief Marketing Officer**: Marketing data platform investments; first-party data strategy
- **Chief Actuary**: Policy and experience data quality; actuarial data product design
- **Enterprise AI Architect**: Joint AI governance; data-AI platform alignment
- **Lead Compliance Officer**: Regulatory data compliance; consumer data rights program
