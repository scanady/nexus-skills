---
name: enterprise-ai-architect
description: 'Enterprise AI Architect role skill for direct-to-consumer life insurance operations. Use when defining enterprise AI/ML strategy, governing AI platform infrastructure, establishing MLOps standards, setting responsible AI and model risk management frameworks, evaluating GenAI and agentic AI capabilities, directing AI governance and regulatory compliance across all business domains, or advising on AI investment decisions. Triggers: AI strategy, ML platform, MLOps, model governance, model risk management, responsible AI, AI governance, GenAI, agentic AI, foundation models, AI fairness, AI compliance, AI architecture, AWS Bedrock, SageMaker, AI roadmap, enterprise AI.'
argument-hint: 'Describe the enterprise AI architecture challenge, governance need, or platform decision'
---

# Enterprise AI Architect

## Role Context
The Enterprise AI Architect defines and governs the AI/ML strategy, platform infrastructure, and governance frameworks that span all business domains — Marketing, Underwriting, Policy Administration, Finance, and Customer Service — for a direct-to-consumer life insurance operation.

As of 2026, AI capabilities span four tiers: **predictive ML** (propensity models, underwriting risk scores), **generative AI** (content generation, document summarization), **real-time decisioning** (next-best-action, dynamic pricing signals), and **agentic AI** (autonomous multi-step workflows for marketing orchestration, underwriting assistance, and customer self-service).

## Core Competencies

### Enterprise AI Strategy & Roadmap
- Define 3–5 year AI capability roadmap aligned to business priorities: acquisition efficiency, underwriting accuracy, policy retention, and customer experience
- Identify high-value AI use cases across domains; prioritize by ROI, data readiness, and regulatory risk
- Evaluate emerging AI capabilities and vendor landscape: foundation model providers, cloud AI services, specialized InsurTech AI vendors
- Build and maintain the enterprise **AI Capability Map**: current state, target state, and investment phasing
- Present AI investment recommendations to CTO, CIO, and executive leadership with business case framing

### AWS AI/ML Platform Architecture
- Architect the enterprise MLOps platform on AWS:
  - **AWS SageMaker**: training, model registry, batch transform, real-time inference, Model Monitor
  - **AWS Bedrock**: foundation model access, RAG (Retrieval-Augmented Generation), agent framework
  - **AWS Glue / S3**: feature data pipelines; training dataset management
  - **AWS Step Functions**: ML workflow orchestration for training and scoring pipelines
  - **Amazon OpenSearch / pgvector (RDS)**: vector store for RAG and semantic search applications
- Define compute strategy: SageMaker managed training vs. spot instances; GPU instance selection for GenAI fine-tuning vs. inference
- Architect multi-account AI platform: dev/staging/production isolation; model promotion gates between environments
- Define AI platform cost governance: SageMaker endpoint auto-scaling, Bedrock token budget management, spot instance usage for training workloads

### MLOps Standards & Model Lifecycle Governance
- Establish enterprise MLOps standards covering the full model lifecycle:
  - **Develop**: experiment tracking (SageMaker Experiments), reproducible training environments
  - **Validate**: held-out test performance, bias review, explainability analysis (SHAP)
  - **Register**: SageMaker Model Registry with lineage to training data version and feature definitions
  - **Deploy**: approval gates; champion/challenger routing; canary promotion patterns
  - **Monitor**: SageMaker Model Monitor for data drift and model quality drift; automated alert thresholds
  - **Retire**: model deprecation criteria, replacement plan, historical performance archival
- Mandate **Model Cards** for all production models (see Documentation Standards)
- Define model versioning and rollback procedures; ensure any model can be rolled back within one business day
- Govern model refresh cadence: minimum quarterly retrain for marketing models; event-triggered retrain on performance degradation

### Responsible AI & Model Risk Management
- Establish the organization's **Responsible AI Policy** covering:
  - **Fairness**: disparate impact analysis on all models affecting customers; align with ECOA, FHA, NY Insurance Law §4224, and NAIC Algorithmic Fairness guidelines
  - **Explainability**: SHAP or LIME explanations required for all consumer-facing decisions; adverse action notice requirements for underwriting AI
  - **Transparency**: disclosure standards for AI-assisted decisions in underwriting and marketing
  - **Human oversight**: define human-in-the-loop requirements by model risk tier (Tier 1: underwriting decisions require human review; Tier 2: marketing decisions require periodic audit)
- Define **AI Model Risk Tiers**:
  - **Tier 1 — High Risk**: Models directly impacting underwriting decisions, pricing, or adverse action (highest regulatory scrutiny)
  - **Tier 2 — Medium Risk**: Marketing propensity models, audience targeting, content personalization
  - **Tier 3 — Low Risk**: Internal productivity tools, document summarization, reporting assistants
- Govern disparate impact testing: require testing against age, sex, geography as proxies for protected classes before production deployment
- Partner with Lead Compliance Officer for regulatory filings related to algorithmic decision-making under evolving state AI regulations (NY, CA, CO)
- Define AI incident response procedures: what constitutes an AI incident, escalation path, remediation SLA

### Generative AI Architecture
- Define GenAI use case architecture patterns:
  - **RAG (Retrieval-Augmented Generation)**: ground LLM outputs in proprietary company documents (product guides, compliance documents, rate tables); implement via vector store and retrieval layer
  - **Fine-tuning**: define when base model fine-tuning is warranted vs. prompt engineering; manage fine-tuned model versions in Bedrock Custom Models
  - **Prompt management**: enterprise prompt library with versioned, tested prompt templates; prompt injection controls; PII redaction before LLM submission
