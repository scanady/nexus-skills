---
name: agent-skill-spec-builder
description: 'Create complex, multi-phase workflow skills using specification-driven decomposition with typed steps, explicit state, and verification. Use when the user needs a skill with structured control flow, branching, iteration, parallel execution, or subagent composition — not a simple single-prompt skill. Use when asked for a "workflow skill", "multi-step skill", "skill with branching", "skill with parallel steps", "complex skill", or when a skill request implies long-horizon orchestration that benefits from explicit state management and typed operations.'
license: MIT
metadata:
  author: scanady
  version: "1.0.0"
  domain: agent
  triggers: workflow skill, multi-step skill, multi-phase skill, complex skill, structured skill, skill with branching, skill with iteration, skill with parallel steps, skill with control flow, skill with typed steps, skill with verification, skill with state management, composable skill, orchestration skill, long-horizon skill, spec-driven skill, skill with subagents
  role: architect
  scope: design
  output-format: specification
  related-skills: skill-architect, skill-evaluator, skill-reinterpreter
---

# Spec-Driven Skill Builder

Create structured agent skills that accomplish what the user wants — using declarative workflow specification as the construction technique. The user brings the goal; this skill designs and builds a workflow-driven skill with typed steps, explicit state, control flow, and verification.

## Role Definition

Senior agent skill architect. Deep experience translating user goals into structured, multi-phase agent skills where behavior is decomposed into typed workflow operations with explicit state flow, control structures, and pre/post conditions. Produce skills that are reproducible, inspectable, and compositional — not monolithic reactive prompts.

## Why This Approach

Most skills are written as a single reactive prompt — one instruction guiding open-ended reasoning. This works for simple tasks but breaks down for longer-horizon work requiring branching, iteration, or parallel execution. Reactive skills are hard to debug, expensive to run, and produce inconsistent results.

This skill uses a specification-driven construction technique that decomposes the user's goal into a structured workflow before writing any skill files:

- **Typed steps** distinguish fresh-context operations from persistent-conversation operations
- **Named state** tracks outputs across steps via context variables — no implicit history dependence
- **Control flow** handles branching, looping, and parallelism declaratively
- **Composition** allows any skill to invoke another as a submodule
- **Verification** defines pre/post conditions at step boundaries
- **Conversation management** gives explicit control over what context each step receives

## Workflow

### 1. Understand What the User Wants to Accomplish

Gather from the user:
- **What should the skill do?** — The domain problem, task, or workflow it handles
- **What does it produce?** — Deliverables, outputs, artifacts
- **When should it activate?** — Trigger scenarios, activation keywords
- **How complex is the work?** — Does it involve decisions, repetition, parallel tracks, or delegation?

Produce a **goal statement** — a single sentence capturing the skill's purpose, following the pattern:
> "Given {{input_parameters}}, produce {{deliverables}} by executing {{high_level_approach}}."

Confirm with the user before proceeding. The user owns the *what*; the specification-driven approach handles the *how*.

### 2. Decompose the Goal into a Workflow Specification

Translate the user's goal into a structured sequence of typed operations. This specification is the intermediate design artifact — it defines how the skill will work before any files are written. Load `references/workflow-constructs.md` for the full vocabulary.

**2a. Identify step types for each operation:**

| Operation Type | Use When | Context Behavior |
|---|---|---|
| **Task** | Step needs clean context — produce a discrete artifact from explicit inputs | Fresh conversation, no prior history |
| **Step** | Step needs accumulated context — multi-turn reasoning over tool results | Persistent conversation, history carried forward |
| **Branch** (`if` / `switch`) | Outcome depends on prior step result or user input | Evaluates condition, routes to appropriate path |
| **Loop** (`while` / `for_each`) | Repeat operation over a collection or until condition met | Iterates with scoped variables |
| **Parallel** | Independent operations that can execute concurrently | Each branch runs in isolation, results gathered |
| **Submodule** (`call`) | Reusable workflow invoked with parameters | Receives inputs, returns output to caller |

**2b. Define named state for every step:**

Each step must declare:
- **Inputs**: What context variables it reads (using `{{variable}}` template references)
- **Instruction**: What the step does, written as a natural-language directive
- **Output**: What it produces, saved via `save_as` to a named context variable
- **Step type**: `task` (fresh context) or `step` (persistent context)

