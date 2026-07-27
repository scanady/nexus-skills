# Interpretation Traps

Read this before writing any conclusion sentence. Each trap below turns a correct calculation into a wrong claim.

## Correlation Is Not Causation

When you find a correlation, explicitly consider:

- **Reverse causation** — maybe B causes A, not A causes B
- **Confounding variables** — maybe C causes both A and B
- **Selection** — the association exists only because of how the sample was assembled
- **Coincidence** — with enough variables, spurious correlations are inevitable

**What you can say:** "Users who use feature X have 30% higher retention."
**What you cannot say without more evidence:** "Feature X causes 30% higher retention."

The most common confounder in product analytics is **engagement**: users who do more of anything retain better. Any feature-usage-vs-retention finding needs engagement controlled or acknowledged.

Causal language is earned by design, not by sample size. Randomized experiments earn it. Observational data earns it only with an explicit identification strategy — and that is a modeling job, not this skill's.

Write associations in association language: "is associated with", "users who … also …", "higher X coincides with higher Y". If a stakeholder will read your sentence as causal, rewrite it.

## Multiple Comparisons

When you test many hypotheses, some will be "significant" by chance:

- Testing 20 metrics at alpha = 0.05 means roughly 1 false positive by construction.
- If you examined many segments before finding one that differs, that search is part of the analysis and must be disclosed.
- Correct with Bonferroni (divide alpha by the number of tests), or report how many tests were run.

```python
from statsmodels.stats.multitest import multipletests

# Bonferroni — strict, controls the chance of ANY false positive
reject, p_adj, _, _ = multipletests(pvals, alpha=0.05, method='bonferroni')

# Benjamini-Hochberg — controls the false discovery rate; better for exploration
reject, p_adj, _, _ = multipletests(pvals, alpha=0.05, method='fdr_bh')
```

Bonferroni for confirmatory decisions where a false positive is costly. Benjamini-Hochberg for exploratory scans where you want a ranked candidate list.

The correction cannot be applied honestly if you do not know how many comparisons were made. Count them as you go — including the segments you looked at and abandoned.

## Simpson's Paradox

A trend in aggregated data can reverse when the data is segmented.

- Always check whether the conclusion holds across key segments.
- Example: overall conversion goes up while conversion falls in *every* segment — because the traffic mix shifted toward a higher-converting segment.

Any aggregate change has two components: within-segment change, and mix shift between segments. When they point in opposite directions, the aggregate number is telling you about the mix, not the performance. Decompose before drawing a conclusion:

```python
df.groupby(['period', 'segment']).agg(
    conversions=('converted', 'sum'), users=('user_id', 'count'))
```

Check the segment weights alongside the segment rates. Both changed, and only one is usually the story.

## Survivorship Bias

You can only analyze entities that survived to be in the dataset:

- Analyzing active users ignores those who churned
- Analyzing successful companies ignores those that failed
- Analyzing completed sessions ignores those that crashed
- Analyzing survey responses ignores everyone who did not respond

Always ask: **"Who is missing from this dataset, and would their inclusion change the conclusion?"**

Usually it would, and in a predictable direction. Say which direction: "This overstates retention, since users who churned before day 7 are not in the cohort."

## Ecological Fallacy

Aggregate trends may not apply to individuals:

- "Countries with higher X have higher Y" does **not** mean "individuals with higher X have higher Y"
- "Accounts on the enterprise plan use more seats" does not mean any particular account will
- Group-level correlations can even carry the opposite sign to individual-level ones

Match the unit of analysis to the unit of the decision. If the decision is about individual users, analyze individual users.

## Anchoring on False Precision

Be wary of implying more certainty than the data supports:

- "Churn will be 4.73% next quarter" implies precision that does not exist
- Prefer ranges: "We expect churn between 4% and 6% based on historical patterns"
- Round appropriately: "about 5%" is often more honest than "4.73%"

Precision should reflect sample size. A rate from 200 observations does not support two decimal places. Percentages from small counts should carry the count: "12% (6 of 50)."

## Regression to the Mean

Extreme values tend to be less extreme on remeasurement, with no intervention required.

- The worst-performing stores will improve next quarter on their own
- Users flagged for unusually low engagement will look better next week
- Any intervention targeted at an extreme group will appear to work

Whenever a group was selected *because* it was extreme, you need a control group before crediting the intervention.

## Base Rates and Denominators

- A 3× higher rate on a tiny base is often noise: "+200% (from 2 to 6 events)."
- Always show the denominator. "40% of respondents" means something different at n = 15 and n = 15,000.
- Rates and counts move independently. Signups can rise while the signup *rate* falls, if traffic rose faster.
- Changing the denominator mid-series (a definition change) creates a fake trend. Verify metric definitions are stable across the whole window before reading movement.

## Checklist Before You Ship a Conclusion

1. Is the causal language earned by the design, or should this read as an association?
2. How many comparisons were made, and is that disclosed or corrected?
3. Does the conclusion hold within key segments, or is it a mix shift?
4. Who is missing from the dataset, and which way does that bias the result?
5. Does the unit of analysis match the unit of the decision?
6. Is the stated precision supported by the sample size?
7. Was the group selected for being extreme?
8. Is the denominator visible and stable across the whole window?
