# Conversion and Engagement Model

Design impact is not purely aesthetic; it is measurable. Every section must serve a declared goal. This reference maps sections to goals, defines the CTA hierarchy, and codifies the copy and engagement rules that move conversion. It applies to both conversion-safe and expressive modes.

## Goal Ladder

Every page declares one primary goal before any visual decision:

| Tier | Goal | Measure |
|------|------|---------|
| **Primary** | Qualified conversion (contact, demo, signup, purchase) | Click-through on primary CTA, form submit |
| **Secondary** | Engagement depth (case study read, content consumption) | Scroll depth ≥ 75%, time on page, secondary clicks |
| **Tertiary** | Return and share (subscribe, bookmark, share) | Repeat visit, share event, newsletter signup |

A page can support all three, but one is primary. The primary CTA is the only one that uses the action color.

## Section to Goal Mapping

| Section | Primary goal | Secondary effect |
|---------|-------------|-----------------|
| Hero | Frame the offer, surface primary CTA in first viewport | Brand impression |
| Manifesto strip | Establish posture (why us) | Builds rhythm, increases scroll depth |
| Sector marquee | Breadth signal (we serve your category) | Visual motion, engagement |
| Numbered cards grid | Drive clicks into deep content | Scannable proof |
| Stat band | Credibility, quantified proof | Reduces friction before CTA |
| Editorial grid | Brand depth, content engagement | Drives return visits |
| Case studies grid | Social proof, portfolio depth | Drives clicks into case study pages |
| Quote / testimonial band | Trust through specificity | Reduces evaluation friction |
| Product demo moment | Demonstrate core value without requiring action | Reduces signup friction |
| Full-bleed prefooter | Final primary CTA push | Last impression before footer |
| Footer | Wayfinding, trust signals | Recovery from bounce intent |

A section that does not tie to one of these gets cut or replaced. "About us" filler sections, generic "Our values" cards, and decorative-only bands fail this test.

## Visual Distinctiveness as a Conversion Factor

Distinctive design and conversion-optimized design are not in tension. They serve the same goal.

A generic, template-looking site communicates implicitly that the product or service is also generic. A distinctive, conceptually coherent site communicates that the team behind it pays attention and sweats details. In categories where trust is a purchase criterion (enterprise software, professional services, financial products, healthcare), the quality of the site is a proxy for the quality of the product.

Visual monotony is a conversion killer for the same reason stock photography is: it signals that no decision was made.

The skills in `references/concept-and-art-direction.md` that produce award-caliber work are the same skills that produce higher-converting work in categories where trust matters.

## CTA Hierarchy

Three button weights, used with discipline:

| Weight | Visual | Use |
|--------|--------|-----|
| **Primary** | Solid signature/action color, bold copy, min 44px height | The primary goal CTA. Max two per page (hero plus prefooter). |
| **Secondary** | Outlined or ghost, ink color | Secondary actions ("See the work," "Read the case study"). |
| **Text link** | Underlined or arrow-suffixed inline | In-flow links, tertiary navigation. |

If every button looks the same, nothing converts. The eye must find the primary action without searching.

## CTA Copy Rules

- Imperative verb first. "Start," "See," "Read," "Get," "Book," "Talk to." Never "Learn more" alone, never "Click here," never "Submit."
- Outcome-oriented. "Start an engagement" beats "Contact us." "See the case study" beats "Read more." "Book a 30-minute call" beats "Get in touch."
- One verb per CTA. Compound CTAs dilute.
- Pair with a one-line value clarifier when above the fold. Hero CTA: button plus 6-word reassurance below ("Reply within one business day").

## Hero Conversion Checklist

Within the first viewport (above the fold), a high-converting hero contains:

1. Eyebrow tag (who this is for, what this is): 3 to 5 words.
2. Headline with the value claim, accent mark on the key word.
3. Subhead clarifying the offer in one sentence.
4. Primary CTA visible without scroll.
5. Trust signal within the first viewport: small logo strip, stat, or quote.

If any of these is missing, conversion leaks at the first viewport.

## Engagement Levers

For pages where engagement (depth, return, share) is the primary goal:

**Scroll-depth rewards.** One surprise moment below the fold per page (full-bleed quote, animated stat reveal, interactive widget, expressive motion moment). One per page, not one per section.

**Sticky chrome that does not shrink.** A scroll-aware header (1px border appearing after scrollY > 80) keeps the brand present without claiming hero space.

**Progress signaling.** For long-form pages, a 2px progress bar at the top of the scroll viewport. Subtle, not gamified.

**Reading-friendly type measure.** 60 to 75 character line length for body copy.

**In-flow CTAs every 2 to 3 sections** on long pages. The conversion path stays close to the reader throughout.

**Expressive mode engagement.** When impression or engagement is the primary goal rather than direct conversion, expressive patterns serve the goal directly. Scroll choreography creates scroll depth. Custom cursor states create dwell time. Entry sequences create attention in the critical first 5 seconds. These are not decorative; they are engagement mechanics. Load `references/concept-and-art-direction.md` for implementation.

## Friction Audit

Run on every page before ship:

- [ ] Is the primary CTA reachable without scroll on mobile?
- [ ] Does any section require more than 3 seconds to understand?
- [ ] Are there 2 or more different "primary" CTAs competing? (Should be 1, max 2 if hero plus prefooter only.)
- [ ] Does any form ask for more than the minimum required to qualify?
- [ ] Does any section make the visitor feel sold-to before earning trust?
- [ ] Does any image look like a stock photo or a screenshot of a demo environment?
- [ ] Does the page look like it could belong to a competitor? (If yes, the concept is not executing.)

Cut whatever fails.

## What Kills Conversion

In order of measured impact:

1. Centered hero with generic gradient and "Learn more": no specificity, no urgency.
2. Stock photography: implicit signal that the product is generic.
3. Three identical feature cards: visual monotony produces scroll-past.
4. Multiple competing primary CTAs: the visitor freezes.
5. Vague copy ("powerful," "modern," "innovative"): no information transferred.
6. Slow LCP: the visitor bounces before the hero renders. Target under 2.5s.
7. No prefooter CTA: the last viewport before footer is dead air.
8. A site that looks like a template: it signals the team uses defaults and does not sweat details.

## Engagement-Friendly Defaults

- Hover-to-open navigation: discovers depth without clicks.
- Marquee: passive motion encourages scroll continuation.
- Numbered cards with arrow links: clear affordance for deeper content.
- Active route in nav with aria-current: orients returning visitors.
- Scroll reveals: fade plus 12px translate, never bouncy. Rewards downward motion.
- Sticky scroll scenes (expressive mode): holds attention through a multi-feature demonstration without requiring navigation.
