# Lint Workflow

Use this workflow when checking repository health.

The lint and stats scripts accept the context root as a positional argument. Pass the actual root directory; for multi-root projects, run them once per root.

## Structural Lint

Run (replace `context/` with the actual root, for example `context-core/`):

```bash
python scripts/context_lint.py context/
```

Optional:

```bash
python scripts/context_lint.py context/ --suggest-pages
python scripts/context_lint.py context/ --json
```

The script reports:

- orphan pages
- broken double-bracket links
- oversized pages
- missing or malformed frontmatter
- duplicate slugs
- stale well-linked pages
- context-pack issues
- candidate pages for recurring terms

## Semantic Lint

Structural lint is not enough. For semantic lint, read selected pages and look for:

- claims that drifted from their sources
- unresolved contradictions
- stale product, policy, pricing, legal, or workflow claims
- packs whose required pages no longer match the task
- missing packs for recurring tasks
- index entries that no longer describe the page
- schema conventions that no longer match practice

## Cadence

Default cadence:

- after every 5 ingests for structural lint
- weekly or after every 20 ingests for semantic lint
- monthly for context-pack freshness

Increase cadence for regulated, legal, financial, medical, policy, or product-launch contexts.

## Present Findings

Report findings as proposed edits, grouped by risk:

- critical: source trace missing for high-stakes claim, broken required pack page, hard size cap violation
- warning: orphan page, stale hub, unclear pack boundary, duplicate concept
- suggestion: tighter summary, better tag, possible new page

Apply low-risk structural repairs when the fix is clear. Do not silently rewrite semantic content when it could alter meaning. Ask for approval or mark it as a proposed change only when human judgment is needed for meaning, authority, freshness, or destructive scope.

Report pack, index, tag, and schema mechanics as outcomes, not decisions, unless the user asked about those mechanics or a finding requires their judgment.

## Log Lint

After running or acting on lint, append:

```markdown
## [YYYY-MM-DD] lint | <scope>
- Findings: <brief count or summary>
- Actions: <pages changed, if any>
```