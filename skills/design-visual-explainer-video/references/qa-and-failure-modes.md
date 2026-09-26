# QA and known failure modes

These come from the public threads on this technique (r/ClaudeAI, Hacker News item 49836374, launchvideo.io's prompt, and c-kick's `explainer-animation` skill) and from testing this skill's pipeline.

## Failure modes and the guard for each

| Failure seen in the wild | Guard in this skill |
|---|---|
| Hours of planning at max effort, no frame rendered, $100 spent | Silent animatic and a draft render early in the workflow; per-job budget ledger; capped key |
| Too fast: "not enough time to read what's on each slide" | 140–160 wpm; `lint.mjs` reading-time check; ≤ 8 words per text element |
| Too much motion: "squeeze in as many animations and transitions" | One focal motion at a time; transitions 0.5–0.7 s; no transition on every line |
| Repetitive, "nearly content-free", "LLM-speak" | `facts.md` first; script self-review checklist; one new idea per line |
| Made-up vocabulary | Use the user's terms only; list and replace coined terms before TTS |
| Music too loud | Timeline ducking; music 16 dB under the voice; measured in `mix.mjs` |
| "Uncanny" AI video look | Code-driven animation of generated stills, no video models |
| Style tells ("flashy slide deck", "office template") | A committed style from `visual-styles.md`; drawn marks; motion keyed to words |
| Garbled text inside generated images | Prompts forbid text; every word is drawn with `text()` |
| Hollow shapes, a background showing through a figure | Contact-sheet review; fill shapes explicitly |
| Style drift across images | One `style` line; `ref` images for recurring characters |
| Labels over titles, captions colliding with arrows | `lint.mjs` overlap check; a 5% safe area |
| Scrolling strip runs out | Draw 3 repeats and scroll modulo one repeat width |
| Mojibake (`’` shows as `â€™`) | `player.html` starts with `<meta charset="utf-8">`; do not remove it |
| Mixed-language narration | All speech and on-screen text in the one requested language |
| Video cut short by the caption track | `render.mjs` sets the length with `-t`, not `-shortest` |

## Contact-sheet review (every scene, at least once)

Read each `shots/sheet-*.jpg` and check:

- The focal point is clear, and the eye knows where to look.
- Nothing is clipped at the frame edges. Nothing important sits in the outer 5%.
- Text is readable at 50% size (the sheet is half size, like a phone in landscape).
- Cut-outs have no green fringe and no hard rectangle edge.
- The scene's first frame (the entry shot from `--auto`) is not empty.
- The frame matches what the narration says at that moment (the sheet label shows the time; check it against `cues.json`).
- Colors and fonts match the chosen style. No stray system font (it shows up as plain Arial or Helvetica).

Crop to a detail with `node shots.mjs <t> --full` and open `shots/t<t>.jpg` when a sheet is not clear enough.

## Timing review

- Open `out.html` in a browser when a person is available. Otherwise trust `lint.mjs` and the sheets.
- With estimated word timings, a beat keyed to a word can land up to about 0.4 s early or late. Key the important beats to line starts, or add a lead of about 0.1 s so the visual arrives just before the word.

## Done checklist

- [ ] `lint.mjs` exits 0. No console errors, no gaps, no overlap or reading-time warnings left without a reason.
- [ ] Every scene has passed a contact-sheet check.
- [ ] `mix.mjs` reports the mix within ±1 LU of −16 LUFS and a true peak ≤ −1.5 dBTP.
- [ ] `verify.mjs` exits 0, and `shots/verify.jpg` (frames from the encoded file) looks right.
- [ ] Spend is within budget. `verify.mjs` prints the ledger.
- [ ] The delivery folder has `video.mp4`, `index.html`, `captions.srt`, `README.md`, and `source/`.
