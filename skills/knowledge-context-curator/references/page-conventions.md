# Page Conventions

These are the default conventions for pages in a context repository. The repository's `SCHEMA.md` may override them.

Paths below use `context/` as the default root name. Substitute the actual root for the repository you are working in.

## Frontmatter

Every page begins with YAML frontmatter.

Default required fields:

```yaml
---
type: <source|entity|concept|synthesis|context-pack>
title: "Human-readable title"
tags: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

Non-source knowledge pages also include:

```yaml
sources: [source-slug-1, source-slug-2]
```

Source pages add:

```yaml
authors: []
url: ""
raw: "context/raw/<source-file>"
ingested: YYYY-MM-DD
```

Context-pack pages add:

```yaml
task: ""
required_pages: []
optional_pages: []
exclusions: []
freshness: ""
```

Frontmatter list values are bare slugs or repository-relative paths. Double-bracket links belong in the body.

## Links

Use double-bracket links for cross-references:

```markdown
[[page-slug]]
[[page-slug|display text]]
```

Every page should have at least one inbound link unless the schema marks it as an intentional root page. New orphan pages are ingest or curation bugs.

## Page Sizing

- Soft cap: 400 lines or about 2,000 words.
- Hard cap: 800 lines.

If a page approaches the soft cap, consider whether a section should become its own page. If it exceeds the hard cap, split it.

## Naming

Page slugs are lowercase, hyphenated, and stable. Avoid special characters. Prefer descriptive slugs over date-only slugs.

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

## Source Grounding

Hedge claims that are not corroborated. When sources contradict, document both and label the contradiction unresolved. Do not silently pick a side.

For high-stakes claims, cite the source brief and be prepared to inspect the raw source.

## Voice

Use a neutral, concise, operational voice. The repository should be useful to both humans and agents. Avoid chatty phrasing and avoid copying the source author's prose except for short exact phrases where wording matters.