# Install Workflows

Use these patterns after selecting the correct runner from `cli-reference.md`.

## List Available Skills

```bash
<runner> list --full
```

Use `--names` for terse verification or when matching an exact skill name.

## Install One Skill Into the Current Project

```bash
<runner> install --skill <skill-name> --project
```

Add an agent target when the user names one:

```bash
<runner> install --skill <skill-name> --project -a github-copilot
```

## Install One Skill Globally

Only use global scope when requested:

```bash
<runner> install --skill <skill-name> --global
```

## Install a Pack

```bash
<runner> install --pack <pack-name> --project
```

Repeat `--pack` for multiple packs.

## Install to Multiple Agents

```bash
<runner> install --skill <skill-name> -a github-copilot -a claude-code -a codex
```

## Upgrade Existing Installed Copies

Prefer narrow upgrades:

```bash
<runner> install --upgrade --skill <skill-name>
```

For broad upgrades, first explain that installed copies will be deleted and replaced:

```bash
<runner> install --upgrade
```

Use `--overwrite` only if the user explicitly asked to skip confirmation.

## Remove or Uninstall One Installed Skill

`nxa` does not currently have an uninstall command. Remove a skill by deleting that skill folder from the resolved target directory.

Linux or macOS shell:

```bash
rm -rf <target-dir>/<skill-name>
```

PowerShell:

```powershell
Remove-Item -Recurse -Force <target-dir>/<skill-name>
```

Before deleting:

- Confirm scope (`--project` vs `--global`) and agent target path.
- Confirm the exact skill folder name.
- Remove only one folder unless the user asked for multiple removals.

## Install From an Explicit Source

Use an explicit source for repeatable team installs or non-default repositories:

```bash
<runner> install --source-url <git-url> --source-ref <branch-tag-or-commit> --skill <skill-name>
```

## Export a Skill

Inside a cloned repo:

```bash
./scripts/export/export-skill.sh <skill-name>
```

Confirm the output zip exists after export.

## Verification Patterns

- Run `<runner> list --names` to verify a skill exists in the available source.
- Check command output for installed or upgraded skill names.
- For a specific project install, confirm the expected skill directory exists under the target agent path.
- For a remove operation, confirm the requested skill directory is absent and neighboring skill folders remain.
- If an installed skill includes a local validation script, run it after upgrade when practical.
