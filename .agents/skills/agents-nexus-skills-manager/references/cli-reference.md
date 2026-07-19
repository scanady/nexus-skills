# Nexus Skills CLI Reference

Use this reference before constructing a command. Prefer the shortest command that satisfies the user's stated scope.

## Command Runners

| Context | Runner |
|---|---|
| Inside a cloned Nexus Skills repository | `node bin/nxa.js` |
| Outside the repo, package runner available | `npx nxa` |
| Outside the repo, direct GitHub source | `npm exec --yes --package=git+https://github.com/scanady/nexus-skills.git#main -- nxa` |

If the user needs a pinned version, add the relevant branch, tag, or commit to the GitHub package spec or pass `--source-ref` with `--source-url`.

## Core Commands

| Command | Purpose |
|---|---|
| `list` | List available skills |
| `install` | Install skills or packs |
| `audit-overlap` | Find duplicate or overlapping skills |

## Common Flags

| Flag | Purpose | Notes |
|---|---|---|
| `--skill <name>` or `-s <name>` | Install a specific skill | Repeatable |
| `--pack <name>` or `-P <name>` | Install a named pack | Repeatable |
| `--agent <name>` or `-a <name>` | Target an agent | Repeatable |
| `--global` or `-g` | Install globally | Requires explicit user intent |
| `--project` or `-p` | Install to current project | Default scope |
| `--upgrade` or `-u` | Replace installed skills | Confirmation expected |
| `--overwrite` or `-o` | Skip upgrade confirmation | Use only when explicitly requested |
| `--source-url <url>` | Clone from a git source | Use for external source selection |
| `--source-ref <ref>` | Pin branch, tag, or commit | Use for repeatable installs |
| `--full` or `-f` | Include descriptions in list output | Useful for selection |
| `--names` or `-n` | List names only | Useful for verification |
| `--count` or `-c` | Print count only | Useful for quick checks |

## Agent Targets

| Agent | Global target | Project target |
|---|---|---|
| `agent-skills` | `~/.agents/skills/` | `.agents/skills/` |
| `github-copilot` | `~/.github/skills/` | `.github/skills/` |
| `claude-code` | `~/.claude/skills/` | `.claude/skills/` |
| `codex` | `~/.codex/skills/` | `.agents/skills/` |

Use these paths for explanation and verification only. Prefer CLI flags over manually copying files.

## Export Scripts

Inside a cloned repository, use the bundled export scripts for manual zip packaging:

```bash
./scripts/export/export-skill.sh <skill-name>
```

On Windows PowerShell:

```powershell
.\scripts\export\export-skill.ps1 <skill-name>
```
