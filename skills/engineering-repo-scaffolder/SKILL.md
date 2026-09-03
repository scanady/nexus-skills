---
name: engineering-repo-scaffolder
description: Engineering repository scaffolding and alignment skill for minimal starter shells, structure audits, and existing-project migrations. Use when a user wants a new repo baseline, a repository brought back to standard, or a reorganization plan for docs, automation, source, and agent assets.
license: MIT
metadata:
  version: "2.6.0"
  domain: engineering
  triggers: create starter shell, bootstrap project structure, apply project structure, align existing repository, audit repository layout, migrate repo to standard, reorganize repository, update scaffold artifacts
  role: repo-scaffolder
  scope: design
  output-format: plan
  related-skills: skill-architect
---

# Engineering Repo Scaffolder

Create or reorganize a project repository to match the structure defined in this skill. Favor a minimal starter shell and add additional artifacts only when an adoption trigger is met.

## Role Definition

Engineering repository scaffolder. Authoritative source for what belongs at the root, under `/docs`, under `/.github`, under `/.agents`, under `/src`, under `/infrastructure`, and in generated or temporary workspaces. Bias toward minimal scaffolding and progressive adoption to avoid clutter. This skill is self-contained and is the sole source of truth for all structure decisions.

---

## Design Principles

All structure decisions derive from these principles:

1. **Keep the repository root clean.** The root should contain only files and folders that contributors, GitHub, development tools, and runtime tooling need to find immediately.
2. **Keep documentation under `/docs`.** Standards, templates, product documentation, engineering documentation, operational documentation, decisions, generated references, and supporting material should live under `/docs`.
3. **Keep GitHub-native assets under `/.github`.** GitHub Copilot instructions, prompts, agents, skills, workflows, issue templates, and pull request templates should remain in `/.github`.
4. **Keep reusable agent assets under `/.agents`.** Agent assets that can be reused across projects should be separated from repository-specific GitHub assets.
5. **Colocate tests with source code.** Unit, component, service, API, and contract tests should live next to the code they validate.
6. **Keep generated, temporary, and system-created work out of the repo.** Use `/output` for generated local outputs and `/scratchpad` for temporary working material only when explicitly needed. Ignore virtual environments, caches, logs, and build artifacts.
7. **Place configuration where it is naturally consumed.** Environment examples and tool configuration should live in the root when appropriate. Application configuration should live near the code that consumes it.
8. **Adopt structure progressively.** Do not pre-create folders, docs, workflows, prompts, agents, skills, or templates until they are actually needed.

---

## Reference Structure

The full annotated tree and all path rules are in [`references/path-rules.json`](references/path-rules.json). This file is the single source of truth for both humans and scripts when verifying a path, annotation, or automation rule.

Inline annotations use `(starter)` for the minimal shell and `(add as needed)` for paths created only when the project is actively using them.

| Topic | Reference | Load When |
|---|---|---|
| Path rules | `references/path-rules.json` | Auditing, scaffolding, reorganizing, or validating repository paths |

---

## Starter Shell

The minimal committed baseline. Every new repository starts here and grows only when an adoption trigger is met.

```text
project-root/
├── README.md
├── {project-name}.code-workspace
├── .gitignore
├── .agents/
│   ├── .gitkeep
│   └── skills/
│       └── .gitkeep
├── .claude/
│   ├── CLAUDE.md                     # one-line shim: @../AGENTS.md
│   └── skills -> ../.agents/skills   # symlink; junction on Windows
├── .github/
│   └── .gitkeep
└── docs/
    ├── .gitkeep
    └── index.md
```

`AGENTS.md` at the repo root is the system of truth for agent-facing instructions (read natively by Codex, GitHub Copilot, and — via the `.claude/CLAUDE.md` shim — Claude Code). It is created by the Phase S3 shared-standards sync, not by the starter shell, because its shared-principles preamble comes from `ifoundry-development` and is refreshed by later syncs. Do not scaffold `.github/copilot-instructions.md` or a repo-root `CLAUDE.md`; the migration tool retires both, and the scaffolder no longer creates them.

### Starter templates

