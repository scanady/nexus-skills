#!/usr/bin/env python3
"""Validate an Agent Skill for spec compliance and best practices.

Performs mechanical checks that don't require LLM judgment:
- Frontmatter field validation (name, description, license, etc.)
- Name format and length
- Description length and content flags
- Unknown frontmatter fields
- SKILL.md line count
- Directory/name consistency
- Metadata block completeness
- Bundled resource structure

Usage:
    python validate.py <skill_directory>
    python validate.py <skill_directory> --json
    python validate.py <skill_directory> --strict
"""

import json
import re
import sys
from pathlib import Path


# --- Constants ---

ALLOWED_FRONTMATTER_KEYS = {
    "name", "description", "license", "allowed-tools", "metadata", "compatibility"
}

RECOMMENDED_METADATA_KEYS = {
    "domain", "triggers", "role", "scope", "output-format", "related-skills"
}

VALID_RESOURCE_DIRS = {"scripts", "references", "assets", "agents"}

MAX_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024
MAX_COMPATIBILITY_LENGTH = 500
MAX_BODY_LINES = 500
MIN_DESCRIPTION_LENGTH = 50


# --- Frontmatter Parsing ---

def parse_frontmatter(content: str) -> tuple[dict | None, str, str | None]:
    """Parse YAML frontmatter from SKILL.md content.

    Returns (frontmatter_dict, body, error_message).
    If parsing fails, frontmatter_dict is None and error_message explains why.
    """
    if not content.startswith("---"):
        return None, content, "No YAML frontmatter found (missing opening ---)"

    # Find closing ---
    lines = content.split("\n")
    end_idx = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_idx = i
            break

    if end_idx is None:
        return None, content, "Invalid frontmatter (missing closing ---)"

    frontmatter_text = "\n".join(lines[1:end_idx])
    body = "\n".join(lines[end_idx + 1:])

    # Parse without requiring PyYAML — handle simple key: value pairs
    frontmatter = _parse_simple_yaml(frontmatter_text)
    if frontmatter is None:
        return None, body, "Failed to parse frontmatter YAML"

    return frontmatter, body, None


def _parse_simple_yaml(text: str) -> dict | None:
    """Parse simple YAML frontmatter without external dependencies.

    Handles flat key-value pairs and one level of nesting (metadata block).
    For production use with complex YAML, import yaml and use yaml.safe_load().
    """
    try:
        import yaml
        result = yaml.safe_load(text)
        return result if isinstance(result, dict) else None
    except ImportError:
        pass
    except Exception:
        # YAML parse error — fall through to simple parser
        pass

    # Fallback: simple line-by-line parser
    result = {}
    current_key = None
    current_nested = None

    for line in text.split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        indent = len(line) - len(line.lstrip())

        if indent == 0 and ":" in stripped:
            key, _, value = stripped.partition(":")
            key = key.strip()
            value = value.strip().strip("'\"")

            if not value:
                # Could be a nested block
                current_key = key
                current_nested = {}
                result[key] = current_nested
            else:
                current_key = None
                current_nested = None
                # Handle multiline indicators
                if value in (">", "|", ">-", "|-"):
                    result[key] = ""
                else:
                    result[key] = value
        elif indent > 0 and current_nested is not None and ":" in stripped:
            key, _, value = stripped.partition(":")
            current_nested[key.strip()] = value.strip().strip("'\"")

    return result


# --- Validation Checks ---

class Finding:
    """A single validation finding."""

    def __init__(self, level: str, code: str, message: str):
        self.level = level  # "error", "warning", "suggestion"
        self.code = code    # e.g., "E01", "W03", "S02"
        self.message = message

    def to_dict(self) -> dict:
        return {"level": self.level, "code": self.code, "message": self.message}

    def __str__(self) -> str:
        prefix = {"error": "ERROR", "warning": "WARN", "suggestion": "INFO"}
        return f"[{self.code}] {prefix.get(self.level, '???')}: {self.message}"


