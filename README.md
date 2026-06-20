
> Agentic skills, prompts, and instructions for AI coding platforms — GitHub Copilot, Claude Code, and Codex.

[![Skills](https://img.shields.io/badge/skills-40%2B-blue.svg)](skills/)

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

- **40+ production-ready skills** organized by domain: marketing, strategy, product, design, tech, and more
- **Multi-platform support** — install to GitHub Copilot, Claude Code, or Codex
- **Project or global scope** — install skills for a single project or system-wide
- **CLI installer** — install, list, and upgrade skills from the command line
- **VS Code agents** — pre-built Copilot agent `.agent.md` configurations
- **Instruction files** — path-scoped coding guidelines for consistent AI behavior across teams
- **Reusable prompts** — 25+ structured `.prompt.md` files for common engineering and product workflows

## Architecture Overview

**Distribution layer** (`skills/`, `bin/`)
The `skills/` folder is the source-of-truth skill registry. Each skill is a self-contained folder with a `SKILL.md` file and optional `references/` materials. The CLI (`bin/cli.js`) copies skills from this registry into AI agent config directories on the local machine.

**VS Code Copilot customization layer** (`.github/`)
The `.github/` folder contains VS Code Copilot customizations: agent definitions (`.github/agents/`), path-scoped instruction files (`.github/instructions/`), reusable prompts (`.github/prompts/`), and global Copilot instructions (`.github/copilot-instructions.md`). These files are picked up automatically by VS Code Copilot and are not installed via the CLI.

## Key Concepts

### Skills

A **skill** is a `SKILL.md` file that gives an AI agent a specialized behavior or workflow. Skills use YAML frontmatter to declare their `name`, `description`, and `metadata`. The description is the search trigger — the agent routes to a skill when the user's request matches it.

Skills are installed into an AI agent's config directory (e.g., `.agents/skills/` for GitHub Copilot). Once installed, skills are invoked by name in chat.

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
│   ├── cli.js                  # CLI installer entry point
│   ├── skills-core.js          # Core skill discovery and validation utilities
│   ├── github-fetch.js         # Remote skill fetch from GitHub
│   ├── skill-overlap-report.js # Skill overlap analysis and reporting
│   ├── export-skill.ps1        # Package a skill into a zip (PowerShell)
│   ├── export-skill.sh         # Package a skill into a zip (Bash)
│   └── rebuild-catalog.py      # Rebuild skill catalog output files
├── skills/                     # Source skill registry
│   ├── agent-catalog-skill-evaluator/
│   ├── agent-design-icon-creator/
│   ├── agent-skill-writer/
│   ├── tech-quality-tdd/
│   └── ...                     # 40+ skills total
├── prompts/                    # Legacy prompt templates
├── docs/                       # Project documentation
├── .github/
│   ├── copilot-instructions.md # Global Copilot instructions
│   ├── agents/                 # Copilot agent definitions
│   ├── instructions/           # Path-scoped instruction files
│   └── prompts/                # Reusable Copilot prompt files
└── package.json
```

## Prerequisites & Requirements

- **Node.js** v16 or later
- **npm** (included with Node.js)
- One or more supported AI agents installed:
  - [GitHub Copilot](https://github.com/features/copilot) (VS Code extension)
  - [Claude Code](https://claude.ai/code)
  - [Codex CLI](https://github.com/openai/codex)

## Installation

### From a cloned repo

From the project root, install all skills to the current project (default agent: GitHub Copilot):

```bash
node bin/cli.js install
```

Install a specific skill to a specific agent:

```bash
node bin/cli.js install --skill content-copy-humanizer -a github-copilot
```

Install to multiple agents at once:

```bash
node bin/cli.js install -a github-copilot
```

Install globally instead of project-scoped:

```bash
node bin/cli.js install --skill product-spec-prd-generator --global
```

### CLI Reference

| Command | Short | Description |
|---------|-------|-------------|
| `install` | | Install skills |
| `list` | | List available skills |
| `audit-overlap` | | Find duplicate and overlapping skills |
| `--skill <name>` | `-s` | Install a specific skill (repeatable) |
| `--agent <name>` | `-a` | Target agent (repeatable, default: `agent-skills`) |
| `--global` | `-g` | Install globally (default: project) |
| `--project` | `-p` | Install to project (explicit) |
| `--upgrade` | `-u` | Upgrade existing skills (prompts for confirmation) |
| `--overwrite` | `-o` | Skip confirmation when upgrading |
| `--source-url <url>` |  | Clone skills from a git repository instead of the bundled skills |
| `--source-ref <ref>` |  | Branch, tag, or commit to clone with `--source-url` |
| `--full` | `-f` | List skills with descriptions |
| `--names` | `-n` | List skill names only |
| `--count` | `-c` | Print skill count only |

**`audit-overlap` options:**

| Option | Short | Description |
|--------|-------|-------------|
| `--threshold <n>` | `-t` | Minimum overlap score to report (default: 0.20) |
| `--top <n>` | | Limit output to top N pairs |
| `--json-only` | | Write JSON report only |
| `--md-only` | | Write Markdown report only |
| `--output <dir>` | `-o` | Output directory (default: `output/`) |

### Supported agents

| Agent | Global path | Project path |
|-------|-------------|--------------|
| `agent-skills` (default) | `~/.agents/skills/` | `.agents/skills/` |
| `github-copilot` | `~/.github/skills/` | `.github/skills/` |
| `claude-code` | `~/.claude/skills/` | `.claude/skills/` |
| `codex` | `~/.codex/skills/` | `.agents/skills/` |

## Usage

After installation, invoke a skill in your AI agent chat by describing what you want to do. The agent matches your request to the closest skill by description.

For repeatable team installs, pin a branch, tag, or commit in the git package spec or pass `--source-ref` so every project pulls the same skill set.

**Examples:**

```
/agent-skill-writer create a new skill for drafting weekly status updates
```

```
/tech-api-mcp-builder build an MCP server for the GitHub API with issues and PR tools
```

```
/product-spec-prd-generator generate a PRD for a mobile expense tracking app
```

```
/tech-quality-tdd implement a user authentication service
```

Skill names map directly to the folder names in `skills/`. Use `node bin/cli.js list --full` to see all available skills with their descriptions.

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

- [Agent Skills specification](https://agentskills.io/specification)
- [GitHub Copilot customization docs](https://docs.github.com/en/copilot/customizing-copilot)
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Skill authoring guide](skills/agent-skill-writer/SKILL.md)
- [Project docs](docs/)
- [Changelog](CHANGELOG.md)

## Automated build pipeline

The repo ships an end-to-end automation that keeps the catalog, plugins, and
distribution site consistent with `skills/`. The same scripts run locally and
in CI, so a local build matches what gets published.

### Local build

```bash
npm run validate        # spec checks against every skills/<skill>/SKILL.md
npm run scan            # writes skill-catalog-scan.json (mechanical metadata)
npm run catalog         # rebuilds skill-catalog.json (merges scan + evaluations + packs)
npm run build:plugins   # regenerates .claude-plugin/marketplace.json + per-pack bundles in dist/plugins/
npm run build:site      # assembles GitHub Pages site in dist/site/ (catalog browser, pack manager, per-pack zips)

npm run build           # all of the above in order
```

Outputs:

| Path | Source of truth | Committed? |
|------|------|------|
| `skill-catalog-scan.json` | `npm run scan` | yes |
| `skill-catalog.json` | `npm run catalog` (merges scan + `skill-catalog-evaluations.json`) | yes |
| `.claude-plugin/marketplace.json` | `npm run build:plugins` (from `packs/*.json`) | yes |
| `.claude-plugin/plugin.json` | `npm run build:plugins` (umbrella `nexus-all`) | yes |
| `dist/plugins/<pack>/` | `npm run build:plugins` (self-contained pack bundles) | no |
| `dist/site/` | `npm run build:site` (GitHub Pages root) | no |

### CI workflows

| Workflow | Trigger | Purpose |
|---|---|---|
| [`.github/workflows/ci.yml`](.github/workflows/ci.yml) | PR + push to `main` | Validate skills, rebuild catalog, generate plugins, build site; warns if committed catalog/marketplace drifts from source. |
| [`.github/workflows/release.yml`](.github/workflows/release.yml) | push to `main` | release-please opens a release PR with bumped version + changelog from Conventional Commits. On merge, tags a release and attaches per-pack zips, `skill-catalog.json`, and `marketplace.json` as release assets. |
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
| `pack:` | patch | 📦 Pack Changes |
| `docs:` | patch | 📝 Documentation |
| `build:` / `ci:` | patch | 🛠️ Build / 🤖 CI |
| `chore:` / `refactor:` / `test:` / `style:` | none | hidden |
| `feat!:` or `BREAKING CHANGE:` footer | major | top of release notes |

release-please maintains a long-lived PR titled `chore(main): release X.Y.Z`.
Merging that PR cuts the release; nothing else needs to be tagged manually.

### Adding a pack

1. Create `packs/<your-pack>.json` with `name`, `description`, and a `skills`
   array (literal names or `prefix-*` globs).
2. Run `npm run build` locally and commit the regenerated catalog + plugin
   manifests.
3. Open a PR. CI verifies everything compiles; on merge, release-please will
   pick the change up in the next release.

