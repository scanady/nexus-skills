---
name: agent-skill-copilot-instructions
description: 'Creates expertly crafted GitHub Copilot custom instructions files (.instructions.md and copilot-instructions.md) tailored to specific domains, languages, frameworks, or repositories. Use when asked to create custom instructions, write copilot instructions, create .instructions.md files, set up copilot-instructions.md, configure Copilot for a project, add path-specific instructions, write coding guidelines for Copilot, or customize Copilot behavior for a repository.'
---

# GitHub Copilot Custom Instructions Writer

## Purpose
Create high-quality GitHub Copilot custom instructions files that give Copilot the context it needs to generate accurate, project-aligned code and reviews.

---

## Execution Logic

**Check $ARGUMENTS first to determine execution mode:**

### If $ARGUMENTS is empty or not provided:
Respond with:
"agent-skill-copilot-instructions loaded, describe the domain, language, framework, or repository you want instructions for"

Then wait for the user to provide their requirements in the next message.

### If $ARGUMENTS contains content:
Proceed immediately to Task Execution (skip the "loaded" message).

---

## Task Execution

When user requirements are available (either from initial $ARGUMENTS or follow-up message):

### 1. MANDATORY: Read Reference Files FIRST
**BLOCKING REQUIREMENT — DO NOT SKIP THIS STEP**

Before doing ANYTHING else, you MUST read every file in `./references/`. This is non-negotiable.

**DO NOT PROCEED** to Step 2 until you have read all reference files and have their content in context.

### 2. Determine Instruction Type

From the user's input, determine which type of instructions file to create:

| Type | When to Use | File Location |
|------|------------|---------------|
| **Path-specific** | Targeted at a language, framework, platform, file type, or directory | `.github/instructions/<domain>.instructions.md` |
| **Repository-wide** | General project guidance, tech stack, structure, conventions | `.github/copilot-instructions.md` |

**Default:** Path-specific. Only create repository-wide if the user explicitly asks for it or the instructions clearly apply to the entire repository.

**Never create agent instructions** (AGENTS.md, CLAUDE.md, GEMINI.md). This skill only creates Copilot instructions files.

### 3. Analyze Input

From the user's requirements, extract:
- **Domain/subject area** — the language, framework, platform, or technology
- **Target files** — what glob pattern should `applyTo` use (path-specific only)
- **Key conventions** — naming, style, patterns, anti-patterns
- **Project context** — any specifics about how this technology is used in the project

For any missing information, apply defaults from **Defaults & Assumptions**.

### 4. Check for Project Context

Before writing, gather context to personalize the instructions:
- Check for existing `.github/copilot-instructions.md` — avoid duplicating what's already there
- Check for existing `.github/instructions/*.instructions.md` — avoid conflicts or overlap
- Check for `README.md`, `package.json`, `pom.xml`, `Cargo.toml`, or other project manifests to understand the tech stack
- Check for linting configs (`.eslintrc`, `.prettierrc`, `ruff.toml`, etc.) — don't repeat what linters enforce
- Check for existing `CLAUDE.md` or `AGENTS.md` — understand existing conventions

Use discovered context to make instructions specific and relevant rather than generic.

### 5. Write the Instructions File

Apply the writing principles from [references/writing-principles.md](references/writing-principles.md) and structure from [references/instructions-anatomy.md](references/instructions-anatomy.md).

**For path-specific instructions:**
1. Add YAML frontmatter with `applyTo` glob pattern
2. Add a clear `#` title describing the domain
3. Organize rules into logical sections using `##` headings
4. Write concise, imperative rules — direct Copilot behavior
5. Include code examples for patterns and anti-patterns where they add clarity
6. Add `excludeAgent` frontmatter only if the user specifies the file is for code review only or coding agent only

**For repository-wide instructions:**
1. Add a project overview (elevator pitch — what, who, key features)
2. Document the tech stack with brief usage notes
3. Spell out coding guidelines that apply across the codebase
4. Describe project structure with directory purposes
5. Point to available resources (scripts, MCP servers, tools)

### 6. Name the File

**Path-specific naming convention:** The filename should clearly indicate the domain:
- Language: `typescript.instructions.md`, `python.instructions.md`, `java.instructions.md`
- Framework: `react.instructions.md`, `django.instructions.md`, `spring-boot.instructions.md`
- Platform: `aws.instructions.md`, `docker.instructions.md`
- Concern: `testing.instructions.md`, `security.instructions.md`, `api-design.instructions.md`
- Combined: `nextjs-frontend.instructions.md`, `java-backend.instructions.md`

**Repository-wide:** Always `copilot-instructions.md` in `.github/`.

### 7. Verify and Present

- Run through the **Quality Checklist**
- Present the complete file content
- Save the file to the correct location

---

## Writing Rules

Hard constraints. No interpretation.

