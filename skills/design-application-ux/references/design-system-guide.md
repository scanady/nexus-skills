# Design System Guide for Application UX

This reference covers design token structures, component patterns, and implementation standards for application interfaces. Read this file when implementing screens or building component libraries.

## Table of Contents

1. Design Token Architecture
2. Color System
3. Typography Scale
4. Spacing and Layout
5. Elevation and Shadows
6. Component API Patterns
7. Responsive Strategy
8. Accessibility Standards
9. Dark Mode Implementation
10. Platform-Specific Patterns

## 1. Design Token Architecture

Use CSS custom properties organized in three layers:

**Primitive tokens** (raw values, never used directly in components):
```css
:root {
  --blue-50: #eff6ff;
  --blue-100: #dbeafe;
  --blue-500: #3b82f6;
  --blue-600: #2563eb;
  --blue-900: #1e3a5f;
  --gray-0: #ffffff;
  --gray-50: #f9fafb;
  --gray-100: #f3f4f6;
  --gray-200: #e5e7eb;
  --gray-300: #d1d5db;
  --gray-400: #9ca3af;
  --gray-500: #6b7280;
  --gray-600: #4b5563;
  --gray-700: #374151;
  --gray-800: #1f2937;
  --gray-900: #111827;
  --gray-950: #030712;
}
```

**Semantic tokens** (purpose-driven, reference primitives):
```css
:root {
  /* Actions */
  --color-action-primary: var(--blue-600);
  --color-action-primary-hover: var(--blue-700);
  --color-action-secondary: var(--gray-100);
  --color-action-destructive: var(--red-600);

  /* Surfaces */
  --color-surface-base: var(--gray-0);
  --color-surface-raised: var(--gray-0);
  --color-surface-sunken: var(--gray-50);
  --color-surface-overlay: var(--gray-0);

  /* Text */
  --color-text-primary: var(--gray-900);
  --color-text-secondary: var(--gray-500);
  --color-text-tertiary: var(--gray-400);
  --color-text-inverse: var(--gray-0);
  --color-text-link: var(--blue-600);

  /* Borders */
  --color-border-default: var(--gray-200);
  --color-border-strong: var(--gray-300);
  --color-border-focus: var(--blue-500);

  /* Status */
  --color-status-success: var(--green-600);
  --color-status-warning: var(--amber-500);
  --color-status-error: var(--red-600);
  --color-status-info: var(--blue-600);
}
```

**Component tokens** (scoped to specific components):
```css
.btn-primary {
  --btn-bg: var(--color-action-primary);
  --btn-bg-hover: var(--color-action-primary-hover);
  --btn-text: var(--color-text-inverse);
  --btn-radius: var(--radius-md);
  --btn-padding: var(--space-2) var(--space-4);
}
```

## 2. Color System

Build palettes with 10 steps (50-950) for each hue. At minimum, define these hue families:

- **Primary**: Brand color, used for primary actions and key UI accents
- **Neutral/Gray**: Used for text, borders, surfaces, and backgrounds (the workhorse)
- **Red**: Destructive actions, errors, critical alerts
- **Amber/Yellow**: Warnings, caution states
- **Green**: Success, positive states, confirmations
- **Blue**: Info states, links (can overlap with primary if brand is blue)

**Color usage rules:**
- Backgrounds: gray-0 through gray-100 for light theme
- Primary text: gray-900 (not pure black, which is too harsh)
- Secondary text: gray-500 (ensure 4.5:1 contrast ratio against background)
- Borders: gray-200 for default, gray-300 for hover/emphasis
- Interactive elements: primary-600 for default, primary-700 for hover
- Status colors: always pair with an icon, never rely on color alone

## 3. Typography Scale

**Recommended application type scale (base 16px):**

| Token | Size | Line Height | Weight | Use |
|-------|------|-------------|--------|-----|
| --text-xs | 12px | 16px | 400 | Captions, badges, helper text |
| --text-sm | 13px | 18px | 400 | Secondary content, metadata |
| --text-base | 14px | 20px | 400 | Body text, form inputs, table cells |
| --text-md | 16px | 24px | 400/500 | Emphasized body, card titles |
| --text-lg | 18px | 26px | 500/600 | Section headings |
| --text-xl | 20px | 28px | 600 | Page section titles |
| --text-2xl | 24px | 32px | 600 | Page titles |
| --text-3xl | 30px | 36px | 700 | Dashboard hero metrics |