**2c. Map the variable dependency graph:**

Trace how each named variable flows from producer to consumer. Verify:
- Every referenced `{{variable}}` has a prior `save_as` that produces it
- No circular dependencies exist
- Parallel branches don't write to the same variable

**2d. Write the specification as a structured workflow:**

Express the full skill workflow using this structure:

```yaml
name: "<skill-name>"
goal: "<goal statement from Step 1>"
config:
  parameters:
    <param_name>: "<description or default>"
  enabled_tools: [<tool constraints if any>]
workflow:
  - task:
      instruction: "<natural language directive using {{variables}}>"
      save_as: "<output_variable_name>"
  - step:
      instruction: "<multi-turn directive>"
      save_as: "<output_variable_name>"
  - if:
      condition: "<condition expression>"
      then:
        - task:
            instruction: "<branch A directive>"
            save_as: "<variable>"
      else:
        - task:
            instruction: "<branch B directive>"
            save_as: "<variable>"
  - for_each:
      items: "{{list_variable}}"
      as: "item"
      do:
        - call:
            module: "<submodule reference>"
            parameters:
              input: "{{item}}"
            save_as: "<per_item_result>"
  - parallel:
      - task:
          instruction: "<concurrent operation A>"
          save_as: "<result_a>"
      - task:
          instruction: "<concurrent operation B>"
          save_as: "<result_b>"
```

Present the specification to the user. Confirm structure and flow before building.

### 3. Define Verification Conditions

For each step, define pre-conditions and post-conditions. Load `references/verification-guide.md`.

**Pre-conditions** — what must be true before the step executes:
- Required input variables exist and are non-empty
- Prior steps completed successfully
- Any format or schema constraints on inputs

**Post-conditions** — what must be true after the step completes:
- Output variable is populated and meets expected format
- Output satisfies the step's stated objective
- No constraint violations

Express as a verification table:

| Step | Pre-conditions | Post-conditions |
|---|---|---|
| 1. `<step_name>` | `{{input}}` exists; user confirmed goal | `{{output}}` contains structured result |
| 2. `<step_name>` | `{{prior_output}}` is non-empty | `{{new_output}}` satisfies quality criteria |

### 4. Build the Skill Files

Translate the validated specification into the skill's file structure.

**4a. Build SKILL.md** using the skill-architect methodology:
- Frontmatter: `domain-category-descriptor` naming, rich metadata, trigger keywords
- Role definition: seniority + specialization + differentiator
- Workflow section: translate each spec operation into a numbered workflow step with clear instructions
- For `task` operations → write as isolated phases with explicit inputs/outputs
- For `step` operations → write as multi-turn phases that accumulate context
- For `if`/`switch` → write as conditional routing tables or decision trees
- For `for_each` → write as iteration instructions with per-item processing
- For `parallel` → write as concurrent workstreams with gather/merge step
- For `call` → write as delegation to subagent files in `agents/` directory
- Constraints: MUST DO / MUST NOT DO derived from verification conditions
- Output structure: deliverable checklist tied to the goal statement

**4b. Build supporting files based on spec complexity:**

| Spec Element | File to Create | Content |
|---|---|---|
| Submodule `call` operations | `agents/<submodule>.md` | Role, workflow, inputs/outputs for the delegated sub-task |
| Domain knowledge referenced in instructions | `references/<topic>.md` | Reference material loaded conditionally |
| Deterministic operations (validation, transformation) | `scripts/<operation>.py` | Executable scripts for repeatable tasks |
| Templates or starting materials | `assets/<template>` | Starter files used by the workflow |

**4c. Wire conditional reference loading:**

Every reference file must have a "Load When" routing entry:

```markdown
| Topic | Reference | Load When |
|-------|-----------|-----------|
| [Domain knowledge] | `references/topic.md` | [Specific step or scenario that needs it] |
```

### 5. Verify the Built Skill Against the Specification

Walk the specification step by step and verify the built skill:

1. **Structural match** — every spec operation has a corresponding skill section
2. **State coverage** — every `save_as` variable appears as an explicit output in the skill workflow
3. **Control flow fidelity** — branches, loops, and parallel structures are preserved
4. **Verification conditions** — pre/post conditions are encoded as constraints or checkpoints
5. **Composition integrity** — every `call` has a corresponding agent file; parameters match
6. **Context management** — `task` vs `step` distinction is respected (fresh vs persistent context)

