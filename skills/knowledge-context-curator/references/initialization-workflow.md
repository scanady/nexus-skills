# Initialization Workflow

Use this workflow when creating a new context-root repository, or when adding another root to a project that already has one.

## Step 1: Confirm Location And Root Name

Ask the user where the repository should live and what the root directory should be called. Defaults:

- Location: project root.
- Name: `context/`.

Alternatives are fully supported. Use the user's preferred name (for example `knowledge/`, `kb/`, `docs/context/`). Record the chosen root in `SCHEMA.md`.

### Multiple Roots In One Project

A project may host several roots when knowledge has clearly separate audiences or domains, for example `context-core/`, `context-product/`, `context-customer/`. Each root is initialized independently and remains self-contained.

When the user signals multiple roots are needed:

1. Confirm the names and what each root will hold.
2. Initialize each root with its own `init_context.py` invocation.
3. Note the sibling roots in each `SCHEMA.md` under Workflow Customizations so future agents understand the split.

## Step 2: Bootstrap Structure

Run once per root:

```bash
python scripts/init_context.py <project-root> --context-dir <root-name>
```

Examples:

```bash
python scripts/init_context.py .                                # creates context/
python scripts/init_context.py . --context-dir knowledge        # creates knowledge/
python scripts/init_context.py . --context-dir context-core     # multi-root: core
python scripts/init_context.py . --context-dir context-product  # multi-root: product
```

The script creates the following inside the chosen root (paths shown for the default `context/`; substitute the root you used):

- `context/SCHEMA.md`
- `context/index.md`
- `context/log.md`
- `context/.page-template.md`
- `context/.context-pack-template.md`
- `context/raw/assets/`
- `context/sources/`
- `context/entities/`
- `context/concepts/`
- `context/synthesis/`
- `context/packs/`
- `context/indexes/`

It is idempotent and does not overwrite existing files. The generated `SCHEMA.md` records the chosen root name in its Repository Location section.

## Step 3: Read And Accept Default Schema

Read the generated `<context-root>/SCHEMA.md`. Use the default page types, tag taxonomy, source-quality rules, naming conventions, and pack conventions unless the user's stated goal requires a change.

Ask about schema customization only when human guidance is needed, for example:

- the user requested multiple audiences, domains, or roots
- the source material needs a page type the schema does not cover
- the user has a specific governance, retention, or source-quality rule
- the default naming or tag conventions would make the repository harder for the user to validate

For hands-off setup, keep defaults and note that the schema should evolve after the first few ingests.

## Step 4: Defer Task Packs Until Patterns Appear

Do not ask the user to define starter packs during initialization. Packs are an internal agent optimization.

If the user has already named a recurring workflow, create a starter pack only when there is enough repository content to make it useful. Otherwise, wait until repeated queries, ingests, or reviews reveal a real task pattern. Avoid speculative packs.

## Step 5: Propose Agent Integration

Offer to add a short stanza to the project's agent instruction file so future agents know the repository (or set of repositories) exists and which root applies for which work. Do not write that file without approval.

See `agent-integration.md` for the recommended stanzas, including the multi-root variant.

## Step 6: Log Initialization

Append to `<context-root>/log.md`:

```markdown
## [YYYY-MM-DD] initialize | Created context repository
```

Include notable customizations and, if part of a multi-root project, name the sibling roots.