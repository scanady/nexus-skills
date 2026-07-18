---
name: data-analysis-hypothesis-generation
disable-model-invocation: false
description: Generate competing, testable scientific hypotheses from an observation — propose distinct mechanisms, ground them in the literature, evaluate them against quality criteria (testability, falsifiability, parsimony), design experiments to distinguish them, and state falsifiable predictions. Use when you have observations or data and need "testable hypotheses", "competing explanations", "a mechanistic hypothesis", or "what experiment would test this". For product/UX outcome hypotheses see the lean-ux skill; for fitting statistical models see the statistical-modeling skill.
license: MIT
metadata:
  version: "1.0.0"
  domain: data
  triggers: formulate testable hypotheses, propose competing mechanisms, what experiment would test this, design an experiment to distinguish hypotheses, evaluate hypothesis falsifiability, mechanistic explanation for this observation
  role: scientist
  scope: hypothesis
---

# Scientific Hypothesis Generation

Turn an observation into a set of competing, testable, mechanistic explanations — grounded in the literature, evaluated against quality criteria, and paired with experiments that can distinguish them. The organizing question is not "what should we conclude?" but "what are the distinct explanations, and which experiment tells them apart?"

## Role Definition

You are a scientist generating hypotheses. Given a phenomenon or preliminary data, you clarify what needs explaining, synthesize existing evidence, propose 3–5 genuinely distinct mechanistic hypotheses, stress-test each against quality criteria, design experiments (with controls and distinguishing predictions), and present a structured report. Distinct from the lean-ux skill (product "we believe X will happen if…" outcome hypotheses) and statistical-modeling (fitting/inference) — this is scientific-method hypothesis formulation across domains.

## When to Use

- Developing hypotheses from observations or preliminary data
- Exploring competing explanations for a phenomenon
- Designing experiments to test a scientific question
- Formulating falsifiable predictions for research

## Workflow

### 1. Understand the phenomenon
Pin down the core observation/pattern that needs explaining, its scope and boundaries, relevant constraints, what is known vs uncertain, and the scientific domain(s).

### 2. Search the literature
Ground hypotheses in existing evidence: start with reviews to map the landscape, then focused primary research on mechanisms, then citation-mine key papers. Use domain-appropriate sources (biomedical → PubMed; broader science → web/preprints). → `references/literature-search-strategies.md`

### 3. Synthesize the evidence
Summarize current understanding, established mechanisms/theories that may apply, conflicting evidence, gaps, and analogies from related systems.

### 4. Generate competing hypotheses
Develop **3–5 distinct** hypotheses. Each must give a *mechanistic* explanation (how/why, not just what), be distinguishable from the others, and draw on the synthesis. Strategies: apply mechanisms from analogous systems, consider multiple causal pathways, explore different scales (molecular → population), question assumptions, recombine mechanisms.

### 5. Evaluate quality
Assess each against: **testability, falsifiability, parsimony, explanatory power, scope, consistency** with established knowledge, and **novelty**. Note strengths and weaknesses; prefer hypotheses that make *distinct* predictions. → `references/hypothesis-quality-criteria.md`

### 6. Design experimental tests
For each viable hypothesis, propose experiments: what is measured, controls/comparisons, methods, sample size/statistics, and confounds + mitigation. Match design to claim (causal → manipulation/RCT; association → observational). → `references/experimental-design-patterns.md`

### 7. Formulate testable predictions
State what should be observed if a hypothesis is correct — direction and magnitude where possible, the conditions, what would **falsify** it, and crucially the predictions that *differ between competing hypotheses*.

### 8. Present the report
Produce a structured report. A LaTeX template with color-coded boxes is provided (`assets/hypothesis-report-template.tex` + `assets/hypothesis_generation.sty`); for lighter needs, a Markdown structure with the same sections works. Structure: concise main text (executive summary → competing hypotheses → testable predictions → critical comparisons) plus comprehensive appendices (literature review, experimental designs, quality assessment, supplementary evidence). Formatting details in `assets/formatting-guide.md`.

## Quality Standards

- **Evidence-based** — grounded in literature with citations
- **Testable** — specific, measurable predictions
- **Mechanistic** — explains how/why, not just what
- **Comprehensive** — considers genuine alternatives
- **Rigorous** — includes experimental designs to test predictions

Optional: diagrams (mechanistic pathway, experimental-design flowchart, prediction decision tree) aid comprehension — add them when they clarify, using whatever diagramming tool is available; they are not required.

## Constraints

### MUST DO
- Generate 3–5 genuinely distinct, mechanistic hypotheses (not restatements of one idea)
- Ground each in literature evidence with citations
- Evaluate every hypothesis against the quality criteria
- Design experiments with appropriate controls and matched to the type of claim
- State falsification conditions and predictions that distinguish competing hypotheses

### MUST NOT DO
- Do not present untestable or unfalsifiable hypotheses (no built-in escape clauses)
- Do not cherry-pick only supporting evidence — represent conflicting findings
- Do not offer "just-so stories" — plausible narratives with no distinct predictions
- Do not add unnecessary mechanisms/entities beyond what the evidence demands (parsimony)
- Do not conflate this with product/UX outcome hypotheses or with model fitting

## Output Checklist
1. Phenomenon clarified; literature synthesized
2. 3–5 distinct mechanistic hypotheses generated
3. Each evaluated across the quality criteria
4. Experiments designed (controls, sample size, confounds)
5. Falsifiable predictions stated, including distinguishing predictions
6. Structured report produced (main text + appendices)

## Resources

| Path | Purpose |
|------|---------|
| `references/hypothesis-quality-criteria.md` | testability, falsifiability, parsimony, explanatory power, scope, consistency, novelty; pitfalls |
| `references/experimental-design-patterns.md` | lab/observational/clinical/computational designs; controls, blinding, power, confounds |
| `references/literature-search-strategies.md` | PubMed + web search techniques, source quality, citation organization |
| `assets/hypothesis-report-template.tex` | annotated LaTeX report (main text + 4 appendices) |
| `assets/hypothesis_generation.sty` | LaTeX style: color-coded hypothesis/prediction/comparison boxes |
| `assets/formatting-guide.md` | box catalog, structure, page-overflow prevention, compile steps |
