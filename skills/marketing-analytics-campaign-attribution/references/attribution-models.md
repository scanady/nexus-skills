# Attribution Models

Attribution splits one conversion's value across the touchpoints before it. No model is true. Each model is a rule. Run all five. Compare. Trust only what survives the comparison.

## The five rules

For a converted journey with `n` touches in time order and value `V`:

| Model | Credit to touch `i` | Rewards | Punishes | Use when |
|---|---|---|---|---|
| first-touch | `V` if `i = 1`, else 0 | Channels that start journeys | Closers | Judging awareness spend, new-market entry |
| last-touch | `V` if `i = n`, else 0 | Channels that close | Openers and nurturers | Short cycles, direct response |
| linear | `V / n` | Every touch alike | Nothing, and nothing is learned about order | First pass on a multi-channel program |
| time-decay | `V * w_i / sum(w)`, `w_i = 2^(-d_i / h)` | Touches near conversion | Early touches in long cycles | Cycles of days to weeks; set `h` near median cycle length |
| position-based | 40% first, 40% last, 20% split over the middle | Opener and closer | Middle nurturing | Full-funnel programs with a clear open and close |

Edge cases the script uses:
- Position-based with 1 touch: 100% to it. With 2 touches: 50/50.
- `d_i` is days between touch `i` and the conversion time. Conversion time is `converted_at` when present, else the last touch time. Touches after `converted_at` are dropped and counted.
- Same channel on several touches: its credits add.

## Pick by question, not by taste

| Question | Model to lead with |
|---|---|
| Where do customers first hear of us? | first-touch |
| What closes the sale? | last-touch |
| Is a channel doing anything anywhere on the path? | linear, plus the Reach table |
| Does recency matter in our cycle? | time-decay, sweep `--half-life` over 3, 7, 14, 30 |
| We run both awareness and conversion spend | position-based |

## Read the sensitivity table first

The sensitivity table gives each channel's lowest and highest share across models.
- Spread under 10 points: the channel's value does not depend on the rule. Act on it with normal confidence.
- Spread of 10 points or more: the channel's value depends on the rule. The decision is a judgment call. Say so. Do not quote one model's number.
- A channel with 0% under first-touch and a large share under last-touch is a closer. The reverse is an opener. Cutting an opener on last-touch data is the classic error.

## Reach table

Reach counts every journey, converted or not. It shows how often a channel is touched and how many of those journeys convert. It is not credit. Two traps:
- A channel that appears late in journeys that already lean to convert (brand search, direct, retargeting) shows a high rate because it sits near the decision, not because it caused it.
- Conversion rate of touched journeys is confounded by who got touched. Do not read it as lift.

## What attribution cannot tell you

- **Cause.** Credit shows association along a path. It does not show what would have happened without the touch. Only a holdout, geo split, or randomized pause shows that (incrementality).
- **Missing touches.** Dark social, offline, walled-garden views, and consent-blocked tracking leave gaps. The model credits only what it sees.
- **Identity.** One person on two devices looks like two journeys. The script takes journeys as given.
- **Platform self-reports.** Each ad platform claims credit with its own window. Summed claims exceed real revenue. Use one journey dataset.
- **Small samples.** Under about 30 converted journeys, shares move with one journey. The script warns.

## Lookback and windows

Set the journey window before export, not after. Use the median time from first touch to purchase as the guide. A window shorter than the real cycle makes first-touch and time-decay look wrong. Write the window next to every result.

## Report rule

Show at least three models side by side with the sensitivity flags. State the window, the sample size, and "this is credit, not proof of lift". Recommend a budget move only where models agree, or label it a test.
