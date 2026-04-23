# Data Collection Framework

Taxonomy of data sources, collection methods, and quality standards for customer segmentation. Use this to assess what data is available, identify gaps, and plan enrichment.

---

## Data Dimension Taxonomy

### 1. Behavioral Data
What customers DO — observable actions and patterns.

| Data Point | Source | Collection Method | Quality Notes |
|-----------|--------|------------------|---------------|
| Purchase history (products, dates, amounts) | CRM, POS, billing system | Automated extraction | High reliability; check for duplicates |
| Product/feature usage | Product analytics (Amplitude, Mixpanel, Pendo) | Event tracking | Depends on instrumentation completeness |
| Engagement frequency (logins, sessions, time-on-platform) | Product analytics, web analytics | Event tracking | Define "active" consistently across systems |
| Content engagement (pages viewed, emails opened, webinars attended) | Marketing automation, CMS analytics | Event tracking | Email opens unreliable post-iOS 15; use clicks |
| Support interactions (tickets, calls, chat) | Help desk, CRM | Automated logging | Categorization quality varies; audit tags |
| Churn/renewal behavior | Billing system, CRM | Automated extraction | Define churn consistently (non-renewal vs. deactivation) |
| Referral activity | Referral program, CRM | Program tracking | Only captures formal referrals; misses organic |
| Trial/demo behavior | Product analytics, CRM | Event tracking + CRM | Critical for acquisition segmentation |
| Search behavior on your platform | Site search analytics | Search log analysis | Extract intent signals from queries |
| API usage | API gateway logs | Automated extraction | Strong signal for technical/integration segments |

### 2. Demographic / Firmographic Data
What customers ARE — attributes and characteristics.

#### B2C Demographics
| Data Point | Source | Collection Method | Quality Notes |
|-----------|--------|------------------|---------------|
| Age / age range | Registration, survey, enrichment | Self-reported or modeled | Self-reported may be inaccurate; ranges more reliable |
| Gender | Registration, survey | Self-reported | Offer non-binary options; don't infer |
| Location (city, state, country) | Registration, IP geolocation, billing | Automated + self-reported | IP geolocation is approximate (~80% city accuracy) |
| Income range | Survey, enrichment (Experian, Acxiom) | Self-reported or modeled | Sensitive; modeled data has ±20% accuracy |
| Education level | Survey, LinkedIn enrichment | Self-reported or enriched | Not always relevant; collect only if meaningful |
| Household composition | Survey, enrichment | Self-reported or modeled | Privacy-sensitive; use for consumer products |
| Device / technology profile | Web analytics, product analytics | Automated | Good proxy for tech sophistication |

#### B2B Firmographics
| Data Point | Source | Collection Method | Quality Notes |
|-----------|--------|------------------|---------------|
| Company size (employees) | Enrichment (ZoomInfo, Clearbit, LinkedIn) | API enrichment | Ranges are more reliable than exact numbers |
| Annual revenue | Enrichment, public filings | API or manual research | Private companies = estimates with ±30% accuracy |
| Industry / vertical | Enrichment, self-reported | API + manual validation | Use standard classification (NAICS/SIC) + custom tags |
| Funding stage / total raised | Crunchbase, PitchBook | API enrichment | Strong signal for growth-stage companies |
| Geography (HQ, offices) | Enrichment | API | HQ ≠ where decision-makers sit in distributed companies |
| Tech stack | Enrichment (BuiltWith, HG Insights, Slintel) | API enrichment | Shows technology sophistication and integration needs |
| Growth rate (headcount, revenue) | Enrichment, public data | API + calculated | YoY change is more useful than absolute number |
| Department structure | LinkedIn, company website | Manual + enrichment | Indicates who the buyers and users are |

### 3. Psychographic Data
What customers THINK and VALUE — attitudes, beliefs, motivations.

