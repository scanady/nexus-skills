---
description: Generate a new agent and prompt file following Copilot best practices
agent: agent
---

# Prompt File Generator

## Purpose

This meta-prompt generates well-structured agent prompt files based on the users objectives while automatically following GitHub Copilot best practices. It analyzes your requirements and creates a complete, ready-to-use agent prompt file with proper structure, variables, validation steps, and context references.

## What I Need From You

**Task description:**
${input:taskDescription:Describe what this prompt should accomplish (e.g., "Generate an agent that is an expert software engineer skilled in solution reviews that will provide a comprehensive analysis of the project" or "Create an agent that is a technology analyst to evalute the product market fit for this project")}

**Agent name:**
${input:agentName:Name for the agent in kebab-case (e.g., "react-component-generator" or "api-endpoint-creator")}

**Target audience:**
${input:targetAudience:Who will use this prompt? (e.g., "frontend team", "all developers", "personal use")}

**Expected output:**
${input:expectedOutput:What should this prompt produce? (e.g., "Comprehensive solution review report" or "Evaluation of product market fit with recommendations")}

**Output type:**
${input:outputType:Output format - "prompt" (default, single prompt file) or "agent" (agent file + pointer prompt file)}

## Output Specification

### Default: Prompt File Only (outputType = "prompt")

Create **one file** containing all instructions, requirements, examples, and validation:

| File | Location | Purpose |
|------|----------|---------|
| Prompt File | `.github/prompts/[descriptive-name].prompt.md` | Self-contained prompt with all instructions, requirements, examples, and validation |

### Agent Mode (outputType = "agent")

Create **two files** when the user explicitly requests an agent:

| File | Location | Purpose |
|------|----------|---------|
| Agent File | `.github/agents/[descriptive-name].agent.md` | Contains all instructions, requirements, examples, and validation |
| Prompt File | `.github/prompts/[descriptive-name].prompt.md` | Points to the agent file with frontmatter: `agent: [descriptive-name]` |

**Filename format:** Use kebab-case (e.g., `react-component-generator`, `api-endpoint-crud`)

## Analysis

Before generating, analyze:
1. Should tools be restricted? (only if limiting available tools, otherwise omit)
2. Should a specific model be recommended? (only if task requires specific capabilities, otherwise omit)
3. What variables should be included for dynamic inputs?
4. What context should be referenced? (files, tools, codebase)

**Important:** Base all specifics on what the user provides. Do not assume project structures, tech stacks, commands, or conventions unless explicitly provided.

## Agent File Structure

Create a complete prompt or agent file (`.prompt.md` or `.agent.md`) with the following structure:

### 1. YAML Frontmatter

**For Prompt File (default):**
```yaml
---
description: [One-sentence description of what this prompt does]
tools: [only include if you need to restrict tools - omit for default access]
model: [only include if task requires specific model - omit to let user choose]
---
```

**For Agent File (when outputType = "agent"):**
```yaml
---
description: [One-sentence description of what this agent does]
tools: [only include if you need to restrict tools - omit for default access]
model: [only include if task requires specific model - omit to let user choose]
---
```

**For Pointer Prompt File (when outputType = "agent"):**
```yaml
---
agent: [agent-name]
---
```

**Note:** Only include `tools` if you want to limit available tools (e.g., read-only prompts). Only include `model` if the task requires specific model capabilities (e.g., vision processing, advanced reasoning). Otherwise omit both for flexibility.

### 2. Prompt Title and Context
- Clear title describing the task
- Brief context explaining the purpose
- Reference to any relevant project standards or patterns

### 3. Input Variables
Define all necessary variables using this format:
```
Variable name: ${input:variableName:Descriptive prompt for user}
```

Include variables for:
- Core inputs required for the task
- Optional configuration parameters
- Target locations or file patterns

### 4. Requirements Section
List specific requirements based on the user's task description:
```markdown
## Requirements

1. **Requirement Category:** Description based on user's needs
   - Specific detail from user input
   - Another specific detail

2. **Another Category:** Description relevant to the task
   - Details here
```

