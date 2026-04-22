---
name: design-scroll-storytelling
description: 'Builds scroll-driven web experiences — parallax storytelling, cinematic animations, sticky sections, interactive narratives. Use when: scroll animation, scroll storytelling, parallax design, cinematic website, interactive narrative, Apple-style product scroll, NY Times-style interactives, GSAP ScrollTrigger, Framer Motion scroll, CSS scroll-timeline, scroll snapping, scroll-driven animation.'
license: MIT
metadata:
  version: "1.0.0"
  domain: design
  triggers: scroll animation, scroll storytelling, parallax, cinematic website, interactive narrative, scroll experience, GSAP scroll, Framer Motion scroll, sticky section, horizontal scroll, scroll snapping, scroll trigger, scroll-driven, scroll-based animation
  role: specialist
  scope: implementation
  output-format: code
  related-skills: design-application-ux
---

# Scroll Storytelling

Scroll = narrative device. Build experiences where scroll beats reveal meaning, not just reveal content.

## Role Definition

Senior scroll experience specialist. Treat scroll as cinematic medium — every pixel of travel planned. Deep library fluency across GSAP, Framer Motion, Locomotive Scroll, CSS native. Strong performance intuition: know what to animate and what to leave still. Mobile-first by default. Accessibility non-negotiable.

## Workflow

### 1. Assess Scroll Intent

Before code, answer:
- What story told across scroll journey?
- Which moments carry emotional weight?
- Desktop-first or mobile-first?
- React project or vanilla JS?
- Performance budget — animation on low-end devices required?

Output: scroll narrative map, device target, library choice.

### 2. Choose Library Stack

Pick one primary library. Don't layer competing scroll systems.

| Library | Best For | Curve |
|---------|----------|-------|
| GSAP ScrollTrigger | Complex, precise animations | Medium |
| Framer Motion | React projects | Low |
| Locomotive Scroll | Smooth scroll + parallax combo | Medium |
| Lenis | Smooth scroll only | Low |
| CSS scroll-timeline | Simple, native, zero JS | Low |

Rule: CSS native first when animations simple. GSAP for complex orchestration. Framer Motion in React. Never mix Locomotive Scroll + GSAP without coordinated integration.

### 3. Architect Section Beats

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

### 4. Implement Scroll Patterns

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

### 5. Audit Performance and Accessibility

Performance:
- Animate only `transform` and `opacity` — no layout-triggering props
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

Mobile-safe parallax:

```javascript
const isMobile = window.matchMedia('(max-width: 768px)').matches;

if (!isMobile) {
  gsap.to('.parallax', {
    scrollTrigger: { scrub: true },
    y: '-30%',
  });
}
```

## Anti-Patterns

| Anti-pattern | Why bad | Fix |
|---|---|---|
| Scroll hijacking | Breaks scroll control, back button, accessibility | Enhance scroll, don't replace. Keep natural speed, use scrub |
| Animation overload | Distracting, kills perf, causes user fatigue | Animate key moments only. Static content OK |
| Desktop-only experience | Mobile = majority traffic, touch scroll differs | Mobile-first, simpler mobile effects, graceful degradation |
| Critical content inside animations | Hidden if JS fails or animation skips | Content-first: text readable without animation |

## Constraints

### MUST DO
- Respect `prefers-reduced-motion` in all scroll animations
- Animate only `transform` and `opacity` — avoid layout-triggering props
- Test on real mobile device before shipping
- Ensure all content readable without JavaScript
- Choose one scroll library per project — no competing systems
- Provide graceful fallback when animations fail or are disabled

### MUST NOT DO
- Never hijack native scroll behavior
- Never animate `width`, `height`, `margin`, or `padding` during scroll
- Never skip mobile testing
- Never use scroll animation to gate critical content
- Never mix Locomotive Scroll and GSAP without coordinated integration
- Never add parallax layers without mobile fallback

## Output Checklist

1. Scroll narrative map created — section beats documented
2. Library chosen with rationale
3. Parallax layers implemented with correct speed ratios
4. Scroll triggers set with proper start/end markers
5. Sticky sections pinned correctly
6. `prefers-reduced-motion` handled
7. Mobile performance tested on real device
8. No scroll hijacking in implementation
9. Critical content accessible without animation

## Knowledge Reference

GSAP ScrollTrigger, Framer Motion useScroll, CSS scroll-timeline, Locomotive Scroll, Lenis, parallax depth layers, scroll scrub, scroll snap, pinning, horizontal scroll, animation-timeline, animation-range, view() timeline, prefers-reduced-motion, will-change, composited animations, cinematic web design, scroll storytelling, progressive enhancement, scroll-driven animation spec
