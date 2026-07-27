# Descriptive Statistics

## Choosing a Measure of Center

| Situation | Use | Why |
|---|---|---|
| Symmetric distribution, no outliers | Mean | Most efficient estimator |
| Skewed distribution | Median | Robust to outliers |
| Categorical or ordinal data | Mode | Only option for non-numeric |
| Heavily skewed with real extremes (revenue per user, session length) | Median **and** mean | Report both — the gap measures the skew |
| Rates built from counts | Weighted mean over the denominator | Averaging per-group rates double-counts small groups |

**Report mean and median together for business metrics.** When they diverge, the mean alone misleads and the divergence is itself worth stating.

Do not average an average. To get an overall conversion rate, sum numerators and sum denominators — the unweighted mean of segment rates gives a different, usually wrong, number.

## Spread and Variability

| Measure | Definition | Use when |
|---|---|---|
| Standard deviation | Typical distance from the mean | Roughly normal data |
| Interquartile range (IQR) | p75 − p25 | Skewed data, or alongside a median |
| Coefficient of variation (CV) | StdDev / Mean | Comparing variability across metrics on different scales |
| Range | Max − Min | Quick sense of extent; highly outlier-sensitive |
| Median absolute deviation (MAD) | Median of \|x − median\| | Robust alternative to StdDev with heavy tails |

CV is undefined or meaningless when the mean is near zero or the metric can be negative.

## Percentiles

Report percentiles to tell a story a single number cannot:

```
p1    Bottom 1% — floor / minimum typical value
p5    Low end of the normal range
p25   First quartile
p50   Median — the typical user
p75   Third quartile
p90   Top 10% — power users
p95   High end of the normal range
p99   Top 1% — extreme users
```

```python
df['value'].describe(percentiles=[.01, .05, .25, .5, .75, .9, .95, .99])
```

**Example narrative:** "The median session duration is 4.2 minutes, but the top 10% of users spend over 22 minutes per session, pulling the mean up to 7.8 minutes."

Percentiles need volume to be stable. p99 on 200 rows is two observations — say so rather than quoting it as a number.

## Describing a Distribution

Characterize every numeric distribution on five axes:

- **Shape** — normal, right-skewed, left-skewed, bimodal, uniform, heavy-tailed
- **Center** — mean and median, and the gap between them
- **Spread** — standard deviation or IQR
- **Outliers** — how many, how extreme
- **Bounds** — is there a natural floor (zero) or ceiling (100%)?

Bimodality usually means two populations are mixed in one dataset. That is a segmentation finding, not a summary-statistics problem — split and describe each group.

Bounded metrics behave badly near their limits. A conversion rate at 97% cannot improve by 10 percentage points; report headroom, not just change.

## Comparing Distributions

Before running a test, look at the two distributions side by side:

```python
df.groupby('segment')['value'].describe(percentiles=[.25, .5, .75])
```

A difference in means with overlapping IQRs and similar shapes is a small effect regardless of what the p-value says. A difference in shape (one bimodal, one not) means the group means are not comparable quantities at all.

## Correlation

```python
df[['a', 'b']].corr()                     # Pearson — linear, sensitive to outliers
df[['a', 'b']].corr(method='spearman')    # Rank-based — monotonic, robust
```

- Pearson measures **linear** association only. A strong curved relationship can read near zero.
- Spearman is the safer default for skewed business metrics.
- Always plot the scatter before quoting a coefficient — a single outlier can create or destroy a correlation.
- r² is the share of variance explained: r = 0.5 explains 25% of the variation, not half.
- Correlation says nothing about direction of cause. See `interpretation-traps.md`.

## Reporting Template

> Across 12,480 accounts, monthly spend is right-skewed (median $340, mean $612). The IQR runs $180–$690; the top 1% exceed $8,400 and account for 22% of total spend. 47 accounts (0.4%) with zero spend were retained. Percentiles above p95 rest on fewer than 600 accounts.
