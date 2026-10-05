#!/usr/bin/env python3
"""Check a sitemap.xml for structural SEO problems.

Usage:
    python3 sitemap_structure.py sitemap.xml
    python3 sitemap_structure.py https://example.com/sitemap.xml --json
    cat sitemap.xml | python3 sitemap_structure.py -
    python3 sitemap_structure.py            # demo sitemap

Reports depth distribution, top sections, URL hygiene problems (query strings,
uppercase, underscores, dates, long URLs, mixed trailing slashes), and same-slug
paths that may duplicate each other. A sitemap alone cannot prove orphan pages:
compare its URL list with a crawl's internal-link list for that. Stdlib only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from urllib.parse import urlparse

MAX_URL_LEN = 75
DEEP_FROM = 4

DEMO = """<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
<url><loc>https://example.com/</loc></url>
<url><loc>https://example.com/pricing</loc></url>
<url><loc>https://example.com/features/</loc></url>
<url><loc>https://example.com/features/email-automation</loc></url>
<url><loc>https://example.com/blog/cold-email-guide</loc></url>
<url><loc>https://example.com/blog/2024/03/email_tips</loc></url>
<url><loc>https://example.com/resources/email-tips</loc></url>
<url><loc>https://example.com/blog/email-tips</loc></url>
<url><loc>https://example.com/resources/guides/email/cold-outreach/advanced/templates</loc></url>
<url><loc>https://example.com/Search?q=cold+email&amp;sort=recent</loc></url>
</urlset>"""


def read_source(src: str | None) -> str:
    if src is None:
        return DEMO
    if src == "-":
        return sys.stdin.read()
    if src.startswith(("http://", "https://")):
        req = urllib.request.Request(src, headers={"User-Agent": "sitemap-structure/1.0"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.read().decode("utf-8", errors="replace")
    with open(src, encoding="utf-8") as f:
        return f.read()


def parse(xml: str) -> tuple[list[str], list[str]]:
    """Return (page URLs, child sitemap URLs)."""
    if re.search(r"<!(DOCTYPE|ENTITY)", xml, re.I):
        sys.exit("[error] sitemap has a DTD or entity declaration; refusing to parse (XXE guard)")
    try:
        root = ET.fromstring(xml)
    except ET.ParseError as e:
        sys.exit(f"[error] invalid XML: {e}")
    locs = lambda tag: [e.findtext("{*}loc", "").strip() for e in root.findall(f".//{{*}}{tag}")]
    return [u for u in locs("url") if u], [u for u in locs("sitemap") if u]


def segments(url: str) -> list[str]:
    return [s for s in urlparse(url).path.split("/") if s]


def analyze(urls: list[str]) -> dict:
    depth = Counter(len(segments(u)) for u in urls)
    sections = Counter((segments(u) or ["(home)"])[0] for u in urls)

    problems: dict[str, list[str]] = defaultdict(list)
    for u in urls:
        p = urlparse(u)
        if p.query:
            problems["query_string"].append(u)
        if p.path != p.path.lower():
            problems["uppercase"].append(u)
        if "_" in p.path:
            problems["underscore"].append(u)
        if re.search(r"/(19|20)\d{2}(/|-)\d{1,2}", p.path):
            problems["date_in_path"].append(u)
        if len(u) > MAX_URL_LEN:
            problems["long_url"].append(u)
        if len(segments(u)) >= DEEP_FROM:
            problems["deep"].append(u)
    paths = [urlparse(u).path for u in urls if len(urlparse(u).path) > 1]
    with_slash = sum(p.endswith("/") for p in paths)
    if 0 < with_slash < len(paths):
        problems["mixed_trailing_slash"] = [f"{with_slash} with slash, {len(paths) - with_slash} without"]

    by_slug: dict[str, list[str]] = defaultdict(list)
    for u in urls:
        if segments(u) and not urlparse(u).query:
            by_slug[segments(u)[-1]].append(u)
    same_slug = {s: v for s, v in by_slug.items() if len({tuple(segments(x)[:-1]) for x in v}) > 1}

    total = len(urls)
    deep_share = round(100 * len(problems["deep"]) / total, 1) if total else 0.0
    return {
        "total_urls": total,
        "depth_distribution": dict(sorted(depth.items())),
        "deep_share_pct": deep_share,
        "depth_rating": "good" if deep_share < 5 else "acceptable" if deep_share < 15 else "poor",
        "top_sections": dict(sections.most_common(10)),
        "problems": dict(problems),
        "same_slug_candidates": same_slug,
    }


def render(r: dict, children: list[str]) -> None:
    print(f"Sitemap structure: {r['total_urls']} URLs")
    for d, n in r["depth_distribution"].items():
        pct = 100 * n / r["total_urls"]
        print(f"  depth {d}: {n:5d} ({pct:4.1f}%) {'#' * round(pct / 2)}")
    print(f"  depth {DEEP_FROM}+ share: {r['deep_share_pct']}% -> {r['depth_rating']}")
    print("Top sections: " + ", ".join(f"/{s} ({n})" for s, n in r["top_sections"].items()))
    advice = {
        "query_string": "keep parameter URLs out of the sitemap; canonicalize or block them",
        "uppercase": "URLs are case-sensitive; lowercase them and 301 the old form",
        "underscore": "use hyphens as word separators",
        "date_in_path": "dates age a URL; drop them unless the date is the content",
        "long_url": f"over {MAX_URL_LEN} chars; shorten",
        "deep": "add shortcut links or flatten the path",
        "mixed_trailing_slash": "pick one form and 301 the other",
    }
    for key, hint in advice.items():
        items = r["problems"].get(key)
        if items:
            print(f"\n{key} ({len(items)}): {hint}")
            for u in items[:5]:
                print(f"  {u}")
            if len(items) > 5:
                print(f"  ... {len(items) - 5} more")
    if r["same_slug_candidates"]:
        print("\nsame slug under different parents (possible duplicates):")
        for slug, us in list(r["same_slug_candidates"].items())[:5]:
            print(f"  {slug}: " + " | ".join(urlparse(u).path for u in us))
    if not r["problems"] and not r["same_slug_candidates"]:
        print("\nNo structural problems found.")
    if children:
        print(f"\nThis is a sitemap index with {len(children)} child sitemaps. Run the tool on each.")


def main() -> None:
    ap = argparse.ArgumentParser(description="Structural SEO check of a sitemap.xml.")
    ap.add_argument("source", nargs="?", help="file path, URL, or - for stdin (default: demo)")
    ap.add_argument("--json", action="store_true", help="JSON output")
    args = ap.parse_args()

    urls, children = parse(read_source(args.source))
    report = analyze(urls)
    if children:
        report["child_sitemaps"] = children
    print(json.dumps(report, indent=2)) if args.json else render(report, children)


if __name__ == "__main__":
    main()
