# Core Web Vitals Triage

Three metrics, judged at the 75th percentile of real-user (field) data, per page group and per device.

| Metric | Good | Needs improvement | Poor | Measures |
|---|---|---|---|---|
| LCP, Largest Contentful Paint | <= 2.5 s | 2.5-4.0 s | > 4.0 s | When the main content shows |
| INP, Interaction to Next Paint | <= 200 ms | 200-500 ms | > 500 ms | Delay after clicks, taps, keys |
| CLS, Cumulative Layout Shift | <= 0.1 | 0.1-0.25 | > 0.25 | Unexpected layout jumps |

INP replaced FID as the responsiveness metric in March 2024. Ignore any report that still cites FID.

**Scorer mapping.** Good = `pass`. Needs improvement = `warn`. Poor = `fail`. A page group passes only when all three metrics pass. Log one check per metric, severity `high` (LCP: `critical` if poor on the main landing templates).

## Field data first

| Source | Type | Use |
|---|---|---|
| CrUX (Chrome UX Report), PageSpeed Insights "field" panel, Search Console CWV report | Field: 28-day rolling, real users | The verdict. This is what page experience reporting uses |
| Lighthouse, PageSpeed "lab" panel, WebPageTest | Lab: one synthetic run | Diagnosis only. A good lab score does not clear a poor field score |
| `web-vitals` library in the site's own analytics | Field, own data | Fills the gap when CrUX has too little traffic for a URL |

Low-traffic URLs have no CrUX data. Then test the origin-level numbers and the lab run, and mark the finding `inferred`.

## Triage by metric

### LCP above 2.5 s

First, find the LCP element (DevTools Performance panel, or PageSpeed diagnostics). Then split the time into four parts and fix the largest:

| Part | Slow means | Fix |
|---|---|---|
| Time to first byte | Server or redirect delay. Target under 0.8 s | Cache, CDN, trim redirects, faster backend |
| Resource load delay | LCP image discovered late | Preload it; do not lazy-load it; put it in HTML, not CSS or JS |
| Resource load time | Heavy file | AVIF/WebP, correct dimensions, `srcset`, CDN |
| Render delay | Blocked by CSS/JS or a font | Inline critical CSS, defer scripts, `font-display: swap` |

### INP above 200 ms

- Find the slow interaction (DevTools Performance, or field attribution from `web-vitals`).
- Split long tasks (over 50 ms) into smaller chunks; yield to the main thread.
- Defer or remove third-party scripts: tags, chat widgets, A/B tools. They are the usual cause.
- Cut work done on input: heavy handlers, large re-renders, layout thrash.
- Hydration cost on JS-heavy pages: ship less JS per route.

### CLS above 0.1

- Set `width` and `height` (or `aspect-ratio`) on images, video, iframes.
- Reserve fixed space for ads, embeds, cookie banners, late-loading widgets.
- Never insert content above existing content after load, except in reply to a user action.
- Match fallback and web font metrics; use `font-display: swap` with `size-adjust`.
- Animate with `transform`, not with properties that move layout.

## Report format

One row per page group and device:

| Page group | Device | LCP p75 | INP p75 | CLS p75 | Verdict | Worst offender | First fix |
|---|---|---|---|---|---|---|---|

Order fixes by (share of traffic on the page group) x (distance past the threshold). Fix the template once; one template change often moves a whole group.
