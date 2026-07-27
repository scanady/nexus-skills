# Outliers and Anomalies

## Detection Methods

### IQR method — the default

Robust to non-normal distributions. Use this unless you have established the data is roughly normal.

```python
Q1 = df['value'].quantile(0.25)
Q3 = df['value'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
outliers = df[(df['value'] < lower_bound) | (df['value'] > upper_bound)]
```

The 1.5 multiplier is convention, not law — 3.0 flags only extreme outliers. On right-skewed business metrics the upper fence fires often and legitimately; consider applying IQR to `log(value)` instead.

### Z-score method — normal data only

```python
z_scores = (df['value'] - df['value'].mean()) / df['value'].std()
outliers = df[abs(z_scores) > 3]   # more than 3 standard deviations
```

Two failure modes: on skewed data the ±3σ threshold flags a large share of legitimate values, and the outliers themselves inflate the mean and standard deviation that define the threshold. A robust variant fixes the second problem:

```python
med = df['value'].median()
mad = (df['value'] - med).abs().median()
robust_z = 0.6745 * (df['value'] - med) / mad
outliers = df[robust_z.abs() > 3.5]
```

### Percentile method — simplest

```python
outliers = df[(df['value'] < df['value'].quantile(0.01)) |
              (df['value'] > df['value'].quantile(0.99))]
```

This always flags exactly 2% of rows whether or not anything is unusual. Use it for trimming, not for detection.

### Choosing

| Data shape | Method |
|---|---|
| Roughly normal | Z-score |
| Skewed or unknown | IQR |
| Heavy tails, outliers already distorting estimates | Robust z (MAD) |
| Need a fixed trim for reporting | Percentile |

## Handling Outliers

**Do NOT automatically remove outliers.** Classify first:

1. **Investigate** — is this a data error, a genuine extreme value, or a different population?
2. **Data errors** — fix or remove. Negative ages, timestamps in 1970, quantities of 10^9, duplicate submissions.
3. **Genuine extremes** — keep them, and switch to robust statistics (median, IQR) so they do not distort the summary.
4. **Different population** — segment out and analyze separately. Enterprise accounts inside an SMB dataset are not noise; they are a second business.

Removing genuine extremes because they are inconvenient understates variance, narrows confidence intervals, and produces conclusions that will not hold in production.

**Report what you did**, with counts and share:

> "We excluded 47 records (0.3%) with transaction amounts above $50K, which represent bulk enterprise orders analyzed separately."

Alternatives to deletion, when extremes are real but disruptive:

- **Winsorize** — clip to p1/p99 rather than dropping. Preserves sample size.
- **Log transform** — compresses the right tail; often removes the "outlier problem" entirely.
- **Report robust statistics** — median and IQR alongside the mean, with no exclusion at all.

Whatever you choose, run the headline number both ways. If the conclusion flips depending on the outlier treatment, that sensitivity *is* the finding and belongs in the report.

## Time Series Anomaly Detection

For unusual values in a time-ordered metric:

1. **Compute the expected value** — moving average, or same-period-last-year for seasonal series.
2. **Compute the deviation** from expected (the residual).
3. **Flag deviations beyond a threshold** — typically 2–3 standard deviations *of the residuals*, not of the raw series.
4. **Classify the anomaly** — point anomaly (single unusual value) vs change point (sustained shift to a new level).

```python
df['expected'] = df['metric'].rolling(window=28, min_periods=7).mean()
df['residual'] = df['metric'] - df['expected']
sigma = df['residual'].std()
df['anomaly'] = df['residual'].abs() > 3 * sigma
```

Detrend and deseasonalize before thresholding. A residual computed against a flat mean will flag every Monday in a weekly-seasonal series.

### Point anomaly vs change point

| Signal | Reads as | Usual cause |
|---|---|---|
| One day out, then back to normal | Point anomaly | Outage, bot traffic, a campaign, a data-pipeline gap |
| Level shifts and stays shifted | Change point | Release, pricing change, tracking change, definition change |
| Slope changes | Trend break | Market or product shift |

A sustained level shift with no product explanation is a **tracking bug** until proven otherwise. Check instrumentation and metric definitions before writing the business narrative.

### Practical guards

- Missing data reads as a drop to zero. Distinguish "no events" from "no data" before flagging.
- Daily anomaly detection at 3σ on 365 days flags roughly one false alarm per year by construction. Tune the threshold to the alert budget.
- Anomalies cluster. Once one fires, the next few days' residuals are correlated — do not count them as independent detections.
