# nexus-skills Agent Guide

<!-- shared-principles:start -->
## Read the general principles first

They are authored once, in [.github/instructions/](.github/instructions/), and are not repeated here:

| File | Owns |
|---|---|
| [core-principles](.github/instructions/core-principles.instructions.md) | Think before acting; build for people; coherence. |
| [coding-principles](.github/instructions/coding-principles.instructions.md) | Simplicity, scope, completion, modernization, DRY. |

**Read `coding-principles` before your first edit.** This file adds only what is specific to this repository.
<!-- shared-principles:end -->

## Repository Map

| Path | Role |
|---|---|
| `skills/` | Canonical skill source. One self-contained folder per skill. |
| `plugin-packages/` | Plugin definitions (`plugin.json`, `skills.json`, `mcp.json`). |
| `bin/`, `src/` | The `nxa` CLI. Option reference: [README](README.md#cli-reference). |
| `scripts/` | Build, catalog, and validation scripts. |
| `docs/` | Taxonomy (`agent-taxonomy.yaml`) and planning notes. |
| `.github/` | Shared instructions, prompts, workflows, PR template. |
| `skill-catalog.json` | Generated. **Committed.** |
| `dist/`, `output/`, `skill-catalog-scan.json` | Generated. Gitignored. |
| `skills-sandbox/`, `prompts-sandbox/` | Experiments. Gitignored. Never put unfinished work in `skills/`. |

## Skill Conventions

- Folder name equals frontmatter `name`: lowercase, hyphens, max 64 characters.
- Name pattern: `<category-prefix>-<descriptor>`. Take the prefix from [docs/agent-taxonomy.yaml](docs/agent-taxonomy.yaml).
- `SKILL.md` sits at the folder root. Optional subfolders: `references/` (knowledge the skill loads), `scripts/`, `assets/`, `agents/`.
- One capability per skill. Do not bundle unrelated work.
- **Self-contained.** A skill never points at repo files (`AGENTS.md`, `CLAUDE.md`, copilot instructions) or at paths outside its own folder. It names other skills by name only.
- Write or revise `description` and `triggers` with the `skill-architect` skill.
- Plugin membership is a validation rule. `plugin-packages/<plugin>/skills.json` lists literal names or `prefix-*` globs. A skill that matches no plugin fails `npm run validate`. Add it in the same change.

## Skill Source of Truth

Folders such as `.agents/skills/`, `.claude/skills/`, `.codex/skills/`, and `.github/skills/` are **installed copies** made by the CLI. Edit `skills/<skill-name>/` only.

- Edited a copy by mistake → mirror the change into `skills/<skill-name>/` in the same commit.
- **Never run `nxa install`, `nxa upgrade`, or `nxa remove` after creating or editing a skill.** Do not refresh copies unless the user asks. Installing writes untracked folders into the repo (the default target is `.agents/skills/`).
- To check what is installed without changing anything, run `node bin/nxa.js list --installed [--global] [-a <agent>]`. Run `--help` to read options. Never run another command to find them.
- When the user does ask for a refresh, limit it to the named skill and use the default agent (`agent-skills`, `.agents/skills/`) unless the user names another:

  ```bash
  node bin/nxa.js upgrade --yes --skill <skill-name>
  ```

  - Always pass `--skill`. Without it the CLI replaces every installed skill in the target.
  - `upgrade` replaces only skills already installed. It never adds one. Use `install --skill <name>` for a new skill.
  - Add `-a <agent>` only when the user names that agent. Repeat `-a` for several.
  - `upgrade` alone asks `y/N` on stdin. In a non-interactive shell it stops with an error and changes nothing. `--yes` takes the default answers and skips the prompt.
  - An upgrade keeps `.env` and `.env.local` files, at any depth. It replaces every other file in the skill, `.env.example` included.
  - `node bin/nxa.js remove --skill <name> --yes` deletes a skill and keeps its `.env` files. Add `--delete-env` only when the user asks. Run it only when the user asks.
  - Add `--global` for the user-level copy.

## Build and Validate

Node 20+, no runtime dependencies.

| Command | Use |
|---|---|
| `npm run validate` | Spec checks on every skill and plugin. Run after any skill or plugin edit. |
| `npm run catalog` | Rebuild `skill-catalog.json`. |
| `npm run build:skills` | One zip per skill in `dist/skills/`. Use this to share a skill. |
| `npm run prepr` | Full build plus stale-artifact check. **Run before every PR.** |

Commit regenerated `skill-catalog.json`. Never commit `dist/` or `skill-catalog-scan.json`.

Commits follow Conventional Commits. Prefixes and their release effect: [README](README.md#releases-and-changelog).

## CLI

In this repo run `node bin/nxa.js`. External consumers run `npx nxa`. The two are equivalent. Flags, agent names, and install paths: [README CLI Reference](README.md#cli-reference).

## Pull Requests

1. Use [.github/pull_request_template.md](.github/pull_request_template.md). If the file is absent, write what changed, why, and how to verify.
2. Read the branch diff first: `git log <base>..HEAD --oneline` and `git diff --stat`.
3. Fill every section with real content. Replace placeholders, check the boxes that apply, delete sections that do not apply. Never submit the raw template.
4. Check the body before opening the PR: `node scripts/validation/check-pr-template.js <body-file>`.