Cover areas relevant to the user's task, which may include:
- Technical requirements (if specified by user)
- Code quality standards (if mentioned by user)
- Testing requirements (if applicable to the task)
- Documentation needs (if part of expected output)
- Performance considerations (if relevant to the task)

**Note:** Only include requirement categories that are relevant to the specific task the user described. Do not assume generic requirements unless they apply to the stated objective.

### 5. Expected Output
Clearly define what files or artifacts should be created based on user's requirements:
```markdown
## Expected Output

1. Create file: `path/to/file.ext` (use paths from user's description)
2. Update file: `path/to/existing.ext` (if applicable)
3. Generate documentation: `docs/filename.md` (if applicable)
```

**Important:** Use file paths and structures that match what the user described in their task description. Do not assume specific directory structures unless provided.

### 6. Code Examples or Patterns
If applicable, include examples showing:
- Expected code structure
- Good vs. bad patterns
- Specific syntax or conventions

Use this format:
```markdown
## Examples

**Good:**
```language
// Example of good implementation
```

**Avoid:**
```language
// Example of what not to do
```
```

### 7. Context References
Include references to relevant context as provided by the user:
- Related files: `#file:path/to/file` (only if user provides file paths)
- Tools to use: `#tool:toolName`
- Codebase search: `#codebase`
- Similar patterns: Search instructions

Example:
```markdown
## Context

Follow the patterns in #file:src/components/Example.tsx
Search for similar implementations: #tool:search pattern-name
```

**Note:** Only include specific file references if the user has provided them in the task description or context.

### 8. Validation Steps
Define how to verify success based on the task requirements:
```markdown
## Validation Steps

After generation:
1. Run `command` - expected result (use commands appropriate to the task)
2. Check for [specific criteria relevant to the output]
3. Verify [another criteria based on requirements]
4. Manual test: [specific steps if applicable]
```

**Note:** Validation commands and steps should be appropriate to the user's described task and environment. Do not assume specific build tools or commands unless the user mentioned them.

### 9. Additional Notes (Optional)
Include relevant considerations based on the task:
- Edge cases to consider
- Common pitfalls to avoid
- Performance tips (if relevant to the task)
- Security considerations (if relevant to the task)

**Note:** Only include notes that are relevant to the specific task. Base these on the user's described requirements, not on assumed project standards.

## Best Practices to Apply

Ensure the generated agent file follows these principles:

1. **User-Driven Content:** Base all specific details on what the user provides - do not assume project structures, tech stacks, or conventions
2. **Specificity:** Be precise about requirements, avoid vague instructions
3. **Self-Contained:** Include all necessary context and instructions
4. **Clear Variables:** Use descriptive variable names and helpful prompts
5. **Actionable Requirements:** Provide specific, testable requirements
6. **Success Criteria:** Define clear validation steps
7. **Context Rich:** Reference relevant files, tools, and patterns that the user has provided
8. **Example Driven:** Show concrete examples of expected output
9. **Minimal Configuration:** Only specify tools or model when necessary to restrict or require specific capabilities

## Example

**Prompt File Only (default):**
For a task like "Generate a new React component with tests":
1. Create a self-contained prompt file with: proper frontmatter, variables for component details, TypeScript/testing requirements, validation steps, and code examples
2. Confirm creation and provide usage instructions

**Agent + Prompt Files (when outputType = "agent"):**
For a task like "Generate a new React component with tests":
1. Create agent file with: proper frontmatter, variables for component details, TypeScript/testing requirements, validation steps, and code examples
2. Create pointer prompt file with agent reference in frontmatter
3. Confirm creation and provide usage instructions

## Execution Steps

### For Prompt File Only (default):
1. Create `.github/prompts` directory if it does not exist
2. Save the prompt file to `.github/prompts/[name].prompt.md`
3. Confirm the file was created successfully
4. Provide the file path and brief usage instructions

### For Agent + Prompt Files (when outputType = "agent"):
1. Create `.github/agents` and `.github/prompts` directories if they do not exist
2. Save the agent file to `.github/agents/[name].agent.md`
3. Save the pointer prompt file to `.github/prompts/[name].prompt.md`
4. Confirm files were created successfully
5. Provide the file paths and brief usage instructions