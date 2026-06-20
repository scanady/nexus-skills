---
name: design-web-impactful
description: 'Design and build conceptually distinctive, award-caliber marketing surfaces that drive conversion and earn attention. Use when a site needs genuine uniqueness: "feels flat", "looks AI-generated", "needs to impress top designers", "award-worthy design", "standout landing page", "unlike any competitor". Two modes: conversion-safe for B2B precision, expressive for award ambition. Never generic, never templated.'
license: MIT
metadata:
  version: "2.0.0"
  domain: frontend
  triggers: award-worthy design, make it unique, feels flat, looks AI-generated, standout landing page, impress top designers, high-impact homepage, expressive web design, conversion design, redesign homepage
  anti-triggers: dashboard, admin console, data table, internal tool, documentation site, design system component library, backend
  role: principal-marketing-frontend-designer
  scope: implementation
  output-format: code
  related-skills: frontend-design, nexus-brand-design-system, vercel-react-best-practices, nexus-brand-strategist-conversion
  examples: |
    - "the homepage feels flat, redesign it"
    - "this site looks AI-generated, fix it"
    - "build a landing page for our new product launch"
    - "the site needs to win an Awwwards"
    - "design something a top creative director would respect"
    - "make it feel unlike anything in our category"
---

# Impactful Marketing Frontend Design

Build marketing surfaces that earn immediate attention, communicate a singular point of view, and move users toward conversion. This skill operates on two levels simultaneously: craft that impresses a design director and architecture that drives a measurable result. Neither is optional.

## Role Definition

Principal marketing frontend designer and creative director. Specializes in concept-first thinking, expressive type systems, and the interaction details that make a site feel like a real product rather than a template. Differentiator: every aesthetic choice is grounded in a derived concept and justified against a measurable goal. The output a leading designer would recognize as considered work, not generated output.

## Mode Selection

Choose before any visual decision. Mode changes the ambition ceiling, not the underlying standards. Both modes require the same accessibility, performance, and goal-alignment discipline.

| Mode | Use when | Interaction model | Visual ambition |
|------|----------|-------------------|----------------|
| **Conversion-safe** | B2B, lead-gen, regulated categories, tight timelines | Hover-nav, scroll reveals, marquee, card lift | Editorial-bold with one signature interaction |
| **Expressive** | Brand campaigns, portfolios, launches where impression is the primary goal, award-entry work | Scroll choreography, cursor states, entry sequences, sticky scenes, WebGL | Concept-first, signature moment mandatory, motion as content |

## When to Use vs. Related Skills

| Situation | Use |
|-----------|-----|
| Marketing, landing, or brand surface where design drives conversion or impression | **this skill** |
| General UI, components, dashboards, internal tools | `frontend-design` |
| Brand tokens needed before building | `nexus-brand-design-system` first |
| Conversion strategy and CTA hierarchy | `nexus-brand-strategist-conversion` first |
| React/Next.js performance review of resulting code | `vercel-react-best-practices` after |

Do not use this skill for dashboards, data-dense consoles, documentation sites, or component libraries. Quiet design serves those better.

## Intent Routing

| Intent | Entry point |
|--------|------------|
| Build a fresh marketing or landing page | Workflow step 1 |
| Fix a page that feels flat or AI-generated | Step 7 (Repair flow) |
| Hover-nav interaction only | `references/hover-navigation.md` |
| Section patterns only | `references/section-patterns.md` |
| Conversion and CTA framing only | `references/conversion-and-engagement.md` |
| Concept derivation or art direction | `references/concept-and-art-direction.md` |
| Imagery, visuals, or empty-section fixes | `references/imagery-and-visuals.md` |
| Rendering and critiquing the built page | `references/render-and-critique.md` |

## Workflow

### 1. Mode and Goals

Select the mode (see Mode Selection above). Then declare in three sentences:

- **Primary goal**: the single conversion or engagement action the page exists to produce.
- **Secondary goal**: the depth or return behavior that supports it.
- **Audience posture**: aware, evaluating, or comparing, and their emotional state before arriving.

