# Design System Guide for Application UX

This reference provides a structural framework for building design systems — token architecture, component patterns, and implementation standards. The specific values (colors, sizes, fonts) shown throughout are illustrative defaults. Override them to match the application's brand, domain, and user needs. The *structure* (how tokens are layered, how components expose variants, how themes are swapped) is the transferable standard; the *values* are project-specific.

See also:
- [Core UI/UX Principles](./ui-ux-principles.md)
- [Application Aesthetics Guidelines](./aesthetics-guidelines.md)
- [Technical Implementation Patterns](./technical-implementation-patterns.md)
- [Application Layout Patterns](./application-layout-patterns.md)

## Table of Contents

0. Design Token File Format
1. Design Token Architecture (CSS Implementation)
2. Color System
3. Typography Scale
4. Spacing and Layout
5. Elevation and Shadows
6. Icon System
7. Animation and Motion Tokens
8. Data Visualization Tokens
9. Component API Patterns
10. Responsive Strategy
11. Accessibility Standards
12. Dark Mode Implementation
13. Brand Customization Layer
14. Platform-Specific Patterns
15. Design System Prose Structure

## 0. Design Token File Format

The canonical representation of a design system is a plain-text file with two layers:

1. **YAML front matter** — machine-readable design tokens delimited by `---` fences. These are the normative values that agents, build tools, and implementation code act on.
2. **Markdown body** — human-readable design rationale organized into `##` sections. Prose explains *why* the tokens exist and *how* they should be applied.

The tokens are the source of truth. The prose provides context that makes the tokens legible to humans and agents alike.

### Token Schema

```yaml
---
version: alpha          # optional
name: <string>          # project or design system name
description: <string>   # optional one-line summary
colors:
  <token-name>: <Color>
typography:
  <token-name>: <Typography>
rounded:
  <scale-level>: <Dimension>
spacing:
  <scale-level>: <Dimension | number>
components:
  <component-name>:
    <property>: <value | token reference>
---
```

### Token Types

| Type | Format | Example |
|------|--------|--------|
| Color | `#` + 6-digit hex (sRGB) | `"#1e40af"` |
| Dimension | number + unit (`px`, `em`, `rem`) | `48px`, `-0.02em` |
| Token Reference | `{path.to.token}` | `{colors.primary}`, `{typography.body-md}` |
| Typography | object with `fontFamily`, `fontSize`, `fontWeight`, `lineHeight`, `letterSpacing` | See example below |

### Recommended Token Names

**Colors:** Required: `primary`. Strongly recommended: `on-primary`, `secondary`, `on-secondary`, `tertiary`, `on-tertiary`, `neutral`, `surface`, `on-surface`, `error`, `on-error`. Common extensions: `surface-container-low`, `surface-container-high`, `surface-container-lowest`, `surface-container-highest`, `outline`, `outline-variant`.

**Typography:** `headline-display`, `headline-lg`, `headline-md`, `body-lg`, `body-md`, `body-sm`, `label-lg`, `label-md`, `label-sm`. Additional levels may use any consistent semantic naming.

**Rounded:** `none`, `sm`, `DEFAULT`, `md`, `lg`, `xl`, `full`. `DEFAULT` is the value applied when no scale modifier is used (the "base" radius).

**Spacing:** `base`, `xs`, `sm`, `md`, `lg`, `xl`, `gutter`, `margin`. The `base` key sets the grid unit.

### Complete Token File Example

```yaml
---
version: alpha
name: Meridian
description: Enterprise analytics design system — precise, trustworthy, data-dense.
colors:
  primary: "#1e40af"
  on-primary: "#ffffff"
  secondary: "#0f766e"
  on-secondary: "#ffffff"
  tertiary: "#7c3aed"
  on-tertiary: "#ffffff"
  neutral: "#f8fafc"
  surface: "#ffffff"
  on-surface: "#0f172a"
  surface-container-low: "#f1f5f9"
  surface-container-high: "#e2e8f0"
  error: "#dc2626"
  on-error: "#ffffff"
typography:
  headline-display:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: 600
    lineHeight: 1.3
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: 400
    lineHeight: 1.6
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.6
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.5
  label-lg:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: 0.01em
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1.4
  label-sm:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: 600
    lineHeight: 1.3
    letterSpacing: 0.03em
rounded:
  none: 0px
  sm: 4px
  DEFAULT: 6px
  md: 8px
  lg: 12px
  xl: 16px
  full: 9999px
spacing:
  base: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 32px
  xl: 64px
  gutter: 24px
  margin: 32px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.label-lg}"
    rounded: "{rounded.md}"
    padding: 8px 16px
    height: 36px
  button-primary-hover:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
  button-secondary:
    backgroundColor: "{colors.surface-container-low}"
    textColor: "{colors.on-surface}"
    typography: "{typography.label-lg}"
    rounded: "{rounded.md}"
    padding: 8px 16px
    height: 36px
  input-field:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    height: 36px
  card:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.lg}"
  list-item-hover:
    backgroundColor: "{colors.surface-container-low}"
    rounded: "{rounded.sm}"
---
```

