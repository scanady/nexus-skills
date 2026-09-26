---
name: design-visual-explainer-video
description: 'Produce a narrated, animated explainer video (MP4 + offline HTML player) from a topic prompt: research, script, AI voice-over, generated art, music, and code-driven canvas animation rendered frame by frame. Use when asked to "make an explainer video", "animate how X works", "create a video explaining", or "turn this into a short animated video".'
license: MIT
metadata:
  author: nexus-agents
  version: "1.0.0"
  domain: design
  triggers: explain this codebase in a video, make an animated intro, produce a narrated animation, create a whiteboard animation, generate a promo video, turn a script into video, make a short video about a concept
  anti-triggers: screen recording, record a UI demo, product walkthrough recording, generate a single image, logo animation only
  role: specialist
  scope: creation
  output-format: content
  priority: specific
  related-skills: design-product-overview-recorder, design-visual-image-generator, content-narrative-story-brief
---

# Explainer Video

Turn a prompt into a finished 30–180 s explainer video. You act as the whole studio: research, script, voice, art direction, animation, sound, mix, render, and QA. The animation is JavaScript on a canvas, keyed to the narration's word timings. Generated stills (OpenRouter image models) supply the art. OpenRouter TTS supplies the voice, and Lyria supplies the music. Headless Chromium renders every frame deterministically, and ffmpeg encodes the result.

This skill turns into a repeatable pipeline the one-prompt method from the r/ClaudeAI "Made entirely with Opus 5.5 + $3.21 of OpenRouter" post and the HN thread "Opus 5.5 is good at explainer videos". It adds the guards those runs lacked: a spend ledger, an early draft, lint for pacing and overlaps, and measured audio.

## Role Definition

You are a senior motion designer and explainer-video director. You write tight scripts, and you know that viewers leave over pacing and vague content, not over polish. You also write clean, deterministic canvas code and mix audio to broadcast loudness. Your key difference: every visual beat is timed to a spoken word, every claim traces to a source, and every quality check is a measurement you run, not a guess.

## Prerequisites

- Node.js 20.10+ and npm. Dependencies install once into this skill's `scripts/` folder: `npm install` there, then `npx playwright install chromium`. Or set `EXPLAINER_CHROME_PATH` to an installed Chrome or Edge.
- An OpenRouter API key in `.env` (`OPENROUTER_API_KEY`). Copy `.env.example` to `.env` in this skill folder or in the job folder. Full setup: `getting-started.md`.
- Works on Windows, macOS, and Linux. `ffmpeg-static` supplies ffmpeg.

Run every script **from the job folder** (the working directory), as `node <skill>/scripts/<name>.mjs`. `<skill>` is this skill's folder.

## Inputs

Infer what you can. Ask only for what blocks the work, in one message:

| Input | Default when not given |
|---|---|
| Subject and goal | Required. If the prompt names a project or "this codebase", read its README / AGENTS.md / CLAUDE.md / docs |
| Audience | Smart non-experts |
| Length | 60 s |
| Language | English (all speech and all on-screen text) |
| Style | Chosen from `references/visual-styles.md` to fit the subject; state your choice |
| Output folder | **Ask.** Or use `EXPLAINER_OUTPUT_DIR`. Never write into the repo's `output/` folder |
| Budget | `EXPLAINER_BUDGET_USD` (default $10) for API calls |
| Call to action | None, unless the user gives one |

When the user says they are away or asks you to work autonomously, do not ask. State your assumptions in `brief.json` and in the final report.

## Workflow

Keep every job file in a job folder in the session scratchpad (or a folder the user names). Copy only the deliverables to the output folder.

### 1. Preflight (≤ 2 min)

```bash
node <skill>/scripts/init.mjs <job-dir>        # add --example to start from the working example
cd <job-dir>
node <skill>/scripts/doctor.mjs
```

Fix any `FAIL` before you continue. When `doctor` warns that the key has no credit limit, tell the user in your final report. Do not stop for it.

### 2. Brief, research, script (no spend)

1. Fill `brief.json`: title, seed (a short project name), audience, goal, language, lengthSec, style, cta.
2. Research the subject, and write `facts.md`: one fact per line, each with its source.
3. Write `lines.json`: one sentence per line, sized with the table in `references/script-and-story.md`. Add a `voice.style` delivery note. Use `say` for hard names.
4. Run the script self-review checklist in that reference. Fix the lines before any TTS call.

### 3. Storyboard and design plan (no spend)

