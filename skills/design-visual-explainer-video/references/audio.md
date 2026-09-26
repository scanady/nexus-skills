# Voice, music, and mix

You cannot listen to the output. Choose settings from the rules below, and check the result by measurement (`mix.mjs` and `verify.mjs` print loudness numbers).

## Voice

- Default: OpenRouter `google/gemini-3.8-flash-tts`, voice `Charon`. The Reddit run used `google/gemini-3.1-flash-tts-preview` (about $0.23 for a 60 s video).
- Set the delivery style in `lines.json` → `"voice": {"style": "..."}`. For Gemini, it goes to the provider as `speech_metadata.style`. **Never write stage directions inside a line's text**: Gemini reads the text word for word.
- Good style lines: "Warm, curious, unhurried. Explaining to a smart friend." / "Upbeat and playful, a light smile, crisp consonants." / "Calm, precise, trustworthy; a documentary narrator."
- Words in the style note change the pace a lot. Measured with Sulafat: "unhurried" gave 114 wpm and a 145 s video; "natural conversational pace with gentle energy" gave 131 wpm and 127 s. Avoid "slow", "unhurried", and "calm" unless you want a slow read. Check the wpm that `timeline.mjs` prints after every re-voice.
- Audition before you voice the whole script: `node tts.mjs --sample "<the hook line>" --voice Puck`. Each sample is one small paid call. Try at most 2–3 voices.
- Commenters said one voice type is "overused like crazy". Match the voice to the audience. Do not use the same voice for every video.

Gemini voices (their published character):

| Voice | Character | Voice | Character |
|---|---|---|---|
| Zephyr | bright | Puck | upbeat |
| Charon | informative | Kore | firm |
| Fenrir | excitable | Leda | youthful |
| Orus | firm | Aoede | breezy |
| Callirrhoe | easy-going | Autonoe | bright |
| Enceladus | breathy | Iapetus | clear |
| Umbriel | easy-going | Algieba | smooth |
| Despina | smooth | Erinome | clear |
| Algenib | gravelly | Rasalgethi | informative |
| Laomedeia | upbeat | Achernar | soft |
| Alnilam | firm | Schedar | even |
| Gacrux | mature | Pulcherrima | forward |
| Achird | friendly | Zubenelgenubi | casual |
| Vindemiatrix | gentle | Sadachbia | lively |
| Sadaltager | knowledgeable | Sulafat | warm |

Other providers (`--provider` or `EXPLAINER_TTS_PROVIDER`):
- `elevenlabs`: exact word timings, so visual sync is tighter. Needs your own ElevenLabs key and voice id. Use it only when the user asks or has already configured it.
- `edge`: free Microsoft Edge voices with exact word timings (e.g. `en-US-AndrewMultilingualNeural`, `en-US-AvaMultilingualNeural`). The endpoint is unofficial and can break. Use it only when the user wants zero TTS cost.
- `silent`: silent clips of estimated length. Use it for a free animatic before any paid voice, and as the fallback when voice generation is blocked.
- Any other OpenRouter speech model works through `--model` (e.g. `openai/gpt-4o-mini-tts-2025-12-15`, `minimax/speech-2.8-hd`). Voice names differ per model.

## Music

- Default: OpenRouter `google/lyria-3-pro-preview` (about $0.08 per track). Write `music.json`:

```json
{
  "prompt": "Whimsical pizzicato strings, glockenspiel and soft brushed percussion, 100 BPM, D major, light and curious",
  "sections": [
    { "at": 0, "text": "gentle intro, sparse" },
    { "at": 14.2, "text": "adds light percussion, builds slightly" },
    { "at": 41.8, "text": "resolves to a warm final chord, ring out" }
  ]
}
```

- Take the section times from `cues.json` (scene changes and the payoff line). `music.mjs` adds "instrumental only, no vocals", the target length, and "leave room for a voice-over".
- Lyria 3 Pro follows the requested length only sometimes. Measured on 2026-09-26: it returned 61 s for a 19 s request, but 126 s for a 127 s request (44.1 kHz stereo WAV both times). Treat the section times as mood hints, not sync points. `mix.mjs` handles it: when the track is longer than the video, it keeps the natural start and splices the track's real ending onto the video's last few seconds (up to 8 s) with a 1.5 s crossfade. `--loop` forces loop-and-fade instead.
- Tie visual beats to the voice, never to the music.
- Match genre to tone: pizzicato, glockenspiel, or ukulele for whimsical; soft piano or pads for calm; a light electronic pulse for tech; felt piano or strings for serious.
- If Lyria fails or the user wants no generated music: `EXPLAINER_MUSIC_PROVIDER=synth` uses the engine's seeded bed (call `music({bpm, key, mood})` in `scenes.js`). Use `file` with `EXPLAINER_MUSIC_FILE` for a licensed track, or `none`.
- Lyria output carries a SynthID watermark. Say so in the delivery README.

## Mix targets (what `mix.mjs` does)

| Item | Target |
|---|---|
| Voice | each line trimmed and normalized to −16 LUFS (two-pass linear `loudnorm`) |
| Music under speech | 16 dB below the voice (`EXPLAINER_MUSIC_UNDER_VOICE_DB`) |
| Music between lines | 8 dB louder than under speech (`--duck 8`), ramped in 0.3 s before and out 0.45 s after each line |
| Music shape | looped or trimmed to length, 0.8 s fade-in, 3 s fade-out |
| SFX | engine levels × `EXPLAINER_SFX_GAIN` (0.8) |
| Final | −16 LUFS integrated, ≤ −1.5 dBTP, 48 kHz stereo |

- Music that is too loud was the single fix needed in one reported one-shot run. When in doubt, raise `--under` (e.g. 18–20) and re-run `mix.mjs`. It is free and takes seconds.
- A mono narration measures about 3 LU quieter than the same voice in the stereo mix. Compare like with like.
- Long silences in the finished video (> 2.5 s) fail `verify.mjs`. Check the pauses in `lines.json` and the length of the tail.
