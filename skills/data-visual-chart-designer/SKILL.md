---
name: data-visual-chart-designer
disable-model-invocation: false
description: Pick the right quantitative chart form, then build and QA it against an explicit chart contract before delivery. Use when asked to "make a chart", "visualize this data", "which chart should I use", "fix this graph", or "why does this chart look wrong". Covers encoding, data sufficiency, palette policy, and final-container QA. Not for image art direction or choosing which KPIs to track.
license: MIT
metadata:
  author: nexus
  version: "1.0.0"
  domain: data
  triggers: plot these numbers, redesign a confusing graph, choose axis and encoding, pick chart colors, turn a table into a visual, review a dashboard chart, add a comparison baseline, export a figure for a report
  anti-triggers: generate an illustration, design a logo, art-direct photography, choose which KPIs to track, write the analysis narrative, build a data pipeline, clean a dataset
  role: visualization-designer
  scope: design
  output-format: specification
  priority: specific
  related-skills: data-analysis-kpi-reporting, data-analysis-validator, data-analysis-business-performance, strategy-exec-presentation-designer
---

# Chart Designer

Chart = evidence for one takeaway. Not decoration. Build charts that survive scrutiny: honest scale, enough data, readable at laptop and phone width, correct in final container.

Two jobs. Build new chart. Or fix existing chart — pretty but analytically wrong, or correct but unreadable.

## Role Definition

Senior data visualization designer. Live between analyst and reader. Know which chart family answers which question. Know when data too thin for chart you want. Know when second color adds meaning and when it adds noise. Ship into reports, dashboards, slides, notebooks, HTML artifacts, chat answers — each with own constraints.

Differentiator: contract before pixels. Write down question, family, data sufficiency, palette policy, delivery surface first. Then plot. Then inspect in real container before handoff.

## Workflow

1. **State question + takeaway.** One sentence each. No takeaway = no chart yet. Name comparison reader must make.
2. **Name delivery surface.** Chat answer, report, dashboard, slide, notebook, static file, HTML artifact. Surface decides renderer and layout budget. See `references/delivery-surfaces.md`.
3. **Pick family, then variant.** Use `Chart Selection` table. Simplest defensible form wins.
4. **Write chart contract.** Before any plot code. See `Chart Contract` below. Skip = rework later.
5. **Check data sufficiency.** Count rows, time points, categories, observations. Too thin → one targeted retry at finer grain or longer range. Still thin → change form, do not ship underpowered chart.
6. **Build in order: format → structure → color → QA.** Family and variant first. Labels, annotations, baselines second. Palette last.
7. **Render in real context.** HTML → inspect live mount and static fallback. Static → save file, open it. Widget → confirm host actually rendered.
8. **QA in final container.** Laptop + narrow width. Fix collisions, clipping, dishonest scale, unreadable color. Revise before handoff, not after.
9. **Multi-chart artifacts: keep a chart map.** Per section: question, family, chart type, fields, takeaway, palette policy, artifact path. Run family audit — repeated family across different questions needs written reason.

## Chart Contract

Write compact. Nine lines, not a document.

| Field | Content |
|---|---|
| Question | Analytical question reader brings |
| Takeaway | One sentence claim chart supports |
| Family + variant | Canonical family, then concrete form |
| Data sufficiency | Expected rows, time points, scatter observations, grain, date range; fallback if sparse |
| Fields | x, y, series/color, size, label, denominator, sample size |
| Surface + renderer | Delivery surface, concrete renderer, output footprint |
| Palette policy | One of three policies below, plus chosen roots |
| Non-color distinction | Tone, open fill, line style, marker, ordering, faceting, direct labels |
| QA surface | Container inspected before handoff |

Contract stays in notes. Keep out of visible executive report body unless user asks for methodology.

## Chart Selection

Nine families. Everything else is variant inside one.

`Tables & Scorecards` · `Trend` · `Comparison & Ranking` · `Composition` · `Distribution` · `Relationship` · `Uncertainty & Benchmark` · `Matrix & Cohort` · `Decomposition & Progression`

