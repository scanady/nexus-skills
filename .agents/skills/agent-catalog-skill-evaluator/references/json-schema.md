# Catalog JSON Schema

The output catalog must conform to this structure. Every field is required unless marked optional.

## Top-Level Structure

```json
{
  "catalog_version": "1.0.0",
  "generated_at": "2025-01-15T10:30:00Z",
  "sources": [
    {
      "id": "source-1",
      "type": "local | github",
      "path": "./skills",
      "url": "https://github.com/owner/repo",
      "commit": "abc123"
    }
  ],
  "summary": {
    "total_skills": 42,
    "evaluated": 42,
    "parse_errors": 0,
    "avg_usage_value": 3.2,
    "avg_best_practices": 2.8,
    "security_risk_distribution": {
      "low": 30,
      "medium": 10,
      "high": 2
    }
  },
  "skills": [ /* ... skill entries ... */ ]
}
```

## Skill Entry Structure

```json
{
  "name": "skill-name",
  "source_id": "source-1",
  "path": "skills/skill-name/SKILL.md",
  "url": "https://github.com/owner/repo/tree/main/skills/skill-name",
  "frontmatter": {
    "name": "skill-name",
    "description": "Full description text",
    "license": "MIT",
    "compatibility": null,
    "allowed_tools": null,
    "metadata": {
      "version": "1.0.0",
      "domain": "backend",
      "triggers": "keyword1, keyword2",
      "role": "specialist",
      "scope": "implementation",
      "output_format": "code",
      "related_skills": "skill-a, skill-b"
    }
  },
  "structure": {
    "has_scripts": true,
    "has_references": true,
    "has_agents": false,
    "has_assets": false,
    "has_license_file": false,
    "file_count": 8,
    "estimated_tokens": 3200
  },
  "evaluation": {
    "usage_value": {
      "score": 4,
      "rationale": "One sentence explaining the score"
    },
    "security_risk": {
      "rating": "medium",
      "rationale": "One sentence explaining the rating",
      "findings": ["Scripts make local file I/O", "References GitHub API"]
    },
    "best_practices": {
      "score": 3,
      "rationale": "One sentence explaining the score",
      "checklist": {
        "valid_frontmatter": true,
        "description_quality": true,
        "metadata_block": false,
        "triggers_field": false,
        "role_definition": true,
        "structured_workflow": true,
        "constraints_section": false,
        "reference_usage": true,
        "concise_instructions": true,
        "knowledge_reference": false
      }
    },
    "core_capabilities": "Brief 1-3 sentence summary of what the skill does",
    "external_requirements_indicator": "self-contained | has-external-dependencies",
    "external_requirements": ["GitHub API", "Node.js 18+"],
    "script_languages": ["python", "bash"],
    "license": "MIT"
  }
}
```

## Field Reference

### Source Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier for this source (used in skill entries) |
| `type` | string | `"local"` or `"github"` |
| `path` | string | Local filesystem path to the skills directory |
| `url` | string (optional) | GitHub repository URL (null for local sources) |
| `commit` | string (optional) | Git commit hash at scan time (null for local or if unavailable) |

### Summary Fields

| Field | Type | Description |
|-------|------|-------------|
| `total_skills` | integer | Number of SKILL.md files found |
| `evaluated` | integer | Number of skills successfully evaluated |
| `parse_errors` | integer | Number of skills that could not be parsed |
| `avg_usage_value` | float | Mean usage value score across all evaluated skills |
| `avg_best_practices` | float | Mean best practices score across all evaluated skills |
| `security_risk_distribution` | object | Count of skills per risk level |

### Evaluation Fields

| Field | Type | Values |
|-------|------|--------|
| `usage_value.score` | integer | 1–5 |
| `security_risk.rating` | string | `"low"`, `"medium"`, `"high"` |
| `best_practices.score` | integer | 1–5 |
| `core_capabilities` | string | 1–3 sentences |
| `external_requirements_indicator` | string | `"self-contained"` or `"has-external-dependencies"` |
| `external_requirements` | array of strings | Specific dependencies, or `["none"]` |
| `script_languages` | array of strings | Detected languages, or `["none"]` |
| `license` | string | SPDX identifier, `"custom"`, or `"unspecified"` |