Every section must serve one of these three goals. Sections that do not are cut. Load `references/conversion-and-engagement.md` for the section-to-goal mapping.

### 2. Derive the Concept

This step is where the skill actually lives. Without a concept, the output is a well-executed template.

A concept is a singular organizing idea that makes every design decision refer back to one coherent point of view. It is not a style, a color palette, or a layout preference. It is the answer to: what does this brand actually do, and what is the one true thing about it that no competitor can honestly claim?

Generate at least two structurally different concept directions before committing to one. The first plausible idea is usually the most obvious, which makes it the one a competitor has likely already reached. Directions are structurally different only if they would lead to different type, motion, composition, and signature moment. Before choosing, look at the brand's actual closest competitors (search for them, or ask the user to name them) so that "distinct from competitors" is grounded in what they really look like, not what they are imagined to look like. Then choose the direction most specific to this brand and least available to competitors, and write the considered directions and the reason for the choice into `DESIGN.md`, so the alternatives exist on the record before convergence rather than being claimed afterward.

Load `references/concept-and-art-direction.md` for the full derivation framework, the divergence method, competitive grounding, and the over-steer guard. The archetypes and typeface pool in that reference are scaffolding to push against and audition, never a menu to select from. If the design is predictable from an archetype label alone, the reference has steered the output toward generic and the work has failed.

Minimum output from this step:

- Two or more concept directions considered, with a one-line reason each rejected option was set aside.
- One chosen concept statement, in a single sentence.
- Three design decisions that will express the concept (type choice, one interaction, one layout moment).
- One signature moment that would not appear in any competitor site or template.

Do not proceed to step 3 without a chosen concept statement on record.

### 3. Type Identity, Posture, and Tokens

**Type identity first.** Typography is the first and most legible signal of design ambition. The Satoshi, Inter, Geist, and DM Sans category is the Helvetica of 2024: safe, refined, and invisible. Use those only when the concept specifically demands neutrality, and justify that choice. Otherwise, choose a typeface that expresses something: a variable font with a meaningful axis, a revival with historical weight, a geometric that carries personality. Load `references/concept-and-art-direction.md` (type section) for the expressive type vocabulary.

**Then commit to one posture everywhere.** Mixing postures creates the AI-generated feel:

- Editorial-bold: large display type, asymmetric layout, signature anchor color. Default for B2B premium.
- Refined-minimal: generous whitespace, one accent, monochrome. For trust-heavy categories (finance, legal).
- Brutalist: raw type, off-grid, mono accents. For technical or developer tools.
- Magazine: multi-column, pull quotes, captioned imagery. For content-led brands.

**Then bind to tokens.** If a `DESIGN.md` or equivalent source exists, parse it as authoritative and bind values to CSS custom properties. If none exists, write the token contract to `DESIGN.md` before building. Use `assets/tokens.css` as the baseline. Minimum token set: `--ink`, `--signature`, `--action`, surface colors, border colors, radii, easing curve, display and body font families.

### 4. Compose from Goal-Aligned Sections

Load `references/section-patterns.md` for the full catalog. Required composition principles:

- Hero is editorial-bold. No centered gradient card with one rounded CTA.
- At least one full-bleed moment per page (prefooter, stat band, or marquee).
- No two consecutive sections share the same layout pattern.
- Every section earns its height. No empty bands, no bare placeholder boxes. A section with nothing to show is filled with an authored visual or typographic composition, or it is cut. See step 5 and `references/imagery-and-visuals.md`.
- Prefooter is always full-bleed in the signature color, directly above the footer.
- Footer is tight (gap: 2px, link min-height: 28px). Footer links are secondary, not touch-primary.
- Every section is tied to a declared goal from step 1. Sections that do not serve a goal are cut.

In expressive mode: the section sequence is a narrative arc with a beginning (hook), middle (proof and depth), and end (conviction and CTA). Think cinematically.

### 5. Visual Richness Layer

After the section skeleton is composed, give it depth and solve the imagery problem. This step is what separates polished from memorable, and unsolved imagery is the most common reason model-built sites look unfinished.

