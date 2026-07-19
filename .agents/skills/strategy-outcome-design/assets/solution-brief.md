# Solution Brief Template

Use this structure adaptively. Do not include empty sections or placeholder tables in the final brief. A compact brief is the default. Expand the detailed review only when it adds decision value.

When saving the brief as a Markdown file, include this YAML frontmatter:

```yaml
---
artifact_type: solution-brief
schema_version: "1.0"
title: ""
status: draft
maturity: unframed
disposition: continue-discovery
outcome_patterns: []
updated: YYYY-MM-DD
---
```

Allowed values:

- `status`: `draft`, `reviewed`, `accepted`, `superseded`
- `maturity`: `unframed`, `framed`, `designed`, `downstream-ready`
- `disposition`: `continue-discovery`, `validate-first`, `proceed-to-downstream-planning`, `accepted-with-known-gaps`

# [Solution Brief Title]

## 1. Handoff summary

**Desired outcome:**  
**Primary beneficiary:**  
**Why it matters:**  
**Success condition:**  
**Experience or operating conditions for success:**

**Time horizon:**  
**Selected design or current design hypothesis:**  
**Maturity:**  
**Disposition:**  
**Most consequential unresolved issue:**  
**Recommended next artifact:**  
**Smallest meaningful next action:**

## 2. Outcome and boundaries

### Desired future state

Describe what should be meaningfully different when the outcome is achieved.

### Outcome pattern

Identify the primary and supporting patterns: create, improve, reduce, learn, decide, change behavior, maintain, or recover.

### Beneficiaries and affected parties

| Party | Intended benefit, cost, risk, or required behavior change |
|---|---|
| | |

### Value and opportunity cost

Explain why this outcome is worth pursuing and what may need to be delayed, reduced, or abandoned.

### Scope, time horizon, and locus of control

**In scope:**  
**Out of scope:**  
**Time horizon:**  
**Controllable:**  
**Influenceable:**  
**Outside control:**

### Anti-outcomes

State what must not happen or what valued conditions must be protected.

### Outcome hierarchy

Use only the relevant layers: impact, beneficiary, experience, capability, operational, and guardrail outcomes.

| Layer | Outcome statement | Evidence that it is succeeding |
|---|---|---|
| | | |

## 3. Success and evidence

### Success model

| Measure or condition | Type | Baseline | Target or threshold | Evaluation period | Evidence source | Limitation or gaming risk |
|---|---|---:|---:|---|---|---|
| | Outcome / Leading / Proxy / Guardrail | | | | | |

### Acceptance conditions

State the minimum combination of conditions required to call the outcome successful.

### Experience and operating conditions

Use when success depends on how a service, workflow, product, or interaction feels, behaves, degrades, or recovers in real use.

| Condition or event | Required behavior | Threshold or quality signal | Evidence source | Failure or recovery expectation |
|---|---|---|---|---|
| | | | | |

### Continue, adjust, pivot, or stop conditions

## 4. Current reality

### Current state and prior attempts

### Evidence register

| Claim | Classification | Evidence or source | Confidence | Design implication |
|---|---|---|---|---|
| | Fact / Interpretation / Assumption / Unknown | | High / Medium / Low | |

### Constraints, resources, and dependencies

| Item | Fixed, negotiable, or assumed | Criticality | Design implication | Owner or source |
|---|---|---|---|---|
| | | | | |

### Ownership and stakeholder dynamics

Identify decision owner, contributors, affected parties, incentives, resistance, and accountability where relevant.

## 5. Causal design

### Backward chain

**Outcome -> evidence -> necessary conditions -> behavior or system changes -> selected mechanism**

### Theory of change

Explain why the proposed mechanism should create the necessary changes and where causality remains uncertain.

### Alternatives considered

| Alternative | Distinct mechanism | Advantages | Limitations and risks | Evidence needed | Disposition |
|---|---|---|---|---|---|
| | | | | | Selected / Rejected / Deferred |

Include doing nothing, delaying, or simplifying when credible.

### Selected design or design hypothesis

### Smallest sufficient design

Explain what can be removed, delayed, or tested without losing the essential causal mechanism.

## 6. Assumptions, feasibility, and risk

### Priority assumptions and unknowns

| Assumption or unknown | Confidence | Impact if wrong | Could change recommendation? | Validation or mitigation |
|---|---|---|---|---|
| | High / Medium / Low | | Yes / No | |

### Highest-value uncertainty to reduce

### Feasibility assessment

Address time, capacity, money, skills, authority, data, technology, regulation, ethics, privacy, and other material constraints.

### Risks, trade-offs, guardrails, and reversibility

| Risk or trade-off | Likelihood | Impact | Guardrail or mitigation | Owner or decision point | Reversibility or recovery |
|---|---|---|---|---|---|
| | | | | | |

## 7. Progress and learning design

| Milestone or necessary condition | Evidence of progress | Decision enabled | Review point |
|---|---|---|---|
| | | | |

### Learning loop

Describe what will be reviewed, what evidence will update the design, and when continuation, adjustment, pivot, or stopping decisions occur.

## 8. Decisions and rationale

| Decision | Rationale | Evidence used | Challenge or counterargument | Residual uncertainty |
|---|---|---|---|---|
| | | | | |

### Rejected or deferred alternatives

### Accepted trade-offs and disagreements

## 9. Readiness assessment

### Quality assessment

Include only applicable dimensions.

| Dimension | Rating | Evidence or gap | Blocker |
|---|---|---|---|
| | Weak / Developing / Strong | | Yes / No |

### Maturity and disposition rationale

### Blocking issues

### Downstream contract

**Recommended next artifact:**  
**The downstream artifact may assume:**  
**The downstream artifact must still resolve:**  
**Qualified review required:**

## 10. Change history

**Version:**  
**Date:**  
**Participants:**  
**Status:** Draft / Reviewed / Accepted / Superseded  
**Change summary:**