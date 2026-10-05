# Segment Gate

Load when the research recommends which market segments to target. Pairs with `scripts/segment_gate.py`. This gate selects target markets. Clustering customer data into segments belongs to `marketing-customer-segmentation`.

## Contents

1. [The five criteria](#1-the-five-criteria)
2. [Why two criteria are hard gates](#2-why-two-criteria-are-hard-gates)
3. [Gather the gate evidence](#3-gather-the-gate-evidence)
4. [Score the other three](#4-score-the-other-three)
5. [Segmentation bases](#5-segmentation-bases)
6. [Verdicts and next steps](#6-verdicts-and-next-steps)

## 1. The five criteria

Kotler and Keller name five tests for a useful segment.

| Criterion | Question | Treatment |
|---|---|---|
| Measurable | Can you count the buyers and estimate their spend? | Scored 1-5 with evidence. |
| Substantial | Is the attainable revenue large enough to fund a program? | Hard gate, from numbers. |
| Accessible | Can you reach the buyers through a channel you can afford? | Hard gate, from numbers. |
| Differentiable | Does the segment respond to an offer differently from other segments? | Scored 1-5 with evidence. |
| Actionable | Can you build and run a program for it with what you have? | Scored 1-5 with evidence. |

## 2. Why two criteria are hard gates

Substantiality and accessibility fail most often, and they fail quietly. A team describes a segment precisely, scores it well on fit, and only finds out in market that it is too small or that no channel reaches it at a sane cost. A high score on the other three criteria cannot rescue either failure, so the script drops the segment.

The gates use numbers, not opinion scores:

```
substantial = accounts x annual_value x attainable_share >= min_segment_revenue
              and accounts >= min_accounts
accessible  = some channel has reach >= min_channel_reach
              and CAC <= max_cac_to_value x annual_value
```

Profile defaults (override any key in the spec's `gates` block):

| Profile | Min attainable revenue | Min accounts | Min channel reach | Max CAC / annual value |
|---|---|---|---|---|
| b2b-saas | 2M | 500 | 30% | 1.0 |
| enterprise | 5M | 50 | 20% | 1.5 |
| consumer | 1M | 20,000 | 25% | 0.5 |
| marketplace | 1M | 5,000 | 25% | 0.5 |
| hardware | 2M | 1,000 | 25% | 0.5 |
| services | 0.5M | 100 | 30% | 0.75 |

The defaults are starting points. Set `min_segment_revenue` from the cost of the program: the team, the marketing, and the product work that the segment needs. Set `max_cac_to_value` from your gross margin and payback target. For example, a 12-month payback at 80% margin allows CAC up to 0.8x annual value.

## 3. Gather the gate evidence

| Field | Good source | Weak source |
|---|---|---|
| `accounts` | Registry, census, or firmographic database count with the same filter as sizing. | "Thousands of firms like this." |
| `annual_value` | Realized price from deals or competitor price pages, times units per account. | List price of the top tier. |
| `attainable_share` | Pipeline capacity x win rate in the planning window. | A share picked to make the number work. |
| `channels[].reach` | Membership counts, list sizes, search volume, partner customer counts as a share of `accounts`. | "Everyone is on LinkedIn." |
| `channels[].cac` | Pilot campaign results or benchmark CAC for the channel and deal size. | Vendor ad calculator. |

Use the same account counts as `triangulate_sizing.py`. Segments must be mutually exclusive. The script warns when segment accounts add up to more than `market_accounts`.

## 4. Score the other three

Score 1 to 5 and write the evidence in one line. A score with no evidence counts as 1.

| Score | Measurable | Differentiable | Actionable |
|---|---|---|---|
| 5 | Counted in a registry, with a field that identifies the segment. | Interviews or data show a different buying trigger, budget owner, or price response. | The current product and team serve it with no change. |
| 3 | Estimable from a proxy with a known error. | Some signal of a different need, not yet tested. | Needs a feature or channel you can add this year. |
| 1 | No way to count it. | Same needs and response as the neighbor segment. | Needs a different product or a team you do not have. |

A segment becomes TARGET when it passes both gates and the mean of the three scores is at least 3.5. Otherwise it is WATCH.

## 5. Segmentation bases

| Basis | Example | Strength | Weakness |
|---|---|---|---|
| Firmographic or demographic | Fleets with 50-199 trucks. Owners under 40. | Easy to count and target. | Often fails differentiable: the slice buys like its neighbors. |
| Needs-based (jobs to be done) | Carriers that run their own repair shop. | Predicts response to an offer. | Harder to count. Needs a proxy. |
| Behavioral | Carriers that switched software in the last two years. | Shows readiness to buy. | Data is often private. |

The strongest segment pairs a needs-based core with a firmographic proxy you can count and reach. The script flags a `demographic` basis. A demographic slice is a segment only when evidence shows it responds differently.

## 6. Verdicts and next steps

| Verdict | Meaning | Next step |
|---|---|---|
| TARGET | Passes both gates, with evidence for fit. | Size it in the brief. Plan the survey quota for it. Recommend a program. |
| WATCH | Passes both gates, but fit is weak or unproven. | Name the one test that would raise the weakest score. |
| DROP | Fails substantiality or accessibility. | State the failing number. Revisit only if that number changes (new channel, new price). |

Competitive intelligence that feeds these fields must use public or properly obtained sources. Do not misrepresent who you are to get pricing or customer data (SCIP Code of Ethics).

## Sources

- Kotler, P., and Keller, K. L., *Marketing Management*, Pearson (segmentation criteria).
- Smith, W. R., "Product Differentiation and Market Segmentation as Alternative Marketing Strategies", *Journal of Marketing*, 1956.
- Christensen, C. M., Hall, T., Dillon, K., and Duncan, D. S., *Competing Against Luck*, Harper Business, 2016.
- Porter, M. E., *Competitive Strategy*, Free Press, 1980.
- SCIP, *Code of Ethics for CI Professionals*.
