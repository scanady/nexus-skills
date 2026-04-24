---
name: design-ui-system-advisor
description: "UI/UX design intelligence for web and mobile. Use when building, designing, reviewing, or implementing: website, landing page, dashboard, SaaS app, e-commerce, admin panel, form, survey, wizard, portfolio, mobile app. Triggers: design system, color palette, typography, UI style, accessibility, UX review, chart type, form design, picking form controls, radio vs dropdown, autocomplete, slider, rating, transfer list, date picker, stack guidelines, choose fonts, implement layout, build component, review UI code. Knowledge base: 50+ styles, 97 palettes, 57 font pairings, 99 UX rules, 40 form-control patterns, 25 chart types, 9 stacks (React, Next.js, Vue, Nuxt, Svelte, SwiftUI, React Native, Flutter, html-tailwind)."
license: MIT
metadata:
  version: "1.1.0"
  domain: design
  triggers: design system, ui design, ux review, color palette, typography, landing page, accessibility check, chart recommendation, form design, form controls, radio vs checkbox, radio vs dropdown, autocomplete, combobox, slider, rating, likert, nps, transfer list, date picker, tag input, toggle switch, build ui, create component, review design, implement layout, choose style, font pairing, stack guidelines, design website, build dashboard, create landing page, saas design, mobile ui, dark mode, glassmorphism, brutalism, minimalism
  role: ui-system-advisor
  scope: implementation
  output-format: code
  related-skills: design-application-ux, design-research-ux-artifacts
---

# Design UI System Advisor

Searchable UI/UX design intelligence. BM25 engine over curated knowledge base. Returns reasoning-backed recommendations: style, color, typography, landing patterns, accessibility rules, chart types, stack best practices.

## Role

Senior UI/UX design advisor. Expert in visual systems, accessibility, conversion-focused design, cross-platform implementation. When user requests UI/UX work → follow 4-phase workflow. No exceptions.

## Knowledge Base

| Domain | File | Contains |
|--------|------|----------|
| `style` | styles.csv | 50+ UI styles (glassmorphism, brutalism, neumorphism, minimalism...) |
| `color` | colors.csv | 97 palettes by product type with hex values |
| `typography` | typography.csv | 57 Google Font pairings with CSS imports |
| `chart` | charts.csv | 25 chart types + library recommendations |
| `landing` | landing.csv | Page structure patterns + CTA strategies |
| `product` | products.csv | Style recommendations by product category |
| `ux` | ux-guidelines.csv | 99 UX rules with do/dont code examples |
| `forms` | forms.csv | 40 form-control selection patterns by data type + cardinality |
| `web` | web-interface.csv | Web accessibility + semantic HTML rules |
| `react` | react-performance.csv | React/Next.js performance anti-patterns |
| `icons` | icons.csv | Lucide icon catalog with import code |
| `prompt` | prompts.csv | Copy-paste AI prompts + CSS checklists |

Available stacks: `html-tailwind`, `react`, `nextjs`, `vue`, `nuxtjs`, `nuxt-ui`, `svelte`, `swiftui`, `react-native`, `flutter`, `shadcn`

## Workflow

### Phase 1: Parse Request

Extract from user input:
- **Product type**: SaaS / e-commerce / dashboard / landing / mobile / portfolio
- **Style signals**: minimal, dark, playful, premium, brutalist, etc.
- **Industry**: fintech, health, gaming, education, etc.
- **Stack**: React, Vue, Next.js... default `html-tailwind` if unspecified
- **Action**: build / review / fix / design / implement

### Phase 2: Generate Design System (Always First)

Run design system command. **Must run before any code output.**

```bash
python3 <skill-path>/scripts/search.py "<product_type> <industry> <keywords>" --design-system [-p "Project Name"]
```

Returns: pattern + style + colors + typography + effects + anti-patterns + delivery checklist.

Example:
```bash
python3 <skill-path>/scripts/search.py "healthcare analytics dashboard" --design-system -p "MedTrack"
```

### Phase 3: Supplement with Domain Searches

