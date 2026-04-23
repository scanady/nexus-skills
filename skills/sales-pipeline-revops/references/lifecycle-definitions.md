# Lifecycle Stage Definitions

Templates for lead lifecycle stages, MQL criteria by GTM motion, SLAs, and rejection/recycling workflows.

---

## Stage Templates

### Subscriber

**Entry:** opted into blog, newsletter, or content. No company info required.

**Exit:**
- Provides company info via form or enrichment
- 3+ pages in single session
- Downloads gated content

**Owner:** Marketing (automated)

**On entry:** tag source, begin engagement tracking, enroll in welcome/awareness sequence

---

### Lead

**Entry:** identified contact — name + email + company. Source: form fill, enrichment, or import.

**Exit:**
- Reaches MQL threshold (fit + engagement score)
- Manually qualified by marketing or SDR

**Owner:** Marketing

**On entry:** enrich company data (size, industry, role), begin scoring, add to nurture sequence

---

### MQL (Marketing Qualified Lead)

**Entry:**
- Hits fit score AND engagement score threshold
- OR triggers high-intent action (demo request, pricing page + form fill)

**Exit:**
- Sales accepts → SQL
- Sales rejects → recycled with reason code
- No response within SLA → escalate to manager

**Owner:** Marketing → Sales (handoff point)

**On entry:**
- Instant alert to assigned rep
- Create follow-up task — 4h SLA
- Pause marketing nurture sequences
- Log recent activity for sales context

---

### SQL (Sales Qualified Lead)

**Entry:**
- Rep completed qualifying conversation
- At least 2 of 4 BANT confirmed: budget, authority, need, timeline

**Exit:**
- Opportunity created with projected value
- Disqualified → recycled with reason code

**Owner:** Sales (SDR or AE)

**On entry:** update CRM stage, notify AE if SDR-qualified, begin sales sequence if not already in conversation

---

### Opportunity

**Entry:** formal opportunity in CRM — deal value, close date, stage assigned

**Exit:** closed-won or closed-lost

**Owner:** Sales AE

**On entry:** add to pipeline reporting, create deal tasks (proposal, demo, etc.), notify CS if close imminent

---

### Customer

**Entry:** closed-won, contract signed, payment terms set

**Exit:** churns, expands, or renews

**Owner:** Customer Success / Account Management

**On entry:** trigger onboarding sequence, assign CS manager, schedule kickoff call, remove from all sales sequences

---

### Evangelist

**Entry:** NPS 9–10 OR active referral behavior OR agreed to case study / testimonial / referral program

**Exit:** ongoing program participation

**Owner:** CS + Marketing

**On entry:** add to advocacy program, request case study or testimonial, invite to referral program, feature in campaigns (with permission)

---

## MQL Criteria Templates by GTM Motion

### PLG (Product-Led Growth)

Weight: **40% fit / 60% engagement** — product usage dominates

**Fit signals:**

| Attribute | Points |
|-----------|--------|
| Company size 10–500 | +15 |
| Company size 500–5000 | +20 |
| Target industry | +10 |
| Decision-maker role | +15 |
| Uses complementary tool | +10 |

**Engagement signals (weight product usage heavily):**

| Signal | Points |
|--------|--------|
| Created free account | +15 |
| Completed onboarding | +20 |
| Used core feature 3+ times | +25 |
| Invited team member | +20 |
| Hit usage limit | +15 |
| Visited pricing page | +10 |

**MQL threshold:** 65 points

---

### Sales-Led (Enterprise)

Weight: **60% fit / 40% engagement** — fit is critical at high ACV

**Fit signals:**

| Attribute | Points |
|-----------|--------|
| Company size 500+ | +20 |
| Target industry | +15 |
| VP+ title | +20 |
| Budget authority confirmed | +15 |
| Uses competitor product | +10 |

**Engagement signals:**

| Signal | Points |
|--------|--------|
| Requested demo | +25 |
| Attended webinar | +10 |
| Downloaded whitepaper | +10 |
| Visited pricing page 2+ times | +15 |
| Engaged with sales email | +10 |

**MQL threshold:** 70 points

---

### Mid-Market (Hybrid)

Weight: **50% fit / 50% engagement** — balanced

**Fit signals:**

| Attribute | Points |
|-----------|--------|
| Company size 50–1000 | +15 |
| Target industry | +10 |
| Manager+ title | +15 |
| Target geography | +10 |

**Engagement signals:**

| Signal | Points |
|--------|--------|
| Demo request | +25 |
| Free trial signup | +20 |
| Pricing page visit | +10 |
| Content download (2+) | +10 |
| Email click (3+) | +10 |
| Webinar attendance | +10 |

**MQL threshold:** 60 points

---

## SLA Templates

### MQL-to-SQL

| Metric | Target | Escalation |
|--------|--------|------------|
| First contact attempt | Within 4 business hours | Alert to sales manager at breach |
| Qualification decision | Within 48 hours | Auto-escalate at limit |
| Meeting scheduled (if qualified) | Within 5 business days | Weekly pipeline review flag |

### SQL-to-Opportunity

| Metric | Target | Escalation |
|--------|--------|------------|
| Discovery call completed | Within 3 business days of SQL | Alert to AE manager |
| Opportunity created | Within 5 business days of SQL | Pipeline review flag |

### Opportunity-to-Close

| Metric | Target | Escalation |
|--------|--------|------------|
| Proposal delivered | Within 5 business days of demo | AE manager alert |
| Deal stale in stage | 2x average days for that stage | Pipeline review flag |
| Close date pushed 2+ times | Immediate | Forecast review required |

---

## Rejection Reason Codes

| Code | Reason | Recycle Action |
|------|--------|----------------|
| FIT-01 | Company too small | Nurture; re-score if company grows |
| FIT-02 | Wrong industry | Archive; do not recycle |
| FIT-03 | Wrong role / no authority | Nurture; monitor for org changes |
| ENG-01 | No response after 3 attempts | Recycle to nurture in 90 days |
| ENG-02 | Interested but bad timing | Recycle in 60 days |
| QUAL-01 | No budget | Recycle in 90 days |
| QUAL-02 | Using competitor, locked in | Recycle; trigger before contract renewal |
| QUAL-03 | Not a real project | Archive; do not recycle |

---

## Recycling Workflow

1. Sales rejects MQL with reason code
2. CRM updates lifecycle stage to "Recycled"
3. Lead enters recycling nurture (lower frequency than initial nurture)
4. Engagement score resets to baseline — fit score preserved
5. Re-MQL: if lead crosses threshold again, re-route with "Recycled MQL" flag
6. Track recycled-MQL conversion rate as separate metric

**Recycling nurture parameters:**
- Frequency: bi-weekly or monthly (lower than initial)
- Content: industry insights, case studies, product updates
- Duration: 6 months then archive if no engagement
- Re-MQL trigger: high-intent action (demo request, pricing page revisit)
