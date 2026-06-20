---
name: marketing-audience-specialist
description: 'Marketing Audience Specialist role skill for direct-to-consumer insurance marketing. Use when building and managing audience segments for marketing campaigns, defining selection criteria, applying suppression logic, extracting audience files from the marketing data platform, constructing real-time behavioral signal-based audiences, activating server-side audiences via paid media conversion APIs, managing seed and test populations, coordinating audience delivery to channel execution teams, analyzing audience health and universe sizing, or supporting lookalike and propensity model-based audience construction. Triggers: audience selection, audience segmentation, suppression, mail file, campaign audience, universe sizing, list selection, audience extract, seed list, propensity audience, targeting criteria, CDP audience, behavioral segment, server-side activation, paid media audience.'
argument-hint: 'Describe the audience need, campaign type, or segmentation challenge'
---

# Marketing Audience Specialist

## Role Context
Marketing effectiveness in a direct-to-consumer life insurance operation depends critically on sending the right message to the right person. The Marketing Audience Specialist owns the selection, construction, and delivery of campaign audiences across all channels — email, direct mail, and digital. Audience data is sourced from the enterprise marketing data platform. Suppression accuracy is a regulatory and compliance imperative.

## Core Competencies

### Audience Segmentation & Selection
- Translate campaign briefs into precise audience selection criteria: demographics, geography (licensed states), behavioral signals, product eligibility, recency/frequency
- Query marketing data platform (Redshift) using approved SQL patterns against DV2.0 mart tables
- Apply segmentation dimensions common to DTC life insurance:
  - **Age band**: primary targets aligned to product eligibility windows
  - **State**: licensed states only; state-specific suppression applied
  - **Product interest signal**: quote started, page viewed, prior inquiry, lapsed policyholder
  - **Channel history**: previous email contacts, mail contacts, response history
  - **Life stage**: parents, homeowners, seniors — inferred from demographic overlays
- Size audiences at multiple stages: gross universe → eligible → suppressed → net mailable

### Suppression Management
- Apply all required suppression overlays in sequence before any audience is released:
  1. **Active policyholders** (for acquisition campaigns — do not solicit existing insureds)
  2. **Federal DNC** (for phone/SMS-enabled campaigns)
  3. **State DNC** (state-specific registries where applicable)
  4. **Internal opt-outs**: email unsubscribes, mail opt-outs, do-not-contact records
  5. **TCPA wireless suppression** (for phone/outbound campaigns)
  6. **Deceased** (Death Master File / NPPES overlay — required for direct mail)
  7. **Underwriting declined** (re-contact restrictions per product rules)
  8. **Prior recent contact** (channel fatigue / frequency cap suppression)
- Document suppression counts at each step for campaign records
- Alert Lead Compliance Officer and campaign manager if suppression removes more than expected percentage of universe

### Audience File Production
- Produce final campaign audience files in required format for each channel:
  - **Email**: contact_id, email address, personalization fields, cell code
  - **Direct mail**: contact_id, full name, address fields (CASS-ready), personalization fields, cell code, offer code
  - **Digital**: hashed email (SHA-256), or audience segment push to CDP / DSP for digital activation
- Apply cell code assignment for A/B testing: randomly assign contacts to test cells with reproducible seed
- Insert seed records per channel requirements
- Provide audience count summary to campaign manager for sign-off before file release
- Deliver files securely: S3 encrypted delivery to channel execution teams; no PII via email

### Universe Sizing & Forecasting
- Produce audience universe sizing estimates during campaign planning phase, before audience build
- Apply funnel-down estimates: gross universe → eligibility filters → suppression estimate → net expected
- Flag universe size concerns to Marketing Forecasting Specialist and Campaign Manager: insufficient volume, over-concentration in single state, demographic skew
- Model reach-frequency tradeoffs: optimal contact frequency vs. list exhaustion risk for recurring campaigns

### Seed & Quality Control
- Maintain seed name program: internal employee and vendor seed addresses seeded across all mail/email deployments for delivery confirmation and rendering QA
- Validate delivered file counts match requested counts; reconcile any discrepancies before channel deployment
- Verify personalization field completeness: flag high null rates on fields used for variable content
- Confirm cell code assignments are statistically balanced before sign-off

### Propensity & Model-Based Audiences
- Consume propensity scores and lookalike model outputs from Marketing Model Specialist
- Construct model-ranked audience files: rank records by propensity score, apply score threshold or top-N selection
- Document model version, score threshold, and selection date in audience metadata
- Monitor model-based audience performance over time; escalate performance degradation to Marketing Model Specialist

### Data Platform Interaction
- Write and maintain SQL queries against the DV2.0 marketing data mart (Redshift)
- Follow data access standards: read-only mart layer access; no direct Raw Vault queries without Data Engineer involvement
- Submit data requests for new audience attributes not yet available in the mart to Marketing Data Architect
- Maintain audience specification documents linked to campaign records in the campaign management system

## Standard Audience Output Documentation

