# Skill Catalog Overlap Audit

Repeatable process for identifying duplicate, overlapping, and boundary-unclear skills in the `skills/` catalog.

## When to Run

- After adding 5+ new skills
- Before any public release
- When routing quality degrades (skill keeps firing when it shouldn't, or fails to fire)
- Quarterly as a catalog hygiene pass

---

## Process

### Step 1 — Run the overlap report

```bash
node bin/cli.js audit-overlap
```

This scans all `skills/*/SKILL.md` files, computes pairwise similarity (triggers, descriptions, name segments, metadata), clusters related skills, and writes two output files:

- `output/skill-overlap-report.json`
- `output/skill-overlap-report.md`

**Options:**

```bash
# Raise threshold to see only strong overlaps (default: 0.20)
node bin/cli.js audit-overlap --threshold 0.30

# Show only the top 30 pairs
node bin/cli.js audit-overlap --top 30

# JSON only (skip markdown)
node bin/cli.js audit-overlap --json-only

# Custom output directory
node bin/cli.js audit-overlap --output /tmp/audit
```

---

### Step 2 — Review the Action Items section

Open `output/skill-overlap-report.md` and go to **Action Items** first. These are `duplicate` and `routing-collision` pairs ranked by overlap score. Work top-to-bottom.

For each cluster, assess:

| Question | Purpose |
|---|---|
| Would the same user prompt trigger both skills? | Primary routing test |
| Do they produce the same output artifact? | Duplicate signal |
| Does one contain unique domain knowledge, scripts, or references the other lacks? | Justification to keep both |
| Can a router reliably choose between them from descriptions/triggers alone? | Routing quality check |
| Is one a stale or weaker version of the other? | Archive candidate |

---

### Step 3 — Classify each cluster

Use these categories:

| Type | Description | Default Action |
|---|---|---|
| `duplicate` | Same user intent, same output, same workflow | Merge or archive one |
| `routing-collision` | Different skills but competing trigger phrases | Sharpen descriptions and triggers |
| `umbrella-plus-specialist` | One broad, one narrow within shared prefix | Add routing links; broad skill defers to specialist |
| `adjacent-distinct` | Related vocabulary, different primary purpose | Verify triggers don't collide; usually keep |
| `stale-successor` | One is an older/weaker version of the other | Archive the older one |

---

### Step 4 — Decide and act

For each cluster, choose one action:

- **keep-as-is** — overlap is intentional and routing is clear
- **keep-with-routing** — keep both but add `related-skills` links and/or sharpen description/trigger boundaries
- **merge** — consolidate into one skill, preserve the best content from both
- **archive** — move to `skills-sandbox/` (the weaker or redundant skill)
- **rename/reposition** — skill is useful but collides because of its name or description

---

### Step 5 — Record decisions

Update `docs/skill-overlap-decisions.md` with your decision for each cluster. This prevents re-litigating the same questions in future audits.

---

### Step 6 — Act on high-priority items

Apply changes to the affected `SKILL.md` files using the `skill-architect` skill for routing fixes:

```
/skill-architect review skills/tech-security-reviewer
```

For merges, consolidate into the stronger skill, update its `related-skills` field, and move the weaker skill to `skills-sandbox/`.

---

## Scoring Reference

The overlap score is a weighted combination of five signals:

| Signal | Weight | What it measures |
|---|---|---|
| Trigger Jaccard | 35% | Token overlap between `metadata.triggers` fields |
| Description Jaccard | 25% | Token overlap between `description` fields |
| Body Jaccard | 15% | Token overlap in first 80 lines of SKILL.md body |
| Name segment similarity | 15% | Shared hyphen-delimited name segments |
| Metadata match | 10% | `domain`, `scope`, `output-format` equality |

A score of 0.20 is the reporting threshold. Scores above 0.50 with high trigger overlap are flagged as `duplicate`.

---

## Overlap Is Not Always Bad

Some overlap is intentional and healthy:

- **Narrow specialists** should share vocabulary with their umbrella skill — that's how routing works
- **Platform-specific skills** (e.g., LinkedIn writer, X writer) share generic content-writing tokens but serve distinct use cases
- **Same workflow, different domain** — sharing procedure tokens is fine if domain knowledge differs

The goal is not zero overlap — it is clear routing. If a user prompt has an unambiguous winner, the catalog is healthy.

---

## New Skill Intake Rule

Every new skill added to `skills/` should answer:

```
Nearest neighbors in the catalog:
Why this is not an update to an existing skill:
Primary trigger phrases (not already owned by a neighbor):
Should-NOT-trigger examples:
Expected output artifact:
```

This one check prevents most catalog drift before it starts.
