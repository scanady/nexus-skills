# Scroll Typography

Thirteen text techniques for scroll scenes. Pick one or two per scene. Text is depth level 4: always crisp, always real DOM text, always readable with animation off.

| # | Technique | Mood | Driver |
|---|---|---|---|
| 1 | Split converge | Big title entrance/exit | pinned scrub |
| 2 | Masked line reveal | Elegant body copy | one-shot |
| 3 | Cylinder rotation | Numbers, short heads | one-shot |
| 4 | Word lighting | Apple-style prose | pinned scrub |
| 5 | Scramble | Tech, digital | one-shot |
| 6 | Skew bounce | Energetic cards, CTAs | one-shot |
| 7 | Theatrical enter/exit | Any block, zero JS | CSS view() |
| 8 | Offset diagonal | Editorial titles | one-shot |
| 9 | Line clip wipe | Feature descriptions | one-shot |
| 10 | Reactive marquee | Dividers, skills | rAF |
| 11 | Variable-font wave | Playful headline | loop |
| 12 | Bleed type | Dramatic section edge | CSS + parallax |
| 13 | Ghost outline | Atmosphere behind hero | CSS + scrub |

## Splitting Text Safely

Splitting breaks a heading into many nodes. Screen readers read fragments one by one. Fix every time:

- Real text goes in `aria-label` on the parent. Fragments get `aria-hidden="true"`.
- GSAP SplitText 3.13+ does this itself (`aria: 'auto'` default). Older versions or hand-split spans: do it manually.
- Re-split on resize (`autoSplit: true` in 3.13+) or lines break wrong.
- Keep the original sentence in the DOM before JS runs.

```javascript
function splitAccessibly(el, type = 'words') {
  el.setAttribute('aria-label', el.textContent.trim());
  const split = SplitText.create(el, { type });
  for (const part of [split.chars, split.words, split.lines].flat().filter(Boolean)) part.setAttribute('aria-hidden', 'true');
  return split;
}
```

## 1. Split Converge

Title halves fly in from opposite sides, meet, hold, fly out. Needs a pin.

```html
<h1 class="hero-title" aria-label="Your Brand Name">
  <span class="word word-left" aria-hidden="true">Your</span><span class="word word-left" aria-hidden="true">Brand</span>
  <span class="word word-right" aria-hidden="true">Name</span><span class="word word-right" aria-hidden="true">Here</span>
</h1>
```

```javascript
const L = gsap.utils.toArray('.word-left'), R = gsap.utils.toArray('.word-right');
gsap.timeline({ defaults: { ease: 'none' },
  scrollTrigger: { trigger: scene, start: 'top top', end: '+=250%', pin: true, scrub: 1.2 } })
  .fromTo(L, { x: '-120vw', opacity: 0 }, { x: 0, opacity: 1, duration: 0.25, stagger: 0.03 }, 0)
  .fromTo(R, { x:  '120vw', opacity: 0 }, { x: 0, opacity: 1, duration: 0.25, stagger: -0.03 }, 0)
  .to({}, { duration: 0.45 })                                  // hold: readable window
  .to(L, { x: '-120vw', opacity: 0, duration: 0.28, stagger: 0.02 })
  .to(R, { x:  '120vw', opacity: 0, duration: 0.28, stagger: -0.02 }, '<');
```

Hold segment is the only time user can read. Make it the longest.

## 2. Masked Line Reveal

Lines slide up from behind an `overflow: hidden` mask.

```javascript
const split = SplitText.create(el, { type: 'lines', mask: 'lines' });   // 3.13+: mask built in
gsap.from(split.lines, { yPercent: 110, duration: 0.9, ease: 'power4.out', stagger: 0.12,
  scrollTrigger: { trigger: el, start: 'top 80%', once: true } });
```

Older SplitText: wrap each line in a `.line-mask { overflow: hidden }` yourself.

## 3. Cylinder Rotation

Letters roll in on a 3D axis behind them.

```css
.cylinder { perspective: 800px; }
.cylinder .char { display: inline-block; transform-origin: 50% 50% -60px; transform-style: preserve-3d; }
```

```javascript
gsap.from(SplitText.create(el, { type: 'chars' }).chars,
  { rotateX: -90, opacity: 0, duration: 0.6, ease: 'back.out(1.5)', stagger: 0.04,
    scrollTrigger: { trigger: el, start: 'top 75%', once: true } });
```

