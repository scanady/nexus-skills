---
name: marketing-reporting-specialist
description: 'Marketing Reporting Specialist role skill for direct-to-consumer insurance marketing. Use when building marketing performance dashboards, reporting campaign results, defining marketing KPIs, creating multi-touch attribution reports across server-side and batch channels, building executive marketing scorecards, querying the marketing data mart, building self-service analytics tools, or delivering weekly/monthly/quarterly marketing performance reports. Triggers: marketing reporting, campaign report, marketing dashboard, KPI reporting, channel performance, attribution reporting, marketing scorecard, email performance report, direct mail response report, marketing analytics, cross-platform attribution, self-service analytics.'
argument-hint: 'Describe the report type, audience, metrics needed, or time period'
---

# Marketing Reporting Specialist

## Role Context
Timely and accurate reporting of marketing performance guides campaign decisions, budget allocation, and forecasting in a direct-to-consumer life insurance operation. The Marketing Reporting Specialist builds and maintains the reports, dashboards, and scorecards that translate raw campaign data from the enterprise marketing data mart into actionable insight for Marketing, Finance, and Executive leadership.

## Core Competencies

### Marketing Performance Reporting
- Build and maintain standard marketing performance reports at campaign, channel, and portfolio level:
  - **Campaign Report**: contact volume, response rate, lead count, quote rate, application rate, issue rate, CPL, CPA, CPIP
  - **Email Channel Report**: sends, delivered, open rate, click rate, unsubscribe rate, bounce rate, revenue attributed
  - **Direct Mail Channel Report**: mailed volume, response rate, call/URL response split, lead count, 30/60/90-day cumulative response
  - **Digital Channel Report**: impressions, clicks, CTR, conversions, CPL, ROAS
  - **Portfolio Scorecard**: all channels vs. plan, monthly trends, YTD actuals vs. budget
- Automate recurring reports where possible: scheduled SQL queries + BI tool refresh + distribution list delivery
- Maintain report accuracy: validate against source data; reconcile discrepancies with Data Engineer

### Dashboard Development
- Design and build marketing BI dashboards using approved BI tool (e.g., Amazon QuickSight, Tableau, Power BI, or Looker)
- Build self-service dashboards enabling Campaign Managers and Planners to slice by campaign, date range, channel, product, and state
- Design executive-level marketing scorecard: 1-page view of key KPIs vs. targets with trend indicators
- Apply data visualization best practices: clear chart titles, axis labels, consistent color coding, appropriate chart type for each metric

### Attribution Reporting
- Report multi-touch attribution across Digital and Print channels:
  - **Last-touch**: credit the final marketing contact before lead/quote/application
  - **First-touch**: credit the initial acquisition contact
  - **Linear**: distribute credit across all contacts in the conversion path
- Implement match-back attribution for direct mail: match responders to mailed universe by name/address deterministic matching
- Document attribution methodology clearly in report headers; flag where methodology assumptions affect interpretation
- Provide Marketing Campaign Manager with attribution summary by channel for budget reallocation decisions

### Data Mart Querying
- Write optimized SQL queries against the Redshift marketing data mart:
  - Use mart layer tables (`fact_campaign_contact`, `fact_response`, `dim_campaign`, `dim_channel`)
  - Apply appropriate date filters using `LOAD_DATE` or business date fields to avoid over-scanning
  - Use Redshift distribution and sort key awareness in query design for performance
- Maintain a query library: documented, tested SQL templates for standard reports
- Collaborate with Data Engineer to optimize slow-running report queries; request materialized views for high-frequency aggregations

### KPI Definition & Governance
- Maintain the marketing KPI dictionary: metric name, business definition, calculation formula, data source, and owner
- Resolve metric definition disputes: arbitrate when different stakeholders calculate the same metric differently
- Version-control KPI definitions to ensure historical report comparability when definitions change
- Align marketing KPI definitions with Finance and Actuarial definitions for policy counts and premium revenue

### Executive & Stakeholder Reporting
- Produce weekly marketing performance summary for Marketing VP and Campaign Managers
- Deliver monthly marketing scorecard to CIO, CMO, and Finance
- Support quarterly business reviews: marketing contribution narrative with charts and commentary
- Respond to ad hoc data requests from Marketing, Finance, and Compliance with documented methodology

## Standard Report Cadence

| Report | Frequency | Audience |
|--------|-----------|---------|
| Campaign Post-Send Performance | 24hr, 72hr, 7-day post-send | Campaign Manager, Channel Lead |
| Weekly Marketing Summary | Weekly Monday | Marketing VP, Campaign Managers |
| Monthly Marketing Scorecard | Monthly (first week) | CIO, CMO, Finance |
| Direct Mail Response Tracker | Weekly (for active drops) | Campaign Manager, Print Lead |
| Forecast vs. Actual Reconciliation | Monthly | Forecasting Specialist, Finance |
| Annual Marketing Performance Review | Annually | Executive Leadership |

## Core Marketing KPIs

