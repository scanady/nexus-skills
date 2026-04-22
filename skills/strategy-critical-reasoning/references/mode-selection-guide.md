# Mode Selection Guide

Auto-recommend or present to user when "You choose" is selected.

## Signal-to-Mode Mapping

| User Signal | Recommended Mode | Rationale |
|-------------|-----------------|-----------|
| "Is this the right approach?" | Socratic Questioning | Exploring assumptions, not yet committed |
| "I'm about to commit to X" | Dialectic Synthesis | Needs strongest counter-argument before committing |
| "What could go wrong?" | Pre-mortem Analysis | Explicitly asking about failure modes |
| "Is this secure/safe?" | Red Team | Security and adversarial framing |
| "The data shows that..." | Evidence Audit | Claims based on evidence need falsification |
| "Everyone agrees that..." | Socratic Questioning | Consensus signals unexamined assumptions |
| "We chose X over Y" | Dialectic Synthesis | Trade-off decision benefits from strongest counter |
| "This will definitely work" | Pre-mortem Analysis | Overconfidence signals need for failure imagination |
| "No one would ever..." | Red Team | Assumptions about adversary behavior |
| "Studies show..." | Evidence Audit | Cited evidence needs quality assessment |

## Decision Type Mapping

| Decision Type | Primary Mode | Secondary Mode |
|---------------|-------------|----------------|
| Technology choice | Dialectic Synthesis | Pre-mortem Analysis |
| Architecture decision | Pre-mortem Analysis | Red Team |
| Business strategy | Dialectic Synthesis | Evidence Audit |
| Security design | Red Team | Pre-mortem Analysis |
| Data-driven conclusion | Evidence Audit | Socratic Questioning |
| Process/workflow design | Pre-mortem Analysis | Socratic Questioning |
| Hiring/team decision | Socratic Questioning | Dialectic Synthesis |
| Vendor selection | Pre-mortem Analysis | Dialectic Synthesis |
| Trade-off resolution | Dialectic Synthesis | Socratic Questioning |
| Risk assessment | Red Team | Pre-mortem Analysis |

## Domain Mapping

| Domain | Default Mode | Why |
|--------|-------------|-----|
| Security | Red Team | Adversarial thinking is native to the domain |
| Infrastructure | Pre-mortem Analysis | Failure modes are the primary concern |
| Data/Analytics | Evidence Audit | Claims require evidence scrutiny |
| Product/UX | Socratic Questioning | Assumptions about users need surfacing |
| Business | Dialectic Synthesis | Strategy benefits from strongest counter |
| Architecture | Pre-mortem Analysis | Systems fail at integration points |
| Legal/Compliance | Evidence Audit | Claims must withstand scrutiny |

## Multi-Mode Sequencing

### Recommended Sequences

| Sequence | When to Use |
|----------|-------------|
| Socratic → Dialectic | Untested idea: surface assumptions first, then argue the counter |
| Pre-mortem → Red Team | High-stakes launch: find internal failures, then external attacks |
| Evidence Audit → Socratic | Data-driven proposal: audit evidence, then question interpretation |
| Dialectic → Pre-mortem | Strategic decision: argue the counter, then stress-test surviving position |

### When to Suggest Multi-Mode

- First mode reveals a risk category user hadn't considered
- Thesis survives first challenge largely intact (may need harder testing)
- Domain spans two mapping categories (e.g., security architecture decision)

### When NOT to Suggest Multi-Mode

- Question is narrow and specific
- First mode already surfaced actionable changes
- User signals they want to move on

## Auto-Recommendation Format

```
Based on [specific context signal], I recommend **[Mode Name]** because [1-sentence rationale].

[If secondary mode relevant:]
After that, a follow-up with **[Secondary Mode]** would [1-sentence benefit].
```

Present as options:
- Option 1: Recommended mode `(Recommended)`
- Option 2: Secondary mode if applicable
- Option 3: "Let me pick" — return to full mode selection

## Edge Cases

| Situation | Default | Reason |
|-----------|---------|--------|
| Vague context | Socratic Questioning | Surfaces what matters |
| Multiple concerns | Pre-mortem Analysis | Covers breadth naturally |
| User is emotional | Dialectic Synthesis | Steel manning validates before challenging |
| Technical vs business split | Match user's emphasis | Follow where the user's concern lives |
