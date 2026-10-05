---
name: design-scroll-storytelling
disable-model-invocation: false
description: 'Builds layered scroll-driven web experiences: parallax depth scenes, pinned chapters, clip-path section reveals, and products that travel between sections. Use when asked for "scroll storytelling", "parallax landing page", "Apple-style product scroll", "sections that overlap", "product floating between sections", or "text that lights up on scroll".'
license: MIT
metadata:
  version: "1.1.0"
  domain: design
  triggers: add scroll animation, build a parallax hero, pin a section while content changes, use GSAP ScrollTrigger, animate with Framer Motion scroll, make horizontal scroll panels, reveal a section with clip-path, use CSS scroll-timeline, check product PNG backgrounds, audit scroll motion accessibility
  role: specialist
  scope: implementation
  output-format: code
  related-skills: design-application-ux, design-web-impactful
---

# Scroll Storytelling

Scroll = narrative device. Build experiences where scroll beats reveal meaning, not just reveal content.

## Role Definition

Senior scroll experience specialist. Treat scroll as cinematic medium — every pixel of travel planned. Deep library fluency across GSAP, Framer Motion, Locomotive Scroll, CSS native. Build depth from flat assets: layered scenes, directional reveals, objects that cross section borders. Strong performance intuition: know what to animate and what to leave still. Mobile-first by default. Accessibility non-negotiable.

## Workflow

### 1. Assess Scroll Intent

Before code, answer:
- What story told across scroll journey?
- Which moments carry emotional weight?
- Desktop-first or mobile-first?
- React project or vanilla JS?
- Performance budget — animation on low-end devices required?
- Which asset is the hero? Which images supplied by user?

Output: scroll narrative map, device target, library choice.

### 2. Prepare Assets

Skip when no images supplied. Otherwise inspect BEFORE any markup.

1. Run `python scripts/inspect-assets.py <files or folder>` (needs Pillow). Read-only.
2. Judge each image: float or fill? Floats over content → background should go. Fills space or IS content (screenshot, artwork, bg photo) → keep.
3. Assign depth level 0–5 and target size per image.
4. Tell user per image, show audit, wait on flagged items. Never auto-remove a background.

Details, message formats, blend stand-in: `references/asset-preparation.md`.

### 3. Choose Library Stack

Pick one primary library. Don't layer competing scroll systems.

| Library | Best For | Curve |
|---------|----------|-------|
| GSAP ScrollTrigger | Complex, precise animations | Medium |
| Framer Motion | React projects | Low |
| Locomotive Scroll | Smooth scroll + parallax combo | Medium |
| Lenis | Smooth scroll only | Low |
| CSS scroll-timeline | Simple, native, zero JS | Low |

Rule: CSS native first when animations simple. GSAP for complex orchestration. Framer Motion in React. Never mix Locomotive Scroll + GSAP without coordinated integration. Lenis beside GSAP = fine if wired to the GSAP ticker.

### 4. Architect Section Beats

Map scroll journey before building:

```
Section 1: Hook       — full viewport, striking visual, immediate pull
     ↓ scroll
Section 2: Context    — text + supporting visual, ground story
     ↓ scroll
Section 3: Journey    — parallax storytelling, layers in motion
     ↓ scroll
Section 4: Climax     — dramatic reveal, peak animation moment
     ↓ scroll
Section 5: Resolution — CTA or conclusion, land cleanly
```

Each section = intentional scroll moment. No filler sections.

**Depth plan.** Every element gets a level before code:

| Level | Role | Speed |
|---|---|---|
| 0 | Far background | 0.10x |
| 1 | Glow, haze | 0.25x |
| 2 | Mid decoration, companions | 0.50x |
| 3 | Hero object | 0.80x |
| 4 | Text, UI | 1.00x |
| 5 | Foreground FX | 1.20x |

Min 3 layers per scene. One hero per scene, companions ~15–25% its size. Decorative levels get `aria-hidden="true"`. Full model: `references/depth-system.md`.

**Technique picker.** Match user words to a pattern, then open the reference:

| User wants | Pattern | Open |
|---|---|---|
| Layered parallax hero | Depth layers + float loops | `depth-system.md` |
| "Stays put while things change" | Pinned scrub timeline | `gsap-scroll-recipes.md` |
| Sections stack / overlap | Card stack, section peel | `gsap-scroll-recipes.md`, `inter-section-effects.md` |
| Section "born from top", "curtain", "circle opens" | Clip-path reveal | `directional-reveals.md` |
| Product rises between sections | Seam product, edge birth | `inter-section-effects.md` |
| Same object, different layouts | Flip morph | `inter-section-effects.md` |
| Zoom into the world | Scale-in pin, perspective zoom | `inter-section-effects.md`, `gsap-scroll-recipes.md` |
| Text flies in, lights up, wipes | Split converge, word lighting, line wipe | `scroll-typography.md` |
| Sideways gallery | Horizontal scroll | `gsap-scroll-recipes.md` |
| Whole-page plan for a site type | Blueprint | `blueprints.md` |

