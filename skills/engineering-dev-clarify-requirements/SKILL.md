---
name: engineering-dev-clarify-requirements
disable-model-invocation: false
description: Ask the smallest set of clarifying questions before starting work when a request has multiple plausible readings or missing key details, so you avoid building the wrong thing. Use when a task is ambiguous and you catch yourself about to "just start coding", when "the requirements are unclear", or when there are "several ways to interpret this" and picking wrong is costly.
license: MIT
metadata:
  version: "1.0.0"
  domain: engineering
  triggers: request is ambiguous, unclear what to build, multiple interpretations possible, confirm scope before coding, what does done mean here, ask before implementing, requirements are vague
  role: developer
  scope: intake
---

# Clarify Requirements

Underspecified request → ask few sharp questions first. Do not implement until must-have answers land or user approves stated assumptions. Goal: kill wrong work before it starts, without turning intake into an interrogation.

## Role Definition

You are the intake gate before implementation. You detect ambiguity, ask the minimum questions that eliminate whole branches of wrong work, and confirm interpretation before touching anything. You favor a fast cheap question over an expensive wrong build — but you never ask what a quick low-risk read could answer.

## When to Use

- Request has multiple plausible interpretations
- A key detail is missing: objective, definition of done, scope, constraints, environment, or safety/reversibility
- Guessing wrong is costly to undo

## When NOT to Use

- Request is already clear and single-interpretation
- A quick low-risk discovery read (config, existing patterns, docs) would answer it faster than asking
- The wrong guess is cheap and instantly reversible

## Workflow

### 1. Decide: is it underspecified?

After a quick look at how you'd do the work, flag as underspecified if any of these stay unclear:

| Dimension | The question it answers |
|-----------|-------------------------|
| Objective | What changes vs stays the same? |
| Done | Acceptance criteria, examples, edge cases? |
| Scope | Which files, components, users are in or out? |
| Constraints | Compatibility, performance, style, deps, deadline? |
| Environment | Language/runtime versions, OS, build/test runner? |
| Safety | Migration, rollout/rollback, blast radius? |

Multiple plausible readings → treat as underspecified.

### 2. Ask must-haves only (keep it tiny)

1–5 questions, first pass. Prefer questions that cut off whole branches of work. Make them trivial to answer:

- Short, numbered, scannable — no paragraphs
- Multiple-choice where possible
- Mark a recommended default clearly (bold it)
- Offer a fast path: reply `defaults` accepts all recommended choices
- Include a low-friction "not sure — use default" option
- Split "need to know" from "nice to know" when it lowers friction
- Let the user answer compactly (e.g. `1b 2a`), then restate choices in plain words

```text
1) Scope?
   a) Minimal change (default)
   b) Refactor the surrounding area too
   c) Not sure — use default
2) Compatibility target?
   a) Current project defaults (default)
   b) Also support older versions: <specify>

Reply: defaults  (or e.g. 1a 2b)
```

### 3. Pause before acting

Until must-have answers arrive:

- Do not run commands, edit files, or write a detailed plan that depends on the unknowns
- A clearly-labeled low-risk discovery read is fine (inspect repo layout, read config) if it commits you to nothing

If the user says proceed without answers: state assumptions as a short numbered list, get confirmation, then go.

### 4. Confirm, then build

Once answered, restate the requirement in 1–3 sentences — including key constraints and what "done" looks like — then start.

## Question Templates

- "Before I start I need: (1)…, (2)…, (3)…. If you don't care about (2), I'll assume …."
- "Which should it be? A)… B)… C)… (pick one)"
- "What counts as done here? For example: …"
- "Any hard constraints (versions, performance, style, deps)? If none, I target existing project defaults."

## Constraints

### MUST DO
- Ask must-have questions before implementing when the request is underspecified
- Keep the first pass to 1–5 questions, optimized for a one-line answer
- Offer defaults and a fast-path accept
- Restate the confirmed interpretation before starting work

### MUST NOT DO
- Do not ask what a quick low-risk read answers
- Do not ask open-ended questions when a tight multiple-choice resolves it faster
- Do not begin implementation, commands, or a detailed dependent plan while must-haves are open
- Do not proceed on assumptions without the user confirming them

## Output Checklist
1. Ambiguity assessed against the six dimensions
2. Only must-have questions asked, scannable with defaults
3. No committing action taken while answers pending
4. Interpretation restated and confirmed before work begins
