# Pricing Page

Load when user asks to design, audit, or test pricing page. General landing-page CRO → `marketing-seo-cro`.

## Contents

1. [Page job](#1-page-job)
2. [Layout spec](#2-layout-spec)
3. [Copy rules](#3-copy-rules)
4. [Price display](#4-price-display)
5. [Audit scorecard](#5-audit-scorecard)
6. [Test backlog](#6-test-backlog)

## 1. Page job

One job: right buyer clicks right plan CTA. Visitor already interested. Asks three things, in order:

1. Which plan is mine?
2. Worth it?
3. What's catch?

Each section answers one. Section answers none → cut.

## 2. Layout spec

Above fold, top to bottom:

| Element | Spec |
|---|---|
| Billing toggle | Monthly / annual above cards. Default annual if annual mix is goal. Savings as badge ("Save 20%" or "2 months free"). |
| Plan cards | 3 cards. 4 max with enterprise. |
| Per card | Segment name, price with unit and period, one-line "for who", 4-6 differentiators, one CTA. |
| Hero tier | Middle card. Badge, brand color or border, slightly taller, first CTA in tab order. |
| Enterprise | Card or row: "Custom" or "From $X", CTA to sales. |

```
[ Monthly | Annual  Save 20% ]

  Solo            Clinic  ★ Most teams     Group
  $29/mo          $89/mo                   $249/mo
  For one...      For clinics with...      For groups that...
  • ...           • ...                    • ...
  [Start trial]   [Start trial]            [Talk to us]
```

Below fold:

| Section | Spec |
|---|---|
| Comparison table | Every feature, grouped (Core, Collaboration, Reporting, Admin, Support). ✅ / — only. Sticky plan header. |
| Social proof | Logos and quotes matched to tier buyer. Real numbers only. |
| FAQ | 5-7 questions. Below. |
| Trust | Security badges (B2B), refund or cancel policy, "cancel anytime" stated. |
| Sales row | "Need custom terms or a demo?" + CTA. Say who qualifies (seat count, compliance). |

FAQ must cover:
- Cancel anytime? How?
- What happens at trial end?
- Switch plans? Proration?
- What happens at limit? (Hard stop or overage — say which.)
- Payment methods, invoice for annual.
- Data security, certifications.
- Need more than top plan?

## 3. Copy rules

Plan names map to buyer, not size.

| Generic | Better | Basis |
|---|---|---|
| Basic / Pro / Business | Solo / Clinic / Group | Customer type |
| Starter / Growth / Scale | Builder / Team / Company | Use stage |
| Individual / Team / Org | Creator / Collaborator / Admin | Role |

Vague segments → keep simple names. Clever name buyer cannot decode = worse than "Pro".

CTA by motion:

| Motion | CTA |
|---|---|
| Free trial | Start free trial |
| Freemium | Get started free |
| Direct buy | Get [Plan] |
| Sales-led | Talk to us / Book a demo |

Kill: "Sign up" (no value), "Subscribe" (newsletter feel), "Buy now" (pushy), "Learn more" (dead end on pricing page).

## 4. Price display

| Case | Show |
|---|---|
| Monthly | $89/month |
| Annual billed monthly | $74/month, billed annually |
| Annual upfront | $890/year (≈ $74/mo) |
| Per seat | $15/user/month |
| Usage | From $0.002 per call, with calculator |
| Enterprise | Custom, or From $X/year |

Rules:
- Unit and period always visible. "$89" alone = ambiguous.
- Never hide monthly price. Hidden price → distrust.
- Annual savings: show % or $, whichever looks bigger.
- Overage price on page if overage exists. Surprise overage = churn.
- Anchor: high tier visible first or alongside → middle looks reasonable. Decoy tier only if real buyers exist for it.

## 5. Audit scorecard

Score 0 (missing), 1 (weak), 2 (done well). 16 items, max 32.

| Area | Item |
|---|---|
| Above fold | Billing toggle. Savings shown. 3-4 distinct cards. Hero tier marked. CTA per card. |
| Content | Comparison table. FAQ 5+. Social proof. Enterprise / sales path. |
| Copy | Buyer-based names. Unambiguous price (unit, period, billing). Action CTAs. One-line positioning per plan. |
| Trust | Security badges (B2B). Refund or cancel policy. "Cancel anytime" explicit. |

Read: 28-32 strong → test specific elements. 20-27 solid base → fix weak items. Under 20 → rebuild with this spec.

## 6. Test backlog

Order by impact ÷ effort.

| Tier | Tests |
|---|---|
| Quick, high impact | Default toggle annual vs monthly. Hero badge placement. CTA copy. $/mo vs $/yr display. |
| Medium | Name style (segment vs feature). Bullets per card (3 vs 6). Social proof position. FAQ collapsed vs open. |
| Slow, high impact | Price points. 2 vs 3 tiers. Add or remove free tier. |

Traffic floor: ~500 visitors per variant per week for page tests. Price-point tests need more and longer. Low traffic → test price on new-customer cohorts over time, not split test. Run tests one at a time per page.
