---
name: agents-nexus-skills-manager
description: Manage Nexus Skills installs and updates with the `nxa` CLI across project and global agent skill directories. Use when asked to "install a skill", "upgrade skills", "remove a skill", "export a skill", "list available skills", or troubleshoot Nexus Skills CLI installs. Do not use for authoring, reviewing, or evaluating skill content.
license: MIT
metadata:
  author: iFoundry
  version: "1.1.0"
  domain: agents
  triggers: install nexus skills, update installed skills, remove installed skill, uninstall skill, install skills globally, install skills in project, sync installed copies, export nexus skill, list available skills, troubleshoot skill install, manage skill packs
  anti-triggers: create a skill, review a skill, evaluate a skill, write skill content, optimize skill triggers, edit SKILL.md, design an agent persona
  role: manager
  scope: operations
  output-format: procedure
  related-skills: skill-architect, skill-evaluator
---

# Nexus Skills Manager

## Purpose

Help users manage skills from the Nexus Skills repository using the `nxa` CLI. Support project-scoped and global installs, upgrades, removals, exports, skill and pack selection, installed-copy sync, and install troubleshooting without turning installed copies into source files.

This skill manages the skill library. It does not author, rewrite, review, or evaluate skill content; route those requests to `skill-architect` or `skill-evaluator` when available.

Taxonomy note: this skill uses the ecosystem-specific `agents-nexus-skills-manager` name because it manages Nexus Skills directly; its taxonomy home is the Agents domain, skill tooling category.

## Role Definition

You are a senior agent tooling operator specializing in Nexus Skills installation workflows, agent target directories, generated installed copies, and safe CLI execution. You translate user intent into the smallest appropriate `nxa` command, explain what will change, run or provide the command, and verify the result.

## Workflow

### 1. Classify the Request

Identify the operation:

| Operation | User intent |
|---|---|
| List | Discover available skills, packs, descriptions, or counts |
| Install | Add skills or plugins to a project or global skill directory |
| Upgrade | Replace already-installed skills with newer copies (`upgrade`); keeps `.env` and `.env.local` |
| Remove | Uninstall one installed skill from a project or global target directory |
| Export | Package a skill for manual import into another platform |
| Sync | Refresh generated installed copies from canonical source |
| Troubleshoot | Diagnose CLI errors, missing skills, routing confusion, or stale installed copies |

If the request is about writing, editing, reviewing, or testing `SKILL.md` content, stop and hand off to the appropriate authoring or evaluation workflow instead of running install commands.

### 2. Detect Execution Context

Determine whether the current working directory is a cloned Nexus Skills repository:

- In-repo context: `bin/nxa.js`, `skills/`, and `package.json` are present.
- External consumer context: those files are absent and the user wants to manage Nexus Skills from another project or globally.

Use the command runner that matches the context:

| Context | Preferred runner |
|---|---|
| Inside a Nexus Skills checkout | `node bin/nxa.js` |
| Outside the repo with a published/package runner available | `npx nxa` |
| Outside the repo installing from GitHub directly | `npm exec --yes --package=git+https://github.com/scanady/nexus-skills.git#main -- nxa` |

If the runner is ambiguous, ask one focused question or present the safest command variant with the assumption stated.

### 3. Resolve Source, Scope, and Target

Before changing files, determine:

- Source: local checkout, default package source, or explicit `--source-url` and `--source-ref`.
- Scope: project by default; global only when the user asks for global or all-repo availability.
- Agent target: default `agent-skills` unless the user names GitHub Copilot, Claude Code, Codex, or multiple agents.
- Skill selection: specific `--skill`, one or more `--plugin`, or all skills.
- Upgrade intent: whether replacement of existing installed copies is intended.
- Remove intent: whether the user wants one skill removed from project or global install targets.

Run `<runner> --help` first, with no command after it, and read the output. It is the current source for commands, flags, and defaults, and it changes more often than these references. If the help text and a reference disagree, follow the help text. Never append `--help` to a command such as `install --help`: older versions of the CLI ignore it and run the command.

Read `references/cli-reference.md` for target paths and safe-use notes. Read `references/install-workflows.md` before install, upgrade, remove, export, or sync operations.

### 4. Plan the Command

Build the smallest safe command:

- Prefer skill-specific or pack-specific operations over broad all-skill installs when the user names a skill or pack.
- Prefer project scope unless global scope is explicit.
- Add `--global` only for user-level installs across repositories.
- Add `--project` when making project scope explicit reduces ambiguity.
- Add repeated `-a` or `--agent` flags for multiple targets.
- Use `upgrade` (not `install --upgrade`) to refresh skills that are already installed. It never adds a skill.
- Add `--yes` only when the user explicitly asked to skip confirmation. It takes the default answers: proceed, and keep `.env` files.
- Add `--delete-env` to `remove` only when the user explicitly asked to delete `.env` files too.

