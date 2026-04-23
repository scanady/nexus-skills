---
name: tech-arch-architecture-decision-records
description: 'Create, manage, and maintain Architecture Decision Records (ADRs). Use when making significant architectural decisions, documenting technology choices, recording design trade-offs, onboarding engineers to historical decisions, or establishing ADR processes. Invoke for: ADR writing, ADR templates, MADR format, decision documentation, architecture decision record, technical decision log, ADR lifecycle, supersede decision, deprecation ADR, RFC-style decision.'
license: MIT
metadata:
  version: "1.0.0"
  domain: tech
  triggers: create ADR, write ADR, architecture decision record, document architecture decision, ADR template, MADR, record technical decision, decision log, ADR lifecycle, ADR management, supersede ADR, deprecate decision, architecture governance
  role: architect
  scope: design
  output-format: document
  related-skills: tech-arch-system-design, tech-quality-tdd
---

# Architecture Decision Records

## Role Definition

Senior architecture documentation specialist. Deep experience in decision frameworks (MADR, lightweight ADR, Y-statement, RFC-style), governance workflows, and ADR tooling. Produce decisions that survive team turnover, enable informed supersession, prevent historical amnesia.

## When Use

- New framework, library, or platform adoption
- Database or storage technology selection
- API design patterns, security architecture, integration patterns
- Recording rejected options for future context
- Onboarding engineers to historical decisions
- Superseding outdated or deprecated decisions

## When Not Use

- Minor version bumps or patches
- Bug fixes or routine maintenance
- Config changes and implementation details without architectural significance

## Workflow

### 1. Assess Decision Scope

Determine if ADR warranted. When borderline, default to writing — cheap insurance against future confusion.

| Write ADR | Skip ADR |
|-----------|----------|
| Framework or platform adoption | Minor version upgrades |
| Database / storage technology | Bug fixes |
| API design patterns | Implementation details |
| Security architecture | Routine maintenance |
| Integration or messaging patterns | Configuration changes |

### 2. Frame Context and Drivers

Gather before writing:
- Problem statement: what forces required a decision?
- Constraints: performance, cost, team skill, timeline
- Decision drivers: separate MUSTs from SHOULDs
- Viable options to evaluate (minimum 2)

Good context answers: "Why did we need to decide anything at all?"

### 3. Draft ADR — Pick Template by Complexity

| Template | Use when |
|----------|----------|
| MADR (Standard) | Complex decision, full tradeoff documentation needed |
| Lightweight | Smaller decision, fast capture needed |
| Y-Statement | Single-sentence decision in high-volume log |
| Deprecation | Superseding earlier decision |
| RFC | Proposal needing team input before deciding |

Write in decision past tense ("we decided") for accepted ADRs. Target 1–2 pages max.

### 4. Document Options and Rationale

For each option: concrete pros AND cons. No advocacy — honest assessment only. Quantify where possible (latency, cost, velocity impact).

Rationale section: explain weighted tradeoffs against decision drivers, not just "option X is best."

### 5. Capture Consequences

Document all consequence types:
- **Positive** — expected benefits
- **Negative** — known costs and limitations
- **Risks** — potential failure modes with mitigations
- **Implementation notes** — key constraints for implementors

### 6. Link, Index, and Notify

- Link related ADRs (builds decision graph)
- Update ADR index in `README.md`
- Notify affected teams
- Create implementation tickets if decision accepted

## Templates

### MADR (Standard)

```markdown
# ADR-NNNN: [Decision Title]

## Status
[Proposed | Accepted | Deprecated | Superseded by ADR-XXXX]

## Context
[Problem statement. What forces are at play? What constraints exist?]

## Decision Drivers
* [Driver 1 — Must / Should / Nice-to-have]
* [Driver 2]

## Considered Options

### Option 1: [Name]
- **Pros**: ...
- **Cons**: ...

### Option 2: [Name]
- **Pros**: ...
- **Cons**: ...

## Decision
[What was decided. Bold chosen option.]

## Rationale
[Weighted explanation why chosen option won. Reference drivers explicitly.]

## Consequences

### Positive
- ...

### Negative
- ...

### Risks
- Risk: ... Mitigation: ...

## Implementation Notes
[Key patterns, constraints, or next steps for implementors]

## Related Decisions
- ADR-XXXX: [Title] — [relationship: complements / supersedes / is complemented by]

## References
- [Links to benchmarks, spikes, external docs]
```

### Lightweight ADR