Short strings only (a number, one word). Long text = hundreds of 3D nodes.

## 4. Word Lighting

Prose dim, then each word lights as scroll advances.

```css
.lit-text .word { opacity: 0.15; }
```

One scrubbed timeline. No per-update class toggling loop:

```javascript
const words = SplitText.create(el, { type: 'words' }).words;
gsap.timeline({ scrollTrigger: { trigger: section, start: 'top top', end: `+=${words.length * 80}`, pin: true, scrub: 0.5 } })
  .to(words, { opacity: 1, stagger: 1, ease: 'none' });
```

Dim state must still pass contrast for users who never scroll the effect: reduced motion shows all words at `opacity: 1`. About 80px of scroll per word; slow it for luxury.

## 5. Scramble

Characters cycle random glyphs, then resolve. Final text is already in the DOM.

```javascript
function scramble(el, duration = 1.6) {
  const final = el.textContent;
  const glyphs = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%';
  el.setAttribute('aria-label', final);           // screen reader gets the final text once
  const t0 = performance.now();
  (function step(now) {
    const p = Math.min((now - t0) / (duration * 1000), 1);
    el.textContent = [...final].map((c, i) =>
      c === ' ' || i / final.length < p ? c : glyphs[(Math.random() * glyphs.length) | 0]).join('');
    if (p < 1) requestAnimationFrame(step);
  })(t0);
}
ScrollTrigger.create({ trigger: el, start: 'top 80%', once: true, onEnter: () => scramble(el) });
```

Keep it on short labels. Reduced motion: skip.

## 6. Skew Bounce

Rise with a skew that corrects, plus overshoot.

```javascript
gsap.from(items, { y: 80, skewY: 7, opacity: 0, duration: 0.9, ease: 'back.out(1.7)', stagger: 0.1,
  scrollTrigger: { trigger: items[0], start: 'top 85%', once: true } });
```

## 7. Theatrical Enter / Exit

CSS only. Enters on view, leaves on exit. Fallback = plain visible text.

```css
@keyframes t-in  { from { opacity: 0; transform: translateY(60px); } }
@keyframes t-out { to   { opacity: 0; transform: translateY(-60px); } }

@supports (animation-timeline: view()) {
  @media (prefers-reduced-motion: no-preference) {
    .theatrical {
      animation: t-in linear both, t-out linear both;
      animation-timeline: view(), view();
      animation-range: entry 0% entry 40%, exit 60% exit 100%;
    }
  }
}
```

Support: Chromium and Safari 26+; Firefox behind flag at last check. Unsupported browsers just show the text. That is the correct degrade.

## 8. Offset Diagonal

Two lines, top-left and lower-right, entering from opposite sides.

```css
.offset-title .line-1 { display: block; text-align: left;  padding-left: 5%;  font-size: clamp(48px, 8vw, 100px); }
.offset-title .line-2 { display: block; text-align: right; padding-right: 5%; margin-top: .4em; font-size: clamp(48px, 8vw, 100px); }
```

```javascript
const st = { trigger: title, start: 'top 75%', once: true };
gsap.from('.line-1', { x: '-15vw', opacity: 0, duration: 1, ease: 'power4.out', scrollTrigger: st });
gsap.from('.line-2', { x:  '15vw', opacity: 0, duration: 1, ease: 'power4.out', delay: 0.15, scrollTrigger: st });
```

## 9. Line Clip Wipe

Each line sweeps left → right.

```javascript
const { lines } = SplitText.create(el, { type: 'lines' });
gsap.fromTo(lines, { clipPath: 'inset(0 100% 0 0)' },
  { clipPath: 'inset(0 0% 0 0)', duration: 0.8, ease: 'power3.out', stagger: 0.12,
    scrollTrigger: { trigger: el, start: 'top 80%', once: true } });
```

## 10. Reactive Marquee

Endless text. Scroll speed pushes it faster.

```css
.marquee { overflow: hidden; white-space: nowrap; }
.marquee-track { display: inline-flex; gap: 4rem; will-change: transform; }
.marquee-item { font-size: clamp(2rem, 5vw, 5rem); font-weight: 700; letter-spacing: -0.02em; }
```

