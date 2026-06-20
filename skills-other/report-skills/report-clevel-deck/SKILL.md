---
name: report-clevel-deck
description: 'HTML report skill for Output 2: C-Level 3-Page Overview. Defines the target audience, three required sections (Why This Initiative, What We Will Build, How We Deliver), sidebar navigation layout, and delivery protocol for the C-Level HTML artifact produced by the project-architect skill. All formatting, CSS class conventions, color palette, typography, interactive features, and the attribution credit block are defined in the html-style skill (design-skills/html-style). Triggers: C-Level overview, 3-page deck, CTO deck, CMO deck, CFO summary, Output 2, executive HTML deck.'
argument-hint: 'Reference this skill when producing Output 2 (C-Level 3-Page Overview) from the project-architect workflow. Load html-style skill first for all formatting rules.'
---

# Report: C-Level 3-Page Overview (Output 2)

## Role Context

This skill defines the specification for **Output 2** of the `project-architect` HTML presentation suite: the C-Level 3-Page Overview.

**Before writing any HTML for this output**, load and apply the `html-style` skill (`design-skills/html-style`). That skill owns:
- Organization brand palette, typography, and brand header rules (see html-style skill)
- HTML-specific compression rules (H-1 through H-7)
- Core chunked delivery protocol (Steps 1–3)
- Attribution credit block requirement and placement (sidebar bottom for Output 2)
- Interactive CSS class conventions and JS module responsibilities
- HTML structural integrity checklist

---

## Target Audience

CTO, CIO, CMO, CFO, CRO — **5-minute read**.

This output bridges the 60-second executive overview (Output 1) and the full technical plan (Output 3). It provides business case, architectural scope, and delivery plan without exposing story IDs, point counts, or DoD criteria.

---

## Format

- 3-section HTML with **Pattern B sidebar navigation** (`<nav id="sb">` + `body.sb-off` collapse — see `html-style` Section 5)
- Main content in `<div id="main">` (NOT `#mc`)
- **No `body.page-mode`** — sections are pre-built in static HTML; first `.sec` has `pg-act` pre-applied in HTML markup; `go()` removes/adds `pg-act` class directly on sections
- **No `buildSectionHeaders()`, `buildCLevelPanels()`, or `buildPageNav()`** — all section content including `.pg-hdr` and `.clv` panels are hardcoded in HTML (not JS-injected)
- Section page header `.pg-hdr` uses Pattern B structure hardcoded in each section: `.ph-top`/`.ph-grp`/`.ph-num` / `.ph-title` / `.ph-ov` (see `html-style` Section 6)
- `.clv` C-Level review panel uses `.clv-lbl` variant with `::before` horizontal rule — hardcoded in HTML, NOT injected (see `html-style` Section 7)
- `gSearch()` uses `classList.toggle('sr-hide', ...)` on rows — NOT `style.display`
- `sbToggle()` toggles `document.body.classList.toggle('sb-off')` (Pattern B)
- No DOMContentLoaded block — bare `window.addEventListener('scroll',...)` + `document.getElementById('n01').classList.add('act')`
- Attribution credit block `.sb-credit` at bottom of `<nav id="sb">` (per `html-style` Section 2)
- `.sb-tog`, `#btt`, `#gst` sidebar search present

---

## Required Sections

Produce all three sections in this exact order:

### Section 1 — Why This Initiative (Business Case)

| Subsection | Content Rules |
|------------|---------------|
| Current state pain points | Quantified where possible; use a table or 3–5 bullets; no prose paragraphs |
| Strategic alignment | Link to organization objectives; cite specific goals by name |
| Expected business outcomes | Target metrics with baseline vs. target format; at least one KPI per outcome |
| Total cost of inaction | One paragraph or a 2-row comparison table: cost of doing nothing vs. cost of initiative |

### Section 2 — What We Will Build (Scope &amp; Architecture)

| Subsection | Content Rules |
|------------|---------------|
| Capability map | 2-column table: Today / Future; one row per capability area; no story IDs |
| Architecture diagram or capability table | Platform registry table or ASCII-art capability diagram; list platforms with current vs. future status |
| Phase-by-phase value delivery | Quarter-by-quarter narrative; one paragraph per phase; no point estimates |
| Key platform and technology decisions | Bullet list of 3–5 decisions that C-Level audience may need to ratify |

### Section 3 — How We Deliver (Delivery Plan &amp; Risks)

| Subsection | Content Rules |
|------------|---------------|
| Quarterly roadmap summary table | One row per quarter: Phase / Theme / Key Deliverables / Teams Involved; no story IDs or point counts |
| Team resource allocation summary | Table: Team / Role / Quarters Active / Capacity Risk (Y/N) |
| Top 5 risks with mitigations | Source exactly from Risk Register; show Rating + Mitigation; no score inflation or deflation |
| Governance and reporting cadence | Who reports to whom, at what cadence, on what artifacts |
| Decisions required from C-Level audience | Numbered list; each decision is one sentence; include consequence of non-decision |

---

## Chunked Delivery

Output 2 is typically deliverable in **a single response** given its 3-section scope and C-Level density rules (no story IDs, no point counts, prose-allowed).

If unusually long:
- Apply all `html-style` compression rules (H-1 through H-7) first
- Use core chunk protocol (Steps 1–3 from `html-style` Section 4)
- Announce the chunk plan before Chunk 1

---

## Quality Checks

Before delivering Output 2:

- [ ] All three sections present in the correct order with all required subsections
- [ ] No story IDs (STORY-NNN), point estimates, or DoD criteria visible in this output
- [ ] Risk ratings in Section 3 exactly match the scored Risk Register  -  no rating changes between outputs
- [ ] Quarterly roadmap in Section 3 uses consistent phase labels matching all other HTML outputs
- [ ] Architecture summary in Section 2 accurately represents the platform registry  -  no platforms added or removed from the Technical Plan
- [ ] Decisions list in Section 3 is actionable (each item states exactly what decision, by whom, by when)
- [ ] Pattern B sidebar used: `<nav id="sb">` with `.logo`, `.sb-search`, `.ng` groups, `<a>` links, `.sb-credit`
- [ ] Main content in `<div id="main">` (NOT `#mc`)
- [ ] No `body.page-mode` class — first `.sec` has `class="sec pg-act"` pre-applied in HTML
- [ ] `.pg-hdr` section page headers hardcoded in all three sections using `.ph-top`/`.ph-grp`/`.ph-num`/`.ph-title`/`.ph-ov` structure (Pattern B)
- [ ] `.clv` panels hardcoded in all three sections using `.clv-lbl` variant (with `::before` rule) — NOT `.clv-h`
- [ ] `gSearch()` uses `classList.toggle('sr-hide', ...)` — no `style.display` manipulation
- [ ] `sbToggle()` toggles `body.sb-off` (NOT `.col` class on `#sb`)
- [ ] No DOMContentLoaded block — bare scroll handler and `n01.classList.add('act')` only
- [ ] Attribution credit block `.sb-credit` at bottom of `<nav id="sb">`
- [ ] `.sb-tog`, `#btt`, `#gst` present
- [ ] No raw Unicode; all special characters HTML-entity-encoded
- [ ] All `html-style` HTML structural integrity checks passed (Section 16 of that skill)
