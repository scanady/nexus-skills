---
name: nyl-direct-context
description: 'Org context skill for NYL Direct. Attach alongside any role skill to ground responses in NYL Direct''s specific business model, products, technology platform, channels, regulatory context, and team structure. Use when working on any NYL Direct business problem, requirement, marketing initiative, data project, or technology decision. Triggers: NYL Direct, org context, company context, business context, division context, NYL Direct context.'
argument-hint: 'Attach alongside a role skill when working on NYL Direct-specific tasks. No additional input required — this skill provides the org grounding layer.'
---

# NYL Direct — Org Context

## Organization
- **Name**: NYL Direct
- **Parent**: New York Life Insurance Company
- **Business model**: Direct-to-consumer (DTC) life insurance — sells directly to consumers without agents or brokers

## Products
- **Term Life Insurance**: Current face value range: $5k–$100k
- **Permanent Life Insurance**: Current face value range: $5k–$100k
- **Underwriting model**: Simplified issue — no medical exam required at current face value ranges; knock-out questions, MIB check, and pharmacy database check apply
- **Target demographic**: Mass-market consumers seeking affordable, accessible life insurance

## Distribution Channels
- **Digital**: Web (online quote and apply), email marketing, paid media (search, display, social)
- **Print**: Direct mail — mailed solicitations to prospective customers
- Digital and Print serve distinct audience segments and operate on different conversion timelines; Print reaches older and less digitally-active demographics that digital channels underserve

## Technology Platform
- **Cloud**: AWS
- **Data architecture**: Data Vault 2.0 (DV2.0)
- **Policy administration**: PAS (Policy Administration System) — see Enterprise Data Architect for data contracts
- **MarTech**: ESP, CDP, tag management (specific platforms managed by Marketing Technology Architect)

## Regulatory Context
- **Domicile state**: New York
- **Licensed**: All 50 states
- **Key regulatory constraints**: TCPA (consent for phone/text marketing), CAN-SPAM (email marketing), state insurance regulations (rate filings, non-forfeiture laws), NAIC model regulations
- **Compliance obligations**: Consent capture, DNC list enforcement, state-specific disclosure logic, actuarial opinion filings per state

## Key Business Metrics
- **CPL**: Cost per lead
- **CPA**: Cost per acquired policy
- **Policy issuance volume**: Primary growth metric
- **LTV**: Lifetime value (modeled by Marketing Model Specialist)
- **A/E ratio**: Actual-to-expected mortality ratio (actuarial performance)
- **Lapse rate**: Policy persistency tracked by channel and acquisition source

## DTC Business Model Dynamics
- Consumers self-select into the purchase funnel — adverse selection risk is a standing actuarial concern
- Simplified underwriting at low face values requires careful knock-out question and MIB/pharmacy check calibration
- High-volume, thin-margin model requires tight expense management and data-driven marketing
- Marketing channel mix directly affects risk pool composition — actuarial and marketing coordinate on this
- Anti-selection at top of face amount bands (applicants choosing maximum coverage may be higher risk) is a pricing consideration

## Role-Specific Implications

How the DTC business model, products, channels, and technology platform shape the work of each discipline. Role skills are written generically; attach this skill to apply these implications.

### Actuarial
- **DTC adverse selection**: Self-selected applicants have higher mortality awareness than agent-sold clients; pricing assumptions must carry a DTC-specific risk loading and A/E ratios must be monitored by channel and acquisition source
- **Simplified underwriting calibration**: No medical exam at low face values — knock-out questions, MIB check, and pharmacy DB check are the full underwriting basis; re-evaluate calibration regularly against actual mortality drift
- **Marketing mix as a mortality signal**: Heavy volume in high-response demographic segments may indicate adverse selection concentration; actuarial and marketing must jointly monitor campaign-level mortality effects
- **Face value banding**: Applicants choosing maximum available coverage represent a higher-risk cohort; anti-selection at band tops is a standing pricing consideration requiring lapse-supported pricing review

### Finance
- **CPIP as the anchor metric**: A lead that does not issue a policy generates zero revenue; all financial analysis must reach issued policy economics, not just CPA or application counts
- **Thin-margin, high-volume economics**: $5k–$100k policies produce thin absolute premium per policy; marketing volume, CPA efficiency, and lapse management are existential financial priorities
- **Lapse-adjusted channel ROI**: A lower CPA in a channel with materially higher lapse may be worth less than a higher CPA in a persistency-strong channel; normalize all ROI comparisons for lapse rate
- **YRT reinsurance cost curve**: Reinsurance cost increases with insured age; multi-year profitability models must reflect this increasing cost, not flat allocations
- **Cloud cost discipline**: Cloud infrastructure costs scale with marketing volume; govern cloud budgets as a function of policy-level economics

