# Providers, models, and costs

All paid calls go through `scripts/lib/openrouter.mjs` (or the ElevenLabs branch in `tts.mjs`). Each call adds a line to `spend.json` in the job folder. A script stops with exit code 3 before a call that would pass `EXPLAINER_BUDGET_USD`. Model slugs were checked against `GET https://openrouter.ai/api/v1/models` on 2026-09-26.

## Endpoints used

| Purpose | Endpoint | Cost source |
|---|---|---|
| Images | `POST /api/v1/images` (`model`, `prompt`, `aspect_ratio`, `resolution`, `seed`, `input_references`, `background`) → `data[0].b64_json` | `usage.cost` in the response |
| Speech | `POST /api/v1/audio/speech` (`model`, `input`, `voice`, `response_format`, `provider.options.<provider>.speech_metadata.style`) → raw audio bytes. Gemini TTS accepts only `response_format: "pcm"` and returns `audio/pcm;rate=24000;channels=1` (16-bit). `tts.mjs` wraps it into WAV, and retries once with the format a 400 error names | `GET /api/v1/generation?id=<X-Generation-Id>` → `data.total_cost`; the script estimates the cost when the lookup fails |
| Music | `POST /api/v1/chat/completions` with `stream: true`, `modalities: ["text","audio"]`, `audio.format` → base64 slices in `choices[0].delta.audio.data` | `usage.cost` in the last chunk |
| Key status | `GET /api/v1/key` → `limit`, `limit_remaining`, `usage` | used by `doctor.mjs` |

A 402 response means the key's credit limit or the account balance is used up. The scripts stop and do not retry.

## Default models

| Role | Default | Alternatives |
|---|---|---|
| Images | `google/gemini-3.1-flash-image` (Nano Banana 2) | `google/gemini-3-pro-image` (Pro, about 2× the price, better detail and text), `google/gemini-3.1-flash-lite-image` (cheaper), `google/gemini-2.5-flash-image` (fallback), `openai/gpt-image-2`, `black-forest-labs/flux.2-pro`, `recraft/recraft-v4.1*` (vector/SVG) |
| Speech | `google/gemini-3.8-flash-tts` | `google/gemini-3.1-flash-tts-preview` (the Reddit run), `google/gemini-3.8-flash-lite-tts`, `openai/gpt-4o-mini-tts-2025-12-15`, `minimax/speech-2.8-hd`, `fish-audio/s2.1-pro` |
| Music | `google/lyria-3-pro-preview` | `google/lyria-3-clip-preview` (30 s clips) |

Model names change often. When a call fails with "model not found", list the current slugs:
`curl -s "https://openrouter.ai/api/v1/models?output_modalities=image"` (or `speech`, `audio`).

## What a video costs (typical)

| Item | 60 s video | Notes |
|---|---|---|
| Images, 6–10 at 1K | $0.40–$0.70 | measured: $0.067 per 1K image on Nano Banana 2; re-rolls add cost |
| Voice, 8–10 lines | $0.01–$0.05 | measured: about $0.0015 per line on `gemini-3.8-flash-tts`; the cache means edits re-voice only changed lines |
| Music | about $0.08 | one track; the cache skips it unless the prompt changes |
| **API total** | **$0.40–$1.50** | the Reddit run spent $3.21 with no cache and more images |
| Model tokens (Claude) | the larger cost | reported at about $4–$20 of Opus usage for a 60 s video. `scenes.js` is written once, then edited in place |

The budget in `EXPLAINER_BUDGET_USD` covers only the API calls the scripts make. It does not cover the agent's own model tokens.

## Budget and safety rules

- Recommend to the user a **dedicated OpenRouter key with a credit limit** (dashboard → Keys → limit, e.g. $10). The limit is the hard stop that holds even if a script has a bug. `doctor.mjs` warns when the key has no limit.
- Never raise `EXPLAINER_BUDGET_USD` on your own. When a script stops with a budget error, report what you spent and what is left to do, and ask.
- A reported failure: an agent at maximum thinking effort planned all night, spent $100, and never rendered a frame. The workflow therefore requires a draft render early (see SKILL.md). A silent animatic costs $0.
- Cached content costs nothing. Delete a cached file only when you mean to pay for it again.

## Environment variables

See `.env.example` for the full list with defaults. The scripts look for settings in this order: real environment variables, then `<job>/.env`, then `<skill>/.env`, then built-in defaults. Never print or log a key. Never write a key into any file in the job or output folder.
