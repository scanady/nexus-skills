# GitHub Copilot Agent and Prompt Best Practices

## Overview

This document provides comprehensive best practices for creating effective GitHub Copilot customizations including custom agents, custom instructions, and prompt files. These techniques enable you to build specialized AI assistants tailored to your development workflows, coding standards, and project requirements.

## Custom Agents (agents.md)

### What Are Custom Agents?

Custom agents are specialized AI assistants defined in `.agent.md` files that assume different personas optimized for specific development roles and tasks. Each agent has its own behavior, available tools, instructions, and optional language model preferences. Custom agents enable you to quickly switch between configurations without manually selecting tools and instructions each time.

### File Structure and Location

Custom agents are stored in `.agent.md` Markdown files with the following locations:

**Workspace agents** (team-shared):
- `.github/agents/[agent-name].agent.md`
- Available only within the workspace
- Shared with team through version control

**User profile agents** (personal):
- Stored in VS Code user profile
- Available across all workspaces
- Personal configurations not shared with team

### Agent File Format

Every agent file consists of YAML frontmatter followed by Markdown instructions:

```markdown
---
name: agent-name
description: Brief description of what this agent does
tools: ['tool1', 'tool2', 'tool3']
model: Claude Sonnet 4
handoffs:
  - label: Next Step
    agent: another-agent
    prompt: Continue with implementation
    send: false
---

# Agent Instructions

Your detailed instructions here...
```

### Frontmatter Properties

**Required properties:**

- `name`: Unique identifier for the agent (lowercase, hyphen-separated)
- `description`: One-sentence description of the agent's purpose

**Optional properties:**

- `tools`: Array of tools the agent can use. Omit to enable all tools.
- `model`: Preferred language model (e.g., "Claude Sonnet 4", "GPT-4o")
- `target`: Limit agent to specific environment ("vscode" or "github-copilot")
- `handoffs`: Define workflow transitions to other agents

### Core Principles for Effective Agents

Analysis of over 2,500 agent files reveals these patterns in successful implementations:

#### 1. Provide a Specific Persona

Avoid vague personas like "You are a helpful coding assistant." Instead, define explicit roles with clear boundaries:

**Good:**
```markdown
You are a test engineer who writes tests for React components, follows these examples, and never modifies source code.
```

**Better:**
```markdown
You are a testing specialist focused on improving code quality through comprehensive testing. You understand test patterns and translate code into comprehensive test suites that catch bugs early.
```

#### 2. Put Commands Early

Place executable commands in an early, prominent section. Include flags and options, not just tool names:

```markdown
## Commands You Can Use

- **Build:** `npm run build` (compiles TypeScript, outputs to dist/)
- **Test:** `npm test -- --coverage` (runs Jest with coverage report)
- **Lint:** `npm run lint --fix` (auto-fixes ESLint errors)
- **Type Check:** `tsc --noEmit` (validates TypeScript without building)
```

#### 3. Show Code Examples Over Explanations

One real code snippet demonstrating your style beats three paragraphs describing it:

```markdown
## Code Style Examples

**Good - descriptive names, proper error handling:**
```typescript
async function fetchUserById(id: string): Promise<User> {
  if (!id) throw new Error('User ID required');
  const response = await api.get(`/users/${id}`);
  return response.data;
}
```

**Bad - vague names, no error handling:**
```typescript
async function get(x) {
  return await api.get('/users/' + x).data;
}
```
```

#### 4. Set Clear Boundaries

Use a three-tier boundary system:

```markdown
## Boundaries

- ✅ **Always do:** Write to `src/` and `tests/`, run tests before commits, follow naming conventions
- ⚠️ **Ask first:** Database schema changes, adding dependencies, modifying CI/CD config
- 🚫 **Never do:** Commit secrets or API keys, edit `node_modules/` or `vendor/`, remove failing tests
```

Common helpful constraints:
- Never commit secrets (most common across successful agents)
- Never modify production configs
- Never touch vendor directories
- Never remove tests because they fail
- Read-only access to specific directories
- Require approval for destructive actions

#### 5. Be Specific About Tech Stack

Specify exact versions and key dependencies:

**Vague:**
```markdown
This is a React project with a Node backend.
```

**Specific:**
```markdown
**Tech Stack:**
- Frontend: React 18.2 with TypeScript 5.0, Vite 4.3, Tailwind CSS 3.3
- Backend: Node.js 20 LTS, Express 4.18
- Database: PostgreSQL 15 with Prisma 5.0 ORM
- Testing: Jest 29, React Testing Library 14, Playwright 1.40
```

#### 6. Cover Six Core Areas

Top-tier agents consistently address:

1. **Commands:** Executable commands with flags and descriptions
2. **Testing:** How to run tests, what framework, coverage requirements
3. **Project Structure:** Key directories and their purposes
4. **Code Style:** Naming conventions and pattern examples
5. **Git Workflow:** Commit message format, branching strategy
6. **Boundaries:** Three-tier system of always/ask/never

### Essential Agents to Build

#### Documentation Agent

Purpose: Reads code and generates or updates documentation

```markdown
---
name: docs-agent
description: Expert technical writer for this project
tools: ['read', 'write', 'search']
---

You are an expert technical writer for this project.

## Your Role

- You are fluent in Markdown and can read TypeScript code
- You write for a developer audience, focusing on clarity and practical examples
- Your task: read code from `src/` and generate or update documentation in `docs/`

## Project Knowledge

- **Tech Stack:** React 18, TypeScript, Vite, Tailwind CSS
- **File Structure:**
  - `src/` - Application source code (you READ from here)
  - `docs/` - All documentation (you WRITE to here)
  - `tests/` - Unit, Integration, and Playwright tests

## Commands You Can Use

- Build docs: `npm run docs:build` (checks for broken links)
- Lint markdown: `npx markdownlint docs/` (validates your work)

## Documentation Practices

- Be concise, specific, and value dense
- Write so that a new developer to this codebase can understand your writing
- Don't assume your audience are experts in the topic/area you are writing about

## Boundaries

- ✅ **Always do:** Write new files to `docs/`, follow the style examples, run markdownlint
- ⚠️ **Ask first:** Before modifying existing documents in a major way
- 🚫 **Never do:** Modify code in `src/`, edit config files, commit secrets
```

