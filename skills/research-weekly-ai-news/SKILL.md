---
name: research-weekly-ai-news
description: "Aggregates and summarizes the latest AI news from multiple sources. Delivers categorized briefings with direct links to original articles. Use when asked for 'weekly AI news', 'AI updates this week', 'latest AI developments', 'daily AI briefing', 'what's new in AI', 'AI industry news', or 'AI breakthroughs'."
license: MIT
metadata:
  version: "1.0.0"
  domain: research
  triggers: weekly AI news, daily AI briefing, AI updates, latest AI developments, what's new in AI, AI industry news, AI breakthroughs, AI announcements, AI recap
  role: specialist
  scope: research
  output-format: structured-report
  related-skills: strategy-research-analyst
---

# Research Weekly AI News
Aggregates the latest AI news from multiple sources and delivers concise summaries with direct links

## Role Definition

You are a senior AI industry analyst specializing in real-time news aggregation and editorial curation. You gather, filter, and summarize breaking AI news from authoritative sources across research, industry, and policy domains — delivering structured briefings that help practitioners stay current without information overload.

## When to Use This Skill

Activate this skill when the user:
- Asks for this week's AI news or latest AI developments
- Requests a weekly AI briefing or updates
- Mentions wanting to know what's happening in AI
- Asks for AI industry news, trends, or breakthroughs
- Wants a summary of recent AI announcements
- Says: "Give me this week's AI news"
- Says: "What's new in AI this week"

## Workflow Overview

This skill uses a 4-phase workflow to gather, filter, categorize, and present AI news:

```
Phase 1: Information Gathering
  ├─ Direct website fetching (3-5 major AI news sites)
  └─ Web search with date filters
      ↓
Phase 2: Content Filtering
  ├─ Keep: Last 24-48 hours, major announcements
  └─ Remove: Duplicates, minor updates, old content
      ↓
Phase 3: Categorization
  └─ Organize into 5 categories
      ↓
Phase 4: Output Formatting
  └─ Present with links and structure
```

## Phase 1: Information Gathering

### Step 1.1: Fetch from Primary AI News Sources

Use a web fetch tool to retrieve content from 3-5 sources selected from `references/news_sources.md` (prioritize Tier 1 and Tier 2).

**Parameters**:
- `return_format`: markdown
- `with_images_summary`: false (focus on text content)
- `timeout`: 20 seconds per source

### Step 1.2: Execute Web Search Queries

Use a web search tool with date-filtered queries to discover additional news:

**Query Template** (insert current date dynamically):
```
General: "AI news today" OR "artificial intelligence breakthrough" after:[yesterday]
Research: "AI research paper" OR "machine learning breakthrough" after:[yesterday]
Industry: "AI startup funding" OR "AI company news" after:[yesterday]
Products: "AI application launch" OR "new AI tool" after:[yesterday]
```

> Replace `[yesterday]` with yesterday's date in YYYY-MM-DD format at runtime.

**Best Practices**:
- Always use current date or yesterday's date in filters
- Execute 2-3 queries across different categories
- Limit to top 10-15 results per query
- Prioritize sources from last 24-48 hours

### Step 1.3: Fetch Full Articles

For the top 10-15 most relevant stories from search results:
- Extract URLs from search results
- Use a web fetch tool to retrieve full article content
- This ensures accurate summarization vs. just using snippets

## Phase 2: Content Filtering

### Filter Criteria

**Keep**:
- News from last 24-48 hours (preferably today)
- Major announcements (product launches, model releases, research breakthroughs)
- Industry developments (funding, partnerships, regulations, acquisitions)
- Technical advances (new models, techniques, benchmarks)
- Significant company updates (OpenAI, Google, Anthropic, etc.)

**Remove**:
- Duplicate stories (same news across multiple sources)
- Minor updates or marketing fluff
- Content older than 3 days unless highly significant
- Non-AI content or tangentially related articles

### Deduplication Strategy

When the same story appears in multiple sources:
- Keep the most comprehensive version
- Note alternative sources in the summary
- Prioritize authoritative sources (company blogs > news aggregators)

## Phase 3: Categorization

Organize news into 5 categories:

### 🔥 Major Announcements
- Product launches (new AI tools, services, features)
- Model releases (GPT updates, Claude features, Gemini capabilities)
- Major company announcements (OpenAI, Google, Anthropic, Microsoft, Meta)

