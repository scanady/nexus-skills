# Verification Checklist

Run before declaring a page done. Work through all three sections: concept, automated, and human judgment. A page that passes automated and fails concept is not done.

## Concept and Art Direction

These checks catch the failures that Lighthouse cannot.

- [ ] At least two structurally different concept directions were considered before committing, with a recorded reason each rejected one was set aside. If only one direction was ever on the table, the first-idea risk is unmanaged.
- [ ] The concept statement is written down in one sentence. If not, the concept has not been derived. Go back to step 2.
- [ ] The concept is expressed in at least three distinct design decisions (type choice, one interaction or motion model, one layout moment). Identify all three before shipping.
- [ ] There is one signature moment that would not appear in any competitor's site or in any Framer, Webflow, or template marketplace. Name it.
- [ ] The type choice was auditioned against the concept, not pulled from the reference pool because it was listed. Set it at hero scale and body scale. If the answer is Satoshi, Inter, DM Sans, or Geist, confirm the justification ties to the concept. "It looks good" is not a justification.
- [ ] The design is not predictable from an archetype label alone. If naming the archetype lets you guess the type, motion, and layout, the archetype steered the work and the brand did not. Push further.
- [ ] No decision traces back to "the reference suggested it" rather than "the concept required it." Replace any that do.
- [ ] Cover the logo and brand name. Could this page belong to any competitor, or does it resemble a recognizable named site? If yes, the concept is not executing or the work is imitating. Find where it breaks down.
- [ ] The motion model matches this concept's emotional register, judged against the concept statement and not against what the archetype is "supposed to" look like.
- [ ] The imagery treatment is consistent across every image on the page. Mixed treatments mean no decision was made.
- [ ] The copy register matches the posture. Read every headline aloud. If any sounds like a SaaS template, rewrite it.

## Render and Critique Gate

This gate is mandatory. A page is not done until it has been rendered, looked at, and iterated. Source review cannot catch what only appears in pixels. Full protocol in `references/render-and-critique.md`.

- [ ] The page was built, served, and screenshotted at 360, 768, 1280, and 1440 (use `assets/screenshot.mjs`).
- [ ] The screenshots were opened and actually examined, not assumed.
- [ ] No section renders empty or near-empty. No tall blank bands. (This is the failure that source review misses most often.)
- [ ] No gray placeholder boxes, broken images, or visible alt text standing in for a missing visual.
- [ ] With JavaScript disabled, all content is still visible. Reveal and entry animations enhance content; they never hide it. (This is the flaw where every section sits at opacity zero waiting on JS.)
- [ ] Vertical spacing is not blown out: no enormous inter-section gaps, hero does not push everything below the phone fold, footer sits directly below content.
- [ ] A signature moment is visible in the render and can be named while looking at it.
- [ ] The logo-cover test was applied to the actual screenshot, not to the source.
- [ ] At least one fix-and-re-render iteration was performed. First renders are drafts.
- [ ] If no real browser could be obtained: a static-rasterizer smoke test was run for structure only, AND the page was explicitly marked a draft and the user told it is not yet verified in a real browser. A page never rendered in a browser does not pass this gate.

## Automated

Run what applies to the project's stack. Detect the stack first; do not run framework commands on a project that does not use that framework.

