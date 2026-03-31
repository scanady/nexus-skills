# Platform Search Guide

AI-specific search query templates and strategy for each platform. Replace `[30d_ago]` with the date 30 days before the current date in YYYY-MM-DD format.

**Tool Resolution Order**: For each platform, use MCP tool (if connected) → bundled script (if available) → web search fallback. See the Tool Discovery section in SKILL.md.

---

## GitHub

> **MCP tools**: `github`, `github-mcp`, any tool with "github" + "search" or "repository"  
> **Script**: `scripts/search_github.py "AI agent" --days 30 --trending`  
> **Web fallback**: `site:github.com` queries + direct fetch of `github.com/trending`

### Why GitHub Matters for AI Research
GitHub is the leading indicator. When developers start building with a new model, framework, or technique, it shows up in repository activity before it hits the news cycle. Star velocity, fork counts, and README updates are signals of real adoption — not just hype.

### GitHub Trending — Explicit Step (Run This First)

GitHub Trending is velocity-based, not cumulative. It catches breakout repos before they accumulate the star counts that make them visible in topic/keyword searches.

**Fetch both views as a web fetch** (or use GitHub MCP tool if available):
```
https://github.com/trending?since=daily   ← highest velocity; daily breakouts
https://github.com/trending?since=weekly  ← weekly view; broader signal
```

**Script shortcut** (proxies trending via recently-updated AI topic repos):
```
python scripts/search_github.py "AI" --days 7 --min-stars 10 --trending
```

**What to look for in trending results**:
- Repos from known researchers (check `references/frontier_researchers.md`) — auto-qualify as `[FRONTIER]`
- New repos (created < 7 days ago) with `stars_per_day ≥ 100` — high-velocity; `≥ 500` — breakout
- Repos from major lab GitHub orgs (`openai`, `anthropic`, `google-deepmind`, `meta-llama`, `mistralai`)

### Standard Repository Searches

**New AI repos by topic (last 30 days)**:
```
github trending AI machine learning LLM after:[30d_ago]
```
```
github trending repositories "artificial intelligence" OR "language model" OR "diffusion" this month
```

**New releases from major AI projects**:
```
site:github.com release "v" (pytorch OR tensorflow OR transformers OR langchain OR llamaindex OR vllm OR ollama) after:[30d_ago]
```

**Agent frameworks & MCP servers**:
```
site:github.com (MCP OR "model context protocol" OR "agent framework" OR "agentic") after:[30d_ago]
```

### What to Extract
- Repository name, description, **star count and `stars_per_day` velocity**
- README summary — what does it do, what's new
- Release notes for significant version bumps
- Language/framework (Python, TypeScript, Rust — signals infrastructure maturity)
- Whether the author/org appears in `references/frontier_researchers.md`

---

## Reddit

> **MCP tools**: `reddit`, any tool with "reddit" + "search"  
> **Script**: `scripts/search_reddit.py "AI release" --days 30 --subreddits MachineLearning,LocalLLaMA`  
> **Web fallback**: `site:reddit.com` queries

### Why Reddit Matters for AI Research
Reddit is the practitioner signal. It's where developers, researchers, and power users share real experiences — not polished marketing. Top comments with high upvotes are often the most insightful, contrarian, or technically accurate takes.

### Key Subreddits

| Subreddit | Focus |
|-----------|-------|
| r/MachineLearning | Research papers, industry news, technical discussion |
| r/LocalLLaMA | Self-hosted models, quantization, inference optimization |
| r/artificial | General AI news and discussion |
| r/ChatGPT | Consumer AI products, OpenAI ecosystem |
| r/ClaudeAI | Anthropic ecosystem, Claude usage |
| r/singularity | AGI speculation, frontier research, existential discussion |
| r/StableDiffusion | Image generation, ComfyUI workflows, model releases |
| r/OpenAI | OpenAI products and API |
| r/ArtificialIntelligence | Broader AI industry discussion |
| r/LangChain | Agent frameworks, RAG, orchestration |

### Search Queries
```
site:reddit.com (r/MachineLearning OR r/LocalLLaMA OR r/artificial) AI announcement OR release OR breakthrough after:[30d_ago]
```
```
site:reddit.com r/MachineLearning "new paper" OR "just released" OR "state of the art" after:[30d_ago]
```
```
site:reddit.com r/LocalLLaMA "new model" OR "just dropped" OR benchmark OR GGUF after:[30d_ago]
```

### What to Extract
- Thread title, subreddit, upvote count, comment count
- Top comment text and upvote count — this is where the real insight lives
- Sentiment: excitement, skepticism, practical adoption signals

---

## X / Twitter

> **MCP tools**: `twitter`, `x-search`, `socialdata`, any tool with "tweet" + "search"  
> **Script**: none (API requires paid access)  
> **Web fallback**: `site:x.com` or `site:twitter.com` queries

