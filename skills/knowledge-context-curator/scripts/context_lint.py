#!/usr/bin/env python3
"""
context_lint.py - Structural health check for a context repository.

Reports orphan pages, broken links, oversized pages, frontmatter issues, stale
pages, duplicate slugs, context-pack issues, and optional candidate pages.

Conservative by design: reports findings, never edits.

Usage:
    python context_lint.py [<context-dir>] [options]
"""

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path


LINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
CAPITALIZED_PHRASE_RE = re.compile(r"\b([A-Z][a-zA-Z0-9]+(?:\s+[A-Z][a-zA-Z0-9]+){0,3})\b")
SKIP_TOP_LEVEL_FILES = {"SCHEMA.md", "index.md", "log.md", "README.md"}
SKIP_TOP_LEVEL_DIRS = {"indexes", "raw"}


def parse_frontmatter(text: str) -> tuple[dict, str, bool]:
    if not text.startswith("---"):
        return {}, text, False
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text, True
    fm_text = match.group(1)
    body = text[match.end():]
    meta: dict = {}
    current_key = None
    for line in fm_text.split("\n"):
        if not line.strip():
            continue
        key_value = re.match(r"^([a-zA-Z_]+):\s*(.*)$", line)
        if key_value:
            key, value = key_value.group(1), key_value.group(2).strip()
            if value.startswith("[") and value.endswith("]"):
                items = [item.strip().strip('"').strip("'") for item in value[1:-1].split(",") if item.strip()]
                meta[key] = items
            elif value:
                meta[key] = value.strip('"').strip("'")
            else:
                meta[key] = []
                current_key = key
        elif line.startswith("  - ") and current_key:
            meta[current_key].append(line[4:].strip().strip('"').strip("'"))
    return meta, body, False


def collect_pages(context_root: Path) -> list[dict]:
    pages = []
    for md_path in context_root.rglob("*.md"):
        rel = md_path.relative_to(context_root)
        if rel.parts[0] in SKIP_TOP_LEVEL_FILES or rel.parts[0] in SKIP_TOP_LEVEL_DIRS:
            continue
        if rel.name.startswith("."):
            continue
        try:
            text = md_path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError) as error:
            pages.append({"path": str(md_path), "rel_path": str(rel), "slug": md_path.stem, "read_error": str(error)})
            continue
        meta, body, malformed = parse_frontmatter(text)
        links = [match.group(1).strip() for match in LINK_RE.finditer(body)]
        pages.append({
            "path": str(md_path),
            "rel_path": str(rel),
            "slug": md_path.stem,
            "meta": meta,
            "body": body,
            "line_count": text.count("\n") + 1,
            "links": links,
            "malformed_fm": malformed,
        })
    return pages


