# PRD Template Structure

This template defines the structure for expert-level Product Requirements Documents grounded in modern PM best practices. It covers new products and new features. Use every applicable section; mark non-applicable sections as "N/A — [reason]" rather than omitting them.

---

## Document Sections

### 1. Document Header

```markdown
# [Product Name] — Product Requirements Document

**Version:** 1.0
**Date:** [YYYY-MM-DD]
**Author:** [Name / PRD Generator]
**Status:** Draft | In Review | Approved
**Stakeholders:** [Engineering Lead, Design Lead, CEO, etc.]
**Last Updated:** [YYYY-MM-DD]
**Change Log:** [v1.0 — Initial draft]
```

---

### 2. Universal Idea Model

The single sentence that defines what this product is and why it exists. Every section of the PRD should be traceable back to it.

```markdown
## Universal Idea Model

> "An [object/product type] for [class of users] that [does something specific] in order to [achieve a goal].
> Users benefit by [getting something tangible] when [they are in a specific situation]."
```

**Example:**
> "An AI-powered onboarding wizard for new SaaS users that personalizes the setup sequence based on role and goals in order to reduce time-to-value. Users benefit by reaching their first 'aha moment' faster when they first activate the product."

**If you cannot complete this sentence cleanly, the problem is not yet understood well enough to write a PRD.**

---

### 3. Executive Summary

4-6 sentences covering: what the product does, who it's for, the core problem it solves, the approach, and the expected measurable outcome.

```markdown
## Executive Summary

[Product Name] is a [type of product] for [primary user] that [core function]. It addresses [the specific problem] by [the approach]. The expected outcome is [measurable result] within [timeframe].
```

---

### 4. Problem Statement

```markdown
## Problem Statement

**Current state:** [What exists today and why it is broken or insufficient]

**Root cause:** [Why the problem persists — underlying cause, not just symptoms]

**Pain points:**
1. [Specific, observable pain — with data/evidence where available]
2. [Specific pain]
3. [Specific pain]

**Impact:** [Business and user cost of NOT solving this — quantify where possible]
- User impact: [e.g., 5+ hours/week lost per person]
- Business impact: [e.g., 25% churn in first 30 days; avg. 2 delayed sprints per quarter]

**Evidence:** [Customer interviews, survey data, support tickets, analytics — cite sources]
```

---

### 5. Goals & Success Metrics

```markdown
## Goals & Success Metrics

**North Star Metric:** [The single most important number that captures core value delivery]
> Example: "Weekly Active Teams — teams with ≥3 members creating tasks in a 7-day window"

**Failure Threshold:** [The result that would trigger a reassessment or pivot]
> Example: "If Week-4 retention is below 30% after 90 days, reassess core value proposition"

### Leading Metrics (early signals)
| Metric | Target | Measurement | Timeline |
|--------|--------|-------------|----------|
| [Activation rate] | [> 60%] | [Analytics] | [30 days] |
| [Time-to-first-value] | [< 24h] | [Event tracking] | [30 days] |

### Lagging Metrics (business outcomes)
| Goal | Metric | Target | Measurement | Timeline |
|------|--------|--------|-------------|----------|
| [Retain users] | [Week-4 retention] | [> 50%] | [Analytics] | [90 days] |
| [Drive revenue] | [Paid conversion] | [> 8%] | [Billing system] | [90 days] |
```

---

### 6. User Personas

Maximum 3 primary personas. More creates unfocused requirements. Each must be named and specific — "users who want productivity" is not a persona.

```markdown
## User Personas

### Persona 1: [Name]
- **Role:** [Job title and company context]
- **Goals:** [What they are trying to accomplish — specific, not generic]
- **Pain points:** [Current frustrations — observable behaviors, not assumed]
- **Technical proficiency:** Low | Medium | High
- **Usage context:** [When, where, and how often they will use this]
- **Representative quote:** "[A sentence this person would actually say about the problem]"

### Persona 2: [Name]
[Same structure]

### Persona 3: [Name] *(if applicable)*
[Same structure]
```

---

### 7. Assumptions & Constraints

```markdown
## Assumptions & Constraints

### Assumptions
These are the hypotheses this product bets on. If any prove false, the strategy may need to change.

1. [Assumption — e.g., "Users have existing GitHub accounts and repos to connect"]
2. [Assumption — e.g., "Teams prefer async communication over live standups"]
3. [Assumption — e.g., "Slack integration will drive adoption better than email"]
4. [Continue — aim for 3-7 named assumptions]

### Constraints
- **Timeline:** [e.g., MVP must ship in 6 weeks]
- **Team:** [e.g., 2 engineers, 1 designer]
- **Budget:** [e.g., infrastructure cost must stay under $500/month at launch]
- **Compliance:** [e.g., GDPR not required for initial US-only launch; SOC2 required within 6 months]
- **Technical:** [e.g., must integrate with existing Salesforce CRM]
```

