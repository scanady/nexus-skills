# Segmentation Methods Reference

Comprehensive guide to quantitative and qualitative segmentation methods. Use this to select the right approach based on data availability, business context, and analytical maturity.

---

## Method Selection Matrix

| Method | Data Required | Best For | Complexity | Interpretability |
|--------|--------------|----------|------------|-----------------|
| RFM Analysis | Transaction history | Quick behavioral segmentation, e-commerce, SaaS usage | Low | High |
| K-Means Clustering | Multi-variable numeric data | General-purpose behavioral/attitudinal grouping | Medium | Medium |
| Hierarchical Clustering | Multi-variable numeric data | Exploratory analysis, understanding segment relationships | Medium | High |
| Latent Class Analysis | Survey/categorical data | Unobserved subgroups from survey responses | High | Medium |
| Decision Tree Segmentation | Mixed data types | Rule-based, explainable segments | Medium | Very High |
| Cohort Analysis | Time-stamped behavioral data | Lifecycle-based patterns, retention analysis | Low-Medium | High |
| Gaussian Mixture Models | Multi-variable numeric data | Overlapping segments, soft clustering | High | Low |
| DBSCAN | Multi-variable numeric data | Finding natural clusters with noise handling | Medium | Medium |

---

## Quantitative Methods: Deep Dive

### RFM Analysis (Recency, Frequency, Monetary)

**When to use:** You have transaction data and need quick, actionable customer value segmentation.

**Variables:**
- **Recency:** Days since last purchase/engagement
- **Frequency:** Total transactions in a time period
- **Monetary:** Total spend in a time period

**Implementation:**
1. Pull transaction data for the analysis period (typically 12-24 months)
2. Calculate R, F, M values for each customer
3. Score each dimension 1-5 using quintile binning (equal-sized groups) or custom thresholds
4. Combine scores into segments

**Standard RFM Segments:**

| Segment | R Score | F Score | M Score | Strategy |
|---------|---------|---------|---------|----------|
| Champions | 5 | 5 | 5 | Reward, ask for referrals, early access |
| Loyal Customers | 3-4 | 4-5 | 4-5 | Upsell, loyalty programs, VIP treatment |
| Potential Loyalists | 4-5 | 2-3 | 2-3 | Onboarding optimization, engagement programs |
| Recent Customers | 5 | 1 | 1-2 | Welcome sequences, product education |
| Promising | 3-4 | 1-2 | 1-2 | Nurture, demonstrate value quickly |
| Need Attention | 3 | 3 | 3 | Personalized re-engagement, feedback collection |
| About to Sleep | 2-3 | 2-3 | 2-3 | Win-back campaigns, special offers |
| At Risk | 1-2 | 3-5 | 3-5 | Urgent retention — high value, disengaging |
| Can't Lose Them | 1 | 4-5 | 4-5 | Escalate to CS, executive outreach, save offers |
| Hibernating | 1-2 | 1-2 | 1-2 | Re-activation or graceful sunset |

**Limitations:**
- Only captures transactional behavior, not motivations
- Treats all products/categories equally
- Static snapshot — doesn't capture trajectory
- Must be layered with qualitative insights for persona development

---

### K-Means Clustering

**When to use:** You have multi-dimensional numeric data and want to discover natural behavioral groupings.

**Implementation steps:**
1. **Feature selection:** Choose 5-15 variables that differentiate customer behavior. Avoid highly correlated features.
2. **Data preparation:**
   - Standardize all variables (z-score normalization)
   - Handle outliers (cap at 99th percentile or log-transform)
   - Impute missing values or exclude records with >20% missingness
3. **Determine optimal K:**
   - Elbow method: Plot within-cluster sum of squares (WCSS) vs. K; look for the "elbow"
   - Silhouette score: Measure how similar each point is to its own cluster vs. others; maximize average silhouette
   - Business constraint: Typically 4-7 segments for operationalizability
4. **Run clustering:** Use K-means++ initialization (avoids poor random starts)
5. **Profile clusters:** Calculate mean/median of each variable per cluster; identify distinguishing characteristics
6. **Validate:** Hold out 20% of data and classify using nearest-centroid — check for stability

**Feature selection guidance for common scenarios:**

| Business Type | Strong Features | Weak Features |
|--------------|----------------|---------------|
| **SaaS B2B** | Feature usage depth, login frequency, seats utilized %, API calls, support tickets, contract value, expansion rate | Company name, signup date alone |
| **E-commerce B2C** | Purchase frequency, AOV, category mix, return rate, browse-to-buy ratio, discount sensitivity, channel mix | Email domain, browser type |
| **Marketplace** | Supply/demand ratio, transaction velocity, rating scores, response time, repeat transaction %, GMV | Registration date alone |

