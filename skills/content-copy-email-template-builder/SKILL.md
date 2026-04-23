---
name: content-copy-email-template-builder
description: 'Design and build production-ready HTML email templates that are on-brand, responsive, and importable into email platforms (Resend, Postmark, Mailgun, SendGrid, Mailchimp, Customer.io, Kit, etc.). Use when asked for "HTML email template", "email template code", "responsive email", "branded email template", "import email template", "transactional email design", "email design system", "email component", "email layout", or "ESP template". Covers full template design: layout, typography, color system, components, responsive behavior, dark mode, and platform export.'
license: MIT
metadata:
  version: "1.0.0"
  domain: content
  triggers: HTML email template, email template code, responsive email template, branded email template, transactional email design, email design system, email component, ESP template, import email template, email layout, email header footer, email button component, email on-brand, Resend template, Postmark template, Mailgun template, SendGrid template, Mailchimp template, Customer.io template, email HTML, mjml template, email CSS, dark mode email
  role: specialist
  scope: creation
  output-format: code
  related-skills: content-copy-email-sequences, content-copy-humanizer, content-style-extractor
---

# Email HTML Template Builder

Senior email design engineer + brand systems specialist. Deep in HTML/CSS email rendering quirks, cross-client compatibility, responsive layout, and design token systems. Specialize in building modular, on-brand template libraries that produce consistent output across every major email client and import cleanly into any ESP.

## Product Context Check

Before building, check for existing brand context:
- If `.agents/product-marketing-context.md` exists → read it first for brand colors, fonts, tone, logo
- If a brand style guide or design system file is referenced → load it
- Ask only for what isn't already covered

---

## Workflow

### Phase 1: Brand Intake

Gather brand foundation before writing a single line of HTML.

**Required inputs:**
- Primary brand color (hex) + secondary / accent colors
- Background color(s) — email body, card/content area
- Primary font family (+ web-safe fallback stack)
- Logo URL or file path
- Brand tone: formal · conversational · playful · technical
- Button style: rounded · pill · square + border or fill

**Helpful but infer if missing:**
- Header layout (logo left · centered · logo + nav)
- Footer structure (unsubscribe · address · social links · legal)
- Content width (600px standard, 640px or 680px acceptable)
- Dark mode preference (support or ignore)

If user provides brand hex + tone → proceed with sensible defaults for the rest. State assumptions clearly.

---

### Phase 2: Design System Definition

Define design tokens before building components. Every template value derives from these tokens — never hardcoded inline.

**Token set (define all before any HTML):**
```
Color tokens:
  --color-brand-primary: #[hex]
  --color-brand-secondary: #[hex]
  --color-accent: #[hex]
  --color-bg-body: #[hex]          (email client background, typically #f4f4f5 or #ffffff)
  --color-bg-content: #[hex]       (content card, typically #ffffff)
  --color-text-primary: #[hex]     (body text, typically #111827 or #1a1a1a)
  --color-text-secondary: #[hex]   (secondary / muted text)
  --color-text-link: #[hex]        (inline links)
  --color-border: #[hex]           (dividers, card borders)
  --color-button-bg: #[hex]
  --color-button-text: #[hex]

Typography tokens:
  --font-family: "[brand font]", [system fallback stack]
  --font-size-base: 16px
  --font-size-sm: 14px
  --font-size-lg: 20px
  --font-size-h1: 28px
  --font-size-h2: 22px
  --line-height-body: 1.6
  --line-height-heading: 1.3

Spacing tokens:
  --spacing-content-width: 600px
  --spacing-padding-outer: 24px
  --spacing-padding-inner: 32px
  --spacing-section-gap: 24px

Border tokens:
  --border-radius-button: [4px | 6px | 24px for pill]
  --border-radius-card: [0px | 4px | 8px]
```

---

### Phase 3: Component Library

Build components in isolation before assembling templates. Every component uses only token values — no hardcoded colors or sizes.

**Core components (always build):**

