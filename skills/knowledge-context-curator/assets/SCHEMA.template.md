# Context Repository Schema

This file is the configuration for this context repository. It documents repository conventions, page types, agent-managed context-pack rules, tag taxonomy, and workflow customizations. Agents read this first when entering the repository, and its conventions override the defaults documented in the `knowledge-context-curator` skill.

This repository conforms to the [Open Knowledge Format (OKF)](https://github.com/GoogleCloudPlatform/knowledge-catalog) specification. Every concept document has parseable YAML frontmatter with a non-empty `type` field. Cross-references use standard markdown links. Index and log files follow OKF §6 and §7 conventions.

This file is co-evolved with the user when human judgment is needed. The agent may update repository mechanics when patterns appear, but should ask before changing conventions that affect meaning, source authority, retention, deletion, or user-visible scope.

## Repository Location

- Context root: `{{CONTEXT_ROOT}}/`
- Raw sources: `{{CONTEXT_ROOT}}/raw/`
- Asset/image storage: `{{CONTEXT_ROOT}}/raw/assets/`
- Context packs: `{{CONTEXT_ROOT}}/packs/`

This project may host additional context roots (for example `context-core/`, `context-product/`, `context-customer/`). Each root is governed independently and has its own `SCHEMA.md`. Document any cross-root relationships under [Workflow Customizations](#workflow-customizations).

## OKF Conformance

This repository follows OKF. Key conformance rules:

- Every `.md` file (except `index.md` and `log.md`) has YAML frontmatter with a non-empty `type` field.
- Cross-references use standard markdown links: `[title](/path/to/concept.md)` (bundle-relative, starting with `/`) or `[title](./relative.md)`.
- `index.md` files use the format: `* [Title](relative-url) - description`.
- `log.md` uses date headings (`## YYYY-MM-DD`) with newest entries first.
- Consumers must tolerate unknown `type` values, unknown frontmatter keys, and broken links.
- The `type` field is the only strictly required frontmatter key for OKF conformance. This repository also requires `title`, `description`, `tags`, `timestamp`, `created`, and `updated` for richer governance.

## Layers

- Evidence layer: immutable source material under `{{CONTEXT_ROOT}}/raw/`.
- Knowledge layer: distilled source, entity, concept, and synthesis pages.
- Context layer: agent-managed context packs under `{{CONTEXT_ROOT}}/packs/`.
- Governance layer: schema, index, log, lint rules, sharded indexes, and curation notes.

## Page Types

This repository uses these page types, each with a dedicated subdirectory:

- `source` (in `{{CONTEXT_ROOT}}/sources/`) - one source brief per ingested source.
- `entity` (in `{{CONTEXT_ROOT}}/entities/`) - pages about specific people, products, organizations, systems, documents, or places.
- `concept` (in `{{CONTEXT_ROOT}}/concepts/`) - pages about ideas, rules, frameworks, methods, or domain abstractions.
- `synthesis` (in `{{CONTEXT_ROOT}}/synthesis/`) - cross-source analyses, comparisons, and durable query answers.
- `context-pack` (in `{{CONTEXT_ROOT}}/packs/`) - internal load plans for recurring agent tasks.

Add additional types here as the repository evolves. Do not create a new type for a one-off page; use tags instead.

## Context Pack Rules

Context packs are agent-managed. Each context pack must define:

- `task` - the recurring task the pack supports.
- `required_pages` - pages an agent should load before performing the task.
- `optional_pages` - pages that may help depending on the request.
- `exclusions` - pages, tags, or topics the agent should avoid for this task.
- `freshness` - when the pack or its required pages should be reviewed.

Packs should be selective. A pack that loads most of the repository is a signal that the repository needs better indexes or narrower packs. Ask the user about pack boundaries only when they depend on human judgment about task scope, authority, exclusions, or risk.

## Tag Taxonomy

(Empty initially. Add tags here as you adopt them, with one-line descriptions. Keep this list small and disciplined.)

Example structure:

- `review-boundary` - pages defining what an agent may and may not decide.
- `source-critical` - pages whose claims should be checked against raw sources before use.
- `stale-risk` - pages likely to expire or drift.
- `contested` - pages where sources contradict.

## Page Sizing

- Soft cap: 400 lines / about 2,000 words. Consider splitting beyond this.
- Hard cap: 800 lines. Must split.

## Frontmatter Requirements

Every page must have (OKF-required marked with *):

- `type` * — the only field required by the OKF spec for conformance
- `title` — display name (OKF RECOMMENDED)
- `description` — single-sentence summary for indexes and search (OKF RECOMMENDED)
- `tags` — cross-cutting classification (OKF optional)
- `timestamp` — ISO 8601 datetime of last meaningful change (OKF RECOMMENDED)
- `created` — creation date (extension field)
- `updated` — last update date (extension field)

Type-specific fields:

- `source` pages: `authors`, `url` if applicable, `raw`, `ingested`
- `source` pages: `resource` — canonical URI of the original source (OKF RECOMMENDED when describing a physical asset)
- Non-source knowledge pages: `sources` listing source briefs drawn from
- `context-pack` pages: `task`, `required_pages`, `optional_pages`, `exclusions`, `freshness`

Frontmatter lists use bare slugs or repository-relative paths. The body uses standard markdown links for cross-references.

## Cross-Reference Convention

Use standard markdown links for all cross-references (OKF §5):

- Bundle-relative (recommended): `[page title](/entities/page-slug.md)`
- Relative: `[page title](./sibling.md)` or `[page title](../concepts/term.md)`

Links express relationships; the type of relationship is conveyed by surrounding prose.

## Citations Convention

Pages that draw on external sources should include a `# Citations` section at the bottom (OKF §8):

```markdown
# Citations
[1] [Source title](https://example.com/article)
[2] [Internal source brief](/sources/source-slug.md)
```

## Index Structure

(Update this section when sharding.)

Currently flat: a single `{{CONTEXT_ROOT}}/index.md` listing all pages and packs using standard markdown links:

```markdown
* [Page Title](relative-path.md) - one-line description
```

When the repository passes about 150 pages or `index.md` exceeds 300 lines, shard into `{{CONTEXT_ROOT}}/indexes/<type>.md` and update this section.

## Workflow Customizations

(Empty initially. Document deviations from the default initialize, ingest, query, curate, package, or lint workflows here.)

## User Preferences

(Empty initially. Capture style, naming, source-quality, scope, and validation preferences here so they persist across sessions.)

## Lint Cadence

- Structural lint: after every 5 ingests.
- Semantic lint: weekly or after every 20 ingests.
- Pack freshness check: monthly or before high-stakes reuse.

Adjust based on the repository's growth rate and risk profile.