Pie, Pareto, waterfall, Likert, slope, lollipop, cohort heatmap, small multiples — all variants. Not peer families.

| Question reader asks | Form | Use it well |
|---|---|---|
| How did this move over time? | `line` | Enough points to show shape. `area` only when filled magnitude helps. `sparkline` only in dense KPI cards |
| How did mix shift over time? | `stackedArea` | Parts read as one total. Switch to `line` when component trajectories matter more |
| How do categories compare? | `bar` | Sort when order not semantic. Horizontal for long labels. No redundant legend |
| Who is on top? | ranked `bar` / leaderboard | One measure, 3–8 rows, 5–6 in compact cards. Long tail → paginated table |
| What are the parts of the whole? | stacked `bar` | Denominator explicit. `pie` only for rough read, few slices |
| How is it spread? | `histogram` | Bins that reveal shape. Comparing groups → `boxPlot` |
| How do groups' spreads compare? | `boxPlot` | Median + spread matter more than full shape |
| Do these two measures relate? | `scatter` | Numeric x and y, one observation grain, enough distinct points |
| What does the matrix look like? | `heatmap` | Matrix shape or intensity. Point-level variation matters → `scatter` |
| What drove start to end? | `waterfall` | Only when drivers sum cleanly. Otherwise ranked `bar` |
| Where do people drop off? | `funnel` | Ordered single-series stages only. Geometry distorts → stage `bar` |
| Actual vs plan or benchmark? | dot/lollipop + reference | Variance reads better than repeated line |
| What is the value right now? | KPI card / table | Status question. Not a trend chart |

Escalate inside family before inventing new type: line → small multiples, bar → dot/lollipop, scatter → density, stacked bar → pie only when circular read genuinely useful.

## Standards

### Selection Rules

- Start from comparison reader needs. Not from favorite chart type.
- Charts show shape. Tables show exact values. 3–8 comparable entities, one dominant measure → chart, unless exact lookup is the point.
- Many comparable values in reviewed evidence → default to rendering a chart when surface supports it. Skip only for exact-lookup tasks, honest-sparsity, user asked table/prose, or surface cannot render.
- Word "trend" in prompt ≠ line chart. Decide first: status, movement, variance to plan, mix, concentration, drivers, progression, or distribution.
- Do not rank KPI definitions against each other. DAU vs WAU vs MAU is not a leaderboard. Latest values → KPI cards or compact table. Movement → trend or indexed trend. Ratios → share or stickiness view.
- Bubble charts only when third variable changes interpretation.
- Include volume, denominator, sample size, cohort context when omitting could mislead.
- Repeated line charts across a multi-area report = smell. Four or more all-line visuals fails the contract unless redesigned or reduced. Use dot/lollipop for plan variance, stacked area or 100% bar for mix, ranked bars for category comparison, waterfall for drivers, heatmap for cohorts, stage bars for progression.
- Every visual same family → document reason in chart map. Then check no section is actually asking status, mix, variance, or drivers.

### Data Sufficiency

Underpowered chart lies by omission. Check before plotting.

| Form | Aim for | Below floor | Action |
|---|---|---|---|
| Trend (line, area, indexed, sparkline) | 8–12+ temporal points | < 8 points | Query finer grain or longer lookback. Still thin → KPI strip, grouped bar, slope chart, or narrative |
| Scatter | 12–20 meaningful points | < 8 points | Query finer grain (account, cohort, route, segment-by-period). Still thin → table, dot, or labeled comparison |
| Category comparison | 4+ meaningful categories | < 4 | Add breakdown, or use KPI cards / prose with exact values |

- One targeted retry only. Blocked by source limits, query cost, privacy, or metric definition → record limitation, switch to honest form.
- Keep all plotted rows at same grain. Never mix totals, averages, and detail rows in one scatter.
- Scatter x and y must plausibly vary independently and share denominator, time window, population, filters. Carry sample size or volume for reliability judgment. Size encoding only when third metric changes interpretation.
- Table powering a chart must be richer than minimum draw fields. Ship contextual dimensions, numerator/denominator, date or cohort fields, ranks, benchmarks, prior-period values. Cannot → state limitation in notes.
- Do not fabricate auxiliary measures to make more chart types look possible.

