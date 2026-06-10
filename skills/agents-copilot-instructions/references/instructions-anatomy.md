# Instructions File Anatomy

Templates and structural patterns for both path-specific and repository-wide instructions.

## Path-Specific Instructions Anatomy

### Required: YAML Frontmatter

Every path-specific file starts with frontmatter:

```yaml
---
applyTo: "<glob-pattern>"
---
```

Optional `excludeAgent` to limit which Copilot feature reads the file:

```yaml
---
applyTo: "**/*.py"
excludeAgent: "code-review"
---
```

### Recommended Sections

Not all sections are required. Include only what adds value for the domain.

#### 1. Title and Scope
```markdown
# TypeScript Coding Standards
```
Clear title indicating the domain. No scope paragraph needed — the `applyTo` frontmatter defines scope.

#### 2. Naming Conventions
```markdown
## Naming Conventions
- Use `camelCase` for variables and functions
- Use `PascalCase` for class and interface names
- Prefix private variables with `_`
- Suffix test files with `.test.ts`
```

#### 3. Code Style
```markdown
## Code Style
- Prefer `const` over `let` when variables are not reassigned
- Use arrow functions for anonymous callbacks
- Avoid using `any` type; specify precise types
- Limit line length to 100 characters
```

#### 4. Error Handling
```markdown
## Error Handling
- Always handle promise rejections with `try/catch` or `.catch()`
- Use custom error classes for application-specific errors
- Log errors with structured context (userId, requestId, operation)
```

#### 5. Testing
```markdown
## Testing
- Write unit tests for all exported functions
- Use Jest for all testing
- Name test files as `<filename>.test.ts`
- Prefer `describe`/`it` blocks over standalone `test()` calls
```

#### 6. Security
```markdown
## Security
- Never log sensitive data (tokens, passwords, PII)
- Validate all user input at API boundaries
- Use parameterized queries for database access
```

#### 7. Framework-Specific Rules
```markdown
## React Patterns
- Use functional components with hooks exclusively
- Prefer `useMemo`/`useCallback` for expensive computations
- Colocate component styles in the same directory
```

#### 8. Code Examples
```markdown
## Examples

```typescript
// Correct: typed function with error handling
const fetchUser = async (id: string): Promise<User> => {
  try {
    const response = await api.get(`/users/${id}`);
    return response.data;
  } catch (error) {
    throw new AppError('Failed to fetch user', { cause: error });
  }
};

// Incorrect: untyped, no error handling
async function fetchUser(id) {
  const response = await api.get(`/users/${id}`);
  return response.data;
}
```
```

---

## Repository-Wide Instructions Anatomy

### Structure Template

```markdown
# Project Name

Brief elevator pitch: what the app does, who it's for, key features.

## Tech Stack

### Backend
- Flask for the API
- PostgreSQL with SQLAlchemy ORM
  - Separate databases for dev, staging, prod

### Frontend
- Next.js with App Router
- TypeScript for all frontend code
- Tailwind CSS for styling

### Testing
- pytest for Python backend
- Vitest for TypeScript
- Playwright for e2e tests

## Coding Guidelines
- Always use type hints in Python and TypeScript
- Unit tests are required for all new functions
- Follow RESTful API design principles
- Use conventional commits for commit messages

## Project Structure
- `backend/` : Flask API code
  - `models/` : SQLAlchemy ORM models
  - `routes/` : API endpoints by resource
  - `tests/` : Unit tests
- `frontend/` : Next.js application
  - `src/components/` : Reusable components
  - `src/app/` : App Router pages and layouts
- `scripts/` : Dev and deployment scripts
- `docs/` : Project documentation

## Resources
- `scripts/start-app.sh` : Installs dependencies and starts the app
- `scripts/test-all.sh` : Runs full test suite
- `docker-compose.yml` : Local development environment
```

### What Makes Great Repository Instructions

1. **Elevator pitch** — 2-3 sentences on what the app does and who uses it
2. **Tech stack with usage notes** — not just "React" but "React with Zustand for state management"
3. **Non-obvious conventions** — things a new developer would get wrong
4. **Project structure with purpose** — what's in each directory
5. **Available automation** — scripts, MCP servers, CI tools

### What to Avoid

- Don't duplicate README.md content verbatim
- Don't include setup instructions (that's README's job)
- Don't list every file — focus on directories and their purposes
- Don't include history or changelog information
- Don't exceed 2 pages of content