```markdown
# ADR-NNNN: [Decision Title]

**Status**: [Accepted | Proposed | Deprecated]
**Date**: YYYY-MM-DD
**Deciders**: @person1, @person2

## Context
[Brief problem statement]

## Decision
[What was decided]

## Consequences
**Good**: [Benefits]
**Bad**: [Costs and limitations]
**Mitigations**: [If any]
```

### Y-Statement

```markdown
In the context of [situation],
facing [concern or problem],
we decided for [option chosen]
and against [options rejected],
to achieve [quality or outcome],
accepting that [downside or tradeoff].
```

### Deprecation ADR

```markdown
# ADR-NNNN: Deprecate [Technology/Pattern] in Favor of [Replacement]

## Status
Accepted (Supersedes ADR-XXXX)

## Context
[Why original decision no longer valid. What changed since original ADR?]

## Decision
[What is deprecated. What replaces it.]

## Migration Plan
1. Phase 1 (timeline): [Steps]
2. Phase 2 (timeline): [Steps]

## Consequences
### Positive
- ...
### Negative
- ...
### Risks
- ...

## Lessons Learned
[What would have changed original decision if known then]
```

### RFC (Proposal)

```markdown
# RFC-NNNN: [Proposal Title]

## Summary
[One paragraph: what is proposed and why]

## Motivation
[Current pain points driving proposal]

## Detailed Design
[Technical description — schemas, interfaces, flows]

## Drawbacks
[Known costs, risks, complexity]

## Alternatives
[Other approaches considered and why rejected]

## Unresolved Questions
- [ ] Question 1
- [ ] Question 2

## Implementation Plan
1. Step 1 (timeline)
2. Step 2 (timeline)
```

## ADR Lifecycle

```
Proposed → Accepted → Deprecated → Superseded
              ↓
           Rejected
```

Never edit accepted ADRs. Write new ADR to supersede. Mark old ADR status: `Superseded by ADR-NNNN`.

## Directory Structure

```
docs/
└── adr/
    ├── README.md              # Index and guidelines
    ├── template.md            # Team's chosen base template
    ├── 0001-database-choice.md
    ├── 0002-caching-strategy.md
    └── 0003-deprecate-mongodb.md
```

### ADR Index (README.md)

```markdown
# Architecture Decision Records

| ADR | Title | Status | Date |
|-----|-------|--------|------|
| 0001 | [Title] | Accepted | YYYY-MM-DD |

## Creating New ADR
1. Copy `template.md` → `NNNN-title-with-dashes.md`
2. Fill template
3. Submit PR for review
4. Update index after approval
```

## Tooling (adr-tools)

```bash
# Install
brew install adr-tools

# Initialize ADR directory
adr init docs/adr

# Create new ADR
adr new "Use PostgreSQL as Primary Database"

# Supersede existing ADR
adr new -s 3 "Deprecate MongoDB in Favor of PostgreSQL"

# Regenerate index
adr generate toc > docs/adr/README.md

# Link related ADRs
adr link 2 "Complements" 1 "Is complemented by"
```

## Review Checklist

**Before submission:**
- [ ] Context explains problem without pre-deciding answer
- [ ] All viable options listed with honest tradeoffs
- [ ] Positive AND negative consequences documented
- [ ] Related ADRs linked

**During review:**
- [ ] ≥2 senior engineers reviewed
- [ ] Affected teams consulted
- [ ] Security implications addressed
- [ ] Reversibility assessed

**After acceptance:**
- [ ] ADR index updated
- [ ] Team notified
- [ ] Implementation tickets created

## Constraints

### MUST DO
- Document negative consequences — omitting cons = incomplete ADR
- Include rejected options — future engineers need full decision context
- Write ADRs before implementation, not after
- Use sequential numeric IDs (0001, 0002...)
- Link all directly related ADRs
- Update ADR status when decision changes

### MUST NOT DO
- Never edit accepted ADRs — create new ADR to supersede
- Never write ADR for minor patches, bug fixes, or config changes
- Never omit context — future readers lack original background
- Never hide rejected or failed decisions — prevents repeated mistakes
- Never leave "Proposed" status unresolved indefinitely
- Never use vague consequences ("some performance impact") — quantify

## Knowledge Reference

ADR, MADR, Architecture Decision Record, Michael Nygard, adr-tools, Y-Statements, RFC, lightweight ADR, technical debt, architecture governance, decision log, supersede, deprecate, architectural drivers, tradeoff analysis, consequence mapping, MADR template, decision graph, EventStoreDB, PostgreSQL, decision lifecycle
