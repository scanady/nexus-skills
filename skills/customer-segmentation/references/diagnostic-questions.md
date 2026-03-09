# Diagnostic Questions

Question bank for gathering segmentation inputs when information is missing. Use these to fill gaps before starting analysis. Ask a maximum of 8 questions — select only what's needed based on available context.

---

## Question Selection Logic

**Ask questions in priority order. Stop when you have enough to proceed.**

### Priority 1: Segmentation Objective (Always ask if unclear)
1. **"What business decision will this segmentation drive?"**
   - Follow-up options: acquisition targeting, retention strategy, pricing optimization, product roadmap, channel strategy, geographic expansion, upsell/cross-sell prioritization
   - *Why it matters:* The objective determines which variables to weight, which methods to use, and what "actionable" means

2. **"What does success look like? If this segmentation works perfectly, what changes in 90 days?"**
   - *Why it matters:* Grounds the analysis in a measurable outcome; prevents analysis paralysis

### Priority 2: Business Context (Ask if not provided)
3. **"Describe your business model: B2B or B2C? Product or service? What do you sell and to whom?"**
   - *Why it matters:* B2B vs. B2C changes every method choice — data types, variables, interview approaches, persona structures

4. **"How large is your current customer base? Approximate number of active customers and annual revenue?"**
   - *Why it matters:* Determines method complexity (rules-based vs. ML), sample sizes, and statistical feasibility

5. **"What is your current average deal size / ARPU / AOV? How does it vary?"**
   - *Why it matters:* Revenue distribution is a primary segmentation variable and determines segment economic viability

### Priority 3: Data Availability (Ask to scope the approach)
6. **"What customer data do you currently have access to? Check all that apply:"**
   - CRM records (accounts, contacts, opportunities)
   - Transaction/purchase history
   - Product usage / behavioral analytics
   - Website / content engagement data
   - Customer survey data
   - NPS scores and verbatim feedback
   - Support ticket data
   - Sales call recordings or notes
   - Win/loss data
   - Firmographic/demographic enrichment (ZoomInfo, Clearbit, etc.)
   - *Why it matters:* Data availability determines which methods are feasible and where assumptions are needed

7. **"How clean and complete is your data? Any known gaps, quality issues, or systems that don't talk to each other?"**
   - *Why it matters:* Prevents false confidence in analyses built on poor data; helps plan enrichment

### Priority 4: Market Context (Ask for deeper analysis)
8. **"Who are your top 3 competitors? How do customers typically choose between you?"**
   - *Why it matters:* Competitive dynamics shape decision criteria, which are central to personas

9. **"Describe your current customer base — who are your best customers? Who are your worst? Any patterns you've noticed?"**
   - *Why it matters:* Practitioner intuition is a useful starting hypothesis to validate or invalidate with data

10. **"Are there customer segments you've tried to serve but found unprofitable, difficult, or mismatched?"**
    - *Why it matters:* Identifies segments to exclude or deprioritize; prevents repeating known mistakes

### Priority 5: Operational Context (Ask for operationalization)
11. **"What systems do you use? (CRM, marketing automation, product analytics, help desk)"**
    - *Why it matters:* Determines what's possible for operationalization — scoring, targeting, dynamic content

12. **"Do you have existing segments or personas? If so, what's working and what's not?"**
    - *Why it matters:* Avoids reinventing what works; identifies specifically what needs improvement

13. **"Who will use these segments day-to-day? (Marketing, Sales, Product, CS, executives?)"**
    - *Why it matters:* Determines output format, complexity level, and which playbooks to create

---

## Question Selection by Scenario

### Scenario: User provides business context but no data
**Ask:** 6, 7, 1, 9
**Then:** Shift to research-driven approach with industry benchmarks

### Scenario: User provides data files/exports
**Ask:** 1, 2, 3, 8
**Then:** Proceed with quantitative analysis of provided data

### Scenario: User wants to validate existing segments
**Ask:** 12, 1, 6, 10
**Then:** Run MASAD validation on existing segments; identify gaps

### Scenario: User is starting from scratch (new product/market)
**Ask:** 3, 1, 8, 9, 6
**Then:** Build initial segmentation hypothesis from market research; plan primary data collection

### Scenario: User has a specific decision to make
**Ask:** 1, 2, 4, 5, 6
**Then:** Optimize segmentation for the specific decision; minimize scope

---

## Response Interpretation Guide

### Business Objective Mapping

| User Says | Segmentation Focus | Primary Variables |
|-----------|-------------------|------------------|
| "We need more customers" | Acquisition targeting | Channel preference, decision criteria, trigger events, ICP fit |
| "Our churn is too high" | Retention segmentation | Usage patterns, satisfaction, engagement depth, churn predictors |
| "We want to increase revenue per customer" | Upsell/cross-sell segmentation | Product usage, expansion signals, willingness to pay, wallet share |
| "We're launching a new product" | Product-market fit | Needs, JTBD, current solution gaps, willingness to switch |
| "We're expanding to a new market" | Market entry segmentation | Regional/vertical differences, competitive landscape, channel access |
| "We need to optimize pricing" | Price sensitivity segmentation | Willingness to pay, value perception, competitive alternatives, deal size distribution |
| "We don't know who our best customers are" | Customer value segmentation | LTV, engagement, advocacy, expansion potential |

### Data Maturity Assessment

| User Response to Q6/Q7 | Data Maturity Level | Recommended Approach |
|------------------------|--------------------|--------------------|
| "We have CRM + transactions + product analytics, mostly clean" | High | Full quantitative + qualitative hybrid |
| "We have CRM data but it's messy, some product analytics" | Medium | Focused quantitative (RFM or simple clustering) + qualitative |
| "Just basic customer lists and some survey data" | Low | Qualitative-led with simple quantitative overlay |
| "We're pre-product, no customer data yet" | None | Research-driven: TAM analysis, needs-based framework, competitor customer analysis |