#### Test Agent

Purpose: Writes comprehensive tests without modifying production code

```markdown
---
name: test-agent
description: Writes unit tests, integration tests, and edge case coverage
tools: ['read', 'write', 'terminal']
---

You are a quality software engineer who writes comprehensive tests.

## Your Role

- Write tests for TypeScript functions and React components
- Achieve comprehensive test coverage including edge cases
- Run tests and analyze results
- Write to `/tests/` directory only

## Project Knowledge

- **Test Framework:** Jest 29 with React Testing Library 14
- **Coverage Requirements:** 80% minimum for new code
- **File Structure:**
  - `src/` - Source code (READ ONLY for you)
  - `tests/` - Test files (you WRITE here)

## Commands You Can Use

- Run tests: `npm test`
- Run with coverage: `npm test -- --coverage`
- Run specific test: `npm test -- path/to/test`
- Watch mode: `npm test -- --watch`

## Test Structure Example

```typescript
describe('calculateTotal', () => {
  it('should sum positive numbers correctly', () => {
    expect(calculateTotal([1, 2, 3])).toBe(6);
  });

  it('should handle empty array', () => {
    expect(calculateTotal([])).toBe(0);
  });

  it('should handle negative numbers', () => {
    expect(calculateTotal([-1, -2, -3])).toBe(-6);
  });

  it('should throw for invalid input', () => {
    expect(() => calculateTotal(null)).toThrow();
  });
});
```

## Boundaries

- ✅ **Always do:** Write comprehensive test coverage, test edge cases, follow naming conventions
- ⚠️ **Ask first:** Before changing test framework configuration
- 🚫 **Never do:** Modify source code, remove failing tests, commit test fixtures with secrets
```

#### Linting/Formatting Agent

Purpose: Fixes code style without changing logic

```markdown
---
name: lint-agent
description: Formats code and fixes style issues without changing logic
tools: ['read', 'write', 'terminal']
---

You are a code quality specialist focused on maintaining consistent style.

## Your Role

- Fix code formatting and style issues
- Enforce naming conventions
- Organize imports
- Never change code logic

## Commands You Can Use

- Lint check: `npm run lint`
- Auto-fix: `npm run lint --fix`
- Format: `prettier --write "src/**/*.{ts,tsx}"`
- Check format: `prettier --check "src/**/*.{ts,tsx}"`

## Style Standards

**Naming Conventions:**
- Functions: camelCase (`getUserData`, `calculateTotal`)
- Classes: PascalCase (`UserService`, `DataController`)
- Constants: UPPER_SNAKE_CASE (`API_KEY`, `MAX_RETRIES`)
- Private methods: prefix with underscore (`_internalMethod`)

**Import Organization:**
1. External dependencies
2. Internal absolute imports
3. Relative imports
4. Type imports (separate block)

## Boundaries

- ✅ **Always do:** Fix formatting, organize imports, enforce naming
- ⚠️ **Ask first:** Before changing linting rules or adding new rules
- 🚫 **Never do:** Change code logic, modify functionality, edit config files without permission
```

#### Planning Agent

Purpose: Generates implementation plans without making code edits

```markdown
---
name: planner
description: Generate an implementation plan for new features or refactoring existing code
tools: ['fetch', 'githubRepo', 'search', 'usages']
model: Claude Sonnet 4
handoffs:
  - label: Implement Plan
    agent: agent
    prompt: Implement the plan outlined above
    send: false
---

# Planning Instructions

You are in planning mode. Your task is to generate an implementation plan for a new feature or for refactoring existing code. Don't make any code edits, just generate a plan.

## Plan Structure

The plan consists of a Markdown document that describes the implementation plan, including:

1. **Overview:** Brief description of the feature or refactoring task
2. **Analysis:** Current state assessment and key considerations
3. **Proposed Changes:** Detailed breakdown of modifications needed
4. **File Changes:** List of files to create, modify, or delete
5. **Testing Strategy:** How to verify the changes work
6. **Risks and Considerations:** Potential issues to watch for
7. **Implementation Steps:** Ordered sequence of changes

## Analysis Tools

- Use `search` to find relevant code patterns
- Use `usages` to understand dependencies
- Use `githubRepo` to research similar implementations
- Use `fetch` to retrieve external documentation

## Boundaries

- ✅ **Always do:** Generate comprehensive plans, research thoroughly, consider edge cases
- ⚠️ **Ask first:** Before recommending architectural changes
- 🚫 **Never do:** Make any code edits, modify files, run commands that change state
```

#### API Development Agent

Purpose: Builds API endpoints and handles routes

```markdown
---
name: api-agent
description: Creates REST endpoints, GraphQL resolvers, and error handlers
tools: ['read', 'write', 'terminal']
---

You are a backend API specialist.

## Your Role

- Build RESTful API endpoints
- Implement proper error handling
- Write API documentation
- Follow RESTful conventions

## Project Knowledge

- **Framework:** Express 4.18 with TypeScript
- **Validation:** Zod for request validation
- **Auth:** JWT-based authentication
- **File Structure:**
  - `src/routes/` - Route definitions (you WRITE here)
  - `src/controllers/` - Business logic (you WRITE here)
  - `src/middleware/` - Middleware functions (you WRITE here)
  - `src/models/` - Database models (READ ONLY)

## Commands You Can Use

- Start dev server: `npm run dev`
- Run API tests: `npm test -- tests/api/`
- Test endpoint: `curl -X GET http://localhost:3000/api/users`
- Check types: `tsc --noEmit`

## API Patterns

**Endpoint Structure:**
```typescript
router.get('/users/:id', authenticate, validateParams(userIdSchema), async (req, res, next) => {
  try {
    const user = await userController.getById(req.params.id);
    res.json({ data: user });
  } catch (error) {
    next(error);
  }
});
```

**Error Handling:**
```typescript
class ApiError extends Error {
  constructor(
    public statusCode: number,
    public message: string,
    public isOperational = true
  ) {
    super(message);
  }
}
```

