---
name: report-executive-overview
description: 'HTML report skill for Output 1: 1-Page Executive Overview. Defines the target audience, required sections, layout rules, and delivery protocol for the single-page executive summary HTML artifact produced by the project-architect skill. All formatting, CSS class conventions, color palette, typography, and the attribution credit block are defined in the html-style skill (design-skills/html-style). Triggers: 1-page executive overview, executive summary HTML, Output 1, one-page deck, board summary, CEO summary.'
argument-hint: 'Reference this skill when producing Output 1 (1-Page Executive Overview) from the project-architect workflow. Load html-style skill first for all formatting rules.'
---

# Report: 1-Page Executive Overview (Output 1)

## Role Context

This skill defines the specification for **Output 1** of the `project-architect` HTML presentation suite: the 1-Page Executive Overview.

**Before writing any HTML for this output**, load and apply the `html-style` skill (`design-skills/html-style`). That skill owns:
- Organization brand palette, typography, and brand header rules (see html-style skill)
- HTML-specific compression rules (H-1 through H-7)
- Core chunked delivery protocol (Steps 1–3)
- Attribution credit block requirement and placement rules
- HTML structural integrity checklist

---

## Target Audience

Executive sponsor, CEO, COO, board observer — **60-second read**.

This output is the highest-compression artifact in the suite. It must communicate the initiative's purpose, outcomes, timeline, and risk in a single glance. No technical detail, no story IDs, no point estimates.

---

## Format

- Single-page HTML; **no sidebar navigation** required
- Print-friendly layout (A4 or letter dimensions, clean white background)
- Page header with organization brand identity (per `html-style` Section 1)
- Page footer with attribution credit block (per `html-style` Section 2, footer placement for Output 1)

---

## Required Sections

Produce all seven sections in this exact order:

| # | Section | Content Rules |
|---|---------|---------------|
| 1 | **Initiative Name + Organization Branding** | Header area; initiative name in Georgia bold; organization logo treatment per `html-style` brand header rules |
| 2 | **Strategic Objective** | One sentence only; no bullet list |
| 3 | **What We Will Deliver** | 3–5 bullet points; outcome statements only (what changes for the business), not activities (what the team does) |
| 4 | **Timeline at a Glance** | Simple 4-column table: Q1 / Q2 / Q3 / Q4; one-line theme per quarter; no story IDs or point estimates |
| 5 | **Investment &amp; Resources** | Team count, total story points, key external dependencies; 3 data points max |
| 6 | **Top 3 Risks** | Name, rating (Critical / High / Medium / Low), mitigation; one row per risk; source from Risk Register |
| 7 | **Decision Needed** | Zero or one item; a single sentence stating exactly what action is required from this audience; omit the section entirely if no decision is pending |

---

## Chunked Delivery

Output 1 is typically short enough to deliver in **a single response** — no chunking required. If the content is unusually long:
- Apply all `html-style` compression rules (H-1 through H-7) to reduce size first
- If still too long after compression, apply the core chunk protocol (Steps 1–3 from `html-style` Section 4)

---

## Quality Checks

Before delivering Output 1:

- [ ] All seven sections present in the correct order
- [ ] Section 3 (What We Will Deliver) uses outcome language — no project activity verbs (build, configure, migrate) without an outcome clause
- [ ] Section 4 (Timeline) uses consistent phase/quarter labels matching all other HTML outputs
- [ ] Section 6 (Top 3 Risks) ratings exactly match the scored Risk Register in the Technical Plan — no inflation or deflation
- [ ] Section 7 (Decision Needed) is either one precise action item or omitted entirely — never a vague call-to-action
- [ ] Attribution credit block present in the page footer (per `html-style` Section 2)
- [ ] Organization brand colors, typography, and header treatment applied (per `html-style` Section 1)
- [ ] No raw Unicode characters in HTML source; all special characters HTML-entity-encoded
- [ ] No sidebar nav included — this is a single-page layout
- [ ] All `html-style` HTML structural integrity checks passed (Section 7 of that skill)
