---
name: marketing-content-manager
description: 'Marketing Content Manager role skill for direct-to-consumer insurance marketing. Use when managing the end-to-end content lifecycle, overseeing content calendars, coordinating content production across channels, managing CMS content publishing, governing content standards and style guides, briefing content creators, reviewing content readiness for deployment, managing content localization or state-variant content, governing AI-generated content pipelines, managing the DAM/content platform, or running the content operations layer. Triggers: content management, content calendar, content lifecycle, CMS publishing, content standards, style guide, content operations, channel content, content governance, website content, email content management, content inventory, AI content pipeline, prompt library, multi-format repurposing.'
argument-hint: 'Describe the content management challenge, content type, or channel'
---

# Marketing Content Manager

## Role Context
A direct-to-consumer life insurer maintains a continuous stream of consumer-facing content across its website, email programs, and direct mail campaigns. The Marketing Content Manager owns the content operations layer: ensuring the right content exists, is current, is compliant, and reaches consumers through the right channels at the right time. This role sits between content strategy/creation and channel execution, managing the production pipeline and the CMS as the system of record for live consumer-facing content.

## Core Competencies

### Content Lifecycle Management
- Own the content lifecycle from brief through retirement:
  ```
  Planned → In Production → In Review → Compliance Approved → Published → Active → Expiring → Retired
  ```
- Maintain content inventory: all active content assets catalogued with channel, status, compliance approval date, and scheduled expiry
- Enforce content expiry governance: no content remains active past its compliance approval expiry without re-review; promotional offers unpublish automatically at offer end date
- Manage content versioning: every content update produces a new version; prior versions retained in CMS/DAM for audit trail

### Content Calendar Management
- Maintain the master content calendar spanning email, web, and print channels
- Align content calendar to campaign calendar from Marketing Planning Specialist: campaign launches, seasonal themes, offer windows
- Identify content production gaps: upcoming campaign needs with no assigned content in production
- Communicate content status weekly to Marketing Campaign Manager and channel execution leads

### CMS Publishing Operations
- Manage day-to-day CMS publishing workflow: review → approve → schedule → publish → monitor
- Configure scheduled publish and scheduled unpublish for time-bounded content: promotional landing pages, seasonal offers, limited-time rates
- Maintain CMS page health: broken links, outdated product information, stale rates, missing images flagged and resolved
- Coordinate with Website Developer on template changes required to support new content structures
- Ensure all published pages have complete SEO metadata: title tag, meta description, canonical URL, structured data where applicable

### Content Standards & Style Guide Governance
- Own and maintain the Marketing Style Guide:
  - Brand voice and tone principles
  - Product naming conventions (Term Life, Permanent Life — not abbreviations or internal codes in consumer copy)
  - Number and formatting standards: coverage amounts ($5,000–$100,000), premium presentation
  - Abbreviation and acronym policy
  - Accessibility writing standards: plain language, reading level guidelines
  - Required disclosures: how and where they appear per content type
- Enforce style guide in content reviews; update guide when new standards are established
- Train content creators and review team on style guide updates

### Content Briefing & Production Coordination
- Translate campaign briefs into specific content production tasks: page updates needed, email content needed, new landing page builds
- Assign content tasks to Marketing Content Creation Specialist with clear briefs: audience, message, CTA, word count, channel spec, compliance constraints, deadline
- Track production status across all active content tasks; flag late deliveries against campaign calendar
- Coordinate review routing: once content is created, route through Content Review Specialist → Compliance → final approval

### State-Variant & Legally Required Content
- Manage state-specific content variants: some pages and emails require different disclosures, rates, or product availability messaging by state
- Maintain state content variant registry: which content has state variants, what states each version is approved for
- Coordinate with Lead Compliance Officer when new state requirements trigger content updates
- Ensure dynamic content logic in ESP and CMS correctly routes state-appropriate content to consumers

### Content Quality Assurance
- Conduct final content review before publication or deployment:
  - All links functional and correctly targeted
  - Phone numbers and URLs current and correct
  - Offer codes and rate callouts match approved values
  - Compliance-required disclosures present and correctly formatted
  - Images render correctly with proper alt text
  - Content displays correctly on mobile and desktop (for web)
- Maintain a pre-publish checklist per content type (web page, email, landing page)

### Content Performance Review
- Monitor content performance in partnership with Marketing Reporting Specialist:
  - Landing page conversion rates: are active pages converting at expected rates?
  - Email content click-through by content type and topic
  - Time-on-page and scroll depth for educational content
- Recommend content updates based on performance data: update underperforming CTAs, refresh stale images, A/B test headline variants
- Conduct content audits annually: review all active web content for accuracy, freshness, and compliance

## Content Inventory Schema

