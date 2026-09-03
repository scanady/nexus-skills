# AGENTS.md Anatomy

Standard structure for a repository's `AGENTS.md` — the system-of-truth agent-instructions file.

## The Rule of the Marker Block

The `<!-- shared-principles:start -->` / `<!-- shared-principles:end -->` block is owned by the sync tool (`scripts/sync-standards.sh` in `ifoundry-development`). It carries the pointer to the shared `.github/instructions/coding-principles.instructions.md` and `core-principles.instructions.md` files. **Never edit its interior.** Keep it byte-identical to what the sync tool produced.

## Standard Section Order

```markdown
# <repo-name> Agent Guide

<!-- shared-principles:start -->
[preamble — do not touch]
<!-- shared-principles:end -->

## Repository specifics
<elevator pitch. What is this repo, who uses it, what makes it unusual.>

## Project structure
- `dir/` — purpose
- `dir/` — purpose

## Workflows
<commands, run scripts, common tasks, server-management notes>

## Conventions
<repo-specific rules that don't warrant a per-file .instructions.md>

## Hard-won facts
<incident-derived warnings. Include dates when the source had them.>

## Resources
<MCP servers, dashboards, tools, integrations>

## Per-file rules
Pattern-scoped rules live in [.github/instructions/](.github/instructions/). See:
- `core-principles.instructions.md`, `coding-principles.instructions.md` (shared, synced)
- `<repo-specific>.instructions.md` (project-owned)
```

## Section Guidance

### `# <repo-name> Agent Guide`

- H1, at the very top.
- Repo basename is the safe default (`# nexus-skills Agent Guide`). If the repo has a proper display name (e.g., `# iFoundry Agent Guide`), use that.

### `<!-- shared-principles:… -->` block

- Immediately after the H1.
- Preserve byte-identical to the sync-tool output.

### `## Repository specifics`

- The first thing an agent should read after the shared block.
- Two to five short paragraphs (or a short paragraph + a small table).
- Answer: what is this repo, who uses it, what makes it different from a generic project of its type?
- Do not restate what the README already covers. Do link to the README when useful.

### `## Project structure`

- Bulleted list of top-level directories with one-line purpose statements.
- Include only directories an agent needs to know about — skip `node_modules/`, `dist/`, `.git/`, and other common noise.
- Match what actually exists. Verify against `ls` before writing.

### `## Workflows`

- Named commands the agent will run: build, test, lint, dev-server, deploy.
- Include the exact command, and any flag that matters ("prefer `-Background` on Windows to avoid blocking terminal").
- Group by task, not by tool. "Frontend server" beats "PowerShell scripts".
- Mention any wrapper scripts (`./scripts/frontend-server.sh`) instead of the raw commands they wrap.

### `## Conventions`

- Rules that don't naturally live in a per-file `.instructions.md`.
- Cross-cutting concerns: PR description conventions, branching, commit message style, sensitivity classifications, taxonomy rules.
- Anything that answers "how do we do this here" without being tied to a file pattern.

### `## Hard-won facts` (optional)

- Warnings derived from a specific incident. Format: state the wrong action, then the correct one, then (when known) the date the lesson was learned.
- Keeps the file honest about where it came from and prevents re-learning.

### `## Resources` (optional)

- MCP servers with their URL and what they're for.
- Dashboards, especially oncall-visible ones.
- External tools the agent should reach for.

### `## Per-file rules` (optional pointer)

- One paragraph pointing at `.github/instructions/`.
- List repo-specific `.instructions.md` files by name and one-line purpose.

## What Does Not Belong in AGENTS.md

- **Rules already in `.github/instructions/*.instructions.md`.** Reference them; don't repeat.
- **Coding principles.** They live in the synced `coding-principles.instructions.md` and `core-principles.instructions.md`. The shared-principles marker block is how AGENTS.md acknowledges them.
- **A copy of the README.** Link to the README instead.
- **Task lists or in-progress work.** Those belong in the issue tracker or `docs/`.
- **Ephemeral context.** Anything that will be false in three months.

## Common Post-Migration Cleanups

After `util-migrate-to-agents-md.sh` runs, an AGENTS.md often carries:

1. **Migrated block from CLAUDE.md** — `<!-- migrated:claude-md:start … end -->`. Content inside is verbatim from the pre-migration CLAUDE.md, minus the shared block. Lift substantive content into the standard sections; drop stale pointers.
2. **Migrated block from copilot-instructions.md** — `<!-- migrated:github-copilot-instructions-md:start … end -->`. Same treatment. Content here is usually project overview, tech stack, or conventions — maps naturally to `## Repository specifics`, `## Project structure`, or `## Conventions`.
3. **Duplicate H1s inside migrated blocks** — the pre-migration `# ProjectName` header from `.github/copilot-instructions.md` often ended up nested inside a migrated block. Delete the nested H1 (the repo's outer H1 already names the project).
4. **Stale pointer stubs** — "See `.github/copilot-instructions.md`" or "See `CLAUDE.md`" pointing at files that no longer exist. Delete.
5. **Orphan migration prefaces** — `**Migrated verbatim from …**` lines whose surrounding markers were cleaned up earlier. Delete.

Apply cleanups conservatively. If a line in a migrated block might carry weight, ask the user before dropping it.