## Boundaries

- ✅ **Always do:** Implement proper error handling, validate inputs, write tests
- ⚠️ **Ask first:** Before modifying database schemas, changing auth logic
- 🚫 **Never do:** Expose sensitive data, bypass authentication, modify production configs
```

### Using Handoffs for Workflows

Handoffs create guided workflows that transition between agents. After a chat response completes, handoff buttons appear that let users move to the next agent with relevant context:

```markdown
---
name: planner
handoffs:
  - label: Start Implementation
    agent: agent
    prompt: Implement the plan outlined above
    send: false
  - label: Review Architecture
    agent: architect
    prompt: Review this plan for architectural concerns
    send: false
---
```

**Handoff Properties:**
- `label`: Button text shown to user
- `agent`: Target agent name to transition to
- `prompt`: Pre-filled prompt for next agent
- `send`: If true, automatically sends prompt; if false, user can review first

### Tool Selection Strategy

Different tasks require different capabilities. Specify tools based on the agent's role:

**Read-only agents** (planning, research, documentation):
```yaml
tools: ['read', 'search', 'fetch', 'githubRepo', 'usages']
```

**Development agents** (implementation, refactoring):
```yaml
tools: ['read', 'write', 'search', 'terminal', 'usages']
```

**Testing agents**:
```yaml
tools: ['read', 'write', 'terminal']
```

**Omit tools property** to enable all available tools (use for general-purpose agents).

### Generating Agents with Copilot

You can use Copilot to generate agent files. Open a new file at `.github/agents/[agent-name].agent.md` and use this prompt pattern:

```
Create a [role] agent for this repository. It should:
- Have the persona of a [specific role description]
- [Primary task description]
- [Tool/command requirements]
- Write to "[target directory]" only
- Never [specific restrictions]
- Include specific examples of [expected output format]
```

Example:
```
Create a test agent for this repository. It should:
- Have the persona of a QA software engineer
- Write tests for this codebase
- Run tests and analyze results
- Write to "/tests/" directory only
- Never modify source code or remove failing tests
- Include specific examples of good test structure
```

Review the generated agent, add YAML frontmatter, adjust commands for your project, and test with sample prompts.

## Custom Instructions

### What Are Custom Instructions?

Custom instructions define common guidelines or rules in Markdown files for tasks like generating code, performing code reviews, or generating commit messages. Unlike custom agents that are invoked explicitly, custom instructions apply automatically to relevant chat requests or can be manually attached.

### Instruction File Types and Locations

**Global instructions** (apply to all requests):
```
.github/copilot-instructions.md
```

**File-specific instructions** (apply to specific file types):
```
.github/instructions/python.instructions.md
src/components/react.instructions.md
```

**User profile instructions** (personal, not shared):
- Stored in VS Code user profile
- Available across all workspaces

### Instruction File Format

Instructions files use Markdown with optional YAML frontmatter:

```markdown
---
applyTo: "**/*.ts"
---

# TypeScript Coding Standards

## Type Definitions

- Always define explicit return types for functions
- Use interfaces for object shapes
- Use type aliases for unions and utility types

## Error Handling

- Use custom error classes that extend Error
- Include error codes and context
- Never swallow errors silently

## Example

```typescript
interface UserRepository {
  findById(id: string): Promise<User | null>;
  save(user: User): Promise<void>;
}

class UserNotFoundError extends Error {
  constructor(userId: string) {
    super(`User not found: ${userId}`);
    this.name = 'UserNotFoundError';
  }
}
```
```

### The applyTo Property

Use `applyTo` with glob patterns to target specific files:

```yaml
# Apply to all TypeScript files
applyTo: "**/*.ts"

# Apply to all files in src directory
applyTo: "src/**/*"

# Apply to React components only
applyTo: "**/*.tsx"

# Apply to test files
applyTo: "**/*.test.{ts,tsx}"

# Apply to all Python files
applyTo: "**/*.py"

# Apply to specific directory
applyTo: "src/components/**/*"
```

Without `applyTo`, instructions apply to all file types.

### Best Practices for Custom Instructions

#### 1. Keep Instructions Short and Self-Contained

Each instruction should be a single, simple statement:

**Good:**
```markdown
- Use async/await instead of Promise chains
- Prefix private methods with underscore
- Always include JSDoc comments for public functions
```

**Too Complex:**
```markdown
- When working with asynchronous code, you should prefer the async/await syntax over Promise chains because it's more readable and easier to debug, unless you're dealing with parallel operations where Promise.all is more appropriate, in which case you should use that instead...
```

#### 2. Provide Concrete Examples

Show what good code looks like:

```markdown
## Error Handling

**Good:**
```typescript
async function fetchUser(id: string): Promise<User> {
  try {
    const response = await fetch(`/api/users/${id}`);
    if (!response.ok) throw new ApiError(response.status, 'Failed to fetch user');
    return response.json();
  } catch (error) {
    logger.error('User fetch failed', { id, error });
    throw error;
  }
}
```

**Bad:**
```typescript
async function fetchUser(id) {
  const response = await fetch('/api/users/' + id);
  return response.json();
}
```
```

#### 3. Organize by Category

Structure instructions logically:

```markdown
# Project Coding Standards

## Naming Conventions
[rules here]

## Type Definitions
[rules here]

## Error Handling
[rules here]

## Testing Requirements
[rules here]

## Documentation
[rules here]
```

#### 4. Reference External Context

Link to relevant files or documentation:

```markdown
## Architecture Patterns

Follow the patterns defined in [architecture.md](../docs/architecture.md).

For database access, use the Repository pattern demonstrated in [UserRepository.ts](../src/repositories/UserRepository.ts).
```

Use `#tool:` syntax to reference agent tools:

```markdown
When implementing new features, search the codebase using #tool:search to find similar patterns.
```

### Common Instruction File Patterns

#### Code Generation Instructions

```markdown
---
applyTo: "**/*.{ts,tsx}"
---

# TypeScript Code Generation Standards

## Component Structure (React)

- Use functional components with hooks
- Define prop types with interfaces
- Include JSDoc comments
- Export component as default

```typescript
interface ButtonProps {
  onClick: () => void;
  label: string;
  variant?: 'primary' | 'secondary';
  disabled?: boolean;
}

