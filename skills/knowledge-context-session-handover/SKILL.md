---
name: knowledge-context-session-handover
disable-model-invocation: true
description: Write an end-of-session handover document that captures progress, decisions and their rationale, current file state, blockers, and concrete next steps, so the next session or agent resumes without re-deriving context. Use when asked to "create a handover", "save session state", "write a handoff doc", or "capture where we left off" before ending or switching a work session.
license: MIT
metadata:
  version: "1.0.0"
  domain: knowledge
  triggers: create a handover, save session state, write a handoff before I stop, capture where we left off, document this session for next time, hand this off to another agent
  role: context-curator
  scope: continuity
---

# Session Handover

Distill a work session into one handover file the next session reads to bootstrap. Capture what happened, why decisions went the way they did, current state, and what to do next. The file is the interface — all context goes in the file, not into chat.

## Role Definition

You are the session-continuity curator. At a session boundary you write a dated handover so a future session — human or agent — continues seamlessly without re-reading the whole history or re-litigating settled decisions. Distinct from broad knowledge-context curation: this is a point-in-time session snapshot, not an evergreen knowledge base.

## When to Use

- User asks to create a handover or save session state
- Ending a session on multi-step work that will continue later
- Work is interrupted mid-flight and picked up another time
- Handing off between people or agents

Manual only. Do not generate handovers automatically.

## Where It Lives

- Plan-bound work: write under the active plan's handover area, e.g. `plans/<name>/handovers/session-<YYYY-MM-DD>.md`
- Standalone (no formal plan): write `docs/handovers/session-<YYYY-MM-DD>.md` and drop plan/phase references
- Same-day repeats: append a counter — `session-<YYYY-MM-DD>-2.md`

Handovers are additive. Each session gets its own; never overwrite a prior one.

## Workflow

### 1. Locate context

Identify what is being worked on and where. Check for an active plan and its current phase/todo. No formal plan → standalone handover.

### 2. Gather session facts

Pull from the session, not from memory where a tool is authoritative:

- **Progress** — completed, in-progress (with current state), planned-but-not-started (with reason)
- **Decisions** — what was decided, the alternatives weighed, and *why* — so the next session doesn't re-open settled questions
- **Implementation state** — modified files and what changed; use `git status` and `git diff --stat` for the file list rather than recall; note uncommitted changes and pending tests
- **Blockers** — what stops progress, with a candidate fix if known

### 3. Write the document

Fill every section of `references/handover-template.md`. Follow its headings and frontmatter keys exactly.

### 4. Reconcile the task list

Update the active todo/plan status: mark completed items, add newly discovered ones, note blockers. Keep it lightweight — simple status edits only; large plan restructuring belongs to a planning skill, not here.

### 5. Confirm with the user

Ask whether anything is missing and whether the next steps are prioritized correctly. Adjust before finishing.

## Rules

1. **Accuracy over completeness** — document only what actually happened; never invent progress.
2. **Concrete next steps** — "continue the auth work" is useless. "Implement JWT refresh rotation in `src/auth/refresh.ts`, starting from the `rotateToken` stub" is actionable.
3. **Capture the why** — record decision rationale, not just the decision, so options aren't re-evaluated.
4. **File is the interface** — all context lands in the file, not in chat.
5. **Don't duplicate the task list** — reference it for status; the handover carries session *context* (decisions, state, blockers).
6. **Trust tools for state** — `git status` / `git diff --stat` over memory for file changes.
7. **Keep it scannable** — headings, tight bullets, tables. The next agent reads this to load context fast.

## Constraints

### MUST DO
- Write only on explicit request, never automatically
- Follow the template's headings and frontmatter keys
- Record decision rationale and concrete, file-level next steps
- Derive changed-file lists from git, not recall
- Confirm completeness and next-step priority with the user

### MUST NOT DO
- Do not invent or assume progress that did not happen
- Do not overwrite an existing handover — add a new dated file
- Do not restate the full task list inside the handover
- Do not bury the next session in prose — keep it scannable

## Output Checklist
1. Context located; plan-bound vs standalone decided
2. Progress, decisions+rationale, file state, blockers gathered
3. Template filled at the correct dated path
4. Task list reconciled lightly
5. Completeness and priorities confirmed with the user
