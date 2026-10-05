# Funnel Diagnosis

Use a funnel to find where users leave before the first retention point. Retention shows if users return. The funnel shows why some never get that far.

## Define the funnel

1. List steps in the order a user must do them. Four to seven steps. Each step is one observable event.
2. Choose strict or loose counting.
3. Choose a time window if steps have natural deadlines (for example, activation within 7 days of signup).

| Mode | Counts a user at step N when | Result |
|---|---|---|
| Strict (default) | The user did steps 1 to N in order, inside the window | Rates never exceed 100%. Honest drop-off |
| Loose (`--loose`) | The user has an event at step N, whatever came before | Rates can exceed 100% when users skip steps or tracking misses an event. Use only to audit tracking |

If loose and strict counts differ a lot at one step, the step is skipped by design or the event is missing. Fix the data first.

## Read the table

| Column | Meaning | Use |
|---|---|---|
| `conversion_from_previous` | Step N users / step N-1 users | Find the weakest step transition |
| `conversion_from_first` | Step N users / step 1 users | Overall yield |
| `lost_from_previous` | Absolute users lost at the step | Find where the most people leave |

Weakest rate and largest absolute loss are often different steps. Report both. Fix the largest absolute loss first unless the weakest rate is cheap to fix.

## Diagnose a leak

1. Split the leaky step by channel, device, plan, and first-seen week. A leak that exists in one split is a different problem than a leak in all of them.
2. Check time-to-step. A long median delay before the drop means friction or confusion. A fast drop means a mismatch of promise and product.
3. Check for tracking gaps: does the step event fire on every platform?
4. Look at what users did instead. The next event after the last completed step shows where they went.
5. Link back to retention. Do users who pass the leaky step retain better? If not, fixing the step moves a vanity number.

## Match funnel to curve

| Funnel signal | Curve signal | Joint reading |
|---|---|---|
| Low activation rate | Cliff at period 1 | Onboarding never reaches value. Fix the funnel, not retention tactics |
| High activation | Cliff at period 1 | Value is delivered once but not repeated. Work on the return trigger |
| Healthy both | Slow bleed | Value fades. Work on depth and habit |

## Input contract

```csv
user_id,stage,ts
u001,visit,2026-03-01T10:00:00
u001,signup,2026-03-01T10:05:00
u002,visit,2026-03-01T11:00:00
```

`ts` is needed only for order checks and `--window-days`. Without it the script counts presence of each step in order of the `--stages` list.