**Header**
- Logo placement + max-width
- Background: brand primary or white
- Responsive: logo scales or stacks on mobile

**Hero / Banner**
- Optional background image (with solid color fallback)
- Headline (H1), optional subhead, optional CTA button
- Centered or left-aligned layout

**Body Content Block**
- Heading (H2) + paragraph text + optional inline link
- List support (styled bullets, no `<ul>` default browser indent artifacts)
- Max-width respected, padding consistent with tokens

**CTA Button**
- Bullet-proof button (VML fallback for Outlook)
- Token-driven: color, radius, padding
- Mobile: full-width option

**Divider**
- Thin rule or spacer (token border color)

**Image Block**
- Responsive `max-width: 100%`, `display: block`
- Alt text placeholder always included

**Two-Column Layout**
- Side-by-side on desktop, stacked on mobile via media query

**Footer**
- Unsubscribe link (required — `{{unsubscribe_url}}` placeholder)
- Physical mailing address (required for CAN-SPAM/GDPR)
- Social links (optional)
- Legal text (optional)
- Muted text color, smaller font size

---

### Phase 4: Assemble Templates

Compose components into full templates. Build only the types the user requests, or the full set if building a template library.

**Standard template set:**

| Template | Use case | Key components |
|----------|----------|----------------|
| `transactional` | Receipts, confirmations, alerts | Header · content block · CTA · footer |
| `welcome` | First email after signup | Header · hero · content block · CTA · footer |
| `newsletter` | Regular content send | Header · hero · multi-section · dividers · footer |
| `promotional` | Offer / campaign | Header · hero w/ image · CTA · content block · footer |
| `notification` | System alert, usage report | Header · content block (no hero) · CTA · footer |

See [assets/templates/](assets/templates/) for base HTML files per type.

---

### Phase 5: Platform Export

Adapt template for the target ESP. Output the correct variable syntax and import format.

**Variable syntax by platform:**

| Platform | Syntax | Notes |
|----------|--------|-------|
| Resend | `{{variable}}` (React Email or raw HTML) | Supports JSX components via `@react-email` |
| Postmark | `{{variable}}` | Handlebars-style; supports conditionals `{{#if}}` |
| Mailgun | `{{variable}}` | Handlebars; also supports `%recipient.variable%` |
| SendGrid | `{{variable}}` or `{{{variable}}}` (unescaped) | Dynamic templates use Handlebars |
| Mailchimp | `*|VARIABLE|*` | Merge tags; `*|IF:VARIABLE|*` for conditionals |
| Customer.io | `{{customer.variable}}` | Liquid-style; `{% if %}` blocks |
| Kit (formerly ConvertKit) | `{{ subscriber.variable }}` | Liquid |
| HubSpot | `{{ contact.variable }}` | HubSpot Expression Language |

**Required placeholders in every template:**
- `{{unsubscribe_url}}` (or platform-equivalent)
- `{{first_name}}` with fallback: `{{first_name | default: "there"}}`
- Mailing address block (static or token)

See [references/platform-export.md](references/platform-export.md) for full import instructions per ESP.

---

### Phase 6: Quality Check

Run before delivering any template.

**Rendering compatibility:**
- Tables-based layout (not CSS Grid/Flexbox for structure)
- All CSS inlined — no `<link>` stylesheets (use `<style>` block for media queries only)
- No JavaScript
- `width` set on `<td>` not just CSS
- Images have `display: block` + explicit `width` + `alt` attribute
- `<a>` tags have explicit `color` and `text-decoration` inline (Outlook strips inherited styles)

**Bullet-proof button check:**
- VML fallback present for Outlook desktop
- Background color set on both `<a>` and surrounding `<td>`
- Padding on `<a>` not `<td>` (for Apple Mail/iOS)

**Responsive check:**
- `<meta name="viewport">` present
- Media query in `<style>` block: `.mobile { width: 100% !important }`
- Two-column layouts collapse to single column on mobile
- Font sizes increase slightly on mobile (`font-size: 18px` for body at <600px)

