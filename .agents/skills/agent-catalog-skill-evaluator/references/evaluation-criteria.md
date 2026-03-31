# Evaluation Criteria

Rubrics for scoring each evaluation dimension. Apply these consistently across all skills in a collection.

## Usage Value (1–5)

How useful is this skill to a broad audience of agent users?

| Score | Criteria |
|-------|----------|
| **5 — Essential** | Solves a common, high-frequency problem. Most agent users would benefit. Clear, well-scoped purpose. Examples: code review, test generation, documentation writing. |
| **4 — Broadly useful** | Solves a real problem for a significant segment of users. Good scope and clear value proposition. Examples: API design, database optimization, CI/CD setup. |
| **3 — Niche but solid** | Useful for a specific audience or domain. Well-executed but limited appeal. Examples: Salesforce development, embedded systems, specific framework expert. |
| **2 — Narrow** | Very specific use case or overlaps heavily with general agent capabilities. Limited incremental value. Examples: single-language formatter, trivial wrapper around existing tools. |
| **1 — Minimal** | Unclear purpose, trivial functionality, or so broad it adds no focus. Examples: generic "helper" skills, placeholder skills, skills that just repeat what the base agent does. |

**Scoring signals:**
- Does the description clearly articulate a problem being solved?
- Would you recommend this skill to a colleague?
- Does it provide knowledge or workflow the base agent lacks?

## Security Risk (low / medium / high)

Does the skill introduce security concerns?

| Rating | Criteria |
|--------|----------|
| **Low** | Self-contained. No scripts, no external URLs, no credential references. Pure prompt/instruction content. |
| **Medium** | Uses scripts but they are read-only or local-only. References external documentation URLs (fetch, not POST). Has `allowed-tools` restrictions. May handle file I/O. |
| **High** | Executes scripts that make network requests. References API keys, tokens, or credentials. Fetches and executes remote content. Uses `allowed-tools` permissively or not at all despite having scripts. Modifies system state (git push, deploy, database writes). |

**Escalation signals — automatically bump to at least medium:**
- Any `scripts/` directory with executable code
- Any URL in SKILL.md body that isn't documentation
- Any reference to environment variables, secrets, or API keys
- Any use of `subprocess`, `os.system`, `exec`, `eval`, or equivalent
- Any `allowed-tools` that includes terminal/shell execution

**Escalation signals — automatically bump to high:**
- Scripts that POST/PUT/DELETE to external APIs
- Scripts that read/write credentials or tokens
- Instructions to clone repos, install packages, or modify system config
- Use of `curl`, `wget`, `fetch` to non-documentation endpoints in scripts

## Best Practices (1–5)

How well does the skill follow Agent Skills specification and design best practices?

| Score | Criteria |
|-------|----------|
| **5 — Exemplary** | Full spec-compliant frontmatter with rich metadata. Clear role definition. Domain-appropriate workflow. Conditional reference loading. Specific MUST/MUST NOT constraints. Knowledge Reference section. Platform-agnostic. Appropriate use of scripts/references/agents. |
| **4 — Good** | Valid frontmatter with most metadata fields. Clear workflow. References used well. Minor gaps (e.g., missing `triggers` or `related-skills`). |
| **3 — Adequate** | Valid frontmatter with basic fields. Functional but could be better structured. Some anti-patterns (verbose instructions, redundant context, missing constraints). |
| **2 — Weak** | Minimal frontmatter (just name + description). No structured workflow. Instructions are prose-heavy or vague. No constraints section. |
| **1 — Poor** | Invalid or missing frontmatter. No clear structure. Instructions are ambiguous or contradictory. Would confuse the agent more than help. |

**Checklist (award 1 point per item, map to 1–5):**
- [ ] Valid YAML frontmatter with `name` and `description`
- [ ] `description` includes WHAT and WHEN
- [ ] `metadata` block with domain, role, scope
- [ ] `triggers` field with activation keywords
- [ ] Clear role definition paragraph
- [ ] Structured workflow with numbered steps
- [ ] MUST DO / MUST NOT DO constraints
- [ ] Appropriate use of references/ for large content
- [ ] No redundant instructions (things the AI already knows)
- [ ] Knowledge Reference vocabulary section

