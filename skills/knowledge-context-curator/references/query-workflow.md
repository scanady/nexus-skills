# Query Workflow

Use this workflow when answering a question from the context repository.

Paths below use `context/` as the default root name. The root is configurable and a project may host several roots; resolve which root applies to the question before reading the schema.

## Step 0: Read The Schema

Read `context/SCHEMA.md` if you have not already done so in this session. Follow any query-specific conventions it defines.

## Step 1: Start With Packs Or Index

If the query clearly maps to a recurring task, read the relevant pack in `context/packs/` first. Otherwise read `context/index.md` or the relevant index shard.

Use packs for task execution. Use the index for open-ended questions.

## Step 2: Select Candidate Pages

Build a short list of pages likely to answer the question. Be selective. If the index does not surface useful candidates, use:

```bash
python scripts/context_search.py "query terms" --context context --top 10
```

Search is a fallback when index-first navigation fails or the query is fuzzy.

## Step 3: Read Candidates

Read selected pages and follow only the most relevant links. If a claim matters for a high-stakes answer, trace from the page to its source brief and, when needed, to the raw source.

## Step 4: Answer With Traceability

Synthesize the answer in your own words. Cite context pages with double-bracket links. Mention source briefs or raw paths when the user needs verification.

If the repository contains contradictory or stale claims, surface that uncertainty explicitly. If the repository lacks coverage, say so and suggest what source, validation, or repository maintenance would fill the gap.

## Step 5: File Back When Useful

If the answer creates durable synthesis, offer to file it under `context/synthesis/`. Do not file trivial lookups or temporary task chatter. Update internal packs only when the question reveals a recurring task pattern.

When filing back, create frontmatter:

```yaml
---
type: synthesis
title: ""
question: "Original question"
sources_consulted: []
tags: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

Update the index and append a `query` log entry.

## Special Query Types

- "What context should I load for X?" - prioritize packs and recommend pack edits if coverage is weak.
- "What is missing?" - perform a targeted gap review and suggest sources or pages.
- "Compare X and Y" - read both pages and existing synthesis; strong file-back candidate.
- "What changed recently?" - read `context/log.md` and relevant `updated` fields.
- "Can an agent use this?" - check pack selectivity, freshness, exclusions, and source-critical claims.

## Anti-Patterns

- Reading the whole repository to be safe.
- Answering beyond repository coverage without labeling it as outside context.
- Citing distilled context for hard claims when the raw source should be checked.
- Filing every answer back as synthesis.