### Why X Matters for AI Research
X is the breaking news wire for AI. Researchers announce papers, companies post launches, and founders share roadmaps here before anywhere else. High-engagement posts (likes, reposts) from known AI voices carry strong signal.

### Key Accounts to Watch
AI researchers: @ylecun, @kaborimaneesh, @sama, @AndrewYNg, @demaborsky
Companies: @OpenAI, @AnthropicAI, @GoogleDeepMind, @Meta, @xaborimaneesh
Developers: @swaborimaneesh, @karpborimaneesh, accounts posting code + demos
VCs/Analysts: @aaborimaneesh, accounts posting funding/market analysis

### Search Queries
```
site:x.com OR site:twitter.com AI model release OR launch OR announcement after:[30d_ago]
```
```
site:x.com "just released" OR "now available" (AI OR LLM OR model OR GPT OR Claude) after:[30d_ago]
```
```
site:x.com "open source" (AI OR LLM OR "language model") release OR weights after:[30d_ago]
```

### What to Extract
- Post text, @handle, like count, repost count
- Whether the poster is a primary source (e.g., company account announcing their own product)
- Thread content if it's a multi-post announcement
- Quote tweets with high engagement — community reaction layer

---

## Hacker News

> **MCP tools**: `hackernews`, `hn`, any tool with "hn" + "search"  
> **Script**: `scripts/search_hackernews.py "AI" --days 30 --limit 25`  
> **Web fallback**: `site:news.ycombinator.com` queries

### Why HN Matters for AI Research
HN is the developer skepticism filter. The community is technically sophisticated and allergic to hype. High-scoring AI stories on HN have passed a quality bar. Comment threads often contain expert rebuttals, alternative perspectives, and practical adoption stories.

### Search Queries
```
site:news.ycombinator.com AI OR LLM OR "machine learning" OR "language model" after:[30d_ago]
```
```
site:news.ycombinator.com "Show HN" (AI OR LLM OR model OR agent) after:[30d_ago]
```

### API Alternative
Algolia HN Search API (`hn.algolia.com`) supports date-filtered queries directly — no auth needed.

### What to Extract
- Story title, points, comment count
- Top comments (especially contrarian or technically substantive takes)
- Show HN posts — these represent new tools being launched

---

## arXiv

> **MCP tools**: `arxiv`, `arxiv-search`, any tool with "arxiv" + "search" or "paper"  
> **Script**: `scripts/search_arxiv.py "agent" --days 7 --limit 25`  
> **Web fallback**: `site:arxiv.org` queries; also `paperswithcode.com` for SOTA tracking

### Why arXiv Matters for AI Research
arXiv is where frontier work appears first — often 2–6 weeks before press coverage, and months before wide adoption. Major labs (OpenAI, Anthropic, DeepMind, Meta AI) post preprints before official blog posts. Breakout techniques (chain-of-thought, LoRA, RLHF, Mamba) appeared on arXiv before any developer community discussion.

### Default Search Pattern (Run Weekly)

```bash
# Broad scan — all recent AI papers
python scripts/search_arxiv.py "" --days 7 --limit 30

# Targeted queries
python scripts/search_arxiv.py "agent" --days 7
python scripts/search_arxiv.py "reasoning" --days 7
python scripts/search_arxiv.py "alignment" --days 7 --categories cs.AI,cs.LG
```

### Web Fallback Queries

```
site:arxiv.org cs.AI OR cs.LG OR cs.CL after:[7d_ago]
```
```
arxiv "language model" OR "large language model" OR "foundation model" submitted:2025 after:[7d_ago]
```
```
paperswithcode.com "state of the art" AI after:[30d_ago]
```

### Auto-Qualify Rule (Single-Source Exception)

These paper types qualify as `[FRONTIER]` without requiring corroboration:
- Any paper from OpenAI, Anthropic, Google DeepMind, Meta AI, Mistral, xAI, Apple ML, Microsoft Research, EleutherAI, Allen Institute
- Papers where the author list matches `references/frontier_researchers.md` entries
- Papers that describe new architectures, new benchmarks, or SOTA claims in core areas (reasoning, agents, alignment, inference efficiency)

### Categories to Watch

| Category | Focus |
|----------|-------|
| `cs.AI` | Artificial intelligence (broadest, catches everything) |
| `cs.LG` | Machine learning (training methods, architectures, optimization) |
| `cs.CL` | Computation & language (NLP, LLMs, dialogue systems) |
| `cs.CV` | Computer vision (multimodal, image/video generation) |
| `cs.RO` | Robotics (embodied AI, robot learning) — add with `--categories` flag |

