# Signature Moments

A signature moment is a microinteraction so distinctive it becomes inseparable from the product's identity — slide-to-unlock, Slack's loading messages, Stripe's payment checkmark. Not features; feelings encoded in tiny interactive moments. Most microinteractions are not signature moments, and shouldn't be.

## What Makes a Moment "Signature"

Six criteria, all required:

| Criterion | Test |
|-----------|------|
| Memorable | users describe it unprompted |
| Frequent | encountered ~weekly+ |
| Distinctive | recognizable from this moment alone |
| Functional | removing it makes the experience worse, not just plainer |
| Brand-aligned | consistent with the product's personality |
| Effortless | adds delight without friction or delay |

Spectrum: functional-only → polished → distinctive → signature. Aim most interactions at "polished"; invest signature effort in 2–3 places total.

## Why the Iconic Ones Work

- **Facebook reactions** — long-press trigger (discoverable, not obtrusive); spring-physics float; each reaction its own character; matches a social, expressive brand.
- **iPhone slide-to-unlock** — the label explains the gesture; direct manipulation with a full-slide constraint (no pocket unlocks); elegant, tactile, on-brand.
- **Slack loading messages** — turns dead startup time into a brand moment; variable copy stays fresh across hundreds of loads; perceived wait shrinks because users are reading.
- **Stripe payment success** — a checkmark that draws itself after a deliberate pause (anticipation → reward); turns payment anxiety into relief; communicates craft/reliability.
- **GitHub 404** — a parallax Octocat turns a frustrating error into something users share, while keeping navigation/search intact.

## Where to Invest (and Not)

High-opportunity, low-risk: loading/waiting states, success confirmations, empty states. Higher-risk but high-payoff: onboarding first action, the primary product action (must add zero friction), error states (must still communicate the error). Avoid signature investment on settings, forms/data entry, administrative actions, error-recovery flows, and background processes — there, prioritize speed and clarity.

## Designing Your Own

1. **Find candidates** — score every interaction on frequency × emotional charge; high/high is the prime candidate.
2. **Match brand personality** — three adjectives, filter every decision (playful → illustration/humor; professional → clean, subtle; bold → dramatic; calm → slow, quiet).
3. **Choose the medium** — animation, microcopy, sound, illustration, or haptics (weigh performance, translation, asset cost, platform support).
4. **Prototype and test at 1st / 10th / 100th use** — delightful at first, not annoying at ten, invisible/non-blocking at a hundred. Then the removal test.

## Everyday Delight (no grand gesture needed)

Personality in copy ("We looked everywhere but came up empty"), physics-based easing (a toggle that settles with a slight bounce), contextual response, progressive reveal, meaningful transitions (new item slides in from the Add button), one intentional signature sound.

**Delight vs distraction** — before adding it, confirm it adds no friction, won't annoy at 100 uses, doesn't delay the task, works on slow devices/connections, respects accessibility settings, and needs no cultural context.

## When to Invest

MVP/early: ~zero (get the basics right). Post product-market-fit: experiment with 1–2. Growing: 2–3 true signature moments. Mature: maintain and refresh so they don't go stale.

**The "would they miss it" test** — remove it: if users complain, it's signature; if they vaguely sense a change, it's a nice detail; if no reaction, it was decoration (consider cutting it).

## Pitfalls
- Delight that delays the critical path
- Trying too hard (everything "delightful" → sensory overload; cap at 2–3)
- Cultural blind spots in humor/imagery
- Relying on vision/motion/hearing without an accessible baseline
- Stale moments (rotate variable content; refresh periodically)
- Copying another product's moment instead of growing your own
