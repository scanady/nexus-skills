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
    "avg_executability": 3.1,
    "avg_invocability": 3.4,
    "security_risk_distribution": {
      "low": 30,
      "medium": 10,
      "high": 2
    },
    "complexity_distribution": {
      "compact": 20,
      "detailed": 15,
      "comprehensive": 7
    },
    "pattern_distribution": {
      "A": 28,
      "B": 12,
      "C": 2
    },
    "over_specification_flagged": 5
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
    "estimated_tokens": 3200,
    "complexity_class": "comprehensive",
    "skill_pattern": "B"
  },
  "evaluation": {
    "usage_value": {
      "score": 4,
      "rationale": "One sentence explaining the score"
    },
    "security_risk": {
      "rating": "medium",
      "rationale": "One sentence explaining the rating",
      "findings": ["Scripts make local file I/O", "References GitHub API"],
      "sub_scores": {
        "data_privacy": 4,
        "prompt_injection": 5,
        "illegal_content": 5,
        "bias": 5,
        "system_integrity": 3,
        "untrusted_communication": 4
      }
    },
    "executability": {
      "score": 3,
      "completeness": 3,
      "determinism": 4,
      "consistency": 4,
      "usability": 2,
      "rationale": "One sentence explaining the score"
    },
    "invocability": {
      "score": 4,
      "rationale": "One sentence explaining the score"
    },
    "over_specification_risk": {
      "flagged": false,
      "rationale": "One sentence explaining the assessment"
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
| `avg_executability` | float | Mean executability score across all evaluated skills |
| `avg_invocability` | float | Mean invocability score across all evaluated skills |
| `security_risk_distribution` | object | Count of skills per risk level |
| `complexity_distribution` | object | Count of skills per token complexity class (compact/detailed/comprehensive) |
| `pattern_distribution` | object | Count of skills per skill pattern (A/B/C) |
| `over_specification_flagged` | integer | Number of skills flagged for over-specification risk |

### Evaluation Fields

| Field | Type | Values |
|-------|------|--------|
| `usage_value.score` | integer | 1–5 |
| `security_risk.rating` | string | `"low"`, `"medium"`, `"high"` |
| `security_risk.sub_scores.*` | integer | 1–5 per dimension (`data_privacy`, `prompt_injection`, `illegal_content`, `bias`, `system_integrity`, `untrusted_communication`) |
| `executability.score` | integer | 1–5 (average of four sub-dimensions) |
| `executability.completeness` | integer | 1–5 |
| `executability.determinism` | integer | 1–5 |
| `executability.consistency` | integer | 1–5 |
| `executability.usability` | integer | 1–5 |
| `invocability.score` | integer | 1–5 |
| `over_specification_risk.flagged` | boolean | `true` or `false` |
| `core_capabilities` | string | 1–3 sentences |
| `external_requirements_indicator` | string | `"self-contained"` or `"has-external-dependencies"` |
| `external_requirements` | array of strings | Specific dependencies, or `["none"]` |
| `script_languages` | array of strings | Detected languages, or `["none"]` |
| `license` | string | SPDX identifier, `"custom"`, or `"unspecified"` |
| `structure.complexity_class` | string | `"compact"`, `"detailed"`, or `"comprehensive"` |
| `structure.skill_pattern` | string | `"A"`, `"B"`, or `"C"` |
