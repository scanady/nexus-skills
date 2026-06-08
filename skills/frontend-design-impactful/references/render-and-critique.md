# Render and Critique

A model cannot see what it builds. It emits HTML and CSS and never perceives the rendered pixels, so every visual judgment in this skill (the logo-cover test, spacing, contrast, whether a section is empty, whether the thing is actually good) is unverifiable from source alone. This reference closes the loop: build the page, render it, look at it, critique it against the concept, fix, and repeat. This step is what turns the quality bar from an aspiration into something enforced. Do not declare a page done without it.

## The Loop

1. Build and serve. Get the page rendering locally. For a static build, that is the HTML file directly. For a framework, start the dev or preview server.
2. Capture. Use Playwright to screenshot the full page at four widths: 360, 768, 1280, 1440. Paste-ready script in `assets/screenshot.mjs`.
3. Look. Open every screenshot with the view tool and actually look at it. This is the step that was missing.
4. Critique against the rubric below. Write down every defect.
5. Fix the defects in code.
6. Re-render and repeat until the page passes. Expect two to four iterations. First renders are never the finished work.

## Getting a Browser

A real browser engine is what makes this loop trustworthy, but it is also the dependency most likely to fail in a locked-down environment. Work down this list and use the first that succeeds. `assets/screenshot.mjs` already tries the bundled browser first and then a system Chrome channel, so usually you just need one of these to have put a browser on the machine.

1. Playwright's own chromium: `npm i -D playwright && npx playwright install chromium`. The normal path.
2. With OS dependencies, if the first install runs but the browser will not launch: `npx playwright install --with-deps chromium`.
3. A system browser already on the machine. The script falls back to `channel: "chrome"`, so installing or pointing at Chrome, Chromium, or Edge is enough. No separate download needed.

```bash
node assets/screenshot.mjs http://localhost:3000 ./.screens   # framework dev server
node assets/screenshot.mjs file:///absolute/path/to/index.html ./.screens   # static file
```

## When No Browser Engine Is Available

If none of the above works (a sandbox with no installable browser, no network to a binary source), do not silently skip the loop and declare the page done.

- Run a structural smoke test with a static rasterizer such as WeasyPrint (`pip install weasyprint`, render to PDF, convert with `pdftoppm -png`). This catches the structural-integrity half of the rubric: empty bands, blown-out spacing, contrast, broken layout, missing copy. It does not run JavaScript and only partially supports modern CSS, so it cannot judge motion, responsive media queries, or JS-driven state, and it must be treated as a smoke test, never the real render. To use it on a page with JS-gated reveals, neutralize them first (force the revealed state visible) or the static render will show hidden content.
- Then tell the user plainly: the page has not been verified in a real browser, what the smoke test did and did not cover, and that they should run the loop locally before treating the page as finished. Mark the deliverable as a draft pending a real render.
- A page that has never been rendered in a real browser is not done. Say so rather than implying otherwise.

## The Critique Rubric

Open the rendered screenshots and judge in this order.

**Structural integrity first**, because these failures make output look broken rather than merely generic:
- Is any section empty or near-empty? Any tall band of blank surface with no content is a failure. Fill it or cut it. See `imagery-and-visuals.md`.
- Is there any gray placeholder box, broken image, or visible alt text standing in for a missing visual?
- With JavaScript disabled, is all content still visible? Reveal and entry animations must be progressive enhancement, never the only thing that makes content appear. If sections vanish without JS, the animation is hiding content rather than revealing it.
- Is vertical spacing blown out anywhere? Enormous gaps between sections, a hero that pushes everything below the phone fold, a footer floating far below the content.
- Does anything overflow horizontally at 360px? Does the layout reflow cleanly at every width?
- Is text contrast actually readable on the rendered colors, not just in theory?

**Then concept and craft:**
- Cover the logo in the screenshot. Could this be a competitor, or a site you have seen before? If yes, the concept is not executing on the page as rendered.
- Did type render at the intended scale and weight with designed line breaks, or did it come out smaller and blander than specified?
- Is a signature moment visible in the render? Point to it. If you cannot find it in the screenshot, it is not there.
- Do the rendered color, spacing, and density match the concept's register, or did they drift toward default?
- Read the headlines as rendered. Do any sound like a template?

A page passes when structural integrity is clean at all four widths and you can name the signature moment while looking at the screenshot.

## Why Iteration, Not One Pass

The distance between a first generation and award-caliber work is iteration with sight. A designer does not ship the first comp. The render, look, fix loop is how taste gets applied to output the model cannot otherwise perceive. Budget for it, and treat the first render as a draft to critique, never as the deliverable.