/**
 * Reusable button component
 */
export default function Button({ 
  onClick, 
  label, 
  variant = 'primary', 
  disabled = false 
}: ButtonProps) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`btn btn-${variant}`}
    >
      {label}
    </button>
  );
}
```

## API Functions

- Use async/await
- Include proper error handling
- Define response types
- Add rate limiting considerations

```typescript
interface ApiResponse<T> {
  data: T;
  status: number;
  message?: string;
}

async function fetchWithRetry<T>(
  url: string,
  retries = 3
): Promise<ApiResponse<T>> {
  for (let i = 0; i < retries; i++) {
    try {
      const response = await fetch(url);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      return { data, status: response.status };
    } catch (error) {
      if (i === retries - 1) throw error;
      await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
    }
  }
}
```
```

#### Test Generation Instructions

```markdown
---
applyTo: "**/*.test.{ts,tsx}"
---

# Test Generation Standards

## Test Structure

- Use describe blocks for grouping
- Write descriptive test names
- Follow AAA pattern (Arrange, Act, Assert)
- Include edge cases and error scenarios

## Example Test Pattern

```typescript
describe('UserService', () => {
  describe('createUser', () => {
    it('should create a new user with valid data', async () => {
      // Arrange
      const userData = { name: 'John Doe', email: 'john@example.com' };
      const mockRepository = createMockRepository();
      const service = new UserService(mockRepository);

      // Act
      const result = await service.createUser(userData);

      // Assert
      expect(result).toMatchObject(userData);
      expect(mockRepository.save).toHaveBeenCalledWith(expect.objectContaining(userData));
    });

    it('should throw ValidationError for invalid email', async () => {
      // Arrange
      const invalidData = { name: 'John', email: 'invalid-email' };
      const service = new UserService(createMockRepository());

      // Act & Assert
      await expect(service.createUser(invalidData))
        .rejects
        .toThrow(ValidationError);
    });
  });
});
```

## Coverage Requirements

- Aim for 80% coverage minimum
- Test all public methods
- Include error paths
- Test edge cases (null, empty, boundary values)
```

#### Code Review Instructions

```markdown
# Code Review Guidelines

## Security Checks

- No hardcoded secrets or API keys
- Proper input validation
- SQL injection prevention
- XSS prevention in user-facing content
- Proper authentication and authorization

## Performance Considerations

- Avoid N+1 queries
- Use appropriate data structures
- Consider time and space complexity
- Implement caching where appropriate
- Lazy loading for heavy resources

## Code Quality

- Functions should be small and focused
- Avoid deep nesting (max 3 levels)
- Use meaningful variable names
- Remove commented-out code
- Update documentation

## Testing Requirements

- Unit tests for new functions
- Integration tests for API endpoints
- Update tests when changing functionality
- All tests must pass
```

### Manually Attaching Instructions

You can manually attach instructions to specific prompts:

1. In Chat view, select Add Context
2. Choose Instructions
3. Select the instruction file to attach
4. Submit your prompt

This is useful when you want instructions to apply only to a specific request rather than automatically.

### Combining Instructions with Agents and Prompts

Instructions files can be referenced in:

**Custom agents:**
```markdown
---
name: my-agent
---

Follow the coding standards defined in the project instructions.

[Rest of agent definition]
```

**Prompt files:**
```markdown
---
description: Generate a React component
---

Create a new React component following our standards.

[Prompt content]
```

This keeps agents and prompts focused while maintaining a single source of truth for standards.

## Prompt Files

### What Are Prompt Files?

Prompt files are Markdown files that define reusable prompts for common development tasks. They are standalone prompts that you can run directly in chat, enabling the creation of a library of standardized development workflows. Prompt files are triggered on-demand for specific tasks.

### File Structure and Location

**Workspace prompt files** (team-shared):
```
.github/prompts/[prompt-name].prompt.md
```

**User profile prompt files** (personal):
- Stored in VS Code user profile
- Available across all workspaces

### Prompt File Format

Prompt files consist of YAML frontmatter followed by the prompt content:

```markdown
---
description: Brief description of what this prompt does
agent: 'agent'
model: GPT-4o
tools: ['githubRepo', 'search/codebase']
---

Your prompt instructions here...

You can reference variables with ${variableName}.
You can reference tools with #tool:toolName.
You can reference files with [relative path](../path/to/file).
```

### Frontmatter Properties

**Required:**
- `description`: Brief description shown in prompt selector

**Optional:**
- `agent`: Which agent to use ('agent', 'ask', 'edit', or custom agent name)
- `model`: Preferred language model
- `tools`: Array of tools to enable for this prompt

### Variables in Prompt Files

Use `${variableName}` syntax for dynamic inputs:

```markdown
---
description: Generate a form component with specified fields
---

Create a new form component with the following specifications:

Component name: ${input:componentName:Enter component name (e.g., UserForm)}
Form fields: ${input:fields:List the fields (e.g., name, email, phone)}
Validation: ${input:validation:Should include validation? (yes/no)}

Generate the component in TypeScript with React Hook Form.
```

When run, VS Code prompts for each variable value.

### Referencing Context

**Reference files:**
```markdown
Follow the pattern used in [UserForm.tsx](../src/components/UserForm.tsx).
```

**Reference tools:**
```markdown
Search for similar implementations using #tool:search.
Check the GitHub repository for examples: #tool:githubRepo owner/repo.
```

**Reference workspace context:**
```markdown
Apply these changes to #file:src/components/Button.tsx.
Review the entire codebase: #codebase.
```

### Common Prompt File Patterns

#### Component Generation Prompt

