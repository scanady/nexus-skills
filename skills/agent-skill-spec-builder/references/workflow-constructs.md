# Workflow Constructs Reference

Vocabulary of typed operations for building declarative workflow specifications. Every operation in a skill specification must use one of these constructs.

## Invocation Constructs

### Task — Fresh Context Operation

Starts a new conversation with no prior history. Use when a step should produce a discrete artifact from explicit inputs only.

```yaml
- task:
    instruction: "Analyze {{user_requirements}} and produce a structured feature list"
    save_as: "feature_list"
```

**When to use task:**
- Step produces a self-contained artifact (summary, analysis, draft)
- Prior conversation history would add noise or cost without value
- Step reads from explicit context variables, not accumulated dialogue
- Step is a transformation: clear input → clear output

**When NOT to use task:**
- Step needs to reason over multiple tool-call results iteratively
- Step is a refinement pass that builds on an ongoing conversation

### Step — Persistent Context Operation

Continues an existing conversation, accumulating history across turns. Use when the operation requires multi-turn reasoning with tool calls.

```yaml
- step:
    instruction: "Search for implementations of {{feature}} and evaluate each against {{criteria}}"
    save_as: "evaluation_results"
```

**When to use step:**
- Operation involves multiple rounds of tool use (search → read → analyze → search again)
- Agent needs to reason over its own prior tool-call results
- Multi-turn refinement within a single phase

**When NOT to use step:**
- A single-shot transformation with clear input/output
- Accumulated history would degrade performance or increase cost unnecessarily

### Default Rule

Default to `task`. Only use `step` when persistent context is required for multi-turn reasoning. `task` is cheaper, more controllable, and more reproducible.

## Control Flow Constructs

### If / Switch — Conditional Branching

Routes execution based on a condition or the value of a context variable.

```yaml
- if:
    condition: "{{analysis_type}} == 'technical'"
    then:
      - task:
          instruction: "Perform technical architecture review of {{input}}"
          save_as: "review_result"
    else:
      - task:
          instruction: "Perform business strategy review of {{input}}"
          save_as: "review_result"
```

```yaml
- switch:
    on: "{{skill_archetype}}"
    cases:
      technical_execution:
        - task:
            instruction: "Design implementation workflow"
            save_as: "workflow"
      content_writing:
        - task:
            instruction: "Design content creation workflow"
            save_as: "workflow"
      research_analysis:
        - task:
            instruction: "Design research workflow"
            save_as: "workflow"
    default:
      - task:
          instruction: "Design generic workflow"
          save_as: "workflow"
```

**Design rules for branching:**
- Both branches must produce the same output variable name (for downstream compatibility)
- Keep branches shallow — deep nesting reduces readability
- Prefer `switch` over chained `if` when routing on a categorical variable
- Always include a `default` / `else` branch

### While — Conditional Loop

Repeats operations until a condition is met or iteration limit reached.

```yaml
- while:
    condition: "{{quality_score}} < 8"
    max_iterations: 3
    do:
      - task:
          instruction: "Improve {{draft}} based on {{feedback}}"
          save_as: "draft"
      - task:
          instruction: "Evaluate {{draft}} against {{criteria}} and score 1-10"
          save_as: "quality_score"
```

**Design rules for while loops:**
- Always set `max_iterations` — unbounded loops risk runaway execution
- The loop condition must reference a variable updated inside the loop body
- Include an explicit evaluation step that updates the loop variable

### For Each — List Iteration

Iterates over a collection, executing operations for each item.

```yaml
- for_each:
    items: "{{research_papers}}"
    as: "paper"
    do:
      - task:
          instruction: "Summarize key findings from {{paper}}"
          save_as: "paper_summary"
    save_as: "all_summaries"
```

**Design rules for for_each:**
- The `items` variable must be a list produced by a prior step
- The loop variable (`as`) is scoped to the loop body
- `save_as` on the `for_each` collects all iteration results into a list

## Composition Constructs

### Call — Submodule Invocation

Invokes another workflow (subagent) as a reusable module, passing parameters and receiving a return value.

```yaml
- call:
    module: "agents/research-synthesizer.md"
    parameters:
      sources: "{{gathered_sources}}"
      focus_area: "{{topic}}"
    save_as: "synthesis"
```

**Design rules for call:**
- The called module must define its expected parameters and return value
- Parameters are passed by value — the submodule cannot modify the caller's state
- Use `call` to extract reusable logic that appears in multiple places
- Use `call` when a workflow phase requires distinct expertise (delegate to a specialist subagent)

### Parallel / Gather — Concurrent Execution

Executes multiple independent operations concurrently and collects results.

```yaml
- parallel:
    - task:
        instruction: "Research competitor A: {{competitor_a}}"
        save_as: "analysis_a"
    - task:
        instruction: "Research competitor B: {{competitor_b}}"
        save_as: "analysis_b"
    - task:
        instruction: "Research competitor C: {{competitor_c}}"
        save_as: "analysis_c"
```

**Design rules for parallel:**
- Each parallel branch must be independent — no branch reads another branch's output
- Each branch writes to a distinct `save_as` variable
- Follow parallel with a merge/synthesis `task` that reads all branch outputs
- Use parallel when operations are independent and latency matters

## State Constructs

### Set Variable — Direct Assignment

Assigns a value to a context variable without invoking the model.

```yaml
- set_variable:
    name: "output_format"
    value: "markdown"
```

**Use for:** configuration values, computed defaults, aggregation setup.

### Input — User Prompt

Pauses execution to collect input from the user.

```yaml
- input:
    prompt: "Which analysis approach do you prefer?"
    options: ["deep-dive", "broad-survey", "comparative"]
    save_as: "user_preference"
```

**Use for:** decision points where user judgment is required, parameter collection.

### Return — Submodule Output

Returns a value from a submodule to the calling workflow.

```yaml
- return:
    value: "{{final_result}}"
```

**Use for:** the last operation in a submodule invoked via `call`.

## Context Variable Rules

### Template Syntax

Reference context variables using double-brace templates: `{{variable_name}}`

Variables are expanded in `instruction` fields before the operation executes.

### Producer-Consumer Contract

- Every `{{variable}}` referenced in an instruction must have a prior `save_as` that produces it, OR be defined in `config.parameters`
- A variable can be produced only once in a linear flow (reassignment in loops is the exception)
- Parallel branches must not write to the same variable

### Scoping

- Top-level variables are visible to all steps in the workflow
- Loop variables (`as` in `for_each`) are scoped to the loop body
- Submodule variables are isolated — pass explicitly via `parameters` and receive via `save_as`
