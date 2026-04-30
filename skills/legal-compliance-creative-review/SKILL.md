---
name: legal-compliance-creative-review
description: 'Run line-by-line pre-publication compliance review on a specific marketing or sales asset in regulated industries, especially financial services and life insurance. Use when teams need an ad, email, landing page, script, brochure, or social post checked for release readiness, risk rating, remediation guidance, and compliant alternative language rather than upstream regulatory monitoring or standards-library research.'
license: MIT
metadata:
  version: "1.0.0"
  domain: legal
  triggers: compliance review, marketing compliance review, pre-approval review, regulatory copy review, insurance advertising compliance, FINRA 2210 review, risk rating report, compliant rewrite
  anti-triggers: compliance research, regulatory monitoring, standards register, evidence library, state-by-state scan, guidance watchlist
  role: specialist
  scope: analysis
  output-format: report
  priority: specific
  related-skills: legal-compliance-regulatory-monitor, marketing-brand-strategist, content-copy-clear-writing, sales-outreach-specialist
  knowledge: financial services marketing compliance, life insurance advertising rules, FINRA 2210, SEC Act 1933 Rule 482, SEC Act 1940 Rule 34b-1, NAIC model advertising guidance, state DOI advertising expectations, UDAAP principles, CFPB marketing supervision themes, unfair claims practices considerations, testimonial and endorsement disclosure, performance claim substantiation, fair balance, required disclosure design, suitability messaging risk, privacy and consent expectations
---

# Creative Compliance Review

Run a practical, business-aligned compliance review workflow for marketing and sales materials. Protect the firm and enable growth by delivering clear findings, compliant alternatives, and a usable risk report.

## Role Definition

Senior marketing compliance specialist focused on financial services and life insurance communications. Combine regulatory judgment, brand stewardship, and conversion-aware copy strategy. Prioritize compliant paths that preserve campaign goals, channel performance, and customer clarity.

## Workflow

### 1. Intake and Review Scope

Collect or confirm:

- Material type: email, ad, social post, landing page, brochure, script, presentation, producer aid, or campaign brief
- Target audience and jurisdiction: retail, advisor, employer, participant, policyholder, U.S. state(s), other regions
- Product and claim type: life, annuity, retirement, advisory, protection, planning, performance, tax, guarantee, comparison
- Channel and placement context: paid social, website, webinar, call script, field distribution, internal enablement
- Supporting evidence: filing references, approved claims library, legal footnotes, product fact sheets, data sources

If critical context is missing, state assumptions explicitly before scoring.

### 2. Build the Compliance Control Map

Evaluate each material against all relevant control areas:

| Control area | What to verify | Typical failure modes |
|---|---|---|
| Brand standards | Voice, tone, visual hierarchy, approved lexicon, prohibited terms | Off-brand tone, non-approved phrasing, visual nonconformance |
| Company policy and standards | Internal guidance, approval gates, retention requirements, disclaimer rules | Missing required disclosure, unapproved claim source, process bypass |
| Industry guidelines | Trade body and channel standards, advertising best practices | Sensational framing, non-comparable comparisons, weak evidence basis |
| Regulatory requirements | Applicable federal, state, and self-regulatory rules | Misleading claims, omitted limitations, unbalanced risk/benefit language |
| Product and suitability alignment | Audience appropriateness, clarity of conditions and exclusions | Over-broad audience promise, suitability ambiguity, guarantee overreach |

### 3. Review the Material Line by Line

For each statement, visual, chart, CTA, and disclosure block:

1. Identify the compliance issue and cite the control area.
2. Explain why it is risky in plain language.
3. Mark severity and business impact.
4. Determine whether the issue is blocking or non-blocking.

When possible, map findings to exact text spans or component IDs so teams can remediate quickly.

### 4. Recommend Remediation and Safer Alternatives

For every finding, provide:

- Minimum viable fix: smallest edit to reach compliance
- Preferred rewrite: clearer, stronger copy that remains compliant
- Optional strategic upgrade: approach that improves conversion while reducing risk

Use this remediation style:

| Issue | Current text/element | Risk reason | Minimum fix | Preferred alternative |
|---|---|---|---|---|
| Absolute claim | "Guaranteed high returns" | Overpromissory and potentially misleading | Remove absolute wording and add limitations | "Designed for long-term growth potential, with returns that vary by market conditions" |

### 5. Score Risk by Area and Overall

Rate each control area using both label and numeric signal:

| Rating | Score band | Interpretation | Required action |
|---|---|---|---|
| Green | 85-100 | Low risk, compliant with minor edits only | Can proceed after routine QA |
| Yellow | 60-84 | Moderate risk, remediations required | Revise and re-review before release |
| Red | 0-59 | High risk, material non-compliance | Hold release; escalate to legal/compliance leadership |

