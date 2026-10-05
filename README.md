
> Agentic skills, prompts, and instructions for AI coding platforms — GitHub Copilot, Claude Code, and Codex.

[![Skills](https://img.shields.io/badge/skills-141-blue.svg)](skills/)

## Table of Contents

- [Overview](#overview)
- [Features \& Capabilities](#features--capabilities)
- [Architecture Overview](#architecture-overview)
- [Key Concepts](#key-concepts)
- [Project Structure](#project-structure)
- [Prerequisites \& Requirements](#prerequisites--requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Skills Reference](#skills-reference)
- [Additional Resources](#additional-resources)

## Overview

Curated collection of agent skills, reusable prompts, and coding instructions for AI development platforms. Skills are self-contained behavior packages that give AI agents specialized capabilities — from drafting PRDs and writing SOPs, to building MCP servers and running TDD workflows.

Install any skill once and invoke it in your AI agent by name. Skills work with GitHub Copilot, Claude Code, and Codex.

## Features & Capabilities

- **141 production-ready skills** organized by domain: marketing, strategy, product, design, tech, and more
- **Multi-platform support** — install to GitHub Copilot, Claude Code, or Codex
- **Project or global scope** — install skills for a single project or system-wide
- **CLI installer** — install, list, and upgrade skills from the command line
- **VS Code agents** — pre-built Copilot agent `.agent.md` configurations
- **Instruction files** — path-scoped coding guidelines for consistent AI behavior across teams
- **Reusable prompts** — 25+ structured `.prompt.md` files for common engineering and product workflows

## Architecture Overview

**Distribution layer** (`skills/`, `bin/`, `src/`)
The `skills/` folder is the source-of-truth skill registry. Each skill is a self-contained folder with a `SKILL.md` file and optional `references/` materials. The CLI (`bin/nxa.js`) copies skills from this registry into AI agent config directories on the local machine, with implementation code in `src/`.

**VS Code Copilot customization layer** (`.github/`)
The `.github/` folder contains VS Code Copilot customizations: agent definitions (`.github/agents/`), path-scoped instruction files (`.github/instructions/`), reusable prompts (`.github/prompts/`), and global Copilot instructions (`.github/copilot-instructions.md`). These files are picked up automatically by VS Code Copilot and are not installed via the CLI.

## Key Concepts

### Skills

A **skill** is a `SKILL.md` file that gives an AI agent a specialized behavior or workflow. Skills use YAML frontmatter to declare their `name`, `description`, and `metadata`. The description is the search trigger — the agent routes to a skill when the user's request matches it.

Skills are installed into an AI agent's skills directory (e.g., `.github/skills/` for GitHub Copilot, `.claude/skills/` for Claude Code). Once installed, skills are invoked by name in chat.

### Agents

**Agents** (`.github/agents/*.agent.md`) are VS Code Copilot custom agent modes. Each agent has a role, system prompt, and optional handoffs to other agents.

### Instructions

**Instructions** (`.github/instructions/*.instructions.md`) are scoped coding guidelines automatically injected by VS Code Copilot for matching file paths. For example, `java-backend.instructions.md` applies to `backend/**/*.java` files.

### Prompts

**Prompts** (`.github/prompts/*.prompt.md`) are reusable task templates invoked with `#` in VS Code Copilot Chat. Examples: `nexus-document-readme.prompt.md`, `nexus-quality-tdd.prompt.md`.

## Project Structure

```
{root}/
├── bin/
│   └── nxa.js                  # Published CLI executable
├── src/
│   ├── cli/                    # CLI parsing, help, and command handlers
│   ├── core/                   # Skill discovery, validation, plugins, and file utilities
│   ├── sources/                # Local, git, and GitHub skill sources
│   └── audit/                  # Skill overlap analysis engine
├── scripts/
│   ├── build/                  # Plugin and GitHub Pages builders
│   ├── catalog/                # Skill catalog scan/rebuild scripts
│   ├── export/                 # Manual skill zip export scripts
│   └── validation/             # Repository validation scripts
├── skills/                     # Source skill registry
│   ├── engineering-doc-agents-md-curator/
│   ├── content-copy-humanizer/
│   ├── engineering-quality-tdd/
│   ├── product-spec-prd-generator/
│   └── ...                     # 153 skills total
├── plugin-packages/            # Plugin definitions (manifest + membership + optional MCP)
│   ├── content/
│   ├── data/
│   └── ...                     # 14 plugins total
├── docs/                       # Project documentation
├── .github/
│   ├── copilot-instructions.md # Global Copilot instructions
│   ├── agents/                 # Copilot agent definitions
│   ├── instructions/           # Path-scoped instruction files
│   └── prompts/                # Reusable Copilot prompt files

```

## Prerequisites & Requirements

- **Node.js** v20 or later
- **npm** (included with Node.js)
- **git** (only for `--source-url`)
- One or more supported AI agents installed:
  - [GitHub Copilot](https://github.com/features/copilot) (VS Code extension)
  - [Claude Code](https://claude.ai/code)
  - [Codex CLI](https://github.com/openai/codex)

## Installation

### From a cloned repo

From the project root, install every skill into the current project. With no `--agent`, the target is the Agent Skills standard path `.agents/skills/`:

```bash
node bin/nxa.js install
```

Install one skill for one agent:

```bash
node bin/nxa.js install --skill content-copy-humanizer -a github-copilot
```

Install to several agents at once:

```bash
node bin/nxa.js install -a agent-skills -a claude-code -a github-copilot -a codex
```

Install every skill in a plugin:

```bash
node bin/nxa.js install --plugin marketing
```

Install globally instead of into the project:

```bash
node bin/nxa.js install --skill product-spec-prd-generator --global
```

Refresh every skill you already have installed globally. It adds no new skills:

```bash
node bin/nxa.js upgrade --global
```

Refresh one installed skill:

```bash
node bin/nxa.js upgrade --skill content-copy-humanizer
```

See what is installed globally, and remove a skill:

```bash
node bin/nxa.js list --installed --global --full
node bin/nxa.js remove --skill content-copy-humanizer --global
```

### Without a clone

`npx nxa <command>` runs the same CLI. When it finds no `skills/` folder next to itself, it downloads skills from GitHub instead of copying a local bundle. The command header shows which source it used (`local bundle`, `GitHub fallback`, or `repository <url>`).

### CLI Reference

```
node bin/nxa.js <command> [options]
```

Inside this repo use `node bin/nxa.js`. Outside it use `npx nxa`. The command comes first, then its options in any order. Run with no command, `help`, `--help`, or `-h` to print the built-in help. `--help` anywhere on the line prints help and runs nothing. `--version` or `-v` prints the version.

The CLI is strict, so a typo never turns into a large or partial install:

- An unknown command, unknown option, or stray word is an error. `nxa install content-copy-humanizer` fails and tells you to use `--skill`.
- An option that does not apply to the command is an error, for example `list --global`.
- An option that needs a value and has none is an error, for example `--skill` at the end of the line.
- An unknown skill, plugin, or agent stops the command before it writes anything.
- Usage errors exit with code 2. Other failures exit with code 1. Errors go to standard error.

Value options also accept `--option=value`. `--skill`, `--plugin`, and `--agent` accept comma-separated lists: `--skill a,b,c`.

#### Commands

| Command | Description |
|---------|-------------|
| `install` | Copy skills into one or more agent skill directories. Skips skills that are already there unless `--upgrade` is set. |
| `upgrade` | Replace skills that are already installed with the source version. Never adds a skill. |
| `remove` | Delete installed skills. Needs `--skill` or `--plugin`. |
| `list` | Print the available skills, or with `--installed`, the skills installed in a target |
| `audit-overlap` | Score every skill pair for duplicate or colliding purpose and write a report |
| `help` | Print usage |

An unknown command is an error (exit code 2).

#### `install` options

| Option | Short | Description |
|--------|-------|-------------|
| `--skill <name>` | `-s` | Install this skill. Repeatable or comma-separated. Default: every available skill. |
| `--plugin <name>` | `-P` | Install every skill in a plugin from `plugin-packages/`, such as `marketing`, `engineering`, or `data`. Repeatable or comma-separated. Combines with `--skill`. |
| `--agent <name>` | `-a` | Target agent. Repeat for several. Default: `agent-skills`. See [Supported agents](#supported-agents). |
| `--project` | `-p` | Install into the current directory (default). |
| `--global` | `-g` | Install into the user-level directory. |
| `--upgrade` | `-u` | Delete and replace skills that already exist. Without this flag, existing skills are skipped. |
| `--yes` | `-y` | With `--upgrade`, skip the `[y/N]` confirmation. Without `--upgrade` it is an error. `--overwrite` / `-o` is the same flag. |
| `--source-url <url>` | | Clone this git repository and read its `skills/` folder instead of the local bundle. |
| `--source-ref <ref>` | | Branch or tag to clone with `--source-url`. Default: the repository's default branch. Without `--source-url` it is an error. |

How `install` behaves:

- It installs into `<agent dir>/<skill-name>/` and prints one line per skill: installed, skipped (already installed), upgraded, or failed. A summary count follows.
- `--upgrade` first lists the existing skills it will replace, then asks `Proceed with upgrade? [y/N]`. When standard input is not a terminal, the command stops with an error and changes nothing. Add `--overwrite` there.
- `install --upgrade` without `--skill` or `--plugin` installs every available skill and replaces the ones already there. To refresh only what is installed, use `upgrade`.
- `--skill` and `--plugin` add up. An unknown skill or plugin name stops the command before it writes anything.
- An unknown agent name stops the command before it writes anything.
- Replacing a skill keeps your `.env` and `.env.local` files, wherever they are in the skill folder (root, `scripts/`, or any other subfolder). Everything else is removed and replaced by the source copy: `SKILL.md`, `scripts/`, `assets/`, `references/`, `.env.example`, and any other file. The output line lists the kept files.
- Each skill is copied into a hidden staging folder first, then swapped into place. If a copy or download fails, the installed version stays as it was, and the command exits with code 1.
- `__pycache__`, `*.pyc`, `.DS_Store`, `.pytest_cache`, and `node_modules` are never copied.
- Agents that share a directory install once. In project scope, `agent-skills` and `codex` both use `.agents/skills/`.
- `--plugin` reads `plugin-packages/`, so it needs a checkout of this repository.
- `--project` against `--global`, and `--names`, `--full`, `--count` against each other: the last one on the command line wins.

#### `upgrade` options

`upgrade` takes the same `--skill`, `--plugin`, `--agent`, `--project`, `--global`, `--yes`, `--source-url`, and `--source-ref` options as `install`.

How `upgrade` behaves:

- It looks at the skills already installed in each target directory and replaces only those. It never adds a skill.
- It keeps your `.env` and `.env.local` files and replaces everything else, as `install --upgrade` does.
- With no `--skill` or `--plugin`, it upgrades every installed skill. With them, it upgrades only the named skills. A plugin's skills that are not installed are ignored.
- A skill named with `--skill` that is not installed is an error. Use `install` to add it.
- An installed skill that the source does not have, such as your own private skill, is listed as left unchanged and is not touched.
- It lists what it will replace and asks for confirmation. `--yes` skips the prompt. When standard input is not a terminal and `--yes` is not set, it stops with an error and changes nothing.

#### `remove` options

`remove` takes `--skill`, `--plugin`, `--agent`, `--project`, `--global`, `--yes`, and `--delete-env`.

How `remove` behaves:

- It needs `--skill` or `--plugin`. It never removes every skill.
- It matches names against what is installed, not against the source, so it can remove a skill the source no longer has. `--plugin` removes the installed skills that the plugin lists.
- A `--skill` name that is not installed in any target stops the command before it deletes anything.
- By default it keeps `.env` and `.env.local` files where they are (root, `scripts/`, or any subfolder) and deletes everything else. A folder left with only those files no longer counts as installed. A later `install` of the same skill fills it back in and keeps the files.
- It lists every skill it will remove and names any `.env` or `.env.local` inside. If there are any, it asks `Keep .env and .env.local files? [Y/n]` (default: keep). Then it asks `Proceed with removal? [y/N]`.
- `--yes` skips both prompts and takes the defaults: proceed, and keep the `.env` files. An agent can run `remove --skill <name> --yes` without waiting for input.
- `--delete-env` also deletes the `.env` and `.env.local` files. Combine it with `--yes` to delete whole folders without prompting.
- When standard input is not a terminal and `--yes` is not set, it stops with an error and changes nothing.

#### `list` options

| Option | Short | Description |
|--------|-------|-------------|
| `--installed` | `-i` | List the skills installed in the target instead of the available ones. Takes `--agent`, `--project`, and `--global`, which `list` rejects without it. |
| `--names` | `-n` | One skill name per line (default). |
| `--full` | `-f` | Each skill with its description. With `--installed`, also marks skills the source does not have and skills that hold `.env` files. |
| `--count` | `-c` | Only the number of skills. |
| `--source-url <url>`, `--source-ref <ref>` | | List the skills of another repository, as in `install`. |

#### `audit-overlap` options

Reads the local `skills/` folder, so run it from a clone. It writes `skill-overlap-report.json` and `skill-overlap-report.md`, then prints the pairs that need action. Put the options after the command. An unknown option, a missing value, a threshold outside 0 to 1, or `--json-only` with `--md-only` is an error.

| Option | Short | Description |
|--------|-------|-------------|
| `--threshold <n>` | `-t` | Minimum overall score to report (default: `0.20`). |
| `--top <n>` | | Report only the top N pairs (default: all). |
| `--json-only` | | Write the JSON report only. |
| `--md-only` | | Write the Markdown report only. |
| `--output <dir>` | `-o` | Report directory (default: `output/`). |

`-o` means `--overwrite` (same as `--yes`) for `install`, `upgrade`, and `remove`, and `--output` for `audit-overlap`.

#### Supported agents

| Agent | Aliases | Global path | Project path |
|-------|---------|-------------|--------------|
| `agent-skills` (default) | `agents`, `agentskills`, `standard` | `~/.agents/skills/` | `.agents/skills/` |
| `github-copilot` | `copilot` | `~/.github/skills/` | `.github/skills/` |
| `claude-code` | `claude` | `~/.claude/skills/` | `.claude/skills/` |
| `codex` | `openai-codex` | `~/.codex/skills/` | `.agents/skills/` |

#### Environment variables

| Variable | Effect |
|----------|--------|
| `NEXUS_AGENTS_REPO_URL` | Same as `--source-url`. The flag wins when both are set. |
| `NEXUS_AGENTS_REPO_REF` | Same as `--source-ref`. In the GitHub fallback it selects the branch or tag to download (default: `main`). |
| `NEXUS_AGENTS_FORCE_REMOTE` | Set to `1` to ignore the local `skills/` folder and use the GitHub fallback. |
| `NEXUS_AGENTS_REPO_OWNER`, `NEXUS_AGENTS_REPO_NAME` | Repository the GitHub fallback downloads from (default: `scanady/nexus-skills`). |

Source order: `--source-url` (or `NEXUS_AGENTS_REPO_URL`), then the local `skills/` folder, then the GitHub fallback.

#### Older flag spellings

These still work but are not in the built-in help: `--pack` for `--plugin`, `--repo-url` for `--source-url`, `--ref` for `--source-ref`.

#### More examples

```bash
node bin/nxa.js list --full
node bin/nxa.js list --count
node bin/nxa.js install --plugin engineering,data -a claude-code
node bin/nxa.js install -a github-copilot --skill content-copy-humanizer -p
node bin/nxa.js upgrade --global --yes
node bin/nxa.js upgrade -a claude-code --plugin marketing
node bin/nxa.js install --source-url https://github.com/scanady/nexus-skills.git --source-ref main
node bin/nxa.js audit-overlap --threshold 0.30 --top 25 --output reports/
```

## Usage

After installation, invoke a skill in your AI agent chat by describing what you want to do. The agent matches your request to the closest skill by description.

For repeatable team installs, pin a branch, tag, or commit in the git package spec or pass `--source-ref` so every project pulls the same skill set.

**Examples:**

```
/skill-architect create a new skill for drafting weekly status updates
```

```
/engineering-api-mcp-builder build an MCP server for the GitHub API with issues and PR tools
```

```
/product-spec-prd-generator generate a PRD for a mobile expense tracking app
```

```
/engineering-quality-tdd implement a user authentication service
```

Skill names map directly to the folder names in `skills/`. Use `node bin/nxa.js list --full` to see all available skills with their descriptions.

## Skills Reference

Review the [skills catalog](skill-catalog.html) viewer and [skill catalog detail](skill-catalog.json).  
Skills are organized by domain prefix.  

## Adding Skills

### Skill structure

```
skills/
└── your-skill-name/
    ├── SKILL.md          # Required: skill definition with YAML frontmatter
    └── references/       # Optional: reference materials loaded by the skill
```

A valid `SKILL.md` requires at minimum:

```yaml
---
name: your-skill-name
description: Use when [trigger condition] — [what it does]
---

# Skill Title

[Skill instructions here]
```

## Additional Resources

- [Skill authoring guide](skills/skill-architect/SKILL.md)
- [Project docs](docs/)
- [Changelog](CHANGELOG.md)

## Automated build pipeline

The repo ships an end-to-end automation that keeps the catalog, plugins, and
distribution site consistent with `skills/`. The same scripts run locally and
in CI, so a local build matches what gets published. Node 20+ is the only
prerequisite — every build script is JavaScript, with no other runtime and no
runtime dependencies.

### Local build

```bash
npm run validate        # spec checks against every skills/<skill>/SKILL.md
npm run scan            # writes skill-catalog-scan.json (mechanical metadata)
npm run catalog         # rebuilds skill-catalog.json (merges scan + evaluations + plugin membership)
npm run build:plugins   # builds per-plugin bundles + dist/plugins/manifest.json from plugin-packages/
npm run build:skills    # creates one skill zip per source skill in dist/skills/
npm run build:site      # assembles GitHub Pages site in dist/site/ (catalog browser, plugin manager, per-plugin zips)
npm run check:artifacts # fails if committed generated artifacts are stale

npm run build           # all of the above in order
npm run prepr           # build, then verify committed artifacts match generated output
```

Before opening a pull request, run `npm run prepr` and commit any changes to
`skill-catalog.json`. It is the only generated file this repo commits — the
plugin distribution is rebuilt into `dist/`, which is gitignored. To install the
same check as a local pre-push hook, run `npm run hooks:install` once in your
clone.

Outputs:

| Path | Source of truth | Committed? |
|------|------|------|
| `skill-catalog-scan.json` | `npm run scan` | no |
| `skill-catalog.json` | `npm run catalog` (merges scan + `skill-catalog-evaluations.json` + `scripts/catalog/new-evaluations.json`) | yes |
| `dist/plugins/<plugin>/` | `npm run build:plugins` (self-contained plugin bundles) | no |
| `dist/skills/<skill>.zip` | `npm run build:skills` (one archive per source skill) | no |
| `dist/plugins/manifest.json` | `npm run build:plugins` (machine-readable index of `plugin-packages/`) | no |
| `dist/site/` | `npm run build:site` (GitHub Pages root) | no |

### CI workflows

| Workflow | Trigger | Purpose |
|---|---|---|
| [`.github/workflows/ci.yml`](.github/workflows/ci.yml) | PR + push to `main` | Validate skills, rebuild catalog, generate plugins, build site; warns if the committed catalog drifts from source. |
| [`.github/workflows/release.yml`](.github/workflows/release.yml) | push to `main` | release-please opens a release PR with bumped version + changelog from Conventional Commits. On merge, tags a release and attaches per-plugin zips and `skill-catalog.json` as release assets. |
| [`.github/workflows/pages.yml`](.github/workflows/pages.yml) | release published (or manual) | Builds `dist/site/` and deploys it to GitHub Pages. |

### Releases and changelog

Versioning is driven by [Conventional Commits](https://www.conventionalcommits.org/).
Use the following prefixes so release-please can categorize commits into the
[CHANGELOG](CHANGELOG.md):

| Prefix | Bump | Changelog section |
|---|---|---|
| `feat:` | minor | ✨ Features |
| `fix:` | patch | 🐛 Bug Fixes |
| `perf:` | patch | ⚡ Performance |
| `skill:` | patch | 🧠 New / Updated Skills |
| `plugin:` | patch | 📦 Plugin Changes |
| `docs:` | patch | 📝 Documentation |
| `build:` / `ci:` | patch | 🛠️ Build / 🤖 CI |
| `chore:` / `refactor:` / `test:` / `style:` | none | hidden |
| `feat!:` or `BREAKING CHANGE:` footer | major | top of release notes |

release-please maintains a long-lived PR titled `chore(main): release X.Y.Z`.
Merging that PR cuts the release; nothing else needs to be tagged manually.

### Adding a plugin

A plugin is defined by a directory under `plugin-packages/`:

| File | Required | Contents |
|---|---|---|
| `plugin.json` | yes | [Agent Plugins](https://agent-plugins.org/) v1.0.0 manifest. `$schema` and `name` are required; the schema is closed, so only `$schema`, `name`, `version`, `description`, `author`, `homepage`, `repository`, `license`, `keywords`, and `extensions` are allowed. Name it `nexus-<directory>`, except `workplace`, whose name is the directory name. |
| `skills.json` | yes | `{ "skills": [...] }` — literal skill names or `prefix-*` globs. Build-only; it is never shipped, and it is not part of the spec. |
| `mcp.json` | yes | `{ "$schema": ..., "mcpServers": {...} }`. Both keys are required and the schema is closed. Every plugin carries one; new plugins start from an empty stub. Declared servers are copied into the bundle as `mcp.json`, the Agent Plugins location. An empty stub ships nothing. |

`plugin-packages/` is the single source of truth for plugin packages. Nothing
about a plugin is authored anywhere else. `npm run build:plugins` projects every
package into `dist/plugins/manifest.json` — description, version, keywords,
membership patterns, resolved skills, and MCP servers — which is what the
[plugin manager](plugin-manager.html) reads and writes back. `skill-catalog.json`
records only which plugins each skill belongs to, never the plugin definitions.

### Agent Plugins conformance

Bundles under `dist/plugins/<name>/` are portable
[Agent Plugins v1.0.0](https://agent-plugins.org/specification) packages:

- `plugin.json` sits at the plugin root — there is no `.claude-plugin/` wrapper.
  It declares `$schema` and `name`, both required, and nothing outside the
  schema's closed key set.
- Skills are **discovered** from `skills/`, not listed in the manifest. Each
  immediate child directory holding a `SKILL.md` is one skill; clients must not
  search deeper, so a nested `SKILL.md` would be invisible.
- `mcp.json` is the only place MCP servers are declared. It is written only when
  a package declares at least one server.
- `version` follows Semantic Versioning, which the spec recommends.

The spec defines no registry, marketplace, or distribution mechanism, so this
repo ships none. Install with `nxa install --plugin <name>` or unzip a bundle.

`npm run validate` checks both schemas: required fields, the closed key sets,
the `name` pattern, and every MCP server against its transport — `stdio`,
`streamable-http`, or `sse`, including the reserved `PLUGIN_ROOT` / `PLUGIN_DATA`
env names and the plugin-root containment rule for `cwd`.

1. Create the directory and its files.
2. Run `npm run build` locally and commit the regenerated `skill-catalog.json`.
   Do not commit `skill-catalog-scan.json` or anything under `dist/`.
   Validation fails if any skill belongs to no plugin, so add new skills to a
   plugin in the same change.
3. Open a PR. CI verifies everything compiles; on merge, release-please will
   pick the change up in the next release.

