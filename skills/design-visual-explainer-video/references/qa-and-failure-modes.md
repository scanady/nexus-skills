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
| Beats land off the spoken word; the voice misreads a word | `align.mjs` measures word times with local Whisper and flags words it did not hear |
| Music or effects bury the voice | `verify.mjs` runs Whisper on the final mix and reports the percent understood |
| The maker scores its own work too high | A fresh reviewer who sees only `review-pack/` (`references/reviewer-brief.md`) |
| A story problem is found only after the voice and art are paid for | A plan review of `plan-pack/` before the user's gate; plan notes from `storyboard.mjs` |
| The video drifts from the approved plan | `lint.mjs` checks the scene names and `onScreen` items in `storyboard.json` |
| Black first frame; hook arrives too late for a muted feed | `lint.mjs` and `verify.mjs` check the first frame; `lint.mjs` checks for large text by 3 s; `shots/hook.jpg` |
| Text too small on a phone | `lint.mjs` measures size at 360 px wide; `shots/phone-*.jpg` |
| The video never names what it explains | `terms` in `brief.json`; `storyboard.mjs` and `lint.mjs` check they are said and shown |
| One-frame glitches and dead stretches | `verify.mjs` measures flashes, small jumps, and frozen stretches on the encoded file |

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
- `timeline.mjs` prints each line's timing source: `exact` (from the provider), `measured` (by `align.mjs`), or `estimated`. `verify.mjs` reports how far the word times are from the final mix.
- When `align.mjs` cannot run, a beat keyed to a word can land up to about 0.4 s early or late. Key the important beats to line starts, or add a lead of about 0.1 s so the visual arrives just before the word.

## What the viewer checks measure

These are defaults. Break one on purpose and state why.

| Check | Script | Floor |
|---|---|---|
| First frame | `lint.mjs` warns, `verify.mjs` fails | Brightness spread at least 6 of 255, mean at least 8. A number catches black or blank. Only a look at `shots/hook.jpg` confirms the picture is finished |
| Hook | `lint.mjs` | Text of at least 84 px at a 1080 short side, fully on screen by 3 s, with contrast of at least 4.5:1 |
| Phone size | `lint.mjs` | At least 8 px on a 360 px wide phone (43 px on a 1920 wide canvas, 24 px on a 1080 wide canvas), for text and captions on screen 0.6 s or more |
| Terms | `storyboard.mjs`, `lint.mjs` | Each `brief.json` term is said and shown |
| Plan notes | `storyboard.mjs` | First scene has on-screen text. Each `onScreen` item has at most 8 words. A scene lasts 1 s + its on-screen words at 180 wpm. Each number written in digits is in `facts.md` |
| Plan drift | `lint.mjs` | Each scene name and `onScreen` item in `storyboard.json` is in the video |
| Flashes | `verify.mjs` fails | One frame differs from both neighbours, and the neighbours match. It skips the frames of a planned `shake()` |
| Small jumps | `verify.mjs` warns | A sudden small change away from a spoken word, a caption change, or a planned `shake()`. A planned hit is fine |
| Frozen stretches | `verify.mjs` warns | Nothing moves for 2.5 s (`--freeze`), except at the very end. A planned hold is fine |
| Speech in the mix | `verify.mjs` | Under 70% understood fails. Under 85% overall, or under 80% on a line, warns. A proxy: Whisper is not a person |

## Done checklist

- [ ] `lint.mjs` exits 0. No console errors, no gaps, no overlap or reading-time warnings left without a reason.
- [ ] Every scene has passed a contact-sheet check.
- [ ] `mix.mjs` reports the mix within ±1 LU of −16 LUFS and a true peak ≤ −1.5 dBTP.
- [ ] `align.mjs` flags no line you have not looked at, and every line's timing is `exact` or `measured`, or the report says why not.
- [ ] `verify.mjs` exits 0, every `warn` is fixed or has a reason, and `shots/verify.jpg`, `shots/hook.jpg`, and `shots/phone-*.jpg` (frames from the encoded file) look right.
- [ ] A fresh reviewer returned PASS, or the report gives the last score and the open defects after 2 fix rounds.
- [ ] Spend is within budget. `verify.mjs` prints the ledger.
- [ ] The output folder `video/` has `<project>.mp4`, `index.html`, `<project>.srt`, `<project>.vtt`, `README.md` (TODOs filled), and `work/`. `project.json` lists it as `delivered`, and `deliver.mjs` reported what it published to `shared/`.
