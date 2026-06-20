---
name: marketing-forecasting-specialist
description: 'Marketing Forecasting Specialist role skill for direct-to-consumer insurance marketing. Use when building marketing response forecasts, projecting policy issuance volumes, modeling CPL and CPA estimates, developing annual marketing volume plans, building scenario models for channel mix decisions, analyzing historical response trends, consuming propensity and LTV model outputs for forecast calibration, or providing financial projections for marketing budget justification. Triggers: marketing forecast, response rate forecast, volume projection, CPL forecast, CPA model, policy issuance projection, marketing ROI, scenario modeling, marketing budget justification, response trend analysis, propensity model, behavioral signal.'
argument-hint: 'Describe the forecast need, time horizon, and available historical data'
---

# Marketing Forecasting Specialist

## Role Context
The marketing organization must project lead volumes, quote rates, application counts, and issued policy counts to set budgets, staff contact centers, and meet business targets. The Marketing Forecasting Specialist builds and maintains the quantitative models that translate marketing activity (campaign mailings, email sends, digital impressions) into expected business outcomes — and tracks forecast accuracy against actuals using the enterprise marketing data platform.

## Core Competencies

### Marketing Response Forecasting
- Build and maintain response rate models by channel, product, audience segment, and season:
  - **Direct mail**: response rate (%) → lead rate → quote rate → application rate → issue rate
  - **Email**: open rate → click rate → quote start rate → application rate → issue rate
  - **Paid search**: CTR → landing page conversion rate → quote start rate → issue rate
- Apply response funnel modeling: top-of-funnel contact volume → conversion rates at each stage → issued policy forecast
- Incorporate seasonal indices: response rates vary significantly by month/quarter; apply seasonality factors to base rate assumptions
- Stratify forecasts by audience segment: acquisition vs. re-engagement; age band; state; product type

### Volume Planning & Business Alignment
- Translate business targets (policy issuance goals, premium revenue goals) into required marketing activity volumes:
  - Given a target of X issued policies, what contact volume is required by channel?
  - What budget is required to achieve X contacts at current CPL?
- Build top-down and bottom-up forecast reconciliation:
  - **Top-down**: from business revenue target to required contact volume
  - **Bottom-up**: from planned campaign calendar to projected response count
- Present forecast to Marketing leadership and Finance as part of annual planning and quarterly reforecast cycles

### CPL / CPA / ROI Modeling
- Define and maintain cost-per-outcome models:
  - **CPL** (Cost Per Lead): total campaign spend ÷ total leads generated
  - **CPQ** (Cost Per Quote): total spend ÷ quotes started
  - **CPA** (Cost Per Application): total spend ÷ applications submitted
  - **CPIP** (Cost Per Issued Policy): total spend ÷ issued policies
- Build marketing ROI models: compare lifetime value (LTV) of acquired policies to CAC (Customer Acquisition Cost)
- Model channel efficiency comparisons: digital CPL vs. direct mail CPL adjusted for response quality (issue rate difference)
- Provide CPL/CPA benchmarks for campaign brief development (Marketing Planning Specialist)

### Scenario & Sensitivity Modeling
- Build scenario models for planning decisions:
  - "If we increase direct mail volume 20%, what is the incremental policy projection and cost?"
  - "If email response rates decline 15% due to deliverability challenges, what is the revenue impact?"
  - "What is the optimal channel mix to hit X issued policies at minimum CPL?"
- Define sensitivity analyses: which input assumptions have the greatest impact on forecast outcomes?
- Present scenarios to Marketing leadership with clear assumption sets and confidence ranges

### Forecast Accuracy Tracking
- Compare forecasted response rates and volumes to actuals at 30, 60, 90-day post-campaign windows
- Maintain a forecast accuracy log: MAPE (Mean Absolute Percentage Error) by campaign type and channel
- Identify systematic forecast biases: consistent over/under-prediction by segment → update base rate assumptions
- Report forecast accuracy scorecard quarterly to Marketing leadership

### Data Platform Interaction
- Query Redshift marketing data mart for historical response, conversion, and cost data to calibrate models
- Define required data fields for forecasting: campaign contact date, response date, quote date, application date, issue date, actual spend — coordinate with Marketing Data Architect for mart availability
- Build and maintain forecasting models in Python (pandas, scipy) or SQL organized in the AWS data platform
- Maintain versioned forecast assumption tables in the data platform for audit trail

## Forecasting Model Framework

```
Contact Volume
    × Response Rate (by channel, segment, season)
= Leads Generated
    × Quote Rate
= Quotes Started
    × Application Rate
= Applications Submitted
    × Issue Rate
= Policies Issued
    × Average Annual Premium
= Projected Premium Revenue

÷ Total Campaign Spend
= Marketing ROI
```

## Key Metrics & Reporting Cadence