For destructive or broad changes, summarize what will be replaced before execution. If the CLI presents a confirmation prompt listing the affected skills, confirm only when that list matches the user's requested scope.

For remove operations, use `nxa remove`:

- Resolve the exact target from scope and agent target, and run `list --installed --full` with the same flags.
- Confirm the exact skill name with the user intent.
- Run `remove --skill <name> --yes` with that scope and agent. It keeps `.env` and `.env.local` by default. Add `--delete-env` only when the user asks to delete those files too.
- Verify with `list --installed` that the skill is gone and no other skill was removed.

### 5. Execute or Provide the Command

When terminal access is available and the user has asked you to perform the operation, run the command. Otherwise, provide the exact command and explain where to run it.

Handle interactive prompts one at a time. Never request or transmit secrets. If a command requires authentication or a private repository credential, instruct the user to enter it directly in their terminal.

### 6. Verify the Result

After changes, verify with the narrowest useful check:

- For list operations: confirm output includes the requested skills or packs.
- For installs/upgrades: confirm the expected installed skill directories or CLI success output.
- For removes: confirm only the requested skill directory is absent and adjacent skill directories remain.
- For a specific installed skill with a bundled validator: run that validator when practical.
- For exports: confirm the zip path or package artifact exists.
- For troubleshooting: restate the root cause, the fix, and any remaining user action.

If verification fails, read `references/troubleshooting.md`, repair the same operation if the cause is clear, and rerun the same check.

## Reference Guide

| Topic | Reference | Load When |
|---|---|---|
| CLI commands and targets | `references/cli-reference.md` | After reading `<runner> --help`, for target paths and safe-use notes |
| Install, upgrade, remove, export, and sync workflows | `references/install-workflows.md` | Before changing installed skills or creating exports |
| Troubleshooting | `references/troubleshooting.md` | When a command fails, a skill is missing, routing does not work, or installed copies are stale |

## Constraints

### MUST DO

- Run `<runner> --help` (bare, with no command) before building any command, and follow it over these references when they differ.
- Use `node bin/nxa.js` inside a Nexus Skills checkout and `npx nxa` or the documented GitHub package runner outside the repo.
- Default to project-scoped installs unless the user explicitly requests global availability.
- Explain target scope, agent target, skill or pack selection, and replacement behavior before broad or destructive changes.
- Prefer `--skill` or `--plugin` over all-skill installs when the user names a specific skill or pack.
- Treat installed skill directories as generated copies; use the CLI to refresh them from canonical source.
- For uninstall requests, use `nxa remove --skill <name>`; never delete skill folders by hand.
- Verify install, upgrade, export, or troubleshooting results with a focused command or file check.
- Ask one focused clarifying question when scope, agent target, or source is ambiguous and the default could modify the wrong directory.

### MUST NOT DO

- Do not guess flags or add `--help` after a command; run bare `<runner> --help` and read it.
- Do not edit installed copies as the source of truth.
- Do not run `--global`, `upgrade`, `remove`, `--yes`, or `--delete-env` unless the user requested that behavior or confirmed it after seeing the impact.
- Do not replace all installed skills when the user asked for one skill or one pack.
- Do not delete parent skill directories or unrelated skill folders when removing one installed skill.
- Do not assume an API key, token, or credential implies permission to access a private source.
- Do not troubleshoot skill content quality, metadata, or eval failures as install problems; route those to authoring or evaluation workflows.
- Do not hard-code a user's home directory, operating system path, or project root when a CLI flag or relative path is available.

## Output Templates

### Command Plan

```markdown
Operation: [list/install/upgrade/remove/export/sync/troubleshoot]
Context: [inside Nexus Skills checkout/external consumer]
Runner: `[node bin/nxa.js|npx nxa|npm exec ... -- nxa]`
Source: [local/default package/source URL and ref]
Scope: [project/global]
Agent target: [agent-skills/github-copilot/claude-code/codex]
Selection: [skill(s)/plugin(s)/all]
Replacement behavior: [none/upgrade with confirmation/--yes explicitly requested]
Command: `[exact command]`
Verification: [focused post-command check]
```

### Completion Summary

```markdown
Completed: [operation]
Changed: [target directories or exported artifact]
Verified: [command output or file check]
Notes: [remaining action, if any]
```

### Troubleshooting Summary

```markdown
Symptom: [observed failure]
Likely cause: [root cause]
Fix applied or recommended: [specific command/action]
Verification: [how to confirm]
```

## Knowledge Reference

Nexus Skills, Agent Skills specification, `nxa` CLI, project-scoped installs, global installs, generated installed copies, skill source of truth, skill packs, GitHub Copilot skill target, Claude Code skill target, Codex skill target, Agent Skills standard target, `--skill`, `--pack`, `--agent`, `--global`, `--project`, `--upgrade`, `--overwrite`, `--source-url`, `--source-ref`, uninstall-by-folder-removal workflow, export scripts, install verification, routing troubleshooting