Starter file templates are individual files under [`assets/starter/`](assets/starter/), mirroring the paths created in a new repository. Copy those templates verbatim when creating the starter shell, replacing `{Project Name}` and `{project-name}` placeholders with the resolved project name.

### Optional templates

Optional templates live under [`assets/optional/`](assets/optional/) and are used only when an adoption trigger applies. Governance templates live under [`assets/optional/governance/`](assets/optional/governance/). Replace placeholders before writing the files. License templates are placeholders, not approved license grants.

### Claude Code integration

Claude Code discovers project skills under `.claude/skills/`. The repo standard keeps reusable skills under `.agents/skills/` so they stay portable across projects. To satisfy both without duplicating content, scaffold creates `.claude/skills` as a symlink to `../.agents/skills` (a directory junction on Windows to avoid the admin/developer-mode requirement of NTFS symbolic links). The link is created after the common skills install so it points at a populated target folder on first scaffold.

### Common skills

The scaffold installs common reusable skills from `https://github.com/scanady/nexus-skills.git` into `/.agents/skills/`. The configured skill list lives in [`assets/common-skills.txt`](assets/common-skills.txt):

- `agents-nexus-skills-manager`
- `skill-architect`
- `skill-evaluator`
- `engineering-github-repo-standards`
- `content-copy-clear-writing`

The source repository stores skills at either `skills/<name>/` or `.agents/skills/<name>/` — for example `agents-nexus-skills-manager` currently lives under `.agents/skills/`, while the others live under `skills/`. The scaffold scripts check both locations before reporting a skill as missing; any hand-install path must do the same. Report only genuinely missing skills and continue installing the rest.

### Shared standards

`.github/instructions/coding-principles.instructions.md`, `core-principles.instructions.md`, and the shared preamble section of `AGENTS.md` are cross-project standards, not repository-specific content — they are kept identical across every repo and synced from `ifoundry-development`, the same way common skills are synced from `nexus-skills`. Full detail: [`references/path-rules.json`](references/path-rules.json) → `shared_standards`.

Do not hand-author or hand-edit these. Edit the source in `ifoundry-development` and run the sync tool. Two implementations ship, and they produce equivalent output:

- Windows: [`scripts/sync-standards.ps1`](../../../scripts/sync-standards.ps1) (`sync-standards` from any directory when the alias is installed — see [`docs/engineering/sync-standards-guide.md`](../../../docs/engineering/sync-standards-guide.md)). Also scans the DevRoot to sync every repo at once.
- Linux/macOS: [`scripts/sync-standards.sh`](../../../scripts/sync-standards.sh). Scoped to a single target repo (`--target-repo <path>`); use the `.ps1` on Windows for the multi-repo sweep.

To bring a single repo up to standard, use `sync-standards.ps1 -TargetRepo <path>` or `sync-standards.sh --target-repo <path>`. The target does not have to be a git repo yet. Bringing an unmigrated repo (one that still carries `.github/copilot-instructions.md` or a repo-root `CLAUDE.md`) into the AGENTS.md shape is a one-time job for [`scripts/util-migrate-to-agents-md.sh`](../../../scripts/util-migrate-to-agents-md.sh); run it once per repo before the first sync.

`repo-scaffold` runs that single-repo sync itself as Phase S3, so a newly scaffolded repository already has both instructions files and an `AGENTS.md`. A repo with no `AGENTS.md` gets one carrying the shared preamble plus a placeholder **Repository specifics** section; fill that section in by hand afterward. Pass `-SkipSharedStandards` / `--skip-shared-standards` to opt out.

### Platform matrix

The two scaffold scripts are peers — pick the one that matches the host:

| Host | Scaffold script | Sync-standards it invokes |
|---|---|---|
| Windows (PowerShell / pwsh) | [`scripts/repo-scaffold.ps1`](scripts/repo-scaffold.ps1) | `scripts/sync-standards.ps1` from the cloned source |
| Linux / macOS (bash) | [`scripts/repo-scaffold.sh`](scripts/repo-scaffold.sh) | `scripts/sync-standards.sh` from the cloned source, falling back to `.ps1` via `pwsh` if only that is available |

The `.ps1` scaffold assumes NTFS-style paths and creates a directory junction for `.claude/skills`; the `.sh` scaffold uses POSIX paths and creates a symlink. Do not cross-invoke.

