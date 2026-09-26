# Engine API for scenes.js

`build.mjs` joins `assets/player.html` + `assets/engine.js` + the job's `scenes.js` into one self-contained `out.html`. You write **only `scenes.js`**. Do not edit `engine.js` for a single video.

`assets/example/scenes.js` is a complete, working example. Copy its patterns, not its content.

## The one rule: pure function of time

Every frame is `drawFrame(t)`. The renderer draws frames out of order and in parallel browser pages. So:

- Compute every position, opacity, and size from `t`. Keep no state that changes between frames.
- Do not use `Date.now()`, `performance.now()`, `setTimeout`, `requestAnimationFrame`, CSS transitions, or DOM elements. The engine replaces `Math.random()` with a seeded version and logs an error when you call it. Use `rng(seed)` or `noise(x)`.
- Precompute expensive things once, at the top level or in an optional `async function setup() {}`. For example: offscreen canvases or a pre-rendered texture. The engine calls `setup()` after it loads images and fonts.

## Globals you can use

| Name | Meaning |
|---|---|
| `W`, `H`, `FPS`, `DUR` | Canvas size, frame rate, video length in seconds (from `timeline.json`) |
| `ctx` | The 2D canvas context. Use it directly for anything the helpers do not cover |
| `DATA` | Build data: `DATA.fontFamilies` (order from `fonts.mjs`), `DATA.seed`, `DATA.title`, `DATA.cues` |
| `IMAGES` | Loaded images by id (`IMAGES.robot`), from `assets/<id>.png` and `assets/extra/*` |
| `CUES` | `[{start, dur, text, words:[{w, t}]}]`, one entry per narration line |
| `END` | The time the last word ends |

## Timing: key everything to the narration

| Function | Returns |
|---|---|
| `at(line, "word", nth = 1)` | The time the nth occurrence of `word` is spoken in line `line` (0-based). Case, accents, and punctuation are ignored. A miss logs a console error that `lint.mjs` reports |
| `lineStart(i)`, `lineEnd(i)` | The start and end of line `i` |
| `seg(t, a, b)` | Progress 0→1 of `t` through `[a, b]`, clamped |
| `within(t, a, b)` | `a <= t < b` |
| `pop(t, start, len = 0.45)` | outBack entrance curve 0 → overshoot → 1 |
| `fadeIO(t, a, b, f = 0.3)` | Fade in at `a`, fade out at `b` |

Never write literal seconds for story beats. Literals desync as soon as a voice, a line, or a pause changes. Derive every time from `at()`, `lineStart()`, or `lineEnd()`, plus small offsets.

When `cues.json` says `"timing": "estimated"` (OpenRouter and Gemini TTS give no word timestamps), word times can be off by about 0.2–0.4 s inside a line. Line starts and ends are exact. Key the big beats to line boundaries or to long, stressed words.

## Scenes

```js
scene({
  name: "mechanism",
  start: lineStart(2) - 0.3,            // absolute seconds
  end: lineEnd(3) + 0.4,
  bg: "#e7f1f4",                        // optional flat background
  transition: "wipe",                   // "fade" (default) | "wipe" (torn paper) | "push" | "cut"
  tlen: 0.6,                            // transition length; overlap the previous scene by at least this much
  draw(t, local, s) { /* t = absolute time, local = t - start */ },
});
```

- Put scene changes in the pause before a line, not on its first word: a boundary at `lineStart(k) - 0.45` with a 0.7 s transition finishes just as line `k` begins. A boundary at `lineStart(k)` makes the new scene's first text fade in over the old scene's text.
- The incoming scene draws over the outgoing scene during the overlap. Make each scene's `start` at least `tlen` before the previous scene's `end`. A gap between scenes shows black frames, and `lint.mjs` reports it as an error.
- `underlay(fn)` draws `fn(t)` under every scene. `overlay(fn)` draws `fn(t)` over every scene (captions, a logo bug, a progress bar).
- `FINISH` controls the frame finish: `{grain: 0.05, vignette: 0.3, fadeIn: 0.4, fadeOut: 0.7}`. Set a value to `0` to turn that effect off.
- Camera: a slow drift is always on. `CAM.drift = 0` turns it off. `shake(time, amp = 10, len = 0.35)` adds an impact shake.

## Drawing helpers

