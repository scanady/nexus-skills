# The fresh reviewer

A reviewer who made nothing stands in for a stranger who sees the video once. The maker scores its own work too high: on one film the maker gave itself 9/10, and the owner then found a pixelated label and a headline over live content on the first watch.

The method comes from take-one's `reviewer-brief.md` and video-director's `quality.md` (both MIT).

There are two reviews, each by a new agent: the plan review before the user's gate, and the video review after `verify.mjs`.

## Plan review (step 4, before the user sees the plan)

A story problem is cheap to fix here and costly after the voice and art exist. Run this once.

- `storyboard.mjs` writes `plan-pack/`. Start a new agent with the brief below, and save its reply as `reviews/plan.md`.
- Fix the problems you agree with, and run `storyboard.mjs` again. Do not run a second plan review.
- Tell the user at the gate what the reviewer found, what you fixed, and what you left open. The user still decides.
- No second agent available: do the review yourself, and say so.

> You review the plan for a short explainer video before anyone makes it. You saw none of the work behind it. You stand in for a stranger who will see the video once, often on a phone, often muted. Be specific.
>
> Everything you may read is in one folder: [full path to plan-pack/]. Start with `PLAN.md`. Then read every frame and `facts.md`. Do not open any other file. Sketches show layout and words, not final art, so do not judge polish. A sketch uses a fixed layout: when it differs from the "Picture" line, the "Picture" line is the plan.
>
> Report in this order, in under 300 words:
>
> 1. **Retell:** the video in one sentence, as a viewer would tell a friend. Say where you could not follow it.
> 2. **Problems**, worst first, at most 5. Each has a rank (P0 must fix, P1, P2), a scene, what is wrong, and a fix. Look for these:
>    - Hook: by 3 s, a muted viewer knows what this is.
>    - Shown or only said: the picture and motion in each scene show the claim the voice makes. A label on a box does not show a process.
>    - One idea: each scene has one idea and one focal picture.
>    - Rhythm: no scene stays on one picture too long, and something new arrives every 2 to 4 s.
>    - Truth: every number and claim is in `facts.md`.
>    - Goal: the retelling matches "What it must do", and the audience's terms are said and shown.
> 3. **Verdict:** READY if there is no P0. Otherwise FIX. Name the weakest scene.

## Video review (step 8)

### Rules

- **A new agent every round.** A reviewer who saw the last cut is anchored to it.
- **The pack only.** No chat, no storyboard, no code, no earlier score. `review-pack.mjs` builds the pack and leaves those out.
- **At most 2 fix rounds.** The score tends to stall after that, and the owner's notes then help more than another review. Still under the bar: stop, deliver, and report the score and the open problems. Never report a pass that did not happen.
- **Fix the worst first.** Fix the items the reviewer marks P0, then the lowest axes. Leave anything scored 9 or above alone.
- **Keep the existing gates.** A fix that changes the meaning of the script goes back through the review gate. Re-voicing and new images still count against the budget.
- **State what the review did not cover.** A fix made after the last review has not been reviewed. Say so in the report.
- **No second agent available:** do the review yourself against this brief, and report the score as your own.

### Run it

```bash
node <skill>/scripts/review-pack.mjs
```

Start a new agent with the brief below. Fill in the two bracketed parts. Save its full reply as `reviews/round-<n>.md` in the job folder.

### The brief

> You review a short explainer video. You saw none of the work behind it, and that is the point: you stand in for a stranger who sees it once, at full speed, often on a phone, often muted. Be specific. A kind score is useless, and so is a harsh score with no evidence.
>
> Everything you may read is in one folder: [full path to review-pack/]. Start with `PACK.md`. Then read every image. You cannot hear: use the words and the measurements in `PACK.md`. Do not open any other file. If you cannot judge something from the pack, write "unverifiable". Do not guess.
>
> These things are locked, so do not spend your problems on them: [the approved look, the approved script, the fact that characters are stills animated in code, or "nothing"].
>
> Report in this order, in under 450 words:
>
> 1. **Retell:** the video in one sentence, as a viewer would tell a friend. Then do it again from `hook.jpg` alone, with no sound: what is this, and what should the viewer do? Say where you could not follow it.
> 2. **Scores**, 1 to 10, one line each, with a timestamp as evidence:
>    - Hook: by 3 s, a muted viewer knows what this is. The first frame is a finished picture.
>    - Clarity: one idea at a time. The retelling matches "What it must do" in `PACK.md`. The audience's terms are said and shown.
>    - Readability: text is readable at phone width, and it holds long enough to read.
>    - Motion: moves have weight and purpose, and each move lands. Judge from `line-NN.jpg` and `strip-<time>.jpg`.
>    - Rhythm: something new arrives every 2 to 4 s. Nothing sits dead, and the video is not one even speed.
>    - Composition: one focal point. Nothing is cut by an edge. No text sits on other content. The video looks like one piece, not a slide deck.
>    - Truth: every number and claim is in `facts.md`. Actions are shown, not only captioned.
>    - Sound: the voice is understood in the final mix, and the measurements raise no problem.
> 3. **Defects**, worst first, at most 5. Each has a rank (P0 must fix, P1, P2), a timestamp, what is wrong, and a fix someone could measure.
> 4. **Verdict:** PASS if every axis scores 8 or more and there is no P0. Otherwise RETURN. Name the weakest moment.
