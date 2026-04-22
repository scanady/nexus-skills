# Product Tour Patterns

Interactive patterns for showcasing platform capabilities — tabbed explorers, sticky scroll walkthroughs, guided tours, and feature discovery interfaces that let visitors explore at their own pace.

---

## Table of Contents

1. [Tabbed Platform Tour](#tabbed-platform-tour)
2. [Sticky Scroll Walkthrough](#sticky-scroll-walkthrough)
3. [Guided Feature Discovery](#guided-feature-discovery)
4. [Interactive Before/After](#interactive-beforeafter)
5. [Step-by-Step Process](#step-by-step-process)
6. [Audience-Segmented Tour](#audience-segmented-tour)

---

## Tabbed Platform Tour

The most effective pattern for feature-rich products (5+ capabilities). Used by SpikeForge's "Everything you need" section, Stripe's product pages, and Notion's feature explorer.

### When to Use
- Product has 5–10 distinct features/capabilities
- Each feature has its own UI/screenshot worth showing
- Visitors have different interests and should self-select what to explore
- The alternative (one long scroll) would cause fatigue

### Structure

```
┌─────────────────────────────────────────────────┐
│  SECTION LABEL (small caps, accent color)       │
│                                                 │
│  Section Headline                               │
│  Brief context paragraph                        │
│                                                 │
│  ┌──────┬──────┬──────┬──────┬──────┬──────┐   │
│  │ Tab1 │ Tab2 │ Tab3 │ Tab4 │ Tab5 │ Tab6 │   │
│  └──────┴──────┴──────┴──────┴──────┴──────┘   │
│                                                 │
│  ┌─────────────────────────────────────────┐    │
│  │  ┌─────────────┐  ┌─────────────────┐  │    │
│  │  │ Feature     │  │                 │  │    │
│  │  │ Headline    │  │  [Screenshot]   │  │    │
│  │  │             │  │                 │  │    │
│  │  │ • Bullet 1  │  │                 │  │    │
│  │  │ • Bullet 2  │  │                 │  │    │
│  │  │ • Bullet 3  │  │                 │  │    │
│  │  │             │  │                 │  │    │
│  │  │ [See more →]│  │                 │  │    │
│  │  └─────────────┘  └─────────────────┘  │    │
│  └─────────────────────────────────────────┘    │
│                                                 │
│  [See all features →]                           │
└─────────────────────────────────────────────────┘
```

### Implementation

```html
<section class="platform-tour">
  <span class="section-label">EXPLORE THE PLATFORM</span>
  <h2>Everything you need to [outcome]</h2>
  <p>Brief context about the platform's breadth</p>

  <div class="tour-tabs" role="tablist">
    <button class="tour-tab active" role="tab" aria-selected="true" data-tab="feature-1">
      Feature 1
    </button>
    <button class="tour-tab" role="tab" aria-selected="false" data-tab="feature-2">
      Feature 2
    </button>
    <!-- ... more tabs -->
  </div>

  <div class="tour-panels">
    <div class="tour-panel active" role="tabpanel" id="feature-1">
      <div class="panel-content">
        <h3>Feature headline (benefit-driven)</h3>
        <p>2-sentence description of what this does and why it matters</p>
        <ul class="feature-bullets">
          <li>Specific capability with concrete detail</li>
          <li>Another capability</li>
          <li>Third capability</li>
        </ul>
      </div>
      <div class="panel-visual">
        <div class="browser-frame">
          <img src="./screenshots/feature-1-name.png" alt="Description" loading="lazy" />
        </div>
      </div>
    </div>
    <!-- ... more panels -->
  </div>
</section>
```

### Tab Bar Styling

```css
.tour-tabs {
  display: flex;
  gap: 0;
  border-bottom: 2px solid var(--border-light);
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
}
.tour-tabs::-webkit-scrollbar { display: none; }

.tour-tab {
  padding: 12px 24px;
  border: none;
  background: transparent;
  color: var(--text-muted);
  font-weight: 500;
  font-size: 15px;
  cursor: pointer;
  white-space: nowrap;
  position: relative;
  transition: color 0.2s ease;
}
.tour-tab::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--brand-primary);
  transform: scaleX(0);
  transition: transform 0.3s ease;
}
.tour-tab.active {
  color: var(--brand-primary);
  font-weight: 600;
}
.tour-tab.active::after {
  transform: scaleX(1);
}
.tour-tab:hover {
  color: var(--text-primary);
}
```

### Panel Transition

```css
.tour-panel {
  display: none;
  opacity: 0;
  transform: translateY(10px);
}
.tour-panel.active {
  display: grid;
  grid-template-columns: 1fr 1.4fr;
  gap: 60px;
  align-items: center;
  animation: panelFadeIn 0.4s ease-out forwards;
}
@keyframes panelFadeIn {
  to { opacity: 1; transform: translateY(0); }
}

/* Mobile: stack vertically */
@media (max-width: 768px) {
  .tour-panel.active {
    grid-template-columns: 1fr;
    gap: 32px;
  }
}
```

### Tab Switching JS

```js
const tourTabs = document.querySelectorAll('.tour-tab');
const tourPanels = document.querySelectorAll('.tour-panel');

tourTabs.forEach(tab => {
  tab.addEventListener('click', () => {
    const targetId = tab.dataset.tab;

    // Update tabs
    tourTabs.forEach(t => {
      t.classList.remove('active');
      t.setAttribute('aria-selected', 'false');
    });
    tab.classList.add('active');
    tab.setAttribute('aria-selected', 'true');

    // Update panels
    tourPanels.forEach(p => p.classList.remove('active'));
    const targetPanel = document.getElementById(targetId);
    if (targetPanel) targetPanel.classList.add('active');
  });
});
```

### Design Notes
- **Tab label style**: Short, scannable labels (1–2 words). Use title case.
- **Active indicator**: Colored underline that slides to the active tab creates a polished feel.
- **Mobile**: Tabs become horizontally scrollable. Consider switching to an accordion on very small screens.
- **Screenshot dominance**: The screenshot panel should be ~60% of the width. The text side is concise.
- **Auto-advance** (optional): Auto-rotate through tabs every 5 seconds, pausing on hover or click. Adds dynamism but can frustrate users who are reading — disabled by default.

---

## Sticky Scroll Walkthrough

Text stays pinned while visuals (screenshots) cycle on scroll. Creates a cinematic, immersive tour experience. Used by Apple product pages, Linear, and Notion.

### When to Use
- 3–5 features that tell a sequential story
- Each feature has a visually distinct screenshot
- You want a premium, editorial feel
- Desktop-focused audiences (this pattern degrades on mobile)

### Structure

```
┌─────────────────────────────────────────────────┐
│                                                 │
│  ┌──────────────┐  ┌──────────────────────────┐ │
│  │              │  │                          │ │
│  │  Feature 1   │  │                          │ │
│  │  headline    │  │     [Screenshot 1]       │ │
│  │  + desc      │  │     (fades to 2, 3...)   │ │
│  │              │  │                          │ │
│  │  Feature 2   │  │                          │ │
│  │  headline    │  │                          │ │
│  │  + desc      │  │                          │ │
│  │  (dimmed)    │  │                          │ │
│  │              │  │                          │ │
│  │  Feature 3   │  │                          │ │
│  │  (dimmed)    │  │                          │ │
│  │              │  │                          │ │
│  └──────────────┘  └──────────────────────────┘ │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Implementation

```html
<section class="scroll-walkthrough">
  <div class="walkthrough-container">
    <div class="walkthrough-text">
      <div class="walkthrough-step active" data-step="1">
        <span class="step-label">STEP 01</span>
        <h3>Create your workspace</h3>
        <p>Set up your environment in minutes with guided configuration.</p>
      </div>
      <div class="walkthrough-step" data-step="2">
        <span class="step-label">STEP 02</span>
        <h3>Import your data</h3>
        <p>Bring everything from your existing tools with one-click migration.</p>
      </div>
      <div class="walkthrough-step" data-step="3">
        <span class="step-label">STEP 03</span>
        <h3>Invite your team</h3>
        <p>Role-based access and instant collaboration from day one.</p>
      </div>
    </div>
    <div class="walkthrough-visual">
      <div class="visual-frame">
        <img class="walkthrough-img active" data-step="1" src="./screenshots/step-1.png" alt="" />
        <img class="walkthrough-img" data-step="2" src="./screenshots/step-2.png" alt="" />
        <img class="walkthrough-img" data-step="3" src="./screenshots/step-3.png" alt="" />
      </div>
    </div>
  </div>
</section>
```

```css
.walkthrough-container {
  display: grid;
  grid-template-columns: 1fr 1.5fr;
  gap: 80px;
  min-height: 100vh;
  align-items: start;
}
.walkthrough-text {
  position: sticky;
  top: 30vh;
  display: flex;
  flex-direction: column;
  gap: 60px;
}
.walkthrough-step {
  opacity: 0.3;
  transition: opacity 0.4s ease;
}
.walkthrough-step.active {
  opacity: 1;
}
.walkthrough-visual {
  position: sticky;
  top: 20vh;
}
.visual-frame {
  position: relative;
}
.walkthrough-img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  opacity: 0;
  transition: opacity 0.5s ease;
}
.walkthrough-img.active {
  opacity: 1;
  position: relative;
}
```

```js
// Scroll-linked step activation
const steps = document.querySelectorAll('.walkthrough-step');
const imgs = document.querySelectorAll('.walkthrough-img');

const stepObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const stepNum = entry.target.dataset.step;
      steps.forEach(s => s.classList.toggle('active', s.dataset.step === stepNum));
      imgs.forEach(i => i.classList.toggle('active', i.dataset.step === stepNum));
    }
  });
}, { rootMargin: '-30% 0px -30% 0px' });

