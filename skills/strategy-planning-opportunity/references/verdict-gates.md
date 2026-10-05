# Verdict Gates

How rubric scores become one decision. Weighted score sets base. Gates cap it. Tensions get argued in prose. Script: `scripts/opportunity_verdict.py`.

## Why not average

Mean lets strength hide fatal weakness. Pain 9 + monetization 2 can still land "Strong". "Nobody pays" not offset by "big upside".

Two rules override mean:
- **Non-compensatory attributes.** Some dimensions disqualify alone, whatever else scores. Buyer pays or not. (Tversky, elimination by aspects, 1972; Hogarth, *Judgement and Choice*, 1987.)
- **Weakest link.** Business ships only if demand AND payment AND reach AND delivery all clear bar. One failed part sinks system. (Kremer, O-ring theory, QJE 1993.)

Weights = compensatory layer. Gates = non-compensatory layer. Both needed.

## Layer 1 — Base decision from band

| Weighted score | Base decision |
|---:|---|
| 70+ | Grow if stage revenue/active; Run for Cash if also cash/lifestyle goal and market ≤5; else Launch |
| 55–69 | Validate |
| 40–54 | Pivot if pain ≥6 (core insight real), else Park |
| <40 | Kill; Remove if portfolio ≤3 |

Weights per profile live in `scoring-rubric.md`. Script mirrors them. Change one, change both.

## Layer 2 — Veto gates

| Gate | Trips when | Meaning |
|---|---|---|
| Demand | pain ≤3 | No specific painful job. No buyer to sell to. |
| Payment | monetization ≤3 | Buyer won't pay or unit economics fail on paper. |
| Reach | distribution ≤2 | No credible path to buyer at affordable cost. |
| Capacity | execution ≤2 | Build/ops/compliance load beyond resources. |
| Fatal flaw | stress-test objection landed (`fatal_flaw` text) | Load-bearing assumption broken. Pre-mortem hit. (Klein, HBR 2007.) |

Cap rules, in order:
1. Demand or payment gate AND score <55 → **Kill**.
2. Two+ gates AND score <70 → **Kill**.
3. Gate on **low** evidence → cap **Validate**. Low score may mean "unknown", not "bad". Test gated dimension first.
4. Gate on medium/high evidence → cap **Pivot**. Dimension known weak. Change it.

Gates only lower. Never raise. Base already below cap → base stands. Founder-fit not gated: fit can be borrowed (cofounder, partner, hire).

## Layer 3 — Tension detection

Named pairs. Flag when high side minus low side ≥4.

| Tension | High | Low | Verdict must answer |
|---|---|---|---|
| Hurts, but no wallet | pain | monetization | Other buyer or budget line pays? |
| Big market, no road in | market | distribution | One owned/affordable channel to first niche? |
| Real pain, unreachable buyer | pain | distribution | Ride existing channel, partner, marketplace? |
| Price logic without pull | monetization | pain | Real job, or spreadsheet-only model? |
| Big market, nobody hurting | market | pain | Which narrow segment feels acute version? |
| Right wave, wrong surfer | timing | fit | Edge owned or borrowable before others move? |
| Moat too costly to dig | defensibility | execution | Cheaper wedge first, moat later? |
| Right founder, wrong slot | fit | portfolio | Beats best other use of same hours/capital? |

Fallback: widest gap ≥5 among dimensions weighted ≥10% for profile, when no named pair covers it. Low-weight dims skipped. Micro project with weak moat = normal, not tension.

Tension = real argument. Verdict "Why" line settles it. Pick side. Say what evidence would flip it. Dialectical inquiry: value sits in clash of thesis and antithesis, not in smoothing it. (Mason & Mitroff, 1981; Cosier & Schwenk, 1990.)

## Layer 4 — Confidence

Start at stated evidence level (rubric). Then cap:
- widest tension ≥6 → Low
- widest tension ≥4 → Medium max
- gate lowered decision → Medium max

Never raise. Same 66 score means different things when dimensions agree vs when 9 fights 2. Aggregate trust grows with judge convergence. (Surowiecki, 2004.)

## Layer 5 — Riskiest assumption

Pick order:
1. `riskiest` override in spec (from stress-test, step 5). Use when risk = retention or assumption cuts across dimensions.
2. Lowest-scoring tripped score gate.
3. Largest weighted shortfall: `weight × (10 − score)` across testable dims.

Dimension → test category: pain/market/timing → demand · monetization → price · distribution → channel · execution/fit → feasibility · defensibility → differentiation. Portfolio = allocation choice, not testable. Test card from `cheapest-tests.md`.

## Disagree with the call?

Don't hand-edit decision. Find score that is wrong. State reason. Change score. Re-run. Call stays reproducible; reasoning stays visible.

## Script does NOT

Write "Why" prose, financial sketch, adjacent alternatives, or secondary category. Analyst owns those. Script fixes decision, confidence, gates, tensions, riskiest test.
