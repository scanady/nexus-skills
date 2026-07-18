# Trigger Design

The trigger is what starts a microinteraction — the entry point. Two kinds: **manual** (the user deliberately acts) and **system** (a condition is met and the product acts). A trigger's quality decides whether users can even discover and initiate the interaction.

## Manual Triggers

Live inside UI controls — buttons, switches, icons, fields, gestures, voice.

| Type | Best for | Example |
|------|----------|---------|
| Tap/click | most actions | submit, checkbox |
| Long press | secondary/preview | context menu, Haptic Touch |
| Swipe | spatial / destructive | swipe-to-delete |
| Drag | reorder, adjust | slider, list reorder |
| Double-tap | quick positive | double-tap to like |
| Type | search, entry | search-as-you-type |
| Voice | hands-free | "set a timer" |

Design principles:
- **Affordance clarity** — it looks like what it does (a toggle looks slideable).
- **Verb labels** — "Save"/"Send"/"Delete" beat vague "Submit"/"OK".
- **Touch targets** — ≥44×44pt (iOS) / 48×48dp (Android); desktop ≥24px with generous padding.
- **Convention placement** — primary bottom-right (mobile FAB) or top-right (desktop toolbar); destructive separated at menu bottom; search top.
- **Discoverability tiers** — always-visible (primary), on hover/focus (secondary), on gesture (tertiary), keyboard-only (expert).

## System Triggers

Fire automatically when a condition is met: **time** (alarm, timeout), **threshold** (low battery at 20%), **data** (new message), **location** (geofence), **state-change** (sync complete), **error** (validation fail), **inactivity** (screen dim).

Design principles:
- **Relevance over frequency** — fire only when genuinely useful now; every needless notification trains users to ignore triggers.
- **Threshold calibration** — not too early, not too late (battery warning at ~20%, not 50% or 2%).
- **Escalation** — passive badge → active banner → blocking alert as importance rises.
- **Silencing** — global Do-Not-Disturb, per-category mute, quiet hours.

## Trigger States

Every manual trigger must be distinguishable across states.

| State | Treatment |
|-------|-----------|
| Default | ready appearance |
| Hover (desktop) | subtle change on proximity |
| Active/pressed | depression or color shift, instant |
| Disabled | reduced opacity, `not-allowed`, reason on hover |
| Loading | spinner replaces label |
| Focus | visible ring (keyboard) |
| Selected/on | filled/checked/colored |
| Error / Success | red border / brief green check |

Transition timing: hover ~50ms ease-out; press instant; loading→success/error 200–400ms ease-in-out; anything→disabled ~150ms.

## Invisible Triggers

Gesture/sensor triggers have zero discoverability — powerful but risky. Appropriate only as a *shortcut* to something also reachable visibly, for power-user acceleration, or platform-standard gestures (pinch-zoom). Never the sole path to a feature or to a destructive action. Make them learnable via one-time coaching, partial reveal (peek the delete background), contextual hints when the user stalls, and reliable behavior with undo.

## Placement & Fitts's Law

Reach time ∝ distance ÷ target size. So: corners/edges are fast on desktop (cursor stops there); the bottom third is the mobile thumb zone; larger triggers are faster; group sequential triggers to cut travel. Grouping patterns: toolbar (peer actions), action group (primary + secondary), contextual menu (many actions on one object), FAB-with-expansion, inline actions.

## Audit Checklist
- First-timer finds it in <5s; looks interactive; verb-labeled; correctly sized
- Default/hover/active/disabled/loading all distinguishable; disabled explains why
- Placed per platform convention; primary more prominent than secondary
- Double-activation, activation-during-loading, slow-connection, and navigate-away all handled
