# Operationalization Checklist

Blueprint for embedding customer segments into systems, workflows, and decision-making processes. Segments that live only in a slide deck are worthless. This checklist ensures they drive real action.

---

## Phase 1: Segment Classification Model

### Define the Classification Approach

| Customer Base Size | Recommended Approach | Rationale |
|-------------------|---------------------|-----------|
| <1,000 | Manual rules + CRM fields | Low volume; rules are transparent and maintainable |
| 1,000-10,000 | Rules-based scoring model | Automatable, auditable, easy to adjust thresholds |
| 10,000-100,000 | ML classification (supervised) | Data volume supports model training; handles complexity |
| >100,000 | ML ensemble + real-time scoring | High volume demands automation; ensemble handles edge cases |

### Rules-Based Scoring Model Specification

**Template:**

```
SEGMENT: [Segment Name]
CLASSIFICATION RULES:

Rule 1: [Variable] [operator] [threshold]
  AND/OR
Rule 2: [Variable] [operator] [threshold]
  AND/OR
Rule 3: [Variable] [operator] [threshold]

CONFIDENCE SCORE:
- All rules match → High confidence (auto-assign)
- 2 of 3 rules match → Medium confidence (assign, flag for review)
- 1 of 3 rules match → Low confidence (do not assign, queue for manual review)

TIEBREAKER (if customer matches multiple segments):
- Priority order: [Segment A > Segment B > Segment C]
- OR: Assign to segment with highest confidence score
- OR: Assign to segment with highest revenue potential
```

**Example:**

```
SEGMENT: High-Growth Mid-Market Consolidators

CLASSIFICATION RULES:
Rule 1: company_size BETWEEN 200 AND 1000
  AND
Rule 2: funding_stage IN ('Series B', 'Series C', 'Pre-IPO')
  AND
Rule 3: integrations_connected >= 3
  AND
Rule 4: monthly_active_users / total_seats >= 0.60

CONFIDENCE SCORE:
- 4/4 rules → High (auto-assign)
- 3/4 rules → Medium (assign, flag)
- 2/4 rules → Low (manual review)
- 1/4 rules → Exclude

TIEBREAKER: Highest revenue per account wins
```

### ML-Based Classification Specification

**Model requirements:**
- **Type:** Multi-class classifier (Random Forest, XGBoost, or logistic regression)
- **Training data:** Manually labeled sample of 200+ customers per segment
- **Features:** Same variables used in cluster analysis + enriched attributes
- **Validation:** Stratified k-fold cross-validation (k=5), target >85% accuracy
- **Output:** Segment label + probability per segment (enables soft assignments)
- **Refresh cadence:** Retrain monthly or when accuracy drops below 80%

**Feature importance tracking:**
- Log feature importances at each retrain
- Alert when feature rankings shift significantly (possible data drift)
- Document which features are most predictive per segment

---

## Phase 2: System Integration

### CRM Integration

**Required fields:**
| Field | Type | Location | Update Mechanism |
|-------|------|----------|-----------------|
| `segment_primary` | Picklist | Account/Contact | Automated (scoring model) |
| `segment_confidence` | Picklist (High/Med/Low) | Account/Contact | Automated |
| `segment_date_assigned` | Date | Account/Contact | Automated |
| `segment_override` | Boolean | Account/Contact | Manual (by sales/CS) |
| `segment_override_reason` | Text | Account/Contact | Manual |

**Automation rules:**
- New accounts: Score and assign within 24 hours of creation
- Existing accounts: Re-score on a [daily/weekly] cadence
- Override protection: Manual overrides persist for 90 days, then re-evaluated
- Historical tracking: Log all segment changes with timestamps

**Views and reports:**
- Pipeline by segment
- Win rate by segment
- Revenue by segment (current + trajectory)
- Segment migration tracking (customers moving between segments)

### Marketing Automation Integration

**Segment-specific elements:**

