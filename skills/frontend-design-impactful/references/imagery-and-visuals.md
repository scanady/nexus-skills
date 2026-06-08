# Imagery and Visuals

The hardest problem for a model-built site and the most common reason output looks unfinished rather than award-caliber. A model has no photographer, illustrator, or stock library. Left unaddressed, it ships empty bands, gray placeholder boxes, or broken image links where a designer would have placed a commissioned visual. The failure is unmistakable in a render: strong type sections separated by large empty voids where visuals were expected. This reference exists to make that outcome impossible.

## The Iron Rule

Every section earns its height. No section ships empty, and no section ships a bare placeholder box. If a section has nothing to show, it has no reason to occupy vertical space. Either fill it with a visual the model can actually author, fill it with a typographic or structural composition, or remove the section. A tall band of blank surface is the single most damaging thing this skill can output, more damaging than a generic layout, because it reads as broken rather than merely safe.

## Visual Source Hierarchy

Work down this list. Use the highest available tier for each visual need.

1. Real assets the user provided: product screenshots, logos, photography, brand illustration. Use them, apply one consistent treatment, never stretch or distort.
2. Visuals the model can genuinely author in code. This is the workhorse tier, and most award-caliber model output lives here. See the catalog below.
3. Honest, art-directed placeholders, only when a real photograph or illustration is genuinely required and unavailable. Never a gray box. A placeholder is a designed element (a captioned frame, a typographic panel, a labeled diagram region) that looks intentional and states exactly what asset belongs there. Flag every one to the user.

Never use hotlinked stock URLs, lorem-ipsum image services, or random Unsplash links. They break, they look generic, and they undercut the concept.

## What the Model Can Author Well

Build these instead of sourcing photos. Each is fully within reach in HTML, CSS, and SVG, and several are exactly what separate a designed page from a wireframe.

**Typographic compositions.** Oversized headline treatments, pull quotes set as art, large numerals, kinetic word lists, vertical or rotated labels, a manifesto set as a full-bleed type panel. Type is the most reliable award-caliber visual a model produces, and it never renders as a void.

**CSS gradient and mesh fields.** Layered radial and linear gradients, soft mesh backgrounds, duotone washes behind a section, paired with grain from an SVG feTurbulence filter for depth. Strong behind a hero or prefooter.

**SVG diagrams and systems art.** Orbit and node diagrams, process flows, concentric systems, connected graphs, data-driven shapes. These read as bespoke and on-concept. A diagram card built this way is a genuine signature-moment candidate.

**Product UI built in HTML and CSS.** Render a believable slice of the actual product in markup rather than pasting a screenshot: a dashboard fragment, a chat thread, a code block, a settings panel. Frame it without a laptop or phone bezel. Crisper than any screenshot and it demonstrates the product directly.

**Geometric and abstract compositions.** Grids of shapes, layered cards, halftone fields, line systems, masked type. Tie the geometry to the concept rather than decorating with it.

**Treated photography, when real photos exist.** Apply one grade across all of them: duotone via SVG or blend modes, matte grade, high-contrast black and white, or a brand-color overlay.

## Treatment Consistency

Whatever the source, every image on a page receives one treatment. Mixed treatments are the tell of no decision. Derive the treatment from the concept (a cold, precise grade for a precision concept; a warm matte for a human one) and apply it everywhere, including authored visuals where it fits.

## Flagging Asset Needs

When a real asset is genuinely required and unavailable, do not fake it and do not leave a void. Build the art-directed placeholder and tell the user in plain language: which section, what asset is needed, what dimensions and treatment, and why. A page delivered with three clearly-marked, designed asset slots is finished work. A page with three gray voids is not.
