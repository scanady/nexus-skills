# Customer Segmentation

Build validated, data-driven customer segments that drive marketing, sales, and product decisions at scale. This skill produces statistical personas grounded in real data — not fictional archetypes — along with opportunity sizing, journey maps, and a plan to operationalize segments across your systems.

## Usage

```
/marketing-customer-segmentation

[describe your business, objective, and available data]
```

Or provide context directly:

```
/marketing-customer-segmentation We're a direct-to-consumer life insurance company selling simplified-issue term and whole life policies through an affinity partnership (similar to the New York Life AARP program). We have 850K active policyholders, a 78% lapse rate over 10 years, and need to reduce early-term lapse while identifying which prospect segments to prioritize for digital acquisition. We have application data, customer policy data, payment history, and call center logs, but no psychographic data. We want to build segments that are actionable for both marketing and retention teams.
```

## What You'll Get

A complete segmentation deliverable with six sections:

1. **Segmentation Objective & Methodology** — The business goal, data sources used, methods applied, and key assumptions
2. **Segment Definitions** — 4-7 validated segments, each with a statistical persona profile
3. **Opportunity Sizing & Prioritization** — TAM, LTV, CAC, and LTV:CAC per segment with a ranked priority matrix
4. **Segment Journey Maps** — End-to-end customer journey for each priority segment
5. **Operationalization Plan** — Scoring models, CRM integration, sales playbooks, and governance
6. **Assumptions & Limitations** — Transparent documentation of data gaps and confidence levels

## Example: Direct-to-Consumer Life Insurance

To make the process concrete, here's how it applies to a DTC life insurance company selling simplified-issue policies through an affinity partnership channel (think: New York Life's AARP Life Insurance Program).

### Step 1: Define Your Objective
The segmentation objective is dual: **reduce early-term policy lapse** (retention) and **prioritize prospect segments for digital acquisition** (acquisition). These are distinct but related — understanding why policyholders lapse informs which prospects to acquire in the first place.

### Step 2: Assess Your Data
The skill evaluates your available data across four dimensions:

| Dimension | DTC Life Insurance Examples |
|-----------|---------------------------|
| **Behavioral** | Policy purchase channel (web, phone, mail), premium payment method, payment frequency, lapse history, claims filed, call center interactions, website visits pre-purchase, quote-to-bind rate |
| **Demographic** | Age, gender, income range, zip code, homeownership, marital status, number of dependents, AARP membership tenure |
| **Psychographic** | Risk aversion level, financial literacy, trust in digital vs. agent channels, motivation for purchase (obligation vs. planning vs. fear) |
| **Needs-based** | Job-to-be-done — final expense coverage, income replacement, legacy/inheritance, mortgage protection, supplement employer coverage |

Gaps are flagged. For example, if psychographic data is thin, the skill recommends mining call center transcripts and claims correspondence for attitudinal signals, or fielding a policyholder survey.

### Step 3: Segment with a Hybrid Method
**Quantitative:** Cluster policyholders using variables like face amount, premium level, policy tenure, payment consistency, channel of acquisition, age-at-issue, and engagement signals (website logins, paperless enrollment, beneficiary updates). RFM analysis adapted for insurance: Recency of last premium payment, Frequency of service interactions, Monetary value of annualized premium.

**Qualitative:** Layer in jobs-to-be-done from call center transcript analysis ("I just want to make sure my wife doesn't have to worry about the funeral"), complaint theme mining, lapse-reason surveys, and win/loss data from the quote-not-bound population.

**Result:** 5-6 segments emerge — not by age bracket, but by the intersection of *why they bought*, *how they engage*, and *how likely they are to persist*.

### Step 4: Validate Every Segment
Each segment is tested against the **MASAD framework**:

| Criterion | Example Validation for DTC Life Insurance |
|-----------|------------------------------------------|
| **Measurable** | "Obligation-Driven Final Expense Buyers" = 185K policyholders, $142M annual premium, avg face amount $12,500 |
| **Accessible** | Reachable via AARP direct mail co-op, Facebook/Meta age-targeted ads, and inbound phone |
| **Substantial** | $142M premium base with 14% lapse rate = $19.8M at-risk premium annually; retention intervention ROI-positive at >3% save rate |
| **Actionable** | This segment responds to simplicity and reassurance messaging, not rate comparisons — requires different creative than "Rate-Shopping Digital Comparers" |
| **Durable** | Final expense need is persistent and growing with aging population; segment stable across 5+ year horizon |

### Step 5: Build Statistical Personas
Here's a condensed example of one persona — the full output includes all components for every segment:

**Segment 2: Obligation-Driven Final Expense Buyers**

| Component | Profile |
|-----------|---------|
| **Size & value** | 22% of policyholders (185K), 26% of premium ($142M), avg premium $768/yr, 9.2-year avg policy duration |
| **Core job-to-be-done** | "Make sure my family isn't burdened with funeral costs — I don't want them to have to set up a GoFundMe" |
| **Decision criteria** | 1. No medical exam required (81%), 2. Monthly premium under $50 (74%), 3. Trusted brand / AARP endorsement (68%), 4. Immediate coverage (52%) |
| **Preferred channels** | 72% acquired via direct mail, 58% complete purchase by phone, 31% research online first but call to buy |
| **Top objections** | "I can't afford it on a fixed income" (47%), "I already have coverage through work" (23%), "I don't trust insurance companies" (18%) |
| **Trigger events** | Death of a friend/spouse, health scare, grandchild born, retirement/fixed-income transition, AARP membership renewal mailer |
| **Behavioral signature** | Pays monthly via bank draft, rarely logs into web portal, calls for any policy question, low digital engagement |
| **Churn risk factors** | Premium increase at renewal, bank draft failure (NSF), first 90 days post-issue (buyer's remorse window) |
| **Expansion signals** | Calls to ask about adding a spouse, requests coverage increase after grandchild, inquires about whole life conversion |

Note: This persona is labeled by its defining behavioral attribute — not "Grandma Betty." Every data point comes from policyholder records, call center analysis, and lapse surveys.

### Step 6: Size and Prioritize
Segments are sized by addressable market and scored on unit economics:

| Segment | Policyholders | Annual Premium | Lapse Rate | Est. LTV | CAC | LTV:CAC | Priority |
|---------|--------------|---------------|-----------|---------|-----|---------|----------|
| Obligation-Driven Final Expense | 185K | $142M | 14% | $5,400 | $380 | 14:1 | **Core** |
| Rate-Shopping Digital Comparers | 128K | $98M | 31% | $2,100 | $210 | 10:1 | **Growth** |
| Milestone-Triggered Income Replacers | 96K | $134M | 11% | $11,200 | $620 | 18:1 | **Core** |
| Legacy-Focused High-Net-Worth | 42K | $187M | 6% | $38,500 | $1,400 | 28:1 | **Core** |
| Employer-Supplement Gap Fillers | 210K | $89M | 28% | $1,800 | $190 | 9:1 | **Harvest** |
| Reluctant Obligation Purchasers | 189K | $72M | 42% | $980 | $350 | 2.8:1 | **Deprioritize** |

The "Reluctant Obligation Purchasers" have a 42% lapse rate and sub-3:1 LTV:CAC — better to reduce acquisition spend here and redirect to "Milestone-Triggered Income Replacers" where retention is strong and LTV is 6x higher.

### Step 7: Map Customer Journeys
Each priority segment gets a journey map. For "Obligation-Driven Final Expense Buyers," the journey looks different from "Rate-Shopping Digital Comparers":

| Stage | Final Expense Buyers | Digital Comparers |
|-------|---------------------|-------------------|
| **Trigger** | Friend's funeral, health scare, AARP mailer | Life event (marriage, baby), mortgage, ad comparison |
| **Research** | Reads AARP mailer, asks family/friends, maybe a Google search | Policygenius, NerdWallet, Google "best term life insurance" |
| **Evaluate** | Calls AARP/NYL phone number, asks about no-exam options | Runs online quotes across 5+ carriers, compares rates side-by-side |
| **Decide** | Agent on phone builds trust, "guaranteed acceptance" closes | Lowest rate wins unless reviews flag a carrier; binds online |
| **Onboard** | Needs bank draft setup help, confirmation call reassures | Self-serve, expects instant policy docs via email |
| **Retain** | Monthly statement, annual check-in call, payment reminder before NSF | Expects portal access, email-only communication, rate lock guarantee |

These journey maps drive specific interventions: the Final Expense segment needs a day-3 welcome call to prevent buyer's remorse lapse, while the Digital Comparer segment needs an instant-issue confirmation email with policy docs attached in under 60 seconds.

### Step 8: Operationalize
The output includes a classification model so every new policyholder and prospect is scored into a segment at the point of quote:

```
IF face_amount <= $25,000
  AND age_at_issue >= 55
  AND acquisition_channel IN ('direct mail', 'inbound phone')
  AND no_exam_product = TRUE
  THEN → "Obligation-Driven Final Expense Buyers" (Confidence: High)
```

Plus integration specs:
- **Policy admin system:** Segment field on every policy record, auto-assigned at issue
- **Marketing automation:** Segment-specific direct mail cadences, email nurture tracks, and digital retargeting audiences
- **Call center:** Segment-specific talk tracks and objection-handling scripts surfaced to agents at call pop
- **Retention:** Segment-specific lapse intervention triggers (e.g., NSF alert for Final Expense → immediate outbound call within 24 hours vs. email-only for Digital Comparers)
- **Quarterly review:** Re-cluster annually, monitor lapse rates by segment monthly, refresh personas when lapse patterns shift >5 percentage points

## What You'll Need to Provide

**At minimum:**
- What your business does and who you sell to
- What you want the segmentation to achieve
- What customer data you have access to

**For the best results, also share:**
- Policyholder data exports (policy records, premium history, lapse/surrender data, claims)
- Call center logs or transcripts
- Web analytics and quote funnel data
- Direct mail response rates by campaign
- Existing personas or segments (even if outdated)
- Competitive context (who are you losing to and where)
- Systems you use (policy admin, CRM, marketing platform, call center software)

**No data at all?** The skill shifts to a research-driven approach using industry benchmarks (LIMRA, NAIC, AM Best), public market data, and qualitative frameworks. All assumptions are documented explicitly.

## When to Use This Skill

| Scenario | What You'll Get |
|----------|----------------|
| "We need to grow new policy sales" | Acquisition segments with channel, message, and product-fit strategies |
| "Our lapse rate is too high" | Retention segments with lapse predictors and intervention playbooks by segment |
| "We want to sell more products per household" | Cross-sell segments with expansion signals and next-best-offer models |
| "We're launching a new product" | Product-market fit segments with needs analysis and willingness-to-pay |
| "We're expanding to a new channel" | Channel-fit segments with sizing, acquisition cost, and expected persistency |
| "We don't know which policyholders to invest in" | LTV-based segmentation with priority ranking and retention ROI by segment |
| "Our existing personas feel made up" | Replace archetype personas with data-grounded statistical profiles |

## Key Principles

- **Data over intuition.** Every segment is grounded in evidence. Assumptions are flagged with confidence levels.
- **Statistical personas, not archetypes.** No "Cautious Carol." Personas are named by their defining behavioral attribute: "Obligation-Driven Final Expense Buyers."
- **Hybrid methods.** Quantitative clustering finds the groups. Qualitative research (call transcripts, lapse surveys, claims data) explains why they're different.
- **Validation required.** If a segment can't pass MASAD, it doesn't ship.
- **Built to operationalize.** Segments include scoring models and system integration plans — not just a slide deck.
