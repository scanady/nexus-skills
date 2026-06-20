# Curation Workflow

Use this workflow to improve repository quality after repeated ingests, lint findings, or user feedback.

Paths below use `context/` as the default root name. The root is configurable and a project may host several roots; curate one root at a time and substitute the actual root name.

## Curation Goals

Curation keeps the repository usable as it grows. It should improve:

- navigability
- source traceability
- page atomicity
- pack usefulness
- freshness visibility
- contradiction handling
- tag discipline

## Step 1: Establish Scope

Infer whether the curation pass is repository-wide or targeted to a topic, page type, pack, or recent ingest batch.

Ask for clarification only when the user's request is ambiguous, destructive, or could reasonably apply to more than one target. For example, if the user says "delete x" and `x` could mean a source file, source brief, page, claim, tag, or topic, ask which target they mean before editing.

For large repositories, prefer targeted passes.

## Step 2: Read Governance Surfaces

Read:

- `context/SCHEMA.md`
- `context/index.md` or relevant shards
- recent entries in `context/log.md`
- relevant lint output if available

## Step 3: Identify Issues

Look for:

- duplicate or overlapping pages
- oversized pages that should split
- orphan pages
- stale or source-critical claims
- vague index summaries
- tags outside the declared taxonomy
- packs that load too much or too little
- claims that lack source pointers
- concepts mentioned often but missing a page

## Step 4: Propose Or Apply Edits

For low-risk structural fixes, apply focused edits. Ask only when human judgment is needed because the target, meaning, authority, freshness, destructive scope, or intended outcome is unclear.

Safe structural fixes include:

- adding missing index entries
- correcting obvious broken links
- tightening one-line summaries
- adding missing inbound links from source briefs
- updating `updated` dates after real edits

Higher-risk changes include:

- merging contested pages
- removing claims
- changing decision boundaries in context packs
- marking a source superseded
- revising schema conventions

For higher-risk changes, present the smallest useful decision to the user in plain language. Avoid asking them to choose repository mechanics such as page type, tag names, or pack structure unless those mechanics are the actual subject of the request.

## Step 5: Update Schema When Patterns Repeat

If the same issue appears repeatedly, change the convention rather than fixing symptoms. Examples:

- repeated tag drift means the taxonomy needs pruning or examples
- repeated oversized pages mean page boundaries are too broad
- repeated pack bloat means packs need required/optional thresholds
- repeated source-trace gaps mean frontmatter rules need tightening

## Step 6: Log The Curation

Append:

```markdown
## [YYYY-MM-DD] curate | <scope>
- Changed: [[page-a]], [[page-b]]
- Reason: <brief reason>
```

## Step 7: Report Back

Briefly tell the user what changed, what you handled as repository maintenance, and what still needs human judgment. Do not expose pack, index, tag, or schema details unless they matter to the user's decision or the user asks.

## Curation Heuristics

- Merge pages only when they genuinely have the same subject.
- Split pages when sections can stand alone as reusable context.
- Prefer a small tag set with clear meaning.
- Keep packs task-shaped, not topic-shaped, unless the task is briefing on a topic.
- Treat source-backed uncertainty as useful information, not mess to hide.