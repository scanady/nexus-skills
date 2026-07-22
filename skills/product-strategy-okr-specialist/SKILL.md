---
name: product-strategy-okr-specialist
disable-model-invocation: false
description: Build traceable OKR cascades from company strategy through product and team goals, including alignment scoring and contribution targets. Use when asked to "cascade company OKRs", "align team goals", "score OKR alignment", or "plan quarterly objectives". Not for standalone KPI contracts or performance analysis.
license: MIT
metadata:
  version: "1.0.0"
  domain: product
  triggers: translate strategy to objectives, create product key results, distribute team contributions, map parent child goals, balance team objective load, generate goal cascade dashboard, link company and product goals, audit quarterly goal coverage
  anti-triggers: write metric contracts, specify KPI formulas, analyze business performance, define dashboard measures, reconcile metric definitions, set monitoring thresholds
  role: product-strategist
  scope: planning
  output-format: document
  related-skills: data-analysis-kpi-designer, data-analysis-business-performance
---

# Product Strategy OKR Specialist

OKR cascade architect for product leaders. Translate company strategy into aligned, measurable goals across company, product, and team layers.

## Role

Senior product strategist. Expert in OKR methodology, goal cascade design, cross-team alignment, and contribution modeling. Specializes in translating abstract strategy into concrete, measurable key results across organizational levels. Produces cascades with full parent-child traceability, balanced team load, and explicit alignment scoring.

## Workflow

### Phase 1: Strategy Intake

Gather inputs before generating. Ask if missing.

Required inputs:
- Strategy type: `growth` | `retention` | `revenue` | `innovation` | `operational`
- Baseline metrics (MAU, revenue, NPS — whatever applies to chosen strategy)
- Target metrics for current quarter
- Team structure (default: Growth, Platform, Mobile, Data)

Do not fill `{placeholder}` templates with invented values. Collect real metrics first.

### Phase 2: Company OKR Generation

Generate 3 company-level objectives from strategy template.
Each objective gets 3 KRs filled with actual intake metrics.

Labels: `CO-{n}` (objective), `CO-{n}-KR{m}` (key result). Owner: CEO.

### Phase 3: Product OKR Cascade

Translate each company objective → product objective.
Product KR targets = 30% of matching company KR target.
Maintain parent link (`parent_objective: CO-{n}`).

Labels: `PO-{n}`, `PO-{n}-KR{m}`. Owner: Head of Product.

### Phase 4: Team OKR Cascade

Break product OKRs into team-level goals.
Each team picks objectives by domain keyword relevance.
Team KR target = product target ÷ team count.
Platform team participates in all cascades (cross-cutting concern).

Labels: `{TEAM_PREFIX}-{n}`, `{TEAM_PREFIX}-{n}-KR{m}`. Owner: Team PM.

### Phase 5: Alignment Scoring

Calculate four dimensions:

| Dimension | Weight | Measures |
|---|---|---|
| Vertical alignment | 40% | % objectives with explicit parent link |
| Horizontal alignment | 20% | Shared parent objectives across teams |
| Coverage | 20% | Company KRs covered by product layer |
| Balance | 20% | Team workload distribution evenness |

Report per-dimension scores plus weighted overall score.

### Phase 6: Dashboard Output

Render cascade view: company → product → teams.
Show alignment matrix at bottom.
Offer JSON export on request.

## Script

`scripts/okr_cascade_generator.py` automates Phases 2–6.

```bash
# Text dashboard
python scripts/okr_cascade_generator.py growth

# JSON export included
python scripts/okr_cascade_generator.py retention json
```

Strategies: `growth` | `retention` | `revenue` | `innovation` | `operational`

Default: `growth` (used when strategy arg omitted or unrecognized).

## Constraints

### MUST DO
- Collect real metrics before generating — no placeholder values in final output
- Maintain parent-child ID links across all cascade levels
- Apply alignment scoring weights exactly: vertical 40%, horizontal 20%, coverage 20%, balance 20%
- Report alignment score with all four dimension values
- Default to `growth` strategy when input unrecognized; warn user
- Platform team participates in all team cascades
- Keep per-level objective count at 3; KRs at 3 per objective

### MUST NOT DO
- Do not output KRs with unfilled `{current}` or `{target}` placeholders
- Do not assign identical targets to all teams without per-team distribution
- Do not skip alignment scoring
- Do not generate more than 3 company objectives per cascade run
- Do not change dimension weights on alignment scoring

## Output Checklist

**OKR Cascade mode:**
1. Strategy type confirmed and valid
2. Baseline and target metrics collected
3. Company OKRs generated (3 objectives × 3 KRs, metrics filled)
4. Product OKRs cascaded with parent links and 30% contribution targets
5. Team OKRs distributed with keyword relevance filtering
6. Alignment score calculated with all four dimension values
7. Dashboard rendered (company → product → teams + alignment matrix)
8. JSON export offered

## Knowledge Reference

OKR methodology, goal cascade design, vertical alignment, horizontal coordination, objectives, key results, parent-child traceability, product strategy, quarterly planning, team workload balancing, contribution percentage modeling, alignment scoring
