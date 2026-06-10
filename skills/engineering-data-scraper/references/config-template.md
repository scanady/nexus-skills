# Config + Requirements Templates

## config.yaml

```yaml
# Customise this file — no code changes needed

# What to collect (pre-filter before AI)
filters:
  required_keywords: []      # item must contain at least one
  blocked_keywords: []       # item must not contain any

# Your priorities — AI uses these for scoring
priorities:
  - "example priority 1"
  - "example priority 2"

# Storage
storage:
  provider: "notion"         # notion | sheets | supabase | sqlite

# Feedback learning
feedback:
  positive_statuses: ["Saved", "Applied", "Interested"]
  negative_statuses: ["Skip", "Rejected", "Not relevant"]

# AI settings
ai:
  enabled: true
  model: "gemini-2.5-flash"
  min_score: 0               # filter out items below this score
  rate_limit_seconds: 7      # seconds between API calls
  batch_size: 5              # items per API call
```

## requirements.txt

```
requests==2.31.0
beautifulsoup4==4.12.3
lxml==5.1.0
python-dotenv==1.0.1
pyyaml==6.0.2
notion-client==2.2.1   # if using Notion
# playwright==1.40.0   # uncomment for JS-rendered sites
```

## .env.example

```
# Copy to .env and fill in your values — never commit .env to git

GEMINI_API_KEY=your_gemini_api_key_here

# Notion (if provider=notion)
NOTION_TOKEN=your_notion_integration_token_here
NOTION_DATABASE_ID=your_notion_database_id_here

# Google Sheets (if provider=sheets)
# SHEET_ID=your_google_sheet_id_here

# Supabase (if provider=supabase)
# SUPABASE_URL=https://your-project.supabase.co
# SUPABASE_KEY=your_supabase_anon_key_here
```
