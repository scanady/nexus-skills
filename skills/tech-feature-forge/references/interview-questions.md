# Interview Questions

## PM Hat Questions

Focus on user value and business goals.

| Area | Questions |
|------|-----------|
| **Problem** | What problem does this solve? Who experiences this problem? How often? |
| **Users** | Who are the target users? What are their goals? Technical level? |
| **Value** | How will users benefit? What's the business value? ROI? |
| **Scope** | What's in scope? What's explicitly out of scope? MVP vs full version? |
| **Success** | How will we measure success? Key metrics? |
| **Priority** | Is this a must-have, should-have, or nice-to-have? |

### Example PM Questions

```markdown
For a "User Export" feature:
- Who needs to export data and why?
- What format do they need (CSV, JSON, Excel)?
- How much data? 100 rows or 1 million?
- Is this for compliance (GDPR) or convenience?
- How often will this be used?
- What's the deadline?
```

## Dev Hat Questions

Focus on technical feasibility and edge cases.

| Area | Questions |
|------|-----------|
| **Integration** | What systems does this touch? APIs, databases, services? |
| **Security** | Authentication required? Data sensitivity (PII, PCI)? |
| **Performance** | Expected load? Response time requirements? Async OK? |
| **Edge Cases** | What happens when X fails? Empty states? Limits? |
| **Data** | What's stored? Retention period? Backup needs? |
| **Dependencies** | External services? Rate limits? Costs? |

### Example Dev Questions

```markdown
For a "User Export" feature:
- What fields to include? Are any sensitive (passwords, tokens)?
- Max export size? Need streaming or background job?
- Should include soft-deleted records?
- What happens if export fails midway?
- File retention - how long to keep generated files?
- Need progress indicator for large exports?
```

## Structured Questioning

Use structured options when questions have a finite set of likely answers. Use open-ended follow-up when answers are unbounded.

If the host platform offers a structured questioning capability, use it. Otherwise, present a compact enumerated choice list and ask the stakeholder to pick from it.

### When to Use Structured Options

| Question Pattern | Example | Options Style |
|-----------------|---------|---------------|
| Priority/ranking | "Is this must-have or nice-to-have?" | Single select: Must-have, Should-have, Nice-to-have |
| Format selection | "What export format?" | Multi-select: CSV, JSON, Excel, PDF |
| Scope decisions | "MVP or full version?" | Single select: MVP, Full, Phased |
| Yes/No with nuance | "Auth required?" | Single select: Public, Authenticated, Role-based |

### When to Use Open-Ended

- "Describe the user journey in your own words"
- "What problem does this solve?"
- "Walk me through the workflow"

### Example: Structured Elicitation

For a "User Export" feature, batch related choices:

**Question 1** (header: "Export scope"):
"What data should users be able to export?"
Options: "Own data only", "Team data", "Organization-wide", multi-select enabled

**Question 2** (header: "Format"):
"Which export formats should be supported?"
Options: "CSV", "JSON", "Excel (.xlsx)", "PDF", multi-select enabled

**Question 3** (header: "Priority"):
"How critical is this feature?"
Options: "Must-have (blocking)", "Should-have (important)", "Nice-to-have (future)"

---

## Interview Flow

### Phase 1: Discovery
Use open-ended questions to understand the problem space:
1. "Tell me about this feature in your own words"
2. "What problem are we solving?"

Then use structured options to narrow down:
- Target users (single select from identified personas)
- Usage frequency (Daily, Weekly, Monthly, Rarely)
- Priority (Must-have, Should-have, Nice-to-have)

### Phase 2: Details
Use structured options for scope and constraint decisions:
- Scope: MVP vs Full vs Phased (single select)
- Key capabilities (multi-select from discovered items)

Then open-ended: "Walk me through the user journey"

### Phase 3: Edge Cases
Use structured options for technical trade-offs:
- Error handling approach (Retry, Fail fast, Queue, Notify)
- Data limits (multi-select thresholds)

Then open-ended: "What happens when [X] fails?"

### Phase 4: Validation
Present spec summary, then use structured options:
- "Does this capture your requirements?" (Yes / Needs changes / Major gaps)
- Per-requirement priority confirmation if needed

## Multi-Agent Pre-Discovery

For features spanning multiple domains, do brief pre-discovery **before** starting the interview. This front-loads technical context so the interview focuses on decisions rather than exploration.

### Pattern: Parallel Domain Discovery

```
User request: "I need a feature that does X"

Before interview, gather facts in parallel where possible:
- Review the relevant architecture, APIs, data models, and integration points
- Review security, privacy, and authorization constraints
- Review existing implementation patterns related to the feature

Collect findings -> Use them to inform interview questions
```

This ensures the Feature Forge interview starts with concrete technical context rather than assumptions.

---

## Quick Reference

| Phase | Focus | Tool |
|-------|-------|------|
| Pre-Discovery | Technical context | Parallel exploration |
| Discovery | Problem, users, value | Open-ended -> structured options |
| Details | Journey, scope, constraints | Structured options -> open-ended |
| Edge Cases | Failures, limits, security | Structured options -> open-ended |
| Validation | Summary, gaps | Structured options |
