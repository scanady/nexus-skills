# Cohort Design

Fix these choices before computing anything. Wrong choice here makes every curve downstream meaningless.

## 1. Anchor event (what puts a user in a cohort)

| Anchor | Use when | Trap |
|---|---|---|
| Signup / install | Question is about acquisition or onboarding | Mixes people who never intended to use the product |
| Activation (first value moment) | Question is about product stickiness | Hides activation failure. Report activation rate beside it |
| First purchase | Commerce, subscription | Misses the browse-only audience |
| Feature first use | Question is about one feature | Self-selected power users. Compare to a non-adopter baseline, never to the whole base |
| Exposure to a change | Release or experiment read | Needs a clean control cohort. Hand off to an experiment skill if randomization matters |

One anchor per analysis. Say it out loud in the result.

## 2. Retained behavior (what counts as "came back")

- Pick the action that proves value, not the action that proves presence. "Opened app" flatters. "Completed core workflow" is honest.
- Same behavior for every cohort. Never change the definition mid-series.
- Name a fallback if the value action is not tracked. State that it is a proxy.

## 3. Retention flavor

| Flavor | Retained at age N means | Best for | Flag |
|---|---|---|---|
| Classic (bracket) | Active in period N exactly | Habitual products with a fixed cadence | default |
| Unbounded | Active in period N or any later period | Irregular-use products (travel, tax, B2B quarterly) | `--unbounded` |
| Rolling | Active in a trailing window | Dashboards that need one smooth number | Compute outside the script |

Unbounded curves can never rise and always look kinder. Never mix flavors in one comparison.

## 4. Grain

| Grain | Use when | Min cohort size guide |
|---|---|---|
| Day | Consumer apps, first-week focus | 100+ users per cohort |
| Week | Default for most SaaS and apps | 50+ |
| Month | Low volume, long cycles, B2B | 30+ |

Pick the grain that matches natural usage cadence. Daily grain on a weekly-use product shows a sawtooth that is not real.

## 5. Right-censoring (incomplete periods)

A cohort that is 3 weeks old has no week 4. The calculator marks unfinished periods and drops them from pooled denominators. If you compute by hand:

- Never count missing future data as churn.
- Never average a young cohort's early ages into an old cohort's late ages without matching denominators.
- Set `--as-of` to the real data cutoff when the export lags behind the latest event.

## 6. Segmenting

Blended curves hide the story. Split at least once before concluding:

- Acquisition channel
- Plan tier or company size
- Platform or device
- First-session behavior (did the user reach the value action?)

Run each split as its own file or filter. Keep segments large enough for the grain table above. Small segments swing wildly. Report sizes with every rate.

## 7. Input contract for the calculator

One row per user activity event.

```csv
user_id,cohort_date,activity_date
u001,2026-01-05,2026-01-05
u001,2026-01-05,2026-01-13
u002,2026-01-06,2026-01-06
```

- Include the anchor event itself as an activity row, or cohort sizes undercount users who never returned.
- Dates are ISO `YYYY-MM-DD`. Time parts are ignored.
- A user with several `cohort_date` values takes the earliest.
- Activity dated before the anchor is ignored.

If the data lives in a warehouse, write the extract query first, then run the script on the export. Check the extract with a row count per cohort before trusting any rate.
