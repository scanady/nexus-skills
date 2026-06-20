---
name: html-presentation-maker
description: 'HTML Presentation Maker skill. Use when creating, editing, or auditing self-contained single-file HTML presentations. Covers organization branding, the standard sidebar nav template, approved color palette, typography stack, interactive JavaScript navigation, and the mandatory character-encoding rules that prevent garbled special characters. Triggers: html presentation, create html deck, html slide, presentation document, data architecture document, marketing platform document, html report, styled html, interactive html, sidebar navigation.'
argument-hint: 'Describe the presentation topic, intended audience, and any sections or data to include. Specify if updating an existing presentation.'
---

# HTML Presentation Maker

## Role Context
Produces and maintains polished, professional, self-contained single-file HTML presentations. Presentations are used internally by technology, data, and marketing leadership. They open directly in a browser — no server, no build step. All CSS and JavaScript is inline. Every presentation must be production-ready the first time: correct encoding, clean rendering, consistent brand, and fully interactive navigation.

---

## 1. Mandatory Encoding Rules (Zero-Tolerance)

**This is the most common failure mode. It must be enforced on every file, every time.**

### Rule E-1: Always declare UTF-8 charset
```html
<meta charset="UTF-8">
```
Must be the **first** tag inside `<head>`. No exceptions.

### Rule E-2: Never paste raw Unicode special characters into HTML source
Special characters must use HTML entities in HTML markup and CSS unicode escapes in CSS `content:` properties.

**Approved HTML entity substitutions:**

| Character | Correct | Never use |
|-----------|---------|-----------|
| em dash — | ` - ` | `—` (raw) or `â€"` (garbled) |
| en dash – | `-` | `–` (raw) or `â€"` (garbled) |
| right arrow → | `->` | `→` (raw) or `â†'` (garbled) |
| left arrow ← | `<-` | `←` (raw) |
| multiplication × | `&times;` | `×` (raw) or `Ã—` (garbled) |
| middle dot · | `&middot;` | `·` (raw) or `Â·` (garbled) |
| right single quote ' | `'` | `'` (raw) or `â€™` (garbled) |
| left single quote ' | `'` | `'` (raw) or `â€˜` (garbled) |
| left double quote " | `"` | `"` (raw) |
| right double quote " | `"` | `"` (raw) |
| ellipsis … | `...` | `…` (raw) or `â€¦` (garbled) |
| non-breaking space | `&nbsp;` | ` ` (raw NBSP) |
| ampersand & | `&amp;` | `&` in attributes |
| Organization (separator) | `&middot;` | garbled form |

### Rule E-3: CSS `content:` values use CSS unicode escapes
```css
/* CORRECT */
.item::before { content: '\2014'; }   /* em dash */
.item::before { content: '\25C6'; }   /* ◆ diamond */
.item::before { content: '\25B8'; }   /* ▸ small right triangle */
.item::before { content: '\00B7'; }   /* · middle dot */

/* WRONG — will produce garbled output */
.item::before { content: '—'; }
.item::before { content: '&mdash;'; }
```

### Rule E-4: Save files with UTF-8 BOM using PowerShell
```powershell
$utf8bom = New-Object System.Text.UTF8Encoding($true)
[System.IO.File]::WriteAllText($path, $content, $utf8bom)
```
Do NOT use `Set-Content` or `Out-File` without explicit encoding — they default to system encoding.

### Rule E-5: Audit after every edit
After generating or editing an HTML file, check for the following garbled patterns (all must be absent):
- `â€"` `â€™` `â€˜` `â€œ` (double-encoded curly quotes / em dash)
- `â†'` (double-encoded arrow)
- `Ã—` (double-encoded ×)
- `Â·` (double-encoded middle dot)
- Any sequence starting with `Ã¢â‚¬` or `Ãƒ`

---

## 2. Brand Standards

### Identity line
- **Organization label**: `[Organization] &middot; [Team]` (e.g., `Data Architecture`, `Marketing Technology`)
- **Product / document name**: Sentence case, serif font (see Typography)
- **Sub-label**: document type, version, year

### Brand copy rules
- Use the organization's canonical name consistently; define it once in the presentation header
- Separator is `&middot;` (middle dot), not slash or pipe
- Section badges use `text-transform:uppercase` at `font-size:9px` — never shout in descriptive text

### Approved badge colors

| Badge variant | Background | Text color | CSS class |
|--------------|-----------|-----------|-----------|
| Default / blue | `var(--blue-light)` | `var(--blue)` | `.sec-badge` |
| Amber / warning | `var(--amber-bg)` | `var(--amber)` | `.sec-badge.amber` |
| Green / success | `var(--green-bg)` | `var(--green)` | `.sec-badge.green` |
| Violet / AI | `var(--violet-bg)` | `var(--violet)` | `.sec-badge.violet` |

