# Quickstart Strategy

Quickstart guides are functional walkthroughs. Each helps user accomplish specific goal. Frame around what user is trying to do, not features or APIs.

## File Set

Default layout when the user asks for onboarding documentation:

```text
docs/quickstart-<user-goal-1>.md
docs/quickstart-<user-goal-2>.md
docs/quickstart-<user-goal-3>.md
```

Adapt to repo's existing docs convention. README quick start covers minimal install + run; quickstart guides take over from there.

Goal-shaped names: `quickstart-send-your-first-message.md`, `quickstart-import-data.md`, `quickstart-deploy-to-production.md`. Not feature-shaped: `quickstart-messaging-api.md`.

## Sequencing the Guide Set

Order so first guide delivers quick first success; later guides build on it:

1. **First success** — Simplest meaningful workflow. Gives reader confidence.
2. **Common goal** — Most-used real-world workflow; ties multiple capabilities together.
3. **Going deeper** — More advanced workflow involving config, integration, or optimization.
4. **Mastery / extension** — Customization, automation, or contribution-adjacent workflows.

Cross-links between guides let experienced reader enter mid-sequence.

## Per-Guide Structure

Follow this order. Optional sections apply when guide is long or advanced enough to warrant — skip on short single-step guides.

1. **Title** — Goal-oriented: "Send your first message", "Import a dataset", "Run your first analysis".
2. **Who this is for** — One or two sentences: reader and situation.
3. **What you will accomplish** — Short bullet list of outcomes.
4. **Already familiar?** *(optional)* — Power-user shortcut: TL;DR commands or direct link to advanced section.
5. **Prerequisites** — Link back to README quick start, plus anything specific to this guide.
6. **Workflow** — Two to four numbered steps from start to outcome.
7. **Validation** — Concrete way to confirm success.
8. **Going further** *(optional)* — Extensions, options, integrations for readers ready to deepen.
9. **Troubleshooting** — Common failures with specific fixes.
10. **Next steps** — Links to next relevant guide and, when relevant, technical overview.

Keep each guide on one user goal. If it grows beyond that, split it.

## Workflow Pattern

Use this pattern for each numbered step. Use appropriate code language for project (bash, JSON, YAML, SQL, HTTP, JavaScript, Python, etc.).

````markdown
## 1. <Do the thing>

Briefly explain what this step does for the user and why it matters.

```bash
<copy-paste-ready command>
```

**Expected output**

```json
{
  "example": "actual response shape from the project"
}
```

**Validation**

```bash
<command or check that proves the step succeeded>
```
````

## Power-User Shortcut Pattern

When guide is long enough that experienced reader wants to skip narrative, add shortcut block near top:

```markdown
## Already familiar?

If you have completed the README quick start, jump to the [TL;DR commands](#tldr) or the [going further](#going-further) section.
```

Follow with optional `## TL;DR` block — commands and key params only. Skip both on short single-step guides.

## Going Further Pattern

When guide has meaningful advanced material, close with short section pointing at it:

```markdown
## Going further

- **Customize <option>** — What to change and what it changes.
- **Combine with <other capability>** — How to compose this workflow with another.
- **Read the internals** — Link to the relevant section of the [technical overview](technical-overview.md).
```

Few lines per item. Link out; don't expand inline.

## Progression Principles

- Open with step that produces visible progress fast.
- Build forward: create/initialize → use → validate → extend.
- Save IDs, tokens, filenames, or generated values explicitly before later steps reference them.
- Show before-and-after state when workflow changes something.
- End with next-step link that feels like natural continuation.

## API Example Requirements

When quickstart uses HTTP APIs, verify and include:

- HTTP method and path
- Auth and authorization requirements
- Required headers
- Request body fields, types, required vs optional, defaults
- Response shape, envelope conventions, timestamps, IDs, nullable fields
- Status codes for success and common errors
- Error format for likely mistakes

## CLI Example Requirements

When quickstart uses CLI, verify and include:

- Exact command and subcommand
- Required and optional flags, defaults, env vars
- Working directory assumptions
- Expected stdout, generated files, or side effects
- Exit behavior and exit codes for common failures

## UI Example Requirements

When quickstart uses UI, verify and include:

- Entry point (URL, screen, or menu path)
- Required fields and example values
- Visible confirmation action succeeded
- Where to find result afterward

## Troubleshooting Pattern

Make troubleshooting concrete and searchable:

```markdown
## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `ECONNREFUSED` when calling the API | The local server is not running | Start the server using the README quick start, then retry this step |
| `401 Unauthorized` | Missing or expired token | Regenerate the token using step 1 |
```

No generic advice like "check your setup" unless it links to specific check.

## Next Steps Pattern

Close every guide with a small set of links pointing the reader where to go next:

```markdown
## Next steps

- Continue to [Guide: <next goal>](quickstart-<next>.md).
- Skip ahead to [Guide: <advanced goal>](quickstart-<advanced>.md) if you are comfortable.
- Learn how this works inside in the [technical overview](technical-overview.md).
- Contribute or report issues — see [Contributing](../README.md#contributing).
```

## Functional Framing

- Lead each step with user outcome, not system action. "Create workspace" not "POST `/workspaces`".
- Technical details only when user must understand to succeed.
- Link to technical overview when reader might want internals: "Curious how this is stored? See the [technical overview](technical-overview.md)."

## Quality Checks

- Guide title names user goal.
- Reader can complete in roughly time promised.
- Every runnable step has expected output and validation check.
- Optional shortcut and "going further" present where helpful, absent where ceremonial.
- Technical internals linked, not embedded.
- Troubleshooting addresses real failures, not generic ones.