def parse_date(value):
    if not value or not isinstance(value, str):
        return None
    try:
        return datetime.strptime(value[:10], "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def required_fields_for(page: dict, base_required: list[str]) -> list[str]:
    page_type = page.get("meta", {}).get("type")
    required = list(base_required)
    if page_type == "source":
        required += ["raw", "ingested"]
    elif page_type == "context-pack":
        required += ["task", "required_pages", "optional_pages", "exclusions", "freshness"]
    elif page_type:
        required += ["sources"]
    return required


def lint(pages: list[dict], soft_cap: int, hard_cap: int, required_fm: list[str], suggest_pages: bool, suggest_min: int) -> dict:
    findings = {
        "orphans": [],
        "broken_links": [],
        "oversized_hard": [],
        "oversized_soft": [],
        "missing_frontmatter": [],
        "malformed_frontmatter": [],
        "duplicate_slugs": [],
        "stale_pages": [],
        "read_errors": [],
        "pack_issues": [],
        "suggested_pages": [],
        "summary": {},
    }

    for page in pages:
        if "read_error" in page:
            findings["read_errors"].append({"path": page["rel_path"], "error": page["read_error"]})

    pages = [page for page in pages if "read_error" not in page]
    slug_to_pages = defaultdict(list)
    for page in pages:
        slug_to_pages[page["slug"]].append(page["rel_path"])
    for slug, paths in slug_to_pages.items():
        if len(paths) > 1:
            findings["duplicate_slugs"].append({"slug": slug, "paths": paths})

    inbound = defaultdict(set)
    all_slugs = set(slug_to_pages.keys())
    for page in pages:
        for link in page["links"]:
            inbound[link].add(page["slug"])

    for page in pages:
        if not inbound.get(page["slug"]):
            findings["orphans"].append({"slug": page["slug"], "path": page["rel_path"]})

        for link in page["links"]:
            if link not in all_slugs:
                findings["broken_links"].append({"from": page["slug"], "from_path": page["rel_path"], "to": link})

        if page["line_count"] > hard_cap:
            findings["oversized_hard"].append({"path": page["rel_path"], "lines": page["line_count"]})
        elif page["line_count"] > soft_cap:
            findings["oversized_soft"].append({"path": page["rel_path"], "lines": page["line_count"]})

        if page["malformed_fm"]:
            findings["malformed_frontmatter"].append({"path": page["rel_path"]})
        else:
            missing = [field for field in required_fields_for(page, required_fm) if field not in page["meta"] or page["meta"].get(field) in ("", None)]
            if missing:
                findings["missing_frontmatter"].append({"path": page["rel_path"], "missing": missing})

        updated = parse_date(page["meta"].get("updated"))
        if updated:
            age_days = (date.today() - updated).days
            if age_days > 90 and len(inbound.get(page["slug"], [])) >= 3:
                findings["stale_pages"].append({
                    "path": page["rel_path"],
                    "updated": page["meta"].get("updated"),
                    "age_days": age_days,
                    "inbound_count": len(inbound.get(page["slug"], [])),
                })

        if page["meta"].get("type") == "context-pack":
            required_pages = page["meta"].get("required_pages", []) or []
            optional_pages = page["meta"].get("optional_pages", []) or []
            if len(required_pages) > 12:
                findings["pack_issues"].append({"path": page["rel_path"], "issue": "required_pages has more than 12 entries"})
            for field, values in [("required_pages", required_pages), ("optional_pages", optional_pages)]:
                for value in values:
                    slug = Path(value).stem
                    if slug and slug not in all_slugs:
                        findings["pack_issues"].append({"path": page["rel_path"], "issue": f"{field} references missing page: {value}"})

    if suggest_pages:
        phrase_pages = defaultdict(set)
        for page in pages:
            seen = set()
            for match in CAPITALIZED_PHRASE_RE.finditer(page["body"]):
                seen.add(match.group(1).strip())
            for phrase in seen:
                phrase_pages[phrase].add(page["slug"])

        existing_titles = {page["meta"].get("title", "").lower() for page in pages}
        existing_slugs = {slug.lower().replace("-", " ") for slug in all_slugs}
        candidates = []
        for phrase, page_set in phrase_pages.items():
            if len(page_set) < suggest_min:
                continue
            if phrase.lower() in existing_titles or phrase.lower() in existing_slugs:
                continue
            if phrase.split()[0] in {"Section", "Sources", "Tags", "Type", "Title", "Context"}:
                continue
            candidates.append({"phrase": phrase, "page_count": len(page_set), "pages": sorted(page_set)[:5]})
        candidates.sort(key=lambda item: -item["page_count"])
        findings["suggested_pages"] = candidates[:30]

    findings["summary"] = {key: len(value) for key, value in findings.items() if key != "summary" and isinstance(value, list)}
    findings["summary"]["total_pages"] = len(pages)
    return findings


def render_text(findings: dict) -> str:
    out = []
    summary = findings["summary"]
    out.append("=" * 60)
    out.append("Context Repository Lint Report")
    out.append("=" * 60)
    out.append(f"Total pages scanned: {summary['total_pages']}")
    out.append("")

    sections = [
        ("orphans", "Orphan pages", lambda item: f"  - {item['slug']}  ({item['path']})"),
        ("broken_links", "Broken links", lambda item: f"  - [[{item['to']}]] referenced from {item['from_path']}"),
        ("oversized_hard", "Oversize over hard cap", lambda item: f"  - {item['path']}  ({item['lines']} lines)"),
        ("oversized_soft", "Oversize over soft cap", lambda item: f"  - {item['path']}  ({item['lines']} lines)"),
        ("missing_frontmatter", "Missing frontmatter fields", lambda item: f"  - {item['path']}  missing: {', '.join(item['missing'])}"),
        ("malformed_frontmatter", "Malformed frontmatter", lambda item: f"  - {item['path']}"),
        ("duplicate_slugs", "Duplicate slugs", lambda item: f"  - {item['slug']}: {', '.join(item['paths'])}"),
        ("stale_pages", "Stale well-linked pages", lambda item: f"  - {item['path']}  (updated {item['updated']}, {item['age_days']}d ago, {item['inbound_count']} inbound)"),
        ("pack_issues", "Context-pack issues", lambda item: f"  - {item['path']}: {item['issue']}"),
        ("read_errors", "Read errors", lambda item: f"  - {item['path']}: {item['error']}"),
    ]

    for key, label, formatter in sections:
        items = findings[key]
        if not items:
            continue
        out.append(f"{label} ({len(items)}):")
        for item in items[:50]:
            out.append(formatter(item))
        if len(items) > 50:
            out.append(f"  ... and {len(items) - 50} more")
        out.append("")

    if findings["suggested_pages"]:
        out.append(f"Suggested page candidates ({len(findings['suggested_pages'])}):")
        for item in findings["suggested_pages"]:
            out.append(f"  - \"{item['phrase']}\"  ({item['page_count']} pages)")
        out.append("")

    if all(value == 0 for key, value in summary.items() if key != "total_pages"):
        out.append("No issues found. Context repository is healthy.")

    return "\n".join(out)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("context", nargs="?", type=Path, default=Path("context"), help="Context repository directory.")
    parser.add_argument("--soft-cap", type=int, default=400, help="Page-size soft cap in lines.")
    parser.add_argument("--hard-cap", type=int, default=800, help="Page-size hard cap in lines.")
    parser.add_argument("--required-fm", default="type,title,tags,created,updated", help="Required frontmatter fields, comma-separated.")
    parser.add_argument("--suggest-pages", action="store_true", help="Surface candidate recurring terms without pages.")
    parser.add_argument("--suggest-min", type=int, default=5, help="Minimum page count for suggestions.")
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    args = parser.parse_args()

    if not args.context.exists():
        print(f"Context repository directory not found: {args.context}", file=sys.stderr)
        sys.exit(1)

    pages = collect_pages(args.context)
    required_fm = [field.strip() for field in args.required_fm.split(",") if field.strip()]
    findings = lint(pages, args.soft_cap, args.hard_cap, required_fm, args.suggest_pages, args.suggest_min)

    if args.json:
        print(json.dumps(findings, indent=2, default=str))
    else:
        print(render_text(findings))


if __name__ == "__main__":
    main()