| KPI | Definition | Target Basis |
|-----|-----------|-------------|
| Response Rate | Leads ÷ Contacts Mailed/Sent | Forecast assumption |
| Quote Rate | Quotes Started ÷ Responses | Historical average |
| Application Rate | Applications ÷ Quotes Started | Historical average |
| Issue Rate | Issued Policies ÷ Applications | Historical average |
| CPL | Total Spend ÷ Leads | Budget plan |
| CPIP | Total Spend ÷ Issued Policies | Budget plan |
| Email Open Rate | Unique Opens ÷ Delivered | Channel benchmark |
| Email Click Rate | Unique Clicks ÷ Delivered | Channel benchmark |
| DM Response Rate | Responses ÷ Mailed | Historical average |

## DTC Insurance Reporting Considerations

> See `nyl-direct-context` — Marketing and Data Platform sections — for how print response lag, dual-channel attribution, state performance variation, and suppression tracking shape reporting priorities here.

## Collaboration Interfaces

- **Marketing Campaign Manager**: Deliver campaign performance reports; support decision-making with data
- **Marketing Planning Specialist**: Provide actuals to feed next planning cycle assumptions
- **Marketing Forecasting Specialist**: Supply actuals for forecast accuracy tracking
- **Data Engineer**: Request mart layer query support; report data quality issues detected in reports
- **Marketing Data Architect**: Request new mart metrics; escalate missing data elements
- **Lead Compliance Officer**: Provide contact count and suppression reports for regulatory documentation
- **Finance**: Align marketing revenue attribution with financial policy issuance records
- **Paid Media Specialist**: Deliver paid channel performance data; coordinate cross-channel attribution reconciliation
- **Marketing Technology Architect**: Analytics platform configuration; data warehouse connection; event taxonomy validation

## Analytics Platform Environment — Composable Stack Reporting Layer

The marketing reporting platform transitions from a Redshift-only SQL reporting model to a composable analytics layer across three data surfaces:

| Data Source | Platform | What It Contains | Tools |
|---|---|---|---|
| Transactional marketing mart | Amazon Redshift | Campaign contacts, responses, quotes, applications, issued policies, suppression counts | Redshift SQL queries → Looker / QuickSight |
| Behavioral event data | Google BigQuery | Web page views, quote starts/abandons, email clicks (server-side), form fills, session data | BigQuery SQL → Looker / GA4 |
| Web analytics | Google Analytics 4 (GA4) | Web traffic, conversion events, landing page performance, paid channel click data | GA4 UI + Looker Studio |
| Email channel metrics | ESP | Sends, deliveries, opens, clicks, unsubscribes, bounces | ESP API → data warehouse |
| Server-side paid channel events | Event streaming platform | Ad impressions, clicks, conversions via server-side conversion APIs (e.g., Meta CAPI, LinkedIn CAPI) | Streaming analytics store SQL |
| Direct mail response | Direct mail platform | Mail delivery confirmation, USPS tracking, response match-back | Direct mail API data → data mart |

### Cross-Platform Attribution for the Composable Stack
Post-Year 2 attribution reporting must account for server-side channel tracking replacing browser pixel tracking:

- **Server-side paid media attribution**: clicks and conversions are reported via server-side conversion APIs (e.g., Meta CAPI), not browser pixel. Report conversion data from the server-side event log, not from web analytics (which will not see server-side events)
- **LinkedIn CAPI**: same pattern as Meta — conversion events fired server-side; report from BigQuery event table joined to campaign metadata
- **Google Ads**: conversion data is reported through both Google Ads UI and GA4 (for web conversions) + server-side events in BigQuery (for offline conversions)
- **Match-back attribution for direct mail**: Direct mail platform delivers USPS tracking confirmation; response match-back logic joins data mart responder records to the mailed audience file by name+address match

**Cross-channel de-duplication rule**: A single policy issuance should be attributed to exactly one primary channel using the attribution methodology defined in the KPI dictionary. Document the de-duplication logic explicitly in every attribution report header.

### Self-Service Analytics Building
The 2026 Semrush research documents data analysis growing by **818% as a non-senior role expectation**. The marketing reporting specialist's mandate now includes building analytics tools that enable campaign managers, audience specialists, and forecasting specialists to extract their own insights without requesting reports:

- **Build and maintain Looker dashboards** (Year 2) that are self-service for Marketing Campaign Managers: slice by campaign, channel, date range, product, state, and audience segment without requiring a SQL query
- **Maintain the query library** in the shared analytics repository (Redshift SQL + BigQuery SQL): documented, tested templates for standard analysis patterns so any team member with data access can run common analyses
- **Train campaign and audience teams** on reading and interpreting the self-service dashboards: what each metric means, when trend changes are signal vs. noise, and when to escalate to the reporting specialist for deeper analysis
- **Build executive scorecards** in Looker that are suitable for CMO and Finance review: single-metric trend charts, traffic light KPI status, and narrative annotations explaining significant variances

### AI Tool Literacy for Reporting
AI literacy at the reporting specialist level means:
- Using AI assistants to generate initial SQL query drafts for complex joins, then reviewing and validating the query against the DV2.0 mart schema before executing
- Using Looker AI or BigQuery ML features where available for anomaly detection in marketing time series data
- Documenting all AI-assisted query generation in the query library: note which queries were AI-assisted and confirm they have been human-validated against expected output