steps.forEach(step => stepObserver.observe(step));
```

### Mobile Fallback
On screens below 768px, collapse to a standard vertical scroll with each step as a full section (text above, screenshot below). The sticky positioning doesn't work well on mobile.

---

## Guided Feature Discovery

A numbered, card-based walkthrough pattern. Shows a clear path through the product. Used by many onboarding/how-it-works sections.

### When to Use
- Explaining a sequential workflow (sign up → configure → launch)
- 3–5 ordered steps
- The process itself is a selling point (simplicity, speed)

### Structure

```
┌─────────────────────────────────────────────────┐
│  HOW IT WORKS                                   │
│                                                 │
│  Section Headline                               │
│  Brief context                                  │
│                                                 │
│  ┌─────┐    ┌─────┐    ┌─────┐    ┌─────┐     │
│  │  1  │───▶│  2  │───▶│  3  │───▶│  4  │     │
│  │     │    │     │    │     │    │     │     │
│  │Title│    │Title│    │Title│    │Title│     │
│  │Desc │    │Desc │    │Desc │    │Desc │     │
│  └─────┘    └─────┘    └─────┘    └─────┘     │
│                                                 │
│  [Primary CTA]                                  │
└─────────────────────────────────────────────────┘
```

### Implementation

```html
<section class="how-it-works">
  <span class="section-label">HOW IT WORKS</span>
  <h2>From sign-up to first [outcome] in minutes</h2>
  <p>A clear path — no implementation project required.</p>

  <div class="steps-grid">
    <div class="step-card animate-on-scroll">
      <div class="step-number">1</div>
      <h3>Create your account</h3>
      <p>Sign up, name your workspace, and set your preferences in under two minutes.</p>
    </div>
    <div class="step-connector"></div>
    <div class="step-card animate-on-scroll">
      <div class="step-number">2</div>
      <h3>Configure your services</h3>
      <p>Define your offerings, pricing, and availability with guided setup.</p>
    </div>
    <div class="step-connector"></div>
    <div class="step-card animate-on-scroll">
      <div class="step-number">3</div>
      <h3>Invite your team</h3>
      <p>Add team members with role-based access and personalized profiles.</p>
    </div>
    <div class="step-connector"></div>
    <div class="step-card animate-on-scroll">
      <div class="step-number">4</div>
      <h3>Go live</h3>
      <p>Launch your branded portal and start accepting clients immediately.</p>
    </div>
  </div>