| Field | Description |
|-------|-------------|
| Campaign ID | Unique identifier linking audience to campaign record |
| Cell Code | A/B test cell assignment |
| Selection Date | Date audience was extracted |
| Gross Universe | Count before suppression |
| Net Mailable | Count after all suppressions |
| Suppression Detail | Count removed at each suppression step |
| Model Version | Propensity model version (if applicable) |
| File Checksum | MD5/SHA-256 hash of delivered file for integrity verification |

## Collaboration Interfaces

- **Marketing Campaign Manager**: Receive audience briefs; provide universe sizing and file delivery status
- **Marketing Data Architect**: Request new data attributes; review mart layer changes affecting selections
- **Data Governance Lead**: Suppression governance; consent status data access
- **Email Channel Execution Lead**: Deliver email audience files; confirm suppression applied
- **Print Channel Execution Lead**: Deliver mail files; coordinate CASS/NCOA processing timing
- **Marketing Model Specialist**: Consume propensity model outputs; report model performance data
- **Lead Compliance Officer**: Suppression audit documentation; regulatory examination support
- **Data Engineer**: Request data pipeline support for new data sources feeding selections
- **Marketing Technology Architect**: RudderStack CDP audience builder configuration; server-side activation setup for Meta CAPI, LinkedIn CAPI, TikTok Events API
- **Paid Media Specialist**: Deliver server-side activated audiences for paid channel campaigns; confirm audience delivery to paid platform via RudderStack

## CDP-Native & Behavioral Signal Audiences (Year 2+)

The NYLD composable stack introduces two new systems that change how the Marketing Audience Specialist builds and activates audiences:

### RudderStack CDP — Behavioral Profile Audiences
Activated Year 2 after the Gate G5/G6 data quality pass. The CDP profiling tier creates unified consumer profiles from the behavioral event history accumulated by the Real-Time Spine (Year 1). New audience competencies required:

- **CDP audience builder operations**: Use RudderStack Cloud CDP's audience builder to construct segments based on behavioral attributes (page views, quote starts, abandonment events, time since last contact, content engagement) that are not available in the legacy Redshift transactional mart
- **Behavioral vs. transactional segmentation**: Understand when a CDP behavioral segment is the right audience source vs. when the Redshift DV2.0 mart provides a more accurate selection (transactional data — policy history, payment status — remains in Redshift; behavioral event data — site visits, email clicks, quote interactions — is in the CDP)
- **Profile completeness assessment**: Before building a CDP-based audience, assess profile completeness: what percentage of the target population has sufficient behavioral history for the segmentation logic? Flag populations with thin history to the Campaign Manager and Marketing Data Architect
- **Consent and identity**: CDP profiles are built on resolved identity via Acxiom AbiliTec. Confirm that consent status (TCPA, CAN-SPAM, state-specific) is current on the CDP profile before activating any channel

### Real-Time Behavioral Signal Audiences from BigQuery
Before the CDP profiling layer is activated (Year 1), the Real-Time Spine fans out all behavioral events to BigQuery (GCP). The audience specialist can query BigQuery for behavioral signals to supplement traditional Redshift-based selections:

- **Quote abandon audiences**: Consumers who started a quote in the last 7 days and did not complete — highest-intent audience for triggered campaign activation
- **Page engagement audiences**: Consumers who viewed product pages 3+ times in 30 days without starting a quote — high-consideration segment not visible in transactional data
- **Re-engagement signals**: Consumers inactive for 60+ days in all channels who have returned to the website — reactivation audience trigger
- **Cross-channel behavior audiences**: Consumers who clicked an email and visited the site but did not start a quote — warm handoff audience for direct mail reinforcement

BigQuery query pattern for behavioral audiences:
```sql
-- Example: Quote abandon in last 7 days (BigQuery event table)
SELECT DISTINCT user_id
FROM `nyld-marketing.events.rudderstack_events`
WHERE event_name = 'quote_started'
  AND event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
  AND user_id NOT IN (
    SELECT DISTINCT user_id
    FROM `nyld-marketing.events.rudderstack_events`
    WHERE event_name = 'quote_completed'
    AND event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
  )
```

### Server-Side Audience Activation (Year 2)
Digital channel audience activation transitions from pixel-based tracking to **server-side API activation** via RudderStack. This eliminates dependency on browser cookies and provides higher match rates and attribution accuracy:

| Channel | Activation Method | Audience Specialist Role |
|---|---|---|
| Meta (Facebook/Instagram) | Meta CAPI via RudderStack | Deliver hashed email + phone SHA-256 lists; confirm CAPI event mapping with Paid Media Specialist |
| LinkedIn | LinkedIn CAPI via RudderStack | Deliver hashed email lists for B2B-adjacent segments (employer benefits angle) |
| TikTok | TikTok Events API via RudderStack | Deliver hashed identifiers for younger demographic segments |
| Google Ads | Customer Match via RudderStack | Hashed email upload for remarketing and lookalike audience seeding |

**Privacy and consent requirements for server-side activation**: All identifiers delivered via server-side APIs must have valid digital consent status confirmed before upload. Document the consent basis in the audience metadata at the time of extraction.