### Component Token Properties

Each component entry maps a name to styled properties. Valid properties:
- `backgroundColor`: Color value or token reference
- `textColor`: Color value or token reference
- `typography`: Typography token reference (`{typography.label-md}`)
- `rounded`: Dimension or rounded token reference
- `padding`: Dimension or shorthand dimension string
- `size`: Dimension (for square/icon components)
- `height`: Dimension
- `width`: Dimension

**Variant naming:** Express hover, active, pressed, and disabled states as separate entries with a suffix: `button-primary`, `button-primary-hover`, `button-primary-active`, `button-primary-disabled`.

### WCAG AA Enforcement

Every component with both `backgroundColor` and `textColor` must meet a minimum contrast ratio of **4.5:1** (WCAG AA for normal text). Large text (≥18px or ≥14px bold) requires 3:1. Validate all component color pairs before finalizing the token file. A contrast failure is a blocking issue — no component ships with a failing pair.

### Implementation Mapping

The YAML token layer is the design-intent source of truth. CSS custom properties are the implementation layer derived from it:

| Token path | CSS custom property |
|------------|--------------------|
| `colors.primary` | `--color-primary` |
| `colors.on-surface` | `--color-text-primary` |
| `typography.body-md.fontSize` | `--text-base` |
| `rounded.md` | `--radius-md` |
| `spacing.sm` | `--space-2` |

---

## 1. Design Token Architecture (CSS Implementation)

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

### Semantic Palette (Design Token Layer)

Define colors as named semantic tokens, not raw palette steps. The semantic names carry meaning that survives brand changes:

| Token | Role | Notes |
|-------|------|-------|
| `colors.primary` | Brand accent, primary actions | Required |
| `colors.on-primary` | Text/icons on primary | Must meet 4.5:1 vs `primary` |
| `colors.secondary` | Secondary actions, supporting accents | |
| `colors.on-secondary` | Text/icons on secondary | Must meet 4.5:1 vs `secondary` |
| `colors.tertiary` | Accent highlights, tags, callouts | |
| `colors.on-tertiary` | Text/icons on tertiary | Must meet 4.5:1 vs `tertiary` |
| `colors.neutral` | Background base, page fill | |
| `colors.surface` | Component surfaces (cards, panels) | |
| `colors.on-surface` | Primary text on surface | Must meet 4.5:1 vs `surface` |
| `colors.surface-container-low` | Subtle background variant | |
| `colors.surface-container-high` | Emphasized container | |
| `colors.outline` | Borders, input strokes | |
| `colors.error` | Error states, destructive actions | |
| `colors.on-error` | Text/icons on error | Must meet 4.5:1 vs `error` |

### Primitive Palette (Implementation Layer)

Build raw hue scales (10 steps: 50–950) to back the semantic tokens above. Hue families to define at minimum:

- **Primary hue**: Brand color backing `colors.primary` variants
- **Neutral/Gray**: Backs surfaces, borders, and text tokens
- **Red**: Backs `colors.error` variants
- **Amber/Yellow**: Warning states (augments, not a required token)
- **Green**: Success states (augments, not a required token)
- **Blue**: Info states, or merge with primary if brand is blue

**Color usage rules:**
- Use semantic tokens (`colors.surface`, `colors.on-surface`) in all component specs — never raw hue steps
- Status colors: always pair with an icon; never rely on color alone for meaning
- All `backgroundColor` / `textColor` component pairs must meet **4.5:1** contrast (WCAG AA)
- Surface hierarchy: `surface-container-lowest` → `surface-container-low` → `surface` → `surface-container-high` for increasing emphasis

