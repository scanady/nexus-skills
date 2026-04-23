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
- **Domain-value calibration:** Skills in specialized domains (healthcare, legal, manufacturing, niche industry) provide higher value because the base model has a larger capability gap in those areas. Skills in well-covered domains (software engineering, mathematics) face a higher bar to earn a 4–5 score.

## Security Risk (low / medium / high)

Does the skill introduce security concerns? Score each of the six sub-dimensions on a 1–5 scale (5 = safest), then derive the composite rating.

### Six-Dimension Safety Sub-Scores

Evaluate each dimension using the static content of SKILL.md and any scripts. Score 1–5 (higher = safer/lower risk). Load `references/security-patterns.md` for pattern examples.

| Sub-Dimension | What to Assess |
|---------------|----------------|
| **Data & Privacy Risk** | Does the skill access, expose, or transmit personal/sensitive data without clear justification? |
| **Prompt Injection / Command Hijacking** | Does the skill contain instructions that could redirect the agent from its intended behavior, override safety constraints, or respond to injected prompts? |
| **Illegal or Offensive Content** | Does the skill generate or facilitate fraud, prohibited activities, abusive language, or other harmful outputs? |
| **Bias or Discrimination** | Does the skill produce or encode unfair, discriminatory, or stereotyped outputs? |
| **System Integrity Risk** | Does the skill perform actions that may compromise system stability, security, or configuration without proper authorization? |
| **Untrusted Communication Risk** | Does the skill interact with unverified external services, retrieve untrusted content, or transmit data to third parties without sufficient justification? |

### Composite Rating Derivation

| Composite | Criteria |
|-----------|----------|
| **low** | All six sub-dimensions score 4–5. No scripts, external calls, or credential handling. |
| **medium** | Any sub-dimension scores 3. Scripts exist but are local/read-only. Some external GET access. Has `allowed-tools` restrictions. |
| **high** | Any sub-dimension scores 1–2. Scripts POST/PUT/DELETE to external APIs. Reads/writes credentials or tokens. Executes remote content. Modifies system state (git push, deploy, database writes). |

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

## Executability (1–5)

How reliably can an agent execute this skill? Score 1–5 based on the average of four sub-dimensions:

| Sub-Dimension | What to Assess |
|---------------|----------------|
| **Completeness** | Are all steps, preconditions, tools, and resources specified? Does the skill include enough detail for an agent to start and finish without guessing? |
| **Determinism** | Are instructions precise and unambiguous? Does the skill define clear decision rules and branching conditions that minimize open-ended interpretation? |
| **Consistency** | Is the skill internally coherent? No contradictory instructions, undefined variables, inconsistent tool names, or references to resources not provided. |
| **Usability** | Does the skill generalize across different instances of the same task, or is it coupled to a single specific scenario? (See also Over-Specification Risk.) |

| Score | Criteria |
|-------|----------|
| **5 — Excellent** | All four sub-dimensions are strong. Step-by-step workflow is complete, precise, and internally consistent. Works across instances without modification. |
| **4 — Good** | Minor gaps in one sub-dimension. A skilled agent can fill in the blanks, but the skill could be more explicit. |
| **3 — Adequate** | Noticeable weaknesses in 1–2 sub-dimensions. Some steps are ambiguous or require significant agent inference. May fail on edge cases. |
| **2 — Weak** | Multiple sub-dimensions are poor. Instructions are vague, incomplete, or inconsistent. Agent would likely deviate significantly or stall. |
| **1 — Poor** | Fails on most sub-dimensions. No usable workflow. Agent cannot complete the task using this skill alone. |

Record `completeness`, `determinism`, `consistency`, and `usability` as individual 1–5 scores; compute `score` as their average (round to nearest integer).

## Invocability (1–5)

How reliably will an agent select and trigger this skill at the right time — and only at the right time?

