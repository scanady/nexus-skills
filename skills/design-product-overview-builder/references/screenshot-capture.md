# Screenshot Capture Workflows

Detailed browser automation workflows for capturing high-quality product screenshots. These techniques produce marketing-grade captures that show the product in its best light.

---

## Capture Strategy

Before opening a browser, plan the capture session:

1. **List target screens** — Map each feature to a specific URL/route and UI state
2. **Determine capture order** — Group by navigation path to minimize back-and-forth
3. **Identify state requirements** — What needs to be clicked, expanded, or filled before capture
4. **Choose capture scope** — Full viewport vs. element-specific for each shot

### Capture Planning Template

```markdown
| # | Feature | URL/Route | State Setup | Capture Scope | Filename |
|---|---------|-----------|-------------|---------------|----------|
| H | Hero/main view | /dashboard | Logged in, data populated | Full viewport | hero.png |
| 1 | Billing | /settings/billing | Monthly tab active | Full viewport | feature-1-billing.png |
| 2 | Analytics | /analytics | Date range: last 30 days | Element: .analytics-panel | feature-2-analytics.png |
| 3 | Team management | /team | Invite modal open | Full viewport | feature-3-team-invite.png |
```

---

## Browser Setup

### Viewport Configuration

Use these standard viewports for marketing screenshots:

| Context | Width × Height | Use When |
|---------|---------------|----------|
| **Desktop (primary)** | 1440 × 900 | Default for all feature captures |
| **Desktop wide** | 1920 × 1080 | Full-width dashboard/data views |
| **Tablet** | 768 × 1024 | Showing responsive design |
| **Mobile** | 375 × 812 | Phone-frame screenshots |

### Browser Configuration

When launching the browser:
- **Disable cookie banners**: These ruin screenshots. Dismiss or block them before capturing.
- **Set language/locale** to match target audience (usually en-US)
- **Disable browser extensions** that might inject UI
- **Set a consistent device scale factor** (1x for standard, 2x for retina-quality captures)
- **Use light color scheme** by default (unless the product is dark-themed)

### Handling Authentication

If the product requires login:
1. Navigate to the login page
2. Fill credentials (use demo/test accounts provided by the user)
3. Submit and wait for redirect to complete
4. Verify you're on the authenticated page before proceeding

If no credentials are available, capture only public-facing pages.

---

## Capture Techniques

### Full Viewport Capture

The most common capture type. Gets everything visible in the browser window.

**When to use:** Dashboard overviews, landing pages, feature pages that fit in one screen.

**Workflow:**
1. Navigate to the target URL
2. Wait for full page load (network idle)
3. Dismiss any modals, tooltips, or onboarding overlays that obstruct the view
4. Wait an additional 500ms for animations to settle
5. Take a screenshot at the configured viewport size

### Element-Specific Capture

Captures a single component, panel, or section of the page.

**When to use:** Specific UI components (a settings panel, a data table, a chart), when the surrounding page chrome would dilute the focus.

**Workflow:**
1. Navigate to the page containing the target element
2. Set up the required state (expand sections, select tabs, etc.)
3. Scroll the target element into view if needed
4. Identify the element by CSS selector, test ID, or visible text
5. Capture just that element — the output will be cropped to the element's bounding box

**Choosing selectors (priority order):**
1. `data-testid` or `data-cy` attributes (most stable)
2. Semantic selectors: `main`, `[role="dialog"]`, `nav`
3. Class selectors with meaningful names: `.billing-panel`, `.analytics-chart`
4. Avoid: fragile auto-generated class names, deep nesting, index-based selectors

### Full-Page Scroll Capture

Captures the entire scrollable page as one tall image.

**When to use:** Long-form pages, documentation, product pages with many sections.

**Workflow:**
1. Navigate to the page
2. Scroll to trigger any lazy-loaded content
3. Return to the top
4. Take a full-page screenshot (browser tools typically support this natively)

**Caution:** Full-page captures are usually too tall for marketing use. Prefer cropping to the most impactful section, or capture specific sections individually.

---

## State Management

### Preparing UI States Before Capture

The difference between a mediocre screenshot and a great one is the UI state. Never capture a default/empty state when a populated/active state is available.

**Common state preparations:**

| State | How to Achieve | Why |
|-------|---------------|-----|
| **Populated data** | Fill forms, add sample entries, import test data | Empty states look broken |
| **Active tab** | Click the target tab and wait for panel to render | Shows the feature you're highlighting |
| **Expanded sections** | Click accordions, toggle visibility | Reveals hidden functionality |
| **Hover/focus** | Hover over key elements | Shows interactive affordances |
| **Selected items** | Click to select rows, cards, checkboxes | Shows bulk actions, selection UI |
| **Notifications** | Trigger toast/notification display | Shows feedback mechanisms |
| **Modal/dialog** | Click trigger button and wait for modal | Shows secondary workflows |
| **Dark mode** | Toggle theme if available | Additional visual variant |

