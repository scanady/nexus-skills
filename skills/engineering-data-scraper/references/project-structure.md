# Project Structure

Standard directory layout for a data scraper agent.

```
my-agent/
├── config.yaml              # User customises this (keywords, filters, preferences)
├── profile/
│   └── context.md           # User context the AI uses (resume, interests, criteria)
├── scraper/
│   ├── __init__.py
│   ├── main.py              # Orchestrator: scrape → enrich → store
│   ├── filters.py           # Rule-based pre-filter (fast, before AI)
│   └── sources/
│       ├── __init__.py
│       └── source_name.py   # One file per data source
├── ai/
│   ├── __init__.py
│   ├── client.py            # Gemini REST client with model fallback
│   ├── pipeline.py          # Batch AI analysis
│   ├── jd_fetcher.py        # Fetch full content from URLs (optional)
│   └── memory.py            # Learn from user feedback
├── storage/
│   ├── __init__.py
│   └── notion_sync.py       # Or sheets_sync.py / supabase_sync.py
├── data/
│   └── feedback.json        # User decision history (auto-updated)
├── .env.example
├── setup.py                 # One-time DB/schema creation
├── enrich_existing.py       # Backfill AI scores on old rows
├── requirements.txt
└── .github/
    └── workflows/
        └── scraper.yml      # GitHub Actions schedule
```

## Adapting the Layout

| Storage choice | Replace `notion_sync.py` with |
|---|---|
| Google Sheets | `sheets_sync.py` |
| Supabase | `supabase_sync.py` |
| Local SQLite | `sqlite_sync.py` |

Add one file per data source under `scraper/sources/`. Name it after the source (e.g., `hackernews.py`, `github_trending.py`).
