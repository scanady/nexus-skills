# Handoff Contracts

What the brief must contain before the next piece of work can start, by consumer. Use when packaging (workflow step 7).

## Minimum Handoff

No matter who receives it, the brief carries:

- the decision or task the analysis feeds
- scope, population, and timeframe, with inferred parts labeled
- the definition of every term the analysis will compute or slice on
- the source that governs each definition, with its owner and date
- current state separated from plans
- conflicts, with a preferred reading and a named resolver
- gaps, with what each would change
- an explicit statement of what the evidence cannot support

If the receiving work would produce a different answer depending on something you left unresolved, that item is not a footnote — put it in the frame.

## By Consumer

### Metric diagnosis and business performance analysis

Needs, beyond the minimum:

- the metric's exact numerator, denominator, filters, exclusions, and grain
- the baseline or comparison window the business actually uses
- every change inside the analysis window that could move the metric without the business moving: instrumentation changes, migrations, backfills, pricing or policy changes, launches, incidents
- which driver dimensions the business monitors and can act on, and where each lives
- whether the segment or hierarchy the question implies can be reconstructed from the available data

Flag hard: any measurement artifact that could be mistaken for a business change. That mistake is the most common way a diagnosis goes wrong, and the brief is the only place to catch it.

### KPI design

Needs, beyond the minimum:

- whether a canonical definition exists at all, or the work is genuinely greenfield
- existing definitions in circulation and who uses each
- what is instrumented today versus what a proposed metric would require
- the decision the metric is meant to inform, and the owner who will act on it

Flag hard: a definition that exists but is not followed. Designing around it creates a third definition.

### KPI reporting and executive readouts

Needs, beyond the minimum:

- which number leadership already cites, and the surface it comes from
- targets or budgets in force for the period, and where they were set
- restatements or definition changes that break comparability with prior periods
- the caveat that must travel with the number when it is repeated out of context

Flag hard: comparability breaks. A readout that silently compares two definitions is worse than no readout.

### Dataset profiling

Needs, beyond the minimum:

- the tables, models, or files the question actually depends on
- the intended grain, so the profiler can test it rather than guess it
- known quality history — backfills, partial periods, deprecated columns, dual-written tables
- the columns that carry business meaning versus the ones that are pipeline artifacts

### Analysis validation

Needs, beyond the minimum:

- the definition the analysis should have used, with its source
- the source that governs each number under review
- the conflicts that were open at framing time and how they were resolved
- every assumption the analysis is standing on

Flag hard: assumptions the analyst may not know they inherited.

### Charts and reports

Needs, beyond the minimum:

- the label each metric should carry, matching the canonical definition
- the period boundaries and timezone convention
- caveats that must appear on the artifact, not only in conversation
- whether any named entity must be excluded or aggregated for sensitivity reasons

## Escalate Instead Of Handing Off

Do not hand off — return to the user — when:

- the governing definition is contested and the conflict changes the answer, with no resolver reachable
- the required source of truth is unavailable and no substitute supports the claim the analysis would make
- the population or timeframe cannot be pinned down closely enough to build a comparison
- the question assumes something the evidence contradicts

Escalation is a finding, not a failure. State what is blocked, what would unblock it, and what a narrower analysis could still answer in the meantime — then let the user choose.

## Closing The Loop

If the downstream work contradicts the brief — the table does not exist, the definition does not reproduce the cited number, the rollout state was wrong — the brief was wrong. Correct it and say which fact changed, rather than quietly working around it. A stale brief travels further than the analysis that came from it.
