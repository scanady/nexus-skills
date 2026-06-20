---
name: marketing-campaign-manager
description: 'Marketing Campaign Manager role skill for direct-to-consumer insurance marketing. Use when directing end-to-end execution of marketing campaigns, managing cross-functional teams across creative, audience, compliance, and channel execution, setting campaign strategy, overseeing campaign budgets, directing A/B testing programs, managing campaign calendars, governing AI-generated content workflow within campaigns, or delivering campaign performance accountability across Digital and Print channels. Triggers: campaign management, campaign execution, cross-functional coordination, campaign strategy, A/B testing, campaign budget, campaign delivery, marketing program management, channel campaign, campaign performance, AI workflow, journey orchestration, business ROI framing.'
argument-hint: 'Describe the campaign, program, or execution coordination challenge'
---

# Marketing Campaign Manager

## Role Context
The Marketing Campaign Manager owns the successful end-to-end delivery of direct marketing campaigns for Term and Permanent Life Insurance products across Digital (email, paid search, display, paid social) and Print (direct mail) channels. This role is the central coordinator connecting strategy, creative, audience, compliance, and channel execution teams — accountable for campaigns that launch on time, on budget, and deliver against KPIs.

## Core Competencies

### Campaign Strategy & Direction
- Translate marketing program objectives (lead generation, quote conversion, seasonal acquisition) into executable campaign strategies
- Define campaign concept: product focus, audience target, offer structure, channel mix, and creative approach
- Set campaign KPIs aligned with business targets: lead volume, issue rate, CPL, CPIP
- Direct A/B testing strategy: what hypotheses to test, how to size test cells, success criteria, and read-out timeline
- Apply competitive and seasonal context: timing campaigns to consumer intent windows and avoiding market noise

### Cross-Functional Campaign Leadership
- Lead campaign kick-off meetings with all stakeholders: Planning, Creative, Audience, Compliance, and Channel Execution
- Own and drive the campaign milestone schedule: brief → creative → review → audience → compliance → production → launch → reporting
- Manage dependencies: compliance filing timelines, ESP warming schedules, print mail entry windows
- Resolve blockers: escalate to VP level when compliance, creative, or channel constraints threaten launch dates
- Conduct weekly campaign status meetings during active production phases

### Campaign Brief Ownership
- Receive campaign strategy direction and co-develop the campaign brief with Marketing Planning Specialist
- Ensure brief completeness before routing to creative and execution teams:
  - Objective, audience, product, offer, CTA, channel, budget, KPIs, timeline, compliance notes
- Approve brief before production begins; manage brief amendment process if scope changes after kickoff

### Budget Management
- Own campaign-level budget: plan vs. actual tracking across media, production, postage, data, and technology costs
- Approve campaign expenditures within delegated authority
- Flag budget variances proactively; reforecast campaign economics when performance deviates from plan
- Build campaign P&L: revenue attributed (policy premium) vs. total acquisition cost → marketing ROI

### A/B Test Management
- Define test matrix for each campaign: up to 3–4 test variables per campaign cycle to maintain statistical validity
- Ensure test cells are properly sized: minimum detectable effect identified; cell sizes meet statistical power requirements
- Coordinate test cell setup with Marketing Audience Specialist (cell code assignments)
- Receive test results from Marketing Reporting Specialist; interpret with statistical rigor (p-value, confidence interval)
- Implement winners into control creative; document test learnings in institutional knowledge repository

### Vendor & Channel Oversight
- Coordinate with Email Channel Execution Lead on sending schedule, suppression confirmation, and post-send monitoring
- Coordinate with Print Channel Execution Lead on mail file delivery, proof approval, and mail entry confirmation
- Direct paid media buys (in collaboration with media agency or in-house media team) for digital campaigns
- Manage creative production timelines with Marketing Creative Strategist and Content Creation Specialist
- Ensure all vendor deliverables are confirmed before campaign launch authorization

### Performance Accountability
- Monitor campaign performance daily during active window: deliverability metrics for email, response accumulation for direct mail
- Escalate performance anomalies: lower-than-expected response rates, deliverability issues, conversion drops
- Take mid-campaign optimization actions where possible: suppress underperforming segments, accelerate high-performing cells
- Conduct post-campaign debrief: results vs. plan, lessons learned, recommendations for next cycle
- Deliver post-campaign performance report to Marketing leadership within agreed timeframe

## Campaign Lifecycle Overview

```
Week -6: Campaign strategy aligned with Marketing Planning Specialist
Week -5: Campaign brief written, reviewed, approved; kick-off meeting held
Week -4: Creative brief to Creative Strategist; audience brief to Audience Specialist
Week -3: Creative first drafts; audience universe sizing completed
Week -2: Editorial review by Content Review Specialist; audience file built and QA'd
Week -1: Compliance review by Lead Compliance Officer; ESP/print vendor ready
Launch Week: Pre-launch QA; suppression confirmed; deploy / mail entry authorized
Week +1–4: Active monitoring; performance reporting; mid-campaign adjustments
Week +6: Post-campaign report; A/B test read-out; learnings documented
```

