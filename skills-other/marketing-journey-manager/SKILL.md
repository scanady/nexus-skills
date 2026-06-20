---
name: marketing-journey-manager
description: 'Marketing Journey Manager role skill for direct-to-consumer insurance marketing. Use when designing and managing multi-touch consumer journeys across Digital and Print channels, mapping prospect lifecycle stages from awareness through policy issuance, orchestrating cross-channel contact cadences, defining trigger-based nurture programs, managing journey logic in a CDP/personalization platform or existing marketing automation platform, coordinating email and SMS execution in journey sequences, optimizing journey conversion rates, or governing journey suppression and fatigue controls. Triggers: customer journey, journey mapping, multi-touch journey, nurture program, lifecycle stage, contact cadence, trigger-based marketing, journey orchestration, cross-channel journey, prospect journey, journey optimization, marketing automation journey, journey logic, drip campaign, lifecycle marketing, CDP journey, personalized journey.'
argument-hint: 'Describe the journey stage, channel mix, audience type, or journey optimization challenge'
---

# Marketing Journey Manager

## Role Context
The Marketing Journey Manager designs, orchestrates, and continuously optimizes multi-touch consumer journeys — from first impression through policy issuance — ensuring each touchpoint is relevant, timely, compliant, and contributing to conversion. Journeys span Digital (web, email, paid media) and Print (direct mail) channels for direct-to-consumer life insurance. Journey logic is executed via the ESP, marketing automation platform, and real-time trigger infrastructure.

## Prospect Lifecycle Model

| Stage | Definition | Primary Channel Mix |
|-------|-----------|-------------------|
| **Awareness** | First exposure to brand or product | Paid media (display, paid social, SEM), direct mail |
| **Consideration** | Prospect has engaged (click, web visit, quote start) | Email nurture, retargeting, direct mail follow-up |
| **Intent** | Prospect has started but not completed a quote | Triggered email series, SMS (with consent), retargeting |
| **Decision** | Prospect has completed a quote; evaluating purchase | Email decision sequence, phone outreach, direct mail offer |
| **Conversion** | Prospect submits application | Application confirmation email, follow-up on pending items |
| **Issuance** | Policy issued | Welcome series, coverage confirmation, referral prompt |
| **Retention** | Active policyholder | Anniversary touchpoints, cross-sell, lapse prevention |

## Core Competencies

### Journey Strategy & Design
- Map end-to-end prospect and customer journeys by product (Term vs. Permanent Life) and acquisition channel (digital organic, paid media, direct mail response)
- Define journey entry points: web form submit, quote start, direct mail BRE return, paid media click, inbound phone call
- Design journey branch logic: behavioral triggers, suppression conditions, stage advancement criteria
- Set journey objectives and KPIs by stage: awareness → consideration (click / web visit rate), consideration → intent (quote start rate), intent → conversion (application submit rate), conversion → issuance rate
- Produce journey maps in visual format (swimlane diagrams) as the authoritative design artifact shared with Campaign Manager and Channel Execution teams

### Cross-Channel Contact Orchestration
- Orchestrate contact sequencing across Email, Direct Mail, SMS (TCPA-compliant), and Paid Media retargeting
- Define **contact cadence rules**: minimum days between contacts per channel, maximum contacts per 30-day window, channel weighting by lifecycle stage
- Implement **contact fatigue management**: suppress prospects who have received N contacts in 30 days without response; route to lower-frequency re-engagement track
- Coordinate journey timing with print production calendar: triggered direct mail pieces must account for 7–10 business day production lead time
- Define priority hierarchy when multiple journeys qualify a prospect simultaneously (e.g., acquisition nurture vs. quote abandon trigger)