**Font weight tokens:**
```css
:root {
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;
}
```

For enterprise/data-heavy apps, use 14px as the base body size. For consumer apps, use 16px. Never go below 12px for any readable text.

## 4. Spacing and Layout

**4px base grid with exponential scale:**

```css
:root {
  --space-0: 0px;
  --space-px: 1px;
  --space-0-5: 2px;
  --space-1: 4px;
  --space-1-5: 6px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-10: 40px;
  --space-12: 48px;
  --space-16: 64px;
  --space-20: 80px;
}
```

**Layout dimensions:**

| Element | Compact | Default | Spacious |
|---------|---------|---------|----------|
| Sidebar width | 220px | 256px | 280px |
| Sidebar collapsed | 56px | 64px | 72px |
| Top bar height | 48px | 56px | 64px |
| Content max-width | 1200px | 1440px | Full |
| Card padding | 12px | 16px | 24px |
| Table row height | 36px | 44px | 52px |
| Form field height | 32px | 36px | 40px |
| Button height | 28px | 36px | 40px |

**Border radius scale:**
```css
:root {
  --radius-none: 0px;
  --radius-sm: 4px;
  --radius-md: 6px;
  --radius-lg: 8px;
  --radius-xl: 12px;
  --radius-full: 9999px;
}
```

Use `--radius-md` for most interactive components (buttons, inputs, cards). Use `--radius-sm` for smaller elements (badges, tags). Use `--radius-full` for avatars and circular buttons. Avoid radii larger than 12px in functional application interfaces.

## 5. Elevation and Shadows

**Shadow scale (light theme):**
```css
:root {
  --shadow-xs: 0 1px 2px rgba(0,0,0,0.05);
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.1), 0 1px 2px rgba(0,0,0,0.06);
  --shadow-md: 0 4px 6px rgba(0,0,0,0.07), 0 2px 4px rgba(0,0,0,0.06);
  --shadow-lg: 0 10px 15px rgba(0,0,0,0.1), 0 4px 6px rgba(0,0,0,0.05);
  --shadow-xl: 0 20px 25px rgba(0,0,0,0.1), 0 8px 10px rgba(0,0,0,0.04);
}
```

**Z-index scale:**
```css
:root {
  --z-base: 0;
  --z-dropdown: 100;
  --z-sticky: 200;
  --z-overlay: 300;
  --z-modal: 400;
  --z-popover: 500;
  --z-toast: 600;
  --z-tooltip: 700;
}
```

**Usage rules:**
- Cards and raised surfaces: `--shadow-xs` or `--shadow-sm`
- Dropdowns and popovers: `--shadow-md`
- Modals and dialogs: `--shadow-lg`
- Prefer border-based separation over shadows for flat/minimal designs
- In dark themes, reduce shadow opacity by 50% or use lighter border colors instead

## 6. Component API Patterns

Design components with consistent prop/variant structures:

**Button variants:**
- `primary`: Solid background, high contrast text. For the primary action on any screen.
- `secondary`: Subtle background, standard text. For secondary actions.
- `ghost`: Transparent background, visible on hover. For tertiary/inline actions.
- `destructive`: Red-toned for irreversible actions. Always require confirmation for destructive bulk actions.
- Sizes: `sm` (28px height), `md` (36px), `lg` (40px)

**Input field states:**
- Default, hover, focus, filled, disabled, error, success
- Error state: red border + error message below the field (never just a red border alone)
- Required fields: label suffix or asterisk, but also validate and show clear error messages

**Table patterns:**
- Sortable columns: header click toggles asc/desc, with a directional indicator
- Filterable: filter controls above or inline with column headers
- Selectable rows: checkbox column, bulk action bar appears on selection
- Pagination: show total count, page size selector, and page navigation
- Empty state: contextual message with a CTA to create the first item

**Modal/Dialog patterns:**
- Always include a visible close button (X) and support Escape key
- Destructive confirmations: require the user to type a confirmation string for high-risk actions
- Forms in modals: validate on submit, keep the modal open on error
- Max width: 480px for simple dialogs, 640px for forms, 800px for complex content

**Toast/Notification patterns:**
- Position: top-right for desktop, top-center for mobile
- Auto-dismiss: 5s for info/success, persist for errors and warnings
- Stack: newest on top, max 3 visible, queue the rest
- Include a dismiss button on all toasts