---

### 8. Out of Scope (v1)

As strategically important as the features list. Every item not explicitly excluded is implicitly included — until the argument happens mid-sprint.

```markdown
## Out of Scope (v1)

The following are explicitly deferred to v2 or later:

- [Feature — e.g., "Multi-language support"]
- [Feature — e.g., "Mobile native apps (responsive web only in v1)"]
- [Feature — e.g., "Admin bulk-import tools"]
- [Feature — e.g., "Enterprise SSO"]
- [Feature — e.g., "AI-generated suggestions"]

These items are not rejected — they are deferred to protect focus and deliver a sharp v1 that tests the core value.
```

---

### 9. Functional Requirements

Organize as Themes → Epics → User Stories where scope warrants. For smaller products, Epics → User Stories is sufficient.

```markdown
## Functional Requirements

### Feature Prioritization (MoSCoW)
- **Must-have:** Without this, the product cannot launch or core value is not delivered
- **Should-have:** Important for v1; include if capacity allows
- **Could-have:** Nice to have; defer if time-constrained
- **Won't-have (v1):** Explicitly deferred — see Out of Scope section

---

### Epic 1: [Epic Name]
*[One sentence describing the large capability this epic covers]*

#### FR-001: [Feature Name]

**Description:** [One sentence — what this feature does and for whom]

**User story:** As a [persona name], I want to [specific action] so that [meaningful outcome this enables].

**Priority:** Must-have | Should-have | Could-have
**Priority rationale:** [Why this tier — "Product cannot launch without this" or "Critical for activation but not for basic functionality"]

**Acceptance criteria:**
- [ ] [Specific, testable, binary criterion — a QA engineer can write a test case from this]
- [ ] [e.g., "Task creation modal opens in < 200ms on a standard connection"]
- [ ] [e.g., "Title field is required (3-200 chars); form blocks submission if empty"]
- [ ] [e.g., "New task appears in board view without page reload"]

**Dependencies:** [FR-XXX, or "None"]
**Open questions:** [Any unresolved decisions about this feature]

---

#### FR-002: [Feature Name]
[Same structure]
```

**Priority distribution guideline:** Must-have ~30-40%, Should-have ~30-40%, Could-have ~15-20%, Won't-have remainder.

---

### 10. Non-Functional Requirements

```markdown
## Non-Functional Requirements

### Performance
- Page load time (initial): < [X]s on [connection type]
- API response time (p95): < [X]ms
- Concurrent users at launch: [N]
- Expected peak load: [N requests/minute]

### Security
- Authentication: [e.g., OAuth2 / JWT / session-based — describe the method, not the vendor]
- Authorization: [RBAC / role model description]
- Encryption: At rest ([AES-256]) and in transit ([TLS 1.3])
- Compliance: [GDPR / SOC2 / HIPAA / None for v1]
- PII handling: [What personal data is stored and how it is protected]

### Reliability & Availability
- Uptime target: [99.9%]
- Backup frequency: [Daily snapshots]
- RTO: [4 hours]
- RPO: [1 hour]

### Scalability
- Initial load: [N users / N requests/day]
- 12-month growth target: [N users / N requests/day]
- Scaling approach: [Horizontal / auto-scale / etc.]

### Accessibility
- Standard: [WCAG 2.1 AA / None for v1]
- Requirements: [Keyboard navigation, screen reader support, etc.]
```

---

### 11. Technical Architecture

```markdown
## Technical Architecture

### System Overview
[Describe the system in plain English — what the major components are and how they relate. AI coding tools interpret prose better than abstract diagrams.]

### System Type
[e.g., "Single-page web application with a REST API backend and a relational database. Deployed as a cloud-hosted service."]

### Deployment Model
[e.g., "Cloud-hosted, always-on service" / "On-premise, single-tenant" / "Serverless / edge-deployed functions"]

### System Components
| Component | Purpose |
|-----------|--------|
| [e.g., Web client] | [What it does — user-facing UI layer] |
| [e.g., API layer] | [Handles business logic and data access] |
| [e.g., Database] | [Persistent storage for [data categories]] |
| [e.g., Background processor] | [Handles async jobs — [examples]] |
| [e.g., File storage] | [Stores [asset types]] |

### Data Flow Description
[Describe how data moves through the system in plain English — no tool names required.]
[e.g., "User requests go through the web client to the API layer, which reads from and writes to the database. Background jobs are queued by the API and processed asynchronously. File uploads are stored separately and served via a CDN."]

### External Boundaries
[What external services or systems does this product depend on or integrate with? Describe by category, not by product name.]
[e.g., "Version control platform (read access to repos)", "Team messaging platform (send notifications)", "Payment processor (subscription billing)"]
```

