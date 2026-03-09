---
name: skill-builder
description: 'Design and generate optimized Agent Skills tailored to the skill''s archetype. Use when asked to "create a skill", "build a skill", "make a new skill", "scaffold a skill", "add a skill", or when building specialized agent capabilities. Classifies the target use case into a skill archetype (technical execution, architecture, specification, workflow/conversational, content/writing, research/analysis) and applies archetype-specific structural patterns for frontmatter, reference loading, constraints, and output templates.'
license: MIT
metadata:
  version: "2.0.0"
  domain: meta
  role: skill-architect
  scope: design
  output-format: specification
---

# Skill Builder
A meta-skill for creating high-quality, archetype-optimized Agent Skills. Skills are not one-size-fits-all — a code generation skill is structurally different from a requirements-gathering skill, which differs from a content-writing skill.

## Core Principles

**Classify before you design.** Archetype determines workflow structure, reference loading strategy, constraint format, and output templates. Read [references/skill-types.md](references/skill-types.md) to identify the right archetype.

**Conditional reference loading over upfront reads.** Use a "Load When" routing table so the skill only loads references relevant to the current context. See [references/workflows.md](references/workflows.md).

**Conciseness.** Only include context the agent doesn't already have. A skill that instructs the agent on things it already knows wastes tokens and reduces focus.

**Platform agnosticism.** Write platform-neutral instructions in SKILL.md body. Isolate platform details in `references/`. See [references/platform-agnostic.md](references/platform-agnostic.md).

**Generalize, don't overfit.** Skills will be used across many prompts, not just the examples used during development. Prefer general principles and reasoning over narrow, example-specific constraints. If a constraint only makes sense for one test case, it's too specific.

**Principle of Lack of Surprise.** A skill's contents should not surprise the user in their intent if described. Skills must not contain exploit code, data exfiltration patterns, or content that could compromise system security. The user who installs the skill should be able to predict its behavior from its description.

## Skill Creation Workflow

This workflow is not strictly sequential — enter at whatever step matches the user's current state. If the user already has a draft skill, jump to the relevant step. If the conversation already contains a workflow the user wants to capture ("turn this into a skill"), extract the tools used, sequence of steps, corrections made, and input/output formats from the conversation history before starting.

### Step 1: Classify the Archetype

Identify which archetype fits the requested skill. Delegate to the archetype classifier agent (`agents/archetype-classifier.md`) for structured analysis, or read [references/skill-types.md](references/skill-types.md) for quick reference.

| Archetype | Typical Domain | Output Format | Workflow Style |
|-----------|---------------|---------------|----------------|
| **Technical Execution** | backend, frontend, data | `code` | Analyze → Implement → Test |
| **Architecture/Design** | infrastructure, system-design | `architecture` | Lifecycle-based (discover → design → operate) |
| **Specification/Contract** | api-architecture, workflow | `specification` | Model → Specify → Evolve |
| **Workflow/Conversational** | workflow, product | `document` | Interview → Document → Validate |
| **Content/Writing** | marketing, communications | `content` | Brief → Draft → Refine |
| **Research/Analysis** | data-ml, strategy | `report` | Frame → Gather → Synthesize |

### Step 2: Build the Frontmatter

Construct rich frontmatter using the `metadata` block. This enables discoverability and explicit skill chaining:

```yaml
---
name: skill-name
description: 'What it does. Use when [specific triggers]. Invoke for [key use cases].'
license: <license>
metadata:
  author: <author>
  version: "1.0.0"
  domain: <domain>           # backend | infrastructure | data-ml | marketing | workflow | etc.
  triggers: keyword1, keyword2, keyword3   # space for primary activation keywords
  role: <specialist|architect|expert|analyst>
  scope: <implementation|design|system-design|analysis|creation>
  output-format: <code|architecture|specification|document|content|report>
  related-skills: skill-a, skill-b   # skills that naturally precede or follow
---
```

`triggers` is the primary automatic activation mechanism — use the specific terms users will say.
`related-skills` enables explicit skill chaining across a domain.

