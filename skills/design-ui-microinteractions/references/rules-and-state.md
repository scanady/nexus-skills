# Rules & State

Rules are the invisible engine: once triggered, they decide what changes, in what order, under what constraints, and when the interaction ends. Users never see rules — they feel them when a toggle forgets its position or a form erases their input.

## What Rules Define

What happens first → the sequence → what the user can do during → what they cannot → the boundaries (min/max/default) → the end condition → the failure behavior.

## Goal-First Method

Start from the goal, not the interface:
1. State the goal in one sentence ("set an alarm time").
2. Identify minimum inputs.
3. Define the simplest happy path.
4. Add constraints (no alarm in the past; max 20).
5. Handle failures (permission denied → error + fix action).
6. Define the end state (alarm set, confirmed, listed).

**Rule complexity scales inversely with frequency.** Many-times-a-day actions get near-zero configuration (one-tap like); once-ever actions can afford a full setup flow (account creation).

## State

Core states every interaction moves through: **idle → active → success / error**, plus **partial** and **disabled**. Users must always know which state they're in. Map every transition so no combination is missed (idle→active→success/error; error→retry; success→timeout→idle; any→cancel→idle).

**Persistence** — pick the right scope:

| Scope | Survives | Use for |
|-------|----------|---------|
| Ephemeral | within session | hover, open/closed |
| Session | navigations | form progress, scroll pos |
| Persistent | app close | theme, preferences |
| Synced | across devices | read/unread, bookmarks |

## Constraints (prevent, don't punish)

The best constraint is one the user never hits because the wrong action was impossible.

| Punishing (bad) | Preventing (good) |
|-----------------|-------------------|
| "Invalid date" after typing | date picker allowing only valid dates |
| "Username taken" after submit | real-time availability check |
| "File too large" after upload | show limit upfront; disable oversized |
| "Can't pick past date" error | gray out past dates |

Constraint types: range, format, type, sequence, dependency, capacity, temporal. Communicate them via disabled states, counters ("23/280"), visual boundaries, inline hints, and progressive disclosure.

## Error States

1. **Preserve the user's work** — never wipe input on error.
2. **Human language** — "That email looks incomplete — missing the domain?" not "Error 422".
3. **Point to the source** — inline by the field, not a top banner.
4. **Offer a path forward** — every error suggests a fix.
5. **Time it right** — format errors on blur; cross-field errors on submit.

Error taxonomy: format, missing-required, range, conflict, system, permission, timeout — each with its own detection timing and display. Recovery patterns: inline correction, undo, retry, suggestion ("Did you mean…?"), fallback, graceful partial completion ("3 of 5 uploaded").

## Edge Cases

Ask "what happens when…?" for: empty state, zero value ("No notifications", not "(0)"), maximum reached, rapid repeated trigger (debounce/disable), interruption mid-action, slow connection, offline (queue), concurrent edit (conflict), very long input, special characters, screen-reader users, keyboard-only users. Test boundaries at 0/1/max-1/max/max+1; test instant vs 3s vs 30s; test 10 rapid triggers; test the slowest device.

## What NOT to Allow

Prevent: double submission (disable on first click + debounce), delete-without-confirm, submitting invalid data, exceeding rate limits, conflicting selections (depart after arrive), accidental mode entry. Some activations should deliberately do nothing (disabled button click, empty required submit) — pair "nothing happens" with an explanation.

## Checklist
- Every state defined and visible; every transition mapped
- What's *not* allowed is defined
- Constraints prevent rather than punish; input preserved on error
- Error messages human, specific, actionable
- Edge cases (empty/max/rapid/offline/interrupted) tested
- Persistence scope appropriate; state changes reach screen readers
