# Data Display

Making tables, metric tiles, and dashboards read cleanly inside a UI refactor. For choosing and styling the charts themselves — categorical/sequential/diverging palettes, mark specs, chart-type selection — defer to the **dataviz** skill; this file covers the surrounding UI: tables, KPI tiles, and dashboard layout.

## Number vs Chart

The first question is whether a chart is warranted at all. A single value or a two-way comparison is usually clearer as text:
```
❌ pie chart, 2 slices (73% / 27%)
✅ "73% of users completed onboarding"
```
Use a chart when a pattern (trend, comparison across many items, distribution) is the point.

## Tables

Tables beat charts when precise values matter, users look up specific rows, there are many attributes per item, or the data will be exported.

Design rules:
- **Right-align numbers, left-align text.** Numbers compare by column when right-aligned.
- **Consistent precision** — `$1,234.00 / $567.89`, not `$1234 / $2.5k` mixed.
- **Minimize borders** — light horizontal rules only; no vertical grid lines.
- **Generous padding** — ~`12px 16px` per cell.
- Optional: zebra striping (`even → bg-gray-50`), hover highlight, sticky header (`position: sticky; top: 0`), sortable columns with an accessible sort control.

## KPI / Metric Tiles

The big-number row at the top of most dashboards.
```html
<div class="metric-card">
  <span class="label">Revenue</span>
  <span class="value">$45,234</span>
  <span class="change positive">↑ 12.3%</span>
</div>
```
- Value large and heavy (~2rem, 600); label small and muted; delta colored (green up / red down) **and** arrowed so it doesn't rely on color alone.
- Keep tiles uniform in size and spacing across the row.

## Dashboard Layout

Order by importance, top to bottom:
1. **KPI row** — 3–5 big-number tiles.
2. **Primary chart** — the single most important trend, full width.
3. **Supporting charts + detail table** — two-column beneath.

Keep one clear focal point per screen; don't give every panel equal visual weight.

## In-UI Chart Hygiene

When a chart is embedded (leave the full design to the dataviz skill, but at minimum): start bar/line axes at zero, label directly instead of forcing legend lookups, cap at 5–7 series/categories, drop 3D and dual Y-axes, and remove non-data "chartjunk."

## Accessibility

Charts need a text equivalent: wrap in `figure role="img"` with an `aria-label`/`figcaption` summarizing the takeaway, and offer the underlying data as a table (`<details>` "View as table"). Never encode a series by color alone — add labels, patterns, or direct annotation. See `accessibility.md`.
