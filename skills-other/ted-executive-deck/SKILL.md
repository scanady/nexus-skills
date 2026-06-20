---
name: ted-executive-deck
description: 'TED-Style Executive Deck skill. Use when transforming a technical initiative brief into a cinematic, TED-talk-style executive presentation rendered as a single self-contained HTML widget with a built-in slide navigator. Deck length is variable (7 slides minimum, up to 14 for multi-chapter initiatives) and sized to the content depth. Follows a structured narrative arc (positioning → hook → context → reframe → solution → investment → close), enforces one-idea-per-slide, applies layout variation as pacing, supports chapter color signals for template reuse, and uses 7 named slide templates. Tone is observational and forward — frames gaps as specific and resolvable. Triggers: ted deck, executive presentation, ted talk slides, cinematic deck, initiative brief, executive slide deck, steerco deck, board deck, executive storytelling, narrative arc deck, html slide deck, executive html presentation, variable length deck, multi-chapter deck.'
argument-hint: 'Provide the initiative brief using the USER PROMPT TEMPLATE below. Fill in: Initiative Name, Audience, Presenting To, Core Tension, Key Metrics, Proposal, Three Solution Pillars, Business Case (investment, benefit, payback, ROI, breakdown), and the 3-4 decisions needed. Optionally supply a brand accent hex color.'
---

# TED-Style Executive Deck

## Role Context

You are an expert presentation designer and executive storyteller. Your job is to transform a technical initiative brief into a cinematic, TED-talk-style slide deck rendered as a single self-contained HTML widget with a built-in slide navigator.

---

## Core Philosophy (Non-Negotiable)

| # | Principle | What it means |
|---|-----------|---------------|
| 1 | **One idea per slide** | If a slide has two points, it has one too many. Strip ruthlessly. |
| 2 | **Significance before setup** | Lead with the most concrete, consequential fact or number  -  before context or explanation. Make the audience understand *why this matters* before you explain *what it is*. |
| 3 | **Layout variation = pacing** | Each slide must use a visually distinct layout. No two consecutive slides share the same template. Cognitive reset = sustained attention. |
| 4 | **Narrative arc over information dump** | The deck follows a logical journey: **context -> insight -> resolution -> ask**. Frame the current state as a gap or opportunity, not a failure. The initiative is the path forward  -  not a verdict on the past. |
| 5 | **Closing affirms opening** | The final words must echo and affirm the opening statement. The close is the promise delivered  -  not a repeat of the problem. |

---

## Slide Template Library

You have exactly **7 slide templates**. Use each one at most once per deck. Select and sequence them to serve the narrative.

### TEMPLATE A  -  TITLE (dark, full-bleed, massive headline)
- **Background:** `#060E1A` (near-black navy)
- A thin colored left-border accent bar (6px, brand color)
- **Eyebrow label:** tiny, uppercase, brand color, `1.6cqw`
- **Main headline:** enormous, `7-8cqw`, white, max 5 words per line, 2-3 lines, one key word in brand color
- **Subhead:** `1.8cqw`, muted blue-gray, max 15 words, bottom-left anchored
- **Use for:** Slide 1 only  -  the positioning statement. A factual, specific claim about why this initiative is necessary. Observations, not accusations.
- **Implementation note:** The `.a-headline` element must use `display:flex; align-items:center` (not `flex-direction:column`). All headline text  -  including `<br>` tags  -  must be wrapped in a single `<span>` child element. Without the span, `<br>` tags become separate flex items and create unwanted gaps between lines.

### TEMPLATE B  -  SINGLE STAT (full-bleed brand color, one enormous number)
- **Background:** brand accent color (e.g. `#378ADD`). In a second chapter, use the chapter's accent color.
- **One number:** `24-28cqw`, white, centered, takes up ~60% of the slide
- **One-line label below:** `2.5-3cqw`, light tint of brand color
- **Two-line explanatory note:** `1.6cqw`, lighter tint, centered, max 20 words
- **Use for:** The most significant, concrete metric that makes the gap or opportunity undeniable. Can appear in any chapter  -  once per chapter maximum.

### TEMPLATE C  -  SPLIT PANEL (dark left block + numbered list right)
- **Left panel (40% width):** solid dark brand color block with section label + bold 2-line headline
- **Right panel (60% width):** dark background, 3-4 numbered items, each with a bold statement lead + supporting sentence
- **Numbers:** `3.5cqw`, brand color
- **Item text:** `1.7cqw`, muted; bold spans in white
- **Use for:** Enumerated context, constraints, or factors  -  specific and consequential. In later chapters, use for foundation layers, architecture sections, or any "4 things to know" narrative beat.

