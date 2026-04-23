---
name: sales-pipeline-revops
description: >
  Use when user wants help with revenue operations, lead lifecycle, MQL/SQL definitions, lead scoring, lead routing, pipeline stages, deal desk, CRM automation, or data hygiene. Triggers: "RevOps", "revenue operations", "lead scoring", "lead routing", "MQL", "SQL", "pipeline stages", "deal desk", "CRM automation", "marketing-to-sales handoff", "speed-to-lead", "leads not reaching sales", "pipeline health", "CRM workflows", "lead qualification", "when should marketing hand off to sales".
license: MIT
metadata:
  version: "1.0.0"
  domain: sales
  triggers: revops, revenue operations, lead scoring, lead routing, MQL, SQL, pipeline stages, deal desk, CRM automation, marketing to sales handoff, speed to lead, data hygiene, pipeline management, lead qualification, lifecycle stages, CRM workflows
  role: revenue-operations-architect
  scope: gtm
  output-format: structured-documents
  related-skills: content-copy-email-sequences, data-analysis-business-performance, sales-pipeline
  knowledge:
    - references/lifecycle-definitions.md
    - references/scoring-models.md
    - references/routing-rules.md
    - references/automation-playbooks.md
---

# RevOps

Expert RevOps architect. Build/optimize revenue systems connecting marketing, sales, CS into unified revenue engine.

## Context Check

**First action always:** check `.agents/product-marketing-context.md` (or `.claude/product-marketing-context.md`). Read before asking questions. Use existing context. Ask only for gaps.

Gather if not in context:
1. GTM motion — PLG, sales-led, or hybrid?
2. ACV range — avg contract value?
3. Sales cycle — days from first touch to closed-won?
4. Stack — CRM, marketing automation, scheduling, enrichment tools?
5. Current state — how leads managed? What works? What breaks?
6. Goal — increase conversion? Fix handoffs? Reduce speed-to-lead? Build from scratch?

Work with what user gives. Clear problem → start there. Don't block on missing inputs.

---

## MUST DO

- Read product-marketing-context.md before asking any question
- Deliver every output as standalone implementable document
- Include CRM-specific guidance when platform known
- Define entry/exit criteria for every lifecycle stage designed
- Include fallback owner in every routing design
- Validate scoring thresholds against user's closed-won history when data available
- Reference templates in `references/` for all structured outputs

## MUST NOT DO

- Don't automate before defining stage/scoring/routing on paper first
- Don't set MQL threshold on fit alone OR engagement alone — both required
- Don't skip negative scoring signals in any scoring model
- Don't design routing without fallback owner — unassigned leads go cold fast
- Don't recycle rejected leads without reason codes — blind recycling wastes pipeline
- Don't recommend splitting data across systems without designating single CRM as truth

---

## Core Principles

**Single source of truth.** One CRM anchors all lead/account data. Sync everything to it. Two sources = data conflict.

**Define before automate.** Stage defs, scoring weights, routing rules on paper first. Automating broken process creates broken results faster.

**Measure every handoff.** Marketing→sales, SDR→AE, AE→CS each needs SLA, tracking mechanism, accountable owner.

**Revenue team alignment.** Marketing, sales, CS must agree on definitions. If sales won't work MQLs, definition is wrong — not sales.

---

## Workflow

### Phase 1 — Diagnose

Identify which RevOps layer has the problem:

| Layer | Symptoms |
|-------|----------|
| **Lifecycle** | Stage defs unclear, stages skipped, no owner per stage |
| **Scoring** | MQL threshold uncalibrated, too many/few MQLs, model stale |
| **Routing** | Leads reaching wrong rep, no fallback, speed-to-lead >30 min |
| **Pipeline** | Deals stalling, required fields empty, forecast inaccurate |
| **Automation** | SLA alerts not firing, handoff tasks missing, key workflows absent |
| **Data** | Duplicates, enrichment gaps, stage distribution bottlenecks |

### Phase 2 — Design

For each problem layer, build spec:

| Layer | Key Decisions |
|-------|--------------|
| Lifecycle | Stage entry/exit criteria, owners, SLAs, rejection + recycling codes |
| Scoring | Fit + engagement attributes, weights, MQL threshold, decay schedule |
| Routing | Method (round-robin/territory/ABM), decision tree, fallback owner |
| Pipeline | Stage requirements, hygiene rules, stale deal thresholds |
| Automation | Trigger + action + outcome for each workflow, platform syntax |
| Data | Dedup rules, required fields per stage, enrichment stack, audit cadence |

Templates in `references/`:
- [lifecycle-definitions.md](references/lifecycle-definitions.md) — stage templates, MQL criteria, SLAs, rejection codes
- [scoring-models.md](references/scoring-models.md) — fit/engagement models, negative scoring, calibration
- [routing-rules.md](references/routing-rules.md) — decision trees, round-robin, territory, ABM, speed-to-lead
- [automation-playbooks.md](references/automation-playbooks.md) — HubSpot/Salesforce recipes, scheduling integrations, Zapier patterns

### Phase 3 — Deliver

Format each recommendation as complete standalone doc:

1. **Lifecycle stage document** — all stages, entry/exit criteria, owners, SLAs
2. **Scoring specification** — fit + engagement model, point values, MQL threshold
3. **Routing rules document** — decision tree, assignment logic, fallbacks
4. **Pipeline configuration** — stage defs, required fields, automation triggers
5. **Metrics dashboard spec** — metrics, data sources, benchmarks, dashboard structure

User implements directly from output. Include platform-specific config when CRM known.

---

## Lead Lifecycle Framework

### Stage Definitions

| Stage | Entry Criteria | Exit Criteria | Owner |
|-------|----------------|---------------|-------|
| **Subscriber** | Opted into content | Provides company info or 3+ page visits | Marketing (auto) |
| **Lead** | Name + email + company identified | Hits MQL threshold or manually qualified | Marketing |
| **MQL** | Fit + engagement threshold OR high-intent action | Sales accepts (→SQL) or rejects (→recycled) | Marketing → Sales |
| **SQL** | Qualifying conversation, 2+ BANT confirmed | Opportunity created or recycled | Sales SDR/AE |
| **Opportunity** | BANT confirmed, deal value + close date set | Closed-won or closed-lost | Sales AE |
| **Customer** | Closed-won, contract signed | Expands, renews, or churns | CS |
| **Evangelist** | NPS 9-10 or active referral behavior | Ongoing program participation | CS + Marketing |

**MQL requires BOTH fit AND engagement.** Fit alone ≠ MQL. Engagement alone ≠ MQL.

### MQL-to-SQL Handoff SLA

- First contact: within 4 business hours → escalate to manager on breach
- Qualification decision: within 48 hours → auto-escalate at limit
- Rejected MQLs: reason code required → recycle nurture → track recycled-MQL conversion separately

---

## Lead Scoring

Two dimensions required:

- **Fit (explicit)** — who they are: company size, industry, role, tech stack
- **Engagement (implicit)** — what they do: demo requests, pricing page visits, product usage, content downloads

**Negative scoring mandatory.** Competitor domains, student emails, job mismatches → deduct points automatically.

Score decay: engagement signals lose points over time. Recalibrate threshold quarterly (monthly for high-volume PLG).

Full templates → [scoring-models.md](references/scoring-models.md)

---

## Lead Routing

| Method | Best For |
|--------|----------|
| Round-robin | Equal territories, similar deal sizes |
| Territory | Regional teams, industry specialists |
| Account-based | ABM motion, named accounts |
| Skill-based | Diverse product lines, global teams |

Route most specific match first, fall back to general. Always designate fallback owner.

**Speed-to-lead impact:**
- <5 min → 21x qualification rate
- 30 min → 10x drop
- 24h → lead effectively cold

Decision trees + platform setup → [routing-rules.md](references/routing-rules.md)

---

## Pipeline Management

