# GSAP Scroll Recipes

Concrete GSAP + ScrollTrigger code for the scroll architectures. `scroll-patterns.md` shows the ideas library-free. This file is the GSAP implementation. Framer Motion or CSS `scroll-timeline` projects: use the ideas, port the calls.

## Setup

GSAP 3.13+ ships every plugin free, SplitText included. Check the licence text for your installed version.

Prefer a bundler: `npm i gsap`, then import. CDN only for single-file prototypes. A CDN tag MUST pin an exact version and carry Subresource Integrity, or a compromised CDN runs code on the page:

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/gsap.min.js"
        integrity="sha384-<hash>" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/ScrollTrigger.min.js"
        integrity="sha384-<hash>" crossorigin="anonymous"></script>
<!-- Add only what you use: Flip, MotionPathPlugin, SplitText, Observer -->
```

Make the hash with `curl -s <url> | openssl dgst -sha384 -binary | openssl base64 -A`, prefix `sha384-`. Never ship the `<hash>` placeholder. Floating tags like `gsap@3` defeat SRI.

**Gate every animation behind `gsap.matchMedia()`.** One block handles reduced motion, touch, cleanup on breakpoint change:

```javascript
gsap.registerPlugin(ScrollTrigger);
const mm = gsap.matchMedia();

mm.add({
  full:    '(prefers-reduced-motion: no-preference) and (pointer: fine) and (min-width: 769px)',
  lite:    '(prefers-reduced-motion: no-preference) and (any-pointer: coarse), (max-width: 768px)',
  reduced: '(prefers-reduced-motion: reduce)',
}, (ctx) => {
  const { full, lite, reduced } = ctx.conditions;
  if (reduced) return showFinalStates();      // no motion, all content visible
  initReveals();                               // lite + full
  if (full) { initDepthParallax(); initPins(); }
});                                            // tweens and triggers auto-revert when query stops matching
```

Never freeze the timeline with `gsap.globalTimeline.timeScale(0)`. Elements that start hidden (`from` tweens) stay hidden. Reduced motion = show end state.

Hidden-until-animated rule: set initial hidden CSS only under a `.js` class added by a script in `<head>`, so no-JS readers still see content.

## 1. Parallax

See `depth-system.md` for the offset formula and per-level speeds.

## 2. Pinned Section

Section stays fixed. Inner content plays on a scrubbed timeline. Page "lives inside" chapter, then moves on.

```javascript
gsap.timeline({ scrollTrigger: { trigger: scene, start: 'top top', end: '+=150%', pin: true, scrub: 1, anticipatePin: 1 } })
  .from('.pinned-title', { opacity: 0, y: 60, duration: 0.3 })
  .from('.pinned-image', { scale: 0.8, opacity: 0, duration: 0.4 })
  .from('.pinned-sub',   { opacity: 0, x: -40, duration: 0.3 });
