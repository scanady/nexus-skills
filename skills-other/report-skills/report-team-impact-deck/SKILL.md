---
name: report-team-impact-deck
description: 'HTML report skill for Output 4: Per-Team Impact Deck. Defines the per-team section structure (5 required subsections), mandatory 3-chunk delivery map, team-group chunk splits, per-team section compression rules, skill consultation requirement, sidebar navigation grouping, and Output 4 interactive feature adaptations for the team-facing HTML artifact produced by the project-architect skill. All shared formatting, CSS class conventions, color palette, typography, core chunk protocol, and the attribution credit block are defined in the html-style skill (design-skills/html-style). Triggers: per-team impact deck, Output 4, team deck HTML, team impact slides, team-by-team plan, team impact HTML.'
argument-hint: 'Reference this skill when producing Output 4 (Per-Team Impact Deck) from the project-architect workflow. Load html-style skill first for all formatting rules and core chunk protocol.'
---

# Report: Per-Team Impact Deck (Output 4)

## Role Context

This skill defines the specification for **Output 4** of the `project-architect` HTML presentation suite: the Per-Team Impact Deck.

**Before writing any HTML for this output**, load and apply the `html-style` skill (`design-skills/html-style`). That skill owns:
- Organization brand palette, typography, and brand header rules (see html-style skill)
- HTML-specific compression rules (H-1 through H-7) — apply ALL before writing any section
- Core chunked delivery protocol (Steps 1–3 format) — use with the 3-chunk map defined below
- Attribution credit block requirement (sidebar bottom for Output 4: `.sb-credit`)
- Interactive CSS class conventions and JS module responsibilities
- HTML structural integrity checklist

---

## Target Audience

Each impacted delivery team — team lead and senior team members — **10-minute read**.

**Purpose**: Translate the full initiative plan into team-specific language — what this team owns, why it matters, what questions get asked, and what the timeline looks like from their seat. Cross-reference the story backlog and team load plan from Output 3 (Technical Plan) to extract each team's actual assignments.

---

## Format

- Multi-section HTML with **Pattern A sidebar navigation** (`<div id="sb">`, `<div id="mc">`, `.col` collapse — same DOM as Output 3; see `html-style` Section 5)
- `<body class="page-mode" id="top">` — `body.page-mode` applied by default
- One section per impacted team; same `go()` / `setAct()` / `buildPageNav()` pattern as Output 3
- Section data stored in `_META` array (not `_SEC_OVERVIEWS` object): `{grp, title, ov}` per team, ordered by section index
- `buildSectionHeaders()` reads `_META[i]` and generates group div with “GROUP &bull; N / TOTAL” format
- `.pg-hdr` section page header at top of each section: team name as title; functional area group label with section count (injected by `buildSectionHeaders()`)
- `.trv` **Team Review panel** (NOT `.clv`) before `.pg-nav` in each section — injected by `buildTRVPanels()` using `_TRV` array; header class `.trv-h` with `&#9733; Team Review Points` (NOT `.trv-lbl`)
- `#gst` global search in `#gst-wrap` filters table rows via `style.display` (same as Output 3)
- `.sb-tog` (`id="sbt"`), `#btt` sidebar collapse and back-to-top
- Attribution credit block `.sb-credit` at bottom of `<div id="sb">`

**Only include teams with at least one assigned story.** Do not generate a section for teams with zero stories in the backlog. Omit empty functional groups from the sidebar if all teams in that group have zero stories.

---

## Skill Consultation Requirement

Before writing any team section, load and consult the corresponding team skill file (if one exists) to ensure accuracy of role context, domain language, and collaboration interfaces. Cross-reference the story backlog (Section 7 of Output 3) and team load plan (Section 9 of Output 3) to extract each team's actual assignments.

| Team | Skill to Consult |
|------|------------------|
| DE  -  Data Engineering | `data-engineer` |
| AIE  -  AI Engineering | `enterprise-ai-architect`, `marketing-ai-architect` |
| MDA  -  Marketing Data Architecture | `marketing-data-architect`, `enterprise-data-architect` |
| MDA-GOV  -  Data Governance | `data-governance-lead` |
| MTA  -  Marketing Technology Architecture | `marketing-technology-architect` |
| MCR  -  Marketing Creative Strategy | `marketing-creative-strategist` |
| MCC  -  Marketing Content Creation | `marketing-content-creation-specialist`, `marketing-content-manager` |
| MCM  -  Marketing Campaign Management | `marketing-campaign-manager` |
| MAN  -  Marketing Analysis | `marketing-reporting-specialist` |
| MFX  -  Marketing Forecasting | `marketing-forecasting-specialist` |
| MAU  -  Marketing Audience | `marketing-audience-specialist` |
| EML  -  Email Channel Execution | `email-channel-execution-lead` |
| PRT  -  Print / Direct Mail | `print-channel-execution-lead` |
| DGT  -  Paid Digital / Performance Media | `paid-media-specialist` |
| PLT  -  Platform Engineering | `chief-technology-officer`, `chief-information-officer` |
| APP  -  Application Engineering | `lead-application-architect` |
| CPL  -  Compliance | `lead-compliance-officer` |
| PMO  -  Program Management | `business-analyst` |

