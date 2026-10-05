# Depth System

Flat PNG + CSS + JS → fake 3D. Every element lives on one of six depth levels. Level sets parallax speed, blur, shadow, asset budget. Four cues together sell depth to the eye.

## Six Levels

| Level | Role | Net scroll speed | Static blur | Shadow | Asset edge / weight |
|---|---|---|---|---|---|
| 0 | Far background | 0.10x | 6–8px | none | 1920px / 150KB |
| 1 | Glow, haze | 0.25x | 4px (+ blob blur 40–100px) | none | 800px / 60KB |
| 2 | Mid decoration, companions | 0.50x | 0 | soft | 400px / 50KB |
| 3 | Hero object | 0.80x | 0 | strong | 1200px / 120KB |
| 4 | Text, UI | 1.00x | 0 | none | 600px / 40KB |
| 5 | Foreground FX | 1.20x | 0 | sharp | 128px / 10KB |

Net speed 1.0 = moves with page. Below 1 = lags (feels far). Above 1 = outruns page (feels close).

Apparent size comes from authored asset size, not CSS `scale`. Shrinking a background with `scale(0.7)` exposes edges. Backgrounds overscan instead (see below).

## Parallax Driver

Pick ONE transform owner per element. Parallax goes on the outer `.layer`. Float loops and entrances go on an inner child. Two systems writing one `transform` = fights, jumps.

Offset a layer needs = `(1 − speed) × scrolled distance`. Centre it so scene middle = zero offset:

```javascript
const SPEED = [0.1, 0.25, 0.5, 0.8, 1.0, 1.2];

function initDepthParallax(scene) {
  const travel = () => scene.offsetHeight + innerHeight; // px scrolled while scene crosses view

  scene.querySelectorAll('[data-depth]').forEach((layer) => {
    const k = 1 - SPEED[Number(layer.dataset.depth)];
    if (k === 0) return; // depth 4 never moves relative to page

    gsap.fromTo(layer,
      { y: () => -k * travel() / 2 },
      {
        y: () => k * travel() / 2,
        ease: 'none',
        scrollTrigger: {
          trigger: scene, start: 'top bottom', end: 'bottom top',
          scrub: true, invalidateOnRefresh: true,
        },
      });
  });
}
```

Overscan for laggy layers so edges never show:

```css
.layer { position: absolute; inset: 0; }
.depth-0, .depth-1 { inset: -15% 0; } /* grow by ~ max travel × k / 2 */
```

No-JS option, modern browsers: `animation-timeline: view()` on the layer, same offsets as keyframes. Gate under `@supports (animation-timeline: view())` and `prefers-reduced-motion: no-preference`.

## What Goes On Each Level

- **0** — gradient, sky, texture. Low detail fine. Photo stays boxed (keep its bg, it IS the bg).
- **1** — radial blobs, flares. `mix-blend-mode: screen`. Cheap CSS gradient beats PNG.
- **2** — shapes, small companions. Moderate shadow.
- **3** — the star: product, character. Transparent cutout. Biggest visual weight. Shadow via `filter: drop-shadow` (follows pixel shape).
- **4** — headline, copy, buttons. Always crisp. Real DOM text.
- **5** — sparkles, droplets. Tiny, sharp, scattered, staggered delays.

## Rule Of One Hero

One dominant asset per scene. Rest serve it.

| Role | Display size | Level |
|---|---|---|
| Hero | 50–85vw | 3 |
| Primary companion | 8–15vw | 2 |
| Secondary companion | 5–10vw | 2 |
| Accent / particle | 1–4vw | 5 |
| Fill | 100vw | 0 |

Companion ≈ 15–25% of hero display size. Equal sizes = flat page.

Hug the hero edge, not random corners:

```css
/* hero width clamp(600px, 70vw, 1000px) → half = clamp(300px, 35vw, 500px) */
.companion-right { position: absolute; right: calc(50% - clamp(300px, 35vw, 500px) - 20px); top: 55%; }
.companion-left  { position: absolute; left:  calc(50% - clamp(300px, 35vw, 500px) - 20px); top: 35%; }
```

Negative gap = slight overlap with hero.

**Scatter on exit.** Hero grows or leaves → companions fly outward, not just fade. They were in orbit.

```javascript
heroTl
  .to('.companion-right', { x: 80,  y: -50, scale: 1.3  }, at)
  .to('.companion-left',  { x: -70, y:  40, scale: 1.25 }, at);
```

Pre-build size check: Which asset is hero? Companions ≤ 25% of hero? Enough size contrast between levels? Anything same-size by accident?

## Float Loops

Levels 2–5 never sit dead still. Put loop on inner child (see transform owner rule).

```css
@keyframes float-y      { 50% { transform: translateY(-18px); } }
@keyframes float-orbit  { 25% { transform: translate(8px,-12px) rotate(2deg); }
                          50% { transform: translateY(-20px); }
                          75% { transform: translate(-8px,-12px) rotate(-2deg); } }
@keyframes float-breathe{ 50% { transform: scale(1.04); } }

.depth-2 .float { animation: float-y 10s ease-in-out infinite; }
.depth-3 .float { animation: float-orbit 8s ease-in-out infinite; }
.depth-5 .float { animation: float-y 6s ease-in-out infinite; }
.float:nth-child(2) { animation-delay: -2s; }
.float:nth-child(3) { animation-delay: -4s; }

@media (prefers-reduced-motion: reduce) { .float { animation: none; } }
```

Loops running > 5s need a way to pause (WCAG 2.2.2). See `scroll-accessibility.md` motion toggle.

## Shadow And Glow

Closer = heavier shadow. All `drop-shadow`, never `box-shadow` on cutouts.

```css
.depth-2 img { filter: drop-shadow(0 10px 20px rgb(0 0 0 / .20)); }
.depth-3 img { filter: drop-shadow(0 25px 50px rgb(0 0 0 / .35)); }
.depth-5 img { filter: drop-shadow(0 5px 15px  rgb(0 0 0 / .50)); }

.glow-blob {              /* level 1, behind hero */
  position: absolute; width: 600px; aspect-ratio: 1; border-radius: 50%;
  background: radial-gradient(circle, var(--brand) 0, transparent 70%);
  filter: blur(80px); opacity: .45; mix-blend-mode: screen;
}
```

## Scene Scaffold

```html
<section class="scene" data-scene="hero" aria-label="Hero">
  <div class="layer depth-0" data-depth="0" aria-hidden="true"><div class="bg-gradient"></div></div>
  <div class="layer depth-1" data-depth="1" aria-hidden="true"><div class="glow-blob"></div></div>
  <div class="layer depth-2" data-depth="2" aria-hidden="true"><img class="float" src="shape.png" alt=""></div>
  <div class="layer depth-3" data-depth="3"><img class="float" src="product.png" alt="Describe the product"></div>
  <div class="layer depth-4" data-depth="4"><h1>Headline</h1><p>Support copy.</p><a href="#next">Explore</a></div>
  <div class="layer depth-5" data-depth="5" aria-hidden="true"><img class="float" src="spark.png" alt=""></div>
</section>
```

Minimum 3 layers per scene. Decorative levels (0, 1, 5, and decorative 2) carry `aria-hidden="true"`. Run `scripts/validate-layers.mjs` to confirm.
