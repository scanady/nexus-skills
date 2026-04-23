# Statistical Persona Template

This template produces data-driven segment personas grounded in cluster analysis. Every field must be populated with data, documented assumptions, or explicitly marked as "Data gap — requires [specific action]."

**Critical rule:** Personas are statistical profiles. Never use fictional names, stock photo descriptions, or marketing-team-invented archetypes.

---

## Persona Template

```markdown
## Segment [N]: [Descriptive Label]

> **One-sentence summary:** [What defines this segment in behavioral and value terms]

### Size & Value
| Metric | Value | Source |
|--------|-------|--------|
| % of customer base | X% | [data source] |
| # of customers/accounts | X,XXX | [data source] |
| Revenue contribution | X% of total ($X.XM) | [data source] |
| Avg revenue per account (ARPA) | $X,XXX/yr | [data source] |
| YoY growth rate | X% | [data source or assumption] |
| Avg customer lifetime | X.X years | [data source] |
| Lifetime value (LTV) | $XX,XXX | [calculated: ARPA × lifetime × margin] |

### Core Job-to-be-Done
**Primary job:** [Specific outcome they hire your product to achieve]
**Context:** [When and where this job arises — the triggering situation]
**Success metric:** [How they measure whether the job is done well]
**Alternative solutions:** [What they would use if your product didn't exist]

### Decision Criteria (Ranked)
| Rank | Criterion | Evidence | Frequency |
|------|-----------|----------|-----------|
| 1 | [Top criterion] | [Source: win/loss, survey, interviews] | Cited by X% |
| 2 | [Second criterion] | [Source] | Cited by X% |
| 3 | [Third criterion] | [Source] | Cited by X% |
| 4 | [Fourth criterion] | [Source] | Cited by X% |
| 5 | [Fifth criterion] | [Source] | Cited by X% |

### Preferred Channels
| Stage | Channel | Engagement Rate | Evidence |
|-------|---------|----------------|----------|
| Discovery | [Channel] | X% | [Source] |
| Research | [Channel] | X% | [Source] |
| Evaluation | [Channel] | X% | [Source] |
| Purchase | [Channel] | X% | [Source] |
| Ongoing engagement | [Channel] | X% | [Source] |

### Top Objections
| Rank | Objection | Frequency | Best Counter |
|------|-----------|-----------|-------------|
| 1 | "[Exact language they use]" | X% of lost deals | [Proven response] |
| 2 | "[Exact language]" | X% | [Proven response] |
| 3 | "[Exact language]" | X% | [Proven response] |

### Trigger Events
Events that initiate a purchase cycle for this segment:

| Trigger | Signal Source | Lead Time | Confidence |
|---------|-------------|-----------|------------|
| [Specific event] | [Where you can detect this] | [How long before purchase] | High/Med/Low |
| [Specific event] | [Detection source] | [Lead time] | High/Med/Low |
| [Specific event] | [Detection source] | [Lead time] | High/Med/Low |

### Behavioral Signature
Quantitative patterns that distinguish this segment:

| Metric | This Segment | Overall Avg | Variance |
|--------|-------------|-------------|----------|
| [Usage metric 1] | X.X | Y.Y | ±Z% |
| [Usage metric 2] | X.X | Y.Y | ±Z% |
| [Engagement metric] | X.X | Y.Y | ±Z% |
| [Transaction metric] | X.X | Y.Y | ±Z% |

### Churn Risk Factors
Leading indicators of attrition specific to this segment:

| Indicator | Threshold | Lead Time | Action |
|-----------|-----------|-----------|--------|
| [Metric drop] | [Specific threshold] | [Days before churn] | [Intervention] |
| [Behavior change] | [Threshold] | [Days] | [Intervention] |

### Expansion Signals
Leading indicators of upsell/cross-sell readiness:

| Signal | Threshold | Next Best Offer | Confidence |
|--------|-----------|----------------|------------|
| [Usage signal] | [Threshold] | [Product/tier] | High/Med/Low |
| [Behavioral signal] | [Threshold] | [Product/tier] | High/Med/Low |

### Buying Committee (B2B only)
| Role | Involvement | Priority | Messaging Angle |
|------|------------|----------|----------------|
| [Title/function] | Champion / Influencer / Decision Maker / Blocker | [Their top criterion] | [What resonates with them] |
| [Title/function] | [Role] | [Criterion] | [Angle] |

### Segment-Specific Messaging
**Value proposition for this segment:** [One sentence — their language, their outcome]
**Proof points that resonate:** [Specific evidence types that move this segment]
**Competitive positioning:** [How to position against their most-considered alternative]
```

