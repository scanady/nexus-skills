#!/usr/bin/env python3
"""Search GitHub for trending AI repositories via the REST API. Free, no auth required.
Optional: set GITHUB_TOKEN env var for higher rate limits (60/hr -> 5000/hr).

Usage:
    python search_github.py "AI agent framework" --days 30 --limit 25
    python search_github.py "LLM" --days 7 --min-stars 100
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from urllib.request import urlopen, Request
from urllib.parse import urlencode
from urllib.error import URLError


API_BASE = "https://api.github.com"


def search_repos(query: str, days: int = 30, limit: int = 25, min_stars: int = 50) -> list[dict]:
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")
    q = f"{query} created:>{cutoff} stars:>={min_stars}"

    params = urlencode({
        "q": q,
        "sort": "stars",
        "order": "desc",
        "per_page": min(limit, 100),
    })
    url = f"{API_BASE}/search/repositories?{params}"

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "ai-landscape-brief/1.0",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = Request(url, headers=headers)
    with urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode())

    results = []
    for repo in data.get("items", []):
        stars = repo.get("stargazers_count", 0)
        created_at = repo.get("created_at", "")
        try:
            created = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            days_old = max(1, (datetime.now(timezone.utc) - created).days)
            stars_per_day = round(stars / days_old, 1)
        except (ValueError, TypeError):
            stars_per_day = None
        results.append({
            "name": repo.get("full_name", ""),
            "description": (repo.get("description") or "")[:300],
            "url": repo.get("html_url", ""),
            "stars": stars,
            "stars_per_day": stars_per_day,
            "forks": repo.get("forks_count", 0),
            "language": repo.get("language", ""),
            "topics": repo.get("topics", []),
            "created_at": created_at,
            "updated_at": repo.get("updated_at", ""),
            "open_issues": repo.get("open_issues_count", 0),
            "license": (repo.get("license") or {}).get("spdx_id", ""),
            "source": "github",
        })
    return results


def search_trending_topics(days: int = 30, limit: int = 25, min_stars: int = 100) -> list[dict]:
    """Search for AI repos gaining stars rapidly, regardless of creation date."""
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")
    q = f"topic:artificial-intelligence OR topic:llm OR topic:machine-learning OR topic:deep-learning pushed:>{cutoff} stars:>={min_stars}"

    params = urlencode({
        "q": q,
        "sort": "updated",
        "order": "desc",
        "per_page": min(limit, 100),
    })
    url = f"{API_BASE}/search/repositories?{params}"

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "ai-landscape-brief/1.0",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = Request(url, headers=headers)
    with urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode())

    results = []
    for repo in data.get("items", []):
        stars = repo.get("stargazers_count", 0)
        created_at = repo.get("created_at", "")
        try:
            created = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            days_old = max(1, (datetime.now(timezone.utc) - created).days)
            stars_per_day = round(stars / days_old, 1)
        except (ValueError, TypeError):
            stars_per_day = None
        results.append({
            "name": repo.get("full_name", ""),
            "description": (repo.get("description") or "")[:300],
            "url": repo.get("html_url", ""),
            "stars": stars,
            "stars_per_day": stars_per_day,
            "forks": repo.get("forks_count", 0),
            "language": repo.get("language", ""),
            "topics": repo.get("topics", []),
            "created_at": created_at,
            "updated_at": repo.get("updated_at", ""),
            "source": "github",
        })
    return results


def main():
    parser = argparse.ArgumentParser(description="Search GitHub AI repositories (REST API)")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--days", type=int, default=30, help="Lookback window in days (default: 30)")
    parser.add_argument("--limit", type=int, default=25, help="Max results (default: 25)")
    parser.add_argument("--min-stars", type=int, default=50, help="Minimum star count (default: 50)")
    parser.add_argument("--trending", action="store_true", help="Also search trending AI topic repos")
    args = parser.parse_args()

    try:
        results = search_repos(args.query, args.days, args.limit, args.min_stars)
        output = {
            "query": args.query,
            "days": args.days,
            "count": len(results),
            "results": results,
        }

        if args.trending:
            trending = search_trending_topics(args.days, args.limit, args.min_stars)
            # Deduplicate against main results
            seen = {r["url"] for r in results}
            trending = [r for r in trending if r["url"] not in seen]
            output["trending_count"] = len(trending)
            output["trending"] = trending

        json.dump(output, sys.stdout, indent=2)
    except URLError as e:
        json.dump({"error": str(e), "query": args.query}, sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
