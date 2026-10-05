# Script Toolkit

Three dependency-free Python scripts in `scripts/` compute the numbers the other references explain. They need Python 3.9+ and nothing else — no scipy, numpy, or pandas. Use them when you have summary numbers (counts, means, standard deviations) and want a reproducible answer instead of mental arithmetic. When you have raw rows and a full Python stack, the library calls in `hypothesis-testing.md` do the same job.

Run every script from the skill folder, or by absolute path. Each takes `--format json` for downstream use and exits with `error: ...` on invalid input.

## Which script

| Question | Script | Mode |
|---|---|---|
| Did conversion differ between two groups? | `hypothesis_test.py` | `proportions` |
| Did a continuous metric (revenue, latency) differ? | `hypothesis_test.py` | `means` |
| Do category mixes differ, or is the split off plan? | `hypothesis_test.py` | `chi2` |
| How uncertain is this one rate or mean? | `confidence_interval.py` | `proportion` / `mean` |
| How many users do we need before launch? | `sample_size.py` | `size` |
| The test was null; what could it have seen? | `sample_size.py` | `mde` |

## Recipes

```bash
# A/B conversion: group 1 is control, group 2 is treatment
python3 scripts/hypothesis_test.py proportions --n1 5000 --x1 250 --n2 5000 --x2 310

# Continuous metric from summary stats (Welch, unequal variances)
python3 scripts/hypothesis_test.py means \
  --mean1 42.3 --sd1 18.1 --n1 800 --mean2 46.1 --sd2 19.4 --n2 820

# Sample-ratio check: planned 50/50 split, observed 4980 vs 5120
python3 scripts/hypothesis_test.py chi2 --observed 4980,5120 --expected 1,1

# Plan mix by segment (rows = groups, columns = outcomes)
python3 scripts/hypothesis_test.py chi2 --table "120,80;90,110"

# One rate or mean with its uncertainty
python3 scripts/confidence_interval.py proportion --n 1200 --x 96
python3 scripts/confidence_interval.py mean --n 800 --mean 42.3 --sd 18.1

# Size before launch: +20% relative on a 5% baseline, 4,000 eligible users a day
python3 scripts/sample_size.py size proportion --baseline 0.05 --mde 0.20 --daily-traffic 4000

# Same, but four metrics will be judged, so alpha is split four ways
python3 scripts/sample_size.py size proportion --baseline 0.05 --mde 0.20 --tests 4

# After a null result with 3,000 per group
python3 scripts/sample_size.py mde proportion --baseline 0.05 --n 3000
```

`--expected` for `chi2` accepts counts or ratios; the script rescales it to the observed total.

## Reading the output

- **Difference and CI** are group 2 minus group 1. Report the CI, not just the p-value.
- **Effect size** is Cohen's h for proportions, Cohen's d for means, Cramér's V for chi-squared. Bands below.
- **WARNING lines** are validity flags, not decoration. Carry each one into the write-up.
- A **small effect label** beside a tiny p-value is the classic large-sample result. Convert it to business units before recommending anything.
- The script never says "ship". It computes; you decide with the table below.

| Effect size | Negligible | Small | Medium | Large |
|---|---|---|---|---|
| Cohen's d, Cohen's h | < 0.2 | 0.2–0.5 | 0.5–0.8 | > 0.8 |
| Cramér's V (1 df) | < 0.1 | 0.1–0.3 | 0.3–0.5 | > 0.5 |

These bands are conventions from behavioral research. A "negligible" h on a checkout flow with ten million sessions can still be worth money. Judge size against the business, with the band as a first read.

## Post-experiment decision frame

| Statistically significant? | Effect worth the cost? | Guardrails | Call |
|---|---|---|---|
| Yes | Yes | Clean | Ship |
| Yes | No, CI lower bound is trivial | Clean | Hold; the lift is real but may not pay for the complexity |
| Yes | Any | A guardrail regressed | Do not ship; investigate the regression |
| No | CI still includes a worthwhile effect | Clean | Extend or re-run; the test was too small to say |
| No | CI rules out any worthwhile effect | Clean | Stop; the idea does not help |

Ask once: "If the true effect were exactly the point estimate, would the business care?" If not, significance alone does not justify shipping.

## Confidence tags for findings

- **Verified** — assumptions hold, sample meets the planned size, no validity threat found.
- **Likely** — minor assumption strain; read the result as directional.
- **Inconclusive** — underpowered, peeked, or the data is suspect; do not act on it.

## Limits of the scripts

- Summary-number inputs only. They cannot read a file, run Mann-Whitney, or do paired tests; use the library calls in `hypothesis-testing.md` for those.
- The normal approximation drives `proportions` and `sample_size.py`. Under about 10 events per cell, switch to an exact test.
- Heavy-tailed metrics break the mean test. Winsorize, log-transform, or compare medians first, then test.
- No sequential or Bayesian analysis. If the team peeked or needs early stopping, see `test-assumptions.md` and escalate.
