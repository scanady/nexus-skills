# Source Families

What each kind of source can establish, what it cannot, and how to get context out of it. Use during the sweep (workflow step 3). Only families actually enabled or provided at runtime are in scope — do not describe a source you could not reach as if you read it.

## Sweep Order

Work from definition toward evidence, not from convenience toward whatever answers fastest:

1. **Semantic layer, metric registry, or data dictionary** — the team's own map of what things mean.
2. **The implementation** — transformation code, models, queries, event catalog. What is actually computed.
3. **The measurement surfaces** — warehouse tables, BI dashboards, product analytics. What is actually observable.
4. **The decision record** — briefs, design docs, launch plans, tickets, release notes. Why it is what it is.
5. **The informal layer** — chat, email, meeting notes. Fast discovery, weak proof, occasionally the newest decision.

Stop as soon as the framing is sound. The order is a priority list, not a checklist to exhaust.

## Per-Family Guide

### Semantic layer / metric registry / data dictionary

- **Establishes:** intended definition, canonical table or model, owner, documented caveats.
- **Cannot establish:** whether the implementation still matches. Registries drift.
- **Discovery move:** look up the metric by name and by alias, then open every artifact it points at.
- **Trap:** treating the layer as the boundary of the search. It is a map of where the team thinks truth lives.

### Warehouse / SQL catalog

- **Establishes:** what is queryable now, grain, column semantics, freshness, lineage.
- **Cannot establish:** business intent, or why a filter exists.
- **Discovery move:** fresh catalog discovery every time — list schemas, then tables and views matching the anchors, then inspect columns and partitions. Check the newest partition or `max(updated_at)` for real freshness.
- **Trap:** a remembered table name that has since been deprecated, renamed, or superseded by a `_v2`.

### Transformation code and repository

- **Establishes:** the definition as computed — filters, joins, exclusions, dedup logic, and when it last changed.
- **Cannot establish:** whether the computed definition is the one leadership uses.
- **Discovery move:** search the metric name and the column name; read the model or job that produces it; read the commit or PR that last touched it for the reason.
- **Trap:** treating the newest branch as production. Confirm what is deployed.

### BI dashboards and reports

- **Establishes:** the number people actually cite, its filters, and its refresh cadence.
- **Cannot establish:** correctness. Two dashboards for one metric usually differ by filter, grain, or timezone.
- **Discovery move:** open the underlying query, not the tile. Record owner, last edit, and default date range.
- **Trap:** an abandoned dashboard that still renders. Check last edit and last successful refresh.

### Product analytics and event catalog

- **Establishes:** what is instrumented, when tracking started or changed, event and property definitions.
- **Cannot establish:** anything before instrumentation shipped. Missing history is not a decline.
- **Discovery move:** find the event behind the metric, then its first-seen date and any rename or version.
- **Trap:** reading an instrumentation change as a business change. This is the single most common false finding.

### Experiment and feature-flag systems

- **Establishes:** live rollout percentage, targeting, exposure population, start and stop dates.
- **Cannot establish:** the decision that followed the experiment.
- **Discovery move:** get the flag or experiment state for the exact analysis window, not today's state.
- **Trap:** assuming a flag at 100% means shipped to everyone — check targeting rules and holdouts.

### Decision docs, product briefs, launch plans

- **Establishes:** intent, scope, success criteria, the owner, and the reasoning.
- **Cannot establish:** what shipped. Plans are written before reality.
- **Discovery move:** find the most recent version and its approval or decision line; check whether a later doc supersedes it.
- **Trap:** a well-written aspirational doc reading as a status report.

### Tickets, project trackers, release notes, changelogs

- **Establishes:** what shipped and when, scope cuts, follow-up work.
- **Cannot establish:** business impact or measured outcome.
- **Discovery move:** filter by the target window; read closed items, not the backlog.
- **Trap:** a "done" ticket that shipped behind a flag to nobody.

### Incident and status records

- **Establishes:** outages, data pipeline failures, backfills, and their exact windows.
- **Cannot establish:** whether the anomaly in the metric is fully explained by the incident.
- **Discovery move:** always check the analysis window for incidents before treating a movement as real.
- **Trap:** skipping this family. It explains an outsized share of surprising metric behavior.

### Chat and email

- **Establishes:** who owns what, what is contested, where the real artifact lives, and sometimes the newest decision.
- **Cannot establish:** a durable definition — unless the message is the owner's explicit, dated decision.
- **Discovery move:** search the anchor, then follow the links people posted rather than quoting the discussion.
- **Trap:** quoting a thread's conclusion when the thread ended in disagreement. Also: never paste long private message content into the brief.

### Calendar and meeting notes

- **Establishes:** when a decision was made and who was in the room.
- **Cannot establish:** what was decided, unless notes are explicit.
- **Discovery move:** use it to date a decision and identify the owner to ask.

### CRM, support, and customer records

- **Establishes:** account state, contract terms, reported problems, segment membership.
- **Cannot establish:** product usage. Reported and measured behavior differ.
- **Discovery move:** confirm which system defines the segment the analysis will slice by.
- **Trap:** carrying personal or payment identifiers into the brief. Names and account identifiers only, and only when needed.

### Spreadsheets and manual exports

- **Establishes:** what a team actually tracked, including adjustments the warehouse does not carry.
- **Cannot establish:** reproducibility. The query behind an export is usually gone.
- **Discovery move:** find who maintains it and what it reconciles against; ask for the query if the numbers matter.
- **Trap:** a spreadsheet that quietly became the source of truth without anyone deciding it should be.

## When A Family Is Unavailable

Say which one, what it would have established, and whether the strongest available substitute covers it.

- **Optional enrichment missing** — continue and label the gap where it affects the reading.
- **Decision-shaping source missing** — do not end on the absence. Give the next step: request access, ask the named owner, or proceed on a labeled assumption with its risk stated.

A source that was searched and returned nothing is different from a source that could not be searched. Report them differently.
