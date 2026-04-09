# /// script
# requires-python = ">=3.9"
# ///
"""Programmatic assertion verification for eval outputs.

Checks assertions that can be verified mechanically — file existence,
format validity, string presence, counts — without LLM judgment.

Usage:
    python3 scripts/verify.py --assertion "<text>" --output-dir <dir>
    python3 scripts/verify.py --grading <grading.json> --output-dir <dir>

Options:
    --assertion TEXT     A single assertion to check against the outputs
    --grading FILE      Path to a grading.json to re-verify programmatic assertions
    --output-dir DIR    Path to the run's outputs directory
    --json              Output results as JSON instead of human-readable text

Examples:
    python3 scripts/verify.py --assertion "The output includes a file named report.json" --output-dir outputs/
    python3 scripts/verify.py --assertion "The output is valid JSON" --output-dir outputs/
    python3 scripts/verify.py --assertion "At least 3 sections" --output-dir outputs/
"""

import argparse
import csv
import io
import json
import re
import sys
from pathlib import Path


def check_file_exists(output_dir: Path, assertion: str) -> dict | None:
    """Check assertions about file existence."""
    patterns = [
        r"includes?\s+(?:a\s+)?file\s+(?:named|called)\s+['\"]?(\S+?)['\"]?\s*$",
        r"output\s+(?:contains?|has)\s+['\"]?(\S+?)['\"]?\s*$",
        r"produces?\s+['\"]?(\S+?)['\"]?\s*$",
        r"(?:a|an)\s+(\S+)\s+file\s+(?:is|was)\s+(?:created|generated|produced)",
    ]
    for pattern in patterns:
        match = re.search(pattern, assertion, re.IGNORECASE)
        if match:
            filename = match.group(1).rstrip(".,;")
            found = list(output_dir.rglob(filename))
            if found:
                return {
                    "text": assertion,
                    "passed": True,
                    "evidence": f"Found {found[0].relative_to(output_dir)} ({found[0].stat().st_size} bytes)",
                    "check_type": "file_exists",
                }
            return {
                "text": assertion,
                "passed": False,
                "evidence": f"File '{filename}' not found in {output_dir}. Files present: {[f.name for f in output_dir.rglob('*') if f.is_file()]}",
                "check_type": "file_exists",
            }
    return None


def check_valid_format(output_dir: Path, assertion: str) -> dict | None:
    """Check assertions about output format validity (JSON, YAML, CSV)."""
    format_match = re.search(
        r"(?:valid|well[- ]formed)\s+(json|yaml|csv)", assertion, re.IGNORECASE
    )
    if not format_match:
        return None

    fmt = format_match.group(1).lower()
    files = list(output_dir.rglob("*"))

    # Try to find a file matching the format
    target_files = [f for f in files if f.is_file() and f.suffix == f".{fmt}"]
    if not target_files:
        # Check response.md for inline content
        response = output_dir / "response.md"
        if response.exists():
            target_files = [response]
        else:
            return {
                "text": assertion,
                "passed": False,
                "evidence": f"No .{fmt} files found and no response.md present",
                "check_type": "format_validity",
            }

    for target in target_files:
        content = target.read_text()
        if fmt == "json":
            # Extract JSON from markdown code blocks if needed
            json_match = re.search(r"```(?:json)?\s*\n(.*?)\n```", content, re.DOTALL)
            to_parse = json_match.group(1) if json_match else content
            try:
                json.loads(to_parse)
                return {
                    "text": assertion,
                    "passed": True,
                    "evidence": f"Valid JSON in {target.name}",
                    "check_type": "format_validity",
                }
            except json.JSONDecodeError as e:
                return {
                    "text": assertion,
                    "passed": False,
                    "evidence": f"Invalid JSON in {target.name}: {e}",
                    "check_type": "format_validity",
                }
        elif fmt == "csv":
            try:
                reader = csv.reader(io.StringIO(content))
                rows = list(reader)
                if len(rows) > 0:
                    return {
                        "text": assertion,
                        "passed": True,
                        "evidence": f"Valid CSV in {target.name} with {len(rows)} rows",
                        "check_type": "format_validity",
                    }
            except csv.Error as e:
                return {
                    "text": assertion,
                    "passed": False,
                    "evidence": f"Invalid CSV in {target.name}: {e}",
                    "check_type": "format_validity",
                }
    return None