```

Background colour change while pinned: tween a stacked overlay's `opacity`, not `backgroundColor` (paint).

Pin distance = reading time. Short = rushed, > 400% = fatigue.

## 3. Card Stack

Each new section slides over the last. Buried card shrinks and dims.

```css
.stack-card { position: sticky; top: 0; height: 100vh; }
.stack-card:nth-child(1) { z-index: 1; } .stack-card:nth-child(2) { z-index: 2; } /* … */
.stack-card::after { content: ''; position: absolute; inset: 0; background: #000; opacity: 0; pointer-events: none; }
```

```javascript
const cards = gsap.utils.toArray('.stack-card');
cards.slice(0, -1).forEach((card, i) => {
  const st = { trigger: cards[i + 1], start: 'top bottom', end: 'top top', scrub: true };
  gsap.to(card, { scale: 0.9, ease: 'none', scrollTrigger: st });
  gsap.to(card, { '--dim': 0.5, ease: 'none', scrollTrigger: st });   // or tween ::after opacity via a child element
});
```

Dim with an overlay's `opacity`, not `filter: brightness() blur()`. Overlay is compositor-cheap. Filter on full-viewport cards is not.

## 4. Scrub Timeline

One pixel scrolled = one frame played. Main cinematic tool. Quarters as a rough score:

```javascript
gsap.timeline({ defaults: { ease: 'none' },
  scrollTrigger: { trigger: scene, start: 'top top', end: '+=200%', pin: true, scrub: 1.5 } })  // scrub 0 = exact, 1–2 = dreamy lag
  .fromTo('.hero-product', { scale: 0.6, opacity: 0, y: 100 }, { scale: 1, opacity: 1, y: 0, duration: 0.25 })
  .to('.hero-title span:first-child', { x: '-30vw', opacity: 0, duration: 0.25 }, 0.25)
  .to('.hero-title span:last-child',  { x:  '30vw', opacity: 0, duration: 0.25 }, 0.25)
  .to('.hero-product', { scale: 1.3, y: -50, duration: 0.25 }, 0.5)
  .fromTo('.next-content', { opacity: 0, y: 80 }, { opacity: 1, y: 0, duration: 0.25 }, 0.5)
  .to('.hero-product', { opacity: 0, scale: 1.6, duration: 0.25 }, 0.75);
```

Timeline length is unit-free. Positions 0–1 map to scroll progress when total duration = 1.

## 5. Clip-Path Wipes

Full set lives in `directional-reveals.md`. Quick horizontal wipe:

```javascript
gsap.fromTo(el, { clipPath: 'inset(0 100% 0 0)' },
  { clipPath: 'inset(0 0% 0 0)', duration: 1.2, ease: 'power3.out', scrollTrigger: { trigger: el, start: 'top 80%', once: true } });
```

## 6. Horizontal Scroll

Vertical scroll drives sideways travel. Total travel = track width − viewport width.

```javascript
const track = container.querySelector('.h-track');
gsap.to(track, {
  x: () => -(track.scrollWidth - innerWidth),
  ease: 'none',
  scrollTrigger: {
    trigger: container, pin: true, scrub: 1, invalidateOnRefresh: true,
    end: () => '+=' + (track.scrollWidth - innerWidth),
  },
});
```

```css
.h-track { display: flex; width: max-content; }
.h-panel { flex: 0 0 100vw; height: 100vh; }
```

Add `snap: { snapTo: 1 / (n - 1), duration: 0.3, ease: 'power1.inOut' }` to nudge to panels. That is a soft settle, user still owns scroll.

On touch/narrow: drop the pin, let panels become a native `overflow-x: auto` scroller with `scroll-snap-type: x mandatory`. Nested scroll traps are worse on phones.

## 7. Perspective Fly-Through

User flies toward content. Scale + z + opacity on a pinned scrub.

```css
.zoom-scene { perspective: 1200px; overflow: hidden; }
.zoom-scene > * { transform-style: preserve-3d; }
```

```javascript
gsap.timeline({ scrollTrigger: { trigger: scene, start: 'top top', end: '+=300%', pin: true, scrub: 2 } })
  .fromTo('.zoom-bg', { scale: 0.4, opacity: 0.3 }, { scale: 1.2, opacity: 1, duration: 0.6 })
  .fromTo('.zoom-product', { scale: 0.1, z: -2000, opacity: 0 }, { scale: 1, z: 0, opacity: 1, duration: 0.5, ease: 'power2.out' }, 0.2)
  .fromTo('.zoom-title', { opacity: 0, scale: 0.9 }, { opacity: 1, scale: 1, duration: 0.3 }, 0.55);
```

Upstream also animated blur and `letterSpacing`. Blur is costly on a large layer, `letterSpacing` re-flows text. Both dropped. Fast zoom is a vestibular trigger: disable under reduced motion.

## 8. Section Snap

**Banned: Observer-driven paging** that calls `preventDefault` on wheel/touch. That takes scroll away. Allowed options:

```css
html { scroll-snap-type: y proximity; }   /* proximity, never mandatory for long sections */
.snap-section { scroll-snap-align: start; }
```

Or soft snap on a pinned timeline: `snap: { snapTo: 'labels', duration: 0.4, delay: 0.1 }`. User scroll stays native, snap only settles after they stop.

## 9. Smooth Scroll (Lenis)

Smooths wheel input. Same scroll position, same native scrollbar. Wire to GSAP ticker so ScrollTrigger sees the same value:

```javascript
import Lenis from 'lenis';              // package renamed from @studio-freight/lenis

const lenis = new Lenis({ duration: 1.2, smoothWheel: true });
lenis.on('scroll', ScrollTrigger.update);
gsap.ticker.add((t) => lenis.raf(t * 1000));
gsap.ticker.lagSmoothing(0);
```

Skip Lenis on reduced motion and touch. Do not run it next to Locomotive Scroll. Anchor links and `find in page` need testing.

## 10. Observer Reveal

For plain entrance effects with no scrub, a one-shot `IntersectionObserver` is cheaper than a ScrollTrigger per element:

```javascript
const ENTER = {
  'fade-up':     (el) => gsap.from(el, { y: 60, opacity: 0, duration: 0.8, ease: 'power3.out' }),
  'fade-in':     (el) => gsap.from(el, { opacity: 0, duration: 1, ease: 'power2.out' }),
  'scale-in':    (el) => gsap.from(el, { scale: 0.8, opacity: 0, duration: 0.7, ease: 'back.out(1.7)' }),
  'slide-left':  (el) => gsap.from(el, { x: -80, opacity: 0, duration: 0.8, ease: 'power3.out' }),
  'slide-right': (el) => gsap.from(el, { x:  80, opacity: 0, duration: 0.8, ease: 'power3.out' }),
};

const io = new IntersectionObserver((entries) => {
  for (const e of entries) {
    if (!e.isIntersecting) continue;
    ENTER[e.target.dataset.animate]?.(e.target);
    io.unobserve(e.target);
  }
}, { threshold: 0.15, rootMargin: '0px 0px -50px 0px' });

document.querySelectorAll('[data-animate]').forEach((el) => io.observe(el));
```

## 11. Elastic Drop With Impact

Hero falls, overshoots, then wrapper shakes on landing. Weight sells it.

```html
<div class="drop-wrapper"><img class="drop-product" src="product.png" alt="…"></div>
```

```javascript
gsap.timeline({ delay: 0.3 })
  .from('.drop-product', { y: -180, opacity: 0, scale: 1.1, duration: 1.3, ease: 'elastic.out(1, 0.65)' })
  .to('.drop-wrapper', {                      // wrapper, not the image: avoids transform clash
    keyframes: [{ rotation: -2, duration: .08 }, { rotation: 2, duration: .08 }, { rotation: -1.5, duration: .07 },
                { rotation: 1, duration: .07 }, { rotation: 0, duration: .10 }],
    ease: 'power1.inOut',
  }, '-=0.35');
```

| Feel | Ease |
|---|---|
| Standard | `elastic.out(1, 0.65)` |
| Heavy | `elastic.out(1.2, 0.5)` |
| Light | `elastic.out(0.8, 0.8)` |
| One clean overshoot | `back.out(2.5)` |

Not for feathers, petals, airy things. Use `power3.out`.
