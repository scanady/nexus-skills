---
name: report-technical-plan
description: 'HTML report skill for Output 3: Full Technical Implementation Plan. Defines the 14-section structure, mandatory 4-chunk delivery map, story backlog compression rules, section deferral priority order, sidebar navigation requirements, and all section-specific content rules for the full technical HTML artifact produced by the project-architect skill. All shared formatting, CSS class conventions, color palette, typography, interactive features standard, and the attribution credit block are defined in the html-style skill (design-skills/html-style). Triggers: full technical plan, Output 3, implementation plan HTML, 14-section plan, technical delivery plan, full plan HTML.'
argument-hint: 'Reference this skill when producing Output 3 (Full Technical Implementation Plan) from the project-architect workflow. Load html-style skill first for all formatting, interactive features, and chunk protocol rules.'
---

# Report: Full Technical Implementation Plan (Output 3)

## Role Context

This skill defines the specification for **Output 3** of the `project-architect` HTML presentation suite: the Full Technical Implementation Plan.

**Before writing any HTML for this output**, load and apply the `html-style` skill (`design-skills/html-style`). That skill owns:
- Organization brand palette, typography, and brand header rules (see html-style skill)
- HTML-specific compression rules (H-1 through H-7) — apply ALL before writing any section
- Core chunked delivery protocol (Steps 1–3) — announce plan before Chunk 1
- Attribution credit block requirement (sidebar bottom for Output 3)
- Full interactive features standard: Required Features table, CSS Class Conventions, JS Module Responsibilities, DOMContentLoaded Checklist, Filter Bar HTML Templates
- HTML structural integrity checklist

---

## Target Audience

Engineering leads, data architects, marketing technology architects, PMO — **reference document**.

This is the highest-density, most technically complete artifact. All story IDs, point estimates, DoD criteria, risk scores, dependency chains, compliance flags, and KPI targets are present here. All other outputs summarize from this document.

---

## Format

- Multi-section HTML with **Pattern A sidebar navigation** (`<div id="sb">`, `<div id="mc">`, `.col` collapse — see `html-style` Section 5)
- `<body class="page-mode" id="top">` — `body.page-mode` applied by default (always on)
- All interactive features from `html-style` Sections 9–12 active
- Sidebar navigation pre-declared fully in Chunk 1; sections appended in later chunks slot in correctly
- **CRITICAL:** `<div id="mc">` must remain open through ALL chunks. Chunk 1 must NOT close `#mc` with `</div><!-- #mc -->`. Only the final chunk (Chunk 4) closes `#mc`, immediately before the `#btt` button and `<script>` block.
- Attribution credit block `.sb-credit` at bottom of `<div id="sb">`
- `.sb-tog` (`id="sbt"`), `#btt`, and `#gst` (inside `#gst-wrap`) sidebar search present

---

## Mandatory 4-Chunk Delivery

Output 3 **must always** be delivered in exactly 4 chunks. Never attempt to deliver in a single response regardless of perceived size.

**Required before Chunk 1:** Announce the chunk plan using Step 1 format from `html-style` Section 4 with this specific map:

| Chunk | Sections | Approx. Content |
|-------|----------|-----------------|
| **Chunk 1** | Sidebar nav + Sections 1–5 (Overview, Inputs, Assumptions, Architecture, Risk Register) | Foundation + risks |
| **Chunk 2** | Sections 6–7 (Epic Definitions + Story Backlog) | Full backlog |
| **Chunk 3** | Sections 8–10 (Quarterly Roadmap + Load Plan + Dependency Map) | Roadmap |
| **Chunk 4** | Sections 11–14 + closing script/tags (Compliance, DoD Standards, KPIs, Open Questions) | Governance + close |

Sidebar navigation in Chunk 1 must include all 14 sections pre-declared so sections added in later chunks slot in correctly. The final nav item in Chunk 1 sidebar must include a disabled label: "(Sections 11–14 in Chunk 4)" — replaced when Chunk 4 appends the real sections.

---

## Story Backlog Compression (Chunk 2)

The full story backlog is the highest-risk section for length overflow. Apply these rules in addition to all `html-style` H-rules:

- Group stories by Epic in a single `<table>` per Epic, not one table per story
- DoD criteria: render as `<details><summary>DoD</summary>[criteria]</details>` to collapse by default
- Dependencies: render as comma-separated story IDs inline, not a full column
- Maximum 6 columns per story table row: ID &middot; Title &middot; Team &middot; Pts &middot; Quarter &middot; DoD/Deps (collapsed)