---

## Required Slide Structure (One Section Per Team)

Each team section must contain all five subsections in this exact order:

### Subsection 1 — Impact Overview
- What this initiative changes for this team: new tools, new processes, new data, new responsibilities
- Current-state vs. future-state comparison (2-column layout or 2-row table)
- One sentence on why this team's work is on the critical path
- **Maximum**: 150 words of prose; use a table or bullet list for the comparison

### Subsection 2 — Why Your Team Is Working on This
- Strategic connection: how this team's work enables the stated initiative objective
- Business outcome this team's deliverables unlock (tie to a KPI or gate criterion from the plan)
- One sentence on what happens if this team's work is delayed
- **Tone**: motivating, factual, no jargon from other teams' domains

### Subsection 3 — FAQ — Decisions &amp; Risks
- 3–5 questions in Q &amp; A format using the team's natural voice
- Questions must be drawn from: (a) risks in the Risk Register that directly involve this team as owner or dependency; (b) open questions in Section 14 assigned to this team; (c) platform or process decisions this team must make or ratify
- Each answer is 1–3 sentences maximum; cite the risk ID or question ID where applicable
- Use `.faq-item` card styling (question in bold navy, answer in normal weight)

**`.faq-item` style**: `background:#F8FAFD; border-left:4px solid #002D62; padding:12px 16px; margin-bottom:10px` — question in `font:bold 12px Georgia,serif; color:#002D62`; answer in `font-size:12px; color:#333`

### Subsection 4 — Timeline
- This team's quarter-by-quarter commitments only — not the full program roadmap
- One row per quarter; columns: Quarter &middot; Phase &middot; Stories / Deliverables &middot; Point Estimate &middot; Load
- Highlight rows where Load = Medium or High: apply `class="ldm"` on `<tr>` for Medium; `class="ldh"` on `<tr>` for High — CSS handles the background color (`#FFFAE5` for ldm, `#FFEECC` for ldh); class applied directly in HTML markup (NOT generated by JS like Output 3)
- If the team has zero stories in a quarter, include the row with "No active delivery" so the full horizon is visible
- Source: Section 8 (Quarterly Roadmap) and Section 9 (Team Load Plan) of Output 3

### Subsection 5 — Review Summary
- What "done" looks like for this team: 3 bullet points referencing actual DoD criteria from this team's stories
- Key success metric: one KPI from Section 13 (Metrics &amp; KPIs of Output 3) that this team's work most directly drives
- Handoff point: what this team delivers to which downstream team or section of the plan
- Contact for questions: Team Lead role title (not a personal name)

---

## Mandatory 3-Chunk Delivery

Output 4 **must always** be delivered in at least 3 chunks. With 14 active teams and 5 subsections per team, never attempt single-response delivery regardless of perceived size.

**Required before Chunk 1**: Announce the chunk plan using Step 1 format from `html-style` Section 4, with this specific map. Close with: "Confirm to start Chunk 1, or type a team name to jump directly to it."

| Chunk | Content | What it includes |
|-------|---------|------------------|
| **Chunk 1** | `<html>` -> `<style>` -> sidebar nav (all teams pre-declared) + Data &amp; Technology group (DE, AIE, MDA, MDA-GOV, MTA, PLT, APP) | Head, CSS, JS scaffolding, 7 team sections |
| **Chunk 2** | Marketing Execution group (MCM, MAN, EML, PRT, MCC) + Program &amp; Compliance group (MCR where applicable, CPL, PMO) | 7–8 team sections |
| **Chunk 3** | Remaining team sections (if any) + closing `</div>` + `<script>` + `</body></html>` | Final teams + JS close |

**Overflow rule**: If any chunk is still at risk of overflow, split Chunk 1 at the MDA-GOV / MTA boundary and promote MTA–APP to Chunk 2, shifting subsequent chunks by one.

---

## Per-Team Section Compression Rules

Apply these in addition to all `html-style` H-rules:

- **Impact Overview**: current-state vs. future-state as a 2-column table; no paragraph prose beyond one intro sentence
- **Why Your Team**: 3 bullet points maximum; no narrative paragraphs
- **FAQ**: 3–5 `.faq-item` cards only; each answer <=2 sentences; cite risk/question ID inline
- **Timeline**: one table row per quarter across the full planning horizon; include quarters with no active delivery as "No active delivery" rows
- **Review Summary**: 3 bullets maximum; handoff stated in one sentence
- Do not repeat the team full name or abbreviation in section body prose once established in the `.pg-hdr` header
- Never use `style=` per-element in team section HTML; all styling via the shared `<style>` block defined in Chunk 1

---

## Sidebar Navigation Structure

Group sections by functional area using `.ng` group labels:

```
Data & Technology
  → DE — Data Engineering
  → AIE — AI Engineering
  → MDA — Marketing Data Architecture
  → MDA-GOV — Data Governance
  → MTA — Marketing Technology Architecture
  → PLT — Platform Engineering
  → APP — Application Engineering
Marketing Execution
  → MCR — Marketing Creative Strategy
  → MCC — Marketing Content Creation
  → MCM — Campaign Management
  → MAN — Marketing Analysis
  → MFX — Marketing Forecasting
  → MAU — Marketing Audience
  → EML — Email Channel Execution
  → PRT — Print / Direct Mail
  → DGT — Paid Digital / Performance Media
Program & Compliance
  → CPL — Compliance
  → PMO — Program Management
```

Only include teams with assigned stories. Omit empty groups if all teams in that group have zero stories.

---

## Interactive Feature Adaptations for Output 4

Output 4 uses the same page-mode interactive standard as Output 3, with these adaptations:

| Feature | Adaptation for Output 4 |
|---------|------------------------|
| **Page mode** | `body.page-mode`; same `go()` / `setAct()` / `buildPageNav()` / `buildSectionHeaders()` pattern as Output 3; also calls `buildTRVPanels()` (NOT `buildCLevelPanels()`) |
| **Section page header** | `.pg-hdr` with team name as title; group label = functional area; section N-of-N |
| **Team review panel** | `.trv` (NOT `.clv`): injected by `buildTRVPanels()` using `_TRV` array; header class `.trv-h` (NOT `.trv-lbl`); `&#9733; Team Review Points`; gold left-border; 3 bullets scoped to this team's deliverables and outcomes |
| **Global search** | `#gst` sidebar search filters table rows across all team timeline tables |
| **Sidebar collapse + back-to-top** | `.sb-tog` + `#btt` — same as Output 3 |
| **Attribution** | `.sb-credit` at sidebar bottom: `Created By: Data Architecture` / `Created Date: YYYY.MM.DD` |
| **FAQ styling** | `.faq-item` card per Subsection 3 spec above |
| **Load highlight rows** | Apply `class="ldm"` on `<tr>` for Medium load; `class="ldh"` on `<tr>` for High load — CSS handles background (`#FFFAE5` for ldm, `#FFEECC` for ldh); classes applied directly in HTML markup (NOT via JS) |
| **Contrast enforcement** | **CRITICAL**: Never apply a CSS class that sets a light background to a `<th>` element. Table `<th>` cells always use `background:#002D62; color:#fff`. Load row classes (`tr.ldm`, `tr.ldh`) are on `<tr>`, not on `<th>`. Verify every `<th>` has dark background + white text. |

---

## Quality Checks

Before delivering Output 4:

- [ ] Chunk plan announced before Chunk 1; closes with "Confirm to start Chunk 1, or type a team name to jump directly to it"
- [ ] Only teams with at least one assigned story are included — no empty team sections
- [ ] Each team section contains all five subsections: Impact Overview, Why Your Team, FAQ, Timeline, Review Summary
- [ ] FAQ questions sourced from Risk Register (Section 5 of Output 3) and Open Questions (Section 14) — no invented questions
- [ ] Timeline table for each team matches Section 8 (Quarterly Roadmap) of Output 3 exactly — no quarter shifts
- [ ] Load column values (L/M/H) match Section 9 (Team Load Plan) of Output 3 exactly
- [ ] Timeline rows use `class="ldm"` on `<tr>` for Medium load and `class="ldh"` for High load (NOT inline `style=` or `.tl-m`/`.tl-h` classes)
- [ ] Corresponding team skill consulted per the skill consultation table before writing each team's section — domain language is accurate
- [ ] Sidebar uses Pattern A DOM: `<div id="sb">` + `<div id="mc">`; `.col` collapse (NOT `body.sb-off`)
- [ ] `.trv` team review panel used (NOT `.clv`); injected by `buildTRVPanels()` using `_TRV` array; header class `.trv-h` (NOT `.trv-lbl`)
- [ ] Section data in `_META` array (NOT `_SEC_OVERVIEWS` object); `buildSectionHeaders()` shows group with bullet and count
- [ ] `.faq-item` styling applied to all FAQ cards; question text is bold navy, answer text is normal weight
- [ ] **Contrast check**: no `<th>` element has a light background class — all `<th>` use `background:#002D62; color:#fff`; load classes (`tr.ldm`, `tr.ldh`) on `<tr>` only
- [ ] Sidebar nav groups correct (Data &amp; Technology / Marketing Execution / Program &amp; Compliance); empty groups omitted
- [ ] Pattern A sidebar: `<div id="sb">` present; `<div id="mc">` present; `.sb-tog` (`id="sbt"`), `#btt`, `#gst` in `#gst-wrap`, `.sb-credit` all present
- [ ] `body.page-mode` on `<body>` element
- [ ] If 9+ team sections, chunk plan announced before Chunk 1
- [ ] No raw Unicode; all special characters HTML-entity-encoded
- [ ] All `html-style` HTML structural integrity checks passed (Section 16 of that skill)
