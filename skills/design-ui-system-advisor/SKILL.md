---
name: design-ui-system-advisor
description: "UI/UX design intelligence for web and mobile. Use when building, designing, reviewing, or implementing: website, landing page, dashboard, SaaS app, e-commerce, admin panel, portfolio, mobile app. Triggers: design system, color palette, typography, UI style, accessibility, UX review, chart type, stack guidelines, choose fonts, implement layout, build component, review UI code. Knowledge base: 50+ styles, 97 palettes, 57 font pairings, 99 UX rules, 25 chart types, 9 stacks (React, Next.js, Vue, Nuxt, Svelte, SwiftUI, React Native, Flutter, html-tailwind)."
license: MIT
metadata:
  version: "1.0.0"
  domain: design
  triggers: design system, ui design, ux review, color palette, typography, landing page, accessibility check, chart recommendation, build ui, create component, review design, implement layout, choose style, font pairing, stack guidelines, design website, build dashboard, create landing page, saas design, mobile ui, dark mode, glassmorphism, brutalism, minimalism
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
