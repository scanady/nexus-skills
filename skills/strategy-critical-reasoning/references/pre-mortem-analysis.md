# Pre-Mortem Analysis

Inverts the question. Instead of "Will this work?" ask: **"It's [timeframe] from now and this has failed. Why?"**

Bypasses optimism bias by making failure the starting point.

## Process

1. **Scene-set** — "Imagine it's [timeframe] from now. This has failed. Not a small setback — a clear failure."
2. **Generate** — Write specific failure narratives
3. **Rank** — By likelihood × impact
4. **Chain** — Trace first → second → third order consequences
5. **Signal** — Identify early warning signs
6. **Mitigate** — Concrete actions, not vague "be careful"

## Failure Narrative Construction

Narratives must be specific. "It didn't scale" is not a narrative.

**Good:** "At 50K concurrent users, the database connection pool exhausted, causing cascading timeouts, triggering the circuit breaker to reject all requests for 4 minutes during peak hours."

### Specificity Checklist

- [ ] Names a specific trigger (not "something goes wrong")
- [ ] Includes a number or threshold
- [ ] Describes chain of events, not just end state
- [ ] Identifies who or what is affected
- [ ] Could actually happen

### Failure Narrative Template

```markdown
**Failure: [Title]**

It's [timeframe] from now. [Specific trigger]. This caused [first-order effect],
which led to [second-order effect]. The team discovered the problem when [detection point],
but by then [consequence]. Root cause: [underlying assumption that proved wrong].
```

### Example

```markdown
**Failure: Migration Data Loss**

It's 3 months from now. During migration from PostgreSQL, a batch job silently drops records
where `legacy_id` contains special characters (~2% of records). The team discovers this
2 weeks post-migration when a customer reports missing order history. By then, the legacy
database has been decommissioned and backups have rotated past the migration date.
Root cause: migration tested against sanitized staging data that excluded special characters.
```

## Second-Order Consequence Chains

Trace at least two orders deep.

```
Trigger: [event]
  → 1st order: [immediate effect]
    → 2nd order: [consequence of 1st order]
      → 3rd order: [consequence of 2nd order]
```

### Example

```
Trigger: Key engineer leaves during migration
  → 1st order: Timeline slips 4 weeks
    → 2nd order: Overlap with legacy system doubles operational cost
      → 3rd order: Budget overrun triggers executive review; project descoped
```

### Common Chains

| First Order | Second Order | Third Order |
|------------|-------------|-------------|
| Feature ships late | Sales misses quarter | Engineering loses trust, gets more oversight |
| Performance degrades | Users adopt workarounds | Workarounds become "requirements" that constrain future design |
| Team member burns out | Knowledge concentrates | Bus factor drops, risk increases |
| Dependency breaks | Hotfix bypasses testing | New bugs introduced, confidence in releases drops |
| Data quality issue | Downstream reports wrong | Business decisions made on bad data |

## Inversion Technique

Ask: **"What would guarantee this fails?"** Then check if any of those conditions exist.

| Category | Guaranteed Failure Conditions |
|----------|-------------------------------|
| **People** | Single point of knowledge, no stakeholder buy-in, team doesn't believe in approach |
| **Process** | No rollback plan, no incremental validation, all-or-nothing deployment |
| **Technology** | Untested at target scale, undocumented dependencies, version lock-in |
| **Timeline** | No buffer, dependencies on external teams with no SLA, parallel critical paths |
| **Data** | Migration without validation, no quality checks, schema changes without backward compatibility |

## Domain-Specific Failure Patterns

### Technical

| Pattern | Trigger | Consequence |
|---------|---------|-------------|
| Integration cliff | New service connects to 3+ existing systems | One integration blocks all others |
| Scale surprise | Load 10x beyond testing | Cascading failures across dependent services |
| Migration trap | "Just move the data" | Data loss, extended downtime, rollback impossible |
| Dependency rot | Pinned to abandoned library | Security vulnerability with no upgrade path |
| Config drift | Manual environment setup | "Works locally" fails everywhere else |

### Business

| Pattern | Trigger | Consequence |
|---------|---------|-------------|
| Adoption cliff | Build it and they don't come | Sunk cost with no revenue impact |
| Competitor preempt | Competitor ships similar feature first | Market positioning lost |
| Timing mismatch | Market shifts during development | Product solves yesterday's problem |
| Stakeholder reversal | Executive sponsor changes | Project loses priority, resources reallocated |
| Hidden cost | Operational burden underestimated | Feature costs more to run than it generates |

### Process

| Pattern | Trigger | Consequence |
|---------|---------|-------------|
| Timeline fantasy | Best-case estimates | Crunch, quality cuts at worst time |
| Dependency chain | Team A waits on Team B waits on Team C | Any slip cascades through all teams |
| Knowledge silo | Expert leaves or unavailable | Progress stops |
| Scope creep | "While we're at it..." | Original goal buried |
| Feedback void | No user testing until launch | Wrong product built correctly |

## Early Warning Signs

| Warning Sign | What It Indicates |
|-------------|-------------------|
| "We'll figure that out later" (3+ times) | Critical decisions deferred, not resolved |
| No one can explain the rollback plan | Rollback hasn't been designed |
| Estimates keep growing | Hidden complexity discovered incrementally |
| Key meetings keep getting rescheduled | Stakeholder alignment weaker than assumed |
| "It works locally" | Environment parity worse than assumed |
| Testing phase compressed | Quality will be sacrificed |
| No success metrics defined | No one will know if this worked |

## Output Template

```markdown
## Pre-Mortem: [Plan/Decision Name]

**Timeframe:** [When would failure be evident]

### Failure Narratives

#### 1. [Failure Title] — Likelihood: High/Medium/Low | Impact: High/Medium/Low

[Specific failure narrative]

**Consequence chain:**
- 1st order: [immediate]
- 2nd order: [downstream]
- 3rd order: [systemic]

#### 2. [Failure Title] — Likelihood: High/Medium/Low | Impact: High/Medium/Low

[Narrative]

### Early Warning Signs

| Signal | Failure It Predicts | Check Frequency |
|--------|-------------------|-----------------|
| [Observable signal] | Failure #X | Weekly / Sprint / Monthly |

### Mitigations

| Failure | Mitigation | Effort | Reduces Risk By |
|---------|-----------|--------|-----------------|
| #1 | [Specific action] | Low/Med/High | [Estimate] |
| #2 | [Specific action] | Low/Med/High | [Estimate] |

### Inversion Check

| Guaranteed Failure Condition | Present? | Action If Yes |
|------------------------------|----------|---------------|
| [Condition] | Yes / No / Partial | [Mitigation] |
```