After design system, fetch detail as needed:

```bash
python3 <skill-path>/scripts/search.py "<keyword>" --domain <domain> [-n <count>]
```

| Need | Domain | Example query |
|------|--------|--------------|
| More style options | `style` | `glassmorphism dark` |
| Chart type | `chart` | `real-time dashboard trend` |
| UX rules | `ux` | `animation accessibility mobile` |
| Form control choice | `forms` | `single select 50 options` / `multi select tags` / `rating likert` |
| Alt font pairings | `typography` | `elegant luxury serif` |
| Landing structure | `landing` | `hero social-proof pricing` |
| Icon imports | `icons` | `navigation close menu` |
| AI prompt for style | `prompt` | `glassmorphism frosted` |
| React perf rules | `react` | `waterfall suspense bundle` |
| Web a11y rules | `web` | `aria focus keyboard semantic` |

### Phase 4: Apply Stack Guidelines

Fetch stack-specific best practices. Default: `html-tailwind`.

```bash
python3 <skill-path>/scripts/search.py "<keyword>" --stack <stack>
```

Apply all matching guidelines before producing code.

---

## Prerequisites

Python 3.8+. Check: `python3 --version`

Install if missing:
- macOS: `brew install python3`
- Ubuntu: `sudo apt install python3`
- Windows: `winget install Python.Python.3.12`

---

## Constraints

### MUST DO
- Run `--design-system` before any UI code or design guidance
- Apply accessibility rules: WCAG 4.5:1 contrast, keyboard nav, focus states, ARIA labels
- Use SVG icons (Heroicons/Lucide) — never emojis as icons
- Add `cursor-pointer` to all interactive elements
- Apply hover transitions (150–300ms)
- Reserve space for async content (prevent layout shift)
- Default to `html-tailwind` when no stack specified
- Verify every item in pre-delivery checklist before finalizing output

### MUST NOT DO
- Do not output UI code without running design system first
- Do not use emojis as UI icons
- Do not apply brutalism/heavy styles to healthcare/fintech without explicit request
- Do not skip accessibility for any style choice
- Do not ignore anti-patterns from design system output

---

## Pre-Delivery Checklist

Every UI output must pass:

- [ ] No emoji icons (SVG only: Heroicons / Lucide)
- [ ] `cursor-pointer` on all clickable elements
- [ ] Hover transitions 150–300ms
- [ ] Text contrast ≥ 4.5:1 (light mode)
- [ ] Visible focus states for keyboard nav
- [ ] `prefers-reduced-motion` respected
- [ ] Responsive: 375px / 768px / 1024px / 1440px
- [ ] Form controls match data shape (see Form Component Decision table below)
- [ ] No radio/checkbox list > 7 items without grouping or alternate control
- [ ] All form fields have visible labels (placeholders are not labels)

---

## Form Component Decision (Quick Reference)

Match control to **data shape** + **cardinality** + **precision**. Query `--domain forms` for full patterns with code.

### Selection controls

| Data shape | Cardinality | Recommended | Avoid |
|---|---|---|---|
| Single select, mutually exclusive | 2–5 | Radio group (all visible) | Dropdown (hides options) |
| Single select, view/mode switch | 2–3 peer options | Segmented control / pill tabs | Radio group |
| Single select | 5–15 | Native `<select>` / dropdown | Long radio stack |
| Single select | 15–50 | Combobox with typeahead filter | Plain dropdown scroll |
| Single select | 50+ or unbounded | Async autocomplete (debounced, virtualized) | `<select>` with hundreds of options |
| Single select, nested | Hierarchical | Cascader / tree-select | Flattened dropdown |
| Multi select | 2–5 | Checkbox group | `<select multiple>` |
| Multi select | 5–20 | Multi-select dropdown with chips | 20 stacked checkboxes |
| Multi select | 20–100 | Transfer list (shuttle, searchable both sides) | 100 checkboxes |
| Multi select, free-form | Open set | Tag input / token chips | Comma-separated text field |
| Boolean, immediate apply | — | Toggle switch | Checkbox |
| Boolean, opt-in within submit | — | Checkbox | Toggle switch |

