## Project Structure

- `skills/` — Skills available for install and export. Each skill is a self-contained folder.
- `prompts/` — Standalone prompt files for specific agents or use cases.
- `bin/` — CLI and export scripts (see below).
- `docs/` — Reference docs, taxonomy files, agent planning notes.
- `output/` — Generated files (zips, catalog JSON/HTML). Not checked in by default.
- `prompts-sandbox/` — Experimental or in-progress prompts, not production-ready.
- `skills-sandbox/` — Experimental skills under development.

## Skill Conventions

- Folder names: lowercase with hyphens (`marketing-content-linkedin-writer`)
- Every skill must have a `SKILL.md` at the root of its folder
- Supporting files go in subfolders: `knowledge/` for reference docs, `scripts/` for runnable code, `references/` for external content
- One skill per folder — do not bundle unrelated capabilities into one skill
- Skill names follow the pattern `domain-category-descriptor` (e.g., `engineering-quality-tdd`)

## Skill Source of Truth

`skills/` is the canonical source for every skill in this repo. Folders under `.github/skills/`, `.agents/skills/`, `.claude/skills/`, `.codex/skills/`, or any other agent-specific path are **installed copies** produced by the CLI (`node bin/cli.js install`).

When updating a skill:
1. Always edit the source in `skills/<skill-name>/` first.
2. Never edit an installed copy as the primary change — copies will be overwritten on the next install.
3. If you've already edited a copy (e.g., `.github/skills/<skill-name>/SKILL.md`), mirror the change back into `skills/<skill-name>/` in the same commit.
4. After updating the source, refresh installed copies by running `node bin/cli.js install --upgrade` from the repo root (use `npx nexus-agents install --upgrade` only when consuming this repo externally).

## CLI — `node bin/cli.js` (in-repo) / `npx nexus-agents` (external)

Use the CLI to install skills into an AI agent's skills directory. It supports the Agent Skills standard path plus GitHub Copilot, Claude Code, and Codex.

**Inside this repo, use `node bin/cli.js`. When consuming this repo externally, use `npx nexus-agents`.** The two are equivalent — the examples below use the in-repo form.

**Common commands:**

```bash
# List all available skills
node bin/cli.js list

# Install all skills into the current project (Agent Skills standard, default)
node bin/cli.js install

# Install a specific skill
node bin/cli.js install --skill marketing-content-linkedin-writer

# Install globally (user-level, not project-level)
node bin/cli.js install --global

# Install for a specific agent
node bin/cli.js install --agent claude-code

# Install to multiple agents at once
node bin/cli.js install -a github-copilot -a claude-code -a codex

# Upgrade (replace) already-installed skills
node bin/cli.js install --upgrade
```

**Install targets by agent:**
- `agent-skills` → `.agents/skills/` (project) or `~/.agents/skills/` (global)
- `github-copilot` → `.github/skills/` (project) or `~/.github/skills/` (global)
- `claude-code` → `.claude/skills/` (project) or `~/.claude/skills/` (global)
- `codex` → `.agents/skills/` (project) or `~/.codex/skills/` (global)

The default scope is `--project`. Use `--global` for personal skills you want available across all repos.

## Invoking Skills

Once installed, skills are invoked by name in the agent's chat interface:

```
/engineering-quality-tdd implement a user login endpoint
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

## Pull Request Descriptions

When creating a pull request, always:
1. Locate the PR template, checking in this order:
   - `.github/pull_request_template.md`
   - `pull_request_template.md` (repo root) or `docs/pull_request_template.md`
   - `.github/PULL_REQUEST_TEMPLATE/` directory — if multiple templates exist, pick the one matching the change type (e.g. `bug_fix.md`, `feature.md`); ask the user if it is ambiguous.
2. Review the branch diff (`git log <base>..HEAD --oneline` and `git diff --stat`) to understand what changed.
3. Fill out every section of the template with real content — replace all placeholders, check applicable boxes, delete sections that don't apply.
4. Never pass the raw template as the PR body; it must be populated before submission.
5. If no template is found, write a clear description covering what changed, why, and how to verify.
