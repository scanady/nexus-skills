#!/usr/bin/env python3
"""
context_stats.py - Quick summary of context repository size, shape, and link density.

Useful for deciding when to shard indexes, split pages, or revise context packs.

Usage:
    python context_stats.py [<context-dir>]
"""

import argparse
import re
import sys
from collections import Counter
from pathlib import Path


LINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
SKIP_TOP_LEVEL_FILES = {"SCHEMA.md", "log.md", "README.md"}
SKIP_TOP_LEVEL_DIRS = {"raw"}


def parse_type(text: str) -> str | None:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None
    for line in match.group(1).split("\n"):
        key_value = re.match(r"^type:\s*(.*)$", line)
        if key_value:
            return key_value.group(1).strip().strip('"').strip("'")
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("context", nargs="?", type=Path, default=Path("context"), help="Context repository directory.")
    args = parser.parse_args()

    if not args.context.exists():
        print(f"Context repository directory not found: {args.context}", file=sys.stderr)
        sys.exit(1)

    total_pages = 0
    total_lines = 0
    total_words = 0
    total_links = 0
    pages_by_type = Counter()
    pages_by_dir = Counter()
    largest = []
    most_linked_in = Counter()
    index_lines = 0
    pack_required_counts = []

    for md_path in args.context.rglob("*.md"):
        rel = md_path.relative_to(args.context)
        if rel.parts[0] in SKIP_TOP_LEVEL_DIRS:
            continue
        try:
            text = md_path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue

        if rel.name == "index.md" and len(rel.parts) == 1:
            index_lines = text.count("\n") + 1
            continue
        if rel.parts[0] in SKIP_TOP_LEVEL_FILES or rel.name.startswith("."):
            continue

        total_pages += 1
        line_count = text.count("\n") + 1
        word_count = len(text.split())
        total_lines += line_count
        total_words += word_count
        body = FRONTMATTER_RE.sub("", text, count=1) if text.startswith("---") else text
        links = LINK_RE.findall(body)
        total_links += len(links)
        for link in links:
            target = link.split("|")[0].strip()
            most_linked_in[target] += 1
        page_type = parse_type(text) or "(none)"
        pages_by_type[page_type] += 1
        pages_by_dir[rel.parts[0] if len(rel.parts) > 1 else "(root)"] += 1
        largest.append((line_count, str(rel)))

        if page_type == "context-pack":
            required_match = re.search(r"^required_pages:\s*\[(.*?)\]", text, re.MULTILINE)
            if required_match:
                values = [item.strip() for item in required_match.group(1).split(",") if item.strip()]
                pack_required_counts.append((len(values), str(rel)))

    largest.sort(reverse=True)

    print("=" * 60)
    print(f"Context Repository Stats: {args.context}")
    print("=" * 60)
    print(f"Pages:         {total_pages}")
    print(f"Total lines:   {total_lines:,}")
    print(f"Total words:   {total_words:,}")
    print(f"Total links:   {total_links:,}")
    if total_pages:
        print(f"Avg page:      {total_lines // total_pages} lines / {total_words // total_pages} words")
        print(f"Link density:  {total_links / total_pages:.1f} links per page")
    print(f"index.md:      {index_lines} lines" + ("  <- shard recommended (>300)" if index_lines > 300 else ""))
    print()

    print("Pages by type:")
    for page_type, count in pages_by_type.most_common():
        print(f"  {page_type:15s} {count}")
    print()

    print("Pages by directory:")
    for directory, count in pages_by_dir.most_common():
        print(f"  {directory:15s} {count}")
    print()

    if largest:
        print("Largest pages:")
        for lines, path in largest[:10]:
            warning = ""
            if lines > 800:
                warning = "  <- OVER HARD CAP"
            elif lines > 400:
                warning = "  <- over soft cap"
            print(f"  {lines:5d}  {path}{warning}")
        print()

    if pack_required_counts:
        print("Largest context packs by required pages:")
        for count, path in sorted(pack_required_counts, reverse=True)[:10]:
            warning = "  <- consider splitting" if count > 12 else ""
            print(f"  {count:5d}  {path}{warning}")
        print()

    if most_linked_in:
        print("Most-linked-to pages:")
        for slug, count in most_linked_in.most_common(10):
            print(f"  {count:4d}  [[{slug}]]")
        print()

    print("Scaling thresholds:")
    if total_pages < 50:
        print("  -> Below first threshold. Flat index is fine.")
    elif total_pages < 150 and index_lines < 300:
        print("  -> Below shard threshold. Continue with single index.md.")
    elif (total_pages >= 150 or index_lines >= 300) and not (args.context / "indexes").exists():
        print("  -> AT SHARD THRESHOLD. Consider sharding index.md into context/indexes/<type>.md.")
    elif total_pages >= 300:
        print("  -> Past 300 pages. Use scripts/context_search.py as a routine fallback.")
    if total_pages >= 500:
        print("  -> Past 500 pages. Run lint and context-pack freshness checks on a cadence.")


if __name__ == "__main__":
    main()