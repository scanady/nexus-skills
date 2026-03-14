# Product Overview Page Patterns

Structural patterns, section blueprints, animation recipes, and screenshot techniques extracted from top-tier product pages (Stripe, Bestow, Linear, Notion, Vercel, Figma).

---

## Page Archetypes

### 1. Stripe-Style (Feature-Dense Technical Product)

Best for: developer tools, APIs, payment platforms, infrastructure products.

```
┌─────────────────────────────────────────┐
│  HERO                                   │
│  Big headline (benefit) + subheadline   │
│  Two CTAs (primary + secondary)         │
│  Hero screenshot/product visual         │
├─────────────────────────────────────────┤
│  FEATURE HIGHLIGHTS (3–4 blocks)        │
│  Alternating: text-left/img-right,      │
│  then text-right/img-left               │
│  Each: headline + 2-line desc + image   │
├─────────────────────────────────────────┤
│  LOGO BAR                               │
│  Row of customer logos, muted colors    │
├─────────────────────────────────────────┤
│  TABBED DEEP-DIVE                       │
│  Section title + subtitle               │
│  Tab bar: [Product A] [Product B] [C]   │
│  Each tab: headline + 3 bullet features │
│  + large screenshot + explore CTA       │
├─────────────────────────────────────────┤
│  STATS BAR                              │
│  3–4 big numbers with labels            │
│  e.g. "11.9% revenue uplift"            │
├─────────────────────────────────────────┤
│  TESTIMONIALS                           │
│  Carousel or grid of 2–4 quotes         │
│  Name + title + company + logo          │
├─────────────────────────────────────────┤
│  ADVANCED FEATURES / CAPABILITIES       │
│  Grid of 4–6 icon + text cards          │
├─────────────────────────────────────────┤
│  PRICING (optional)                     │
│  2–3 tiers side by side                 │
├─────────────────────────────────────────┤
│  FOOTER CTA                             │
│  "Ready to get started?" + buttons      │
│  Related product links below            │
└─────────────────────────────────────────┘
```

**Key traits:**
- Heavy use of anchored section navigation (sticky subnav)
- Screenshots show actual UI — not abstract illustrations
- Metrics are prominent with large type
- Tabs group related sub-products to prevent scroll fatigue
- Dark-on-light primary, with occasional dark sections for contrast

### 2. Bestow-Style (B2B / Enterprise SaaS)

Best for: enterprise tools, insurance tech, admin platforms, B2B portals.

```
┌─────────────────────────────────────────┐
│  HERO                                   │
│  Headline + short description           │
│  Single CTA button                      │
├─────────────────────────────────────────┤
│  VALUE PROPS (3 cards)                  │
│  Icon + title + short description       │
│  Arranged in a row                      │
├─────────────────────────────────────────┤
│  TABBED OVERVIEW                        │
│  Section title + paragraph              │
│  Tabs: [Suite] [Portal] [Features]      │
│  Selected tab shows screenshot panel    │
├─────────────────────────────────────────┤
│  FEATURE CARDS WITH SCREENSHOTS         │
│  2x2 grid of cards                      │
│  Each: screenshot thumbnail + title     │
│  + short description                    │
├─────────────────────────────────────────┤
│  PROCESS / TIMELINE                     │
│  3-step visual workflow                 │
│  Icon + title + bullet list each        │
├─────────────────────────────────────────┤
│  CASE STUDY / DOWNLOAD CTA             │
│  Callout box with resource link         │
├─────────────────────────────────────────┤
│  RELATED PRODUCTS                       │
│  2–3 cards linking to other products    │
├─────────────────────────────────────────┤
│  CONTACT CTA                            │
│  "Let's connect" + form or button       │
└─────────────────────────────────────────┘
```

**Key traits:**
- Cleaner, more corporate feel
- Value props up front before any detail
- Screenshots in cards rather than full-bleed
- Process/timeline sections to show workflow
- Download/resource CTAs for lead generation

### 3. Showcase-Style (Consumer / Design Product)

Best for: design tools, consumer apps, creative products, portfolios.

