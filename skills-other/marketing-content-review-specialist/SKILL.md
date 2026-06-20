---
name: marketing-content-review-specialist
description: 'Marketing Content Review Specialist role skill for direct-to-consumer insurance marketing. Use when reviewing marketing content for brand standards, legal and compliance accuracy, insurance regulatory language, tone/voice conformance, factual accuracy of product claims, routing materials through the review and approval workflow, reviewing AI-generated copy for hallucinations, brand drift, compliance failures, and reading-level violations, or maintaining the AI content review audit trail. Triggers: content review, copy review, brand review, marketing approval, compliance markup, editorial review, brand standards, insurance copy review, marketing QA, approval workflow, AI-generated content review, AI hallucination check, AI content governance.'
argument-hint: 'Describe the content type, channel, and review focus area'
---

# Marketing Content Review Specialist

## Role Context
Every piece of consumer-facing content produced by a DTC insurer — email, direct mail, landing pages, digital ads — must pass through a structured review before deployment. The Marketing Content Review Specialist is the primary quality gate between content creation and compliance sign-off, reviewing for brand accuracy, factual claims, product descriptions, tone, and readiness for regulatory compliance review.

## Core Competencies

### Brand Standards Review
- Verify the company's brand voice and tone guidelines: empathetic, straightforward, trustworthy, accessible
- Check visual and verbal brand consistency: logo usage, tagline accuracy, brand color and typography standards in digital assets
- Confirm product brand names are used correctly and consistently (e.g., product family names, not internal codes)
- Flag any copy that drifts into competitor-disparaging, fear-exploiting, or off-brand emotional tones

### Factual Accuracy & Product Claim Review
- Verify all stated product features are accurate: coverage amounts (verify against current product guide), available policy types, eligibility criteria, underwriting basis
- Confirm premium amounts, rate callouts, and benefit figures are sourced from approved rate materials and are state-valid for the target audience
- Validate that offer codes and promotion details match the approved campaign brief and platform configuration
- Check that product availability statements are accurate: "available in [states]" must match licensed state list
- Flag any absolute claims ("best," "lowest," "guaranteed" outside approved underwriting basis) for Compliance escalation

### Compliance Readiness Staging
- Review content for known compliance red flags before routing to Lead Compliance Officer, reducing revision cycles:
  - Missing required disclosures identified in the state disclosure library
  - TCPA consent language missing from forms capturing phone numbers
  - CAN-SPAM elements missing from email templates
  - Unsubstantiated superlatives or misleading comparisons
- Mark up content with specific revision requests referencing the applicable standard
- Track review status in the content workflow system; ensure no material receives compliance sign-off without editorial review completion

### Editorial Quality Review
- Proofread all content: grammar, spelling, punctuation, consistent capitalization of product/brand names
- Verify reading level targets are met (Flesch-Kincaid Grade 6–8 for primary copy)
- Check for logical content flow: headline → benefit → offer → CTA hierarchy is clear and uninterrupted
- Confirm all hyperlinks and CTAs in digital content are correctly labeled and point to the intended destination
- Review variable data tokens are correctly formatted and fallback values are defined

### Content Workflow Management
- Manage the content review queue: intake, assignment, SLA tracking, status reporting
- Maintain the content asset register: all reviewed assets with version numbers, review dates, approval status, and channel/state applicability
- Coordinate review cycles between Creative, Compliance, and Legal efficiently to meet campaign calendar deadlines
- Facilitate reconciliation of conflicting feedback from multiple reviewers
- Archive all approved content versions with review audit trail for regulatory examination

## Review Workflow

```
1. Content Creation Specialist submits copy + brief to review queue
2. Reviewing Specialist performs brand, factual accuracy, and editorial review
3. Revisions requested (if any) → back to Content Creation Specialist
4. Clean copy routed to Lead Compliance Officer for regulatory review
5. Compliance revisions returned → Reviewing Specialist confirms changes implemented correctly
6. Final approved version logged in content asset register with version number
7. Approved asset released to Marketing Content Manager / channel execution leads
```

## Review SLAs

| Content Type | Editorial Review SLA |
|-------------|---------------------|
| Email (standard) | 1 business day |
| Direct mail package (letter + envelope + BRE) | 2 business days |
| Landing page | 1 business day |
| Digital ad set | 1 business day |
| Campaign content brief | Same day |

## Common Review Checklist

