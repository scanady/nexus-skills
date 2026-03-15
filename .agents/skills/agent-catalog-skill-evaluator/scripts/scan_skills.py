#!/usr/bin/env python3
"""
Scan a directory tree for Agent Skills (SKILL.md files) and extract
structural metadata without LLM involvement.

Usage:
    python scan_skills.py <skills-directory> [--output results.json]

Produces a JSON file with mechanical extraction results per skill:
frontmatter, directory structure, script languages, external service
indicators, and SKILL.md body excerpt.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path


def parse_yaml_frontmatter(text: str) -> dict | None:
    """Extract YAML frontmatter from markdown text (between --- delimiters).

    Uses manual parsing to avoid external dependencies on PyYAML.
    Handles simple key-value pairs, nested maps (one level), and multi-line
    quoted strings.
    """
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None

    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break
    if end_idx is None:
        return None

    frontmatter = {}
    current_key = None
    current_nested = None
    yaml_lines = lines[1:end_idx]

    for line in yaml_lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        indent = len(line) - len(line.lstrip())

        # Nested key under a parent (indented with 2+ spaces)
        if indent >= 2 and current_nested is not None:
            match = re.match(r"(\w[\w-]*):\s*(.*)", stripped)
            if match:
                k, v = match.group(1), match.group(2).strip()
                v = v.strip("'\"")
                frontmatter[current_nested][k] = v
                continue

        # Top-level key
        match = re.match(r"^(\w[\w-]*):\s*(.*)", line)
        if match:
            key = match.group(1)
            value = match.group(2).strip()
            current_key = key
            current_nested = None

            if value == "" or value == "|":
                # Could be a nested map or multi-line value
                frontmatter[key] = {}
                current_nested = key
            else:
                value = value.strip("'\"")
                frontmatter[key] = value

    return frontmatter


def detect_script_languages(scripts_dir: Path) -> list[str]:
    """Detect programming languages in a scripts/ directory."""
    ext_map = {
        ".py": "python",
        ".sh": "bash",
        ".bash": "bash",
        ".js": "javascript",
        ".mjs": "javascript",
        ".ts": "typescript",
        ".rb": "ruby",
        ".ps1": "powershell",
        ".pl": "perl",
        ".lua": "lua",
        ".r": "r",
        ".R": "r",
    }
    shebang_map = {
        "python": "python",
        "python3": "python",
        "bash": "bash",
        "sh": "bash",
        "node": "javascript",
        "ruby": "ruby",
        "perl": "perl",
    }

    languages = set()
    if not scripts_dir.is_dir():
        return ["none"]

    for f in scripts_dir.rglob("*"):
        if not f.is_file():
            continue
        # Check extension
        ext = f.suffix.lower()
        if ext in ext_map:
            languages.add(ext_map[ext])

        # Check shebang
        try:
            with open(f, "r", encoding="utf-8", errors="ignore") as fh:
                first_line = fh.readline().strip()
                if first_line.startswith("#!"):
                    for keyword, lang in shebang_map.items():
                        if keyword in first_line:
                            languages.add(lang)
                            break
        except (OSError, UnicodeDecodeError):
            pass

    return sorted(languages) if languages else ["none"]


# Patterns that indicate external service usage
EXTERNAL_URL_RE = re.compile(
    r"https?://(?!agentskills\.io|modelcontextprotocol\.io|example\.com)"
    r"[^\s\)\"'>]+",
    re.IGNORECASE,
)
CREDENTIAL_RE = re.compile(
    r"(API[_-]?KEY|API[_-]?TOKEN|SECRET|CREDENTIALS?|AUTH[_-]?TOKEN"
    r"|PASSWORD|BEARER|oauth|\.env\b)",
    re.IGNORECASE,
)
NETWORK_CALL_RE = re.compile(
    r"(requests\.(get|post|put|delete|patch)|fetch\(|urllib|httpx|aiohttp"
    r"|axios\.|http\.request|curl\s|wget\s|subprocess.*curl)",
    re.IGNORECASE,
)
EXEC_RE = re.compile(
    r"(os\.system|subprocess\.run.*shell\s*=\s*True|exec\(|eval\("
    r"|__import__|child_process\.exec|new\s+Function\()",
    re.IGNORECASE,
)
INSTALL_RE = re.compile(
    r"(pip\s+install|npm\s+install|cargo\s+install|apt-get\s+install"
    r"|brew\s+install)",
    re.IGNORECASE,
)


def detect_external_indicators(skill_dir: Path, skill_text: str) -> dict:
    """Scan skill content and scripts for external service indicators."""
    indicators = {
        "urls": [],
        "credential_refs": False,
        "network_calls": False,
        "exec_patterns": False,
        "install_commands": False,
    }

    # Scan SKILL.md text
    urls = EXTERNAL_URL_RE.findall(skill_text)
    indicators["urls"] = list(set(urls))[:20]  # Cap at 20 unique URLs
    indicators["credential_refs"] = bool(CREDENTIAL_RE.search(skill_text))
    indicators["network_calls"] = bool(NETWORK_CALL_RE.search(skill_text))
    indicators["exec_patterns"] = bool(EXEC_RE.search(skill_text))
    indicators["install_commands"] = bool(INSTALL_RE.search(skill_text))

    # Scan scripts/ if present
    scripts_dir = skill_dir / "scripts"
    if scripts_dir.is_dir():
        for f in scripts_dir.rglob("*"):
            if not f.is_file():
                continue
            try:
                with open(f, "r", encoding="utf-8", errors="ignore") as fh:
                    content = fh.read(50_000)  # Cap at 50KB per file
                script_urls = EXTERNAL_URL_RE.findall(content)
                indicators["urls"].extend(script_urls)
                if CREDENTIAL_RE.search(content):
                    indicators["credential_refs"] = True
                if NETWORK_CALL_RE.search(content):
                    indicators["network_calls"] = True
                if EXEC_RE.search(content):
                    indicators["exec_patterns"] = True
                if INSTALL_RE.search(content):
                    indicators["install_commands"] = True
            except (OSError, UnicodeDecodeError):
                pass

    indicators["urls"] = sorted(set(indicators["urls"]))[:20]
    return indicators


def detect_license(skill_dir: Path, frontmatter: dict | None) -> str:
    """Detect the license for a skill."""
    # 1. Frontmatter
    if frontmatter and "license" in frontmatter:
        val = frontmatter["license"]
        if isinstance(val, str) and val.strip():
            return val.strip()

    # 2. LICENSE files in skill dir
    for name in ("LICENSE.txt", "LICENSE.md", "LICENSE"):
        license_file = skill_dir / name
        if license_file.is_file():
            try:
                text = license_file.read_text(encoding="utf-8", errors="ignore")[
                    :2000
                ]
                if "MIT" in text:
                    return "MIT"
                if "Apache" in text and "2.0" in text:
                    return "Apache-2.0"
                if "GPL" in text:
                    if "3.0" in text:
                        return "GPL-3.0"
                    if "2.0" in text:
                        return "GPL-2.0"
                    return "GPL"
                if "BSD" in text:
                    return "BSD"
                if "ISC" in text:
                    return "ISC"
                return "custom"
            except OSError:
                pass

    return "unspecified"


def count_files(skill_dir: Path) -> int:
    """Count total files in a skill directory."""
    count = 0
    for _ in skill_dir.rglob("*"):
        if _.is_file():
            count += 1
    return count


def estimate_tokens(skill_dir: Path) -> int:
    """Estimate token count from total lines across all text files."""
    total_lines = 0
    text_exts = {
        ".md",
        ".txt",
        ".py",
        ".js",
        ".ts",
        ".sh",
        ".bash",
        ".yaml",
        ".yml",
        ".json",
        ".rb",
        ".lua",
        ".r",
        ".ps1",
        ".pl",
    }
    for f in skill_dir.rglob("*"):
        if f.is_file() and f.suffix.lower() in text_exts:
            try:
                with open(f, "r", encoding="utf-8", errors="ignore") as fh:
                    total_lines += sum(1 for _ in fh)
            except OSError:
                pass
    return int(total_lines * 1.3)


def scan_skill(skill_md_path: Path, base_dir: Path) -> dict:
    """Scan a single SKILL.md and its parent directory."""
    skill_dir = skill_md_path.parent
    rel_path = str(skill_md_path.relative_to(base_dir))

    try:
        text = skill_md_path.read_text(encoding="utf-8", errors="ignore")
    except OSError as e:
        return {
            "path": rel_path,
            "error": f"Could not read: {e}",
        }

    frontmatter = parse_yaml_frontmatter(text)

    # Extract body (after frontmatter)
    body_lines = text.split("\n")
    in_frontmatter = False
    body_start = 0
    for i, line in enumerate(body_lines):
        if line.strip() == "---":
            if not in_frontmatter:
                in_frontmatter = True
            else:
                body_start = i + 1
                break

    body_excerpt = "\n".join(body_lines[body_start : body_start + 200])

    # Structure detection
    has_scripts = (skill_dir / "scripts").is_dir()
    has_references = (skill_dir / "references").is_dir()
    has_agents = (skill_dir / "agents").is_dir()
    has_assets = (skill_dir / "assets").is_dir()
    has_license_file = any(
        (skill_dir / n).is_file() for n in ("LICENSE.txt", "LICENSE.md", "LICENSE")
    )

    # Script languages
    script_languages = (
        detect_script_languages(skill_dir / "scripts") if has_scripts else ["none"]
    )

    # External indicators
    external_indicators = detect_external_indicators(skill_dir, text)

    # License
    license_value = detect_license(skill_dir, frontmatter)

    return {
        "path": rel_path,
        "name": frontmatter.get("name", skill_dir.name) if frontmatter else skill_dir.name,
        "frontmatter": frontmatter,
        "structure": {
            "has_scripts": has_scripts,
            "has_references": has_references,
            "has_agents": has_agents,
            "has_assets": has_assets,
            "has_license_file": has_license_file,
            "file_count": count_files(skill_dir),
            "estimated_tokens": estimate_tokens(skill_dir),
        },
        "script_languages": script_languages,
        "external_indicators": external_indicators,
        "license": license_value,
        "body_excerpt": body_excerpt,
    }


def scan_directory(base_dir: Path) -> list[dict]:
    """Find all SKILL.md files and scan each one."""
    results = []
    skill_files = sorted(base_dir.rglob("SKILL.md"))

    for skill_md in skill_files:
        result = scan_skill(skill_md, base_dir)
        results.append(result)
        # Progress indicator for large collections
        if len(results) % 25 == 0:
            print(f"  Scanned {len(results)} skills...", file=sys.stderr)

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Scan a directory for Agent Skills and extract metadata"
    )
    parser.add_argument("directory", help="Path to the skills directory to scan")
    parser.add_argument(
        "--output",
        "-o",
        default="skill-scan-results.json",
        help="Output JSON file path (default: skill-scan-results.json)",
    )
    args = parser.parse_args()

    base_dir = Path(args.directory).resolve()
    if not base_dir.is_dir():
        print(f"Error: {base_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    print(f"Scanning {base_dir} for SKILL.md files...", file=sys.stderr)
    results = scan_directory(base_dir)
    print(f"Found {len(results)} skills", file=sys.stderr)

    output = {
        "source_directory": str(base_dir),
        "total_skills": len(results),
        "skills": results,
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=False))
    print(f"Results written to {output_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