| Element | Implementation |
|---------|---------------|
| **Email nurture tracks** | One nurture sequence per segment, triggered by segment assignment |
| **Dynamic content** | Email/landing page content blocks swap based on segment field |
| **Lead scoring** | Segment-specific scoring models (activities weighted differently per segment) |
| **Ad audiences** | Sync segment lists to ad platforms for targeted campaigns |
| **Content recommendations** | Map content library to segments; recommend based on assignment |

**Nurture track template:**

```
SEGMENT: [Segment Name]
TRIGGER: segment_primary = "[Segment Name]" AND lifecycle_stage = "Lead"
CADENCE: [Frequency — e.g., 2 emails/week for 4 weeks]

Touch 1 (Day 0): [Content type] — Addresses [primary pain point]
Touch 2 (Day 3): [Content type] — Demonstrates [core job-to-be-done] value
Touch 3 (Day 7): [Content type] — Social proof from [similar customers]
Touch 4 (Day 10): [Content type] — Handles [top objection #1]
Touch 5 (Day 14): [Content type] — [Trigger event]-relevant content
Touch 6 (Day 18): [Content type] — Handles [top objection #2]
Touch 7 (Day 21): [Content type] — Case study with [ROI proof point]
Touch 8 (Day 25): [Content type] — CTA to [next action — demo, trial, etc.]

EXIT CONDITIONS:
- Converts to opportunity → Move to sales sequence
- Unsubscribes or bounces → Remove
- No engagement after 8 touches → Move to re-engagement track
```

### Sales Enablement

**Segment-specific playbooks (one per segment):**

```markdown
## Sales Playbook: [Segment Name]

### Segment Profile Summary
[2-3 sentences — from persona]

### Ideal Discovery Questions
1. [Question targeting their core JTBD]
2. [Question surfacing their trigger event]
3. [Question about current solution and pain]
4. [Question about decision process and timeline]
5. [Question about budget and buying authority]

### Value Proposition (Their Language)
"[Value prop framed in segment-specific terms]"

### Objection Handling
| Objection | Response | Proof Point |
|-----------|----------|-------------|
| "[Objection 1]" | [Response script] | [Case study / data point] |
| "[Objection 2]" | [Response script] | [Case study / data point] |
| "[Objection 3]" | [Response script] | [Case study / data point] |

### Competitive Positioning
| Competitor | Their Advantage | Our Counter |
|-----------|----------------|-------------|
| [Competitor A] | [What they lead with] | [Our differentiation] |
| [Competitor B] | [What they lead with] | [Our differentiation] |

### Demo Script Emphasis
- Lead with: [Feature/capability most relevant to this segment's JTBD]
- Show: [Specific use case they care about]
- Skip: [Features irrelevant to this segment]
- Close with: [Proof point that addresses their biggest risk]

### Pricing & Packaging
- Recommended package: [Package name]
- Typical deal size: $[range]
- Discount guidelines: [When/how much is acceptable]
- Negotiation leverage: [What matters more than price for this segment]
```

### Product Integration

**Segment-specific product experiences:**

| Element | Implementation |
|---------|---------------|
| **Onboarding flows** | Segment-specific setup wizards emphasizing their core JTBD |
| **Feature flagging** | Surface features most relevant to segment; de-emphasize others |
| **In-app messaging** | Segment-specific tooltips, walkthroughs, upgrade prompts |
| **Default configurations** | Pre-set defaults optimized for each segment's typical use case |
| **Success metrics** | Track segment-specific activation and value realization milestones |

### Analytics & Reporting

**Required dashboards:**

| Dashboard | Metrics | Audience |
|-----------|---------|----------|
| **Segment Health** | Size, revenue, growth rate, retention, NPS per segment | Executive |
| **Segment Acquisition** | Pipeline, conversion rate, CAC, velocity per segment | Marketing + Sales |
| **Segment Engagement** | Usage, feature adoption, engagement scores per segment | Product + CS |
| **Segment Economics** | LTV, CAC, LTV:CAC, payback period per segment | Finance + Strategy |
| **Segment Migration** | Customers moving between segments over time | Strategy |

