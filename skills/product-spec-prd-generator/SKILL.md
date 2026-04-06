---
name: product-spec-prd-generator
description: Generates professional PRD (Product Requirements Document) files using expert product management practices. Takes a rough product idea, asks clarifying questions, and outputs a structured Markdown document ready to feed into AI coding assistants or share with stakeholders.
---

# PRD Generator

## Purpose
Transform a rough product idea into a comprehensive, expert-level Product Requirements Document (Markdown) through targeted discovery questions and structured output grounded in product management best practices.

---

## Execution Logic

**Check $ARGUMENTS first to determine execution mode:**

### If $ARGUMENTS is empty or not provided:
Respond with:
"prd-generator loaded, describe your product idea"

Then wait for the user to provide their product concept in the next message.

### If $ARGUMENTS contains content:
Proceed immediately to Task Execution (skip the "loaded" message).

---

## Task Execution

### 1. MANDATORY: Read Reference Files FIRST
**BLOCKING REQUIREMENT — DO NOT SKIP THIS STEP**

Before doing ANYTHING else, use the Read tool to read:
- `./references/prd_template.md`

This template defines the exact structure your PRD must follow. **DO NOT PROCEED** to Step 2 until you have read this file.

---

### 2. Analyze Initial Input
From the user's initial description, extract what's already provided:
- Product name or working title
- Core problem being solved
- Target users and their context
- Key features or capabilities mentioned
- Technical preferences or constraints
- Success criteria or metrics mentioned
- Competitive context or differentiators
- Scope signals (what's in and what's out)

Note what is **missing or unclear** — this drives Step 4.

---

### 3. Problem Framing Check (GATE)
**Before asking questions or writing anything**, assess whether the problem is sufficiently understood.

Ask yourself: *Can I articulate this product using the Universal Idea Model?*

> "An [object] for [class of users] that [does something] in order to [achieve a goal]. Users benefit by [getting something back] when [they are in a specific situation]."

- **If YES** — capture this statement internally; it becomes the PRD's opening line
- **If NO** — the problem is not yet clear enough to proceed; discovery questions must focus here first

**CRITICAL GATE:** A PRD written before the problem is understood is fiction. If the user's input is too vague to complete the Universal Idea Model, your first questions must resolve the who, what, and why — not the how or the features.

---

### 4. Reflect and Confirm Understanding
**Before asking any questions**, present your current understanding back to the user in this format:

```
Here's what I understand so far:
- **Product:** [name or working title]
- **Problem:** [what you understand the core problem to be]
- **User:** [who you understand the primary user to be]
- **Core value:** [what the product does and why the user benefits]
- **Universal Idea Model:** "An [X] for [Y] that [does Z] in order to [achieve W]."

Before I ask clarifying questions, does this capture the right framing?
Are there any corrections or important context I'm missing?
```

Wait for the user to confirm or correct. If the framing is wrong, update it before proceeding. This step prevents building a PRD on a misunderstood foundation.

---

### 5. Ask Clarifying Questions
With the framing confirmed, use **AskUserQuestion tool** to fill remaining gaps. Ask a maximum of 8 questions total, but fewer is better — stop when you have enough to produce a complete PRD.

**Question Bank (priority order):**

| # | Question | Why it matters | Skip if... |
|---|----------|----------------|------------|
| 1 | Who specifically is the primary user? What's their role, technical level, and what frustrates them most today? | Grounds all persona and UX decisions in a real person | Persona with role, context, and pain point is explicit |
| 2 | What does the user do today without this product? What's the workaround? | Defines the current state, root cause, and the baseline to improve on | Current workflow and workaround are clearly described |
| 3 | What are the 3-5 capabilities that absolutely must exist for v1 to be useful? What would make it a failure if missing? | Identifies the true P0 core; prevents features masquerading as MVP | Features listed with clear must-have rationale |
| 4 | Who are your main competitors or alternatives? What makes this different in a way users will actually care about? | Defines competitive positioning and differentiator for the problem statement | Competitive landscape or differentiator is stated |
| 5 | What does success look like 90 days after launch? What is the single most important number? | Anchors the North Star Metric and failure threshold | Success metrics or OKRs are explicitly stated |
| 6 | What should explicitly NOT be included in v1? What are the tempting features you're deferring? | Out-of-scope is as strategically important as in-scope | Out-of-scope is clearly stated |
| 7 | Are there any existing systems, platforms, or services this must integrate with or operate within? Any architectural constraints (e.g., must be web-based, must run on-premise, must comply with a data residency requirement)? | Defines external boundaries and non-negotiable architectural constraints | Integrations, deployment model, or technical constraints are specified |
| 8 | Are there any known risks, assumptions, deadlines, budget constraints, or compliance requirements? | Surfaces blockers early; shapes the Risks & Assumptions sections | Constraints, risks, or timeline are explicitly stated |

