# Test Assumptions and Experiment Validity

The math behind the scripts, the assumptions each test needs, and the experiment-level threats that make a correct calculation wrong. Load when a result looks surprising, when a test was peeked at, or when someone asks why a test was chosen.

## Errors and power

| | No real effect | Real effect |
|---|---|---|
| Reject H0 | Type I error (alpha): false positive | Correct detection (power = 1 − beta) |
| Fail to reject | Correct | Type II error (beta): missed effect |

- Alpha is the false-positive rate you accept; 0.05 is a habit, not a law. Lower it when a false win is costly or hard to undo.
- Power is the chance of catching an effect of a stated size; 0.80 is the usual floor.
- Required n rises with higher power, lower alpha, a smaller effect, and noisier data. Halving the detectable effect roughly quadruples n.

## Tests, assumptions, formulas

**Two-proportion z-test.** Independent groups. At least about 10 successes and 10 failures per group. Units do not affect each other.

```
z = (p2 − p1) / sqrt( p̄(1 − p̄)(1/n1 + 1/n2) ),   p̄ = (x1 + x2)/(n1 + n2)
CI for p2 − p1 uses the unpooled standard error.
Cohen's h = 2·asin(√p2) − 2·asin(√p1)
```

**Welch t-test.** Independent groups, roughly normal means (central limit theorem helps once n is in the hundreds). Does not need equal variances, so use it by default.

```
t  = (m2 − m1) / sqrt(s1²/n1 + s2²/n2)
df = (s1²/n1 + s2²/n2)² / [ (s1²/n1)²/(n1−1) + (s2²/n2)²/(n2−1) ]
Cohen's d = (m2 − m1) / pooled sd
```

Revenue, LTV, and latency are heavy-tailed. A few whales can move the mean and the variance together. Winsorize at the 99th percentile, test log values (positive data only), or compare medians, and say which you did.

**Chi-squared.** Independent observations, expected count at least 5 per cell, otherwise Fisher's exact or merged categories.

```
chi² = Σ (O − E)² / E
df   = k − 1 (goodness of fit);   (r − 1)(c − 1) (independence)
Cramér's V = sqrt( chi² / (n · (min(r, c) − 1)) )
```

Goodness of fit against the planned split is the **sample-ratio-mismatch check**. A significant result means assignment or logging is broken. Fix that before reading any metric.

## Proportion intervals

The textbook interval `p ± z·sqrt(p(1−p)/n)` can leave the 0–1 range and undercovers at small n or extreme p. Use the Wilson score interval, which `confidence_interval.py` does:

```
center = (p + z²/2n) / (1 + z²/n)
margin = z/(1 + z²/n) · sqrt( p(1−p)/n + z²/4n² )
```

## Sample-size formulas

```
proportions: n = (z_a/2 + z_b)² · [p1(1−p1) + p2(1−p2)] / (p2 − p1)²   per group
means:       n = 2σ²(z_a/2 + z_b)² / δ²                                  per group
```

State the effect as relative (+20%) or absolute (+1 pp) once and keep it. Mixing them is the usual cause of a sample size that is off by a factor of five.

Duration is `n per group × groups ÷ eligible daily traffic`, then round up to whole weeks so every weekday appears equally.

## Experiment validity threats

Raise these unprompted when the signal is present.

| Threat | Signal | Consequence | Action |
|---|---|---|---|
| **Peeking** | "We checked it every day" | Looking at 50%, 75%, 100% of planned n lifts true alpha from 0.05 to about 0.13 | Fix the stopping rule up front. If early stopping is needed, use a sequential method and escalate |
| **Multiple metrics** | More than 3 outcomes judged | 10 tests at 0.05 give a 40% chance of at least one false win | Name one primary metric; correct or disclose the rest |
| **Underpowered** | n below the planned size | A null result says nothing | Run `sample_size.py mde` and report what could not be seen |
| **Sample-ratio mismatch** | Group sizes off the planned split | Assignment or logging bug | Run the `chi2` split check first; distrust all results until resolved |
| **Interference (SUTVA)** | Shared inventory, social features, two-sided markets | Control is contaminated by treatment | Randomize by cluster or region; escalate |
| **Novelty or primacy effect** | Early lift decays, or early dip recovers | Early read misstates the steady state | Run at least two full weekly cycles; re-measure after the novelty window |
| **Simpson's paradox** | Segment results reverse the total | Mix shift between arms | Check key segments; see `interpretation-traps.md` |
| **Clustered data** | Many rows per user, store, or session | Standard errors too small, p-values too good | Aggregate to the randomization unit before testing |

False-positive inflation from several looks or tests, in numbers:

| Tests | P(at least one false positive at 0.05) |
|---|---|
| 1 | 5% |
| 3 | 14% |
| 5 | 23% |
| 10 | 40% |
| 20 | 64% |

Corrections: Bonferroni (divide alpha by the test count; `sample_size.py --tests k` does this for sizing) is simple and strict. Benjamini-Hochberg controls the false discovery rate and suits exploratory sweeps. Code for both is in `interpretation-traps.md`.
