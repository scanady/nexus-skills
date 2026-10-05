# Nexus Skills CLI Reference

Run `<runner> --help` first (bare, no command after it). It lists the current commands, flags, defaults, and supported agents, and it wins over this file if they differ. This reference adds the safe-use notes and target paths the help text does not. Prefer the shortest command that satisfies the user's stated scope.

Never write `install --help` or any `<command> --help`: older versions of the CLI ignore `--help` after a command and run it.

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
| `list` | List available skills. `--installed` (`-i`) lists what is installed in a target |
| `install` | Install skills or plugins. Skips installed skills unless `--upgrade` is set |
| `upgrade` | Replace only the skills already installed in the target. Never adds a skill |
| `remove` | Delete installed skills. Needs `--skill` or `--plugin` |
| `audit-overlap` | Find duplicate or overlapping skills |

The command comes first. The CLI rejects unknown commands, unknown options, stray words, and unknown skill, plugin, or agent names before it writes anything. `--help` anywhere prints help and runs nothing.

For remove operations, use `remove --skill <name>` with the scope and agent the user named. It keeps `.env` and `.env.local` files in place by default; `--yes` takes that default without prompting. `--delete-env` also deletes them.

## Common Flags

| Flag | Purpose | Notes |
|---|---|---|
| `--skill <name>` or `-s <name>` | Select a specific skill | Repeatable or comma-separated |
| `--plugin <name>` or `-P <name>` | Select every skill in a plugin (`--pack` is the old spelling) | Repeatable or comma-separated |
| `--agent <name>` or `-a <name>` | Target an agent | Repeatable or comma-separated |
| `--global` or `-g` | Install globally | Requires explicit user intent |
| `--project` or `-p` | Install to current project | Default scope |
| `--upgrade` or `-u` | `install` only: also replace installed skills | Confirmation expected |
| `--yes` or `-y` (same as `--overwrite`, `-o`) | Take the default answers without prompting | Required in a non-interactive shell, where a prompt is an error. With `remove`, keeps `.env` files. Invalid on `install` without `--upgrade` |
| `--delete-env` | `remove` only: also delete `.env` and `.env.local` | Use only when explicitly requested |
| `--source-url <url>` | Clone from a git source | Use for external source selection |
| `--source-ref <ref>` | Pin branch, tag, or commit | Needs `--source-url` |
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

To check a target before changing it, run `list --installed --full` with the same scope and agent flags.

## Export Scripts

Inside a cloned repository, use the bundled export scripts for manual zip packaging:

```bash
./scripts/export/export-skill.sh <skill-name>
```

On Windows PowerShell:

```powershell
.\scripts\export\export-skill.ps1 <skill-name>
```