**Question strategy:**
- Ask 2-4 questions per batch using AskUserQuestion
- Prioritize questions 1-3 first; 4-8 only if gaps remain
- Never ask more than 8 questions total across all batches
- Never ask about something the user has already answered

---

### 6. Discovery Synthesis (Pre-Writing Confirmation)
**Before writing a single word of the PRD**, present a synthesis of everything you now know. This is the most important alignment step.

Present it as:

```
## Discovery Synthesis — Ready to Draft

**Universal Idea Model:**
"An [X] for [Y] that [does Z] in order to [achieve W]. Users benefit by [V] when [situation]."

**Core problem:** [1-2 sentence description of the current state and root cause]
**Primary user:** [persona name, role, key context]
**North Star Metric:** [the single most important success number]
**Failure threshold:** [what result would trigger a pivot or reassessment]
**P0 capabilities (MVP core):** [bulleted list of must-haves]
**Out of scope (v1):** [bulleted list of explicit deferrals]
**Key assumptions:** [top 3-5 bets this product makes]
**Key risks:** [top 2-3 risks identified]

Does this accurately capture what we're building? Any corrections before I draft the PRD?
```

**Do not proceed to Step 7 until the user confirms this synthesis is correct.** A wrong synthesis produces a wrong PRD.

---

### 7. Generate the PRD
Using the confirmed synthesis and the template structure from `./references/prd_template.md`, write a complete PRD:

**Non-negotiable requirements:**
1. **Fill every applicable section** — if a section doesn't apply, write "N/A — [reason]", never leave it blank
2. **Never prescribe implementation** — state what the user needs to do, not how the UI or code should work; that belongs in technical specs
3. **Every feature needs a user story** — "As a [persona], I want [action] so that [outcome]" — the outcome is the most important part
4. **Every feature needs testable acceptance criteria** — binary pass/fail, no ambiguity; if a QA engineer couldn't write a test case from it, rewrite it
5. **Prioritize using MoSCoW** — Must-have (launch blocker), Should-have (important for v1), Could-have (nice to have), Won't-have (explicitly deferred)
6. **One North Star Metric** — the single number that best captures whether the product is delivering value
7. **Failure threshold** — define what result would trigger a pivot, not just what success looks like
8. **Explicit out-of-scope section** — as important as the features list; document what v1 will NOT include
9. **3-7 named assumptions** — these are the hypotheses the product bets on; unstated assumptions become missed expectations
10. **Implementation Notes for AI section is mandatory** — this is what makes the PRD actionable for AI coding tools

---

### 8. PRD Self-Review (Quality Gate)
**After writing the PRD but before saving**, run it through this quality checklist. Fix any failures before proceeding.

**Five Quality Signals (from industry best practice):**

| Signal | Test | Pass / Fix |
|--------|------|-----------|
| **Engineer can estimate it** | Could an engineer read this and form a rough effort estimate without asking clarifying questions? | If no → requirements are too vague; add specificity |
| **Designer can prototype it** | Could a designer begin wireframing immediately from the user stories and UX requirements? | If no → user needs and flows are not clear enough |
| **Stakeholder can explain it back** | Could a business stakeholder read this and explain the purpose and scope in their own words? | If no → executive summary or problem statement needs rewriting |
| **Success is pre-defined** | Can you state what winning looks like without any post-launch data? | If no → success metrics are not specific enough |
| **Out-of-scope surprises no one** | Would a stakeholder be surprised by what's excluded? | If yes → the out-of-scope section needs to be shared and confirmed |