## Core Capabilities

Extract a 1–3 sentence summary of what the skill does. Focus on:
- Primary task or output
- Target audience or domain
- Key differentiator from general agent behavior

**Template:** "[Skill name] helps [audience] [do what] by [how it differs from baseline agent]. Primary output: [output type]."

## External Requirements Indicator

Binary classification: **self-contained** or **has-external-dependencies**.

**Critical distinction — runtime dependency vs. content reference:**
A skill that *discusses*, *teaches*, or *helps users work with* an external service is NOT dependent on that service. External requirements are only things the **skill itself** needs at runtime to function. A skill about building Chrome extensions mentions the Chrome Web Store — that is subject matter, not a dependency.

A skill is **self-contained** if:
- It has no scripts that make network calls
- It does not require the agent to authenticate with or call an external API to complete its workflow
- It does not require specific CLI tools or runtimes to be installed before use
- All reference content is bundled in the skill directory

A skill **has external dependencies** if ANY of these are true:
- Scripts in `scripts/` make network requests (HTTP calls, API calls)
- The skill's workflow cannot complete without a live external service being available (e.g., must query a database, must call a REST API)
- Requires specific CLI tools to be installed (e.g., `terraform`, `docker`, `aws`)
- References MCP servers that must be configured and running
- Scripts include `pip install`, `npm install`, or similar package installation

**Does NOT count as an external dependency:**
- External services, platforms, or SDKs mentioned as examples or context within the skill's guidance
- Platforms the skill *helps users build for* (e.g., an agent-skill-plugin-builder skill mentioning Chrome Web Store, Firefox Add-ons, VS Code Extension API, or JetBrains Platform SDK as target platforms)
- Documentation URLs or links to external references
- APIs or services mentioned as subject matter the skill teaches users about
- Tool names cited in skill content that the human user would use — not the agent itself

## External Requirements

List specific external dependencies — only things the **skill's agent workflow** requires at runtime. Categories:

| Category | Examples |
|----------|----------|
| **APIs** | GitHub API (when scripts call it), OpenAI API (when scripts call it) |
| **Services** | PostgreSQL (when scripts connect to it), Redis (when scripts use it) |
| **CLI tools** | Docker, Terraform, AWS CLI (when skill instructions invoke these directly) |
| **Runtimes** | Python 3.x, Node.js 18+ (when `scripts/` directory requires them) |
| **MCP servers** | Specific MCP server integrations the skill requires to be configured |
| **Package managers** | pip, npm, cargo (only when scripts install packages at runtime) |

Record as an array of strings. Use `["none"]` (as a single-element array) if self-contained.

**Anti-patterns to avoid:**
- Do NOT list platforms or SDKs mentioned in the skill's content as subject matter (e.g., an "agent-skill-plugin-builder" skill that teaches plugin development should not have "Chrome Web Store" or "VS Code Extension API" as external requirements — those are content references, not runtime dependencies)
- Do NOT infer requirements from the skill's name or topic area; only extract what is explicitly required for the skill's workflow to function

## Script Language Detection

Scan the `scripts/` directory (if present):

1. **File extensions** — `.py` → Python, `.sh/.bash` → Bash, `.js/.mjs` → JavaScript, `.ts` → TypeScript, `.rb` → Ruby, `.ps1` → PowerShell
2. **Shebang lines** — `#!/usr/bin/env python3` → Python, `#!/bin/bash` → Bash, etc.
3. **Mixed** — Report all languages found as an array

Record as an array of strings. Use `["none"]` if no scripts directory exists.

## License Detection

Check in order:
1. `license` field in YAML frontmatter
2. `LICENSE.txt` or `LICENSE.md` in the skill directory
3. `LICENSE` file in the skill directory
4. Parent directory LICENSE (for monorepo skills)

Record the SPDX identifier when possible (MIT, Apache-2.0, GPL-3.0, etc.). If a custom license or no license is found, record "custom" or "unspecified" respectively.