---

## Adoption Triggers

Add the next layer only when there is active work to place there.

| Add artifact | Add it when |
|---|---|
| `CONTRIBUTING.md`, `LICENSE`, `LICENSE_EE`, `LICENSE_NOTICE.md`, `SECURITY.md`, `CHANGELOG.md` | The project has governance, sharing, release, or contribution needs that require them. Use templates from `assets/optional/governance/` when creating them. |
| `.env.example` | The project has environment variables that contributors need documented. |
| `src/`, `bin/`, `scripts/`, `infrastructure/` | The repository contains code, executables, automation, or infrastructure definitions. |
| `.github/workflows/`, `CODEOWNERS`, `dependabot.yml`, `ISSUE_TEMPLATE/`, `pull_request_template.md` | The repository is ready to automate CI/CD, review ownership, dependency management, or contribution workflows. |
| `.github/prompts/`, `.github/agents/`, `.github/skills/`, repo-specific files under `.github/instructions/` | Repository-specific AI assets have been created and will be maintained. The two shared `*-principles.instructions.md` files are not covered by this trigger — every repo gets them from the standards sync (see Phase S3). |
| `.agents/` | Reusable cross-project agent assets exist and need a portable home. |
| `docs/design/`, `docs/product/`, `docs/engineering/`, `docs/standards/`, `docs/templates/`, `docs/decisions/`, `docs/operations/`, `docs/generated/`, `docs/references/` | That class of documentation is being actively authored. |
| `output/`, `scratchpad/` | The team explicitly wants committed placeholders for local generated or temporary work. |

---

## Location Rules

### Root directory