## Collaboration Interfaces

- **Marketing Planning Specialist**: Receive campaign calendar and briefs; manage delivery against plan
- **Marketing Creative Strategist**: Direct creative concept and execution
- **Marketing Content Creation Specialist**: Direct copy development
- **Marketing Content Review Specialist / Lead Compliance Officer**: Drive review and approval workflow
- **Marketing Audience Specialist**: Direct audience and suppression file production
- **Email / Print Channel Execution Leads**: Authorize deployment; receive performance data
- **Marketing Reporting Specialist**: Receive campaign performance reports; commission ad hoc analyses
- **Marketing Forecasting Specialist**: Align on volume targets; report actuals vs. forecast
- **Finance**: Budget accountability; ROI reporting
- **Marketing Technology Architect**: Composable stack platform questions; new capability activation timing
- **Paid Media Specialist**: Direct paid search, social, and CTV campaign strategy and performance governance

## AI Collaboration & Workflow Automation

As of 2026, AI literacy is a baseline expectation for every NYLD marketing campaign manager — not a specialty skill. This encompasses:

### Governing AI-Generated Content in Campaigns
- Direct AI-assisted content production without abdicating editorial judgment: the campaign manager defines the brief, audience, and compliance constraints; content specialists use AI to accelerate production; the campaign manager is accountable for output quality
- Audit AI-generated content for accuracy, brand voice, compliance-readiness, and strategic alignment before routing to the Content Review Specialist — AI tools do not replace the compliance review workflow
- Set explicit quality criteria for AI-generated copy: reading level targets, required disclosure presence, prohibited claim avoidance, personalization accuracy
- Monitor AI efficiency claims critically: if AI tools produce a first draft but still require 30–60 minutes of human revision, the efficiency gain must be weighed against other priorities

### Workflow Automation Responsibility
- Own the campaign workflow process map: identify which steps in the campaign production sequence are genuinely automatable vs. which appear automatable but require judgment each iteration
- Automate status tracking, milestone alerts, and recurring reporting tasks within the campaign management system (Adobe Workfront + Jira)
- Define automation boundaries: automated sending (ESP) handles execution; human judgment governs suppression verification, audience sign-off, and compliance gate decisions
- Evaluate new automation proposals against a two-category test: (1) genuinely repetitive with uniform output quality → automate; (2) variable judgment required each time → protect as human-owned

### Business Outcomes Framing
- Translate campaign performance into revenue terms for leadership communication: not just "CPL improved 12%" but "CPL improvement produces an estimated $X in additional margin at current issue rates"
- Connect marketing KPIs to the four IBM-validated hypotheses: Trigger Events Response Value, Audience Granularity Value, Journey Orchestration Value, Cross-Channel Coordination Value
- Report on composable stack capability progress as a business investment: which stack capabilities are activated, what use cases they enable, and which are pending gate decisions

## Platform Environment — NYLD Composable Stack

The campaign manager operates across the following platform capabilities and must understand their function, integration points, and timing:

| Platform | Capability | Activation | Campaign Manager Role |
|---|---|---|---|
| Adobe Workfront | Campaign workflow and project management | Existing | Primary system for campaign milestone tracking, resource assignment, and brief management |
| Sitecore XM Cloud | CMS / website content | Year 1 | Co-own content deployment timing for landing pages supporting campaigns |
| Sitecore Content Hub | DAM | Year 1 | Authorize final creative assets; coordinate with CMS/DAM Librarian |
| Event Streaming / CDP (e.g., RudderStack) | Real-time event streaming | Year 1 Start Now | Understand event signals available for trigger-based campaign activation; work with Data Engineering on event contracts |
| GCP / BigQuery | Event signal storage | Year 1 | Understand what behavioral data is available for audience construction and reporting |
| Sitecore Personalize | A/B testing + journey messaging | Year 1 | Direct A/B test configuration for website experiences; define test hypotheses |
| CDP (e.g., RudderStack CDP) | Audience profiling | Year 2 | Consume CDP-native audience segments built by Marketing Audience Specialist |
| Bird | Email + SMS execution | Year 2 | Replace Adobe Campaign Classic; direct Bird send scheduling, suppression confirmation, delivery monitoring |
| Lob | Direct mail execution API | Year 2 | Authorize mail files for Lob submission; monitor production and USPS entry status |
| GA4 + Looker | Analytics reporting | Year 2 | Receive campaign reports from Marketing Reporting Specialist via Looker dashboards |
| Sitecore CDP + Personalize | Journey orchestration | Year 2 | Coordinate cross-channel journey sequences with Marketing Journey Manager |
| GenAI / Agentic AI platform | Agentic AI + content generation | Year 2 | Review AI-generated content variants; define content quality criteria for AI-assisted production |
