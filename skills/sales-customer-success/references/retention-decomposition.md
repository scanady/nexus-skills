# Retention Decomposition

Decision: is our retention number honest, and where does it leak? Tool: `scripts/retention_decomposer.py`.

## The trap

"NRR is 115%, retention is great." Not proof. 85% GRR plus 30% expansion = 115% NRR, and 15% of paying customers still failed. Survivors' growth hides it. Always split:

```
GRR = (start - churned - contraction) / start
NRR = GRR + expansion / start
Logo retention = 1 - churned logos / starting logos
```

Leaky bucket: NRR at 100% or more with GRR below the "concerning" line. Acquisition holds the number up; expansion will not outrun churn forever.

## Thresholds by stage

| Metric | Stage | Healthy | Concerning | Critical |
|---|---|---|---|---|
| GRR | Seed / A | 85% or more | 75-85% | under 75% |
| | Growth (B) | 90% | 85-90% | under 85% |
| | Scale | 95% | 90-95% | under 90% |
| NRR | Seed / A | 100% | 95-100% | under 95% |
| | Growth | 110% | 100-110% | under 100% |
| | Scale | 120% | 110-120% | under 110% |
| Logo | Seed / A | 80% | 70-80% | under 70% |
| | Growth | 85% | 80-85% | under 80% |
| | Scale | 90% | 85-90% | under 85% |

Logo thresholds sit about 5 points under GRR. Logo gap vs GRR shows who leaves: many small accounts (logo low, GRR fine) or few big ones (GRR low, logo fine).
Contraction target: under 5% per year. Expansion at healthy company: 15-25% per year.

Use GRR as truth metric. Use NRR only beside GRR.

## Cohorts

Cut by acquisition cohort (quarter or month). Reporting-period retention mixes vintages and hides the leaky one.

| Pattern | Meaning |
|---|---|
| Cohort GRR improving | Product and onboarding maturing |
| Flat | Stable. No regression, no gain |
| Degrading | Newer cohorts churn faster: quality regression, ICP drift, or wrong acquisition. Buy less, fix product, or both |

Tool compares newest cohort GRR with mean of earlier ones; 2 points is the drift line.

## Seven churn causes

Tag every churned logo with one.

| Cause | Meaning | Preventable | Fix |
|---|---|---|---|
| product_fit | Product missed the real job | Mostly, long term | Sharpen ICP; fix onboarding mismatch; or price-segment out |
| competitor_loss | Rival won on fit or price | Partly | Competitive intelligence; differentiation; price review |
| no_value_realized | Never reached first value | Yes | Redesign onboarding; milestone tracking; intervention triggers |
| pricing | Too costly or low perceived value | Sometimes | Price-value audit; downsell offer instead of loss |
| champion_left | Champion gone | Partly | Multi-thread; never rely on one contact |
| company_event | Merger, layoffs, shutdown | No | Track frequency; high rate means unstable ICP |
| tactical_failure | Service or support failure | Always | Playbook gaps; response time; escalation paths |

Preventable = product_fit + no_value_realized + tactical_failure. Over 50% = CS has clear leverage. Under 30% = mostly structural (ICP, market, rivals). In between = mixed.
Churn reasons must add up to churned logos. Tool reports the gap.

## Leading indicators

Customer who cancels is already 60-90 days gone. Watch earlier.

- **Product:** weekly drop in daily active users; fewer features per session; fewer API calls; no login from any user for 14+ days
- **Commercial:** failed or late payment; seat reduction; champion ducks QBR scheduling; customer-side team reshuffle
- **Sentiment:** NPS or CSAT down over 2; ticket spike; negative tone in tickets; public complaint

Build the health score from 3-5 of these; calibrate it ([calibration-method.md](calibration-method.md)).

## NPS and CSAT

Good for: quarter-over-quarter trend; segment comparison; moments (after onboarding, after renewal).
Bad for: benchmarking against other firms (method varies); predicting one account's churn; one-shot verdicts.

## Quarterly retention review (4 hours)

1. Pull cohorts for the last 8 quarters
2. Run the decomposer; read GRR, NRR, contraction, expansion apart
3. For each cohort with GRR under 90%, assign the cause taxonomy
4. Check expansion math with sales leadership; check product gaps with product leadership
5. Output: top three leaks, 90-day mitigation plan