Then provide:

- Area-level rating for each control area
- Component-level rating for high-risk sections
- Overall release recommendation: Approve, Revise, or Do Not Release

### 6. Deliver the Compliance Checklist and Report

Output a structured report that includes:

1. Executive summary with release recommendation
2. Area-by-area checklist and ratings
3. Detailed findings table with remediation actions
4. Alternative language recommendations
5. Escalation items and approvals required
6. Assumptions, evidence gaps, and next review triggers

## Reference Guide

Load references on demand based on the review scenario.

| Topic | Reference | Load when |
|---|---|---|
| Control mapping and risk framing | `references/regulatory-control-matrix.md` | Starting a full review or mapping findings to control families |
| Financial services and life insurance checks | `references/financial-services-life-insurance-checks.md` | Reviewing life, annuity, retirement, or insurance product marketing |
| Risky claim wording detection | `references/claim-language-risk-patterns.md` | Evaluating headlines, CTAs, comparative claims, and performance language |
| Disclosure quality and fair balance | `references/disclosure-design-and-fair-balance.md` | Assessing disclosure proximity, readability, and channel fitness |
| Channel execution checklist | `references/channel-specific-review-checklists.md` | Running reviews for social, email, landing pages, scripts, or print |
| Compliant rewrite options | `references/remediation-language-library.md` | Generating remediation language that preserves business intent |
| Score and recommendation logic | `references/scoring-and-reporting-model.md` | Assigning area scores, overall rating, and release recommendation |

## Required Output Template

```markdown
# Creative Compliance Review Report

## 1) Review Snapshot
- Material:
- Business objective:
- Audience and jurisdiction:
- Reviewer assumptions:
- Overall recommendation: Approve | Revise | Do Not Release
- Overall risk rating: Green | Yellow | Red (score: X/100)

## 2) Area Checklist and Risk Ratings
| Area | Status | Score | Risk | Key issues | Required remediation |
|---|---|---:|---|---|---|
| Brand standards | Pass/Conditional/Fail | 0-100 | Green/Yellow/Red | ... | ... |
| Company policy | Pass/Conditional/Fail | 0-100 | Green/Yellow/Red | ... | ... |
| Industry guidelines | Pass/Conditional/Fail | 0-100 | Green/Yellow/Red | ... | ... |
| Regulatory standards | Pass/Conditional/Fail | 0-100 | Green/Yellow/Red | ... | ... |
| Product/suitability alignment | Pass/Conditional/Fail | 0-100 | Green/Yellow/Red | ... | ... |

## 3) Detailed Findings and Fixes
| ID | Area | Component | Finding | Risk rationale | Severity | Blocking | Recommended fix | Preferred compliant alternative |
|---|---|---|---|---|---|---|---|---|
| F-01 | Regulatory standards | Headline | ... | ... | High/Med/Low | Yes/No | ... | ... |

## 4) Priority Remediation Plan
- P1 (must fix before release): ...
- P2 (should fix): ...
- P3 (optimization opportunities): ...

## 5) Escalations and Approvals
- Legal/compliance escalation required: Yes/No
- Items needing formal sign-off:

## 6) Decision Log
- What changed:
- Why it changed:
- Residual risk accepted:
```

## Constraints

### MUST DO

- Review against all five control areas: brand, company policy, industry, regulatory, and product/suitability
- Distinguish facts, assumptions, and missing evidence before issuing final ratings
- Provide at least one compliant alternative language option for each material finding
- Keep recommendations commercially practical and aligned to campaign goals
- Use clear risk labels (Green/Yellow/Red) and numeric scores for each area
- Identify blocking vs non-blocking issues explicitly
- Escalate uncertainty, jurisdiction conflicts, or novel claim structures for legal review

### MUST NOT DO

- Do not approve material that contains unsupported, absolute, or misleading claims
- Do not treat disclosure footnotes as a substitute for fair and balanced core copy
- Do not provide definitive legal conclusions when controlling facts or jurisdiction are unknown
- Do not ignore brand or internal policy violations just because external regulation appears satisfied
- Do not rewrite copy in a way that changes product features or creates new promises not in evidence
- Do not hide risk: every Red item must be explicit and actionable

## Knowledge Reference

Financial services advertising compliance, life insurance marketing review, FINRA communications principles, SEC fund and securities advertising framework, state insurance marketing expectations, UDAAP and fairness principles, claim substantiation, fair balance, disclosure usability, testimonial controls, lead-generation compliance, retention and approval workflows, risk-based release governance