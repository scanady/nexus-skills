---
name: marketing-intel-customer-segmentation
description: 'Expert-level customer segmentation analysis using hybrid qualitative/quantitative methods. Builds data-driven segment personas grounded in statistical profiles, not archetypes. Use when asked to "segment customers", "identify customer segments", "build buyer personas", "customer clustering", "market segmentation", "audience segmentation", "TAM analysis", "ICP definition", "customer profiling", "segment sizing", "segment prioritization", or when needing to understand who to target for acquisition, retention, upsell, or product-market fit.'
---

# Customer Segmentation

## Purpose
Produce validated, data-driven customer segments with statistical personas, opportunity sizing, journey maps, and an operationalization plan — ready to drive marketing, sales, and product decisions at scale.

---

## Execution Logic

**Check $ARGUMENTS first to determine execution mode:**

### If $ARGUMENTS is empty or not provided:
Respond with:
"marketing-intel-customer-segmentation loaded. Provide your business context, customer data, or segmentation objective to begin."

Then wait for the user to provide their requirements in the next message.

### If $ARGUMENTS contains content:
Proceed immediately to Task Execution (skip the "loaded" message).

---

## Task Execution

When user requirements are available (either from initial $ARGUMENTS or follow-up message):

### 1. MANDATORY: Read Reference Files FIRST
**BLOCKING REQUIREMENT — DO NOT SKIP THIS STEP**

Before doing ANYTHING else, you MUST read every file in `./references/`. This is non-negotiable.

**DO NOT PROCEED** to Step 2 until you have read all reference files and have their content in context.

### 2. Check for Project Context
Check for project-level context files relevant to the task (e.g., `README.md`, `FOUNDER_CONTEXT.md`, docs in `references/`), then use that context to personalize the output.

### 3. Define the Segmentation Objective
Clarify the primary goal before any analysis. Ask the user (or extract from their input):

**Required inputs:**
- **Business objective:** What is the segmentation optimizing for? (acquisition, retention, upsell/cross-sell, product-market fit, pricing strategy, channel strategy, geographic expansion)
- **Current customer base:** B2B, B2C, or B2B2C? Approximate size? Revenue range?
- **Data availability:** What customer data exists? (CRM records, purchase history, behavioral/product analytics, survey data, firmographics, demographics, support tickets)
- **Decision context:** How will these segments be used? (campaign targeting, product roadmap, sales playbooks, pricing tiers, content strategy)

**If critical information is missing:** Ask up to 8 targeted diagnostic questions before proceeding. See [references/diagnostic-questions.md](references/diagnostic-questions.md) for the question bank.

**If the user has no data:** Shift to a research-driven approach using industry benchmarks, publicly available market data, and qualitative frameworks. Document all assumptions explicitly.

### 4. Gather and Assess Data
Evaluate available data across four dimensions:

| Dimension | Examples | Source |
|-----------|----------|--------|
| **Behavioral** | Purchase frequency, AOV, product mix, engagement depth, churn signals, feature usage | CRM, product analytics, purchase history |
| **Demographic/Firmographic** | Age, income, company size, industry, role, geography, tech stack | CRM, enrichment tools, surveys |
| **Psychographic** | Values, motivations, risk tolerance, decision style, brand affinity | Surveys, interviews, review mining |
| **Needs-based** | Jobs-to-be-done, pain points, desired outcomes, unmet needs | Interviews, support data, NPS verbatims |

**Data quality assessment:**
- Flag missing dimensions explicitly
- Note sample sizes and confidence levels
- Identify potential biases (survivorship bias, self-selection, recency)
- Recommend data enrichment where gaps exist

Refer to [references/data-collection-framework.md](references/data-collection-framework.md) for detailed guidance on data sources, collection methods, and quality standards.

### 5. Apply Hybrid Segmentation Method
Use a combined qualitative + quantitative approach. Never rely on a single method.

**Quantitative methods (select based on data availability):**
- **RFM Analysis** — Recency, Frequency, Monetary scoring for transactional segmentation
- **K-means / hierarchical clustering** — For multi-variable behavioral grouping
- **Latent class analysis** — For identifying unobserved subgroups
- **Decision tree segmentation** — For rule-based, interpretable splits
- **Cohort analysis** — For time-based behavioral patterns

**Qualitative methods (layer on top of quantitative):**
- **Jobs-to-be-done interviews** — Uncover purchase causality
- **Contextual inquiry** — Observe real usage/purchase behavior
- **Review and support ticket mining** — Extract language, pain points, triggers
- **Win/loss analysis** — Understand competitive decision factors

