# Feedback

Feedback is what a system sends back after an action. Without it users operate in the dark — unsure if the action registered, succeeded, or what state the system is in. Absent feedback is one of the most common and damaging failures: **every action must produce a perceivable response.**

## Channels

- **Visual** (primary, works for nearly everything) — color change, animation, icon change, text update, position change, opacity.
- **Auditory** — confirmation tone, error sound, notification chime, typing clicks. Always mutable; never the sole channel (accessibility); supplements visual.
- **Haptic** (touch devices) — tap confirmation, selection pulse, error double-buzz, boundary feedback, success pulse. Pair with visual.
- **Progress** — determinate bar (known duration), indeterminate spinner (unknown), skeleton screen, percentage text, step indicator, elapsed-time counter.

## Response-Time Thresholds

| Delay | Perception | Required feedback |
|-------|-----------|-------------------|
| 0–100ms | instantaneous | direct visual change; no indicator |
| 100ms–1s | responsive but "thinking" | cursor change / subtle animation |
| 1–10s | attention wanders | spinner / progress indicator |
| 10–60s | may switch tasks | progress bar + %/estimate; allow backgrounding |
| >60s | may assume failure | progress + elapsed + remaining; notify on done |

## Patterns by Interaction

- **Click/tap** — hover → active (pressed) → loading → success (check/green) → error (shake/red).
- **Form submission** — inline per-field validation → button loading (inputs disabled) → success toast/redirect → partial-success warning → failure with inline errors, **input preserved**.
- **Drag & drop** — lift on start, drop-zone highlight on valid target, not-allowed on invalid, animate to position on drop, animate back on cancel.
- **Errors** — say what happened, why (if helpful), how to fix, and an alternative; place near the source; preserve work; match severity (red=block, yellow=warn, gray=hint); never blame the user.

Error message template: `[icon] what happened → why → how to fix → [alternative action]`. Success: toast (non-critical), inline banner (forms), full-screen (milestones), redirect-with-flash, subtle state change, or email/notification (background).

## Too Much vs Too Little

- **Too little** — click with no change (→ duplicate clicks), silent submit, invisible background save, silent errors, long process with no progress. Fix: add a perceivable response to every action; show progress for anything >1s.
- **Too much** — a dialog for every action (→ dialog blindness), sound on every click, animation on every change, redundant multi-channel notifications. Fix: reserve dialogs for critical confirmations; match feedback prominence to action importance (critical→modal, important→toast, routine→subtle state change, ambient→tiny indicator).

## Accessibility

Screen readers: `aria-live` regions for dynamic updates, `role="alert"` for errors, progress announcements, focus moves to new messages. Keyboard: visible focus, focus moves to resulting content. Low-vision: color paired with icon/text, WCAG 4.5:1. Motion-sensitive: `prefers-reduced-motion` alternatives.

## Audit

Presence: every clickable element responds <100ms; every submission gives explicit success/error; every >1s operation shows loading; errors are human-readable with remediation. Timing: inline validation ~300ms after typing stops; spinners within 1s; toasts auto-dismiss 4–8s with manual control; background ops notify on completion. Content: errors say what/why/how; success confirms what was done; state (saved/unsaved, connected, mode) always visible.
