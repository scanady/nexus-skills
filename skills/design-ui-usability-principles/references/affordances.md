# Affordances

An affordance is a relationship between an object's properties and a user's capabilities that determines how it *could* be used — a chair affords sitting, a button affords pressing. Affordances exist whether or not they're perceived; the design challenge is aligning **real** affordances (what the system supports) with **perceived** ones (what the user believes) so every real affordance is perceived and no false one exists.

## Types

| Type | Definition | Example |
|------|-----------|---------|
| Real | genuinely supported action | a button can be pressed; an input accepts keystrokes |
| Perceived | user believes it's possible | a raised, shadowed rectangle looks pressable |
| Hidden | exists but not visible | right-click menu, trackpad gesture |
| False | appears to afford but doesn't | underlined non-link text; a shadowed non-clickable card |
| Anti-affordance | deliberately prevents action | grayed-out disabled button; a guardrail |

## Digital Patterns

Manufacture every affordance through visual design (physical objects get theirs free from material):
- **Buttons** — raised/shadow/color + hover + active + disabled states.
- **Links** — color + underline + pointer cursor + visited state (two signals minimum).
- **Inputs** — visible border, placeholder, focus ring, blinking cursor, label.
- **Sliders** — handle + track + fill + min/max labels.
- **Drag targets** — grip icon, grab cursor, lift-on-drag, drop-zone highlight.

Rules: every interactive element gets deliberate visual treatment; non-interactive elements must look distinct from interactive; new patterns (gestures, voice) start with zero perceived affordance and need onboarding.

## The Flat-Design Problem

Removing skeuomorphic cues (shadows, borders, underlines, gradients, depth) creates a systematic affordance crisis — buttons look like labels and vice versa. Recover with: color contrast for interactive vs static, hover/focus states, consistent clickable regions, subtle shadows/borders (flat ≠ zero depth), cursor changes, icon+label pairing.

## Touch vs Mouse

| Factor | Mouse | Touch |
|--------|-------|-------|
| Hover | available, essential | none — can't preview interactivity |
| Precision | high (pixel) | low (~44px finger) |
| Right-click / cursor feedback | yes | none |
| Min target | ~24px | 44×44pt (iOS) / 48×48dp (Material) |

Touch strategy: targets ≥44×44pt; use size/color/shadow (not hover) to signal interactivity; haptic feedback replaces the mouse click; always give gestures a visible alternative; hint at swipeable content (peek next card, dots).

## Accessibility

Visual affordances are invisible to some users — provide **semantic** ones: correct ARIA roles / native HTML for every interactive element; visible high-contrast focus rings (the keyboard equivalent of hover); operable via keyboard; never color-only (add shape/border/icon); adequate target size; a non-drag alternative for every drag interaction.

## Audit

Interactive: every button/link/input/slider/drag-handle is visually distinguishable and adequately sized. Non-interactive: static text isn't link-colored; decorative elements have no pointer/hover. Hidden: gestures/shortcuts/right-click have visible alternatives or documentation. False: no underlined non-links, no shadow/hover/pointer on non-interactive elements.

**Before → after examples:** flat "Submit" label → filled blue button with hover; hamburger-only nav → visible labeled nav + "More"; thin underline input → bordered field with label + focus ring; swipe-only delete → swipe *plus* a visible trash icon.
