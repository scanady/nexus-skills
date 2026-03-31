---
name: marketing-content-product-overview-page
description: 'Builds polished product overview pages with automated screenshot capture, scroll-triggered animations, and modern SaaS design patterns. Use when asked to create a product page, feature page, product overview, landing page with screenshots, product showcase, or feature tour. Automatically captures screenshots from live URLs or local apps using browser automation, then assembles them into production-grade HTML pages inspired by Stripe, Linear, Notion, and Bestow-style product marketing pages.'
---

# Product Overview Page Builder

Builds high-fidelity product overview pages — the kind of feature-rich marketing pages used by Stripe (/payments), Bestow (/administration), Linear, Notion, and other top SaaS companies to showcase product capabilities with real screenshots, animations, and social proof.

**Core capability: Automated screen capture.** This skill uses browser automation to navigate a live product (URL or local dev server), capture targeted screenshots of key features and UI states, then assembles those captures into a polished overview page.

## Prerequisites

- Browser automation tools (Playwright, Puppeteer, or equivalent)
- A live URL or local dev server for the product to screenshot
- If no live product exists, the skill falls back to generating HTML/CSS UI mockups

## Execution Logic

**Check $ARGUMENTS first to determine execution mode:**

### If $ARGUMENTS is empty or not provided:
Respond with:
"marketing-content-product-overview-page loaded — give me a URL to your product and describe the features you want to showcase"

Then wait for the user to provide their product details in the next message.

### If $ARGUMENTS contains content:
Proceed immediately to Task Execution.

---

## Task Execution

### 1. MANDATORY: Read Reference Files FIRST
**BLOCKING REQUIREMENT — DO NOT SKIP THIS STEP**

Before doing ANYTHING else, use the Read tool to read:
- `./references/page-patterns.md`
- `./references/screenshot-capture.md`

**DO NOT PROCEED** to Step 2 until you have read both files and have their content in context.

### 2. Gather Product Context

From the user's input, extract:
- **Product URL** — live URL or local address (e.g., `http://localhost:3000`). This is the primary input.
- **Product name** and tagline
- **Target audience** (developers, business users, consumers, etc.)
- **Features to capture** — list of features/screens/views to screenshot (aim for 3–7)
- **Screenshot instructions** — specific pages, UI states, workflows to capture (e.g., "the dashboard after login", "the settings page with the billing tab active", "the onboarding wizard step 3")
- **Tone** — technical/developer-focused, enterprise, consumer-friendly, playful
- **Social proof** — customer logos, testimonials, stats/metrics
- **CTA** — primary call-to-action (sign up, contact sales, try demo, etc.)
- **Brand colors / fonts** — if provided; otherwise extract from the live product during capture

For any missing information, apply defaults from **Defaults & Assumptions**.

If the user hasn't provided a URL, ask for one. If no URL is available, fall back to HTML/CSS mockup generation.

### 3. Create Output Directory

All output goes into a structured directory:

```bash
mkdir -p ./output/<product-name>/screenshots
```

Final structure:
```
./output/<product-name>/
├── screenshots/
│   ├── hero.png
│   ├── feature-1-<name>.png
│   ├── feature-2-<name>.png
│   ├── feature-3-<name>.png
│   └── ... (one per feature)
├── <product-name>-overview.html
└── capture-manifest.md  (log of what was captured)
```

### 4. Capture Screenshots

**This is the core step.** Use browser automation tools to capture real product screenshots.

Follow the detailed capture workflow in `./references/screenshot-capture.md`. Summary:

#### 4a. Launch browser and set viewport
- Open a browser instance
- Set viewport to **1440×900** for desktop captures (the standard marketing screenshot size)
- Navigate to the product URL
- Wait for the page to fully load (network idle, animations settled)

#### 4b. Capture the hero screenshot
- This is the first thing visitors see — make it count
- Capture the full above-the-fold view at 1440×900
- Save as `screenshots/hero.png`
- If the product has a particularly impressive dashboard or main view, navigate there first

