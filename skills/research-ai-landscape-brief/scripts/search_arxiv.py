#!/usr/bin/env python3
"""Search arXiv for recent AI research papers. Free, no auth required.

Uses the arXiv Export API (https://export.arxiv.org/api/). Returns papers
from cs.AI, cs.LG, cs.CL, and cs.CV by default, filtered by submission date.

Usage:
    python search_arxiv.py "transformer agent" --days 7 --limit 20
    python search_arxiv.py "LLM reasoning" --days 3 --limit 10
    python search_arxiv.py "" --days 1 --limit 30           # All recent AI papers (last 24h)
    python search_arxiv.py "diffusion" --categories cs.CV,cs.LG --days 7
"""

import argparse
import json
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


API_BASE = "https://export.arxiv.org/api/query"
NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom",
}
DEFAULT_CATEGORIES = ["cs.AI", "cs.LG", "cs.CL", "cs.CV"]


def build_query(query: str, categories: list[str]) -> str:
    cat_filter = " OR ".join(f"cat:{c}" for c in categories)
    if query.strip():
        # Wrap multi-word queries in quotes for phrase matching if needed
        return f"({cat_filter}) AND all:{query}"
    return f"({cat_filter})"


def fetch_papers(
    query: str,
    days: int = 7,
    limit: int = 25,
    categories: list[str] | None = None,
) -> list[dict]:
    if categories is None:
        categories = DEFAULT_CATEGORIES

    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    search_query = build_query(query, categories)

    # Fetch extra to allow for date filtering (arXiv API sorts by submission date
    # but can include slightly older results depending on indexing lag)
    fetch_count = min(limit * 3, 200)

    params = urlencode(
        {
            "search_query": search_query,
            "start": 0,
            "max_results": fetch_count,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }
    )
    url = f"{API_BASE}?{params}"

    req = Request(url, headers={"User-Agent": "ai-landscape-brief/1.0"})

    # arXiv asks for ≥3s between requests; retry once on transient errors
    for attempt in range(2):
        try:
            with urlopen(req, timeout=45) as resp:
                xml_data = resp.read().decode("utf-8")
            break
        except (TimeoutError, OSError) as e:
            if attempt == 0:
                time.sleep(10)
            else:
                raise

    root = ET.fromstring(xml_data)
    papers = []

    for entry in root.findall("atom:entry", NS):
        # Use 'published' (original submission) not 'updated' (revision)
        pub_elem = entry.find("atom:published", NS)
        if pub_elem is None:
            continue
        published_str = pub_elem.text.strip()

        try:
            published = datetime.fromisoformat(published_str.replace("Z", "+00:00"))
        except ValueError:
            continue

        if published < cutoff:
            # arXiv API returns sorted by submission date, so once we're past
            # the cutoff we can stop
            break

        id_elem = entry.find("atom:id", NS)
        if id_elem is None:
            continue
        arxiv_id_url = id_elem.text.strip()
        arxiv_id = arxiv_id_url.split("/abs/")[-1]

        title_elem = entry.find("atom:title", NS)
        title = title_elem.text.strip().replace("\n", " ") if title_elem is not None else ""

        summary_elem = entry.find("atom:summary", NS)
        abstract = ""
        if summary_elem is not None:
            abstract = summary_elem.text.strip().replace("\n", " ")[:600]

        authors = [
            a.find("atom:name", NS).text.strip()
            for a in entry.findall("atom:author", NS)
            if a.find("atom:name", NS) is not None
        ]

        # Primary category is the first term with scheme containing "subjectscheme"
        cats = [c.get("term", "") for c in entry.findall("atom:category", NS)]
        primary_cat = cats[0] if cats else ""

        papers.append(
            {
                "arxiv_id": arxiv_id,
                "title": title,
                "authors": authors[:6],
                "abstract": abstract,
                "primary_category": primary_cat,
                "categories": cats,
                "published": published_str,
                "url": f"https://arxiv.org/abs/{arxiv_id}",
                "source": "arxiv",
            }
        )

        if len(papers) >= limit:
            break

    return papers


def main():
    parser = argparse.ArgumentParser(
        description="Search arXiv for recent AI research papers (no auth required)"
    )
    parser.add_argument(
        "query",
        nargs="?",
        default="",
        help='Search query (optional — omit to get all recent papers from target categories)',
    )
    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Lookback window in days (default: 7; recommend ≤14 for focused queries)",
    )
    parser.add_argument("--limit", type=int, default=25, help="Max results (default: 25)")
    parser.add_argument(
        "--categories",
        default=",".join(DEFAULT_CATEGORIES),
        help="Comma-separated arXiv category filters (default: cs.AI,cs.LG,cs.CL,cs.CV)",
    )
    args = parser.parse_args()

    categories = [c.strip() for c in args.categories.split(",") if c.strip()]

    try:
        papers = fetch_papers(args.query, args.days, args.limit, categories)
        output = {
            "query": args.query,
            "days": args.days,
            "categories": categories,
            "count": len(papers),
            "results": papers,
        }
        json.dump(output, sys.stdout, indent=2)
    except (URLError, TimeoutError, OSError) as e:
        json.dump({"error": str(e), "query": args.query}, sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