**Anti-pattern Check — verify the PRD does NOT:**
- [ ] Prescribe UI implementation ("the button should be blue") rather than user needs
- [ ] Have vague personas ("users who want productivity") instead of named, specific people
- [ ] Have missing or unmeasurable success metrics
- [ ] Have features with no acceptance criteria
- [ ] Have everything marked as Must-have
- [ ] Have an unclear or missing out-of-scope section
- [ ] Have assumptions that are unstated or treated as facts

**After reviewing:** Note any sections you strengthened and confirm the PRD is complete.

---

### 9. Save as Markdown

**Step 9a: Create output folder**
```bash
mkdir -p ./prd_outputs/[Project Name]/
```
Use the product name with spaces, e.g., `./prd_outputs/Churn Prevention Tool/`

**Step 9b: Save markdown file**
Write the PRD content to:
```
./prd_outputs/[Project Name]/[project_name]_PRD.md
```
Use snake_case for the filename, e.g., `churn_prevention_tool_PRD.md`

---

### 10. Confirm Output
Tell the user:
- Where the Markdown file is saved (full path)
- The Universal Idea Model sentence (one-line product summary)
- The North Star Metric
- The P0/Must-have feature count vs total features
- Any open questions logged in the PRD that still need decisions

---

## Writing Rules

### Core Rules
- Every feature MUST have testable, binary acceptance criteria (pass/fail — no ambiguity)
- Use specific numbers, not vague terms ("loads in <2s" not "loads quickly")
- Use MoSCoW prioritization — Must-have (launch blocker), Should-have (important), Could-have (nice to have), Won't-have (explicitly deferred)
- Data models must include field types, constraints, and relationships
- API specs must include request/response examples with realistic sample data
- Never invent requirements — if the user hasn't specified something, note it as an open question
- **Never prescribe implementation** — what the user needs to accomplish, not how the UI or code should do it

### PM Best Practices
- **Universal Idea Model**: Before writing, confirm you can articulate the product as one clear sentence: "An [X] for [Y] that [does Z] in order to [achieve W]."
- **Problem-first discipline**: Every feature must trace back to a stated user problem; features with no problem are scope creep
- **North Star Metric**: Every PRD must identify a single NSM — the one number that captures core value delivery
- **Failure threshold**: Define what result would trigger a pivot, not just what success looks like
- **Assumptions**: Document 3-7 key assumptions explicitly — these are the hypotheses the product bets on
- **Out of Scope**: Every undocumented assumption becomes a scope creep opportunity; explicitly deferred items become the v2 backlog
- **Risks**: Top 3-5 risks with likelihood, impact, and mitigation — a PRD without a risk section is incomplete
- **Open Questions**: List unresolved decisions with owners — prevents stale questions becoming surprise blockers
- **User stories**: The outcome clause ("so that...") is the most important part — if you can't write it, you don't understand the feature yet
- **Leading vs lagging metrics**: Include both early signals (activation, engagement) and business outcomes (retention, revenue)
- **Never write alone**: PRDs written without engineering/design input often contain impossible requirements

### PRD-Specific Rules
- Executive summary: 4-6 sentences covering what, who, why, and the expected measurable outcome
- Problem statement: Must include current state, root cause, and business/user impact with numbers where possible
- User personas: Maximum 3 primary personas with names, roles, specific frustrations, and behavioral context
- Feature hierarchy: Organize as Themes → Epics → User Stories where scope warrants it
- **Tech architecture**: Describe what the system does architecturally (components, data flow, deployment model, external boundaries) — not which frameworks or languages to use; those belong in a technical design doc
- Implementation Notes for AI section: Mandatory — never skip

### Anti-Patterns to Avoid
- Jumping to features before the problem is framed
- Vague personas ("users who want productivity") instead of specific, named people
- Missing or unmeasurable success metrics
- Requirements that prescribe the solution instead of describing the user need
- Everything marked as Must-have — if everything is critical, nothing is
- Out-of-scope section missing or vague
- PRD written in isolation without engineering or design input
- Assumptions treated as facts rather than explicitly named hypotheses

