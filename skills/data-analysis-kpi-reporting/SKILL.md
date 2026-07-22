---
name: data-analysis-kpi-reporting
description: Convert established metrics into a comparable, evidence-backed operating readout with status, pacing, drivers, and decisions. Use when asked to "prepare a KPI update", "write a WBR", "build an MBR scorecard", or "summarize performance for leaders". Not for choosing KPIs or open-ended diagnosis.
license: MIT
metadata:
  author: nexus
  version: "1.0.0"
  domain: data
  triggers: report weekly results, assemble executive scorecard, compare actuals to budget, explain scorecard movement, prepare quarterly readout, update operating review, assess target pacing, package performance narrative
  anti-triggers: define success measures, design KPI portfolio, reconcile metric ownership, investigate unknown root cause, build financial model, create analytics dashboard
  role: performance-reporter
  scope: reporting
  output-format: report
  priority: specific
  related-skills: data-analysis-kpi-designer, data-analysis-business-context, data-analysis-business-performance
---

# KPI Operating Readout

Turn an established metric set into a recurring decision document. Reproduce the numbers, establish comparability, judge pace against an explicit basis, separate evidence from explanation, and make the next operating decision visible.

## Role Definition

Senior analytics lead specializing in weekly, monthly, and quarterly operating reviews. Combine metric governance, variance interpretation, pacing analysis, and executive communication. The differentiator is reporting discipline: this skill packages known metrics and supported explanations into a repeatable readout; it does not invent a measurement system or disguise exploratory diagnosis as settled fact.

## Boundary

Use this skill when metrics already exist and the task is to report what happened, how performance compares, what is known about movement, and what decision follows.

Use `data-analysis-kpi-designer` when the team must choose metrics or write metric contracts. Consider `data-analysis-business-context` when definitions, ownership, or source authority conflict. Consider `data-analysis-business-performance` when the request requires broad root-cause analysis, financial modeling, scenarios, or strategic recommendations. This skill must still complete a bounded readout when companion skills are unavailable.

If the user requests only a template or mockup, label every sample value as illustrative. Otherwise, do not produce an authoritative readout without actuals from a user-provided or connected source.

## Workflow

### 1. Contract The Review

Establish the readout contract:

- audience and decision owner
- decision, escalation, or operating conversation supported
- reporting period, cutoff timestamp, timezone, and freshness expectation
- cadence: weekly, monthly, quarterly, or one-time
- comparison basis: prior period, prior year, plan, target, forecast, benchmark, or control range
- delivery surface and desired depth

Ask only for missing inputs that could change interpretation. Otherwise state a bounded assumption. Treat the audience's decision as the filter for what belongs in the readout.

### 2. Freeze The Metric Frame

For each headline KPI, record:

- definition, formula, unit, grain, population, and exclusions
- authoritative source and owner
- current and comparison windows
- target, plan, or pacing rule when one exists
- definition version and effective date

Use the existing governed definition. Do not redesign metrics during reporting. When definitions or sources conflict, show the conflict and pause precise interpretation until an owner or authoritative artifact resolves it.

Select the smallest useful metric set:

1. headline outcomes that determine overall status
2. supporting drivers needed to interpret movement
3. guardrails that reveal harmful trade-offs
4. diagnostics only when they answer a live question

### 3. Build The Evidence Ledger

Create a compact internal ledger before writing prose:

| Claim or value | Source | As of | Definition version | Check | Evidence state |
|---|---|---|---|---|---|
| [actual/target/driver] | [artifact] | [timestamp] | [version] | [recompute/reconcile] | [verified/qualified/missing] |

Discover relevant user-provided or connected sources rather than assuming the named dashboard is exhaustive. Compare overlapping sources by ownership, freshness, definition, grain, coverage, and directness. Prefer the current authoritative source; preserve material disagreement.

Stop the authoritative path when a required actual, definition, or comparison source is unavailable. Name the exact dependency. Optional context may be omitted with a visible limitation.

### 4. Reproduce And Reconcile Actuals

Recompute headline values from the strongest available evidence when feasible. At minimum:

- verify units, signs, filters, and time boundaries
- reconcile components to totals within a stated tolerance
- compare against the prior published value or independent control
- inspect missing periods, late data, backfills, and partial windows
- check segment mix or denominator changes when they can move the aggregate

Do not continue from a screenshot, copied number, or stale export as though it were verified when a live source is required and available.

### 5. Pass The Comparability Gate

Before calculating movement, test whether current, comparison, and target values share compatible:

- metric definition and version
- population, segment, and grain
- calendar length, cutoff, and seasonality treatment
- currency, unit, and exchange-rate basis
- data maturity and backfill state

Classify each comparison:

| State | Meaning | Reporting treatment |
|---|---|---|
| Comparable | Differences do not materially change interpretation | Calculate and interpret normally |
| Restated | History was recalculated on the current basis | Label restatement and use it |
| Qualified | Limitation remains but direction is still useful | Show limitation beside the variance |
| Broken | Bases are materially incompatible | Do not calculate a misleading variance |

### 6. Calculate Status And Pace

For each headline KPI, calculate where supported:

- current actual
- absolute variance: $A - B$
- relative variance: $\frac{A-B}{|B|}$, with denominator caveats
- target gap: $A - T$
- period progress and expected pace for time-bound goals
- confidence or evidence state

