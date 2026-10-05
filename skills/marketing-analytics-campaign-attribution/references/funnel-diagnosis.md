# Funnel Diagnosis

A funnel is a chain of step rates. Final conversion is their product. This file covers how to read the numbers from `analyze_funnel.py` and what to check next.

## Define stages first

- Count unique entities (people, sessions, or accounts) at every stage. Do not mix units. The script rejects a stage larger than the one before it for this reason.
- Use stages your tracking can see. A default ecommerce chain: visit, product view, add to cart, checkout, purchase. A default B2B chain: visit, lead, qualified lead, opportunity, customer.
- Keep one time window for all stages. State it.

## Reading the output

| Output | Meaning | Caution |
|---|---|---|
| Step rate | Share of the previous stage that reached this one | Always read with the 95% interval |
| 95% interval | Wilson range for the step rate | Wide interval means too few entrants; do not rank on it |
| Largest absolute loss | Transition that loses the most people | Top-of-funnel steps always lose most; this is volume, not a defect |
| Lowest step rate | Transition with the weakest rate | Compare to your own history before calling it a problem |
| Segment finding | Segment rate against all other segments, with p-value | Alpha is Bonferroni-corrected over all tests run; segments are not randomized |
| Gap to best | Extra final conversions if the segment matched the best segment's rate at that step | Upper bound. Assumes the same downstream rates |

## Diagnosis in four moves

1. **Quantify.** Find the transition with both a low rate and a large entry count. Weak rate with a tiny entry count is noise.
2. **Segment.** Split by channel, device, new versus returning, geography, offer. Keep the segment list short and name it before looking. Many splits produce false gaps.
3. **Hypothesize the cause.** Match the step to the usual causes below. Check with a session sample, a form audit, or a quick user test. The numbers say where, not why.
4. **Rank fixes** by `entries x plausible rate gain x value per conversion`, divided by effort. Run the top one as a test.

## Usual causes by step

| Step | Common causes |
|---|---|
| Visit to interest | Ad-to-page mismatch, slow load, weak first screen, wrong traffic |
| Interest to consideration | Unclear offer, missing proof, hard navigation |
| Consideration to intent | No price clarity, weak comparison, no trust signal, long form |
| Intent to purchase | Surprise fees, forced signup, payment friction, slow page, errors |
| Purchase to retention | Weak onboarding, no follow-up, product gap |

## Funnel math

- Rates multiply. A 10% relative lift at any single step lifts final conversions by 10%. So pick the step where a lift is cheapest and most believable, not the step with the biggest percentage.
- Value of a change: `entries at the step x rate gain x downstream rate x value per conversion`. The script's gap-to-best uses this form.

## Traps

- **Wrong stage.** Fixing a step that is already near its natural ceiling.
- **Blended view.** One average hides a segment that is failing and one that is strong. Check segments before you act.
- **Rate-only goal.** Raising a rate by cutting traffic quality can lower revenue. Track volume and value beside rate.
- **Time lag.** A recent cohort has not finished its journey. Compare cohorts of the same age, or wait for the cycle to complete.
- **Peeking.** Testing a fix and stopping when the number looks good. Size the test first. See `data-analysis-statistical-methods`.

## Review cadence

Weekly for live campaigns, monthly for the whole funnel, quarterly for stage definitions and benchmarks. Re-baseline after any tracking change.
