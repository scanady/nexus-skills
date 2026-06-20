# Scaling Playbook

The goal is to keep context-loading cost roughly bounded as the repository grows.

Paths and CLI examples below use `context/` as the default root name. The root is configurable; substitute the actual root, and apply scaling decisions per root in multi-root projects.

## Failure Modes

- The index becomes too large to read cheaply.
- Pages grow unboundedly.
- Packs load too many pages.
- Search replaces curated navigation.
- Source traceability weakens as pages are reused.
- Tags multiply until they stop helping.

## Threshold 1: Under 50 Pages

A flat `context/index.md` is enough. Use standard subdirectories from the start because they are cheap and make future growth easier.

## Threshold 2: About 150 Pages Or `index.md` Over 300 Lines

Shard the index:

1. Create `context/indexes/` if it does not exist.
2. Move entries into `indexes/sources.md`, `indexes/entities.md`, `indexes/concepts.md`, `indexes/synthesis.md`, and `indexes/packs.md`.
3. Replace top-level `index.md` with a directory of shards and counts.
4. Update `SCHEMA.md` to document the sharded structure.

If a shard later exceeds 300 lines, shard by domain-specific subcategory.

## Threshold 3: About 300 Pages

Use `scripts/context_search.py` as a routine fallback when index navigation does not surface candidates.

Examples:

```bash
python scripts/context_search.py "review boundary" --context context --top 10
python scripts/context_search.py "" --context context --backlinks compliance-review-boundaries
python scripts/context_search.py "" --context context --top-linked 10
```

Index-first navigation remains the default.

## Threshold 4: About 500 Pages

Increase lint and curation cadence. Watch for:

- packs that should split by task variant
- pages that should split into narrower concepts
- tags that should be pruned
- source-critical claims that need re-verification

Consider using `--cache` with search if repository size makes repeated runs slow.

## Threshold 5: About 1,000+ Pages

Reassess whether markdown is still the right storage layer. If most queries are relational, permissioned, transactional, or require strict constraints, recommend a database or graph-backed system.

The markdown repository remains valuable migration input because pages have frontmatter, source pointers, and explicit links.

## Pack Scaling Rules

- If a pack requires more than about 12 pages, split the task or move some pages to optional.
- If many packs repeat the same required set, create a shared prerequisite concept page and link to it.
- If a pack's freshness rules differ by page, make those rules explicit next to each required page.
- If agents routinely need pages outside a pack, update the pack or create a sibling pack for that task variant.