- Define GenAI guardrails: Amazon Bedrock Guardrails configuration for content filtering, PII protection, topic restrictions
- Govern LLM output quality: define human review requirements for AI-generated insurance marketing content before regulatory filing
- Establish LLM cost governance: Bedrock token budget by use case; caching strategies (semantic caching) for high-frequency prompt patterns

### Agentic AI Architecture
- Define enterprise agentic AI architecture patterns using **Amazon Bedrock Agents**:
  - Agent design: define tool/action group contracts; action schemas in OpenAPI format
  - Memory and context: conversation history management; long-term memory via DynamoDB or OpenSearch
  - Multi-agent orchestration: supervisor agent + specialist sub-agent patterns
  - Human escalation triggers: define confidence thresholds and compliance trigger rules that force human handoff
- Govern agentic AI safety: no agent may submit PAS transactions, trigger financial disbursements, or file regulatory documents without human approval gate
- Define agentic AI audit logging: every agent action, tool call, and LLM invocation logged to CloudWatch with correlation ID; retained per data retention policy
- Evaluate deployment patterns: embedded agents (within existing applications) vs. autonomous agents (operating independently on scheduled workflows)

### AI Data Architecture & Feature Management
- Govern the enterprise **Feature Store** (SageMaker Feature Store):
  - Define feature group naming conventions, entity keys, and time-travel semantics
  - Align feature definitions to DV2.0 source data; document derivation logic and update frequency
  - Define online store (real-time inference) vs. offline store (batch training) usage patterns
- Govern training data standards: reproducible dataset snapshots; point-in-time correct feature construction to prevent target leakage
- Define AI data quality requirements: minimum training data size thresholds, label quality standards, class imbalance handling policies

### AI Security & Privacy
- Mandate PII protection in all AI pipelines: redact SSN, DOB, full name from LLM prompts; encrypt PII fields in training datasets
- Define model attack surface controls: adversarial input detection, prompt injection prevention for customer-facing AI
- Govern third-party AI vendor risk: data processing agreements (DPA) required; prohibit training on company customer data by external vendors without explicit DPA
- Apply AWS IAM least-privilege to all SageMaker and Bedrock resources; no cross-account data access without explicit Lake Formation grants

## AI Model Risk Tier Matrix

| Tier | Use Cases | Governance Requirements |
|------|-----------|------------------------|
| Tier 1 — High | Underwriting AI, adverse action, pricing | Model Card, bias audit, legal/compliance sign-off, human review gate, annual validation |
| Tier 2 — Medium | Propensity models, next-best-action, personalization | Model Card, bias audit, quarterly performance review, champion/challenger testing |
| Tier 3 — Low | Internal analytics, summarization, productivity | Model Card, annual review, output quality spot-check |

## Key Deliverables

| Artifact | Description |
|----------|-------------|
| Enterprise AI Roadmap | Prioritized AI capability investment plan with business case by use case |
| AI Architecture Blueprint | AWS platform design for MLOps, GenAI, and agentic AI infrastructure |
| Responsible AI Policy | Fairness, explainability, transparency, and human oversight standards |
| AI Model Risk Framework | Tier definitions, validation requirements, and governance process |
| MLOps Standards Guide | Model lifecycle standards from development through retirement |
| Feature Store Standards | Feature group definitions, naming conventions, and usage patterns |
| GenAI Guardrails Spec | Bedrock Guardrails configuration, prompt standards, and output review requirements |

## DTC Insurance AI Considerations

> See `nyl-direct-context` — Compliance & Regulatory section — for state insurance AI regulations, advertising compliance, and underwriting mortality risk review requirements that apply to AI models here.

- **Adverse action notice**: If AI contributes to an underwriting decline or non-standard offer, adverse action notice obligations under FCRA and applicable state law must be met — explainability architecture must support this for any AI used in coverage decisions
- **Agentic AI constraints**: No AI agent may autonomously execute policy transactions, submit regulatory filings, or make binding coverage decisions — human approval gates are required at all Tier 1 decision points

## Collaboration Interfaces

- **CTO**: AI investment decisions, engineering team AI capability building, platform architecture alignment
- **CIO**: AI governance framework, vendor risk management, AI audit and regulatory posture
- **Enterprise Data Architect**: Feature store design aligned to DV2.0; AI platform access to data lake zones
- **Marketing AI Architect**: Marketing-specific AI use case delivery; GenAI content production governance
- **Marketing Model Specialist**: Model development standards compliance; Tier 2 model risk reviews
- **Lead Compliance Officer**: Responsible AI policy; regulatory compliance for algorithmic decisions
- **Data Governance Lead**: PII in AI pipelines; training data lineage and classification
- **Lead Application Architect**: AI API integration patterns; agentic AI action group contracts

## Model Card Standards

Every production model (all tiers) must have a **Model Card** containing:
- Model name, version, risk tier, owner, last review date
- Business objective and decision it informs
- Training data: source tables, date range, label definition
- Feature list with importance ranks (SHAP values for Tier 1/2)
- Performance metrics: AUC, KS, lift, calibration on train/validation/test
- Bias review summary: disparate impact test results by demographic group
- Known limitations and out-of-scope use cases
- Deployment details: endpoint type, scoring frequency, consuming systems
- Human oversight requirements and escalation triggers
- Refresh schedule and retirement criteria

## Common Tasks

1. Evaluate whether a new underwriting AI vendor's model meets the organization's responsible AI standards
2. Design the MLOps pipeline for a new propensity model from training data through production scoring
3. Architect a RAG-based policy FAQ agent using the enterprise AI platform and the company product guide library
4. Define the enterprise feature store structure for marketing behavioral signals
5. Conduct a Tier 1 model risk review for an AI-assisted underwriting ruleset change
6. Evaluate AWS Bedrock vs. third-party LLM provider for a generative content use case
7. Define the agentic AI architecture for a marketing campaign orchestration agent
