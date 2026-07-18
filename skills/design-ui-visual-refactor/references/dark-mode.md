# Palettes & Dark Mode

Building a systematic color palette (the light-mode foundation) and adapting it correctly for dark mode. Dark mode is not an inversion — it needs deliberate decisions to keep hierarchy, comfort, and depth.

## Systematic Palette (Light Foundation)

Every color needs a ramp of 5–9 shades (50 → 900), derived so they feel like one family:
- **Darkest shade is a dark gray, not `#000`.** Pure black is harsh and causes text "halation."
- **Grays carry subtle saturation** matched to the UI temperature — cool product → blue-tinted grays; warm product → brown/yellow-tinted.
- **Derive shades via HSL**: lighter = raise lightness, drop saturation; darker = lower lightness, raise saturation.
- Three working text levels: dark (`gray-900`), medium (`gray-600`), light (`gray-400`), plus semantic ramps (success/warning/error).

## Dark Mode Principles

**1. Dark grays, not pure black.** Base around `#18181b`; layer surfaces upward (`#09090b` deepest → `#18181b` cards → `#27272a` inputs/hover → `#3f3f46` active).

**2. Off-white text, reduced contrast.** Primary text ~`#fafafa` (not `#fff`), secondary `#a1a1aa`, tertiary `#71717a`. Max contrast reads harsher in the dark.

**3. Desaturate accents.** Bright saturated colors vibrate on dark backgrounds — shift accents lighter and less saturated (light `#2563eb` → dark `#3b82f6`).

**4. Elevate with lightness, not shadow.** Shadows are near-invisible on dark surfaces; show elevation by making raised surfaces *lighter* than their background.

## Semantic Tokens

Drive everything through tokens that swap by theme, so components never hardcode a mode:
```css
:root {
  --color-bg: #ffffff;      --color-bg-subtle: #f4f4f5;
  --color-text: #18181b;    --color-text-muted: #71717a;
  --color-border: #e4e4e7;  --color-primary: #2563eb;
}
[data-theme="dark"] {
  --color-bg: #18181b;      --color-bg-subtle: #27272a;
  --color-text: #fafafa;    --color-text-muted: #a1a1aa;
  --color-border: #3f3f46;  --color-primary: #3b82f6;
}
```
Structural tokens (spacing, radius) stay fixed; only color tokens change per theme. Multiple brand themes work the same way — swap the color tokens.

## Implementation

- **System-only**: `@media (prefers-color-scheme: dark)` overriding the `:root` custom properties.
- **User toggle**: a `data-theme` attribute (or Tailwind `darkMode: 'class'`) + `localStorage` persistence, initialized from the saved value or the system preference. Offer Light / Dark / System.

## Component Notes

- **Cards/surfaces**: dark mode uses a lighter surface (`gray-900`) and a subtle border instead of a shadow.
- **Inputs**: dark bg (`gray-900`) + `gray-700` border.
- **Images**: dim slightly (`filter: brightness(.9) contrast(1.1)`); invert line diagrams if needed.
- **Code blocks**: ship a dark syntax theme, don't leave a light block glowing.

## Testing

Same WCAG ratios apply in dark mode (4.5:1 text, 3:1 large/UI). Check every text-on-surface combination — colors interact differently against dark. Common fails: muted gray text too dim, disabled states invisible, focus rings lost. Verify hierarchy, focus visibility, and that images don't blow out.