---

## 3. Standard Color Palette

Define these CSS custom properties in `:root`. Do NOT deviate from these values.

```css
:root {
  --sidebar-w: 220px;
  --navy:    #0f172a;
  --navy-2:  #1e293b;
  --navy-3:  #334155;
  --bg:      #f8fafc;
  --surface: #ffffff;
  --border:  #e2e8f0;
  --border-2:#cbd5e1;
  --text:    #0f172a;
  --text-2:  #475569;
  --text-3:  #94a3b8;
  --blue:    #2563eb;
  --blue-light: #eff6ff;
  --blue-mid:   #bfdbfe;
  --amber:   #b45309;
  --amber-bg:#fffbeb;
  --amber-border: #fde68a;
  --green:   #065f46;
  --green-bg:#ecfdf5;
  --green-border: #a7f3d0;
  --violet:  #4c1d95;
  --violet-bg:#f5f3ff;
  --violet-border: #ddd6fe;
  --red:     #7f1d1d;
  --red-bg:  #fef2f2;
  --red-border: #fecaca;
  --radius:  8px;
  --radius-lg: 12px;
}
```

---

## 4. Typography Stack

```css
/* Google Fonts import — always include both */
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Serif+Display&display=swap" rel="stylesheet">

body        { font-family: 'DM Sans', sans-serif; font-size: 13px; line-height: 1.55; }
h1, .sec-h1 { font-family: 'DM Serif Display', serif; font-size: 28px; }
```

**Do NOT use system fonts, fallback stacks without DM Sans, or fonts not in the approved list.**

---

## 5. Standard Sidebar Navigation Template

Every presentation uses a fixed left sidebar. Copy this template verbatim and replace navigation items.

```html
<nav class="sidebar">
  <div class="sidebar-logo">
    <div class="logo-org">[Organization] &middot; [Team]</div>
    <div class="logo-title"><!-- Presentation Title --></div>
    <div class="logo-sub"><!-- Subtitle &middot; Version &middot; Year --></div>
  </div>

  <!-- Repeat nav-group blocks for each logical group of sections -->
  <div class="nav-group">
    <div class="nav-group-label"><!-- Group Label --></div>
    <div class="nav-item active" onclick="goTo('sectionId')">
      <span class="nav-icon"><!-- APPROVED ICON (see §6) --></span><!-- Label -->
    </div>
  </div>

  <div class="sidebar-bottom">v<!-- N --> &middot; <!-- doc descriptor --><br>Updated <!-- Month Year --></div>
</nav>
```

### Required CSS for sidebar
```css
*  { box-sizing: border-box; margin: 0; padding: 0; }
body { display: flex; min-height: 100vh; }
.sidebar { position: fixed; top: 0; left: 0; width: var(--sidebar-w); height: 100vh;
  background: var(--navy); display: flex; flex-direction: column; z-index: 200; overflow-y: auto; }
.sidebar-logo { padding: 22px 18px 16px; border-bottom: 1px solid var(--navy-2); }
.logo-org     { font-size: 10px; font-weight: 600; letter-spacing: .12em; text-transform: uppercase; color: #64748b; }
.logo-title   { font-family: 'DM Serif Display', serif; font-size: 15px; color: #f1f5f9; line-height: 1.3; margin-top: 3px; }
.logo-sub     { font-size: 10px; color: #475569; margin-top: 3px; }
.nav-group    { padding: 16px 0 4px; }
.nav-group-label { padding: 0 18px 6px; font-size: 9px; font-weight: 600; letter-spacing: .12em; text-transform: uppercase; color: #334155; }
.nav-item     { display: flex; align-items: center; gap: 9px; padding: 8px 18px; font-size: 12px; color: #64748b; cursor: pointer; transition: all .15s; border-left: 2px solid transparent; }
.nav-item:hover  { color: #cbd5e1; background: var(--navy-2); }
.nav-item.active { color: #f1f5f9; background: var(--navy-2); border-left-color: var(--blue); font-weight: 500; }
.nav-icon     { font-size: 12px; width: 16px; text-align: center; flex-shrink: 0; }
.sidebar-bottom { margin-top: auto; padding: 14px 18px; border-top: 1px solid var(--navy-2); font-size: 10px; color: #334155; line-height: 1.5; }
.main { margin-left: var(--sidebar-w); padding: 36px 48px; flex: 1; min-width: 0; max-width: 1200px; }
.section { display: none; }
.section.active { display: block; }
```

