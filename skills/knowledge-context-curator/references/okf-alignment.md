# OKF Alignment

This reference documents how this skill's context repositories align with the [Open Knowledge Format (OKF)](https://github.com/GoogleCloudPlatform/knowledge-catalog) specification.

## What Is OKF

OKF is a vendor-neutral, open specification for representing structured knowledge as a plain directory of markdown files with YAML frontmatter. It is intentionally minimal: a directory of `.md` files where every non-reserved file has parseable YAML frontmatter with at least a `type` field. The spec is designed to be readable by humans without tools, parseable by LLMs and agents without SDKs, version-controlled in git, and portable across organizations.

## Conformance Requirements

A bundle conforms to OKF if:

1. Every non-reserved `.md` file contains a parseable YAML frontmatter block.
2. Every frontmatter block contains a non-empty `type` field.
3. Every `index.md` and `log.md` follows the structure described in OKF §6/§7 when present.

## How This Skill Aligns

| OKF Requirement | This Skill's Implementation |
|---|---|
| `type` field (required) | Every page has `type` in frontmatter: `source`, `entity`, `concept`, `synthesis`, or `context-pack` |
| `title` (recommended) | Required by this skill's schema |
| `description` (recommended) | Required by this skill's schema — one-sentence summary for indexes and search |
| `timestamp` (recommended) | Required — ISO 8601 datetime of last meaningful change |
| `resource` (recommended) | Used on `source` pages when describing a physical asset with a canonical URI |
| `tags` (optional) | Supported; governed by tag taxonomy in `SCHEMA.md` |
| Standard markdown links (§5) | All cross-references use `[text](/path/to/concept.md)` or `[text](./relative.md)` |
| `index.md` format (§6) | Uses `* [Title](relative-path) - description` format |
| `log.md` format (§7) | Uses `## YYYY-MM-DD` date headings, newest first, with `* **Verb**: description` entries |
| `# Citations` (§8) | Pages include a `# Citations` section at the bottom for external source references |
| Extension fields allowed | Additional fields (`created`, `updated`, `sources`, `freshness`, etc.) are preserved |

## Extensions Beyond OKF

This skill adds governance and agent-optimization layers that go beyond what OKF specifies, while remaining fully conformant:

- **`SCHEMA.md`** — repository-level governance configuration (not an OKF reserved filename; treated as a regular concept document with `type: schema` or excluded from concept validation).
- **Context packs** — `context-pack` type documents under `packs/` that define agent load plans for recurring tasks.
- **Evidence layer** — immutable raw sources under `raw/` for audit and traceability.
- **Additional frontmatter** — `created`, `updated`, `sources`, `task`, `required_pages`, `optional_pages`, `exclusions`, `freshness`, `ingested`, `raw`, `authors`, `url`.
- **Structural and semantic lint** — tooling that validates both OKF conformance and skill-specific governance rules.
- **Page sizing rules** — soft cap (400 lines) and hard cap (800 lines) for bounded context loading.

## Reserved Filenames

Per OKF §3.1, these filenames have defined meaning and must not be used for concept documents:

- `index.md` — directory listing for progressive disclosure
- `log.md` — chronological update history

This skill also reserves `SCHEMA.md` as the repository's governance configuration file. It is not an OKF-defined reserved file but is treated specially by the skill's tooling.

## Migration From Wiki Links

If an existing repository uses `[[wiki-style links]]`, migrate to standard markdown links:

1. Replace `[[slug]]` with `[title](/type/slug.md)` where `type` is the page's subdirectory.
2. Replace `[[slug|display text]]` with `[display text](/type/slug.md)`.
3. Run the lint script to verify no broken links remain.
4. Update `SCHEMA.md` to note the migration.

The lint script supports both link styles during migration, detecting inbound links from either format.
