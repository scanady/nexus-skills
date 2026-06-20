---
name: html-style
description: 'Shared HTML style system for all four HTML presentation outputs produced by the project-architect skill. Defines the default brand color palette, typography, attribution requirement, HTML-specific compression rules, core chunked delivery protocol (Steps 1-3), interactive feature CSS class conventions, interactive JavaScript module responsibilities, DOMContentLoaded initialization checklists per report type, and filter bar HTML templates. All four report skills reference this skill for every formatting, CSS, JS, and attribution decision. Triggers: HTML style, HTML presentation, HTML theme, interactive features, CSS class conventions, JS module, attribution credit, chunk delivery, filter bar.'
argument-hint: 'Reference this skill when building any HTML presentation output. Apply all rules here before writing any HTML.'
---

# HTML Style  -  Shared Presentation Standard

## Role Context

This skill defines every shared formatting, CSS, JavaScript, and delivery rule that applies to **all four** HTML presentation outputs:

- **Output 1**: 1-Page Executive Overview (`report-executive-overview`)  -  static HTML, no JS
- **Output 2**: C-Level 3-Page Overview (`report-clevel-deck`)  -  Pattern B sidebar (`<nav id="sb">`, `body.sb-off` collapse)
- **Output 3**: Full Technical Implementation Plan (`report-technical-plan`)  -  Pattern A sidebar (`<div id="sb">`, `.col` collapse)
- **Output 4**: Per-Team Impact Deck (`report-team-impact-deck`)  -  Pattern A sidebar, same as Output 3

Outputs 3 and 4 share the same sidebar DOM and collapse mechanism. Output 2 uses a different sidebar DOM and collapse. Output 1 has no sidebar.

---

## 1. Default Brand Visual Identity

> **Configurable**: The values below are defaults. Replace with your organization's brand colors, fonts, and identity tokens before use.

| Element | Output 1 & 2 | Output 3 & 4 |
|---------|-------------|--------------|
| Primary navy | `#002D62` | `#002D62` |
| Dark navy | `#001A3D` | `#001A3D` |
| Accent navy | `#004A9F` | `#004A9F` |
| Gold accent | `#FFD700` | `#FFD700` |
| Page background | `#F5F7FA` | `#f4f6f9` |
| Steel blue | `#9BBFE4` | `#9BBFE4` |
| Heading font | `Georgia, serif` | `Georgia, serif` |
| Body font | `Helvetica Neue, Arial` | `Arial, sans-serif` |
| Table `<th>` | `background:#002D62; color:#fff; padding:6px 10px; font-size:11px; text-align:left` | same |
| Callout `.info` | `background:#EBF3FF; border-left:4px solid #002D62; padding:11px 14px; font-size:12px` | same |
| Callout `.warn` | `background:#FFF8E1; border-left:4px solid #F9A825` | same |
| Section gradient | `background:linear-gradient(135deg,#001A3D 0%,#002D62 100%)` (Output 2) | `background:linear-gradient(135deg,#002D62 0%,#004A9F 100%)` |

**Sidebar logo templates:**

Output 3 & 4 (Pattern A):
```html
<div id="sb-logo">[ORGANIZATION] - [TEAM]<br><span style="font-size:10px;opacity:.6;font-weight:400">Subtitle</span></div>
```

Output 2 (Pattern B):
```html
<div class="logo">[Organization]<span>Subtitle</span></div>
```

---

## 2. Attribution Requirement

Every HTML presentation must include both of these lines, visually distinct from content:

```
Created By: Data Architecture
Created Date: YYYY.MM.DD
```

**Sidebar presentations (Outputs 2, 3 and 4):** Place at the absolute bottom of the sidebar as a `.sb-credit` block:
```css
.sb-credit{padding:10px;font-size:10px;color:rgba(255,255,255,.35);border-top:1px solid rgba(255,255,255,.12);margin-top:auto}
```

**Single-page (Output 1):** Place in a centered `.doc-credit` div after `.doc-footer`:
```html
<div class="doc-credit">Created By: Data Architecture &nbsp;&middot;&nbsp; Created Date: 2026.05.07</div>
```
```css
.doc-credit{margin-top:8px;font-size:10px;color:#888;text-align:center}
```

---

## 3. HTML-Specific Compression Rules (H-1 through H-7)

Apply ALL H-rules before writing any HTML section content. HTML outputs are the largest artifact type and most prone to response truncation.

