# Changelog

## 1.2.0

- Renamed the skill and installable directory to `strategy-outcome-design` to match the repository's `<domain>-<name>` convention.
- Standardized frontmatter to repository conventions: added `disable-model-invocation`, `license`, and `metadata` fields (`author`, `domain`, `triggers`, `anti-triggers`, `role`, `scope`, `output-format`, `related-skills`).
- Updated `evals.json` `skill_name` and README references to the new directory name.

## 1.1.0

- Moved version metadata into the standards-compliant `metadata` map.
- Renamed the installable root directory to match the skill name.
- Rewrote the description for clearer positive and negative triggering.
- Added adaptive checkpoints and explicit stopping behavior.
- Added a priority model for selecting the highest-value question.
- Separated maturity from disposition.
- Replaced execution readiness with downstream readiness.
- Added outcome desirability, opportunity cost, anti-outcomes, locus of control, decision rights, and stakeholder dynamics.
- Strengthened measurement integrity, causal design, alternatives, reversibility, and uncertainty prioritization.
- Added light, standard, and deep review behavior without requiring a mode-selection menu.
- Added external-evidence and high-stakes guidance.
- Added a compact, machine-readable record header and downstream contract.
- Wired supporting resources into `SKILL.md` with explicit load conditions.
- Added runnable evaluation and trigger-query files.
- Added a package validator and complete example record.