### Format Rules
- Use markdown headers consistently (# for title, ## for sections, ### for subsections)
- Use tables for structured data (metrics, data models, API specs, risks, open questions)
- Use code blocks for JSON examples and technical specs
- Use checkboxes for acceptance criteria
- Bold key terms on first use within a section

---

## Output Format

The PRD follows the structure in `./references/prd_template.md`. Sections included (in order):

1. Document Header (version, date, status, stakeholders)
2. Universal Idea Model
3. Executive Summary
4. Problem Statement
5. Goals & Success Metrics (including North Star Metric)
6. User Personas
7. Assumptions & Constraints
8. Out of Scope
9. Functional Requirements (with user stories and acceptance criteria)
10. Non-Functional Requirements
11. Technical Architecture
12. API Specifications
13. UI/UX Requirements
14. Data Models
15. Integration Points
16. Edge Cases & Error Handling
17. Risks & Mitigations
18. Testing Requirements
19. Release Criteria
20. Launch Strategy
21. Open Questions
22. Implementation Notes for AI
23. Appendix

Here's a condensed example:

```markdown
# TaskFlow — Product Requirements Document

**Version:** 1.0
**Date:** 2026-04-05
**Author:** PRD Generator
**Status:** Draft
**Stakeholders:** Engineering Lead, Design Lead, CEO

## Executive Summary
TaskFlow is a task management tool for remote engineering teams that eliminates context switching between disconnected project tools. It targets engineering managers at companies with 10-50 engineers who lose visibility during async sprints. By centralizing task creation, assignment, and status tracking in a single interface integrated with GitHub and Slack, TaskFlow reduces coordination overhead and surfaces blockers before they delay delivery. The expected outcome is a 40% reduction in sprint planning overhead and fewer missed deadlines.

## Problem Statement
**Current state:** Engineering teams juggle tasks across Jira, Slack threads, GitHub Issues, and spreadsheets with no single source of truth.
**Root cause:** No tool was designed for async-first teams; most tools assume synchronous standups and co-located teams.
**Pain points:**
1. Status updates require manual cross-referencing across 3+ tools
2. Blockers surface too late — after daily standups, not before
3. Engineering managers lack real-time visibility without interrupting engineers
**Impact:** 5+ hours/week per engineer lost to coordination overhead; avg. 2 delayed sprints per quarter.

## Goals & Success Metrics

**North Star Metric:** Weekly Active Teams (teams with ≥3 active members creating tasks in a 7-day window)

| Goal | Metric | Target | Measurement Method | Timeline |
|------|--------|--------|-------------------|----------|
| Reduce coordination overhead | Zeit spent in status meetings | -40% | Calendar integration | 90 days |
| Surface blockers earlier | Avg hours between blocker creation and resolution | < 4h | In-app tracking | 60 days |
| Drive retention | Week-4 retention | > 60% | Analytics | 30 days post-launch |

## Assumptions & Constraints
**Assumptions:**
1. Users have GitHub accounts and existing repos to connect
2. Teams run 1-2 week sprints and do async standups
3. A Slack integration will drive adoption better than email notifications

**Constraints:**
- Budget: MVP must ship in 6 weeks with 2 engineers
- Compliance: No PII beyond email address in v1; GDPR not required for initial US-only launch

## Out of Scope (v1)
- Time tracking or billing
- Gantt charts or roadmap views
- Mobile native apps (responsive web only)
- AI-generated task suggestions

## Functional Requirements

### FR-001: Task Creation
**Description:** Users can create tasks with title, description, assignee, due date, and priority.
**User story:** As an engineer, I want to create a task in under 10 seconds so that I capture work items without breaking my flow.
**Priority:** P0 — Product doesn't function without task creation.
**Acceptance criteria:**
- [ ] Task creation modal opens in < 200ms
- [ ] Title is required (3-200 chars); all other fields optional
- [ ] Due date defaults to end of current sprint if sprint exists
- [ ] New task appears in board view without page reload
- [ ] Creator is auto-assigned as default assignee

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| GitHub API rate limits during high activity | Medium | High | Cache GitHub data; implement exponential backoff |
| Low activation if onboarding is complex | High | High | Limit onboarding to 3 steps; defer team configuration to later |
| Slack app review delays launch | Low | Medium | Build email fallback notifications in parallel |

## Open Questions

| Question | Owner | Decision Needed By |
|----------|-------|--------------------|
| Should tasks auto-close when linked PR is merged? | Product | Sprint 2 kickoff |
| What's the pricing model for teams > 10 members? | CEO | Before public launch |

## Implementation Notes for AI

### Build Order
1. Data schema and persistence layer
2. Authentication and authorization
3. Core API / business logic
4. Background processing and integrations
5. User interface components
6. End-to-end flows and polish

### Key Behavioral Constraints
- All timestamps stored in UTC; convert to user's local timezone on display
- Use optimistic updates for status changes — board UX depends on instant feedback
- Soft deletes for all user-generated content — never permanently remove records
- Human-readable record identifiers in the UI (e.g., TASK-001), backed by internal IDs

### Data Integrity Rules
- A task must belong to exactly one project; orphaned tasks are not permitted
- Sprint dates cannot overlap for the same team

### Common Pitfalls to Avoid
- Do not expose internal database IDs in public URLs — use slugs or opaque identifiers
- Pagination must handle real-time data correctly — avoid offset-based pagination on live feeds
```
```

---

## References

**This file MUST be read using the Read tool before task execution (see Step 1):**

| File | Purpose |
|------|---------|
| `./references/prd_template.md` | Complete PRD structure with all 23 sections, format examples, and usage notes |

**Why this matters:** The template ensures every PRD follows a consistent, comprehensive structure that AI coding tools can parse and implement. Skipping the template results in incomplete PRDs that miss critical sections.

---

## Quality Checklist (Self-Verification)

### Pre-Execution Check
- [ ] I read `./references/prd_template.md` before starting
- [ ] I have the template structure in context

### Discovery Check
- [ ] I articulated the product using the Universal Idea Model before asking questions
- [ ] I reflected understanding back to the user and received confirmation before questioning
- [ ] I asked 8 or fewer questions total
- [ ] I only asked questions where information was genuinely missing
- [ ] I presented a Discovery Synthesis and received confirmation before drafting

### PRD Content Check
- [ ] Universal Idea Model sentence is in the executive summary
- [ ] Problem statement includes current state, root cause, and impact with numbers
- [ ] Personas are named, specific, with clear frustrations and behavioral context (not generic)
- [ ] Every feature has a user story with a meaningful outcome clause
- [ ] Every feature has testable, binary acceptance criteria (checkboxes)
- [ ] MoSCoW prioritization applied — not everything is Must-have
- [ ] Prioritization rationale is stated for each tier
- [ ] North Star Metric is a single, specific number
- [ ] Failure threshold (pivot trigger) is defined
- [ ] Leading and lagging success metrics are both included
- [ ] Assumptions section lists 3-7 named hypotheses
- [ ] Out-of-scope section explicitly lists deferred items
- [ ] Risks section covers top 3-5 risks with likelihood, impact, mitigation
- [ ] Open questions are logged with owners
- [ ] No requirements prescribe implementation (how) instead of user needs (what)
- [ ] Data models include field types and relationships
- [ ] "Implementation Notes for AI" section is complete

### Five Quality Signals Check
- [ ] An engineer could estimate effort from this PRD without asking clarifying questions
- [ ] A designer could begin wireframing from the user stories and UX sections
- [ ] A stakeholder could explain the purpose and scope back in their own words
- [ ] Success can be measured before any post-launch data exists
- [ ] The out-of-scope section would surprise no stakeholder

### Output Check
- [ ] Markdown file saved to `./prd_outputs/[Project Name]/`
- [ ] User informed of file path, Universal Idea Model, North Star Metric, and open questions

**If ANY check fails → fix before completing.**

---

## Defaults & Assumptions

Use these unless the user specifies otherwise:

- **Document version:** 1.0
- **Status:** Draft
- **Author:** PRD Generator
- **Prioritization:** MoSCoW — Must-have ~30-40%, Should-have ~30-40%, Could-have ~15-20%, Won't-have remainder
- **User personas:** Maximum 3 unless scope complexity demands more
- **API style:** REST unless otherwise specified
- **Feature hierarchy:** Epics → User Stories unless scope is small enough for a flat structure

Document any defaults applied in the PRD's Assumptions section.