**Hybrid integration process:**
1. Start with quantitative clustering to identify natural groupings in data
2. Layer qualitative insights to explain WHY clusters behave differently
3. Validate that qualitative themes align with quantitative boundaries
4. Refine cluster boundaries using qualitative signals the data missed

See [references/segmentation-methods.md](references/segmentation-methods.md) for method selection criteria, implementation guidance, and worked examples.

### 6. Validate the Segments
Every segment MUST pass the **MASAD validation framework:**

| Criterion | Definition | Test |
|-----------|------------|------|
| **Measurable** | Segment size, purchasing power, and characteristics can be quantified | Can you assign a dollar value and count to this segment? |
| **Accessible** | Segment can be effectively reached through marketing and sales channels | Can you target them specifically in your channels? |
| **Substantial** | Segment is large and profitable enough to justify dedicated strategy | Does the revenue potential exceed the cost to serve? |
| **Actionable** | Segment differences drive meaningfully different strategies | Would you market, sell, or build differently for this segment? |
| **Durable** | Segment is stable enough to justify investment (not a temporary cohort) | Will this segment exist in 18+ months? |

**If a segment fails any criterion:** Merge it with an adjacent segment, split it differently, or discard it. Document the decision.

### 7. Build Statistical Personas (NOT Archetypes)
Each persona is a **statistical profile derived from cluster analysis**, not a marketing brainstorm.

**Every persona MUST include:**

| Component | Description | Example |
|-----------|-------------|---------|
| **Segment label** | Descriptive, data-grounded name | "High-frequency SMB Power Users" not "Marketing Mary" |
| **Size & value** | % of base, revenue contribution, growth trajectory | 22% of customers, 41% of revenue, growing 15% YoY |
| **Core job-to-be-done** | The primary outcome they hire your product/service to achieve | "Reduce manual reporting time from 8hrs/week to <1hr" |
| **Top 3-5 decision criteria** | Ranked factors that drive purchase decisions | 1. Time-to-value, 2. Integration depth, 3. Price per seat |
| **Preferred channels** | Where they discover, evaluate, and purchase — with data | 67% discover via peer referral, 80% evaluate on G2/Capterra |
| **Top objections** | Ranked barriers to purchase with frequency | "Too expensive for our stage" (cited by 43% of lost deals) |
| **Trigger events** | Specific events that initiate a purchase cycle | Series A funding, new VP of Ops hire, failed audit |
| **Behavioral signature** | Quantitative behavioral patterns unique to this segment | Avg 12 sessions/week, 3.2 integrations connected, 89% DAU/MAU |
| **Churn risk factors** | Leading indicators of attrition specific to this segment | Usage drop >40% in 14 days, support ticket spike |
| **Expansion signals** | Leading indicators of upsell/cross-sell readiness | Hitting seat limits, API call volume >80% of plan |

**Persona naming rules:**
- Use descriptive, functional labels — never fictional names or stock photo descriptions
- Lead with the defining behavioral or firmographic attribute
- Examples: "Enterprise Late Adopters", "High-Growth Mid-Market Consolidators", "Price-Sensitive Solo Operators"

See [references/persona-template.md](references/persona-template.md) for the complete output template.

### 8. Size and Prioritize by Opportunity
For each validated segment, calculate:

| Metric | Formula / Approach |
|--------|-------------------|
| **Total Addressable Market (TAM)** | Segment population × average revenue per account |
| **Serviceable Addressable Market (SAM)** | TAM filtered by reachability and product fit |
| **Current penetration** | Existing customers in segment ÷ SAM |
| **Growth trajectory** | Segment growth rate (historical + projected) |
| **Cost to acquire (CAC)** | Channel costs ÷ segment-specific conversion rates |
| **Lifetime value (LTV)** | Segment-specific retention × ARPU × margin |
| **LTV:CAC ratio** | Segment LTV ÷ Segment CAC |
| **Time to payback** | CAC ÷ monthly gross margin per customer |

**Prioritization matrix:**
Plot segments on a 2×2 of **Opportunity Size** (TAM × growth) vs. **Ease of Capture** (LTV:CAC × product fit). Prioritize:
1. **Core segments** — High opportunity, high ease → maximize investment
2. **Growth bets** — High opportunity, lower ease → invest selectively, test
3. **Harvest segments** — Lower opportunity, high ease → maintain efficiently
4. **Deprioritize** — Low opportunity, low ease → minimal investment

### 9. Map Segments to Journeys
For each priority segment, map the end-to-end customer journey:

**Journey stages:**
1. **Trigger** — What event initiates the buying process?
2. **Problem awareness** — How do they recognize and frame the problem?
3. **Solution exploration** — Where do they research? What do they search for?
4. **Evaluation** — What criteria do they compare on? Who is involved?
5. **Decision** — What tips the decision? Who has final authority?
6. **Onboarding** — What does successful activation look like?
7. **Value realization** — When do they experience the core value?
8. **Expansion** — What triggers upsell/cross-sell consideration?
9. **Advocacy / Churn** — What drives referral vs. attrition?

**For each stage, document:**
- Key actions the customer takes
- Questions they ask
- Content and channels they engage with
- Emotional state and confidence level
- Decision-makers and influencers involved
- Friction points and drop-off risks
- Your optimal intervention (message, channel, offer)

See [references/journey-mapping-template.md](references/journey-mapping-template.md) for the full mapping framework.

### 10. Create the Operationalization Plan
Segments are worthless unless they're embedded in systems and workflows.

**Scoring and classification:**
- Define a **segment classification model** — rules-based or ML-based scoring that assigns every customer/prospect to a segment
- Specify input variables, weights, and thresholds
- Define confidence scores and handling for ambiguous cases
- Plan for re-scoring frequency (real-time, daily, weekly)

**System integration:**
- CRM: segment field on account/contact records, automated assignment
- Marketing automation: segment-specific nurture tracks, dynamic content
- Sales: segment-specific playbooks, talk tracks, objection handling
- Product: segment-specific onboarding flows, feature flagging
- Analytics: segment as a primary reporting dimension

**Governance:**
- Quarterly segment review cadence
- Trigger conditions for segment refresh (market shift, product pivot, data drift)
- Ownership: who maintains the segmentation model?
- Measurement: segment-level KPIs and dashboards

See [references/operationalization-checklist.md](references/operationalization-checklist.md) for the implementation blueprint.

### 11. Format and Verify
- Structure output according to **Output Format** section
- Complete **Quality Checklist** self-verification before presenting output

---

## Writing Rules
Hard constraints. No interpretation.

### Core Rules
- Every segment must be grounded in data or clearly documented assumptions — never intuition
- Personas are statistical profiles, NOT fictional characters with names like "Marketing Mary"
- Zero generic segmentation. Every output must be specific to THIS business and market.
- Quantify everything possible: sizes, percentages, dollar values, growth rates
- Active voice only. No hedging language ("might", "could potentially").
- When data is unavailable, state the assumption explicitly and flag confidence level (High / Medium / Low)
- Every recommendation must be actionable — specify what to do, not just what to think about

### Specificity Rules
- **BAD:** "This segment values quality"
- **GOOD:** "This segment's top decision criterion is implementation speed (cited by 62% in win/loss analysis), followed by native integration count (cited by 48%)"

- **BAD:** "Target these customers with email"
- **GOOD:** "Deploy a 5-touch nurture sequence triggered by the 'Series A announcement' signal, sent via email (72% open rate for this segment), with case study content featuring similar-stage companies"

- **BAD:** "This is a valuable segment"
- **GOOD:** "This segment represents 18% of the addressable market (~4,200 accounts), with an estimated LTV of $48,000, LTV:CAC of 5.2:1, and 12% current penetration — the highest-ROI growth opportunity"

### Data Integrity Rules
- Distinguish between observed data, inferred patterns, and assumptions
- Always state sample sizes when referencing survey or interview data
- Flag when a finding is based on <30 data points
- Never present modeled estimates as observed facts
- When using industry benchmarks, cite the source and year

---

## Output Format

The final deliverable follows this structure. Adapt depth per section based on data availability and user needs.

