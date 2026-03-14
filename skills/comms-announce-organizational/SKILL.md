---
name: comms-announce-organizational
description: Draft professional internal announcements for organizational and role changes, including promotions, new hires, restructures, and leadership transitions.
---

# Internal Comms - Organizational Announcement

## Purpose
Create polished, supportive internal announcements for organizational or role changes.

## When to use this skill
Use this skill when you need to announce:
- Promotions
- New hires
- Department restructures
- Leadership transitions
- Role changes and transition plans

## Execution Logic

**Check $ARGUMENTS first to determine execution mode:**

### If $ARGUMENTS is empty or not provided:
Respond with:
"comms-announce-organizational loaded, proceed with additional instructions"

Then wait for the user to provide announcement details.

### If $ARGUMENTS contains content:
Proceed immediately to Task Execution.

## Task Execution

When requirements are available:

1. Identify the change type (promotion, hire, restructure, transition, or other role change).
2. Collect or infer core inputs:
   - Person/team names and roles
   - Nature of the change
   - Prior contributions or achievements
   - Rationale/business goal
   - Effective date and transition details
3. Draft the announcement in this structure:
   - Clear headline
   - Brief introduction
   - Body with achievements, rationale, and next steps
   - Optional encouraging/forward-looking close
4. Ensure tone is professional, supportive, appreciative, and aligned with corporate communication standards.
5. If details are missing, make reasonable corporate assumptions and state them.

## Writing Rules

- Keep language clear, concise, and respectful.
- Be specific about what is changing and when.
- Acknowledge contributions without exaggeration.
- Explain the "why" behind the change.
- Include immediate next steps or transition coverage details.
- Avoid jargon, humor, or informal phrasing.

## Output Format

Produce output in this format:

1. **Headline**
2. **Introduction** (1 short paragraph)
3. **Details** (achievements, rationale, next steps)
4. **Optional closing** (encouraging forward-looking note)
5. **Assumptions used** (only when information is missing)

## Defaults & Assumptions

If not provided, assume:
- Effective date: first business day of next month
- Transition coverage: current manager provides interim support until full transition
- Tone: company-wide internal memo style with appreciative, forward-looking language
