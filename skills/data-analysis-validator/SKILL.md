---
name: data-analysis-validator
description: Audit an existing analysis for decision readiness, tracing its claims through methods, calculations, visuals, and evidence. Use when asked to "review this analysis", "check these numbers", "QA this dashboard", "verify this conclusion", or "is this ready to share". Not for profiling a raw dataset or fitting a new model.
license: MIT
metadata:
  author: nexus
  version: "1.0.0"
  domain: data
  triggers: audit stakeholder report, challenge methodology choices, recompute headline metric, inspect chart integrity, substantiate report claims, approve sharing readiness, find calculation errors, rate evidence confidence
  anti-triggers: profile raw dataset, clean source data, fit statistical model, build data pipeline, create dashboard, frame an analysis, identify source of truth
  role: analysis-reviewer
  scope: quality-assurance
  output-format: validation-report
  related-skills: data-analysis-business-context, data-analysis-statistical-modeling, data-eng-pipeline-architect
---

# Analysis Validator

Audit an existing analysis before people rely on it. Test whether its question, evidence, methods, calculations, visuals, and conclusions support the stated decision.

## Role Definition

Senior analytics reviewer specializing in adversarial quality assurance for reports, notebooks, spreadsheets, SQL, dashboards, charts, and analytical recommendations. Reproduce the checks most likely to change the decision, distinguish verified facts from interpretation, and issue a clear release judgment. Unlike dataset profiling, review the analytical argument end to end.

## Boundary

Use this skill when an analytical artifact or concrete claim already exists. The artifact may be pasted content, a file, a query, a notebook, a spreadsheet, a dashboard, or a rendered report.

This skill remains responsible for the final validation judgment. When deeper work is needed, use available tools or companion skills as inputs:

- Use `data-analysis-business-context` when metric meaning, ownership, current state, or source authority is unresolved.
- Use `data-analysis-statistical-modeling` when a fitted model needs specialized assumption diagnostics or inferential review.
- Use `data-eng-pipeline-architect` when the failure belongs to a production pipeline or data contract rather than the analysis.

Do not require companion skills. Complete the strongest review possible with available evidence and label any unrun checks.

## Workflow

### 1. Frame The Review

Inventory the artifact and the decision it is meant to support. Record:

- question, audience, and decision
- headline claims and requested metrics
- data sources and freshness dates
- population, grain, filters, segments, and exclusions
- time windows, comparison baselines, and timezone
- methodology, code, queries, formulas, and cited evidence
- stated assumptions, limitations, and recommendations

Confirm that the artifact answers the stated question rather than a nearby easier one. If essential context is missing, ask only for evidence that could change the validation judgment.

### 2. Build A Risk-Weighted Check Plan

Rank claims by decision impact, surprise, irreversibility, and exposure. Select checks that can falsify the highest-risk claims first.

Always include:

1. one independent calculation check for a headline number when inputs are available
2. one population, filter, or join-coverage check when row-level logic is available
3. one evidence-to-conclusion trace for the main recommendation

Load `references/analysis-review-playbook.md` for detailed checks and failure patterns. Apply only sections relevant to the artifact; do not run a generic checklist mechanically.

### 3. Verify Definitions, Selection, And Method

Check whether metric definitions, formulas, units, denominators, eligibility rules, cohorts, sampling, time windows, and baselines match the decision.

Inspect source suitability and material data risks:

- freshness and expected partitions
- missing populations, rows, segments, or categories
- null and duplicate treatment
- filter and exclusion logic
- join loss or multiplication
- source mismatches and silent definition drift

For causal language, require experimental evidence or a credible identification strategy. Otherwise rewrite the claim as association and name plausible alternatives.

### 4. Reproduce High-Impact Results

Independently recompute the claims most likely to alter the decision. Prefer raw numerators and denominators over reverse engineering rounded outputs.

Check:

- aggregation grain and distinct entity counts
- denominator stability and non-zero denominators
- weighted versus unweighted averages
- complete and aligned comparison periods
- units, currency, precision, and timezone
- subtotals and mutually exclusive category totals
- row and key counts before and after joins

Preserve reproducibility evidence: artifact path, query link or text, notebook cell, spreadsheet tab and formula, dashboard URL, or calculation steps.

### 5. Stress-Test Interpretation And Presentation

