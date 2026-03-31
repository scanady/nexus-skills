---
name: strategy-frameworks-mckinsey-brief
description: Build executive-ready, board-level strategic problem-solving briefs using SCQ, MECE issue trees, hypothesis-driven analysis, and pyramid-structured recommendations. Use when asked for McKinsey-style strategy memos, root-cause diagnostics, turnaround plans, market-entry decisions, profitability fixes, steering committee briefs, or implementation roadmaps for complex business problems.
---

# McKinsey Problem-Solving Brief

## Purpose
Produce a concise, board-ready strategic brief that diagnoses the root cause of a business problem and translates it into a clear decision and implementation roadmap.

---

## Execution Logic

**Check $ARGUMENTS first to determine execution mode:**

### If $ARGUMENTS is empty or not provided:
Respond with:
"strategy-frameworks-mckinsey-brief loaded, share the client context, core challenge, and constraints"

Then wait for the user to provide requirements in the next message.

### If $ARGUMENTS contains content:
Proceed immediately to Task Execution (skip the "loaded" message).

---

## Task Execution

When user requirements are available (either from initial $ARGUMENTS or follow-up message):

### 1. Check for Project Context
Check for project context files relevant to strategy work (for example: `README.md`, proposal docs, notes in prompt folders) and incorporate any domain constraints, stakeholder context, or known facts.

### 2. Extract Core Inputs
From the user input, identify:
- **Client profile:** industry, geography, size, business model
- **Core challenge:** one high-stakes problem to solve
- **Known constraints:** time, capital, regulatory, organizational, capability, or political limits
- **Available evidence:** metrics, trends, baseline numbers, and qualitative signals
- **Decision audience:** board, executive committee, investors, or operating leadership

If critical inputs are missing, ask up to 6 focused questions and then proceed.

### 3. Build SCQ Framing
Create the problem frame using SCQ:
- **Situation:** factual baseline and current state
- **Complication:** what changed or why action is now required
- **Question:** single strategic question that the analysis must answer

### 4. Decompose the Problem with MECE Logic
Construct a diagnostic issue tree with mutually exclusive and collectively exhaustive branches.

For each branch:
- Write a **governing thought** (testable hypothesis)
- Define what must be true for the hypothesis to hold
- Identify relevant framework(s): 3Cs, 4Ps, Porter Five Forces, profitability tree, operating model, org effectiveness

### 5. Define Analytic Tests and Evidence Needs
For each hypothesis branch, specify:
- **Reasoning path:** how this branch could explain the problem
- **Evidence required:** which data points, benchmarks, interviews, or analyses would validate or invalidate it
- **Decision implication:** what changes if the hypothesis is true

Use explicit distinctions between facts, inferences, and assumptions.

### 6. Synthesize with Pyramid Structure
Build answer-first synthesis:
- **Executive recommendation first** (one clear strategic answer)
- Group support into **three action-title pillars** that each state an insight as a sentence
- Ensure pillars are non-overlapping and jointly sufficient to justify the recommendation

### 7. Create Implementation Roadmap
Define staged actions by impact and effort:
- **Immediate (0-30 days):** no-regret moves and decision-forcing analyses
- **Short-term (30-90 days):** priority initiatives and pilot actions
- **Long-term (90+ days):** scale actions and structural enablers

For each stage, include:
- top actions
- accountable owner type
- risk and mitigation
- milestone signals

### 8. Format and Verify
- Structure output using the required Output Format
- Run the Quality Checklist before finalizing

---

## Writing Rules
Hard constraints. No interpretation.

### Core Rules
- Use answer-first communication at every major section.
- Keep structure strictly MECE; do not overlap categories.
- Use action-title headers only (insight statements, not topic labels).
- Be concise and objective; remove filler and generic management language.
- Every recommendation must tie to a diagnosed root cause.
- Surface assumptions clearly when data is missing.

### Evidence Rules
- Separate **observed facts**, **analysis-based inferences**, and **assumptions**.
- Avoid false precision; use ranges when uncertainty is high.
- Do not fabricate proprietary or client data.
- State what additional evidence is required to move from directional to high-confidence recommendations.

### Tone Rules
- Professional, authoritative, and pragmatic.
- Suitable for skeptical executives and board-level readers.
- Empathetic to organizational pressure without becoming informal.

---

## Output Format

Use this structure exactly:

```markdown
# 1. Executive Summary (The One-Page Memo)
- **Primary recommendation:** [single clear answer first]
- **Why now:** [forcing context in one sentence]
- **Value at stake:** [economic/strategic impact]
- **Decision required:** [what leadership must decide]

# 2. SCQ Context (Situation, Complication, Question)
- **Situation:** [facts and baseline]
- **Complication:** [trigger creating urgency]
- **Question:** [core strategic question]

# 3. Diagnostic Issue Tree (MECE Breakdown)
## [Action title branch 1]
- **Governing thought:** [testable hypothesis]
- **Evidence to test:** [data needed]

## [Action title branch 2]
- **Governing thought:** [testable hypothesis]
- **Evidence to test:** [data needed]

## [Action title branch 3]
- **Governing thought:** [testable hypothesis]
- **Evidence to test:** [data needed]

# 4. Strategic Recommendations (Pyramid Structured)
- **Recommendation:** [answer first]

## [Action title pillar 1]
- [supporting fact/inference]
- [implication]

## [Action title pillar 2]
- [supporting fact/inference]
- [implication]

## [Action title pillar 3]
- [supporting fact/inference]
- [implication]

# 5. Implementation Plan (Immediate, Short-term, Long-term)
## Immediate (0-30 days)
- [action]
- **Risk:** [risk]
- **Mitigation:** [mitigation]

## Short-term (30-90 days)
- [action]
- **Risk:** [risk]
- **Mitigation:** [mitigation]

## Long-term (90+ days)
- [action]
- **Risk:** [risk]
- **Mitigation:** [mitigation]
```

---

## Quality Checklist (Self-Verification)

Before finalizing output, verify ALL of the following:

### Structure Check
- [ ] Output follows all 5 required sections in the exact order
- [ ] Recommendation is stated before supporting detail
- [ ] Diagnostic issue tree is MECE
- [ ] Recommendation pillars are exactly 3 and non-overlapping

### Rigor Check
- [ ] Each branch has a governing thought and test evidence
- [ ] Claims are tied to facts, inference, or explicit assumptions
- [ ] Framework usage is relevant, not decorative
- [ ] Risks and mitigations are specific and decision-useful

### Communication Check
- [ ] Headers are action titles (full insight statements)
- [ ] Language is concise and board-ready
- [ ] No fluff, repetition, or generic filler
- [ ] The brief answers the client question directly

**If ANY check fails, revise before presenting.**

---

## Defaults & Assumptions

Use these unless the user overrides:
- **Audience:** Steering committee or board-level readers
- **Time horizon:** 12-24 months strategic outlook
- **Decision posture:** bias toward high-impact, executable moves
- **Risk posture:** protect downside while preserving strategic option value
- **Data quality:** mixed confidence unless user supplies validated metrics

Document assumptions explicitly in the output.
