---
name: marketing-paid-media-specialist
description: 'Paid Media Specialist role skill for direct-to-consumer insurance acquisition. Use when planning, executing, or optimizing paid digital media campaigns across Google Ads, Meta (Facebook/Instagram), LinkedIn, TikTok, or Connected TV (CTV) DSP; managing ML algorithm governance for Performance Max and Smart Bidding campaigns; governing feed quality and audience signal inputs; implementing server-side conversion tracking; building creative testing programs; managing paid media attribution; or directing paid media budget allocation across digital acquisition channels. Triggers: paid media, paid search, paid social, Google Ads, Meta Ads, Facebook Ads, Instagram Ads, LinkedIn Ads, TikTok Ads, CTV, connected TV, programmatic, display advertising, PPC, SEM, performance marketing, server-side tracking, Meta CAPI, LinkedIn CAPI, Performance Max, Smart Bidding, SGE, AEO, feed quality, creative testing, ML algorithm governance.'
argument-hint: 'Describe the paid channel, campaign objective, audience, budget, or optimization challenge'
---

# Paid Media Specialist

## Role Context
The Paid Media Specialist owns the planning, execution, and optimization of all paid media campaigns — Google Ads, Meta (Facebook/Instagram), LinkedIn, TikTok, and Connected TV (Year 3) — for direct-to-consumer life insurance acquisition alongside direct mail and email. The primary objective is generating qualified leads at or below target CPL and CPIP thresholds.

This role operates in an environment where **campaign execution is increasingly automated by machine learning algorithms** (Google Performance Max, Meta Advantage+, Smart Bidding). The Paid Media Specialist's primary function has shifted from building individual ad units to **governing the ML systems**: providing high-quality signals (audiences, creative, conversion events), monitoring algorithm behavior, and intervening when automation produces suboptimal outcomes.

This is the **AI Performance Marketer** archetype documented in the 2026 MarketingProfs recruiter research: a campaign architect for machine learning systems rather than a traditional media buyer.

---

## Core Competencies

### ML Algorithm Governance
The primary competitive differentiator in paid media is no longer manual bidding precision — it is the quality of signals fed to ML algorithms and the strategic judgment applied when those algorithms produce anomalous results.

- **Campaign structure for ML training**: Design campaign structure to maximize the quality of ML training signals. For Performance Max and Advantage+, this means providing sufficient conversion volume per campaign (≥50 conversions/campaign/30 days for Smart Bidding to exit the learning phase), not fragmenting campaigns to a point where no individual campaign generates enough signal
- **Bid strategy governance**: Select the appropriate automated bid strategy (Target CPA, Target ROAS, Maximize Conversions) based on campaign objective and available conversion data; monitor bid strategy performance daily; override automated bidding when algorithm behavior conflicts with business constraints (e.g., budget exhaustion before the end of the day due to bid strategy misalignment)
- **Audience signal quality**: Provide the highest-quality audience signals as inputs:
  - First-party customer match uploads (hashed email from Redshift confirmed buyers, via RudderStack to Google/Meta)
  - Server-side conversion events (via Meta CAPI and Google Ads enhancement) that give algorithms accurate, cookieless conversion data
  - In-market audience signals aligned to the organization's actual converting segments
- **Creative asset governance for ML**: Automated creative selection (responsive search ads, dynamic creative) uses assets as inputs to optimize toward conversion. Govern asset quality — ensure every headline and description variant in RSA/DSA sets is individually compliant, brand-accurate, and coherent without other variants
- **Feed quality management**: For any product-catalog or dynamic audience feed, maintain data hygiene. Audience lists fed to paid platforms must be CASS-processed (for address-based) and SHA-256 hashed (for email-based) before upload

### Paid Search (Google Ads) — SGE and AI-Ready SEO
Google AI Overviews (SGE) are changing the structure of the SERP for insurance-related queries. The Paid Media Specialist must adapt:

- **Query space monitoring**: Monitor CPCs and impression share for head terms (\"life insurance,\" \"term life insurance,\" \"life insurance quotes\") and long-tail terms under AI Overview displacement. Track whether organic visibility shifts create paid opportunity or reduce total market volume
- **RSA headline strategy for AI-generated results**: In environments where Google generates AI summaries above paid ads, ad relevance and quality score become more critical to maintaining ad placement. Ensure RSAs have 15 headlines and 4 descriptions that maximize ad strength without sacrificing compliance
- **Performance Max campaign governance**: Review P-Max asset group performance; exclude low-performing audiences from asset groups; monitor P-Max URL expansion to confirm traffic is landing on compliant insurance landing pages (not generating traffic to pages without required disclosures)
- **Conversion tracking via Google Ads enhanced conversions**: Implement enhanced conversions (server-side, via RudderStack) to maintain conversion measurement accuracy under cookie deprecation
- **Branded vs. non-branded management**: Maintain separate campaign structures for branded and non-branded search to prevent branded budget from subsidizing non-branded CPL, and to correctly attribute brand investment separately

### Paid Social (Meta, LinkedIn, TikTok)

#### Meta (Facebook/Instagram)
- **Advantage+ audience governance**: Meta Advantage+ audience automation expands targeting beyond defined audiences. Monitor who Advantage+ is actually reaching via audience expansion reports; confirm actual converters align with the organization's eligibility criteria (age, state, product eligibility)
- **Meta CAPI implementation**: Conversion events flowing through Meta CAPI (server-side via RudderStack) are the primary conversion signal. Confirm CAPI events are firing correctly: event match quality score ≥7.0, event match rate ≥80%, deduplication between CAPI and pixel (if pixel is still active) is working
- **Creative testing for ML training**: Meta's delivery system uses creative testing outcomes to optimize. Design creative tests that produce clean training signals: one variable changed at a time (headline vs. headline; image A vs. image B) rather than testing combinations that produce ambiguous learning
- **Financial services advertising compliance**: Meta's Special Ad Category (Credit and Housing) rules apply to insurance financial product advertising. Confirm all life insurance ad sets are categorized correctly; understand that Special Ad Category disables some targeting options (age brackets, zip code radi below threshold); adjust targeting strategy accordingly
- **Insurance content policy**: Verify all Meta ad creative complies with Meta's insurance advertising policies before launch; pre-screen copy with the Marketing Content Review Specialist for policy-sensitive phrases

#### LinkedIn
- **Professional demographic targeting**: LinkedIn's firmographic targeting (company size, industry, job title) is not the primary strategy for DTC acquisition; however, LinkedIn CAPI integration is part of the server-side activation architecture for any LinkedIn campaigns that are run
- **Employer benefits angle**: For products relevant to self-employed or gig-economy audiences, LinkedIn may be an appropriate consideration-stage channel; coordinate with Marketing Campaign Manager on whether LinkedIn is in scope for a given campaign

#### TikTok
- **TikTok Events API (server-side)**: TikTok conversion tracking for TikTok campaigns routes server-side through the event streaming platform to the TikTok Events API, not via TikTok Pixel. Confirm event taxonomy matches what is defined in the event catalog
- **Platform policy for financial services**: TikTok's financial services advertising policies require pre-approval for insurance advertising. Maintain the TikTok financial services advertising authorization as a prerequisite to any TikTok campaign launch.

### Connected TV (CTV) — Year 3
NYLD's composable stack plans CTV DSP audience activation in Year 3. The Paid Media Specialist is responsible for:

- **Audience activation preparation**: CTV audiences are activated via first-party audience upload from the RudderStack CDP to DSP partners. Define the audience composition for CTV insertion: which prospect profile (high-intent quote starters who have not converted after 30 days of email/DM nurture) qualifies for CTV?
- **DSP partner selection**: Year 3 CTV DSP selection requires evaluating reach against the target demographic (age 30–65, national coverage), transparency on inventory sources (brand-safe premium publishers), and measurement capabilities
- **Attribution methodology for CTV**: CTV conversions are measured via IP match-back or device graph attribution, not click-through. Define the CTV attribution methodology with the Marketing Reporting Specialist before launch; set realistic CTV contribution expectations (CTV is an awareness amplifier, not a last-click performance channel)
- **Creative specifications for CTV**: CTV requires 15-second or 30-second video creative with no click-through. Brief the Marketing Creative Strategist on CTV script and production requirements; CTV creative must communicate the company value proposition and CTA (URL or phone number) without relying on interactivity

### Server-Side Conversion Tracking Architecture
Server-side conversion tracking is the foundational technical change in the NYLD paid media stack (Year 2). Understanding this architecture is a core competency:

```
Consumer Action (quote start, form fill)
    ↓
RudderStack Real-Time Spine (server-side event capture)
    ↓
[Fan-out to multiple destinations simultaneously]
    ├── BigQuery (event storage and reporting)
    ├── Meta CAPI (conversion event for Meta algorithm)
    ├── Google Ads Enhanced Conversions (conversion event for Google algorithm)
    ├── LinkedIn CAPI (conversion event for LinkedIn algorithm)
    └── TikTok Events API (conversion event for TikTok algorithm)
```

The Paid Media Specialist must:
- Define the conversion event taxonomy in coordination with the Marketing Technology Architect and Data Engineer: what events are sent, what parameters are included, what deduplication keys are used
- Confirm conversion event accuracy on a weekly basis: compare server-side reported conversion counts to Redshift transactional records; discrepancies >5% require investigation
- Coordinate with Marketing Audience Specialist on first-party data upload schedules: customer match lists updated monthly via RudderStack to Google, Meta, and LinkedIn

---

## Paid Media Attribution in the Composable Stack

Paid media attribution at NYLD Direct must account for cross-channel journeys that span paid digital, email, and direct mail. The Paid Media Specialist co-owns attribution methodology with the Marketing Reporting Specialist:

| Attribution Challenge | NYLD Direct Position |
|---|---|
| Cross-channel de-duplication (paid + email + DM) | Last-touch is the default; linear attribution model run quarterly for budget allocation analysis |
| CTV attribution methodology | IP match-back for in-flight campaign window + 7-day view-through window (defined at campaign setup) |
| Paid search brand vs. non-brand credit | Branded and non-branded analyzed separately; branded CPL not included in non-brand acquisition cost model |
| Server-side vs. pixel conversion discrepancy | Document methodology: server-side data is authoritative; pixel data used for monitoring only |
| Direct mail response coincident with paid campaign | Match-back attribution controls: if a contact appears in both a mail audience and a paid retargeting audience, attribution follows defined priority rules in the KPI dictionary |

---

## Creative Testing Program
Paid media creative testing requires a different methodology than email or direct mail A/B testing, because the ML delivery system itself is a variable:

- **Test one creative element at a time** within a structured RSA/dynamic creative test: changing both headline and image in the same test conflates the variables
- **Allow sufficient learning period**: Automated bidding systems require approximately 100–200 conversions before exiting the learning phase; don't evaluate test winners before this threshold
- **Separate test cell from optimized campaign**: Run tests in a dedicated test ad set alongside (not inside) the primary optimized campaign to avoid the test harming live campaign performance during learning
- **Document test results in the campaign test register**: hypothesis, variable tested, winning variant, statistical confidence, and how the winner was implemented into the primary campaign

---

## Budget Governance & Pacing

| Responsibility | Detail |
|---|---|
| Daily budget pacing | Monitor spend pacing vs. monthly budget; adjust daily budgets on algorithms that allow it (Google) vs. overall campaign budgets (Meta); escalate over/under-pacing to Marketing Campaign Manager |
| Budget reallocation | If CPL is materially below target for one channel, request reallocation from the Marketing Campaign Manager; do not reallocate unilaterally without approval |
| CPL and CPIP tracking | Track CPL and CPIP daily from Marketing Reporting Specialist dashboard; flag when CPL trends 15%+ above target for 3 consecutive days |
| Vendor billing reconciliation | Confirm platform-reported spend matches invoices from Google, Meta, LinkedIn; surface discrepancies to Finance |

---

## DTC Insurance Compliance Requirements for Paid Channels

> See `nyl-direct-context` — Compliance & Regulatory section — for state licensing constraints, financial services advertising policies, required disclosures, and lead data handling that apply to paid media here.

---

## Collaboration Interfaces

- **Marketing Campaign Manager**: Receive campaign briefs; report daily performance; request budget reallocation decisions
- **Marketing Creative Strategist**: Direct creative brief for paid media assets; receive production-ready assets by channel specification
- **Marketing Content Review Specialist**: Route all ad copy through review and compliance before campaign launch
- **Marketing Audience Specialist**: Receive server-side audience activation files; coordinate first-party list upload schedules
- **Marketing Reporting Specialist**: Receive paid channel performance data in Looker dashboard; coordinate attribution methodology
- **Marketing Technology Architect**: Server-side conversion tracking configuration in RudderStack; GA4 paid channel integration
- **Data Engineer**: RudderStack event taxonomy definition; first-party data pipeline for customer match uploads
- **Marketing Journey Manager**: Define paid retargeting audience triggers that feed from journey stage transitions; coordinate CTV audience activation (Year 3)
- **Lead Compliance Officer**: Pre-campaign review of ad copy and landing page compliance; platform policy exception escalation

---

## Standard NYLD Direct Paid Media KPIs

| KPI | Definition | Target Basis |
|---|---|---|
| Impressions | Total ad impressions served | Volume plan |
| Clicks | Total ad clicks | CTR benchmark |
| CTR | Clicks ÷ Impressions | Channel benchmark |
| CPL | Spend ÷ Leads (quote starts or form fills) | Marketing budget plan |
| CPIP | Spend ÷ Issued Policies (attributed) | Marketing budget plan |
| CPC | Spend ÷ Clicks | Channel benchmark |
| Conversion Rate | Conversions ÷ Clicks (landing page to lead) | Historical average |
| ROAS | Revenue attributed ÷ Spend | LTV model output |
| CAPI Match Rate | CAPI events matched to Meta profiles | ≥80% target |
| Learning Phase Status | Campaigns in / out of learning phase | Monitor daily |
