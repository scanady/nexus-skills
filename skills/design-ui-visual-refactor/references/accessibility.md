# Accessibility (WCAG 2.1 AA)

The accessibility layer of a visual refactor. Accessibility is not just compliance — good contrast, focus, and structure improve the experience for everyone. Organized by the four POUR principles, then focus management and testing.

## Perceivable

**Text alternatives** — every image gets `alt`; decorative images get `alt=""`/`role="presentation"`; icon-only buttons get `aria-label` and mark the glyph `aria-hidden="true"`; complex images get a longer `aria-describedby` description.

**Semantic structure** — real `header/nav/main/article/section/footer`, one `<h1>` per page, no skipped heading levels. Every input has a real `<label>` (use `sr-only` when the visual design hides it).

**Contrast** — normal text ≥ 4.5:1, large text (≥18px, or ≥14px bold) ≥ 3:1, UI components/graphics ≥ 3:1. Practical grays on white: `gray-400 #9ca3af` fails (~3.1:1), `gray-500 #6b7280` passes AA (~4.6:1), `gray-700 #374151` passes AAA (~9:1). **Never encode meaning in color alone** — pair with icon + text (e.g. an invalid field gets `aria-invalid`, a red border, an icon, *and* a message). Content must stay usable at 200% zoom — size text in `rem`/`em`.

## Operable

**Keyboard** — all functionality works without a mouse:

| Key | Behavior |
|-----|----------|
| Tab / Shift+Tab | move focus forward / back |
| Enter | activate links, buttons |
| Space | activate buttons, toggle checkboxes |
| Arrows | move within a component (tabs, menus, radios) |
| Escape | close modal/dropdown, cancel |

**Visible focus** — never `outline: none` without a replacement; use `:focus-visible` with a ring + offset. Modals trap focus but must exit on Escape. Provide a "skip to main content" link. Don't set positive `tabindex`; only `0` (focusable) or `-1` (programmatic).

**Link purpose** — link text makes sense out of context ("Read more about X", not bare "Click here").

## Understandable

Declare page language (`<html lang>`, plus `lang` on foreign phrases). Keep navigation consistent across pages. No surprise changes — don't auto-submit on `select` change or move focus unexpectedly. Identify errors in text with a fix hint, mark required fields with both a visible marker and `aria-required`, and confirm/allow-undo on destructive actions.

## Robust

Valid HTML (unique IDs, proper nesting). Prefer native elements over ARIA (`<button>` over `role="button"`). When ARIA is needed, use it correctly — states (`aria-pressed`, `aria-expanded`, `aria-controls`) and live regions (`aria-live="polite"`) for dynamic updates.

## Focus Management

| Event | Focus action |
|-------|--------------|
| Modal opens | first element inside |
| Modal closes | return to the trigger |
| Error | the error/first invalid field |
| New content loads | its heading / first new element |
| Item deleted | neighbor or container |

Store the trigger element before opening an overlay and restore focus on close. For component groups (tabs, menus, radio groups) use a roving `tabindex` (active = `0`, others = `-1`) with arrow-key navigation.

## Screen Readers

Announce dynamic changes through an `aria-live` region. Hide purely decorative glyphs with `aria-hidden`. Disambiguate repeated controls ("Delete" → `aria-label="Delete comment by John"`).

## Testing

Automated tools (axe, WAVE, Lighthouse, eslint-jsx-a11y) catch ~30% of issues — the rest is manual. Checklist:
- [ ] Full page operable by keyboard only
- [ ] Screen-reader pass (VoiceOver/NVDA)
- [ ] Contrast checked with a tool
- [ ] Usable at 200% zoom
- [ ] Focus indicators always visible
- [ ] Heading structure logical
- [ ] Forms announce and locate validation errors
- [ ] `prefers-reduced-motion` respected