### TEMPLATE D  -  PULL QUOTE (white background, editorial, emotional)
- **Background:** white (`#fff`)
- **Oversized decorative quotation mark:** `14cqw`, lightest gray, positioned top-left behind text
- **Quote text:** `4-4.5cqw`, near-black, centered, max 25 words, key phrase in brand color
- **Attribution line:** `1.5cqw`, gray, uppercase, centered
- **Use for:** The reframe  -  the moment you want the audience to *feel* something, not just know something. **Write the quote yourself  -  do not quote anyone.**

### TEMPLATE E  -  THREE COLUMN (dark, bold headline above, equal columns below)
- **Background:** `#060E1A`
- Slide number + eyebrow label top-right
- **Large 2-line headline:** `5-6cqw`, white, one key word in brand color
- Three columns below, each with a colored top border (3 distinct accent colors)
- **Column header:** `1.9cqw`, white, font-weight 500
- **Column body:** `1.5cqw`, gray, 2-3 sentences max
- **Use for:** The solution  -  three pillars, workstreams, or principles

### TEMPLATE F  -  METRICS SPLIT (dark left with stats + colored right with bar chart)
- **Left panel:** dark background, eyebrow, 2-line headline, 2 large metrics (`4.5cqw` value + `1.6cqw` description)
- **Right panel:** a distinct dark-tinted accent color, 3-4 horizontal bar rows showing proportional breakdown
- **Bar labels:** `1.4cqw`, light tint
- **Bar tracks:** dark background, filled with accent color
- **Closing note:** `1.4cqw`, light, 2 lines
- **Use for:** The business case  -  ROI, payback, cost breakdown

### TEMPLATE G  -  BOLD CTA (full-bleed brand color, minimal, the close)
- **Background:** brand accent color
- **Tiny tag:** `1.6cqw`, light tint, uppercase
- **Giant headline:** `6-7cqw`, white, centered, 2 lines, bold imperative or affirmative callback phrase
- **Frosted box:** semi-transparent white border, the specific ask in `2-2.5cqw` white text + sub-line
- **Decision chips:** 3-4 small pill boxes in a row, one decision each, `1.5cqw`
- **Use for:** Final slide only  -  the close and the ask

---

## Narrative Structure Map

### Base Arc (7 slides  -  minimum viable deck)

For concise briefs, map to this 7-slide sequence:

| Slide | Template | Narrative Role | Content Source |
|-------|----------|----------------|----------------|
| 1 | A  -  Title | The positioning statement. A factual, specific claim about why this initiative is necessary. | Derive from the core tension in the brief |
| 2 | B  -  Single Stat | The hook. The one number that makes the gap or opportunity concrete. | The most significant metric in the brief |
| 3 | C  -  Split Panel | The problem or context. Four enumerated, specific factors. | Key constraints or pain points from the brief |
| 4 | D  -  Pull Quote | The reframe. One sentence that shifts perspective. **Write it yourself  -  never quote from the brief verbatim.** | Synthesize the insight |
| 5 | E  -  Three Column | The solution. Three named pillars (outcomes, not features). | The proposal |
| 6 | F  -  Metrics Split | The return. Two headline numbers + proportional breakdown. | ROI / investment / payback |
| 7 | G  -  Bold CTA | The ask. One crisp close + 3-4 decisions. | Decision requirements |

### Variable-Length Decks (8-14 slides)

For richer briefs where the material cannot be faithfully covered in 7 slides, the deck may be extended by **repeating templates in additional chapters**. A chapter is a new section of the narrative that requires its own template sequence.

**Rules for variable-length decks:**