| Data Point | Source | Collection Method | Quality Notes |
|-----------|--------|------------------|---------------|
| Priorities / values | Customer surveys (quantitative) | Survey (Likert scale, MaxDiff, conjoint) | Requires 300+ responses for stable segments |
| Decision-making style | Surveys, interview analysis | Survey + qualitative coding | Risk tolerance, speed, consensus-seeking |
| Brand perception | NPS surveys, brand tracking | Survey | Track over time; single snapshots are noisy |
| Willingness to pay | Conjoint analysis, Van Westendorp | Survey (specialized) | Requires careful survey design; n>200 |
| Innovation adoption tendency | Survey (Rogers adoption framework) | Survey | Useful for product launch sequencing |
| Communication preferences | Survey, engagement data | Survey + behavioral | Behavioral data (clicks, channels) > self-reported |
| Goals and aspirations | JTBD interviews, open-ended survey | Qualitative → coded | Small sample; use for enrichment, not primary segmentation |

### 4. Needs-Based Data
What customers NEED — the jobs they're hiring solutions for.

| Data Point | Source | Collection Method | Quality Notes |
|-----------|--------|------------------|---------------|
| Core job-to-be-done | JTBD interviews | Structured interviews (n=15-25) | Gold standard for understanding purchase causality |
| Pain points (ranked) | Surveys, support data, review mining | Mixed methods | Triangulate across sources; any single source is biased |
| Desired outcomes | Interviews, NPS verbatims | Qualitative analysis | Extract from open-ended responses |
| Unmet needs | Competitive win/loss, churn interviews | Structured interviews | Lost customers and churned customers are richest source |
| Decision criteria | Win/loss analysis, conjoint | Mixed methods | Stated preferences ≠ revealed preferences; validate with data |
| Feature requests / wishlist | Product feedback, support tickets | Text analysis | Volume ≠ importance; weight by segment value |

---

## Data Quality Assessment Framework

Before running segmentation analysis, score each data source:

| Dimension | Score 1 (Poor) | Score 3 (Acceptable) | Score 5 (Strong) |
|-----------|---------------|---------------------|------------------|
| **Completeness** | <50% of records have this field | 50-80% populated | >80% populated |
| **Accuracy** | Known errors, outdated | Mostly correct, some staleness | Validated, fresh (<90 days) |
| **Consistency** | Different definitions across systems | Minor inconsistencies | Single definition, reconciled |
| **Granularity** | Too aggregated for segmentation | Usable but some signal loss | Individual-level, detailed |
| **Coverage** | Only captures a subset of customers | Covers most customers | Represents full customer base |

**Minimum threshold for segmentation:** Average score ≥ 3 across all dimensions for primary segmentation variables. Variables scoring <3 should be flagged as supplementary, not primary.

---

## Data Enrichment Playbook

When internal data has gaps, enrich from external sources:

### B2B Enrichment Stack