#### 4c. Capture each feature
For each feature the user wants to showcase:
1. **Navigate** to the relevant page/section
2. **Set up the state** — click tabs, expand menus, fill in demo data, trigger the UI state that best shows the feature
3. **Wait** for transitions/animations to complete
4. **Scroll** to the target area if needed
5. **Capture** — either full viewport or a specific element:
   - Full viewport for dashboard/overview shots
   - Element-level capture for specific components (forms, cards, panels)
6. **Save** as `screenshots/feature-N-<descriptive-name>.png`

#### 4d. Capture interaction states (optional but high-impact)
- **Hover states**: Hover over key interactive elements and capture
- **Modal/dialog states**: Trigger modals and capture
- **Before/after**: Capture a sequence showing a workflow (e.g., empty state → filled state)
- **Dark mode**: If the product supports it, capture a dark mode variant

#### 4e. Capture mobile views (optional)
- Resize viewport to 375×812 (iPhone)
- Navigate to key screens
- Capture for use in phone-frame mockups
- Save as `screenshots/mobile-<name>.png`

#### 4f. Extract brand assets during capture
While the browser is open on the product:
- Note the primary brand colors visible in the UI (for the overview page palette)
- Note the font families used (inspect if possible)
- Capture any logo visible in the nav bar

#### 4g. Write capture manifest
Create `capture-manifest.md` logging what was captured:
```markdown
# Screenshot Capture Manifest
- **URL**: https://...
- **Viewport**: 1440x900
- **Date**: YYYY-MM-DD

## Captures
| File | Description | Page/URL | Viewport | Notes |
|------|-------------|----------|----------|-------|
| hero.png | Main dashboard | /dashboard | 1440x900 | After login |
| feature-1-billing.png | Billing settings | /settings/billing | 1440x900 | Monthly tab active |
```

### 5. Choose Page Architecture

Select a page structure based on the product type and number of features. Refer to the **Page Archetypes** in `./references/page-patterns.md` and pick the best fit:

| Product Type | Recommended Archetype |
|---|---|
| Developer tool / API platform | **Stripe-style**: Hero → feature blocks with alternating screenshots → tabbed product deep-dives → metrics → logo bar → pricing → CTA |
| B2B SaaS / enterprise | **Bestow-style**: Hero with value props → tabbed section groups → feature cards with screenshots → case study CTA → related products → contact CTA |
| Consumer product | **Showcase-style**: Full-bleed hero with product shot → feature scroll with parallax screenshots → social proof → download/signup CTA |
| Multi-product platform | **Hub-style**: Hero → product grid cards → expandable feature sections per product → comparison table → CTA |

### 6. Design the Page

Apply these design principles — every page must feel intentionally designed, not templated:

**Typography**: Pick a distinctive display font + clean body font. Never use Inter, Roboto, or Arial. Use Google Fonts or system fonts with character. Pair weights deliberately — heavy headlines, light body. If brand fonts were extracted during capture, use those.

**Color**: If brand colors were captured from the live product, use them as the foundation. Otherwise, commit to a bold palette. One dominant brand color, one accent, generous use of neutrals. Dark sections for contrast.

**Screenshots**: These are real captures now — they are the centerpiece:
- Frame in device mockups (browser chrome, phone frames) or floating with subtle shadows
- Slightly rotated or perspective-transformed where appropriate
- Annotated with callout labels or highlight overlays pointing to key UI elements
- Reference images using relative paths: `./screenshots/hero.png`

**Layout**: Use the alternating pattern — text-left/image-right, then text-right/image-left. Break the grid occasionally with full-width sections, overlapping elements, or asymmetric compositions.

**Spacing**: Generous vertical rhythm between sections (120–200px). Tight internal spacing within cards.

### 7. Implement Animations

Product overview pages come alive with motion. Implement these animation layers:

**Scroll-triggered reveals** (most important):
- Fade-up elements as they enter the viewport using `IntersectionObserver`
- Stagger child elements within sections (50–100ms delay between items)
- Screenshots slide in from the side they're positioned on

**Hero animations**:
- Headline text fades in first, subheadline follows, CTA buttons last
- Hero screenshot scales up slightly or fades in with a delay

