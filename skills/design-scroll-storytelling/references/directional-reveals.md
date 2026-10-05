# Directional Reveals

Sections need not rise from below. Born from top, opened from a keyhole, swept in from a corner. Eight patterns. Mostly `clip-path`: bounded, one-shot, scrubbed. Keep each reveal on one element at a time (paint cost, see `scroll-performance.md`).

| # | Pattern | Feel | Driver |
|---|---|---|---|
| 1 | Top-down clip birth | Curtain drop | scrub |
| 2 | Window-pane iris | Peek through keyhole | scrub |
| 3 | Curtain panel roll-up | Peel layers | pinned scrub |
| 4 | Morphing border | Fluid seam | scrub |
| 5 | Diagonal wipe | Corner sweep | one-shot |
| 6 | Circle iris | Aperture, spotlight | scrub |
| 7 | Multi-direction grid | Assembly | one-shot |
| 8 | Loader curtain | Opening title | timed |

Reduced motion: replace every reveal with a plain opacity fade, or show final state. Wrap all in `gsap.matchMedia()` (see `gsap-scroll-recipes.md`).

## 1. Top-Down Clip Birth

Section clipped to nothing, grows downward from top edge.

`inset(top right bottom left)`: bottom 100% = nothing visible.

```javascript
gsap.fromTo(section,
  { clipPath: 'inset(0 0 100% 0)' },
  { clipPath: 'inset(0 0 0% 0)', ease: 'power2.out',
    scrollTrigger: { trigger: section.previousElementSibling, start: 'bottom 80%', end: 'bottom 20%', scrub: 1.5 } });
```

Optional exit, retract upward (clip from top):

```javascript
gsap.to(section, { clipPath: 'inset(100% 0 0 0)', ease: 'power2.in',
  scrollTrigger: { trigger: section, start: 'bottom 20%', end: 'bottom top', scrub: 1 } });
```

Enter clips bottom away. Exit clips top away. Reads as same motion reversed.

## 2. Window-Pane Iris

Section starts as small centred rectangle, grows to full viewport.

```javascript
const st = { trigger: section, start: 'top 90%', end: 'top 10%', scrub: 1.2 };
gsap.fromTo(section, { clipPath: 'inset(42% 35% 42% 35% round 12px)' },
                     { clipPath: 'inset(0 0 0 0 round 0px)', ease: 'none', scrollTrigger: st });
gsap.fromTo(section.querySelector('.iris-content'), { scale: 1.4 }, { scale: 1, ease: 'none', scrollTrigger: st });
```

Inner counter-scale adds zoom depth.

Blinds variant: two bars slide apart.

```javascript
gsap.timeline({ scrollTrigger: { trigger: reveal, start: 'top 70%', toggleActions: 'play none none reverse' } })
  .to(topBar,    { yPercent: -100, duration: 1, ease: 'power3.inOut' })
  .to(bottomBar, { yPercent:  100, duration: 1, ease: 'power3.inOut' }, 0);
```

## 3. Curtain Panel Roll-Up

Stacked panels, each rolls away to expose the next. Pin the stack, step panels along one timeline.

```css
.curtain-stack { position: relative; height: 100vh; overflow: hidden; }
.curtain-panel { position: absolute; inset: 0; }
.curtain-panel:nth-child(1) { z-index: 5; }
.curtain-panel:nth-child(2) { z-index: 4; }
.curtain-panel:nth-child(3) { z-index: 3; }
```

```javascript
const panels = gsap.utils.toArray('.curtain-panel', stack);
const tl = gsap.timeline({ scrollTrigger: { trigger: stack, start: 'top top', end: `+=${panels.length * 120}%`, pin: true, scrub: 1 } });

panels.slice(0, -1).forEach((panel, i) => {      // last panel stays: it is the destination
  tl.to(panel, { clipPath: 'inset(100% 0 0 0)', duration: 1, ease: 'power2.inOut' }, i);
  const h = panels[i + 1].querySelector('.panel-heading');
  if (h) tl.from(h, { opacity: 0, y: 30, duration: 0.4 }, i + 0.5);
});
```

## 4. Morphing Border

Section bottom edge drifts between straight, wave, diagonal. Upstream snapped between shapes. Tween instead: all paths share the same command layout, so GSAP interpolates the numbers.

```html
<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <clipPath id="morph" clipPathUnits="objectBoundingBox">
    <path id="morph-path" d="M0,0 L1,0 L1,1 Q0.5,1 0,1 Z"/>
  </clipPath>
</svg>
<section class="morphed" style="clip-path:url(#morph)">…</section>
```