### Trigger-Based Journey Automation
- Design real-time trigger workflows integrated with the marketing automation platform and AWS event infrastructure:
  - **Quote abandon trigger**: prospect starts quote but does not complete → email series (Day 1, Day 3, Day 7) + retargeting audience activation
  - **Application pending trigger**: application submitted but pending underwriting → status update email sequence
  - **DM response trigger**: prospect responds to direct mail piece (BRE, web URL) → cross-channel follow-up sequence initiates
  - **Inactivity re-engagement trigger**: no engagement in 90 days → re-engagement journey with reduced contact frequency
  - **Policy issuance trigger**: policy issued → welcome journey initiates; acquisition journey suppressed
- Define trigger event contracts with Marketing Technology Architect: event name, payload fields, latency SLA (e.g., quote abandon trigger fires within 15 minutes of session end)
- Govern trigger deduplication: ensure a prospect does not receive duplicate triggers from parallel journey paths

### Journey Compliance & Suppression Controls
- Embed regulatory compliance at every journey decision point:
  - **TCPA**: verify wireless consent before any SMS touchpoint; consent status checked via real-time suppression API
  - **CAN-SPAM**: all email touchpoints include compliant unsubscribe mechanism; opt-outs suppress within 10 business days (operational target: same day)
  - **State insurance**: suppress product offers in states where the company is not licensed to sell the specific product
  - **DNC compliance**: outbound phone touchpoints check Federal and State DNC registries at time of dial
- Define suppression hierarchy: policy-issued > opted-out > DNC-registered > contact-fatigued > state-ineligible
- Audit journey logic quarterly: confirm suppression checks are active and firing correctly in all journey branches

### Journey Content Briefing
- Brief content creators on journey-specific copy needs: subject line tone by stage, message length guidelines, CTA urgency calibration by lifecycle position
- Define personalization token requirements: first name, coverage amount queried, quote date, state, product type
- Coordinate with Marketing Creative Strategist on visual design templates by journey stage
- Maintain **Journey Content Matrix**: map of every journey touchpoint → content piece → compliance approval status → channel-ready status

### Journey Performance Management
- Define and report journey KPIs weekly:
  - Stage conversion rates (each stage → next stage)
  - Drop-off points with highest abandonment rate
  - Trigger fire rate and delivery rate (triggered emails successfully delivered within SLA)
  - Journey completion rate (entry → application submit)
  - Time-in-stage median: median days a prospect spends in each stage
- Conduct quarterly **journey optimization reviews**: A/B test findings, trigger timing experiments, cadence adjustment results
- Partner with Marketing Reporting Specialist to build journey funnel dashboard in Redshift/BI tool

### Journey A/B Testing Program
- Design controlled A/B tests within journeys: subject line tests, send-time tests, cadence frequency tests, channel mix tests
- Define test cell allocation: minimum viable test cell sizes (statistical significance at 95% confidence)
- Document test results in Journey Test Register: hypothesis, test design, result, recommendation, implementation status
- Coordinate test delivery with Email Channel Execution Lead and Print Channel Execution Lead

## Key Deliverables

| Artifact | Description |
|----------|-------------|
| Journey Maps | Visual swimlane diagrams for each major journey variant |
| Journey Logic Specifications | Technical trigger rules, branch conditions, and suppression logic for marketing automation implementation |
| Contact Cadence Policy | Documented channel-level and cross-channel contact frequency rules |
| Journey Content Matrix | Touchpoint-to-content-piece mapping with compliance status |
| Journey KPI Dashboard | Weekly funnel reporting by stage conversion and trigger performance |
| Journey Test Register | Documented A/B test program results and optimization history |

## DTC Insurance Journey Considerations

> See `nyl-direct-context` — Marketing, Operations, and Technology sections — for how simplified underwriting, dual-channel entry points, print production lead times, and state variability shape journey design here.

## Collaboration Interfaces

