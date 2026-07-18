# Case Studies

Norman's principles applied to real products, physical and digital. The same small set of principles explains why a product is intuitive or infuriating.

## 1. The Norman Door — affordances, signifiers, constraints
A flat plate affords pushing; a handle affords pulling. A handle on the push side contradicts the required action, so the "Push" sign is a band-aid for a broken affordance. The deeper failure is a missing constraint. **Fix:** flat plate on the push side (affords only pushing), vertical handle on the pull side — or automatic doors. **Lesson:** when users consistently do the wrong thing, the design is wrong; the cheapest fix (a sign) is the weakest.

## 2. The Thermostat — conceptual models
Users set 90° expecting faster heating; the system heats at a constant rate to a target. They apply a "valve" model because the system image shows only the target number. **Fix:** show current *and* target, a "Heating to 72…" indicator, and estimated time. **Lesson:** consistent misuse means the system image is failing to communicate the model — make the mechanism visible, don't rely on manuals.

## 3. Stovetop Burners — mappings
Four burners in a 2×2 grid, four knobs in a row → no natural mapping, so users read labels or guess. **Fix:** arrange knobs in a matching 2×2 or adjacent to each burner. **Lesson:** natural spatial mapping removes the need for labels, memory, and guesswork.

## 4. Cockpit Mode Errors — feedback, signifiers, conceptual models
Autopilots have dozens of modes; tiny annunciations and silent automation transitions cause mode confusion (implicated in real accidents). **Fix:** large color-coded mode displays, alerts on (especially uncommanded) mode changes, fewer/simpler modes, consistent behavior. **Lesson:** modes must be visible and mode changes unmissable — the more modes, the more likely users lose track.

## 5. Hospital Medication Errors — constraints, signifiers, feedback, mappings
Look-alike drug names, free-text dose entry (a 10× error uncaught), unlocked units, alert fatigue (90%+ overridden), dense flat lists. **Fix:** Tall Man lettering (hydrOXYzine vs hydrALAzine), dose-range validation, pre-set dose dropdowns, tiered alerts (reserve modals for true contraindications), visual grouping. **Lesson:** in high-stakes settings, constraints are the most important tool — prevent, don't detect; alert fatigue is a feedback failure.

## 6. ATM Evolution — mapping through direct manipulation
1980s unlabeled buttons beside cryptic menus (arbitrary mapping, high errors) → 1990s labeled buttons adjacent to items → 2010s touchscreens (tap the option itself). **Lesson:** direct manipulation — acting on the thing itself — is the best possible mapping.

## 7. Smartphone Unlock Evolution — affordances, constraints, feedback
Slide-to-unlock (arrow + track, springs back) → PIN/pattern → fingerprint (haptic, PIN fallback) → face (ambient, padlock animation). Each generation cut execution-gulf friction while keeping evaluation clear and security intact. **Lesson:** as technology improves, constraints can hold while affordances become invisible — the best interface approaches no interface.

## 8. Smart-Home Lighting — conceptual models, mappings, affordances
"Turn on the kitchen light" now spans wall switch, app, voice, hub, and automations. A wall switch that cuts power to a smart bulb breaks the user's model; multiple control points create state ambiguity ("is it off because of the switch, app, schedule, or no power?"). **Fix:** single source of truth, switches that send commands (not cut power), always-visible state, fallback to the simple physical switch. **Lesson:** adding "smart" to a simple product undermines its simplicity unless every control point integrates with one model.

## Cross-Cutting Patterns

**Intuitive** = direct manipulation, spatial correspondence, visible system state, physical constraints, immediate feedback, familiar metaphors. **Confusing** = hidden modes, arbitrary mapping, silent failures, conflicting affordances, broken metaphors, alert fatigue.

**The universal fix** — six questions, each naming a principle and its solution:
1. Can the user see what actions are possible? *(affordances, signifiers)*
2. Which control affects which outcome? *(mappings)*
3. Can they avoid errors? *(constraints)*
4. Can they see what happened? *(feedback)*
5. Do they understand how it works? *(conceptual model)*
6. Can they recover from mistakes? *(error tolerance)*

Any "no" identifies both the problem and the category of fix.
