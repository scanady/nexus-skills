# KPI Readout Patterns

Load this reference only after the audience, cadence, decision, and delivery surface are known. These patterns control emphasis, not analytical rigor. Complete the evidence, comparability, pacing, and driver checks before formatting.

## Pattern Selection

| Pattern | Best for | Primary question |
|---|---|---|
| Inline update | Chat, email, short memo | What changed and what happens next? |
| KPI scorecard | Fast comparison across metrics | Where is attention required? |
| Weekly operating review | Near-term execution | What changed this week and what will we do now? |
| Monthly business review | Trend and plan management | Are we on plan and why? |
| Quarterly business review | Strategic performance | What did we learn and what must change next quarter? |

## Inline Update

Keep to five blocks:

1. one-sentence status and implication
2. two to five headline actuals with comparison and target or pace
3. one to three drivers labeled by evidence level
4. action, owner, and date
5. one material qualification, if needed

Do not add background that the audience already knows. Put a qualification immediately after the affected number.

## KPI Scorecard

Use when leaders need to scan several metrics with a common status system.

| KPI | Actual | Prior / benchmark | Target / pace | Status | Driver or note |
|---|---:|---:|---:|---|---|

Order rows by decision importance, then by status severity. Keep definitions stable across editions. Put detailed decomposition below the table rather than inside cells.

Status labels must share a declared threshold system. When metrics use different rules, link each row to its own threshold basis or show the basis in a note.

## Weekly Operating Review

Emphasize short feedback loops and commitments:

```markdown
## This Week In One Line
[Status, movement, implication]

## Scorecard
[Compact metric table]

## What Changed
[Largest verified movements and immediate drivers]

## Commitments
| Commitment | Owner | Due | Closure signal | State |
|---|---|---|---|---|

## Risks And Escalations
[Only items requiring cross-team attention or a decision]
```

Prefer week-over-week comparison only when weekday mix, holidays, event timing, and data maturity are compatible. Use trailing averages or year-over-year context when a single week is noisy.

## Monthly Business Review

Emphasize plan, trend, and decomposition:

```markdown
## Executive Readout
[Overall status, plan variance, operating implication]

## KPI Scorecard
[Actual, month-over-month, year-over-year when relevant, plan, pace]

## Performance Decomposition
[Largest quantified drivers, supported associations, residual]

## Guardrails And Trade-offs
[Quality, cost, risk, customer, or reliability effects]

## Forecast And Risks
[Forecast only when supplied or separately modeled; distinguish it from actuals]

## Decisions And Actions
[Prioritized register with owners and dates]
```

Use month-over-month and year-over-year together only when both add distinct context. Call out month length, business-day count, seasonality, and accounting close status when material.

## Quarterly Business Review

Emphasize strategic learning and resource decisions:

```markdown
## Quarter Verdict
[Outcome versus plan and strategic implication]

## Outcome And Guardrail Scorecard
[Minimal portfolio, multi-quarter trend, target]

## What Drove The Quarter
[Reconciled decomposition and evidence-ranked context]

## What We Learned
[Which assumptions held, failed, or remain unresolved]

## Strategic Decisions
[Start, stop, continue, reallocate, or escalate]

## Next-Quarter Commitments
| Outcome | Action | Owner | Date | Leading signal |
|---|---|---|---|---|

## Appendix
[Definitions, source notes, detailed cuts, reconciliation]
```

Do not turn a quarterly review into a chronology of activity. Organize around outcomes, drivers, learning, and resource choices.

## Visual Guidance

Use a visual only when it answers a specific comparison:

| Question | Useful form |
|---|---|
| Current status across KPIs | Scorecard or bullet chart |
| Trend and target over time | Line chart with target or control band |
| Contribution to movement | Waterfall only when components reconcile |
| Funnel or process loss | Funnel or stage-conversion table |
| Segment concentration | Sorted bar chart or heatmap |
| Actual versus plan by period | Variance bars or paired lines |

Label units, period, cutoff, target basis, and material breaks. Avoid dual axes unless the relationship cannot be shown clearly another way. Never use a chart to imply causality that the evidence does not establish.

## Recurrence Rules

- Preserve metric names, formulas, order, units, rounding, and status thresholds across editions.
- Version any definition change and state the effective date.
- Restate comparable history when feasible; otherwise mark the series break.
- Carry open actions forward with state changes visible.
- Remove a recurring section only when the owner agrees or the readout explains why it is absent.
- Keep source and cutoff notes concise but sufficient for another analyst to reproduce the result.