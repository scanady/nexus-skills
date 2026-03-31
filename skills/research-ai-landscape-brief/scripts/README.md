# Platform Search Scripts

Bundled Python scripts for searching platforms with free, unauthenticated APIs. These serve as the **second tier** in the tool resolution strategy (MCP → Script → Web Search).

## Requirements

- Python 3.10+
- All scripts use only the Python standard library — no `pip install` needed

## Usage

All scripts accept a search query as the first argument and output structured JSON to stdout:

```bash
python scripts/search_hackernews.py "AI language model" --days 30 --limit 25
python scripts/search_polymarket.py "AI" --limit 20
python scripts/search_reddit.py "LLM release" --days 30 --limit 25
python scripts/search_github.py "AI agent framework" --days 30 --limit 25 --trending
python scripts/search_arxiv.py "agent" --days 7 --limit 20
python scripts/search_arxiv.py "" --days 1 --limit 30   # all recent AI papers (last 24h)
```

## Scripts

| Script | Platform | API | Auth Required | Rate Limits |
|--------|----------|-----|---------------|-------------|
| `search_hackernews.py` | Hacker News | Algolia HN Search | No | Generous, unspecified |
| `search_polymarket.py` | Polymarket | Gamma API | No | Generous, unspecified |
| `search_reddit.py` | Reddit | Public `.json` endpoints | No | ~1 req/sec (enforced by script) |
| `search_github.py` | GitHub + GitHub Trending | REST API v3 | Optional `GITHUB_TOKEN` | 10/min unauth, 30/min with token |
| `search_arxiv.py` | arXiv | arXiv Export API | No | ≥3s between requests required; script retries on timeout |

## Output Format

All scripts output JSON with this structure:

```json
{
  "query": "search terms used",
  "days": 30,
  "count": 15,
  "results": [
    {
      "title": "...",
      "url": "...",
      "source": "hackernews|polymarket|reddit|github",
      ...platform-specific fields...
    }
  ]
}
```

## Optional Environment Variables

| Variable | Script | Purpose |
|----------|--------|---------|
| `GITHUB_TOKEN` | `search_github.py` | Higher rate limits (60→5000 req/hr) |
