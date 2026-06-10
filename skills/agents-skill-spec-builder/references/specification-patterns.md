# Specification Patterns

Ready-to-use workflow specification templates for common skill archetypes. Select the pattern that matches the skill's execution shape, then customize.

## Pattern 1: Linear Pipeline

Sequential transformation — each step produces an artifact consumed by the next.

```yaml
name: "<skill-name>"
goal: "Given {{input}}, produce {{final_output}} through sequential transformation"
config:
  parameters:
    input: "<description>"
workflow:
  - task:
      instruction: "Analyze {{input}} and extract structured elements"
      save_as: "extracted_elements"
  - task:
      instruction: "Transform {{extracted_elements}} into {{intermediate_format}}"
      save_as: "transformed"
  - task:
      instruction: "Produce final {{output_type}} from {{transformed}}"
      save_as: "final_output"
```

**Best for:** Content creation, data transformation, document generation, code generation.

**Verification focus:** Each step's output format matches the next step's expected input.

---

## Pattern 2: Branch and Merge

Decision point routes to different processing paths, results converge.

```yaml
name: "<skill-name>"
goal: "Given {{input}}, classify and apply the appropriate processing strategy"
config:
  parameters:
    input: "<description>"
workflow:
  - task:
      instruction: "Classify {{input}} into one of: [category_a, category_b, category_c]"
      save_as: "classification"
  - switch:
      on: "{{classification}}"
      cases:
        category_a:
          - task:
              instruction: "Apply strategy A to {{input}}"
              save_as: "processed"
        category_b:
          - task:
              instruction: "Apply strategy B to {{input}}"
              save_as: "processed"
        category_c:
          - task:
              instruction: "Apply strategy C to {{input}}"
              save_as: "processed"
  - task:
      instruction: "Finalize {{processed}} with quality checks and formatting"
      save_as: "final_output"
```

**Best for:** Triage, routing, adaptive processing, context-dependent workflows.

**Verification focus:** All branches produce the same output variable; the merge step handles all possible branch outputs.

---

## Pattern 3: Iterative Refinement

Loop that improves output until quality threshold is met.

```yaml
name: "<skill-name>"
goal: "Given {{input}}, iteratively refine until {{quality_criteria}} is satisfied"
config:
  parameters:
    input: "<description>"
    quality_criteria: "<description>"
    max_rounds: 3
workflow:
  - task:
      instruction: "Produce initial {{output_type}} from {{input}}"
      save_as: "draft"
  - set_variable:
      name: "quality_score"
      value: 0
  - while:
      condition: "{{quality_score}} < {{quality_threshold}}"
      max_iterations: "{{max_rounds}}"
      do:
        - task:
            instruction: "Evaluate {{draft}} against {{quality_criteria}}. Score 1-10. List specific improvements needed."
            save_as: "feedback"
        - task:
            instruction: "Extract numeric score from {{feedback}}"
            save_as: "quality_score"
        - task:
            instruction: "Revise {{draft}} addressing each point in {{feedback}}"
            save_as: "draft"
  - task:
      instruction: "Finalize {{draft}} with final polish"
      save_as: "final_output"
```

**Best for:** Writing, design, code quality, any skill where output quality benefits from structured iteration.

**Verification focus:** Loop variable is updated each iteration; `max_iterations` prevents runaway; exit condition is achievable.

---

## Pattern 4: Fan-Out / Fan-In

Parallel independent work followed by synthesis.

```yaml
name: "<skill-name>"
goal: "Given {{topic}}, research from multiple angles and synthesize findings"
config:
  parameters:
    topic: "<description>"
workflow:
  - task:
      instruction: "Decompose {{topic}} into 3-5 independent research angles"
      save_as: "research_angles"
  - parallel:
      - task:
          instruction: "Research angle 1: {{research_angles[0]}}"
          save_as: "findings_1"
      - task:
          instruction: "Research angle 2: {{research_angles[1]}}"
          save_as: "findings_2"
      - task:
          instruction: "Research angle 3: {{research_angles[2]}}"
          save_as: "findings_3"
  - task:
      instruction: "Synthesize {{findings_1}}, {{findings_2}}, {{findings_3}} into a unified analysis"
      save_as: "synthesis"
  - task:
      instruction: "Produce final report from {{synthesis}}"
      save_as: "final_report"
```

**Best for:** Research, competitive analysis, multi-perspective review, any skill benefiting from independent parallel investigation.

**Verification focus:** Parallel branches are truly independent; synthesis step accounts for all branch outputs.

---

## Pattern 5: Staged Pipeline with Iteration

Process a list of items through a submodule, then synthesize.

```yaml
name: "<skill-name>"
goal: "Given {{items}}, process each through {{processing_method}} and produce {{aggregate_output}}"
config:
  parameters:
    items: "<description of list input>"
workflow:
  - task:
      instruction: "Parse and validate {{items}}, producing a structured list"
      save_as: "validated_items"
  - for_each:
      items: "{{validated_items}}"
      as: "item"
      do:
        - call:
            module: "agents/item-processor.md"
            parameters:
              item: "{{item}}"
            save_as: "item_result"
      save_as: "all_results"
  - task:
      instruction: "Aggregate {{all_results}} into {{aggregate_format}}"
      save_as: "aggregated"
  - task:
      instruction: "Produce final {{output_type}} from {{aggregated}}"
      save_as: "final_output"
```

**Best for:** Batch processing, multi-document analysis, portfolio review, any skill that applies uniform processing to a collection.

**Verification focus:** Submodule contract (expected parameters and return type); aggregation handles variable-length results.

---

## Pattern 6: Hierarchical Composition

Complex skill assembled from reusable sub-skills.

```yaml
name: "<skill-name>"
goal: "Given {{input}}, produce {{complex_output}} by orchestrating specialized sub-workflows"
config:
  parameters:
    input: "<description>"
workflow:
  - task:
      instruction: "Analyze {{input}} and produce an execution plan with phases"
      save_as: "execution_plan"
  - call:
      module: "agents/phase-1-specialist.md"
      parameters:
        plan: "{{execution_plan}}"
        input: "{{input}}"
      save_as: "phase_1_output"
  - call:
      module: "agents/phase-2-specialist.md"
      parameters:
        plan: "{{execution_plan}}"
        prior_work: "{{phase_1_output}}"
      save_as: "phase_2_output"
  - call:
      module: "agents/phase-3-specialist.md"
      parameters:
        plan: "{{execution_plan}}"
        prior_work: "{{phase_2_output}}"
      save_as: "phase_3_output"
  - task:
      instruction: "Integrate {{phase_1_output}}, {{phase_2_output}}, {{phase_3_output}} into final deliverable"
      save_as: "final_output"
```

**Best for:** Complex multi-domain skills, skills requiring distinct expertise per phase, large skills that exceed single-file complexity.

**Verification focus:** Each submodule has a clear contract; orchestrator does not duplicate submodule logic; integration step accounts for all phase outputs.

---

## Pattern Selection Guide

| Skill Characteristics | Recommended Pattern |
|---|---|
| Clear input → output, no decisions | Linear Pipeline |
| Output depends on input classification | Branch and Merge |
| Quality improves with iteration | Iterative Refinement |
| Multiple independent research/analysis threads | Fan-Out / Fan-In |
| Same operation applied to a list of items | Staged Pipeline |
| Multiple distinct expertise areas needed | Hierarchical Composition |
| Complex skill combining several of the above | Compose patterns — use submodules to nest patterns within patterns |
