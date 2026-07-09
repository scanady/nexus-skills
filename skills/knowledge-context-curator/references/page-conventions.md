# Page Conventions

These are the default conventions for pages in a context repository. The repository's `SCHEMA.md` may override them.

This repository conforms to the [Open Knowledge Format (OKF)](https://github.com/GoogleCloudPlatform/knowledge-catalog) specification. All concept documents use standard markdown with YAML frontmatter.

Paths below use `context/` as the default root name. Substitute the actual root for the repository you are working in.

## Frontmatter

Every page begins with YAML frontmatter.

Default required fields:

```yaml
---
type: <source|entity|concept|synthesis|context-pack>
title: "Human-readable title"
description: "One-sentence summary for indexes and search."
tags: []
timestamp: "YYYY-MM-DDTHH:MM:SSZ"
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

OKF conformance requires only `type`. This repository requires all fields above for richer governance.

Non-source knowledge pages also include:

```yaml
sources: [source-slug-1, source-slug-2]
```

Source pages add:

```yaml
authors: []
url: ""
resource: ""
raw: "context/raw/<source-file>"
ingested: YYYY-MM-DD
```

The `resource` field (OKF RECOMMENDED) holds the canonical URI of the underlying asset when the concept describes a physical resource (a URL, API endpoint, database table, etc.). Omit it for abstract concepts.

Context-pack pages add:

```yaml
task: ""
required_pages: []
optional_pages: []
exclusions: []
freshness: ""
```

Frontmatter list values are bare slugs or repository-relative paths. Standard markdown links belong in the body.

## Links

Use standard markdown links for cross-references (OKF §5):

**Bundle-relative (recommended)** — begin with `/`, relative to the context root:

```markdown
[page title](/entities/page-slug.md)
[display text](/concepts/some-concept.md)
```

**Relative** — standard relative paths:

```markdown
[sibling page](./sibling.md)
[parent concept](../concepts/term.md)
```

Links assert a relationship; the type (depends-on, extends, contradicts, etc.) is conveyed by surrounding prose.

Every page should have at least one inbound link unless the schema marks it as an intentional root page. New orphan pages are ingest or curation bugs.

## Citations

Pages that draw on external sources should include a `# Citations` section at the bottom (OKF §8):

```markdown
# Citations
[1] [Source title](https://example.com/article)
[2] [Internal source brief](/sources/source-slug.md)
```

Use citations for external evidence. The frontmatter `sources:` field lists internal source briefs; the `# Citations` section lists external references and URLs.

## Page Sizing

- Soft cap: 400 lines or about 2,000 words.
- Hard cap: 800 lines.

If a page approaches the soft cap, consider whether a section should become its own page. If it exceeds the hard cap, split it.

## Naming

Page slugs are lowercase, hyphenated, and stable. Avoid special characters. Prefer descriptive slugs over date-only slugs.

The concept ID for OKF purposes is the file path within the context root minus the `.md` suffix (e.g., `entities/acme-corp` for `context/entities/acme-corp.md`).

Suggested locations:

- source pages: `context/sources/<source-slug>.md`
- entity pages: `context/entities/<entity-slug>.md`
- concept pages: `context/concepts/<concept-slug>.md`
- synthesis pages: `context/synthesis/<topic-or-question-slug>.md`
- context packs: `context/packs/<task-slug>.md`

## Body Structure

Source pages should capture the source's durable contribution, key claims, evidence notes, open questions, and where it fits.

Entity pages should define the entity, note relevant attributes, cite source briefs, and link related concepts.

Concept pages should define the concept, explain how it is used, document contested aspects, and link related concepts.

Synthesis pages should preserve durable analysis that future agents should not re-derive.

Context packs should define a task-specific load plan.

All page types may include a `# Citations` section at the bottom for external references.

## Source Grounding

Hedge claims that are not corroborated. When sources contradict, document both and label the contradiction unresolved. Do not silently pick a side.

For high-stakes claims, cite the source brief and be prepared to inspect the raw source.

## Voice

Use a neutral, concise, operational voice. The repository should be useful to both humans and agents. Avoid chatty phrasing and avoid copying the source author's prose except for short exact phrases where wording matters.