</section>
```

```css
.steps-grid {
  display: flex;
  align-items: flex-start;
  gap: 0;
  margin-top: 60px;
}
.step-card {
  flex: 1;
  text-align: center;
  padding: 0 24px;
}
.step-number {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: var(--brand-primary);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 20px;
  margin: 0 auto 20px;
}
.step-connector {
  width: 60px;
  height: 2px;
  background: var(--border-light);
  margin-top: 24px;
  flex-shrink: 0;
}

/* Mobile: vertical layout */
@media (max-width: 768px) {
  .steps-grid {
    flex-direction: column;
    gap: 32px;
  }
  .step-card { text-align: left; padding: 0; }
  .step-connector {
    width: 2px;
    height: 32px;
    margin-left: 24px;
  }
}
```

---

## Interactive Before/After

Shows transformation — the state before the product and after. Extremely effective for tools that replace manual processes.

### When to Use
- The product replaces a painful manual process
- There's a clear visual "before" (spreadsheets, chaos) and "after" (the product UI)
- You want to create an emotional contrast

### Structure

```html
<section class="before-after">
  <h2>Replace [pain] with [solution]</h2>
  <div class="comparison">
    <div class="before">
      <span class="label">Before</span>
      <img src="./screenshots/before-state.png" alt="Before: manual spreadsheet tracking" />
      <ul class="pain-points">
        <li>Manual data entry across 4 tools</li>
        <li>No visibility into team capacity</li>
        <li>Client details lost in email threads</li>
      </ul>
    </div>
    <div class="divider">
      <span class="arrow">→</span>
    </div>
    <div class="after">
      <span class="label">After</span>
      <img src="./screenshots/after-state.png" alt="After: unified dashboard" />
      <ul class="benefits">
        <li>One dashboard for everything</li>
        <li>Real-time capacity and utilization</li>
        <li>Complete client history at a glance</li>
      </ul>
    </div>
  </div>