| Helper | Notes |
|---|---|
| `text(str, x, y, {font, size, weight, italic, color, align, baseline, maxWidth, lineHeight, reveal, alpha, stroke:{width,color}, rot})` | Wraps at `maxWidth`. `reveal` 0..1 types it on. Returns `{w, h, lines}`. **Always use this for on-screen words**: lint checks only text drawn with `text()` |
| `measure(str, {font, size, maxWidth})` | Width in pixels, for layout before drawing |
| `tracked(ls, fn)` | Runs `fn` with letter spacing `ls` (`"3px"` for mono labels, `"-2px"` for tight headlines) and restores it. **Never set `ctx.letterSpacing` directly**: Chromium can read it back as `""` inside `save()`, writing `""` back is ignored, and the tracking leaks into every later text |
| `img(id, x, y, {w, h, anchor:[0.5,0.5], rot, scale, alpha, shadow:{blur,x,y,color}, clip})` | Draws an image asset. `clip` 0..1 reveals it left to right |
| `cover(id, x, y, w, h, {r, zoom, px, py, dim, alpha, shadow})` | Cover-fits a photo into a (rounded) box. Animate `zoom` from 1.02 to 1.1 over the scene for a slow push-in. `px`/`py` (0..1) choose the crop focus |
| `ink(points, {t, reveal, width, color, wobble, boilFps, seed, passes, alpha})` | Hand-drawn polyline that writes on. Pass `t` so the line "boils" at `boilFps` |
| `arrow(x1, y1, x2, y2, {reveal, bend, head, ...ink options})` | Curved hand-drawn arrow |
| `highlight(x, y, w, h, {reveal, color, alpha})` | Marker swipe. Draw it before the text it sits under |
| `rrect(x, y, w, h, r, {fill, stroke, lineWidth, alpha, shadow})`, `circle(x, y, r, {...})` | Shapes |
| `bg(color)`, `gradientBg(c1, c2, angle)` | Full-frame fills |
| `captions(t, {y, size, color, active, box, font, maxWords})` | Burned-in, word-highlighted captions. Call it from `overlay()`. The MP4 also gets a soft caption track, so burned-in captions are optional. Use them for social or muted autoplay |
| `ease.*` | `linear`, `inCubic`, `outCubic`, `inOutCubic`, `outQuint`, `outBack`, `outElastic`, `inOutSine` |
| `lerp`, `clamp`, `noise(x, seed)` (smooth −1..1), `rng(seed)`, `boil(t, fps)` (stepped time) | Math |

Fonts: `DATA.fontFamilies[0]` is the first family passed to `fonts.mjs`, and so on. With no fonts, the engine uses the system sans-serif, which looks generic, so always embed fonts.

## Sound

| Function | Notes |
|---|---|
| `sfx(time, kind, {gain, pitch})` | Kinds: `pop click tick whoosh swoosh ding chime thud sparkle riser boom type`. `riser` takes `{len}`. `type` takes `{count, every}` |
| `music({bpm, key, mood, level})` | Turns on the built-in synth bed. Moods: `bright`, `calm`, `serious`, `mysterious`. `mix.mjs` uses it only when `EXPLAINER_MUSIC_PROVIDER=synth` |

Put one sound on every visual event: pops for entrances, a whoosh for flights and wipes, clicks and type for write-ons, a thud with `shake()` for stamps, a chime or ding for success moments. Vary `pitch` (0.8–1.3) on repeated pops so they do not sound mechanical. Keep SFX sparse under speech. `mix.mjs` sets the final levels.

## Hooks the scripts use (do not call them yourself)

`window.__ready`, `__render(t)`, `__renderAudio("sfx" | "music")`, `__meta`, `__text()`, `__active(t)`, `__sfx()`, `__canvas`.

## Common defects and fixes

| Defect | Fix |
|---|---|
| Label sits on top of another label or the title | Lay out with `measure()`. `lint.mjs` flags overlaps |
| Text leaves before it can be read | Hold it at least `1 s + 0.33 s × words`. `lint.mjs` flags it |
| Empty frames at the start of a scene | Draw something from the scene's first frame. Build up detail on the words |
| Everything moves at once | One focal motion at a time. Stagger entrances by 0.08–0.15 s |
| A loop or strip runs out of content | Draw 3 repeats and scroll modulo one repeat width |
| A sprite pops in with a hard edge | Use `pop()` scale plus alpha, and add a `shadow` to cut-outs |
| An `at()` miss | The word is not in that line (check the line index, which is 0-based) or it is spelled differently. Read the console error |