---

### 12. API Specifications

```markdown
## API Specifications

#### [HTTP Method] /api/[endpoint]

**Purpose:** [One sentence]
**Authentication:** Required | Optional | None

**Request:**
```json
{
  "field_name": "string — description",
  "field_name_2": "number — description"
}
```

**Response (200):**
```json
{
  "id": "uuid",
  "field": "value"
}
```

**Error responses:**
- 400: [Missing/invalid input]
- 401: [Unauthorized]
- 404: [Resource not found]
- 429: [Rate limit exceeded]
```

---

### 13. UI/UX Requirements

```markdown
## UI/UX Requirements

### [Screen/View Name]

**Purpose:** [What the user is trying to accomplish here]

**Key user needs:**
- [What the user must be able to do]
- [What information they need to see]

**User flow:**
1. User [action]
2. System [observable response]
3. User [next action or outcome]

**States:**
- **Empty state:** [Not blank — provide context and a call to action]
- **Loading state:** [Skeleton / spinner]
- **Error state:** [Plain language message + recovery action]
- **Success state:** [Confirmation and next step]
```

---

### 14. Data Models

```markdown
## Data Models

### [Model Name]

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| id | UUID | Yes | PK, auto-generated | Primary identifier |
| [field_name] | string | Yes | max 200 chars | [Purpose] |
| [field_name_2] | integer | No | > 0 | [Purpose] |
| created_at | timestamp | Yes | UTC | Creation time |
| updated_at | timestamp | Yes | UTC | Last modification |
| deleted_at | timestamp | No | UTC, soft delete | Null = not deleted |

**Relationships:**
- [Model] has many [OtherModel] via [foreign key]
- [Model] belongs to [OtherModel]

**Indexes:**
- `[field_name]` — for [query type]
- `[field_1, field_2]` — for [composite query type]
```

---

### 15. Integration Points

```markdown
## Integration Points

### [Service Name]

**Purpose:** [Why this integration exists — user need it serves]
**Integration type:** REST API | Webhook | SDK | OAuth | Embed
**Data exchanged:**
- Inbound: [What we receive]
- Outbound: [What we send]
**Authentication:** [API key / OAuth token / etc.]
**Rate limits:** [Relevant limits and how we handle them]
**Fallback:** [What still works if this integration fails]
**Required for launch:** Yes | No
```

---

### 16. Edge Cases & Error Handling

```markdown
## Edge Cases & Error Handling

### Edge Cases

| Scenario | Expected Behavior | Priority |
|----------|-------------------|----------|
| [Empty form submission] | [Block; highlight required fields] | Must handle |
| [Network drops mid-upload] | [Resume on reconnect; notify user] | Should handle |
| [Concurrent edits to same record] | [Last-write-wins with conflict notification] | Should handle |

### Error Handling Strategy

- **User-facing errors:** Plain language + recovery action; never expose stack traces
- **System errors:** Log to [service]; alert on-call if error rate exceeds [threshold]
- **Validation:** Inline field-level messages; do not reset form on error
- **Retry logic:** Exponential backoff for transient failures; max [N] retries
- **Graceful degradation:** [What still works if [service X] is unavailable]
```

---

### 17. Risks & Mitigations

```markdown
## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| [e.g., API rate limits under high usage] | Medium | High | Cache data; exponential backoff; show stale data with timestamp |
| [e.g., Low activation if onboarding is complex] | High | High | Limit onboarding to ≤3 steps; run usability test pre-launch |
| [e.g., Key dependency delayed] | Low | High | Identify fallback or parallel path |

**Risk review cadence:** At each sprint planning session.
```

---

### 18. Testing Requirements

