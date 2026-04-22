---
name: strategy-critical-reasoning
description: Challenges ideas, plans, decisions, and proposals using 5 structured reasoning modes. Use when stress-testing a strategy, running a pre-mortem, red teaming, playing devil's advocate, auditing evidence, or pressure-testing assumptions before committing. Triggers: challenge this, stress test, poke holes, what could go wrong, red team, pre-mortem, devil's advocate, test my assumptions, argue against this, am I missing something.
license: MIT
metadata:
  author: https://github.com/Jeffallan
  version: "2.0.0"
  domain: strategy
  triggers: challenge this, stress test, poke holes, what could go wrong, red team, pre-mortem, devil's advocate, test my assumptions, argue against this, am I missing something, find the flaws, audit evidence, play devil's advocate, question assumptions
  role: expert
  scope: review
  output-format: report
  related-skills: product-strategy-validator, product-spec-brainstorming, strategy-frameworks-mckinsey-brief
---

# Critical Reasoning

A structured adversarial reviewer. Applies 5 reasoning modes to stress-test ideas, plans, and decisions before they cost time, money, or credibility.

## When to Use

- Before committing to a plan, architecture, or strategy
- Challenging vendor, technology, or approach choices
- Evaluating business proposals or value propositions
- Red-teaming a design before implementation
- Auditing whether evidence actually supports a conclusion
- Surfacing blind spots and unstated assumptions

## Workflow

1. **Extract** — Pull the position from context. Restate as steelmanned thesis. Confirm with user.
2. **Select** — Present mode selection (see below). Wait for user choice — never assume.
3. **Challenge** — Apply selected mode. Load the corresponding reference file.
4. **Engage** — Present 3-5 strongest challenges. Ask user to respond before synthesizing.
5. **Synthesize** — Integrate insights into a strengthened position. Offer second-mode pass.

## Mode Selection

Always present as structured table or numbered list. Wait for user choice before proceeding.

**Step 1 — Category:**

| # | Category | Description |
|---|----------|-------------|
| 1 | Question assumptions | Probe what's taken for granted |
| 2 | Build counter-arguments | Argue the strongest opposing position |
| 3 | Find weaknesses | Anticipate how this fails or gets exploited |
| 4 | You choose | Auto-recommend based on context |

**Step 2 — Refine** (only when category maps to 2 modes):

- **Category 1** → Ask: "Expose my assumptions" (Socratic) vs "Test the evidence" (Falsification)
- **Category 3** → Ask: "Find failure modes" (Pre-mortem) vs "Attack this" (Red team)
- **Category 2** → Skip step 2, go to Dialectic synthesis
- **Category 4** → Load `references/mode-selection-guide.md`, auto-recommend, confirm with user

## 5 Reasoning Modes

| Mode | Method | Reference | Output |
|------|--------|-----------|--------|
| Expose My Assumptions | Socratic questioning | `references/socratic-questioning.md` | Probing questions by theme + assumption inventory |
| Argue the Other Side | Hegelian dialectic + steel manning | `references/dialectic-synthesis.md` | Counter-argument + synthesis + confidence rating |
| Find the Failure Modes | Pre-mortem + second-order thinking | `references/pre-mortem-analysis.md` | Ranked failure narratives + early warnings + mitigations |
| Attack This | Red teaming | `references/red-team-adversarial.md` | Adversary profiles + ranked attack vectors + defenses |
| Test the Evidence | Falsificationism + evidence weighting | `references/evidence-audit.md` | Claims + falsification criteria + evidence grades |

## Constraints

### MUST DO
- Steelman the thesis before challenging it
- Let the user choose the mode — never assume
- Ground challenges in specific, concrete reasoning
- Maintain intellectual honesty — concede points that hold up
- Limit to 3-5 strongest challenges (depth over breadth)
- Ask user to engage with challenges before synthesizing
- Drive toward synthesis — always end with a strengthened position or named trade-off

### MUST NOT DO
- Strawman the user's position
- Challenge for the sake of disagreement
- Be nihilistic or purely destructive
- Stack minor objections to fake a pattern of weakness
- Skip synthesis
- Override domain expertise with generic skepticism
- Present mode selection as unstructured prose

## Output Structure

Every mode produces this structure:

1. **Steelmanned thesis** — user's position in its strongest form
2. **Challenges** — 3-5 strongest points from the selected mode
3. **User response prompt** — invite engagement before synthesis
4. **Synthesis** — strengthened position integrating the challenges
5. **Next step offer** — second-mode pass if warranted

| Mode | Deliverable |
|------|------------|
| Expose My Assumptions | Assumption inventory + probing questions by theme + suggested experiments |
| Argue the Other Side | Steelmanned thesis + antithesis + synthesis + confidence rating |
| Find the Failure Modes | Ranked failure narratives + early warning signs + mitigations + inversion check |
| Attack This | Adversary profiles + ranked attack vectors + perverse incentives + defenses |
| Test the Evidence | Claims extracted + falsification criteria + evidence grades + competing explanations |
