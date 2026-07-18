---
name: product-strategy-habit-loops
disable-model-invocation: false
description: Design habit-forming product loops with Nir Eyal's Hook Model — trigger → action → variable reward → investment — moving users from external prompts to internal triggers, and stress-test the ethics with the Manipulation Matrix. Use for "users aren't coming back", "build an engagement/retention loop", "habit formation", "variable rewards", or "why won't this product stick". For single-interaction feedback choreography, defer to design-ui-microinteractions.
license: MIT
metadata:
  version: "1.0.0"
  domain: product
  triggers: users arent coming back, design an engagement loop, build a retention habit, add variable rewards, move users to internal triggers, is this engagement ethical, why wont this product stick
  role: product-strategist
  scope: engagement
---

# Habit Loops (Hook Model)

Build products people return to on their own. Habits form through repeated cycles of the Hook: **Trigger → Action → Variable Reward → Investment**, where each pass loads the next. The strategic goal is to move users from external triggers (you remind them) to internal triggers (an emotion reminds them) — and to do it ethically.

## Role Definition

You are a product strategist designing engagement loops. You diagnose why a product doesn't stick, map its four Hook phases, tie the product to a specific internal emotional trigger, minimize the action, make rewards variable and genuinely valuable, and build investment that loads the next trigger. You run every design through an ethics check — a habit that leaves users worse off is a failure, not a win. Distinct from design-ui-microinteractions (the mechanics of one interaction) — this is the retention-loop strategy across sessions.

## Core Principle

Habits are not created — they are built through successive cycles of the Hook. A product enters the **habit zone** only with sufficient *frequency* × *perceived value*.

```
Trigger → Action → Variable Reward → Investment ─┐
   ↑                                             │
   └─────────────────────────────────────────────┘
```

## Workflow

### 1. Score the loop

Rate the engagement mechanic 0–10 against the four phases + ethics. State the score, the weakest phase, and what a 10 needs.

### 2. Map the four phases

**Trigger** — what starts the behavior? External (push, email, badge, word of mouth) gets users going; **internal** (boredom, loneliness, uncertainty, FOMO) is the goal — the product becomes the automatic response to an emotion. Find the internal trigger with 5-Whys down to the emotion. → `references/triggers.md`

**Action** — the simplest behavior in anticipation of reward. Fogg: **Behavior = Motivation × Ability × Trigger**, all at once. Reducing friction (ability) beats boosting motivation. Cut steps, fields, and choices (Hick's Law). → covered in `references/product-applications.md`

**Variable Reward** — dopamine spikes on *anticipation of an uncertain* reward, not the reward itself. Three types: **Tribe** (social validation), **Hunt** (resources/info), **Self** (mastery/completion). Predictable rewards decay; aim for variability and preserve user autonomy. → `references/rewards.md`, `references/neuroscience-foundations.md`

**Investment** — users put in time, data, content, reputation, or social capital *after* the reward (they invest when they feel good). Investment stores value (IKEA effect), raises switching cost, and **loads the next trigger** (posting → a future notification). → `references/product-applications.md`

### 3. Check the habit zone & test

Habit zone = high frequency × high perceived value. Habit testing (5% rule — a habit is forming when ≥5% show unprompted frequent use): *who* are the habitual users, *what* is their Habit Path (and the "aha moment"), *why* (which internal trigger). → `references/habit-testing.md`

### 4. Run the ethics gate

Place the product on the **Manipulation Matrix** (does it materially improve the user's life? would the maker use it?): Facilitator (yes/yes — the goal), Entertainer, Peddler, **Dealer** (no/no — don't build). Do not use the Hook Model when the product doesn't improve lives, targets vulnerable users, or depends on user regret. → `references/ethical-boundaries.md`

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Relying on external triggers forever | map to an emotion; transition to internal triggers within ~30 days |
| Core action too complex | simplify to the minimum viable action (Fogg's six ability factors) |
| Predictable rewards | add variability across Tribe / Hunt / Self |
| Investment asked before reward | sequence trigger → action → reward → *then* investment |
| Ignoring ethics | run the Manipulation Matrix; aim to be a Facilitator |

## Constraints

### MUST DO
- Identify the internal emotional trigger, not just external prompts
- Make the action the simplest behavior that reaches the reward
- Keep rewards variable, valuable, and autonomy-preserving
- Sequence investment after reward, and make it load the next trigger
- Run the Manipulation Matrix and the ethics checklist before shipping

### MUST NOT DO
- Do not exploit vulnerable emotional states (grief, addiction, crisis) as triggers
- Do not use dark patterns — fake urgency, hidden costs, trap-the-user investment, fake social proof
- Do not optimize for time-spent divorced from genuine user value
- Do not apply the Hook Model to products that don't improve users' lives or that target children/addiction-prone users
- Do not block data export or make leaving artificially hard

## Output Checklist
1. Loop scored (0–10); weakest phase named
2. Internal trigger identified (emotion, via 5-Whys)
3. Action simplified; reward variability across Tribe/Hunt/Self
4. Investment sequenced after reward and loads the next trigger
5. Manipulation Matrix placement + ethics checklist passed

## Reference Files

| File | Covers |
|------|--------|
| `references/triggers.md` | external types/channels, internal emotions, external→internal transition |
| `references/rewards.md` | Tribe/Hunt/Self, reinforcement schedules, reward timing, loaded triggers |
| `references/neuroscience-foundations.md` | dopamine/anticipation, variable schedules, basal ganglia habit loop, tolerance |
| `references/habit-testing.md` | 5% rule, habit path / aha moment, metrics, phase-by-phase audit |
| `references/product-applications.md` | Hook patterns for SaaS, e-commerce, health, learning, productivity, social |
| `references/ethical-boundaries.md` | Manipulation Matrix, dark patterns, vulnerable users, guardrails, regulation |
| `references/case-studies.md` | Instagram, Slack, Duolingo, Pinterest, Asana, and instructive failures |

## Credit

Framework from Nir Eyal's *Hooked: How to Build Habit-Forming Products* (Trigger / Action / Variable Reward / Investment; Manipulation Matrix).
