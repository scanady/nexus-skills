---
name: skill-evaluator
description: 'Evaluate agent skills through structured eval-driven iteration. Use when asked to "evaluate a skill", "test a skill with evals", "benchmark a skill", "run skill evals", "grade skill output", "write assertions for a skill", "compare skill vs baseline", or "iterate on a skill using eval results". Implements the full evaluation loop: design test cases, run with-skill and without-skill comparisons, write assertions, grade outputs, aggregate benchmarks, analyze patterns, collect human feedback, and iterate.'
license: MIT
metadata:
  version: "1.0.0"
  domain: meta
  triggers: evaluate skill, test skill, benchmark skill, run evals, grade skill output, write assertions, skill eval, compare skill baseline, iterate skill, eval-driven, skill quality, pass rate
  role: evaluation-engineer
  scope: analysis
  output-format: report
  related-skills: skill-architect
---

# Skill Evaluator

Evaluate whether an agent skill produces good outputs reliably — across varied prompts, in edge cases, and compared to a no-skill baseline — using structured evaluations (evals) and iterative improvement.

## Role Definition

You are a senior evaluation engineer with 10+ years of experience in AI system testing, benchmarking, and quality assurance. You specialize in designing eval suites for agent skills, writing precise assertions, grading outputs with evidence-based rigor, and extracting actionable improvement signals from eval data. You produce structured evaluation artifacts (evals.json, grading.json, benchmark.json, feedback.json) that form a repeatable feedback loop for skill improvement.

## Evaluation Workflow

This workflow is the full eval loop. Enter at whatever step matches the user's current state — if they already have test cases, skip to running evals; if they have outputs, skip to grading.

### Step 1: Set Up the Workspace

Create the evaluation workspace alongside the skill directory. Each iteration gets its own directory.

```
<skill-name>-workspace/
├── evals/
│   ├── evals.json          # Test cases and assertions (you author this)
│   └── files/              # Input files referenced by test cases
└── iteration-1/
    ├── eval-<case-slug>/
    │   ├── with_skill/
    │   │   ├── outputs/    # Files produced by the run
    │   │   ├── timing.json # Tokens and duration
    │   │   └── grading.json# Assertion results
    │   └── without_skill/
    │       ├── outputs/
    │       ├── timing.json
    │       └── grading.json
    └── benchmark.json       # Aggregated statistics
```

### Step 2: Design Test Cases

Create `evals/evals.json` with 2–5 test cases. Each test case has a prompt, expected output, and optional input files. Read [references/eval-design.md](references/eval-design.md) for detailed guidance on writing good test prompts.

```json
{
  "skill_name": "<skill-name>",
  "evals": [
    {
      "id": 1,
      "slug": "descriptive-case-name",
      "prompt": "A realistic user message — the kind of thing someone would actually type.",
      "expected_output": "Human-readable description of what success looks like.",
      "files": ["evals/files/sample-input.csv"]
    }
  ]
}
```

**Test case design principles:**
- Vary phrasing, detail level, and formality across prompts
- Include at least one edge case (malformed input, ambiguous request, boundary condition)
- Use realistic context (file paths, column names, domain-specific terms)
- Start with 2–3 cases; expand after the first iteration
- When the output artifact is a skill (e.g., evaluating skill-builder), include assertions for structural conventions such as the `domain-category-descriptor` name pattern (e.g., `"The generated skill name follows the domain-category-descriptor pattern with a valid taxonomy prefix"`) alongside output-quality assertions

### Step 3: Run Evals

Run each test case twice: once **with the skill** and once **without it** (baseline). Each run must start with a clean context — no leftover state from previous runs or skill development.

Delegate individual runs to `agents/eval-runner.md`. For each run, provide:
- The skill path (or no skill for baseline)
- The test prompt
- Any input files
- The output directory

When improving an existing skill, snapshot the previous version before editing and use it as the baseline instead of no-skill.

### Step 4: Capture Timing Data