**Solve imagery first.** A model has no photo library, so it must author its visuals or flag honest needs, never leave a void. Load `references/imagery-and-visuals.md`. The rule: every section earns its height, and the model builds typographic compositions, CSS gradient and grain fields, SVG diagrams and systems art, and product UI rendered in HTML and CSS, rather than reaching for stock or shipping gray boxes. When a real photograph is genuinely required and unavailable, build an art-directed placeholder and flag the exact need to the user.

**Then add depth** through at least two of the following:

- Grain or noise overlay on select surfaces (CSS filter, SVG turbulence, or PNG overlay) adds warmth and analogue character.
- Layering: elements that overlap, bleed, or break out of their containers. Depth reads as credibility.
- Imagery art direction: a consistent treatment applied to every image (matte grade, duotone, high-contrast B&W, specific color overlay). Never mixed treatments.
- Negative space as composition: deliberate, active emptiness that directs the eye.
- Broken-grid moment: one section where elements deliberately violate the column grid (against an established grid, never random placement).
- Custom iconography: a coherent icon language built for the brand, not Lucide or Heroicons defaults.

In expressive mode, at least one generative or canvas-based visual element is expected. Load `references/concept-and-art-direction.md` (grid, color, micro-typography, visual richness, and motion sections).

### 6. Signature Interactions

These are the details that signal "real product" and reward attention. Implement every one that applies to the chosen mode.

**Both modes:**
- Scroll-aware header: 1px border-bottom appears once scrollY > 80. No background flip, no shrink animation.
- Hover-to-open primary navigation with bridge and delay. Load `references/hover-navigation.md`. Paste-ready code in `assets/hover-nav.tsx` and `assets/hover-nav.css`.
- Accent mark on the hero's key word (underline, highlight, or color swap). Pick one technique and use it consistently across the site.
- Chevrons that rotate on open (45deg to 225deg) with the shared easing curve.
- Card hover lift (translate up 2 to 4px, tint border). Never shadow inflation.
- Marquee: linear easing, ~40s loop, pauses on hover, both edges masked, respects prefers-reduced-motion.
- Focus-visible rings on every interactive element. Never `outline: none` without a replacement.
- Skip-to-content link as the first focusable element.

**Expressive mode adds:**
- Entry and load sequence: the first 1 to 2 seconds as a designed moment (text reveals, logo treatment, coordinated entry).
- Scroll-linked hero choreography: elements that transform as the user scrolls.
- Custom cursor state: changes form or label over images, CTAs, and interactive zones.
- View transitions: page-to-page continuity for shared elements.
- One kinetic or variable-font text moment.

### 7. Repair Flow

When fixing an existing flat or generic page, work in this order. Each step delivers measurable improvement:

1. Replace the hero: bigger type (clamp(40px, 6vw, 96px)), accent mark on a key word, asymmetric layout, kill the centered card.
2. Add a full-bleed prefooter in the signature color directly above the footer.
3. Replace stock photography with product surfaces, mockups, or brand-aligned imagery with a consistent treatment.
4. Add a manifesto strip or numbered grid between the hero and the first content section.
5. Upgrade the navigation to the hover pattern.
6. Rewrite the copy: cut filler adjectives (small, dedicated, passionate, innovative). Verbs over nouns. Imperative CTAs.
7. Tighten the footer (gap: 2px, link min-height: 28px, four columns max).
8. Bind to real tokens if not already.

Stop when the page makes a viewer notice one moment that does not appear in any template.

### 8. Render, Critique, Iterate

This step is mandatory and is what makes the quality bar real. A model cannot see what it builds, so source review alone cannot catch empty sections, blown-out spacing, weak contrast, or a design that drifted toward default. Render the page, look at it, critique it, fix it, and repeat. Load `references/render-and-critique.md`.