```
┌─────────────────────────────────────────┐
│  HERO (full-bleed)                      │
│  Large product screenshot as backdrop   │
│  Overlay: headline + CTA               │
├─────────────────────────────────────────┤
│  FEATURE SCROLL                         │
│  Sticky text on left, screenshots       │
│  scroll on right (or vice versa)        │
│  3–5 feature steps                      │
├─────────────────────────────────────────┤
│  FULL-WIDTH SCREENSHOT BREAK            │
│  Edge-to-edge product visual            │
├─────────────────────────────────────────┤
│  BENEFIT GRID                           │
│  2x3 grid of icon + headline + desc     │
├─────────────────────────────────────────┤
│  SOCIAL PROOF                           │
│  Press logos or testimonial strip        │
├─────────────────────────────────────────┤
│  DOWNLOAD / SIGNUP CTA                  │
│  App store badges or email signup       │
└─────────────────────────────────────────┘
```

**Key traits:**
- Screenshots ARE the design — they dominate the page
- Minimal text, maximum visual impact
- Parallax and scroll-linked effects
- Cinematic full-bleed sections
- Often uses dark background with glowing product UI

### 4. Hub-Style (Multi-Product Platform)

Best for: platforms with multiple distinct products, marketplaces.

```
┌─────────────────────────────────────────┐
│  HERO                                   │
│  Platform headline + value prop         │
│  CTA buttons                            │
├─────────────────────────────────────────┤
│  PRODUCT GRID                           │
│  3–6 cards, each a sub-product          │
│  Icon + name + one-line desc + link     │
├─────────────────────────────────────────┤
│  EXPANDABLE FEATURE SECTIONS            │
│  One per product, accordion or scroll   │
│  Screenshot + feature list each         │
├─────────────────────────────────────────┤
│  COMPARISON TABLE (optional)            │
│  Feature matrix across products         │
├─────────────────────────────────────────┤
│  INTEGRATIONS / ECOSYSTEM               │
│  Logo grid of partners and integrations │
├─────────────────────────────────────────┤
│  UNIFIED CTA                            │
│  "Get started with [Platform]"          │
└─────────────────────────────────────────┘
```

---

## Section Blueprints

### Hero Section

The hero sets the entire tone. Must accomplish three things in under 3 seconds: (1) what the product does, (2) why it matters, (3) what to do next.

**Anatomy:**
```html
<section class="hero">
  <div class="hero-content">
    <h1>Benefit-driven headline</h1>
    <p>One or two sentences adding specificity</p>
    <div class="hero-ctas">
      <a class="btn-primary">Primary action</a>
      <a class="btn-secondary">Secondary action</a>
    </div>
  </div>
  <div class="hero-visual">
    <!-- Product screenshot in device frame -->
  </div>
</section>
```

**Headline formulas:**
- "[Verb] + [outcome] + [qualifier]" → "Convert more customers with intelligent checkout"
- "[Adjective] + [noun] + for [audience]" → "Unified payments for global businesses"
- "[Outcome] + without [pain]" → "Ship faster without breaking things"

**Visual approaches:**
- Screenshot floating with perspective shadow (Stripe-style)
- Full-browser-frame screenshot (Linear-style)
- Product UI composited over gradient/pattern background
- Animated screenshot showing workflow sequence

### Feature Highlight Block

The workhorse section. Repeat 3–5 times with alternating layout.

**Anatomy:**
```html
<section class="feature-block">
  <div class="feature-text">
    <h2>Benefit headline</h2>
    <p>2–3 sentences explaining the feature and its impact</p>
    <a class="feature-link">Learn more →</a>
  </div>
  <div class="feature-visual">
    <!-- Screenshot with annotations or highlight overlays -->
  </div>
</section>
```

**Layout alternation:**
- Odd blocks: text left (40%), image right (60%)
- Even blocks: image left (60%), text right (40%)
- The image side should always be larger — screenshots need room

### Tabbed Product Showcase

Groups multiple sub-features without scroll fatigue.