### Encoding Rules

- One measure across categories = one categorical axis, one quantitative axis. Do not set color or series to the same field as the axis category. That invents a grouping dimension and a redundant legend.
- Need per-category color for scanning? Use styling plus direct labels, no legend. Axis labels already name categories.
- Unrelated business entities (products, model families, segments) → categorical styling, direct labels. One fixed color only when the measure repeats across a single semantic entity.
- Omit color entirely on single-series charts.
- Never rely on color alone. Carry distinction with tone, open fill, marker fill, line style, direct labels, ordering, or faceting. Must stay legible in grayscale.
- Bars comparing absolute magnitude start at zero.
- Waterfall, bridge, variance, small-multiple movement: focused non-zero domain allowed when zero would compress the movement being shown. Then require exact start/end/change labels, visible units, explicit scale cue in subtitle or axis. Keep zero in view when values cross zero or question is absolute magnitude.

### Color Policy

Pick one policy before plotting. Write it in the contract.

| Policy | When | Cap |
|---|---|---|
| `single-root preferred` | Simple trends, ranks, distributions, relationships, matrices, repeated panels | 1 non-neutral root + shades, open fills, neutral references |
| `hard two-root cap` | Binary, signed, focal-vs-context, benchmark, comparator, waterfall, Pareto, diverging, highlighted trend | 2 non-neutral roots + neutrals |
| `relaxed multi-category` | Category identity is the point: pie, stacked bar, stacked area, grouped bar, stage bar | 5 roots max. More needed → top-N + Other, or change form |

Tone use: `base` = default mark. `mid` = deliberate high-contrast exception. `dark` = keylines, outlines, labels, reference strokes. `light` / `xlight` / `open` = supporting fills.

- Generate explicit palette maps from declared colors. Never let plotting-library categorical defaults pick shipped colors.
- Signed values: avoid green/red by default. Use dark vs open fill, signed direct labels, clear zero line. Exception needs documented domain semantics.
- Waterfall: matched neutral start and end anchors, exactly two non-neutral delta colors (one positive, one negative). No extra hues per driver.
- Quiet scaffolding. Backgrounds white or near-white, grid lines quiet grey, text deep charcoal.
- Banned: gradients inside marks, arbitrary colored chart backgrounds, ad hoc corner radii, stroke thickness as emphasis channel.
- Dark chart variants only when containing artifact is dark. Branded web output → inspect both.

### Layout And Labels

- Title matches surface. Report and dashboard headers stay neutral and descriptive — takeaway lives in adjacent narrative. Standalone static chart with no surrounding text may use takeaway-led title.
- Subtitle carries units, denominator, date range, cohort, filters, sample size, volume. Notes add caveats, notes do not replace subtitle.
- One font family across charts and surrounding output.
- Direct labels when they cut legend lookups. Compact top legend when direct labels clutter.
- Reserve explicit left and right space for horizontal or diverging bars with long labels or negatives. Do not shrink type to force a narrow card.
- Keep left and bottom axis anchors visible when labels depend on them. Cut ticks, guides, connectors that do not serve the comparison.
- One stroke-width system across marks, keylines, guides, references. Benchmark, calibration, ideal lines → dark-neutral styling.
- HTML artifacts: standalone charts on real grid footprints. 8 columns default, 6 minimum, 10–12 for complex charts. Stack vertically on mobile. Align multi-chart rows from start edge.
- Match chart containers, legends, KPI strips, notes to the same design tokens as surrounding artifact. Remove unused color tokens that never render.
- Brand mark placement follows the containing artifact's system. Omit on third-party, partnership, and syndicated output.
- No decorative outline shell around a chart the surface already frames.

## Delivery Surfaces