| Path | Purpose |
|---|---|
| `README.md` | Main project overview, getting started guidance, and navigation. |
| `CONTRIBUTING.md` | Contribution workflow, branch strategy, pull request expectations, and coding expectations. |
| `LICENSE` | Project license. |
| `LICENSE_EE` | Enterprise or commercial license terms, when the project uses a dual-license or enterprise-license model. |
| `LICENSE_NOTICE.md` | Human-readable summary of the repository's license structure and contact path. |
| `SECURITY.md` | Security policy, reporting process, and supported versions. |
| `CHANGELOG.md` | Notable changes by version or release. |
| `.gitignore` | Files and folders excluded from version control. |
| `AGENTS.md` | Repository-wide agent-facing instructions and system of truth. Read natively by Codex, GitHub Copilot, and — via `.claude/CLAUDE.md` — Claude Code. Carries the synced shared-principles preamble at the top (see **Shared standards** above); everything below the markers is repo-owned. |
| `{project-name}.code-workspace` | VS Code workspace file for opening the project root with shared workspace settings. |
| `.env.example` | Example environment variables. |
| Project manifests | `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `pom.xml`, etc. Live at root for single-module projects. For multi-module repos, place in the relevant module folder under `/src`. |
| Container files | `Dockerfile`, `docker-compose.yml` at root for simple single-service projects. For multi-service or complex deployments, place under `/infrastructure`. |
| `.github/` | GitHub-native workflows, supplemental Copilot instruction files, prompts, agents, skills, and templates. |
| `.agents/` | Reusable cross-project agent assets. |
| `.claude/` | Claude Code integration folder. Holds `CLAUDE.md` as a one-line `@../AGENTS.md` shim so Claude Code loads the repo-root `AGENTS.md`, plus `skills/` as a symlink to `.agents/skills/` (junction on Windows). Do not hand-author additional content here. |
| `docs/` | Documentation, standards, templates, decisions, references, and generated durable docs. |
| `src/` | Source code. |
| `bin/` | Runtime entry points, command-line tools, or executable wrappers. |
| `scripts/` | Development, build, setup, generation, and maintenance scripts. |
| `infrastructure/` | Infrastructure-as-code, container, and deployment infrastructure. |
| `output/` | Local generated output. |
| `scratchpad/` | Temporary working material. |

### Documentation (`/docs`)

| Path | Purpose |
|---|---|
| `/docs/index.md` | Documentation landing page and navigation map. |
| `/docs/glossary.md` | Shared terminology, acronyms, and definitions. |
| `/docs/design/` | Higher-level design principles and quality expectations. |
| `/docs/product/` | Product vision, roadmap, requirements, personas, use cases, and UX work. |
| `/docs/product/ux/` | UX prototypes, wireframes, and research notes. |
| `/docs/engineering/` | Architecture and technical documentation. |
| `/docs/standards/` | Canonical standards used by humans and agents. |
| `/docs/templates/` | Reusable templates for repeatable work products. |
| `/docs/decisions/` | Architecture Decision Records and other durable decision records. |
| `/docs/operations/` | Runbooks, deployment documentation, support model, and incident response. |
| `/docs/generated/` | Durable generated documentation, such as API references or schema documentation. |
| `/docs/references/` | Curated internal or upstream references for humans and agents. |

### Standards sub-folders (`/docs/standards`)

| Path | Purpose |
|---|---|
| `/docs/standards/engineering/` | Engineering standards for code, APIs, data, security, testing, and observability. |
| `/docs/standards/product/` | Product documentation, UX, and acceptance criteria standards. |
| `/docs/standards/ai/` | Agent, prompt, skill, tool-use, and context-management standards. |
| `/docs/standards/governance/` | Decision, risk, release-readiness, and governance standards. |

### GitHub assets (`/.github`)

| Path | Purpose |
|---|---|
| `/.github/CODEOWNERS` | Default ownership rules for repository paths and reviews. |
| `/.github/dependabot.yml` | Automated dependency update configuration. |
| `/.github/prompts/` | Repository-specific prompts used with GitHub Copilot or agent workflows. |
| `/.github/agents/` | Repository-specific agents. |
| `/.github/skills/` | Repository-specific skills that agents can use. |
| `/.github/instructions/` | Optional supplemental Copilot instruction files using the `.instructions.md` convention. |
| `/.github/workflows/` | GitHub Actions workflows. |
| `/.github/ISSUE_TEMPLATE/` | Issue templates. |
| `/.github/pull_request_template.md` | Pull request template. |

### Reusable agent assets (`/.agents`)

| Path | Purpose |
|---|---|
| `/.agents/.gitkeep` | Placeholder when `/.agents/` is intentionally scaffolded before it contains a reusable asset file. |
| `/.agents/agents/` | Reusable cross-project agent definitions. |
| `/.agents/agents/.gitkeep` | Placeholder when `/.agents/agents/` is intentionally scaffolded before it contains an agent file. |
| `/.agents/skills/` | Reusable cross-project agent skills. |
| `/.agents/skills/.gitkeep` | Placeholder when `/.agents/skills/` is intentionally scaffolded before it contains a skill folder. |

Do not create `/.agents/` until a reusable cross-project asset is being introduced or the user explicitly asks to scaffold reusable agent structure. Do not create `/.agents/prompts/`; repo-specific prompts belong in `/.github/prompts/`. Do not add `README.md` files to standard, well-understood folders such as `/.agents/`, `/.agents/agents/`, `/.agents/skills/`, `/.github/`, `/.github/prompts/`, `/.github/agents/`, `/.github/skills/`, `/.github/instructions/`, or `/.github/workflows/` just to explain the folder. If a standard repo-owned folder is intentionally scaffolded before it has real files, add `.gitkeep`.

### Asset type routing

| Asset type | Location |
|---|---|
| Repository-wide agent instructions (Codex, Copilot, Claude Code) | `/AGENTS.md` at the repo root; `.claude/CLAUDE.md` is a one-line `@../AGENTS.md` shim |
| Repository-specific supplemental instructions (path-scoped) | `/.github/instructions/{slug}.instructions.md` |
| Repository-specific prompts | `/.github/prompts/` |
| Repository-specific agents | `/.github/agents/` |
| Repository-specific skills | `/.github/skills/` |
| Reusable cross-project agents | `/.agents/agents/` |
| Reusable cross-project skills | `/.agents/skills/` |

### Configuration placement

Do not create a generic `/config` folder. Configuration lives where it is consumed.

| Configuration type | Correct location |
|---|---|
| Environment example | `/.env.example` at root |
| Local environment values | `/.env` at root |
| Tool-specific config (linters, formatters, test runners) | Root — for example `eslint.config.js`, `prettier.config.js`, `playwright.config.ts` |
| Application configuration | Near the consuming code in `/src` |
| Infrastructure configuration | `/infrastructure` |
| GitHub workflow configuration | `/.github/workflows` |

### Test placement

Tests are colocated with the code they validate. Do not create a top-level `/test` or `/tests` folder.

| Test type | Location |
|---|---|
| Unit tests | Next to the source file being tested. |
| Component tests | Next to the component. |
| Service tests | Next to the service. |
| API/controller tests | Next to the API/controller. |
| Contract tests | Near the provider or consumer module. |
| E2E tests | Under the relevant application area, such as `/src/frontend/e2e`. |
| Test fixtures | Near the domain or module that uses them. |
| Shared test utilities | Near the application or module that consumes them. |

### Generated and temporary work

Use these short purpose notes so AI agents understand the structure:

- `scratchpad/` is for local temporary work.
- `output/` is for local generated output.

When these folders need committed placeholders, create them with `.gitkeep` only. Do not create `output/README.md`, `scratchpad/README.md`, or other explanatory files for these folders.

```text
output/
└── .gitkeep

