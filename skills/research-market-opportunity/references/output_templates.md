# Output Templates

Use these templates to package opportunity research into decision-ready outputs. Default to the Ranked Opportunity Scan unless the user requests a different format.

## Ranked Opportunity Scan

```markdown
# Opportunity Research Scan — [Theme or Scope]

**Date:** [Current Date]
**Research window:** [Last 7/30/90 days or custom]
**Focus:** [software / AI / embedded / ESP32 / domain]
**Source mix:** [X sources across news, startup, research, communities, embedded ecosystems]

## 1. Search Frame
[What was researched, why, and any constraints or assumptions.]

## 2. Signal Summary
| Signal | Type | Source / Date | Opportunity Implication |
|--------|------|---------------|-------------------------|
| [Signal] | Technology / customer pain / market / platform / regulation | [source] | [what it suggests] |

## 3. Ranked Opportunity Shortlist

### 1. [Opportunity Name]
**Short thesis:** [One-sentence opportunity thesis]
**Target customer:** [specific buyer/user]
**Pain / job:** [current workaround, frequency, severity]
**Why now:** [technical, regulatory, cost, platform, behavioral, or market shift]
**Distinctive wedge:** [non-obvious angle, distribution, data, workflow, embedded, or integration advantage]
**Solution shape:** [software product, workflow, service-plus-software, embedded device + cloud, data product]
**Embedded / ESP32 angle:** [None / optional / core — specify device role, sensor/control function, firmware/cloud split]
**Business model:** [subscription, usage, service, device + SaaS, data, licensing, marketplace]
**Evidence:**
- [Source-backed signal 1]
- [Source-backed signal 2]
**Confidence:** [High / Medium / Low]
**Biggest unknown:** [assumption that must be tested]
**Fast validation test:** [specific test and success threshold]
**Assessment handoff:** [Use strategy-planning-opportunity to score this if it fits portfolio goals.]

### 2. [Opportunity Name]
[Repeat compact structure]

## 4. Distinctiveness Check
| Opportunity | Why it is not generic | Main risk of being too obvious or crowded |
|-------------|------------------------|-------------------------------------------|
| [Name] | [distinctive element] | [risk] |

## 5. Recommended Next Steps
1. **Assess now:** [1–3 ideas best suited for strategy-planning-opportunity]
2. **Research deeper:** [ideas needing market or customer evidence]
3. **Park:** [interesting but not timely or not aligned]
4. **Discard:** [weak ideas and why]
```

## Opportunity Brief

Use this when the user wants one fully developed idea from the research.

```markdown
# Opportunity Brief — [Opportunity Name]

## Thesis
[One paragraph explaining the opportunity and why now.]

## Source Signals
| Signal | Source / Date | Interpretation |
|--------|---------------|----------------|
| [Signal] | [source] | [why it matters] |

## Customer and Pain
- **Customer:** [specific buyer/user]
- **Current workaround:** [what they do today]
- **Pain intensity:** [High / Medium / Low + rationale]
- **Budget owner:** [who pays]

## Solution Concept
- **Product:** [what it does]
- **Workflow:** [where it fits]
- **Software architecture shape:** [app/API/dashboard/agent/data/workflow]
- **Embedded/ESP32 component:** [if applicable: device role, connectivity, firmware, cloud, dashboard]

## Distinctive Wedge
[Why this approach is novel, overlooked, or newly feasible.]

## Business Model
- **Revenue path:** [subscription / usage / service / device + SaaS / data / other]
- **Initial pricing hypothesis:** [rough range or pricing logic]
- **Expansion path:** [how it grows if it works]

## Risks and Unknowns
1. [Risk]
2. [Risk]
3. [Risk]

## Fast Validation Plan
- **Test:** [what to do]
- **Audience:** [who to test with]
- **Threshold:** [what result means continue]
- **Time/cost:** [rough range]

## Assessment Handoff
Use `strategy-planning-opportunity` next to produce a score, financial sketch, and grow/launch/pivot/kill recommendation.
```

## Embedded Opportunity Matrix

Use this for ESP32, IoT, edge AI, or sensor-heavy asks.

```markdown
# Embedded Software Opportunity Matrix — [Domain]

| Rank | Opportunity | Customer | Device Role | Software Revenue Layer | Why ESP32 / Edge | Confidence | Key Risk |
|-----:|-------------|----------|-------------|-------------------------|------------------|------------|----------|
| 1 | [Name] | [segment] | [sense/control/infer/gateway] | [SaaS/data/service] | [cost/power/connectivity/local] | [H/M/L] | [risk] |
| 2 | [Name] | [segment] | [role] | [layer] | [reason] | [H/M/L] | [risk] |

## Top Pick
[Name] — [why it is strongest]

## Validation Sequence
1. [Customer pain validation]
2. [Technical feasibility validation]
3. [Economics validation]
```

## Brief Idea List

Use when the user asks for quick ideas only.

```markdown
# Quick Opportunity Ideas — [Theme]

| Idea | Customer | Pain | Why Now | Distinctive Wedge | Confidence |
|------|----------|------|---------|--------------------|------------|
| [Idea] | [specific customer] | [pain] | [signal] | [wedge] | [H/M/L] |

**Best 3 to assess next:** [Idea 1], [Idea 2], [Idea 3]
```

## Evidence Labels

Use labels consistently:

- **Fact:** Directly supported by source.
- **Signal:** Observed pattern that may imply opportunity.
- **Inference:** Analyst interpretation of signals.
- **Assumption:** Unverified but necessary belief.
- **Idea:** Generated concept, not evidence.