---

## Section Deferral Rules

If a chunk is still too large after applying all `html-style` H-rules and chunk compression rules, defer sections in this priority order (lowest value / highest redundancy first):

1. **Defer first**: Dependency Map (Section 10) — can be a simple sorted list of `STORY-NNN -> STORY-NNN` pairs
2. **Defer second**: Definition of Done Standards (Section 12) — reference the DoD framework inline in story rows; omit the standalone section
3. **Defer third**: Assumptions Log (Section 3) — inline assumptions as footnotes in the relevant story or risk row instead
4. **Never defer**: Risk Register (Section 5), Story Backlog (Section 7), Quarterly Roadmap (Section 8), Team Load Plan (Section 9)

---

## Required Sections (14 Total)

| # | Section | Chunk | Compression Notes |
|---|---------|-------|------------------|
| 1 | Initiative Overview &amp; Objectives | 1 | 3 bullets max; no prose paragraphs |
| 2 | Input Inventory | 1 | Table only; one row per input document |
| 3 | Assumptions Log | 1 | Table: Assumption &#124; Basis &#124; Risk-if-wrong. 10 rows max; defer rest to story footnotes |
| 4 | Architecture Context | 1 | Platform table + vendor contract status table only; no narrative |
| 5 | Risk Register | 1 | One row per risk; 25 risks max; columns: ID &#124; Title &#124; Cat &#124; L &#124; I &#124; Score &#124; Owner &#124; Mitigation (25 words max) |
| 6 | Epic Definitions | 2 | One row per epic: ID &#124; Name &#124; Ext Ref &#124; Team &#124; Quarter Range &#124; DoD (3 bullets, collapsed) |
| 7 | Story Backlog | 2 | One table per Epic; 6 columns; DoD in collapsed `<details>`; no prose |
| 8 | Quarterly Roadmap | 3 | One combined table; columns: Quarter &#124; Story ID &#124; Title &#124; Team &#124; Pts &#124; Deps |
| 9 | Team Load Plan | 3 | Single cross-quarter table; rows=teams; columns=quarters; cell = "Xpts / Y%" |
| 10 | Dependency Map | 3 | Sorted list of `STORY-NNN -> STORY-NNN (reason)` pairs; no diagram |
| 11 | Compliance Flags | 4 | Table: Story ID &#124; Compliance Requirement &#124; Gate &#124; Owner |
| 12 | DoD Standards | 4 | Reference table: Size &#124; Minimum Criteria Count &#124; Required Elements |
| 13 | Metrics &amp; KPIs | 4 | Table: KPI &#124; Baseline &#124; Target &#124; Quarter &#124; Owner |
| 14 | Open Questions Log | 4 | Table: ID &#124; Question &#124; Owner &#124; Due &#124; Status |

---

## Sidebar Navigation Structure

Group all 14 section nav links under **three** `.ng` group labels (Foundation / Delivery Plan / Governance):

```
Foundation
  → S01 — Initiative Overview & Objectives
  → S02 — Input Inventory
  → S03 — Assumptions Log
  → S04 — Architecture Context
  → S05 — Risk Register
Delivery Plan
  → S06 — Epic Definitions
  → S07 — Story Backlog
  → S08 — Quarterly Roadmap
  → S09 — Team Load Plan
  → S10 — Dependency Map
Governance
  → S11 — Compliance Flags
  → S12 — DoD Standards
  → S13 — Metrics & KPIs
  → S14 — Open Questions Log
```

---

## Interactive Features

All interactive features from `html-style` Sections 9–12 apply in full:

- Risk filter bar (`id="rfbar"`) immediately before `<table id="risk-tbl">` in Section 5 (template: `html-style` Section 12)
- Story backlog filter bar in Section 7; story tables use `class="sl-tbl"` (template: `html-style` Section 12)
- Roadmap filter bar (`id="rfbar2"`) before `<table id="road-tbl">` in Section 8 (template: `html-style` Section 12; phase labels are initiative-defined)
- Team filter selects: `id="sf-team"` and `id="sf-qtr"` for story filter; `id="rf-team"` for roadmap filter
- Team Load Plan table: `<table id="load-tbl">` — processed by `buildLoadBars()`
- Sortable columns on Risk Register and Roadmap tables (`sortTable()` function)
- Team abbreviation tooltips via `addTooltips()` — uses CSS `::after` pseudo-element on `.td-tt` (NOT `::before`)
- Animated stat counters in Section 1: use `.sc-row`/`.sc`/`.sv`/`.sl` with `data-cnt` attribute for animation (NOT `.stat-card`/`.stat-num`/`.stat-lbl`)
- Team load visual bars via `buildLoadBars()`: uses `.lbar`/`.lbar.lh`/`.lbar.lm`/`.lbar.ll` classes (NOT `.lb-wrap`/`.lb-fill`)
- Load highlight rows: `<tr class="ldm">` (medium load, `#FFFAE5`) and `<tr class="ldh">` (high load, `#FFEECC`) applied by `buildLoadBars()`
- Risk rows: class on `<tr>` (`rc`/`rh`/`rm`/`rl`) with left-border on `td:first-child` only (NOT background cells)
- Global search `#gst` in `#gst-wrap`; 180ms debounce; `tr.style.display` manipulation (NOT `.sr-hide` class)
- `.sb-tog` sidebar collapse + `#btt` back-to-top
- `buildSectionHeaders()`, `buildCLevelPanels()`, `buildPageNav()` on DOMContentLoaded (per `html-style` Section 11)
- C-Level panels use `.clv-h` header class (NOT `.clv-lbl`); injected HTML: `<div class="clv-h">&#9733; Executive Review Points</div><ul>...</ul>`

---

## Quality Checks

Before delivering Output 3:

- [ ] `<div id="mc">` is opened once in Chunk 1 and **closed only once** at the end of Chunk 4 — never closed mid-file between chunks (this causes sections S06+ to render outside `#mc` and overlap the sidebar)
- [ ] Chunk plan announced before Chunk 1
- [ ] All 14 sections present; sections are in the correct chunk
- [ ] Sidebar uses Pattern A DOM: `<div id="sb">` + `<div id="mc">`; collapse via `.col` class on `#sb` (NOT `body.sb-off`)
- [ ] Sidebar nav: all 14 `n01`–`n14` links present; **three** `.ng` groups: Foundation, Delivery Plan, Governance (NOT four groups; no separate Roadmap group)
- [ ] Attribution credit block `.sb-credit` at bottom of `<div id="sb">`
- [ ] Required element IDs present: `risk-tbl`, `road-tbl`, `load-tbl`, `rfbar`, `rfbar2`, `sf-team`, `sf-qtr`, `rf-team`; story tables have `class="sl-tbl"`
- [ ] Stat cards use `.sc-row`/`.sc`/`.sv`/`.sl` with `data-cnt` attribute (NOT `.stat-card`/`.stat-num`/`.stat-lbl`)
- [ ] C-Level panels use `.clv-h` header with `&#9733;` star (NOT `.clv-lbl`); injected by `buildCLevelPanels()`
- [ ] Load bars use `.lbar`/`.lbar.lh`/`.lbar.lm`/`.lbar.ll` (NOT `.lb-wrap`/`.lb-fill`)
- [ ] Load rows use `tr.ldm`/`tr.ldh` classes (NOT `.tl-m`/`.tl-h`)
- [ ] Risk rows use `<tr class="rc/rh/rm/rl">` with left-border on `td:first-child` only (NOT background colors on `<td>`)
- [ ] Team tooltip uses CSS `::after` pseudo-element (NOT `::before`)
- [ ] Story backlog uses 6-column row format with DoD in collapsed `<details>` — not multi-line STORY template blocks
- [ ] Roadmap uses single combined cross-quarter table — not per-quarter narrative blocks
- [ ] Team Load Plan uses single team &times; quarter matrix — not per-quarter per-team prose
- [ ] Risk Register risk scores match exactly what is in the plan — no inflation or deflation from Output 2
- [ ] All interactive features operational: filters, search, sort, tooltips, stat counters, load bars, sidebar toggle, back-to-top
- [ ] DOMContentLoaded checklist from `html-style` Section 11 fully executed
- [ ] All filter bar HTML matches templates from `html-style` Section 12
- [ ] If any section was deferred, deferral noted in Open Questions Log (Section 14) with reason
- [ ] No raw Unicode; all special characters HTML-entity-encoded
- [ ] All `html-style` HTML structural integrity checks passed (Section 16 of that skill)