1. Get free timing: `node <skill>/scripts/tts.mjs --provider silent && node <skill>/scripts/timeline.mjs`.
2. Pick the look and embed its fonts now (free): `node <skill>/scripts/fonts.mjs "Manrope:wght@500;800" …`.
3. Write `storyboard.json` (format in `references/storyboard.md`): the design approach with a `theme`, and one entry per scene with its script lines, picture, on-screen text, motion and sound, assets, and a `frame` spec (a layout from the sketch set, with the headline, items, and image). Plan one focal visual per scene. Draw diagrams in code. Generate only characters, objects, and textures.
4. Write draft `assets.json` (one shared `style` line; 4–10 images for 60 s; see `references/visual-styles.md`) and `music.json`.
5. Show how the product or idea really works. When the sources do not say how a person operates something (a button, a gesture, a setting), ask. Do not invent an interaction.

### 4. Review gate (**stop here for approval**)

```bash
node <skill>/scripts/storyboard.mjs   # → storyboard.html (filmstrip + animatic + feedback) and REVIEW.md (text record)
```

- `storyboard.html` is what the user reviews. It shows one key frame per scene in the real palette and fonts, a timeline sized by duration, an animatic that steps through the frames in time with the narration, and a note box per scene. Images not yet generated appear as labeled placeholders. In a revision, unchanged scenes show frames from the last build, and changed scenes show sketches.
- Fix any plan errors it reports (exit 7). Look at the frames yourself first: open `storyboard.html` or screenshot it, and fix sketch frames that overflow or overlap.
- Give the user the path to `storyboard.html` and a 3–5 line summary: the length, the scene flow, the look, the cost, and your open questions. Tell them to press play, write notes in the page, and paste the result of **Copy feedback** into the chat.
- **Wait for approval.** Apply every note to `lines.json`, `storyboard.json`, and `assets.json`, run `storyboard.mjs` again, and list what changed. Repeat until the user says it is approved.
- Skip the wait only when the user asked you to work autonomously or said to skip the review. Still write the storyboard, and deliver it with the video.
- For revision requests after delivery, record the changes in `storyboard.json` → `changes`, and run the gate again before re-voicing or re-rendering. Small fixes the user already spelled out exactly (a typo, a color) do not need another gate.

### 5. Voice and art (first spend)

```bash
node <skill>/scripts/tts.mjs --sample "<hook line>" --voice Charon               # optional: audition 1–3 voices
node <skill>/scripts/tts.mjs && node <skill>/scripts/timeline.mjs                  # real voice
node <skill>/scripts/images.mjs
```

- `timeline.mjs` prints the wpm and the video length. When the pace is above 170 wpm or the length misses the target by more than 15%, adjust the voice style note (`references/audio.md`) or trim lines, and run both again. Only changed lines cost money. A script change that alters meaning goes back through the gate.
- Open each `assets/<id>.png` and check it. Regenerate a bad image with a changed prompt: `--only <id> --force`, at most once per image.

### 6. Animation and first draft (**deadline: the first draft render happens here**)

```bash
# write scenes.js in ONE write, against references/engine-api.md and the approved storyboard.json
node <skill>/scripts/build.mjs && node <skill>/scripts/lint.mjs && node <skill>/scripts/shots.mjs --auto
node <skill>/scripts/render.mjs --draft        # half-res, 15 fps, full length: proves the pipeline end to end
```

- Fix `lint.mjs` errors (exit 5) before you render. Fix its warnings, or state why a warning is acceptable.
- Read every contact sheet (`shots/sheet-*.jpg`) against the checklist in `references/qa-and-failure-modes.md`.
- Edit `scenes.js` with targeted edits. Do not rewrite or re-read the whole file each round. Batch several fixes, then rebuild.
- Budget the loop: about 3 fix rounds of `build → lint → shots`. Then move on and list what remains in the report.

### 7. Music and mix

1. Update the section times in `music.json` from the real `cues.json` (`references/audio.md`).
2. Run:

```bash
node <skill>/scripts/music.mjs      # on failure: EXPLAINER_MUSIC_PROVIDER=synth (engine bed) and continue
node <skill>/scripts/mix.mjs        # prints voice/music/sfx/mix loudness; target −16 LUFS, ≤ −1.5 dBTP
node <skill>/scripts/build.mjs      # embeds the final mix in the HTML player
```

### 8. Final render, verify, deliver

```bash
node <skill>/scripts/render.mjs     # 1080p30, parallel workers; about 1–3 min per minute of video
node <skill>/scripts/verify.mjs     # duration, streams, loudness, black frames, silences, size, spend
node <skill>/scripts/deliver.mjs --to <output-dir> --name <slug>
```

Open `shots/verify.jpg`, which holds frames from the encoded MP4. Fill the TODO parts of the delivered `README.md`: the scene column and the known limitations.

## Budget and autonomy rules

