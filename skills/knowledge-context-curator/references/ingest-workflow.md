# Ingest Workflow

Use this workflow when adding source material to the context repository.

Paths below use `context/` as the default root name. The root is configurable and a project may host several roots; substitute the actual root and confirm which root the source belongs in before placing files.

## Step 0: Read The Schema

Read `context/SCHEMA.md` first. Its page types, tag taxonomy, naming conventions, and workflow customizations override this reference.

## Step 1: Place The Raw Source

If the source is not already under `context/raw/`, place it there with a stable, slugified filename. Keep raw material immutable after placement.

For web articles or pasted text, save a markdown capture. For PDFs, keep the original PDF if feasible and extract text only as a helper artifact if needed.

## Step 2: Read The Source

For short sources, read the whole file. For long sources, read in chunks: first outline or section headings, then sections in order. Do not load a large source all at once if it would crowd out the rest of the ingest work.

For images, inspect only those that carry argument, evidence, structure, or content that cannot be inferred from surrounding text.

## Step 3: Surface Takeaways

Briefly tell the user what seems important, surprising, uncertain, or connected to existing repository content. In batch mode, keep this terse and record ambiguities in the log.

## Step 4: Survey Existing Context

Read `context/index.md` or relevant shards. Identify:

- existing pages to update
- likely new pages
- packs affected by the new source
- contradictions or freshness issues

Read candidate pages before deciding to create duplicates.

## Step 5: Create The Source Brief

Create `context/sources/<source-slug>.md` with source frontmatter:

```yaml
---
type: source
title: "Original source title"
authors: []
url: ""
raw: "context/raw/<source-slug>.<ext>"
ingested: YYYY-MM-DD
tags: []
entities: []
concepts: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

The body should summarize the source's durable contribution. Capture key claims, constraints, definitions, evidence, and open questions. Do not paraphrase the entire source.

End with links to pages the source touches.

## Step 6: Update Existing Pages

For each touched page, make focused edits that add what the new source contributes. Add the source brief slug to frontmatter `sources:` when appropriate.

Common patterns:

- Corroboration: add the new source as support.
- Contradiction: document both claims and mark the conflict unresolved.
- New dimension: add a narrow subsection rather than diluting existing prose.
- Freshness update: mark older claims as superseded or requiring review.

If a page crosses the hard size cap, split it during the ingest.

## Step 7: Create New Pages When Warranted

Create a new entity or concept page only when the topic is likely to recur or is first-class in the source. Every new page needs at least one inbound link from an existing page, source brief, or pack.

## Step 8: Update Affected Packs

If the source changes what an agent should load for a recurring task, update the relevant `context/packs/` page as internal maintenance. Add required pages sparingly and update freshness notes when the source affects time-sensitive claims.

Ask the user only when the recurring task boundary, authority, or risk level cannot be inferred from the source and existing context. Do not ask the user to define or maintain packs.

## Step 9: Update Index And Log

Add one-line entries for new pages and packs to `context/index.md` or the relevant shard. Append a log entry:

```markdown
## [YYYY-MM-DD] ingest | <source title>
- Added: [[source-slug]]
- Updated: [[page-a]], [[page-b]]
```

## Step 10: Report Back

Tell the user what was created, what was updated, what claims need caution, and what follow-up sources or validation would improve the repository. Mention internal maintenance, such as pack or index updates, only when it helps the user understand the outcome.

## Anti-Patterns

- Creating pages without inbound links.
- Treating an existing distilled page as source truth.
- Updating a context pack to load too much.
- Hiding contradictions by choosing one source silently.
- Letting schema changes remain implicit.