# PRD Templates

Four templates. Match scope → pick template. See routing table in SKILL.md.

---

## Standard PRD

**Use for:** Major features, 6+ weeks, cross-functional alignment required.

### 1. Executive Summary

| Field | Content |
|---|---|
| Problem | 2–3 sentences |
| Solution | 2–3 sentences |
| Business impact | 3 bullets |
| Timeline | Key milestones |
| Resources | Team + budget |
| Success metrics | 3–5 KPIs |

### 2. Problem Definition

**Customer problem**
- Who: Target persona(s)
- What: Specific problem
- When/Where: Context and frequency
- Why: Root cause
- Impact: Cost of not solving

**Market opportunity**
- Market size: TAM / SAM / SOM
- Competition: Existing solutions and gaps
- Timing: Why now

**Business case**
- Revenue or retention impact
- Cost savings / efficiency gains
- Strategic fit
- Risk of inaction

### 3. Solution

**Proposed solution:** What we're building and why it solves the problem.

**In scope:**
- Feature 1 — [priority]
- Feature 2 — [priority]

**Out of scope:** *(required — explicitly list what is excluded)*
- Not doing X because Y
- Future consideration: Z

**MVP definition:**
- Core features: minimum viable set
- Success criteria: definition of "working"
- Learning goals: what we validate at launch

### 4. User Stories & Requirements

**User story format:**
```
As a [persona], I want to [action] so that [outcome].
Acceptance criteria:
- [ ] Criterion 1
- [ ] Criterion 2
```

**Functional requirements:**
| ID | Requirement | Priority | Notes |
|---|---|---|---|
| FR1 | User can... | P0 | MVP-critical |
| FR2 | System should... | P1 | Important |

**Non-functional requirements:**
- Performance: response time targets
- Scalability: user/data growth targets
- Security: auth, authorization, PII handling
- Reliability: uptime, error rate targets
- Compliance: regulatory requirements

### 5. Design & UX

- Design principles: 3 bullets
- Figma / wireframe links
- Key flows and edge cases
- Information architecture

### 6. Technical Specs

- Architecture overview + key integration points
- API design: endpoints, auth, rate limits
- Data model: key entities and relationships
- Security: encryption, PII, access control

### 7. Go-to-Market

- Soft launch: beta users + timeline
- Full launch: channels + timeline
- Support: docs, training, escalation path
- Pricing: model + competitive rationale

### 8. Risks

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Technical debt | Medium | High | Reserve 20% capacity for refactoring |
| Adoption | Low | High | Beta program with feedback loop |
| Scope creep | High | Medium | Weekly stakeholder reviews |

### 9. Timeline

| Milestone | Date | Deliverables | Success Criteria |
|---|---|---|---|
| Design complete | Week 2 | Mockups | Stakeholder approval |
| MVP development | Week 6 | Core features | All P0s done |
| Beta | Week 8 | Limited release | 100 beta users |
| Full launch | Week 12 | GA | <1% error rate |

### 10. Team & Budget

| Role | Name | Allocation |
|---|---|---|
| PM | [Name] | 100% |
| Engineering lead | [Name] | 100% |
| Designer | [Name] | 50% |
| Engineers | X FTEs | |

Budget: Dev $X · Infra $X · Marketing $X · Total $X

### 11. Appendix

Research data · competitive analysis · architecture diagrams · legal/compliance docs

---

## One-Page PRD

**Use for:** Mid-size features, 2–5 weeks. Fast alignment with single-page constraint.

**[Feature Name]** | Date: | Author: | Status: Draft / In Review / Approved

**Problem** — *What are we solving? For whom?*
[2–3 sentences]

**Solution** — *What are we building?*
[2–3 sentences]

**Why now?**
- Driver 1
- Driver 2

**Success metrics:**
| Metric | Current | Target |
|---|---|---|
| KPI 1 | X | Y |
| KPI 2 | X | Y |

**In scope:** Feature A, Feature B, Feature C
**Out of scope:** *(required)* Feature X, Feature Y

**User flow:** Step 1 → Step 2 → Step 3 → Success

**Risks:**
1. Risk 1 → Mitigation
2. Risk 2 → Mitigation

**Timeline:** Design: Wk 1–2 · Dev: Wk 3–6 · QA: Wk 7 · Launch: Wk 8

**Resources:** Engineering: X devs · Design: X · QA: X

**Open questions:**
1. Question 1?

---

## Agile Epic

**Use for:** Sprint-based delivery. Pairs with ticket backlog.

**Epic: [Name]** | ID: EPIC-XXX | Theme: [Theme] | Quarter: QX YYYY | Status: Discovery / In Progress / Complete

**Problem:** [2–3 sentences]

**Goals:**
1. Objective 1
2. Objective 2

**Success metrics:**
- Metric 1: Target
- Metric 2: Target

**User stories:**
| Story ID | Title | Priority | Points | Status |
|---|---|---|---|---|
| US-001 | As a... | P0 | 5 | To Do |

**Dependencies:**
- Dep 1: Team/System
- Dep 2: Team/System

**Acceptance criteria:**
- [ ] All P0 stories complete
- [ ] Performance targets met
- [ ] Security review passed
- [ ] Docs updated

---

## Feature Brief

**Use for:** Exploration / pre-PRD. Hypothesis-driven. 1-week time horizon.

**Feature: [Name]**

**Context:** Why are we considering this?

**Hypothesis:**
> We believe that [building this] for [user] will [outcome].
> Confirmed when [measurable metric].

**Problem signal:** What evidence (interviews, data) prompted this?

**Proposed scope:** Smallest thing we could build to test the hypothesis.

**Out of scope:** *(required)*

**Learning goals:** What do we need to know before committing to a full PRD?

**Success / failure definition:**
- Success: [specific observable outcome]
- Failure / pivot trigger: [what causes us to stop or change direction]

**Time box:** [Date] — if no signal by this date, revisit.

---

## Prioritization Reference

### RICE Formula

```
score = (Reach × Impact × Confidence%) / Effort_months

Impact:     massive=3.0 · high=2.0 · medium=1.0 · low=0.5 · minimal=0.25
Confidence: high=100% · medium=80% · low=50%
Effort:     xl=13 · l=8 · m=5 · s=3 · xs=1  (person-months)
```

### Portfolio Balance

```
             Low Effort     High Effort
High Value   QUICK WINS     BIG BETS
             Prioritize     Strategic
Low Value    FILL-INS       TIME SINKS
             Maybe          Avoid
```

### MoSCoW

| Label | Meaning |
|---|---|
| Must Have | Critical for launch |
| Should Have | Important, not blocking |
| Could Have | Nice to have |
| Won't Have | Out of scope |

---

## Discovery Reference

### Interview Guide (30 min)

| Phase | Duration | Focus |
|---|---|---|
| Context | 5 min | Role, workflow, tools used |
| Problem exploration | 15 min | Pain points, frequency, workarounds |
| Solution validation | 7 min | Reaction to concepts, value perception |
| Wrap-up | 3 min | Open thoughts, referrals, follow-up permission |

### Hypothesis Template

```
We believe that [building this feature]
for [these users]
will [achieve this outcome].
We'll know we're right when [metric].
```

### Opportunity Solution Tree

```
Outcome
├── Opportunity 1
│   ├── Solution A
│   └── Solution B
└── Opportunity 2
    ├── Solution C
    └── Solution D
```

### Feature Success Metrics

| Metric | Definition |
|---|---|
| Adoption | % users using feature |
| Frequency | Uses per user per time period |
| Depth | % of feature capability used |
| Retention | Continued usage over time |
| Satisfaction | NPS / CSAT for feature |
