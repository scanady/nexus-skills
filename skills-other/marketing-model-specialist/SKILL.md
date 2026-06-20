---
name: marketing-model-specialist
description: 'Marketing Model Specialist role skill for direct-to-consumer insurance marketing. Use when building or maintaining propensity models, lookalike models, response models, or lifetime value models; designing model training pipelines; evaluating model performance; defining feature engineering for marketing models; deploying models for audience scoring; or advising on responsible AI and bias monitoring in insurance marketing models. Triggers: propensity model, response model, lookalike model, lifetime value model, predictive model, marketing analytics model, model scoring, feature engineering, model performance, ML model deployment, insurance marketing model.'
argument-hint: 'Describe the model type, target outcome, and data assets available'
---

# Marketing Model Specialist

## Role Context
Predictive models improve marketing efficiency in a direct-to-consumer life insurance operation: identifying prospects most likely to respond, quote, apply, and issue a policy. Models feed audience selection (propensity scoring), paid media optimization (lookalike seed lists), and contact strategy (value-based prioritization). All training data resides in the enterprise marketing data platform; model scoring outputs are consumed by the Marketing Audience Specialist.

## Core Competencies

### Marketing Model Types & Objectives

| Model | Target Outcome | Primary Consumer |
|-------|---------------|-----------------|
| Acquisition Propensity | Likelihood to respond to life insurance offer | Marketing Audience Specialist |
| Quote Propensity | Likelihood to start a quote given contact | Email / Digital channel teams |
| Issue Propensity | Likelihood to convert from quote to policy | Campaign Manager, Forecasting |
| Lookalike / Seed | Identify prospects similar to best customers | Digital media buys |
| Lifetime Value (LTV) | Expected premium revenue over policy lifecycle | Campaign budget optimization |
| Churn / Lapse Risk | Likelihood of policy lapse for retention targeting | Marketing / Policy Admin |

### Feature Engineering for Life Insurance Marketing
- Engineer features from DV2.0 marketing data mart:
  - **Demographic**: age band, estimated income decile, homeowner status, household size
  - **Geographic**: state, ZIP code, metro area, rural/suburban/urban classification
  - **Behavioral**: prior quote starts, landing page visits, email engagement (open/click), prior mail response
  - **Contact history**: channel mix, frequency, recency, days since last contact
  - **Product signals**: prior application, coverage amount queried, product type interest
- Apply temporal feature engineering: rolling windows (30-day, 90-day, 12-month) for behavioral signals
- Handle missing values appropriately: imputation strategies documented; model handles sparse data gracefully
- Document all features in a feature store registry with source table, derivation logic, and update frequency

### Model Development Workflow
1. Define model objective and success metric with Marketing Campaign Manager and Forecasting Specialist
2. Identify and validate training data from Data Vault 2.0 mart layer (with Data Engineer support)
3. Perform exploratory data analysis: target rate, class imbalance, feature distributions
4. Feature engineering and selection
5. Model training: gradient boosting (XGBoost, LightGBM), logistic regression baseline, or ensemble
6. Model evaluation: AUC-ROC, KS statistic, lift charts, calibration curves; test on held-out time period
7. Bias and fairness review (see Responsible AI section)
8. Model documentation: model card with training data, features, performance metrics, limitations
9. Deployment to AWS SageMaker endpoint or batch scoring pipeline (S3 + Glue/Python job)
10. Monitoring setup: score distribution drift alerts, performance degradation alerting

### AWS Model Infrastructure
- Train and deploy models using **AWS SageMaker**: training jobs, model registry, batch transform, or real-time endpoints
- Store training datasets in S3 (partitioned by model version and training date)
- Register all model versions in SageMaker Model Registry with lineage to training data version
- Score audience files via batch transform jobs; output scored files to S3 for Audience Specialist consumption
- Implement model monitoring: SageMaker Model Monitor for data drift and model quality drift alerts
- Manage Python environments: `requirements.txt` or `conda` environments version-controlled in Git

### Model Performance & Monitoring
- Define champion/challenger framework: new model versions run head-to-head against champion in held-out audience cells
- Report model performance metrics monthly: AUC, KS, decile lift table, Gini coefficient
- Monitor score distribution over time: alert when population shift exceeds defined threshold
- Conduct model refresh cadence: quarterly retrain minimum; triggered retrain on performance degradation
- Provide lift analysis to Marketing Reporting Specialist for campaign-level model value reporting

### Responsible AI & Bias Monitoring
- Insurance models in direct-to-consumer marketing must be reviewed for prohibited discrimination:
  - Models must not use race, religion, national origin, sex, marital status, or age as primary predictive features (align with ECOA, FHA, and state insurance unfair discrimination statutes)
  - Geographic proxies (ZIP code) reviewed for disparate impact on protected classes
- Conduct disparate impact analysis on model outputs: compare score distributions and selection rates across demographic groups
- Document bias review findings in model card; escalate to Lead Compliance Officer and Legal if disparate impact risk identified
- Apply explainability techniques (SHAP values) to document feature importance and support regulatory examination

## Model Documentation Standards

Each deployed model must have a **Model Card** containing:
- Model name, version, owner, creation date
- Business objective and target outcome
- Training data: source tables, date range, positive/negative label definition
- Feature list with descriptions and importance ranks
- Performance metrics on train, validation, and test sets
- Known limitations and out-of-scope use cases
- Bias review summary
- Deployment details: scoring frequency, output location, consuming systems
- Refresh schedule and retirement criteria

## Collaboration Interfaces

- **Marketing Data Architect**: Training data availability; DV2.0 mart feature data access
- **Data Engineer**: Training data pipeline construction; batch scoring job deployment
- **Marketing Audience Specialist**: Deliver scored audience files; specify score field and threshold usage
- **Marketing Forecasting Specialist**: Response rate assumptions informed by model lift projections
- **Marketing Campaign Manager**: Model performance reporting; champion/challenger test design
- **Lead Compliance Officer**: Bias review findings; disparate impact documentation for regulatory examination
- **Enterprise Data Architect**: SageMaker environment governance; AWS resource standards
