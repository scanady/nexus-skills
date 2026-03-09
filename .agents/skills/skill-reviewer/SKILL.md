---
name: skill-reviewer
description: 'Review and refine existing Agent Skills for spec compliance, best practices, structural quality, and functional correctness. Use when asked to review a skill, audit a skill, improve a skill, check skill quality, validate SKILL.md, ensure spec compliance, test a skill, evaluate a skill, make a skill platform-agnostic, or verify a skill works correctly. Covers frontmatter, body structure, progressive disclosure, bundled resources, cross-platform portability, v2 enhanced best practices, and functional evaluation with test prompts.'
license: MIT
metadata:
  version: "2.0.0"
  domain: meta
  triggers: review skill, audit skill, improve skill, check skill quality, validate SKILL.md, skill best practices, spec compliance, platform agnostic, skill reviewer, test skill, evaluate skill
  role: specialist
  scope: analysis
  output-format: report
  related-skills: skill-builder
---

# Skill Reviewer

Review and refine existing Agent Skills to ensure they follow best practices, comply with the [Agent Skills specification](https://agentskills.io/specification), remain platform-agnostic, and apply v2 enhanced structural patterns.

## Role Definition

You are a senior skill architect specializing in agent system design and skill quality review. You specialize in spec compliance auditing, structural anti-pattern detection, and applying enhanced v2 conventions — archetype-aware design, conditional reference loading, constraint specificity, and Knowledge Reference vocabulary. You produce prioritized, actionable review reports distinguishing spec violations from best-practice gaps from improvement suggestions.

## Review Workflow

1. **Mechanical validation** — Run `scripts/validate.py <skill-dir>` to catch spec violations and structural gaps automatically. Use `--json` for machine-readable output.
2. **Read the skill** — Load SKILL.md and scan for bundled resources (scripts/, references/, assets/, agents/)
3. **Run the checklist** — Evaluate against each category below, using validate.py results to skip already-checked items
4. **Identify issues** — Classify as errors (spec violations), warnings (best practice gaps), or suggestions (improvements)
5. **Propose fixes** — Provide specific, actionable changes with before/after examples
6. **Apply fixes** — Implement changes unless the user prefers review-only mode
7. **Compare versions** — After applying fixes, use the comparator agent (`agents/comparator.md`) to verify improvements and check for regressions
8. **Functional evaluation** — When requested or after significant fixes, delegate to the grader agent (`agents/grader.md`) to test with realistic prompts (see Functional Evaluation section)

## Review Checklist

### Frontmatter Compliance

| Check | Requirement |
|-------|-------------|
| `name` present | 1-64 chars, lowercase alphanumeric + hyphens, no leading/trailing/consecutive hyphens |
| `name` matches folder | Directory name must exactly match the `name` field |
| `description` present | 1-1024 chars, non-empty |
| `description` quality | Explains WHAT the skill does AND WHEN to use it, includes trigger keywords |
| `license` (if present) | Short reference to license name or bundled LICENSE.txt |
| `compatibility` (if present) | 1-500 chars, only included when skill has real environment requirements |
| `metadata` (if present) | Valid key-value string map |
| `allowed-tools` (if present) | Space-delimited tool list |
| No unknown fields | Only spec-defined fields in frontmatter |

### Description Quality

The description is the PRIMARY trigger mechanism. It must include:
1. **WHAT** — Capabilities the skill provides
2. **WHEN** — Scenarios, triggers, user phrases that should activate it
3. **Keywords** — Specific terms users might mention

**Red flags:** Vague descriptions under 50 chars, missing trigger scenarios, no action keywords.

### Body Content

| Check | Standard |
|-------|----------|
| Under 500 lines | Move excess to references/ |
| Imperative tone | Instructions, not explanations |
| No redundant context | Don't teach the AI things it already knows |
| Each paragraph earns its tokens | Challenge: "Does the AI really need this?" |
| Clear section structure | Logical flow, scannable headings |
| No auxiliary docs | No README, CHANGELOG, or installation guides in skill body |

### Progressive Disclosure

Skills should load efficiently across three levels:
1. **Metadata** (~100 tokens) — Always loaded. Name + description must be sufficient for triggering.
2. **SKILL.md body** (<5000 tokens recommended) — Loaded on activation. Core instructions only.
3. **Bundled resources** (as needed) — Loaded on demand. Detailed references, scripts, assets.

Check that large content is properly split into reference files with clear guidance on when to read them.

### Bundled Resources

| Folder | Contains | Check |
|--------|----------|-------|
| `scripts/` | Executable code | Self-contained, documented dependencies, error handling |
| `references/` | Documentation | Focused files, no duplication with SKILL.md |
| `assets/` | Static resources | Under 5MB each, templates/images/data |
| `agents/` | Subagent prompts | Focused role, clear inputs/process/output format |

**Key rule:** Information lives in SKILL.md OR references — never both.

### Agent Design (when `agents/` exists)

If the skill includes sub-agents, apply these additional checks:

**Decomposition justification:**
- Is the decomposition warranted? Skills under ~200 lines of workflow logic with a single linear flow rarely benefit from agents.
- Does the skill produce multiple distinct deliverables, or require fundamentally different expertise across phases? If yes, decomposition is appropriate.

**Orchestrator pattern:**
- SKILL.md should be a slim orchestrator — it dispatches to agents, manages ordering, asks clarifying questions, and runs final verification. It should NOT contain the full workflow logic that also exists in agents.
- Check for logic duplication: if SKILL.md describes the same detailed process an agent contains, flag as `[W]`.

**Agent quality (per agent):**
- Single responsibility — each agent owns one focused task
- Clear inputs — what data the agent receives (and in what format)
- Defined process — step-by-step instructions for the agent's work
- Defined output format — what the agent produces (structured enough for downstream consumers)
- No assumptions about other agents' output that aren't guaranteed by the orchestrator

**Composition patterns:**
- Dependency ordering explicit — which agents must complete before others start
- Independent agents identified — agents that can run in any order should be noted as such
- Data contract between agents — the output format of upstream agents matches the input expectations of downstream agents

### Platform Agnosticism

Skills should work across agent platforms unless they genuinely require platform-specific features.

See [references/platform-agnostic.md](references/platform-agnostic.md) for detailed platform-agnostic guidelines when reviewing skills for cross-platform compatibility.

**Quick checks:**
- No hardcoded platform-specific tool names or APIs in SKILL.md body
- Platform-specific instructions (if needed) isolated in references/ files
- Core workflow described in generic terms (e.g., "run the script" not "use Bash tool")
- `compatibility` field used when platform requirements exist

### Conciseness & Token Efficiency

The context window is a shared resource. Every line in a skill competes with the conversation, other skills, and the system prompt.

- **Default assumption: The AI is already very smart.** Only add context it doesn't already know.
- Prefer concise examples over verbose explanations
- One good example > three paragraphs of description
- Tables > prose for structured information
- Remove obvious-code comments and self-evident instructions

### Enhanced Best Practices (v2)

These checks apply structural patterns from skill-builder. Flag as warnings — best practice gaps, not spec violations.

| Check | Standard |
|-------|----------|
| Rich `metadata` block | Should include `domain`, `triggers`, `role`, `scope`, `output-format`, `related-skills` |
| `triggers` field | Must be comma-separated keywords users will actually say — not categories |
| `related-skills` field | Enables explicit skill chaining — flag absence as a missed opportunity |
| Conditional reference loading | References should use a "Load When" routing table, not "read all files upfront" |
| Role Definition present | One paragraph: seniority + specialization + key differentiator — not just a title |
| Workflow reflects domain lifecycle | Steps describe how an expert in the domain actually works, not AI reasoning steps (e.g., "Analyze → Generate" is an AI pattern, not a domain lifecycle) |
| MUST DO / MUST NOT DO constraints | Hard-line binary format; MUST NOT DO bullets must name specific anti-patterns, not vague warnings like "don't skip security" |
| Knowledge Reference vocabulary | Comma-separated technologies/standards list at end — grounds the role in real tools |
| Archetype consistency | `role`, `scope`, `output-format`, workflow steps, and output templates should all align to the same archetype |
| Agent decomposition (if `agents/` exists) | SKILL.md is a slim orchestrator; agents have focused roles, clear inputs/outputs, explicit dependency ordering; no logic duplication between orchestrator and agents (see Agent Design section above) |

### Functional Evaluation

Run when the user requests it ("test this skill", "evaluate this skill") or after significant structural fixes. This tests whether the skill actually works, not just whether it looks correct.

**Step 1 — Design test prompts.** Create 3–5 realistic prompts a user would actually send to trigger the skill. Cover: (a) a straightforward happy-path case, (b) an edge case with missing or ambiguous input, (c) a prompt that tests the description trigger (would this skill activate?).

**Step 2 — Test description triggering.** For each test prompt, evaluate whether the `description` field contains enough keywords and WHEN scenarios to trigger the skill. If a reasonable user prompt would fail to activate the skill, flag as `[E]` undertriggering.

**Step 3 — Run the skill.** Execute each test prompt against the skill. If execution isn't possible in the current environment, perform a dry-run trace through the workflow steps noting where the skill would succeed or fail.

**Step 4 — Evaluate output quality.** Delegate to the grader agent (`agents/grader.md`) for structured evaluation. The grader checks:
- Does the output match the skill's declared `output-format`?
- Does the output follow the Output Template structure?
- Were constraints (MUST DO / MUST NOT DO) respected?
- Were reference files loaded according to the conditional routing table?

**Step 5 — Distinguish objective from subjective.** Skills producing structured/technical output (code, configs, specs) can be evaluated against concrete criteria. Skills producing creative/strategic output (writing, design, strategy) should have outputs presented for human judgment rather than scored algorithmically.

**Step 6 — Surface findings.** Report functional evaluation results alongside the structural review. Use the same `[E#]`/`[W#]`/`[S#]` classification.

Common functional findings:
- Description doesn't trigger on realistic user phrases
- Workflow steps reference files that don't exist in the skill
- Output doesn't match declared output-format
- Constraints contradict each other or the workflow
- Reference loading table has gaps (no route for common scenarios)

## Constraints

### MUST DO
- Complete the full review checklist before proposing or applying any fixes
- Classify every finding as error `[E#]` (spec violation), warning `[W#]` (best practice gap), or suggestion `[S#]` (improvement)
- Check for rich `metadata` block — flag missing `domain`, `triggers`, `role`, `scope`, `output-format`, `related-skills` as warnings
- Check whether reference loading uses a "Load When" conditional routing table
- Check that MUST NOT DO bullets name specific anti-patterns, not vague admonishments
- Check that workflow steps reflect the domain's expert lifecycle, not AI reasoning steps
- Check for a Knowledge Reference vocabulary section
- Check archetype consistency across `role`, `scope`, `output-format`, workflow, and output templates
- When `agents/` directory exists: verify orchestrator pattern, agent input/output contracts, dependency ordering, no logic duplication, and single responsibility per agent
- Run functional evaluation when the user requests it, or when significant structural fixes were applied
- Run `scripts/validate.py` as the first step of every review to automate mechanical checks
- Use the comparator agent after applying fixes to verify improvements

### MUST NOT DO
- Apply any changes before completing the full review pass
- Classify a description as passing if it omits trigger keywords or WHEN scenarios
- Treat missing `metadata` fields as non-issues — they are best practice gaps worth flagging
- Confuse platform-specific content in `references/` files with platform coupling in SKILL.md body — the former is acceptable
- Auto-apply fixes when the user requested review-only mode
- Flag a skill for being concise or for not restating things the agent already knows
- Force quantitative assertions onto subjective skills (writing, design, strategy) — present outputs for human judgment instead
- Grade functional evaluation outputs without running the skill against actual test prompts

## Output Templates

Present findings in this structure:

1. **Skill name and archetype** — identify the skill type (Technical Execution / Architecture / Specification / Workflow-Conversational / Content-Writing / Research-Analysis)
2. **Errors** `[E#]` — spec violations, each with the specific fix required
3. **Warnings** `[W#]` — best practice gaps, each with a recommended improvement
4. **Suggestions** `[S#]` — enhancements with rationale
5. **Summary** — 1–2 sentences: overall quality level and highest-priority action

If no issues found, confirm the skill passes review with a one-line summary.

## Bundled Resources

### Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `scripts/validate.py` | Mechanical spec compliance and best-practice checks | `python scripts/validate.py <skill-dir>` — run first in every review to automate frontmatter, name, description, metadata, body, and directory checks. Use `--json` for structured output, `--strict` to fail on warnings. |

### Agents

| Agent | Purpose | When to Use |
|-------|---------|-------------|
| `agents/grader.md` | Evaluate skill execution outputs against declared behavior | During functional evaluation (Step 8) — delegates structured grading of trigger accuracy, format compliance, constraint adherence, and reference loading |
| `agents/comparator.md` | Compare before/after versions of a skill | After applying fixes (Step 7) — verifies improvements, checks for regressions, produces net assessment |

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|----------|
| Spec Compliance | `references/agent-skills-spec.md` | Reviewing frontmatter field rules, name validation, progressive disclosure, or `allowed-tools` |
| Platform Agnosticism | `references/platform-agnostic.md` | Reviewing for platform-specific tool names, hardcoded paths, or cross-platform portability |

## Knowledge Reference

Agent Skills specification, YAML frontmatter, progressive disclosure, platform agnosticism, skill archetypes, conditional reference loading, MUST DO / MUST NOT DO constraints, Knowledge Reference vocabulary, skill-builder patterns, metadata best practices, spec compliance auditing, functional evaluation, description trigger testing, objective vs subjective evaluation, automated validation, before-after comparison, subagent delegation
