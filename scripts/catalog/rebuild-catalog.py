#!/usr/bin/env python3
"""
Rebuild skill-catalog.json by merging:
 - New scan results (output/skill-catalog-scan.json)
 - Old evaluations (output/skill-catalog.json)
 - Manually authored evaluations for new skills (embedded below)

Usage:
    python scripts/catalog/rebuild-catalog.py
"""

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCAN_FILE = ROOT / "skill-catalog-scan.json"
OLD_CATALOG = ROOT / "skill-catalog.json"
OUT_FILE = ROOT / "skill-catalog.json"
EVALUATIONS_FILE = ROOT / "skill-catalog-evaluations.json"
PACKS_DIR = ROOT / "packs"


# ---------------------------------------------------------------------------
# Complexity and pattern classification helpers
# ---------------------------------------------------------------------------

def classify_complexity(estimated_tokens: int) -> str:
    if estimated_tokens < 700:
        return "compact"
    if estimated_tokens < 2000:
        return "detailed"
    return "comprehensive"


def classify_pattern(has_scripts: bool) -> str:
    return "B" if has_scripts else "A"


# ---------------------------------------------------------------------------
# Pack helpers
# ---------------------------------------------------------------------------

def load_packs() -> dict:
    """Load all pack manifests from packs/ and return a dict keyed by pack name."""
    packs = {}
    if PACKS_DIR.exists():
        for f in sorted(PACKS_DIR.glob("*.json")):
            try:
                pack = json.loads(f.read_text(encoding="utf-8"))
                packs[pack["name"]] = pack
            except Exception:
                pass
    return packs


def resolve_skill_packs(skill_name: str, packs: dict) -> list:
    """Return sorted list of pack names that claim this skill."""
    result = []
    for pack_name, pack in packs.items():
        for pattern in pack.get("skills", []):
            if pattern.endswith("*"):
                if skill_name.startswith(pattern[:-1]):
                    result.append(pack_name)
                    break
            elif skill_name == pattern:
                result.append(pack_name)
                break
    return sorted(result)


# ---------------------------------------------------------------------------
# Evaluations for the 7 new skills
# All scores follow the same extended schema as the existing catalog.
# ---------------------------------------------------------------------------