| Rule | Requirement |
|------|-------------|
| **H-1: Tables, not lists** | Any structured data with 3+ rows and 2+ columns MUST be a `<table>`, not a `<ul>` or prose |
| **H-2: Collapse long content** | Any content block with more than 5 items or 100 words MUST use `<details><summary>Label</summary>content</details>` to collapse by default |
| **H-3: Inline CSS only** | All styles in a single `<style>` block in `<head>`. No `<link rel="stylesheet">`. No external stylesheets. No inline `style=""` except for dynamically-set values. |
| **H-4: No placeholder sections** | Never write a section skeleton with "content follows". Either write the full section or omit it and defer per the deferral rules in the relevant report skill. |
| **H-5: Compress table prose** | Every table cell: <=15 words. No sentence-length cells. Use a nested `<details>` if more detail is required. |
| **H-6: No redundant headings** | Do not repeat a section title as both a sidebar nav label AND a `<h2>` in the content AND a `.pg-hdr` title. Use only the `.pg-hdr` heading; omit standalone `<h2>` if `.pg-hdr` is present. |
| **H-7: Structural discipline** | Every `<div>` opened in a chunk MUST be closed in the same chunk OR explicitly documented as intentionally left open for a named subsequent chunk to close. Never silently leave tags open. |

---

## 4. Chunked Delivery Protocol (Steps 1-3)

Use this protocol whenever a single HTML output must span multiple model responses.

### Step 1  -  Announce the Chunk Plan (BEFORE Chunk 1)

Before writing any HTML, output a plain-text chunk plan in this format:

```
## Chunk Plan - [Output Name]

This output will be delivered in [N] chunks:

| Chunk | Sections | Approx. Content |
|-------|----------|-----------------|
| 1     | [sections] | [description] |
| 2     | [sections] | [description] |
...

Chunk 1 begins below.
```

### Step 2  -  Continuation Header Format (Chunks 2+)

Every chunk after Chunk 1 begins with:

```html
<!-- ============================================================ -->
<!-- CHUNK [N] OF [TOTAL] - Continuing [Output Name]         -->
<!-- Open elements from prior chunk: [list or "none"]            -->
<!-- ============================================================ -->
```

### Step 3  -  Final Chunk Close

The final chunk MUST close all open HTML elements in this exact order:
1. `</div><!-- #mc -->`  -  Pattern A only; only if `#mc` was opened in Chunk 1 and not yet closed
2. `<button id="btt" ...>...</button>`
3. `<div id="gst-wrap"><div id="gst"></div></div>` (if sidebar search is present)
4. `</div><!-- body wrapper -->` (if an outer wrapper div was used)
5. `<script>...</script>` block with all JS inline
6. `</body></html>`

**Critical rule for Pattern A:** Never close `#mc` in Chunk 1. Only the final chunk closes `#mc`.

---

## 5. Sidebar Navigation Patterns

### Pattern A  -  Outputs 3 & 4 (`<div id="sb">`, `.col` collapse)

```html
<div id="sb">
  <div id="sb-logo">[ORGANIZATION] - [TEAM]<br><span style="font-size:10px;opacity:.6;font-weight:400">Subtitle</span></div>
  <div id="sb-search">
    <input id="gsi" type="text" placeholder="Search..." oninput="gSearch(this.value)">
  </div>
  <nav id="sb-nav">
    <div class="ng">Group Label</div>
    <a id="n01" href="#s01" class="act">S01 - Section Name</a>
    <a id="n02" href="#s02">S02 - Section Name</a>
    <!-- ... -->
  </nav>
  <button id="sbt" class="sb-tog" onclick="sbToggle()">&#9776;</button>
  <div class="sb-credit">Created By: Data Architecture<br>Created Date: YYYY.MM.DD</div>
</div>
<div id="mc">
  <!-- All .sec divs go here; #mc stays open until final chunk -->
```

**Collapse:** `sbToggle()` toggles `.col` on both `#sb` and `#mc`:
```javascript
function sbToggle(){
  document.getElementById('sb').classList.toggle('col');
  document.getElementById('mc').classList.toggle('col');
}
```
```css
#sb{width:220px;min-height:100vh;transition:width .25s;overflow:hidden}
#mc{margin-left:220px;transition:margin-left .25s}
#sb.col{width:0}
#mc.col{margin-left:0}
```

