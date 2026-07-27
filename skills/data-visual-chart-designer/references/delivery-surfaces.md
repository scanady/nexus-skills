# Delivery Surfaces

Load after the surface is chosen, to pick a renderer. This file does not choose the surface. It never downgrades a selected report, dashboard, or HTML artifact into a chat answer.

Rule that governs everything below: the surface the user or the parent workflow selected stays selected. Renderer choice happens inside it.

## Capability Tiers

Hosts differ. Describe your host in these terms, then route.

| Tier | What it is | Typical shape |
|---|---|---|
| T1 — native chart widget | Host renders a chart from a JSON spec you hand it | Fixed family set, host owns card, axes, colors, tooltips, dark mode |
| T2 — native HTML block | Host renders a self-contained HTML fragment you author | You own marks and layout; host owns the container |
| T3 — document renderer | Report, dashboard, notebook, slide, BI tool with its own chart primitives | Surface owns rendering; this skill supplies spec and QA bar |
| T4 — static renderer | Local plotting to an image or vector file | Full control, no interaction, inspectable artifact |
| T5 — no renderer | Text-only channel | Compact table or prose with exact values |

Tool-provided renderers (MCP servers, plugins, analytics backends) are data sources plus, sometimes, a T1 or T3 renderer. A successful tool result is not a rendered chart. Confirm the reader's surface painted something before saying it did.

## Routing

Work down this list. Stop at first match.

1. **User named an output** — Python, notebook, static image or file, BI tool, slides, docs, HTML, or "no chart". Honor it. Contribute selection, data plan, encoding, and QA only.
2. **Parent workflow selected a report, dashboard, or HTML artifact** — use that surface's chart primitives. HTML → `html-chart-builds.md`.
3. **Chat-visible answer, one simple chart** — T1 if the host has it and the family is supported. Do not skip T1 because a static image feels safer.
4. **Chat-visible answer, richer composition** — T2 if the host surfaces it. KPI cards, filters, coordinated views, or a family T1 cannot draw.
5. **T1/T2 attempted and rejected or failed to render** — T4 static from the same reviewed rows. Inspect the image, then deliver.
6. **No visual renderer available, or answer is genuinely table-shaped** — T5. Preserve exact values. Do not claim a visual exists.

## T1 vs T2

T1 JSON chart widgets cover a small family set — typically bar, line, pie, and fixed-size scatter. Boundaries that matter:

- A T1 scatter positions by x and y. It usually cannot map a third measure to point area. Bubble chart is therefore **not** a T1 scatter.
- Heatmap, waterfall, funnel, histogram, box plot, cohort matrix generally fall outside T1.
- Shared filters, KPI cards, or coordinated multi-chart layout fall outside T1.

Any of those → T2, not T4. Do not decline the request, do not ask the user to repeat it, do not emit an unsupported spec shape, do not drop to a static image just because T1 cannot draw the family.

### T1 spec discipline

- One valid chart-spec object, placed directly in the widget's content argument. Do not stringify it, do not nest it under an extra key.
- No prose, Markdown, JavaScript, JSX, imports, comments, or code fences inside the spec.
- Never print the spec as the assistant's visible response. A spec pasted as text is not a chart.
- Include chart type, meta (concise title, reader-facing description, optional footer), field mappings, then data last.
- Percentages passed as percentage points when the format carries a `%` suffix — `42`, not `0.42`.
- Six or more categories, or long labels → horizontal layout.
- Friendly date labels in the data unless exact source labels are required.
- Let the host own card, spacing, axes, grid, tooltip, legend, colors, hover, responsive layout, compact number formatting, dark mode. Do not wrap it in your own card or color system.

### T2 fragment discipline

- One self-contained fragment: app markup, optional scoped `<style>`, one optional trailing `<script>`.
- Excluded: doctype, `<html>`, `<head>`, `<body>`, outer `<main>`, CDN scripts, imports, exports, frameworks, JSX, custom elements, iframes, external stylesheets, network requests, storage APIs, permission-gated APIs.
- Vanilla JavaScript with `addEventListener`. No inline event handlers.
- All reviewed data embedded and bounded. No render-time fetch. No implication of live refresh.
- Inline SVG for marks, axes, labels, annotations. HTML/CSS for cards, legends, filters, tables. No raster images.
- Top-level fragment adds no decorative card, border, shadow, background, or padding. Reserve those for meaningful internal controls, KPI cards, chart regions, result boxes.
- Semantic controls with visible labels, local state, focus-safe spacing, `aria-live` on dynamic results.
- Responsive grids and stacks that fit message width.

Good T2 shape: short heading, one or two labeled controls only when they materially help exploration, compact KPI row when headline numbers matter, one primary chart, optional supporting comparison, concise takeaway or caveat. Interaction stays focused — one filter, metric switch, series toggle, or highlighted comparison. Not a dashboard. Not a multi-screen app. No upload flow. No remote data.

### T2 patterns worth copying

**Bubble** — bounded embedded rows; inline SVG axes, grid, labels, circles; x and y to position, third measure to circle area (radius by square root, not linear); compact size legend; hover or focus tooltip and `aria-live` status only when they add exploration value.

**Funnel** — inline SVG or semantic HTML/CSS for ordered stages; label every stage and value directly; show step-to-step conversion where useful; keep highlight or filter interaction local and simple.

## Mermaid

Not a quantitative chart renderer. Never a substitute for T1, T2, or the static fallback.

## Failure Path

- T1 emitted and rejected or unrendered → one targeted correction. Still failing → T4 static from the same rows.
- T2 not surfaced by the host and no other native renderer fits the family → T4 static.
- T4 also impossible → T5 table or prose with exact values.
- Prefer a static visual over a table. A table is the last rung, not the convenient one.
- Do not convert a selected report into an inline block because the inline block would look nicer.

## Data And Honesty On Any Surface

- Only reviewed values. Grain, time window, units, denominator, and filters stay consistent with surrounding analysis.
- Simplest family that answers the question. Readable labels. Honest axes. Restrained color. Compact number formatting. Direct labels or a clear legend when grouping matters.
- Source names, methodology, and material caveats live in visible text or a concise note. Never hover-only.
- Do not say a chart, block, or filter rendered unless the selected surface actually rendered it.
