# Script and story

The script decides most of the quality. Viewers of AI explainers complain most about content, not visuals: "nearly content-free", "kept repeating the same point", "LLM-speak", "made-up vocabulary", "too fast to read". Write and check the script before you spend anything on art.

## Research first

1. Collect the facts the video will state. Sources, in order: what the user gave you, the project folder's `shared/brief.md` and `shared/facts.md` (when they exist), the project's docs (README, AGENTS.md, CLAUDE.md, docs/), then primary sources on the web.
2. Write `facts.md` in the job folder: one claim per line, as `- <claim> — <source>`, where the source is a URL, a file path, or `user (chat, <date>)`. `init.mjs` starts it with the lines of `shared/facts.md`; add yours below them. Every claim in the script must trace to a line in this file. `deliver.mjs` adds your new lines to `shared/facts.md`.
3. Collect the user's own vocabulary: product names, feature names, the terms their docs use. Use those words. Do not coin terms.
4. For a codebase explainer, map each beat to a real subsystem (a file or module). Explain what it does and how it works. Do not write marketing copy.

## Length and pace

| Target length | Words (at 150 wpm) | Lines | Scenes |
|---|---|---|---|
| 30 s | 65–75 | 4–5 | 4–6 |
| 60 s (default) | 130–150 | 7–10 | 6–10 |
| 90 s | 200–225 | 11–14 | 9–14 |
| 2–3 min | 300–450 | 16–28 | 14–24 |

- Narration pace: 140–160 wpm. `timeline.mjs` prints the actual wpm. Above 170 wpm, cut words. Do not speed up the voice.
- One line = one sentence = one idea. Keep it to 8–22 words. TTS reads short lines with better intonation.
- Add `"pauseAfter": 0.9` after a line that lands a key point, to give viewers a beat to absorb it. The default gap is 0.55 s.

## Structure

1. **Hook (line 0, ≤ 5 s):** a question, a surprising fact, or the problem, in concrete words. Not "In this video we will…".
2. **Setup (1–2 lines):** who has the problem and why it matters.
3. **Mechanism (3–6 lines):** how it works, in causal order. Each line adds one new step. Show the mechanism on screen, not stock imagery.
4. **Payoff (1–2 lines):** what changes for the viewer. Use a concrete number only if it is in `facts.md`.
5. **Close (1 line):** a short recap or call to action, plus the name. Hold the final frame about 2 s (the `--tail` of `timeline.mjs`).

For a story-driven brief ("tell the story of someone's struggle"), put a character in the setup. Give the character a small setback in the mechanism, and let the product or idea resolve it in the payoff.

## Line-level rules

- Use spoken language: contractions, short words, active verbs. Read each line aloud in your head.
- No filler openers ("Imagine…", "Let's dive in", "Here's the thing"). No aphorisms or slogans that restate the previous line.
- No repeated point. If two lines say the same thing, cut one.
- Numbers: write them the way the voice should say them ("about forty percent"). Keep the digits in `text` for captions, and put the spoken form in `say`.
- Hard names: keep `text` correct for captions and give TTS a phonetic `say`. Example: `{"text": "Friendr.nl", "say": "Friender dot N L"}`. `say` turns off provider word timings for that line, so timing becomes estimated.
- The language of **all** speech and **all** on-screen text is the user's requested language (default English). Write natively in that language. Do not translate word for word.

## Script self-review (do this before any TTS call)

- [ ] Every claim traces to `facts.md`.
- [ ] No term appears that is not in the user's material or in common use. List any coined term and replace it.
- [ ] No two lines make the same point.
- [ ] The hook works with the sound off (the on-screen text says it too).
- [ ] Word count matches the target length (see the table).
- [ ] Each mechanism line names something a viewer could draw on paper. If you cannot picture the visual, rewrite the line.

## On-screen text

- The voice carries the detail. The screen carries the key noun, number, or label.
- At most 8 words per text element, and at most about 12 words on screen at once.
- Hold text at least `1 s + 0.33 s × words`. `lint.mjs` checks this.
- Burned-in captions are optional. The MP4 always gets a soft caption track from `captions.srt`.

## Storyboard

The storyboard format, the frame layouts, and the review loop are in `references/storyboard.md`.

Rules:
- One focal point per moment. Each scene changes the picture in a way that matches the line. Do not show a talking-head slide.
- Visual metaphors must be concrete and literal enough to draw: a queue of envelopes, a funnel, a lock with two keys.
- Show real interactions only. How someone turns a device on, starts a session, or uses a feature must come from the sources or the user. When in doubt, ask in `questions`.
- Plan 2–3 recurring elements (a mascot, a color code, an icon set) so the video reads as one piece.
- Mark the single biggest moment. Give it the one dramatic audio gesture (a `boom`, or a riser into silence).