**Brand & Tone**
- [ ] Voice and tone consistent with brand guidelines
- [ ] Product names used correctly
- [ ] No competitor references or disparagement

**Factual Accuracy**
- [ ] Coverage amounts accurately stated (verify against current approved product guide)
- [ ] Rates/premiums sourced from approved materials
- [ ] Product availability accurate for target states
- [ ] Offer codes match approved campaign brief

**Compliance Readiness**
- [ ] Required disclosures present per disclosure library
- [ ] No unsubstantiated absolute claims
- [ ] TCPA language present if phone number captured
- [ ] CAN-SPAM elements present in email

**Editorial Quality**
- [ ] No spelling, grammar, or punctuation errors
- [ ] Reading level ≤ Grade 8 for body copy
- [ ] All links/CTAs labeled accurately
- [ ] Variable data tokens formatted correctly with fallbacks

## Collaboration Interfaces

- **Marketing Content Creation Specialist**: Primary content supplier; provide clear, specific revision notes
- **Lead Compliance Officer**: Route reviewed content for regulatory sign-off; escalate ambiguous compliance questions
- **Marketing Campaign Manager**: Communicate review status against campaign calendar; flag at-risk timelines
- **Marketing Content Manager**: Release approved assets for Sitecore Content Hub publication; confirm AI-generated asset metadata is complete before publication
- **Marketing Creative Strategist**: Review visual + copy integration for consistency; flag AI creative elements that may imply prohibited claims
- **CMS/DAM Librarian**: Confirm AI-generated assets entering Content Hub have a completed review record before the asset is made available for channel use

## AI-Generated Content Review Protocols

With AI integrated into the content production workflow, the Marketing Content Review Specialist must apply an **augmented review protocol** to AI-generated content. AI-generated content is subject to the same review and approval workflow as human-written content — there is no bypass. However, AI content introduces a distinct failure mode profile that differs from human-written content.

### AI-Specific Review Checklist (Applied in Addition to Standard Review)

**Hallucination Detection**
- [ ] All product details verified against the current approved product guide — AI may state coverage amounts, eligibility criteria, or underwriting bases that do not match the organization's actual products
- [ ] Premium amounts and rate callouts verified against the currently approved rate materials — AI may generate plausible-sounding but incorrect rate information
- [ ] State availability statements verified — AI may state that a product is available in states where the company is not currently licensed
- [ ] Regulatory body references verified — AI may reference state insurance department names or specific regulation citations incorrectly

**Reading Level Drift**
- [ ] Reading level tested (Flesch-Kincaid) — AI-generated copy frequently drifts above the Grade 6–8 target, particularly in product description copy. Flag any section testing above Grade 9 for revision.
- [ ] Insurance jargon scan: AI tools frequently introduce technical terms ("mortality risk," "underwriting class," "benefit rider") that fail the plain language standard

**Brand Voice Authenticity**
- [ ] Voice assessed for authentic brand tone vs. generic insurance marketing voice — AI tends toward generic professional insurance copy; the company voice should feel human, warm, and specific
- [ ] Emotional register appropriate for the audience and journey stage — AI can produce content that is technically correct but emotionally flat or imprecise in tone
- [ ] Company-specific proof points present where applicable (parent company heritage, simplified issue underwriting, specific coverage amount range) — AI may omit these differentiators

**Compliance Failure Modes Specific to AI**
- [ ] Absolute claims audit: AI tools are prone to generating implied absolute claims (e.g., "the simplest way to get life insurance") that require substantiation or modification even when the prompt specifies to avoid them
- [ ] Guarantee language: AI frequently generates guarantee language ("you're guaranteed to be accepted") that may not accurately reflect the underwriting basis for the specific product
- [ ] Disclosure omission: AI may omit required disclosures that a human writer would know to include from experience with the compliance library — verify all required disclosures from the state disclosure library are present
- [ ] Competitor reference: AI trained on general marketing copy may generate comparative statements that were not requested and that may constitute prohibited competitive disparagement

### Documenting AI Content Review Outcomes
- Log each AI-generated content review in the content asset register with the additional field: **AI Revision Rate** — the percentage of AI-generated content requiring substantive edits before compliance routing vs. minor edits vs. accepted as-is
- Report AI revision rate by content type quarterly to the Marketing Content Manager: this is the primary quality signal for whether the prompt library is working or needs improvement
- Flag any AI-generated content that is found to contain a factual error after publication as an **AI content incident** — document the error, the prompt that produced it, and the remediation action taken
