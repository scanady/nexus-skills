---
name: data-analysis-statistical-modeling
disable-model-invocation: false
description: Fit, diagnose, and interpret classical statistical models in Python with statsmodels — OLS/GLM/logit/Poisson/ARIMA — for rigorous inference with coefficient tables, standard errors, and residual diagnostics. Use when you need "a regression with p-values", "logistic regression odds ratios", "time series forecast with confidence intervals", "check heteroskedasticity", or "which model fits this outcome type".
license: MIT
metadata:
  version: "1.0.0"
  domain: data
  triggers: fit a regression in statsmodels, logistic regression odds ratios, poisson count model, arima forecast, test residual assumptions, robust standard errors, pick a model for this outcome, interpret coefficient table
  role: statistician
  scope: inference
---

# Statistical Modeling with statsmodels

Rigorous estimation, inference, and diagnostics — coefficient tables, standard errors, hypothesis tests, residual checks. Reach here when the goal is *understanding and inference* (why, how much, is it significant), not black-box prediction. For pure predictive accuracy, a machine-learning model is usually the better tool.

## Role Definition

You are a statistician working in statsmodels. You match the model to the outcome type, add the intercept, fit, then validate assumptions before trusting any number. You report effect sizes and intervals, not just p-values, and you interpret coefficients on the correct scale (log, logit, link).

## Model Selection — Start Here

Pick by outcome type. Details live in the reference files.

| Outcome | Model | Family / class | Reference |
|---------|-------|----------------|-----------|
| Continuous | OLS (→ WLS/GLS/robust if assumptions fail) | `sm.OLS` | `references/linear-models.md` |
| Continuous, quantiles | Quantile regression | `QuantReg` | `references/linear-models.md` |
| Clustered / repeated measures | Mixed effects | `MixedLM` | `references/linear-models.md` |
| Binary | Logit / Probit | `Logit`, `Probit` | `references/discrete-outcomes.md` |
| 3+ unordered categories | Multinomial logit | `MNLogit` | `references/discrete-outcomes.md` |
| Ordered categories | Ordered logit/probit | `OrderedModel` | `references/discrete-outcomes.md` |
| Counts | Poisson → Negative Binomial if overdispersed | `Poisson`, `NegativeBinomial` | `references/discrete-outcomes.md` |
| Counts, excess zeros | Zero-inflated / hurdle | `ZeroInflated*`, `HurdleCountModel` | `references/discrete-outcomes.md` |
| Non-normal continuous | GLM (Gamma, Inverse Gaussian, Tweedie) | `sm.GLM` | `references/glm.md` |
| Time-ordered | ARIMA / SARIMAX / VAR / ETS | `tsa.*` | `references/time-series.md` |

Assumption tests, influence diagnostics, robust SEs, power/effect size → `references/diagnostics.md`.

## Two Ways to Specify a Model

Array API and R-style formula API are interchangeable; formulas auto-handle categoricals and interactions.

```python
import statsmodels.api as sm
import statsmodels.formula.api as smf

# Array API — ALWAYS add the constant yourself
X = sm.add_constant(X_data)
results = sm.OLS(y, X).fit()

# Formula API — intercept implicit, C() = categorical, : = interaction
results = smf.ols("y ~ x1 + x2 + C(group) + x1:x2", data=df).fit()

print(results.summary())
```

The single most common bug: forgetting `sm.add_constant()` in the array API, which silently drops the intercept.

## Canonical Workflow

1. **Explore** — plot the outcome and predictors; know the outcome type before choosing a model.
2. **Specify** — match model to outcome (table above); add constant / use formula.
3. **Fit** — `results = model.fit()`; check for convergence warnings.
4. **Validate assumptions** — residuals, heteroskedasticity, autocorrelation, normality, multicollinearity, influence (`references/diagnostics.md`). This step is not optional.
5. **Repair if needed** — robust/HAC/cluster SEs, a different family, or a transformation when assumptions fail.
6. **Interpret on the right scale** — raw β for OLS; `exp(β)` for log/logit links (odds ratios, rate ratios, multiplicative effects); report marginal effects for nonlinear models.
7. **Compare** — AIC/BIC for non-nested, likelihood-ratio test for nested, out-of-sample validation for predictive claims.
8. **Report** — coefficients with SEs and confidence intervals, effect sizes, and the diagnostics you ran.

## Reading the Results Object

```python
results.params          # coefficients
results.bse             # standard errors
results.pvalues         # p-values
results.conf_int()      # coefficient CIs
results.fittedvalues    # in-sample predictions
results.resid           # residuals
results.aic, results.bic, results.llf   # fit / comparison
results.predict(X_new)  # predictions on new data
results.summary()       # full table
```

## Interpretation Cheatsheet

| Link / model | `exp(β)` means |
|--------------|----------------|
| OLS (identity) | (no exp) additive change in y per unit x |
| Logit | odds ratio |
| Log-binomial | risk ratio |
| Poisson / log link | rate ratio (multiplicative effect on expected count) |
| Gamma / log link | multiplicative effect on the mean |

## Model Comparison

```python
# Non-nested: lower AIC/BIC wins
pd.DataFrame({"AIC": {n: r.aic for n, r in models.items()},
             "BIC": {n: r.bic for n, r in models.items()}}).sort_values("AIC")

# Nested: likelihood-ratio test
from scipy import stats
lr = 2 * (full.llf - reduced.llf)
p = stats.chi2.sf(lr, full.df_model - reduced.df_model)
```

## Constraints

### MUST DO
- Match the model to the outcome type before fitting
- Add the constant (array API) or use the formula API
- Validate assumptions before trusting coefficients or p-values
- Interpret coefficients on the correct scale for the link
- Report effect sizes and confidence intervals, not p-values alone
- Use robust/HAC/cluster SEs when heteroskedasticity or autocorrelation is present

### MUST NOT DO
- Do not fit OLS to binary, count, or categorical outcomes
- Do not use Poisson when the data are overdispersed — switch to Negative Binomial
- Do not read raw coefficients from a log/logit model as additive effects
- Do not compare non-nested models with a likelihood-ratio test — use AIC/BIC
- Do not fit ARIMA to a non-stationary series without differencing
- Do not ignore convergence warnings

## Reference Files

| File | Covers |
|------|--------|
| `references/linear-models.md` | OLS, WLS, GLS, GLSAR, recursive/rolling, quantile, mixed effects; linear diagnostics, robust SEs, hypothesis tests |
| `references/glm.md` | GLM families, link functions, deviance/dispersion, GLM diagnostics |
| `references/discrete-outcomes.md` | Binary, multinomial, ordinal, count, zero-inflated, hurdle models; marginal effects |
| `references/time-series.md` | Stationarity, ARIMA/SARIMAX, exponential smoothing/ETS, VAR/VARMAX/VECM, forecasting and evaluation |
| `references/diagnostics.md` | Residual/specification tests, influence, multicollinearity, hypothesis tests, multiple comparisons, robust covariance, power and effect sizes |

Official docs: https://www.statsmodels.org/stable/