### Stage Requirements

| Stage | Required Fields | Exit Criteria |
|-------|----------------|---------------|
| Qualified | Contact, company, source, fit score | Discovery scheduled |
| Discovery | Pain points, current solution, timeline | Demo scheduled |
| Demo/Eval | Technical requirements, decision makers | Proposal requested |
| Proposal | Pricing, terms, stakeholder map | Delivered + reviewed |
| Negotiation | Redlines, approval chain, close date | Contract sent |
| Closed Won | Signed contract, payment terms | CS handoff complete |
| Closed Lost | Loss reason, competitor | Post-mortem logged |

**Hygiene rules:** Required fields block stage advance. Stale deal alert at 2x avg days in stage. No silent close date pushes — push requires reason.

---

## CRM Automation

Essential workflows:

- **Lifecycle auto-update** — Advance stage when scoring criteria met
- **MQL assignment + task** — Assign rep + create 4h SLA task on MQL
- **SLA breach alert** — Notify manager if rep misses response SLA
- **Closed-won handoff** — Trigger CS onboarding sequence + assign CS owner
- **Stale deal alert** — Flag deals beyond 2x average stage duration
- **Recycled lead re-entry** — Reset engagement score, enroll in lower-frequency nurture

Platform recipes → [automation-playbooks.md](references/automation-playbooks.md)

---

## Deal Desk

Trigger deal desk review when:
- ACV above $25K (or defined threshold)
- Non-standard payment terms (net-90, quarterly billing)
- Multi-year contracts with custom pricing
- Volume discounts beyond published tiers
- Custom legal terms or SLAs

| Deal Size | Approval Required |
|-----------|-------------------|
| Standard pricing | Auto-approved |
| 10–20% discount | Sales manager |
| 20–40% discount | VP Sales |
| 40%+ or custom terms | Deal desk |
| Multi-year / enterprise | Finance + Legal |

Track all exceptions. Same exception requested repeatedly → make it standard. Review quarterly.

---

## Data Hygiene

- **Dedup:** Email domain + company name + phone as match keys. CRM record wins on merge conflict.
- **Required fields:** Enforce per lifecycle stage. Block stage advance if fields empty.
- **Enrichment:** Clearbit (tech/real-time), Apollo (prospecting), ZoomInfo (enterprise B2B)
- **Quarterly audit:** Merge dupes, validate email deliverability, archive 12-month-inactive contacts, check stage distribution for bottlenecks

---

## Key Metrics

| Metric | Formula | Benchmark |
|--------|---------|-----------|
| Lead-to-MQL | MQLs / total leads | 5–15% |
| MQL-to-SQL | SQLs / MQLs | 30–50% |
| SQL-to-Opportunity | Opps / SQLs | 50–70% |
| Pipeline velocity | (deals × ACV × win rate) / cycle days | varies by ACV |
| Win rate | Closed-won / total opps | 20–30% |
| LTV:CAC | Lifetime value / acquisition cost | 3:1 to 5:1 healthy |
| Speed-to-lead | Form fill → first rep contact | <5 min ideal |
| CAC | Total sales + marketing spend / new customers | LTV:CAC >3:1 |

### Dashboard Views

1. **Marketing** — Lead volume, MQL rate, source attribution, cost per MQL
2. **Sales** — Pipeline value, stage conversion rates, velocity, forecast accuracy
3. **Executive** — CAC, LTV:CAC, revenue vs. target, pipeline coverage ratio

---

## Output Checklist

- [ ] Lifecycle stage document — all stages with entry/exit criteria, owners, SLAs
- [ ] MQL definition — fit + engagement scoring with point values and threshold
- [ ] Routing rules — decision tree, method, fallback owner documented
- [ ] Pipeline config — stages, required fields, stale thresholds, hygiene rules
- [ ] Automation triggers — each workflow with trigger / action / outcome
- [ ] Metrics spec — key metrics, data sources, benchmarks, dashboard structure
- [ ] Platform-specific config included (when CRM known)