**Common pitfalls:**
- Using too many features (curse of dimensionality) — apply PCA if >15 variables
- Not standardizing variables — a revenue variable in thousands will dominate a frequency variable in single digits
- Ignoring the business context when selecting K — statistical optimum ≠ operational optimum
- Treating clusters as permanent — re-run quarterly with fresh data

---

### Hierarchical Clustering (Agglomerative)

**When to use:** Exploratory analysis where you want to understand the nested structure of customer groups. Excellent for visualizing segment relationships via dendrograms.

**Implementation:**
1. Calculate pairwise distance matrix (Euclidean for numeric, Gower for mixed data types)
2. Choose linkage method:
   - **Ward's method** (recommended default): Minimizes within-cluster variance — produces compact, even-sized clusters
   - **Complete linkage:** Uses maximum pairwise distance — produces compact clusters but sensitive to outliers
   - **Average linkage:** Uses mean pairwise distance — balances between single and complete
3. Build dendrogram and cut at the level that produces 4-7 segments
4. Profile and validate same as K-means

**Advantage over K-means:** Produces a hierarchy — you can see which segments are most similar and would merge first. Useful for creating "segment tier" structures (e.g., 3 macro-segments containing 7 micro-segments).

---

### Latent Class Analysis (LCA)

**When to use:** You have categorical or ordinal data (survey responses, preference data, behavioral flags) and want to identify unobserved subgroups.

**Implementation:**
1. Select 8-15 indicator variables (survey items, behavioral flags, categorical attributes)
2. Fit LCA models with 2, 3, 4, ... K classes
3. Select optimal K using BIC (Bayesian Information Criterion) — lower is better
4. Examine class-conditional probabilities to profile each latent class
5. Assign each customer a posterior probability of membership in each class

**Key advantage:** Handles categorical data natively (K-means requires encoding). Produces probabilistic assignments — a customer can be 70% Class A and 30% Class B, enabling nuanced targeting.

---

### Decision Tree Segmentation (CHAID / CART)

**When to use:** You need highly interpretable, rule-based segments that non-technical stakeholders can understand and implement.

**Implementation:**
1. Define target variable (e.g., high-value customer Y/N, churned Y/N, product tier)
2. Select predictor variables (mix of behavioral, demographic, firmographic)
3. Run CHAID (chi-square automatic interaction detection) or CART (classification and regression trees)
4. Prune tree to 4-7 terminal nodes (segments)
5. Each terminal node IS a segment, defined by the path of splits

**Example output:**
```
IF company_size > 200 employees
  AND industry IN (SaaS, FinTech, HealthTech)
  AND monthly_usage > 500 events
  THEN → "Enterprise Power User" segment (avg LTV: $120,000)

IF company_size <= 200 employees
  AND trial_to_paid_days < 7
  AND integrations_connected >= 2
  THEN → "Fast-Converting SMB" segment (avg LTV: $18,000)
```

**Key advantage:** Segments come with built-in classification rules — operationalization is trivial. Stakeholders can read the tree and immediately understand who belongs where.

---

### Cohort Analysis

**When to use:** You want to understand how customer behavior evolves over time and segment by lifecycle patterns rather than static attributes.

**Implementation:**
1. Define cohort dimension (signup month, first purchase month, acquisition channel, etc.)
2. Define metric to track (retention rate, cumulative revenue, feature adoption, etc.)
3. Build cohort table: rows = cohorts, columns = time periods
4. Identify cohorts with distinctly different trajectories
5. Investigate what differentiates high-performing vs. low-performing cohorts

**Segmentation application:** Cohorts with similar retention curves can be merged into behavioral segments. A "rapid adopter" cohort (high Day 7 retention) vs. "slow burner" cohort (low Day 7 but high Day 90 retention) suggests different onboarding needs.

---

## Qualitative Methods: Deep Dive

### Jobs-to-be-Done (JTBD) Interviews

**Purpose:** Uncover the causal mechanism behind purchases — what progress is the customer trying to make in their life/work?

**Interview structure (30-45 minutes):**
1. **Timeline mapping:** Walk through the entire purchase journey from first thought to final decision
2. **Push/pull forces:** What was pushing them away from the old solution? What pulled them toward the new one?
3. **Anxieties:** What almost stopped them from switching?
4. **Habits:** What comfortable habits did they have to give up?
5. **Hiring criteria:** What specific criteria made them "hire" this product?

**Key questions:**
- "Tell me about the moment you first realized you needed something different."
- "What were you using before? What wasn't working?"
- "Walk me through the day you actually decided to [sign up / buy / switch]."
- "What almost made you NOT go through with it?"
- "If I took this product away tomorrow, what would you do instead?"

**Segmentation application:** Group customers by the job they hired the product for, NOT by demographics. Two CFOs at similar companies might hire the same product for completely different jobs. The job IS the segment boundary.

