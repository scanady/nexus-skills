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
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def load_json(path: str) -> dict:
    """Load and parse a JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


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
        "usage_value": {"score": 0, "rationale": "Not evaluated"},
        "security_risk": {
            "rating": "unknown",
            "rationale": "Not evaluated",
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
            "rationale": "Not evaluated",
        },
        "invocability": {"score": 0, "rationale": "Not evaluated"},
        "over_specification_risk": {"flagged": False, "rationale": "Not evaluated"},
        "core_capabilities": "Not evaluated",
        "external_requirements_indicator": "unknown",
        "external_requirements": ["unknown"],
        "script_languages": scan_entry.get("script_languages", ["none"]),
        "license": scan_entry.get("license", "unspecified"),
    }

    evaluation = eval_entry if eval_entry else default_eval

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
    args = parser.parse_args()

    scan_data = load_json(args.scan_results)
    eval_data = load_json(args.evaluations)

    # Build evaluation lookup by skill name
    eval_lookup = {}
    if isinstance(eval_data, list):
        for entry in eval_data:
            name = entry.get("name", "")
            eval_lookup[name] = entry.get("evaluation", entry)
    elif isinstance(eval_data, dict) and "skills" in eval_data:
        for entry in eval_data["skills"]:
            name = entry.get("name", "")
            eval_lookup[name] = entry.get("evaluation", entry)

    source = build_source(scan_data, args.source_url, args.source_type)

    skill_entries = []
    for scan_entry in scan_data.get("skills", []):
        name = scan_entry.get("name", "")
        eval_entry = eval_lookup.get(name)
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
    output_path.write_text(json.dumps(catalog, indent=2, ensure_ascii=False))
    print(f"Catalog written to {output_path} ({len(skill_entries)} skills)", file=sys.stderr)


if __name__ == "__main__":
    main()