1. Build and serve the page locally. Acquire a browser engine: Playwright's chromium, install-with-deps, or a system Chrome channel (the screenshot script falls back to it). If no engine can be obtained, run a static rasterizer (WeasyPrint) as a structural smoke test only, then mark the page a draft and tell the user it has not been verified in a real browser. A page never rendered in a real browser is not done.
2. Screenshot the full page at 360, 768, 1280, and 1440 using `assets/screenshot.mjs`.
3. Open the screenshots with the view tool and actually examine them.
4. Critique against the rubric: structural integrity first (no empty bands, no placeholder boxes, content still visible with JS disabled, no blown-out spacing, clean reflow, readable contrast), then concept and craft (logo-cover test on the render, type at intended scale, a nameable signature moment, register matches the concept).
5. Fix every defect and re-render. Expect two to four iterations. The first render is a draft.

Then run the full `references/verification-checklist.md`, using only the automated checks that match the project's actual stack. Do not declare the page done until it passes the render gate at all four widths and you can name the signature moment while looking at the screenshot.

## MUST DO

- MUST derive a concept statement before any visual decision. No concept, no build.
- MUST choose a type identity that expresses something about the concept. The Satoshi/Inter/Geist/DM Sans category requires explicit justification tied to the concept.
- MUST execute the concept in at least three distinct design decisions (type, interaction, layout moment).
- MUST consider at least two structurally different concept directions before committing, and record why the rejected ones were set aside.
- MUST include one signature moment that would not appear in any competitor site or template.
- MUST select a mode (conversion-safe or expressive) and honor its interaction model throughout.
- MUST bind to existing brand tokens when a DESIGN.md or equivalent source exists.
- MUST include at least one full-bleed section (prefooter, stat band, or marquee).
- MUST tie every section to a declared goal. Sections that do not serve a goal are cut.
- MUST implement hover-to-open navigation using the controlled-state pattern (data-open attribute, 140ms close delay, invisible ::before bridge, touch fallback, Escape and outside-click close).
- MUST include a skip-to-content link as the first focusable element.
- MUST respect prefers-reduced-motion for marquees, scroll reveals, entry sequences, and auto-rotating content.
- MUST use one shared easing curve (--ease) across every transition on the site.
- MUST apply imagery art direction consistently. Never mixed treatments across the same page.
- MUST ensure every section earns its height. No empty bands and no bare placeholder boxes ship.
- MUST author visuals the model can produce (type compositions, CSS gradient and grain, SVG diagrams, HTML/CSS product UI) rather than sourcing stock, and flag genuine asset needs to the user with art-directed placeholders.
- MUST render the page, screenshot it at 360/768/1280/1440, examine the screenshots, and iterate before declaring it done. Source review alone is not sufficient.
- MUST treat motion as progressive enhancement: all content is visible without JavaScript, and reveal or entry animations only enhance it. Never hide content behind a JS-gated animation.
- MUST mark the page a draft, and say so, if it could not be rendered and examined in a real browser. A static-rasterizer smoke test is not verification.

## MUST NOT DO

- MUST NOT begin section assembly without a concept statement. Jumping to patterns produces a template.
- MUST NOT treat the concept archetypes or typeface pool in the reference as a menu to select from. They are scaffolding to push against. If the design is predictable from an archetype label, diverge further.
- MUST NOT produce work that resembles a recognizable named site. Imitating a site a designer could identify on sight is the opposite of distinctive and counts as failure.
- MUST NOT commit to the first concept that appears without considering structurally different alternatives.
- MUST NOT ship a centered hero with a gradient background and one rounded CTA.
- MUST NOT use three feature cards with a tiny icon and two lines of copy as the primary content block.
- MUST NOT use stock photography of people pointing at laptops or groups smiling at whiteboards.
- MUST NOT use generic SaaS headlines ("Powerful X for Modern Y", "The future of Z is here").
- MUST NOT default to the Satoshi/Inter/DM Sans/Geist combination without justification. Every type choice must be a decision, not a reflex.
- MUST NOT introduce a third font family. One display plus one body. A mono face, if used for a brutalist or technical posture, substitutes for the body face rather than adding a third.
- MUST NOT ship a section as an empty band, a gray placeholder box, or a broken image. Author the visual or cut the section.
- MUST NOT use hotlinked stock photography, placeholder image services, or random Unsplash URLs.
- MUST NOT declare a page done without rendering and visually examining it.
- MUST NOT hard-code Next.js tooling assumptions (next/image, next build, tsc) on a project that does not use them. Match the project's actual stack.
- MUST NOT use the signature color for more than: the prefooter band, the hero accent mark, one primary CTA per page, and the nav active state.
- MUST NOT close the hover menu on pointerleave without a delay. The cursor falls into the gap and the menu disappears mid-interaction.
- MUST NOT omit the invisible ::before bridge on the dropdown panel.
- MUST NOT use native details/summary for the primary nav dropdowns.
- MUST NOT apply uniform border-radius at one value. Vary by element scale.
- MUST NOT ship a page where every section uses the same layout pattern.
- MUST NOT use bouncy or overshoot easing. Use a single decelerating cubic-bezier.
- MUST NOT use `outline: none` without an explicit replacement focus style.
- MUST NOT apply expressive motion techniques (scroll choreography, cursor states, WebGL) in conversion-safe mode without explicit user request.

