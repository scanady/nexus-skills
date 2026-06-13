# Orchestration — main.py + GitHub Actions

## scraper/main.py

```python
# scraper/main.py
import os, sys, yaml
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from scraper.sources import my_source          # add your sources

# NOTE: This example uses Notion. If storage.provider is "sheets" or "supabase",
# replace this import with storage.sheets_sync or storage.supabase_sync and update
# the env var and sync() call accordingly.
from storage.notion_sync import sync

SOURCES = [
    ("My Source", my_source.fetch),
]


def ai_enabled():
    return bool(os.environ.get("GEMINI_API_KEY"))


def main():
    config = yaml.safe_load((Path(__file__).parent.parent / "config.yaml").read_text())
    provider = config.get("storage", {}).get("provider", "notion")

    # Resolve the storage target identifier from env based on provider
    if provider == "notion":
        db_id = os.environ.get("NOTION_DATABASE_ID")
        if not db_id:
            print("ERROR: NOTION_DATABASE_ID not set"); sys.exit(1)
    else:
        # Extend here for sheets (SHEET_ID) or supabase (SUPABASE_TABLE) etc.
        print(f"ERROR: provider '{provider}' not yet wired in main.py"); sys.exit(1)

    all_items = []

    for name, fetch_fn in SOURCES:
        try:
            items = fetch_fn()
            print(f"[{name}] {len(items)} items")
            all_items.extend(items)
        except Exception as e:
            print(f"[{name}] FAILED: {e}")

    # Deduplicate by URL
    seen, deduped = set(), []
    for item in all_items:
        if (url := item.get("url", "")) and url not in seen:
            seen.add(url); deduped.append(item)

    print(f"Unique items: {len(deduped)}")

    if ai_enabled() and deduped:
        from ai.memory import load_feedback, build_preference_prompt
        from ai.pipeline import analyse_batch

        # load_feedback() reads data/feedback.json written by your feedback sync script.
        # To keep it current, implement a separate feedback_sync.py that queries your
        # storage provider for items with positive/negative statuses and calls save_feedback().
        feedback = load_feedback()
        preference = build_preference_prompt(feedback)
        context_path = Path(__file__).parent.parent / "profile" / "context.md"
        context = context_path.read_text() if context_path.exists() else ""
        deduped = analyse_batch(deduped, context=context, preference_prompt=preference)
    else:
        print("[AI] Skipped — GEMINI_API_KEY not set")

    added, skipped = sync(db_id, deduped)
    print(f"Done — {added} new, {skipped} existing")


if __name__ == "__main__":
    main()
```

## .github/workflows/scraper.yml

```yaml
name: Data Scraper Agent

on:
  schedule:
    - cron: "0 */3 * * *"  # every 3 hours — adjust to your needs
  workflow_dispatch:        # allow manual trigger

permissions:
  contents: write   # required for the feedback-history commit step

jobs:
  scrape:
    runs-on: ubuntu-latest
    timeout-minutes: 20

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"

      - run: pip install -r requirements.txt

      # Uncomment if Playwright is enabled in requirements.txt
      # - name: Install Playwright browsers
      #   run: python -m playwright install chromium --with-deps

      - name: Run agent
        env:
          NOTION_TOKEN: ${{ secrets.NOTION_TOKEN }}
          NOTION_DATABASE_ID: ${{ secrets.NOTION_DATABASE_ID }}
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        run: python -m scraper.main

      - name: Commit feedback history
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add data/feedback.json || true
          git diff --cached --quiet || git commit -m "chore: update feedback history"
          git push
```

## Cron Schedule Reference

| Cron | Frequency |
|---|---|
| `0 */3 * * *` | Every 3 hours |
| `0 */6 * * *` | Every 6 hours |
| `0 8 * * *` | Daily at 8am UTC |
| `0 8 * * 1` | Weekly on Monday at 8am UTC |
