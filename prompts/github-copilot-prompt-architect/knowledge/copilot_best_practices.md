# Copilot Prompt and Agent Best Practices

## Overview
This document outlines best practices for creating effective Copilot prompts, reusable prompt files, and custom agents. The goal is to drive consistency, improve output quality, reduce rework, and support collaborative use across engineering teams.

## Core Principles

### Provide Clear Context
Give the AI a grounded understanding of the task, including project purpose, architecture, coding patterns, constraints, and expected outputs. Ambiguity leads to poor results.

### Use Well-Scoped Tasks
The most reliable outputs come from concise, bounded tasks. Avoid multi-layered or open-ended prompts. Break larger objectives into smaller steps when possible.

### Favor Reusable Instructions
Capture standards, conventions, and expectations in shared instruction files or prompt templates. Avoid rewriting requirements every time.

### Treat AI Output Like PRs
Review, test, and validate everything generated. Copilot accelerates work but does not replace architectural rigor or code reviews.

## Writing Effective Prompts

### Describe the Objective Clearly
State exactly what the output should accomplish. Include:
- The problem being solved.
- Expected format or structure.
- Any required constraints or exclusions.
- The files, modules, or boundaries the AI should stay within.

### Be Specific About Format
Define the form of the output:
- Code snippet
- Class or component
- Test suite
- Markdown document
- JSON object
- Refactored version of the existing file

Specific formats remove guesswork.

### Reference Existing Patterns
Point Copilot toward the patterns, structures, or style conventions already used in the repository. Consistency improves reliability.

### Provide Acceptance Criteria
Even simple criteria help:
- Inputs and expected behavior
- Error conditions
- Performance expectations
- Edge cases to consider
- Required documentation or comments

### Use Natural Language
The strongest prompts use straightforward, conversational language. Long lists of unnatural rules tend to reduce quality.

## Prompt File Best Practices

Prompt files allow repeatable, high-quality outputs for common tasks. Keep them simple, readable, and focused.

### Structure Prompt Files Intentionally
Each prompt file should include:
- A concise description of the purpose.
- Inputs or user-provided variables.
- Expected outputs.
- Constraints and guardrails.
- Step-by-step actions if the workflow requires them.

### Make Tasks Single-Purpose
Avoid “do everything” prompts. One prompt should map to one task:
- Generate tests.
- Refactor code.
- Scaffold a new module.
- Create documentation.
- Review changes.

### Parameterize When Appropriate
Use variables to allow prompt reuse across files or components. Provide examples when helpful.

### Store Prompt Files in Version Control
Treat them like a shared toolkit:
- Keep in a predictable folder such as `.copilot/prompts`.
- Keep them updated as standards or tooling evolve.
- Remove or refactor prompts that become outdated.

## Custom Agent Best Practices

Custom agents allow fully defined roles with scope, authority, and behavior. These become powerful when purpose-driven.

### Define a Narrow Role
Agents should be specialists, not generalists. Examples:
- Security reviewer
- API designer
- Documentation writer
- Architecture reviewer
- Unit test generator
- Code migration assistant

### Establish the Operating Boundaries
Specify:
- What the agent is allowed to modify.
- What it must not modify.
- Relevant languages or frameworks.
- Required tools or capabilities.
- Limits on scope or authority.

Narrow boundaries produce reliable behavior.

### Provide Persistent Context
Include in agent configuration:
- Architecture summaries
- Naming conventions
- Coding standards
- Test expectations
- Domain-specific rules
- Dependency or library preferences

Agents perform better when they have consistent, evergreen context.

### Encourage Agent Handoff
Complex tasks often require sequential roles:
- A design agent defines the structure.
- An implementation agent produces the code.
- A testing agent generates the tests.
- A documentation agent writes the usage guide.

Handoff workflows preserve clarity and reduce risk.

## Designing Tasks for Copilot Agents

### Keep Tasks Atomic
Provide one clear objective per request. Agents handle small, well-scoped tasks accurately and quickly.

### Place Prompts Close to the Work
Tasks embedded in comments near code tend to produce better results because Copilot can inspect local context.

### Avoid Overly Detailed or Overly Sparse Instructions
Balance matters:
- Too much detail can confuse.
- Too little detail produces generic output.

Aim for clarity over completeness.

### Use Recap or Confirmation Steps
Have the agent list its understanding of the task before generating the final output when the stakes are high. This catches misunderstandings early.

## Maintaining High-Quality Agent Behavior

### Review and Version Instructions
Treat agent configuration as software:
- Version it.
- Review it.
- Refactor to maintain clarity.
- Remove duplication.

### Standardize Folder Structure
Keep consistent structure such as:
```
.copilot/
  instructions/
  prompts/
  agents/
```

### Refresh as the Codebase Evolves
Agents and prompts must evolve with:
- New frameworks
- New architectural rules
- Updated linters or formatting tools
- Extended testing patterns
- Reorganized repositories

Stale instructions degrade output.

## Risk Management

### Prevent Architectural Drift
Codify architectural rules and boundaries in instruction files or agents. This prevents Copilot from generating code outside the intended design.

### Watch for Security or Performance Issues
Even strong models can introduce vulnerabilities. Use security-focused agents or explicit review prompts.

### Avoid Overscoped Agents
Broad, multi-purpose agents increase risk. Train smaller agents instead.

### Avoid Copy-Paste Problems
Large blocks of outdated or repeated instructions inside prompts create divergence. Keep reusable guidance in a single source.

## Summary

Effective Copilot usage depends on clarity, structure, and consistent boundaries. Strong prompts and agents:
- Provide sufficient context.
- Reflect coding and architecture standards.
- Have a narrow scope.
- Produce predictable, high-quality results.
- Fit into a workflow of review, testing, and refinement.

Teams that invest in reusable prompt files, disciplined agent design, and shared instruction libraries achieve higher productivity and significantly smoother adoption.