### Pattern B  -  Output 2 (`<nav id="sb">`, `body.sb-off` collapse)

```html
<nav id="sb">
  <div class="logo">[Organization]<span>Subtitle</span></div>
  <div id="gst"><input id="gsi" type="text" placeholder="Search..." oninput="gSearch(this.value)"></div>
  <div class="ng">Sections</div>
  <a id="n01" href="#s01" class="act" onclick="go(1)">Section 1 Name</a>
  <a id="n02" href="#s02" onclick="go(2)">Section 2 Name</a>
  <a id="n03" href="#s03" onclick="go(3)">Section 3 Name</a>
  <button class="sb-tog" onclick="sbToggle()">&#9776;</button>
  <div class="sb-credit">Created By: Data Architecture<br>Created Date: YYYY.MM.DD</div>
</nav>
<div id="main">
  <!-- .sec divs; first has class="sec pg-act" -->
</div>
```

**Collapse:** `sbToggle()` toggles `body.sb-off`:
```javascript
function sbToggle(){document.body.classList.toggle('sb-off');}
```

---

## 6. Section Page Header  -  `.pg-hdr` (Output 2, Pattern B)

Hardcoded in HTML for each section in Output 2  -  NOT injected by JS. Uses Pattern B structure.

```html
<div class="pg-hdr">
  <div class="ph-top">
    <div class="ph-grp">Initiative Name &nbsp;&middot;&nbsp; Category</div>
    <div class="ph-num">01 / 03</div>
  </div>
  <div class="ph-title">Section Title</div>
  <div class="ph-ov">One-sentence section overview.</div>
</div>
```

```css
.pg-hdr{background:linear-gradient(135deg,#001A3D 0%,#002D62 100%);color:#fff;padding:28px 32px 22px;border-radius:8px 8px 0 0;margin-bottom:0}
.ph-top{display:flex;justify-content:space-between;font-size:10px;opacity:.65;margin-bottom:8px;text-transform:uppercase;letter-spacing:.08em}
.ph-title{font-family:Georgia,serif;font-size:24px;font-weight:700;margin-bottom:6px}
.ph-ov{font-size:13px;opacity:.8;font-style:italic}
```

---

## 7. C-Level Review Panel  -  `.clv` (Output 2 only)

Two variants exist. **Output 2 uses `.clv-lbl` exclusively** (with `::before` horizontal rule label).

**`.clv-lbl` variant** (standard for Output 2):
```html
<div class="clv clv-lbl" data-lbl="Executive Summary">
  <p>Panel content here.</p>
</div>
```

**`.clv-h` variant** (heading-based; not used in Output 2):
```html
<div class="clv clv-h">
  <h3>Panel Heading</h3>
  <p>Panel content here.</p>
</div>
```

```css
.clv{background:#fff;border:1px solid #e2e8f0;border-radius:6px;padding:20px 24px;margin:16px 0}
.clv-lbl{position:relative;padding-top:28px}
.clv-lbl::before{content:attr(data-lbl);position:absolute;top:-1px;left:16px;background:#002D62;color:#fff;font-size:9px;text-transform:uppercase;letter-spacing:.1em;padding:3px 10px;border-radius:0 0 4px 4px}
```

---

## 8. Section Structure  -  `.sec`

All content sections in Outputs 2, 3, and 4 use this pattern:

```html
<div id="s01" class="sec pg-act">
  <!-- Output 2 only: hardcoded .pg-hdr here -->
  <div class="sec-body">
    <!-- section content -->
  </div>
</div>
<div id="s02" class="sec">
  ...
</div>
```

- First visible section: `class="sec pg-act"`  -  all others: `class="sec"`
- **Output 2 (Pattern B):** `go(n)` toggles `pg-act` for section switching; sections are hidden when not active
- **Outputs 3 & 4 (Pattern A):** All sections visible simultaneously; `pg-act` not used for visibility control

---

## 9. Required Interactive Features by Output

