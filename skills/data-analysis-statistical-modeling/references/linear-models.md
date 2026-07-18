# Linear Models

Regression for continuous outcomes: OLS and its variants for correlated or heteroskedastic errors, quantile regression, and mixed effects. All examples assume `import statsmodels.api as sm` and a design matrix built with `X = sm.add_constant(X_data)`.

## Choosing the Variant

| Situation | Use | Why |
|-----------|-----|-----|
| i.i.d., constant-variance errors | `OLS` | standard baseline |
| Known non-constant variance | `WLS(weights=1/var)` | down-weight noisy observations |
| Known error covariance Σ | `GLS(sigma=Σ)` | general correlated errors |
| Autocorrelated (time series) errors | `GLSAR` or OLS + HAC SEs | serial correlation |
| Parameters drift over time | `RecursiveLS` / `RollingOLS` | detect structural change |
| Care about quantiles / outlier-robust | `QuantReg` | conditional median or tails |
| Grouped / repeated-measures data | `MixedLM` | random effects for clusters |

Rule of thumb: fit OLS first, diagnose, then upgrade only if a diagnostic fails. Often the fix is robust standard errors on the OLS fit rather than a different estimator.

## OLS

```python
X = sm.add_constant(X_data)
res = sm.OLS(y, X).fit()
print(res.summary())
```

Key attributes: `params`, `bse`, `tvalues`, `pvalues`, `rsquared`, `rsquared_adj`, `fittedvalues`, `resid`, `conf_int()`.

Prediction with intervals — `mean_ci_*` is the confidence interval for the mean, `obs_ci_*` the (wider) prediction interval for a new observation:

```python
pred = res.get_prediction(sm.add_constant(X_new)).summary_frame()
pred[["mean", "mean_ci_lower", "mean_ci_upper", "obs_ci_lower", "obs_ci_upper"]]
```

## WLS and Feasible WLS

When variance is known, weight by its inverse. When unknown, estimate it from an OLS pass:

```python
ols = sm.OLS(y, X).fit()
# model log squared residuals to estimate variance
var_hat = sm.OLS(np.log(ols.resid**2), X).fit().fittedvalues
res = sm.WLS(y, X, weights=1/np.exp(var_hat)).fit()
```

## GLS and GLSAR

`GLS(y, X, sigma=Σ)` handles an arbitrary known covariance. For AR(p) errors in time-series regression, `GLSAR(y, X, rho=1).iterative_fit()` estimates the AR structure iteratively; inspect `res.model.rho`.

## Time-Varying Parameters

```python
from statsmodels.regression.recursive_ls import RecursiveLS
from statsmodels.regression.rolling import RollingOLS

rls = RecursiveLS(y, X).fit()      # rls.recursive_coefficients, rls.cusum (structural breaks)
roll = RollingOLS(y, X, window=60).fit()   # roll.params is a DataFrame over time
```

## Quantile Regression

Models conditional quantiles instead of the mean; robust to outliers at q=0.5. Fit each quantile separately and compare coefficients across quantiles to see distributional effects:

```python
from statsmodels.regression.quantile_regression import QuantReg
model = QuantReg(y, X)
fits = {q: model.fit(q=q) for q in [0.1, 0.25, 0.5, 0.75, 0.9]}
```

## Mixed Effects

For nested/hierarchical data (students in schools, repeated measures per subject):

```python
from statsmodels.regression.mixed_linear_model import MixedLM
# random intercept
MixedLM(y, X, groups=group_ids).fit()
# random intercept + slope
MixedLM(y, X, groups=group_ids, exog_re=X_random).fit()
```

## Diagnostics (linear-model specific)

Full test catalog is in `diagnostics.md`; the linear-model essentials:

```python
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.stattools import durbin_watson, jarque_bera
from statsmodels.stats.outliers_influence import variance_inflation_factor

het_breuschpagan(res.resid, X)[1]   # heteroskedasticity p-value
durbin_watson(res.resid)            # ~2 ok; <2 positive autocorr; >2 negative
jarque_bera(res.resid)[1]           # residual normality p-value
[variance_inflation_factor(X.values, i) for i in range(X.shape[1])]  # VIF>10 = collinear
res.get_influence()                 # Cook's D, leverage, DFFITS (see diagnostics.md)
```

## Hypothesis Tests on Coefficients

```python
res.f_test("x1 = x2 = 0")             # joint restriction, formula form
res.f_test(([[0,1,1,0]], [1]))        # linear combination: b1 + b2 = 1
res.wald_test([[0,1,0,0],[0,0,1,0]])  # Wald equivalent
```

## Robust Standard Errors

Keep the OLS point estimates, fix the inference:

```python
res.get_robustcov_results(cov_type="HC3")                      # heteroskedasticity (HC0–HC3; HC3 safest small-n)
res.get_robustcov_results(cov_type="HAC", maxlags=4)           # + autocorrelation (Newey-West)
res.get_robustcov_results(cov_type="cluster", groups=cluster)  # clustered data
```

## Model Comparison

```python
from statsmodels.stats.anova import anova_lm
anova_lm(res_restricted, res_full)   # nested F-test
# non-nested: compare .aic / .bic (lower is better)
```

## Pitfalls

- Missing `add_constant` → no intercept, biased everything.
- Heteroskedasticity ignored → wrong SEs; use WLS or HC SEs.
- Autocorrelated errors with plain OLS SEs → over-confident; use GLSAR or HAC.
- Interpreting coefficients under multicollinearity → check VIF/condition number first.
- Confidence vs prediction intervals confused → prediction intervals are wider.
- Comparing models fit on different row subsets (e.g. after differing NA drops).