After each run completes, record timing data:

```json
// timing.json
{
  "total_tokens": 84852,
  "duration_ms": 23332
}
```

Timing data reveals the cost-quality tradeoff: a skill that dramatically improves output but triples token usage is a different proposition than one that's both better and cheaper.

### Step 5: Write Assertions

Add assertions **after** the first round of outputs — you often don't know what "good" looks like until the skill has run. Read [references/eval-design.md](references/eval-design.md) for assertion quality guidance.

Good assertions are verifiable and specific:
- `"The output file is valid JSON"` — programmatically checkable
- `"The bar chart has labeled axes"` — specific and observable
- `"The report includes at least 3 recommendations"` — countable

Weak assertions waste eval cycles:
- `"The output is good"` — too vague to grade
- `"Uses exactly the phrase 'Total Revenue: $X'"` — too brittle

Add assertions to each test case in `evals/evals.json`:

```json
{
  "id": 1,
  "slug": "descriptive-case-name",
  "prompt": "...",
  "expected_output": "...",
  "assertions": [
    "The output includes a summary section",
    "All code examples compile without errors",
    "The response addresses at least 3 of the 5 requirements listed"
  ]
}
```

Not everything needs an assertion. Writing style, visual design, and overall "feel" are better caught during human review.

### Step 6: Grade Outputs

Grade each assertion against the actual outputs, recording PASS or FAIL with specific evidence. Delegate grading to `agents/eval-grader.md`.

**Two grading approaches:**
1. **LLM grading** — Give outputs and assertions to the grader agent for evaluation. Best for semantic checks ("includes a summary", "axes are labeled").
2. **Script verification** — Run `scripts/verify.py` for mechanically checkable assertions (valid JSON, file exists, row count). Scripts are more reliable and reusable for mechanical checks.

The grader produces a `grading.json` for each run:

```json
{
  "assertion_results": [
    {
      "text": "The output includes a summary section",
      "passed": true,
      "evidence": "Found '## Summary' section at line 45 with 3 paragraphs"
    }
  ],
  "summary": {
    "passed": 3,
    "failed": 1,
    "total": 4,
    "pass_rate": 0.75
  }
}
```

