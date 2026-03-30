#!/usr/bin/env python3
"""Search Hacker News via the Algolia API. Free, no auth required.

Usage:
    python search_hackernews.py "AI language model" --days 30 --limit 25
"""

import argparse
import json
import sys
import time
from datetime import datetime, timedelta, timezone
from urllib.request import urlopen, Request
from urllib.parse import urlencode
from urllib.error import URLError


API_BASE = "https://hn.algolia.com/api/v1"


def search_stories(query: str, days: int = 30, limit: int = 25) -> list[dict]:
    cutoff = int((datetime.now(timezone.utc) - timedelta(days=days)).timestamp())
    params = urlencode({
        "query": query,
        "tags": "story",
        "numericFilters": f"created_at_i>{cutoff}",
        "hitsPerPage": min(limit, 50),
    })
    url = f"{API_BASE}/search?{params}"
    req = Request(url, headers={"User-Agent": "ai-landscape-brief/1.0"})
    with urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode())

    results = []
    for hit in data.get("hits", []):
        results.append({
            "title": hit.get("title", ""),
            "url": hit.get("url", ""),
            "hn_url": f"https://news.ycombinator.com/item?id={hit.get('objectID', '')}",
            "author": hit.get("author", ""),
            "points": hit.get("points", 0),
            "comments": hit.get("num_comments", 0),
            "created_at": hit.get("created_at", ""),
            "source": "hackernews",
        })
    return results


def main():
    parser = argparse.ArgumentParser(description="Search Hacker News (Algolia API)")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--days", type=int, default=30, help="Lookback window in days (default: 30)")
    parser.add_argument("--limit", type=int, default=25, help="Max results (default: 25, max: 50)")
    args = parser.parse_args()

    try:
        results = search_stories(args.query, args.days, args.limit)
        json.dump({"query": args.query, "days": args.days, "count": len(results), "results": results}, sys.stdout, indent=2)
    except URLError as e:
        json.dump({"error": str(e), "query": args.query}, sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
