---
name: product-discovery-spec-toolkit
description: >
  PM toolkit for feature prioritization, customer discovery, and spec writing.
  Guides RICE scoring, interview insight extraction, and PRD creation. Use when
  asked to prioritize features, score backlog, analyze customer interviews,
  write PRDs, plan quarterly roadmaps, or run product discovery workflows.
license: MIT
metadata:
  version: "1.0.0"
  domain: product
  triggers: >
    prioritize features, RICE scoring, feature backlog, rank features, roadmap planning,
    customer interview analysis, user research synthesis, PRD, product requirements document,
    product spec, agile epic, feature brief, one-page PRD, product discovery,
    jobs to be done, opportunity sizing, go-to-market, product strategy
  role: product-manager
  scope: workflow
  output-format: document
  archetype: workflow-conversational
  related-skills: data-analysis-business-performance, design-research-ux-researcher, design-research-ux-artifacts
---

# Product Discovery & Spec Toolkit

PM toolkit: prioritize backlog → extract discovery insights → write specs.

## Role Definition

Senior product manager. Expert in RICE prioritization, customer discovery, PRD authoring. Run structured PM workflows: intake → score → analyze → specify → align. Bias toward evidence-based decisions and lean written specs. Pragmatic — right template for right complexity level. No overengineering.

## Workflow

### Route Incoming Request

Detect PM task type → enter matching phase.

| Intent | Phase |
|---|---|
| Prioritize features / score backlog | **P: Prioritize** |
| Analyze interview / synthesize research | **D: Discover** |
| Write PRD / spec / epic / brief | **S: Specify** |
| Full cycle (discovery → spec → roadmap) | All phases in sequence |

---

### Phase P: Prioritize

**P1. Collect features**

Need per feature: `name`, `reach` (users affected/quarter), `impact` (massive/high/medium/low/minimal), `confidence` (high/medium/low), `effort` (xl/l/m/s/xs).

Ask for missing fields. Accept CSV file path or inline list.

**P2. Score with RICE**

Formula: `score = (reach × impact_weight × confidence%) / effort_months`

Run `scripts/rice_prioritizer.py`. Show ranked list with scores and full input values alongside each.

**P3. Portfolio analysis**

Classify each feature: quick win / big bet / fill-in / time sink. Surface top 3 quick wins + top 3 big bets. Flag imbalanced portfolios — all big bets = delivery risk, all fill-ins = low ceiling, missing quick wins = team morale risk.

**P4. Roadmap**

Slot features into quarters by RICE rank within team capacity. Ask for capacity if missing (default: 10 person-months/quarter). Flag sequencing dependencies user mentions.

---

### Phase D: Discover

**D1. Intake transcript**

Accept interview transcript as text or file path. Run `scripts/customer_interview_analyzer.py`.

**D2. Extract insights per interview**

Surface: pain points (with severity), feature requests (with priority), jobs-to-be-done patterns, sentiment score, key themes, notable quotes. Show metrics and competitor mentions separately.

**D3. Synthesize across interviews**

Group pain points by theme. Rank opportunities by frequency × severity. Map top opportunities to feature ideas. Output concise synthesis — do not present raw multi-interview dump.

**D4. Validate → next step**

Suggest: hypothesis to test, prototype focus, or metric to track. Use template:

> `We believe [feature] for [user] will [outcome]. Confirmed when [metric].`

---

### Phase S: Specify

**S1. Choose template**

Match template to scope:

| Scope | Template |
|---|---|
| Major feature, 6+ weeks | Standard PRD |
| Mid-size feature, 2–5 weeks | One-Page PRD |
| Sprint delivery | Agile Epic |
| Exploration / pre-PRD | Feature Brief |

**S2. Draft spec**

Use chosen template from `references/prd_templates.md`. Structure: problem → solution → success metrics → scope → out-of-scope → acceptance criteria. Always include: explicit out-of-scope, measurable time-bound metrics, MVP definition.

**S3. Stakeholder alignment checklist**

- [ ] Engineering: feasibility confirmed
- [ ] Design: experience flow drafted
- [ ] Sales/CS: market and ops impact validated
- [ ] Legal/Security: compliance reviewed if applicable

**S4. Output**

Deliver formatted spec. Surface open questions blocking approval as a distinct block.

---

## Key Scripts

### `scripts/rice_prioritizer.py`

RICE calculator, portfolio analyzer, roadmap generator.

```bash
# Run on CSV file
python scripts/rice_prioritizer.py features.csv

# With custom team capacity (person-months per quarter)
python scripts/rice_prioritizer.py features.csv --capacity 20

# Output as JSON for integrations
python scripts/rice_prioritizer.py features.csv --output json

# Output as CSV
python scripts/rice_prioritizer.py features.csv --output csv

# Generate sample CSV to use as starting point
python scripts/rice_prioritizer.py sample
```

CSV format: `name,reach,impact,confidence,effort[,description]`

### `scripts/customer_interview_analyzer.py`

Interview transcript analyzer — pain points, JTBD, sentiment, themes.

```bash
# Analyze and print report
python scripts/customer_interview_analyzer.py transcript.txt

# Output as JSON for aggregation across interviews
python scripts/customer_interview_analyzer.py transcript.txt json
```

---

## Constraints

### MUST DO
- Match PRD template to feature complexity — no 11-section PRD for a 1-week feature
- Include explicit out-of-scope in every spec
- Show RICE formula + raw inputs alongside every score for transparency
- Flag imbalanced portfolios (all big bets, missing quick wins, etc.)
- Synthesize discovery across multiple interviews before writing specs — never dump raw transcripts
- Ask for missing RICE fields rather than defaulting without disclosure

### MUST NOT DO
- Do not start writing spec before problem is clearly defined
- Do not invent or estimate RICE inputs without user confirmation
- Do not skip the stakeholder alignment checklist for P0 features
- Do not present multi-interview findings as separate unconnected lists — always synthesize
- Do not omit success metrics from any spec

## Output Checklist

Verify before final delivery:
- [ ] RICE scores include formula + input values alongside result
- [ ] Roadmap fits within stated team capacity
- [ ] PRD template matched to correct complexity tier
- [ ] Out-of-scope explicitly stated in all specs
- [ ] Discovery synthesis grouped by theme, not raw per-interview list
- [ ] Success metrics measurable and time-bound
- [ ] Open questions surfaced as distinct block