</section>
```

---

## Audience-Segmented Tour

Different visitors need different features highlighted. This pattern lets users self-select their segment for a personalized tour. Used by products serving multiple personas.

### When to Use
- Product serves distinct personas (solo users, teams, enterprise)
- Features matter differently to different audiences
- You want visitors to self-identify early

### Structure

```
┌─────────────────────────────────────────────────┐
│  WHO IT'S FOR                                   │
│                                                 │
│  Section Headline                               │
│                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │ Persona1 │  │ Persona2 │  │ Persona3 │     │
│  │          │  │          │  │          │     │
│  │ Label    │  │ Label    │  │ Label    │     │
│  │ Subtitle │  │ Subtitle │  │ Subtitle │     │
│  │          │  │          │  │          │     │
│  │ • Feat 1 │  │ • Feat 1 │  │ • Feat 1 │     │
│  │ • Feat 2 │  │ • Feat 2 │  │ • Feat 2 │     │
│  │ • Feat 3 │  │ • Feat 3 │  │ • Feat 3 │     │
│  │          │  │          │  │          │     │
│  │ [CTA →]  │  │ [CTA →]  │  │ [CTA →]  │     │
│  └──────────┘  └──────────┘  └──────────┘     │
└─────────────────────────────────────────────────┘
```

### Implementation

```html
<section class="audience-tiers">
  <span class="section-label">FOR EVERY STAGE</span>
  <h2>Whether you're solo or scaling a team</h2>
  <p>Adapts to your stage and grows with you.</p>

  <div class="tier-grid">
    <div class="tier-card animate-on-scroll">
      <span class="tier-badge">INDIVIDUALS</span>
      <h3>Solo Practitioner</h3>
      <p>Launch your professional presence and stop juggling tools.</p>
      <ul>
        <li>Branded site</li>
        <li>Client pipeline</li>
        <li>Self-serve scheduling</li>
      </ul>
      <a href="#" class="tier-cta">Learn more →</a>
    </div>
    <!-- ... more tiers -->
  </div>
</section>
```

```css
.tier-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 32px;
  margin-top: 60px;
}
.tier-card {
  background: var(--surface);
  border: 1px solid var(--border-light);
  border-radius: 16px;
  padding: 40px 32px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.tier-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08);
}
.tier-badge {
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: var(--brand-primary);
}

@media (max-width: 768px) {
  .tier-grid { grid-template-columns: 1fr; }
}
```

---

## Combining Tour Patterns

The most effective product pages combine multiple tour patterns in a deliberate sequence:

```
Hero
  ↓
Tabbed Platform Tour        ← overview: what can it do?
  ↓
Feature Deep-Dives          ← alternating blocks: 2–3 most compelling features
  ↓
Stats Bar                   ← credibility: quantified proof
  ↓
How It Works (Steps)        ← friction reduction: is this hard?
  ↓
Audience Tiers              ← self-identification: is this for me?
  ↓
Social Proof                ← validation: who else trusts this?
  ↓
Final CTA                   ← conversion: what do I do next?
```

**Pattern selection rules:**
- Use **Tabbed Platform Tour** when features ≥ 5 (prevents scroll fatigue)
- Use **Sticky Scroll** when you want a premium, immersive feel for 3–5 sequential features
- Use **Guided Feature Discovery** for the "How It Works" section
- Use **Audience Tiers** when the product serves 2–4 distinct personas
- Use **Before/After** when the product replaces a painful status quo

**Never use more than 2 interactive patterns on one page** (e.g., tabbed tour + sticky scroll). Too many competing interaction models confuse visitors. Pick one primary interactive pattern and keep the rest as standard scroll sections.