scratchpad/
└── .gitkeep
```

### Folder placeholders

Use `.gitkeep` for intentionally scaffolded, repo-owned folders that would otherwise be empty. Examples include `.agents/`, `.agents/agents/`, `.agents/skills/`, `.github/prompts/`, `.github/agents/`, `.github/skills/`, `.github/instructions/`, `.github/workflows/`, and optional `/docs` subtrees when the folder itself is part of the requested scaffold.

Do not use `README.md` as a folder placeholder. Do not add `.gitkeep` to folders that already contain real files unless the user explicitly wants a uniform placeholder convention.

### System-generated folders and files

System-generated folders and files are not project structure. Do not create, document, or commit placeholders for them.

Examples include:

- Virtual environments: `.venv/`, `venv/`
- Caches: `__pycache__/`, `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`, `.cache/`
- Logs: `logs/`, `*.log`
- Build and test outputs: `dist/`, `build/`, `coverage/`, `.next/`, `out/`, `target/`, `playwright-report/`, `test-results/`, `.nyc_output/`

When these paths appear, add or keep the matching `.gitignore` pattern. Do not add `README.md`, `.gitkeep`, or explanatory notes inside them.

---

## Asset File Conventions

### Agent files

Use the `.agent.md` suffix. Example: `.github/agents/solution-architect.agent.md`

Recommended sections: `Purpose`, `Responsibilities`, `Inputs`, `Outputs`, `Required Context`, `Standards to Follow`, `Tools and Skills`, `Workflow`, `Quality Bar`, `Constraints`, `Example Tasks`.

### Prompt files

Use the `.prompt.md` suffix. Example: `.github/prompts/create-adr.prompt.md`

Recommended sections: `Goal`, `When to Use`, `Inputs Needed`, `Instructions`, `Output Format`, `Review Criteria`.

### Skill files

Use the `.skill.md` suffix (or `SKILL.md` as the index inside a named folder). Example: `.github/skills/api-design.skill.md`

Recommended sections: `Capability`, `Use Cases`, `Required Inputs`, `Process`, `Standards`, `Expected Output`, `Validation Checklist`.

---

## Placement Decision Aid

When uncertain where something belongs, apply the 7-part separation model:

| What | Where |
|---|---|
| Human-facing project documentation | `/docs` |
| Canonical standards | `/docs/standards` |
| Reusable templates | `/docs/templates` |
| GitHub-specific AI assets (prompts, agents, skills, instructions, workflows) | `/.github` |
| Reusable cross-project AI assets | `/.agents` |
| Source code and colocated tests | `/src` |
| Generated and temporary local work | `/output` and `/scratchpad` |

---

## Intent Routing

Detect intent → enter matching phase.

| User intent | Phase | Entry point |
|---|---|---|
| Create new repo / scaffold starter shell / bootstrap project | **Scaffold** | Step S1 — Confirm target |
| Reorganize existing repo / restructure / migrate to standard | **Reorganize** | Step R1 — Inventory current repo |
| Audit existing repo against the standard (read-only) | **Audit** | Step A1 — Compare against standard |
| Decide which optional artifacts to add now | **Adopt** | Step D1 — Evaluate adoption triggers |

---

## Phase S: Scaffold a New Repository

Used when creating a new repository or initializing a clean directory.

### S1: Confirm target

1. Confirm the target directory with the user. Do not write files outside it.
2. Tell the user the scaffold runs in two parts: first the minimal starter shell (Phases S2–S3), then a walk-through of optional add-ons (Phase S4). Do not ask the user which optional artifacts they want up front — Phase S4 does that, and users generally will not know what to ask for.

### S2: Create the starter shell

Create exactly the starter shell defined in the **Starter Shell** section above. Populate each file from its corresponding template under [`assets/starter/`](assets/starter/), replacing `{Project Name}` and `{project-name}` placeholders with the resolved project name.

Existing scaffold artifacts are skipped by default. Use `--update-existing` / `-UpdateExisting` only when intentionally aligning an existing project to the current standard. Update mode replaces existing starter-template files and common skill folders with the current configured versions.

Rules:

- Use kebab-case for any new filenames or object identifiers not already specified in this skill.
- Do not create empty folders. Every intentionally scaffolded repo-owned folder must contain either a real artifact or `.gitkeep`.
- Do not add `README.md` files as placeholders or explanatory notes inside standard, well-understood folders such as `/.github/` or `/.agents/` and their subfolders.
- Do not create `CONTRIBUTING.md`, `LICENSE`, `LICENSE_EE`, `LICENSE_NOTICE.md`, `SECURITY.md`, `CHANGELOG.md`, `.env.example`, `src/`, `bin/`, `scripts/`, `infrastructure/`, `output/`, `scratchpad/`, or any `/docs` sub-folder (`docs/design/`, `docs/product/`, etc.) unless the user explicitly opts in or an adoption trigger is met (see Phase D). The `.agents/`, `.github/`, and `docs/` starter folders are part of the starter shell.
- Install the configured common skills into `/.agents/skills/` unless the user explicitly opts out or the environment cannot reach the source repository.

### S3: Apply shared standards

Every repo carries the shared standards unconditionally — they are not an adoption trigger. `repo-scaffold` applies them automatically after the starter shell; if you are scaffolding by hand, run the sync tool that matches the host — `sync-standards.ps1 -TargetRepo <path>` on Windows, `sync-standards.sh --target-repo <path>` on Linux/macOS — instead of authoring these files. That adds `.github/instructions/coding-principles.instructions.md` and `core-principles.instructions.md`, and creates `AGENTS.md` with the shared-principles preamble block at the top and a placeholder **Repository specifics** section below it.

Run it after the starter shell exists, not before: the starter shell writes the `.claude/CLAUDE.md` shim so that once `AGENTS.md` lands, Claude Code loads it via that shim. Fill in the **Repository specifics** section by hand with what is actually specific to this repository.

### S4: Offer progressive add-ons

This step is NOT optional and NOT skippable — run it every time you scaffold a repo, even if the user did not ask about optional artifacts. Users generally do not know what optional artifacts exist; the whole point of this step is to surface them.

After the starter shell exists:

1. Briefly tell the user you are going to walk them through the optional add-ons the scaffold supports.
2. For each row in the **Adoption Triggers** table, ask whether it applies to their project. Give a short plain-English description of what the artifact is and why they might want it — do not just paste the trigger text.
3. Ask about triggers one at a time, or in small logically-grouped batches (for example, "governance files" as one group; "CI and automation" as another). Do not dump the whole table into a single question — users will skim past it. Use a structured question tool (`AskUserQuestion` or the host's equivalent) so choices are captured cleanly.
4. For each trigger the user confirms, create only the specific paths called for, then move on. Do not bulk-create entire subtrees.

When creating governance files, use the matching template from `assets/optional/governance/` and replace placeholders. Do not create license files unless the user confirms the license model or asks for placeholder files to complete later.

### S5: Summarize

Report exactly which files and folders were created and which were intentionally skipped.

---

## Phase R: Reorganize an Existing Repository

Used when the repository already has content that needs to be aligned with the standard.

### R1: Inventory current repo

1. List the top-level files and folders.
2. List the contents of `/.github`, `/.agents`, `/docs`, `/src`, `/infrastructure`, `/scripts`, `/bin`, `/output`, `/scratchpad` if they exist.
3. Identify any non-standard top-level paths (for example, `/config`, `/tools`, `/lib`, `/test`, `/tests`, `/assets`, `/build`).

### R2: Compare against the standard

Build a table of findings with these columns:

| Current path | Standard location | Status | Recommended action |
|---|---|---|---|

Status values: `correct`, `misplaced`, `non-standard`, `missing required`, `missing optional`, `duplicate`.

Apply these mappings:

- `/config` → move tool configs to root, application config near consuming code in `/src`, infrastructure config to `/infrastructure`. Delete `/config` after migration.
- `/test` or `/tests` (top level) → colocate tests with code under `/src` per the **Test placement** rules above.
- `/lib`, `/tools` → reclassify to `/src/common`, `/scripts`, or `/bin` based on purpose.
- `/assets` → if documentation assets, move under `/docs`; if runtime assets, place near consuming code in `/src`.
- `/build`, `/dist`, `/out`, `/target` (top level) → build outputs; add patterns to `.gitignore` under `# Build outputs`. Do not commit build outputs. Do not add README files, `.gitkeep`, or explanatory notes inside them. If a specific artifact must be committed (for example, a pre-built binary for a release), move it under `/output` and document the exception.
- `.venv/`, `venv/`, `__pycache__/`, cache folders, `logs/`, test reports, and coverage folders → system-generated paths; add patterns to `.gitignore`, do not commit them, and do not add README files or placeholders inside them.
- `/.vscode`, `/.editorconfig` → not part of this standard; do not require, do not block.
- Existing `/.github/custom-instructions.md` → replace with `/.github/instructions/<slug>.instructions.md` files.
- Existing `/.github/copilot-instructions.md` or repo-root `/CLAUDE.md` → migrate to the AGENTS.md shape with `scripts/util-migrate-to-agents-md.sh` in the `ifoundry-development` repo. It preserves each file's content verbatim inside `AGENTS.md`, writes `.claude/CLAUDE.md` as a `@../AGENTS.md` shim, and deletes the source files. Do not scaffold either file again.
- Existing `/infra` → rename to `/infrastructure`.
- Existing `/.agents/prompts/` → not part of this standard; relocate prompts to `/.github/prompts/` (repo-specific) or remove.