| Feature | Output 1 | Output 2 | Output 3 | Output 4 |
|---------|----------|----------|----------|----------|
| Sidebar navigation |  -  | Pattern B | Pattern A | Pattern A |
| Sidebar collapse (`sbToggle`) |  -  | Yes | Yes | Yes |
| Section switching (`go(n)`) |  -  | Yes |  -  |  -  |
| Global search (`gSearch`) |  -  | Yes | Yes | Yes |
| Back-to-top button (`#btt`) |  -  | Yes | Yes | Yes |
| Sidebar search box (`#gst`) |  -  | Yes | Yes | Yes |
| Filter bar |  -  |  -  | Yes | Yes |
| `body.page-mode` |  -  |  -  | Yes | Yes |
| Active nav highlight on scroll |  -  |  -  | Yes | Yes |
| DOMContentLoaded block |  -  |  -  | Yes | Yes |

---

## 10. CSS Class Conventions

| Class | Element | Purpose |
|-------|---------|---------|
| `.sec` | `<div>` | Content section wrapper |
| `.pg-act` | `.sec` | Active/visible section (Output 2 section switching) |
| `.sec-body` | `<div>` | Section body padding wrapper |
| `.sec-badge` | `<span>` | Section category badge (top-left label) |
| `.ng` | `<div>` | Navigation group label in sidebar |
| `.act` | `<a>` in sidebar | Currently active nav link |
| `.sr-hide` | any | Hidden by search or filter; use `classList.toggle` — never `style.display` |
| `.col` | `#sb`, `#mc` | Collapsed sidebar (Pattern A only) |
| `.sb-off` | `<body>` | Collapsed sidebar (Pattern B only) |
| `.sb-tog` | `<button>` | Sidebar collapse toggle button |
| `.sb-credit` | `<div>` | Attribution block at sidebar bottom |
| `.info` | `<div>` | Info callout (blue left border) |
| `.warn` | `<div>` | Warning callout (amber left border) |
| `.clv` | `<div>` | C-Level review panel (Output 2 only) |
| `.clv-lbl` | `.clv` modifier | `.clv` with `::before` rule label |
| `.clv-h` | `.clv` modifier | `.clv` with heading |
| `.pg-hdr` | `<div>` | Section page header (Output 2, hardcoded) |
| `.ph-top` / `.ph-grp` / `.ph-num` | `.pg-hdr` children | Page header metadata row |
| `.ph-title` / `.ph-ov` | `.pg-hdr` children | Page header title and overview |
| `.filter-btn` | `<button>` | Filter bar button |
| `.filter-btn.active` | `.filter-btn` | Currently selected filter |
| `.sr-row` | `<tr>` or `<div>` | Searchable/filterable row element |

---

## 11. JavaScript Module Responsibilities

| Function | Outputs | Responsibility |
|----------|---------|----------------|
| `go(n)` | 2 | Remove `pg-act` from all `.sec`; add to `#s0n`; update `.act` on nav links; scroll to top |
| `sbToggle()` | 2,3,4 | Toggle sidebar: Pattern A -> `.col` on `#sb`+`#mc`; Pattern B -> `body.sb-off` |
| `gSearch(q)` | 2,3,4 | Toggle `.sr-hide` on `.sr-row` elements that don't contain the query string |
| `buildSectionHeaders()` | 3,4 | Inject `.pg-hdr` content into each `.sec` from a JS data array (Pattern A only) |
| `filterBy(cat)` | 3,4 | Show only `.sr-row` elements where `data-cat` matches; update `.active` on filter buttons |
| `highlightActive()` | 3,4 | On scroll: detect which section is in viewport; set `.act` on corresponding sidebar `<a>` |
| Scroll handler | 2,3,4 | Show/hide `#btt` based on `window.scrollY`; call `highlightActive()` (Outputs 3 & 4 only) |

---

## 12. DOMContentLoaded Initialization  -  Pattern A (Outputs 3 & 4)

```javascript
document.addEventListener('DOMContentLoaded', function() {
  // 1. Inject section page headers
  buildSectionHeaders();

  // 2. Initialize filter bar (show all)
  filterBy('all');

  // 3. Register scroll handler
  window.addEventListener('scroll', function() {
    document.getElementById('btt').style.opacity = window.scrollY > 100 ? '1' : '0';
    highlightActive();
  });

  // 4. Set first nav item active
  document.getElementById('n01').classList.add('act');
});
```

**Pattern B has NO DOMContentLoaded block.** Use instead:
```javascript
window.addEventListener('scroll', function() {
  document.getElementById('btt').style.opacity = window.scrollY > 100 ? '1' : '0';
});
document.getElementById('n01').classList.add('act');
```

---

## 13. Filter Bar HTML Template (Outputs 3 & 4)

