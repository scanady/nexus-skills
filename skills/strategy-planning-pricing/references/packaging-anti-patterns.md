# Packaging Anti-Patterns

Load at step 6 (build tiers), in Mode 2 audits, and before any tier ships. Scan tier table against each pattern. Any hit → name it in output, fix before price point.

Value metric problems live in `value-metrics-and-models.md` §3. This file = what sits in each tier and how tiers relate.

## Contents

1. [Quick scan](#1-quick-scan)
2. [Patterns](#2-patterns)
3. [Audit procedure](#3-audit-procedure)
4. [Sources](#4-sources)

## 1. Quick scan

Thresholds = heuristics 🟡. Treat as trigger for closer look, not verdict.

| # | Pattern | Test | Severity |
|---|---|---|---|
| 1 | Transparent decoy | Top price > 2x middle, value < 1.5x middle | High |
| 2 | Feature dump at top | Top features > 2x middle count, price < 1.5x middle | High |
| 3 | No upgrade trigger | Cannot name one event pushing tier N → N+1 | High |
| 4 | Hidden meter | Flat tier with buried overage per unit | High |
| 5 | Loss-leader entry | Entry price below price floor, or COGS > 80% of price | Medium-high |
| 6 | Unanchored top | "Contact sales" with no "from $X" and no qualifying criteria | Medium |
| 7 | Clone feature | Same feature, same scope, every tier | Low |
| 8 | Tier sprawl | > 4 self-serve tiers | Medium |
| 9 | Buried hero | Middle tier not best value per dollar for target segment | Medium |

## 2. Patterns

### 1. Transparent decoy

**Looks like:** middle tier exists only to make top look sane, or top exists only to make middle look cheap. Gap fake: thin features, cosmetic difference.
**Detect:** top/middle price ratio > 2.0 while value delivered (key features, limits, or MaxDiff score sum) < 1.5x middle.
**Hurts:** buyers spot it. Trust in whole price list drops. Sales gets "why so much?" on every deal.
**Fix:** close gap with real value (higher metric limit, admin, compliance) or cut top price. Decoy fine only when decoy tier still sells to real buyer.

### 2. Feature dump at top

**Looks like:** every roadmap item lands in top tier "because enterprise wants it". Top has 3x features for 2x price.
**Detect:** top feature count > 2x middle, price ratio < 1.5x.
**Hurts:** top tier = bargain nobody needs. Middle buyers see gap too big, never move. Roadmap value leaks.
**Fix:** move 1-3 trigger features down to middle, raise middle. Keep top for features only large buyers need (SSO, audit log, SLA, custom contract).

### 3. No upgrade trigger

**Looks like:** tier copy says "advanced features". Nobody can name moment customer outgrows tier.
**Detect:** finish sentence "customer upgrades when ___" for each step. Blank or vague → hit. MaxDiff: middle-tier features score lower than entry features → hit.
**Hurts:** customers park in entry tier. Expansion depends on sales push. Most buyers pick cheapest when tiers lack clear difference.
**Fix:** pick 1-2 pain-moment gates per step: metric limit reached (5th seat, 10k calls, 3rd location), team need (permissions, approvals), risk need (SSO, audit). Tie gate to value metric when possible.

### 4. Hidden meter

**Looks like:** "Pro: up to 100k events, then $X per 1k" in small print. Two models dressed as one.
**Detect:** manual. Read pricing page and contract terms. Overage not shown next to tier price → hit.
**Hurts:** first overage bill feels like trick. Churn and support load spike. Procurement flags it in renewals.
**Fix:** pick one. Flat tier with honest hard cap and upgrade prompt, or open hybrid: platform fee + visible meter + usage alerts + calculator. Never bury meter.

### 5. Loss-leader entry

**Looks like:** entry tier so cheap cost to serve eats revenue. Value per dollar so good nobody leaves it.
**Detect:** entry price below price floor (COGS ÷ (1 − target margin); `pricing_modeler.py` flags). Severe: COGS > 80% of entry price.
**Hurts:** acquisition cost recovers only through upgrades that never come. Entry tier grows, margin shrinks.
**Fix:** raise entry to floor, cut entry limit, or move one feature up. If entry exists for acquisition only, make it free tier with hard limits and own its cost in CAC.

### 6. Unanchored top

**Looks like:** top tier lists features, price says "Contact sales", nothing else.
**Detect:** no "from $X", no seat or usage minimum, no qualifying line ("for teams of 50+").
**Hurts:** budget-limited buyers disqualify themselves silently. Competitors with published ranges win shortlist. Sales spends calls on poor fits.
**Fix:** publish "from $X/mo" or "from $X/yr" anchor. Number need not be exact. Job = qualify right buyers, screen wrong ones. Pre-revenue with no enterprise data → show qualifying criteria only.

### 7. Clone feature

**Looks like:** "API access ✓ ✓ ✓" in every column, same scope.
**Detect:** feature appears in all tiers with identical limits.
**Hurts:** wastes comparison space. Hides real differences. Weakens upgrade story.
**Fix:** move to "All plans include" line above table, or differentiate scope (rate-limited → metered → unlimited).

### 8. Tier sprawl

**Looks like:** 5-7 self-serve tiers, each a small step.
**Detect:** > 4 self-serve tiers, or two adjacent tiers within 1.3x price with near-identical features.
**Hurts:** choice overload. Buyers stall or default to cheapest. Support explains differences forever.
**Fix:** merge to 3 (4 with Enterprise). Use add-ons for niche needs instead of new tiers.

### 9. Buried hero

**Looks like:** middle tier meant to be main seller, but entry or top gives better value per dollar for target buyer.
**Detect:** > 70% of customers on entry or top tier (`pricing_modeler.py` crowding flag). Or middle price > 3x entry with < 2x value.
**Hurts:** revenue mix drifts away from plan. Anchoring fails.
**Fix:** middle 2-3x entry price with clear trigger features. Mark "Recommended". Top tier priced to anchor middle, not to sell volume.

## 3. Audit procedure

1. Build tier table: tier, monthly price, metric limit, feature list, customer count (if live).
2. Compute ratios: middle/entry price, top/middle price, feature counts per tier.
3. Run quick scan 1-9. Record hits with evidence (numbers, quotes from page).
4. Check value-metric red flags (`value-metrics-and-models.md` §3). Metric hit outranks packaging hit. Fix metric first.
5. Write fix per hit. Order: metric → triggers (3) → hidden meter (4) → ratios (1, 2, 9) → floor (5) → page clean-up (6, 7, 8).
6. Re-score tier table after fixes. Zero High hits before ship.

Output row per hit:

| Pattern | Evidence | Fix | Owner |
|---|---|---|---|

## 4. Sources

Thresholds and patterns draw on:

- Madhavan Ramanujam & Georg Tacke, *Monetizing Innovation* (2016). Feature shock, minivation, undifferentiated tiers. Maps to patterns 2, 3, 7.
- Patrick Campbell, ProfitWell / Paddle subscription pricing research. Upgrade triggers and net revenue retention.
- Kyle Poyar, *Growth Unhinged*. Pricing page anatomy, PLG to enterprise transition. Maps to patterns 5, 6.
- OpenView SaaS benchmarks and Bessemer Venture Partners vertical SaaS writing. Tier mix and tier count.
- Simon-Kucher & Partners global pricing studies. Pricing page complexity vs conversion. Maps to patterns 4, 8.
- SaaS Capital spending benchmarks. Cost to serve by ACV band. Basis for pattern 5 severe threshold.