**Sample size:** 12-20 interviews typically surfaces 80%+ of jobs. Continue until you hear the same stories repeated (saturation).

---

### Review and Support Ticket Mining

**Purpose:** Extract customer language, pain points, and decision criteria at scale from existing unstructured data.

**Implementation:**
1. **Collect:** Pull all reviews (G2, Capterra, TrustRadius, App Store), support tickets, NPS verbatims, sales call transcripts
2. **Code themes:** Tag each piece of feedback with:
   - Pain point mentioned
   - Use case / job described
   - Feature referenced
   - Sentiment (positive / negative / neutral)
   - Customer segment indicators (company size, role, industry if detectable)
3. **Frequency analysis:** Rank themes by frequency within each quantitative segment
4. **Language extraction:** Pull exact phrases customers use — these become messaging foundations

**Segmentation application:** Overlay theme frequencies onto quantitative clusters. If Cluster A mentions "reporting" 3x more than Cluster B, that's a qualitative differentiator that enriches the persona.

---

### Win/Loss Analysis

**Purpose:** Understand competitive decision dynamics — why customers chose you (or didn't).

**Implementation:**
1. Sample 15-25 recent wins AND 15-25 recent losses (stratified by segment if possible)
2. Conduct 20-minute structured interviews or surveys within 30 days of decision
3. Capture: decision criteria, alternatives evaluated, decisive factor, objections, timeline, buying committee

**Key questions:**
- "What were the top 3 criteria in your evaluation?"
- "Which alternatives did you seriously consider?"
- "What was the single most important factor in your final decision?"
- "What was your biggest concern about [our product]?"
- "Who else was involved in the decision? What were their priorities?"

**Segmentation application:** Different segments often have different win/loss patterns. Segment A might be won on price; Segment B on integrations. These differences validate that segments are truly distinct and drive different go-to-market strategies.

---

## Hybrid Integration: Putting It Together

### Recommended Workflow

```
Phase 1: Quantitative Foundation (Week 1-2)
├── Data collection and cleaning
├── Exploratory analysis (distributions, correlations)
├── Run primary clustering method (K-means or RFM)
├── Profile clusters statistically
└── Identify 4-7 preliminary segments

Phase 2: Qualitative Enrichment (Week 2-4)
├── Select 5-8 customers per preliminary segment for JTBD interviews
├── Mine reviews and support tickets for theme frequencies per segment
├── Conduct 10-15 win/loss interviews stratified by segment
└── Document qualitative themes per segment

Phase 3: Synthesis and Validation (Week 4-5)
├── Overlay qualitative themes onto quantitative clusters
├── Refine segment boundaries based on combined evidence
├── Run MASAD validation on each segment
├── Build statistical personas
└── Size and prioritize segments

Phase 4: Operationalization (Week 5-6)
├── Define classification rules / scoring model
├── Map segments to journeys
├── Create segment-specific playbooks
├── Integrate into systems (CRM, marketing automation, etc.)
└── Establish governance and refresh process
```

### Method Selection by Data Maturity

| Data Maturity | Available Data | Recommended Primary Method | Recommended Qualitative Layer |
|--------------|----------------|---------------------------|-------------------------------|
| **Low** (startup, <500 customers) | Basic transaction data, limited behavioral | RFM + manual review | JTBD interviews (15-20), review mining |
| **Medium** (growth, 500-10K customers) | Rich behavioral + some firmographic/demographic | K-means clustering | JTBD (20-30) + win/loss analysis + support mining |
| **High** (scale, >10K customers) | Multi-dimensional behavioral + enriched demographic + survey | Latent class analysis or ensemble (K-means + decision tree) | Large-scale survey + targeted interviews + full review corpus |
| **No primary data** | Industry reports, public data only | Needs-based framework + TAM modeling | Expert interviews + secondary research + competitive analysis |

---

## Statistical Validation Techniques

### Internal Validation
- **Silhouette score:** >0.5 = strong structure, 0.25-0.5 = reasonable, <0.25 = weak/overlapping
- **Calinski-Harabasz index:** Higher = better separation between clusters
- **Davies-Bouldin index:** Lower = better — measures average similarity between clusters

### External Validation
- **Stability test:** Run clustering on 80% random samples 10 times — segments that appear consistently are robust
- **Predictive validation:** Use segment membership to predict a held-out outcome (churn, LTV tier) — if segments predict behavior, they're capturing real differences
- **Business validation:** Present segments to sales, CS, and product teams — they should say "yes, we see this in practice"

### Minimum Sample Sizes
- **K-means:** Minimum 10× the number of features × K (e.g., 10 features, 5 clusters → 500 minimum)
- **LCA:** Minimum 200-300 per class
- **JTBD interviews:** 12-20 for saturation
- **Win/loss analysis:** 15-25 per outcome (win/loss)
- **Survey-based segmentation:** 300+ respondents minimum for stable factors