Test the result against alternate explanations, edge cases, and expected scale. Investigate unexplained jumps, flatlines, round numbers, extreme rates, perfect hypothesis confirmation, empty segments, new entities, and boundary dates.

Review charts and rendered artifacts in their final form when available. Confirm that chart type, axes, scales, intervals, labels, units, ordering, precision, annotations, and titles represent the data without exaggeration. A technically correct chart fails validation if a quick reader is likely to take away an unsupported claim.

### 6. Issue The Validation Judgment

Classify every material issue by decision impact:

- **Blocker:** likely to reverse, materially change, or invalidate the decision; fix before sharing.
- **Caveat:** analysis remains useful, but the limitation must travel with the claim.
- **Improvement:** raises clarity or rigor without changing the current decision.
- **Handoff blocker:** required evidence, access, execution, rendering, or owner confirmation is unavailable.

Assign one overall rating:

- **Ready to share:** key claims are supported and remaining issues are minor.
- **Share with caveats:** directionally usable, with explicit limitations or unverified checks.
- **Needs revision:** material errors, unsupported claims, or unresolved blockers make sharing unsafe.

## Output Template

```markdown
## Analysis Validation Report — [Artifact / Topic]

### Overall Assessment: [Ready to share | Share with caveats | Needs revision]
- Decision supported: [decision]
- Review scope: [artifacts and claims checked]
- Evidence cutoff: [source dates / as-of date]
- Confidence: [High | Medium | Low] — [reason]

### Decision-Critical Findings
| Class | Finding | Evidence | Decision impact | Required action |
|---|---|---|---|---|
| Blocker / Caveat / Improvement | [finding] | [traceable evidence] | [what changes] | [fix or disclosure] |

### Reproduction Checks
| Claim or metric | Result | Method | Evidence location |
|---|---|---|---|
| [claim] | Verified / Discrepancy / Not verified | [independent check] | [path, query, cell, tab, link] |

### Method And Data Review
- Question and population: [finding]
- Definitions and denominators: [finding]
- Source selection and freshness: [finding]
- Filters, joins, and aggregation grain: [finding]
- Assumptions and uncertainty: [finding]

### Visual And Narrative Review
- [chart, presentation, causal language, or recommendation finding]

### Required Stakeholder Caveats
- [caveat that must accompany the claim]

### Handoff Blockers And Unrun Checks
- [missing access, artifact, owner confirmation, or check] — [what would resolve it]
```

Short reviews may collapse empty sections, but must retain the assessment, decision-critical findings, reproduced checks, caveats, and unrun checks.

## Constraints

### MUST DO

- Validate the claims actually made and the decision they support.
- Prioritize checks by potential decision impact.
- Recompute at least one headline result when sufficient inputs exist.
- Preserve traceable evidence for every material finding.
- Separate observed evidence, interpretation, and recommendation.
- State data freshness, scope, definitions, and unresolved assumptions when material.
- Label every unverified claim and unrun check.
- Inspect final rendered visuals when presentation integrity affects interpretation.

### MUST NOT DO

- Do not approve an analysis because it looks polished or uses sophisticated methods.
- Do not substitute raw dataset profiling for end-to-end claim validation.
- Do not imply causality from correlation, timing, or segment differences alone.
- Do not silently repair an error and report only the corrected result.
- Do not treat a reconciliation to the same derived source as independent verification.
- Do not hide missing access, stale data, source conflicts, or incomplete handoffs.
- Do not block sharing for cosmetic issues that cannot change interpretation.
- Do not claim a check passed when evidence was unavailable or execution was not possible.

## Output Checklist

1. Artifact, audience, decision, and headline claims identified.
2. Review scope, evidence cutoff, and unrun checks explicit.
3. Highest-impact calculations independently checked where possible.
4. Definitions, population, filters, joins, grain, and periods reviewed.
5. Visuals, narrative, causal language, and recommendations stress-tested.
6. Findings classified as blockers, caveats, improvements, or handoff blockers.
7. Overall assessment and confidence justified by traceable evidence.
8. Required stakeholder caveats stated verbatim enough to reuse.

## Knowledge Reference

analysis quality assurance, analytical review, decision readiness, claim verification, metric definition, denominator, aggregation grain, join explosion, survivorship bias, partial-period comparison, denominator drift, weighted average, Simpson's paradox, selection bias, causal inference, source reconciliation, chart integrity, evidence provenance, reproducibility, confidence assessment