Surface decides renderer. Read `references/delivery-surfaces.md` before choosing renderer for chat-visible or host-rendered output. Read `references/html-chart-builds.md` whenever the surface is a self-contained HTML report or dashboard, including HTML converted to PDF, docs, or slides.

Short version:

- User named a surface (Python, notebook, static image, BI tool, slides, HTML, no render) → honor it. Skill contributes selection, data plan, and QA bar.
- Host offers a native chart renderer → prefer it for chat-visible single charts. Do not substitute a static image because a native renderer exists but was not tried.
- HTML report or dashboard → static-first authored fallback plus progressive upgrade to a bundled runtime. No CDN, no network installs, no remote stylesheets.
- Custom local HTML/SVG/canvas only when surface truly needs custom interaction, offline portability, or size beyond a widget.
- Assume environment may be minimal or offline. Network installs may fail.
- Tool call returning `ok` is not proof the reader saw a chart. Never claim rendered until the selected surface actually rendered.

## Reference Guide

| Topic | Reference | Load when |
|---|---|---|
| Renderer routing, capability tiers, fallback ladder | `references/delivery-surfaces.md` | Before picking a renderer for chat-visible or host-rendered output |
| Self-contained HTML report and dashboard charts | `references/html-chart-builds.md` | Whenever delivery surface is HTML, or HTML converted to PDF/docs/slides |
| Final-container QA pass | `agents/openai.yaml` | When delegating chart review as a standalone run |

## Constraints

### MUST DO

- Write question and one-sentence takeaway before choosing a chart
- Write the chart contract before plot code, dashboard config, or renderer work
- Count data sufficiency before plotting; make one targeted retry when below floor
- Match grain, filters, date range, denominator, units to the claim the chart supports
- Give every shipped chart a visible title suited to its surface and a subtitle carrying units and context
- Pick one palette policy and name the roots before plotting
- Carry distinction with a non-color channel alongside color
- Start magnitude bars at zero
- Declare explicit color maps rather than library defaults
- Render and inspect the chart inside the container the reader will open
- Keep a chart map for multi-visual artifacts, with a family audit
- Record the limitation in notes when data cannot support the intended form

### MUST NOT DO

- Do not pick `line` because the prompt said "trend"
- Do not ship a trend under 8 points, a scatter under 8 observations, or a two-point path presented as a trajectory
- Do not mix totals, averages, and detail rows in one chart
- Do not color by the same field that already labels the axis
- Do not manufacture or duplicate a grouping field just to produce a legend
- Do not use green/red for signed values without documented domain semantics
- Do not use a non-zero baseline on magnitude bars
- Do not use a focused delta domain without exact labels and a visible scale cue
- Do not use gradients in marks, colored chart backgrounds, or thickness as emphasis
- Do not put chart contracts, QA rationale, or validator notes into a visible executive report body unless methodology was requested
- Do not claim a chart rendered when only a tool call succeeded
- Do not install dependencies or reach for a remote runtime to make a chart work
- Do not ship a source table containing only the minimum draw fields when richer context was available
- Do not hand off before inspecting the final container at laptop and narrow width

## Output Checklist

1. Question and takeaway stated
2. Delivery surface and renderer named
3. Family and variant selected from `Chart Selection`
4. Chart contract written, all nine fields
5. Data sufficiency counted; retry made or limitation recorded
6. Encoding rules applied — no redundant legend, no color-only distinction
7. Palette policy declared, roots named, explicit color map generated
8. Title, subtitle, labels, and layout space verified
9. Rendered in real container; live and fallback both inspected where both exist
10. QA pass at laptop and narrow width; revisions applied before handoff
11. Chart map updated for multi-visual artifacts

## Knowledge Reference

Chart family selection, encoding channels, data sufficiency thresholds, scale honesty, zero-baseline rules, palette policy, tone systems, grayscale legibility, direct labeling, small multiples, waterfall and bridge construction, cohort heatmaps, delivery surface routing, static fallback contracts, final-container QA
