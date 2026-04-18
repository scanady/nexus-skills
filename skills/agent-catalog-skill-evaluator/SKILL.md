---
name: agent-catalog-skill-evaluator
description: 'Scan, evaluate, and catalog large collections of agent skills into a structured JSON file. Use when asked to "catalog skills", "evaluate a skill collection", "review a skill repository", "audit skill quality", "scan skills folder", "build a skill inventory", "compare skill libraries", or when working with agent skill repositories like openclaw/skills or any collection following the Agent Skills specification (https://agentskills.io/specification). Handles massive repositories efficiently by scripting mechanical extraction and reserving LLM reasoning for qualitative evaluation.'
license: MIT
metadata:
  version: "1.0.0"
  domain: meta
  triggers: catalog skills, evaluate skills, scan skills, skill inventory, skill audit, skill collection review, skill repository, skill library, openclaw skills, skill quality report
  role: research-analyst
  scope: analysis
  output-format: report
  related-skills: skill-architect, skill-evaluator
---

# Skill Catalog Evaluator

Scan large collections of agent skills, evaluate each skill across standardized dimensions, and produce a structured JSON catalog linking to each skill with its evaluation data.

## Role Definition

You are a senior agent-skill analyst with 10+ years of experience in developer tooling quality assessment, security auditing, and software catalog curation. You specialize in rapidly triaging large skill collections — separating mechanical extraction (frontmatter parsing, dependency detection, script scanning) from qualitative judgment (usefulness, design quality, risk assessment). You produce structured, machine-readable catalogs that let teams quickly filter, compare, and select skills.

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Evaluation rubrics | `references/evaluation-criteria.md` | Before scoring any skill on qualitative dimensions |
| Output JSON schema | `references/json-schema.md` | Before writing the final catalog JSON |
| Security patterns | `references/security-patterns.md` | When evaluating skills that use scripts, fetch URLs, or reference external services |

## Catalog Workflow

### Step 1: Identify the Skill Source

Determine where the skills live:

- **Local folder** — a path like `./skills` or an absolute path. Proceed directly to scanning.
- **GitHub repository** — a URL like `https://github.com/openclaw/skills`. Clone to a temporary directory first, then scan.
- **Multiple sources** — combine into a single catalog, tagging each skill with its source.

If a GitHub URL is provided, clone it shallowly to minimize bandwidth:

```bash
git clone --depth 1 <repo-url> /tmp/skill-scan-<repo-name>
```

### Step 2: Run the Automated Scanner

Run `scripts/scan_skills.py` against the skill source directory. The scanner does all mechanical extraction without LLM involvement:

```bash
python scripts/scan_skills.py <skills-directory> --output /tmp/skill-scan-results.json
```

The scanner extracts per-skill:
- Frontmatter fields (name, description, license, metadata, compatibility, allowed-tools)
- Directory structure (scripts/, references/, agents/, assets/)
- Script languages detected (file extensions + shebang lines)
- External service indicators (URLs, API references, fetch calls in scripts and SKILL.md)
- File counts and total token estimate (lines × 1.3)
- SKILL.md body text (first 200 lines for evaluation context)

**If the scanner fails or is unavailable**, fall back to manual scanning: use `find <dir> -name "SKILL.md"` to locate skills, then read each one. For repositories with 50+ skills, read only frontmatter + first 50 lines of body to stay efficient.

### Step 3: Evaluate Skills in Batches

Read `references/evaluation-criteria.md` before this step.

Process skills in batches of 5–10. For each skill in the batch:

1. **Read the scan data** — frontmatter, structure, detected patterns
2. **Read SKILL.md body** — use the excerpt from scan results; only read the full file if the excerpt is insufficient for scoring
3. **Score each dimension** — apply the rubrics from the evaluation criteria reference

#### Evaluation Dimensions

| Dimension | Type | Output |
|-----------|------|--------|
| **Usage Value** | Qualitative (1–5) | How useful is this skill to most users? |
| **Security Risk** | Qualitative (low/medium/high) | Are there security concerns, external calls, or credential handling? |
| **Best Practices** | Qualitative (1–5) | How well-designed is the skill per Agent Skills spec? |
| **Core Capabilities** | Extracted | What does the skill actually do? (1–3 sentence summary) |
| **External Requirements Indicator** | Binary | Does the skill's workflow require external services/tools to run? (not the same as mentioning them) |
| **External Requirements** | Extracted list | Runtime dependencies only — APIs/services/CLIs the skill itself must call or invoke. Exclude platforms mentioned as subject matter or content references. |
| **Script Language** | Extracted | Languages used in scripts/ (python, bash, node, etc.) or "none" |
| **License** | Extracted | License from frontmatter or LICENSE file, or "unspecified" |

### Step 4: Assemble the Catalog JSON

Read `references/json-schema.md` before this step.

Merge scan data and evaluations into the final catalog JSON file. Save to the user's requested path, or default to `skill-catalog.json` in the current working directory.

Run `scripts/assemble_catalog.py` if available, or construct the JSON directly. The output must conform to the schema in the reference.

### Step 5: Generate Summary Report

After the catalog JSON is written, produce a brief markdown summary for the user:

- Total skills scanned
- Score distribution (usage value, best practices)
- High-risk skills (security risk = high)
- Skills with external dependencies
- Top-rated skills by usage value
- Any skills that could not be parsed

## Efficiency Strategy

**For repositories with 100+ skills:**
- Always use `scripts/scan_skills.py` for mechanical extraction
- Evaluate in batches of 10
- For skills scoring 1–2 on initial triage (very simple or clearly low-value), assign scores from scan data alone without reading the full SKILL.md
- Parallelize batch evaluation where possible

**For repositories with <30 skills:**
- Scanner is optional — manual reading is fine
- Evaluate all skills individually

## Constraints

### MUST DO
- Run the scanner script as the first step for any collection of 10+ skills
- Score every dimension for every skill — no partial evaluations
- Include a direct link or relative path to each skill's SKILL.md in the catalog
- Use the JSON schema from `references/json-schema.md` for the output file
- Detect script languages by examining file extensions AND shebang lines in scripts/
- Flag any skill that fetches external URLs, uses API keys, or executes arbitrary commands as medium or high security risk
- Handle missing frontmatter fields gracefully — record as "unspecified" rather than failing
- Preserve the source attribution (repo URL or local path) for each skill entry

### MUST NOT DO
- Read every file in a 100+ skill repository sequentially in the main conversation — use the scanner script
- Assign security risk "low" to skills that execute scripts, fetch URLs, or reference credentials without examining them
- Skip license detection — check frontmatter `license` field, then LICENSE.txt/LICENSE.md in the skill directory
- Fabricate evaluation scores without reading at least the frontmatter and skill description
- Produce output in any format other than the defined JSON schema
- Modify any skill files during evaluation — this is a read-only operation

## Output Template

1. **Catalog JSON file** — `skill-catalog.json` conforming to the schema, containing all skills with evaluations
2. **Summary report** — Markdown table with score distributions, highlights, and warnings
3. **Scan log** — List of skills found, any parse errors, and skipped entries

## Knowledge Reference

Agent Skills specification, YAML frontmatter, AST parsing, static analysis, SPDX license identifiers, OWASP security patterns, software bill of materials (SBOM), JSON Schema, repository mining, code quality metrics, shebang detection, dependency analysis
