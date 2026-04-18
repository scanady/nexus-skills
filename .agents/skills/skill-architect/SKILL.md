---
name: skill-architect
description: 'Full lifecycle skill management — build, review, and optimize Agent Skills. Use when asked to "create a skill", "build a skill", "scaffold a skill", "make a new skill", "review a skill", "audit a skill", "improve a skill", "optimize a skill", "add metadata to a skill", "refine metadata", or "update skill frontmatter". Handles the full lifecycle: classifies archetype, scaffolds new skills, reviews existing skills for spec compliance and best practices, and updates metadata for discoverability. Use whenever the user is working on a SKILL.md file or wants to create one.'
license: MIT
metadata:
  version: "1.0.0"
  domain: meta
  triggers: create skill, build skill, scaffold skill, new skill, review skill, audit skill, improve skill, optimize skill, check skill quality, validate SKILL.md, skill metadata, refine metadata, update frontmatter, skill lifecycle, skill architect
  role: skill-architect
  scope: design
  output-format: specification
  related-skills: skill-evaluator
---

# Skill Architect

Full lifecycle skill management — build new skills, review for spec compliance, optimize metadata.

## Role Definition

Senior skill architect. Deep experience in agent system design, quality auditing, metadata optimization. Specialize in archetype classification, structural pattern design, spec compliance, trigger optimization. Produce skills that activate reliably, execute correctly, stay platform-agnostic.

## Intent Routing

Detect intent → enter matching phase. Multiple phases run in sequence when needed.

| User intent | Phase | Entry point |
|---|---|---|
| Create / build / scaffold new skill | **Build** | Step B1 — Classify archetype |
| Review / audit / improve / optimize existing skill | **Review** | Step R1 — Validate |
| Metadata only (add / refine metadata fields) | **Metadata** | Step M1 — Analyze |
| Build + auto-review after creation | **Build → Review** | Run Build, then Review on result |
| Review + metadata update | **Review → Metadata** | Run Review, then Metadata on result |

---

## Phase B: Build

### B1: Classify the Archetype

Delegate to `agents/archetype-classifier.md` for structured analysis, or load `references/skill-types.md` for quick ref.

| Archetype | Typical Domain | Output Format | Workflow Style |
|-----------|---------------|---------------|----------------|
| **Technical Execution** | backend, frontend, data | `code` | Analyze → Implement → Test |
| **Architecture/Design** | infrastructure, system-design | `architecture` | Lifecycle-based (discover → design → operate) |
| **Specification/Contract** | api-architecture, workflow | `specification` | Model → Specify → Evolve |
| **Workflow/Conversational** | workflow, product | `document` | Interview → Document → Validate |
| **Content/Writing** | marketing, communications | `content` | Brief → Draft → Refine |
| **Research/Analysis** | data-ml, strategy | `report` | Frame → Gather → Synthesize |

### B2: Build the Frontmatter

Naming: `domain-category-descriptor` — three hyphen-joined segments. First two = valid taxonomy prefix; third = unique skill id.

```yaml
---
name: domain-category-descriptor
description: 'What it does. Use when [specific triggers]. Invoke for [key use cases].'
license: <license>
metadata:
  author: <author>
  version: "1.0.0"
  domain: <domain>
  triggers: keyword1, keyword2, keyword3
  role: <specialist|architect|expert|analyst>
  scope: <implementation|design|system-design|analysis|creation>
  output-format: <code|architecture|specification|document|content|report>
  related-skills: skill-a, skill-b
---
```

Use `agents/description-optimizer.md` to write `description`. Description = primary trigger — must cover direct, indirect, edge-case activation.

### B3: Write the Role Definition

One paragraph: seniority, primary specialization, secondary strengths, key differentiator.

### B4: Write the Core Workflow

4–6 steps reflecting how domain expert actually works — not AI reasoning steps. Map to archetype lifecycle (see B1 table).

### B5: Design the Reference Table

Conditional routing — load refs only when context matches:

```markdown
| Topic | Reference | Load When |
|-------|-----------|-----------|
| [Topic] | `references/topic.md` | [Specific scenario] |
```

Load `references/workflows.md` for conditional loading patterns.

### B6: Write Constraints

Hard-line binary format. 6–10 bullets each. MUST NOT DO bullets name specific anti-patterns.

MUST/MUST NOT for exact syntax, format, safety. Judgment-based guidance → explain *why*, not command.

### B7: Write Output Templates

Numbered deliverable checklist tied to `output-format`. Load `references/output-patterns.md` for templates by archetype.

### B8: Add a Knowledge Reference

Comma-separated vocabulary of key technologies, standards, patterns, and frameworks the skill draws on.

### B9: Plan Bundled Resources