## 7. Responsive Strategy

**Breakpoints:**
```css
--breakpoint-sm: 640px;   /* Mobile landscape */
--breakpoint-md: 768px;   /* Tablet portrait */
--breakpoint-lg: 1024px;  /* Tablet landscape / small desktop */
--breakpoint-xl: 1280px;  /* Desktop */
--breakpoint-2xl: 1536px; /* Large desktop */
```

**Application-specific responsive rules:**
- Sidebar: collapse to icon-only at `< lg`, hide completely at `< md` and use a hamburger menu
- Data tables: switch to card view at `< md`, or use horizontal scroll with sticky first column
- Dashboard grids: 3-4 columns at xl, 2 columns at lg, 1 column at md and below
- Form layouts: 2-column at lg+, single column below
- Modals: full-screen on mobile (`< md`), centered overlay on desktop

## 8. Accessibility Standards

Every implementation must meet WCAG 2.1 AA as a baseline:

**Color contrast:**
- Normal text (< 18px): 4.5:1 minimum ratio
- Large text (>= 18px or >= 14px bold): 3:1 minimum ratio
- Interactive component borders: 3:1 against adjacent colors
- Focus indicators: 3:1 against the surrounding background

**Keyboard navigation:**
- All interactive elements must be reachable via Tab
- Logical tab order that follows visual layout
- Visible focus indicators (never `outline: none` without a replacement)
- Escape closes modals, dropdowns, and popovers
- Arrow keys navigate within component groups (tabs, menus, radio groups)

**Screen reader support:**
- Use semantic HTML: `<nav>`, `<main>`, `<aside>`, `<header>`, `<footer>`, `<section>`
- ARIA landmarks for major page regions
- `aria-label` for icon-only buttons
- `aria-live` regions for dynamic content updates (toasts, counters, status changes)
- `aria-expanded` for collapsible sections and dropdowns
- Form fields linked to labels via `for`/`id` or wrapping `<label>`

**Interaction patterns:**
- Touch targets: minimum 44x44px on mobile, 32x32px on desktop
- No hover-only interactions on mobile; always provide a tap alternative
- Respect `prefers-reduced-motion` and `prefers-color-scheme`

## 9. Dark Mode Implementation

Use semantic tokens that swap values per theme, not component-level overrides:

```css
/* Light theme (default) */
:root {
  --color-surface-base: var(--gray-0);
  --color-surface-raised: var(--gray-0);
  --color-surface-sunken: var(--gray-50);
  --color-text-primary: var(--gray-900);
  --color-text-secondary: var(--gray-500);
  --color-border-default: var(--gray-200);
}

/* Dark theme */
[data-theme="dark"] {
  --color-surface-base: var(--gray-900);
  --color-surface-raised: var(--gray-800);
  --color-surface-sunken: var(--gray-950);
  --color-text-primary: var(--gray-100);
  --color-text-secondary: var(--gray-400);
  --color-border-default: var(--gray-700);
}
```

**Dark mode rules:**
- Never invert colors mechanically. Dark mode needs its own considered palette.
- Reduce shadow intensity; use subtle borders or lighter surface colors for elevation instead.
- Primary brand colors often need a lighter variant in dark mode for sufficient contrast.
- Status colors (red, green, amber) typically need a lighter/more saturated variant.
- Images and illustrations may need a dark-mode variant or a subtle overlay to reduce glare.
- Test all states in both themes: empty, error, loading, and populated.

## 10. Platform-Specific Patterns

**Web applications:**
- Support browser zoom up to 200% without horizontal scrolling
- Handle browser back/forward for navigation state (use URL-driven routing)
- Support Cmd/Ctrl+K command palette for power users in complex apps
- Provide keyboard shortcuts for frequent actions and display them in tooltips

**Mobile web (responsive):**
- Bottom-anchored action buttons for primary actions (thumb zone)
- Swipe gestures for list item actions (delete, archive) with visual affordance
- Pull-to-refresh for data lists
- Sheet/drawer pattern instead of modals for secondary content

**Desktop-class web apps:**
- Support split panes, resizable panels, and drag-and-drop
- Right-click context menus for power users
- Multi-select with Shift+Click and Ctrl/Cmd+Click
- Status bar or footer bar for persistent contextual info
