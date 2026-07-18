# Outcome Design

A challenge-first Agent Skill that helps people work backward from a desired outcome into a measurable, feasible, reviewable design before planning or execution.

## What it produces

The skill produces an **Outcome Design Record** that captures:

- Desired outcome and value
- Success evidence and guardrails
- Current reality and evidence
- Constraints, ownership, and dependencies
- Causal design and alternatives
- Assumptions, feasibility, and risks
- Milestones, learning loops, and decision points
- Decisions, rationale, maturity, and downstream contract

The record is deliberately decoupled from execution. Other humans or skills can use it to create experiments, project plans, implementation designs, decision analyses, habit systems, research plans, or other artifacts.

## Package structure

```text
strategy-outcome-design/
├── SKILL.md
├── README.md
├── assets/
│   └── outcome-design-record.md
├── references/
│   ├── methodology.md
│   ├── patterns.md
│   └── quality-rubric.md
├── examples/
│   ├── example-conversation.md
│   └── example-record.md
├── evals/
│   ├── evals.json
│   ├── trigger-queries.json
│   └── manual-conversation-tests.md
└── scripts/
    └── validate_package.py
```

## Installation

Copy the `strategy-outcome-design` directory into the skills directory supported by your agent client. The parent directory must remain named `strategy-outcome-design` because the Agent Skills specification requires the directory name to match the `name` in `SKILL.md`.

## Invocation behavior

The skill should trigger when a user wants to:

- Clarify or pressure-test a goal
- Work backward from an outcome
- Define meaningful success criteria
- Evaluate feasibility before committing
- Separate a proposed solution from the outcome
- Explore assumptions, alternatives, risks, and trade-offs
- Produce a design record for downstream work

It should not trigger for simple factual questions or straightforward execution of an already-defined plan.

## Validation

Run:

```bash
python scripts/validate_package.py .
```

The validator checks frontmatter, naming, links, required resources, JSON evaluation files, and key record-template fields.

## Evaluation

- `evals/trigger-queries.json` tests whether the description activates on the right prompts and avoids near-miss prompts.
- `evals/evals.json` tests first-turn behavior and final artifact quality.
- `evals/manual-conversation-tests.md` tests persistence, checkpointing, stopping, and disagreement handling across multiple turns.

Run each automated evaluation in a fresh context and compare the skill against a no-skill baseline or the previous version.
