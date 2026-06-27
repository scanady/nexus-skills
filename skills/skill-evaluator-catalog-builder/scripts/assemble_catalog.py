#!/usr/bin/env python3
"""
Assemble a final skill catalog JSON from scan results and evaluation data.

Usage:
    python assemble_catalog.py <scan-results.json> <evaluations.json> \
        --output skill-catalog.json [--source-url URL] [--source-type local|github]

The scan results come from scan_skills.py. The evaluations come from the
agent's qualitative review (a JSON array with per-skill scores).

This script merges them into the final catalog format defined in
references/json-schema.md.
"""

import argparse
import copy
import json
from pathlib import PurePosixPath
import sys
from datetime import datetime, timezone
from pathlib import Path


USAGE_SCORE_WEIGHTS = {
    "problem_clarity": 0.25,
    "audience_breadth": 0.20,
    "capability_gap": 0.25,
    "actionability": 0.20,
    "reusability": 0.10,
}

SPECIALIZED_DOMAIN_HINTS = {
    "healthcare",
    "clinical",
    "regulatory",
    "compliance",
    "legal",
    "actuarial",
    "insurance",
    "behavioral",
    "behavioural",
    "nudge",
    "choice architecture",
    "prospect theory",
    "bias",
    "sre",
    "forensics",
    "owasp",
    "mcp",
    "revops",
}


def clamp(value: float, low: float, high: float) -> float:
    """Clamp a number to the provided inclusive range."""
    return max(low, min(high, value))


def clamp_int_score(value: int | float, default: int = 0) -> int:
    """Clamp a score to the inclusive 0-5 integer range."""
    try:
        n = int(round(float(value)))
    except (TypeError, ValueError):
        return default
    return int(clamp(n, 0, 5))


def derive_usage_sub_scores(scan_entry: dict, frontmatter: dict) -> dict:
    """Derive fallback usage sub-scores when evaluators did not provide them."""
    description = (frontmatter.get("description") or "").strip()
    excerpt = (scan_entry.get("body_excerpt") or "").lower()
    desc_lower = description.lower()

    if "use when" in desc_lower or "invoked when" in desc_lower:
        problem_clarity = 5
    elif len(description) >= 120:
        problem_clarity = 4
    elif description:
        problem_clarity = 3
    else:
        problem_clarity = 1

    trigger_count = description.count(",") + description.count(" or ")
    if "any issue" in desc_lower or "any goal" in desc_lower:
        audience_breadth = 4
    elif trigger_count >= 10:
        audience_breadth = 4
    elif trigger_count >= 4:
        audience_breadth = 3
    else:
        audience_breadth = 2

    capability_gap = 4 if has_specialized_domain_signal(frontmatter, scan_entry) else 3

    if "phase 1" in excerpt or "workflow" in excerpt or "step" in excerpt:
        actionability = 4
    elif "deliver" in excerpt or "output" in excerpt:
        actionability = 4
    else:
        actionability = 3

    if "generalize" in excerpt or "any issue" in desc_lower or "any goal" in desc_lower:
        reusability = 4
    else:
        reusability = 3

    return {
        "problem_clarity": problem_clarity,
        "audience_breadth": audience_breadth,
        "capability_gap": capability_gap,
        "actionability": actionability,
        "reusability": reusability,
    }


def has_specialized_domain_signal(frontmatter: dict, scan_entry: dict) -> bool:
    """Detect whether a skill appears domain-specialized based on static content."""
    text_parts = [
        frontmatter.get("name") or "",
        frontmatter.get("description") or "",
        scan_entry.get("body_excerpt") or "",
    ]
    corpus = " ".join(text_parts).lower()
    return any(term in corpus for term in SPECIALIZED_DOMAIN_HINTS)


def infer_domain_calibration_bonus(usage_eval: dict, frontmatter: dict, scan_entry: dict) -> float:
    """Infer a deterministic domain calibration bonus when not explicitly provided."""
    provided = usage_eval.get("domain_calibration_bonus")
    if provided is not None:
        try:
            return round(clamp(float(provided), 0.0, 0.7), 2)
        except (TypeError, ValueError):
            pass

    return 0.3 if has_specialized_domain_signal(frontmatter, scan_entry) else 0.0


