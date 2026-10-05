# Statistical Honesty

Why most social "insights" are noise, and the gates the scripts apply to stop that. The sentence to prevent: "videos do 3x better for me", built on four posts. With results this skewed, four posts will show a 3x gap between almost any two groups, including groups defined by the first letter of the title.

## The gates

A candidate pattern must pass all four. Most fail at the first two.

### 1. Size floor: 5 posts in, 5 out

Under five, a group median is one or two posts. Such candidates are `NOT_TESTED` and stay out of the multiple-comparisons family. "Not enough data yet" is a real finding.

### 2. Permutation test

Shuffle the group labels many times; recompute the difference of medians each time; ask how often random labels give a gap at least as large as the observed one (two-sided).

- No distribution assumption. A t-test expects roughly normal data; engagement is not, and one breakout post decides a mean on its own.
- **Exact** when the number of ways to pick the group is at most 20,000 (it enumerates them all). Otherwise **Monte Carlo** with 5,000 shuffles and `(extreme + 1) / (shuffles + 1)`, so p is never 0.
- Fixed seed. Same data and flags give the same verdict. An analysis tool that changes its answer on re-run is not one.
- Assumption: posts are interchangeable under the null. A trend over time breaks that. The scripts compute the Spearman correlation of the metric with post order and warn at |rho| of 0.4 or more. Then read every p-value as optimistic.

### 3. Multiple-comparisons correction

Test ten candidates at alpha 0.10 and about one passes on noise alone. Test twenty and about two do. Correction is the answer; a note about it is not.

- The **family** is every candidate that cleared the size floor. It is counted before the effect floor is applied. Counting only the candidates with a big observed effect would undercount the family, because a big observed effect and a small p-value come from the same data.
- **Benjamini-Hochberg** (default) controls the false discovery rate: among the patterns reported, the expected share that are false is at most alpha. Right for exploratory screening.
- **Holm** controls the family-wise error rate: the chance of any false pattern at all is at most alpha. Stricter; use when a single false lead is costly.
- `none` exists to show what correction removes. Never report from it.
- Skipped on purpose: for a two-level attribute, "video vs rest" and "text vs rest" are one comparison. Counting both double-counts.
- Levels of one attribute share posts, so they are not independent. Read the group as one question.

Measured on 200 simulated no-effect datasets (40 posts, three declared attributes, one-vs-rest groups, effect floor 15%): no correction reported at least one "pattern" in 63% of datasets; BH and Holm each in 5%. Re-run that check if you change the defaults.

### 4. Effect floor: 15% relative difference in medians

A real 3% difference changes no decision, so it is not reported as a pattern (`TOO_SMALL`). Set the floor to the size at which you would actually act.

### Also reported

- A 90% bootstrap interval for the relative effect. When it spans zero or runs from near zero to large, the effect is fragile even if the p-value passed.
- A time-confounding flag per group (Spearman of group membership against post order). A group concentrated in one period is mixed up with that period.

## Forking paths

Even without formally testing twenty things, an analyst who would have tried a different cut had the data looked different is effectively multiple-testing (Gelman and Loken). The defense is to declare candidates before looking: pass `--attribute` explicitly. With no declaration the script tests every low-cardinality text column plus weekday, and counts all of them.

Rules that follow:
- Choose attributes before opening results.
- Do not re-slice after a "nothing survived" verdict. That verdict is the result.
- Numeric splits use the median, not a cut chosen after the data was seen.

## Why a surviving pattern is still a hypothesis

The finding comes from posts you already wrote, chosen for reasons that correlate with everything else about them. Videos may have gone out when you had better material, on easier topics, in better weeks. No statistic on the same data removes confounding. Only a planned test does: name the variable first, randomize arm order, hold other things constant, run the window. `size_experiment.py` plans it.

## Power and the uncomfortable arithmetic

Sizing uses the log scale. A lift of `e` is a mean shift of `ln(1 + e)` between arms, spread `sigma_log`:

```
n per arm = 2 (z_alpha/2 + z_power)^2 sigma_log^2 / ln(1 + e)^2  +  z_alpha/2^2 / 4
```

- That is the normal-theory size. The planned analysis is a permutation test on medians, which is a little less efficient on skewed data. `--simulate` runs the actual test on simulated data and grows n until simulated power reaches the target within one standard error. Example: at sigma_log 0.45 and a 30% lift, the formula gives 38 per arm and the simulation found 68% power there; it raised n to 47.
- `--comparisons k` splits alpha across k planned comparisons (Bonferroni). Looking at more than one thing costs posts.
- At sigma_log 0.35-0.6 and a 30% lift, expect roughly 25-80 posts per arm after the simulation check. At three posts a week that is 17-53 weeks.

So many tests people describe are not runnable at their volume. Honest responses:
- Test only variables where you expect a large lift.
- Accept a large minimum detectable lift, and say so (the script returns it).
- Skip the test and write what you would rather write.

## What is not evidence

- One post that did well. The commonest cause of a strategy change and the least informative event.
- This month against last month: season, news cycle, audience growth, and platform changes move together.
- Someone else's benchmark: unknown denominator, different audience.
- A pattern that appeared after you went looking.
- A p-value from a test you chose after seeing the data.

## What to do instead of measuring more

Post steadily for a quarter against a written brief. Log Tier 1 outcomes by hand. Re-run the tester every six weeks and expect "nothing survived" most times. Compounding comes from consistency; optimization is mostly out of reach at this sample size.

## Sources

1. Good, P. (2005). *Permutation, Parametric, and Bootstrap Tests of Hypotheses*, 3rd ed. Distribution-free tests.
2. Gelman, A. and Loken, E. (2013). "The Garden of Forking Paths."
3. Benjamini, Y. and Hochberg, Y. (1995). "Controlling the False Discovery Rate." *JRSS-B*.
4. Holm, S. (1979). "A Simple Sequentially Rejective Multiple Test Procedure." *Scandinavian Journal of Statistics*.
5. Cohen, J. (1988). *Statistical Power Analysis for the Behavioral Sciences*, 2nd ed. Two-sample sizing and a stated minimum effect of interest.
6. Ioannidis, J. P. A. (2005). "Why Most Published Research Findings Are False." *PLoS Medicine*.
7. Efron, B. and Tibshirani, R. (1993). *An Introduction to the Bootstrap*. Percentile intervals.
8. Tukey, J. W. (1977). *Exploratory Data Analysis*. Exploratory versus confirmatory work.
