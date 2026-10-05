# Calibration Method

Default weights and cutoffs are industry guesses. Calibration tests them on your own churn history and moves them only as far as data allows. Tool: `scripts/calibrate_scoring.py`.

## When to calibrate

- First 12 months of history exist (churned and retained accounts)
- After product change that shifts what good usage looks like
- After pricing, packaging, or ICP change
- After any churn that score did not flag 60 days ahead
- Every quarter as routine

No history yet: run defaults, label every output "uncalibrated defaults", log scores monthly so history builds.

## Data needed

One record per account whose outcome is known. Outcome = churned, or retained through renewal.

| Field | Meaning |
|---|---|
| customer_id, segment | Segment is enterprise, mid-market, or smb |
| outcome | churned or retained |
| snapshots | Dimension scores (usage, engagement, support, relationship; each 0-100) at fixed days before outcome: 90, 60, 30 |

Anchor day: churn date for churned, renewal date for retained. Take snapshots by running `health_scorer.py` on archived metrics, or from your CS platform's score history. Never reconstruct scores from memory after the fact; hindsight bias inflates results.

Minimums:

| Need | Count |
|---|---|
| Refit dimension weights | 20 churned and 20 retained in train data |
| Refit one segment's cutoffs | 10 churned and 10 retained in that segment's train data |

Below minimum = keep defaults for that part and say why. Thin data fits noise.

## Procedure

1. **Split.** Sort by outcome and id; every 4th account goes to holdout. Fit on train only.
2. **Fit weights.** For each dimension, effect size at the evaluation lead (default 60 days) = (retained mean - churned mean) / pooled standard deviation. Negative or zero effect gets zero raw weight. Blend 50/50 with default weight. Floor each at 0.10. Renormalise to sum 1.0.
3. **Fit green cutoff per segment.** Account is flagged when score is below green_min. Choose the lowest green_min that flags at least `--target-recall` (default 80%) of churned accounts at the evaluation lead. Lowest = fewest false alarms.
4. **Fit yellow cutoff per segment.** Red = below yellow_min. Choose the highest yellow_min whose red zone is at least `--red-precision` (default 50%) churned, with 3+ accounts in red. Keep yellow_min at least 5 below green_min.
5. **Cap the move.** Each cutoff stays within 10 points of default. Wider shift means the model or the data is wrong, not the cutoff.
6. **Validate on holdout.** Report recall, false-alarm rate, red precision for defaults and calibrated, on train and holdout.
7. **Measure warning lead.** For each churned account, the earliest snapshot below green_min. Report median days and share flagged at or before the evaluation lead.
8. **Write profile.** `--write-profile profile.json`, then `health_scorer.py --profile profile.json`.

## Adopt or reject

| Check | Adopt when |
|---|---|
| Holdout recall | At least target minus 15 points |
| Train vs holdout recall | Gap under 15 points (larger = overfit) |
| False-alarm rate | Better than or close to defaults; CSMs can absorb the flagged volume |
| Median warning lead | 60 days or more |
| Never flagged | Near zero; each one needs a manual autopsy |

Any check fails = keep defaults, collect more history, or add a leading signal. Do not tune until numbers look good.

## Autopsy for misses

For each churned account the score never flagged, name the cause: no usage data? sentiment guess wrong? sudden event (champion left, acquisition)? Sudden events are not a score problem; route them to churn-risk signals and the 7-category taxonomy in [retention-decomposition.md](retention-decomposition.md).

## Pitfalls

- **Threshold creep.** Lowering green_min so portfolio looks healthier. The 10-point cap and recall target guard against it; do not edit the profile by hand to hide reds
- **Leaky labels.** Snapshots taken after the account announced intent to leave
- **Survivor bias.** Only counting accounts that reached renewal; early churn is churn
- **One cutoff for all segments.** Segment fits exist for a reason
- **Lagging dimension overweight.** Support reacts after damage; effect size at 60 days shows if it earns weight
- **Overfitting small segments.** Respect minimums

## Recalibration log

Keep: date, lead, accounts, weights, cutoffs, holdout recall and false-alarm rate. Compare to last run. Drift in weights across runs = product or ICP change worth a conversation.
