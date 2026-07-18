# Feedback Patterns

Feedback answers "what just happened?" — it makes the rules visible and closes the Gulf of Evaluation. Too little breeds anxiety; too much breeds noise.

## The Feedback Hierarchy

Match intensity and duration to the event's significance. **Use the least feedback that still communicates.**

| Event | Feedback level | Duration |
|-------|----------------|----------|
| Micro (hover, focus) | subtle visual change | instant |
| Minor (tap, toggle) | clear visual change | 100–300ms |
| Medium (save, send) | visual + state label | 1–3s |
| Major (purchase, delete) | multi-signal + undo | 3–5s, dismissable |
| Critical (error) | prominent, persistent | until acknowledged |

## Visual (primary channel)

Color: state shift (toggle gray→green), validation (green/red border), progress fill, attention flash, semantic system (red/green/yellow/blue used consistently).

Animation — keep to a small set of durations, applied by category:

| Animation | Duration | Easing |
|-----------|----------|--------|
| Button press | 50–100ms | ease-out (scale ~0.97) |
| Toggle slide | 150–250ms | ease-in-out |
| Expand/collapse | 200–300ms | ease-in-out |
| Fade in/out | 150–300ms | ease-in / ease-out |
| Slide panel | 200–400ms | ease-out / ease-in |
| Checkmark draw | 300–500ms | ease-out |
| Shake (invalid) | 300–500ms | oscillate |

Principles: purpose over decoration; interruptible (never make users wait for an animation); consistent timing; physics-based easing (ease-out enters, ease-in exits, ease-in-out stays-and-changes).

## Progress Indicators

Choose by load time:

| Load time | Indicator |
|-----------|-----------|
| <0.3s | none (would flash) |
| 0.3–1s | subtle inline spinner |
| 1–5s | skeleton screen |
| 5–30s | determinate progress bar |
| 30s+ | bar + % + time remaining + allow backgrounding |
| unknown | indeterminate spinner + status text |

## Audio (sparingly)

Appropriate for important confirmations (payment), attention-needing errors, background completions, accessibility — **not** every click, hover, or frequent action. Rules: short (50–200ms), quiet, distinct (success vs error obviously different), non-verbal, consistent across the product.

## Haptic (mobile)

Light tap = toggle/selection; medium = button/snap; heavy = significant confirmation; system patterns for success/warning/error. Always pair with visual (never replace it), match intensity to significance, use sparingly, and respect system haptic settings.

## Timing

| Delay | Perception | Needed |
|-------|-----------|--------|
| 0–100ms | instantaneous | visual state change |
| 100–300ms | responsive | transition, inline spinner |
| 0.3–1s | slight delay | loading indicator |
| 1–5s | waiting | spinner/skeleton |
| 5–30s | impatient | progress + estimate |
| 30s+ | will leave | progress + backgrounding + completion notice |

**Optimistic UI** — show the result immediately, reconcile on server response (like fills instantly; unfill + toast on failure). Use when success is ~certain, reverting is clear, and stakes are low. Avoid for high-failure, irreversible, or confusing-to-revert actions.

## Preventing Overload

Signs: users ignore toasts, "jittery" interface, disabled notifications, annoying sounds. Fixes: **consolidate** ("4 files uploaded", not four toasts), **batch** ("while you were away: 3 likes, 2 comments"), **tier by priority** (high = banner+sound+haptic; medium = toast; low = visual only), and reduce feedback during rapid sequential actions or when backgrounded.

## Accessibility

- Screen readers: `aria-live="polite"` for status, `"assertive"` for errors; loading gets `role="status"`; progress bars get `role="progressbar"` + `aria-valuenow/min/max`.
- Never color-only — pair with shape/text/icon; ≥3:1 contrast for state changes.
- Respect `prefers-reduced-motion` (swap animation for instant change); always pair audio with visual.

## Checklist
- Immediate visual feedback on every activation, proportional to significance
- Loading indicator for >300ms; progress bar for >10s
- Errors explain what + how to fix; success brief and non-blocking
- Animations <500ms and interruptible; audio optional; haptics respect settings
- All channels accessible (visual + ARIA + reduced-motion)