```javascript
const SHAPES = {
  wave:     'M0,0 L1,0 L1,.95 Q.5,1.05 0,.95 Z',
  diagonal: 'M0,0 L1,0 L1,.88 Q.5,.94 0,1 Z',
};
gsap.timeline({ scrollTrigger: { trigger: '.morphed', start: 'top 80%', end: 'bottom 20%', scrub: 2 } })
  .to('#morph-path', { attr: { d: SHAPES.wave } })
  .to('#morph-path', { attr: { d: SHAPES.diagonal } });
```

Keep to one morphing section on screen. Large SVG clips repaint.

## 5. Diagonal Wipe

Polygon sweeps from a corner.

```javascript
const WIPE = {
  'top-left':   ['polygon(0 0, 0 0, 0 0)',          'polygon(0 0, 120% 0, 0 120%)'],
  'top-right':  ['polygon(100% 0, 100% 0, 100% 0)', 'polygon(-20% 0, 100% 0, 100% 120%)'],
  'center-out': ['polygon(50% 50%, 50% 50%, 50% 50%, 50% 50%)',
                 'polygon(-10% -10%, 110% -10%, 110% 110%, -10% 110%)'],
};
function diagonalWipe(el, dir = 'top-left') {
  const [from, to] = WIPE[dir];
  gsap.fromTo(el, { clipPath: from }, { clipPath: to, duration: 1.4, ease: 'power3.inOut',
    scrollTrigger: { trigger: el, start: 'top 70%', once: true } });
}
```

Polygon point count must match between from and to.

## 6. Circle Iris

Circle grows from a chosen origin. Boldest reveal. Use once or twice per page.

```javascript
gsap.fromTo(el, { clipPath: 'circle(0% at 50% 50%)' },
  { clipPath: 'circle(80% at 50% 50%)', ease: 'none',
    scrollTrigger: { trigger: el, start: 'top 75%', end: 'top 25%', scrub: 1 } });
```

Origin from a CTA or product position ties the reveal to the story. `80%` radius covers the corners of a typical viewport; raise it for very wide ones.

## 7. Multi-Direction Grid

Cards enter from different edges. One timeline, one trigger. Not one trigger per card.

```javascript
const DIRS = [[-80,0],[0,-80],[80,0],[0,80],[-60,-60],[60,-60],[-60,60],[60,60]];
const tl = gsap.timeline({ scrollTrigger: { trigger: grid, start: 'top 75%', once: true } });
gsap.utils.toArray('.grid-item', grid).forEach((item, i) => {
  const [x, y] = DIRS[i % DIRS.length];
  tl.from(item, { x, y, opacity: 0, duration: 0.8, ease: 'power3.out' }, i * 0.08);
});
```

## 8. Loader Curtain

Branded intro splits open. Highest risk pattern for access and content. Rules:

- Page content stays in DOM, readable, behind the curtain. No hidden-until-JS.
- Never lock scroll longer than ~1.5s total. No `overflow:hidden` left behind on error: clear it in `finally`.
- Skip entirely on reduced motion, repeat visit (`sessionStorage`, in try/catch), or slow load.
- Make curtain `inert` + `aria-hidden` once done, then `display:none`.
- Start scroll animations after it lifts, call `ScrollTrigger.refresh()`.

```css
.loader { position: fixed; inset: 0; z-index: 9999; pointer-events: none; }
.loader-half { position: absolute; left: 0; right: 0; height: 50%; background: var(--loader-bg, #0a0a0a); }
.loader-top { top: 0; } .loader-bottom { bottom: 0; }
```

```javascript
function runLoader() {
  const loader = document.querySelector('.loader');
  const done = () => { loader.hidden = true; ScrollTrigger.refresh(); initAllAnimations(); };
  gsap.timeline({ onComplete: done })
    .from('.loader-logo', { opacity: 0, scale: 0.8, duration: 0.5 })
    .to('.loader-logo',   { opacity: 0, duration: 0.3 }, '+=0.2')
    .to('.loader-top',    { yPercent: -100, duration: 0.7, ease: 'power4.inOut' })
    .to('.loader-bottom', { yPercent:  100, duration: 0.7, ease: 'power4.inOut' }, '<');
}
```

## Chaining Across A Page

Vary the reveal per boundary. Same trick five times = boring.

```
Hero → 2   window-pane iris
2 → 3      top-down clip birth
3 → 4      diagonal wipe
4 → 5      circle iris
5 → 6      curtain roll-up
```

Cap: two or three distinct reveals per page unless story asks for more.
