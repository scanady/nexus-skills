# Trends and Forecasting

## Smoothing

Raw daily series are too noisy to read a trend from. Smooth first.

```python
# 7-day moving average — removes weekly seasonality in daily data
df['ma_7d'] = df['metric'].rolling(window=7, min_periods=1).mean()

# 28-day moving average — smooths weekly AND monthly patterns
df['ma_28d'] = df['metric'].rolling(window=28, min_periods=1).mean()

# Centered — better for describing history, unusable for the latest point
df['ma_7c'] = df['metric'].rolling(window=7, center=True).mean()
```

- Window length should match the seasonal period you want removed. A 7-day window on daily data removes day-of-week effects exactly.
- `min_periods=1` fills the leading edge but those first points are averages of fewer days — do not read them as trend.
- Trailing averages lag the series by roughly half the window. Do not report a trailing MA as "the current level."

## Period-over-Period Comparison

| Comparison | Compares | Use for |
|---|---|---|
| Week-over-week (WoW) | Same weekday, 7 days apart | Fast-moving operational metrics |
| Month-over-month (MoM) | Same month prior | Medium-horizon movement; watch unequal month lengths |
| Year-over-year (YoY) | Same period last year | The honest default for any seasonal business |
| Same-day-last-year | Specific calendar day | Holiday-sensitive metrics |

MoM comparisons are contaminated by month length (28 vs 31 days is an 11% swing) and by the number of weekends in the month. Use a daily average within the month, or compare YoY.

## Growth Rates

```
Simple growth:  (current - previous) / previous
CAGR:           (ending / beginning) ** (1 / years) - 1
Log growth:     ln(current / previous)        # better for volatile series
```

- CAGR is a smoothed rate, not a description of the path. A metric that fell 50% then rose 300% has a fine CAGR and a terrible story — show the series.
- CAGR is meaningless when the starting value is near zero or negative.
- Simple growth is asymmetric: −50% then +50% does not return to start. Log growth is symmetric and additive, which is why it is preferred for volatile series.
- Percentage change on a small base is noise. State the absolute numbers next to any large percentage: "+300% (from 4 to 16 accounts)."
- Percentage points ≠ percent. A conversion rate moving 2.0% → 2.6% is +0.6 percentage points, or +30% relative. Name which one you mean.

## Seasonality

Establish seasonality **before** claiming a trend. Check in this order:

1. **Plot the raw series.** Visual inspection first — most seasonality is obvious.
2. **Day-of-week profile.** Is there a clear weekly pattern?
3. **Month-of-year profile.** Is there an annual cycle?
4. **Compare like periods only.** YoY or same-period comparisons keep trend and seasonality from being confused.

```python
df['dow'] = df['date'].dt.day_name()
df.groupby('dow')['metric'].mean().reindex(
    ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'])

df.groupby(df['date'].dt.month)['metric'].mean()
```

Also check for calendar effects that are not strictly seasonal: holidays, billing cycles, marketing sends, release dates, and pay periods. A recurring spike on the 1st of the month is a billing artifact, not demand.

Two or more years of history are needed before an annual pattern is a pattern rather than a coincidence.

## Simple Forecasting

For business analysts — not data scientists — these baselines are usually sufficient and always worth computing first:

| Method | Rule | Use as |
|---|---|---|
| Naive | Tomorrow = today | The baseline any other method must beat |
| Seasonal naive | Tomorrow = same day last week / last year | Baseline for seasonal series |
| Moving average | Forecast = trailing average | Stable, low-trend series |
| Linear trend | Fit a line to history | Only for clearly and persistently linear trends |

**Always communicate uncertainty.** Give a range, not a point estimate:

- "We expect 10K–12K signups next month based on the 3-month trend"
- Not "We will get 11,234 signups next month"

Derive the range from history rather than intuition — for example, the spread of the last 6–12 same-period actuals around their own trailing forecast.

Name the method with the number. "Seasonal naive, 3-month lookback" tells the reader how much to trust it; a bare figure does not.

## When to Escalate

Hand off to time-series modeling (`data-analysis-statistical-modeling`) when:

- The trend is clearly non-linear
- There are multiple overlapping seasonalities (weekly and annual)
- External drivers matter — marketing spend, pricing changes, holidays
- Forecast accuracy drives resource allocation or a budget commitment
- You need calibrated prediction intervals rather than a plausible range

Say so explicitly rather than extending a linear fit past its useful range.