**Combat undertriggering.** Agents tend to under-activate skills — failing to use them even when relevant. Use the description optimizer agent (`agents/description-optimizer.md`) to write descriptions that cover direct, indirect, and edge-case activation scenarios. At minimum, write descriptions that are slightly "pushy": explicitly name edge cases where the skill should activate even if the user hasn't used the exact skill name. Instead of just "Build dashboards", write "Build dashboards. Use whenever the user mentions dashboards, data visualization, metrics display, or wants to present any kind of data visually, even if they don't explicitly ask for a 'dashboard'." 

### Step 3: Write the Role Definition

One paragraph. Include: seniority level (years of experience), primary specialization, secondary strengths, and key differentiator — what makes this expert valuable that a generalist wouldn't provide.

```markdown
## Role Definition

You are a senior [title] with [N]+ years of experience [doing X]. You specialize in [primary area],
[secondary area], and [tertiary area]. You [key differentiator — concrete statement of what this expert
produces that others don't].
```

### Step 4: Write the Core Workflow

The workflow must reflect how an expert in this domain actually works — not how an AI reasons through a task. Map to the domain's natural lifecycle. Steps should be 4–6, outcome-focused, not tool-focused.

- **Technical Execution**: Analyze requirements → Design schemas → Implement → Secure → Test
- **Architecture/Design**: Discovery → Design → Security/Resilience → Cost/Scale → Deploy → Operate
- **Specification/Contract**: Analyze domain → Model resources → Design contract → Plan evolution → Document
- **Workflow/Conversational**: Discover → Interview → Document → Validate → Plan
- **Content/Writing**: Understand brief → Contextualize audience → Draft → Refine → Finalize
- **Research/Analysis**: Frame question → Gather → Analyze → Synthesize → Recommend

### Step 5: Design the Reference Table

Use the "Load When" conditional routing pattern. Each row is a topic that loads only when the context matches:

```markdown
## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| [Topic] | `references/topic.md` | [Specific scenario that triggers this load] |
```

Plan reference files around sub-topics that arise situationally. 4–6 focused reference files is the right range for most skills.

For large reference files (>300 lines), include a table of contents at the top so the agent can navigate directly to the relevant section without reading the entire file.

### Step 6: Write Constraints

Hard-line binary format — no conditional logic. Both sections should have 6–10 bullets. MUST NOT DO bullets must name a specific anti-pattern precisely enough to be actionable (not "don't skip security").

**When to use commands vs. reasoning:** Use hard MUST/MUST NOT rules for exact syntax, format, or safety requirements where there is one correct answer. For judgment-based guidance (priorities, tradeoffs, style preferences), explain *why* something matters instead — reasoning helps the agent generalize to novel situations better than commands do.

```markdown
## Constraints

### MUST DO
- [Specific, actionable requirement]

### MUST NOT DO
- [Specific anti-pattern with enough detail to be unambiguous]
```

### Step 7: Write Output Templates

Output templates are numbered deliverable checklists tied to the skill's `output-format`:

| output-format | Typical deliverables |
|---|---|
| `code` | Schema/model file · Implementation file · Config or test file · Rationale for key decisions |
| `architecture` | Architecture diagram + service topology · Component selection rationale · Security model · Cost/scale strategy · Deployment approach |
| `specification` | Resource/entity model · Full formal specification · Auth model · Versioning/deprecation strategy · Error catalog |
| `document` | Overview + user value · Formal requirements · Acceptance criteria · Error handling table · Implementation checklist · Save path |
| `content` | Final copy (ready to use) · Usage notes (channel, tone, format) · Optional: 3–5 variations |
| `report` | Executive summary · Key findings with supporting data · Trade-off analysis · Ranked recommendations · Assumptions/limitations |

### Step 8: Add a Knowledge Reference

End the skill with a comma-separated vocabulary of the key technologies, standards, patterns, and frameworks the skill draws on. This grounds the role in real tools, not abstract expertise:

```markdown
## Knowledge Reference
technology1, technology2, pattern1, standard1, framework1, ...
```

### Step 9: Plan Bundled Resources

Decide which resource directories the skill needs beyond `references/`:

| Directory | Purpose | When to include |
|---|---|---|
| `references/` | Domain knowledge loaded into context on demand | Almost always — conditional reference loading is a core pattern |
| `scripts/` | Executable code for deterministic, repeatable operations | When the skill involves validation, data transformation, aggregation, or any operation where consistency matters more than flexibility |
| `agents/` | Subagent prompt files (markdown) for delegated tasks | When the skill's workflow decomposes into parallel or specialized sub-tasks — common in Workflow/Conversational and Research/Analysis archetypes |
| `assets/` | Templates, images, data files used in output | When the skill produces artifacts from fixed starting materials |

