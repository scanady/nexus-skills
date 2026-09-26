# Getting started

This skill makes a narrated, animated explainer video from a prompt. The agent writes the script, generates the voice, art, and music through OpenRouter, animates everything in JavaScript, and renders an MP4 plus a self-contained HTML player. `SKILL.md` is for the agent. This file is for the person who sets it up.

## What you need

| Item | Notes |
|---|---|
| Node.js 20.10+ | `node -v` |
| About 400 MB of disk | Playwright's Chromium (≈115 MB) plus npm packages and ffmpeg |
| An OpenRouter account and API key | https://openrouter.ai/settings/keys |
| Network access | openrouter.ai, fonts.googleapis.com, fonts.gstatic.com, and npm during setup |

Windows, macOS, and Linux all work. You do not need a system ffmpeg: the `ffmpeg-static` package supplies one.

## One-time setup

1. Install the dependencies in this skill's `scripts/` folder:

   ```bash
   cd <skill>/scripts
   npm install
   npx playwright install chromium
   ```

   Run this in the **installed** copy of the skill (for example `.claude/skills/design-visual-explainer-video/scripts`), not in a source repo that packages skills: `node_modules` is large and must not ship inside a skill zip.

   When the Playwright browser download is blocked, skip the second command. The scripts then try your installed Chrome and Edge. Or set `EXPLAINER_CHROME_PATH`.

2. Copy `.env.example` to `.env` in the skill folder, and set at least:

   ```ini
   OPENROUTER_API_KEY=sk-or-...
   EXPLAINER_BUDGET_USD=10
   EXPLAINER_OUTPUT_DIR=C:/Users/you/Videos/explainers   # optional; the agent asks when it is empty
   ```

   A `.env` in a job folder overrides the skill-level one. Real environment variables override both.

3. **Recommended:** give the key a credit limit in the OpenRouter dashboard (Keys → Edit → Credit limit). The scripts keep their own ledger, but the key limit is the stop that holds whatever happens.

4. Check the setup:

   ```bash
   node <skill>/scripts/doctor.mjs
   ```

## First run without spending anything

This renders the built-in three-line example with a silent voice and synthesized music. It proves the toolchain end to end in about 2 minutes.

```bash
node <skill>/scripts/init.mjs ./explainer-test --example
cd explainer-test
node <skill>/scripts/tts.mjs --provider silent
node <skill>/scripts/timeline.mjs
node <skill>/scripts/fonts.mjs "Caveat:wght@700" "Nunito:wght@400;800"
node <skill>/scripts/build.mjs
node <skill>/scripts/lint.mjs
node <skill>/scripts/shots.mjs --auto
EXPLAINER_MUSIC_PROVIDER=synth node <skill>/scripts/music.mjs
node <skill>/scripts/mix.mjs
node <skill>/scripts/build.mjs
node <skill>/scripts/render.mjs
node <skill>/scripts/verify.mjs
```

On Windows PowerShell, set the variable with `$env:EXPLAINER_MUSIC_PROVIDER="synth"` on its own line first.

Open `out.html` in a browser to play it, or open `video.mp4`.

## Using it

Ask your agent for a video, for example:

- "Make a 60-second explainer video about how our billing retry system works, for new support staff."
- "Create a whimsical hand-drawn explainer about photosynthesis for 10-year-olds. Work autonomously; max spend $5."
- "Explain this codebase in a 90-second video, in Dutch."

Expect 30–90 minutes of agent time for a 60 s video. API spend is typically $0.40–$1.50. The agent's own model tokens cost more (reported at $4–$20 for a 60 s video on a top model).

## What you get

| File | What it is |
|---|---|
| `<name>.mp4` | H.264 + AAC, 1080p30, −16 LUFS, soft captions embedded |
| `index.html` | Self-contained player: fonts, art, and audio embedded; works offline |
| `<name>.srt` / `.vtt` | Captions |
| `README.md` | Script, models, spend, limitations, rebuild steps |
| `source/` | `lines.json`, `scenes.js`, `assets.json`, `music.json`, cues: everything needed to edit and rebuild |

## Settings

Every setting and its default is in `.env.example`. The ones people change most:

| Variable | Use |
|---|---|
| `EXPLAINER_TTS_VOICE` | Gemini voice name (`Charon`, `Puck`, `Kore`, `Aoede`, …; list in `references/audio.md`) |
| `EXPLAINER_TTS_PROVIDER` | `openrouter`, `elevenlabs` (exact word timing, own key), `edge` (free, unofficial), `silent` |
| `EXPLAINER_MUSIC_PROVIDER` | `openrouter` (Lyria), `synth` (free), `file`, `none` |
| `EXPLAINER_IMAGE_MODEL` | e.g. `google/gemini-3-pro-image` for more detail |
| `EXPLAINER_WIDTH` / `EXPLAINER_HEIGHT` | `1080` / `1920` for vertical video |

## Troubleshooting

| Symptom | Fix |
|---|---|
| `doctor` FAIL: browser | `npx playwright install chromium` in `scripts/`, or set `EXPLAINER_CHROME_PATH` |
| `budget stop` (exit 3) | The job reached `EXPLAINER_BUDGET_USD`. Raise it in `.env` only if you agree to spend more |
| `402 payment_required` | The key's credit limit or the account balance is used up |
| "model not found" | Model slugs change. List them: `curl -s "https://openrouter.ai/api/v1/models?output_modalities=image"` (or `speech`, `audio`), then set the model variable |
| Music generation fails | Set `EXPLAINER_MUSIC_PROVIDER=synth` and re-run `music.mjs` and `mix.mjs` |
| Text shows in a plain system font | Run `fonts.mjs` before `build.mjs`. Check the family names in `fonts.json` |
| Garbled characters (`â€™`) | Keep `<meta charset="utf-8">` as the first line of `assets/player.html` |
| Render is slow | Raise `EXPLAINER_RENDER_WORKERS` (up to the number of CPU cores), or use `render.mjs --draft` for checks |