def compute_usage_value(usage_eval: dict, frontmatter: dict, scan_entry: dict) -> dict:
    """Compute usage value from weighted sub-scores with calibration and guards."""
    usage_eval = dict(usage_eval or {})
    existing_rationale = (
        usage_eval.get("rationale")
        or "Auto-generated from scan-only fallback."
    )

    provided_sub_scores = usage_eval.get("sub_scores") or {}
    normalized_sub_scores = {}
    for factor in USAGE_SCORE_WEIGHTS:
        if factor in provided_sub_scores:
            normalized_sub_scores[factor] = clamp_int_score(
                provided_sub_scores.get(factor),
                default=0,
            )

    if len(normalized_sub_scores) != len(USAGE_SCORE_WEIGHTS):
        normalized_sub_scores = derive_usage_sub_scores(scan_entry, frontmatter)

    weighted_raw = sum(
        normalized_sub_scores[factor] * weight
        for factor, weight in USAGE_SCORE_WEIGHTS.items()
    )
    domain_bonus = infer_domain_calibration_bonus(usage_eval, frontmatter, scan_entry)
    weighted_with_bonus = clamp(weighted_raw + domain_bonus, 1.0, 5.0)

    computed_score = int(round(weighted_with_bonus))
    score = computed_score

    # Consistency guard: rationale indicating "domain-specific" should not score below 3.
    rationale_l = str(existing_rationale).lower()
    if (
        ("domain-specific" in rationale_l or "niche" in rationale_l)
        and score < 3
    ):
        score = 3

    if existing_rationale.strip().lower() == "not evaluated" and score > 0:
        existing_rationale = (
            "Computed from weighted sub-scores with domain calibration in assembler."
        )

    return {
        "score": int(clamp(score, 0, 5)),
        "rationale": existing_rationale,
        "sub_scores": normalized_sub_scores,
        "weighted_score": round(weighted_raw, 2),
        "domain_calibration_bonus": round(domain_bonus, 2),
        "method_version": "weighted-v2",
    }


def normalize_evaluation(evaluation: dict, frontmatter: dict, scan_entry: dict) -> dict:
    """Normalize evaluation payload and compute derived scoring fields."""
    evaluation = copy.deepcopy(evaluation)
    evaluation = sanitize_not_evaluated_placeholders(evaluation)
    evaluation["usage_value"] = compute_usage_value(
        evaluation.get("usage_value", {}),
        frontmatter,
        scan_entry,
    )

    if "executability" in evaluation:
        evaluation["executability"]["score"] = clamp_int_score(
            evaluation.get("executability", {}).get("score"),
            default=0,
        )
    if "invocability" in evaluation:
        evaluation["invocability"]["score"] = clamp_int_score(
            evaluation.get("invocability", {}).get("score"),
            default=0,
        )

    return evaluation


