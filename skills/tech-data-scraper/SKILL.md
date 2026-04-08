---
name: tech-data-scraper
description: Build a fully automated AI-powered data collection agent for any public source — job boards, prices, news, GitHub, sports, anything. Scrapes on a schedule, enriches data with a free LLM (Gemini Flash), stores results in Notion/Sheets/Supabase, and learns from user feedback. Runs 100% free on GitHub Actions. Use when the user wants to monitor, collect, or track any public data automatically, or when they say "build a bot that checks", "monitor X for me", "collect data from", "automate data collection", "track prices", "track jobs", "web scraper", or "data scraper".
license: MIT
metadata:
  version: "1.0.0"
  domain: tech
  triggers: scrape website, build a bot that checks, monitor X for me, collect data, track prices, track jobs, automate data collection, data scraper, web scraper, build scraper, free scraper, GitHub Actions scraper, Gemini scraper, Notion scraper
  role: specialist
  scope: execution
  output-format: code
  related-skills: tech-api-mcp-builder, tech-dev-writing-plans
---

# Data Scraper Agent

## Role Definition

You are a senior Python automation engineer specializing in production-grade data collection systems. You build scrapers that are resilient, frugal, and genuinely useful — using free-tier infrastructure (Gemini Flash, GitHub Actions, Notion/Sheets/Supabase) to deliver agents that run indefinitely without cost. You don't build toy examples; you build deployable systems with deduplication, AI enrichment, feedback learning, and scheduled automation from day one.

**Stack: Python · Gemini Flash (free) · GitHub Actions (free) · Notion / Sheets / Supabase**

## When to Activate

- User wants to scrape or monitor any public website or API
- User says "build a bot that checks...", "monitor X for me", "collect data from..."
- User wants to track jobs, prices, news, repos, sports scores, events, listings
- User asks how to automate data collection without paying for hosting
- User wants an agent that gets smarter over time based on their decisions

## Core Concepts

### The Three Layers

```
COLLECT → ENRICH → STORE
  │           │        │
Scraper    AI (LLM)  Database
runs on    scores/   Notion /
schedule   summarises Sheets /
           & classifies Supabase
```

### Free Stack

| Layer | Tool | Why |
|---|---|---|
| **Scraping** | `requests` + `BeautifulSoup` | No cost, covers 80% of public sites |
| **JS-rendered sites** | `playwright` (free) | When HTML scraping fails |
| **AI enrichment** | Gemini Flash via REST API | 500 req/day, 1M tokens/day — free |
| **Storage** | Notion API | Free tier, great UI for review |
| **Schedule** | GitHub Actions cron | Free for public repos |
| **Learning** | JSON feedback file in repo | Zero infra, persists in git |

### AI Model Fallback Chain

Build agents to auto-fallback across Gemini models on quota exhaustion:

```
gemini-2.0-flash-lite (30 RPM) →
gemini-2.0-flash (15 RPM) →
gemini-2.5-flash (10 RPM) →
gemini-flash-lite-latest (fallback)
```

### Batch API Calls for Efficiency

Never call the LLM once per item. Always batch:

```python
# BAD: 33 API calls for 33 items
for item in items:
    result = call_ai(item)  # 33 calls → hits rate limit

# GOOD: 7 API calls for 33 items (batch size 5)
for batch in chunks(items, size=5):
    results = call_ai(batch)  # 7 calls → stays within free tier
```

---

## Workflow

### Step 1: Understand the Goal

Ask the user:

1. **What to collect:** "What data source? URL / API / RSS / public endpoint?"
2. **What to extract:** "What fields matter? Title, price, URL, date, score?"
3. **How to store:** "Where should results go? Notion, Google Sheets, Supabase, or local file?"
4. **How to enrich:** "Do you want AI to score, summarise, classify, or match each item?"
5. **Frequency:** "How often should it run? Every hour, daily, weekly?"

Common examples to prompt:
- Job boards → score relevance to resume
- Product prices → alert on drops
- GitHub repos → summarise new releases
- News feeds → classify by topic + sentiment
- Sports results → extract stats to tracker
- Events calendar → filter by interest

---

### Step 2: Design the Architecture

Load `references/project-structure.md` for the standard directory layout. Adapt to the user's storage choice and sources.

---

### Step 3: Build the Scraper Source

See `references/scraper-source.md` for the full source template, HTML scraping pattern, and RSS feed pattern.

---

### Step 4: Build the Gemini AI Client

See `references/ai-client.md` for the full Gemini REST client with model fallback.

---

### Step 5: Build the AI Pipeline (Batch)

See `references/ai-client.md` for the batch pipeline implementation.

---

### Step 6: Build the Feedback Learning System

See `references/feedback-learning.md` for the memory module and storage integration pattern.

---

### Step 7: Build Storage (Notion example)

See `references/storage-notion.md` for the full Notion sync implementation (get_existing_urls, push_item, sync).

---
        _client = Client(auth=os.environ["NOTION_TOKEN"])
    return _client

def get_existing_urls(db_id: str) -> set[str]:
    """Fetch all URLs already stored — used for deduplication."""
    client, seen, cursor = get_client(), set(), None
    while True:
        resp = client.databases.query(database_id=db_id, page_size=100, **{"start_cursor": cursor} if cursor else {})
        for page in resp["results"]:
            url = page["properties"].get("URL", {}).get("url", "")
            if url: seen.add(url)
        if not resp["has_more"]: break
        cursor = resp["next_cursor"]
    return seen

