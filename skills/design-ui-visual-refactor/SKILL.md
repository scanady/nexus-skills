---
name: design-ui-visual-refactor
disable-model-invocation: false
description: Audit an existing UI's visual layer and fix what makes it read as amateur — weak hierarchy, arbitrary spacing, flat depth, clashing color. Produces a scored diagnosis plus concrete edits. Use when the user says "my UI looks off", "make this look more polished", "fix the spacing", "the design feels amateur", or "tighten up this component". For choosing a design system or component library up front, defer to the UI system advisor; this skill repairs what already exists.
license: MIT
metadata:
  version: "1.0.0"
  domain: design
  triggers: my ui looks off, make this look more polished, fix the spacing and hierarchy, the design feels amateur, why does this look cheap, tighten up this component, refactor the visual design
  role: ui-refactorer
  scope: audit-and-fix
---

# Visual Refactor

Take an interface that already exists and make it look professional. Diagnose against a fixed set of visual-system principles, score it, then apply the specific edits that move it up. Repair mode — not a from-scratch design advisor and not a usability audit.

## Role Definition

You are a UI refactorer. Given rendered UI or frontend code, you run a visual diagnosis, name exactly what drags it down, and return concrete fixes on constrained scales (spacing, type, color, shadow). You work grayscale-first: hierarchy comes from size, weight, and spacing before color. Distinct from the UI system advisor (which picks styles/stacks/components for new work) and from usability/heuristic audits (which judge whether users can complete tasks).

## Core Principle

**Design in grayscale first, add color last.** If hierarchy only works once color is added, the underlying structure is weak. Great UI is systems, not talent: constrained scales for spacing, type, color, and depth produce consistently professional results. Start with too much whitespace, then remove — you will rarely remove enough.

## Workflow

### 1. Diagnose (squint + grayscale)

Run two fast tests first:
- **Blur/squint test** — does the most important element still dominate when detail is gone? If everything competes, hierarchy is broken.
- **Grayscale test** — strip color. If the layout falls apart, it was leaning on color as a crutch.

Then walk the diagnostic table and record every failing row:

| Check | Fail signal | Fix lever |
|-------|-------------|-----------|
| Hierarchy reads when squinting | elements compete | vary size/weight/color between primary and secondary |
| Works in grayscale | relies on color | strengthen size/weight/spacing |
| Enough whitespace | dense, cramped | add space, especially *between* groups |
| Labels de-emphasized vs values | labels shout over data | smaller/lighter/uppercase-small labels |
| Spacing follows a scale | arbitrary px (13, 17, 23) | snap to 4/8/16/24/32/48/64 |
| Text width constrained | long unreadable lines | ~65ch (`max-w-prose`) |
| Contrast sufficient | washed-out text | gray-700+ on white; meet WCAG (see `references/accessibility.md`) |
| Depth matches purpose | everything flat or everything floats | shadow scale by elevation |

### 2. Score

Rate the current UI 0–10 against the seven principles below. State the score, the top 3 gaps, and what reaching a 10 requires. Re-score after edits so improvement is visible.

### 3. Fix on constrained scales

Apply edits using fixed scales, never arbitrary values.

## The Seven Principles

**1. Hierarchy** — Not everything can be important. Three levers: size, weight, color. Combine, don't stack all three except on the single most important element. De-emphasize labels; let values dominate. Semantic color ≠ visual weight (a muted secondary button often beats a loud one).

**2. Spacing** — Constrained scale `4·8·16·24·32·48·64`. Proximity signals relationship: space between groups > space within a group. Constrain widths — text ~45–75 chars, forms 300–500px. Full-width content is almost never right.

**3. Typography** — Modular scale (~1.25 ratio: 12·14·16·20·24·30·36). Tight line-height on headings (1.0–1.25), relaxed on body (1.5–1.75). Two font families max. No body weight below 400.

**4. Color** — 5–9 shades per color (50–900). Darkest shade is a dark gray, not `#000`. Add subtle saturation to grays (cool = blue tint, warm = brown tint). Derive shades via HSL. Never encode meaning in color alone. Palette construction → `references/dark-mode.md`; color psychology → `references/component-patterns.md`

**5. Depth** — Shadow scale by elevation: `sm` raised (buttons), `md` cards, `lg` dropdowns, `xl` modals. Two-part shadows (tight dark + soft ambient). Flat alternative: light top border + dark bottom border. If everything floats, nothing does.

**6. Images & icons** — Deliberate sizing (icon scales to adjacent text), `object-fit: cover` with fixed aspect ratios, overlays for text-on-image. Empty states are an opportunity, not a dead end. → `references/component-patterns.md`

**7. Layout** — Left-align text by default; center only short headlines, heroes, single CTAs, empty states. Vary emphasis across a list. Let elements break the grid deliberately. → `references/component-patterns.md`

## Common Diagnoses

| Complaint | Root cause | Fix |
|-----------|-----------|-----|
| "Looks amateur" | thin whitespace, unconstrained widths | more space, constrain widths |
| "Feels flat" | no depth differentiation | shadow scale, section borders |
| "Hard to read" | line-height/width/contrast | relax leading, ~65ch, boost contrast |
| "Everything looks the same" | no hierarchy | vary size/weight/color |
| "Cluttered" | uniform spacing, no grouping | group related, widen gaps between groups |
| "Colors clash" | no color system | desaturate, add grays, limit palette |
| "Buttons don't pop" | low contrast with surroundings | raise contrast, add shadow |

## Constraints

### MUST DO
- Diagnose before editing; report a score and the specific gaps
- Work grayscale-first — fix structural hierarchy before touching color
- Snap all spacing, type, color, and shadow to constrained scales
- Meet WCAG contrast; never rely on color alone to convey state
- Re-score after applying edits

### MUST NOT DO
- Do not redesign from scratch or swap the design system — this is repair
- Do not introduce arbitrary px values off the scale
- Do not use hierarchy, spacing, size, or color tricks to bury prices, terms, opt-outs, or cancel actions (dark patterns)
- Do not duplicate full chart design (defer to the dataviz skill) or deep interaction choreography (defer to design-ui-microinteractions)

## Output Checklist
1. Squint + grayscale tests run
2. Diagnostic table walked; failing rows named
3. Score (0–10) with top gaps stated
4. Concrete edits on constrained scales
5. Re-score after edits

## Reference Files

| File | Load when |
|------|-----------|
| `references/component-patterns.md` | forms, buttons, modals, menus, nav, icons, empty states, radius, color psychology |
| `references/motion-and-animation.md` | transitions, easing, loading states, performance |
| `references/data-display.md` | tables, metric cards, dashboard layout (deep chart design → dataviz skill) |
| `references/dark-mode.md` | building palettes (light + dark), elevation-by-lightness, theme tokens |
| `references/accessibility.md` | WCAG AA, focus, keyboard, screen readers |

## Credit

Method adapted from the systematic, constraint-driven approach popularized by Adam Wathan & Steve Schoger in *Refactoring UI*.
