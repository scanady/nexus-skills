# Discrete Outcome Models

Maximum-likelihood models for binary, categorical, ordinal, and count outcomes. These `discrete` classes add marginal effects, pseudo-R², and count-specific extensions on top of what GLM offers. Assumes `X = sm.add_constant(X_data)`.

## Pick by Outcome Shape

| Outcome | Model | Import |
|---------|-------|--------|
| Binary (odds interpretation) | `Logit` | `statsmodels.discrete.discrete_model` |
| Binary (normal latent, econometrics) | `Probit` | same |
| 3+ unordered categories | `MNLogit` | same |
| Choice with alternative-specific vars | `ConditionalLogit` | `statsmodels.discrete.conditional_models` |
| Ordered categories | `OrderedModel` | `statsmodels.miscmodels.ordinal_model` |
| Counts, mean ≈ variance | `Poisson` | `statsmodels.discrete.count_model` |
| Counts, variance > mean | `NegativeBinomial` | same |
| Counts, excess zeros | `ZeroInflatedPoisson` / `ZeroInflatedNegativeBinomialP` | same |
| Counts, distinct zero process | `HurdleCountModel` | same |

## Binary: Logit / Probit

```python
from statsmodels.discrete.discrete_model import Logit, Probit
res = Logit(y, X).fit()
```

Interpretation:
- Odds ratios: `np.exp(res.params)`; CIs `np.exp(res.conf_int())`. OR>1 raises odds, <1 lowers.
- Marginal effects (often more interpretable than odds): `res.get_margeff().summary()`.
- Probabilities: `res.predict(X)`; classify with a threshold, `(p > 0.5).astype(int)`.
- Pseudo-R²: `res.prsquared`.

Probit vs Logit give near-identical marginal effects; coefficients differ in scale and aren't directly comparable. Evaluate with AUC / classification report on predicted probabilities.

## Multinomial and Conditional Logit

`MNLogit(y, X)` with `y` as integer categories 0..K. One category is the reference; coefficients are log-odds vs reference, `exp(β)` = relative-risk ratios. `res.predict(X)` returns an (n × K) probability matrix; `argmax(axis=1)` is the predicted class.

`ConditionalLogit(y_choice, X_alternatives, groups=id)` handles choice data in long format where regressors vary across alternatives.

## Ordinal

Respect the ordering — do not treat ordered categories as nominal.

```python
from statsmodels.miscmodels.ordinal_model import OrderedModel
res = OrderedModel(y_ordered, X, distr="logit").fit(method="bfgs")   # or distr="probit"
```

The model estimates coefficients plus cutpoints (thresholds between adjacent categories). `res.predict(X)` gives per-category probabilities. The proportional-odds assumption (constant effects across cutpoints) should be checked.

## Counts: Poisson → Negative Binomial

Start with Poisson; it assumes mean = variance.

```python
from statsmodels.discrete.count_model import Poisson, NegativeBinomial
res = Poisson(y, X).fit()          # np.exp(res.params) = rate ratios
res = Poisson(y, X, offset=np.log(exposure)).fit()   # rate model
```

Check overdispersion (`y.var()/y.mean()` ≫ 1, or Pearson dispersion > 1.5). If overdispersed, use Negative Binomial and confirm it wins:

```python
nb = NegativeBinomial(y, X).fit()   # estimates dispersion α
lr = 2 * (nb.llf - Poisson(y, X).fit().llf)
stats.chi2.sf(lr, 1)                # significant → NB preferred
```

## Excess Zeros: Zero-Inflated and Hurdle

When zeros exceed what Poisson/NB predict, two processes are at work.

- **Zero-inflated** — a structural "always zero" class mixed with a count process. `ZeroInflatedPoisson(y, X, exog_infl=X_infl)` (or `ZeroInflatedNegativeBinomialP`). Predict components with `which="prob"` / `which="mean"`.
- **Hurdle** — separate model for zero-vs-positive, then counts among positives. `HurdleCountModel(y, X, exog_infl=X_h, dist="poisson"|"negbin")`.

Example framing: insurance claims — most people never claim (inflation/hurdle stage), some have a count distribution (count stage).

## Diagnostics and Comparison

```python
res.prsquared                          # McFadden pseudo-R²
res.aic, res.bic, res.llf
lr = 2 * (res.llf - res.llnull); stats.chi2.sf(lr, res.df_model)   # vs null
res.wald_test([[0,1,0,0],[0,0,1,0]])   # joint test
```

Binary eval: accuracy/precision/recall/F1/AUC on thresholded predictions. Multinomial: accuracy, per-class report, log-loss on the probability matrix. Counts: compare observed vs predicted frequency distributions (a rootogram-style check).

## Formula API

```python
smf.logit("y ~ x1 + C(group)", data=df).fit()
smf.mnlogit(...); smf.poisson(...); smf.negativebinomial(...)
```

## Pitfalls

- OLS on binary/count/categorical outcomes.
- Poisson under overdispersion → Negative Binomial.
- Reading coefficients as additive instead of log-odds / log-rate.
- Ignoring excess zeros → ZIP/ZINB/hurdle.
- Ordinal outcome modeled as nominal.
- Perfect separation stalling logit/probit convergence — watch the warnings.
- Non-nested models compared with an LR test instead of AIC/BIC.
