# Scroll Accessibility

Scroll motion hurts real people: parallax and zoom trigger vestibular disorders (dizziness, nausea, migraine). Treat access as a build input, not a final pass. Target WCAG 2.2 AA, plus the AAA motion criterion.

Standards that apply:
- 2.3.3 Animation from Interactions (**AAA**): motion from interaction can be disabled. `prefers-reduced-motion` is how you meet it. Worth doing though not AA.
- 2.2.2 Pause, Stop, Hide (**A**): auto-moving content over 5s needs a pause. Float loops and marquees count.
- 1.4.3 Contrast (AA), 2.4.7 Focus Visible (AA), 1.1.1 Non-text Content (A), 2.4.1 Bypass Blocks (A).

## 1. Reduced Motion: Build It First

Design reduced motion as the **base**. Add motion only when user has no preference.

```css
.float { animation: none; }
.scene .layer { transform: none; }

@media (prefers-reduced-motion: no-preference) {
  .float { animation: float-y 10s ease-in-out infinite; }
}
```

Last-resort global stop (safety net, not the plan):

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

JS animation ignores CSS media queries. Gate it:

```javascript
gsap.matchMedia().add('(prefers-reduced-motion: reduce)', () => {
  // end states, no motion
  gsap.set('[data-animate], .word, .line, .clip-reveal', { clearProps: 'all', opacity: 1 });
});
```

Do not call `timeScale(0)` or kill everything and leave `from()` start states in place. Result: invisible content. Always land on the end state.

### Per-Effect Policy

Not all motion is equal. Fast, large, continuous = bad. Small, one-shot, opacity-only = fine.

| Effect | Under reduced motion |
|---|---|
| Scroll parallax | **Disable** (continuous) |
| Float loops, marquee, variable-font wave | **Disable** |
| Scale-in pin, perspective zoom, fly-through | **Disable** |
| Particles, cursor trails | **Disable** |
| Horizontal-scroll conversion | **Disable**, show stacked panels |
| Clip-path reveals (one-shot) | Keep, or swap to fade |
| Opacity fades | Keep |
| Word lighting | Keep as plain colour change, or show all lit |
| Curtain, wipe (one-shot) | Keep, shorter duration |
| Text slides (one-shot) | Keep with ≤ 200ms and short distance |

## 2. Semantic Structure

Animated layers do not replace markup.

- One `<main id="main-content">`. One `<h1>`. Headings step down without skipping.
- Each scene is a `<section>` with `aria-label` or a heading.
- Decorative layers (levels 0, 1, 5, decorative 2): `aria-hidden="true"`; decorative `<img>` gets `alt=""`.
- Meaningful hero image: real alt text describing the object, not "image".
- Content readable and in order with CSS and JS off. DOM order = reading order, regardless of how layers visually overlap.
- Seam products and Flip travelers: single image in DOM, alt describes it once.

```html
<a href="#main-content" class="skip-link">Skip to main content</a>
<main id="main-content">
  <section aria-label="Hero: product introduction">…</section>
</main>
```

## 3. Split Text

Fragmented text reads one piece at a time. Set `aria-label` on the parent with the full text, `aria-hidden` on fragments. SplitText 3.13+ handles it by default. Details and helper: `scroll-typography.md`.

## 4. Pinned Sections And Keyboard

Pins and scrubs can trap keyboard users.

- Every interactive element reachable by Tab, in a logical order. Hidden-by-clip content must not be focusable: add `inert` or `visibility: hidden` on parts not yet revealed, and remove when shown.
- Focused element must scroll into view. Test Tab through a pinned scene: focus should not land off-screen on an unrevealed panel.
- Anchor links and `Home/End/PageDown/Space` keep working. Do not intercept them.
- No scroll lock beyond a short loader.

```css
:focus-visible { outline: 3px solid #005fcc; outline-offset: 3px; border-radius: 3px; }
.skip-link { position: absolute; top: -100px; left: 0; padding: 12px 20px; background: #005fcc; color: #fff; z-index: 10000; }
.skip-link:focus { top: 0; }
```

