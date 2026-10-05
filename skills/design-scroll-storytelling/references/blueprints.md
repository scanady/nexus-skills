# Blueprints

Five scene plans. Each lists the technique mix, then the sections in order. Use as a starting score, not a template to paste. Swap techniques to fit story. Code lives in the linked references.

Reference key: **D** = `depth-system.md`, **R** = `directional-reveals.md`, **I** = `inter-section-effects.md`, **G** = `gsap-scroll-recipes.md`, **T** = `scroll-typography.md`.

Every blueprint obeys the base rules: depth level per element, `aria-hidden` on decoration, reduced-motion and lite fallbacks, content readable without JS.

## 1. Beverage Brand Launch

Premium juice. One glass hero. Product rises between sections.

Mix: loader curtain (R8), 6-layer parallax (D), seam product (I1), top-down birth (R1), word lighting (T4), card stack (G3), split converge (T1), circle iris (R6), bleed type (T12).

| Section | Plan |
|---|---|
| Loader | Logo on dark, splits open. Under 1.5s. Skipped on repeat visit |
| Hero (deep purple) | L0 gradient · L1 orange glow · L2 citrus slices · L3 glass (float) · L4 headline, converge · L5 splash dots |
| Seam | Glass hovers across the border between hero and ingredients |
| Ingredients (cream) | Enter by top-down birth. L3 large orange. L4 tagline lights word by word |
| Flavours | Stack of 3 cards. Each buried card shrinks as the next arrives. Bottle L3, title L4 |
| CTA (dark again) | Circle iris. Bleed headline. One button |

Palette: hero `#0a0014 → #2d0b4e`, glow `#ff6b00`/`#ff9900`, ingredients `#fdf4e7`. Last section returns to the hero dark: closes the loop.

## 2. SaaS Landing

B2B analytics. Precise, modern, product screenshot as proof.

Mix: window-pane iris (R2), scale-in pin (I4), scrub timeline (G4), curtain roll-up (R3), cylinder number (T3), line wipe (T9), horizontal strip (G6), reactive marquee (T10), circle iris (R6).

| Section | Plan |
|---|---|
| Hero (midnight blue) | Iris opens the site. L0 mesh gradient · L1 CSS grid at 0.15 · L2 faint shapes · L3 dashboard shot (subtle float, keep its bg) · L4 headline, "10x" by cylinder |
| Feature zoom | Pinned ~300%. Dashboard grows to full viewport. Three features land in turn, descriptions by line wipe |
| How it works | Top-down birth. Three steps enter from left, top, right (R7) |
| Integrations | Horizontal scroll of logos. Marquee line below |
| Pricing | Curtain roll-up, one tier per panel, price numbers scramble in (T5) |
| CTA | Circle iris, bleed "START FREE TODAY" |

Screenshot keeps background: see `asset-preparation.md`. Nothing here should delay LCP.

## 3. Creative Portfolio

Designer's site. Work is the hero. Bold, editorial.

Mix: offset diagonal (T8), theatrical enter/exit (T7), horizontal scroll (G6), Flip morph (I2), marquee (T10), bleed type (T12), diagonal wipe (R5), section peel (I6), circle iris (R6), word wave (T11).

| Section | Plan |
|---|---|
| Intro (black) | No loader. Huge name, offset diagonal: line 1 top-left, line 2 lower-right, role far right italic. "See work" bottom-right |
| Marquee | "AVAILABLE FOR WORK · BASED IN LONDON · …" speeds up with scroll |
| Projects | Pinned horizontal scroll, 4 panels. Title by line wipe, blurb by theatrical. Diagonal wipe between panels |
| About | Peel reveals it. Portrait opens by circle iris. Body by masked lines |
| Process | Pinned scrub, three stages. Numbers by cylinder |
| Contact | Circle iris. Email scrambles on hover. Links skew-bounce |

Skip cursor effects on touch. Keep project panels as a plain stacked list under reduced motion.

## 4. Game Launch

Dark, cinematic, deep layers.

Mix: curved path (I5), perspective fly-through (G7), full 6-level parallax (D), morphing borders (R4), card stack (G3), word lighting (T4), float loops (D), loader (R8).

| Section | Plan |
|---|---|
| Loader | Bar fills, logo rolls in by cylinder, curtain splits. Cap short |
| Hero | L0 distant mountains (very slow) · L1 fog, screen blend · L2 terrain · L3 character · L4 title converge · L5 embers |
| Fly-through | Pinned ~300%. Background rushes in, character from far, title resolves. **Off under reduced motion** |
| Lore | Pinned ~400%. Words light as you scroll. Faint silhouette at L1 |
| Characters | Card stack of 4. Name by cylinder, class by line wipe. Stat bars scale-X on enter |
| World map | Horizontal scroll, 5 zones, zone titles offset diagonal |
| Pre-order | Window-pane iris, bleed "ENTER THE REALM" |

Heaviest blueprint. Needs lite mode from day one. Fly-through and path travel must drop to a still image + fade on phones.

## 5. Luxury Product Store

Watch or jewellery. Every move whispers. Slow durations (1.2–2s), small distances, halved parallax speeds.

Mix: scale-in pin (I4, gentle), Flip morph (I2), section peel (I6), masked lines (T2), edge birth (I3), seam product (I1), word lighting (T4, very slow), small circle iris (R6), bleed collection names (T12).

| Section | Plan |
|---|---|
| Hero (cream) | No loader. L0 cream gradient · L1 faint warm glow 0.2 · L2 thin line art 0.3 · L3 watch, 14s float with tiny travel · L4 thin wide-tracked brand name, "Est. 1887". L3 parallax speed 0.3 |
| Product transition | Flip: watch moves from hero centre to left of the detail view, text on right by masked lines. 1.4s |
| Materials | Edge birth: watch grows through the boundary. Close-ups fade up gently, 0.2s stagger |
| Craft | Top-down birth. Maker footage by soft scale-in. Prose lights word by word, meditative pace |
| Collection | Peel into horizontal gallery of 4 variants. Clip wipe on labels |
| Purchase | Small slow circle iris (2s). Price, materials, add to cart. CTA barely-there skew |

Restraint is the brief. If a technique draws attention to itself, cut it.

## Combos That Repeat

| Combo | Pieces |
|---|---|
| Product hero | Seam product + top-down birth + split converge + word lighting |
| Cinematic chapter | Pinned section + scrub timeline + curtain roll-up + theatrical enter/exit |
| Tech premium | Window-pane iris + scale-in pin + line wipe + cylinder rotation |
| Editorial | Bleed type + offset diagonal + horizontal scroll + diagonal wipe |
| Minimal luxury | Flip morph + section peel + masked lines + halved parallax speeds |

## Picking From A Brief

1. Name the emotion (awe, trust, energy, calm). Match tempo: awe = long pins, calm = short slow reveals.
2. Pick the one signature move (seam product, scale-in, horizontal). Build it first.
3. Add supporting reveals, max two or three types per page.
4. Check the weight: count animated elements, check lite mode, check reduced motion.
5. Cut one thing. Then ship.