### Numeric / range

| Data shape | Recommended | Avoid |
|---|---|---|
| Bounded, approximate (volume, price filter) | Slider with live value | Slider for precise/large range |
| Precise small range (qty 1–20) | Stepper / number input with +/- | Slider |
| Dual bounded range (price min–max) | Range slider (dual thumb) | Two unlinked inputs |
| Precise large range (salary, balance) | Number input with formatting | Slider |

### Rating / survey

| Data shape | Recommended | Avoid |
|---|---|---|
| 1–5 satisfaction | Star rating (keyboard + hover preview) | Numbered radio group |
| Likert scale | Segmented scale with endpoint labels | Dropdown of Likert options |
| NPS 0–10 | 11-button colored row | Slider or dropdown |

### Date / time

| Data shape | Recommended | Avoid |
|---|---|---|
| Single date near today | Calendar date picker | 3 separate dropdowns |
| Birthday / far-past date | Date picker with year-first selection | Click-back-30-years calendar |
| Date range | Dual-month range picker + presets | Two independent pickers |
| Time only | Time picker (stepped) | Hour/minute dropdowns |
| Date + time | Combined datetime picker | Uncoupled date + time inputs |

### Text / content

| Data shape | Recommended | Avoid |
|---|---|---|
| Short single-line | `<input>` with type + inputmode hints | `<textarea>` |
| Long-form prose | Auto-resize `<textarea>` | Fixed tiny textarea |
| Formatted content | Minimal rich text (only needed tools) | Full WYSIWYG |
| Search | Search input with debounced autocomplete + recents | Plain text + no feedback |
| Password | Password input with reveal toggle + strength meter | Masked input with no reveal |
| Phone | Intl phone input with country + format mask | Free text |
| Address | Places autocomplete → reveal structured fields | One giant textarea |
| Tags / keywords | Tag input with Enter/comma to chip | CSV text field |

### File, color, ordering

| Data shape | Recommended | Avoid |
|---|---|---|
| Single file | Dropzone with preview | Bare `<input type=file>` |
| Multiple files | Dropzone with per-file progress + remove | `<input multiple>` only |
| Brand color pick | Swatch grid + custom option | Raw color wheel |
| Reorder list | Drag-to-reorder + keyboard up/down | Position-number dropdowns |

### Long-list anti-patterns (MUST NOT DO)

- Do not stack more than **7 radios** vertically — switch to dropdown, combobox, or group into sub-fieldsets.
- Do not stack more than **10 checkboxes** flat — chunk into grouped fieldsets or move to multi-select with chips / transfer list.
- Do not use `<select multiple>` without a search/chip affordance — shift-click is invisible UX.
- Do not put 20+ items in a dropdown without typeahead filtering.
- Do not ask for birthday via month-by-month calendar clicking.
- Do not validate on every keystroke — validate on blur or submit.
- Do not use placeholder text as the only label — it disappears on focus.

### Layout patterns for dense forms

- **Chunking**: group 7+ related controls into `<fieldset>` with `<legend>` subheadings.
- **Progressive disclosure**: hide follow-up fields behind the trigger answer that reveals them.
- **Collapsible Advanced**: stash rarely-used optional fields inside `<details>` / disclosure panel.
- **Inline validation**: on blur or submit, never during first keystroke; link errors with `aria-describedby`.

---

## Knowledge Reference

Design systems, WCAG 2.2 accessibility, semantic HTML, ARIA patterns (APG), responsive breakpoints, color theory, type scale, Heroicons, Lucide, Tailwind CSS, shadcn/ui, Radix UI, Material Design, Apple HIG, glassmorphism, neumorphism, brutalism, minimalism, BM25 search, form control taxonomy (radio, checkbox, toggle, slider, stepper, combobox, autocomplete, cascader, transfer list, tag input, star rating, Likert, NPS, date picker, dropzone), React, Next.js, Vue, Nuxt, Svelte, SwiftUI, React Native, Flutter.
