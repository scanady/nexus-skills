# Description & Trigger Optimization

How to write skill `description` fields and `metadata.triggers` that activate reliably, avoid collisions with neighbor skills, and stay discoverable. Use alongside `description-optimizer.md` (agent) and `metadata-fields.md` (per-field rules).

The description and triggers are the **only** signals the router sees before loading a skill. Everything else — body, references, agents — is invisible at routing time. Treat them as a retrieval problem, not a documentation problem.

---

## Core Principles

### 1. One Skill = One Semantic Core

Every skill must have a single, compressible "semantic core" — a phrase a user could say that uniquely identifies this skill versus every neighbor in the library. If you cannot state it in 5–10 words, the skill is either too broad, duplicating another skill, or merging two skills.

Write the core before the description. Example cores:
- `skill-architect` → "build or review an Agent Skill file"
- `skill-evaluator` → "run eval suites against a skill and iterate"
- `content-copy-caveman` → "rewrite prose in ultra-compressed caveman style"

Test: if the core phrase could plausibly describe two skills in the library, narrow it.

### 2. Specificity Beats Breadth

A narrow, distinctive description triggers *more* reliably than a broad one because:
- Routing favors distinctive vocabulary over common vocabulary
- Broad descriptions collide with neighbors and get deprioritized
- Users phrase requests with concrete nouns and verbs, not taxonomy categories

A skill that claims to handle "all writing tasks" loses to a skill that claims to handle "LinkedIn posts with a hook and CTA." The LinkedIn skill also catches more LinkedIn requests — because its language matches the user's surface form.

### 3. Distinctive Anchors Over Keyword Stuffing

Routers don't reward keyword count; they reward keyword distinctiveness. A single distinctive anchor phrase outperforms ten generic triggers. Stuffed triggers dilute the skill's signal, compete with its own description, and create false positives that push it ahead of better-matched skills.

### 4. First Sentence Wins

The first sentence of the description carries the most routing weight. Put the differentiator — the thing that distinguishes this skill from every neighbor — in sentence one. Put activation nudges later.

### 5. Mirror User Surface Forms

Triggers and description phrases should echo how a user would actually type a request, not how the skill's author categorizes it. Prefer `"write a LinkedIn post"` over `"professional social content generation"`. If you cannot find evidence of a phrase in real user requests, it will not route.

### 6. Exclusion Sharpens Inclusion

Stating what the skill is NOT often improves triggering more than adding new triggers. `anti-triggers` and negative phrasing in the description narrow the activation surface and prevent the skill from being shadowed by, or shadowing, its neighbors.

---

## Description Structure

Target length: **150–400 characters**. Longer than 500 characters signals the skill is trying to be too many things. Shorter than 100 usually misses the WHEN clause.

Three required components, in order:

### WHAT (1 sentence)
Concrete capability and primary output. Use the domain noun a user would say. No abstract categories.

- Good: `"Create a new interpretation of an existing skill while preserving original intent."`
- Weak: `"Helps with skill content transformation tasks."` (no noun a user would type)

### WHEN (1–2 sentences, quoted trigger phrases)
Specific activation scenarios. Embed 3–6 quoted phrases the user might actually say. Quoted phrases route more reliably than plain nouns because they match exact user input.

- Good: `"Use when asked to \"reinterpret a skill\", \"clone and improve a skill\", or \"rebuild a skill from scratch\"."`
- Weak: `"Use for skill transformation work."` (no quoted phrases, vague scenario)

### PUSH (optional, 1 sentence — for broad-activation skills only)
Explicit nudge for indirect requests that should still activate. Use only when the WHAT/WHEN language is narrower than the skill's true scope. Over-use of PUSH causes over-triggering.

- Pattern: `"Use whenever the user is [activity pattern], even if they don't use these exact terms."`
- Omit PUSH for narrow, purpose-specific skills — it widens activation unnecessarily.

---

## Trigger Count & Quality

### Count

**6–10 triggers total.** Fewer than 4 usually misses obvious phrasings; more than 12 dilutes signal and almost always includes low-signal duplicates.

Diminishing returns kick in hard after ~8. If you are writing trigger 13, it is nearly always a variant that adds no new routing coverage (`"create skill"` vs `"creating skills"` vs `"skill creation"` — pick one).

### Quality Tests

Each trigger must pass all four:

1. **User-authored** — would a user actually type this in a chat? If it is a category label ("skill governance"), cut it.
2. **Distinctive** — is this phrase used by fewer than ~3 other skills in the library? If every marketing skill has `"marketing"` as a trigger, none of them route well on it.
3. **Action-shaped** — verb + object (`"create skill"`, `"write LinkedIn post"`) routes better than noun-only (`"skill"`, `"LinkedIn"`).
4. **Non-redundant** — does it cover a phrasing not already implied by the description or another trigger? Variants of one phrase count as one trigger.

### What to Cut