| Score | Criteria |
|-------|----------|
| **5 — Excellent** | `name` is globally unique, domain-scoped, and immediately recognizable. `description` contains specific trigger keywords matching real user prompts and clearly excludes adjacent tasks. `triggers` metadata is populated. No false-positive invocation risk. |
| **4 — Good** | Name and description are clear and mostly specific. Minor risk of over-triggering on adjacent tasks, or slight under-triggering on less obvious phrasings. |
| **3 — Adequate** | Name or description is somewhat generic. A capable agent will usually invoke correctly, but edge cases exist where the skill is missed or triggers when it shouldn't. |
| **2 — Weak** | Name is vague (e.g., "helper", "utils") or description is overloaded with multiple unrelated triggers. Likely to either miss invocations or false-positive frequently. |
| **1 — Poor** | No effective trigger mechanism. Name conflicts with other skills or is too generic. Description is absent or provides no discriminating signal. Agent cannot reliably select this skill. |

**Invocability checklist:**
- [ ] `name` is unique, specific, and domain-namespaced (e.g., `tech-quality-tdd`, not `testing`)
- [ ] `description` starts with when-to-use phrasing ("Use when...", "Invoked when...")
- [ ] `description` lists specific trigger phrases that match realistic user prompts
- [ ] `description` does NOT describe competing or adjacent skills (reduces false positives)
- [ ] `triggers` metadata field is populated with comma-separated keywords
- [ ] No namespace collision with other skills in the collection

**False positive check:** Would a prompt for a related-but-different task incorrectly trigger this skill? If yes, deduct 1–2 points.

## Token Efficiency

Estimate the skill's token footprint and classify it. Token count is the combined character count of SKILL.md plus all files in `references/` and inline script content, divided by 4.

> **Note:** This uses a character-count / 4 approximation. Scripts and reference files are included in the estimate since they are typically loaded into context during execution.

| Class | Token Count | Assessment |
|-------|-------------|------------|
| **compact** | < 800 tokens | Ideal. Focused, high signal-to-noise. Less context consumed during execution. |
| **detailed** | 800–1,200 tokens | Good. Sufficient depth without bloat. |
| **comprehensive** | > 1,200 tokens | Review for trim opportunities. Research shows skills in this range average lower task accuracy than compact/detailed skills, likely due to increased cognitive load and context dilution. |

Record as `complexity_class` in the JSON output. Flag comprehensive skills in the evaluation summary as candidates for trimming.

## Over-Specification Risk

Binary flag: does the skill hardcode instance-specific values that would cause it to fail or mislead when the task parameters change?

**Flag as `true` if the skill contains:**
- Hardcoded file paths, column names, entity names, or numerical thresholds tied to a specific dataset or project
- Exact output values or expected results baked into the instructions
- Task-specific tool configurations that won't generalize
- References to specific user/org names, repository names, or environments

**Flag as `false` if:**
- All parameters are described as inputs to be determined from context
- The skill provides guidance patterns and decision rules, not fixed answers
- Any example values are clearly marked as illustrations, not requirements

Record as `over_specification_risk: { "flagged": true/false, "rationale": "one sentence" }`.

This is distinct from Executability's *usability* sub-dimension: over-specification risk is about hardcoded values, while usability is about structural generalizability.

## Skill Pattern (A / B / C)

Classify the skill by its structural composition:

| Pattern | Composition | Signal |
|---------|-------------|--------|
| **A** | Instructions only — SKILL.md prose/markdown with no executable scripts | Most common. Appropriate for workflow guidance, design patterns, domain knowledge. |
| **B** | Instructions + scripts — SKILL.md with one or more files in `scripts/` | Appropriate for tasks requiring data processing, automation, or tool invocation. Human-authored skills are ~33% Pattern B. |
| **C** | Instructions + MCP servers or sub-agents — skill orchestrates external agent infrastructure | Rare (~2% of human-authored skills). Appropriate for complex multi-system workflows. |

Record as `skill_pattern` in the JSON output (`"A"`, `"B"`, or `"C"`).

**Pattern upgrade signal:** If a skill is Pattern A but its workflow involves numerical computation, file transformation, API calls, or multi-step data processing, flag it as a candidate for Pattern B upgrade.

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