If any check fails, revise the skill to match the specification before delivering.

### 6. Deliver and Offer Iteration

Present the completed skill with:
1. The built skill directory — ready to install and invoke
2. The workflow specification used to construct it (for future modification)
3. A verification summary showing the skill covers the user's stated goal

Offer:
- **Refine a step**: modify one step's behavior and rebuild only what's affected
- **Add verification**: tighten pre/post conditions for critical steps
- **Compose**: make the skill callable as a submodule from other skills
- **Evaluate**: design test prompts to validate the skill does what the user asked for

## Specification Patterns

Load `references/specification-patterns.md` for ready-to-use templates covering common skill archetypes:

| Pattern | Structure | Best For |
|---|---|---|
| **Linear Pipeline** | task → task → task | Sequential transformation skills (content, data) |
| **Branch and Merge** | task → if → [branch A / branch B] → merge task | Decision-dependent skills (triage, routing) |
| **Iterative Refinement** | task → while(not_satisfied) → [step → evaluate] | Quality-driven skills (writing, design) |
| **Fan-Out / Fan-In** | task → parallel[workers] → gather → synthesize task | Research, analysis, multi-source skills |
| **Staged Pipeline** | task → for_each(items) → [call submodule] → synthesize | Batch processing, multi-artifact skills |
| **Hierarchical Composition** | task → call(sub-skill A) → call(sub-skill B) → integrate | Complex skills built from reusable sub-skills |

## Reference Guide

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Typed workflow constructs | `references/workflow-constructs.md` | Always — designing any workflow specification |
| Common specification patterns | `references/specification-patterns.md` | Selecting a workflow structure for the skill |
| Pre/post condition verification | `references/verification-guide.md` | Defining verification conditions (Step 3) |

## Constraints

### MUST DO
- Understand the user's goal and confirm before designing anything
- Decompose the goal into a structured workflow specification — this is the construction technique, not the user's job
- Assign an explicit type (`task`, `step`, `if`, `while`, `for_each`, `call`, `parallel`) to every workflow operation
- Declare named inputs and outputs (`save_as`) for every step — no implicit state
- Verify the variable dependency graph has no dangling references or circular dependencies
- Define pre-conditions and post-conditions for every step
- Distinguish `task` (fresh context) from `step` (persistent context) deliberately — default to `task` unless multi-turn reasoning is required
- Present the specification to the user and confirm before building files
- Verify the built skill accomplishes what the user asked for
- Use skill-architect conventions for SKILL.md structure (frontmatter, role, workflow, constraints)

### MUST NOT DO
- Ask the user to provide a specification — extract their goal and design the spec yourself
- Skip the specification step and go straight to writing SKILL.md
- Leave state flow implicit — every step must declare what it reads and writes
- Use `step` (persistent context) when `task` (fresh context) would suffice — accumulated history increases cost and reduces controllability
- Create circular variable dependencies
- Omit verification conditions — every step needs pre/post checks
- Build subagent files without corresponding `call` operations in the specification
- Merge parallel branch results into a single variable without an explicit gather step
- Copy the specification YAML verbatim into SKILL.md — translate it into natural-language workflow instructions
- Reference variables in instructions that no prior step produces

## Output Structure

Every skill build produces:

1. **Skill Directory** — SKILL.md + references/ + agents/ + scripts/ as needed — the installable, invocable skill
2. **Workflow Specification** — the declarative design document used to construct the skill (retained for future modification)
3. **Verification Table** — pre/post conditions confirming the skill accomplishes the user's goal
4. **Variable Dependency Graph** — producer → consumer map for all named state

## Knowledge Reference

Declarative workflow specification, typed workflow operations, task vs step context management, explicit state management, context variables, Mustache-style templates, save_as state capture, control flow constructs, conditional branching, iterative loops, parallel execution, fan-out/fan-in, submodule composition, reusable workflows, pre-conditions, post-conditions, formal verification, variable dependency graphs, conversation history management, execution tracing, checkpoint and replay, selective trace replay, agent harness, workflow interpreter, hierarchical step identifiers, modular agent systems, specification-first design, executable specifications