**Anatomy:**
```html
<section class="product-showcase">
  <h2>Section headline</h2>
  <p>Brief context paragraph</p>
  <div class="tab-bar">
    <button class="tab active">Product A</button>
    <button class="tab">Product B</button>
    <button class="tab">Product C</button>
  </div>
  <div class="tab-panel active">
    <div class="panel-content">
      <h3>Sub-headline</h3>
      <ul class="feature-list">
        <li>Feature with icon</li>
        <li>Feature with icon</li>
        <li>Feature with icon</li>
      </ul>
      <a class="panel-cta">Explore →</a>
    </div>
    <div class="panel-visual">
      <!-- Large screenshot -->
    </div>
  </div>
</section>
```

**Tab transition:** Crossfade panels (opacity 0→1, 300ms ease).

### Stats / Metrics Bar

Social proof through numbers. Must feel impactful, not informational.

**Anatomy:**
```html
<section class="stats-bar">
  <div class="stat">
    <span class="stat-number" data-target="11.9">0</span>
    <span class="stat-suffix">%</span>
    <p class="stat-label">average revenue uplift</p>
  </div>
  <!-- Repeat 3–4 times -->
</section>
```

**Design rules:**
- Large type for numbers (48–72px)
- Animated counter on scroll-into-view (count from 0 to target over 1.5s)
- Add context below: "average revenue uplift" not just "revenue"
- Dark background section works well for contrast

### Testimonial Section

**Anatomy:**
```html
<section class="testimonials">
  <div class="testimonial-card">
    <blockquote>"Quote text here."</blockquote>
    <div class="attribution">
      <span class="name">Full Name</span>
      <span class="role">Title, Company</span>
    </div>
    <img class="company-logo" src="..." alt="Company" />
  </div>
</section>
```

**Layouts:**
- Single featured quote (large, centered)
- Carousel with dots/arrows (auto-advance optional)
- 2–3 cards in a row
- Alternating left/right with colored accent borders

---

## Screenshot Presentation Techniques

### Browser Frame
```css
.browser-frame {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}
.browser-toolbar {
  background: #f0f0f0;
  padding: 12px 16px;
  display: flex;
  gap: 8px;
  align-items: center;
}
.browser-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #ddd;
}
.browser-dot:first-child { background: #ff5f57; }
.browser-dot:nth-child(2) { background: #ffbd2e; }
.browser-dot:nth-child(3) { background: #28c840; }
```

### Floating with Perspective
```css
.screenshot-float {
  border-radius: 16px;
  box-shadow:
    0 20px 60px rgba(0, 0, 0, 0.15),
    0 0 0 1px rgba(0, 0, 0, 0.05);
  transform: perspective(1200px) rotateY(-5deg) rotateX(2deg);
  transition: transform 0.5s ease;
}
.screenshot-float:hover {
  transform: perspective(1200px) rotateY(0deg) rotateX(0deg);
}
```

### Phone Frame
```css
.phone-frame {
  width: 280px;
  padding: 12px;
  border-radius: 36px;
  background: #1a1a1a;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
}
.phone-frame .screen {
  border-radius: 24px;
  overflow: hidden;
}
.phone-frame .notch {
  width: 120px;
  height: 28px;
  background: #1a1a1a;
  border-radius: 0 0 16px 16px;
  margin: 0 auto;
  position: relative;
  top: -1px;
}
```

### Annotation Overlays
```css
.screenshot-annotated {
  position: relative;
}
.callout {
  position: absolute;
  background: var(--accent);
  color: white;
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  white-space: nowrap;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
.callout::before {
  content: '';
  position: absolute;
  width: 2px;
  height: 30px;
  background: var(--accent);
  /* Position based on callout direction */
}
```

---

## Animation Recipes

### Scroll-Triggered Fade-Up (Foundation)

Apply to every section. This is the bread and butter.

```js
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.15 });

document.querySelectorAll('.animate-on-scroll').forEach(el => {
  observer.observe(el);
});
```

```css
.animate-on-scroll {
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.6s ease-out, transform 0.6s ease-out;
}
.animate-on-scroll.visible {
  opacity: 1;
  transform: translateY(0);
}

/* Stagger children */
.stagger-children .animate-on-scroll:nth-child(1) { transition-delay: 0ms; }
.stagger-children .animate-on-scroll:nth-child(2) { transition-delay: 100ms; }
.stagger-children .animate-on-scroll:nth-child(3) { transition-delay: 200ms; }
.stagger-children .animate-on-scroll:nth-child(4) { transition-delay: 300ms; }
```

