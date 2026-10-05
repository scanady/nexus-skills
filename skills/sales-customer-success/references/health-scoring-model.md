# Health Scoring Model

Rules behind `scripts/health_scorer.py`. Score 0-100. Four dimensions. Segment targets. Segment cutoffs. Trend decides priority.

## Dimensions and weights

| Dimension | Weight | Why this weight |
|---|---|---|
| Usage | 30% | Most objective. Decline precedes churn. Not higher: seasonal usage misleads |
| Engagement | 25% | Shows relationship beyond product use. Meetings without usage = evaluating. Usage without meetings = self-serving or fading |
| Relationship | 25% | Best defence against rival. Strong ties buy second chances |
| Support | 20% | Lagging. Damage already done. Still strong churn predictor when engagement also falls |

Weights are defaults. `calibrate_scoring.py` refits them from churn history ([calibration-method.md](calibration-method.md)).

## Metrics inside each dimension

"Up" metric: score = value / target, cap 100. "Down" metric: score = 1 - value / limit, floor 0.

| Dimension | Metric | Direction | Sub-weight |
|---|---|---|---|
| Usage | login_frequency | up | 35% |
| | feature_adoption | up | 40% |
| | dau_mau_ratio | up | 25% |
| Engagement | support_ticket_volume | down | 20% |
| | meeting_attendance | up | 30% |
| | nps_score | up | 25% |
| | csat_score | up | 25% |
| Support | open_tickets | down | 35% |
| | escalation_rate | down | 35% |
| | avg_resolution_hours | down | 30% |
| Relationship | executive_sponsor_engagement | up | 35% |
| | multi_threading_depth | up | 30% |
| | renewal_sentiment | label | 35% |

Renewal sentiment: positive 100, neutral 60, unknown 50, negative 20. Sentiment is a human guess. Never let it carry a score alone.

## Segment targets

| Metric | Enterprise | Mid-market | SMB |
|---|---|---|---|
| login_frequency (%) | 90 | 80 | 70 |
| feature_adoption (%) | 80 | 70 | 60 |
| dau_mau_ratio | 0.50 | 0.40 | 0.30 |
| support_ticket_volume (max) | 5 | 8 | 10 |
| meeting_attendance (%) | 95 | 85 | 75 |
| nps_score | 9 | 8 | 7 |
| csat_score | 4.5 | 4.0 | 3.8 |
| open_tickets (max) | 10 | 15 | 20 |
| escalation_rate (max) | 0.25 | 0.30 | 0.40 |
| avg_resolution_hours (max) | 72 | 96 | 120 |
| executive_sponsor_engagement | 90 | 75 | 60 |
| multi_threading_depth | 5 | 3 | 2 |

Strategic accounts use the enterprise column. Segment missing or unknown = error, not silent fallback.

## Segment cutoffs

| Segment | Green at least | Yellow at least | Red below |
|---|---|---|---|
| Enterprise | 75 | 50 | 50 |
| Mid-market | 70 | 45 | 45 |
| SMB | 65 | 40 | 40 |

Enterprise bar higher: complex deployments, higher expectation. SMB bar lower: simpler use, lighter engagement. One shared cutoff misreads both ends.

## Missing data

Skip missing metric. Renormalise remaining sub-weights. Skip dimension with no metrics. Renormalise dimension weights. Report `data_coverage` (share of weight observed). Coverage under 70% = say so before acting on the band. A sparse record must never score as a bad one.

## Trend

| Trend | Rule |
|---|---|
| improving | current above previous by more than 5 points |
| stable | within 5 points |
| declining | current below previous by more than 5 points |
| no_data | no previous score. Treat as stable. Set `baseline_missing`. Save this score as baseline |

Previous scores come from `previous_period` (dimension scores plus `overall_score`).

## Trend-priority matrix

Snapshot says where account is. Trend says where it goes. Priority uses both.

| Band | Declining | Stable | Improving |
|---|---|---|---|
| Green | HIGH. Intervene before it falls | LOW. Standard cadence, look for expansion | LOW. Reinforce |
| Yellow | CRITICAL. Path leads to red | MEDIUM. Find root cause, raise touch | MEDIUM. Back the momentum |
| Red | CRITICAL | CRITICAL. Current approach failed; change it | HIGH. Support the recovery |

Order the queue by priority, then by ARR descending. Declining green outranks stable yellow in urgency of attention, not in ARR size.

| Priority | Response time | Owner |
|---|---|---|
| CRITICAL | 48 hours | CSM plus leader |
| HIGH | 1 week | CSM |
| MEDIUM | 2 weeks | CSM |
| LOW | Next scheduled touch | CSM or automation |

## Profile file

`--profile` accepts the file `calibrate_scoring.py --write-profile` writes:

```json
{"dimension_weights": {"usage": 0.36, "engagement": 0.24, "support": 0.14, "relationship": 0.26},
 "thresholds": {"enterprise": {"green_min": 68, "yellow_min": 60}}}
```

Weights must sum to 1.0. `green_min` must exceed `yellow_min`. Segments absent from file keep defaults.
