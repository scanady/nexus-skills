# Dialectic Synthesis

Hegelian dialectic with steel manning. Goal: produce a stronger position than either thesis or antithesis alone. Argue the other side well enough that the user must refine their position or acknowledge a genuine trade-off.

## Process

1. **Restate** — Steelman the user's position first
2. **Construct** — Build the strongest opposing argument
3. **Clash** — Show where thesis and antithesis genuinely conflict
4. **Synthesize** — Propose a position that incorporates the best of both

## Steel Manning

Restate the user's position in its strongest possible form before arguing against it.

| Step | Action | Example |
|------|--------|---------|
| 1. Identify core claim | Strip weak framing | "We should use microservices" → "Independent deployment will accelerate team velocity" |
| 2. Add strongest evidence | Supply what user implied | "...especially given 4 teams on different release cycles" |
| 3. Acknowledge real benefits | Name what's genuinely good | "This eliminates the current deploy queue bottleneck" |
| 4. Confirm with user | "Is this a fair restatement?" | Ensures you're attacking the real position |

### Steelman Checklist

- [ ] Made the position stronger, not weaker?
- [ ] User would recognize this as their view (or better)?
- [ ] Included the strongest evidence for their side?
- [ ] Attacking this version, not an easier one?

## Antithesis Construction

Ask: "If a smart, informed person disagreed, what would their best argument be?"

| Source | Example |
|--------|---------|
| Opposing trade-off | "Speed now vs. maintainability later" |
| Hidden cost | "Migration cost exceeds savings for 18 months" |
| Alternative solving the same problem | "A modular monolith gets 80% of the benefit at 20% of the cost" |
| Precedent from similar situations | "Company X tried this and reverted after 2 years" |
| Stakeholder the thesis doesn't serve | "Junior developers will struggle with added complexity" |

### Reductio ad Absurdum (Supporting Technique)

Take thesis to logical extreme to reveal hidden limits. Use sparingly.

| Thesis | Reductio | Reveals |
|--------|----------|---------|
| "Optimize for developer experience" | "Then never ship to production, since bugs hurt DX" | DX must be balanced against delivery |
| "More tests always better" | "100% coverage including getters/setters" | Test value has diminishing returns |
| "Move fast" | "Skip code review and testing" | Speed has a quality floor |

## Synthesis Patterns

| Pattern | When to Use | Example |
|---------|-------------|---------|
| **Conditional** | X true when A; Y true when B | "Microservices for payment (compliance boundary); monolith for admin (low traffic, fast iteration)" |
| **Scope Partition** | Apply X to domain A, Y to domain B | "Event sourcing for audit trail; CRUD for user profiles" |
| **Temporal** | Start X, migrate to Y when Z | "Start with monolith; extract services when team exceeds 3 squads" |
| **Risk Mitigation** | Proceed with X but add safeguards from Y | "Adopt new framework but keep abstraction layer for swap-back" |
| **Hybrid Extraction** | Take strongest element from each | "Microservices deployment model + shared database with schema ownership" |

## Confidence Assessment

| Level | Meaning | Action |
|-------|---------|--------|
| **HIGH** | Synthesis clearly stronger than either side | Proceed with synthesis |
| **MEDIUM** | Plausible but untested | Identify riskiest assumption, suggest experiment |
| **LOW** | Irreconcilable claims | Name the genuine trade-off; let user decide based on priorities |
| **PIVOT** | Antithesis stronger than thesis | Recommend user reconsider original position |

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| False synthesis | "Just do both!" without resolving tension | Name the specific trade-off being resolved |
| Weak antithesis | Counter-argument is a strawman | Steelman the counter too |
| Thesis bias | Synthesis suspiciously close to original | Check if antithesis was genuinely engaged |
| Complexity creep | Synthesis more complex than either original | Simpler synthesis is usually better |
| Fence-sitting | "It depends" without specifying on what | Name the exact conditions for each path |

## Output Template

```markdown
## Thesis (Steelmanned)

[User's position in strongest form]

**Strongest evidence for:** [1-2 supporting points]

## Antithesis

[Strongest counter-argument]

**Strongest evidence for:** [1-2 supporting points]

## Points of Genuine Conflict

| Dimension | Thesis Says | Antithesis Says |
|-----------|------------|-----------------|
| [e.g., Speed] | [Position] | [Counter-position] |
| [e.g., Cost] | [Position] | [Counter-position] |

## Proposed Synthesis

**Pattern:** [Conditional / Scope Partition / Temporal / Risk Mitigation / Hybrid]

[Concrete synthesis proposal]

**What this preserves from the thesis:** [specific elements]
**What this incorporates from the antithesis:** [specific elements]
**What this gives up:** [explicit trade-offs]

**Confidence:** HIGH / MEDIUM / LOW / PIVOT
**If MEDIUM:** Test [riskiest assumption] by [experiment]
```
