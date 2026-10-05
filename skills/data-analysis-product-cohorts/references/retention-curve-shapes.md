# Retention Curve Shapes

Read the whole curve and the cohort-over-cohort pattern together. One point (for example "day 30 is 20%") says nothing about shape.

## Shape catalog

| Shape | Signature | Usual meaning | Check next | Action |
|---|---|---|---|---|
| Cliff, low floor | Big period-1 drop (over 60%), tail under 10% and still falling | Promise and product do not match, or onboarding never reaches value | Funnel before activation. Session recordings of first visit. Channel split | Fix activation first. Do not buy more traffic |
| Cliff, healthy plateau | Big early drop, then flat at 15% or more | A real core audience plus a tourist crowd | Who stays? Compare first-session behavior of stayers and leavers | Make the stayer path the default onboarding path |
| Gentle decay to plateau | Smooth fall, flat tail | Healthy product with predictable churn | Plateau level vs. goal | Raise the level through depth, not breadth |
| Slow bleed | No plateau. Steady fall through the tail | Value fades. No habit forms | Usage frequency of retained users over time. Competing alternatives | Build a recurring reason to return. See habit-loop work |
| Near-zero floor | Tail under 5% and flat | Occasional-use product or no retained value | Is the product meant to be occasional? Switch to unbounded or a longer window | Redefine the value metric, or accept and target use-case frequency |
| Smile (recovery) | Dips, then rises in the tail | Resurrection: seasonal use, lifecycle emails, reactivation campaign | Event calendar. Reactivation sends | Separate resurrected users from continuous users before judging |
| Sawtooth | Peaks at regular spacing (7, 14, 21 days) | Weekly use rhythm, or grain too fine | Grain choice | Move to weekly grain |
| Step down | Sudden fall at one fixed age | Trial end, billing event, expiring credit, forced re-login | Product rules at that age | Fix the cliff or move the decision earlier |

## Cohort-over-cohort patterns

Put the matrix on the page. Read down a column (same age, different cohorts) and across a row.

| Pattern | Reading |
|---|---|
| Newer cohorts higher at the same age | Onboarding, targeting, or product change is working. Tie to the release date |
| Newer cohorts lower | Channel mix shifted, quality fell, or a release broke something |
| One diagonal stripe (same calendar date, all cohorts) low | An outage, a tracking bug, or a holiday. Not a cohort effect |
| One cohort row off while neighbors agree | Promo, campaign, or a data load error for that cohort |
| Late ages noisy | Cohort too small at that age. Widen the grain |

The script's `shape` command gives a first-pass label for the pooled curve and the trend. It is a heuristic. Confirm by reading the matrix.

## Confounders to rule out before telling a story

1. **Mix shift.** A growing channel with lower intent drags the blend down while every channel holds steady. Split by channel.
2. **Seasonality.** Compare with the same weeks last year when available. Never read a holiday dip as product decay.
3. **Definition drift.** Anchor or behavior changed mid-series, or tracking was added or broken. Check the event schema history.
4. **Survivor skew.** The pooled tail uses only older cohorts. If old cohorts were better or worse, the tail misleads. Check the matrix.
5. **Small n.** Under the minimum cohort size, differences of 5 points are noise.
6. **Resurrected users.** Unbounded and classic curves disagree when users return after gaps. Report both if the product has irregular use.

## Reporting a finding

Write each finding in this order:

1. Shape and size: "Week 1 drops 62% to 34%. The tail holds near 28% from week 3."
2. Comparison: "Cohorts since 2026-03-02 sit 4 points above older ones at week 4."
3. Confounders checked, and which remain open.
4. One action with an owner, and the number that would show it worked.

Do not quote an external benchmark as a target unless the user supplies a comparable one. Retention levels depend on product type, anchor, and behavior definition.
