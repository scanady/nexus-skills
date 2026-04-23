# Lead Scoring Models

Scoring templates, example models by GTM motion, negative signals, and threshold calibration guidance.

---

## Fit Scoring (Explicit)

Fit = who they are. Score based on observable company and contact attributes.

### Company Attributes

| Attribute | Criteria | Points |
|-----------|----------|--------|
| Company size | 1–10 employees | +5 |
| | 11–50 | +10 |
| | 51–200 | +15 |
| | 201–1000 | +20 |
| | 1000+ | +15 (or +25 if enterprise-focused) |
| Industry | Primary target | +20 |
| | Secondary target | +10 |
| | Non-target | 0 |
| Revenue | Under $1M | +5 |
| | $1M–$10M | +10 |
| | $10M–$100M | +15 |
| | $100M+ | +20 |
| Geography | Primary market | +10 |
| | Secondary market | +5 |
| | Non-target | 0 |

### Contact Attributes

| Attribute | Criteria | Points |
|-----------|----------|--------|
| Job title | C-suite | +25 |
| | VP level | +20 |
| | Director | +15 |
| | Manager | +10 |
| | Individual contributor | +5 |
| Department | Primary buying dept | +15 |
| | Adjacent dept | +5 |
| | Unrelated | 0 |
| Seniority | Decision maker | +20 |
| | Influencer | +10 |
| | End user | +5 |

### Technology Attributes

| Attribute | Criteria | Points |
|-----------|----------|--------|
| Tech stack | Uses complementary tool | +15 |
| | Uses competitor | +10 (understands category) |
| | Uses tool you replace | +20 |
| Tech maturity | Modern SaaS stack | +10 |
| | Legacy stack | +5 |

---

## Engagement Scoring (Implicit)

Engagement = what they do. Score based on behavioral signals with time decay.

### High-Intent Signals

| Signal | Points | Decay |
|--------|--------|-------|
| Demo request | +30 | None |
| Contact sales form | +30 | None |
| Free trial signup | +25 | None |
| Pricing page visit | +20 | −5 per week |
| ROI calculator used | +20 | −5 per 2 weeks |
| Comparison page visit | +15 | −5 per week |
| Case study pages (2+) | +15 | −5 per 2 weeks |

### Medium-Intent Signals

| Signal | Points | Decay |
|--------|--------|-------|
| Webinar attendance | +15 | −5 per month |
| Webinar registration | +10 | −5 per month |
| Whitepaper download | +10 | −5 per month |
| Blog visits (3+ in a week) | +10 | −5 per 2 weeks |
| Email click | +5 per click | −2 per month |
| Email opens (3+) | +5 | −2 per month |
| Social media engagement | +5 | −2 per month |

### Low-Intent Signals

| Signal | Points | Decay |
|--------|--------|-------|
| Single blog visit | +2 | −2 per month |
| Newsletter open | +2 | −1 per month |
| Single email open | +1 | −1 per month |
| Homepage only | +1 | −1 per week |

### Product Usage Signals (PLG)

| Signal | Points | Decay |
|--------|--------|-------|
| Created account | +15 | None |
| Completed onboarding | +20 | None |
| Core feature used 3+ times | +25 | −5 per month inactive |
| Invited team member | +25 | None |
| Hit usage limit | +20 | −10 per month |
| Exported data | +10 | −5 per month |
| Connected integration | +15 | None |
| Daily active 5+ days | +20 | −10 per 2 weeks inactive |

---

## Negative Scoring

Apply automatically. Don't skip — bad signals inflate pipeline.

| Signal | Points | Notes |
|--------|--------|-------|
| Competitor email domain | −50 | Auto-flag for review |
| Student email (.edu) | −30 | May still be valid; review case-by-case |
| Personal email (gmail, yahoo) | −10 | Less relevant for B2B; adjust for SMB |
| Unsubscribe | −20 | Reduce engagement score |
| Hard bounce | −50 | Remove from scoring |
| Spam complaint | −100 | Remove from all sequences |
| Title: Student / Intern | −25 | Low buying authority |
| Title: Consultant | −10 | May be evaluating for client |
| No site visit in 90 days | −15 | Decay signal |
| Invalid phone | −10 | Data quality flag |
| Careers page only | −30 | Likely job seeker |

---

## Example Models by GTM Motion

### Model 1: PLG SaaS (ACV $500–$5K)

**Weight: 30% fit / 70% engagement**

Fit:
- Company 10–500: +15
- Target industry: +10
- Manager+ role: +10
- Complementary tool: +10

Engagement:
- Created account: +15
- Completed onboarding: +20
- Core feature 3+ times: +25
- Invited team member: +25
- Hit usage limit: +20
- Pricing page: +15

Negative: personal email −10, no login 14 days −15, competitor domain −50

**MQL threshold: 60 points. Recalibrate monthly.**

---

### Model 2: Enterprise Sales-Led (ACV $50K+)

**Weight: 60% fit / 40% engagement**

Fit:
- Company 500+: +20
- Revenue $50M+: +15
- Target industry: +15
- VP+ title: +20
- Decision maker confirmed: +15
- Uses competitor: +10

Engagement:
- Demo request: +30
- Multiple stakeholders engaged: +20
- Executive webinar attendance: +15
- ROI guide download: +10
- Pricing page 2+: +15

Negative: company <100 −30, individual contributor only −15, competitor domain −50

**MQL threshold: 75 points. Recalibrate quarterly.**

---

### Model 3: Mid-Market Hybrid (ACV $5K–$25K)

**Weight: 50% fit / 50% engagement**

Fit:
- Company 50–1000: +15
- Target industry: +10
- Manager–VP title: +15
- Target geography: +10
- Complementary tool: +10

Engagement:
- Demo request or trial signup: +25
- Pricing page: +15
- Case study download: +10
- Webinar attendance: +10
- Email engagement (3+ clicks): +10
- Blog visits (5+ pages): +10

Negative: personal email −10, no engagement 30 days −10, competitor domain −50, student/intern −25

**MQL threshold: 65 points. Recalibrate quarterly.**

---

## Threshold Calibration

### Setting Initial Threshold

1. Pull closed-won data — last 6–12 months
2. Retroactively score each deal using new model
3. Find natural breakpoint — what score separated wins from losses?
4. Set threshold just below score where 80% of closed-won deals qualified
5. Validate against closed-lost — if many closed-lost score above threshold, tighten

### Calibration Cadence

| GTM Motion | Frequency | Why |
|------------|-----------|-----|
| PLG / high volume | Monthly | Fast feedback loop, large data set |
| Mid-market | Quarterly | Moderate cycle length |
| Enterprise | Quarterly–semi-annually | Long cycles, small sample |

### Calibration Steps

1. Pull MQL-to-closed data for calibration period
2. Compare outcomes:
   - High score + closed-won → correctly scored
   - High score + closed-lost → false positive → tighten
   - Low score + closed-won → false negative → loosen
3. Adjust attribute weights based on actual correlation with wins
4. Raise threshold if MQL volume too high; lower if too few MQLs
5. Document all changes + communicate to sales team

### Warning Signs Model Needs Recalibration

- MQL-to-SQL acceptance rate below 30%
- Sales consistently rejects MQLs as "not ready"
- High-scoring leads don't convert; low-scoring leads do
- MQL volume spikes without revenue uplift
- New product launch or market shift since last calibration
