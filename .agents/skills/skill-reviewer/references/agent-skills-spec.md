# Agent Skills Specification Reference

Source: https://agentskills.io/specification

## Directory Structure

A skill is a directory containing at minimum a `SKILL.md` file:

```
skill-name/
├── SKILL.md              # Required
├── scripts/              # Optional: executable code
├── references/           # Optional: documentation loaded on demand
└── assets/               # Optional: static resources used in output
```

## SKILL.md Format

Must contain YAML frontmatter followed by Markdown content.

### Frontmatter Fields

| Field | Required | Constraints |
|-------|----------|-------------|
| `name` | **Yes** | 1-64 chars. Lowercase alphanumeric + hyphens only. No leading/trailing/consecutive hyphens. Must match parent directory name. |
| `description` | **Yes** | 1-1024 chars. Non-empty. Describes what the skill does and when to use it. Include trigger keywords. |
| `license` | No | License name or reference to a bundled license file. |
| `compatibility` | No | 1-500 chars. Environment requirements (product, system packages, network access). Most skills don't need this. |
| `metadata` | No | Arbitrary string key-value map for additional properties. Use unique key names to avoid conflicts. |
| `allowed-tools` | No | Space-delimited list of pre-approved tools. Experimental — support varies by agent. |

### Frontmatter Examples

Minimal:
```yaml
---
name: skill-name
description: A description of what this skill does and when to use it.
---
```

Full:
```yaml
---
name: pdf-processing
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF documents or when the user mentions PDFs, forms, or document extraction.
license: MIT
compatibility: Requires poppler-utils for PDF processing
metadata:
  author: example-org
  version: "1.0"
allowed-tools: Bash(python3:*) Read
---
```

### Name Validation Rules

Valid:
- `pdf-processing`
- `data-analysis`
- `code-review`

Invalid:
- `PDF-Processing` — uppercase not allowed
- `-pdf` — cannot start with hyphen
- `pdf-` — cannot end with hyphen
- `pdf--processing` — consecutive hyphens not allowed

### Description Best Practices

The description is the PRIMARY trigger mechanism for skill activation.

**Include:**
1. WHAT the skill does (capabilities)
2. WHEN to use it (triggers, scenarios)
3. Keywords users might mention

**Good:**
```yaml
description: 'Extracts text and tables from PDF files, fills PDF forms, and merges multiple PDFs. Use when working with PDF documents or when the user mentions PDFs, forms, or document extraction.'
```

**Poor:**
```yaml
description: 'Helps with PDFs.'
```

### Body Content

The Markdown body after frontmatter contains skill instructions. No format restrictions — write whatever helps agents perform the task effectively.

Recommended sections:
- Step-by-step instructions
- Examples of inputs and outputs
- Common edge cases

The agent loads the entire file on skill activation, so keep it focused.

## Optional Directories

### scripts/

Executable code that agents can run. Should be:
- Self-contained or clearly document dependencies
- Include helpful error messages
- Handle edge cases gracefully

Supported languages depend on the agent implementation (Python, Bash, JavaScript common).

### references/

Additional documentation agents read on demand:
- Technical reference docs
- Form templates or structured data formats
- Domain-specific files (finance.md, legal.md, etc.)

Keep reference files focused — agents load them on demand, so smaller files mean less context use.

### assets/

Static resources used as-is in output:
- Templates (document, configuration)
- Images (diagrams, examples)
- Data files (lookup tables, schemas)

## Progressive Disclosure

Skills use three-level loading for efficient context use:

1. **Metadata** (~100 tokens) — `name` and `description` loaded at startup for all skills
2. **Instructions** (<5000 tokens recommended) — Full SKILL.md body loaded on activation
3. **Resources** (as needed) — Scripts, references, assets loaded only when required

**Target: SKILL.md under 500 lines.** Move detailed reference material to separate files.

## File References

Use relative paths from skill root:
```markdown
See [the reference guide](references/REFERENCE.md) for details.
Run: scripts/extract.py
```

Keep file references one level deep from SKILL.md. Avoid deeply nested reference chains.

## Validation

Use the skills-ref reference library:
```
skills-ref validate ./my-skill
```

Checks frontmatter validity and naming conventions.

Repository: https://github.com/agentskills/agentskills/tree/main/skills-ref