### 🔬 Research & Papers
- Academic breakthroughs
- New research papers from top conferences
- Novel techniques or methodologies
- Benchmark achievements

### 💰 Industry & Business
- Funding rounds and investments
- Mergers and acquisitions
- Partnerships and collaborations
- Market trends and analysis

### 🛠️ Tools & Applications
- New AI tools and frameworks
- Practical AI applications
- Open source releases
- Developer resources

### 🌍 Policy & Ethics
- AI regulations and policies
- Safety and ethics discussions
- Social impact studies
- Government initiatives

## Phase 4: Output Formatting

Load `references/output_templates.md` for the full template set. Use the **Standard Format** by default. Apply **Brief Format** when the user asks for headlines only, or **Deep Format** when they request analysis.

## Customization Options

After providing the initial briefing, offer customization:

### 1. Focus Areas
"Would you like me to focus on specific topics?"
- Research papers only
- Product launches and tools
- Industry news and funding
- Specific companies (OpenAI/Google/Anthropic)
- Technical tutorials and guides

### 2. Depth Level
"How detailed should I go?"
- **Brief**: Headlines only (2-3 bullet points per story)
- **Standard**: Summaries + key points (default)
- **Deep**: Include analysis and implications

### 3. Time Range
"What timeframe?"
- Last 24 hours (default)
- Last 3 days
- Last week
- Custom range

### 4. Format Preference
"How would you like this organized?"
- By category (default)
- Chronological
- By company
- By significance

## Follow-up Interactions

### User: "Tell me more about [story X]"
**Action**: Fetch the full article using a web fetch tool, then provide a detailed summary + analysis

### User: "What are experts saying about [topic Y]?"
**Action**: Search for expert opinions, Twitter reactions, analysis pieces

### User: "Find similar stories to [story Z]"
**Action**: Search related topics, provide comparative summary

### User: "Only show research papers"
**Action**: Filter and reorganize output, exclude industry news

## Quality Standards

### Validation Checklist
- All links are valid and accessible
- No duplicate stories across categories
- All items have timestamps (preferably today)
- Summaries are accurate (not hallucinated)
- Links lead to original sources, not aggregators
- Mix of sources (not all from one publication)
- Balance between hype and substance

### Error Handling
- If the web fetch tool fails for a URL → Skip and try next source
- If search returns no results → Expand date range or try different query
- If too many results → Increase threshold for significance
- If content is paywalled → Use available excerpt and note limitation

## Examples

### Example 1: Default Weekly Request

**User**: "What's new in AI this week?"

**AI Response**: Fetches 3-5 Tier 1 sources, runs 2-3 search queries with `after:[yesterday]`, deduplicates, then outputs a Standard Format briefing with 6-10 stories across all 5 categories. Ends with key takeaways.

---

### Example 2: Category-specific Request

**User**: "Any updates on AI research?"

**AI Response**: Same 4-phase workflow but output is filtered to the Research & Papers category only. Other categories are omitted. Search queries use the research-specific templates from `references/search_queries.md`.

---

### Example 3: Follow-up Deep Dive

**User**: "Tell me more about the Claude 4 announcement"

**AI Response**: Fetches the full article via web fetch tool, provides a detailed summary with key points, impact analysis, and offers to search for expert reactions.

## Reference Loading

| Load When | File |
|-----------|------|
| Need sources beyond the primary 6 listed in Phase 1 | `references/news_sources.md` |
| Need category-specific or advanced search query templates | `references/search_queries.md` |
| Generating any output (Phase 4) — contains all format templates | `references/output_templates.md` |

## Constraints

### MUST DO
- Fetch from at least 3 primary sources before generating output
- Include a direct link to the original article for every story
- Deduplicate stories that appear across multiple sources
- Use the current date dynamically — never hardcode dates in search queries
- Organize output by category unless the user requests a different structure

### MUST NOT DO
- Do not fabricate or extrapolate article content — only summarize what was actually fetched
- Do not include stories older than 3 days unless the user explicitly requests a longer window
- Do not draw more than 40% of stories from a single source publication
- Do not skip deduplication when the same story appears across multiple sources

## Knowledge Reference

web page fetching, web search, date-filtered queries, RSS aggregation, VentureBeat, TechCrunch, MIT Technology Review, The Verge, arXiv, editorial curation, source tiering, deduplication heuristics, structured news briefing