**Hover micro-interactions**:
- Feature cards lift with subtle shadow on hover
- CTA buttons have smooth color/scale transitions
- Screenshot frames respond to hover with slight scale or glow

**Optional advanced animations** (use when the design calls for it):
- Parallax scrolling on background elements or screenshots
- Animated stat counters that count up when scrolled into view
- Tab transitions with crossfade or slide effects
- Floating/breathing animation on decorative elements
- CSS-only animated gradients or grain overlays for backgrounds

All animations must use CSS transforms and opacity for GPU acceleration. Use `prefers-reduced-motion` media query to disable animations for accessibility.

### 8. Build the Page

Generate the HTML file at `./output/<product-name>/<product-name>-overview.html`.

The page references screenshots via relative paths (`./screenshots/hero.png`), so the HTML and screenshots directory must stay together.

**Structure the HTML semantically:**
```
<header>  — Nav bar with logo + links + CTA button
<section> — Hero: headline, subheadline, CTA buttons, hero screenshot
<section> — Feature highlights (3–5 alternating text/screenshot blocks)
<section> — Tabbed or segmented deep-dive (if applicable)
<section> — Stats/metrics bar
<section> — Social proof: testimonials + customer logos
<section> — Pricing or comparison (if applicable)
<footer>  — Final CTA + footer links
```

**CSS requirements:**
- CSS custom properties for all colors, fonts, spacing
- Responsive design: desktop-first with tablet and mobile breakpoints
- Smooth scroll behavior
- Clean transitions on all interactive elements

**JS requirements:**
- Intersection Observer for scroll-triggered animations
- Tab switching logic (if tabbed sections exist)
- Animated counters (if stats section exists)
- No external JS dependencies — vanilla JS only

**Image references:**
- All `<img>` tags use relative paths: `src="./screenshots/feature-1-billing.png"`
- Every image has a descriptive `alt` attribute
- Images are wrapped in device frames built with CSS
- Consider `loading="lazy"` for below-the-fold images

### 9. Verify and Deliver

Before presenting the output:
- Open the HTML file in a browser to verify rendering
- Confirm all screenshot images load correctly
- Check responsive behavior at mobile (375px), tablet (768px), and desktop (1280px+)
- Verify all animations fire correctly on scroll
- Confirm all interactive elements (tabs, hovers, CTAs) work

Tell the user:
- Output directory path with contents
- How many screenshots were captured
- How to preview (open HTML in browser)
- Brief summary of sections included

---

## Writing Rules

### Core Rules
- Every section must serve a purpose — no filler content
- Headlines are benefit-driven, not feature-driven ("Convert more customers" not "Payment processing")
- Subheadlines add specificity with concrete details or numbers
- CTA text is action-oriented and specific ("Start free trial" not "Learn more")
- Real screenshots are the primary visual element — they carry the page

### Design Rules
- Never center everything — use left-aligned text with right-aligned images (and alternate)
- Maximum 7 feature sections before it feels like a wall — group into tabs if more
- Stats should use real-looking numbers with context ("11.9% average revenue uplift")
- Testimonials need attribution (name, title, company, logo)
- Color contrast must meet WCAG AA minimum (4.5:1 for body text)

### Screenshot Rules
- Capture at 1440×900 for desktop, 375×812 for mobile
- Wait for full page load before capturing (no spinners, no half-rendered states)
- Set up realistic demo states — populated data, active tabs, expanded views
- Descriptive filenames: `feature-2-billing-dashboard.png` not `screenshot3.png`
- Log every capture in the manifest

### Animation Rules
- All animations must feel subtle and purposeful — no bouncing, no spinning
- Scroll reveals use `ease-out` timing, 400–600ms duration
- Stagger delays between 50–150ms — never more than 150ms
- Hero load animation completes within 1 second
- Honor `prefers-reduced-motion` — disable all motion

### Code Rules
- HTML file + screenshots directory, no other external dependencies (fonts from Google Fonts CDN is acceptable)
- CSS custom properties for theming
- Semantic HTML5 elements
- `alt` attributes on all images
- Mobile-responsive with proper viewport meta tag

