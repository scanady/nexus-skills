# Case Studies

Five common patterns broken down through the four-part structure (Trigger · Rules · Feedback · Loops & Modes) plus edge cases and accessibility. Use these as blueprints.

## 1. Form Submission

High-stakes — users have invested time and data.

- **Trigger** — "Submit" button (primary); Enter in last field (convention); auto-save draft after 30s idle (system).
- **Rules** — validate required fields client-side first; on failure, block and scroll to first invalid field; on pass, disable button + loading; send; on 200 show success + redirect/reset; on 4xx/5xx show error and **preserve all input**; on >15s timeout offer retry with input preserved.
- **Feedback** — idle "Submit" → "Checking…" → inline field errors → "Submitting…" spinner → green check "Done" → red banner on server error (button re-enabled) → yellow "connection lost, saved locally" on network error.
- **Loops & Modes** — auto-save draft to local storage (open loop); after 3+ submissions hide optional hints (long loop); no modes.
- **Edge cases** — double-click (disable + debounce), navigate-away (unsaved-changes dialog + draft), session expiry (queue + re-auth), 20+ fields (section validation), pasted formatting (strip), autofill (accept + re-validate).

## 2. Toggle / Switch

Binary, deceptively simple.

- **Trigger** — tap track or thumb; Space when focused; drag thumb; external system state change.
- **Rules** — start transition immediately; if server-backed, send in background; toggling on may reveal settings; toggling off may confirm destructive change; on server rejection revert with error; debounce rapid toggling to the final state only.
- **Feedback** — thumb left/gray (off) → sliding → thumb right/green (on) with a light haptic; disabled = faded; loading = faded + inline spinner; error = flash red, revert.
- **Animation** — thumb + track 150–200ms ease-in-out synchronized; revert 200ms with red flash.
- **Accessibility** — `role="switch"` + `aria-checked`; Space toggles (not Enter); SR announces "label, switch, on"; skip animation under reduced motion; ≥44×44pt target.
- **Loops & Modes** — no loop; first 3 toggles may show a feature tooltip (long loop); no modes.

## 3. Pull-to-Refresh

Gesture-triggered, invisible affordance.

- **Trigger** — pull down past ~60pt at list top (the gesture *is* the trigger); system fallback auto-refresh on foreground after X minutes.
- **Rules** — active only at scroll top; below threshold shows a hint but doesn't fire; past threshold "locks"; release past threshold refreshes; release before snaps back; keep spinner ≥500ms (no flash); rate-limit if last refresh <5s ago.
- **Feedback** — 0–20pt rubber-band; 20–60pt spinner appears, rotating with pull; at threshold spinner completes + light haptic; on data new items slide in and the area collapses; on error brief "Could not refresh".
- **Discoverability** — zero visible affordance, so for unfamiliar audiences add hint text (remove after 3 successes), auto-refresh on first load, and keep a visible refresh button as a permanent fallback.
- **Platform** — iOS `UIRefreshControl`, Android `SwipeRefreshLayout`, web custom (`overscroll-behavior: contain` to avoid the browser's own pull-to-refresh).

## 4. Loading States

A family of "the system is working" patterns. Selection is by duration (see the table in `feedback-patterns.md`).

- **Skeleton screens** — show within 100ms; shapes match the final layout exactly; subtle pulse (opacity 0.3→0.6, ~1.5s); load text before images; crossfade to content (200ms); never skeleton cached content.
- **Progress bars** — appear within 200ms; **real** progress only; never go backward (pause if it would); reserve the last ~5% for server confirmation; fill to 100% then success.
- **Accessibility** — `aria-live="polite"` announces load start/end; `role="progressbar"` with value attributes; under reduced motion swap pulse/spinner for static "Loading…"; after 30s announce "still loading — wait or try again".

## 5. Notifications (Toast / Snackbar)

Transient, must not demand full attention.

- **Trigger** — system events (save/send/delete complete, incoming data, error) or a user action with a reversible outcome (delete → "Undo" toast).
- **Rules** — consistent position; stack max 3, queue the rest; auto-dismiss informational after 5–8s but **persist errors** until acknowledged; slide in 300ms / out 200ms; never cover primary actions; keep an "Undo" action available for the whole display window; dismissable by swipe/close.
- **Feedback** — color + icon by type: success (green/check), info (blue), warning (amber, 8s), error (red, persist, "Retry"), undo (dark, 8s, "Undo").
- **Loops & Modes** — stack/queue loop; consolidate repeats ("3 files uploaded" not three toasts); no modes.
- **Accessibility** — `role="status"`/`aria-live="polite"` for info, `role="alert"`/`"assertive"` for errors; don't steal focus; Esc dismisses; pause auto-dismiss timer on hover/focus; fade instead of slide under reduced motion.
- **Edge cases** — 10 at once (queue, dismiss oldest), covering a primary action (reposition), last-second Undo (honor within window), full-screen overlay (higher z-index), long text (2-line clamp + "Show more"), offline Undo (queue locally, run on reconnect).

## Cross-Cutting

Patterns that recur across all five: **debouncing** (prevent duplicate triggers), **optimistic UI** (show result before server confirms, for low-stakes reversible actions), **progressive disclosure** (summary first, detail on demand), **graceful degradation** (works without JS/animation/haptics), an **accessibility baseline** (ARIA, keyboard, reduced motion, screen reader), and **state persistence** (drafts, scroll position, toggle state survive interruption).