## 3. Typography Scale

### Semantic Scale (Design Token Layer)

Define typography as named semantic roles. Each role is a typography object with `fontFamily`, `fontSize`, `fontWeight`, `lineHeight`, and optionally `letterSpacing`:

| Token | Typical Size | Weight | Use |
|-------|-------------|--------|-----|
| `typography.headline-display` | 40–48px | 700 | Hero text, landing page hero |
| `typography.headline-lg` | 28–32px | 600–700 | Page titles, major section headings |
| `typography.headline-md` | 22–26px | 600 | Card headings, dialog titles |
| `typography.body-lg` | 18px | 400 | Lead paragraphs, emphasized content |
| `typography.body-md` | 16px | 400 | Default body text, form inputs |
| `typography.body-sm` | 14px | 400 | Secondary content, table cells, dense apps |
| `typography.label-lg` | 14px | 500 | Button labels, nav items, strong labels |
| `typography.label-md` | 12px | 500 | Field labels, table headers, badges |
| `typography.label-sm` | 11px | 600 | Fine print, timestamps, overlines |

### Implementation Scale (CSS Layer)

CSS custom property equivalents for the above roles:

| Semantic token | CSS custom property |
|----------------|--------------------|
| `typography.headline-display` | `--text-3xl` / `--text-4xl` |
| `typography.headline-lg` | `--text-2xl` |
| `typography.headline-md` | `--text-xl` |
| `typography.body-lg` | `--text-lg` |
| `typography.body-md` | `--text-base` / `--text-md` |
| `typography.body-sm` | `--text-sm` / `--text-base` |
| `typography.label-lg` | `--text-base` (medium weight) |
| `typography.label-md` | `--text-xs` |
| `typography.label-sm` | `--text-xs` (semibold) |

**Font weight tokens:**
```css
:root {
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;
}
```

For enterprise/data-heavy apps, `typography.body-sm` (14px) is the default body size. For consumer apps, use `typography.body-md` (16px). Never go below 11px for any readable text.

## 4. Spacing and Layout

### Semantic Spacing (Design Token Layer)

Define spacing as named semantic scale levels. The `base` key sets the grid unit (commonly 4px or 8px); all other values should be multiples of the base:

| Token | Typical Value | Use |
|-------|--------------|-----|
| `spacing.base` | 4px or 8px | Grid unit, minimum step |
| `spacing.xs` | 4px | Icon gaps, tight inline spacing |
| `spacing.sm` | 8px | Stack gaps within a component |
| `spacing.md` | 16px | Component internal padding, list gaps |
| `spacing.lg` | 32px | Section spacing, card padding |
| `spacing.xl` | 64px | Major layout gaps, page section gaps |
| `spacing.gutter` | 16–24px | Column gutters, grid gaps |
| `spacing.margin` | 24–40px | Page edge margins |

### Semantic Rounded (Design Token Layer)

| Token | Typical Value | Use |
|-------|--------------|-----|
| `rounded.none` | 0px | Sharp, utility elements |
| `rounded.sm` | 4px | Badges, tags, small elements |
| `rounded.md` | 6px | Buttons, inputs, chips |
| `rounded.lg` | 8–12px | Cards, panels, dialogs |
| `rounded.xl` | 12–16px | Feature cards, sheet handles |
| `rounded.full` | 9999px | Avatars, circular buttons, pills |

### Implementation Scale (CSS Layer)

**4px base grid with exponential scale:**

