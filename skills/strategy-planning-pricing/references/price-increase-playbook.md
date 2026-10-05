# Price Increase Playbook

Load in Mode 3 (Raise Prices). Pair with `scripts/pricing_modeler.py` for numbers.

## Contents

1. [Go / no-go](#1-go--no-go)
2. [Strategy matrix](#2-strategy-matrix)
3. [Execution checklist](#3-execution-checklist)
4. [Customer notice template](#4-customer-notice-template)
5. [Monitor and stop rules](#5-monitor-and-stop-rules)

## 1. Go / no-go

Raise only when all hold:

| Check | Pass | Fail action |
|---|---|---|
| Churn | Monthly logo churn ≤ 5% (SMB) or ≤ 1.5% (mid-market). | Fix retention first. Increase speeds up churners. |
| Value story | Specific new value since last price, or price clearly below market. | Ship value or gather proof first. |
| Signal | Conversion signal `healthy` or `underpricing`, or win rate rising with no price pushback. | Fix funnel friction, not price. |
| Break-even | Expected base loss < modeler break-even loss for chosen increase. | Smaller increase, or new-customers-only. |
| Contract room | Contracts allow change with notice. | Wait for renewal dates. |

Break-even base loss = increase ÷ (1 + increase). 10% → 9.1%. 20% → 16.7%. 30% → 23.1%. Lose more of base than that → MRR drops.

## 2. Strategy matrix

Pick one row per segment. Different segments can get different rows.

| Strategy | Use when | Revenue speed | Churn risk | Trust cost | Ops effort |
|---|---|---|---|---|---|
| New customers only | Pushback expected, base fragile, testing price. | Slow | Very low | None | Low |
| Grandfather with end date | Loyal base, need to respect history. | Medium | Low | Low | Medium |
| Tied to new value | Big release, new tier, new capability. | Medium | Low | Low | Medium |
| Plan restructure | Packaging or metric change, not just number. | Medium | Medium | Medium | High |
| Annual lock-in offer | Want cash and retention, monthly base large. | Fast cash | Low | Low | Low |
| Uniform increase | Price far below market, value clear, churn low. | Fast | Medium-high | Medium | Low |

Rules:
- Start with new customers only when no price test exists yet. Use result to set base increase.
- Grandfather always has end date. Open-ended grandfather = permanent two-price system.
- Restructure ≠ hidden increase. Customer must see what changed and why.
- Never move metric and raise price same release. Two changes → unreadable churn signal.

## 3. Execution checklist

| # | Step | Owner | Output |
|---|---|---|---|
| 1 | Model it. Run modeler: scenarios, rollout mode, break-even, retention table at 100/90/80/70%. | Pricing lead | Chosen increase + rollout. |
| 2 | Segment base by risk: annual contracts, renewal dates, champions vs detractors (NPS/health), usage-heavy accounts, top 20 by revenue. | CS lead | Risk list with treatment per segment. |
| 3 | Pick strategy per segment from matrix. | Pricing lead | Segment → strategy table. |
| 4 | Set dates. Notice 60-90 days for existing customers. 30 days minimum. Respect contract terms. | Finance + legal | Effective date per segment. |
| 5 | Write reason. Specific: features shipped, cost changes, investment planned. No vague "to serve you better". | Marketing | Notice + FAQ. |
| 6 | Offer path. Annual lock at current price, or window to switch plan. One offer, clear deadline. | Pricing lead | Offer terms. |
| 7 | Arm CS and sales. FAQ, talking points, discount authority with limit and approver. | CS lead | Enablement doc. |
| 8 | Personal outreach to top accounts before mass notice. | Account owners | Calls logged. |
| 9 | Send notice. Update pricing page and billing same day for new customers. | Marketing + eng | Live prices. |
| 10 | Monitor 60-90 days (section 5). | Pricing lead | Weekly report. |

## 4. Customer notice template

Plain. Specific. No spin.

```
Subject: Your [Product] price changes on [date]

On [date], [plan] moves from [old price] to [new price] per [unit].

Why: since [last change date] we shipped [2-3 specific things] and [cost or investment reason].

What you can do:
- Keep your current price for 12 months by switching to annual before [deadline].
- Move to [other plan] at any time if it fits better.

Nothing changes before [date]. Questions: reply here or book time with [owner].
```

## 5. Monitor and stop rules

Track weekly vs pre-notice baseline, per segment:

| Metric | Watch | Stop / rethink trigger |
|---|---|---|
| Logo churn | Weekly rate vs baseline. | Cumulative extra churn approaches break-even loss. |
| Downgrades | Plan moves down. | Downgrade spike in one tier → tier gap too wide. |
| New-customer conversion | Trial or demo close rate. | Drop larger than modeled loss for 3+ weeks. |
| Support tickets on price | Volume and tone. | Same objection repeating → fix FAQ or offer. |
| Expansion | Upgrades, seat adds. | Expansion stall in raised segment. |
| Net MRR | Total after churn and uplift. | Below no-change projection after 60 days. |

Expected: 20-30% increase often costs 5-15% extra churn over notice period 🟡. Net MRR positive → hold. Negative → stop rollout for remaining segments, keep raised price for new customers, review value story.
