# Output Format Templates

Templates for three depth levels. Choose based on user preference or default to Standard.

---

## Standard Format (Default)

```markdown
# 🔬 AI Landscape Intelligence Brief

**Period**: [Start Date] – [End Date] (last 30 days)
**Platforms Searched**: GitHub Trending, arXiv, GitHub, Reddit, X, TikTok, Instagram, Hacker News, Polymarket, Bluesky, Truth Social, Web
**Sources Reviewed**: [N] items across [N] platforms
**Generated**: [Current Date]
**Time Windows**: ⚡ This Week ([7d count] items) · 📅 This Month ([14–30d count] items) · 🔭 Horizon ([FRONTIER count] items)

---

## Executive Summary

[5–8 sentences. Lead with the 3–5 most significant developments of the period. State what happened, what it means, and who should care. Written for a busy CTO/founder who will read only this section if short on time. Explicitly call out if any `[FRONTIER]` items have emerged that deserve attention before they're widely covered.]

---

## 🔗 Cross-Platform Highlights

Stories corroborated across 3+ platforms — the strongest signals in this research.

### [Headline 1] `[GitHub + Reddit + X + HN]` `[7d]`

**What happened**: [2–3 sentence overview]

**Why it matters**: [1–2 sentences on strategic significance]

**The conversation**: [What are practitioners actually saying? Quote a top Reddit comment or X post directly.]

📊 **Signal**: [Engagement summary — e.g., "2.4K upvotes on r/LocalLLaMA, 8K likes on X, trending #3 on GitHub"]
🎯 **Applicability**: [Who should pay attention and what to consider doing]

---

### [Headline 2] `[Reddit + X + YouTube]` `[14–30d]`

[Same structure]

---

## ⚡ This Week — High-Velocity Signals

*Items from the last 7 days with high star velocity, fresh lab releases, or emerging community traction. Lower corroboration bar — flag `[FRONTIER]` items that haven't yet spread across platforms.*

### [Headline] `[FRONTIER]` or `[GitHub]`

**What happened**: [2–3 sentences]

**Why flag it now**: [Why this is worth surfacing before corroboration — star velocity, known researcher, major lab, HN breakout]

**Star velocity**: [N] stars/day (total: [N] stars, created [N] days ago) *— or —* Appearing on GitHub trending daily view

⚠️ **Corroboration**: Single source — watch for Reddit / X / HN follow-up in next 7 days

---

## 🔭 Horizon — Preprints & Early Signals

*arXiv papers, known-researcher repos, and early-stage tools not yet widely covered. These are tomorrow's stories — include without requiring cross-platform confirmation.*

### [Paper Title] `[FRONTIER]` `[arxiv]`

**Authors**: [Author list — note institutional affiliation]
**Categories**: [cs.AI / cs.LG / etc.]
**Submitted**: [Date]

**What it claims**: [1–2 sentences on the core contribution or result]

**Why it matters**: [Strategic or technical significance — what does this enable or threaten?]

**Watch for**: GitHub implementation, community discussion on r/MachineLearning or HN

---

## [Category Emoji] [Category Name]

### [Headline] `[7d]` or `[14–30d]`

**Summary**: [One-sentence overview]

**Key Points**:
- [Detail 1]
- [Detail 2]
- [Detail 3]

**Impact**: [Scope] | [Magnitude: Incremental / Notable / Major / Paradigm shift]
**Source**: [Platform attribution — per @handle, per r/subreddit, per channel name]
**Applicability**: [What practitioners should consider doing in response]

---

[Repeat for each finding within the category]

---

[Repeat for each category — typically 4–7 categories]

---

## 🔮 Signals & Trend Analysis

### Themes Gaining Momentum
- **[Theme 1]**: [Description + supporting evidence across platforms]
- **[Theme 2]**: [Description + supporting evidence]
- **[Theme 3]**: [Description + supporting evidence]

### Prediction Markets
- [Market question]: [Odds]% ([direction] [amount]% this month) — per Polymarket
- [Market question]: [Odds]% — per Polymarket

### Community Sentiment Snapshot
- **Excitement about**: [What has developers/practitioners most energized]
- **Skepticism about**: [What the community is pushing back on]
- **Watching closely**: [What people are waiting to see unfold]

---

## 🎯 Strategic Takeaways

1. **[Finding]** — [What to consider doing about it]
2. **[Finding]** — [What to consider doing about it]
3. **[Finding]** — [What to consider doing about it]
4. **[Finding]** — [What to consider doing about it]
5. **[Finding]** — [What to consider doing about it]

---

[STATS BLOCK — see SKILL.md for format]

---

[FOLLOW-UP INVITATION — see SKILL.md for format]
```

