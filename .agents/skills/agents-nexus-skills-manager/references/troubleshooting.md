# Troubleshooting

Use this reference when a command fails, installed skills do not appear, or the wrong skill version seems active.

## Skill Not Found

Checks:

1. Run `<runner> list --names` and confirm the exact folder name.
2. If outside the repo, confirm the package/source is Nexus Skills and not another package with an `nxa` binary.
3. If using `--source-url`, confirm `--source-ref` points to a branch, tag, or commit containing the skill.

Fix:

- Correct the skill name or source ref, then rerun the install command.

## Installed Copy Is Stale

Cause:

- Installed copies are generated files and do not update when source files change.

Fix:

```bash
<runner> install --upgrade --skill <skill-name>
```

Verify the installed `SKILL.md` contains the expected version or wording.

## Wrong Scope

Symptoms:

- Skill works in one repository but not another.
- Skill appears globally but not in the current project, or vice versa.

Checks:

- Confirm whether the previous command used `--project` or `--global`.
- Confirm which agent target was selected.

Fix:

- Reinstall with the intended scope and agent target.

## Upgrade Prompt Lists Unexpected Skills

Cause:

- A broad `--upgrade` may replace every installed skill in the target directory.

Fix:

- Answer no, then rerun with `--skill <name>` or `--pack <name>`.

## Routing Does Not Pick the Installed Skill

Checks:

1. Confirm the skill is installed in the target agent's expected directory.
2. Confirm the agent client supports Agent Skills or the selected target format.
3. Restart or reload the agent client if it caches skill metadata.
4. If routing still fails, evaluate the skill description and triggers with a skill-authoring workflow.

## Permission or Credential Failure

Do not ask the user to paste secrets. Ask the user to authenticate in their terminal or confirm access to the private git source, then rerun the same command.