- **Morphological variants** — `"review skill"` implies `"reviewing skill"` and `"skill review"`. Keep one.
- **Skill name echoes** — repeating the skill name as a trigger adds nothing; the router already sees the name.
- **Internal jargon** — `"metadata routing optimization"` is not how users ask for things.
- **Category-only terms** — `"quality"`, `"design"`, `"meta"` are already in `domain`; do not burn a trigger slot on them.

---

## Avoiding Collisions & Overlap

Collisions happen when two skills compete for the same prompts. The router picks one, often inconsistently, and both skills feel unreliable.

### Detection

Before publishing a new or revised description:

1. List the skill's top 5 trigger phrases.
2. For each, check how many other skills in the library share that phrase or near-synonyms.
3. If any phrase overlaps with ≥2 neighbors, the description will collide.
4. Read the descriptions of the nearest 2–3 neighbor skills. If the opening sentences are interchangeable, the skills will collide.

### Resolution Options

When a collision is detected:

| Situation | Action |
|---|---|
| Two skills genuinely cover the same space | Merge them, or narrow one to a sub-scope |
| Skills overlap on a shared domain but differ on outcome | Lead each description with the **outcome**, not the domain (e.g., "produces a PRD" vs "produces an eval report") |
| One skill is broader and contains the other | Broader skill uses `priority: broad`; narrower uses `priority: specific`; narrower skill names its exact scope in sentence one |
| Skills differ by audience or phase | Lead with the audience/phase word (`"for an existing skill"` vs `"for a new skill"`) |
| Borderline overlap, hard to separate on wording | Add `anti-triggers` naming the neighbor skill's core phrases |

### Narrow-Skill Protection

Narrow skills are routinely shadowed by broader neighbors whose descriptions sweep up their activation surface. Protect a narrow skill by:

- Opening the description with the narrowing qualifier (not at the end)
- Using a distinctive trigger phrase that the broader skill does not mention
- Setting `priority: specific` if the repo uses priority
- Avoiding any trigger that also appears in the broader skill's description

---

## Over-Triggering vs Under-Triggering

Most routing failures in practice are **under-triggering**: a relevant skill stays silent because its description used the wrong vocabulary. Only a small fraction are over-triggering (activating on unrelated prompts).

This asymmetry matters when tuning. If you have to choose:

- Err toward including a concrete user phrase in the description — under-triggering is the more common failure.
- Do not widen the description by adding generic category words — over-triggering from category words is common and painful to debug.
- Use `anti-triggers` to handle the specific over-triggers you have seen, without widening the under-trigger surface.

Signs of under-triggering:
- Users re-phrase requests 2–3 times before the skill fires
- Related-domain prompts activate a generic or wrong skill instead

Signs of over-triggering:
- The skill fires on prompts the user didn't intend it for
- The skill shadows a more-specific neighbor for prompts that neighbor should own

---

## Tradeoffs

Several tensions have no universal right answer. Resolve each one deliberately, not by default.

### Broad vs Narrow Descriptions
A broader description catches more prompts but collides more with neighbors and drops routing precision. A narrower description is more precise but misses adjacent phrasings. **Default narrow** — library scale amplifies collisions.

### Quoted Phrases vs Free Prose
Quoted phrases (`"create a skill"`) route on exact match and work well for direct user language. Prose phrasing generalizes to semantic variants. **Use quotes for 3–5 high-signal phrases; prose for the surrounding framing.**

### Triggers List vs Description-Embedded Phrases
Phrases inside the description often route more heavily than the `triggers` metadata field, depending on platform. Put critical routing phrases in the description; use `triggers` for supplementary variants. **Do not duplicate** — if a phrase is in the description, drop it from `triggers`.

### Coverage vs Crispness
Extending the description to cover every edge case degrades routing for the primary case. **Write for the top 3 prompts**; rely on `anti-triggers` and neighbor skills to handle edges.

### Author Vocabulary vs User Vocabulary
Skill authors reach for domain terminology; users reach for plain verbs and concrete nouns. **User vocabulary wins** in the description. Keep author vocabulary for the body.

---

## Review Checklist

Apply before shipping any description or trigger change:

### Description
- [ ] 150–400 characters
- [ ] WHAT sentence names the concrete output, not a category
- [ ] WHEN sentence includes 3–6 quoted phrases in real user language
- [ ] First sentence distinguishes this skill from its nearest neighbor
- [ ] No angle brackets, no placeholder text, no skill-name echo
- [ ] PUSH sentence present only if the skill legitimately needs broad activation

### Triggers
- [ ] 6–10 entries, comma-separated
- [ ] Every entry is a verb-object user phrase
- [ ] No morphological duplicates
- [ ] No phrase also present in the description
- [ ] No phrase shared by ≥3 neighbor skills
- [ ] No category-only terms already covered by `domain`

### Collision
- [ ] Nearest 2–3 neighbor skills were read; descriptions are not interchangeable
- [ ] Shared phrases with neighbors were either eliminated or disambiguated with leading qualifier
- [ ] If overlap is unavoidable, `anti-triggers` or `priority` was set

### Failure Mode Coverage
- [ ] Description would route for at least one indirect phrasing (not just the direct skill-name request)
- [ ] Description would NOT route for the closest adjacent task that belongs to a neighbor skill
