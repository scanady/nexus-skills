#!/usr/bin/env python3
"""Search Reddit via public .json endpoints. Free, no auth required.

Usage:
    python search_reddit.py "AI language model" --days 30 --limit 25
    python search_reddit.py "LLM release" --subreddits MachineLearning,LocalLLaMA --days 7
"""

import argparse
import json
import sys
import time
from urllib.request import urlopen, Request
from urllib.parse import urlencode, quote
from urllib.error import URLError


DEFAULT_SUBREDDITS = [
    "MachineLearning", "LocalLLaMA", "artificial", "ChatGPT",
    "ClaudeAI", "singularity", "StableDiffusion", "OpenAI",
    "ArtificialIntelligence", "LangChain",
]

# Map --days to Reddit time filter
TIME_FILTERS = {
    (0, 1): "day",
    (2, 7): "week",
    (8, 30): "month",
    (31, 365): "year",
    (366, 99999): "all",
}


def days_to_time_filter(days: int) -> str:
    for (lo, hi), val in TIME_FILTERS.items():
        if lo <= days <= hi:
            return val
    return "month"


def search_subreddit(subreddit: str, query: str, time_filter: str, limit: int) -> list[dict]:
    params = urlencode({
        "q": query,
        "sort": "top",
        "t": time_filter,
        "limit": min(limit, 25),
        "restrict_sr": "on",
    })
    url = f"https://www.reddit.com/r/{quote(subreddit)}/search.json?{params}"
    req = Request(url, headers={
        "User-Agent": "ai-landscape-brief/1.0 (research tool; not a bot)",
    })

    with urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode())

    results = []
    for child in data.get("data", {}).get("children", []):
        post = child.get("data", {})
        results.append({
            "title": post.get("title", ""),
            "subreddit": post.get("subreddit", subreddit),
            "url": f"https://www.reddit.com{post.get('permalink', '')}",
            "upvotes": post.get("ups", 0),
            "comments": post.get("num_comments", 0),
            "author": post.get("author", ""),
            "created_utc": post.get("created_utc", 0),
            "selftext_preview": (post.get("selftext", "") or "")[:300],
            "source": "reddit",
        })
    return results


def main():
    parser = argparse.ArgumentParser(description="Search Reddit (.json endpoints)")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--days", type=int, default=30, help="Lookback window in days (default: 30)")
    parser.add_argument("--limit", type=int, default=25, help="Max results per subreddit (default: 25)")
    parser.add_argument("--subreddits", type=str, default=None,
                        help=f"Comma-separated subreddits (default: {','.join(DEFAULT_SUBREDDITS[:5])}...)")
    args = parser.parse_args()

    subreddits = args.subreddits.split(",") if args.subreddits else DEFAULT_SUBREDDITS
    time_filter = days_to_time_filter(args.days)

    all_results = []
    errors = []
    for sub in subreddits:
        try:
            results = search_subreddit(sub.strip(), args.query, time_filter, args.limit)
            all_results.extend(results)
            time.sleep(1)  # Rate limit: 1 request per second for unauthenticated
        except URLError as e:
            errors.append({"subreddit": sub, "error": str(e)})

    # Sort by upvotes descending, deduplicate
    seen = set()
    unique = []
    for r in sorted(all_results, key=lambda x: x["upvotes"], reverse=True):
        if r["url"] not in seen:
            seen.add(r["url"])
            unique.append(r)

    output = {
        "query": args.query,
        "days": args.days,
        "subreddits_searched": subreddits,
        "count": len(unique),
        "results": unique[:args.limit * 2],  # Cap total output
    }
    if errors:
        output["errors"] = errors

    json.dump(output, sys.stdout, indent=2)


if __name__ == "__main__":
    main()