```markdown
---
description: Generate a new React form component
agent: 'agent'
model: GPT-4o
tools: ['githubRepo', 'search/codebase']
---

# Generate React Form Component

Your goal is to generate a new React form component based on the templates in #tool:githubRepo contoso/react-templates.

## Component Details

Component name: ${input:componentName:Enter the component name}
Form fields: ${input:fields:List fields separated by commas}

## Requirements

1. Use TypeScript with strict typing
2. Implement form validation with Zod
3. Use React Hook Form for state management
4. Include proper error handling
5. Add loading states for async operations
6. Follow the pattern in [BaseForm.tsx](../src/components/BaseForm.tsx)

## Output

- Create component file in `src/components/forms/`
- Create test file in `tests/components/forms/`
- Update component index exports
```

#### Code Review Prompt

```markdown
---
description: Perform comprehensive code review
agent: 'ask'
tools: ['search', 'usages']
---

# Code Review Checklist

Review the following aspects of the code changes:

## Security
- Check for hardcoded secrets or sensitive data
- Verify input validation and sanitization
- Review authentication and authorization logic
- Check for SQL injection vulnerabilities
- Verify XSS prevention measures

## Performance
- Identify potential N+1 query problems
- Check for inefficient algorithms or data structures
- Review database query optimization
- Identify opportunities for caching
- Check for unnecessary re-renders (React)

## Code Quality
- Verify functions are small and focused
- Check for proper error handling
- Review naming conventions
- Verify test coverage
- Check for code duplication

## Best Practices
- Verify adherence to project coding standards
- Check documentation completeness
- Review commit message quality
- Verify proper logging

Target files: ${input:files:Enter file paths or patterns to review}
```

#### Test Generation Prompt

```markdown
---
description: Generate comprehensive test suite
agent: 'agent'
tools: ['read', 'search']
---

# Generate Test Suite

Generate a comprehensive test suite for the specified component or function.

Target file: ${input:targetFile:Enter path to file to test}
Test type: ${input:testType:Unit, Integration, or E2E}

## Test Requirements

1. **Coverage:** Achieve at least 80% code coverage
2. **Test Cases:** Include:
   - Happy path scenarios
   - Edge cases (null, empty, boundary values)
   - Error conditions and exceptions
   - Integration points with dependencies

3. **Test Structure:**
   ```typescript
   describe('Component/Function Name', () => {
     describe('method/function name', () => {
       it('should [expected behavior]', () => {
         // Arrange
         // Act
         // Assert
       });
     });
   });
   ```

4. **Mocking:** Mock external dependencies appropriately
5. **Assertions:** Use specific, descriptive assertions
6. **Documentation:** Add comments for complex test logic

Reference existing test patterns in #tool:search to maintain consistency.
```

#### Documentation Generation Prompt

```markdown
---
description: Generate API documentation from code
agent: 'ask'
tools: ['read', 'search']
---

# Generate API Documentation

Generate comprehensive API documentation for the specified module.

Module path: ${input:modulePath:Enter module path (e.g., src/api/users.ts)}

## Documentation Requirements

1. **Overview:** Brief description of module purpose
2. **Endpoints/Functions:** Document each with:
   - Purpose and use cases
   - Parameters with types and descriptions
   - Return types and values
   - Error conditions and codes
   - Example usage

3. **Format:**
   ```markdown
   ## Function Name
   
   Description of what the function does.
   
   ### Parameters
   - `param1` (type): Description
   - `param2` (type): Description
   
   ### Returns
   `ReturnType`: Description of return value
   
   ### Throws
   - `ErrorType`: When this error occurs
   
   ### Example
   ```typescript
   const result = await functionName(arg1, arg2);
   ```
   ```

4. **Cross-references:** Link to related functions/modules
5. **Authentication:** Document any auth requirements

Search for similar documentation patterns: #tool:search documentation
```

#### Migration/Refactoring Prompt

```markdown
---
description: Generate migration plan for framework upgrade
agent: 'agent'
model: Claude Sonnet 4
tools: ['search', 'usages', 'githubRepo']
---

# Framework Migration Plan

Create a detailed migration plan for upgrading the framework.

Current version: ${input:currentVersion:Current framework version}
Target version: ${input:targetVersion:Target framework version}
Framework: ${input:framework:Framework name (e.g., React, Express)}

## Analysis Steps

1. **Inventory:** Identify all files using the framework
2. **Breaking Changes:** Research breaking changes between versions
3. **Dependencies:** Check compatibility of dependencies
4. **Testing Impact:** Assess test suite modifications needed

## Migration Plan Structure

1. **Overview:** Summary of changes required
2. **Breaking Changes:** List each with impact assessment
3. **Migration Steps:** Ordered sequence of changes
4. **File Changes:** Specific files requiring modification
5. **Testing Strategy:** How to verify migration success
6. **Rollback Plan:** Steps if migration fails
7. **Timeline Estimate:** Rough effort estimate

Research similar migrations: #tool:githubRepo to find example upgrades.
Check framework usage across codebase: #tool:usages.
```

### Running Prompt Files

**From Chat view:**
1. Type `/` to see available prompts
2. Select the prompt from the list
3. Fill in any required variables
4. Review and submit

**From Command Palette:**
1. Run `Chat: New Prompt File` command
2. Select existing prompt or create new one

### Best Practices for Prompt Files

#### 1. Make Prompts Self-Contained

Include all necessary context and instructions:

```markdown
---
description: Create REST API endpoint with tests
---

Create a new REST API endpoint with the following specifications:

Endpoint: ${input:endpoint:Enter endpoint path (e.g., /api/users)}
Method: ${input:method:HTTP method (GET, POST, PUT, DELETE)}
Description: ${input:description:Brief description of endpoint purpose}

## Requirements

1. Follow the repository pattern used in #file:src/repositories/UserRepository.ts
2. Implement proper error handling with ApiError class
3. Add input validation using Zod schemas
4. Include unit tests with 80% coverage
5. Add integration tests for the endpoint
6. Update API documentation in docs/api/
7. Follow coding standards in #file:.github/copilot-instructions.md

## File Structure

- Controller: `src/controllers/[resource]Controller.ts`
- Route: `src/routes/[resource]Routes.ts`
- Validation: `src/validation/[resource]Schema.ts`
- Tests: `tests/api/[resource].test.ts`
```

#### 2. Specify Expected Output

Be clear about what files should be created or modified:

```markdown
## Expected Output

1. Create component file: `src/components/${componentName}.tsx`
2. Create test file: `tests/components/${componentName}.test.tsx`
3. Create story file: `src/components/${componentName}.stories.tsx`
4. Update exports: Add to `src/components/index.ts`
5. Update documentation: Add to `docs/components.md`
```

#### 3. Include Success Criteria

Define how to verify the prompt succeeded:

```markdown
## Validation Steps

After generation:
1. Run `npm test` - all tests should pass
2. Run `npm run type-check` - no TypeScript errors
3. Run `npm run lint` - no linting errors
4. Verify component renders in Storybook
5. Check that examples in documentation work
```

#### 4. Reference Similar Examples

Help AI understand context by referencing existing code:

```markdown
Follow the patterns used in these examples:
- Component structure: #file:src/components/UserForm.tsx
- Test patterns: #file:tests/components/Button.test.tsx
- Documentation style: #file:docs/components/button.md

Search for similar components: #tool:search form component
```

#### 5. Break Down Complex Tasks

For complex prompts, provide step-by-step instructions:

```markdown
## Implementation Steps

Step 1: Create data model
- Define TypeScript interface
- Create Zod validation schema
- Add to type exports

Step 2: Implement repository
- Create repository class
- Implement CRUD methods
- Add error handling

Step 3: Create controller
- Implement business logic
- Add input validation
- Handle errors appropriately

Step 4: Add routes
- Define route handlers
- Apply middleware
- Connect to controller

Step 5: Write tests
- Unit tests for repository
- Unit tests for controller
- Integration tests for routes
```

### Combining Instructions with Prompt Files

Reference instructions files in prompts to maintain consistency:

```markdown
---
description: Generate TypeScript service class
---

Create a new service class following our standards.

Class name: ${input:className:Enter class name}
Purpose: ${input:purpose:Describe the service purpose}

Follow the coding standards in #file:.github/copilot-instructions.md.
Use the patterns demonstrated in #file:src/services/UserService.ts.
```

## Language Model Selection

### Available Models

GitHub Copilot in VS Code provides access to multiple language models, each optimized for different tasks:

**Fast Models (for quick interactions):**
- GPT-4o mini: Optimized for speed and inline suggestions
- Claude Haiku: Fast responses for simple queries

**Balanced Models (general purpose):**
- GPT-4o: Good balance of performance and quality
- Claude Sonnet 4: Efficient for everyday use

**Reasoning Models (for complex tasks):**
- GPT-5: Advanced reasoning capabilities
- Claude Opus 4.1: Deep analysis and complex problem solving

**Auto Selection:**
- Automatically chooses optimal model based on task
- Reduces rate limits from excessive usage
- Adapts to degraded performance

### When to Use Each Model

**Use fast models for:**
- Inline code completions
- Quick refactoring
- Simple explanations
- Formatting and linting
- Repetitive tasks

**Use balanced models for:**
- General coding tasks
- Chat conversations
- Code reviews
- Documentation writing
- Moderate complexity tasks

**Use reasoning models for:**
- Complex architectural decisions
- Debugging difficult issues
- Planning large refactors
- Analyzing security concerns
- Multi-file coordination

### Specifying Models in Agents and Prompts

**In custom agents:**
```yaml
---
name: architect
model: Claude Sonnet 4
---
```

**In prompt files:**
```yaml
---
description: Complex refactoring task
model: GPT-5
---
```

**From chat UI:**
- Use model picker dropdown to select
- Selection applies to current session
- Different agents may restrict available models

### Model Selection Strategy

Consider these factors when choosing models:

**Task Complexity:**
- Simple, well-defined: Fast models
- Moderate complexity: Balanced models
- Complex, ambiguous: Reasoning models

**Speed Requirements:**
- Need immediate feedback: Fast models
- Can wait for quality: Reasoning models
- Balance needed: Balanced models

**Token Budget:**
- Frequent, small tasks: Fast models (lower cost)
- Occasional, complex tasks: Reasoning models
- Mixed usage: Auto selection

**Tool Calling Requirements:**
- Agent mode needs models with good tool support
- Check agent mode model availability
- Some models better at tool orchestration

### Model-Specific Considerations

**For planning agents:**
```yaml
model: Claude Sonnet 4  # Strong reasoning for architecture
```

**For implementation agents:**
```yaml
model: GPT-4o  # Good balance for coding
```

**For quick fixes:**
```yaml
model: GPT-4o mini  # Fast responses
```

**For code review:**
```yaml
model: Claude Opus 4.1  # Deep analysis
```

### Bringing Your Own Models

VS Code supports custom language model providers:

**Benefits:**
- Access hundreds of models beyond built-in options
- Experiment with new models
- Run local models
- Bypass standard rate limits
- Greater control over usage

**Setup:**
1. Install AI Toolkit extension or model provider extension
2. Configure provider via Chat: Manage Language Models
3. Enter API key for provider
4. Select models to enable

**Common providers:**
- OpenAI (direct API)
- Anthropic (direct API)
- Azure OpenAI
- Local models via AI Toolkit

## Comprehensive Example: Full Project Setup

Here's a complete example showing how to set up agents, instructions, and prompts for a TypeScript/React project:

### Project Structure

```
project-root/
├── .github/
│   ├── agents/
│   │   ├── docs-agent.agent.md
│   │   ├── test-agent.agent.md
│   │   ├── api-agent.agent.md
│   │   ├── planner.agent.md
│   │   └── reviewer.agent.md
│   ├── instructions/
│   │   ├── typescript.instructions.md
│   │   ├── react.instructions.md
│   │   └── testing.instructions.md
│   ├── prompts/
│   │   ├── component.prompt.md
│   │   ├── api-endpoint.prompt.md
│   │   ├── test-suite.prompt.md
│   │   └── code-review.prompt.md
│   └── copilot-instructions.md
├── src/
├── tests/
└── docs/
```

### Global Instructions (copilot-instructions.md)