**Script design principle:** Scripts handle what must be deterministic (validation against a schema, data aggregation, file packaging). The SKILL.md body handles what requires judgment (workflow decisions, user interaction, content generation). Don't put judgment in scripts or determinism in prose.

**Subagent design principle:** Each `agents/*.md` file defines a focused role, its inputs, its evaluation process, and its output format. The SKILL.md workflow orchestrates when and how to spawn each subagent. This pattern is useful when a single skill needs multiple specialized perspectives (e.g., grading + analysis + comparison) or when tasks can run in parallel.

**When to decompose into sub-agents.** Not every skill needs agents. Decompose when:
- The SKILL.md body exceeds ~250 lines of workflow logic (not counting frontmatter, constraints, or templates)
- The workflow has a clear separation between data-gathering and multiple independent output-generation phases
- The skill produces 2+ distinct deliverables that could be authored independently from the same source data
- Different phases require fundamentally different expertise (e.g., codebase analysis vs. executive writing)

Do NOT decompose when the skill is a single linear workflow under 200 lines, or when the "agents" would just be sections of the same document with artificial boundaries.

**The orchestrator pattern.** When decomposing, restructure SKILL.md as a slim orchestrator:
1. **SKILL.md** owns: execution logic, agent dispatch sequence, dependency ordering, clarifying questions, final quality verification, and delivery
2. **Data-gathering agent(s)** run first — they explore, research, or interview and produce a structured intermediate model
3. **Writer/builder agent(s)** consume that model — they are independent of each other and can run in any order
4. SKILL.md should NOT duplicate logic that lives in an agent. The orchestrator dispatches and verifies; agents do the work.

**Agent composition patterns:**

| Pattern | Structure | When to use |
|---------|-----------|-------------|
| Sequential pipeline | A → B → C (each depends on the previous) | Rare — usually only the first agent is sequential; prefer fan-out after data gathering |
| Fan-out after shared input | A → (B, C, D) in parallel | Most common — one discovery/research agent feeds multiple independent writers |
| Peer review | A produces, B evaluates | Quality-critical skills — the skill-reviewer itself uses this pattern (grader + comparator) |

### Step 10: Scaffold the Directory

Use `scripts/scaffold.py` to generate the directory structure and starter files:

```bash
python scripts/scaffold.py <skill-name> --archetype <type> [--with-agents] [--with-scripts]
```

Or create manually:

```
skill-name/
├── SKILL.md
├── references/
│   ├── [topic-a].md
│   └── [topic-b].md
├── scripts/              # only if needed
│   └── [operation].py
└── agents/               # only if needed
    └── [role].md
```

Folder name must match `name` field exactly (lowercase with hyphens). Only include directories that contain files — delete empty directories.

## After Building

A generated skill should be evaluated before it's considered done. Use the **skill-reviewer** to run structural review (spec compliance, best practices) and functional evaluation (test with realistic prompts, verify description triggering, check output quality). Iterate based on findings.

## Bundled Resources

### Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `scripts/scaffold.py` | Generate skill directory structure with archetype-specific boilerplate | `python scripts/scaffold.py <name> --archetype <type>` — creates SKILL.md, references/, and optional agents/ and scripts/ directories with starter content |

### Agents

| Agent | Purpose | When to Use |
|-------|---------|-------------|
| `agents/archetype-classifier.md` | Classify a skill request into one of 6 archetypes with structural recommendations | Step 1 — when the archetype isn't obvious or when you want a structured justification for the classification |
| `agents/description-optimizer.md` | Write and refine descriptions for maximum triggering accuracy | Step 2 — after drafting the description, or when refining based on trigger failures |

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Skill Archetypes | `references/skill-types.md` | Classifying the skill type or designing archetype-specific sections |
| Platform Agnosticism | `references/platform-agnostic.md` | Reviewing SKILL.md body for platform-specific language |
| Workflow Patterns | `references/workflows.md` | Designing sequential or conditional workflows |
| Output Patterns | `references/output-patterns.md` | Designing output templates or adding examples |
| Spec Reference | `references/agent-skills-spec.md` | Frontmatter field rules, naming validation, progressive disclosure |

