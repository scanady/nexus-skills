# Knowledge Consolidation Patterns

Use this reference when a source skill has uploaded-knowledge candidates, especially one-rule-per-file corpora.

## Inventory Procedure

Record these metrics before grouping:

- Source folders and file counts.
- Markdown/text file count and total bytes.
- Binary assets and whether they are needed for GPT behavior.
- ID pattern in filenames, headings, or YAML front matter.
- YAML fields useful for indexing: `rule_id`, `title`, `classification`, `rule_type`, `status`, `products`, `channels`, `jurisdictions`, `audience`, `tags`, `related_rules`.
- Largest files and mixed-topic files.

## File Count Targets

For Custom GPTs:

- Hard cap: 20 uploaded files.
- Preferred complex-bundle target: 12-18 uploaded files.
- Reserve slots for `00-knowledge-index.md`, optional full output template, and optional domain guidance.

If the user asks for another deployment target, confirm and document the target-specific cap before changing the grouping plan.

## Grouping Strategies

Choose the first strategy that fits the corpus.

### 1. ID Prefix Plus Category

Use when filenames look like `LIFE-MKT-002.md` or IDs have meaningful segments.

Group by the first two segments when the first segment is too broad:

- `LIFE-MKT-*` -> `rules-life-marketing.md`
- `LIFE-DISC-*` and `LIFE-PROD-*` -> `rules-life-disclosure-product.md`
- `NYLD-PASS-*` and `NYLD-PROC-*` -> `rules-nyld-process-pass.md`

This preserves retrieval scoping better than one file per top-level prefix.

### 2. Topic or Channel

Use when IDs are absent or not meaningful. Group by the retrieval question the GPT must answer:

- Pricing and affordability.
- Disclosure and prominence.
- Email/channel rules.
- Visual review.
- Editorial and brand.
- Pass patterns and accepted risks.

### 3. Source File As-Is Plus Index

Use only when total uploaded files remain safely below the cap after adding `00-knowledge-index.md`.

### 4. Single File

Use only for small, cohesive corpora under about 50 KB. Do not use one mega-file for rule corpora merely because it fits the size cap.

## Consolidated File Format

Each grouped file should use this structure:

```markdown
# <Group Title>

Source: <source folder>
Canonical items: <count>
Citation rule: cite only the exact IDs shown in item headings or front matter.

---

## <ID> - <Title>

<full original file text, including YAML front matter>

---
```

Do not summarize or truncate item bodies. If the source YAML has applicability or citation fields, keep it.

## Index Format

Create `00-knowledge-index.md` with one row per canonical item.

Recommended columns:

| ID | Title | Classification | Type | Applicability | Tags | Bundled file |
|---|---|---|---|---|---|---|

Keep the index concise. If rows become too wide, collapse arrays into short comma-separated text and move detail to the bundled file.

## Build Script Requirements

Generate `scripts/build-gpt-knowledge.py` when the corpus has more than about 30 canonical files or will be maintained over time.

The script should:

- Use only the Python standard library.
- Parse enough YAML front matter with regex/string logic to extract IDs and titles.
- Sort deterministically.
- Emit `00-knowledge-index.md` first.
- Preserve original item text exactly.
- Print counts: source items, grouped files, indexed IDs, missing IDs, duplicate IDs, total uploaded files, total bytes.

## Marketing Compliance Reviewer Bundle Shape

For `marketing-compliance-content-reviewer`, the source has 85 markdown knowledge files including README, 84 rule files, about 280 KB of knowledge, and these rule prefixes:

- CONTENT: 17
- JUSTIN: 18
- LIFE: 31
- NYLD: 18

Recommended Custom GPT knowledge shape:

1. `00-knowledge-index.md`
2. `01-rules-life-disclosure-product.md`
3. `02-rules-life-marketing.md`
4. `03-rules-nyld-pricing-marketing-advice.md`
5. `04-rules-nyld-disclosure-visual-brand-editorial.md`
6. `05-rules-nyld-process-pass.md`
7. `06-rules-justin-pricing-marketing-advice.md`
8. `07-rules-justin-disclosure.md`
9. `08-rules-justin-channel-brand-visual-editorial.md`
10. `09-rules-content-marketing.md`
11. `10-rules-content-disclosure-editorial.md`
12. `11-output-template.md` if the full report template cannot fit in Instructions
13. `12-domain-guidance.md` if long interpretive guidance must move out of Instructions

This shape stays below the 20-file cap and gives retrieval better topical boundaries than four broad prefix files.