---

## 6. Approved Navigation Icons

Nav icons must be rendered using HTML entities (numeric or named). **Never paste raw Unicode glyphs into source.** The icon appears inside `<span class="nav-icon">...</span>`.

| Use case | Entity | Character | Notes |
|----------|--------|-----------|-------|
| Overview / dashboard | `&#x25C8;` | ◈ | Default first nav item |
| Signals / data domains | `&#x25CE;` | ◎ | |
| Identity / profile | `&#x25C9;` | ◉ | |
| Architecture / grid | `&#x229E;` | ⊞ | Layout/structure topics |
| Capabilities / list | `&#x229F;` | ⊟ | |
| Patterns / plus | `&#x2295;` | ⊕ | |
| Data Vault / multiply | `&#x2297;` | ⊗ | Data modeling |
| Blueprint / circle X | `&#x2298;` | ⊘ | Platform / system design |
| Governance / tools | `&#x2692;` | ⚒ | Governance, compliance |
| Roadmap / play | `&#x25B7;` | ▷ | Roadmap, next steps |
| Settings / star | `&#x2605;` | ★ | Configuration |
| Alert / warning | `&#x26A0;` | ⚠ | Risk, issues |
| Summary / square | `&#x25A0;` | ■ | Executive summary |
| Options / check | `&#x2610;` | ☐ | Decision framework |
| Cost / dollar | `$` | $ | Cost reference (literal) |

**Do not use:**
- Emoji (🚀 📊 ✅ etc.) — unprofessional in enterprise documents
- Font Awesome or icon library CDN classes — no external icon dependencies
- Inline SVGs in nav items — too verbose for nav icons
- Empty boxes or question marks as production icons

---

## 7. Interactive Navigation JavaScript

Every presentation requires this JavaScript block placed before `</body>`. This is the ONLY JavaScript needed for basic section navigation. Do not add frameworks or CDN-loaded scripts.

```html
<script>
function goTo(id) {
  document.querySelectorAll('.section').forEach(function(s) { s.classList.remove('active'); });
  document.querySelectorAll('.nav-item').forEach(function(n) { n.classList.remove('active'); });
  var sec = document.getElementById('sec-' + id);
  if (sec) sec.classList.add('active');
  var nav = document.querySelector('[onclick="goTo(\'' + id + '\')"]');
  if (nav) nav.classList.add('active');
}
</script>
```

### Section naming convention
- Section element: `<section class="section" id="sec-SECTIONID">`
- Nav item: `onclick="goTo('SECTIONID')"`
- First section gets `class="section active"` at page load

### Optional: interactive tables, toggles and tabs
For interactivity beyond navigation, add self-contained JavaScript only using DOM APIs. No jQuery, no external libraries. Keep all JavaScript at the bottom of `<body>`.

---

## 8. Standard Section Structure

Every content section follows this skeleton:

```html
<section class="section" id="sec-SECTIONID">
  <div class="sec-badge"><!-- Short category label --></div>
  <h1 class="sec-h1"><!-- Section Title --></h1>
  <p class="sec-desc"><!-- 1–3 sentence description, max 680px wide --></p>
  <hr class="sec-divider">
  <!-- content -->
</section>
```

Required CSS:
```css
.sec-badge  { display: inline-block; padding: 3px 10px; border-radius: 100px; font-size: 10px; font-weight: 700; letter-spacing: .07em; text-transform: uppercase; background: var(--blue-light); color: var(--blue); margin-bottom: 10px; }
.sec-h1     { font-family: 'DM Serif Display', serif; font-size: 28px; line-height: 1.2; }
.sec-desc   { font-size: 13px; color: var(--text-2); margin-top: 8px; max-width: 680px; line-height: 1.7; }
.sec-divider{ border: none; border-top: 1px solid var(--border); margin: 24px 0; }
```

---

## 9. Table and Grid Column Alignment

**Rule A-1: All repeating row components sharing a visual column layout must use identical, fixed column widths — never `auto`.**

When multiple cards, rows, or tiles stack vertically and each contains the same columnar structure (e.g., a name column, a description column, and an outcome column), every instance must use the same `grid-template-columns` definition with explicit fixed or fractional widths. Using `auto` for any shared column causes that column to size independently per row, making vertical borders and edges misalign across rows — producing a "staircase" effect on dividers.

```css
/* WRONG — auto sizes each row's third column independently */
.pat-header { grid-template-columns: 200px 1fr auto; }

/* CORRECT — fixed width keeps the right column border aligned across all rows */
.pat-header { grid-template-columns: 200px 1fr 200px; }
```