```markdown
# Project Coding Standards

This project is a TypeScript/React application with Express backend.

## Tech Stack

- Frontend: React 18.2, TypeScript 5.0, Vite 4.3, Tailwind CSS 3.3
- Backend: Node.js 20 LTS, Express 4.18, Prisma 5.0
- Testing: Jest 29, React Testing Library 14, Playwright 1.40
- Build: Vite for frontend, TSC for backend

## Core Principles

- Type safety: Use TypeScript strictly, no any types
- Testability: Write testable code with dependency injection
- Simplicity: Prefer simple solutions over clever ones
- Consistency: Follow established patterns in the codebase

## Naming Conventions

- Files: kebab-case (user-profile.tsx)
- Components: PascalCase (UserProfile)
- Functions/variables: camelCase (getUserData)
- Constants: UPPER_SNAKE_CASE (API_BASE_URL)
- Interfaces: PascalCase with descriptive names (UserRepository)
- Types: PascalCase ending with Type (ConfigType)

## Project Structure

- `src/components/` - React components
- `src/hooks/` - Custom React hooks
- `src/api/` - API client code
- `src/services/` - Business logic
- `src/types/` - TypeScript type definitions
- `src/utils/` - Utility functions
- `tests/` - All test files mirror src structure
- `docs/` - Project documentation

## Required Practices

- All public functions must have JSDoc comments
- All components must have prop type definitions
- All API calls must have error handling
- All user input must be validated
- All async operations must handle loading states
```

### TypeScript Instructions

```markdown
---
applyTo: "**/*.ts"
---

# TypeScript Standards

## Type Definitions

```typescript
// Good: Explicit types
interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'user';
}

async function fetchUser(id: string): Promise<User> {
  // implementation
}

// Bad: Implicit or any types
async function fetchUser(id) {
  // implementation
}
```

## Error Handling

```typescript
// Good: Typed errors with context
class ApiError extends Error {
  constructor(
    public statusCode: number,
    message: string,
    public context?: Record<string, unknown>
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

// Usage
throw new ApiError(404, 'User not found', { userId: id });
```

## Null Safety

```typescript
// Good: Handle null explicitly
function getUserName(user: User | null): string {
  return user?.name ?? 'Anonymous';
}

// Bad: Assume non-null
function getUserName(user: User): string {
  return user.name;
}
```
```

### React Instructions

```markdown
---
applyTo: "**/*.tsx"
---

# React Component Standards

## Component Structure

```typescript
interface ComponentProps {
  // Props interface first
}

/**
 * Component description
 */
export default function Component({ ...props }: ComponentProps) {
  // 1. Hooks
  // 2. Derived state
  // 3. Event handlers
  // 4. Effects
  // 5. Render
}
```

## Hooks Best Practices

```typescript
// Good: Custom hooks for complex logic
function useUserData(userId: string) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    fetchUser(userId)
      .then(setUser)
      .catch(setError)
      .finally(() => setLoading(false));
  }, [userId]);

  return { user, loading, error };
}

// Usage in component
function UserProfile({ userId }: { userId: string }) {
  const { user, loading, error } = useUserData(userId);
  
  if (loading) return <Loading />;
  if (error) return <Error message={error.message} />;
  if (!user) return <NotFound />;
  
  return <div>{user.name}</div>;
}
```

## Props Patterns

```typescript
// Good: Discriminated unions for variants
type ButtonProps = 
  | { variant: 'primary'; onClick: () => void }
  | { variant: 'link'; href: string };

// Good: Optional props with defaults
interface CardProps {
  title: string;
  description?: string;
  variant?: 'default' | 'outlined';
}

export default function Card({ 
  title, 
  description, 
  variant = 'default' 
}: CardProps) {
  // implementation
}
```
```

### Workflow Example

**Step 1: Planning a new feature**

User runs planner agent:
```
@planner Create a user authentication system with JWT tokens
```

Planner generates implementation plan with architecture decisions.

**Step 2: Implement API routes**

User uses api-agent:
```
@api-agent Implement the auth endpoints from the plan
```

API agent creates:
- `/src/routes/authRoutes.ts`
- `/src/controllers/authController.ts`
- `/src/middleware/authenticate.ts`

**Step 3: Generate tests**

User uses test-agent:
```
@test-agent Create comprehensive tests for the auth system
```

Test agent creates:
- `/tests/api/auth.test.ts`
- `/tests/middleware/authenticate.test.ts`

**Step 4: Code review**

User uses reviewer agent:
```
@reviewer Review the auth implementation for security issues
```

Reviewer checks for common security problems.

**Step 5: Documentation**

User uses docs-agent:
```
@docs-agent Document the authentication system
```

Docs agent creates API documentation.

## Advanced Patterns and Techniques

### Iterative Agent Development

Start simple and refine based on actual usage:

**Version 1: Basic agent**
```markdown
---
name: api-agent
description: Creates API endpoints
---

You are a backend developer. Create API endpoints in Express.
```

**Version 2: Add commands and structure**
```markdown
---
name: api-agent
description: Creates API endpoints
---

You are a backend developer.

## Commands
- Start server: `npm run dev`
- Run tests: `npm test`

## File Structure
- Routes: `src/routes/`
- Controllers: `src/controllers/`
```

**Version 3: Add examples and boundaries**
```markdown
---
name: api-agent
description: Creates API endpoints
tools: ['read', 'write', 'terminal']
---

You are a backend developer.

## Commands
- Start server: `npm run dev`
- Run tests: `npm test`

## Code Example
[Include actual code example]

## Boundaries
- ✅ Always: Add tests, validate input
- ⚠️ Ask first: Schema changes
- 🚫 Never: Commit secrets
```

### Context Management

**Minimize context size for performance:**

```markdown
---
name: focused-agent
tools: ['read', 'write']  # Only essential tools
---

You work only with files in `src/components/`.

Don't search the entire codebase. Focus on:
- `src/components/` for implementations
- `tests/components/` for tests
```

**Provide focused examples:**

Instead of including 10 examples, include 2-3 most relevant ones.

### Agent Specialization Strategies

**By domain:**
- frontend-agent: Only touches UI code
- backend-agent: Only touches server code
- database-agent: Only touches schema and migrations

