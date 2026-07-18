# Signifiers

Signifiers are perceivable cues telling people *where* and *how* to act. Affordances define what's possible; signifiers are what users actually rely on to discover and use them. A door affords pulling, but the "Pull" label is the signifier — and in practice signifiers matter more, because they're what users see.

## Types

- **Deliberate** — designed to communicate: "Push" label, placeholder text, tooltip, dropdown chevron, step indicator ("1 of 4"), breadcrumbs.
- **Accidental** — informative but unintended: worn path in grass, fingerprints on a touchscreen, analytics heatmaps (accidental signifiers *for the designer*).
- **Social** — derived from others' behavior: a queue, star ratings, "1,204 people viewing", typing indicator.

## Digital Catalog

- **Cursor** — pointer (clickable), text beam (editable), grab/grabbing (draggable), resize arrows, wait, not-allowed.
- **Hover** — background change (whole area interactive), underline (link), shadow lift, border change, opacity/scale.
- **Labels/placeholders** — a permanent label identifies the field; placeholder shows format/example and **never replaces the label**; helper text for constraints; character counter; required marker.
- **Icons** — pair with a text label whenever meaning is even slightly ambiguous (a gear can mean settings *or* processing).
- **Color** — blue=interactive, red=error, green=success, amber=warning, gray=disabled — never the *sole* signal.
- **Position** — logo top-left, account/cart top-right, close top-right of a card, primary action bottom-right of a form, mobile primary nav at the bottom.

## Hierarchy

When many signifiers compete, rank them: **primary** (large, high-contrast, filled — one per view), **secondary** (medium, outlined/muted), **tertiary** (small, text/icon-only), **ambient** (subtle, always-present nav/status). Mistakes: multiple primary buttons, competing accent colors, equal-weight labels.

## Cultural / Localization

Signifiers carry cultural meaning that doesn't always translate: red = danger (West) vs luck (East Asia); checkmark = correct (West) vs incorrect (Japan/Korea); thumbs-up offensive in parts of the Middle East; LTR "forward" arrow means "back" in RTL. Checklist: review icons per market; adapt directional signifiers to RTL; don't rely on color alone; test comprehension with target-culture users; pair icons with text in localized versions.

## Over- vs Under-Signifying

- **Under** — too few cues: "what do I do here?", low discovery, clicks on non-interactive elements.
- **Over** — too many cues: visual noise, nothing stands out, "cluttered", primary action missed.

Balance: every signifier earns its place (remove any that don't help a task); progressive disclosure (essentials first); consistent patterns (learn once, apply everywhere); whitespace itself signifies importance.

## Testing

- **5-second test** — show for 5s, hide, ask what the page was about, what you could do, what you'd click first.
- **First-click test** — <70% correct first clicks means the target's signifier is too weak.
- **Think-aloud** — listen for "is this a button?", "what does this icon mean?", "I didn't notice that."

## Audit

Visibility: every interactive element has ≥1 visible signifier; primary actions strongest; system state always visible. Clarity: icons paired with labels/tooltips; color never sole signal; cursor changes on desktop; placeholders don't replace labels. Consistency: same pattern means the same thing everywhere; position conventions held. Accessibility: signifiers work without color; visible focus; screen-reader-equivalent info via ARIA.