### R3: Produce a reorganization plan

Output an ordered plan with reversible, low-risk steps first:

1. **Doc moves** — relocate documentation into `/docs` subtrees.
2. **Config relocations** — move configuration per the **Configuration placement** rules above.
3. **Source relocations** — move code into `/src/{frontend,backend,common}` and colocate tests per the **Test placement** rules above.
4. **Infrastructure renames** — rename `/infra` to `/infrastructure`, etc.
5. **GitHub asset moves** — consolidate prompts, agents, skills, instructions, workflows under `/.github`.
6. **Cleanup** — delete empty legacy folders only after their contents have moved.

Require explicit user approval before:

- Deleting any file or folder.
- Force-pushing, amending published commits, or rewriting Git history.
- Bulk-renaming files that may break external links or CI.

### R4: Execute approved steps

Execute only the steps the user approves. Prefer one logical change per commit. After each step, restate what changed and what remains.

### R5: Verify

After execution, rerun the inventory from R1 and report remaining gaps. List which adoption triggers are now met and which optional artifacts can be added next (see Phase D).

---

## Phase A: Audit (Read-Only)

Used when the user wants a structural review without changes.

### A1: Compare against the standard

Run Steps R1 and R2 only. Do not write files. Do not propose deletions.

### A2: Report

Produce:

1. A summary table of correct, misplaced, non-standard, and missing paths.
2. A prioritized list of recommended actions, marked `safe`, `needs-approval`, or `discussion-required`.
3. For each finding, cite the relevant section of this skill (Location Rules, Adoption Triggers, etc.).

---

## Phase D: Adoption Decisions

Used when the user wants to decide which optional artifacts to add now.

### D1: Evaluate adoption triggers

Walk the **Adoption Triggers** table above. For each row, ask whether the trigger is currently met. Record the answer.

### D2: Recommend additions

For each trigger that is met, recommend creating only the specific paths called for, with the minimum viable content:

If an optional artifact already exists, skip it by default. Replace existing optional artifacts only when the user explicitly asks to update existing files to the current template or standard.

- `CONTRIBUTING.md` — short contribution workflow and PR expectations.
- `LICENSE` — chosen SPDX license text.
- `LICENSE_EE` — enterprise or commercial license terms for dual-license or enterprise-license models.
- `LICENSE_NOTICE.md` — human-readable summary of the repository's license structure and contact path.
- `SECURITY.md` — disclosure process and supported versions.
- `CHANGELOG.md` — Keep a Changelog format header and an `Unreleased` section.
- `.env.example` — variable names with empty values and comments.
- `src/`, `bin/`, `scripts/`, `infrastructure/` — create only the subfolders that have actual content arriving in the same change.
- `.github/workflows/` — start with a single CI workflow rather than the full `ci.yml`, `lint.yml`, `test.yml`, `release.yml` set.
- `.github/{prompts,agents,skills,instructions}/` — create only when the first asset of that kind is being added.
- `.agents/` — create only when a reusable cross-project asset is being introduced or the user explicitly asks to scaffold reusable agent structure. Create `agents/` and `skills/` sub-folders only when assets of that type exist or the user asks for the scaffold. Add `.gitkeep` to intentionally scaffolded empty `.agents` folders. Do not create `.agents/prompts/`. Do not add README files as folder placeholders.
- `output/` and `scratchpad/` — create each with a committed `.gitkeep` only. Do not add README files or other documentation notes for these folders.
- `docs/standards/` — create with four sub-folders: `engineering/`, `product/`, `ai/`, `governance/`. Add files inside each sub-folder only when that standard is being authored.
- `docs/templates/` — create with a `README.md` and add template files from this list only as they are authored: `adr-template.md`, `product-spec-template.md`, `api-spec-template.md`, `security-review-template.md`, `release-readiness-template.md`, `runbook-template.md`.
- Any other `/docs/<subtree>/` — create only when at least one document in that subtree is being authored in the same change.

