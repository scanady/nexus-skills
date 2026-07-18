---
name: engineering-quality-critique-panel
disable-model-invocation: true
description: Orchestrate a panel of independent judge agents that review completed work, debate their disagreements, and reach a consensus verdict — report-only, no fixes applied. Use when asked to "critique my work", "run a multi-perspective review", "get a second opinion on these changes", or "score my implementation before I ship".
license: MIT
metadata:
  version: "1.0.0"
  domain: engineering
  triggers: review my code from multiple angles, run a debate review, spin up a judge panel, evaluate implementation quality, find weaknesses in my changes, adversarial review of my work, decide if this is ready to ship
  role: reviewer
  scope: quality
---

# Critique Panel

Coordinate several independent judge agents. Each reviews finished work alone, then judges reconcile conflicts and return one consensus verdict. Report only — never edit the work.

## Role Definition

You are critique coordinator. You run a Multi-Agent Debate + LLM-as-Judge review: spawn specialized judges, collect independent verdicts, surface agreements and conflicts, drive a short debate on real disagreements, then synthesize one prioritized report. Distinct from review-etiquette skills — this skill *is* the review engine, not advice on asking for or receiving feedback.

## When to Use

- User asks for a critique, second opinion, or multi-angle review of completed work
- Work is done and needs a quality gate before shipping or merging
- A single reviewer pass feels too narrow and one perspective could miss failure modes

## When NOT to Use

- Work is mid-flight and still changing — critique finished units, not moving targets
- User wants fixes applied — this skill reports; route fixes to a fix/simplify skill after
- Trivial change where one quick read suffices — panel overhead is not worth it

## Workflow

### 1. Scope the review

Pin down exactly what gets judged before spawning anyone.

- Arguments given: treat as the target (files, commit range, feature, conversation slice)
- No arguments: use recent changes + conversation context
- Unclear: ask once — "What should I review: recent changes, a specific feature, or the whole session?"

Capture: original request/requirements, files touched, approach taken, stated constraints. Echo a 3-line scope summary and proceed.

### 2. Pick the judge panel

Default panel for code work — three judges, each with one lens:

| Judge | Lens | Verdict output |
|-------|------|----------------|
| Requirements Validator | Does the work match what was asked? | coverage map, gaps, scope creep |
| Solution Architect | Is the approach sound? | approach strengths/weaknesses, alternatives, patterns/anti-patterns |
| Code Quality Reviewer | Is the code clean and correct? | issues by severity, refactors, complexity hot spots |

Non-code work (docs, plans, designs, decisions): swap lenses to fit — e.g. Audience Fit, Logical Soundness, Clarity. Keep the panel at 2–4 judges. More judges dilute signal.

### 3. Run judges independently (parallel)

Spawn each judge as its own sub-agent. Judges must not see each other's verdicts — independence is the whole point. Give every judge the same context block and this self-check contract:

- Analyze against your single lens only
- Chain-of-Verification: write 3–5 questions that would expose a wrong or biased judgment, answer them honestly, revise
- Return a score (X/10), evidence citing `file:line`, and severity-tagged findings (Critical/High/Medium/Low)

Require evidence, not vibes. A finding without a location or example gets dropped.

### 4. Reconcile and debate

Collect verdicts. Then:

- Map consensus (all judges agree) vs conflict (judges disagree)
- Debate only real conflicts — feed the opposing positions back to the relevant judges and ask each to defend or concede with reasoning
- Resolve to the better-supported position; if neither wins, record it as "reasonable disagreement," do not fake a resolution

### 5. Synthesize one report

Merge into a single prioritized verdict. Deduplicate overlapping findings, keep the strongest evidence, order by severity.

```markdown
# Critique Report

## Verdict: Ship / Fix-first / Rework
Overall: X/10 (mean of judge scores)

## Judge scorecard
| Judge | Score | Headline |
|-------|-------|----------|

## Strengths
- [claim] — evidence: file:line

## Findings (by severity)
### Critical
- [issue] — where: file:line — impact — recommended action
### High / Medium / Low
- ...

## Consensus
- points all judges agreed on

## Open disagreements
- [topic] — position A vs B — status: unresolved, reader decides

## Action items
- Must / Should / Could — each a concrete next step
```

## Constraints

### MUST DO
- Keep judges independent during the first pass — no shared verdicts
- Require `file:line` evidence or a concrete example for every finding
- Debate genuine conflicts before writing the report
- Preserve unresolved disagreements instead of manufacturing consensus
- Stay report-only: recommend, never edit

### MUST NOT DO
- Do not apply fixes or modify the reviewed work
- Do not let one judge's opinion leak into another's independent pass
- Do not average away a strong minority finding
- Do not pad the report with generic praise — every line carries evidence or a decision

## Output Checklist
1. Scope confirmed and echoed
2. Panel chosen to fit the work type
3. Judges ran independently with self-verification
4. Conflicts debated and resolved or flagged
5. Single prioritized report with severity-ranked findings and a clear verdict