### What to Extract
- Paper title, first/last author, institutional affiliation
- Abstract — what's claimed, what's novel
- arXiv category (primary category signals research domain)
- Submission date (velocity matters — day-1 papers are frontier signal)
- GitHub repo link (often included in abstract or linked from arXiv page)
- Whether it implements or benchmarks against a known model

---

## Polymarket

> **MCP tools**: `polymarket`, any tool with "prediction" + "market"  
> **Script**: `scripts/search_polymarket.py "AI" --limit 20`  
> **Web fallback**: `site:polymarket.com` queries

### Why Polymarket Matters for AI Research
Real money on outcomes cuts through opinion. When Polymarket has AI-related markets, the odds represent informed consensus — not wishful thinking. Look for: AGI timeline markets, company milestone markets, regulation markets.

### Search Queries
```
site:polymarket.com AI OR "artificial intelligence" OR AGI OR OpenAI OR Google OR Anthropic
```

### API Alternative
Polymarket Gamma API (`gamma-api.polymarket.com`) — free, no auth.

### What to Extract
- Market question, current odds, trading volume
- Direction of movement (up/down over time period)
- Multiple outcomes if it's a multi-choice market

### Interpretation Priority
1. Structural/long-term markets > near-term deadline markets
2. Higher trading volume = more reliable signal
3. Always report specific odds AND direction of movement

---

## TikTok

> **MCP tools**: `tiktok`, `scrapecreators`, any tool with "tiktok" + "search"  
> **Script**: none (API requires paid access)  
> **Web fallback**: `site:tiktok.com` queries

### Why TikTok Matters for AI Research
TikTok is the mainstream adoption signal. When AI tools go viral on TikTok, it means they've crossed from developer niche to mass-market awareness. View counts indicate cultural penetration.

### Search Queries
```
site:tiktok.com AI tool OR AI app OR "ChatGPT" OR "AI generated" after:[30d_ago]
```

### What to Extract
- Creator handle, view count, like count
- Caption text and hashtags
- Whether it's a demo, tutorial, reaction, or native AI use

---

## Instagram

> **MCP tools**: `instagram`, `scrapecreators`, any tool with "instagram" + "search"  
> **Script**: none (API requires paid access)  
> **Web fallback**: `site:instagram.com` queries

### Why Instagram Matters for AI Research
Instagram signals AI adoption by creative professionals. When photographers, designers, and content creators post about AI tools, it indicates the tools have reached professional-grade usability.

### Search Queries
```
site:instagram.com AI art OR AI tool OR "AI generated" OR "made with AI" after:[30d_ago]
```

### What to Extract
- Creator handle, view count, like count
- Caption/description
- Whether it represents professional use or casual experimentation

---

## Bluesky

> **MCP tools**: `bluesky`, `bsky`, any tool with "bluesky" + "search"  
> **Script**: none (AT Protocol is free but requires more complex integration)  
> **Web fallback**: `site:bsky.app` queries

### Why Bluesky Matters for AI Research
Several prominent AI safety researchers and academics migrated from X to Bluesky. It's a smaller but higher-signal-density platform for nuanced AI discussion, particularly around safety, alignment, and ethics.

### Search Queries
```
site:bsky.app AI OR "language model" OR "machine learning" OR safety OR alignment after:[30d_ago]
```

### What to Extract
- Post text, author handle, like count
- Whether the author is a known researcher or institution

---

## Truth Social

> **MCP tools**: none known  
> **Script**: none (no public API)  
> **Web fallback**: `site:truthsocial.com` queries

### Why Truth Social Matters for AI Research
Truth Social is a narrow political-signal source. Relevant only when AI intersects with government policy, executive orders, regulation, or political debate.

### Search Queries
```
site:truthsocial.com "artificial intelligence" OR AI policy OR AI regulation after:[30d_ago]
```

### What to Extract
- Post text, author, engagement
- Policy positions or regulatory signals

---

## Web (General)

### Priority Sources for AI Web Research

| Source Type | Examples |
|---|---|
| Company blogs | openai.com/blog, anthropic.com/news, blog.google/technology/ai, ai.meta.com/blog |
| Trade press | VentureBeat AI, TechCrunch AI, The Verge AI, MIT Technology Review |
| Research hubs | arxiv.org (cs.AI, cs.LG, cs.CL), paperswithcode.com |
| Developer platforms | huggingface.co/blog, modal.com/blog, replicate.com/blog |
| Wire services | Reuters Technology, Bloomberg Technology |

### Search Queries
```
AI news OR announcement OR release OR breakthrough this month after:[30d_ago]
```
```
"AI model" OR "language model" release OR launch OR benchmark after:[30d_ago]
```
```
AI funding OR acquisition OR partnership OR investment after:[30d_ago]
```
```
AI regulation OR policy OR legislation OR executive order after:[30d_ago]
```