NEW_EVALUATIONS = {
    "strategy-decision-documenter": {
        "usage_value": {
            "score": 4,
            "rationale": "Addresses a practical workflow with solid reuse beyond a single project. Pairing live interrogation with real-time CONTEXT.md and ADR updates is a genuine productivity multiplier for design teams.",
        },
        "security_risk": {
            "rating": "low",
            "rationale": "Pure instruction-led skill. No scripts, no external URLs, no credential references.",
            "findings": [],
            "sub_scores": {
                "data_privacy": 5,
                "prompt_injection": 5,
                "illegal_content": 5,
                "bias": 5,
                "system_integrity": 5,
                "untrusted_communication": 5,
            },
        },
        "executability": {
            "score": 4,
            "completeness": 4,
            "determinism": 4,
            "consistency": 5,
            "usability": 4,
            "rationale": "Clear five-step workflow with specific turn patterns. Minor interpretation required for context-doc location heuristics.",
        },
        "invocability": {
            "score": 4,
            "rationale": "Triggers and description are specific; name could overlap with general documentation skills but anti-triggers and priority field mitigate collision.",
        },
        "over_specification_risk": {
            "flagged": False,
            "rationale": "Workflow is framed as reusable guidance; no hardcoded paths or project-specific assumptions.",
        },
        "core_capabilities": "strategy-decision-documenter is an instruction-led skill. Combines Socratic plan interrogation with real-time documentation edits — grilling one question per turn while updating CONTEXT.md, CONTEXT-MAP.md, and ADRs whenever terms or decisions resolve. Primary output: sharpened domain vocabulary and durable decision records.",
        "external_requirements_indicator": "self-contained",
        "external_requirements": ["none"],
    },
    "strategy-decision-interrogator": {
        "usage_value": {
            "score": 4,
            "rationale": "Highly useful for design and planning sessions. The one-question-at-a-time Socratic pattern is a real workflow enhancer with broad appeal across tech and strategy teams.",
        },
        "security_risk": {
            "rating": "low",
            "rationale": "Pure instruction-led skill. No scripts, no external URLs, no credential references.",
            "findings": [],
            "sub_scores": {
                "data_privacy": 5,
                "prompt_injection": 5,
                "illegal_content": 5,
                "bias": 5,
                "system_integrity": 5,
                "untrusted_communication": 5,
            },
        },
        "executability": {
            "score": 4,
            "completeness": 4,
            "determinism": 4,
            "consistency": 5,
            "usability": 4,
            "rationale": "Workflow is clear and well-structured. Compact skill by design — no references needed.",
        },
        "invocability": {
            "score": 5,
            "rationale": "Triggers like 'grill me' and 'ask one at a time' are distinctive; strong anti-triggers prevent doc-editing collision.",
        },
        "over_specification_risk": {
            "flagged": False,
            "rationale": "Workflow is fully generic — no project-specific assumptions.",
        },
        "core_capabilities": "strategy-decision-interrogator is an instruction-led skill. Runs live, dependency-ordered Socratic interrogation of plans and designs — one precise question per turn with a recommended answer and rationale, narrowing ambiguity through sequential branch resolution. Primary output: a clarified decision tree with resolved branches and locked choices.",
        "external_requirements_indicator": "self-contained",
        "external_requirements": ["none"],
    },
    "tech-dev-git-commit": {
        "usage_value": {
            "score": 5,
            "rationale": "Git commit-and-push is an extremely high-frequency developer task. Every dev team benefits from consistent Conventional Commit message formatting with minimal friction.",
        },
        "security_risk": {
            "rating": "low",
            "rationale": "Pure instruction-led skill. No scripts, no external URLs, no credential references. Git push guidance is user-executed, not agent-executed.",
            "findings": [],
            "sub_scores": {
                "data_privacy": 5,
                "prompt_injection": 5,
                "illegal_content": 5,
                "bias": 5,
                "system_integrity": 4,
                "untrusted_communication": 5,
            },
        },
        "executability": {
            "score": 4,
            "completeness": 4,
            "determinism": 5,
            "consistency": 5,
            "usability": 4,
            "rationale": "Step sequence is deterministic. Caveman writing style is intentional compression — functional but unconventional.",
        },
        "invocability": {
            "score": 5,
            "rationale": "Triggers are precise git action phrases; anti-triggers cleanly separate from workflow-design use cases.",
        },
        "over_specification_risk": {
            "flagged": False,
            "rationale": "Workflow is platform-agnostic and applies to any git repository.",
        },
        "core_capabilities": "tech-dev-git-commit is an instruction-led skill. Executes the full git commit-and-push cycle — inspecting diffs, categorizing changes, drafting tight Conventional Commit messages (≤50 char subject, imperative mood), staging appropriate files, committing, and pushing. Primary output: executed git commands with a precisely formatted commit message.",
        "external_requirements_indicator": "self-contained",
        "external_requirements": ["none"],
    },
    "tech-dev-git-finish-branch": {
        "usage_value": {
            "score": 4,
            "rationale": "Completing development work and integrating branches is a common, important workflow. The four-option menu (merge, PR, keep, discard) with test verification makes this broadly useful.",
        },
        "security_risk": {
            "rating": "medium",
            "rationale": "The workflow guides git merge, git push, and PR creation — modifying remote repository state. No scripts, but system-state modification via user-executed commands warrants medium.",
            "findings": [
                "Workflow instructs git push to remote repository.",
                "Workflow instructs branch deletion after merge.",
            ],
            "sub_scores": {
                "data_privacy": 5,
                "prompt_injection": 5,
                "illegal_content": 5,
                "bias": 5,
                "system_integrity": 3,
                "untrusted_communication": 5,
            },
        },
        "executability": {
            "score": 4,
            "completeness": 4,
            "determinism": 4,
            "consistency": 5,
            "usability": 4,
            "rationale": "Workflow is clear with well-defined decision branches. Missing license field is a minor spec gap.",
        },
        "invocability": {
            "score": 5,
            "rationale": "Triggers like 'finish branch', 'merge branch', and 'create pull request' are specific and unambiguous.",
        },
        "over_specification_risk": {
            "flagged": False,
            "rationale": "Workflow is generic — no project-specific assumptions beyond detecting base branch name.",
        },
        "core_capabilities": "tech-dev-git-finish-branch is an instruction-led skill. Guides branch completion with test verification, a four-option integration menu (local merge, PR, keep, or discard), and post-merge cleanup. Primary output: executed branch integration with optional automated PR creation and local branch cleanup.",
        "external_requirements_indicator": "self-contained",
        "external_requirements": ["none"],
    },
    "tech-dev-git-start-branch": {
        "usage_value": {
            "score": 5,
            "rationale": "Starting a properly-named branch from an up-to-date base is a foundational, high-frequency developer action. Consistent naming and upstream tracking prevent common team friction.",
        },
        "security_risk": {
            "rating": "low",
            "rationale": "Pure instruction-led skill. Creates local branches and pulls base — non-destructive operations. No scripts, no external URLs, no credential references.",
            "findings": [],
            "sub_scores": {
                "data_privacy": 5,
                "prompt_injection": 5,
                "illegal_content": 5,
                "bias": 5,
                "system_integrity": 5,
                "untrusted_communication": 5,
            },
        },
        "executability": {
            "score": 4,
            "completeness": 4,
            "determinism": 5,
            "consistency": 5,
            "usability": 4,
            "rationale": "Step sequence is clear and deterministic. Proposes branch name before executing — good confirmation gate.",
        },
        "invocability": {
            "score": 5,
            "rationale": "Triggers are precise; anti-triggers cleanly separate from commit/merge/finish-branch scenarios.",
        },
        "over_specification_risk": {
            "flagged": False,
            "rationale": "GitHub Flow naming conventions are widely applicable — no hardcoded project assumptions.",
        },
        "core_capabilities": "tech-dev-git-start-branch is an instruction-led skill. Infers work type, derives a kebab-case branch name (with optional ticket prefix), updates the base branch with --ff-only, creates the branch, and sets upstream tracking. Primary output: a correctly named, up-to-date development branch with upstream tracking confirmed.",
        "external_requirements_indicator": "self-contained",
        "external_requirements": ["none"],
    },
    "tech-dev-git-workflow-design": {
        "usage_value": {
            "score": 4,
            "rationale": "Git workflow design is an important team-level decision. Well-scoped for team leads and platform engineers; reference loading table is exemplary.",
        },
        "security_risk": {
            "rating": "low",
            "rationale": "Pure advisory skill with no scripts and no external service calls. Explicitly warns about destructive commands like --force.",
            "findings": [],
            "sub_scores": {
                "data_privacy": 5,
                "prompt_injection": 5,
                "illegal_content": 5,
                "bias": 5,
                "system_integrity": 5,
                "untrusted_communication": 5,
            },
        },
        "executability": {
            "score": 5,
            "completeness": 5,
            "determinism": 4,
            "consistency": 5,
            "usability": 5,
            "rationale": "Excellent reference loading table, clear workflow, explicit MUST/MUST NOT constraints, and Knowledge Reference section — exemplary structure.",
        },
        "invocability": {
            "score": 5,
            "rationale": "Specific advisory triggers; strong anti-triggers prevent collision with action-oriented git skills.",
        },
        "over_specification_risk": {
            "flagged": False,
            "rationale": "Workflow is framed as tailored-to-context guidance — no hardcoded assumptions.",
        },
        "core_capabilities": "tech-dev-git-workflow-design is an instruction-led skill. Advises teams on branching strategy, commit conventions, merge vs rebase trade-offs, PR processes, conflict resolution, and release management by loading domain-specific reference files on demand. Primary output: tailored workflow recommendations with copy-paste ready commands, templates, and configuration.",
        "external_requirements_indicator": "self-contained",
        "external_requirements": ["none"],
    },
    "tech-github-repo-standards": {
        "usage_value": {
            "score": 4,
            "rationale": "Repository standardization at scale is genuinely valuable for platform engineers and compliance-oriented teams. Four profiles and two context modes make this practical for diverse org types.",
        },
        "security_risk": {
            "rating": "high",
            "rationale": "Applies branch protection, security scanning, and access controls directly to GitHub repositories via the gh CLI with admin-level permissions. Modifies shared infrastructure. References credential scopes and token requirements.",
            "findings": [
                "Directly modifies GitHub repository settings via gh CLI API calls.",
                "Requires admin permissions on target repository.",
                "References token scopes and authentication credentials.",
                "Scanner detected install/credential patterns in skill content.",
                "Modifies branch protection rules that could lock out contributors if misconfigured.",
            ],
            "sub_scores": {
                "data_privacy": 4,
                "prompt_injection": 4,
                "illegal_content": 5,
                "bias": 5,
                "system_integrity": 2,
                "untrusted_communication": 3,
            },
        },
        "executability": {
            "score": 5,
            "completeness": 5,
            "determinism": 5,
            "consistency": 5,
            "usability": 4,
            "rationale": "Comprehensive workflow with input validation, dry-run support, profile matrix, and prerequisite checks. One of the most thoroughly designed skills in the collection.",
        },
        "invocability": {
            "score": 5,
            "rationale": "Specific triggers; compatibility field documents runtime requirement upfront; description clearly distinguishes from general GitHub ops.",
        },
        "over_specification_risk": {
            "flagged": True,
            "rationale": "Bakes in specific gh CLI version requirement (≥ 2.28) and fixed profile names. Profiles are intentional design choices but tie the skill to a specific version contract.",
        },
        "core_capabilities": "tech-github-repo-standards is an instruction-led skill. Applies standardized branch protection, security scanning, access controls, and file artifacts to one or more GitHub repositories via the gh CLI across four configurable profiles (standard, collaborative, monorepo, regulated) and two context modes (internal, external). Primary output: applied repository settings plus a pull request delivering generated file artifacts.",
        "external_requirements_indicator": "has-external-dependencies",
        "external_requirements": ["gh CLI ≥ 2.28", "GitHub API (admin permissions)"],
    },
}