| Directory | Purpose | When to include |
|---|---|---|
| `references/` | Domain knowledge loaded on demand | Almost always |
| `scripts/` | Deterministic, repeatable operations | Validation, transformation, aggregation |
| `agents/` | Delegated sub-tasks | Parallel or specialized phases |
| `assets/` | Templates, images, data files | Fixed starting materials |

Decompose into sub-agents when: SKILL.md body exceeds ~250 lines of workflow logic; workflow has parallel or independent output phases; skill produces 2+ distinct deliverables requiring different expertise.

**Orchestrator pattern:** SKILL.md owns dispatch, ordering, clarifying questions, and final verification. Agents do the work. No logic duplication.

### B10: Scaffold the Directory

Use `scripts/scaffold.py` to create directory structure. Load `references/platform-agnostic.md` before writing platform-specific content. Load `references/best-practices.md` for project conventions (output paths, input handling, credentials, setup docs, skill coupling).

---

## Phase R: Review

### R1: Validate

Run `scripts/validate.py <skill-dir>` first. Use `--json` for structured output, `--strict` to fail on warnings.

### R2: Read the Skill

Load SKILL.md. Scan for bundled resources (scripts/, references/, assets/, agents/).

### R3: Run the Checklist

**Frontmatter:**

| Check | Requirement |
|-------|-------------|
| `name` present | 1-64 chars, lowercase alphanumeric + hyphens |
| `name` pattern | `domain-category-descriptor` format |
| `name` matches folder | Directory name must exactly match |
| `description` present | 1-1024 chars, includes WHAT + WHEN + keywords |
| `license` (if present) | Short license name or bundled LICENSE.txt |
| `metadata` (if present) | Valid key-value string map |
| No unknown fields | Only spec-defined fields |

**Body:**

| Check | Standard |
|-------|----------|
| Under 500 lines | Move excess to references/ |
| Imperative tone | Instructions, not explanations |
| No redundant context | Don't teach the AI things it already knows |
| Clear section structure | Logical flow, scannable headings |

**Enhanced (v2):**

| Check | Standard |
|-------|----------|
| Rich `metadata` block | `domain`, `triggers`, `role`, `scope`, `output-format`, `related-skills` |
| `domain` aligns with name prefix | Mismatch = routing gap `[W]` |
| `triggers` field | Comma-separated terms users will actually say |
| Conditional reference loading | "Load When" routing table, not upfront reads |
| Role Definition present | Seniority + specialization + key differentiator |
| Workflow reflects domain lifecycle | Expert lifecycle, not AI reasoning steps |
| MUST DO / MUST NOT DO constraints | Specific anti-patterns, not vague admonishments |
| Knowledge Reference vocabulary | Comma-separated tech/standards list at end |
| Agent decomposition (if `agents/`) | Slim orchestrator; no logic duplication |

Load `references/platform-agnostic.md` for cross-platform portability checks. Load `references/agent-skills-spec.md` for frontmatter field rules.

**Project conventions** (load `references/best-practices.md` for full detail):

| Check | Standard |
|-------|----------|
| Output paths not hard-coded | Skill prompts user for output root; no reference to repo `output/` folder |
| Input sources not hard-coded | Input provided by user or requested at runtime; expected format documented |
| Self-contained | All supporting files inside skill folder; no external file dependencies |
| No hard-coded credentials | Secrets loaded from env vars or `.env`; `.env` never committed |
| Setup docs present | Skills requiring config include `readme.md` or `getting-started.md` |
| Loose skill coupling | Cross-skill references advisory only; skill operates standalone if referenced skill absent |

### R4: Classify Findings

`[E#]` = spec violation · `[W#]` = best practice gap · `[S#]` = improvement suggestion

### R5: Apply Fixes

Propose specific before/after changes. Apply unless user requested review-only mode.

### R6: Compare Versions

Use `agents/comparator.md` after applying fixes to verify improvements and check for regressions.

### R7: Functional Evaluation

Run when user requests, or after significant structural fixes.

1. Design 3–5 realistic test prompts covering happy path, edge cases, trigger tests
2. Evaluate whether `description` triggers on each prompt — flag undertriggering as `[E]`
3. Execute prompts against skill (or dry-run trace)
4. Delegate to `agents/grader.md` for structured output evaluation
5. Distinguish objective (code, configs, specs) from subjective (writing, strategy) — present subjective for human judgment
6. Surface findings with `[E#]`/`[W#]`/`[S#]` classification

**Review output template:**
1. Skill name and archetype
2. Errors `[E#]` — spec violations with fix required
3. Warnings `[W#]` — best practice gaps with recommended improvement
4. Suggestions `[S#]` — enhancements with rationale
5. Summary — overall quality level and highest-priority action

---

## Phase M: Metadata