---

## Phase 3: Governance

### Ownership

| Role | Responsibility |
|------|---------------|
| **Segmentation owner** (typically Strategy, Marketing Ops, or RevOps) | Maintains model, leads quarterly reviews, owns data quality |
| **Sales leadership** | Validates segments reflect real market dynamics, enforces playbook usage |
| **Marketing leadership** | Ensures campaigns align with segment strategy, measures segment-level ROI |
| **Product leadership** | Incorporates segment insights into roadmap, measures segment-level adoption |
| **Data/Analytics team** | Maintains scoring model, monitors data quality, detects drift |

### Review Cadence

| Cadence | Activity | Participants |
|---------|----------|-------------|
| **Weekly** | Monitor segment-level KPIs, flag anomalies | Segmentation owner + analyst |
| **Monthly** | Review segment performance vs. targets, identify action items | Cross-functional leads |
| **Quarterly** | Full segment review — validate definitions, update personas, adjust strategy | All stakeholders |
| **Annual** | Complete segmentation refresh — re-cluster, re-validate, re-size | Strategy team + external data |

### Refresh Triggers

Re-run the full segmentation analysis (not just the quarterly review) when:

- [ ] Product pivot or major feature launch changes value proposition
- [ ] Market enters new segments (geographic expansion, new vertical)
- [ ] Customer base grows >50% since last segmentation
- [ ] Win rates shift >10 percentage points for any segment
- [ ] Merge/acquisition changes competitive landscape
- [ ] Scoring model accuracy drops below 80%
- [ ] Two consecutive quarters of segment migration >15% of base

### Data Quality Standards

| Metric | Standard | Measurement |
|--------|----------|-------------|
| **Segment assignment coverage** | >95% of active accounts have a segment | Weekly audit |
| **Classification confidence** | >70% of accounts at "High" confidence | Weekly audit |
| **Data freshness** | Scoring inputs updated within 7 days | Automated monitoring |
| **Override rate** | <10% of accounts have manual overrides | Monthly review |
| **Accuracy validation** | >85% agreement between model and manual review (sample of 50) | Quarterly |

---

## Implementation Timeline Template

```
Week 1-2: Foundation
├── [ ] Finalize segment definitions and classification rules
├── [ ] Create CRM fields and picklists
├── [ ] Score and assign all existing accounts
├── [ ] Build segment health dashboard

Week 3-4: Marketing Activation
├── [ ] Build segment-specific nurture tracks
├── [ ] Configure dynamic content rules
├── [ ] Set up segment-based ad audiences
├── [ ] Adjust lead scoring models per segment

Week 5-6: Sales Enablement
├── [ ] Create segment playbooks
├── [ ] Train sales team on segment recognition and playbook usage
├── [ ] Configure CRM views and reports per segment
├── [ ] Set up segment-based pipeline reporting

Week 7-8: Product & CS
├── [ ] Configure segment-specific onboarding flows
├── [ ] Set up in-app messaging rules
├── [ ] Create CS playbooks per segment
├── [ ] Configure churn risk alerts per segment

Week 9-10: Measurement & Optimization
├── [ ] Validate segment assignments (sample audit)
├── [ ] Establish baseline KPIs per segment
├── [ ] Set up automated monitoring and alerts
├── [ ] Document governance process and assign ownership
```

---

## Common Operationalization Failures

| Failure | Root Cause | Prevention |
|---------|-----------|------------|
| Segments live in a slide deck, never used | No system integration | Start with CRM fields in Week 1 |
| Sales ignores segments | Playbooks not practical enough | Co-create playbooks with top sellers |
| Segments go stale | No refresh process | Establish governance in Week 1 |
| Conflicting segment definitions across teams | No single owner | Assign segmentation owner before launch |
| Over-complex model nobody understands | Data science without business context | Use rules-based approach first; earn complexity |
| Manual overrides become majority | Classification model is wrong | Re-validate model, fix root cause |
