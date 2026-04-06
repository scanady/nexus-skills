# Application Aesthetics Guidelines

Use this reference when the user needs stronger visual direction, clearer application personality, or help avoiding generic AI-generated UI patterns.

## Typography for Applications

- Choose fonts optimized for UI, not display. Good application fonts have multiple weights, clear numeric distinction, and strong readability at 13-16px. Avoid decorative display fonts for body or UI text.
- Define a strict type scale and use it consistently. Suggested starting point: 12, 13, 14, 16, 18, 20, 24, 30px with corresponding line-heights.
- Use font weight, not just size, to create hierarchy. Semi-bold headings with regular body text usually creates cleaner contrast than oversized headings.
- Use a monospace companion font for code, data, and technical values.

## Color for Applications

- Build the palette from function outward. Start with semantic colors for action, success, warning, error, and info, then derive neutrals and surfaces.
- Use CSS custom properties with a naming convention like `--color-{category}-{variant}`.
- Design for both light and dark themes from the start. Map semantic tokens per theme instead of hard-coding colors into components.
- Reserve high-saturation colors for status and actions. Keep large surfaces more restrained.

## Motion for Applications

- Motion should communicate state changes, not decorate static content.
- Use consistent timing: around 150ms for micro-interactions, 250ms for panel transitions, and 350ms for page-level changes.
- Reduce motion when `prefers-reduced-motion` is set.
- Keep skeleton loading animation subtle. Prefer opacity pulsing over dramatic shimmer effects.

## Layout for Applications

- Use a 4px or 8px spatial grid consistently.
- Keep sidebar widths in the 240-280px range when expanded and 64-72px when collapsed.
- Keep content areas around 1200-1440px for most apps, with full width reserved for tables and analytics surfaces that need it.
- Use `auto-fill` with `minmax()` for responsive card grids.
- Respect the fold for dashboards. The most important KPIs belong above it.

## Anti-Patterns to Avoid

- Purple-gradient hero sections in application interfaces
- Excessive border-radius over 12px on functional components
- Decorative blob or wave backgrounds in tool interfaces
- Marketing-style testimonial cards inside product UIs
- Stock illustration empty states when purposeful copy or domain-specific illustration would be clearer
- Overusing shadows when borders or surface contrast are sufficient
- Generic AI-generated aesthetics like purple-blue-teal gradients, floating card grids, or over-rounded components

Every application should feel designed for the domain, the users, and the operating context rather than assembled from interchangeable prompt-era patterns.