### Hero Load-In Sequence

```css
.hero-content > * {
  opacity: 0;
  transform: translateY(20px);
  animation: fadeInUp 0.7s ease-out forwards;
}
.hero-content h1    { animation-delay: 0.1s; }
.hero-content p     { animation-delay: 0.25s; }
.hero-content .ctas { animation-delay: 0.4s; }
.hero-visual        {
  opacity: 0;
  transform: translateY(40px) scale(0.97);
  animation: fadeInUpScale 0.8s ease-out 0.5s forwards;
}

@keyframes fadeInUp {
  to { opacity: 1; transform: translateY(0); }
}
@keyframes fadeInUpScale {
  to { opacity: 1; transform: translateY(0) scale(1); }
}
```

### Animated Counter

```js
function animateCounter(element) {
  const target = parseFloat(element.dataset.target);
  const decimals = (target.toString().split('.')[1] || '').length;
  const duration = 1500;
  const start = performance.now();

  function update(now) {
    const elapsed = now - start;
    const progress = Math.min(elapsed / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
    const current = target * eased;
    element.textContent = current.toFixed(decimals);
    if (progress < 1) requestAnimationFrame(update);
  }
  requestAnimationFrame(update);
}
```

### Tab Crossfade

```js
tabs.forEach(tab => {
  tab.addEventListener('click', () => {
    const targetId = tab.dataset.tab;
    // Deactivate all
    tabs.forEach(t => t.classList.remove('active'));
    panels.forEach(p => {
      p.classList.remove('active');
      p.style.opacity = '0';
    });
    // Activate selected
    tab.classList.add('active');
    const panel = document.getElementById(targetId);
    panel.classList.add('active');
    requestAnimationFrame(() => {
      panel.style.opacity = '1';
    });
  });
});
```

```css
.tab-panel {
  display: none;
  opacity: 0;
  transition: opacity 0.3s ease;
}
.tab-panel.active {
  display: grid; /* or flex */
  opacity: 1;
}
```

### Subtle Parallax on Scroll

```js
window.addEventListener('scroll', () => {
  const scrolled = window.scrollY;
  document.querySelectorAll('[data-parallax]').forEach(el => {
    const speed = parseFloat(el.dataset.parallax) || 0.1;
    const rect = el.getBoundingClientRect();
    const offset = (rect.top + scrolled - window.innerHeight / 2) * speed;
    el.style.transform = `translateY(${offset}px)`;
  });
}, { passive: true });
```

### Reduced Motion Respect

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
  .animate-on-scroll {
    opacity: 1;
    transform: none;
  }
}
```

---

## CSS Architecture Pattern

Use this variable structure for consistent theming:

```css
:root {
  /* Colors */
  --color-primary: #...;
  --color-primary-dark: #...;
  --color-accent: #...;
  --color-text: #...;
  --color-text-secondary: #...;
  --color-bg: #...;
  --color-bg-alt: #...;
  --color-surface: #...;
  --color-border: #...;

  /* Typography */
  --font-display: '...', sans-serif;
  --font-body: '...', sans-serif;
  --font-mono: '...', monospace;

  /* Spacing */
  --section-padding: 120px;
  --container-width: 1200px;
  --gap: 24px;

  /* Shadows */
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.08);
  --shadow-md: 0 4px 16px rgba(0,0,0,0.1);
  --shadow-lg: 0 20px 60px rgba(0,0,0,0.15);
  --shadow-screenshot: 0 25px 50px -12px rgba(0,0,0,0.25);

  /* Radii */
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-xl: 24px;
}
```

---

## Responsive Breakpoints

```css
/* Tablet */
@media (max-width: 1024px) {
  :root { --section-padding: 80px; }
  .feature-block { flex-direction: column; }
  .feature-visual { order: -1; } /* Image on top on tablet */
}

/* Mobile */
@media (max-width: 640px) {
  :root { --section-padding: 60px; }
  .stats-bar { flex-direction: column; gap: 32px; }
  .tab-bar { overflow-x: auto; white-space: nowrap; }
  h1 { font-size: 2rem; }
  h2 { font-size: 1.5rem; }
}
```