### Compliance & Regulatory
- **50-state licensing constraint**: Product availability, offer suppression, rate filing status, and disclosure requirements must be enforced per state in every outbound channel and digital touchpoint
- **TCPA consent at scale**: DTC direct outreach at high volume makes consent accuracy a material legal exposure; capture and record consent at every contact entry point and treat consent records as Tier-1 data
- **State insurance advertising filing**: Consumer-facing materials require pre-approval or post-use filing in most states; compliance review is a required workflow gate before any material enters production
- **Suppression as a legal control**: DNC, opt-out, and policy-status suppression errors carry per-contact statutory damages; suppression table accuracy is a legal control with zero tolerance for systematic failures
- **AI in insurance underwriting**: State insurance AI guidance (e.g., NY DFS Circular Letter No. 1, NAIC Model Bulletin) governs algorithm use in insurance decisions; Tier 1 AI models require compliance review before deployment

### Data Platform
- **Suppression tables are Tier-1 data**: Treat suppression tables with the same SLA rigor as production systems — failures cause regulatory violations, not just operational errors
- **Print + Digital identity unification**: The data model must accommodate both digital identifiers (email hash, cookie, GAID) and physical identifiers (postal address, phone) under a unified customer hub
- **Marketing data as competitive asset**: First-party response history, propensity model training data, and contact history are primary competitive differentiators; protect and invest in them as strategic assets
- **Regulatory data retention**: State insurance regulations require policy and marketing contact data retained 5–7 years; archive strategy must be designed into the platform from the start
- **Consent as time-variant data**: TCPA/CAN-SPAM consent status must be modeled as a time-variant record with effective-date tracking to support retroactive compliance queries and regulatory audits
- **Dual-channel attribution**: The same consumer may receive email and direct mail; cross-channel deduplication logic is required for accurate campaign attribution

### Technology & Applications
- **Digital channel reliability = sales**: Quote-and-apply system availability is directly linked to policy issuance volume; consumer-facing digital SLAs are mission-critical
- **State-configurable product rules**: Product availability, rates, and required disclosures vary by state; design a configurable rules layer, not hard-coded state logic
- **Print + digital interoperability**: Platforms must support both real-time digital (sub-second) and batch print (weekly/bi-weekly production cycles) — they operate on fundamentally different timescales
- **TCPA at application intake**: Phone number capture at policy application intake triggers TCPA consent obligations; consent flag must be captured, persisted, and propagated to all downstream systems at capture time

### Operations
- **Marketing calendar drives volume spikes**: Direct mail drops and digital campaign launches create sharp application intake surges; operations must capacity-plan against the marketing campaign calendar
- **Multi-state operational compliance**: Policy servicing, claims, and consumer communications must comply with state-specific requirements across all 50 licensed states (claims timeliness, free-look periods, reinstatement rules)
- **Print production lead times**: Triggered direct mail requires a 7–10 business day production buffer; real-time triggered DM requires pre-produced inventory

### Marketing
- **Dual-channel dynamics**: Digital and Print serve different audience segments with different conversion windows; Print reaches older, less digitally-active demographics that digital underserves
- **Print response accumulation**: Direct mail responses accumulate over 2–8 weeks post in-home date; volume forecasts require response curve modeling, not point-in-time snapshots
- **State-level performance variation**: Response rates, issue rates, and required offer variants differ meaningfully by state; segment campaigns, forecasts, and reports at state level for high-volume states
- **Actuarial-marketing coordination**: Marketing volume mix and channel selection directly influence the mortality risk profile of the insured population; joint monitoring with actuarial is an operational requirement

---

## Internal Team Structure

**Marketing**
CMO, Campaign Manager, Audience Specialist, Content Creation Specialist, Content Manager, Content Review Specialist, Creative Strategist, Data Architect, Forecasting Specialist, Journey Manager, Model Specialist, Planning Specialist, Reporting Specialist, Technology Architect, AI Architect

**Technology & Data**
CIO, CTO, Lead Application Architect, Enterprise Data Architect, Enterprise AI Architect, Data Engineer, Data Governance Lead, Data Quality Lead, Data Profiler Lead, Business Analyst, Application Support Manager

**Finance & Risk**
CFO, Chief Actuary, Chief Risk Officer, Lead Compliance Officer, Financial Analyst

**Operations**
COO, Project Architect, Project Architecture Analyst, Project Implementation Specialist

**Channels**
Email Channel Execution Lead, Print Channel Execution Lead, Paid Media Specialist

**Executive**
CEO, Executive Advisor
