# Component Patterns

Repair-time patterns for the components that most often look unpolished: forms, buttons, images/icons, empty states, overlays, navigation, and radius. Tailwind-flavored class names shown as shorthand for the underlying values.

## Forms

**Input width should match expected content** — don't stretch a ZIP field full-width. Email/address full or ~400px; phone ~200px; city ~200px; state ~150px; ZIP ~100px.

**Label, always.** Never use a placeholder as the only label — it vanishes on focus. Placeholders are for format hints (`MM/DD/YYYY`) and examples, not identity.

**Input states** must be visually distinct:

| State | Treatment |
|-------|-----------|
| Default | `border-gray-300` |
| Focus | `border-blue-500` + `ring-2 ring-blue-200` |
| Error | `border-red-500` + `ring-2 ring-red-200` + message |
| Disabled | `bg-gray-100 text-gray-400` |

**Layout** — one column by default. Two columns only for genuinely paired fields (first/last, city/state). Group related fields with spacing, not heavy boxes.

## Button Hierarchy

One primary action per view; everything else recedes.

| Level | Treatment |
|-------|-----------|
| Primary | solid, high contrast (`bg-blue-600 text-white`) |
| Secondary | outline or muted (`border-gray-300`) |
| Tertiary | text only (`text-blue-600 hover:underline`) |
| Danger | red but calm — solid only on the confirm step, text-red on the trigger |

## Interaction States

Every interactive element needs visible feedback. Hover: subtle bg/shadow shift or 10% darken. Active: darker than hover + slight `scale-95`. Focus: an obvious ring via `focus-visible` (never `outline: none` without a replacement). Loading: disable, show spinner/skeleton, and hold layout size to prevent shift.

## Images

Text over images is the recurring failure. Fixes: semi-transparent overlay (`bg-black/50`), gradient (`bg-gradient-to-t from-black/80`), or a solid text box. Never distort — `object-fit: cover` with a fixed `aspect-ratio`. Avatars: consistent per-context size, fallback initials, round for people.

## Icons

Size relative to adjacent text: 12–14px text → 16px icon, 16px text → 20px, 18–20px → 24px. Center-align with text, ~8px gap. Skip icons on buttons whose text is already clear ("Submit"), and never add them just to fill space.

## Empty States

An opportunity, not a dead end. Include an illustration/icon, a one-line explanation of what goes here, and a primary action to fill it. Match the product tone.
```
❌ "No items"
✅ "No projects yet. Create your first to get started."   [+ Create Project]
```

## Overlays

**Modal width by content:** confirmation 400–500px, form 500–600px, content 600–800px (cap height ~70–80vh). Structure = title + close, scrollable body, right-aligned actions. Backdrop `rgba(0,0,0,0.5)`, optional `backdrop-filter: blur(4px)`. Enter with fade + slight scale (see `motion-and-animation.md`).

**Dropdowns/menus:** open below-left, flip up if no room, constrain to viewport. `min-width ~180px`, `max-height ~300px` with scroll, `shadow-lg`, 8px radius, `4px 8px`-ish item padding, hover `bg-gray-100`, divider `1px bg-gray-200`.

## Navigation

Top nav: logo left, links center/right, one CTA, clear active state, collapse to hamburger on mobile. Side nav: group related items, collapsible to icons on desktop, full overlay on mobile. Breadcrumbs on nested pages (current page not a link). Tabs: underline or pill, active gets a 2px accent border, horizontal-scroll on mobile.

## Border Radius

Pick one system and stay in it. Sharp/modern: `2·4·6` + `full`. Soft/friendly: `4·8·12·16` + `full`. Rules: inner radius = outer − padding; smaller elements get smaller radius; images in cards match the card or use `overflow-hidden`.

## Color Psychology (light touch)

Use hue purposefully, not decoratively: blue = trust/primary, green = success, red = error/destructive, yellow/orange = warning, purple = premium, gray = neutral structure. Cap at ~3 accent colors. Avoid red for non-destructive primaries and green for errors (colorblind users). Deeper palette construction lives in `dark-mode.md`; never rely on color alone (see `accessibility.md`).

## Text Truncation

Truncate nav items, fixed-width table cells, and card titles (reveal on hover). Never truncate body text, error messages, or search results. Multi-line clamp via `-webkit-line-clamp`.
