# Skill Catalog Evaluator

Scan, evaluate, and catalog large collections of [Agent Skills](https://agentskills.io/specification) into a structured JSON file with scores across usage value, security risk, best practices, and more.

## What It Does

- **Scans** a local folder or GitHub repository for `SKILL.md` files
- **Extracts** frontmatter, directory structure, script languages, license, and external dependency indicators — mechanically, with no LLM cost
- **Evaluates** each skill on 8 dimensions (usage value, security risk, best practices, core capabilities, external requirements, script languages, license)
- **Produces** a `skill-catalog.json` with per-skill evaluations and aggregate summary statistics

## Directory Structure

```
agent-catalog-skill-evaluator/
├── SKILL.md                           # Skill instructions
├── README.md                          # This file
├── references/
│   ├── evaluation-criteria.md         # Scoring rubrics for all dimensions
│   ├── json-schema.md                 # Output JSON schema definition
│   └── security-patterns.md           # Security risk detection patterns
└── scripts/
    ├── scan_skills.py                 # Automated metadata scanner
    └── assemble_catalog.py            # Merges scan data + evaluations → JSON catalog
```

## Usage Examples

### Catalog a local skills folder

> "Catalog all the skills in ./skills and save the results to skill-catalog.json"

### Evaluate a GitHub repository

> "Scan and evaluate the skills at https://github.com/openclaw/skills — give me a catalog with quality scores"

### Audit a specific collection

> "Build an inventory of the skills in this repo. I want to know which ones have security risks and which rely on external services"

### Compare skill quality

> "Evaluate this skill repository and show me the top-rated skills by usage value and best practices"

## Scripts

### scan_skills.py

Walks a directory tree, finds all `SKILL.md` files, and extracts structured metadata. No external dependencies — pure Python 3.

```bash
python scripts/scan_skills.py <skills-directory> --output scan-results.json
```

### assemble_catalog.py

Merges scanner output with agent-produced evaluations into the final catalog JSON.

```bash
python scripts/assemble_catalog.py scan-results.json evaluations.json \
    --output skill-catalog.json \
    --source-url https://github.com/owner/repo \
    --source-type github
```

## Output

The catalog JSON includes:

- **Source metadata** — where the skills came from (local path or repo URL)
- **Summary statistics** — total skills, average scores, security risk distribution
- **Per-skill entries** — frontmatter, structure, and evaluation scores with rationale
- **Direct links** — path or URL to each skill's `SKILL.md`

See [references/json-schema.md](references/json-schema.md) for the full schema.
