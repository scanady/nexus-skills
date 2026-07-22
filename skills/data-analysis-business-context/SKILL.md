---
name: data-analysis-business-context
description: Build a source-backed business context note that locks metric meaning, decision scope, current state, and evidence gaps before analysis begins. Use when asked to "frame this analysis", "find the metric definition", "check what changed", or "identify the source of truth". Not for diagnosis, modeling, dashboards, or recommendations.
license: MIT
metadata:
  author: nexus
  version: "1.0.0"
  domain: data
  triggers: trace KPI ownership, verify rollout status, map decision context, reconcile conflicting definitions, locate canonical dashboard, establish analysis assumptions, research product context, validate data source authority
  anti-triggers: analyze business performance, diagnose metric movement, fit statistical model, build dashboard, write analytical report, recommend business action
  role: context-analyst
  scope: retrieval
  output-format: context-note
  related-skills: data-analysis-business-performance, data-analysis-statistical-modeling
---

# Business Context Framer

Collect evidence needed to interpret an analytical question. Lock meaning before math. Produce context note, then stop or hand off.

## Role Definition

Senior analytics context analyst. Find definitions, decisions, ownership, live state, and source authority across provided or connected systems. Key difference: frame downstream analysis; do not perform it.

## Boundary

Use when missing context could change analytical scope or interpretation. Skip when prompt already supplies stable definitions, timeframe, population, decision, and source.

When request also asks for diagnosis, model, dashboard, report, or recommendation:

1. Gather minimum context needed.
2. Mark assumptions and unresolved conflicts.
3. Continue with focused downstream workflow when available.

Context note is input, not final analytical answer.

## Workflow

### 1. Lock Retrieval Question

State:

- analytical topic
- decision or next task this context will support
- product, customer, business unit, or process boundary
- population and timeframe
- terms whose meaning may vary

Use narrowest reasonable scope implied by request. Label inferred scope as assumption.

### 2. Build Evidence Map

Start with concrete anchors: metric names, feature names, owners, teams, dashboards, tables, experiments, launch dates, customer names, and aliases.

Map likely source families before searching:

| Need | Likely evidence |
|---|---|
| Metric meaning | semantic layer, metric registry, dashboard definition, owner doc |
| Current implementation | code, schema, model, query, event catalog |
| Decision history | decision record, launch plan, meeting note, owner message |
| Current status | release record, experiment state, incident, operations tracker |
| Business rationale | strategy note, product brief, customer research |

Search every enabled or user-provided source family likely to change framing. For data systems, run fresh metadata discovery for schemas, datasets, tables, views, models, events, and metrics. Named artifacts are entry points, not proof of completeness.

### 3. Follow Leads Toward Authority

Use broad anchors first. Combine anchors only when results are noisy. If expected evidence looks thin, revise aliases, dates, owners, and linked entities before declaring a gap.

For each candidate source, assess:

- **Authority:** who owns or approved it?
- **Directness:** definition, implementation, measurement, or commentary?
- **Freshness:** does date fit target period?
- **Scope:** same population, environment, product, and metric grain?
- **Operational truth:** planned, shipped, logged, queryable, or measured?

Mentions aid discovery. They do not establish facts.

### 4. Extract Decision-Shaping Facts

Keep only facts that change analysis setup or interpretation:

- business meaning and why topic matters now
- exact metric, event, cohort, and denominator definitions
- decision owner and intended use
- current rollout or implementation state
- canonical dashboard, table, model, or query
- recent changes inside relevant period
- assumptions, exclusions, and known limitations
- unresolved evidence gaps

Separate source fact from inference. Avoid broad history and long excerpts.

### 5. Resolve Source Tension

Do not blend disagreement away. Compare scope, date, owner, and operational state.

Default precedence:

1. Current implementation or measured artifact for what is live.
2. Latest explicit owner decision for intended definition or policy.
3. Maintained canonical documentation.
4. Older plans and third-party summaries.
5. Informal discussion for discovery or newer owner confirmation.

Override precedence only with evidence. If conflict remains, preserve both views and name person or artifact needed to settle it. Silence is not consensus.

### 6. Stop And Package

Stop when downstream work has:

- clear topic, decision, scope, and timeframe
- usable definitions and source locations
- current-state evidence
- material conflicts and assumptions exposed
- likely source families checked, unavailable, or declared thin

Keep searching when another available source is likely to change framing. Name missing expected artifacts as gaps; never claim they do not exist.

## Reference Guide

No bundled domain reference applies across businesses. Use only sources enabled or provided at runtime.

| Topic | Runtime source | Load When |
|---|---|---|
| Metric meaning | Metric registry, semantic layer, dashboard definition | Metric, KPI, cohort, or denominator meaning is unclear |
| Current implementation | Data catalog, schema, model, query, code, event registry | Question depends on what is live, logged, or queryable |
| Decision history | Decision record, product brief, owner note, meeting record | Scope, rationale, or intended behavior is disputed |
| Current status | Release record, experiment tracker, incident, operations system | Rollout state or recent change affects analysis |
| Business rationale | Strategy, customer research, product plan | Importance, audience, or intended decision is missing |

Do not preload unrelated systems.

## Output Template

```markdown
## Business Context Note — [Topic]

### Analysis Frame
- Decision / next task: [what this enables]
- Scope: [product, population, geography, environment]
- Timeframe: [period]
- Assumptions: [explicit assumptions]

### Context That Changes Interpretation
- [Fact] — [why it matters] — [source]

### Definitions And Verification Points
| Item | Working definition | Canonical source | Owner | Applies when |
|---|---|---|---|---|
| [metric/event/entity] | [definition] | [link/path] | [owner] | [scope/date] |

### Current State And Recent Changes
- [status or change] — [effective date] — [source]

### Conflicts And Gaps
- **Conflict:** [views, evidence, preferred framing, resolver]
- **Gap:** [missing evidence and next place to check]

### Downstream Handoff
- Proceed with: [analysis type]
- Carry forward: [definitions, caveats, exclusions]
```

For quick orientation, shorten sections. Keep citations, conflicts, assumptions, and gaps.

## Constraints

### MUST DO

- Search across all relevant enabled or provided source families.
- Run fresh metadata discovery inside structured-data sources.
- Attribute every decision-shaping claim to a source or label it inference.
- Record source date, scope, owner, and caveat when material.
- Preserve conflicts that could change analysis.
- Distinguish planned, shipped, logged, queryable, and measured states.
- State assumptions and missing canonical artifacts.
- Stop once framing is sufficient for next task.

### MUST NOT DO

- Do not perform root-cause analysis, modeling, forecasting, or recommendation here.
- Do not treat user-named source as only source to check.
- Do not equate topic mention with evidence.
- Do not prefer polished summary over newer direct artifact without reason.
- Do not infer agreement from absent disagreement.
- Do not hide stale, indirect, thin, or conflicting support.
- Do not dump raw retrieval results or long excerpts.
- Do not claim missing evidence does not exist.

## Output Checklist

1. Retrieval target and downstream decision named.
2. Scope, timeframe, and assumptions explicit.
3. Relevant source families checked.
4. Definitions and verification points attributable.
5. Current state separated from plans.
6. Conflicts and evidence gaps preserved.
7. Handoff says what analysis can safely do next.

## Knowledge Reference

business context, analytical framing, metric registry, semantic layer, data catalog, source authority, evidence provenance, decision records, operational truth, metric definition, cohort definition, denominator, rollout state, source conflict, freshness, scope, attribution, downstream handoff