## Project Structure

- `skills/` — Skills available for install and export. Each skill is a self-contained folder.
- `prompts/` — Standalone prompt files for specific agents or use cases.
- `prompts-sandbox/` — Experimental or in-progress prompts, not production-ready.
- `skills-sandbox/` — Experimental skills under development.
- `bin/` — CLI and export scripts (see below).
- `output/` — Generated files (zips, catalog JSON/HTML). Not checked in by default.
- `docs/` — Reference docs, taxonomy files, agent planning notes.

## Skill Conventions

- Folder names: lowercase with hyphens (`marketing-content-linkedin-writer`)
- Every skill must have a `SKILL.md` at the root of its folder
- Supporting files go in subfolders: `knowledge/` for reference docs, `scripts/` for runnable code, `references/` for external content
- One skill per folder — do not bundle unrelated capabilities into one skill
- Skill names follow the pattern `domain-category-descriptor` (e.g., `tech-quality-tdd`)

## CLI — `npx forge-agents`

Use the CLI to install skills into an AI agent's skills directory. It supports the Agent Skills standard path plus GitHub Copilot, Claude Code, and Codex.

When consuming this repo externally, use `npx forge-agents`. When working inside this repo directly, use `node bin/cli.js` instead.

**Common commands:**

```bash
# List all available skills
npx forge-agents list

# Install all skills into the current project (Agent Skills standard, default)
npx forge-agents install

# Install a specific skill
npx forge-agents install --skill marketing-content-linkedin-writer

# Install globally (user-level, not project-level)
npx forge-agents install --global

# Install for a specific agent
npx forge-agents install --agent claude-code

# Install to multiple agents at once
npx forge-agents install -a github-copilot -a claude-code -a codex

# Upgrade (replace) already-installed skills
npx forge-agents install --upgrade
```

**Install targets by agent:**
- `agent-skills` → `.agents/skills/` (project) or `~/.agents/skills/` (global)
- `github-copilot` → `.agents/skills/` (project) or `~/.copilot/skills/` (global)
- `claude-code` → `.claude/skills/` (project) or `~/.claude/skills/` (global)
- `codex` → `.agents/skills/` (project) or `~/.codex/skills/` (global)

The default scope is `--project`. Use `--global` for personal skills you want available across all repos.

## Invoking Skills

Once installed, skills are invoked by name in the agent's chat interface:

```
/tech-quality-tdd implement a user login endpoint
/marketing-content-linkedin-writer write a post about our new product launch
```

The skill name maps directly to the folder name in `skills/`.

## Export Scripts — `bin/export-skill.sh` / `bin/export-skill.ps1`

Use these to package a skill as a `.zip` file for manual import into Claude or other platforms that accept zip-based skill uploads.

```bash
# Linux/macOS
./bin/export-skill.sh research-deep-reading-analyst

# Windows (PowerShell)
.\bin\export-skill.ps1 research-deep-reading-analyst
```

Output is written to `output/<skill-name>.zip`. The zip preserves the folder structure required by Claude (`<skill-name>/SKILL.md`, ...).

Use the export scripts when:
- Sharing a skill outside of GitHub (e.g., sending to a teammate)
- Importing manually into Claude's skill upload UI
- The CLI install path isn't applicable for the target platform

## General Guidelines

- Don't add files to `output/` unless they are generated artifacts
- Keep `skills/` and `prompts/` clean — sandbox work belongs in `*-sandbox/` folders
- The `ai-personal-kb/` folder contains personal context data, not agent prompts — don't treat it as a skill source
