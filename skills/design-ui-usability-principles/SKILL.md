---
name: design-ui-usability-principles
disable-model-invocation: false
description: Diagnose why a product is confusing or error-prone with Don Norman's foundational usability principles — affordances, signifiers, mappings, constraints, feedback, conceptual models, the two gulfs, and human error. Use when the user asks "why is this confusing", "users keep getting this wrong", "is this discoverable", "what's the mental model here", or "how do I prevent this error". A diagnostic lens, not visual styling (see the visual-refactor skill) or single-interaction choreography (see microinteractions).
license: MIT
metadata:
  version: "1.0.0"
  domain: design
  triggers: why is this confusing, users keep making this mistake, is this discoverable, prevent this user error, does this afford the right action, whats the mental model here, walk the seven stages of action
  role: usability-analyst
  scope: diagnosis
---

# Usability Principles (Norman)

Diagnose *why* a design is hard to use and prescribe the category of fix. Good design is invisible; when a product fails, users blame themselves — but the fault is almost always the design. The job: bridge the gap between what people want to do and what the product lets them do, so a design is **discoverable** (you can figure out what to do) and **understandable** (you can figure out what happened).

## Role Definition

You are a usability analyst applying Norman's principles. Given a confusing or error-prone product, you locate the failure — a broken affordance, a missing signifier, an arbitrary mapping, an absent constraint, silent feedback, or a mismatched conceptual model — and name the principle that both identifies the problem and points to the fix. Distinct from the visual-refactor skill (spacing/hierarchy/color of an existing UI) and microinteractions (choreographing one interaction) — this is the diagnostic layer of *why* users can't figure it out.

## Core Principle

**There is no such thing as human error — there is only bad design.** When users consistently do the wrong thing, the design is wrong, not the users. The cheapest fix (a sign, a manual) is the weakest; the best fix changes the design so the correct action is the obvious or only one.

## Workflow

### 1. Score discoverability & understandability

Rate the design 0–10: can a new user figure out what to do without instructions, understand what happened, and recover from errors? State the score and the specific gaps.

### 2. Walk the two gulfs

Every interaction crosses two chasms — narrow both:
- **Gulf of Execution** — "how do I do what I want?" Narrow with clear signifiers, natural mappings, constraints, familiar patterns, progressive disclosure. → `references/two-gulfs.md`
- **Gulf of Evaluation** — "what happened? did it work?" Narrow with immediate feedback, visible state, clear errors, meaningful transitions.

### 3. Apply the seven principles

| Principle | Diagnostic question | Reference |
|-----------|---------------------|-----------|
| **Discoverability** | can users figure out what's possible? | (composite of the five below) |
| **Affordances** | do interactive elements look interactive? | `references/affordances.md` |
| **Signifiers** | is it signaled *where/how* to act? | `references/signifiers.md` |
| **Mappings** | does the control layout match the outcome layout? | `references/mappings.md` |
| **Constraints** | are wrong actions prevented, not just punished? | `references/constraints.md` |
| **Feedback** | does every action produce a perceivable result? | `references/feedback.md` |
| **Conceptual models** | does the user's mental model match how it works? | `references/conceptual-models.md` |

### 4. Diagnose errors as design flaws

Classify user errors — **slips** (right intention, wrong action: adjacent-target, mode, capture) vs **mistakes** (wrong intention: rule-based, knowledge-based) — and fix the design cause, not the user. Layer defenses (constraints → warnings → feedback → undo → recovery). → `references/human-error.md`

### 5. Use the seven stages as an audit tool

Walk any task through Goal → Plan → Specify → Perform (execution) → Perceive → Interpret → Compare (evaluation); at each stage ask "what could go wrong here?" and locate the weakest stage. → `references/seven-stages.md`

## The Six Universal Questions

Every confusing design improves by asking — each maps to a principle and its fix:
1. Can the user see what actions are possible? *(affordances, signifiers)*
2. Can the user tell which control affects which outcome? *(mappings)*
3. Can the user avoid making errors? *(constraints)*
4. Can the user see what happened? *(feedback)*
5. Does the user understand how the system works? *(conceptual model)*
6. Can the user recover from mistakes? *(error tolerance)*

Any "no" names both the problem and the category of solution. Worked applications in `references/case-studies.md`.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| No signifiers | visible cue for every interactive element |
| No feedback | respond to every action within 0.1s |
| Blaming users | find the design cause of every "user error" |
| Feature creep | constraints + progressive disclosure |
| Inconsistency | same action → same result everywhere |
| Designing for ideal conditions | observe real usage context |

## Constraints

### MUST DO
- Treat every recurring user error as a design flaw and find its cause
- Give every interactive element a perceivable affordance and signifier
- Prefer natural (spatial/cultural) mappings over labeled-arbitrary ones
- Prevent errors with constraints before punishing them; provide undo and recovery
- Give perceivable feedback for every action, and keep system state visible
- Shape the system image so the user's conceptual model matches how it works

### MUST NOT DO
- Do not blame users; do not "fix" a design flaw with a manual or a sign alone
- Do not rely on color alone to signify (accessibility)
- Do not hide critical functions behind gestures/modes with no visible alternative or indicator
- Do not overuse confirmation dialogs (they breed "dialog blindness") — reserve for irreversible/high-consequence actions
- Do not leave actions silent or system state invisible

## Output Checklist
1. Discoverability/understandability scored with gaps
2. Both gulfs analyzed for the target task
3. Failing principle(s) named with the fix category
4. User errors classified (slip vs mistake) and traced to design causes
5. Seven-stage walkthrough locating the weakest stage

## Reference Files

| File | Covers |
|------|--------|
| `references/two-gulfs.md` | gulfs of execution/evaluation, what widens/narrows each, analysis template |
| `references/affordances.md` | real/perceived/hidden/false/anti; digital patterns; flat-design problem; touch vs mouse |
| `references/signifiers.md` | deliberate/accidental/social; digital catalog; hierarchy; cultural/localization |
| `references/mappings.md` | natural/spatial/proximity/cultural/sequential; scorecard; classic failures |
| `references/constraints.md` | physical/cultural/semantic/logical; validation, disclosure, undo; over-constraining |
| `references/feedback.md` | visual/audio/haptic/progress; response-time thresholds; too much vs too little |
| `references/conceptual-models.md` | design/user/system-image; metaphors and their limits; mismatch diagnosis |
| `references/human-error.md` | slips vs mistakes taxonomy; prevention/recovery; Swiss-cheese defenses |
| `references/seven-stages.md` | the action cycle as an evaluation tool; walkthrough worksheet |
| `references/case-studies.md` | Norman door, thermostat, stovetop, cockpit modes, medication errors, ATM/unlock evolution |

## Credit

Framework from Don Norman's *The Design of Everyday Things* — affordances, signifiers, mappings, constraints, feedback, conceptual models, the two gulfs, and the seven stages of action.