### Core Rules
- **Be direct** — use short, imperative statements ("Use X", "Prefer Y over Z", "Never do W")
- **Be specific** — concrete patterns beat abstract principles ("Use `camelCase` for variables" not "use consistent naming")
- **Show, don't just tell** — include code examples for non-obvious patterns
- **Stay under 1000 lines** — shorter is better; aim for 50-200 lines for path-specific files
- **No external links** — Copilot cannot follow them; inline the relevant content
- **No meta-commentary** — don't explain why the file exists or how Copilot works; just state the rules
- **No vague directives** — never write "be more accurate" or "write clean code"

### Structural Rules
- Use Markdown headings (`##`) to organize into scannable sections
- Use bullet points or numbered lists — never dense paragraphs
- Use code blocks with language tags for examples
- Label examples as correct/incorrect patterns when showing both
- Keep each rule to 1-2 lines; expand only with examples

### Content Rules
- **Don't duplicate linter rules** — if ESLint/Prettier/Ruff already enforce it, skip it
- **Don't state obvious language conventions** — focus on project-specific decisions
- **Don't contradict existing instructions** — check what's already in `.github/`
- **Focus on decisions, not defaults** — document choices that deviate from standard conventions
- **Include framework-specific patterns** — these are the highest-value instructions
- **Add error handling patterns** — how should errors be handled in this codebase
- **Add testing conventions** — testing framework, naming, patterns

### Frontmatter Rules (Path-Specific Only)
- `applyTo` is required — must be a valid glob pattern
- Use `**/*.ext` for language-wide rules
- Use `src/dir/**` for directory-scoped rules
- Combine patterns with commas: `"**/*.ts,**/*.tsx"`
- `excludeAgent` is optional — use `"code-review"` or `"coding-agent"` only when needed

---

## Output Format

### Path-Specific Instructions

```markdown
---
applyTo: "<glob-pattern>"
---
# <Domain> Guidelines

## <Section 1>
- [Rule as imperative statement]
- [Rule as imperative statement]

## <Section 2>
- [Rule]

## Code Examples

```<language>
// Correct pattern
<example>

// Incorrect pattern
<example>
```

## <Additional Sections as Needed>
- [Rules organized by topic]
```

### Repository-Wide Instructions

```markdown
# <Project Name>

<Brief description of what the project does, who it's for, and key features.>

## Tech Stack

### Backend
- [Technology and how it's used]

### Frontend
- [Technology and how it's used]

### Testing
- [Framework and conventions]

## Coding Guidelines
- [Cross-cutting rules that apply everywhere]

## Project Structure
- `dir/` : [Purpose]
- `dir/` : [Purpose]

## Resources
- `scripts/` : [Available automation]
- [Tools and how to use them]
```

---

## References

**These files MUST be read before task execution (see Step 1):**

| File | Purpose |
|------|---------|
| `./references/writing-principles.md` | Core principles for effective instructions writing |
| `./references/instructions-anatomy.md` | Structural patterns and section templates for both file types |
| `./references/applyto-patterns.md` | Common glob patterns for `applyTo` frontmatter |

**Why these matter:** The reference files contain distilled best practices from GitHub's official documentation and real-world instructions files, ensuring the output follows proven patterns rather than generic advice.

---

## Quality Checklist (Self-Verification)

Before finalizing output, verify ALL of the following:

### Pre-Execution Check
- [ ] I read all reference files before starting
- [ ] I checked for existing instructions files to avoid conflicts
- [ ] I checked project context (README, configs, manifests)

### Content Check
- [ ] Every rule is specific and actionable (no vague directives)
- [ ] No external links are included
- [ ] No rules that duplicate linter/formatter enforcement
- [ ] Code examples are included where patterns aren't obvious
- [ ] Correct/incorrect patterns are labeled clearly
- [ ] Content is organized under clear section headings

### Format Check
- [ ] Frontmatter `applyTo` uses correct glob syntax (path-specific only)
- [ ] File is named according to the naming convention
- [ ] File is saved to the correct directory (`.github/instructions/` or `.github/`)
- [ ] Total length is reasonable (50-200 lines for path-specific, up to 500 for repo-wide)

### Quality Check
- [ ] Instructions are specific to the domain, not generic filler
- [ ] Rules reflect actual project conventions (not just language defaults)
- [ ] A developer reading this would learn something non-obvious about the project
- [ ] No contradictions with existing instructions files

**If ANY check fails → revise before presenting.**

---

## Defaults & Assumptions

Use these unless the user specifies otherwise:

- **Instruction type:** Path-specific (`.instructions.md`)
- **File location:** `.github/instructions/`
- **Target audience for rules:** Copilot (AI coding assistant), not human developers
- **excludeAgent:** Not set (both coding agent and code review use the file)
- **Code examples:** Include at least one correct/incorrect pair for the most important convention
- **Scope:** Focus on the specific domain requested; don't try to cover everything
- **Length target:** 50-200 lines for path-specific; up to 500 lines for repository-wide

Document any assumptions made in a brief comment at the end of the generated file.
