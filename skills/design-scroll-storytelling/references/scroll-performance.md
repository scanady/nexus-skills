# Scroll Performance

Goal: 60fps scroll on a mid-range phone. Scroll effects fail on cost, not on code. Budget first, effects second.

## Property Tiers

| Tier | Properties | Rule |
|---|---|---|
| Compositor | `transform`, `opacity` | Default. Free to animate |
| Paint | `clip-path`, `filter`, `box-shadow`, `background-color`, `color` | Allowed for one-shot or scrubbed reveals on ONE bounded element at a time. Check cost |
| Layout | `width`, `height`, `top`, `left`, `margin`, `padding`, `font-size`, `letter-spacing`, `border-width`, `font-variation-settings` | Never during scroll. Re-flows the page each frame |

Why `clip-path` and `filter` are allowed at all: directional reveals need them, and they ship fine on small or short-lived targets. Limits:
- One clip or filter animation active per viewport at once.
- No `filter: blur()` animation on full-viewport layers. Static blur is OK.
- `drop-shadow` filters on animated PNGs: fine, small sprites only.
- Measure on a real phone. If it drops frames, swap to an opacity overlay.

Individual transform props (`translate`, `scale`, `rotate`) keep `transform` free for GSAP, avoiding clashes.

## Scroll Handlers

Never run animation logic straight in a scroll listener. Batch to one frame:

```javascript
let pending = null, latestY = 0;
addEventListener('scroll', () => {
  latestY = scrollY;
  pending ??= requestAnimationFrame(() => { pending = null; root.style.setProperty('--scroll-y', latestY); });
}, { passive: true });
```

`passive: true` is required. It lets the browser scroll on its own thread.

Better: no listener. `ScrollTrigger` with `scrub`, or CSS `animation-timeline: scroll() / view()`. Both run off the main handler path.

## GSAP Habits

```javascript
// BAD: new tween every scroll event
addEventListener('scroll', () => gsap.to(el, { y: scrollY * 0.5 }));

// GOOD: one scrubbed tween
gsap.to(el, { y: 200, ease: 'none', scrollTrigger: { scrub: true } });

// GOOD: kill what you finish with
const st = ScrollTrigger.create({ … });  /* later */ st.kill();

// GOOD: instant placement, no tween cost
gsap.set('.el', { x: 0, opacity: 1 });

// GOOD: tune slow inputs
ScrollTrigger.config({ ignoreMobileResize: true });
```

Also:
- Never create tweens inside `onUpdate`. Use one timeline and let `scrub` drive it.
- `invalidateOnRefresh: true` when values are functions of layout.
- Call `ScrollTrigger.refresh()` after images and fonts load.
- `ScrollTrigger.batch()` for many similar reveals: one observer, grouped callbacks.
- Group effects per scene in `gsap.context()` / `matchMedia` so teardown is one call.

## will-change

Promotes element to its own GPU layer. Memory cost per layer.

- Apply to elements about to animate. Remove when done.
- Never `* { will-change: … }`. Never on dozens of static elements.
- GSAP sets and clears it itself during tweens. Do not duplicate in CSS.
- Constant parallax layers (levels 0–3) are the one fair case for a static hint. Cap total promoted layers under ~20.

## Visibility Gating

Animate only what is on screen.

```javascript
const io = new IntersectionObserver((entries) => {
  for (const e of entries) e.target.classList.toggle('is-active', e.isIntersecting);
}, { threshold: 0.1, rootMargin: '50px 0px' });
document.querySelectorAll('.animated-layer').forEach((el) => io.observe(el));
```

```css
.float { animation-play-state: paused; }
.is-active .float, .float.is-active { animation-play-state: running; }
```

Off-screen sections skip rendering:

```css
.scene:not(:first-of-type) { content-visibility: auto; contain-intrinsic-size: auto 100vh; }
```

Never on the first scene (flash of blank). Never on a scene that holds a pin trigger target: measured heights shift. Test pins after enabling.

## Asset Budgets

Hard limits per depth level. Same numbers `scripts/inspect-assets.py` checks.

| Level | Role | Max edge | Max weight |
|---|---|---|---|
| 0 | Background | 1920px | 150KB |
| 1 | Glow | 1000px | 60KB |
| 2 | Decoration | 400px | 50KB |
| 3 | Hero | 1200px | 120KB |
| 4 | UI image | 800px | 40KB |
| 5 | Particle | 128px | 10KB |

Page total under 2MB of images.

Prefer formats: WebP or AVIF with alpha for cutouts (far smaller than PNG). Gradients and glows in CSS, not images. Noise textures tile small.

```html
<link rel="preload" as="image" href="hero-product.webp" fetchpriority="high">
<img src="hero-product-800.webp"
     srcset="hero-product-400.webp 400w, hero-product-800.webp 800w, hero-product-1200.webp 1200w"
     sizes="(max-width: 768px) 100vw, 50vw" width="1200" height="1200" alt="…">
<img src="scene-2-bg.webp" loading="lazy" decoding="async" width="1920" height="1080" alt="">
```

Always set `width` and `height`: no layout shift, so ScrollTrigger measures stay valid.

## Lite Mode

Touch and weak devices get a lighter scene. Detect once, switch by class.

```javascript
const lite = matchMedia('(pointer: coarse)').matches
          || matchMedia('(max-width: 768px)').matches
          || (navigator.hardwareConcurrency ?? 8) <= 4;     // heuristic, not proof
document.documentElement.classList.toggle('perf-lite', lite);
```

```css
.perf-lite .depth-0, .perf-lite .depth-1, .perf-lite .depth-5 { transform: none !important; will-change: auto; }
.perf-lite .float { animation: none; }
.perf-lite .glow-blob, .perf-lite .particle { display: none; }
```

Lite keeps: fades, one-shot reveals, pins that are cheap. Lite drops: continuous parallax, float loops, particles, perspective zoom, pointer tracking, Lenis. `gsap.matchMedia()` (see `gsap-scroll-recipes.md`) does the same job with auto-cleanup.

Heuristics miss. Test on a real device.

## Count Limit

Over ~80 animated elements in one page → expect trouble. Merge decorative sprites into one sprite sheet or one SVG, cut particle count on small screens, or lazy-init scenes when they near the viewport.

## Pre-Ship Checklist

1. DevTools → Rendering → Layer borders. Promoted layers under ~20.
2. Performance panel: record a scroll. Frames > 16ms? Find the paint or layout cause.
3. Memory: heap does not grow while scrolling (no leaked triggers or listeners).
4. Coverage: strip unused animation CSS/JS.
5. Throttle CPU 4x, then try a real mid-range phone. Throttle ≠ touch.
6. No layout-tier property in any `@keyframes`, `transition`, or tween.
7. Lighthouse: LCP element is not an animated layer behind a loader.
8. Scroll back up the whole page. Reverse state matches forward.
