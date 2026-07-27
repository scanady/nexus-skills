# Evidence Authority

How to judge what a source can prove, and what to do when two of them disagree. Use during ranking (workflow step 4) and reconciliation (step 6).

## The Five Tests

Run every candidate through these before it enters the brief.

### Authority — who owns or approved it

The owner of the metric, the system, or the decision outranks anyone summarizing them. An unowned artifact is weak evidence no matter how well written. If you cannot name who stands behind a claim, the claim is unowned; say so.

### Directness — how close it sits to the thing itself

Ranked, strongest first: the implementation that computes it, the measurement that records it, the artifact that defines it, a maintained summary of that artifact, commentary about any of the above. Each step away adds a chance for the meaning to have shifted.

### Freshness — does its date cover the target period

A source is fresh relative to the question, not to today. A definition written last year is fine for last year's data and wrong if the definition changed in March. Check for a change inside the analysis window, not just the artifact's edit date.

### Scope — is it about the same thing

Same population, same grain, same environment, same product surface, same geography. A definition that is correct for self-serve accounts and applied to enterprise accounts produces a confidently wrong analysis.

### Operational state — how real is it

See the ladder below. Confusing a state for the one above it is the most expensive framing error available.

## Operational State Ladder

| State | Means | Evidence that proves it |
|---|---|---|
| Planned | Someone intends it | Roadmap, brief, plan |
| Decided | An owner committed | Decision record, approval, dated owner message |
| Shipped | Code is deployed | Release note, merged and deployed change, flag state |
| Logged | Events are being emitted | Event catalog first-seen date, raw event volume |
| Queryable | Data is in a usable table | Catalog entry, row counts across the window |
| Measured | A number exists and has been checked | Dashboard, query result, reconciled report |

Two rules:

- Each rung requires its own evidence. Shipped does not imply logged; logged does not imply queryable at usable grain.
- When the question is "what is true right now," the highest rung with evidence governs. When the question is "what was intended," the decision rung governs.

## Precedence Ladder

Default order when sources conflict. Each level can be overridden, but only by evidence, never by preference.

1. **The implementation or the measurement** — for what is live, computed, or observable now.
2. **The most recent explicit owner decision** — for intended definition, policy, or scope.
3. **Maintained canonical documentation** — for stable definitions no one has recently disputed.
4. **Older plans, third-party summaries, secondhand write-ups** — background, not proof.
5. **Informal discussion** — discovery, and occasionally the newest decision when an owner states it explicitly with a date.

Level 5 overrides levels 2 and 3 only when the message clearly records a decision — a named owner, a definite statement, and a date after the artifact it contradicts. A preference expressed in chat is not a decision.

## Conflict Patterns

| Pattern | What is usually going on | Resolution |
|---|---|---|
| Two dashboards disagree | Different filters, grain, timezone, or refresh time | Diff the underlying queries; report the difference as a definition fact, not a data error |
| Doc and code disagree | The doc was not updated when the logic changed | Code governs measurement, doc governs intent; flag the drift to the owner |
| Warehouse and source system disagree | Sync lag, late-arriving rows, or a filter in the pipeline | Compare freshness and row counts at the boundary before blaming either side |
| Numbers changed retroactively | Backfill, restatement, or a definition change applied to history | Get the change date and whether history was restated; both readings may be valid for different windows |
| Plan and reality disagree | Scope was cut during implementation | Shipped evidence governs; note what was dropped, it often explains the metric |
| Two owners claim the metric | Ownership moved and was never announced | Name both, prefer the one whose team maintains the implementation, ask to confirm |

## False-Authority Traps

- **Polish reading as authority.** A well-formatted deck is not stronger than a scrappy owner message from last week.
- **Repetition reading as corroboration.** Five sources quoting one original are one source.
- **Silence reading as agreement.** No objection in a thread proves nothing.
- **Recency reading as correctness.** A newer document can restate an older error.
- **A mention reading as a definition.** The metric appearing in a doc does not mean the doc defines it.
- **Confidence reading as evidence.** How firmly a source states something is not information about whether it is true.
- **Precision reading as accuracy.** A number carried to four decimals is not thereby correct.

## Labeling What You Found

Every decision-shaping line in the brief carries one of:

- **Established** — a direct source states it, and the source passes the five tests. Cite it.
- **Inferred** — you concluded it from evidence that does not state it. Say what it rests on.
- **Contested** — sources disagree. Give both readings, the preferred one, and the resolver.
- **Unknown** — nobody's artifact answers it. Say what would.

A single-source fact is usable. A single-source fact that would change the analysis's conclusion needs a second source or an explicit flag that it rests on one.
