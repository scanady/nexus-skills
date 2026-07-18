#!/usr/bin/env python3
"""Validate the Outcome Design Agent Skill package using only the standard library."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "assets/outcome-design-record.md",
    "references/methodology.md",
    "references/patterns.md",
    "references/quality-rubric.md",
    "evals/evals.json",
    "evals/trigger-queries.json",
]

REQUIRED_TEMPLATE_TERMS = [
    "Handoff summary",
    "Desired outcome",
    "Success and evidence",
    "Causal design",
    "Assumptions, feasibility, and risk",
    "Readiness assessment",
    "Downstream contract",
]


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def parse_frontmatter(text: str) -> dict[str, object]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("SKILL.md frontmatter is not closed")
    block = text[4:end]
    result: dict[str, object] = {}
    metadata: dict[str, str] = {}
    current_map: str | None = None

    for raw_line in block.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if raw_line.startswith("  ") and current_map == "metadata":
            key, sep, value = raw_line.strip().partition(":")
            if not sep:
                raise ValueError(f"Invalid metadata line: {raw_line}")
            metadata[key.strip()] = value.strip().strip('"\'')
            continue
        key, sep, value = raw_line.partition(":")
        if not sep:
            raise ValueError(f"Invalid frontmatter line: {raw_line}")
        key = key.strip()
        value = value.strip()
        if key == "metadata" and not value:
            current_map = "metadata"
            result["metadata"] = metadata
        else:
            current_map = None
            result[key] = value.strip('"\'')
    return result


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    errors: list[str] = []

    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            fail(errors, f"Missing required file: {relative}")

    skill_path = root / "SKILL.md"
    if skill_path.is_file():
        skill_text = skill_path.read_text(encoding="utf-8")
        try:
            frontmatter = parse_frontmatter(skill_text)
        except ValueError as exc:
            fail(errors, str(exc))
            frontmatter = {}

        name = str(frontmatter.get("name", ""))
        description = str(frontmatter.get("description", ""))
        metadata = frontmatter.get("metadata", {})

        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            fail(errors, "Frontmatter name must contain lowercase letters, numbers, and single hyphens only")
        if name and root.name != name:
            fail(errors, f"Directory name '{root.name}' must match skill name '{name}'")
        if not description:
            fail(errors, "Frontmatter description is required")
        if len(description) > 1024:
            fail(errors, f"Description is {len(description)} characters; maximum is 1024")
        if "version" in frontmatter:
            fail(errors, "Version must be nested under metadata, not a top-level frontmatter field")
        if not isinstance(metadata, dict) or not metadata.get("version"):
            fail(errors, "metadata.version is required for this package")
        if len(skill_text.splitlines()) > 500:
            fail(errors, "SKILL.md exceeds the recommended 500-line limit")
        if len(skill_text) / 4 > 5000:
            fail(errors, "SKILL.md exceeds the recommended approximate 5,000-token limit")

        links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", skill_text)
        for link in links:
            if "://" in link or link.startswith("#"):
                continue
            if not (root / link).is_file():
                fail(errors, f"Broken relative link in SKILL.md: {link}")

    template_path = root / "assets/outcome-design-record.md"
    if template_path.is_file():
        template = template_path.read_text(encoding="utf-8")
        for term in REQUIRED_TEMPLATE_TERMS:
            if term not in template:
                fail(errors, f"Record template is missing required term: {term}")

    evals_path = root / "evals/evals.json"
    if evals_path.is_file():
        try:
            evals = json.loads(evals_path.read_text(encoding="utf-8"))
            if evals.get("skill_name") != root.name:
                fail(errors, "evals.json skill_name must match the directory name")
            if len(evals.get("evals", [])) < 3:
                fail(errors, "evals.json should contain at least three evaluations")
            for item in evals.get("evals", []):
                for field in ("id", "prompt", "expected_output", "assertions"):
                    if field not in item:
                        fail(errors, f"Evaluation is missing field '{field}': {item}")
        except json.JSONDecodeError as exc:
            fail(errors, f"Invalid evals/evals.json: {exc}")

    triggers_path = root / "evals/trigger-queries.json"
    if triggers_path.is_file():
        try:
            queries = json.loads(triggers_path.read_text(encoding="utf-8"))
            positives = sum(1 for item in queries if item.get("should_trigger") is True)
            negatives = sum(1 for item in queries if item.get("should_trigger") is False)
            if positives < 5 or negatives < 5:
                fail(errors, "Trigger query suite needs at least five positive and five negative cases")
            for item in queries:
                if "query" not in item or "should_trigger" not in item:
                    fail(errors, f"Invalid trigger query entry: {item}")
        except json.JSONDecodeError as exc:
            fail(errors, f"Invalid evals/trigger-queries.json: {exc}")

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Validation passed: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