Place the filter bar immediately inside `#mc`, before the first `.sec` div:

```html
<div id="filter-bar">
  <button class="filter-btn active" onclick="filterBy('all')">All</button>
  <button class="filter-btn" onclick="filterBy('de')">DE</button>
  <button class="filter-btn" onclick="filterBy('aie')">AIE</button>
  <button class="filter-btn" onclick="filterBy('mta')">MTA</button>
  <button class="filter-btn" onclick="filterBy('plt')">PLT</button>
  <!-- Add/remove team buttons to match the delivery teams in the plan -->
</div>
```

```css
#filter-bar{display:flex;flex-wrap:wrap;gap:6px;padding:12px 16px;background:#f0f4f8;border-bottom:1px solid #dde3ea;position:sticky;top:0;z-index:10}
.filter-btn{padding:4px 12px;font-size:11px;border:1px solid #c5d0dc;border-radius:12px;background:#fff;cursor:pointer;color:#445566}
.filter-btn.active{background:#002D62;color:#fff;border-color:#002D62}
```

```javascript
function filterBy(cat) {
  document.querySelectorAll('.filter-btn').forEach(function(b) {
    b.classList.toggle('active', cat === 'all' || b.textContent.trim().toLowerCase() === cat);
  });
  document.querySelectorAll('.sr-row').forEach(function(row) {
    row.classList.toggle('sr-hide', cat !== 'all' && row.dataset.cat !== cat);
  });
}
```

---

## 14. `gSearch()` Implementation

```javascript
function gSearch(q) {
  q = q.toLowerCase().trim();
  document.querySelectorAll('.sr-row').forEach(function(row) {
    row.classList.toggle('sr-hide', q.length > 0 && !row.textContent.toLowerCase().includes(q));
  });
}
```

**Rules:**
- Apply `.sr-hide` via `classList.toggle`  -  **never `style.display`**
- Search is additive with filter: both `sr-hide` conditions may apply to the same element simultaneously
- Searchable rows must carry class `sr-row`

---

## 15. `go(n)` Implementation (Output 2  -  Pattern B only)

```javascript
function go(n) {
  document.querySelectorAll('.sec').forEach(function(s) { s.classList.remove('pg-act'); });
  document.getElementById('s0' + n).classList.add('pg-act');
  document.querySelectorAll('nav a').forEach(function(a) { a.classList.remove('act'); });
  document.getElementById('n0' + n).classList.add('act');
  window.scrollTo({top: 0, behavior: 'smooth'});
}
```

---

## 16. HTML Structural Integrity Checklist

Verify all items before delivering any HTML output:

- [ ] `<meta charset="UTF-8">` is the **first** tag inside `<head>`
- [ ] `<meta name="viewport" content="width=device-width,initial-scale=1">` present
- [ ] No raw Unicode special characters  -  all encoded as HTML entities (see html-presentation-maker for entity reference table)
- [ ] All `<div>`, `<nav>`, and `<section>` elements properly closed; no orphaned tags
- [ ] All CSS in a single `<style>` block in `<head>`  -  no inline `style=""` except dynamically-set values
- [ ] All JS in a single `<script>` block immediately before `</body>`  -  no `<script>` in `<head>`
- [ ] No `<link>` to external CSS or JS files; fully self-contained
- [ ] Attribution credit block present: `.sb-credit` (sidebar outputs) or `.doc-credit` (Output 1)
- [ ] Correct sidebar DOM pattern: Pattern A (`<div id="sb">`) for Outputs 3 & 4; Pattern B (`<nav id="sb">`) for Output 2; none for Output 1
- [ ] `body.page-mode` class present on Outputs 3 & 4; absent on Outputs 1 & 2
- [ ] Filter bar (`#filter-bar`) present on Outputs 3 & 4; absent on Outputs 1 & 2
- [ ] All section `id` attributes: `s01`, `s02`, ... format
- [ ] All sidebar nav link `id` attributes: `n01`, `n02`, ... format
- [ ] `#btt` back-to-top button present on all sidebar outputs (2, 3, 4)
- [ ] `#gst` sidebar search input present on all sidebar outputs (2, 3, 4)
- [ ] No placeholder text (`[TBD]`, `[Insert here]`, `TODO`) in any deliverable output
- [ ] Organization brand identity applied per Section 1: color palette, typography, brand header
