# Time Series

Modeling and forecasting time-ordered data: univariate (AR/ARIMA/SARIMAX, exponential smoothing) and multivariate (VAR family), plus stationarity and residual diagnostics. The cardinal rule: **establish stationarity first**, and never let future information leak into transformations or splits.

## The Standard Path

1. Plot the series — trend? seasonality? changing variance?
2. Test stationarity (ADF, KPSS); difference until stationary.
3. Identify orders from ACF/PACF, or grid-search by AIC.
4. Fit; check residuals are white noise (Ljung-Box).
5. Forecast with prediction intervals; evaluate out-of-sample.

## Stationarity

Two complementary tests with opposite null hypotheses — agreement is reassuring:

```python
from statsmodels.tsa.stattools import adfuller, kpss
adfuller(y)[1]                 # H0: unit root (non-stationary). p<0.05 → stationary
kpss(y, regression="c")[1]     # H0: stationary. p<0.05 → non-stationary
```

Non-stationary → difference (`y.diff().dropna()`) and retest; that difference count is ARIMA's `d`. `seasonal_decompose(y, model="additive", period=s)` or the more robust `STL(y, seasonal=13).fit()` separates trend/seasonal/residual.

## Univariate Models

| Model | Import | Use |
|-------|--------|-----|
| `AutoReg(y, lags=p)` | `tsa.ar_model` | pure AR, stationary series |
| `ARIMA(y, order=(p,d,q))` | `tsa.arima.model` | AR + differencing + MA |
| `SARIMAX(y, order, seasonal_order=(P,D,Q,s), exog=)` | `tsa.statespace.sarimax` | seasonality + exogenous regressors |
| `ExponentialSmoothing` / `ETSModel` | `tsa.holtwinters` / `tsa.exponential_smoothing.ets` | level/trend/seasonal smoothing |

### ARIMA order selection

- **d**: number of differences to reach stationarity (from ADF/KPSS above).
- **p, q**: read the stationary series' PACF (cuts off at `p` → AR) and ACF (cuts off at `q` → MA); both decaying → mixed ARMA.
- Confirm by AIC grid search:

```python
best = min(
    ((p, q) for p in range(5) for q in range(5)),
    key=lambda pq: ARIMA(y, order=(pq[0], d, pq[1])).fit().aic,
)
```

### SARIMAX

`SARIMAX(y, order=(p,d,q), seasonal_order=(P,D,Q,s))` — `s` is the seasonal period (12 monthly, 4 quarterly). Reasonable starting points for monthly data: `(0,1,1)(0,1,1,12)`. Add `exog=` for external drivers; forecasting then requires future exog values. `enforce_stationarity=False, enforce_invertibility=False` helps difficult fits converge.

### Exponential Smoothing / ETS

Level only (simple), + trend (Holt), + trend & seasonality (Holt-Winters). Additive when seasonal swing is constant; multiplicative when it grows with level. `ETSModel` is the state-space formulation and generally more robust:

```python
ETSModel(y, error="add", trend="add", seasonal="add", seasonal_periods=12).fit()
```

## Multivariate

| Model | Use |
|-------|-----|
| `VAR(df)` | several interrelated series, bidirectional dynamics, Granger causality |
| `VARMAX(df, order=(p,q), exog=)` | VAR + MA and exogenous variables |
| `DynamicFactor(df, k_factors, factor_order)` | extract common latent factors |
| `VECM(df, k_ar_diff, coint_rank)` | cointegrated (long-run equilibrium) series |

```python
from statsmodels.tsa.api import VAR
res = VAR(df).fit(maxlags=5, ic="aic")
res.irf(10).plot(orth=True)     # impulse responses
res.fevd(10).plot()             # forecast error variance decomposition
```

Granger causality: `grangercausalitytests(df[["effect","cause"]], maxlag)`. Cointegration screen before VECM: `coint_johansen(df, det_order=0, k_ar_diff=1)`.

## Forecasting

```python
fc = res.get_forecast(steps=h).summary_frame()   # mean, mean_se, mean_ci_lower/upper
res.forecast(steps=h)                             # point forecast only
# SARIMAX with exog: res.get_forecast(steps=h, exog=X_future)
```

Static forecast (`get_prediction`, one-step, uses actuals) vs dynamic (`dynamic=True`, multi-step, feeds its own predictions) — dynamic is the honest test of multi-step skill.

## Residual Diagnostics

Residuals should be indistinguishable from white noise:

```python
from statsmodels.stats.diagnostic import acorr_ljungbox, het_arch
acorr_ljungbox(res.resid, lags=10, return_df=True)   # p>0.05 → no leftover autocorr (good)
het_arch(res.resid, nlags=10)[1]                     # ARCH effects → consider GARCH
res.plot_diagnostics(figsize=(12, 8))                # residuals, hist, Q-Q, correlogram
```

## Out-of-Sample Evaluation

Split by time — never shuffle.

```python
train, test = y[:n], y[n:]
fc = ARIMA(train, order=(1,1,1)).fit().forecast(steps=len(test))
rmse = np.sqrt(mean_squared_error(test, fc))
```

Rolling one-step refits are more realistic than a single long forecast. For cross-validation use `TimeSeriesSplit` (expanding window), not `KFold`. Avoid MAPE when the series has zeros or negatives.

## Advanced

- `ARDL(y, lags, exog, order)` — autoregressive distributed lag, bridges uni/multivariate.
- `MarkovRegression(y, k_regimes=2, order=1)` — regime switching; `smoothed_marginal_probabilities` gives regime membership.
- State-space custom models via `MLEModel` for unobserved components / Kalman filtering / missing data.

## Pitfalls

- Fitting ARIMA to a non-stationary series (skipping `d`).
- Data leakage: transformations or scaling computed over the full series before splitting.
- Wrong seasonal period `s`.
- Overfitting orders; ignoring residual autocorrelation (model is inadequate).
- SARIMAX forecasts without future exog values.
- Confusing static and dynamic forecasts when judging multi-step accuracy.
