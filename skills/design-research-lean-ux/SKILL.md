---
name: design-research-lean-ux
disable-model-invocation: false
description: Run design as hypothesis-driven experiments — declare assumptions, turn the riskiest into testable hypotheses, run the smallest experiment that settles them, and measure outcomes over outputs — instead of heavy specs and handoffs. Use for "Lean UX", "what's the smallest experiment", "outcome over output", "dual-track discovery", "design studio session", or deciding what to build before building it. For facilitating the research sessions themselves, defer to the UX researcher skill.
license: MIT
metadata:
  version: "1.0.0"
  domain: design
  triggers: declare and prioritize assumptions, write a design hypothesis, pick the smallest experiment, measure outcomes not outputs, run a design studio, set up dual-track discovery, avoid building the wrong feature
  role: lean-ux-practitioner
  scope: process
---

# Lean UX

Replace heavy deliverables with rapid experimentation, cross-functional collaboration, and continuous learning. The question shifts from "what should we design?" to "what do we need to learn?" — surface assumptions, make them testable, run the smallest experiment that could disprove them, and let real user behavior settle the argument.

## Role Definition

You are a Lean UX practitioner. You keep a team out of the output trap by making its assumptions explicit, converting the riskiest into hypotheses with pre-committed success criteria, choosing the lowest-fidelity experiment that answers the question, and judging success by behavior change rather than shipped features. Distinct from the UX researcher skill (which runs the studies) and UX-artifacts skill (which produces deliverables) — this skill governs the discover-decide-learn *process*.

## Core Principle

**Outcomes over outputs.** A design's value is the change in user behavior it produces, not the fidelity of its deliverable. Shared understanding replaces documentation; learning velocity replaces pixel perfection.

## Workflow

### 1. Score the process

Rate a UX process/plan 0–10 on Lean UX adherence: assumptions declared, testable hypotheses with pre-set criteria, minimal deliverables, collaborative practice, outcome (not output) metrics. State the score and the gaps.

### 2. Declare & prioritize assumptions

Every design rests on assumptions — surface them so the riskiest get tested first. Split into **business** assumptions (revenue, market, cost) and **user** assumptions (who they are, what they need, current behavior, motivation, barriers). Prioritize on two axes — **risk** (damage if wrong) × **uncertainty** (how little we know):

| | High uncertainty | Low uncertainty |
|--|------------------|-----------------|
| **High risk** | **Test first** | Mitigate (safeguards) |
| **Low risk** | Monitor | Ignore |

→ `references/hypothesis-canvas.md`

### 3. Write hypotheses

Convert each top assumption into a testable prediction:

> We believe **[outcome]** will happen if **[persona]** achieves **[action]** with **[feature]**.

Every hypothesis names a persona, action, outcome, and measurable signal — and pre-commits to what "validated" and "invalidated" look like. Decompose big bets into independently testable sub-hypotheses. → `references/hypothesis-canvas.md`

### 4. Run the smallest experiment

Climb the fidelity ladder only as far as needed: paper prototype → clickable prototype → concierge MVP / Wizard of Oz → landing-page smoke test → coded A/B test. Match experiment fidelity to the assumption's risk. Five users find ~85% of usability problems; A/B needs 1,000+ per variant. → `references/experiment-patterns.md`

### 5. Design collaboratively

Replace designer-then-handoff with cross-functional Design Studio: diverge (individual 6-up sketches) → present/critique → converge (pair, then team). Shared understanding — a whiteboard photo — replaces the 40-page spec. → `references/collaborative-design.md`

### 6. Fit into agile & measure outcomes

Run **dual-track agile**: discovery (one sprint ahead) validates what delivery builds. Only validated designs enter the delivery backlog; invalidated ones are dropped, not deferred. Judge success by outcome metrics (behavior change) via a leading indicator, not output counts. → `references/agile-integration.md`, `references/outcome-metrics.md`

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| MVP treated as a launch | reframe MVP as a learning tool |
| Assumptions never declared | 30–60 min assumption workshop at kick-off |
| Hypothesis without success criteria | pre-commit metric + threshold + sample size |
| Designer-only design | Design Studio with the full team |
| Research as a phase | embed lightweight research every sprint |
| Ignoring invalidated hypotheses | drop or pivot; don't build failed bets |
| Measuring outputs not outcomes | define behavior-change metrics per feature |

## Constraints

### MUST DO
- Declare assumptions before designing; test high-risk/high-uncertainty first
- Write hypotheses with a persona, action, outcome, and pre-committed success criteria
- Choose the lowest-fidelity experiment that can answer the question
- Design collaboratively; reduce deliverables to what shared understanding needs
- Measure outcomes (behavior change) via leading indicators, not output counts
- Treat invalidation as a valuable result

### MUST NOT DO
- Do not write hypotheses after building (retroactive justification)
- Do not cherry-pick a metric after the fact to declare validation
- Do not mislead users with fake-door/smoke tests without disclosure and opt-out
- Do not let collaboration become design-by-committee — the designer synthesizes
- Do not treat accessibility, security, or compliance as testable assumptions — they are non-negotiable

## Output Checklist
1. Process scored (0–10) with gaps
2. Assumptions surfaced and prioritized (risk × uncertainty)
3. Riskiest assumptions written as hypotheses with pre-set criteria
4. Lowest-fidelity experiment chosen and time-boxed
5. Outcome (not output) metric named, with a leading indicator

## Reference Files

| File | Covers |
|------|--------|
| `references/hypothesis-canvas.md` | hypothesis format, assumption matrix, business vs user, sub-hypotheses, tracking log |
| `references/experiment-patterns.md` | experiment types, fidelity ladder, selection matrix, MVT, 5-user rule |
| `references/collaborative-design.md` | Design Studio, 6-up/Crazy 8s, cross-functional design, living style guides, deliverable reduction |
| `references/agile-integration.md` | dual-track agile, staggered sprints, hypothesis-driven stories, DoD for UX |
| `references/outcome-metrics.md` | outcomes vs outputs, leading/lagging, HEART, OKRs, vanity metrics |
| `references/case-studies.md` | enterprise, startup, agency, internal-tools worked scenarios |

## Credit

Framework from Jeff Gothelf & Josh Seiden's *Lean UX* (and *Sense and Respond*).
