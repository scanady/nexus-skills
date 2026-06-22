# Pattern Analysis and Iteration

How to interpret eval benchmark results, identify patterns, and plan skill improvements.

## Reading the Benchmark

The `benchmark.json` has three key sections:

### Run Summary

```json
{
  "with_skill": {
    "pass_rate": { "mean": 0.83, "stddev": 0.06 },
    "time_seconds": { "mean": 45.0, "stddev": 12.0 },
    "tokens": { "mean": 3800, "stddev": 400 }
  }
}
```

- **pass_rate mean**: The skill's average assertion pass rate across all evals. Above 0.8 is strong, below 0.5 needs work.
- **stddev**: Only meaningful with multiple runs per eval. In early iterations, focus on raw pass counts. High stddev (>0.15) signals inconsistency.
- **time/tokens**: Cost metrics. Compare against baseline to assess the tradeoff.

### Delta

```json
{
  "delta": {
    "pass_rate": 0.50,
    "time_seconds": 13.0,
    "tokens": 1700
  }
}
```

The delta is the core decision metric:
- **Positive pass_rate delta + moderate cost increase**: Skill is worth it
- **Positive pass_rate delta + large cost increase**: May need optimization
- **Near-zero pass_rate delta**: Skill isn't adding value — investigate why
- **Negative pass_rate delta**: Skill is actively harmful — rollback

#### Complexity Class Context

Interpret token delta relative to the skill's complexity class from `static-analysis.json`:

| Complexity Class | Token Range | High Token Delta Is... |
|-----------------|-------------|------------------------|
| **compact** | < 800 tokens | A red flag — skill is small but expensive to follow; look for wasted steps |
| **detailed** | 800–1,200 tokens | Expected — a 20–40% increase over baseline is normal |
| **comprehensive** | > 1,200 tokens | Expected — thoroughness has a cost; focus on pass rate delta instead |

A compact skill with a token delta larger than its own baseline cost likely has inefficient instructions (redundant validation, unnecessary reference loading, repeated steps). Read the execution transcript to find the bottleneck.

### Per-Eval Breakdown

The `per_eval` array reveals which test cases the skill handles well and which it struggles with. Focus iteration effort on test cases with the largest gap between expected and actual pass rates.

## Pattern Investigation

### Step 1: Classify Assertions

Sort all assertions into four buckets:

| Bucket | Pattern | Action |
|--------|---------|--------|
| **Always pass (both)** | 100% in with_skill AND without_skill | Remove — doesn't measure skill value |
| **Always fail (both)** | 0% in both | Fix assertion or remove — broken check |
| **Skill value** | Pass with skill, fail without | Keep — this is the skill's contribution |
| **Inconsistent** | Sometimes pass, sometimes fail | Investigate — ambiguity in skill or assertion |

### Step 2: Investigate Skill Value Assertions

For assertions that pass with the skill but fail without:
- Which instructions in SKILL.md made the difference?
- Was it a specific workflow step, constraint, or reference file?
- Can you strengthen these instructions to make the pass more reliable?

### Step 3: Investigate Inconsistencies

High stddev or assertions that pass/fail non-deterministically:
- **Ambiguous instructions**: The model interprets them differently each run. Add examples, use more specific language, or provide a template.
- **Flaky assertions**: The assertion tests something that varies naturally (exact wording, ordering). Loosen the assertion or focus on structural checks.
- **Model randomness**: Some variation is inherent. If the assertion passes >70% of the time, it may be acceptable.

### Step 4: Check Time/Token Outliers

If one eval takes 3x longer or uses 3x more tokens than others:
1. Read the execution transcript for that eval
2. Look for: wasted steps, unnecessary validation, repeated attempts, loading unneeded references
3. Simplify the relevant skill instructions or add guardrails

### Step 5: Correlate Static Predictions with Dynamic Results

Compare the `predicted_failure_modes` in `static-analysis.json` against the actual pattern of assertion failures. This validates the static model and sharpens your iteration priorities.

| Static Prediction | Look for in Dynamic Results |
|------------------|-----------------------------|
| Low completeness | Agent stalls mid-workflow, asks clarifying questions, or skips required steps |
| Low determinism | High stddev on pass rates; same assertion passes in some runs, fails in others |
| Low consistency | Different runs produce different tool names, paths, or output formats for the same task |
| Low usability | Assertions fail when test inputs vary slightly from the skill's assumed context |
| Over-specification flagged | Assertions pass for the original instance but fail on the over-specification variant case |
| Low invocability | Should-trigger case fails (skill not selected); should-not-trigger case fails (skill incorrectly selected) |

When a predicted failure mode is confirmed by dynamic results, the iteration fix is clear. When a prediction doesn't match (e.g., low determinism predicted but stddev is low), the static rubric may have been too conservative — update the `static-analysis.json` notes for future reference.

## Planning Improvements

### Signals → Changes

| Signal | Typical Fix |
|--------|-------------|
| Assertion fails because skill misses a step | Add or clarify the step in the workflow |
| Human feedback says output is poorly structured | Add an output template or tighten the existing one |
| Transcript shows agent ignored an instruction | Instruction may be ambiguous — add reasoning ("Do X because Y") |
| Transcript shows agent did unnecessary work | Remove or simplify over-prescriptive instructions |
| Same helper script written independently every run | Bundle the script in `scripts/` |
| Pass rate plateau despite adding rules | Skill may be over-constrained — try removing instructions |

### Generalize, Don't Patch

When a test case fails, the fix should address the underlying issue broadly — not add a narrow rule that only fixes that specific test case. The skill will be used across many prompts, not just the test set.

**Bad fix**: "When the user asks about revenue, always include a bar chart"
**Good fix**: "When the task involves data comparison, visualize results using an appropriate chart type"

### Keep It Lean

Fewer, better instructions outperform exhaustive rules. Each iteration should consider:
- Can any instructions be removed without hurting pass rates?
- Are there redundant instructions saying the same thing differently?
- Do MUST DO / MUST NOT DO constraints contradict each other?

### Reasoning Over Commands

"Do X because Y tends to cause Z" works better than "ALWAYS do X, NEVER do Y." Models follow instructions more reliably when they understand the purpose. Reserve hard commands for exact syntax, format, or safety requirements.

## Stopping Criteria

Stop iterating when:
1. Human feedback is consistently empty across all test cases
2. Pass rate improvements between iterations are <5 percentage points
3. The cost-quality tradeoff (delta) is acceptable for the use case
4. You've completed 3–5 iterations (diminishing returns beyond this)

## Cross-Iteration Comparison

Compare benchmark.json across iterations to track progress:

| Metric | Iteration 1 | Iteration 2 | Iteration 3 |
|--------|-------------|-------------|-------------|
| Pass rate (skill) | 0.58 | 0.75 | 0.83 |
| Pass rate (baseline) | 0.33 | 0.33 | 0.33 |
| Delta | 0.25 | 0.42 | 0.50 |
| Avg tokens | 2800 | 3200 | 3800 |

This table tells you: "The skill went from +25pp to +50pp improvement over baseline, but token usage grew 36%. Is the quality gain worth the cost?"
