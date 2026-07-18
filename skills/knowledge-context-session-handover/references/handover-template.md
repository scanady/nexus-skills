---
type: session-handover
plan: "{{plan_name}}"        # omit for standalone handovers
session_date: "{{YYYY-MM-DD}}"
phase: {{phase}}             # omit for standalone handovers
---

# Session Handover — {{YYYY-MM-DD}}

<!-- Plan-bound only; delete this line for standalone handovers -->
> Plan: [{{plan_name}}](../plan.md) · Phase {{phase}}

## Summary

<!-- 2–3 sentences: what this session was about and where it ended. -->

## Progress

### Done
- {{completed_item}}

### In progress (interrupted)
- {{item}} — state: {{where_it_stands}}

### Not started (deferred)
- {{item}} — reason: {{why_deferred}}

## Key Decisions

<!-- Capture the why so the next session doesn't re-open these. -->

| Decision | Why | Alternatives considered |
|----------|-----|-------------------------|
| {{decision}} | {{rationale}} | {{alternatives}} |

## Current State

### Modified files
<!-- From `git status` / `git diff --stat`, not memory. -->

| File | Change | Status |
|------|--------|--------|
| {{path}} | {{what_changed}} | complete / partial |

Uncommitted changes: {{yes_no_details}}

### Pending tests
- {{test_to_run}}

## Blockers

- {{blocker}} — candidate fix: {{fix_if_known}}

## Next Steps

<!-- Ordered, concrete, file-level. What to do first. -->
1. {{next_step}}

## Context for Next Session

<!-- Anything that would otherwise be lost: assumptions made, workarounds applied,
     error messages hit, "watch out for" notes, half-formed reasoning. -->
