# Hypothesis Testing

## When to Use

Use hypothesis testing when you need to determine whether an observed difference is likely real or could be due to random chance:

- **A/B test results** — is variant B actually better than A?
- **Before/after comparison** — did the product change actually move the metric?
- **Segment comparison** — do enterprise customers really have higher retention?

Do not use it when the difference is obvious and enormous, when nothing changes based on the answer, or when the data is a full population rather than a sample — in a census, every difference is "real" and the question is whether it is *large*.

## The Framework

1. **Null hypothesis (H0)** — there is no difference (the default assumption)
2. **Alternative hypothesis (H1)** — there is a difference
3. **Choose the significance level (alpha)** — typically 0.05 (5% chance of a false positive)
4. **Compute the test statistic and p-value**
5. **Interpret** — if p < alpha, reject H0 (evidence of a real difference)

Fix alpha and the test *before* looking at results. Choosing the test after seeing which one gives p < 0.05 invalidates the p-value.

**What a p-value is:** the probability of seeing a difference this large or larger if there were truly no difference. **What it is not:** the probability the hypothesis is true, the probability the result will replicate, or a measure of effect size.

## Choosing a Test

| Scenario | Test | When to use |
|---|---|---|
| Compare two group means | t-test (independent) | Roughly normal data, two groups |
| Compare two group proportions | z-test for proportions | Conversion rates, binary outcomes |
| Compare paired measurements | Paired t-test | Before/after on the same entities |
| Compare 3+ group means | ANOVA | Multiple segments or variants |
| Non-normal data, two groups | Mann-Whitney U | Skewed metrics, ordinal data |
| Association between categories | Chi-squared | Two categorical variables |
| Small expected cell counts | Fisher's exact | Any expected cell < 5 |

```python
from scipy import stats
from statsmodels.stats.proportion import proportions_ztest, confint_proportions_2indep

# Two means
t, p = stats.ttest_ind(group_a, group_b, equal_var=False)   # Welch — the safer default

# Paired
t, p = stats.ttest_rel(before, after)

# Two proportions
z, p = proportions_ztest([conv_a, conv_b], [n_a, n_b])

# Skewed / ordinal
u, p = stats.mannwhitneyu(group_a, group_b)

# Categorical association
chi2, p, dof, expected = stats.chi2_contingency(contingency_table)

# 3+ groups
f, p = stats.f_oneway(g1, g2, g3)
```

Use `equal_var=False` (Welch's t-test) by default — equal variances are rarely justified and Welch costs almost nothing.

ANOVA tells you *some* group differs, not which. Follow with pairwise tests and a multiple-comparisons correction.

## Practical vs Statistical Significance

**Statistical significance** means the difference is unlikely due to chance.
**Practical significance** means the difference is large enough to matter for the decision.

A difference can be statistically significant and practically meaningless — common with large samples. Always report:

- **Effect size** — how big is the difference? "Variant B improved conversion by 0.3 percentage points"
- **Confidence interval** — the range of plausible true effects
- **Business impact** — what this translates to in revenue, users, or cost

```python
# Difference in proportions with a 95% CI
low, high = confint_proportions_2indep(conv_b, n_b, conv_a, n_a, method='wald')

# Cohen's d for two means
import numpy as np
pooled = np.sqrt((a.std(ddof=1)**2 + b.std(ddof=1)**2) / 2)
d = (b.mean() - a.mean()) / pooled     # ~0.2 small, ~0.5 medium, ~0.8 large
```

The confidence interval is more informative than the p-value: it shows both whether zero is plausible and how large the effect might be. A "significant" result whose CI runs from +0.1 to +5.0 percentage points has not settled the business question.

**A non-significant result is not evidence of no effect.** It means the data cannot distinguish the effect from zero. Report the CI so the reader can see what sizes remain plausible.

## Sample Size and Power

- Small samples produce unreliable results even when the p-value is significant.
- Rule of thumb for proportions: at least 30 events per group for basic reliability — events, not users.
- Detecting small effects (a 1 percentage-point conversion change) takes thousands of observations per group.
- If your sample is small, say so: "With only 200 observations per group, we have limited power to detect effects smaller than X%."

```python
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

# Required n per group for an 18% -> 20% lift, 80% power, alpha 0.05
n = NormalIndPower().solve_power(
    effect_size=proportion_effectsize(0.20, 0.18), alpha=0.05, power=0.8)
```

Run this **before** the test to size it, and **after** a null result to state the minimum detectable effect. "We could not detect anything smaller than a 3-point lift" is a useful finding; "no significant difference" alone is not.

## Reading an A/B Test

1. **Check the assignment** — are the groups balanced on size and on pre-experiment metrics? Imbalance means the randomization or the logging is broken.
2. **Confirm the test ran to its planned duration.** Stopping when it looks good inflates false positives badly.
3. **Use the pre-registered primary metric.** Guardrail and secondary metrics are context, not the verdict.
4. **Report the effect with its CI**, in both relative and absolute terms.
5. **Segment only to generate hypotheses**, never to rescue a null result. A win found in one of eight segments is a multiple-comparisons artifact until it replicates.
6. **Translate to business impact** at full rollout traffic.

Novelty effects, weekday/weekend mix, and sample-ratio mismatch account for more surprising A/B results than genuine product effects. Check them before believing a large lift.

## Reporting Template

> Variant B converted at 20.4% vs 18.1% for control (n = 4,200 per arm), a +2.3 percentage-point absolute lift (+12.7% relative), 95% CI [+0.6, +4.0] pp, p = 0.008. At current traffic that is roughly 1,100 additional conversions per month. The test ran a full 14 days on the pre-registered primary metric; no guardrail metric regressed.
