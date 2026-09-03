# Writing Principles for Copilot Instructions

Distilled from GitHub's official guidance and real-world effectiveness patterns.

## The Five Pillars

### 1. Be Concise
- Copilot works best with focused, short instructions
- Even a single line can guide behavior
- Files over ~1,000 lines lead to inconsistent behavior
- Challenge each line: "Does this rule earn its place?"

### 2. Be Direct
- Use imperative mood: "Use", "Prefer", "Never", "Always"
- Short rules > long paragraphs
- One concept per bullet point
- Eliminate filler words and qualifications

### 3. Be Specific
- Name exact patterns: "`camelCase` for variables, `PascalCase` for types"
- Name exact tools: "Use Jest for testing" not "use a testing framework"
- Name exact files: "`src/models/` contains database models"
- Provide concrete values: "Limit lines to 100 characters" not "keep lines short"

### 4. Show with Examples
- Code blocks demonstrate patterns faster than prose
- Always label correct vs. incorrect
- Keep examples minimal — show just the pattern, not a full implementation
- Use the same language/framework the instructions target

### 5. Structure for Scanning
- Use Markdown headings to create scannable sections
- Use bullet points or numbered lists
- Group related rules together
- Put the most important rules first within each section

## What NOT to Include

- **Vague directives:** "Be more accurate", "Write clean code", "Follow best practices"
- **External links:** Copilot cannot follow URLs; inline the content
- **Meta-commentary:** Don't explain what instructions files are or how they work
- **Linter-enforced rules:** If ESLint/Prettier/Ruff already enforce it, skip it
- **Language defaults:** Don't state conventions that are universal to the language
- **UX/formatting requests:** Copilot cannot change its comment formatting
- **Product behavior changes:** Don't try to make Copilot block PRs or modify workflows

## High-Value Content Patterns

These types of rules deliver the most impact:

1. **Framework-specific patterns** — How your project uses React/Django/Spring, not how the framework works in general
2. **Architecture decisions** — Where code should go, how layers communicate
3. **Error handling conventions** — Custom error classes, logging patterns, retry strategies
4. **Testing conventions** — Framework choices, naming patterns, what to test
5. **Naming conventions** — Project-specific naming that differs from defaults
6. **Anti-patterns** — Specific things to avoid with explanation of why
7. **Database patterns** — ORM conventions, migration patterns, query patterns
8. **Security patterns** — Auth patterns, input validation, secrets handling