### Timing and Waits

Screenshots captured too early show loading states. Too late shows idle states that might have expired.

**Wait strategy:**
1. After navigation: wait for network idle (no pending requests for 500ms)
2. After clicking: wait for transition/animation to complete (300–500ms)
3. After scrolling: wait briefly (200ms) for lazy content
4. Before capture: final 300ms settle period

**Watch for and handle:**
- Loading spinners / skeleton screens — wait until real content appears
- Progressive image loading — wait until images are fully rendered
- Animated charts — wait until animation completes
- Toast notifications — capture during display window (they auto-dismiss)

---

## Capture for Specific Page Sections

### Hero / Above-the-Fold
- Navigate to the product's most visually impressive page (usually the main dashboard or home screen)
- Ensure the most important UI elements are visible without scrolling
- If the product has a command palette or spotlight search, consider showing it active
- This screenshot carries the most weight — spend extra time getting the state right

### Feature Showcase
- Navigate to the feature's dedicated page or view
- Activate the specific sub-feature (click the right tab, select the right option)
- Populate with realistic-looking data (names, numbers, dates — not "Lorem ipsum" or "Test 123")
- Capture with enough context to understand the feature but not so much that it's noisy

### Workflow Sequences
For features best shown as a process (e.g., onboarding wizard, checkout flow):
- Capture each step in sequence
- Name files with step numbers: `feature-3-onboarding-step1.png`, `feature-3-onboarding-step2.png`
- Consider creating an animated GIF or noting these should be presented as a sequence in the overview page

### Mobile Captures
- Resize viewport to 375×812 before navigating
- Some sites redirect to different routes for mobile — verify you're on the right page
- Capture navigation states (hamburger menu open) as well as content states
- These work best inside phone-frame CSS mockups in the final page

---

## Post-Capture Processing

### Image Quality
- Save as PNG for UI screenshots (sharp text, no compression artifacts)
- Use 2x device pixel ratio captures if file size is acceptable (crisper on retina displays)
- If file sizes are too large (>2MB per image), consider converting to WebP or optimizing PNG compression

### Naming Convention
```
hero.png                          — The main product shot
feature-1-<descriptive-name>.png  — Feature screenshots (numbered)
feature-2-<descriptive-name>.png
mobile-<descriptive-name>.png     — Mobile viewport captures
detail-<descriptive-name>.png     — Zoomed-in element captures
state-<descriptive-name>.png      — Special UI states (hover, modal, dark mode)
```

Use lowercase, hyphens for spaces. Names should describe what's shown, not where it is:
- Good: `feature-1-billing-dashboard.png`
- Bad: `screenshot-3.png`, `page2.png`

### Capture Manifest

Always create `capture-manifest.md` documenting what was captured. This serves as both a record and a reference when building the HTML page:

```markdown
# Screenshot Capture Manifest

**Product**: [Name]
**URL**: [Base URL]
**Date**: [YYYY-MM-DD]
**Viewport**: 1440×900 (desktop), 375×812 (mobile)
**Brand colors observed**: primary #XXXXXX, accent #XXXXXX, bg #XXXXXX
**Fonts observed**: [Display font], [Body font]

## Captures

| File | Description | Route | Setup Steps | Notes |
|------|-------------|-------|-------------|-------|
| hero.png | Dashboard overview | /dashboard | Login → wait for data load | Shows all key metrics |
| feature-1-billing.png | Billing management | /billing | Click "Monthly" tab | Shows invoice list |
| feature-2-analytics.png | Analytics dashboard | /analytics | Set range to "Last 30 days" | Charts fully rendered |
| feature-3-team.png | Team management | /team | Click "Invite member" | Modal visible |
| mobile-dashboard.png | Mobile dashboard | /dashboard | Viewport 375×812 | Responsive layout |
```

---

## Troubleshooting Common Issues

| Issue | Solution |
|-------|---------|
| Cookie consent banner blocks content | Dismiss the banner programmatically before capture; click "Accept" or find the dismiss button |
| Login wall | Use provided credentials or capture only public pages |
| Content behind feature flags | Ask user to provide a URL/account where features are enabled |
| Lazy-loaded images not appearing | Scroll through the page once to trigger loads, then scroll back and capture |
| Animated elements in mid-state | Add extra wait time (1–2s) or wait for specific CSS classes that indicate completion |
| Dark mode active but light mode wanted | Check for theme toggle and set explicitly before capture |
| Different content in different locales | Set browser locale to en-US explicitly |
| Chat widget / support bubble overlay | Look for and dismiss or hide third-party widgets before capture |
| Responsive layout not triggering | Set viewport size BEFORE navigation, not after |
