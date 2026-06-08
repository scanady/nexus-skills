# Section Pattern Catalog

The section vocabulary for impactful marketing pages. Every section must serve a declared goal. Mix and match but do not ship every pattern on one page. Always include at least one full-bleed moment and one moment that could not appear in a template.

## Composition Principles

Before selecting patterns, declare the narrative arc:
- Hero serves the first impression and surfaces the primary CTA.
- The section immediately after the hero establishes credibility or rhythm (manifesto strip, stat band, or numbered grid).
- Middle sections build proof and depth.
- Prefooter is the final conversion push.

**Layout variation is required.** No two consecutive sections share the same layout pattern. The eye needs rhythm and contrast to stay engaged.

**Every section earns its height.** No section ships empty or as a bare placeholder box. A tall band of blank surface where a visual was expected is the most damaging defect this skill can produce, because it reads as broken, not merely safe. If a section has nothing to show, fill it with an authored visual or a typographic composition, or cut it. See `references/imagery-and-visuals.md` for what to build instead of sourcing a photo. Alternating surface colors and authored SVG or type compositions are the reliable ways to give a long page rhythm without depending on imagery.

**Establish a grid, then break it once.** Define a column grid, gutters, and a modular spacing scale before composing. The broken-grid moment only reads as intentional against a rigorous structure. See the grid section in `references/concept-and-art-direction.md`.

**In expressive mode, think cinematically.** The sequence has a beginning, middle, and end. Each section knows what comes before and after it.

## Hero: Editorial-Bold

**Goal it serves:** first impression, primary CTA discoverability.

**Anatomy:**
- One eyebrow tag: short, ALL CAPS or small-caps, letter-spacing: 0.08em, muted ink. Max 5 words.
- One oversized headline: clamp(40px, 6vw, 96px), display font, line-height ~1.05, letter-spacing: -0.02em.
- An accent mark on the single most important word. Pick ONE technique, use it consistently across the site:
  - Yellow brushstroke underlay (SVG behind the word)
  - Hand-drawn underline (SVG path beneath)
  - Color swap to signature color
  - Solid highlight block behind the word
- One subhead (~18 to 22px, body font, muted ink, 60 to 75 character line length).
- One primary CTA (signature/action color, imperative verb copy, visible without scroll on mobile).
- One secondary text link.
- Asymmetric layout: content left, off-grid visual or stat block right. Never dead-center.
- Trust signal within the first viewport: small logo strip, one stat, or one brief quote.

**Anti-pattern:** centered gradient hero with a single rounded CTA.

## Hero: Type-Led

**Goal it serves:** first impression through type as concept. Use when the concept positions type as the primary visual statement.

**Anatomy:**
- Headline at genuine editorial scale: clamp(72px, 10vw, 140px). Type occupies meaningful canvas space.
- Deliberately designed line breaks: the breaks are a typographic decision, not a browser default.
- Near-zero imagery. The type is the visual.
- One accent mark (technique consistent with editorial-bold rules).
- Asymmetric layout, but composition is driven by the letterforms themselves.
- CTA below the headline, restrained in weight so it does not compete.

**Best for:** velocity or craft-signal concepts, agencies, tools where the product requires no visual explanation.

## Manifesto Strip

**Goal it serves:** establish rhythm, communicate posture in one scan.

**Anatomy:**
- A horizontal band of 3 to 5 numbered stages or principles.
- Each stage: large number (display font, dominant element), short label, one line of copy.
- Numbers in signature color or with a thin underline beneath.
- Sits between hero and the first deep content section. Establishes that this is not a template.

## Sector / Capability Marquee

**Goal it serves:** breadth signal, visual motion, engagement.

**Anatomy:**
- Single-line horizontally scrolling band of capability names, separated by a small bullet, dash, or icon.
- animation: marquee 40s linear infinite with a duplicated track for seamless looping.
- Pause on hover (animation-play-state: paused).
- Mask both edges with gradient fade.
- Respects prefers-reduced-motion:

```css
@media (prefers-reduced-motion: reduce) {
  .marquee-track { animation: none; }
}
```

## Numbered Cards Grid

**Goal it serves:** depth scan, drive clicks into deeper content.

**Anatomy:**
- 4 to 6 cards in a grid. Each card:
  - Large two-digit number (01, 02, 03): display font, signature or ink color, dominant element.
  - Title.
  - Short description (1 to 2 lines).
  - Link with arrow ("Read it" or "Explore").
- 1px border (--border-subtle), no shadow.
- Hover: lift 2 to 4px (transform: translateY(-3px)), tint border to --border-strong. Never inflate shadow.

## Stat Band

**Goal it serves:** credibility, scannable proof.

**Anatomy:**
- 3 to 4 numerical stats in a horizontal row, full-bleed or near full-bleed.
- Numbers in display font, 48 to 72px, optionally counting up on viewport entry.
- Labels below in small-caps.
- Optional thin divider lines between stats.

**Expressive variant:** add a grain overlay surface and a mechanical typeface. The material makes the number feel earned.

## Editorial Grid

**Goal it serves:** depth and richness, communicates brand as a body of thought rather than a product page.

**Anatomy:**
- Multi-column editorial layout: a wide feature item left, two or three smaller items stacked right.
- Each item: image with consistent art direction, headline, date or category tag, read-time or link.
- Pull quote or large statistic breaks the grid between items.
- Tight typography: headline at 22 to 28px, body at 15 to 16px, line-height 1.6.
- No card borders. Separation through whitespace and typographic hierarchy alone.

**Best for:** content-led brands, magazine posture, any brand that positions its thinking as a product.

## Case Study / Work Grid

**Goal it serves:** social proof, portfolio depth, drives clicks into case study pages.

**Anatomy:**
- 2 to 3 featured cases, full-width or large cards.
- Each case: full-bleed image with consistent treatment, client or project name, one-line outcome statement, category tags.
- Hover reveals a CTA overlay or expands to show a brief.
- Avoid the "logo plus name plus 5 bullet points" pattern. Show the work.

**Expressive variant:** cursor changes to a labeled state ("View case") on hover over each card.

## Product Demo Moment

**Goal it serves:** demonstrates the product without requiring the visitor to install, sign up, or imagine.

**Anatomy:**
- A live or animated representation of the product's core action.
- Can be a video loop, an interactive prototype, an animated diagram, or a screenshot at editorial scale.
- Framed without a laptop or phone device bezel. The UI is the content, not a prop.
- One-line caption beneath explaining what the visitor just saw.

**Expressive variant:** sticky scroll scene. The product UI frame is fixed in the viewport while feature highlights scroll through it.

## Sticky Scroll Scene (Expressive Mode)

**Goal it serves:** demonstrates multiple product capabilities without leaving the viewport. Creates the impression of a deep, considered product.

**Anatomy:**
- Container: position sticky, height: 100vh, displays a fixed product frame.
- Content: a series of panels (each 100vh) that scroll past inside the sticky container.
- As each panel scrolls into view, the product UI transitions to show the relevant feature.
- Implementation: parent has height equal to (number of panels x 100vh). Child product frame is sticky.
- Graceful degradation: without JS, panels display as standard sequential sections.

## Quote / Testimonial Band

**Goal it serves:** trust through specificity, reduces evaluation friction.

**Anatomy:**
- One quote per band. Not a carousel of six.
- Large pull-quote text (28 to 36px, display font or italic body), not body-copy size.
- Attribution: name, title, company, company logo small (16 to 20px tall).
- The quote contains a specific claim, not a vague compliment. "Reduced our deploy time from 45 minutes to 4 minutes" beats "This tool changed our lives."

## Full-Bleed Prefooter

**Goal it serves:** the final conversion push before the footer. Non-negotiable on every marketing page.

**Anatomy:**
- Full-bleed section in the signature color. Lives immediately above the footer.
- Centered or left-aligned: oversized headline, one subhead, one CTA.
- Text in deep ink for contrast.
- Should feel like a poster. It is the last thing a visitor sees before leaving or converting.
- Grain overlay on the surface adds material quality.