| Field | Description |
|-------|-------------|
| Content ID | Unique identifier |
| Title | Consumer-facing title or internal name |
| Content Type | Page / Email Template / Landing Page / Disclosure / Component |
| Channel | Web / Email / Both |
| Status | In Production / Review / Approved / Active / Expiring / Retired |
| Compliance Approved | Yes/No + approval date |
| Compliance Expiry | Date requiring re-review |
| Approved States | States where this content is cleared for use |
| Owner | Content Manager / assigned owner |
| Last Updated | Date of last content change |
| CMS Location | URL or CMS node path |
| DAM Asset Link | Link to associated creative assets in DAM |

## Collaboration Interfaces

- **Marketing Campaign Manager**: Align content calendar to campaign calendar; report content readiness status
- **Marketing Creative Strategist**: Receive creative assets; coordinate integration of copy and design in CMS
- **Marketing Content Creation Specialist**: Brief and coordinate copywriting production
- **Marketing Content Review Specialist**: Route content through review workflow; track approvals
- **Lead Compliance Officer**: Gate publishing on compliance approval; manage re-review of expiring content
- **CMS/DAM Librarian**: Coordinate CMS publishing governance; ensure DAM assets are synchronized with CMS content
- **Website Developer**: Request CMS template changes; coordinate technical publishing issues
- **Email Channel Execution Lead**: Deliver email content ready for ESP build; confirm template versions are current
- **Marketing Technology Architect**: Coordinate CMS configuration changes, DAM/Content Hub workflow setup, and AI content generation integration

## AI-First Content Operations

The AI-First Content Operations Manager archetype (documented in the 2026 MarketingProfs recruiter research) is now the standard for this role. At NYLD Direct, "content manager" means managing **content at scale through AI-assisted production pipelines** — not just managing writers. Core competencies added for 2026:

### Prompt Library Governance
- Maintain the NYLD Direct content prompt library: curated, compliance-reviewed prompts for each content type (email acquisition, email nurture, DM letter, landing page, FAQ, social)
- Prompt structure standards: each prompt includes audience specification, reading-level constraint, prohibited language list, required disclosure triggers, brand voice instructions, and CTA framework
- Version-control prompts: when compliance requirements change (state-specific filings, new regulatory guidance), update the affected prompts and route the updated prompt through the same review cycle as the content it generates
- Train Content Creation Specialists on prompt library usage: which prompts to use for which use cases, how to customize within approved boundaries, and when to escalate prompt failures
- Document prompt performance: maintain a log of which prompts consistently produce compliant, on-brand output vs. which require heavy human revision (high revision rate = prompt needs improvement)

### AI-Generated Content Quality Governance
- Establish and enforce quality standards specific to AI-generated content at NYLD Direct:
  - **Compliance gate**: AI-generated copy routes through the same Content Review Specialist → Lead Compliance Officer workflow as human-written copy — no bypass for AI content
  - **Revision rate tracking**: track the ratio of AI draft accepted vs. requiring significant revision by content type; use as a proxy for prompt and tool effectiveness
  - **Reading level audit**: AI tools frequently drift above the Grade 6–8 Flesch-Kincaid target; audit monthly across content types
  - **Hallucination monitoring**: maintain a register of AI content errors specific to NYLD — incorrect coverage amounts, unavailable state offers, hallucinated product features, incorrect rate callouts — and update prompts and training examples to reduce recurrence
- Govern the use of AI-generated content in state-filed materials: some states require filed marketing materials; AI-generated content in those materials must be reviewed against the filing before deployment

### Multi-Format Content Repurposing Workflows
- Design and maintain workflows that repurpose long-form content into multi-channel formats via templated automation:
  - Email series → SMS drip adaptation
  - Long-form landing page → display ad variants (headline + 90 char description)
  - Feature article → social media post series
  - Product FAQ → IVR-ready language (Amazon Connect scripts)
- Own the format specification registry: what constraints apply to each channel (character limits, image ratios, compliance disclosure placement rules per format)
- Coordinate with the Marketing Journey Manager on content sequencing: the multi-format repurposing workflow must align to the journey stage — awareness content, consideration content, and intent content have different message hierarchies even when derived from the same source material

## Platform Environment — Sitecore Stack

| Platform | Role for Content Manager | Notes |
|---|---|---|
| Sitecore XM Cloud | Primary CMS | Headless CMS; content managed via structured content models; publishing workflow configured in XM Cloud |
| Sitecore Content Hub | DAM + content planning | Asset storage, metadata governance, content calendar, campaign planning board; replaces legacy DAM |
| Sitecore Personalize | A/B testing + personalization (Year 1+) | Website content variants; test setup coordinated with Campaign Manager |
| Sitecore CDP + Personalize | Journey personalization (Year 2) | Content manager provides personalized content variants mapped to journey stage; CDP delivers segment context |
| AI Content Generation (Year 2) | AI content generation | Integrated content draft generation; content manager governs prompt library and output quality standards |
| ESP (Year 2) | Email execution | Content manager delivers final email content packages to ESP templates |
