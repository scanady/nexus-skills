# Segmentation and ICP Fit

Decision: which customers get how much CS investment, and why? Tool: `scripts/segment_designer.py`.

## Failure mode

"All customers equal." Cannot be done. Should not be done. Result: strategic accounts starve (loudest wins sponsor time), SMB gets over-served (kills unit economics), misfits eat budget meant for next strategic win. Fix = differential investment: more time and money per ARR dollar for high-fit, high-value accounts; less or none for low-fit, low-value.

## Four tiers

ARR floors are B2B SaaS baseline. Shift to match your ACV spread.

| Tier | ARR | Share of customers | Share of ARR | Coverage | Spend per account per year |
|---|---|---|---|---|---|
| Strategic | $100K+ | about 5% | 30-50% | Named CSM, executive sponsor, dedicated implementation | $20K-50K |
| Enterprise | $20K-100K | 15-20% | 25-35% | Named CSM | $5K-15K |
| Mid-market | $5K-20K | 30-40% | 15-25% | Pooled CSM, automation | $1K-3K |
| SMB / long tail | under $5K | 40-50% | under 10% | Tech-touch, self-serve | $50-500 |

Hallmarks:
- **Strategic:** multi-year contract; QBR and EBR; custom integration; roadmap input; executive on both sides; reference expected
- **Enterprise:** annual contract; quarterly check-in; standard integrations; one CSM; sponsor only if escalated
- **Mid-market:** one CSM per 50-150 accounts; auto-renew; self-serve onboarding with human option; trigger-based touch
- **SMB:** fully self-serve; email and community support; one CSM for whole tier as escalation handler; price-sensitive

Health segment mapping: strategic and enterprise use the **enterprise** health column; mid-market uses **mid-market**; SMB uses **smb** ([health-scoring-model.md](health-scoring-model.md)). The designer prints `health_segment`.

Shape check: over 30% of customers strategic = company is not choosing. Over 70% SMB = PLG business; design CS, product, pricing for it.

## ICP fit score (0-10)

ARR alone misleads. A $50K misfit may cost more than it earns.

| Signal | Points | Why |
|---|---|---|
| in_target_industry | 2.0 | Industry fit drives product fit |
| uses_target_workflow | 2.0 | Strongest retention predictor |
| in_target_size_range | 1.5 | Wrong size = wrong needs |
| has_executive_sponsor | 1.5 | Single-threaded accounts churn 3-5x more |
| advocates_publicly | 1.0 | Forward signal |
| expansion_potential_high | 1.0 | Customers are next revenue round |
| competitor_concentration_low | 1.0 | High concentration = price war |

| Score | Action |
|---|---|
| 8-10 | Invest hard, whatever current ARR |
| 5-7 | Standard tier investment |
| under 5 | Tech-touch only, or kill list |

Weights are defaults. Replace with fit signals from your own retained vs churned accounts.

## Kill list

Five checks. One hit = watch. Two or more = kill candidate.

1. ICP fit under 5
2. Yearly serving cost over 50% of ARR
3. Tenure under 12 months and 2+ escalations
4. Acquired by a conflicting company
5. In a declining or closing industry

Three paths: (a) do not renew; send notice 60-90 days before term end; (b) downgrade to tech-touch and let them self-serve; (c) reprice to recover cost. Accept either outcome of (c).
Anti-pattern: "strategic" accounts that are kill candidates. Founders guard first 5-10 customers long past economic sense. Quarterly audit forces the talk.

## Tier migration

| Move | Gate (besides ARR floor) |
|---|---|
| SMB to mid-market | Tenure 12+ months and ICP fit 6+ |
| Mid-market to enterprise | Executive contact |
| Enterprise to strategic | Multi-year deal, executive sponsor, high expansion potential |
| Down a tier | ARR below floor or ICP fit drops, confirmed in quarterly review |

Supply `current_tier` per customer to get promote / hold / demote. Review every account above $5K each quarter. Below $5K, automation assigns tier.

## Why this is strategy, not ops

Segmentation says which customers the company exists to serve. Wrong answer misfires CS team, roadmap, and pricing together.

## Segmentation audit (1 day)

1. Build input: ARR, tenure, ICP signals, serving cost
2. Run designer; read tier mix and ARR shares
3. List migrations and kill list for sales review
4. Output: new tier per account, spend per tier, kill list with chosen path

Sizing the team for new tiers: [coverage-model.md](coverage-model.md). For marketing-side segmentation and personas, use a marketing skill; this one covers post-sale tiers only.