**Rule A-2: Fixed-width columns should not also carry `min-width`.** When the column is defined with an explicit pixel width in `grid-template-columns`, `min-width` on the cell is redundant and can override the grid definition, causing misalignment. Remove it.

**Rule A-3: Shared-column text should use consistent alignment.** All cells in the same logical column across rows must use the same `text-align` and `justify-content` values. Mixed alignment across rows (center in one, left-aligned in another) makes the column look unintentional.

```css
/* Outcome / summary column — consistent center alignment */
.pat-outcome-col {
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  /* No min-width when column width is fixed in grid-template-columns */
}
```

**Rule A-4: `<table>` elements must define explicit column widths.** Use `<colgroup>` or `width` attributes on `<th>` elements to prevent browsers from sizing columns to content, which produces ragged borders in multi-row tables.

```css
/* Fixed-layout table — enforces declared widths */
.doc-table { table-layout: fixed; width: 100%; }
```

**Checklist for any new repeating-row layout:**
- [ ] `grid-template-columns` has no `auto` in positions that should align vertically across rows
- [ ] No `min-width` on cells whose grid column is already fixed-width
- [ ] All cells in the same logical column share `text-align` / `justify-content`
- [ ] Tables use `table-layout: fixed` with `<th>` widths declared

---

## 10. Print and Responsive Support

Always include these media queries at the end of the `<style>` block:

```css
@media print {
  .sidebar { display: none; }
  .main    { margin: 0; padding: 20px; }
  .section { display: block !important; page-break-after: always; }
}
@media (max-width: 900px) {
  .main    { margin-left: 0; padding: 20px; }
  .sidebar { display: none; }
  /* Collapse multi-column grids to 1 or 2 columns on mobile */
  .two-col, .three-col, .four-col { grid-template-columns: 1fr; }
}
```

---

## 11. Info / Warning / Highlight Boxes

Use consistently for callouts:

```html
<!-- Blue info box -->
<div class="info-box"><strong>Label:</strong> Body text.</div>

<!-- Amber warning box -->
<div class="warn-box"><strong>Label:</strong> Body text.</div>

<!-- Green new/positive box -->
<div class="new-box"><strong>Label:</strong> Body text.</div>
```

```css
.info-box { background: var(--blue-light); border: 1px solid var(--blue-mid);     border-radius: var(--radius); padding: 13px 16px; font-size: 12px; color: #1e40af; line-height: 1.65; margin-bottom: 16px; }
.warn-box { background: var(--amber-bg);   border: 1px solid var(--amber-border); border-radius: var(--radius); padding: 13px 16px; font-size: 12px; color: #92400e; line-height: 1.65; margin-bottom: 16px; }
.new-box  { background: #f0fdf4;           border: 1px solid #bbf7d0;             border-radius: var(--radius); padding: 13px 16px; font-size: 12px; color: #166534; line-height: 1.65; margin-bottom: 16px; }
```

---

## 12. Minimal Full-File Skeleton

When creating a new presentation from scratch, start from this skeleton:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>[Organization] &middot; <!-- Presentation Title --></title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Serif+Display&display=swap" rel="stylesheet">
<style>
/* === PASTE FULL CSS BLOCK HERE === */
/* Include: reset, :root vars, sidebar/main/section/nav, all component styles, media queries */
</style>
</head>
<body>

<!-- SIDEBAR -->
<nav class="sidebar">
  <div class="sidebar-logo">
    <div class="logo-org">[Organization] &middot; <!-- Team --></div>
    <div class="logo-title"><!-- Title --></div>
    <div class="logo-sub"><!-- Subtitle --></div>
  </div>
  <div class="nav-group">
    <div class="nav-group-label"><!-- Group --></div>
    <div class="nav-item active" onclick="goTo('overview')"><span class="nav-icon">&#x25C8;</span>Overview</div>
  </div>
  <div class="sidebar-bottom">v1 &middot; <!-- Description --><br><!-- Month Year --></div>
</nav>

<!-- MAIN CONTENT -->
<main class="main">

<section class="section active" id="sec-overview">
  <div class="sec-badge"><!-- Category --></div>
  <h1 class="sec-h1"><!-- Title --></h1>
  <p class="sec-desc"><!-- Description --></p>
  <hr class="sec-divider">
  <!-- Content here -->
</section>

</main>

