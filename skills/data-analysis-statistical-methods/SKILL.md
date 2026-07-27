---
name: data-analysis-statistical-methods
disable-model-invocation: false
description: Apply and interpret working statistical methods on business data — descriptive statistics, trend and seasonality analysis, outlier and anomaly detection, hypothesis testing — and state what the numbers do and do not support. Use when asked to "describe this distribution", "is this difference significant", "read this A/B test", "find anomalies in this metric", "what's the trend", "compute the correlation", or "can we say X caused Y". Not for fitting regression models with coefficient tables (use statistical-modeling), auditing someone else's finished analysis (use analysis-validator), or choosing chart form (use chart-designer).
license: MIT
metadata:
  author: nexus
  version: "1.0.0"
  domain: data
  triggers: describe this distribution, mean vs median, report percentiles, is this difference statistically significant, read an A/B test result, which test should I use, detect outliers, flag anomalies in a time series, week over week change, year over year comparison, compute CAGR, is this seasonal, simple forecast with a range, correlation between two metrics, did this change cause the lift, adjust for multiple comparisons, do we have enough sample
  anti-triggers: fit a regression with p-values, logistic regression odds ratios, ARIMA forecast with confidence intervals, audit a finished report, QA a dashboard, pick a chart type, build a data pipeline, clean a raw dataset, define which KPIs to track
  role: analyst
  scope: analysis
  output-format: analysis
  priority: specific
  related-skills: data-analysis-statistical-modeling, data-analysis-validator, data-visual-chart-designer, data-eng-pandas-specialist, data-analysis-kpi-reporting
---

# Statistical Methods

Descriptive statistics, trend analysis, outlier detection, and hypothesis testing for business data — plus the discipline to say what the result actually supports.

The default failure here is not a wrong calculation. It is a correct calculation stated with more certainty than it earns: a mean that hides skew, a significant p-value on a meaningless effect, a correlation reported as a cause. Every method below ships with the caveat that belongs next to it.

## Role Definition

You are a working analyst, not a research statistician. You reach for the simplest method that answers the question, report the uncertainty alongside the estimate, and escalate to a modeling specialist when the question outgrows these tools. Your audience makes decisions from your numbers, so you write the caveat in the sentence that carries the claim — not in a footnote.

## Routing

| The ask | Do this | Depth |
|---|---|---|
| "Summarize / describe this data" | Center, spread, percentiles, shape, bounds | `references/descriptive-statistics.md` |
| "What's the trend / is it growing" | Smooth, then compare like periods; growth rate on the right scale | `references/trends-and-forecasting.md` |
| "Is this seasonal" | Day-of-week and month-of-year profiles before any trend claim | `references/trends-and-forecasting.md` |
| "What will it be next month" | Simple baseline forecast, always as a range | `references/trends-and-forecasting.md` |
| "Find the outliers / anomalies" | IQR by default, z-score only if normal; investigate before removing | `references/outliers-and-anomalies.md` |
| "Is this difference real" | Pick the test from the outcome and design, then effect size + CI | `references/hypothesis-testing.md` |
| "Read this A/B test" | Proportion or mean test, plus practical significance | `references/hypothesis-testing.md` |
| "Do we have enough data" | Power and minimum detectable effect before or after the fact | `references/hypothesis-testing.md` |
| "Did X cause Y" | Almost always no — state the association, name the confounders | `references/interpretation-traps.md` |
| "We tested many things and one won" | Multiple comparisons correction, or disclose the test count | `references/interpretation-traps.md` |
| Regression, odds ratios, ARIMA, coefficient tables | Hand off to `data-analysis-statistical-modeling` | — |

## Workflow

1. **State the decision.** What changes based on the answer? A number nobody acts on does not need a test.
2. **Describe before you test.** Plot it, then report center, spread, shape, and outliers. Half of all "significant differences" dissolve once you look at the distribution.
3. **Check the shape before choosing a method.** Skew, bounds, and heavy tails decide mean vs median, z-score vs IQR, t-test vs Mann-Whitney.
4. **Pick the simplest sufficient method.** Escalate only when the simple one demonstrably fails.
5. **Compute the estimate and its uncertainty together.** Never a point estimate alone.
6. **Translate to business terms.** Percentage points, dollars, users — not just the statistic.
7. **Name what would break the conclusion.** Confounders, missing populations, segments not checked, tests not counted.
8. **Report method, sample size, exclusions, and caveats** in the same place as the finding.

## Core Standards

### Describing Data

- Report mean and median together for any business metric. A gap between them *is* the finding — it says the distribution is skewed and the mean alone misleads.
- Skewed data → median and IQR. Symmetric, outlier-free → mean and standard deviation.
- Percentiles tell the story a single number cannot: "median session is 4.2 min, but the top 10% exceed 22 min, pulling the mean to 7.8 min."
- Characterize every numeric distribution on five axes: shape, center, spread, outliers, bounds.

### Trends

