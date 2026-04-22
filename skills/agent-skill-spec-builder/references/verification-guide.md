# Verification Guide

Define and check pre-conditions and post-conditions at every step boundary. Verification makes skill behavior predictable, debuggable, and reproducible.

## Why Verify

Without explicit verification:
- Steps silently consume malformed inputs and produce degraded outputs
- Failures propagate downstream before detection
- Debugging requires replaying the entire workflow to find the failure point
- Skill behavior varies unpredictably across runs

With verification:
- Failures are caught at the step that caused them
- Each step's contract is documented and enforceable
- Selective replay can resume from the last verified checkpoint
- Skill behavior is reproducible and inspectable

## Pre-Conditions

Pre-conditions define what must be true **before** a step executes. They gate execution — if a pre-condition fails, the step should not run.

### Common Pre-Condition Types

| Type | Check | Example |
|---|---|---|
| **Existence** | Required variable exists and is non-empty | `{{research_angles}}` is populated |
| **Format** | Variable matches expected structure | `{{feature_list}}` is a structured list, not prose |
| **Cardinality** | Collection has expected number of items | `{{competitors}}` contains 2-5 entries |
| **Dependency** | Prior step completed successfully | Step 2 output was saved |
| **User confirmation** | User approved a prior result | User confirmed the goal statement |
| **Constraint** | Value is within acceptable bounds | `{{iteration_count}}` < `{{max_iterations}}` |

### Writing Pre-Conditions

Express as testable assertions:

```
Pre-conditions for Step 3 (Draft Report):
- {{research_findings}} exists and contains structured findings from Step 2
- {{report_template}} is defined in config.parameters
- {{audience}} was confirmed by user in Step 1
```

## Post-Conditions

Post-conditions define what must be true **after** a step completes. They validate output quality and correctness.

### Common Post-Condition Types

| Type | Check | Example |
|---|---|---|
| **Completeness** | Output contains all required sections | Report has intro, body, and conclusion |
| **Format compliance** | Output matches expected structure | `{{analysis}}` is valid JSON / structured markdown |
| **Quality threshold** | Output meets minimum quality bar | Evaluation score >= 7/10 |
| **Constraint satisfaction** | Output respects stated constraints | Word count within specified range |
| **Non-regression** | Output is not worse than prior iteration | Revised draft addresses all feedback points |
| **Contract match** | Output satisfies the step's stated objective | "Produce a ranked list" → output is actually ranked |

### Writing Post-Conditions

Express as verifiable statements:

```
Post-conditions for Step 3 (Draft Report):
- {{draft_report}} is saved and non-empty
- {{draft_report}} contains all sections specified in {{report_template}}
- {{draft_report}} addresses all points from {{research_findings}}
- {{draft_report}} is written for {{audience}} (tone and complexity match)
```

## Verification Table Template

Build one row per step. This becomes the authoritative verification contract for the skill.

```markdown
| Step | Operation | Pre-conditions | Post-conditions |
|------|-----------|----------------|-----------------|
| 1 | task: Elicit goal | User provided input | {{goal_statement}} is a single sentence with input/output/approach |
| 2 | task: Decompose | {{goal_statement}} confirmed by user | {{research_angles}} is a list of 3-5 independent angles |
| 3 | parallel: Research | {{research_angles}} has 3+ items | Each {{findings_N}} contains sourced, structured findings |
| 4 | task: Synthesize | All {{findings_N}} are populated | {{synthesis}} integrates all findings without omission |
| 5 | task: Final report | {{synthesis}} is complete | {{final_report}} is formatted, complete, meets quality bar |
```

## Variable Dependency Graph

Map every context variable from producer to consumer. This catches:
- **Dangling references**: a step reads `{{variable}}` that no prior step produces
- **Dead writes**: a step produces a variable that no subsequent step reads
- **Shadow writes**: two steps write to the same variable outside a loop
- **Circular dependencies**: step A reads from step B which reads from step A

### Building the Graph

```
config.parameters.topic → Step 1 (reads {{topic}})
Step 1 → {{research_angles}} → Step 2 (reads {{research_angles}})
Step 2 → {{findings_1}}, {{findings_2}}, {{findings_3}} → Step 3 (reads all)
Step 3 → {{synthesis}} → Step 4 (reads {{synthesis}})
Step 4 → {{final_report}} [terminal output]
```

### Validation Checklist

- [ ] Every `{{variable}}` in an instruction has a producer (save_as or config.parameters)
- [ ] Every `save_as` variable has at least one consumer (unless it is the final output)
- [ ] No variable is written by two different steps in the same scope
- [ ] Loop variables (`as` in `for_each`) are only referenced inside the loop body
- [ ] Submodule parameters are explicitly passed — no implicit variable leakage
- [ ] Parallel branches write to distinct variables

## Checkpoint Strategy

For long-running workflows, define checkpoint boundaries — points where execution state can be saved and resumed.

### Checkpoint Placement Rules

- **After every task/step**: save the produced context variable
- **Before branching**: save the condition variable and current state
- **At loop iteration boundaries**: save iteration index and accumulated results
- **After submodule return**: save the returned value
- **After parallel gather**: save all gathered results

### Hierarchical Step Identifiers

Assign each operation a hierarchical ID for traceability:

```
1       — Step 1 (top-level)
2       — Step 2 (top-level)
3       — for_each loop
3.1     — first iteration
3.1.1   — first operation in first iteration
3.2     — second iteration
4       — Step 4 (top-level)
```

Use these IDs in the verification table, checkpoint records, and execution traces.

## Selective Trace Replay

When modifying a single step in a workflow:

1. Load execution trace from a prior successful run
2. Replay steps 1 through N-1 from the trace (restoring their outputs without re-executing)
3. Execute the modified step N with live execution
4. Continue live execution for steps N+1 onward

This isolates the effect of a change without re-running the entire workflow. Useful during:
- Prompt iteration on a specific step
- Debugging a step that produces unexpected output
- A/B testing different instructions for the same step

## Translating Verification to Skill Constraints

Verification conditions map directly to the skill's MUST DO / MUST NOT DO section:

| Verification Element | Skill Constraint |
|---|---|
| Pre-condition: required input | MUST validate that {{input}} exists before proceeding |
| Post-condition: format compliance | MUST produce output in {{specified_format}} |
| Post-condition: quality threshold | MUST evaluate output against criteria before delivering |
| Variable dependency: no dangling refs | MUST NOT reference context from steps that haven't executed |
| Checkpoint: resumability | MUST save intermediate artifacts to enable selective replay |
| Loop guard: max iterations | MUST NOT iterate more than {{max_iterations}} times |
