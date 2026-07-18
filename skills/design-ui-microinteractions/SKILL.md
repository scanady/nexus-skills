---
name: design-ui-microinteractions
disable-model-invocation: false
description: Design a single self-contained interaction end-to-end using Dan Saffer's four-part structure — trigger, rules, feedback, loops & modes. Use for one contained moment: "design a toggle", "get the button/loading feedback right", "pull-to-refresh behavior", "what should happen when they tap this", "error and empty state behavior". For overall visual polish defer to the visual-refactor skill; for affordance and discoverability defer to the usability-principles skill.
license: MIT
metadata:
  version: "1.0.0"
  domain: design
  triggers: design a toggle switch, get button press feedback right, loading and progress states, pull to refresh behavior, what happens when they tap this, error and empty state behavior, add a signature delight moment
  role: interaction-designer
  scope: single-interaction
---

# Microinteractions

Design the small, contained moments — a toggle, a password field, a like button, a loading state, pull-to-refresh. Each is one use case, so small users barely notice it consciously but feel it. Work the four parts in order: a **Trigger** starts it, **Rules** decide what happens, **Feedback** shows what's happening, **Loops & Modes** govern its behavior over time.

## Role Definition

You are an interaction designer working at the detail level. Given one contained moment, you specify its trigger, rules, feedback, and long-term behavior, then audit it for edge cases and accessibility. Distinct from the visual-refactor skill (whole-screen hierarchy/spacing/color) and the usability-principles skill (whether users understand what an object affords) — this skill choreographs a single interaction from tap to resolution.

## Core Principle

The gap between a product users tolerate and one they love is almost always in the microinteractions. Every one follows the same structure — so make each part deliberate rather than default.

## Workflow

### 1. Score, then design/audit

Rate the interaction 0–10: does it have a discoverable trigger, simple predictable rules, immediate proportional feedback, and thoughtful loop/mode behavior? State the score and the specific gaps to reach 10.

### 2. Work the four parts + two disciplines

| Part | Question | Deep dive |
|------|----------|-----------|
| **Trigger** | How is it initiated (manual or system)? Is it discoverable? Does it show state? | `references/trigger-design.md` |
| **Rules** | What happens, in what order, with what constraints, when does it end, what if it fails? | `references/rules-and-state.md` |
| **Feedback** | What does the user see/hear/feel, and is it proportional and immediate? | `references/feedback-patterns.md` |
| **Loops & Modes** | How does it behave on the 100th use? Are there modes (and are they visible)? | `references/loops-modes.md` |

Then two cross-cutting disciplines:
- **Signature moments** — should this be a brand-defining moment? Most shouldn't. `references/signature-moments.md`
- **Reduce & simplify** — the best microinteraction has zero configuration, one action, immediate result. If it needs instructions, it's too complex.

### 3. Check the worked patterns

Blueprints for the most common interactions (form submission, toggle, pull-to-refresh, loading states, notifications) are in `references/case-studies.md` — each broken down by the four parts plus edge cases and accessibility.

## The Six Focus Areas

**1. Triggers** — Manual (tap, swipe, type, voice) or system (time, threshold, data, error). A trigger must show three things: that it exists, what it does, its current state. Invisible/gesture triggers always need a visible fallback.

**2. Rules** — Derive from the goal, not the interface. Match platform conventions. Constrain inputs to *prevent* errors rather than punish them. Handle edge cases explicitly (zero, max, repeat, interruption). Simple rules → complex-feeling interaction; complex rules → confusing.

**3. Feedback** — Immediate (<100ms for direct manipulation). Use the *least* feedback that communicates; scale it to the event's significance. Visual is primary; audio/haptic supplement, never replace. Honest progress only.

**4. Loops & Modes** — Open loops run until stopped, closed loops run once. Long loops evolve the interaction (progressive reduction for experts). Modes are dangerous (same action, different result) — minimize them and make the active mode unmistakable, with an always-visible exit.

**5. Signature moments** — Distinctive, frequent, functional-first details that become product identity (slide-to-unlock, Slack loading messages). Restraint: 2–3 per product, max. If removing it wouldn't be missed, it was decoration.

**6. Reduce & simplify** — Fewer options, steps, decisions. Smart defaults over configuration. Rule count proportional to frequency of use.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| No feedback on action | immediate visual state change on every interactive element |
| Overdesigning frequent moments | reserve rich animation for infrequent, high-impact events |
| Ignoring edge cases | map empty/loading/partial/full/error/disabled |
| Invisible triggers | pair gestures with a visible alternative |
| Mode errors | make active mode visible; minimize modes |
| Same at use 1 and use 100 | progressive reduction via long loops |
| Feedback overload | tier feedback; consolidate; reserve big signals for big events |
| Fake progress bars | honest/deterministic progress; indeterminate spinner when unknown |

## Constraints

### MUST DO
- Design all four parts, not just the visible feedback
- Give every trigger discoverable, state-communicating affordance
- Prevent errors with constraints; preserve user input on failure
- Make feedback immediate and proportional to the event
- Design the long loop (behavior over repeated use) and any mode's visible exit
- Meet accessibility baseline: ARIA state, keyboard operation, `prefers-reduced-motion`, non-color signals

### MUST NOT DO
- Do not hide essential functionality behind an invisible trigger with no fallback
- Do not use hidden rules to manipulate (unsubscribe harder than subscribe, fake urgency timers)
- Do not use deceptive/fake progress indicators
- Do not add "delight" that delays the task or fails on slow devices
- Do not ship more than 2–3 signature moments or 3+ modes without redesigning

## Output Checklist
1. Score (0–10) with specific gaps
2. Trigger, rules, feedback, loops/modes each specified
3. Edge cases mapped (empty, max, rapid, offline, interrupted)
4. Accessibility baseline met
5. Reduced to its simplest form

## Credit

Framework from Dan Saffer's *Microinteractions: Designing with Details* — the Trigger / Rules / Feedback / Loops & Modes structure.
