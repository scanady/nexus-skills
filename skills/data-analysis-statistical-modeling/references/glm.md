# Generalized Linear Models

GLMs extend linear regression to non-normal responses via three pieces: a **distribution family** (conditional response distribution), a **link function** `g` where `g(μ) = Xβ`, and an implied **variance function**. Fit by iteratively reweighted least squares (IRLS). Assumes `import statsmodels.api as sm` and `X = sm.add_constant(X_data)`.

Use GLM when the outcome is non-normal but you want the regression framework: binary, counts, positive-skewed, or semi-continuous. For discrete outcomes specifically, the dedicated `Logit`/`Poisson`/`NegativeBinomial` classes in `discrete-outcomes.md` give richer post-estimation (marginal effects, pseudo-R²); GLM is the unified interface and the home for Gamma/Inverse Gaussian/Tweedie.

## Families and When to Reach for Them

| Family | Outcome | Default (canonical) link | `exp(β)` interprets as |
|--------|---------|--------------------------|------------------------|
| `Binomial` | binary / proportion | logit | odds ratio (risk ratio with log link) |
| `Poisson` | counts | log | rate ratio |
| `NegativeBinomial` | overdispersed counts | log | rate ratio |
| `Gamma` | positive, right-skewed (cost, duration) | inverse (use log for interpretability) | multiplicative effect on mean |
| `InverseGaussian` | positive skewed, var ∝ μ³ | inverse-squared | — |
| `Gaussian` | continuous (≡ OLS via IRLS) | identity | additive |
| `Tweedie` | semi-continuous, zeros + positives (insurance) | log, `var_power` | multiplicative |

Tweedie power `p`: 0=Normal, 1=Poisson, 2=Gamma, 3=Inverse Gaussian; `1<p<2` = compound Poisson-Gamma (claims).

```python
sm.GLM(y, X, family=sm.families.Poisson()).fit()
sm.GLM(y, X, family=sm.families.Gamma(link=sm.families.links.Log())).fit()
smf.glm("success ~ x1 + x2", data=df, family=sm.families.Binomial()).fit()
```

## Link Functions

Available: `Identity`, `Log`, `Logit`, `Probit`, `CLogLog`, `InversePower`, `InverseSquared`, `Sqrt`, `Power(power=p)` (under `sm.families.links`).

Use the canonical link unless you have a reason:
- Log link on Binomial → **risk ratios** instead of odds ratios.
- Identity → additive effects (only when predictions stay in the valid range).
- Probit vs Logit → nearly identical fit; choose by field convention. Coefficients aren't directly comparable (scale differs); marginal effects are.
- CLogLog → asymmetric response, common in survival/discrete-hazard.

## Offsets for Rate Models

When modeling a rate (counts per exposure), pass `offset=np.log(exposure)` so `log(μ) = log(exposure) + Xβ`. Forgetting the offset is a classic rate-model bug.

## Results and Fit Statistics

```python
res.params, res.bse, res.pvalues, res.conf_int()
res.fittedvalues            # μ̂
res.aic, res.bic, res.llf, res.deviance, res.null_deviance, res.pearson_chi2, res.df_resid
res.resid_deviance, res.resid_pearson, res.resid_response, res.resid_anscombe
```

McFadden-style pseudo-R²: `1 - res.deviance / res.null_deviance`.

## Dispersion and Goodness of Fit

Dispersion should be ≈1. Over/under-dispersion signals the wrong family:

```python
dispersion = res.pearson_chi2 / res.df_resid   # >1.5 → overdispersed
```

Poisson overdispersed → switch to Negative Binomial. Deviance and Pearson χ² each test overall fit against `chi2.sf(stat, df_resid)`.

## Diagnostics

```python
from statsmodels.stats.outliers_influence import GLMInfluence
infl = GLMInfluence(res)
infl.cooks_distance[0]      # influence; flag > 4/n
infl.hat_matrix_diag        # leverage
```

Plot deviance residuals vs fitted (should be patternless) and a Q-Q of deviance residuals (roughly normal). See `diagnostics.md` for the full influence toolkit.

## Hypothesis Tests and Comparison

```python
# nested: likelihood-ratio test
from scipy import stats
lr = 2 * (full.llf - reduced.llf)
stats.chi2.sf(lr, full.df_model - reduced.df_model)

res.wald_test([[0,1,0,0],[0,0,1,0]])   # joint Wald
# non-nested: compare AIC/BIC
```

Robust SEs via `res.get_robustcov_results(cov_type="HC0" | "cluster", groups=...)`.

## Prediction

`res.predict(X_new)` returns μ (probabilities for Binomial, expected counts for Poisson). Analytic prediction intervals aren't standard for GLMs — bootstrap when you need them (resample rows, refit, take percentiles of predictions).

## Worked Interpretations

- **Logistic**: `np.exp(res.params)` = odds ratios; `np.exp(res.conf_int())` = their CIs. Evaluate with AUC/classification report on `res.predict(X)`.
- **Poisson**: `np.exp(res.params)` = rate ratios; check dispersion before trusting SEs.
- **Gamma + log link**: `np.exp(res.params)` = multiplicative effect on the mean cost/duration.

## Pitfalls

- Wrong family for the outcome → check the response distribution first.
- Overdispersed Poisson → Negative Binomial.
- Coefficients read on the linear-predictor scale instead of transformed by the link.
- Missing offset in a rate model.
- IRLS non-convergence (e.g. complete separation in logistic) ignored — read the warnings.
- Identity link producing out-of-range predictions for bounded outcomes.
