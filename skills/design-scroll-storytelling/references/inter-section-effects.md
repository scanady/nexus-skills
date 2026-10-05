# Inter-Section Effects

Element persists, travels, or transitions across section borders. Thread that ties the page into one story. Highest polish, highest risk: most work lives in `ScrollTrigger` timing across two or more sections.

| Situation | Technique |
|---|---|
| Product site, hero image | 1. Seam product |
| Same object, many layouts | 2. Flip morph |
| Product grows out of a section edge | 3. Edge birth |
| "Enter the world" zoom | 4. Scale-in pin |
| Object travels a story path | 5. Curved path |
| Page-turn between sections | 6. Section peel |
| Dark → light section change | 1. Seam product (bg flips behind it) |

Reduced motion: drop travel, show object in its destination section. See `scroll-accessibility.md`.

## 1. Seam Product

Product sits ON the border of two sections, owned by neither. Grows and gains shadow mid-pass, then settles into section two.

Upstream used a zero-height sticky wrapper. Sticky cannot outlive a zero-height parent, so it stuck nowhere. Use an anchor placed on the seam instead. Product is absolutely centred on it.

```html
<section class="hero" style="position:relative; z-index:1">…</section>

<div class="seam">
  <img class="seam-product float" src="product.png" alt="Product name, between hero and features">
</div>

<section class="features" style="position:relative; z-index:1">…</section>
```

```css
.seam { position: relative; height: 0; z-index: 10; pointer-events: none; }
.seam-product {
  position: absolute; left: 50%; top: 0;
  width: clamp(280px, 35vw, 560px);
  translate: -50% -50%;          /* individual transform props leave `transform` free for GSAP */
}
```

One scrubbed timeline spans both sections. No per-update `gsap.to`.

```javascript
gsap.timeline({
  defaults: { ease: 'none' },
  scrollTrigger: { trigger: '.hero', endTrigger: '.features', start: 'bottom 85%', end: 'top 15%', scrub: 1.2 },
})
  .fromTo('.seam-product',
    { scale: 0.85, y: 0,    filter: 'drop-shadow(0 10px 20px rgb(0 0 0 / .2))' },
    { scale: 1.1,  y: '-4vh', filter: 'drop-shadow(0 40px 80px rgb(0 0 0 / .5))', duration: 0.5 })
  .to('.seam-product', { scale: 0.95, y: '3vh', duration: 0.5 });
```

Hero has no product copy of its own. Image lives in `.seam` only, so there is one source of truth. If the image must also exist in hero for no-JS, hide the seam copy under `.no-js`.

## 2. Flip Morph

One DOM node, many layouts. `Flip` records state, you move the node, it animates the difference.

```html
<div class="slot slot-hero"><img class="traveler" src="product.png" alt="Product"></div>
…
<div class="slot slot-feature"></div>
<div class="slot slot-detail"></div>
```

```javascript
gsap.registerPlugin(Flip, ScrollTrigger);
const traveler = document.querySelector('.traveler');

function moveTo(slot) {
  const state = Flip.getState(traveler);
  slot.appendChild(traveler);
  Flip.from(state, { duration: 0.9, ease: 'power3.inOut' });
}

[['.slot-feature', '.slot-hero', '.feature-section'], ['.slot-detail', '.slot-feature', '.detail-section']]
  .forEach(([enter, back, trigger]) =>
    ScrollTrigger.create({
      trigger, start: 'top 60%',
      onEnter:     () => moveTo(document.querySelector(enter)),
      onLeaveBack: () => moveTo(document.querySelector(back)),
    }));
```

Notes: Flip morph is triggered, not scrubbed, so fast scroll can queue moves. Guard with `Flip.killFlipsOf(traveler)` before each move. Slots reserve layout space so nothing jumps. Slow = luxury (1.2–1.4s). Reduced motion: call `moveTo` with `duration: 0`.

## 3. Edge Birth

Product hidden below the section edge, grows up through it like a plant. Section is the stage.

```css
.birth-section { position: relative; overflow: hidden; min-height: 100vh; }
.birth-product { position: absolute; bottom: 0; left: 50%; translate: -50% 0; width: clamp(300px, 40vw, 600px); }
```