```markdown
## Testing Requirements

### Unit Tests
- [Component/Function] — [What critical logic to test]

### Integration Tests
- [API/Flow] — [What interaction to verify end-to-end]

### E2E Tests (Critical Paths)
- [User journey] — [e.g., "Sign up → complete onboarding → create first item"]

### Performance Tests
- [Scenario] — [e.g., "100 concurrent users; p95 API < 300ms"]

### Usability Tests (Pre-launch)
- [Persona + task] — [e.g., "New user completes onboarding without assistance"]
```

---

### 19. Release Criteria

```markdown
## Release Criteria

| Dimension | Criterion | Met? |
|-----------|-----------|------|
| **Functionality** | All Must-have features complete and verified | [ ] |
| **Usability** | Onboarding completion ≥ [X]% in usability test | [ ] |
| **Reliability** | Zero P0 bugs; crash rate < [0.1%] | [ ] |
| **Performance** | p95 API < [300ms]; page load < [2s] | [ ] |
| **Supportability** | Runbook exists; on-call set up; error alerting live | [ ] |

**Launch is blocked if Functionality or Reliability criteria are unmet.**
```

---

### 20. Launch Strategy

```markdown
## Launch Strategy

**Target launch date:** [Date or sprint milestone]

### Milestones
| Milestone | Date | Owner |
|-----------|------|-------|
| Alpha (internal) | [Date] | [Team] |
| Beta (limited users) | [Date] | [Team] |
| GA | [Date] | [Team] |

### Rollout
- **Initial audience:** [Who gets access first and why]
- **Approach:** [Phased / full / invite-only]
- **30/60/90 day checkpoints:** [What we measure to confirm we are on track]

### PRD Update Triggers
[Conditions that require updating this document — new user research, sprint retro findings, data signals, strategy shifts]
```

---

### 21. Open Questions

```markdown
## Open Questions

| # | Question | Context / Options | Owner | Decision Needed By |
|---|----------|-------------------|-------|--------------------|
| 1 | [e.g., Auto-close task when PR merges?] | [Option A: auto-close. Option B: prompt user.] | Product | Sprint 2 kickoff |
| 2 | [e.g., Pricing for teams > 10 members?] | [Per-seat vs flat rate] | CEO | Before public launch |
```

---

### 22. Implementation Notes for AI

**MANDATORY — provides implementation context for AI coding tools without prescribing specific technologies.**

```markdown
## Implementation Notes for AI

### Build Order
1. Data schema and persistence layer (always start here)
2. Authentication and authorization
3. Core API / business logic endpoints
4. Background processing and integrations
5. User interface components
6. End-to-end flows, edge cases, and polish

### Key Behavioral Constraints
[Rules the implementation must respect regardless of technology choice.]

- [e.g., "All timestamps must be stored in UTC and converted to the user's local timezone on display"]
- [e.g., "User-generated content must use soft deletes — records are flagged as deleted, never permanently removed"]
- [e.g., "Status changes must provide immediate UI feedback — do not wait for server confirmation before updating the interface"]
- [e.g., "All user-facing record identifiers should be human-readable (e.g., TASK-001), not internal database IDs"]

### Data Integrity Rules
[Business rules the data layer must enforce.]

- [e.g., "A task must always belong to exactly one project; orphaned tasks are not permitted"]
- [e.g., "Changing a subscription tier must log the previous tier for audit purposes"]

### Security Requirements
- [e.g., "All API endpoints that return user data must verify the requesting user has permission to see that specific record"]
- [e.g., "File uploads must be scanned before being made accessible to other users"]

### Common Pitfalls to Avoid
- [e.g., "Do not expose database row IDs in public URLs — use slugs or opaque identifiers"]
- [e.g., "Pagination must be cursor-based, not offset-based, to handle real-time data correctly"]
```

---

### 23. Appendix

```markdown
## Appendix

### Glossary
| Term | Definition |
|------|-----------|
| [Term] | [Product/domain-specific definition] |

### Research & Evidence
- [Links or summaries of customer interviews, surveys, analytics that informed this PRD]

### Competitive Notes
- [Key differentiators vs. Competitor A, Competitor B]

### Version History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [Date] | [Author] | Initial draft |
```

---

## Usage Notes

**The PRD does NOT define:** Visual design specifics, exact UI implementation, specific frameworks or libraries, programming languages, or hosting providers — those belong in a technical design document. Technology choices change; the PRD's functional and non-functional requirements should remain stable.

**The PRD DOES define:** What users need to accomplish, why it matters, how success is measured, what is in scope, what is not in scope, and the architectural constraints the implementation must satisfy.

**Living document:** Update when user research reveals new insights, sprint reviews surface constraints, or data shows assumptions were wrong. Add a changelog entry every time.