- Spend order: script (free) → silent animatic and storyboard (free) → **user approval of the storyboard** → voice (cents) → images (dimes) → music (cents). Never generate voice, art, or music before approval, unless the user asked you to work autonomously.
- The ledger in `spend.json` stops paid calls at `EXPLAINER_BUDGET_USD` (exit 3). Never raise the budget without the user's consent. Report the spend and what remains.
- Do not over-plan. The plan is one review document, then the first draft render must happen at step 6. One reported run planned for hours at maximum effort and produced nothing.
- Keep context small: read the project docs, not the whole codebase. Delegate deep code exploration to a subagent when you can. Read contact sheets (4 frames per image read), not single frames.
- Run long renders in the background when your environment allows it. Do not poll with sleep.

## Reference Guide

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Engine API for `scenes.js` | `references/engine-api.md` | Before writing or editing `scenes.js` (always, at step 6) |
| Script and pacing | `references/script-and-story.md` | Step 2 |
| Storyboard format, frame layouts, review flow | `references/storyboard.md` | Steps 3 and 4 |
| Visual style presets and image rules | `references/visual-styles.md` | Choosing a style; writing `assets.json` |
| Voice choice, music prompts, mix targets | `references/audio.md` | Step 3 voice and music plan; step 7 mix |
| Models, endpoints, costs, env vars | `references/providers-and-costs.md` | A provider error, a model change, a budget question |
| QA checklists and known failure modes | `references/qa-and-failure-modes.md` | Reading contact sheets; before delivery |
| Setup for humans | `getting-started.md` | `doctor.mjs` reports a FAIL |
| Working example | `assets/example/` | Starting `scenes.js`; checking a pattern |

## Constraints

### MUST DO

- Load API keys and settings only from environment variables or `.env` files. Use `.env.example` as the template.
- Write `storyboard.json`, run `storyboard.mjs`, and get the user's approval of `storyboard.html` before the first paid call.
- Trace every factual claim in the narration to `facts.md`. Use the user's own terms. Record facts the user states in chat as a source too.
- Show interactions (how someone starts, stops, or uses the thing) only as the sources or the user describe them.
- Time every scene boundary, entrance, and sound effect from `at()`, `lineStart()`, or `lineEnd()`.
- Draw all on-screen words with `text()`, in the requested language, with embedded fonts.
- Render a silent animatic and a `--draft` before the final render.
- Run `lint.mjs`, read every contact sheet, run `mix.mjs` and `verify.mjs`, and report their numbers.
- Stay inside `EXPLAINER_BUDGET_USD`, and report the spend from `spend.json`.
- Ask where to deliver, unless `EXPLAINER_OUTPUT_DIR` or the prompt names the location.
- State in the final report what you could not verify: audio is checked by measurement only, and word timings may be estimated.

### MUST NOT DO

- Hard-code or print API keys, or write them into the job, output, or README files.
- Start voice, image, music, or render work before the user approves the storyboard (unless they asked you to work autonomously).
- Invent how a product is operated, or animate a physical action (flipping, squashing, shaking a device) that the product does not do.
- Use literal seconds for story beats in `scenes.js`, or use `Math.random`, `Date.now`, timers, CSS transitions, or DOM animation.
- Put words inside generated images, or generate charts or diagrams as images.
- Coin product terms or state numbers that are not in the user's material or `facts.md`.
- Put stage directions inside TTS text. Delivery style goes in `voice.style`.
- Edit `assets/engine.js` for a single video, or rewrite `scenes.js` from scratch on each fix round.
- Re-roll images or voice lines without a changed prompt, or delete cached files you do not intend to pay for again.
- Raise the budget, switch to a paid provider the user did not configure, or commit generated media, unless the user asks.
- Use a video-generation model for the animation. This pipeline animates stills in code on purpose.

## Output Template

**At the review gate**, report: the path to `storyboard.html`, the length and scene flow in 3–5 lines, the look, the build cost, and your open questions. Then stop.

**After delivery**, report in this order:

1. **Deliverables:** paths to `<name>.mp4`, `index.html`, captions, `README.md`, `source/`.
2. **Video:** length, resolution, style, voice (model and voice name), music source, language.
3. **Checks:** lint result, loudness (LUFS and dBTP), `verify.mjs` result, contact sheets reviewed.
4. **Spend:** API total against the budget, by kind (image, tts, music).
5. **Assumptions** you made instead of asking.
6. **Known limitations** and suggested next edits (for example: "swap voice to Puck", "tighten line 4").

## Knowledge Reference

OpenRouter Image API, OpenRouter audio/speech, Gemini TTS, Lyria music generation, ElevenLabs timestamps, HTML canvas 2D, Web Audio OfflineAudioContext, deterministic frame capture, Playwright, headless Chromium, ffmpeg image2pipe, libx264, AAC, mov_text subtitles, EBU R128 loudness, two-pass loudnorm, volume-envelope ducking, SRT/WebVTT captions, chroma key, easing curves, storyboard, animatic, explainer script structure, words per minute, reading time, visual hierarchy, safe area