| Metric | Reporting Frequency |
|--------|-------------------|
| Campaign-level forecast vs. actual | Post-campaign (30/60/90 days) |
| Monthly volume forecast vs. plan | Monthly |
| Annual forecast recast | Quarterly |
| Forecast accuracy (MAPE) | Quarterly |
| Channel efficiency scorecard (CPL, CPIP) | Monthly |

## DTC Insurance Forecasting Considerations

> See `nyl-direct-context` — Marketing section — for how simplified underwriting, print response accumulation, state-level variation, and multi-touch attribution dynamics shape forecasting here.

## Collaboration Interfaces

- **Marketing Planning Specialist**: Provide response rate assumptions and volume targets for campaign briefs
- **Marketing Campaign Manager**: Deliver campaign volume projections; track and report actuals vs. forecast
- **Marketing Reporting Specialist**: Receive actual performance data to feed forecast accuracy tracking
- **Marketing Model Specialist**: Consume model lift projections to adjust propensity-based audience forecasts
- **Finance**: Deliver marketing volume and revenue forecasts for financial planning
- **Marketing Audience Specialist**: Coordinate universe sizing estimates with forecast assumptions
- **Data Engineer**: Request BigQuery and Redshift data pipeline access for behavioral signal integration into forecasting models
- **Marketing AI Architect**: Coordinate SageMaker model output consumption; receive propensity scores, LTV estimates, and response predictions for forecast calibration

## SageMaker ML Integration for Forecasting

The composable stack includes a **ML platform** (e.g., AWS SageMaker or equivalent) for propensity modeling, LTV estimation, and response prediction. The Marketing Forecasting Specialist consumes model outputs as inputs to forecasting models — rather than relying solely on historical average response rates.

### ML-Assisted Forecast Calibration
- **Propensity-weighted forecasts**: Rather than applying a flat segment response rate, consume audience propensity scores from SageMaker to produce a score-distribution-weighted response forecast. A 10,000-name audience scored by propensity model will produce a materially different forecast than the same 10,000 names forecasted at the segment average response rate.
- **LTV-adjusted CPL targets**: Consume SageMaker LTV model outputs to set CPL targets that reflect the expected lifetime premium revenue of the audience being targeted, not just the single-campaign acquisition cost. High-LTV audiences may warrant a higher CPL budget; low-LTV audiences may need tighter CPL constraints.
- **Model-vs-actual tracking**: Maintain a forecast accuracy log that separately tracks model-assisted forecasts vs. historical average forecasts. If SageMaker propensity models are adding lift to forecast accuracy (lower MAPE), this is evidence to invest further in model development. If model-assisted forecasts are not materially more accurate, escalate to the Marketing Model Specialist.

### Behavioral Signal Integration from BigQuery
The real-time behavioral event pipeline (Year 1) accumulates behavioral event data in a streaming analytics store — data not available in the transactional mart. This creates new forecasting dimensions:

- **Quote-to-abandon rate**: What percentage of quote starts abandon before completion? How does this vary by entry channel (email click, paid search, direct mail BRE)? This rate is now observable in real-time from BigQuery event data rather than inferred from delayed transactional records.
- **Re-engagement signal value**: How much more likely is a prospect who has returned to the website after a 30-day absence to convert vs. a prospect who has not visited? This signal can be used to weight re-engagement campaign volume forecasts.
- **Cross-channel sequence impact**: Does a prospect who receives both a direct mail piece and a triggered email in the same window convert at a higher rate than single-channel contacts? This cross-channel lift factor is measurable from BigQuery event sequences joined to Redshift response records, and should be incorporated in cross-channel campaign volume forecasts.

## Strategic Transformation Hypothesis Validation Forecasting

When a marketing transformation roadmap defines strategic hypotheses to be validated, the Marketing Forecasting Specialist is responsible for the **quantitative validation framework** for each hypothesis:

| Hypothesis | Validation Metric | Forecasting Role |
|---|---|---|
| **Trigger Events Response Value**: Are trigger-based campaigns more effective than batch campaigns? | Triggered vs. batch response rate lift; triggered CPL vs. batch CPL | Build side-by-side forecast models for triggered vs. batch campaigns; track actuals vs. both forecasts to measure true lift |
| **Audience Granularity Value**: Does granular segmentation produce better outcomes than broad segments? | Response rate lift for fine-segment vs. broad-segment audiences of comparable size | Model expected response by segment granularity level; track whether actual response matches or exceeds the model prediction for granular segments |
| **Journey Orchestration Value**: Does multi-touch journey orchestration produce higher lifetime conversion rates? | Multi-touch conversion rate vs. single-touch conversion rate; journey-attributed policy rate | Build journey-attributed volume forecast; track policy issuance attributable to multi-step journeys vs. single-touch contacts |
| **Cross-Channel Coordination Value**: Does coordinated multi-channel contact produce higher response than single-channel? | Cross-channel contact response rate vs. single-channel contact response rate | Maintain separate forecast tracks for cross-channel coordinated audiences and single-channel audiences; MAPE tracking per hypothesis |
