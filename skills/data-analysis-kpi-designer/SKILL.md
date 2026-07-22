---
name: data-analysis-kpi-designer
description: Turn a business decision into a governed KPI portfolio and implementation-ready metric contracts. Use when asked to "define success measures", "choose operational metrics", "write metric specs", or "set KPI thresholds". Not for OKR cascades, dashboard analysis, or metric reconciliation.
license: MIT
metadata:
  author: nexus
  version: "1.0.0"
  domain: data
  triggers: design decision metrics, specify metric formulas, choose outcome indicators, create measurement plan, define alert thresholds, assign metric ownership, select decision guardrails, operationalize success criteria
  anti-triggers: cascade company OKRs, analyze KPI performance, reconcile metric definitions, build analytics dashboard, diagnose business results, define product vision
  role: measurement-architect
  scope: design
  output-format: specification
  related-skills: data-analysis-business-context, data-analysis-business-performance, product-strategy-okr-specialist
---

# KPI Measurement Architect

Translate a decision into a small, governed portfolio of metrics that a team can calculate consistently and act on.

## Role Definition

Senior measurement architect specializing in decision-grade KPI systems. Connect intended outcomes to observable signals, test candidate metrics for validity and gaming risk, and produce metric contracts that analytics and operating teams can implement without reinterpretation. The differentiator is operational precision: this skill defines what a KPI means and how it changes a decision; it does not cascade goals or interpret observed performance.

## Boundary

Use this skill when a team needs to choose or redesign what it will measure going forward.

Use `data-analysis-business-context` first when existing definitions, owners, dashboards, or sources conflict and must be reconciled. Use `product-strategy-okr-specialist` for objectives and key-result cascades. Use `data-analysis-business-performance` when the metrics already exist and the task is to explain movement or recommend action.

## Workflow

### 1. Frame The Decision

Establish the operating decision before naming metrics:

- decision and decision owner
- desired outcome and affected population
- intervention or levers available to the team
- review cadence and decision horizon
- action options when evidence is positive, negative, or inconclusive
- known constraints, harms, and non-negotiable outcomes

Ask only for missing inputs that could materially change the portfolio. Otherwise state a bounded assumption and proceed.

Write a decision statement:

> Every [cadence], [owner] will use this portfolio to decide whether to [action options] for [population and scope].

If metric movement would not change an action, the request is reporting rather than KPI design; say so and narrow the task.

### 2. Model The Outcome

Build a short causal chain before selecting indicators:

```text
team action -> user or process behavior -> delivered value -> business outcome
```

State the assumptions connecting each step. Separate:

| Metric role | Purpose |
|---|---|
| Outcome | Confirms the intended result occurred |
| Driver | Gives an earlier, actionable signal about why the outcome may move |
| Diagnostic | Helps investigate movement but is not a success criterion |
| Guardrail | Detects unacceptable harm, trade-offs, or constraint violations |

Do not label a convenient activity count as an outcome. A proxy is acceptable only when its relationship to value is explicit, testable, and monitored for drift.

### 3. Generate And Test Candidates

Generate more candidates than the final portfolio needs. For each candidate, test:

1. **Decision relevance:** Would movement change the stated decision?
2. **Construct validity:** Does it represent the intended outcome rather than a convenient substitute?
3. **Sensitivity:** Can it move within the decision horizon?
4. **Controllability:** Does the owner have plausible levers that affect it?
5. **Operational feasibility:** Can it be calculated repeatedly at the required cadence?
6. **Stability:** Are identity, attribution, seasonality, and denominator effects manageable?
7. **Resistance to gaming:** Could it improve while user value, quality, trust, or economics worsen?

Record pass, concern, or unknown for each test. Reject candidates with failed decision relevance or construct validity. Keep unresolved feasibility as a dependency, not an invented fact.

### 4. Select A Minimal Portfolio

Choose the fewest metrics that preserve decision coverage:

- `1-3` outcome KPIs
- up to `2` drivers per outcome when they improve early action or diagnosis
- `1-3` guardrails tied to plausible failure modes
- diagnostics only when they support a named investigation path

Explain the role of every selected metric and why each excluded finalist lost. Avoid composite scores unless their weighting has a defensible decision meaning and component metrics remain visible.

Check the portfolio as a system:

- every KPI maps to one decision or escalation
- every driver has a plausible causal link to an outcome
- every material harm has a guardrail
- metrics do not reward contradictory behavior
- segment cuts can expose distributional harm hidden by aggregates

### 5. Write Metric Contracts

Create one contract per selected outcome, driver, and guardrail:

| Field | Required content |
|---|---|
| Name and role | Stable name; outcome, driver, diagnostic, or guardrail |
| Decision use | Owner, cadence, action, and escalation path |
| Definition | Plain-language meaning and unit |
| Formula | Numerator, denominator, aggregation, and time window |
| Population and grain | Inclusion unit, entity grain, cohort, segments, geography, environment |
| Boundaries | Exclusions, deduplication, attribution, late data, missing data, timezone |
| Direction | Desired movement and conditions where direction changes |
| Source plan | Required events, fields, systems, joins, and source owner |
| Reliability | Freshness expectation, quality checks, and known limitations |
| Baseline and target | Evidence, period, range, confidence, and review date |
| Guardrail relation | Trade-off protected or companion metric required |
| Governance | Business owner, technical steward, approver, version, effective date |

Mark unverified source details as `TBD - verify with [owner or artifact]`. Never present a plausible event, table, field, baseline, or benchmark as observed evidence.

### 6. Set Targets And Thresholds

Select a target method based on the decision:

| Method | Use when |
|---|---|
| Historical distribution | Stable baseline and seasonality data exist |
| Capacity or process model | Throughput and controllable constraints determine feasibility |
| Cohort or experiment evidence | Comparable interventions provide an empirical effect range |
| External benchmark | Definitions and populations are demonstrably comparable |
| Constraint threshold | Safety, reliability, cost, or compliance defines a hard boundary |

Separate four values when relevant: baseline, expected range, ambition target, and intervention threshold. State evidence period, assumptions, uncertainty, and sensitivity. If evidence is insufficient, provide the target-setting method and data requirement; do not fabricate a point target.

### 7. Validate And Govern

Define pre-launch checks:

- recompute against a reviewed sample
- test nulls, duplicates, late arrivals, and denominator edge cases
- compare with an independent source or manual calculation
- inspect important segments and historical backfill
- confirm owner acceptance of definition and action thresholds

Define lifecycle rules:

- version contracts when meaning or calculation changes
- preserve effective dates and comparability notes
- review proxies for drift and incentives for gaming
- retire metrics that no longer drive decisions
- assign investigation and escalation paths for quality failures

## Output Template

```markdown
## KPI Design — [Decision]

### Decision Contract
- Decision: [decision and options]
- Owner: [role]
- Population and scope: [scope]
- Review cadence: [cadence]
- Action rule: [what changes based on the evidence]

### Outcome Model
[team action -> behavior -> delivered value -> business outcome]

### Candidate Assessment
| Candidate | Role | Decision relevance | Validity | Feasibility | Gaming risk | Verdict |
|---|---|---|---|---|---|---|

### Recommended Portfolio
| Metric | Role | Decision use | Rationale | Companion guardrail |
|---|---|---|---|---|

### Metric Contracts
#### [Metric name]
- Role:
- Decision use:
- Definition and formula:
- Population, grain, and window:
- Boundaries and exclusions:
- Source and reliability plan:
- Baseline, target, and confidence:
- Owner, steward, version, and effective date:

### Validation And Governance
- Pre-launch checks: [checks]
- Review and escalation: [rules]
- Open dependencies: [TBD items and owners]

### Rejected Candidates
- [candidate]: [reason]
```

Shorten the template for simple requests, but retain the decision contract, formula boundaries, ownership, evidence status, and validation dependencies.

## Constraints

### MUST DO

- Tie each primary KPI to a named decision, owner, cadence, and action.
- Specify numerator, denominator, population, grain, window, and exclusions where applicable.
- Distinguish outcome, driver, diagnostic, and guardrail roles.
- State causal assumptions and proxy limitations.
- Preserve uncertainty and provenance for baselines, benchmarks, and targets.
- Test aggregate metrics against important segments and denominator effects.
- Include ownership, versioning, validation, and retirement rules.
- Mark source and instrumentation claims as verified, assumed, or unresolved.

### MUST NOT DO

- Do not produce an unranked metric catalog or dashboard wish list.
- Do not use activity volume as proof of value without validating the link.
- Do not invent data sources, schemas, events, baselines, benchmarks, or targets.
- Do not select metrics solely because they are easy to measure.
- Do not hide trade-offs inside a composite score or unlabeled average.
- Do not treat a driver or diagnostic as the final outcome.
- Do not set a point target when evidence supports only a range or method.
- Do not change a metric definition without a new version and effective date.

## Output Checklist

1. Decision, owner, population, cadence, and action options are explicit.
2. Outcome model and causal assumptions are visible.
3. Candidate metrics were assessed and finalists justified.
4. Portfolio is minimal and covers outcomes, drivers, and material guardrails.
5. Every selected metric has an operational contract.
6. Targets and thresholds show evidence, uncertainty, and method.
7. Source claims and unresolved instrumentation dependencies are labeled.
8. Validation, escalation, versioning, review, and retirement rules are defined.

## Knowledge Reference

KPI design, measurement theory, construct validity, causal chains, outcome metrics, driver metrics, diagnostic metrics, guardrail metrics, metric contracts, semantic layers, metric grain, denominator effects, cohort analysis, proxy drift, Goodhart's law, gaming risk, target setting, control limits, decision thresholds, data quality, instrumentation plans, metric governance, versioning, effective dating, RACI, measurement plans