def check_count(output_dir: Path, assertion: str) -> dict | None:
    """Check assertions about minimum counts."""
    count_match = re.search(
        r"(?:at\s+least|minimum\s+(?:of\s+)?|more\s+than|>=?\s*)\s*(\d+)\s+(\w+)",
        assertion,
        re.IGNORECASE,
    )
    if not count_match:
        return None

    threshold = int(count_match.group(1))
    item_type = count_match.group(2).lower()

    response = output_dir / "response.md"
    if not response.exists():
        return {
            "text": assertion,
            "passed": False,
            "evidence": "No response.md found to count items in",
            "check_type": "count",
        }

    content = response.read_text()

    # Count based on item type
    count = 0
    if item_type in ("section", "sections", "heading", "headings"):
        count = len(re.findall(r"^#{1,6}\s+", content, re.MULTILINE))
    elif item_type in ("recommendation", "recommendations"):
        count = len(re.findall(r"^[\-\*]\s+|^\d+\.\s+", content, re.MULTILINE))
    elif item_type in ("item", "items", "bullet", "bullets", "point", "points"):
        count = len(re.findall(r"^[\-\*]\s+|^\d+\.\s+", content, re.MULTILINE))
    elif item_type in ("line", "lines"):
        count = len(content.strip().splitlines())
    elif item_type in ("file", "files"):
        count = len([f for f in output_dir.rglob("*") if f.is_file()])
    elif item_type in ("row", "rows"):
        count = len(content.strip().splitlines())
    else:
        return None

    passed = count >= threshold
    return {
        "text": assertion,
        "passed": passed,
        "evidence": f"Found {count} {item_type} (threshold: {threshold})",
        "check_type": "count",
    }


def check_string_presence(output_dir: Path, assertion: str) -> dict | None:
    """Check assertions about string/phrase presence."""
    presence_match = re.search(
        r"(?:contains?|includes?|mentions?|has)\s+(?:the\s+(?:word|phrase|term|string)\s+)['\"](.+?)['\"]",
        assertion,
        re.IGNORECASE,
    )
    if not presence_match:
        return None

    search_term = presence_match.group(1)
    response = output_dir / "response.md"
    if not response.exists():
        return {
            "text": assertion,
            "passed": False,
            "evidence": "No response.md found",
            "check_type": "string_presence",
        }

    content = response.read_text()
    if search_term.lower() in content.lower():
        # Find the line containing the match
        for i, line in enumerate(content.splitlines(), 1):
            if search_term.lower() in line.lower():
                return {
                    "text": assertion,
                    "passed": True,
                    "evidence": f"Found '{search_term}' at line {i}: {line.strip()[:100]}",
                    "check_type": "string_presence",
                }
    return {
        "text": assertion,
        "passed": False,
        "evidence": f"'{search_term}' not found in response",
        "check_type": "string_presence",
    }


CHECKERS = [check_file_exists, check_valid_format, check_count, check_string_presence]


def verify_assertion(output_dir: Path, assertion: str) -> dict:
    """Run all checkers against an assertion. Returns result or 'needs LLM' marker."""
    for checker in CHECKERS:
        result = checker(output_dir, assertion)
        if result is not None:
            return result

    return {
        "text": assertion,
        "passed": None,
        "evidence": "Cannot verify programmatically — requires LLM judgment",
        "check_type": "needs_llm",
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Programmatic assertion verification for eval outputs."
    )
    parser.add_argument("--assertion", help="A single assertion to check")
    parser.add_argument(
        "--grading", help="Path to grading.json to re-verify programmatic assertions"
    )
    parser.add_argument(
        "--output-dir", required=True, help="Path to the run's outputs directory"
    )
    parser.add_argument(
        "--json", action="store_true", help="Output as JSON"
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    if not output_dir.is_dir():
        print(f"Error: '{output_dir}' is not a directory.", file=sys.stderr)
        sys.exit(1)

    results: list[dict] = []

    if args.assertion:
        results.append(verify_assertion(output_dir, args.assertion))
    elif args.grading:
        grading_path = Path(args.grading)
        if not grading_path.exists():
            print(f"Error: '{grading_path}' not found.", file=sys.stderr)
            sys.exit(1)
        with open(grading_path) as f:
            grading = json.load(f)
        for ar in grading.get("assertion_results", []):
            results.append(verify_assertion(output_dir, ar["text"]))
    else:
        print("Error: Provide --assertion or --grading.", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for r in results:
            status = "PASS" if r["passed"] else ("FAIL" if r["passed"] is False else "SKIP")
            print(f"[{status}] {r['text']}")
            print(f"       {r['evidence']}")
            print()


if __name__ == "__main__":
    main()