<script>
function goTo(id) {
  document.querySelectorAll('.section').forEach(function(s) { s.classList.remove('active'); });
  document.querySelectorAll('.nav-item').forEach(function(n) { n.classList.remove('active'); });
  var sec = document.getElementById('sec-' + id);
  if (sec) sec.classList.add('active');
  var nav = document.querySelector('[onclick="goTo(\'' + id + '\')"]');
  if (nav) nav.classList.add('active');
}
</script>
</body>
</html>
```

---

## 14. Large Presentation Chunking Protocol

**When to use:** Any presentation with 6 or more sections, or any presentation whose estimated HTML body exceeds ~600 lines. Generating the full file in a single `create_file` call risks a response-length timeout that silently truncates the file — often mid-section, producing a broken document.

**Why this matters:** The `create_file` tool writes whatever content is passed to it in one call. If the AI's response generation is cut off before the full content is assembled, the file is written incomplete. The truncation produces no error — the file simply ends mid-tag. This is the most common failure mode for large HTML presentations.

### Chunking Procedure

#### Step 1 — Create the skeleton

Call `create_file` with:
- Complete `<head>`, full `<style>` block (all CSS)
- Sidebar with all nav items defined
- `<main>` containing all `<section>` elements — each with the badge, h1, sec-desc, hr, and a single placeholder comment: `<!-- CONTENT_{sectionid} -->`
- Closing `<script>` and `</body></html>`

The placeholder comment format must be exactly:
```html
<!-- CONTENT_{sectionid} -->
```
where `{sectionid}` matches the section's `id="sec-{sectionid}"` attribute.

**Example skeleton section:**
```html
<section class="section" id="sec-roadmap">
  <div class="sec-badge">Roadmap</div>
  <h1 class="sec-h1">Implementation Roadmap</h1>
  <p class="sec-desc">Phase-by-phase delivery sequence from Pre-Phase through full stack operational.</p>
  <hr class="sec-divider">
  <!-- CONTENT_roadmap -->
</section>
```

#### Step 2 — Fill sections one at a time

For each section, call `replace_string_in_file` replacing the placeholder with the section's full HTML content:

```
oldString: "  <!-- CONTENT_roadmap -->"
newString:  <div class="phase-block">
              ... full section HTML ...
            </div>
```

Process sections in order, high-content sections first (tables, phase grids) since those are most likely to cause issues if generated in bulk.

#### Step 3 — Run the quality checklist (Section 13)

After all sections are filled, verify the complete file passes the quality checklist. Pay particular attention to garbled-characters check — `replace_string_in_file` is UTF-8 safe but verify no raw special chars slipped into section content.

### Section Sizing Guidelines

| Section type | Estimated HTML lines | Chunking required? |
|---|---|---|
| Simple text + 1 table | < 80 lines | No — include in skeleton |
| Phase workflow table (6+ rows) | 80–200 lines | Yes — fill via replace |
| Score matrix + multi-perspective evaluation | 200–400 lines | Yes — fill via replace |
| Full roadmap with phase blocks | 300–500 lines | Yes — fill via replace |
| Research integration table (10+ rows) | 80–150 lines | Yes — fill via replace |

### Rule: Never Skip the Placeholder

If a section is short enough to include inline in the skeleton (< 80 lines), include it directly — do not add a placeholder for it. Only use the placeholder pattern for sections whose content would meaningfully contribute to a generation-limit timeout.

---

## 13. Quality Checklist

Run this checklist before delivering any HTML presentation:

- [ ] `<meta charset="UTF-8">` is the FIRST tag in `<head>`
- [ ] Title uses `&middot;` (not literal `·` or garbled `Â·`)
- [ ] No garbled chars: search source for `â€`, `â†`, `Ãƒ`, `Â·`, `â–`, `â—`
- [ ] CSS `content:` values use CSS escapes (`\xxxx`), not HTML entities or raw chars
- [ ] All nav icons use numeric HTML entities (`&#x25C8;` etc.), not raw Unicode
- [ ] No emoji in nav or headings
- [ ] `goTo()` JavaScript is present before `</body>`
- [ ] Every `<section id="sec-X">` has a corresponding `onclick="goTo('X')"` nav item
- [ ] First section has `class="section active"` for correct initial display
- [ ] `@media print` and `@media (max-width:900px)` blocks are present
- [ ] `.sidebar-bottom` shows correct version and date
- [ ] Google Fonts CDN links are present (both `preconnect` and `stylesheet`)
- [ ] No external JavaScript CDN links (no jQuery, no Bootstrap, no icon fonts)
- [ ] Organization label in sidebar reads `[Organization] &middot; [Team]`
- [ ] No `auto` in `grid-template-columns` for repeating-row layouts (use fixed px or fr values)
- [ ] No `min-width` on grid cells whose column is already explicitly sized
- [ ] Tables use `table-layout: fixed` with `<th>` widths declared