```javascript
function reactiveMarquee(wrap) {
  const track = wrap.querySelector('.marquee-track');          // content duplicated once for a seamless loop
  const half = () => track.scrollWidth / 2;
  let x = 0, boost = 0, lastY = scrollY, onScreen = true;

  new IntersectionObserver(([e]) => { onScreen = e.isIntersecting; }).observe(wrap);
  addEventListener('scroll', () => { boost = Math.min(Math.abs(scrollY - lastY) * 0.15, 20); lastY = scrollY; }, { passive: true });

  gsap.ticker.add(() => {
    if (!onScreen) return;                                     // no work off-screen
    boost *= 0.92;
    x = (x - (0.8 + boost)) % half();
    track.style.transform = `translate3d(${x}px,0,0)`;
  });
}
```

Reduced motion: static row, no ticker. Duplicate copy gets `aria-hidden`.

## 11. Variable-Font Wave

Weight axis ripples across letters. Needs a variable font (Inter Variable, Fraunces, Recursive).

```javascript
gsap.to(SplitText.create(el, { type: 'chars' }).chars,
  { fontVariationSettings: '"wght" 800', duration: 0.4, ease: 'power2.inOut', stagger: { each: 0.06, yoyo: true, repeat: -1 } });
```

Changing weight changes glyph width, so this IS layout. One short headline, decorative, never in body copy, off for reduced motion. Endless loop > 5s needs pause (see `scroll-accessibility.md`).

## 12. Bleed Type

Giant headline crossing section borders.

```css
.bleed-title { font-size: clamp(80px, 18vw, 220px); font-weight: 900; line-height: .9; letter-spacing: -.04em;
               margin-inline: -.05em; position: relative; z-index: 10; pointer-events: none; translate: 0 30%; }
.bleed-section { position: relative; z-index: 2; overflow: visible; }
.bleed-section + .next-section { position: relative; z-index: 3; }   /* next section traps the lower half */
```

```javascript
gsap.to('.bleed-title', { yPercent: -12, ease: 'none',
  scrollTrigger: { trigger: '.bleed-section', start: 'top bottom', end: 'bottom top', scrub: true } });
```

Watch horizontal overflow on phones: `overflow-x: clip` on the page wrapper.

## 13. Ghost Outline

Huge stroke-only text behind the hero.

```css
.ghost { color: transparent; -webkit-text-stroke: 1px rgb(255 255 255 / .15);
         font: 900 clamp(5rem, 15vw, 18rem)/.85 var(--display); letter-spacing: -.04em;
         white-space: nowrap; user-select: none; pointer-events: none; z-index: 2; }
```

| Stroke opacity | Reads as |
|---|---|
| 0.08–0.12 | Barely-there air |
| 0.15–0.22 | Subtle, visible on inspection |
| 0.25–0.35 | Focal. Only if text IS the visual |

Rules: `aria-hidden="true"`, never the real `<h1>`; dark backgrounds only; max 2 lines; weight 800–900; z-index below hero (level 3).

```javascript
gsap.set(lines, { yPercent: 110 });
gsap.to(lines, { yPercent: 0, stagger: 0.1, duration: 1.1, ease: 'power4.out', delay: 0.2 });
// exit, on the hero scrub timeline `tl`:
tl.to(line1, { x: '-12vw', opacity: 0.06, duration: 0.3 }, 0).to(line2, { x: '12vw', opacity: 0.06, duration: 0.3 }, 0);
```

## Layering For A Hero

```javascript
gsap.timeline({ scrollTrigger: { trigger: '.hero', start: 'top top', end: '+=300%', pin: true, scrub: 1 } })
  .from('.hero-sub .line', { yPercent: 110, duration: 0.2, stagger: 0.05 }, 0)   // 2. masked reveal
  .from('.hero-cta', { y: 40, skewY: 5, opacity: 0, duration: 0.15, ease: 'back.out' }, 0.15)  // 6. skew bounce
  .to('.word-left',  { x: '-80vw', opacity: 0, duration: 0.25, stagger: 0.03 }, 0.7)           // 1. converge exit
  .to('.word-right', { x:  '80vw', opacity: 0, duration: 0.25, stagger: -0.03 }, 0.7);
```

Bleed title (12) is CSS, already on screen. Stack no more than three techniques in one scene.