```css
:root {
  --space-0: 0px;
  --space-px: 1px;
  --space-0-5: 2px;
  --space-1: 4px;   /* spacing.xs */
  --space-1-5: 6px;
  --space-2: 8px;   /* spacing.sm */
  --space-3: 12px;
  --space-4: 16px;  /* spacing.md */
  --space-5: 20px;
  --space-6: 24px;  /* spacing.gutter */
  --space-8: 32px;  /* spacing.lg */
  --space-10: 40px;
  --space-12: 48px;
  --space-16: 64px; /* spacing.xl */
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

## 6. Icon System

**Icon size tokens:**
```css
:root {
  --icon-xs: 12px;   /* Inline with small text, badges */
  --icon-sm: 16px;   /* Inline with body text, table cells, compact buttons */
  --icon-md: 20px;   /* Default: nav items, standard buttons, form field icons */
  --icon-lg: 24px;   /* Page headers, feature cards, prominent actions */
  --icon-xl: 32px;   /* Empty states, feature highlights */
  --icon-2xl: 48px;  /* Hero empty states, onboarding illustrations */
}
```

**Icon design constraints:**
- **Stroke width**: Use 1.5px stroke for 20-24px icons, 1px for 16px icons, 2px for 32px+ icons. Maintain consistent stroke weight within each size tier.
- **Optical alignment**: Icons inside buttons should optionally reduce by 1-2px from the standard size at that tier. A 20px icon in a button may render at 18px for optical balance with the label text.
- **Color**: Icons inherit `currentColor` by default and should never have hard-coded fill colors. Apply color through the parent element's text color.
- **Touch targets**: The clickable area around an icon must meet minimum target sizes (44x44px mobile, 32x32px desktop) regardless of the icon's visual size. Use padding, not scaling.
- **Icon-only buttons**: Always include `aria-label` with a descriptive action label. Always include a tooltip on hover for sighted users.

**Recommended icon pairing with text:**
| Context | Icon Size | Gap Between Icon and Text |
|---------|-----------|--------------------------|
| Navigation item | 20px | 12px (--space-3) |
| Button with icon | 16-18px | 8px (--space-2) |
| Table cell status | 16px | 6px (--space-1-5) |
| Badge / tag | 12px | 4px (--space-1) |
| Section heading | 20-24px | 8-12px |

## 7. Animation and Motion Tokens

**Duration tokens:**
```css
:root {
  --duration-instant: 0ms;
  --duration-fast: 100ms;     /* Hover states, color transitions */
  --duration-normal: 150ms;   /* Button presses, micro-interactions */
  --duration-moderate: 250ms; /* Panel slides, dropdowns, accordions */
  --duration-slow: 350ms;     /* Page transitions, modal enter/exit */
  --duration-slower: 500ms;   /* Complex choreographed transitions */
}
```

**Easing tokens:**
```css
:root {
  --ease-default: cubic-bezier(0.25, 0.1, 0.25, 1.0);     /* General purpose */
  --ease-in: cubic-bezier(0.42, 0, 1, 1);                   /* Elements exiting */
  --ease-out: cubic-bezier(0, 0, 0.58, 1);                  /* Elements entering */
  --ease-in-out: cubic-bezier(0.42, 0, 0.58, 1);            /* Elements moving */
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);         /* Playful/bouncy enter */
  --ease-premium: cubic-bezier(0.16, 1, 0.3, 1);            /* Elegant fast-out */
}
```

**Standard transition compositions:**
```css
:root {
  --transition-colors: color var(--duration-fast) var(--ease-default),
                       background-color var(--duration-fast) var(--ease-default),
                       border-color var(--duration-fast) var(--ease-default);
  --transition-opacity: opacity var(--duration-normal) var(--ease-default);
  --transition-transform: transform var(--duration-normal) var(--ease-out);
  --transition-shadow: box-shadow var(--duration-fast) var(--ease-default);
  --transition-all-micro: all var(--duration-normal) var(--ease-default);
}
```

**Reduced motion override:**
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

## 8. Data Visualization Tokens

**Categorical color palette** (for charts with distinct categories):
```css
:root {
  --chart-cat-1: #2563eb;  /* Blue */
  --chart-cat-2: #7c3aed;  /* Purple */
  --chart-cat-3: #db2777;  /* Pink */
  --chart-cat-4: #ea580c;  /* Orange */
  --chart-cat-5: #ca8a04;  /* Yellow */
  --chart-cat-6: #16a34a;  /* Green */
  --chart-cat-7: #0891b2;  /* Cyan */
  --chart-cat-8: #4f46e5;  /* Indigo */
}
```

**Sequential color palette** (for magnitude/intensity, single hue):
```css
:root {
  --chart-seq-1: var(--blue-100);
  --chart-seq-2: var(--blue-200);
  --chart-seq-3: var(--blue-300);
  --chart-seq-4: var(--blue-400);
  --chart-seq-5: var(--blue-500);
  --chart-seq-6: var(--blue-600);
  --chart-seq-7: var(--blue-700);
  --chart-seq-8: var(--blue-800);
}
```

**Diverging color palette** (for above/below threshold, positive/negative):
```css
:root {
  --chart-div-neg-3: #dc2626;  /* Strong negative */
  --chart-div-neg-2: #f87171;
  --chart-div-neg-1: #fca5a5;
  --chart-div-neutral: #e5e7eb;
  --chart-div-pos-1: #86efac;
  --chart-div-pos-2: #4ade80;
  --chart-div-pos-3: #16a34a;  /* Strong positive */
}
```

**Chart typography and spacing:**
```css
:root {
  --chart-font-size: 11px;
  --chart-font-family: var(--font-sans);
  --chart-label-color: var(--color-text-secondary);
  --chart-grid-color: var(--color-border-default);
  --chart-axis-color: var(--color-text-tertiary);
  --chart-tooltip-bg: var(--color-surface-overlay);
  --chart-tooltip-shadow: var(--shadow-md);
  --chart-bar-radius: var(--radius-sm);
  --chart-line-width: 2px;
  --chart-dot-radius: 4px;
}
```

**Chart design rules:**
- Maximum 6-8 categories in a single chart; group smaller slices into "Other"
- Always include axis labels, units, and a chart title
- Use consistent color mapping across all charts on the same page (if "Revenue" is blue in one chart, it is blue in every chart)
- Tooltips on hover for precise values — never rely on reading exact values from axes
- Responsive: charts should resize with their container; use SVG-based renderers or responsive chart libraries

## 9. Component API Patterns

### Component Token Format (Design Token Layer)

Before implementing any component, define its visual contract in the token file. Each component entry specifies what tokens back its appearance, making the component independently auditable for accessibility and brand consistency.

**Valid component properties:**

| Property | Type | Description |
|----------|------|-------------|
| `backgroundColor` | Color or token reference | Fill color |
| `textColor` | Color or token reference | Foreground text/icon color |
| `typography` | Token reference | Type style applied to label/content |
| `rounded` | Dimension or token reference | Border radius |
| `padding` | Dimension string | Internal spacing (shorthand OK) |
| `height` | Dimension | Fixed or minimum height |
| `width` | Dimension | Fixed or minimum width |
| `size` | Dimension | Shorthand for square components |

All `backgroundColor` + `textColor` pairs must meet **4.5:1 contrast** (WCAG AA). Validate before finalizing.

**Example: Button token entries**
```yaml
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.label-lg}"
    rounded: "{rounded.md}"
    padding: 8px 16px
    height: 36px
  button-primary-hover:
    backgroundColor: "{colors.primary}"  # darken 10% at CSS layer
    textColor: "{colors.on-primary}"
  button-primary-active:
    backgroundColor: "{colors.primary}"  # darken 15%
    textColor: "{colors.on-primary}"
  button-primary-disabled:
    backgroundColor: "{colors.surface-container-high}"
    textColor: "{colors.on-surface}"    # check contrast at ~38% opacity
  button-secondary:
    backgroundColor: "{colors.surface-container-low}"
    textColor: "{colors.on-surface}"
    typography: "{typography.label-lg}"
    rounded: "{rounded.md}"
    padding: 8px 16px
    height: 36px
