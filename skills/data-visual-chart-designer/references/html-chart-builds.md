# HTML Chart Builds

Load whenever the delivery surface is a self-contained HTML report or dashboard — including HTML later converted to PDF, a doc, or slides. Does not apply to host chart widgets or to explicit standalone Python/static-image requests.

## Static-First Contract

One file. Two layers.

**Layer 1 — authored static HTML.** Narrative, KPI cards, tables, caveats, sources, and a readable fallback chart for every chart slot. Renders with scripts disabled. This layer is the deliverable if anything else fails.

**Layer 2 — progressive upgrade.** A bundled chart runtime replaces each fallback after it has painted, and only after it produces a real rendered chart surface. Upgrade is an enhancement, never a dependency.

Why: conversion helpers, PDF printers, and script-suppressed viewers read the static layer. A chart that exists only after JavaScript runs is a chart that silently disappears in half the delivery paths.

Hard limits on the delivered file:
- No CDN, no remote scripts, no remote stylesheets, no `fetch`, no `/api/*` calls, no required storage.
- No sibling image files, no local runtime paths. Self-contained means one file.
- No dependency installs, no build server, no patching minified runtime symbols.
- Runtime parts unavailable → ship the static layer and label the missing live upgrade as a stated delivery limitation. Do not improvise a CDN.

## Placeholder Shape

Each chart card carries one host element whose id matches a payload entry.

```html
<div class="chart-card" data-chart="weekly-signups">
  <div class="chart-fallback" data-chart-fallback>
    <svg viewBox="0 0 960 420" role="img" aria-label="Weekly signups, Apr–Jun 2026">
      <!-- Static marks drawn from the same rows as the payload entry. -->
    </svg>
  </div>
  <div data-chart-live aria-hidden="true"></div>
</div>
```

Exactly one host per payload chart. Leave one runtime marker before `</body>` for the embedding step to replace with escaped payload JSON plus the bundled runtime.

Fallback form: compact inline SVG for line, bar, area, scatter, and composition charts. Compact semantic table when a faithful static SVG would be risky — leaderboards, heatmaps, dense matrices.

## Payload Shape

Separate JSON file, one entry per chart. Reviewed row objects. Numeric fields on the y encoding. Percent formats take fractional values (`0.193` for 19.3%).

```json
{
  "charts": [
    {
      "id": "weekly-signups",
      "type": "line",
      "height": 320,
      "dataset": {
        "id": "weekly-signups",
        "title": "Weekly signups by plan",
        "data": [
          { "week": "2026-04-06", "plan": "Free",  "signups": 1080 },
          { "week": "2026-04-06", "plan": "Team",  "signups": 214 },
          { "week": "2026-04-13", "plan": "Free",  "signups": 1122 },
          { "week": "2026-04-13", "plan": "Team",  "signups": 224 }
        ],
        "spec": {
          "id": "weekly-signups",
          "type": "line",
          "encodings": {
            "x": { "field": "week", "type": "temporal" },
            "y": { "field": "signups", "type": "quantitative", "label": "Weekly signups" },
            "color": { "field": "plan", "type": "nominal" }
          },
          "xAxisTitle": "",
          "yAxisTitle": "",
          "valueFormat": "number"
        }
      }
    }
  ]
}
```

- **Multi-series:** prefer long rows — one numeric y field, one categorical color field. Legend then reads reader-facing series values instead of column names.
- **Horizontal bars:** category in the x encoding, numeric measure in y, plus orientation `horizontal` and grouped mode in settings.
- **Axis titles:** set explicitly. Empty strings when the visible header and subtitle already carry unit and field context — repeated titles are clutter.
- **Tooltips:** array of encoding objects, only when needed.

## Layout Rules

| Constraint | Value |
|---|---|
| Live chart height | 280 minimum, 320 default, more for dense labels or many horizontal bars |
| Left gutter, wide layouts | 96px around live charts so exact currency ticks stay inside clipped cards |
| Narrow layouts | Compact symmetric padding; keep plot area readable rather than preserving desktop gutters |
| Fallback labels | Inside the SVG viewBox with edge padding |
| Signed horizontal bars | Negative value labels inside the bar or on its zero side — never in the category-label lane |
| Table cards | Shared reading width; wide charts get the wide variant, not tables |
| Tables | Wrap directly in the scroll container so narrow tables fill their card and wide tables scroll inside it |

Delta-focused charts — waterfall, bridge, variance — may use a focused value-axis domain when zero would compress the movement. Then carry exact start, end, and change labels plus a visible scale cue.

## Section Map

The shell scaffold assumes a stakeholder or executive report. When the selected specification is technical, replace the section map rather than renaming the summary. Preserve section roles in this order:

`title` → `technical-summary` → `key-findings` → `scope-data-and-metric-definitions` → `methodology` → `limitations-uncertainty-and-robustness-checks` → `recommended-next-steps` → `further-questions`

Set the report audience attribute to match. Audience placeholders get resolved before handoff, not left in the delivered file.

## Build And QA

1. Copy the report shell into a working output file. Keep the audience specification's required section attributes.
2. Author narrative, metric cards, semantic tables, and same-data fallbacks. Add one chart host and one payload entry per chart.
3. Run the embedding step to fold the payload and bundled runtime into the single output file.
4. **Open the delivered file with scripts enabled.** Confirm each live mount contains a rendered chart, the fallback was replaced, exactly one visible chart per host, labels fit, live text stays inside its card, bar value labels do not intersect category-axis labels, and the console is clean. Counting hosts is not a rendering check — look at it.
5. **Open it with scripts disabled.** Confirm fallbacks, tables, narrative, and source context are still readable and still say the same thing.
6. **Check desktop and narrow widths.** Every table card aligned to the reading column, narrow tables filling their card, wide tables scrolling inside their container, and the document itself never scrolling horizontally.
7. Fix clipping, overflow, long labels, inconsistent scales, or fallback values that disagree with the payload before handoff.

Fallback and payload disagreeing on a number is a shipped contradiction. Treat it as a blocker, not a polish item.