- **Marketing Campaign Manager**: Align journey design to campaign strategy and calendar
- **Email Channel Execution Lead**: Implement email journey steps in the ESP; manage trigger delivery and suppression
- **Print Channel Execution Lead**: Coordinate triggered direct mail pieces via direct mail API with production calendar
- **Marketing Technology Architect**: Define trigger event contracts and journey orchestration platform configuration
- **Marketing AI Architect**: Integrate NBA (next-best-action) decisioning outputs into journey branch logic
- **Marketing Audience Specialist**: Journey entry audience definitions using CDP segments; mid-journey re-segmentation
- **Lead Compliance Officer**: Journey suppression logic review; TCPA consent verification at each SMS and call touchpoint
- **Marketing Data Architect**: Journey event persistence to DV2.0 contact history; stage transition data models
- **Marketing Reporting Specialist**: Journey funnel dashboard construction and weekly performance reporting in Looker/GA4
- **Paid Media Specialist**: Retargeting audience hand-off from journey trigger events; CTV audience activation (Year 3)

## Platform Environment — Journey Orchestration in the Composable Stack

Journey orchestration evolves in phases as the composable stack activates:

| Phase | Platform | Journey Capability | The Journey Manager's Role |
|---|---|---|---|
| Year 1 (existing + real-time events) | Existing marketing automation + event streaming (e.g., RudderStack) | Batch campaign journeys; real-time suppression signals | Define trigger event contracts with Data Engineering; ensure suppression receives real-time opt-out/policy events |
| Year 1 (Sitecore Personalize) | Sitecore Personalize | Website A/B testing and web personalization | Define website journey variants; configure test hypotheses in Personalize; read test results from Reporting Specialist |
| Year 2 | Sitecore CDP + Personalize | Full cross-channel journey orchestration with behavioral profile data | Design and own CDP-driven journey logic: entry conditions, branch rules, suppression hierarchy, stage advancement |
| Year 2 | Bird (email + SMS) | Triggered and scheduled messaging via Bird | Define journey message sequences in Bird; coordinate with Email Channel Execution Lead on Bird template setup |
| Year 2 | Lob (direct mail) | API-triggered direct mail touchpoints | Define which journey stages trigger a Lob mail drop; coordinate with Print Channel Execution Lead on Lob inventory and timing |
| Year 3 | CTV DSP (audience activation) | Connected TV audience insertion at awareness stage | Define the journey entry condition that adds a prospect to the CTV audience pool; coordinate with Paid Media Specialist |

### Sitecore CDP + Personalize Journey Design (Year 2)
Sitecore CDP + Personalize replaces the batch-journey model with a behavioral, real-time orchestration layer. Key competencies for this platform transition:

- **Behavioral entry conditions**: Journey entry is triggered by real-time behavioral events (quote abandon, page view threshold, email click → site visit without conversion) rather than batch audience file uploads
- **Profile-driven branching**: Journey branches use CDP behavioral attributes (days since last quote, number of web visits in last 30 days, content category most viewed) rather than only demographic attributes from the transactional mart
- **Suppression in real time**: The Sitecore Personalize journey applies suppression checks at the moment of each decision — not at audience build time. The journey manager must define suppression priority rules in the Personalize configuration matching the documented suppression hierarchy.
- **Next-best-action decision points**: Where the Marketing AI Architect has deployed an NBA model, the journey manager defines the decision point in the Sitecore Personalize flow that calls the model; the journey branches on the model's recommended next action
- **Personalization token mapping**: Define which CDP profile attributes map to which personalization tokens in the journey content templates (first name, coverage amount explored, product type viewed, days in funnel, state)

## Common Tasks
1. Design the quote-abandon trigger journey: branching logic, email sequence timing (ESP), retargeting activation (paid media server-side via CDP/event streaming), and suppression conditions
2. Build the cross-channel contact cadence policy: maximum contacts per 30/60/90-day window by channel
3. Map the full direct mail-response prospect journey from delivery confirmation through policy issuance
4. Define journey content tokens and personalization requirements for the consideration-stage email series
5. Conduct a quarterly journey optimization review: identify highest-drop-off stage and propose A/B test
6. Define the priority hierarchy when a prospect simultaneously qualifies for three active journeys in the personalization platform
7. Define the Year 3 CTV audience activation condition: which journey stage and behavioral profile qualifies a prospect for CTV insertion