def validate_skill(skill_path: Path) -> list[Finding]:
    """Run all validation checks on a skill directory. Returns list of findings."""
    findings: list[Finding] = []
    skill_path = Path(skill_path).resolve()

    # --- Check SKILL.md exists ---
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        findings.append(Finding("error", "E01", "SKILL.md not found"))
        return findings

    content = skill_md.read_text(encoding="utf-8")
    frontmatter, body, parse_error = parse_frontmatter(content)

    if parse_error:
        findings.append(Finding("error", "E02", parse_error))
        return findings

    # --- Frontmatter field checks ---
    _check_frontmatter_fields(frontmatter, findings)

    # --- Name validation ---
    _check_name(frontmatter, skill_path, findings)

    # --- Description validation ---
    _check_description(frontmatter, findings)

    # --- Compatibility validation ---
    _check_compatibility(frontmatter, findings)

    # --- Unknown fields ---
    _check_unknown_fields(frontmatter, findings)

    # --- Metadata block ---
    _check_metadata(frontmatter, findings)

    # --- Body checks ---
    _check_body(body, findings)

    # --- Directory structure ---
    _check_directory_structure(skill_path, findings)

    return findings


def _check_frontmatter_fields(fm: dict, findings: list[Finding]):
    """Check required frontmatter fields."""
    if "name" not in fm:
        findings.append(Finding("error", "E03", "Missing required 'name' field in frontmatter"))
    if "description" not in fm:
        findings.append(Finding("error", "E04", "Missing required 'description' field in frontmatter"))