def push_item(db_id: str, item: dict) -> bool:
    """Push one item to Notion. Returns True on success."""
    props = {
        "Name": {"title": [{"text": {"content": item.get("name", "")[:100]}}]},
        "URL": {"url": item.get("url")},
        "Source": {"select": {"name": item.get("source", "Unknown")}},
        "Date Found": {"date": {"start": item.get("date_found")}},
        "Status": {"select": {"name": "New"}},
    }
    # AI fields
    if item.get("ai_score") is not None:
        props["AI Score"] = {"number": item["ai_score"]}
    if item.get("ai_summary"):
        props["Summary"] = {"rich_text": [{"text": {"content": item["ai_summary"][:2000]}}]}
    if item.get("ai_notes"):
        props["Notes"] = {"rich_text": [{"text": {"content": item["ai_notes"][:2000]}}]}

    try:
        get_client().pages.create(parent={"database_id": db_id}, properties=props)
        return True
    except APIResponseError as e:
        print(f"[notion] Push failed: {e}")
See `references/storage-notion.md` for the full Notion sync implementation.

---

### Step 8: Orchestrate in main.py

See `references/orchestration.md` for the full `main.py` orchestrator.

---

### Step 9: GitHub Actions Workflow

See `references/orchestration.md` for the GitHub Actions cron workflow.

---

### Step 10: config.yaml Template

See `references/config-template.md` for the full `config.yaml` and `requirements.txt` templates.

---

## Common Scraping Patterns

All 5 patterns (REST API, HTML scraping, RSS feed, paginated API, Playwright) are in `references/scraper-source.md`.

---

## Reference Guide

| Component | Reference | Load When |
|---|---|---|
| Project directory structure | `references/project-structure.md` | Step 2 — designing the layout |
| Scraper source template + all patterns | `references/scraper-source.md` | Building any data source file |
| Gemini AI client + batch pipeline | `references/ai-client.md` | Adding AI enrichment |
| Feedback learning system | `references/feedback-learning.md` | Adding learn-from-decisions feature |
| Notion storage | `references/storage-notion.md` | User selects Notion as target |
| Orchestration (main.py + GitHub Actions) | `references/orchestration.md` | Wiring up the final agent or setting up the schedule |
| Config + requirements templates | `references/config-template.md` | Creating the user-facing config file |

## Constraints

### MUST DO
- Ask all 5 goal questions (Step 1) before writing any code
- Use the 4-model fallback chain for all Gemini calls
- Batch LLM calls — minimum 5 items per API call
- Deduplicate by URL before every storage push
- Put all user-facing settings in `config.yaml` — no hardcoded values in code
- Store all secrets in `.env` + GitHub Secrets — never in source
- Respect `robots.txt`; prefer public APIs over HTML scraping when available
- Provide `.env.example` for onboarding
- Run through the Quality Checklist before marking the agent complete

### MUST NOT DO
- Call the LLM once per item — always batch
- Hardcode keywords, thresholds, or filters in source code — they belong in `config.yaml`
- Make any `requests.get` call without a `User-Agent` header and a `timeout`
- Set `maxOutputTokens` below 2048 — truncated JSON causes silent parse failures
- Commit any API key, token, or secret to the repo
- Skip deduplication — duplicate rows corrupt storage over time

## Quality Checklist

Before marking the agent complete:

- [ ] `config.yaml` controls all user-facing settings — no hardcoded values
- [ ] `profile/context.md` holds user-specific context for AI matching
- [ ] Deduplication by URL before every storage push
- [ ] Gemini client has 4-model fallback chain
- [ ] Batch size ≤ 5 items per API call
- [ ] `maxOutputTokens` ≥ 2048
- [ ] `.env` is in `.gitignore`
- [ ] `.env.example` provided for onboarding
- [ ] `setup.py` creates DB schema on first run
- [ ] `enrich_existing.py` backfills AI scores on old rows
- [ ] GitHub Actions workflow commits `feedback.json` after each run
- [ ] README covers: setup in < 5 minutes, required secrets, customisation

## Free Tier Limits

| Service | Free Limit | Typical Usage |
|---|---|---|
| Gemini Flash Lite | 30 RPM, 1500 RPD | ~56 req/day at 3-hr intervals |
| Gemini 2.0 Flash | 15 RPM, 1500 RPD | Good fallback |
| Gemini 2.5 Flash | 10 RPM, 500 RPD | Use sparingly |
| GitHub Actions | Unlimited (public repos) | ~20 min/day |
| Notion API | Unlimited | ~200 writes/day |
| Supabase | 500MB DB, 2GB transfer | Fine for most agents |
| Google Sheets API | 300 req/min | Works for small agents |

## Real-World Examples

```
"Build me an agent that monitors Hacker News for AI startup funding news"
"Scrape product prices from 3 e-commerce sites and alert when they drop"
"Track new GitHub repos tagged with 'llm' or 'agents' — summarise each one"
"Collect job listings from multiple boards into Notion"
"Monitor a subreddit for posts mentioning my company — classify sentiment"
"Scrape new academic papers from arXiv on a topic I care about daily"
"Track sports fixture results and keep a running table in Google Sheets"
"Build a real estate listing watcher — alert on new properties under budget"
```

## Knowledge Reference

Python requests, BeautifulSoup, lxml, Playwright, Gemini Flash REST API, GitHub Actions cron, Notion API, Supabase, Google Sheets API, python-dotenv, PyYAML, rate limiting, web scraping etiquette, robots.txt, deduplication patterns, JSON parsing, batch LLM calls, free-tier infrastructure