## Footer

**Goal it serves:** wayfinding and trust signals, not primary engagement.

**Anatomy:**
- Tight vertical rhythm: link list gap: 2px, link min-height: 28px.
- The 44px touch target does not apply to footer links. They are secondary navigation.
- 3 to 4 columns at most. Each column: small-caps heading plus short link list.
- Bottom bar: copyright, small print, social icons no larger than 16px.

## Typography

**One display family plus one body family.** No third font.

Headline scale: clamp(40px, 6vw, 96px) for hero, clamp(28px, 3.5vw, 48px) for section headings. Type-led hero: clamp(72px, 10vw, 140px).

Body: 16 to 18px, line-height 1.55 to 1.7, 60 to 75 character line length.

Eyebrow/small-caps: 12 to 13px, letter-spacing: 0.08em, uppercase, muted ink.

Tighten display headlines: letter-spacing: -0.02em at large sizes. At 96px and above, adjust manually.

**Variable fonts.** When using a variable font, define axis ranges as tokens:
```css
--font-wght-body: 400;
--font-wght-strong: 600;
--font-wght-display: 800;
--font-opsz-display: 72;
--font-opsz-body: 16;
```

Use the opsz axis if available. It is not decorative; it makes display type more legible at large sizes and body type more readable at small ones.

## Color Discipline

Three roles: ink (near-black), signature (saturated brand color), action (CTA accent).

Surfaces: surface (white), surface-sunken (off-white), surface-raised (white plus shadow for popovers), surface-inverse (deep ink for footer).

Borders: border-subtle (very light), border-strong (mid).

Muted text: one muted gray, not three.

Reserve the signature color for: prefooter band, hero accent mark, one primary CTA per page, nav active state. Nothing else.

## Spacing and Rhythm

Section padding: clamp(80px, 10vw, 160px) vertical, 24px horizontal on mobile, max-content-width 1200 to 1400px desktop.

Primary nav items: 44px min-height (touch target).

Footer links: 28px min-height (secondary).

Card gaps: clamp(16px, 2vw, 24px).

## Composition: Layering and Broken Grid

Use these techniques to break visual monotony and signal craft:

**Layering:** elements that overlap or bleed across section boundaries. Negative top margin, absolute-positioned elements that escape their container, imagery that extends past the section edge.

**Broken-grid moment:** one section per page where elements deliberately violate the column grid. A pull quote at -40px left margin, a number that overflows its card container, a headline that extends past the content-width boundary. Use once. More becomes decoration.

**Asymmetry:** every hero should have visual mass on one side, not balanced across a center axis. Asymmetry creates tension. Tension holds attention.

## Motion

Easing: one custom cubic-bezier across the entire site, bound as --ease (example: cubic-bezier(0.2, 0, 0, 1)).

Durations: 120ms for micro (hover state), 160ms for small UI (chevron, panel open), 240 to 320ms for section transitions.

Scroll reveals: fade plus 12px translate-up on Intersection Observer. Never bounce, never overshoot. Content is visible by default and the reveal is layered on only when JS is present (for example, set a `js` class on the document and scope the hidden initial state to `.js .reveal`). Never leave content at opacity zero waiting on JS, or the page is blank without it.

Marquees: linear, slow (~40s), pause on hover, respect reduced motion.

Header: subtle 1px border-bottom at scrollY > 80. No background flip, no shrink.

## Copy Rules

These matter as much as layout.

Cut every filler adjective. "Small," "dedicated," "passionate," "innovative," "powerful," "modern" are signals that the copy is describing instead of showing. Delete or replace with a concrete noun or specific claim.

Verbs over nouns. "Ship" beats "shipping." "Build" beats "builders."

Specifics over generalities. "End-to-end engagement from brief to launch" beats "full-service."

One eyebrow tag per section, five words or fewer.

CTAs are imperatives with an outcome. "Start an engagement," "See the work," "Read the case study." Never "Learn more" alone, never "Submit," never "Click here."
