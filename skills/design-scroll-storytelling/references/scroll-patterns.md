# Scroll Patterns

Illustrative patterns for scroll-driven experiences. Pseudocode shows structure and key parameters — implement using the project's actual library and current API.

---

## Parallax Layers

Depth illusion: layers move at different speeds relative to scroll. Background slowest, floating elements fastest.

**Speed ratios:**

| Layer | Speed | Effect |
|-------|-------|--------|
| Background | ~0.2x | Far, slow |
| Midground | ~0.5x | Middle depth |
| Foreground | 1.0x | Normal |
| Floating elements | ~1.2x | Pop forward |

```
// For each layer:
onScroll(scrollY) {
  layer.translateY = scrollY * speedMultiplier
}
// Only animate transform — never top/margin/height
```

---

## Scrub Animation

Scroll position is the playhead. Animation plays forward on scroll down, reverses on scroll up. No auto-play.

```
animation = defineAnimation(element, { from: stateA, to: stateB })

onScroll(progress) {           // progress: 0.0 → 1.0
  animation.seek(progress)     // drives animation, not time
}

// scrubStrength: low = tight/immediate, high = cinematic lag
```

---

## Scroll-Triggered Reveal

One-shot animation fires when element crosses a viewport threshold. Plays once to completion — does not reverse.

```
observe(element, {
  triggerAt: "element.top reaches viewport 60%",
  onEnter: () => animate(element, { opacity: 0→1, translateY: 40px→0 })
})
// Animate only opacity and transform
```

---

## Sticky Section

Element pinned at `top: 0` while scroll travels through a defined range. Content inside animates during the pin window.

```
pin(element, {
  startAt: "element.top reaches viewport.top",
  holdFor: 150vh,              // scroll travel while pinned
})

// While pinned, animate inner content:
scrub(innerContent, {
  scrollRange: [pinStart, pinEnd],
  translateX: 0 → -100vw      // e.g. panel swipe
})
```

Good for: feature walkthroughs, before/after, step-by-step, image galleries.

---

## Horizontal Scroll Section

Vertical scroll drives horizontal panel travel. Container pinned; panels translate left as scroll progresses.

```
pin(container, { holdFor: panelCount * 100vw })

scrub(panelTrack, {
  scrollRange: [pinStart, pinEnd],
  translateX: 0 → -(panelWidth * (panelCount - 1))
})
// Total travel = panelWidth × (panelCount − 1)
```

---

## Text Reveal

Text split into units (words or characters). Units stagger in across a shared scroll range.

```
units = splitText(element, by: "word" | "char")

units.forEach((unit, i) => {
  scrub(unit, {
    scrollRange: [triggerStart + i * staggerOffset, ...],
    opacity: 0→1,
    translateY: 20px→0
  })
})
```

---

## Accessibility: Reduced Motion

Non-negotiable. All scroll animations must respect this.

```css
@media (prefers-reduced-motion: reduce) {
  /* Remove all scroll-driven transforms and animations.
     Content must be fully readable with no animation. */
  [data-scroll-animate] {
    animation: none;
    transform: none;
    opacity: 1;
  }
}
```

---

## Mobile: Disable or Simplify Parallax

Continuous scroll tracking causes jank on touch devices. Detect at init and bail out or substitute.

```
if (isTouchDevice || viewportWidth < breakpoint) {
  // Option A: skip parallax entirely, render layers static
  // Option B: replace scrub with simple one-shot fade-in on enter
  registerSimpleFallback()
} else {
  registerFullParallax()
}
// Always test on real device — DevTools throttle ≠ touch scroll
```
