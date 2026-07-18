# Tests and Diagnostics

The validation layer: assumption tests, influence detection, hypothesis tests, multiple-comparison corrections, robust covariance, and power/effect-size tools. Run the relevant checks *before* trusting any coefficient or p-value. Imports vary per test and are shown inline.

## Residual Assumption Tests

Fit a model, then interrogate its residuals.

| Concern | Test | Call | H0 |
|---------|------|------|----|
| Autocorrelation | Ljung-Box | `acorr_ljungbox(resid, lags=10, return_df=True)` | no autocorrelation |
| Autocorrelation (1st order) | Durbin-Watson | `durbin_watson(resid)` | ≈2 means none |
| Autocorrelation (general) | Breusch-Godfrey | `acorr_breusch_godfrey(res, nlags=5)` | no autocorrelation |
| Heteroskedasticity | Breusch-Pagan | `het_breuschpagan(resid, exog)` | constant variance |
| Heteroskedasticity (general) | White | `het_white(resid, exog)` | constant variance |
| Volatility clustering | ARCH | `het_arch(resid, nlags=5)` | no ARCH effects |
| Normality | Jarque-Bera | `jarque_bera(resid)` | normal |
| Normality | Omnibus | `omni_normtest(resid)` | normal |
| Normality | Anderson-Darling | `normal_ad(resid)` | normal |
| Normality | Lilliefors | `lilliefors(resid, dist="norm")` | normal |
| Functional form | Ramsey RESET | `linear_reset(res, power=2)` | correctly specified |
| Linearity | Harvey-Collier | `linear_harvey_collier(res)` | linear |

Diagnostic tests live in `statsmodels.stats.diagnostic`; Durbin-Watson, Jarque-Bera, Omnibus in `statsmodels.stats.stattools`. Most return `(stat, p, ...)`; p<0.05 rejects H0.

## Multicollinearity

```python
from statsmodels.stats.outliers_influence import variance_inflation_factor
[variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
```

VIF: >5 moderate, >10 serious, >20 severe. Condition number `res.condition_number`: 10–30 moderate, >30 strong, >100 severe.

## Influence and Outliers

```python
infl = res.get_influence()          # OLSInfluence; GLMInfluence(res) for GLMs
```

| Quantity | Attribute | Flag when |
|----------|-----------|-----------|
| Leverage (hat) | `infl.hat_matrix_diag` | > 2p/n |
| Cook's distance | `infl.cooks_distance[0]` | > 4/n |
| DFFITS | `infl.dffits[0]` | \|·\| > 2·√(p/n) |
| DFBETAs | `infl.dfbetas` | \|·\| > 2/√n (per coefficient) |
| Studentized resid | `infl.resid_studentized_external` | \|·\| > 3 |

`influence_plot(res, criterion="cooks")` combines leverage, residual, and Cook's D in one view (bubble size = influence).

## Hypothesis Tests (standalone)

Means (`scipy.stats`): `ttest_1samp`, `ttest_ind` (add `equal_var=False` for Welch), `ttest_rel` (paired).

Proportions (`statsmodels.stats.proportion.proportions_ztest`): one- or two-sample z-tests on counts/nobs.

Categorical association: `chi2_contingency(table)` (independence), `chisquare(observed, expected)` (goodness of fit), `mcnemar(table, exact=True)` (paired binary), `StratifiedTable` (Cochran-Mantel-Haenszel across strata).

Non-parametric (`scipy.stats`, when normality fails): `mannwhitneyu` (independent), `wilcoxon` (paired), `kruskal` (>2 groups); `sign_test` from `statsmodels.stats.descriptivestats`.

## ANOVA

```python
# one-way
from scipy.stats import f_oneway; f_oneway(g1, g2, g3)
# two-way / factorial
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm, AnovaRM
anova_lm(ols("y ~ C(a) + C(b) + C(a):C(b)", data=df).fit(), typ=2)
AnovaRM(df_long, depvar="score", subject="id", within=["time"]).fit()   # repeated measures
```

## Multiple Comparisons

```python
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.multitest import multipletests
pairwise_tukeyhsd(values, groups, alpha=0.05).summary()
multipletests(pvals, alpha=0.05, method="bonferroni")   # or "fdr_bh" (less conservative)
```

Correct whenever you run many tests — uncorrected multiplicity inflates Type-I error.

## Robust Covariance

Same estimates, defensible SEs:

```python
res.get_robustcov_results(cov_type="HC3")                       # heteroskedasticity (HC0–HC3)
res.get_robustcov_results(cov_type="HAC", maxlags=4)            # + autocorrelation (Newey-West)
res.get_robustcov_results(cov_type="cluster", groups=cluster)   # clustered data
```

## Effect Sizes and Power

Report effect sizes alongside p-values — significance is not magnitude.

- **Cohen's d** = (mean₁ − mean₂) / pooled SD. Guide: 0.2 small, 0.5 medium, 0.8 large.
- **Eta-squared** (ANOVA) = SS_effect / SS_total. Guide: 0.01 / 0.06 / 0.14.

Power / sample size (`statsmodels.stats.power`):

```python
from statsmodels.stats.power import tt_ind_solve_power, TTestIndPower
tt_ind_solve_power(effect_size=0.5, alpha=0.05, power=0.8)   # n per group
tt_ind_solve_power(effect_size=0.5, nobs1=50, alpha=0.05)    # power at given n
TTestIndPower().solve_power(...)                             # for power curves
```

## Descriptives and Group Comparison

```python
from statsmodels.stats.weightstats import DescrStatsW, CompareMeans
d = DescrStatsW(x, weights=w)      # d.mean, d.std, d.tconfint_mean(), d.quantile(...)
cm = CompareMeans(DescrStatsW(g1), DescrStatsW(g2))
cm.ttest_ind(); cm.tconfint_diff(); cm.test_equal_var()
```

## Causal / Treatment Effects

- Propensity scores: fit `Logit(treatment, X)`, predict scores, then match or weight.
- Difference-in-differences: the interaction coefficient in `ols("y ~ treat + post + treat:post", data=df)`.

## Pitfalls

- Skipping assumption tests, then over-trusting the coefficient table.
- Multiple testing without correction.
- Parametric tests on clearly non-normal data — switch to non-parametric.
- Reporting p-values without effect sizes or confidence intervals.
- Conflating statistical significance with practical significance.
- Underpowered study → Type-II errors; check power before concluding "no effect."