---

## Brief Format (Headlines Only)

Use when user requests "just the headlines" or "quick version."

```markdown
# 🔬 AI Landscape Brief — Headlines

**Period**: [Start Date] – [End Date]
**Generated**: [Current Date]

## Executive Summary

[3–5 sentences. The absolute essentials.]

---

## Top Stories

### Cross-Platform (3+ sources)
• [Headline 1] `[platforms]` — [one-line summary]
• [Headline 2] `[platforms]` — [one-line summary]

### [Category 1]
• [Headline] — [one-line summary] (per @source)
• [Headline] — [one-line summary] (per @source)

### [Category 2]
• [Headline] — [one-line summary] (per @source)
• [Headline] — [one-line summary] (per @source)

[Repeat for each category]

---

## Quick Takeaways

1. [Takeaway — 1 sentence]
2. [Takeaway — 1 sentence]
3. [Takeaway — 1 sentence]

---

[STATS BLOCK]
```

---

## Deep Format (Strategic Analysis)

Use when user requests "deep analysis", "strategic", or "full report."

```markdown
# 🔬 AI Landscape Intelligence Report — Deep Analysis

**Period**: [Start Date] – [End Date]
**Platforms Searched**: GitHub, Reddit, X, YouTube, TikTok, Instagram, Hacker News, Polymarket, Bluesky, Truth Social, Web
**Sources Reviewed**: [N] items across [N] platforms
**Depth**: Strategic analysis with forward-looking assessment
**Generated**: [Current Date]

---

## Executive Summary

[8–12 sentences. Comprehensive overview covering: most significant developments, dominant narrative of the period, key shifts in the competitive landscape, and a forward-looking statement. Written for a board-level audience.]

---

## 🔗 Cross-Platform Highlights

[Same structure as Standard, but with expanded analysis sections]

### [Headline] `[platforms]`

**What happened**: [3–5 sentence detailed overview]

**Strategic analysis**: [3–5 sentences. Who wins, who loses? What does this change about the competitive landscape? What second-order effects should we expect?]

**The conversation**: [Expanded — quotes from multiple platforms, noting differences in sentiment between platforms]

**Applicability by audience**:
- **For builders**: [What developers should consider]
- **For enterprises**: [What enterprise teams should evaluate]
- **For investors**: [What funding/market signals to note]

---

## [Category sections — same as Standard but with expanded analysis per item]

---

## 📈 Deep Trend Analysis

### Dominant Narratives This Period
- **[Narrative 1]**: [Extended description — what happened, evidence across platforms, why it's the dominant theme]
- **[Narrative 2]**: [Extended description]

### Competitive Landscape Shifts
| Dimension | 30 Days Ago | Now | Direction |
|-----------|-------------|-----|-----------|
| [e.g., Top open model] | [Previous leader] | [Current leader] | [Arrow] |
| [e.g., Agent framework] | [Previous status] | [Current status] | [Arrow] |
| [e.g., Regulation] | [Previous status] | [Current status] | [Arrow] |

### Prediction Markets Deep Dive
| Market | Current Odds | 30-Day Movement | Volume | Interpretation |
|--------|-------------|-----------------|--------|----------------|
| [Market 1] | [X]% | [+/-Y]% | [Volume] | [What this tells us] |
| [Market 2] | [X]% | [+/-Y]% | [Volume] | [What this tells us] |

### Signals to Watch Next 30 Days
- **[Signal 1]**: [What to watch for + what it would mean if confirmed]
- **[Signal 2]**: [What to watch for + what it would mean if confirmed]
- **[Signal 3]**: [What to watch for + what it would mean if confirmed]

### What's Notably Absent
[Topics or themes with surprisingly little activity — and what the silence might indicate]

---

## 🎯 Strategic Recommendations

1. **[Finding]** — [Detailed recommendation: what to do, why, and by when]
2. **[Finding]** — [Detailed recommendation]
3. **[Finding]** — [Detailed recommendation]
4. **[Finding]** — [Detailed recommendation]
5. **[Finding]** — [Detailed recommendation]
6. **[Finding]** — [Detailed recommendation]
7. **[Finding]** — [Detailed recommendation]

---

## Methodology & Limitations

- **Platforms searched**: [List all platforms and number of queries per platform]
- **Date range**: [Exact dates]
- **Known gaps**: [Any platforms that returned limited results, paywalled sources, geographic blind spots]
- **Confidence**: [Overall assessment of research completeness]

---

[STATS BLOCK]

---

[FOLLOW-UP INVITATION]
```