Use the organization's approved pacing method. If none exists, either ask for one or use a clearly labeled fallback whose assumptions are explicit. Do not assume linear pacing for seasonal, cohort-based, inventory-constrained, or compounding metrics.

Assign `Ahead`, `On track`, `At risk`, or `Off track` only when thresholds and comparison basis are known. Pair every status with text; never rely on color alone.

### 7. Bound The Driver Story

Separate explanations into an evidence ladder:

| Level | Meaning | Allowed wording |
|---|---|---|
| Quantified contribution | Reconciled contribution or validated decomposition | "Contributed" with amount or share |
| Supported association | Timely, scoped relationship with corroboration | "Associated with" or "consistent with" |
| Operating context | Relevant event without measured linkage | "Occurred during" |
| Hypothesis | Plausible but untested explanation | "Hypothesis to test" |

Show the few largest contributors, known non-drivers, and unresolved residual. Use an additive bridge only when components reconcile. State whether movement is broad-based or concentrated when that changes action.

Never promote a launch, campaign, incident, customer event, or market narrative into a cause based only on timing.

### 8. Convert Evidence Into Decisions

Lead with the operating implication:

- what changed and whether it matters
- whether performance is ahead, on track, at risk, off track, or not judgeable
- what is driving the result at each evidence level
- what action, escalation, or diagnostic follows
- owner and due date for each committed action

Recommend an action only when evidence supports it. Otherwise recommend the smallest validation step and name the decision it will unlock. Carry prior commitments forward until closed, superseded, or explicitly dropped.

### 9. Validate And Publish

Before delivery:

1. recalculate displayed variances and pacing values
2. match every material claim to the evidence ledger
3. confirm status labels follow declared thresholds
4. keep qualifications adjacent to affected claims
5. verify totals, dates, units, rounding, and signs
6. distinguish actuals, targets, forecasts, and estimates visually and verbally
7. confirm the headline, evidence, and requested decision agree

Load `references/readout-patterns.md` after the delivery surface and cadence are known. Adapt the selected pattern; do not force every section into every update.

## Reference Guide

| Topic | Reference | Load When |
|---|---|---|
| Readout patterns | `references/readout-patterns.md` | Formatting an inline update, scorecard, weekly review, monthly review, or quarterly review |

## Default Output

```markdown
# [Cadence] KPI Readout — [Scope] — [Period]

## Decision Summary
- **Overall status:** [Ahead / On track / At risk / Off track / Not judgeable]
- **What changed:** [answer-first statement with magnitude]
- **Operating implication:** [why it matters]
- **Decision or escalation:** [owner, action, due date]

## KPI Scorecard
| KPI | Actual | Comparison | Target / pace | Status | Evidence |
|---|---:|---:|---:|---|---|
| [metric] | [value] | [variance and basis] | [gap or pacing] | [text status] | [verified/qualified] |

## Movement And Drivers
- **Quantified:** [driver and contribution]
- **Supported:** [association and evidence]
- **Context:** [event without causal claim]
- **Unresolved:** [residual or hypothesis]

## Actions And Open Decisions
| Priority | Action or decision | Owner | Due | Success / closure signal |
|---|---|---|---|---|

## Comparability And Data Notes
- [definition change, restatement, cutoff, missing data, or other material limitation]

## Source Notes
- [metric or claim]: [source, as-of timestamp, definition version]
```

For a brief inline update, retain only the decision summary, headline scorecard rows, driver evidence, action, and material qualification.

## Constraints

### MUST DO

- Anchor every readout to an audience, period, cutoff, comparison basis, and decision.
- Attribute headline actuals, targets, and driver claims to identifiable sources.
- Gate every variance through a comparability check.
- Show actual, comparison, target or pace, status basis, and evidence state together.
- Separate quantified drivers, supported associations, context, and hypotheses.
- Keep recurring definitions and section order stable unless a change is declared.
- Carry material data limitations next to the affected claim.
- Track actions with an owner, due date, and closure signal.

### MUST NOT DO

- Do not publish placeholders or illustrative values as actual performance.
- Do not infer precise status when definition, cutoff, target, or pacing basis is unresolved.
- Do not compare incompatible periods, populations, units, or metric versions.
- Do not call timing correlation a cause or convert business context into driver evidence.
- Do not hide residual movement behind a polished narrative.
- Do not use traffic-light color without text and declared thresholds.
- Do not flood the readout with every available metric, segment, or caveat.
- Do not redesign the KPI portfolio inside a reporting task.

## Output Checklist

1. Audience, decision, cadence, period, cutoff, and comparison basis are explicit.
2. Headline metrics use stable definitions and attributable sources.
3. Actuals were reproduced or clearly qualified.
4. Comparability state is known for every displayed variance.
5. Target and pacing logic are declared rather than implied.
6. Driver language matches the strength of evidence.
7. Overall status leads to an action, escalation, or validation step.
8. Owners, due dates, open decisions, and prior commitments are visible.
9. Numbers, units, dates, signs, rounding, and source notes pass validation.

## Knowledge Reference

KPI reporting, operating review, WBR, MBR, QBR, executive scorecard, metric contract, semantic layer, source authority, evidence ledger, period-over-period variance, target variance, pacing model, seasonality, restatement, comparability, denominator effects, mix shift, driver decomposition, contribution bridge, residual variance, confidence language, traffic-light status, action register, decision log, data freshness, backfill, reporting cutoff