```

**Variant naming convention:** Append `-hover`, `-active`, `-pressed`, `-disabled`, `-focused`, `-selected`, `-error` to the base component name.

### Component Behavior Patterns

Design components with consistent prop/variant structures:

**Button variants:****
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

## 10. Responsive Strategy

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

## 11. Accessibility Standards

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

## 12. Dark Mode Implementation

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

## 13. Brand Customization Layer

When building a design system that serves a specific brand, override primitive tokens at the brand level while keeping the semantic and component token structure intact.

**Brand override file structure:**
```css
/* brand-tokens.css — loaded after base tokens */
:root {
  /* Override primary hue to match brand */
  --brand-hue: 210;       /* Brand's primary hue (HSL) */
  --brand-sat: 80%;       /* Brand saturation */

  /* Generate primary scale from brand hue */
  --primary-50:  hsl(var(--brand-hue), var(--brand-sat), 97%);
  --primary-100: hsl(var(--brand-hue), var(--brand-sat), 93%);
  --primary-200: hsl(var(--brand-hue), var(--brand-sat), 85%);
  --primary-300: hsl(var(--brand-hue), var(--brand-sat), 72%);
  --primary-400: hsl(var(--brand-hue), var(--brand-sat), 58%);
  --primary-500: hsl(var(--brand-hue), var(--brand-sat), 48%);
  --primary-600: hsl(var(--brand-hue), var(--brand-sat), 40%);
  --primary-700: hsl(var(--brand-hue), var(--brand-sat), 33%);
  --primary-800: hsl(var(--brand-hue), var(--brand-sat), 26%);
  --primary-900: hsl(var(--brand-hue), var(--brand-sat), 18%);

  /* Override neutral temperature */
  --neutral-hue: 220;     /* Tinted neutrals matching brand */
  --neutral-sat: 10%;     /* Keep low for functional neutrals */

  /* Override font families */
  --font-sans: 'Custom Brand Font', system-ui, sans-serif;
  --font-mono: 'Custom Mono Font', 'Fira Code', monospace;

  /* Override radius to match brand personality */
  --radius-sm: 3px;       /* Sharper = more technical */
  --radius-md: 5px;
  --radius-lg: 8px;

  /* Override elevation model (flat brands can reduce shadows) */
  --shadow-xs: none;
  --shadow-sm: 0 0 0 1px var(--color-border-default);
}
```

**Brand customization principles:**
- Override primitives, not semantics. Change the hue scale, not `--color-action-primary`.
- Keep the semantic token layer intact so that dark mode, accessibility, and component patterns continue to work.
- Maximum two custom fonts (one sans, one mono or one serif). Additional fonts degrade performance and consistency.
- Test the brand overrides against all component states (hover, active, focus, disabled, error) in both light and dark themes before shipping.
- Document departures from the base system. If the brand requires a radius larger than 12px or a non-standard shadow, record the rationale.

## 14. Platform-Specific Patterns

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

---

## 15. Design System Prose Structure

The human-readable body of a design token file follows a canonical section order. When sections are present, they must appear in this sequence. Sections may be omitted but must not be reordered.

### Canonical Section Order

| # | Section Title (aliases) | Documents |
|---|------------------------|-----------|
| 1 | **Overview** (Brand & Style) | Design personality, product purpose, visual direction brief. The "why" that explains all token choices. |
| 2 | **Colors** | Palette rationale, color roles, emotional intent, usage rules, dark/light variants. |
| 3 | **Typography** | Typeface selection rationale, scale logic, voice and readability principles. |
| 4 | **Layout** (Layout & Spacing) | Grid system, spacing principles, density strategy, breakpoints. |
| 5 | **Elevation & Depth** (Elevation) | Hierarchy method, shadow philosophy, layering strategy. |
| 6 | **Shapes** | Radius language, corner logic, how shape expresses personality. |
| 7 | **Components** | Atom-level component guidance, interaction principles, state rules. |
| 8 | **Do's and Don'ts** | Guardrails, anti-patterns, common misapplications. |

### Section Content Guidelines

**Overview:** Write 2–4 paragraphs. Cover: (1) product context and intended user, (2) emotional register and brand personality, (3) one-sentence design direction ("This system is ____. It is not ____."). Reference the font and primary color as anchors for the direction.

**Colors:** Name every palette entry and explain its role. Cover: primary story, neutral strategy (warm/cool/pure), accent use, status color philosophy. Do not just list hex values — explain the emotional logic.

**Typography:** Name the typefaces chosen and explain *why* — not just what they look like, but what they say about the product. Cover: scale reasoning, weight strategy, editorial vs. functional use cases.

**Layout:** Cover: base grid unit and why, spacing philosophy (generous vs. dense), responsive behavior intention.

**Elevation & Depth:** Declare the elevation model (flat / layered / blended) and explain which surfaces are elevated and why.

**Shapes:** Describe the radius personality: sharp = technical/precise, rounded = friendly/approachable, circular = energetic/bold. State the default radius and when to deviate.

**Components:** Describe design principles for atomic components. When a full component token set is present in the YAML front matter, this section contextualizes the choices.

**Do's and Don'ts:** Use short, concrete entries. Format as: ✓ Do [specific thing] / ✗ Don't [specific thing]. Cover color misuse, typography abuse, layout violations, accessibility anti-patterns.