```javascript
gsap.timeline({ defaults: { ease: 'none' }, scrollTrigger: { trigger: section, start: 'top 80%', end: 'bottom top', scrub: 1.2 } })
  .fromTo(product, { yPercent: 120, scale: 0.7, opacity: 0 }, { yPercent: 0, scale: 1, opacity: 1, duration: 0.5 })
  .to(product,     { yPercent: -25, opacity: 0, scale: 1.15, duration: 0.5 }, 0.7);
```

One timeline, enter and exit. Upstream used a second trigger re-creating tweens each frame.

## 4. Scale-In Pin

DJI-style. Small framed image scales to fill the viewport, text lands over it, then section unpins.

Upstream tweened `width`, `left`, `top`: layout every frame. Make media full-size from the start and reveal it with `clip-path` inset.

```css
.zoom-section { position: relative; height: 100vh; overflow: hidden; }
.zoom-media   { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.zoom-overlay { position: absolute; inset: 0; background: linear-gradient(transparent, rgb(0 0 0 / .8)); opacity: 0; }
.zoom-copy    { position: absolute; left: 8%; right: 8%; bottom: 15%; color: #fff; }
```

```javascript
gsap.timeline({ scrollTrigger: { trigger: section, start: 'top top', end: '+=300%', pin: true, scrub: 1.5 } })
  .fromTo(media, { clipPath: 'inset(20% 20% 20% 20% round 20px)', scale: 1.15 },
                 { clipPath: 'inset(0% 0% 0% 0% round 0px)', scale: 1, duration: 0.4, ease: 'power2.inOut' })
  .fromTo(overlay, { opacity: 0 }, { opacity: 0.6, duration: 0.2 }, 0.35)
  .from(section.querySelectorAll('.zoom-line'), { y: 40, opacity: 0, stagger: 0.08, duration: 0.25 }, 0.45);
```

Text must stay readable on the overlay (contrast, see `scroll-accessibility.md`). Pinned distance ≥ 300% is a long ride: keep one idea per pin.

## 5. Curved Path

Object arcs across page on a Bézier path. Advanced; test on mid-range phone.

```javascript
gsap.registerPlugin(MotionPathPlugin, ScrollTrigger);

const tl = gsap.timeline({ defaults: { ease: 'none' },
  scrollTrigger: { trigger: '.journey', start: 'top top', end: '+=400%', pin: true, scrub: 1.5 } });

tl.to(product, { motionPath: { path: [{x:0,y:0},{x:-200,y:-100},{x:100,y:-300},{x:300,y:-150},{x:200,y:50}],
                               curviness: 1.4, autoRotate: false }, duration: 1 }, 0)
  .to(product, { keyframes: { scale: [0.8, 1.1, 0.9, 1.0, 1.2] }, duration: 1 }, 0);
```

Position and scale run as two tweens on one timeline, same start. Upstream put `gsap.utils.interpolate(...)` (returns a function) in the `scale` slot, which does nothing useful. Path coordinates are relative to the element's start position. For a real SVG path, pass `path: '#route'`.

## 6. Section Peel

Upper section scrolls away like a page turning, lower section waits underneath. Pure CSS core.

```html
<div class="peel">
  <section class="peel-upper">…</section>
  <section class="peel-lower">…</section>
</div>
```

```css
.peel-upper { position: relative; z-index: 2; min-height: 100vh; background: var(--bg-upper); }
.peel-lower { position: sticky; bottom: 0; z-index: 1; min-height: 100vh; }
```

Upper needs an opaque background or lower shows through. Lower sticks to the viewport bottom while upper leaves.

Optional polish: lower content entrance, scrubbed to the peel.

```javascript
gsap.from('.peel-lower .peel-content > *', {
  y: 30, opacity: 0, stagger: 0.1, duration: 0.6,
  scrollTrigger: { trigger: '.peel', start: '30% top', toggleActions: 'play none none reverse' },
});
```

Upstream also clipped the upper section while lower was sticky. Two mechanisms for one effect fight each other. Pick CSS, or pick clip, not both.

## Shared Rules

- Product image appears once in DOM unless a no-JS fallback needs a copy.
- Section `z-index` ordering decides who covers whom. Write it down before coding.
- Call `ScrollTrigger.refresh()` after images load. Cross-section triggers use measured positions and break on late layout shifts.
- Test scrolling backward. Reverse state is where seams go wrong.
- Pointer events off on the traveling element unless it is interactive.