```markdown
# Customer Segmentation Analysis: [Company/Product Name]

## Executive Summary
- Segmentation objective: [objective]
- Method: [hybrid approach used]
- Segments identified: [count]
- Key finding: [single most important strategic insight]
- Primary recommendation: [highest-priority action]

---

## 1. Segmentation Objective & Methodology
- Business goal driving this segmentation
- Data sources used (with quality assessment)
- Methods applied (quantitative + qualitative)
- Key assumptions and limitations

## 2. Segment Definitions

### Segment [N]: [Descriptive Label]
**Size & Value:** [% of base] | [revenue contribution] | [growth rate]

**Statistical Profile:**
| Attribute | Value |
|-----------|-------|
| Core job-to-be-done | [specific outcome] |
| Decision criteria (ranked) | 1. [criterion] 2. [criterion] 3. [criterion] |
| Preferred channels | [channels with data] |
| Top objections | [objections with frequency] |
| Trigger events | [specific events] |
| Behavioral signature | [quantitative patterns] |
| Churn risk factors | [leading indicators] |
| Expansion signals | [leading indicators] |

**MASAD Validation:** [Pass/Fail per criterion with notes]

[Repeat for each segment]

## 3. Opportunity Sizing & Prioritization

| Segment | TAM | SAM | Penetration | LTV | CAC | LTV:CAC | Priority |
|---------|-----|-----|-------------|-----|-----|---------|----------|
| [name] | $X  | $X  | X%          | $X  | $X  | X:1     | Core / Growth / Harvest / Deprioritize |

**Prioritization rationale:** [Explain ranking logic]

## 4. Segment Journey Maps
[Journey map per priority segment — see Step 9]

## 5. Operationalization Plan
- Scoring model specification
- System integration requirements
- Governance and refresh cadence
- Segment-level KPIs and measurement plan

## 6. Assumptions & Limitations
- Data gaps and their impact on confidence
- Assumptions made with confidence ratings
- Recommended next steps to validate
```

---

## References

**These files MUST be read before task execution (see Step 1):**

| File | Purpose |
|------|---------|
| `./references/segmentation-methods.md` | Deep-dive on quantitative and qualitative methods with selection criteria and worked examples |
| `./references/persona-template.md` | Complete statistical persona template with filled example |
| `./references/journey-mapping-template.md` | Full customer journey mapping framework with stage-by-stage guidance |
| `./references/operationalization-checklist.md` | Implementation blueprint for embedding segments into systems and workflows |
| `./references/data-collection-framework.md` | Data source taxonomy, collection methods, and quality standards |
| `./references/diagnostic-questions.md` | Question bank for gathering segmentation inputs when information is missing |
| `./references/industry-benchmarks.md` | Benchmark data and research references for common segmentation scenarios |

**Why these matter:** The reference files provide the methodological depth, templates, and research-backed frameworks that transform this from a generic segmentation exercise into a rigorous, implementable analysis. The methods guide ensures the right analytical approach is selected. The templates ensure output consistency and completeness. The benchmarks provide grounding when primary data is limited.

---

## Quality Checklist (Self-Verification)
Before finalizing output, verify ALL of the following:

### Pre-Execution Check
- [ ] I read all reference files before starting
- [ ] I have the reference content in context
- [ ] Segmentation objective is clearly defined and agreed with user

### Execution Check
- [ ] Segments are derived from data/analysis, not invented archetypes
- [ ] Hybrid method was applied (both quantitative and qualitative elements)
- [ ] Every segment passes MASAD validation (Measurable, Accessible, Substantial, Actionable, Durable)
- [ ] Personas contain ALL required components (JTBD, decision criteria, channels, objections, triggers, behavioral signature, churn risks, expansion signals)
- [ ] No persona uses a fictional name or stock description
- [ ] Opportunity sizing includes TAM, SAM, penetration, LTV, CAC, LTV:CAC for each segment
- [ ] Prioritization matrix is applied and justified
- [ ] Journey maps cover all stages for priority segments
- [ ] Operationalization plan includes scoring model, system integration, and governance

### Output Check
- [ ] Output matches the Output Format structure
- [ ] All numbers are sourced (data) or flagged (assumption with confidence level)
- [ ] Specificity rules are followed — no generic statements
- [ ] Assumptions and limitations are documented
- [ ] Output is directly actionable for the stated business objective

**If ANY check fails → revise before presenting.**

---

## Defaults & Assumptions
Use these unless the user overrides:

- **Segment count target:** 4-7 segments (fewer than 4 is too coarse, more than 7 is operationally impractical)
- **Prioritization method:** 2×2 matrix of Opportunity Size vs. Ease of Capture
- **Validation framework:** MASAD (Measurable, Accessible, Substantial, Actionable, Durable)
- **Persona format:** Statistical profile (never fictional archetypes)
- **Journey stages:** 9-stage model (Trigger → Advocacy/Churn)
- **Confidence threshold:** Flag any finding based on <30 data points as low-confidence
- **Scoring approach:** Rules-based classification for <10K customers, ML-based for >10K
- **Refresh cadence:** Quarterly review, annual full refresh (unless market shift triggers earlier)
- **LTV:CAC minimum:** Segments below 3:1 are flagged as "requires investigation"
- **B2B default enrichment:** Firmographic (industry, size, stage, geography) + technographic (tech stack, tools used)
- **B2C default enrichment:** Demographic + behavioral + psychographic

Document any assumptions made in the output.