**By task type:**
- builder-agent: Creates new code
- refactor-agent: Improves existing code
- fix-agent: Debugs and fixes issues

**By expertise level:**
- junior-agent: Guided with extensive examples
- senior-agent: Minimal guidance, more autonomy
- expert-agent: Handles complex architectural decisions

### Error Handling in Instructions

Define how to handle common error scenarios:

```markdown
## Error Handling Patterns

### API Errors
```typescript
try {
  const response = await apiCall();
  return response.data;
} catch (error) {
  if (error instanceof ApiError) {
    logger.error('API call failed', { error, context });
    throw error;
  }
  throw new UnexpectedError('API call failed', { originalError: error });
}
```

### User Input Validation
```typescript
const schema = z.object({
  email: z.string().email(),
  age: z.number().min(0).max(120),
});

try {
  const validated = schema.parse(input);
  return validated;
} catch (error) {
  if (error instanceof z.ZodError) {
    throw new ValidationError('Invalid input', { errors: error.errors });
  }
  throw error;
}
```
```

### Testing Strategy in Instructions

Define what types of tests to write:

```markdown
## Testing Requirements

### Unit Tests (80% coverage minimum)
- Test each function in isolation
- Mock external dependencies
- Test edge cases and error conditions

### Integration Tests
- Test API endpoints end-to-end
- Test database interactions
- Test external service integrations

### E2E Tests (Critical paths only)
- User authentication flow
- Primary user workflows
- Payment processing

### Test Organization
```
tests/
├── unit/
│   ├── services/
│   └── utils/
├── integration/
│   ├── api/
│   └── database/
└── e2e/
    └── flows/
```
```

## Common Pitfalls and Solutions

### Pitfall 1: Vague Agent Personas

**Problem:**
```markdown
You are a helpful assistant for coding.
```

**Solution:**
```markdown
You are a senior backend engineer specializing in Node.js microservices. You write production-grade code with comprehensive error handling, logging, and monitoring. You follow SOLID principles and ensure high test coverage.
```

### Pitfall 2: Missing Boundaries

**Problem:**
Agent modifies production config files or removes tests.

**Solution:**
```markdown
## Boundaries

- 🚫 **Never do:** 
  - Modify `.env`, `.env.production`, or any config files
  - Remove or skip failing tests
  - Commit code without running tests
  - Change database schema without migration
```

### Pitfall 3: Unclear Success Criteria

**Problem:**
No way to verify the agent did what was requested.

**Solution:**
```markdown
## Verification Steps

After completing the task:
1. Run `npm test` - all tests must pass
2. Run `npm run type-check` - no TypeScript errors
3. Run `npm run lint` - no linting violations
4. Manual test: [specific test steps]
5. Verify changes in: [specific files to check]
```

### Pitfall 4: Too Many Examples

**Problem:**
Including excessive examples bloats context and confuses the model.

**Solution:**
Include 1-2 clear examples showing the exact pattern to follow:

```markdown
## Code Style

Follow this pattern:

```typescript
// This is the pattern to follow
async function fetchResource(id: string): Promise<Resource> {
  const result = await api.get(`/resources/${id}`);
  return result.data;
}
```

Not this:
```typescript
// Don't do this
async function fetch(x) {
  return await api.get('/resources/' + x).data;
}
```
```

### Pitfall 5: Ignoring Tech Stack Versions

**Problem:**
Agent suggests deprecated patterns or incompatible versions.

**Solution:**
```markdown
## Tech Stack (with versions)

- React: 18.2.0 (use hooks, no class components)
- TypeScript: 5.0.0 (use satisfies operator, no enums)
- Node.js: 20.0.0 LTS (use native fetch, no node-fetch)
- Jest: 29.0.0 (use modern timer APIs)

Do not suggest:
- Class components (deprecated)
- Enums (prefer union types)
- node-fetch (use native fetch)
- Legacy Jest timer APIs
```

## Maintenance and Evolution

### Regular Review Cycle

**Monthly:**
- Review agent usage metrics
- Collect feedback from team
- Update examples with current patterns
- Remove outdated instructions

**Quarterly:**
- Major revision of all agents
- Update tech stack versions
- Add new agents for emerging needs
- Deprecate unused agents

### Version Control Best Practices

Treat agent/instruction files like code:

```
git commit -m "feat(agents): add security review agent

- Focuses on common security vulnerabilities
- Includes OWASP Top 10 checks
- Provides remediation suggestions
- Configured with read-only tools
```

**Use conventional commits:**
- `feat(agents):` - New agent
- `fix(agents):` - Fix agent behavior
- `docs(agents):` - Update agent documentation
- `refactor(agents):` - Restructure agent

### Team Collaboration

**Share knowledge:**
- Document successful patterns
- Share example conversations
- Maintain a tips and tricks document
- Hold regular team reviews

**Centralize common patterns:**
- Create shared instruction library
- Maintain example repository
- Document edge cases and solutions
- Share prompt file templates

### Measuring Effectiveness

**Track metrics:**
- Agent usage frequency
- Success rate (tasks completed correctly)
- Time saved vs. manual approach
- Quality of generated code
- Test pass rate

**Collect qualitative feedback:**
- What works well?
- What needs improvement?
- What new agents would be helpful?
- What instructions are unclear?

## Summary of Key Principles

1. **Specificity Over Generality:** Define narrow, focused roles rather than general assistants
2. **Show, Don't Tell:** Provide concrete code examples rather than abstract descriptions
3. **Clear Boundaries:** Use the three-tier system (always/ask/never) to prevent mistakes
4. **Commands First:** Put executable commands prominently with flags and descriptions
5. **Tech Stack Precision:** Specify exact versions and key dependencies
6. **Iterative Refinement:** Start simple and add detail based on actual usage
7. **Context Management:** Keep instructions focused and examples concise
8. **Team Alignment:** Share and version control agents, instructions, and prompts
9. **Measurable Success:** Define clear verification steps for every task
10. **Continuous Improvement:** Regularly review and update based on feedback

By following these best practices, you can build a suite of specialized AI assistants that understand your codebase, follow your standards, and significantly accelerate development workflows while maintaining code quality and consistency.
