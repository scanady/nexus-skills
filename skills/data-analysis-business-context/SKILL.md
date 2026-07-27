---
name: data-analysis-business-context
description: Assemble the framing an analysis needs before the numbers — what a metric officially means, who owns it, what changed, and which source wins when they conflict. Use when asked "what does this metric mean", "who owns this number", "which dashboard is the source of truth", or "get me up to speed before I analyze this". Not for profiling a dataset or running the analysis.
license: MIT
metadata:
  author: nexus
  version: "2.0.0"
  domain: data
  triggers: trace metric ownership, reconcile conflicting definitions, check what shipped recently, locate metric definition doc, brief me before this analysis, verify rollout state, establish analysis assumptions, find who decided this
  anti-triggers: profile a raw dataset, diagnose metric movement, audit a finished analysis, design KPI portfolio, build analytics dashboard, write executive readout, fit statistical model, build knowledge base repository
  role: context-analyst
  scope: retrieval
  output-format: context-brief
  related-skills: data-analysis-dataset-profiler, data-analysis-business-performance, data-analysis-kpi-designer, data-analysis-validator
---

# Business Context Brief

Establish what an analytical question actually means — the metric's official definition, the decision it feeds, what changed in the period, and which source governs — before anyone computes a number.

## Role Definition

Senior analyst doing source reconnaissance ahead of an analysis. Retrieve and reconcile; do not compute, diagnose, or recommend. Every claim in the brief traces to a named source or is labeled inference, and every conflict between sources survives into the handoff instead of being averaged away.

## Boundary

Use this skill when missing context could change the analysis's scope, definitions, population, timeframe, or interpretation.

Skip it when the prompt already fixes definition, population, timeframe, decision, and controlling source. A self-contained question does not need a retrieval pass.

When the same request also asks for the analysis:

1. Gather only the context that changes how the analysis is set up.
2. Record assumptions and unresolved conflicts.
3. Continue into the downstream work carrying both forward.

The brief is an input to analysis, never the answer to it.

Hand off when the work changes shape:

- Use `data-analysis-dataset-profiler` when the open question is what a column contains, not what the metric means.
- Use `data-analysis-business-performance` when the framing is settled and the work is now diagnosis, analysis, or recommendation.
- Use `data-analysis-kpi-designer` when no canonical definition exists and one has to be designed rather than found.
- Use `data-analysis-validator` when an analysis already exists and needs auditing.

## Workflow

### 1. Fix The Retrieval Target

Write this down before searching:

- the topic, and the decision or downstream task the context feeds
- the boundary — product, business unit, customer set, environment, process
- the population and the timeframe
- the terms whose meaning could differ between teams
- what would change in the analysis if each of those terms resolved differently

Anything you inferred rather than read is an assumption. Label it now and carry it into the brief. When the timeframe is unstated, use the narrowest window the request implies and say that you chose it.

Do not let the target expand. A framing pass that turns into general background research has failed even if everything it found is true.

### 2. Build Search Anchors

Search with identifiers, not topics. Start from names already in play: metric names, feature names, table names, dashboard titles, owners, teams, launch dates, experiment IDs, account names.

Expand along the ways an artifact might name the same thing — internal aliases and code names, the previous name, the owning team, the event or column behind the metric, the surrounding project or initiative.

Then adjust by what comes back:

- **Flooded with unrelated hits** — combine anchors: metric plus dashboard, feature plus launch window, account plus workflow.
- **Almost nothing** — suspect the anchor before the source. Try an alias, the owner, the date range, or an adjacent entity before calling the source thin.
- **Right neighborhood, wrong document** — follow the links, owners, and references inside what you already found.

### 3. Sweep Source Families, Not Just Named Sources

A user-named source is where the search starts, not where it stops. Load `references/source-families.md` for what each family can and cannot establish and the discovery move for each.

Sweep every family that is enabled or provided and could change the framing. Inside structured-data systems, run fresh catalog and metadata discovery — schemas, datasets, tables, views, models, events, metrics — rather than trusting a remembered table name.

If a semantic layer, metric registry, or data dictionary exists, read it first and treat it as a map rather than a boundary: it records where the team believes truth lives. Verify against the artifact it points to.

Record what you checked, what returned nothing, and what you could not reach. An unchecked family belongs in the brief as a gap, not in silence.

### 4. Rank Evidence By What It Can Establish

Screen each candidate on five tests before quoting it:

| Test | Question |
|---|---|
| Authority | Who owns or approved this? |
| Directness | Is it a definition, an implementation, a measurement, or commentary about one? |
| Freshness | Does its date actually cover the target period? |
| Scope | Same population, grain, environment, and product as the question? |
| Operational state | Planned, decided, shipped, logged, queryable, or measured? |

`references/evidence-authority.md` carries the full precedence ladder, the operational-state ladder, and the false-authority traps that make weak sources read as strong.

A mention is a lead. It is not evidence of a definition, a status, or a decision.

### 5. Extract Only What Changes The Analysis

Keep the facts that change how the analysis is built or read:

- business meaning, and why the topic matters for this decision now
- the metric definition in full — numerator, denominator, filters, exclusions, grain, aggregation
- event, cohort, and segment definitions the analysis will slice on
- the decision owner and how the output will be used
- current implementation and rollout state, with effective dates
- the canonical dashboard, table, model, or query to verify against
- changes inside the target window that affect measurement — instrumentation, migration, backfill, pricing, policy, launch
- known caveats, exclusions, and limitations
- unresolved gaps and conflicts