- [ ] Typecheck passes if the project uses TypeScript (`npx tsc --noEmit`). Skip if not.
- [ ] Build passes using the project's actual build command (`npm run build`, `vite build`, or none for a static HTML file). Do not assume Next.js.
- [ ] Lighthouse on the served page: Accessibility ≥ 95, Performance ≥ 90 on mobile.
- [ ] LCP < 2.5s, CLS < 0.1, INP < 200ms.
- [ ] No console errors on initial load. For React, no hydration warnings.
- [ ] All interactive elements have visible :focus-visible styles (tab through and confirm in the render; no missing rings).
- [ ] At 360px viewport: nothing overflows horizontally, type scales down, nav collapses to drawer.
- [ ] With prefers-reduced-motion: reduce: marquees stop, scroll reveals are instant, entry sequences skip to final state, no auto-rotating content.
- [ ] Images are optimized for the stack and sized: explicit width and height (or aspect-ratio), hero eager, below-fold lazy. Use `next/image` only on Next.js; use `loading="lazy"` and `decoding="async"` on plain `<img>`.
- [ ] No hotlinked stock or placeholder-service image URLs. Visuals are authored or user-provided per `imagery-and-visuals.md`.
- [ ] All buttons and links have descriptive accessible names (no "Click here," no icon-only without aria-label).
- [ ] aria-current="page" is set on the active nav route.
- [ ] Skip-to-content link is the first focusable element on the page.
- [ ] Color contrast ≥ 4.5:1 for body text, ≥ 3:1 for large text and UI elements, verified on the rendered colors.

## Hover Navigation

- [ ] Click a trigger: data-open flips to "true," panel becomes visible, chevron rotates.
- [ ] Hover in a real browser: opens immediately; cursor crosses gap to panel; menu stays open; cursor away closes after ~140ms.
- [ ] Tab key: focus reaches trigger, opens menu; Tab continues through items in order; Escape closes; focus returns to trigger.
- [ ] Click outside the nav: open menu closes.
- [ ] At below 768px: drawer mode active, tap toggles, hover suppressed.

## Human Judgment

These require a person to look, not a tool.

- [ ] The headline is the first thing the eye lands on. Not the logo, not the nav, not the CTA button.
- [ ] There is one accent mark on a key word in the hero, executed with the same technique used consistently across the site.
- [ ] The page has at least one full-bleed section (prefooter, stat band, or marquee).
- [ ] No two consecutive sections share the same layout pattern.
- [ ] The signature color appears in four places or fewer: prefooter, hero accent mark, one primary CTA, nav active state.
- [ ] Footer feels tight: link rows close together, not airy.
- [ ] CTAs are imperative and outcome-oriented. No "Learn more" alone, no "Submit," no "Click here."
- [ ] Every image carries the same treatment (one grade, one duotone, one overlay). No mixed treatments.
- [ ] Surfaces are off-white and layered, not pure white. Text uses an ink scale (headline, body, muted), not a single black. No pure #000 or #fff doing real work.
- [ ] A grid is evident, and the one broken-grid moment reads as deliberate against it rather than as a mistake.
- [ ] Read every sentence aloud. If any sentence sounds like a SaaS template, rewrite it before shipping.
- [ ] The page makes you stop and notice one moment that would not appear in any template. If you cannot identify that moment, the concept is not executing. Go back.

## Expressive Mode (Additional Checks)

Run these only when operating in expressive mode.

- [ ] Entry sequence is present and coordinated. Does not block interactivity. Respects prefers-reduced-motion.
- [ ] Scroll-linked choreography works correctly at normal scroll speed and fast scroll speed. No layout jitter or CLS.
- [ ] Custom cursor degrades gracefully on touch devices. Touch users never see the custom cursor.
- [ ] View transitions (if implemented) do not flash or produce layout shift on slow connections. Test with network throttling.
- [ ] Kinetic type is used once and has a clear relationship to the concept. If it appears more than once, reconsider.
- [ ] Any WebGL or canvas element loads asynchronously and does not block LCP.
- [ ] Sticky scroll scene (if used) works on 360px mobile viewport. Fallback is a standard section sequence.

## Goal Alignment

- [ ] The primary goal of the page is declared in one sentence.
- [ ] Every section ties to one of the three goal tiers (conversion, engagement, return).
- [ ] The primary CTA is reachable in the first viewport on mobile without scroll.
- [ ] The prefooter contains the same primary CTA (last chance before footer).
- [ ] No more than two primary-weight CTAs total on the page.

## Stop Conditions

If all checks pass: ship.

If the concept checks fail: return to workflow step 2. The automated and human checks are not replacements for a clear concept; they are quality gates around one.

If any automated check fails below 90: investigate before shipping. A slow or inaccessible site communicates the same thing as a generic one: the team did not finish the job.
