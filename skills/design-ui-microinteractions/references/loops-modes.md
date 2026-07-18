# Loops & Modes

The long-term behavior of a microinteraction: how it evolves across repeated use (loops) and how the same trigger can mean different things in different contexts (modes). This is where interactions feel alive — or unreliable.

## Loops

The key question: what happens when it's triggered *again*?

| Type | Behavior | Ends when |
|------|----------|-----------|
| Open loop | repeats until stopped | user/system stops it (repeating alarm, auto-save) |
| Closed loop | runs fixed times/duration | completion condition met (countdown, 3-retry limit) |

**Open loops** — match frequency to need (auto-save every 30s, not every second), show status unobtrusively ("saved 2 min ago"), give control (toggle/frequency), minimize resource cost, degrade gracefully on a failed cycle.

**Closed loops** — show progress ("attempt 2 of 3"), signal completion clearly, allow early exit, define the end state, handle failure-to-complete.

## Long Loops (behavior over time)

The most neglected, most powerful lever: how should this behave on the 100th use vs the 1st?

**Progressive reduction** — remove scaffolding as mastery grows:

| Uses | Behavior |
|------|----------|
| 1–3 | full labels, tooltips, coaching |
| 4–10 | labels stay, tooltips gone |
| 11–50 | labels shrink to icons |
| 50+ | icons only, shortcuts promoted |

Drive it by use counter, time since first use, detected competence, or explicit "don't show again."

**Adaptive loops** — smart defaults (default to the team you write to most), frequency adjustment (fewer notifications after 5 ignored), content personalization, complexity scaling, suggestion refinement.

Principles: never degrade core function (remove scaffolding, not features); always provide a way back to hidden help; track per-feature not globally; keep adaptation either invisible (smart defaults) or transparent (explicit suggestions) — half-visible feels creepy; **test the 100th use**, not just the first.

## Modes

A mode is a temporary state where the same trigger produces a different result. Powerful but dangerous.

Dangers: **mode error** (right action, wrong mode — typing with Caps Lock on), **mode confusion** (which mode am I in?), **mode amnesia** (forgot I'm in Do-Not-Disturb), action inconsistency.

Justified when: physical input constraints (limited keys), genuine separation of concerns (edit vs view vs suggest), safety (protect published content), or distinct tool sets (brush vs eraser).

Guidelines:
1. **Make the active mode unmistakable** — color-coded background, persistent banner, tool indicator, or status label.
2. **Deliberate transitions** — enter/exit by conscious action, never by hover/proximity.
3. **Minimize count** — every mode multiplies testing surface; 1 is ideal, 2 acceptable, 3 reconsider, 4+ redesign.
4. **Always-visible escape** — explicit "Done" button, Esc key, timeout, or dismiss gesture.

## Avoiding Mode Errors

Strategies: **spring-loaded modes** (exist only while a trigger is held — Shift for uppercase, Space for Quick Look preview; the held action prevents amnesia), undo-on-exit, entry confirmation, preemptive warnings ("you're in eraser mode"), or eliminate the mode entirely (per-field inline editing instead of a global "edit mode").

## Loop × Mode Combinations

A mode can suppress a loop (Do-Not-Disturb silences the notification loop), a loop can trigger a mode (3 failed logins → locked), a mode can change loop frequency (Focus mode → hourly instead of real-time), a loop can exit a mode (inactivity → sleep).

## Checklist
- Open vs closed is the right choice; open loops are controllable; closed loops show progress and completion
- Long-loop behavior designed (1st / 10th / 100th use); progressive reduction with a way back
- Every mode is necessary, visible, deliberately entered, and has an always-visible exit
- Tested for mode errors; considered spring-loaded instead of toggle; total modes ≤3