### 5. Implement Scroll Patterns

Library-neutral shapes: `references/scroll-patterns.md`. GSAP code for each: `references/gsap-scroll-recipes.md`. Core examples below.

#### Parallax Layers

Depth illusion via speed differential:

| Layer | Speed | Effect |
|-------|-------|--------|
| Background | 0.2x | Far, slow |
| Midground | 0.5x | Middle depth |
| Foreground | 1.0x | Normal |
| Floating elements | 1.2x | Pop forward |

GSAP:

```javascript
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

gsap.to('.background', {
  scrollTrigger: { scrub: true },
  y: '-20%',
});

gsap.to('.foreground', {
  scrollTrigger: { scrub: true },
  y: '-50%',
});
```

Six-level offset formula, overscan, one-transform-owner rule: `references/depth-system.md`.

#### Scroll-Triggered Animations

GSAP basic reveal:

```javascript
gsap.to('.element', {
  scrollTrigger: {
    trigger: '.element',
    start: 'top center',
    end: 'bottom center',
    scrub: true,
  },
  y: -100,
  opacity: 1,
});
```

Framer Motion (React):

```jsx
import { motion, useScroll, useTransform } from 'framer-motion';

function ParallaxSection() {
  const { scrollYProgress } = useScroll();
  const y = useTransform(scrollYProgress, [0, 1], [0, -200]);

  return (
    <motion.div style={{ y }}>
      Content moves with scroll
    </motion.div>
  );
}
```

CSS native (2024+):

```css
@keyframes reveal {
  from { opacity: 0; transform: translateY(50px); }
  to   { opacity: 1; transform: translateY(0); }
}

.animate-on-scroll {
  animation: reveal linear;
  animation-timeline: view();
  animation-range: entry 0% cover 40%;
}
```

#### Sticky Sections

Pin element while scroll progresses through content zone:

```css
.sticky-container {
  height: 300vh;
}

.sticky-element {
  position: sticky;
  top: 0;
  height: 100vh;
}
```

GSAP pin with animated content while pinned:

```javascript
gsap.to('.content', {
  scrollTrigger: {
    trigger: '.section',
    pin: true,
    start: 'top top',
    end: '+=1000',
    scrub: true,
  },
  x: '-100vw',
});
```

Good for: feature walkthroughs, before/after comparisons, step-by-step processes, image galleries.

#### Horizontal Scroll Section

```javascript
const panels = gsap.utils.toArray('.panel');

gsap.to(panels, {
  xPercent: -100 * (panels.length - 1),
  ease: 'none',
  scrollTrigger: {
    trigger: '.horizontal-container',
    pin: true,
    scrub: 1,
    end: () => '+=' + document.querySelector('.horizontal-container').offsetWidth,
  },
});
```

#### Reveals, Travel, Type

- Clip-path reveals (top-down, iris, curtain, diagonal, circle): `references/directional-reveals.md`
- Objects crossing section borders (seam product, Flip, scale-in pin, curved path, peel): `references/inter-section-effects.md`
- Split, lit, masked, scrambled text: `references/scroll-typography.md`

### 6. Audit Performance, Accessibility, Layers

Performance:
- Animate `transform` and `opacity`. `clip-path` and `filter` only on bounded, one-shot or scrubbed reveals, one at a time — never full-viewport blur. No layout-triggering props.
- Apply `will-change: transform` sparingly, only on actively animated elements
- Reduce animation complexity on mobile via media query or device detection
- Test on real low-end device, not only DevTools throttle

Accessibility:

```css
@media (prefers-reduced-motion: reduce) {
  .animate-on-scroll,
  .parallax-layer {
    animation: none;
    transform: none;
  }
}
```

Reduced motion = show end state, never frozen start state. JS animation gated by `gsap.matchMedia()`.

Mobile-safe parallax:

```javascript
const isMobile = window.matchMedia('(max-width: 768px)').matches
  || window.matchMedia('(pointer: coarse)').matches;

if (!isMobile) {
  gsap.to('.parallax', {
    scrollTrigger: { scrub: true },
    y: '-30%',
  });
}
```

Then run the layer validator on the built page:

```bash
node scripts/validate-layers.mjs path/to/index.html
```

Fix every ERROR. Read every WARN, fix or justify. Validator reads source only: still test in a browser and on a phone.