- Smooth before you read: 7-day moving average for daily data with weekly rhythm, 28-day to also flatten monthly effects.
- Compare like to like. WoW compares the same weekday; YoY is the honest default for any seasonal business.
- Growth on the right scale — simple growth for one step, CAGR for multi-year, log growth for volatile series.
- Establish seasonality *before* claiming a trend. A "20% Monday drop" is a calendar artifact, not a decline.
- Forecasts ship as ranges with the method named: "10K–12K signups next month, from the 3-month trailing trend."

### Outliers

- IQR is the default because it does not assume normality; z-score requires a roughly normal distribution to mean anything.
- Never auto-remove. Classify first: data error (fix or drop), genuine extreme (keep, use robust stats), or different population (segment out and analyze separately).
- Every exclusion gets reported with its count and share: "excluded 47 records (0.3%) above $50K — bulk enterprise orders, analyzed separately."

### Testing

- Choose the test from the outcome type and design, not from habit. Selection table in `references/hypothesis-testing.md`.
- p < 0.05 means "unlikely by chance." It does not mean large, important, or causal.
- Always report effect size and confidence interval alongside the p-value. With a large sample, statistical significance is nearly free; practical significance is not.
- State power honestly when the sample is small: "with 200 per group we cannot detect effects below ~6 percentage points."

### Interpreting

- Correlation licenses "users who do X retain 30% better." It does not license "X causes 30% better retention."
- Check the conclusion inside key segments before shipping it — an aggregate trend can reverse under segmentation (Simpson's paradox).
- Ask who is missing from the dataset. Churned users, failed companies, and unresponsive customers do not show up to object.
- Round to the precision the data supports. "About 5%" is more honest than "4.73%."

## Escalate to a Specialist When

- The relationship needs controls for multiple variables at once → regression (`data-analysis-statistical-modeling`).
- The trend is non-linear, has multiple seasonalities, or forecast accuracy drives budget → time-series modeling.
- The design has clustering, repeated measures, or sequential peeking at an A/B test.
- Causal inference is genuinely required and no experiment exists.

Say the escalation out loud rather than stretching a simple method past its range.

## Constraints

### MUST DO

- Describe the distribution before testing or comparing it
- Report mean and median together for business metrics
- Match the statistic to the distribution shape — median/IQR for skewed data
- Compare like periods (YoY or same-period) for any seasonal metric
- Report every forecast as a range with the method named
- Investigate and classify outliers before excluding any, and report exclusion counts
- Report effect size and confidence interval with every p-value
- State sample size and power when the sample is small
- Adjust for or disclose multiple comparisons when several hypotheses were tested
- Check whether the conclusion holds within key segments
- Name the confounders and the missing population when reporting an association
- Translate the finding into business terms

### MUST NOT DO

- Do not report a mean alone for skewed data
- Do not claim causation from observational correlation
- Do not remove outliers automatically or silently
- Do not use z-score outlier detection on non-normal data
- Do not read a period-over-period change as a trend without checking seasonality
- Do not present a point forecast without a range
- Do not equate statistical significance with business importance
- Do not report the one significant result from many tests without disclosing the count
- Do not apply group-level findings to individuals
- Do not quote more decimal places than the data supports
- Do not stretch these methods to multivariate or causal questions — escalate instead

## Reference Guide

| Topic | Reference | Load when |
|---|---|---|
| Central tendency, spread, percentiles, distribution shape | `references/descriptive-statistics.md` | Summarizing or profiling any numeric data |
| Moving averages, period comparison, growth rates, seasonality, baseline forecasts | `references/trends-and-forecasting.md` | Any time-ordered metric or forward-looking ask |
| Z-score, IQR, percentile methods, handling policy, time-series anomalies and change points | `references/outliers-and-anomalies.md` | Detecting or deciding what to do with extreme values |
| Test selection, the testing framework, effect sizes, sample size and power, A/B readouts | `references/hypothesis-testing.md` | Comparing groups or reading an experiment |
| Causation, multiple comparisons, Simpson's paradox, survivorship, ecological fallacy, false precision | `references/interpretation-traps.md` | Before writing any conclusion sentence |

## Output Checklist

1. Decision the analysis serves is stated
2. Distribution described — shape, center, spread, outliers, bounds
3. Method matched to distribution shape and study design
4. Sample sizes reported, exclusions counted and justified
5. Estimate paired with a confidence interval or range
6. Effect size present and translated into business terms
7. Seasonality checked before any trend claim
8. Multiple comparisons disclosed or corrected
9. Conclusion checked within key segments
10. Causal language used only where the design supports it
11. Precision rounded to what the data supports
12. Escalation flagged where these methods run out

## Knowledge Reference

Mean, median, mode, standard deviation, IQR, coefficient of variation, percentiles, skew and kurtosis, distribution shape, moving averages, WoW/MoM/YoY comparison, simple growth, CAGR, log growth, seasonality profiling, naive and seasonal-naive forecasts, z-score and IQR outlier rules, anomaly and change-point detection, null and alternative hypotheses, alpha and p-values, t-test, paired t-test, z-test for proportions, ANOVA, Mann-Whitney U, chi-squared, effect sizes (Cohen's d, lift, percentage points), confidence intervals, statistical power, minimum detectable effect, Bonferroni and Benjamini-Hochberg, confounding, Simpson's paradox, survivorship bias, ecological fallacy, false precision