def _check_name(fm: dict, skill_path: Path, findings: list[Finding]):
    """Validate the name field."""
    name = fm.get("name")
    if not name:
        return

    if not isinstance(name, str):
        findings.append(Finding("error", "E05", f"Name must be a string, got {type(name).__name__}"))
        return

    name = name.strip()

    if not re.match(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$|^[a-z0-9]$", name):
        findings.append(Finding("error", "E06",
            f"Name '{name}' must be lowercase alphanumeric + hyphens, "
            "no leading/trailing/consecutive hyphens"))
    elif "--" in name:
        findings.append(Finding("error", "E06",
            f"Name '{name}' contains consecutive hyphens"))

    if len(name) > MAX_NAME_LENGTH:
        findings.append(Finding("error", "E07",
            f"Name is {len(name)} chars, max is {MAX_NAME_LENGTH}"))

    # Check folder name matches
    folder_name = skill_path.name
    if folder_name != name:
        findings.append(Finding("error", "E08",
            f"Folder name '{folder_name}' does not match name field '{name}'"))


def _check_description(fm: dict, findings: list[Finding]):
    """Validate the description field."""
    desc = fm.get("description")
    if not desc:
        return

    if not isinstance(desc, str):
        findings.append(Finding("error", "E09",
            f"Description must be a string, got {type(desc).__name__}"))
        return

    desc = desc.strip()

    if "<" in desc or ">" in desc:
        findings.append(Finding("error", "E10",
            "Description cannot contain angle brackets (< or >)"))

    if len(desc) > MAX_DESCRIPTION_LENGTH:
        findings.append(Finding("error", "E11",
            f"Description is {len(desc)} chars, max is {MAX_DESCRIPTION_LENGTH}"))

    if len(desc) < MIN_DESCRIPTION_LENGTH:
        findings.append(Finding("warning", "W01",
            f"Description is only {len(desc)} chars — likely too short to trigger reliably. "
            "Include WHAT the skill does, WHEN to use it, and trigger keywords."))

    # Check for trigger keywords
    trigger_phrases = ["use when", "use for", "invoke when", "invoke for",
                       "activate when", "trigger when", "use this"]
    has_when = any(phrase in desc.lower() for phrase in trigger_phrases)
    if not has_when:
        findings.append(Finding("warning", "W02",
            "Description doesn't include WHEN scenarios (e.g., 'Use when...'). "
            "This may cause undertriggering."))


def _check_compatibility(fm: dict, findings: list[Finding]):
    """Validate the compatibility field if present."""
    compat = fm.get("compatibility")
    if not compat:
        return

    if not isinstance(compat, str):
        findings.append(Finding("error", "E12",
            f"Compatibility must be a string, got {type(compat).__name__}"))
        return

    if len(compat) > MAX_COMPATIBILITY_LENGTH:
        findings.append(Finding("error", "E13",
            f"Compatibility is {len(compat)} chars, max is {MAX_COMPATIBILITY_LENGTH}"))


def _check_unknown_fields(fm: dict, findings: list[Finding]):
    """Flag unknown top-level frontmatter fields."""
    unknown = set(fm.keys()) - ALLOWED_FRONTMATTER_KEYS
    if unknown:
        findings.append(Finding("error", "E14",
            f"Unknown frontmatter field(s): {', '.join(sorted(unknown))}. "
            f"Allowed: {', '.join(sorted(ALLOWED_FRONTMATTER_KEYS))}"))


def _check_metadata(fm: dict, findings: list[Finding]):
    """Check metadata block for recommended fields."""
    metadata = fm.get("metadata")
    if metadata is None:
        findings.append(Finding("warning", "W03",
            "No metadata block — missing domain, triggers, role, scope, "
            "output-format, related-skills"))
        return

    if not isinstance(metadata, dict):
        findings.append(Finding("error", "E15",
            f"Metadata must be a key-value map, got {type(metadata).__name__}"))
        return

    missing = RECOMMENDED_METADATA_KEYS - set(metadata.keys())
    if missing:
        findings.append(Finding("warning", "W04",
            f"Metadata missing recommended field(s): {', '.join(sorted(missing))}"))

    # Check triggers quality
    triggers = metadata.get("triggers", "")
    if isinstance(triggers, str) and triggers:
        trigger_count = len([t.strip() for t in triggers.split(",") if t.strip()])
        if trigger_count < 3:
            findings.append(Finding("warning", "W05",
                f"Only {trigger_count} trigger keyword(s) — consider adding more "
                "to improve activation coverage"))


def _check_body(body: str, findings: list[Finding]):
    """Check the SKILL.md body content."""
    lines = body.strip().split("\n") if body.strip() else []
    line_count = len(lines)

    if line_count > MAX_BODY_LINES:
        findings.append(Finding("error", "E16",
            f"SKILL.md body is {line_count} lines (max {MAX_BODY_LINES}). "
            "Move content to references/."))

    # Check for common structural elements
    body_lower = body.lower()

    if "## role" not in body_lower and "## role definition" not in body_lower:
        findings.append(Finding("warning", "W06",
            "No Role Definition section found"))

    if "## constraints" not in body_lower:
        findings.append(Finding("warning", "W07",
            "No Constraints section found"))

    if "must do" not in body_lower:
        findings.append(Finding("warning", "W08",
            "No MUST DO constraints found"))

    if "must not" not in body_lower:
        findings.append(Finding("warning", "W09",
            "No MUST NOT DO constraints found"))

    if "## reference" not in body_lower and "## reference guide" not in body_lower:
        findings.append(Finding("warning", "W10",
            "No Reference Guide section found"))

    if "knowledge reference" not in body_lower:
        findings.append(Finding("warning", "W11",
            "No Knowledge Reference vocabulary section found"))

    if "load when" not in body_lower and "## reference" in body_lower:
        findings.append(Finding("warning", "W12",
            "Reference table found but no 'Load When' conditional routing column"))


def _check_directory_structure(skill_path: Path, findings: list[Finding]):
    """Check bundled resource directories."""
    for item in skill_path.iterdir():
        if item.is_dir():
            if item.name.startswith("."):
                continue
            if item.name == "__pycache__":
                continue
            if item.name not in VALID_RESOURCE_DIRS:
                findings.append(Finding("warning", "W13",
                    f"Non-standard directory '{item.name}/'. "
                    f"Expected: {', '.join(sorted(VALID_RESOURCE_DIRS))}"))

            # Check for empty directories
            contents = list(item.iterdir())
            real_files = [f for f in contents if f.name != ".gitkeep"]
            if not real_files:
                findings.append(Finding("warning", "W14",
                    f"Directory '{item.name}/' is empty (only .gitkeep). "
                    "Remove empty directories from skills."))

    # Check for auxiliary files that shouldn't be in a skill
    auxiliary_files = {"README.md", "CHANGELOG.md", "CONTRIBUTING.md", "INSTALL.md"}
    for aux in auxiliary_files:
        if (skill_path / aux).exists():
            findings.append(Finding("warning", "W15",
                f"Auxiliary file '{aux}' found — skills should not include "
                "README, CHANGELOG, or installation guides"))

    # Check references/ for duplication hints
    refs_dir = skill_path / "references"
    if refs_dir.is_dir():
        for ref in refs_dir.iterdir():
            if ref.is_file() and ref.stat().st_size > 50_000:
                findings.append(Finding("suggestion", "S01",
                    f"Reference file '{ref.name}' is large ({ref.stat().st_size // 1024}KB). "
                    "Consider adding a table of contents at the top."))


# --- Output Formatting ---

def format_text(findings: list[Finding], skill_path: Path) -> str:
    """Format findings as human-readable text."""
    if not findings:
        return f"✓ {skill_path.name}: All checks passed"

    errors = [f for f in findings if f.level == "error"]
    warnings = [f for f in findings if f.level == "warning"]
    suggestions = [f for f in findings if f.level == "suggestion"]

    lines = [f"Validation results for {skill_path.name}:", ""]

    if errors:
        lines.append(f"Errors ({len(errors)}):")
        for f in errors:
            lines.append(f"  {f}")
        lines.append("")

    if warnings:
        lines.append(f"Warnings ({len(warnings)}):")
        for f in warnings:
            lines.append(f"  {f}")
        lines.append("")

    if suggestions:
        lines.append(f"Suggestions ({len(suggestions)}):")
        for f in suggestions:
            lines.append(f"  {f}")
        lines.append("")

    summary = f"Total: {len(errors)} error(s), {len(warnings)} warning(s), {len(suggestions)} suggestion(s)"
    lines.append(summary)

    return "\n".join(lines)


def format_json(findings: list[Finding], skill_path: Path) -> str:
    """Format findings as JSON."""
    return json.dumps({
        "skill": skill_path.name,
        "valid": not any(f.level == "error" for f in findings),
        "findings": [f.to_dict() for f in findings],
        "summary": {
            "errors": sum(1 for f in findings if f.level == "error"),
            "warnings": sum(1 for f in findings if f.level == "warning"),
            "suggestions": sum(1 for f in findings if f.level == "suggestion"),
        }
    }, indent=2)


# --- CLI ---

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Validate an Agent Skill for spec compliance and best practices"
    )
    parser.add_argument("skill_dir", help="Path to the skill directory")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--strict", action="store_true",
                        help="Exit with error code on warnings (not just errors)")

    args = parser.parse_args()
    skill_path = Path(args.skill_dir).resolve()

    if not skill_path.is_dir():
        print(f"Error: '{args.skill_dir}' is not a directory", file=sys.stderr)
        sys.exit(1)

    findings = validate_skill(skill_path)

    if args.json:
        print(format_json(findings, skill_path))
    else:
        print(format_text(findings, skill_path))

    has_errors = any(f.level == "error" for f in findings)
    has_warnings = any(f.level == "warning" for f in findings)

    if has_errors:
        sys.exit(1)
    elif args.strict and has_warnings:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