---

## Output Format

Structured output directory:

```
./output/<product-name>/
├── screenshots/
│   ├── hero.png
│   ├── feature-1-<name>.png
│   ├── feature-2-<name>.png
│   └── ...
├── <product-name>-overview.html
└── capture-manifest.md
```

The HTML references screenshots via relative paths and opens directly in any browser when the directory structure is preserved.

**Example:** `./output/acme-payments/acme-payments-overview.html`

---

## References

**These files MUST be read using the Read tool before task execution (see Step 1):**

| File | Purpose |
|------|---------|
| `./references/page-patterns.md` | Page archetypes, section blueprints, animation recipes, and screenshot framing techniques drawn from Stripe, Bestow, Linear, and other top product pages |
| `./references/screenshot-capture.md` | Detailed browser automation workflows for capturing product screenshots — viewport setup, navigation patterns, element targeting, state management, and image optimization |

**Why these matter:** The page-patterns file provides battle-tested structural patterns that prevent the output from looking like a generic template. The screenshot-capture file ensures captures are high-quality, properly framed, and show the product in its best light.

---

## Quality Checklist (Self-Verification)

### Pre-Execution Check
- [ ] I read `./references/page-patterns.md` before starting
- [ ] I read `./references/screenshot-capture.md` before starting
- [ ] I have both reference files in context

### Screenshot Capture Check
- [ ] Output directory and screenshots/ folder created
- [ ] Hero screenshot captured at 1440×900
- [ ] Each feature has a dedicated screenshot
- [ ] Screenshots show realistic, populated UI states (not empty/loading)
- [ ] capture-manifest.md documents all captures
- [ ] No screenshots of error states, spinners, or blank screens

### Design Check
- [ ] Typography is distinctive — no Inter, Roboto, or Arial (unless it's the product's actual font)
- [ ] Color palette is cohesive — derived from product brand if possible
- [ ] Screenshots are framed and presented as the hero visual elements
- [ ] Layout alternates and breaks the grid where appropriate
- [ ] No centered-everything syndrome

### Animation Check
- [ ] Scroll-triggered reveals work on all sections
- [ ] Hero has a load-in animation sequence
- [ ] Hover states exist on interactive elements
- [ ] `prefers-reduced-motion` is respected
- [ ] No janky or over-the-top motion

### Code Check
- [ ] HTML file + screenshots directory structure is correct
- [ ] All image paths resolve correctly (relative paths)
- [ ] Responsive at 375px, 768px, 1280px+
- [ ] Semantic HTML with proper heading hierarchy
- [ ] CSS custom properties used for theming
- [ ] All images have alt text
- [ ] Vanilla JS, no external dependencies

### Content Check
- [ ] Headlines are benefit-driven
- [ ] Every section has a clear purpose
- [ ] Social proof feels authentic
- [ ] CTAs are specific and action-oriented
- [ ] Stats include context, not just numbers

**If ANY check fails → revise before presenting.**

---

## Defaults & Assumptions

- **Tech stack**: HTML file with inline CSS/JS + screenshot image files (unless user requests React, in which case use the web-artifacts-builder skill for scaffolding)
- **Output location**: `./output/<product-name>/` with `screenshots/` subdirectory
- **Capture viewport**: 1440×900 desktop, 375×812 mobile
- **Sections**: Hero → 3–5 feature blocks → stats bar → testimonials → CTA footer
- **Animation level**: Medium (scroll reveals + hero animation + hover states). Dial up for "impressive" requests, dial down for "clean/minimal" requests
- **Screenshots**: Captured from live URL. If no URL is available, fall back to generating realistic UI mockups with HTML/CSS
- **Font pairing**: Extract from product if possible. Otherwise, one display font from Google Fonts + one body font with personality matching the product tone
- **Color scheme**: Extract from product brand. Otherwise, choose a distinctive palette that matches the product's domain
- **Responsive**: Desktop-first, works down to 375px mobile
- **Content tone**: Professional but not stuffy. Concrete, not vague. Benefits over features