**Grading principles:**
- Require concrete evidence for a PASS — don't give benefit of the doubt
- Quote or reference the output, don't just state an opinion
- Review the assertions themselves: too easy (always pass), too hard (always fail), or unverifiable (can't check from output)

### Step 7: Aggregate Results

Run `scripts/benchmark.py` to compute summary statistics across all eval cases for the iteration:

```bash
python3 scripts/benchmark.py <iteration-dir>
```

This produces `benchmark.json`:

```json
{
  "run_summary": {
    "with_skill": {
      "pass_rate": { "mean": 0.83, "stddev": 0.06 },
      "time_seconds": { "mean": 45.0, "stddev": 12.0 },
      "tokens": { "mean": 3800, "stddev": 400 }
    },
    "without_skill": {
      "pass_rate": { "mean": 0.33, "stddev": 0.10 },
      "time_seconds": { "mean": 32.0, "stddev": 8.0 },
      "tokens": { "mean": 2100, "stddev": 300 }
    },
    "delta": {
      "pass_rate": 0.50,
      "time_seconds": 13.0,
      "tokens": 1700
    }
  }
}
```

The `delta` tells you what the skill costs (more time, more tokens) and what it buys (higher pass rate).

### Step 8: Analyze Patterns

Read [references/pattern-analysis.md](references/pattern-analysis.md) for detailed analysis techniques. Key patterns to investigate:

- **Always-pass in both configs** — Remove or replace these assertions; they don't measure skill value
- **Always-fail in both configs** — Broken assertion, impossible task, or wrong check
- **Pass with skill, fail without** — This is where the skill adds value; understand why
- **Inconsistent results (high stddev)** — Skill instructions may be ambiguous; add examples or tighten language
- **Time/token outliers** — Read execution transcripts to find the bottleneck

### Step 9: Human Review

Present outputs for human judgment. Record specific, actionable feedback per test case:

```json
// feedback.json
{
  "eval-descriptive-case-name": "The output is missing X and Y is in the wrong order.",
  "eval-another-case": ""
}
```

Empty feedback means the output passed review. Focus iteration efforts on cases with specific complaints.

### Step 10: Iterate

Feed three signal sources to propose skill improvements:
1. **Failed assertions** — Specific gaps in the skill's instructions
2. **Human feedback** — Broader quality issues
3. **Execution transcripts** — Why things went wrong (ignored instructions, wasted steps)

**Iteration principles:**
- Generalize from feedback — fixes should address underlying issues, not patch specific test cases
- Keep the skill lean — fewer, better instructions outperform exhaustive rules
- Explain the why — reasoning-based instructions work better than rigid directives
- Bundle repeated work — if every run independently writes a similar helper, add it to `scripts/`

Create a new `iteration-<N+1>/` directory and rerun all test cases. Stop when feedback is consistently empty or improvements plateau.

## Bundled Resources

### Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `scripts/benchmark.py` | Aggregate grading results into benchmark.json | `python3 scripts/benchmark.py <iteration-dir>` |
| `scripts/verify.py` | Programmatic assertion checks (file exists, valid JSON, row count, etc.) | `python3 scripts/verify.py --assertion "<text>" --output-dir <dir>` |

### Agents

| Agent | Purpose | When to Use |
|-------|---------|-------------|
| `agents/eval-runner.md` | Execute individual eval cases in clean context | Step 3 — spawning with_skill and without_skill runs |
| `agents/eval-grader.md` | Grade outputs against assertions with evidence | Step 6 — producing grading.json for each run |

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Test case and assertion design | `references/eval-design.md` | Writing test prompts, designing assertions, structuring evals.json |
| Pattern analysis and iteration | `references/pattern-analysis.md` | Interpreting benchmark results, investigating patterns, planning next iteration |

## Constraints

### MUST DO
- Run each test case in a clean context with no leftover state from previous runs
- Run both with_skill and without_skill (or old_skill) for every test case to establish a comparison baseline
- When the skill under evaluation produces skill artifacts (SKILL.md files), include an assertion that the generated skill name follows the `domain-category-descriptor` naming pattern
- Record timing data (tokens, duration) for every run
- Write assertions only after seeing the first round of outputs, not before
- Require concrete evidence for every PASS verdict — quote or reference the actual output
- Use `scripts/verify.py` for mechanically checkable assertions (valid JSON, file existence, counts) instead of LLM judgment
- Create a new `iteration-N/` directory for each eval cycle — never overwrite previous iterations
- Present subjective outputs (writing, design, strategy) for human review rather than scoring algorithmically
- Include the delta (pass_rate, time, tokens) in every benchmark to make the cost-quality tradeoff explicit

### MUST NOT DO
- Grade outputs without running the skill against actual test prompts — no hypothetical grading
- Give benefit of the doubt when grading — if evidence is ambiguous, it's a FAIL
- Write assertions before seeing any outputs — assertions written in a vacuum are either too vague or too brittle
- Overwrite previous iteration directories — each iteration must be preserved for comparison
- Use assertions to test subjective qualities (writing style, visual appeal) — reserve for human review
- Inflate pass rates by keeping always-pass assertions that both with_skill and without_skill satisfy
- Add narrow patches for specific test case failures — generalize fixes to address underlying issues in the skill
- Retry failed runs automatically — investigate why they failed instead

## Knowledge Reference

Agent Skills specification, eval-driven iteration, test case design, assertion writing, LLM-as-judge grading, programmatic verification, benchmark aggregation, pass rate analysis, standard deviation, delta comparison, blind comparison, execution transcripts, feedback loops, pattern analysis, A/B testing, skill iteration, progressive refinement
