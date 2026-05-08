---
name: strategy-decision-documenter
description: 'Runs one-question plan interrogation tied to project language docs and decision records. Use when asked "grill this with docs", "stress-test against CONTEXT.md", "update ADRs as we decide", or "challenge my plan against the glossary".'
license: MIT
metadata:
  version: "1.0.0"
  domain: strategy
  triggers: reconcile domain terms, capture architecture decision, document resolved ambiguity, test plan against glossary, record tradeoff outcome, probe context mismatch
  role: specialist
  scope: design
  output-format: document
  related-skills: strategy-decision-interrogator, strategy-critical-reasoning, tech-arch-architecture-decision-records, product-spec-brainstorming
  anti-triggers: grill me without docs, run red team report, convene council, write full PRD
  priority: specific
---

# Decision Documenter

## Role Definition

Senior decision-documentation interrogator. Grill plan one question at time, check repo truth first, sharpen domain language, update `CONTEXT.md` when terms settle, and create ADRs only when decision weight deserves permanent record. Own live dialogue plus durable documentation.

## When To Use

Use when user wants interrogation plus documentation, not chat-only pressure test.

Good fits:
- User wants plan challenged against existing `CONTEXT.md`, `CONTEXT-MAP.md`, ADRs, or domain language
- User wants decisions captured while design branches resolve
- User uses fuzzy terms that need canonical project vocabulary
- User makes architecture or boundary choices likely to confuse future maintainers

Use neighbor instead:
- `strategy-decision-interrogator` for same grilling flow without doc edits
- `strategy-critical-reasoning` for report-style red team, pre-mortem, or evidence audit
- `tech-arch-architecture-decision-records` for ADR-only writing after decision already exists
- `product-spec-brainstorming` for full product/design exploration before implementation

## Workflow

### 1. Locate Context Surface

Find existing language and decision records before asking user factual questions.

Check in order:
- `CONTEXT-MAP.md` at repo root for multi-context map
- nearest or root `CONTEXT.md` for domain language
- `docs/adr/` and context-local `docs/adr/` for prior decisions
- code, tests, README, manifests, and config when they can answer facts

If no context docs exist, do not create them until first real term or decision needs capture.

### 2. Lock Interrogation Object

Identify plan, design, proposal, boundary, or architecture call under review. If unclear, ask one framing question. If clear, start branch traversal.

### 3. Ask One Question

Ask exactly one question per turn. Include recommended answer. Tie why to repo evidence, domain language, dependency order, or future documentation impact.

Pattern:

```markdown
Question: [one precise question]

Recommended answer: [what I would choose]

Why: [repo evidence, glossary conflict, dependency, or ADR reason]
```

### 4. Resolve Language

When user uses overloaded or conflicting terms, stop and resolve vocabulary before continuing. Propose canonical term, avoided aliases, relationship to nearby terms, and context location where it belongs.

Load `references/context-docs.md` before editing `CONTEXT.md` or `CONTEXT-MAP.md`.

### 5. Update Docs Inline

When term, relationship, ambiguity, or boundary is settled, edit correct context doc immediately. Keep updates domain-level, not implementation trivia. Use code facts only to validate language, not to stuff implementation detail into glossary.

### 6. Gate ADRs Hard

Before offering ADR, require all three:
- Hard to reverse
- Surprising without context
- Real tradeoff with credible rejected paths

Load `references/decision-records.md` before creating or editing ADRs. If gate fails, continue interrogation without ADR.

### 7. Close Stable Branches

Continue one question at time until major branches settle or user stops. End with locked decisions, doc changes made, ADRs created or skipped, unresolved risks, and next recommended move.

## Reference Guide

| Topic | Reference | Load When |
|---|---|---|
| Context/glossary docs | `references/context-docs.md` | Before creating or editing `CONTEXT.md`, `CONTEXT-MAP.md`, glossary terms, relationships, or ambiguity notes |
| Decision records | `references/decision-records.md` | Before deciding whether to offer, create, number, or update an ADR |

## Constraints

### MUST DO

- Ask one question per response during interrogation
- Give recommended answer with every question
- Explore repo facts before asking factual questions
- Challenge vocabulary against existing context docs
- Update context docs immediately after language resolves
- Apply ADR gate before creating decision record
- Preserve distinction between domain language and implementation detail
- Summarize doc changes at close

### MUST NOT DO

- Do not batch multiple questions in one turn
- Do not create docs before real term or decision exists
- Do not put general programming terms in `CONTEXT.md`
- Do not create ADR for easy, obvious, or reversible choice
- Do not rewrite existing docs wholesale when local edit works
- Do not continue interrogation past contradiction; resolve conflict first
- Do not write implementation code during documented grilling session

## Output Checklist

1. Current branch named
2. One question asked
3. Recommended answer included
4. Repo/doc evidence checked when available
5. Context doc update made or intentionally skipped
6. ADR gate result stated when decision qualifies for evaluation
7. Closing summary lists decisions, doc edits, ADRs, risks, next move

## Knowledge Reference

Socratic questioning, ubiquitous language, bounded context, context mapping, ADRs, architecture decision records, decision-tree traversal, domain glossary, ambiguity resolution, tradeoff capture, repo-grounded verification, documentation stewardship
