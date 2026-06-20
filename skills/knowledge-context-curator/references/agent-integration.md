# Agent Integration

Use this reference when the user wants future agents to notice and use the context repository automatically.

## Ask First

Do not edit project-level agent instruction files without approval. Show the proposed stanza and ask where to place it.

Common files include:

- `AGENTS.md`
- `.github/copilot-instructions.md`
- `CLAUDE.md`
- `GEMINI.md`

Use whichever file the project already uses. If several exist, ask the user which should be authoritative.

## Recommended Stanza (Single Root)

Replace `<context-root>` with the actual directory name (default `context`).

```markdown
## Context Repository

This project uses a curated context repository under `<context-root>/`.

Before answering repository-specific questions or performing recurring workflows, read `<context-root>/SCHEMA.md`, then navigate via `<context-root>/index.md` or relevant context packs in `<context-root>/packs/`. Preserve source traceability: raw sources live under `<context-root>/raw/`, distilled source briefs under `<context-root>/sources/`, and reusable task load plans under `<context-root>/packs/`.

Use index-first navigation. Use search only when the index or packs do not surface the needed pages. Update `<context-root>/index.md` and `<context-root>/log.md` whenever creating or materially changing context pages.
```

## Short Variant

```markdown
Use `<context-root>/` as the project's curated agent context repository. Read `<context-root>/SCHEMA.md` first, navigate through `<context-root>/index.md` and `<context-root>/packs/`, and preserve source traceability to `<context-root>/raw/` and `<context-root>/sources/`.
```

## Multi-Root Variant

Use this when the project hosts more than one context root (for example `context-core/`, `context-product/`, `context-customer/`). List each root and its scope so the agent picks the right one.

```markdown
## Context Repositories

This project hosts multiple curated context roots. Each is independently governed and has its own `SCHEMA.md`, indexes, packs, and logs.

- `context-core/` - <one-line scope, e.g. shared definitions, decisions, and architecture>
- `context-product/` - <one-line scope, e.g. product strategy, specs, and roadmaps>
- `context-customer/` - <one-line scope, e.g. customer research, calls, and synthesis>

When a task starts, identify which root applies, then read that root's `SCHEMA.md` and navigate via its `index.md` or relevant `packs/`. Preserve source traceability and keep raw sources immutable. Update the chosen root's `index.md` and `log.md` whenever creating or materially changing context pages. Do not silently copy material between roots; cross-root links are allowed but each root must remain navigable on its own.
```

## When To Integrate

Recommend integration after initialization or after the first successful ingest. If the repository is experimental or temporary, skip integration until conventions stabilize.

## What Not To Do

- Do not add integration text that claims agents must always read the entire repository.
- Do not hide task-specific loading rules outside `<context-root>/packs/`.
- Do not hard-code `context/` as the root in agent instructions; use the actual directory name(s) the project uses.
- Do not create a new agent instruction file when the project already has an authoritative one unless the user asks.