---

## Filled Example: B2B SaaS

```markdown
## Segment 3: High-Growth Mid-Market Consolidators

> **One-sentence summary:** Mid-market companies (200-1,000 employees) in rapid scaling mode that are consolidating their tech stack to reduce operational complexity and prepare for enterprise-grade operations.

### Size & Value
| Metric | Value | Source |
|--------|-------|--------|
| % of customer base | 22% | CRM analysis, Q4 2024 |
| # of accounts | 1,340 | CRM count, active accounts |
| Revenue contribution | 38% of total ($12.4M ARR) | Revenue reporting |
| Avg revenue per account (ARPA) | $9,250/yr | Revenue / account count |
| YoY growth rate | 18% | Cohort comparison Q4 2023 vs Q4 2024 |
| Avg customer lifetime | 3.8 years | Survival analysis, n=890 |
| Lifetime value (LTV) | $28,120 | ARPA × lifetime × 80% margin |

### Core Job-to-be-Done
**Primary job:** Replace 3-5 point solutions with a single platform that scales with the company through Series B to IPO readiness.
**Context:** Arises when operational complexity creates visible drag — typically after headcount crosses 200 and existing tools require dedicated admin time.
**Success metric:** Reduce tool count by 50%+, eliminate manual data reconciliation, pass SOC 2 audit without custom workarounds.
**Alternative solutions:** Hiring a full-time ops/integration engineer ($120K+/yr), building custom integrations, or maintaining the multi-tool status quo with increasing admin overhead.

### Decision Criteria (Ranked)
| Rank | Criterion | Evidence | Frequency |
|------|-----------|----------|-----------|
| 1 | Native integration depth (API + pre-built connectors) | Win/loss analysis, n=45 | Cited by 71% |
| 2 | Time-to-value (<30 days to full deployment) | Customer interviews, n=22 | Cited by 62% |
| 3 | SOC 2 / compliance readiness out-of-box | Sales call transcripts, n=38 | Cited by 54% |
| 4 | Per-seat pricing that scales sub-linearly | Pricing page analytics + deal desk data | Cited by 41% |
| 5 | Self-serve admin (no dedicated admin required) | NPS verbatims, n=180 | Cited by 33% |

### Preferred Channels
| Stage | Channel | Engagement Rate | Evidence |
|-------|---------|----------------|----------|
| Discovery | Peer referral (VP Ops networks) | 34% of pipeline | Attribution data, 12-month |
| Research | G2 comparison pages | 67% visit pre-demo | G2 analytics integration |
| Evaluation | Interactive product demo + sandbox | 78% request sandbox | Demo request form data |
| Purchase | Direct sales (AE-led) | 91% of deals involve AE | CRM closed-won analysis |
| Ongoing engagement | In-app announcements + CSM QBRs | 82% feature adoption rate | Product analytics |

### Top Objections
| Rank | Objection | Frequency | Best Counter |
|------|-----------|-----------|-------------|
| 1 | "Migration from our current tools seems risky and time-consuming" | 48% of stalled deals | Dedicated migration engineer (free) + 30-day parallel run guarantee |
| 2 | "Price per seat gets expensive as we scale past 500 users" | 35% of stalled deals | Volume pricing tier + ROI calculator showing tool consolidation savings |
| 3 | "We need [specific integration] that you don't have yet" | 22% of lost deals | Custom integration SLA (60-day build guarantee) or API + Zapier bridge |

### Trigger Events
| Trigger | Signal Source | Lead Time | Confidence |
|---------|-------------|-----------|------------|
| Series B funding announcement | Crunchbase alerts, press monitoring | 60-90 days | High |
| VP of Operations or RevOps hire | LinkedIn job change alerts | 30-60 days | High |
| SOC 2 audit initiation | Intent data (Bombora), G2 category research | 90-120 days | Medium |
| Headcount crossing 200 employees | LinkedIn company data, ZoomInfo signals | 45-90 days | Medium |

### Behavioral Signature
| Metric | This Segment | Overall Avg | Variance |
|--------|-------------|-------------|----------|
| Integrations connected | 4.8 | 2.1 | +129% |
| Weekly active users / total seats | 78% | 52% | +50% |
| API calls per month | 12,400 | 3,200 | +288% |
| Support ticket volume | 1.2/month | 2.8/month | -57% |
| Feature adoption (% of features used) | 68% | 41% | +66% |

### Churn Risk Factors
| Indicator | Threshold | Lead Time | Action |
|-----------|-----------|-----------|--------|
| Integration disconnection (2+ in 30 days) | 2 disconnections | 45 days | CSM outreach to diagnose integration issues |
| Weekly active user rate drops below 50% | <50% WAU/seats | 60 days | Usage review QBR, retraining or champion re-engagement |
| Admin login drops to <1x/week | <4 logins/month | 30 days | Product email highlighting new admin features + CSM check-in |

### Expansion Signals
| Signal | Threshold | Next Best Offer | Confidence |
|--------|-----------|----------------|------------|
| Seat utilization >90% | 90%+ seats used | Seat expansion + volume discount | High |
| API calls >80% of plan limit | 80%+ API plan | Enterprise API tier | High |
| 3+ departments actively using | Cross-functional usage | Platform license (vs. per-module) | Medium |

### Buying Committee
| Role | Involvement | Priority | Messaging Angle |
|------|------------|----------|----------------|
| VP of Operations / RevOps | Champion | Consolidation + time savings | "One platform replaces 4 tools — your team gets 10 hrs/week back" |
| CFO / Finance | Decision Maker | Total cost of ownership | "Net savings of $180K/yr vs. current tool stack" |
| IT / Security Lead | Blocker | Compliance + security | "SOC 2 Type II certified, SSO/SCIM native, no custom security work" |
| End Users (Dept Leads) | Influencer | Ease of use + no disruption | "Same-day onboarding, works with your existing workflow" |

### Segment-Specific Messaging
**Value proposition:** Replace your growing stack of disconnected tools with one platform that scales from 200 to 2,000 employees without adding headcount to manage it.
**Proof points that resonate:** Migration case studies showing timeline + tool count reduction, ROI calculators with real customer data, SOC 2 compliance documentation.
**Competitive positioning against [Competitor X]:** "Unlike [Competitor X], which requires a dedicated admin at 500+ users, our platform is self-serve by design — no admin tax as you scale."
```

---

## Persona Naming Guide

### Naming Formula
`[Behavioral/Value Modifier] + [Firmographic/Demographic Identifier] + [Functional Role or Pattern]`

### Good Names (Descriptive, Data-Grounded)
- "High-Growth Mid-Market Consolidators"
- "Enterprise Late Adopters"
- "Price-Sensitive Solo Operators"
- "API-Heavy Technical Integrators"
- "High-Frequency Low-AOV Browsers"
- "Compliance-Driven Financial Services Buyers"
- "Champion-Led Bottom-Up Adopters"

### Bad Names (Never Use)
- "Marketing Mary" / "Developer Dave"
- "The Innovator" / "The Pragmatist" (too generic)
- "Segment A" / "Cluster 3" (meaningless)
- "Small Business Owner" (too broad, not behavioral)
- "Tech-Savvy Millennial" (demographic stereotype, not data-driven)
