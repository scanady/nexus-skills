# Survey Sampling

Load when the research needs primary survey data, and before any survey result is reported by segment. Pairs with `scripts/segment_sample_planner.py`.

## Contents

1. [Size for the segments you will report](#1-size-for-the-segments-you-will-report)
2. [The formulas](#2-the-formulas)
3. [Inputs and where they come from](#3-inputs-and-where-they-come-from)
4. [Quotas, oversampling, and weights](#4-quotas-oversampling-and-weights)
5. [Errors that sample size does not fix](#5-errors-that-sample-size-does-not-fix)
6. [Question design](#6-question-design)
7. [Reporting rules](#7-reporting-rules)

## 1. Size for the segments you will report

A survey sized for the total does not support results per segment. If the brief will say "mid-size fleets prefer X", the mid-size segment needs its own sample that meets its own margin of error.

Decide first:
- Which segments the report will show alone.
- The margin of error each one needs. A segment that drives a decision needs a tighter margin than one shown for context.

Then size each segment, and let the total be the sum. The planner does this.

## 2. The formulas

For a proportion, at confidence level with critical value `z`, expected proportion `p`, and margin of error `e`:

```
n0 = z^2 * p * (1 - p) / e^2                 Cochran
n  = n0 / (1 + (n0 - 1) / N)                  finite-population correction, N = segment size
n  = n * deff                                  design effect from weighting or clustering
invites = n / response_rate
```

Reference values at 95% confidence, `p = 0.5`, no correction: +/-10% needs 97, +/-8% needs 151, +/-5% needs 385, +/-3% needs 1,068.

The correction matters when the segment is small. For a segment of 2,200 accounts at +/-10%, n falls from 97 to 93. For a segment of 150 accounts, n falls by about 40% and the planner may report that you need a census.

**Budget mode** runs the formula in reverse. Given a fixed number of completes, it reports the margin of error each segment can support:

```
e = z * sqrt(p * (1 - p) / (n / deff) * (N - n) / (N - 1))
```

Use budget mode when the number of completes is fixed by cost or panel size. Any segment that misses its target margin of error is either oversampled or reported with the other segments, never alone.

## 3. Inputs and where they come from

| Input | Default | Source |
|---|---|---|
| Confidence | 0.95 | Convention. Use 0.90 only for early exploration, and say so. |
| Expected proportion `p` | 0.5 | Gives the largest n. Use a pilot or prior-wave value only if it exists. |
| Margin of error | 0.05 total, 0.08-0.10 per segment | The smallest difference that would change the decision. |
| Segment population `N` | none | Same registry or census used in sizing. Keep the two consistent. |
| Response rate | 1.0 (no inflation) | Panel vendor history or a prior wave. B2B cold email often sits at 5-15%. |
| Design effect | 1.0 | Pilot data or a prior wave. Weighting a skewed sample often adds 1.2-1.5. |

State the source of every non-default input in the report.

## 4. Quotas, oversampling, and weights

The planner sets each quota to the larger of:
- the segment's floor (its own margin of error), and
- its proportional share of the total n.

Small segments therefore get more completes than their population share. That is oversampling. It makes segment results valid, but it distorts any total.

Fix totals with a post-stratification weight per segment:

```
weight = population share / sample share
```

The planner prints the weight. A weight below 0.5 means heavy oversampling. Every total must be weighted, and the design effect from weighting must be counted in the next wave.

## 5. Errors that sample size does not fix

Margin of error covers sampling error only. Total survey error (Groves) adds:

| Error | Example | Control |
|---|---|---|
| Coverage | An email panel misses firms with no listed contact. | Compare the frame with the sizing registry. Report who is missing. |
| Non-response | Only satisfied customers answer. | Compare early and late responders. Follow up a sample of non-responders. Report the response rate (AAPOR definitions). |
| Measurement | Wording or order pushes an answer. | Pre-test with 5-8 cognitive interviews. Randomize option order. |
| Processing | Coding or weighting mistakes. | Script the cleaning. Check weighted totals against known population figures. |

A tight margin of error on a biased frame gives precise wrong answers.

## 6. Question design

- **One question, one idea.** "Is it fast and reliable?" is two questions.
- **No lead.** "How much do you value our time-saving reports?" assumes the answer.
- **Balanced scales.** Equal positive and negative points, with a labelled midpoint.
- **Behaviour before attitude.** "How many work orders did you log last month?" is more reliable than "How important is tracking?"
- **Trade-offs over ratings.** When every attribute rates "important", use MaxDiff or conjoint to force a choice.
- **Pre-test** every instrument before field.

## 7. Reporting rules

- Report each segment with its n and its achieved margin of error.
- Do not report a segment that missed its margin of error alone. Combine it or label it directional.
- Weight every total. State the weighting variables.
- Report the response rate and the frame.
- A difference between two segments is real only when it exceeds the combined margin of error. Test it. Do not compare by eye.

## Sources

- Cochran, W. G., *Sampling Techniques*, 3rd ed., Wiley, 1977.
- Kish, L., *Survey Sampling*, Wiley, 1965 (design effect).
- Groves, R. M., et al., *Survey Methodology*, 2nd ed., Wiley, 2009 (total survey error).
- Dillman, D. A., Smyth, J. D., and Christian, L. M., *Internet, Phone, Mail, and Mixed-Mode Surveys: The Tailored Design Method*, 4th ed., Wiley, 2014.
- Schuman, H., and Presser, S., *Questions and Answers in Attitude Surveys*, Academic Press, 1981.
- AAPOR, *Standard Definitions: Final Dispositions of Case Codes and Outcome Rates for Surveys* (current edition).
