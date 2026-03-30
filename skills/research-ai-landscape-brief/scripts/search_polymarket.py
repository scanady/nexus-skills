#!/usr/bin/env python3
"""Search Polymarket AI-related prediction markets via the Gamma API. Free, no auth required.

Uses the /events endpoint (which embeds market questions and prices) and paginates
through multiple pages to find AI-related markets, which are sparse in the overall feed.

Usage:
    python search_polymarket.py "AI" --limit 20
"""

import argparse
import json
import re
import sys
from urllib.request import urlopen, Request
from urllib.parse import urlencode
from urllib.error import URLError


API_BASE = "https://gamma-api.polymarket.com"
PAGE_SIZE = 100  # Events per page
MAX_PAGES = 5    # Scan up to 500 events to find AI-related ones


def is_ai_related(text: str, query_lower: str, ai_terms: set) -> bool:
    return any(re.search(r'\b' + re.escape(term) + r'\b', text)
               for term in ({query_lower} | ai_terms))


def parse_market_outcomes(market: dict) -> tuple[list[str], list[float]]:
    """Parse outcomes and prices from a market dict. Gamma API may return JSON strings."""
    outcomes_raw = market.get("outcomes", [])
    if isinstance(outcomes_raw, str):
        try:
            outcomes_raw = json.loads(outcomes_raw)
        except (json.JSONDecodeError, TypeError):
            outcomes_raw = []
    outcomes = [o for o in outcomes_raw if isinstance(o, str)]

    prices_raw = market.get("outcomePrices", [])
    if isinstance(prices_raw, str):
        try:
            prices_raw = json.loads(prices_raw)
        except (json.JSONDecodeError, TypeError):
            prices_raw = []
    prices = []
    for p in prices_raw:
        try:
            prices.append(round(float(p), 4))
        except (TypeError, ValueError):
            prices.append(0.0)
    return outcomes, prices


def search_events(query: str, limit: int = 20) -> list[dict]:
    query_lower = query.lower()
    ai_terms = {
        "ai", "artificial intelligence", "agi", "llm", "gpt", "openai",
        "anthropic", "deepmind", "machine learning", "neural", "language model",
        "claude", "gemini", "copilot", "chatgpt", "midjourney", "stable diffusion",
    }

    results = []
    for page in range(MAX_PAGES):
        params = urlencode({
            "limit": PAGE_SIZE,
            "offset": page * PAGE_SIZE,
            "active": "true",
            "closed": "false",
        })
        url = f"{API_BASE}/events?{params}"
        req = Request(url, headers={"User-Agent": "ai-landscape-brief/1.0"})
        with urlopen(req, timeout=20) as resp:
            events = json.loads(resp.read().decode())

        if not events:
            break  # No more pages

        for event in events:
            title = event.get("title", "")
            description = event.get("description") or ""
            text = f"{title} {description}".lower()

            if not is_ai_related(text, query_lower, ai_terms):
                continue

            # Collect individual market questions and prices from the embedded markets list
            markets = event.get("markets", [])
            market_items = []
            for m in markets:
                outcomes, prices = parse_market_outcomes(m)
                market_items.append({
                    "question": m.get("question", ""),
                    "outcomes": outcomes,
                    "outcome_prices": prices,
                })

            results.append({
                "title": title,
                "description": description[:300],
                "url": f"https://polymarket.com/event/{event.get('slug', event.get('id', ''))}",
                "volume": round(float(event.get("volume", 0) or 0), 2),
                "liquidity": round(float(event.get("liquidity", 0) or 0), 2),
                "end_date": event.get("endDate", ""),
                "markets": market_items,
                "source": "polymarket",
            })

        if len(results) >= limit:
            break

    results.sort(key=lambda x: x["volume"], reverse=True)
    return results[:limit]


def main():
    parser = argparse.ArgumentParser(description="Search Polymarket AI prediction markets (Gamma API)")
    parser.add_argument("query", help="Search query (filters AI-related events)")
    parser.add_argument("--limit", type=int, default=20, help="Max results (default: 20)")
    args = parser.parse_args()

    try:
        results = search_events(args.query, args.limit)
        json.dump({"query": args.query, "count": len(results), "results": results}, sys.stdout, indent=2)
    except URLError as e:
        json.dump({"error": str(e), "query": args.query}, sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