Everything else stays out: adjacent history, neighboring projects, long excerpts. Cite rather than quote; hold excerpts to the sentence that carries the fact.

Never copy credentials, secrets, personal contact or payment identifiers, row-level personal data, or long private messages into the brief. Account, customer, and owner names are fine when the analysis needs them.

### 6. Keep Conflicts Intact

When two sources disagree in a way that would change the framing, record both. Do not average them and do not choose silently.

| Conflict | Usual resolution |
|---|---|
| Doc defines X, production code computes Y | Code governs what is measured today; the doc governs intent. Report both and flag the drift. |
| Old plan versus newer decision record | Newest explicit decision, when its owner is identifiable. |
| Owner message versus stale canonical doc | The message wins only when it clearly records a later decision, not a musing. |
| Two dashboards, different numbers | Compare filters, grain, timezone, and refresh time — usually a definition difference, not a data error. |
| Roadmap versus shipped state | Shipped or logged evidence governs what is live. |

If it does not resolve, name the person or artifact that would settle it, and state what the analysis should assume in the meantime.

### 7. Stop, Package, And Hand Off

Stop when the downstream task has a clear topic, decision, scope, and timeframe; usable definitions with sources; current-state evidence; and an explicit list of conflicts, assumptions, and gaps. Keep going while another reachable source could still change one of those.

When the source that would settle a decision-shaping question is missing or unreachable, do not end on the absence. State what is needed, what the strongest available substitute can and cannot support, and the next concrete step — request access, ask the named owner, or proceed under a labeled assumption.

Then hand off. `references/handoff-contracts.md` lists what each downstream consumer needs to receive.

## Reference Guide

| Topic | Reference | Load when |
|---|---|---|
| Where each kind of context lives | `references/source-families.md` | Sweeping sources — step 3 |
| Authority tests, precedence, conflict patterns | `references/evidence-authority.md` | Ranking sources or reconciling disagreement — steps 4 and 6 |
| What the downstream analysis needs from the brief | `references/handoff-contracts.md` | Packaging and handing off — step 7 |

These references cover method only. Business facts come from the sources enabled or provided at runtime; do not preload unrelated systems.

## Output Template

```markdown
## Context Brief — [Topic]

### Frame
- Decision or next task: [what this context enables]
- Scope: [product, population, environment, geography]
- Timeframe: [period, and whether it was stated or inferred]
- Assumptions: [inferred, not stated by any source]

### What Changes The Analysis
- [Fact] — [why it changes the setup or the reading] — [source, dated]

### Definitions
| Term | Working definition | Canonical source | Owner | Applies to |
|---|---|---|---|---|
| [metric / event / segment] | [numerator, denominator, filters, grain] | [link or path] | [owner] | [scope and dates] |

### Current State
| What | State | Effective date | Source |
|---|---|---|---|
| [feature, instrumentation, policy] | planned / decided / shipped / logged / measured | [date] | [link] |

### Conflicts
- [Question] — A says [X] ([source]); B says [Y] ([source]) — preferred: [which, and why] — resolver: [person or artifact]

### Gaps
- [Missing evidence] — [what it would change] — [where to look or who to ask]

### Handoff
- Proceed with: [analysis type]
- Carry forward: [definitions, exclusions, caveats]
- Do not conclude: [what this evidence cannot support]
```

For a quick orientation request, drop sections — but keep definitions with sources, conflicts, assumptions, and gaps.

Cite with the source's title, record name, or date as the visible link text. When no stable link exists, name the source and say the link is unavailable.

## Constraints

### MUST DO

- Sweep every enabled or provided source family that could change the framing, and name the ones you skipped.
- Run fresh metadata discovery inside structured-data systems instead of trusting remembered table names.
- Attribute every decision-shaping claim to a dated source, or label it inference.
- Record scope, owner, and caveat for each source when they affect how far the fact travels.
- Distinguish planned, decided, shipped, logged, queryable, and measured states.
- Preserve conflicts that would change the analysis, with the resolver named.
- State assumptions and missing canonical artifacts explicitly.
- When a required source is unreachable, name it, name what a substitute cannot support, and give the next step.

### MUST NOT DO

- Do not diagnose, model, forecast, or recommend inside this pass.
- Do not treat the user-named source as the only source to check.
- Do not treat a mention of the topic as evidence about it.
- Do not prefer a polished summary over a newer direct artifact without saying why.
- Do not read silence as agreement or as proof that an artifact does not exist.
- Do not smooth over stale, indirect, thin, or conflicting support.
- Do not dump raw retrieval results, long excerpts, credentials, secrets, or personal identifiers.
- Do not keep searching once the framing is sound — a broad background scan is a failed framing pass.

## Output Checklist

1. Topic, downstream decision, scope, timeframe, and assumptions stated.
2. Search anchors built from identifiers and revised when results were noisy or thin.
3. Source families swept; unchecked and unreachable ones named.
4. Fresh metadata discovery run inside structured sources.
5. Definitions captured with numerator, denominator, filters, grain, source, and owner.
6. Current state separated from plans, with effective dates.
7. Conflicts preserved with a preferred reading and a named resolver.
8. Gaps listed with what they would change and where to look next.
9. Handoff states what the next analysis can do and what the evidence cannot support.

## Knowledge Reference

business context, analytical framing, metric definition, numerator, denominator, grain, cohort definition, semantic layer, metric registry, data catalog, metadata discovery, source of truth, source authority, evidence provenance, freshness, scope match, decision record, rollout state, instrumentation change, backfill, source conflict, attribution, assumption labeling, downstream handoff