| Rule | Requirement |
|------|-------------|
| **V-1: No consecutive repeats** | Never place the same template on two consecutive slides, even across chapters. |
| **V-2: Chapter color signal** | When a template repeats in a new chapter, apply a `.ch2` (or `.ch3`) CSS modifier class that changes the dominant accent color. Blueprint chapter 1 uses brand blue. Chapter 2 uses success green (`#1D9E75`). Chapter 3 uses amber (`#EF9F27`). |
| **V-3: Minimum chapter templates** | Each chapter should include at least 2 templates before repeating a template from an earlier chapter. |
| **V-4: G always closes** | Template G is always the final slide, regardless of deck length. |
| **V-5: One idea per slide** | Adding slides does not lower the one-idea-per-slide standard. More chapters = more slides, not more content per slide. |
| **V-6: Deck sizing guideline** | 7 slides = concise brief. 9-11 slides = medium-complexity initiative. 12-14 slides = full multi-chapter strategic narrative. Beyond 14: split into two separate decks. |

**Chapter color system:**
```css
/* Chapter 1 — Brand blue (default) */
.slide-b          { background: #378ADD; }
.slide-c .c-left  { background: #0C447C; }
.slide-d .d-quote em { color: #378ADD; }
.slide-e .e-tag   { color: #378ADD; }

/* Chapter 2 — Success green */
.slide-b.ch2          { background: #1D9E75; }
.slide-c.ch2 .c-left  { background: #073B2F; }
.slide-d.ch2 .d-quote em { color: #1D9E75; }
.slide-e.ch2 .e-tag   { color: #1D9E75; }

/* Chapter 3 — Amber */
.slide-b.ch3          { background: #B45309; }
.slide-c.ch3 .c-left  { background: #3B1F00; }
.slide-d.ch3 .d-quote em { color: #EF9F27; }
.slide-e.ch3 .e-tag   { color: #EF9F27; }
```

**Example 11-slide sequence for a multi-chapter initiative:**

| # | Template | Chapter | Role |
|---|----------|---------|------|
| 1 | A |  -  | Positioning statement |
| 2 | B ch1 | 1 | Hook stat |
| 3 | C ch1 | 1 | Context / differentiators |
| 4 | D ch1 | 1 | Reframe |
| 5 | E ch1 | 1 | Principles / approach |
| 6 | F | 1 | Investment / platform map |
| 7 | C ch2 | 2 | Foundation layers |
| 8 | E ch2 | 2 | Validation strategy |
| 9 | B ch2 | 2 | Chapter 2 hook stat |
| 10 | D ch2 | 2 | Chapter 2 reframe |
| 11 | G |  -  | The close and ask |

---

## Technical Implementation Rules

1. **Generate a single self-contained HTML fragment**  -  no `<html>`, `<head>`, or `<body>` tags.

2. **Structure:**
   ```
   <style> ... </style>
   [slide deck HTML]
   <script> ... </script>
   ```

3. **Slide container:**
   - Outer frame: `width: 100%; aspect-ratio: 16/9`  -  all slides are 16:9
   - All slides stacked with `position: absolute; display: none`  -  only `.active` slide shows
   - Navigator below: Prev button &middot; dot indicators &middot; slide label + count &middot; Next button

4. **Typography  -  use container query units (`cqw`) for ALL text inside slides:**
   - Headlines: `5-8cqw` &nbsp; Stats: `14-28cqw` &nbsp; Body copy: `1.5-2cqw` &nbsp; Labels: `1.3-1.6cqw`
   - **Never use `px` for font sizes inside `.slide` elements**

5. **Color system:**
   ```
   Primary dark background:  #060E1A
   Brand blue (primary):     #378ADD
   Brand blue dark:          #0C447C
   Brand blue mid:           #185FA5
   Brand blue light:         #85B7EB  #B5D4F4  #E6F1FB
   Success green:            #1D9E75  #9FE1CB
   Amber:                    #EF9F27
   Gray text:                #888780  #444441
   White:                    #fff
   ```

6. **Navigator:**
   - Prev / Next buttons: styled with CSS variable borders, hover states
   - Dot indicators: 6px circles, active dot scales up and uses `var(--color-text-primary)`
   - Slide label shows current slide name + "N of [total]" where total is the actual deck length
   - Use plain JS  -  no libraries
   - For decks &gt;10 slides, allow dots to `flex-wrap` so they remain legible

7. **Dark mode:** All non-slide UI (navigator, wrapper) must use CSS variables (`var(--color-text-primary)`, `var(--color-border-secondary)`, etc.) so it adapts to the host theme. Slide interiors use hardcoded hex because they are intentionally opaque presentation surfaces.

---

## Character Encoding Rules

These apply to all HTML output. See the `html-presentation-maker` skill for the full entity table. Key rules:

- Always use HTML entities for special characters  -  never paste raw Unicode into HTML source
- Em dash: ` - ` &nbsp; En dash: `-` &nbsp; Right arrow: `->` &nbsp; Middle dot: `&middot;`
- CSS `content:` properties use unicode escapes: `'\2014'` (em dash), `'\25C6'` (diamond)

---

## User Prompt Template

Use this to invoke the skill. Fill in every bracketed section:

```
Create a TED-style executive slide deck for the following initiative:

INITIATIVE NAME: [e.g. "Unified Data Platform — Phase 1"]
AUDIENCE: [e.g. "Executive Leadership Team — CTO, CFO, Chief Data Officer"]
PRESENTING TO: [e.g. "Q2 2025 SteerCo"]

THE CONTEXT (what the current state is and why it matters):
[2-4 sentences. Be specific and factual - describe the gap or opportunity without framing it as organizational failure. Include numbers where available.]

KEY METRICS / NUMBERS:
- Most significant stat: [e.g. "40% of campaign reports require engineering to produce"]
- Opportunity or cost figure: [e.g. "$3.4M in addressable inefficiency"]
- Other supporting numbers: [list any relevant figures]

THE PROPOSAL (what you are asking them to approve):
[2-4 sentences. What specifically will be built or done?]

THREE SOLUTION PILLARS (name three outcomes, not features):
1. [e.g. "Unify — one source of truth across all data"]
2. [e.g. "Govern — audit-ready lineage and quality"]
3. [e.g. "Activate — self-serve intelligence for 200+ users"]

THE BUSINESS CASE:
- Investment ask: [e.g. "$2.4M over 18 months"]
- Total 3-year benefit: [e.g. "$7.1M"]
- Payback period: [e.g. "16 months"]
- ROI: [e.g. "196%"]
- Benefit breakdown: [e.g. "62% OpEx savings / 24% revenue uplift / 14% risk avoidance"]

THE ASK — decisions needed in this meeting:
1. [e.g. "Approve $2.4M Phase 1 budget"]
2. [e.g. "Designate executive sponsor"]
3. [e.g. "Authorize vendor negotiations"]
4. [e.g. "Approve 4 FTE data engineering hires"]

BRAND ACCENT COLOR (optional, hex): [default: #378ADD]

OUTPUT: A single self-contained HTML fragment. No prose explanation. Just the code.
```

---

## Pre-Output Quality Checklist

Before finalizing any output, verify every item:

| # | Check | Pass criteria |
|---|-------|---------------|
| 1 | Slide 1 headline is a **positioning statement** | Factual, specific, and consequential  -  not a project name, not hostile. Frame as an observation, not an accusation. |
| 2 | Slide 2 stat is **concrete and significant** | Minimum `24cqw` font size. The number must be specific and directly relevant to the initiative. |
| 3 | **No two consecutive slides share** template type, regardless of chapter | Verify every adjacent pair in the full deck |
| 4 | All pull quotes are **agent-written** | Not lifted verbatim from any brief section  -  synthesized insight that shifts perspective |
| 5 | Solution pillar names are **outcome words** | "Unify" not "Data consolidation"  -  active verbs or strong nouns that name end states |
| 6 | Final slide headline **callbacks Slide 1** | The closing affirms the opening. Affirmative, not imperative. |
| 7 | **Tone throughout**: observational, not accusatory | Frame gaps as specific and resolvable. Frame the initiative as forward motion, not organizational criticism. |
| 8 | **Deck length matches content depth** | 7 slides for a focused brief. 9-11 for a multi-chapter initiative. Never pad; never compress at the cost of meaning. |
| 9 | **Chapter color signals applied** when templates repeat | `.ch2` class on every repeated-template slide; never same `.ch` class on two consecutive slides |
| 10 | All font sizes inside `.slide` use **`cqw` units** | Zero `px` font sizes inside any `.slide` element |
| 11 | Navigator uses **CSS variables** | `var(--color-fg-default)`, `var(--color-border-default)`, etc. for all non-slide UI |
| 12 | **`aspect-ratio: 16/9`** on the slide frame | Present on the outer slide container |
| 13 | JS navigator is **fully functional** | Dots, prev/next, slide label all work correctly at the actual deck length |
| 14 | **Zero external dependencies** | No CDN links, no `<script src>`, no `<link rel="stylesheet">` pointing outward |
| 15 | Proper **HTML entities** used | No raw Unicode special characters in HTML source |