def load_json(path: str) -> dict:
    """Load and parse a JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize_key(value: str | None) -> str:
    """Normalize an identifier for deterministic matching/deduping."""
    return (value or "").strip().lower()


def scan_entry_lookup_keys(scan_entry: dict) -> list[str]:
    """Return ordered alias keys used to resolve evaluation entries."""
    keys: list[str] = []

    def add(value: str | None):
        key = normalize_key(value)
        if key and key not in keys:
            keys.append(key)

    add(scan_entry.get("name"))
    frontmatter = scan_entry.get("frontmatter") or {}
    add(frontmatter.get("name"))

    raw_path = (scan_entry.get("path") or "").replace("\\", "/")
    if raw_path:
        posix_path = PurePosixPath(raw_path)
        parts = list(posix_path.parts)
        if parts and parts[-1].lower() == "skill.md":
            parts = parts[:-1]
        if parts:
            add(parts[-1])

    return keys


def resolve_evaluation_for_scan_entry(scan_entry: dict, eval_lookup: dict) -> dict | None:
    """Resolve an evaluation by trying scan name and stable aliases."""
    for key in scan_entry_lookup_keys(scan_entry):
        eval_entry = eval_lookup.get(key)
        if eval_entry is not None:
            return eval_entry
    return None


def sanitize_not_evaluated_placeholders(value):
    """Replace legacy placeholder strings with stable fallback language."""
    if isinstance(value, dict):
        return {k: sanitize_not_evaluated_placeholders(v) for k, v in value.items()}
    if isinstance(value, list):
        return [sanitize_not_evaluated_placeholders(v) for v in value]
    if isinstance(value, str) and value.strip().lower() == "not evaluated":
        return "Auto-generated from scan-only fallback."
    return value


def build_source(scan_data: dict, source_url: str | None, source_type: str) -> dict:
    """Build the source entry for the catalog."""
    source = {
        "id": "source-1",
        "type": source_type,
        "path": scan_data.get("source_directory", ""),
    }
    if source_url:
        source["url"] = source_url
    else:
        source["url"] = None

    source["commit"] = None
    return source


def build_skill_entry(scan_entry: dict, eval_entry: dict | None, source_id: str, source_url: str | None) -> dict:
    """Merge scan data and evaluation for a single skill."""
    # Build the URL if we have a GitHub source
    skill_url = None
    if source_url:
        # Strip trailing .git and slashes
        base = source_url.rstrip("/")
        if base.endswith(".git"):
            base = base[:-4]
        skill_path = scan_entry.get("path", "")
        # Remove SKILL.md from path to get directory
        dir_path = str(Path(skill_path).parent)
        skill_url = f"{base}/tree/main/{dir_path}"

    # Frontmatter — normalize metadata keys
    fm = scan_entry.get("frontmatter") or {}
    metadata = fm.get("metadata", {})
    if isinstance(metadata, str):
        metadata = {}

    # Default evaluation if not provided
    default_eval = {
        "usage_value": {
            "score": 0,
            "rationale": "Auto-generated from scan-only fallback.",
            "sub_scores": {
                "problem_clarity": 0,
                "audience_breadth": 0,
                "capability_gap": 0,
                "actionability": 0,
                "reusability": 0,
            },
            "weighted_score": 0,
            "domain_calibration_bonus": 0,
            "method_version": "weighted-v2",
        },
        "security_risk": {
            "rating": "unknown",
            "rationale": "Auto-generated from scan-only fallback.",
            "findings": [],
            "sub_scores": {
                "data_privacy": 0,
                "prompt_injection": 0,
                "illegal_content": 0,
                "bias": 0,
                "system_integrity": 0,
                "untrusted_communication": 0,
            },
        },
        "executability": {
            "score": 0,
            "completeness": 0,
            "determinism": 0,
            "consistency": 0,
            "usability": 0,
            "rationale": "Auto-generated from scan-only fallback.",
        },
        "invocability": {
            "score": 0,
            "rationale": "Auto-generated from scan-only fallback.",
        },
        "over_specification_risk": {
            "flagged": False,
            "rationale": "Auto-generated from scan-only fallback.",
        },
        "core_capabilities": "Auto-generated from scan-only fallback.",
        "external_requirements_indicator": "unknown",
        "external_requirements": ["unknown"],
        "script_languages": scan_entry.get("script_languages", ["none"]),
        "license": scan_entry.get("license", "unspecified"),
    }

    evaluation = normalize_evaluation(
        eval_entry if eval_entry else default_eval,
        fm,
        scan_entry,
    )

    # Always override script_languages and license from scan data (mechanical)
    evaluation["script_languages"] = scan_entry.get("script_languages", ["none"])
    evaluation["license"] = scan_entry.get("license", "unspecified")

    # Enrich structure with computed fields
    structure = dict(scan_entry.get("structure", {}))
    tokens = structure.get("estimated_tokens", 0)
    if "complexity_class" not in structure:
        if tokens < 800:
            structure["complexity_class"] = "compact"
        elif tokens <= 1200:
            structure["complexity_class"] = "detailed"
        else:
            structure["complexity_class"] = "comprehensive"
    if "skill_pattern" not in structure:
        if structure.get("has_agents"):
            structure["skill_pattern"] = "C"
        elif structure.get("has_scripts"):
            structure["skill_pattern"] = "B"
        else:
            structure["skill_pattern"] = "A"

    return {
        "name": scan_entry.get("name", "unknown"),
        "source_id": source_id,
        "path": scan_entry.get("path", ""),
        "url": skill_url,
        "frontmatter": {
            "name": fm.get("name"),
            "description": fm.get("description"),
            "license": fm.get("license"),
            "compatibility": fm.get("compatibility"),
            "allowed_tools": fm.get("allowed-tools"),
            "metadata": {
                "version": metadata.get("version"),
                "domain": metadata.get("domain"),
                "triggers": metadata.get("triggers"),
                "role": metadata.get("role"),
                "scope": metadata.get("scope"),
                "output_format": metadata.get("output-format") or metadata.get("output_format"),
                "related_skills": metadata.get("related-skills") or metadata.get("related_skills"),
            },
        },
        "structure": structure,
        "evaluation": evaluation,
    }


def compute_summary(skill_entries: list[dict]) -> dict:
    """Compute aggregate summary statistics."""
    total = len(skill_entries)
    evaluated = sum(
        1 for s in skill_entries
        if s["evaluation"]["usage_value"]["score"] > 0
    )
    parse_errors = sum(1 for s in skill_entries if "error" in s.get("path", ""))

    usage_scores = [
        s["evaluation"]["usage_value"]["score"]
        for s in skill_entries
        if s["evaluation"]["usage_value"]["score"] > 0
    ]
    exec_scores = [
        s["evaluation"]["executability"]["score"]
        for s in skill_entries
        if s["evaluation"].get("executability", {}).get("score", 0) > 0
    ]
    invoc_scores = [
        s["evaluation"]["invocability"]["score"]
        for s in skill_entries
        if s["evaluation"].get("invocability", {}).get("score", 0) > 0
    ]

    risk_dist = {"low": 0, "medium": 0, "high": 0}
    complexity_dist = {"compact": 0, "detailed": 0, "comprehensive": 0}
    pattern_dist = {"A": 0, "B": 0, "C": 0}
    over_spec_flagged = 0
    for s in skill_entries:
        rating = s["evaluation"]["security_risk"]["rating"]
        if rating in risk_dist:
            risk_dist[rating] += 1
        cc = s["structure"].get("complexity_class", "")
        if cc in complexity_dist:
            complexity_dist[cc] += 1
        sp = s["structure"].get("skill_pattern", "")
        if sp in pattern_dist:
            pattern_dist[sp] += 1
        if s["evaluation"].get("over_specification_risk", {}).get("flagged", False):
            over_spec_flagged += 1

    return {
        "total_skills": total,
        "evaluated": evaluated,
        "parse_errors": parse_errors,
        "avg_usage_value": round(sum(usage_scores) / len(usage_scores), 2) if usage_scores else 0,
        "avg_executability": round(sum(exec_scores) / len(exec_scores), 2) if exec_scores else 0,
        "avg_invocability": round(sum(invoc_scores) / len(invoc_scores), 2) if invoc_scores else 0,
        "security_risk_distribution": risk_dist,
        "complexity_distribution": complexity_dist,
        "pattern_distribution": pattern_dist,
        "over_specification_flagged": over_spec_flagged,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Assemble a skill catalog from scan results and evaluations"
    )
    parser.add_argument("scan_results", help="Path to scan results JSON from scan_skills.py")
    parser.add_argument("evaluations", help="Path to evaluations JSON from agent review")
    parser.add_argument(
        "--output", "-o", default="skill-catalog.json",
        help="Output catalog JSON path (default: skill-catalog.json)",
    )
    parser.add_argument("--source-url", help="GitHub repository URL (if applicable)")
    parser.add_argument(
        "--source-type", default="local", choices=["local", "github"],
        help="Source type (default: local)",
    )
    parser.add_argument(
        "--allow-missing-evaluations",
        action="store_true",
        help=(
            "Allow scan entries without matching evaluations. When unset, "
            "the assembler fails fast to prevent unevaluated skills."
        ),
    )
    parser.add_argument(
        "--allow-duplicate-names",
        action="store_true",
        help=(
            "Allow duplicate skill names from scan results. When unset, "
            "duplicate names are deterministically deduped (first occurrence kept)."
        ),
    )
    args = parser.parse_args()

    scan_data = load_json(args.scan_results)
    eval_data = load_json(args.evaluations)

    # Build evaluation lookup by skill name
    eval_lookup = {}
    if isinstance(eval_data, list):
        for entry in eval_data:
            name = entry.get("name", "")
            eval_lookup[normalize_key(name)] = entry.get("evaluation", entry)
    elif isinstance(eval_data, dict) and "skills" in eval_data:
        for entry in eval_data["skills"]:
            name = entry.get("name", "")
            eval_lookup[normalize_key(name)] = entry.get("evaluation", entry)

    source = build_source(scan_data, args.source_url, args.source_type)

    scan_entries = scan_data.get("skills", [])
    deduped_scan_entries = []
    seen_names = set()
    dropped_duplicates = []
    for scan_entry in scan_entries:
        name_key = normalize_key(scan_entry.get("name", ""))
        if not args.allow_duplicate_names and name_key in seen_names:
            dropped_duplicates.append(scan_entry.get("name", ""))
            continue
        seen_names.add(name_key)
        deduped_scan_entries.append(scan_entry)

    missing_evaluations = []
    for scan_entry in deduped_scan_entries:
        if resolve_evaluation_for_scan_entry(scan_entry, eval_lookup) is None:
            missing_evaluations.append(scan_entry.get("name", ""))

    if missing_evaluations and not args.allow_missing_evaluations:
        sample = ", ".join(missing_evaluations[:10])
        print(
            (
                "Error: missing evaluations for "
                f"{len(missing_evaluations)} scanned skills. "
                "Rerun evaluator or pass --allow-missing-evaluations. "
                f"Examples: {sample}"
            ),
            file=sys.stderr,
        )
        sys.exit(2)

    if dropped_duplicates:
        print(
            (
                "Warning: dropped duplicate scan entries by name "
                f"({len(dropped_duplicates)} dropped)."
            ),
            file=sys.stderr,
        )

    skill_entries = []
    for scan_entry in deduped_scan_entries:
        name = scan_entry.get("name", "")
        eval_entry = resolve_evaluation_for_scan_entry(scan_entry, eval_lookup)
        entry = build_skill_entry(scan_entry, eval_entry, source["id"], args.source_url)
        skill_entries.append(entry)

    catalog = {
        "catalog_version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "sources": [source],
        "summary": compute_summary(skill_entries),
        "skills": skill_entries,
    }

    output_path = Path(args.output)
    output_path.write_text(
        json.dumps(catalog, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"Catalog written to {output_path} ({len(skill_entries)} skills)", file=sys.stderr)


if __name__ == "__main__":
    main()
