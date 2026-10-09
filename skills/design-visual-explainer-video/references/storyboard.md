# Storyboard and review gate

The user approves the plan by looking at it, not by reading it. `storyboard.mjs` turns `storyboard.json` into `storyboard.html`:

- **Animatic:** the key frames advance in time with the narration. Lines already voiced play the real clip; new lines use the browser's speech voice as a stand-in. A timeline sized by duration, colored by chapter, marks changed scenes.
- **Filmstrip:** one card per scene: the key frame, the time range, the narration (changed lines highlighted), the on-screen text, the motion, the images, and a note box.
- **Look and sound:** palette swatches, font samples in the real fonts, the image style, the voice, and the music.
- **Questions, images to generate, sources.**
- **Copy feedback:** gathers every note and answer into one markdown block for the chat. Notes persist in the browser between reloads.

It also writes `REVIEW.md`, a plain-text record of the same plan. Both stay in `work/` and ship with the output folder.

## Where the key frames come from

| Scene state | Frame |
|---|---|
| Unchanged since the last build (same `name` in the built `out.html`, no new or changed lines) | A frame from the real video, about 85% through the scene, badge "From the current video" |
| New or changed, with a `frame` spec | A sketch drawn with `assets/layouts.js` in the video's theme and fonts, badge "Sketch" |
| No `frame` spec | A text card with the scene's `visual` description (avoid this) |

`--sketch-all` forces sketches for every scene. The first review of a new video always uses sketches, because there is no build yet.

## `storyboard.json`

```json
{
  "design": {
    "summary": "Warm editorial, matching the brand site",
    "palette": { "paper": "#f6f5f2", "ink": "#111110", "accent": "#e07a2e" },
    "theme": {
      "light": "#f6f5f2", "dark": "#171614", "ink": "#111110", "inkOnDark": "#f5f3ee", "accent": "#e07a2e",
      "muted": "#55524d", "mutedOnDark": "#a9a59d", "card": "#ffffff", "cardOnDark": "#201e1b", "border": "#e6e3dd",
      "display": "Manrope", "serif": "Instrument Serif", "mono": "JetBrains Mono"
    },
    "fonts": ["Manrope 800 (headlines)", "Instrument Serif italic (quotes)", "JetBrains Mono (labels)"],
    "motion": "Fade-up entrances keyed to spoken words, slow push-ins on photos, crossfades in the pauses",
    "voice": "Gemini Sulafat: warm, natural conversational pace",
    "music": "Soft felt piano and acoustic guitar, 84 BPM"
  },
  "scenes": [
    {
      "name": "light",
      "title": "Touch to start, touch to stop",
      "chapter": "How it works",
      "lines": [6, 7],
      "visual": "Device close-up on charcoal; tap ripples on the screen and the top button; the glow turns on and off",
      "onScreen": ["One touch to start.", "Another to stop.", "Light on: listening."],
      "motion": "Ripple + chime on 'starts'; ripple + click on 'ends'; glow returns on 'light'",
      "assets": ["device"],
      "notes": "Interaction confirmed by the user",
      "frame": {
        "layout": "device", "bg": "dark", "image": "device",
        "kicker": "Starting a sitting", "headline": "One touch to start.", "headline2": "Another to stop.",
        "items": ["Light on: listening."],
        "callouts": [{ "x": 0.70, "y": 0.47, "text": "Touch the screen" }]
      }
    }
  ],
  "changes": ["Revisions only: what changed since the last approved version"],
  "questions": ["Anything the user must decide"],
  "userFacts": ["Facts the user stated in chat, with the date"]
}
```

- `name` must match the `scene({name})` in `scenes.js`, so later revisions can reuse frames from the build.
- Every script line (by index in `lines.json`) belongs to exactly one scene, in order. Every image id is in `assets.json`, `assets/extra/`, or already made. `storyboard.mjs` checks both (exit 7).
- `visual` describes one focal picture a person could sketch. `onScreen` holds the exact words, at most 8 per item.
- `chapter` groups scenes on the timeline. Use 3–6 chapters that match the story's structure (for example: Why, What it is, How it works, What you keep, What's next).
- `theme` feeds the sketch layouts. Take the colors from the palette and the families from `fonts.json`. When the project has `shared/brand.json`, take the palette and fonts from it.

## Frame layouts (`assets/layouts.js`)

| Layout | Use for | Fields |
|---|---|---|
| `type` | A big statement or question on a plain ground | `headline`, `headline2` (accent), `kicker`, `sub`, `items` |
| `photo-card` | Text beside a photo in a rounded card | `image`, `imageSide` (`right`/`left`), `kicker`, `headline`, `headline2`, `sub`, `items` (chips) |
| `photo-full` | A full-bleed photo with text over a scrim | `image`, `textSide` (`left`/`right`/`bottom`), `focus` `[px, py]`, `kicker`, `headline`, `sub`, `items` |
| `cards` | Three or four parallel ideas | `kicker`, `headline`, `items` (card titles) |
| `list` | A checklist, optionally with a photo card | `kicker`, `headline`, `items` (checks), `image` |
| `quote` | A dialogue or transcript beside a photo | `image`, `kicker`, `quote: [{label, text}]` |
| `diagram` | A flow (`items` in a row with arrows), or sources into one node (`items` + `target`) | `kicker`, `headline`, `items`, `target` |
| `device` | A product close-up with a glow | `image` (a cut-out), `kicker`, `headline`, `headline2`, `items` |
| `map` | A constellation of labeled nodes with a thread between them (topics, areas, a network), plus an optional card | `items` (node labels), `points` `[[x, y]…]` in 0..1 (optional), `path` (labels the thread visits; the last is active), `kicker`, `headline`, `quote: [{label, text}]` (the card), `sub` |

Every layout also takes `bg` (`light`, `dark`, or a hex color) and `callouts: [{x, y, text}]` (x and y in 0..1 of the frame). A callout draws an accent ring with a label, to show a tap, a highlight, or where the eye should go.

A sketch shows layout, content, and look, not the final motion. Put the motion in `motion`, and it appears beside the frame in the page. When no layout fits, pick the closest one and describe the difference in `visual`.

## The review loop

1. Run `storyboard.mjs`. Screenshot the page or open it, and fix frames that overflow or overlap before the user sees them.
2. Send the path and a 3–5 line summary. Stop.
3. The user pastes feedback, or replies in their own words. Apply it: script edits go to `lines.json`, scene edits to `storyboard.json`, image edits to `assets.json`. Add a line to `changes` for each.
4. Run `storyboard.mjs` again and list what changed. Repeat until the user approves.
5. Build from the approved plan. Keep `storyboard.json` in step with `scenes.js` if the build forces a change, and tell the user.
