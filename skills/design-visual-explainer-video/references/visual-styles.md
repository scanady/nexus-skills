# Visual styles

Pick one style per video and hold it. Each preset gives the image style line for `assets.json`, fonts for `fonts.mjs`, a palette, and motion notes. Adapt the preset to the subject. Do not ship the preset unchanged: build the opening around an object or metaphor from this subject.

A reviewer called AI explainers "flashy slide decks" and "office templates". What makes this skill's output look made, not templated: drawn marks that write on, cut-out art with shadows, motion keyed to words, and a consistent palette. Use at most 2 background colors per video, plus scene-specific paper or tint changes.

## 1. Paper collage (the Reddit "whimsical hand-drawn collage" look)

- **Image style:** "Hand-cut paper collage illustration, torn paper edges with a thin white rim, visible paper grain, warm vintage palette (kraft brown, cream, teal, mustard, tomato red, navy), thick slightly wobbly near-black ink outlines, flat soft lighting, playful and friendly, no text."
- **Backgrounds:** "green" key for every sprite. Draw paper backgrounds in code (`bg()` + `grain`), or generate 1–2 "scene" paper textures.
- **Fonts:** `"Caveat:wght@700" "Nunito:wght@400;800"`, or `"Permanent+Marker"` for stamps.
- **Palette:** ink `#1f1a17`, paper `#f4ecd8`, kraft `#c9a77c`, teal `#2f8f8a`, mustard `#e0a526`, tomato `#d8452f`, navy `#23395b`.
- **Motion:** `pop()` entrances, slight rotations (±0.06 rad), `boil` jitter on sprites (`noise(boil(t,8))*1.5` px), torn-paper `wipe` transitions, stamp + `shake()` + `thud` on key facts, red handwritten annotations with `ink()` arrows.
- **Mascot:** one simple character (a cardboard robot, a paper bird). Generate it once, then use `ref` for every other pose.

## 2. Whiteboard / sketchnote

- **Image style:** "Black marker line drawing on white, clean single-weight strokes, minimal flat color accents in one color, sketchnote style, no shading, no text."
- **Backgrounds:** "green" or "scene" on pure white. Or skip images and draw everything with `ink()`/`arrow()`.
- **Fonts:** `"Patrick+Hand"` or `"Kalam:wght@400;700"`.
- **Palette:** white `#fbfbf8`, ink `#1b1b1b`, one accent (blue `#2d6cdf` or orange `#f06a28`).
- **Motion:** everything writes on (`reveal`), `type` sfx for text, camera pans between areas of one big board (translate in `underlay`), no wipes (use `cut` or a pan).

## 3. Flat vector editorial (Kurzgesagt-adjacent)

- **Image style:** "Flat vector illustration, bold simple geometric shapes, subtle gradients, soft long shadows, rich saturated palette on a deep background, clean edges, no outlines, no text."
- **Backgrounds:** `gradientBg()` deep navy/purple; sprites "green" keyed.
- **Fonts:** `"Poppins:wght@500;800"` or `"Fredoka:wght@500;700"`.
- **Palette:** bg `#1d1b3a`→`#2b2159`, accents `#ffb347`, `#ff6f91`, `#5ee6c4`, `#6fa8ff`, text `#ffffff`.
- **Motion:** smooth `outCubic` / `inOutCubic`, parallax layers (move far layers less), `push` transitions, glow via shadowBlur, no boil.

## 4. Blueprint / technical

- **Image style:** "Technical blueprint illustration, white and light-cyan line art on blueprint blue, precise isometric linework, dimension marks, no text."
- **Backgrounds:** blueprint blue `#1f4e8c` with a code-drawn grid.
- **Fonts:** `"IBM+Plex+Mono:wght@400;600"` + `"IBM+Plex+Sans:wght@600"`.
- **Motion:** lines draw on, labels type on, measured and calm. Best for architecture and codebase explainers.

## 5. Clean product explainer (SaaS)

- **Image style:** "Clean modern 3D-ish illustration, soft clay render, pastel palette, rounded shapes, studio lighting, isolated object, no text."
- **Backgrounds:** light `#f6f7fb`; UI panels drawn in code with `rrect` (never generate UI screenshots with text in them).
- **Fonts:** `"Inter:wght@400;700"` or `"Plus+Jakarta+Sans:wght@500;800"`.
- **Motion:** crisp `outQuint`, cards that slide and stack, cursor or highlight to guide the eye, `fade` transitions.
- For real product UI, use real screenshots put in `assets/extra/`: copy them from the project's `shared/screenshots/` when it has them (check `rights` in `shared/assets.json`), and consider the `design-product-overview-recorder` skill for live recordings.

## 6. Chalkboard

- **Image style:** "White and pastel chalk drawing on a dark green chalkboard, dusty chalk texture, hand-drawn, no text."
- **Fonts:** `"Gochi+Hand"` or `"Schoolbell"`.
- **Palette:** board `#2e4a3a`, chalk `#f2f2ea`, pastel yellow/pink/blue.
- **Motion:** write-on everything, higher `wobble` (3–4), `grain` 0.08.

## Explaining a real product or brand

- Match the brand instead of picking a preset. Read the site's CSS for its color variables and `font-family` values, and screenshot the site to see the look.
- Use the brand's own photos where they fit: put them in `assets/extra/` (resized to ≤ 1920 px) and draw them with a cover-fit photo helper. They show the real product, which no model can.
- Generate only the shots the brand does not have. To keep the product and the look consistent, save a 1024 px PNG of a brand photo as `assets/raw/<id>.png` and list that id in the image's `ref`.
- Brand photos have rights. Record which ones you used in the delivery README, and tell the user to confirm usage before publishing.

## Image generation rules

- One `style` line in `assets.json` for the whole video. Put subject detail in each image's `prompt`.
- Ask for no text in images. Put all words on screen with `text()`: generated text is often misspelled, and code text stays sharp and editable.
- Sprites (characters, objects): `"background": "green"`, `"aspect": "1:1"`. Full backgrounds: `"background": "scene"`, `"aspect": "16:9"`.
- Character consistency: generate the hero pose first. Then give every other pose `"ref": ["hero-id"]` and describe only the change ("same robot, now waving").
- Keep the count low: 4–10 images for a 60 s video. Code-drawn shapes, arrows, charts, and diagrams are free, sharper, and animate better. Diagrams must always be code.
- Look at every generated image (open the PNG) before you use it. Reject hands with wrong finger counts, garbled pseudo-text, wrong subject, or a green fringe. Regenerate with a changed prompt, at most once per image, then simplify the composition.
- Charts and numbers are code (`rrect`, `ink`, `text`), never generated images.