# ---------------------------------------------------------------------------
# Main rebuild logic
# ---------------------------------------------------------------------------

def compute_avg(skills, key_path):
    """Compute average of a nested score field across all skills."""
    values = []
    for s in skills:
        ev = s.get("evaluation", {})
        node = ev
        for k in key_path:
            if isinstance(node, dict):
                node = node.get(k)
            else:
                node = None
                break
        if isinstance(node, (int, float)):
            values.append(node)
    return round(sum(values) / len(values), 2) if values else 0.0


def without_generated_at(catalog: dict) -> dict:
    comparable = dict(catalog)
    comparable.pop("generated_at", None)
    return comparable


def main():
    # Load inputs
    scan_data = json.loads(SCAN_FILE.read_text(encoding="utf-8"))
    old_catalog = json.loads(OLD_CATALOG.read_text(encoding="utf-8"))

    # Load pack manifests
    packs = load_packs()

    # Load external evaluations file (highest priority)
    fresh_evals = {}
    if EVALUATIONS_FILE.exists():
        raw_evals = json.loads(EVALUATIONS_FILE.read_text(encoding="utf-8"))
        fresh_evals = {e["name"]: e["evaluation"] for e in raw_evals}

    # Index old evaluations by skill name
    old_evals = {s["name"]: s for s in old_catalog["skills"]}

    # Index scan results by skill name
    scan_by_name = {s["name"]: s for s in scan_data["skills"]}

    skills_out = []
    parse_errors = 0

    for scan_entry in scan_data["skills"]:
        if "error" in scan_entry:
            parse_errors += 1
            continue

        name = scan_entry["name"]
        fm = scan_entry.get("frontmatter") or {}
        metadata = fm.get("metadata", {})
        if isinstance(metadata, str):
            metadata = {}

        # Structure block — prefer old catalog values for complexity/pattern
        raw_structure = scan_entry.get("structure", {})
        complexity = raw_structure.get("complexity_class")
        pattern = raw_structure.get("skill_pattern")

        if name in old_evals:
            old_struct = old_evals[name].get("structure", {})
            if not complexity:
                complexity = old_struct.get("complexity_class") or classify_complexity(
                    raw_structure.get("estimated_tokens", 0)
                )
            if not pattern:
                pattern = old_struct.get("skill_pattern") or classify_pattern(
                    raw_structure.get("has_scripts", False)
                )
        else:
            # New skill — compute from scan data
            complexity = classify_complexity(raw_structure.get("estimated_tokens", 0))
            pattern = classify_pattern(raw_structure.get("has_scripts", False))

        structure_block = {
            "has_scripts": raw_structure.get("has_scripts", False),
            "has_references": raw_structure.get("has_references", False),
            "has_agents": raw_structure.get("has_agents", False),
            "has_assets": raw_structure.get("has_assets", False),
            "has_license_file": raw_structure.get("has_license_file", False),
            "file_count": raw_structure.get("file_count", 0),
            "estimated_tokens": raw_structure.get("estimated_tokens", 0),
            "complexity_class": complexity,
            "skill_pattern": pattern,
        }

        # Evaluation priority: fresh_evals > NEW_EVALUATIONS > old_evals > placeholder
        if name in fresh_evals:
            evaluation = {**fresh_evals[name]}
            # Refresh mechanical fields from scan
            evaluation["script_languages"] = scan_entry.get("script_languages", ["none"])
            evaluation["license"] = scan_entry.get("license", "unspecified")
        elif name in NEW_EVALUATIONS:
            evaluation = {**NEW_EVALUATIONS[name]}
            # Override mechanically-extracted fields from scan
            evaluation["script_languages"] = scan_entry.get("script_languages", ["none"])
            evaluation["license"] = scan_entry.get("license", "unspecified")
        elif name in old_evals:
            evaluation = old_evals[name].get("evaluation", {})
            # Refresh mechanical fields
            evaluation["script_languages"] = scan_entry.get("script_languages", ["none"])
            evaluation["license"] = scan_entry.get("license", "unspecified")
        else:
            evaluation = {
                "usage_value": {"score": 0, "rationale": "Not evaluated"},
                "security_risk": {"rating": "unknown", "rationale": "Not evaluated", "findings": []},
                "executability": {"score": 0, "rationale": "Not evaluated"},
                "invocability": {"score": 0, "rationale": "Not evaluated"},
                "over_specification_risk": {"flagged": False, "rationale": "Not evaluated"},
                "core_capabilities": "Not evaluated",
                "external_requirements_indicator": "unknown",
                "external_requirements": ["unknown"],
                "script_languages": scan_entry.get("script_languages", ["none"]),
                "license": scan_entry.get("license", "unspecified"),
            }

        skill_entry = {
            "name": name,
            "source_id": "source-1",
            "path": scan_entry.get("path", ""),
            "url": None,
            "packs": resolve_skill_packs(name, packs),
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
            "structure": structure_block,
            "evaluation": evaluation,
        }
        skills_out.append(skill_entry)

    # ---------------------------------------------------------------------------
    # Summary statistics
    # ---------------------------------------------------------------------------
    total = len(skills_out)
    evaluated = sum(
        1 for s in skills_out
        if s["evaluation"].get("usage_value", {}).get("score", 0) > 0
    )
    avg_usage = compute_avg(skills_out, ["usage_value", "score"])
    avg_exec = compute_avg(skills_out, ["executability", "score"])
    avg_invoc = compute_avg(skills_out, ["invocability", "score"])

    sec_dist = {"low": 0, "medium": 0, "high": 0}
    for s in skills_out:
        rating = s["evaluation"].get("security_risk", {}).get("rating", "unknown")
        if rating in sec_dist:
            sec_dist[rating] += 1

    complexity_dist = {"compact": 0, "detailed": 0, "comprehensive": 0}
    for s in skills_out:
        cc = s["structure"].get("complexity_class", "")
        if cc in complexity_dist:
            complexity_dist[cc] += 1

    pattern_dist = {"A": 0, "B": 0, "C": 0}
    for s in skills_out:
        p = s["structure"].get("skill_pattern", "")
        if p in pattern_dist:
            pattern_dist[p] += 1

    over_spec_flagged = sum(
        1 for s in skills_out
        if s["evaluation"].get("over_specification_risk", {}).get("flagged", False)
    )

    # Pack summary: name, description, skill_count, skills list
    packs_summary = {}
    for pack_name, pack in packs.items():
        member_skills = [s["name"] for s in skills_out if pack_name in s["packs"]]
        packs_summary[pack_name] = {
            "description": pack.get("description", ""),
            "version": pack.get("version", "1.0.0"),
            "skill_count": len(member_skills),
            "skills": sorted(member_skills),
        }

    catalog = {
        "catalog_version": "1.0.0",
        "generated_at": old_catalog.get("generated_at"),
        "sources": [
            {
                "id": "source-1",
                "type": "local",
                "path": "skills",
                "url": None,
                "commit": None,
            }
        ],
        "summary": {
            "total_skills": total,
            "evaluated": evaluated,
            "parse_errors": parse_errors,
            "avg_usage_value": avg_usage,
            "avg_executability": avg_exec,
            "avg_invocability": avg_invoc,
            "security_risk_distribution": sec_dist,
            "complexity_distribution": complexity_dist,
            "pattern_distribution": {k: v for k, v in pattern_dist.items() if v > 0},
            "over_specification_flagged": over_spec_flagged,
            "packs": packs_summary,
        },
        "skills": skills_out,
    }

    if not catalog["generated_at"] or without_generated_at(old_catalog) != without_generated_at(catalog):
        catalog["generated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    OUT_FILE.write_text(
        json.dumps(catalog, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"Catalog written: {OUT_FILE}")
    print(f"  Total skills : {total}")
    print(f"  Evaluated    : {evaluated}")
    print(f"  Fresh evals  : {len(fresh_evals)}")
    print(f"  Parse errors : {parse_errors}")
    print(f"  Avg usage    : {avg_usage}")
    print(f"  Avg exec     : {avg_exec}")
    print(f"  Security     : {sec_dist}")
    print(f"  Complexity   : {complexity_dist}")
    print(f"  Over-spec    : {over_spec_flagged}")


if __name__ == "__main__":
    main()