| Provider | Best For | Data Points | Cost Range |
|----------|---------|-------------|------------|
| **ZoomInfo** | Firmographics, contacts, intent | Employee count, revenue, tech stack, org charts, intent signals | $$$ |
| **Clearbit** | Real-time enrichment, technographics | Company data, employee data, tech stack | $$ |
| **6sense / Bombora** | Intent data (who's researching your category) | Buyer intent scores, topic-level signals | $$$ |
| **BuiltWith** | Technology stack identification | Detailed tech stack from web presence | $$ |
| **LinkedIn Sales Navigator** | Contact-level data, company insights | Job titles, company updates, connections | $$ |
| **Crunchbase** | Funding, growth stage, investors | Funding rounds, investors, acquisitions | $ |
| **G2 / TrustRadius** | Buyer intent from review sites | Category research, competitor comparisons | $$ |

### B2C Enrichment Stack

| Provider | Best For | Data Points | Cost Range |
|----------|---------|-------------|------------|
| **Experian / TransUnion** | Financial, demographic modeling | Income, household composition, credit behavior | $$$ |
| **Acxiom / Oracle Data Cloud** | Lifestyle, interests, purchase behavior | Purchase propensities, interests, media consumption | $$$ |
| **Fullcontact** | Identity resolution, social data | Social profiles, demographics, interests | $$ |
| **Quantcast / Lotame** | Audience insights, digital behavior | Website visitation, content consumption | $$ |

### Free/Low-Cost Sources

| Source | Data Available | Use Case |
|--------|---------------|---------|
| **LinkedIn (company pages)** | Headcount, growth rate, job postings | Company growth signals |
| **Crunchbase (free tier)** | Basic funding data | Startup/growth stage identification |
| **Google Trends** | Search interest over time | Market sizing, topic validation |
| **Census / BLS data** | Population, employment, economic data | B2C market sizing |
| **SEC filings** | Revenue, customer data for public companies | Enterprise segment research |
| **Job postings (Indeed, LinkedIn)** | Hiring signals, technology needs | Growth and tech stack signals |

---

## Data Collection Best Practices

### Survey Design for Segmentation

**Sample size requirements:**
- **Factor analysis / LCA:** Minimum 300 respondents (10:1 ratio of respondents to variables)
- **MaxDiff:** Minimum 200 respondents
- **Conjoint:** Minimum 200 respondents per segment
- **Open-ended coding:** 50+ responses per theme for quantification

**Question types for segmentation:**
| Question Type | Best For | Example |
|--------------|---------|---------|
| **MaxDiff (Best-Worst Scaling)** | Ranking priorities without forcing artificial differentiation | "Which of these is MOST important to you? LEAST important?" |
| **Conjoint analysis** | Understanding trade-offs and willingness to pay | Profile-based choice tasks with varying attributes |
| **Likert scales** | Measuring attitudes and agreement | "Rate your agreement: 1 (Strongly Disagree) to 7 (Strongly Agree)" |
| **Behavioral frequency** | Capturing self-reported behavior | "How often do you [action]? Daily / Weekly / Monthly / Never" |
| **Open-ended** | Capturing context, language, unstructured needs | "What's the biggest challenge you face with [domain]?" |

**Common survey mistakes to avoid:**
- Leading questions that bias toward desired answers
- Too many questions (>15 minutes = completion drop-off)
- Double-barreled questions (asking two things at once)
- Missing "not applicable" or "other" options
- Sampling only current customers (survivorship bias)

### Interview Protocol for JTBD

**Recruitment:**
- Sample 5-8 customers per preliminary quantitative segment
- Include recent purchasers (last 90 days) — memory is fresh
- Include churned customers — they reveal unmet needs
- Include non-customers who evaluated and chose a competitor

**Interview guide structure:**
1. **Background (5 min):** Role, context, current setup
2. **Timeline (15 min):** Walk through the purchase journey backwards from decision
3. **Forces (10 min):** Push, pull, anxiety, habit
4. **Criteria (5 min):** What mattered most? What almost stopped you?
5. **Outcome (5 min):** Did it do the job? What's still missing?

**Analysis approach:**
1. Transcribe interviews
2. Code for: jobs, circumstances, decision criteria, anxieties, alternatives
3. Cluster by job similarity (not demographic similarity)
4. Map qualitative clusters onto quantitative segments
5. Document where they align and where they diverge

---

## Data Privacy and Compliance

### Key Considerations
- **Consent:** Ensure data collection complies with GDPR, CCPA, and applicable regulations
- **Minimization:** Collect only data needed for segmentation — don't hoard "just in case"
- **Anonymization:** Segment analysis can use aggregated/anonymized data; personas should not be traceable to individuals
- **Third-party data:** Verify enrichment providers are compliant with relevant privacy regulations
- **Documentation:** Maintain a record of data sources, purposes, and retention policies

### Practical Guidelines
- Use aggregate statistics in persona profiles, never individual examples
- Store raw interview transcripts with consent documentation
- When using enrichment data, document the provider and their compliance certifications
- Segment labels and classification rules should work on attributes, not PII
- Allow customers to request what segment they're in and how they were classified (GDPR Art. 22)
