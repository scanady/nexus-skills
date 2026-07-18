# The Two Gulfs

Every human–product interaction crosses two chasms. The **Gulf of Execution** separates what the user wants to do from the actions the product requires ("how do I do this?"). The **Gulf of Evaluation** separates what the product did from the user's understanding of it ("what happened?"). Narrowing both is the central job of interaction design.

## Gulf of Execution

Exists whenever a user has a goal but can't figure out how to achieve it.

**Widens it:** hidden controls (gesture with no indicator), unfamiliar vocabulary ("Reconcile ledger" vs "Match payments"), non-obvious multi-step sequences, mismatched mappings (identical switches for different zones), missing affordances (clickable text with no cue).

**Narrows it:** clear signifiers (`"Search by name or email…"`), natural mappings (vertical volume slider, up = louder), constraints (date picker blocks invalid dates), familiar patterns (cart top-right), progressive disclosure (payment fields appear after Checkout).

Common offenders — web: desktop hamburger menus, icon-only toolbars, right-click-only actions, shortcut-only features. Mobile: gesture-only navigation, hidden bottom sheets, long-press menus. Physical: push-plates on pull doors, stove knobs in a row for a burner grid.

## Gulf of Evaluation

Exists whenever the user acted but can't tell what happened, whether it worked, or what state the system is now in.

**Widens it:** no feedback, delayed feedback, ambiguous feedback (a number changed with no explanation), hidden state (silent background sync), technical error text ("Error 0x80070005").

**Narrows it:** immediate feedback (<100ms), persistent state indicators ("Draft"/"Published"), progress communication ("Step 3 of 5"), clear errors ("That email is already registered — try logging in"), meaningful transitions (deleted item slides to trash).

Offenders — silent auto-saves (no "Saved"), pagination with no count, unindicated background processing, form submit with no redirect/toast; kiosks that accept input with no confirmation so users re-submit.

## Estimating Gulf Width

| Width | Execution | Evaluation |
|-------|-----------|------------|
| Narrow | first-attempt success, no hesitation | immediately understands the result |
| Medium | pauses, scans, then finds it | notices a change, briefly interprets it |
| Wide | tries wrong actions first, or gives up | unsure it worked; repeats or re-checks |
| Very wide | can't complete without external help | no idea what happened; abandons/support |

## Patterns

**Widen execution:** mystery-meat navigation, modes with no indicator, menus nested past two levels, inconsistent action locations, hiding scrollbars. **Widen evaluation:** toasts that vanish in <2s, silent failures, optimistic UI that never corrects, near-identical on/off states, aggregate status with no breakdown.

**Narrow execution:** labeled toolbars, contextual/inline actions, command palettes, first-run spotlights, consistent layout grids. **Narrow evaluation:** persistent status bars, inline validation, undo toasts with timers, state-change animations, confirmation/summary screens.

## Analysis Template

For a chosen task, attempt it as a new user and score 1–5 each:
- **Execution** — can the user identify available actions? are the right controls visible? familiar patterns/vocabulary? clear mapping? invalid actions constrained? obvious sequence?
- **Evaluation** — immediate feedback? current state determinable? feedback informative? errors clear with recovery? goal-achievement confirmable? transitions visible?

At every hesitation, note which gulf is too wide, rate severity, and propose a fix. Conclude which gulf is the bigger problem for this task.
