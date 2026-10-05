#!/usr/bin/env python3
"""Score the on-page SEO of one HTML page from 0 to 100.

Usage:
    python3 seo_page_checker.py --file page.html
    python3 seo_page_checker.py --url https://example.com/page
    python3 seo_page_checker.py --file page.html --domain example.com --json
    python3 seo_page_checker.py            # demo page

Each check returns pass (100), warn (50) or fail (0). The overall score is the
weighted mean. Stdlib only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from html.parser import HTMLParser
from urllib.parse import urlparse

GENERIC_ANCHORS = {"click here", "here", "read more", "learn more", "more", "this", "link"}

WEIGHTS = {
    "title": 20,
    "h1": 15,
    "meta_description": 12,
    "indexability": 10,
    "heading_order": 8,
    "canonical": 8,
    "image_alt": 8,
    "word_count": 8,
    "internal_links": 6,
    "viewport": 5,
    "anchor_text": 4,
    "structured_data": 4,
    "html_lang": 3,
}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.meta: dict[str, str] = {}
        self.canonical = ""
        self.lang = ""
        self.headings: list[tuple[int, str]] = []
        self.images: list[str | None] = []
        self.links: list[tuple[str, str]] = []
        self.jsonld: list[str] = []
        self.words: list[str] = []
        self._tag_stack: list[str] = []
        self._heading: tuple[int, list[str]] | None = None
        self._link: tuple[str, list[str]] | None = None
        self._script_type = ""
        self._script_buf: list[str] = []

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        self._tag_stack.append(tag)
        if tag == "html":
            self.lang = a.get("lang", "")
        elif tag == "meta" and a.get("name"):
            self.meta[a["name"].lower()] = a.get("content", "")
        elif tag == "link" and "canonical" in a.get("rel", "").lower().split():
            self.canonical = a.get("href", "")
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._heading = (int(tag[1]), [])
        elif tag == "img":
            self.images.append(a.get("alt") if "alt" in a else None)
        elif tag == "a" and "href" in a:
            self._link = (a["href"], [])
        elif tag == "script":
            self._script_type = a.get("type", "").lower()
            self._script_buf = []

    def handle_endtag(self, tag):
        if tag in self._tag_stack:
            while self._tag_stack and self._tag_stack.pop() != tag:
                pass
        if self._heading and tag == f"h{self._heading[0]}":
            self.headings.append((self._heading[0], " ".join(self._heading[1]).strip()))
            self._heading = None
        elif tag == "a" and self._link:
            self.links.append((self._link[0], " ".join(self._link[1]).strip()))
            self._link = None
        elif tag == "script" and self._script_type == "application/ld+json":
            self.jsonld.append("".join(self._script_buf))
            self._script_type = ""

    def handle_data(self, data):
        if "title" in self._tag_stack and "head" in self._tag_stack:
            self.title += data
        if self._heading:
            self._heading[1].append(data.strip())
        if self._link:
            self._link[1].append(data.strip())
        if "script" in self._tag_stack:
            self._script_buf.append(data)
        elif "style" not in self._tag_stack and "body" in self._tag_stack:
            self.words.extend(re.findall(r"\w+", data))


def result(status: str, note: str, **extra) -> dict:
    return {"status": status, "score": {"pass": 100, "warn": 50, "fail": 0}[status], "note": note, **extra}


def band(value: int, good: tuple[int, int], ok: tuple[int, int]) -> str:
    if good[0] <= value <= good[1]:
        return "pass"
    if ok[0] <= value <= ok[1]:
        return "warn"
    return "fail"


def is_internal(href: str, domain: str) -> bool:
    if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
        return False
    host = urlparse(href).netloc.lower().removeprefix("www.")
    return not host or (bool(domain) and host == domain)


def analyze(html: str, domain: str = "") -> dict:
    p = PageParser()
    p.feed(html)
    domain = domain.lower().removeprefix("www.")
    checks: dict[str, dict] = {}

    title = p.title.strip()
    n = len(title)
    checks["title"] = result(
        band(n, (30, 60), (20, 70)) if n else "fail",
        f"{n} chars (target 30-60)" if n else "missing <title>",
        value=title,
    )

    desc = p.meta.get("description", "").strip()
    n = len(desc)
    checks["meta_description"] = result(
        band(n, (70, 160), (50, 200)) if n else "fail",
        f"{n} chars (target 70-160)" if n else "missing meta description",
    )

    h1s = [t for lvl, t in p.headings if lvl == 1]
    checks["h1"] = result(
        "pass" if len(h1s) == 1 else ("warn" if h1s else "fail"),
        "no H1" if not h1s else (f"{len(h1s)} H1s" if len(h1s) > 1 else "one H1"),
        values=h1s,
    )

    skips, prev = [], 0
    for lvl, _ in p.headings:
        if prev and lvl > prev + 1:
            skips.append(f"H{prev} -> H{lvl}")
        prev = lvl
    checks["heading_order"] = result(
        "pass" if not skips else ("warn" if len(skips) <= 2 else "fail"),
        "no skipped levels" if not skips else "skips: " + ", ".join(skips),
    )

    robots = p.meta.get("robots", "").lower()
    checks["indexability"] = result(
        "fail" if "noindex" in robots else "pass",
        "meta robots has noindex" if "noindex" in robots else "no noindex directive",
    )
    checks["canonical"] = result(
        "pass" if p.canonical else "warn",
        f"canonical -> {p.canonical}" if p.canonical else "no canonical tag",
    )

    missing = sum(1 for alt in p.images if alt is None)
    checks["image_alt"] = result(
        "pass" if missing == 0 else ("warn" if missing <= max(1, len(p.images) // 5) else "fail"),
        f"{len(p.images) - missing}/{len(p.images)} images have an alt attribute"
        if p.images else "no images",
    )

    wc = len(p.words)
    checks["word_count"] = result(
        "pass" if wc >= 300 else ("warn" if wc >= 150 else "fail"),
        f"{wc} words (thin-content signal below 300; judge against search intent)",
    )

    internal = [(h, t) for h, t in p.links if is_internal(h, domain)]
    checks["internal_links"] = result(
        "pass" if len(internal) >= 3 else ("warn" if internal else "fail"),
        f"{len(internal)} internal links of {len(p.links)}"
        + ("" if domain else " (no --domain: only relative links count as internal)"),
    )
    generic = [t for _, t in internal if t.lower() in GENERIC_ANCHORS]
    share = len(generic) / len(internal) if internal else 0
    checks["anchor_text"] = result(
        "pass" if share <= 0.10 else ("warn" if share <= 0.25 else "fail"),
        f"{len(generic)} generic anchors among {len(internal)} internal links",
    )

    checks["viewport"] = result(
        "pass" if "viewport" in p.meta else "fail",
        "viewport meta present" if "viewport" in p.meta else "missing viewport meta",
    )
    checks["html_lang"] = result(
        "pass" if p.lang else "warn",
        f"lang={p.lang}" if p.lang else "missing lang on <html>",
    )

    types = []
    for block in p.jsonld:
        try:
            data = json.loads(block)
        except json.JSONDecodeError:
            checks.setdefault("structured_data", result("fail", "invalid JSON-LD block"))
            continue
        for item in data if isinstance(data, list) else [data]:
            if isinstance(item, dict):
                t = item.get("@type")
                types.extend(t if isinstance(t, list) else [t or "?"])
    if "structured_data" not in checks:
        checks["structured_data"] = result(
            "pass" if types else "warn",
            "JSON-LD types: " + ", ".join(map(str, types)) if types else "no JSON-LD found",
        )

    total = sum(WEIGHTS.values())
    overall = round(sum(c["score"] * WEIGHTS[k] for k, c in checks.items()) / total)
    return {"overall_score": overall, "grade": grade(overall), "checks": checks}


def grade(score: float) -> str:
    return "A" if score >= 90 else "B" if score >= 75 else "C" if score >= 60 else "D" if score >= 40 else "F"


DEMO_HTML = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Cold Email Templates That Get Replies | Example</title>
<meta name="description" content="Copy 12 cold email templates tested on 4,000 sends, with subject lines, follow-up timing, and notes on when each template fails.">
<link rel="canonical" href="https://example.com/cold-email-templates">
<script type="application/ld+json">{"@context":"https://schema.org","@type":"Article","headline":"Cold Email Templates"}</script>
</head><body><h1>Cold Email Templates That Get Replies</h1>
<p>Short intro paragraph.</p><h3>Skipped level</h3>
<img src="a.png" alt="Reply rate by template"><img src="b.png">
<a href="/pricing">Pricing</a><a href="/blog/follow-ups">Follow-up guide</a><a href="/guide">click here</a>
<a href="https://other.com">Other</a></body></html>"""


def main() -> None:
    ap = argparse.ArgumentParser(description="Score one page's on-page SEO (0-100).")
    ap.add_argument("--file", help="local HTML file")
    ap.add_argument("--url", help="URL to fetch")
    ap.add_argument("--domain", default="", help="site domain, used to tell internal links from external")
    ap.add_argument("--json", action="store_true", help="JSON output")
    args = ap.parse_args()

    if args.file:
        html = open(args.file, encoding="utf-8", errors="replace").read()
    elif args.url:
        req = urllib.request.Request(args.url, headers={"User-Agent": "seo-page-checker/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode("utf-8", errors="replace")
        args.domain = args.domain or urlparse(args.url).netloc
    else:
        html = DEMO_HTML
        args.domain = args.domain or "example.com"
        if not args.json:
            print("No input: running on the demo page.\n", file=sys.stderr)

    report = analyze(html, args.domain)
    if args.json:
        print(json.dumps(report, indent=2))
        return
    print(f"On-page score: {report['overall_score']}/100 (grade {report['grade']})")
    for name, c in report["checks"].items():
        print(f"  [{c['status'].upper():4}] {name:<17} {c['note']}")


if __name__ == "__main__":
    main()