Focus ring needs ≥ 3:1 contrast against both its own surroundings and the adjacent colour.

## 5. Contrast

- Body text: 4.5:1. Large text (≥ 24px, or ≥ 19px bold): 3:1. UI parts and focus rings: 3:1.
- Test text over gradients, glows, and photos at the lightest AND darkest point behind it.
- Dim-state text in word lighting still counts for anyone who reads it unlit. Reduced motion lights everything.
- Boost with a scrim, not only a shadow:

```css
.text-on-image { color: #fff; text-shadow: 0 0 20px rgb(0 0 0 / .8), 0 2px 4px rgb(0 0 0 / .6); }
.text-scrim    { background: rgb(0 0 0 / .55); backdrop-filter: blur(8px); padding: 1rem 1.5rem; border-radius: 8px; }
```

## 6. User Motion Control

OS setting is not enough: not everyone knows it exists, and 2.2.2 wants a page-level pause for loops. Offer a toggle.

```html
<button class="motion-toggle" type="button" aria-pressed="false">Pause animations</button>
```

```javascript
const root = document.documentElement;
const btn = document.querySelector('.motion-toggle');
const KEY = 'motion';

function setMotion(off) {
  root.classList.toggle('no-motion', off);
  btn.setAttribute('aria-pressed', String(off));
  btn.textContent = off ? 'Resume animations' : 'Pause animations';
  gsap.globalTimeline.paused(off);
  try { localStorage.setItem(KEY, off ? 'off' : 'on'); } catch {}
}

btn.addEventListener('click', () => setMotion(!root.classList.contains('no-motion')));
let saved = null; try { saved = localStorage.getItem(KEY); } catch {}
if (saved === 'off' || matchMedia('(prefers-reduced-motion: reduce)').matches) setMotion(true);
```

```css
.no-motion *, .no-motion *::before, .no-motion *::after { animation-play-state: paused !important; transition: none !important; }
```

Pausing is not the same as a safe state. For scrubbed content that must also show end state. Pair with the matchMedia path when the pause is a "reduce" request.

Storage can throw (private mode): always try/catch.

## 7. Alt Text

| Image | Handling |
|---|---|
| Hero product | Descriptive alt: what it is and looks like |
| Decorative shape, glow, particle | `alt=""` and `aria-hidden="true"` on wrapper |
| Icon next to a text label | `alt=""` |
| Standalone icon button | alt or `aria-label` names the action |
| Screenshot with content | Alt summarises purpose, not every pixel |

## 8. Loader

If a loader exists:
- Do not hide content from assistive tech while loading longer than needed.
- Announce completion once: a visually hidden `role="status"` node.
- Remove or `inert` the curtain when done.

```css
.sr-only { position: absolute; width: 1px; height: 1px; margin: -1px; padding: 0; overflow: hidden; clip-path: inset(50%); white-space: nowrap; border: 0; }
```

## Ship Checklist

- [ ] Reduced motion is the base; motion added under `no-preference`
- [ ] JS animations gated by `matchMedia`; reduced users see all content, no frozen start states
- [ ] Per-effect policy table applied
- [ ] Loops > 5s have a page-level pause
- [ ] Decorative layers `aria-hidden`, decorative images `alt=""`
- [ ] Meaningful images have descriptive alt
- [ ] Split text has `aria-label` on parent
- [ ] One `<main>`, one `<h1>`, ordered headings, labelled sections, `lang` set
- [ ] Skip link first in `<body>`
- [ ] Tab order logical through pinned and clipped scenes; unrevealed content not focusable
- [ ] Focus ring ≥ 3:1, visible
- [ ] Text contrast 4.5:1 (3:1 large) at worst point of backgrounds
- [ ] Page fully readable with JS and CSS off
- [ ] Anchors and keyboard scroll keys untouched
- [ ] Run `node scripts/validate-layers.mjs <file>`