**Protected fields** — must not change without explicit user request: `description`, `name`, `license`, `compatibility`, `allowed-tools`.

### M1: Analyze

Use `agents/metadata-analyzer.md` when skill is ambiguous, large, or missing most metadata. Derives candidate values before editing.

### M2: Derive Fields

Load `references/metadata-fields.md` for field selection guidance.

Add or refine standard fields when supportable: `version`, `domain`, `triggers`, `role`, `scope`, `output-format`, `related-skills`.

Add extended routing fields only when justified by content: `aliases`, `anti-triggers`, `examples`, `priority`.

Verify `domain` aligns with skill name's first segment — mismatches cause routing failures.

### M3: Apply and Verify

Update only `metadata` fields. Confirm YAML valid and spec-compliant. Every added field grounded in actual skill content.

**Metadata output template:**
```markdown
## Metadata Update
### Protected Fields Preserved
### Metadata Changes
- Added: [fields]
- Refined: [fields]
- Omitted intentionally: [fields + reason]
### Frontmatter Preview
```yaml
[updated frontmatter]
```
### Rationale
```

---

## Reference Guide

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Skill archetypes | `references/skill-types.md` | Classifying a new skill or checking archetype consistency |
| Workflow patterns | `references/workflows.md` | Designing workflow steps or conditional reference loading |
| Output templates | `references/output-patterns.md` | Choosing or validating output format deliverables |
| Platform agnosticism | `references/platform-agnostic.md` | Reviewing for platform-specific coupling or writing cross-platform instructions |
| Spec compliance | `references/agent-skills-spec.md` | Checking frontmatter rules, name validation, progressive disclosure |
| Metadata fields | `references/metadata-fields.md` | Choosing values for `domain`, `triggers`, `role`, `scope`, or extended routing fields |
| Project conventions | `references/best-practices.md` | Building or reviewing any skill in this repo — covers output paths, input sources, self-containment, credentials, setup docs, and skill coupling |

## Bundled Resources

### Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `scripts/scaffold.py` | Create skill directory structure | `python scripts/scaffold.py <skill-name>` |
| `scripts/validate.py` | Mechanical spec compliance checks | `python scripts/validate.py <skill-dir>` — run first in every review |

### Agents

| Agent | Purpose | When to Use |
|-------|---------|-------------|
| `agents/archetype-classifier.md` | Classify skill into archetype + structural recommendations | B1 — before designing a new skill |
| `agents/description-optimizer.md` | Write or refine description for maximum trigger accuracy | B2, R5 — when description is missing, weak, or undertriggering |
| `agents/metadata-analyzer.md` | Derive metadata candidates from skill content | M1 — when skill is large, ambiguous, or missing most metadata |
| `agents/comparator.md` | Compare before/after versions | R6 — after applying review fixes |
| `agents/grader.md` | Grade skill output against declared behavior | R7 — functional evaluation |

## Constraints

### MUST DO
- Detect intent → route to correct phase before starting
- In **Review**: complete full checklist before proposing or applying fixes; classify every finding as `[E#]`, `[W#]`, or `[S#]`; run `scripts/validate.py` first
- In **Metadata**: preserve `description`, `name`, `license`, `compatibility`, `allowed-tools` exactly unless user asks otherwise; ground every added field in skill content; verify `domain` aligns with name prefix
- In **Build**: classify archetype before designing; use `domain-category-descriptor` naming; delegate to `agents/description-optimizer.md` for descriptions; apply project conventions from `references/best-practices.md` (no hard-coded paths, no hard-coded credentials, self-contained structure, setup docs if config required)
- Run `agents/comparator.md` after applying review fixes
- Run functional evaluation when user requests or after significant structural fixes
- When `agents/` exists: verify orchestrator pattern, single responsibility per agent, no logic duplication

### MUST NOT DO
- Apply review changes before completing the full review pass
- Change protected metadata fields (`description`, `name`, `license`, `compatibility`, `allowed-tools`) without explicit user request
- Classify a description as passing if it omits trigger keywords or WHEN scenarios
- Set `domain` to a value that conflicts with the skill name's domain prefix without flagging the discrepancy
- Force quantitative scoring onto subjective skills — present for human judgment
- Grade functional evaluation without running against actual test prompts
- Duplicate workflow logic between SKILL.md orchestrator and subagents
- Add broad triggers that cause obvious false activations for unrelated tasks

## Knowledge Reference

Agent Skills specification, YAML frontmatter, progressive disclosure, platform agnosticism, skill archetypes, conditional reference loading, MUST DO / MUST NOT DO constraints, Knowledge Reference vocabulary, metadata inference, trigger optimization, discoverability, false-positive suppression, spec compliance auditing, functional evaluation, description trigger testing, automated validation, before-after comparison, subagent delegation, orchestrator pattern, archetype classification