**Dark mode check (if supported):**
- `@media (prefers-color-scheme: dark)` block defined
- Background and text color overrides set
- Logo: use SVG or white/light version for dark mode
- `color-scheme: light dark` in `<meta>` tag

**Accessibility:**
- `lang` attribute on `<html>`
- `role="presentation"` on layout tables
- Meaningful alt text on all images (not empty unless purely decorative)
- Sufficient color contrast (4.5:1 for body text)

See [references/rendering-compatibility.md](references/rendering-compatibility.md) for client-specific quirks.

---

## Output Format

### Design System Block
```
Brand tokens defined:
- Primary color: #[hex]
- Font: [family]
- Content width: [px]
- Button style: [description]
- [any assumptions stated]
```

### Per Template / Component
```
File: [template-name].html
Platform: [target ESP or "universal"]
Variables: [list of {{placeholders}} used]
[Full HTML code block]
```

### Export Notes
```
Platform: [ESP name]
Variable syntax: [syntax used]
Import method: [how to import — dashboard / API / CLI]
Required setup: [any platform-specific steps]
```

---

## Constraints

### MUST DO
- Define all design tokens before writing any HTML
- Use tables-based layout for structural columns — not CSS Flexbox or Grid
- Inline all CSS except media queries and `prefers-color-scheme`
- Include bullet-proof VML button fallback for all CTA buttons
- Set `display: block` + explicit `width` + `alt` on every `<img>`
- Include unsubscribe link placeholder in every template footer
- Include physical mailing address in every template footer
- Use platform-correct variable syntax when a target ESP is specified
- State brand assumptions explicitly when inputs are incomplete
- Deliver complete, copy-paste-ready HTML — no truncated "add your content here" stubs

### MUST NOT DO
- Don't use CSS Grid or Flexbox for layout columns
- Don't use `<link>` external stylesheets
- Don't use JavaScript
- Don't use background-image for critical content (Outlook ignores it)
- Don't hardcode colors or font sizes outside the token system
- Don't use `padding` on `<tr>` or `<table>` elements (use `<td>`)
- Don't reference specific brand assets (logos, images) without confirming they're accessible URLs
- Don't deliver templates without running the Phase 6 quality check mentally

---

## Output Checklist

- [ ] Brand tokens defined (colors, fonts, spacing, radius)
- [ ] All assumptions stated if inputs were incomplete
- [ ] Tables-based layout — no Flexbox/Grid for structure
- [ ] All CSS inlined except media queries
- [ ] VML bullet-proof button included
- [ ] Images: `display: block`, explicit `width`, `alt` text
- [ ] Unsubscribe placeholder in footer
- [ ] Physical address in footer
- [ ] Platform variable syntax correct for target ESP
- [ ] Responsive: viewport meta + media query for mobile
- [ ] Dark mode blocks present (if requested)
- [ ] Accessibility: `lang`, `role="presentation"`, contrast checked
- [ ] Full copy-paste-ready HTML delivered

---

## References

- [references/platform-export.md](references/platform-export.md) — import instructions and variable syntax for each ESP
- [references/rendering-compatibility.md](references/rendering-compatibility.md) — client-specific quirks (Outlook, Gmail, Apple Mail, etc.)
- [assets/templates/](assets/templates/) — base HTML starter files per template type

---

## Knowledge Reference

HTML email, CSS inlining, tables-based layout, VML, MSO conditionals, Outlook rendering, Gmail CSS support, Apple Mail dark mode, media queries, `@media prefers-color-scheme`, `color-scheme`, responsive email, fluid layout, bullet-proof buttons, Litmus, Email on Acid, MJML, React Email, Handlebars merge tags, Liquid templating, CAN-SPAM, GDPR, design tokens, brand systems, Resend, Postmark, Mailgun, SendGrid, Mailchimp, Customer.io, Kit, HubSpot, ESP import, transactional email, accessibility, WCAG contrast, `role="presentation"`, alt text
