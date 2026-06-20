#!/usr/bin/env python3
"""
context_search.py - BM25 search over context repository pages with frontmatter filters.

Fallback for when index-first navigation does not surface the right pages.
Pure-Python implementation with no third-party dependencies.

Usage:
    python context_search.py "query terms" [options]

Options:
    --context <dir>         Context repository directory (default: ./context)
    --top N                 Return top N results (default: 10)
    --type <type>           Filter by frontmatter type
    --tag <tag>             Filter by tag (repeatable)
    --since YYYY-MM-DD      Only pages updated on or after this date
    --backlinks <slug>      Find pages that link to <slug>; ignores the query
    --top-linked N          Show the N most-linked-to pages; ignores the query
    --cache <path>          Reserved for a future persistent index
"""

import argparse
import json
import math
import re
import sys
from collections import Counter
from datetime import date, datetime
from pathlib import Path


LINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
TOKEN_RE = re.compile(r"[a-z0-9]+")
SKIP_TOP_LEVEL_FILES = {"SCHEMA.md", "index.md", "log.md", "README.md"}
SKIP_TOP_LEVEL_DIRS = {"indexes", "raw"}


def parse_frontmatter(text: str) -> tuple[dict, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
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
    return meta, body


def tokenize(text: str) -> list[str]:
    return TOKEN_RE.findall(text.lower())


def extract_links(body: str) -> list[str]:
    return [match.group(1).strip() for match in LINK_RE.finditer(body)]


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
        except (UnicodeDecodeError, OSError):
            continue
        meta, body = parse_frontmatter(text)
        title = meta.get("title", "")
        task = meta.get("task", "")
        tags = " ".join(meta.get("tags", []) or [])
        pages.append({
            "path": str(md_path),
            "rel_path": str(rel),
            "slug": md_path.stem,
            "meta": meta,
            "body": body,
            "tokens": tokenize(body + " " + title + " " + task + " " + tags),
            "links": extract_links(body),
        })
    return pages


def build_bm25(pages: list[dict]) -> dict:
    doc_count = len(pages)
    df = Counter()
    doc_lens = []
    term_freqs = []
    for page in pages:
        tokens = page["tokens"]
        doc_lens.append(len(tokens))
        tf = Counter(tokens)
        term_freqs.append(tf)
        for term in tf:
            df[term] += 1
    avgdl = sum(doc_lens) / doc_count if doc_count else 0
    return {"N": doc_count, "df": df, "avgdl": avgdl, "doc_lens": doc_lens, "term_freqs": term_freqs}


def bm25_score(query_tokens: list[str], doc_idx: int, index: dict, k1: float = 1.5, b: float = 0.75) -> float:
    score = 0.0
    doc_count = index["N"]
    df = index["df"]
    avgdl = index["avgdl"]
    doc_len = index["doc_lens"][doc_idx]
    tf = index["term_freqs"][doc_idx]
    for term in query_tokens:
        if term not in df:
            continue
        idf = math.log(1 + (doc_count - df[term] + 0.5) / (df[term] + 0.5))
        frequency = tf.get(term, 0)
        if frequency == 0:
            continue
        denom = frequency + k1 * (1 - b + b * (doc_len / avgdl if avgdl else 1))
        score += idf * (frequency * (k1 + 1)) / denom
    return score


def parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return datetime.strptime(value[:10], "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def passes_filters(page: dict, args) -> bool:
    meta = page["meta"]
    if args.type and meta.get("type") != args.type:
        return False
    if args.tag:
        page_tags = set(meta.get("tags", []) or [])
        if not all(tag in page_tags for tag in args.tag):
            return False
    if args.since:
        since = parse_date(args.since)
        updated = parse_date(meta.get("updated"))
        if since and updated and updated < since:
            return False
        if since and not updated:
            return False
    return True


def cmd_search(args, pages: list[dict]) -> None:
    filtered = [page for page in pages if passes_filters(page, args)]
    if not filtered:
        print("No pages matched the filters.", file=sys.stderr)
        return
    index = build_bm25(filtered)
    query_tokens = tokenize(args.query)
    if not query_tokens:
        print("Empty query.", file=sys.stderr)
        return
    scored = [(bm25_score(query_tokens, i, index), i) for i in range(len(filtered))]
    scored.sort(key=lambda item: -item[0])
    top = [(score, filtered[i]) for score, i in scored[:args.top] if score > 0]
    if not top:
        print("No matches.", file=sys.stderr)
        return
    print(f"Top {len(top)} results for: {args.query!r}")
    print()
    for score, page in top:
        title = page["meta"].get("title") or page["slug"]
        page_type = page["meta"].get("type", "?")
        print(f"  [{score:6.2f}] [{page_type:12}] {title}")
        print(f"                {page['rel_path']}")


def cmd_backlinks(args, pages: list[dict]) -> None:
    inbound = [page for page in pages if args.backlinks in page["links"]]
    if not inbound:
        print(f"No pages link to [[{args.backlinks}]].", file=sys.stderr)
        return
    print(f"Pages linking to [[{args.backlinks}]] ({len(inbound)}):")
    for page in inbound:
        title = page["meta"].get("title") or page["slug"]
        print(f"  - {title}  ({page['rel_path']})")


def cmd_top_linked(args, pages: list[dict]) -> None:
    inbound_count = Counter()
    for page in pages:
        for link in page["links"]:
            inbound_count[link] += 1
    top = inbound_count.most_common(args.top_linked)
    if not top:
        print("No links found in the context repository.", file=sys.stderr)
        return
    print(f"Top {len(top)} most-linked-to pages:")
    for slug, count in top:
        match = next((page for page in pages if page["slug"] == slug), None)
        title = (match["meta"].get("title") if match else None) or slug
        marker = "" if match else "  [BROKEN LINK]"
        print(f"  {count:4d}  {title}  ({slug}){marker}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("query", nargs="?", default="", help="Query terms.")
    parser.add_argument("--context", type=Path, default=Path("context"), help="Context repository directory.")
    parser.add_argument("--top", type=int, default=10, help="Top N results.")
    parser.add_argument("--type", help="Filter by frontmatter type.")
    parser.add_argument("--tag", action="append", default=[], help="Filter by tag; repeatable.")
    parser.add_argument("--since", help="Only pages updated on or after YYYY-MM-DD.")
    parser.add_argument("--backlinks", help="Find pages linking to this slug.")
    parser.add_argument("--top-linked", type=int, help="Show the N most-linked-to pages.")
    parser.add_argument("--cache", type=Path, help="Reserved for a future persistent index.")
    args = parser.parse_args()

    if not args.context.exists():
        print(f"Context repository directory not found: {args.context}", file=sys.stderr)
        sys.exit(1)

    pages = collect_pages(args.context)
    if not pages:
        print(f"No context pages found under {args.context}", file=sys.stderr)
        sys.exit(0)

    if args.backlinks:
        cmd_backlinks(args, pages)
    elif args.top_linked:
        cmd_top_linked(args, pages)
    elif args.query:
        cmd_search(args, pages)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()