### D3: Confirm and stop

Confirm the proposed additions with the user, create them, and stop. Do not chain into further additions in the same turn.

---

## Constraints

### MUST DO

- This skill is the authoritative source of structure rules. Do not invent additional paths or conventions not defined here.
- Prefer kebab-case for new filenames and object identifiers, unless this skill specifies otherwise (for example, `CONTRIBUTING.md`, `CODEOWNERS`, `SKILL.md`).
- Limit each turn to one phase unless the user explicitly chains phases.

### MUST NOT DO

- Never delete files or folders without explicit user approval.
- Never rewrite Git history, force push, or bypass safety checks.
- Do not pre-create empty folders. Every created folder must have at least one committed file.
- Never create `.editorconfig` or `.vscode/`. They are not part of this standard.
- Never create `/.agents/prompts/`. Prompts belong in `/.github/prompts/`.

## Quality Bar

- Every committed top-level path in the resulting repository appears in the Reference Structure or in an approved exception confirmed with the user.
- The starter shell is reproducible from a clean directory by following Phase S.
- Reorganizations preserve file history where possible (`git mv` rather than copy-delete).
- All recommendations cite a specific section of this skill.

## Example Tasks

- "Scaffold a new repo." → Phase S.
- "My repo has /infra, /config, and /tests at the top level. Clean it up." → Phase R.
- "Audit this repository structure and tell me what is off." → Phase A.
- "We are adding our first GitHub Actions workflow — what should I create?" → Phase D, single trigger.
- "Bootstrap a starter shell, then add CONTRIBUTING.md and a CI workflow." → Phase S → Phase D.

## Knowledge Reference

Repository structure standards, starter shell scaffolding, existing repository alignment, AGENTS.md system of truth, .claude/CLAUDE.md shim, GitHub Copilot instructions files, reusable agent skills, `.agents` asset routing, `.github` asset routing, documentation trees, colocated tests, generated output handling, `.gitkeep` placeholders, `.gitignore` conventions, VS Code workspace files, governance templates, structural audit reports, shared engineering standards, coding-principles.instructions.md, core-principles.instructions.md, sync-standards, util-migrate-to-agents-md