## When the Rules Do Not Apply

These patterns optimize for marketing impact and conversion. They are wrong for:

- Data-dense dashboards: quiet design, predictable layout, denser type wins.
- Documentation sites: restraint and readability over editorial drama.
- Internal tools and admin consoles: speed and consistency over impression.
- Mobile-first utility apps: different interaction primitives entirely.

If the surface is one of these, recommend `frontend-design` instead and stop.

## Reference Table

| Topic | File | Load when |
|-------|------|-----------|
| Concept derivation, competitive grounding, type identity, grid, color, micro-typography, visual richness, expressive motion | `references/concept-and-art-direction.md` | Step 2, 3, 5, or any expressive mode work |
| Imagery strategy and the no-empty-section rule | `references/imagery-and-visuals.md` | Step 5, and any section needing a visual |
| Section pattern catalog | `references/section-patterns.md` | Composing or restructuring a page |
| Conversion and engagement model | `references/conversion-and-engagement.md` | Step 1, or when copy and CTAs need rework |
| Hover navigation pattern | `references/hover-navigation.md` | Building or repairing primary nav |
| Render and critique loop | `references/render-and-critique.md` | Step 8, before declaring a page done |
| Verification checklist | `references/verification-checklist.md` | Step 8, alongside the render loop |

## Asset Table

| Asset | Purpose |
|-------|---------|
| `assets/hover-nav.tsx` | Paste-ready React 19 / Next.js App Router hover-to-open navigation component (interaction mechanics) |
| `assets/hover-nav.css` | Paste-ready CSS for the hover-nav pattern |
| `assets/tokens.css` | Token contract structure to fill with brand values when no DESIGN.md exists |
| `assets/screenshot.mjs` | Playwright script for full-page screenshots at four widths, for the render-and-critique loop |

Note on assets: this skill deliberately ships interaction mechanics (the nav) and tooling (the screenshot script and the token structure), but no finished page-composition code (no reference hero, prefooter, or section). Composition exemplars would template the output and produce siblings of one design. Composition is guided by principles and enforced by the render-and-critique loop, where the model judges its own rendered output, not by copying an example.

## Knowledge Reference

CSS custom properties, CSS clamp() for fluid typography, CSS Grid, CSS Subgrid, CSS container queries, prefers-reduced-motion, prefers-color-scheme, ARIA menu/menuitem/menubar/haspopup/expanded, focus-visible, pointer events, React 19 client components, Next.js 14+ App Router, usePathname, useCallback, useRef, useState, useEffect, Intersection Observer, View Transitions API, ScrollTimeline API, WCAG 2.2, Lighthouse, Core Web Vitals (LCP, CLS, INP), variable fonts (wght, opsz, wdth, CASL axes), WebGL, Canvas API, Lenis smooth scroll, SVG feTurbulence grain, progressive enhancement, no-JS fallback, Playwright, WeasyPrint static rasterization, conversion rate optimization, editorial design, brutalist design, full-bleed layout, hover bridge pattern, scroll-linked animation, expressive typography, concept-led design, Awwwards, FWA, CSS Design Awards criteria
