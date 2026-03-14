# Business Statistics & Modeling Reference

## Table of Contents
- [Forecasting Methods](#forecasting-methods)
- [Regression and Causal Modeling](#regression-and-causal-modeling)
- [Scenario and Sensitivity Analysis](#scenario-and-sensitivity-analysis)
- [Statistical Testing for Business Decisions](#statistical-testing-for-business-decisions)
- [Data Quality and Interpretation](#data-quality-and-interpretation)

---

## Forecasting Methods

### Time Series Approaches

| Method | Use When | Strengths | Limitations |
|--------|----------|-----------|------------|
| Moving Average | Stable data, smoothing noise | Simple, intuitive | Lags trend changes |
| Exponential Smoothing | Recent data matters more | Adapts to trend shifts | Sensitive to parameter choice |
| ARIMA | Stationary data with autocorrelation | Rigorous, well-understood | Requires stationarity testing |
| Seasonal Decomposition | Clear seasonal patterns | Separates trend/season/residual | Assumes stable seasonality |
| Growth Curves (S-curve, logistic) | Adoption/saturation dynamics | Models ceilings naturally | Requires ceiling estimate |

### Choosing a Forecast Method
1. **Plot the data first** — visual inspection reveals trend, seasonality, outliers, and structural breaks before any model selection
2. **Start simple** — a naive forecast (last period repeated, or linear trend) is the baseline to beat; complex models must justify their complexity
3. **Test out-of-sample** — always hold out recent data for validation; in-sample fit is not forecast accuracy
4. **State the confidence interval** — a point forecast without a range is incomplete; wider ranges on longer horizons

### Revenue Forecasting Models
- **Bottom-up:** Units × Price, by segment/product/channel — best for businesses with observable demand drivers
- **Top-down:** Market size × Market share × Pricing — useful for market-entry or TAM-based planning
- **Cohort-based:** Retention curves × New cohort acquisition — essential for subscription/recurring revenue
- **Driver-based:** Build from leading indicators (pipeline, traffic, conversion rates) — best when causal relationships are understood

Always triangulate: if bottom-up and top-down give very different answers, investigate why before choosing one.

## Regression and Causal Modeling

### Linear Regression Fundamentals
```
Y = β₀ + β₁X₁ + β₂X₂ + ... + ε
```

**Interpretation rules:**
- β coefficients represent the marginal effect of each X on Y, holding other variables constant
- R² tells you proportion of variance explained — but high R² doesn't prove causation
- p-values test whether the coefficient is statistically distinguishable from zero at a given confidence level
- Always check residual plots for patterns (non-linearity, heteroscedasticity, outliers)

### Common Business Regression Applications
| Application | Dependent Variable | Typical Independent Variables |
|-------------|-------------------|------------------------------|
| Pricing elasticity | Unit sales | Price, competitor price, seasonality, promotions |
| Marketing mix modeling | Revenue or conversions | Spend by channel, seasonality, macro indicators |
| Cost drivers | Total cost | Volume, complexity, headcount, inflation |
| Churn prediction | Churn probability | Usage, tenure, support tickets, engagement score |

### Correlation vs. Causation Checklist
Before claiming X drives Y, verify:
1. **Temporal precedence:** X changes before Y changes
2. **No confounders:** A third variable Z doesn't drive both X and Y
3. **Dose-response:** More X produces proportionally more/less Y
4. **Mechanism:** A plausible causal pathway exists (not just statistical association)
5. **Consistency:** The relationship holds across time periods, segments, or geographies

## Scenario and Sensitivity Analysis

### Scenario Construction
Build scenarios around the 2-3 variables with the highest uncertainty AND the highest impact:

1. **Identify key uncertainties** — what factors does the outcome depend on that we cannot predict?
2. **Define discrete scenarios** — not just high/low but narratively coherent combinations of factor values
3. **Assign probabilities** — subjective but explicit; forces calibration of beliefs
4. **Model each scenario end-to-end** — same model structure, different input assumptions
5. **Define trigger points** — observable signals that indicate which scenario is materializing

### Sensitivity Analysis (Tornado Diagram)
For each key input variable:
```
Variable          Downside ◄══════════════► Upside        Impact Range
─────────────────────────────────────────────────────────
Price elasticity   [-$2.1M] ◄══════════════► [+$1.8M]    $3.9M
Volume growth      [-$1.5M] ◄══════════════► [+$2.0M]    $3.5M
Input costs        [-$1.2M] ◄══════════════► [+$0.8M]    $2.0M
FX rates           [-$0.6M] ◄══════════════► [+$0.5M]    $1.1M
```

Rank variables by impact range. The top 2-3 variables deserve the most analytical attention and the most robust monitoring.

### Break-Even and Threshold Analysis
- **Financial break-even:** Volume or revenue at which total contribution covers fixed costs
- **Project break-even:** Time period at which cumulative cash flows turn positive
- **Decision threshold:** Value of a key variable at which the optimal decision changes (e.g., "if CAC exceeds $X, the channel becomes unprofitable")

Always express thresholds in terms management can observe and act on.

### Monte Carlo Simulation Design
When deterministic scenarios aren't sufficient:
1. **Define distributions** for each uncertain input (normal, triangular, uniform — choose based on what you know about the variable)
2. **Model correlations** between inputs (don't assume independence when variables are related)
3. **Run 1,000+ iterations** — report percentile outcomes (P10, P50, P90)
4. **Present as probability distributions** — "There is a 70% probability that NPV exceeds $X"

## Statistical Testing for Business Decisions

### Hypothesis Testing Framework
1. **State hypotheses:** H₀ (null — no effect) vs. H₁ (alternative — effect exists)
2. **Choose significance level:** α = 0.05 is conventional; for high-stakes decisions, consider α = 0.01
3. **Calculate test statistic** and p-value
4. **Interpret:** p < α → reject H₀ (evidence of effect); p ≥ α → fail to reject H₀ (insufficient evidence)

**Critical nuance:** "Not statistically significant" ≠ "no effect." It means the sample didn't provide enough evidence. Check statistical power — was the sample large enough to detect a meaningful effect?

### A/B Testing for Business Metrics
| Parameter | How to Set |
|-----------|-----------|
| Sample size | Calculate required N for desired minimum detectable effect (MDE) and power (typically 80%) |
| Duration | Run for at least 1-2 full business cycles to capture day-of-week and seasonal effects |
| Significance | α = 0.05 standard; for multiple tests, apply Bonferroni correction |
| Metric | Choose a primary metric tied to business value; track guardrail metrics for unintended harm |

### Common Pitfalls
- **Peeking:** Checking results before the test reaches required sample size inflates false positive rates
- **Multiple comparisons:** Testing 20 metrics at α = 0.05 → expect 1 false positive on average
- **Simpson's paradox:** An effect that appears in aggregate can reverse within segments — always check segment-level results
- **Survivorship bias:** Analyzing only the customers/products that still exist overstates average performance

## Data Quality and Interpretation

### Data Quality Checks (Before Any Analysis)
1. **Completeness:** What percentage of records have missing values? Is missingness random or systematic?
2. **Consistency:** Do related metrics reconcile? (e.g., sum of segment revenue = total revenue)
3. **Timeliness:** How current is the data? Is there a reporting lag that affects conclusions?
4. **Accuracy:** Spot-check against source systems or known benchmarks
5. **Outliers:** Identify extreme values — are they data errors or real phenomena?

### Presentation and Interpretation Rules
- **Base rate:** Always provide the denominator. "Conversion increased 50%" means nothing without knowing if it went from 2% to 3% or from 40% to 60%.
- **Per-unit vs. absolute:** Both matter. Show absolute impact for resource decisions, per-unit for efficiency and scalability.
- **Cohort effects:** Group data by cohort (acquisition date, product version, segment) before averaging — aggregate trends often mask divergent cohort behavior.
- **Leading vs. lagging:** Identify which metrics predict future performance (leading) vs. confirm past performance (lagging). Manage with leading indicators, report with lagging.