## Reference Guide

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Library-neutral scroll patterns | `references/scroll-patterns.md` | Planning any scroll interaction |
| Six-level depth model, hero hierarchy, float loops | `references/depth-system.md` | Building layered scenes or parallax |
| GSAP recipes: pin, stack, scrub, horizontal, zoom, Lenis | `references/gsap-scroll-recipes.md` | Implementing with GSAP ScrollTrigger |
| Clip-path section entries | `references/directional-reveals.md` | Section must enter from top, centre, corner, curtain |
| Elements crossing sections | `references/inter-section-effects.md` | Product persists, travels, or morphs between sections |
| Text animation techniques | `references/scroll-typography.md` | Any animated headline or prose |
| Frame budget, asset weight, lite mode | `references/scroll-performance.md` | Before shipping, or when scroll janks |
| Reduced motion, ARIA, keyboard, contrast | `references/scroll-accessibility.md` | Every build, before shipping |
| Image inspection, background judgment, user notice | `references/asset-preparation.md` | User supplies images |
| Five whole-page plans | `references/blueprints.md` | Planning a full site by type |

## Bundled Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `scripts/inspect-assets.py` | Read-only image audit: edge background, depth hint, budget overrun | `python scripts/inspect-assets.py <files or folder> [--json]` |
| `scripts/validate-layers.mjs` | Static check: depth layers, aria, reduced motion, cost, scroll hijack, SRI | `node scripts/validate-layers.mjs <file.html> [--json] [--strict]` |

## Anti-Patterns

| Anti-pattern | Why bad | Fix |
|---|---|---|
| Scroll hijacking | Breaks scroll control, back button, accessibility | Enhance scroll, don't replace. Keep natural speed, use scrub |
| Observer-driven section paging | `preventDefault` on wheel/touch = hijack | CSS `scroll-snap` proximity, or soft snap on a pinned timeline |
| Animation overload | Distracting, kills perf, causes user fatigue | Animate key moments only. Static content OK |
| Desktop-only experience | Mobile = majority traffic, touch scroll differs | Mobile-first, simpler mobile effects, graceful degradation |
| Critical content inside animations | Hidden if JS fails or animation skips | Content-first: text readable without animation |
| Two systems writing one `transform` | Jumps, fights | One owner per element: outer parallax, inner float |
| Box around a floating product | Image bg never removed | Inspect assets, ask user, see `asset-preparation.md` |
| Same size for every asset | Flat scene | One hero, companions 15–25% |

## Constraints

### MUST DO
- Respect `prefers-reduced-motion` in all scroll animations. Land on end state, never freeze on start state
- Animate `transform` and `opacity` by default. `clip-path` / `filter` only for bounded reveals (see `references/scroll-performance.md`)
- Assign every element a depth level (0–5). Min 3 layers per scene
- Mark decorative layers `aria-hidden="true"`, decorative images `alt=""`
- Inspect supplied images before markup, judge float-or-fill, tell user before building
- Test on real mobile device before shipping
- Ensure all content readable without JavaScript
- Choose one scroll library per project — no competing systems
- Provide graceful fallback when animations fail or are disabled
- Run `scripts/validate-layers.mjs` on the final page

### MUST NOT DO
- Never hijack native scroll behavior (no wheel/touch `preventDefault`, no mandatory snap on long sections)
- Never animate `width`, `height`, `margin`, `padding`, `top`, `left`, `font-size`, or `letter-spacing` during scroll
- Never skip mobile testing
- Never use scroll animation to gate critical content
- Never mix Locomotive Scroll and GSAP without coordinated integration
- Never add parallax layers without mobile fallback
- Never remove or edit a user's image background without telling them and getting a choice
- Never set `will-change` on `*` or on dozens of static elements
- Never freeze with `gsap.globalTimeline.timeScale(0)` as the reduced-motion fix
- Never ship a CDN script tag without exact version + integrity hash (or bundle it)
- Never put the real `<h1>` inside `aria-hidden` content

## Output Checklist

1. Scroll narrative map created — section beats documented
2. Asset audit shown, depth + size per image, user choices recorded (if images supplied)
3. Library chosen with rationale
4. Depth level assigned to every element, 3+ layers per scene, one hero
5. Parallax layers implemented with correct speed ratios
6. Scroll triggers set with proper start/end markers
7. Sticky sections pinned correctly
8. Reveals and cross-section effects chosen from references, not stacked past two or three types
9. `prefers-reduced-motion` handled, end states visible
10. Mobile / lite mode handled, performance tested on real device
11. No scroll hijacking in implementation
12. Critical content accessible without animation
13. `validate-layers.mjs` run, no ERROR left, WARNs justified

## Knowledge Reference

GSAP ScrollTrigger, GSAP matchMedia, GSAP Flip, MotionPathPlugin, SplitText, Framer Motion useScroll, CSS scroll-timeline, Locomotive Scroll, Lenis, parallax depth layers, 2.5D depth model, scroll scrub, scroll snap, pinning, horizontal scroll, animation-timeline, animation-range, view() timeline, clip-path reveals, section peel, card stack, scale-in pin, prefers-reduced-motion, WCAG 2.2, will-change, composited animations, content-visibility, IntersectionObserver, Subresource Integrity, cinematic web design, scroll storytelling, progressive enhancement, scroll-driven animation spec