## Constraints

### MUST DO
- Classify the skill archetype before designing any section — the archetype drives every other decision
- Use rich frontmatter with a `metadata` block including domain, triggers, role, scope, output-format, and related-skills
- Write descriptions that combat undertriggering — explicitly name edge-case activation scenarios
- Use the "Load When" conditional reference table — not the "read all references upfront" pattern
- Write the workflow to match the archetype's natural domain lifecycle
- Make MUST NOT DO bullets specific — name concrete anti-patterns, not vague warnings
- Use reasoning ("why this matters") for judgment-based guidance; reserve hard commands for exact syntax/format/safety rules
- Delegate archetype classification to `agents/archetype-classifier.md` when the archetype isn't immediately obvious
- Use `agents/description-optimizer.md` to write or refine descriptions, especially when addressing undertriggering
- Evaluate whether the skill should decompose into sub-agents using the heuristics in Step 9 — especially when the skill produces multiple distinct deliverables or exceeds ~250 lines of workflow logic
- When decomposing, restructure SKILL.md as a slim orchestrator that dispatches to agents and verifies output — not a monolith that also happens to have agents
- Use `scripts/scaffold.py` to generate directory structure instead of manual creation
- Tie output templates explicitly to the `output-format` field
- Include a Knowledge Reference vocabulary section at the end
- Keep SKILL.md under 500 lines

### MUST NOT DO
- Design any section before identifying the skill archetype
- Use "read ALL reference files before proceeding" upfront loading
- Write workflow steps that describe AI reasoning ("Understand → Generate") instead of expert domain process
- Write vague MUST NOT DO items ("don't skip security", "avoid bad patterns")
- Omit the `related-skills` metadata field
- Create a single monolithic reference file when multiple focused files would serve context better
- Add generic best-practice advice the agent already knows
- Conflate archetypes — a content skill should not have an implementation workflow; an architecture skill should not produce copy
- Overfit constraints to specific test examples — if a constraint only applies to one scenario, it's too narrow
- Include content that would surprise the user if they read the skill — no hidden behaviors, exploit code, or data exfiltration
- Duplicate workflow logic in both SKILL.md and an agent — the orchestrator dispatches, agents execute
- Create agents for skills under 200 lines of workflow logic where a single linear flow suffices
- Add README, CHANGELOG, or other auxiliary documentation to the skill directory

## Validation Checklist

Before finalizing the generated skill, verify:

- [ ] Archetype identified and all sections reflect it consistently
- [ ] `name` matches folder name, lowercase with hyphens only
- [ ] `description` includes WHAT the skill does, WHEN to use it, and trigger keywords
- [ ] `metadata` block includes domain, triggers, role, scope, output-format, related-skills
- [ ] Role Definition is one paragraph with seniority, specialization, and key differentiator
- [ ] Core Workflow has 4–6 steps that match the archetype's domain lifecycle (not AI reasoning steps)
- [ ] Reference table uses "Load When" column with specific routing conditions
- [ ] Constraints has MUST DO and MUST NOT DO with 6+ bullets each
- [ ] MUST NOT DO bullets name specific anti-patterns
- [ ] Constraints use reasoning for judgment calls and hard commands for exact requirements
- [ ] Output Templates match the `output-format` field
- [ ] Knowledge Reference vocabulary section present
- [ ] SKILL.md is under 500 lines
- [ ] No platform-specific tool names in SKILL.md body
- [ ] Description combats undertriggering — names edge-case activation scenarios
- [ ] Constraints generalize beyond test examples — no overfitted rules
- [ ] Skill contents would not surprise the user if described (Principle of Lack of Surprise)
- [ ] Scripts (if any) handle deterministic operations only — no judgment or workflow logic
- [ ] Subagent prompts (if any) define focused roles with clear inputs, process, and output format
- [ ] If agents exist: SKILL.md is a slim orchestrator (dispatch + verify), not a monolith that duplicates agent logic
- [ ] If agents exist: dependency ordering is explicit (which agents must complete before others can start)
- [ ] If agents exist: each agent's output format is defined clearly enough to be consumed by downstream agents or by SKILL.md
- [ ] Decomposition decision is justified — skill either warrants agents (250+ lines, multiple deliverables) or correctly stays inline
- [ ] No empty directories in the scaffold
