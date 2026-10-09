# Project folder

Several skills can build outputs for the same subject in one shared project folder. Each skill owns one subfolder. They exchange material only through `shared/` and `project.json`. Every skill works alone, and in any order: a missing file means "do your normal research or capture", never an error.

The skills that follow this layout: `design-visual-explainer-video` (`video/`), `design-product-overview-builder` (`overview/`), `design-product-overview-recorder` (`demo/`), and `design-scroll-storytelling` (`scroll/`).

## Layout

```text
<parent>/<project>/
├── project.json        # manifest: title and the outputs that exist
├── README.md           # index of outputs, one marked section per output
├── shared/             # material any skill may read and add to
│   ├── brief.md        # subject, audience, goal, tone, call to action
│   ├── facts.md        # one claim per line, with its source
│   ├── brand.json      # palette, fonts, logo, voice
│   ├── ui-map.md       # real UI: pages, fields, buttons, flows
│   ├── assets.json     # one entry per shared image or recording
│   ├── images/         # generated art, key frames, logos, cut-outs
│   └── screenshots/    # captures of the real product UI
├── video/              # one subfolder per output; its working files in <output>/work/
├── overview/
├── demo/
└── scroll/
```

The user picks `<parent>` and names `<project>`. Ask for both unless the prompt gives them. Never create a project inside the repo's `output/` folder.

## Start: join or create

1. When `<parent>/<project>/project.json` exists, **join** the project. Read `project.json` and everything in `shared/` before you research, capture, or generate anything.
2. When the folder does not exist, **create** it: `project.json`, `README.md`, and an empty `shared/`.
3. When the folder exists without `project.json` and is not empty, stop and ask the user. Never adopt a folder you did not create.
4. Pick your output folder. Use your skill's default name (`video`, `overview`, `demo`, `scroll`). When `project.json` already lists that folder for another run, ask the user for a suffix, such as `video-vertical`. Never write into an existing output folder that is not yours to update.

## Write rules

A skill writes only to:

- its own output folder (deliverables at its top, working files and caches in `<output>/work/`);
- its own entry in `project.json` → `outputs`;
- its own marked section of `README.md`;
- `shared/`, by adding files and entries. Change or delete an entry another skill made only when the user asks.

A skill reads another skill's output only through that output's `entry` file, for example to embed the finished video in an overview page. It never reads another output's `work/` folder.

Never write API keys, `.env` files, spend ledgers, or caches to `shared/`, `project.json`, or `README.md`. Each output keeps its own `.env` and ledger in its `work/` folder.

All paths in these files are relative to the project folder and use forward slashes, so the folder can move or be zipped. Edit JSON by read, change, write: keep every key and entry you do not own, including ones you do not recognise.

## project.json

```json
{
  "schema": 1,
  "name": "why-is-the-sky-blue",
  "title": "Why is the sky blue?",
  "outputs": [
    {
      "dir": "video",
      "skill": "design-visual-explainer-video",
      "kind": "explainer-video",
      "entry": "video/why-is-the-sky-blue.mp4",
      "status": "delivered",
      "updated": "2026-10-09"
    }
  ]
}
```

- `name` is the project folder name. `title` is the human title; set it once, change it only when the user asks.
- One `outputs` entry per output folder, keyed by `dir`. `kind` is one of `explainer-video`, `product-overview`, `demo-recording`, `scroll-story`. `entry` is the main deliverable, or `null` until there is one. `status` is `in-progress` or `delivered`. `updated` is an ISO date.
- When `schema` is greater than 1, read the fields you know, keep the rest, and tell the user the folder was made by a newer version.

## README.md

The first skill writes a `# <title>` heading. Each skill then owns one section between markers named after its output folder:

```markdown
<!-- output:video -->
## Explainer video
`video/why-is-the-sky-blue.mp4` (1:02), player `video/index.html`. Details: `video/README.md`.
<!-- /output:video -->
```

Replace only the text between your own markers. Add your section at the end when it is missing.

## shared/brief.md

Markdown with these headings, in this order: `## Subject`, `## Audience`, `## Goal`, `## Tone`, `## Call to action`. The first skill fills what it knows. Later skills add under a heading; they never rewrite another skill's text. When the user's request contradicts the brief, ask before you change it.

## shared/facts.md

One claim per line, in this form:

```markdown
- Shorter wavelengths scatter more strongly in air (Rayleigh scattering). — https://example.org/rayleigh
- The retry queue waits 30 s before the first retry. — src/billing/retry.ts
- Support staff call a failed charge a "bounce". — user (chat, 2026-10-09)
```

Add lines; do not repeat a claim already there. Every claim a skill states in its output must trace to a line in this file. A claim without a source does not go in.

## shared/brand.json

```json
{
  "palette": { "background": "#0E1A2B", "text": "#F4F1EA", "accent": "#FFB000" },
  "fonts": [{ "family": "Manrope", "weights": [500, 800], "role": "heading" }],
  "logo": "shared/images/logo.png",
  "voice": "Warm, clear, curious."
}
```

All keys are optional, and `palette` may hold more named colors. The first skill to settle a look writes this file. Later skills use it, so all outputs match. Change it only when the user asks for a new look.

## shared/ui-map.md

What the real product's UI contains, as observed in a browser, never guessed. One `## <route>` heading per page, with its fields, buttons, and their exact labels, then the flows a user takes:

```markdown
## /items/new
- Name: text input, required
- Category: select (5 options)
- Create: button "Create"

## Flows
- Create an item: /items → "New Item" → fill Name, Category → "Create" → /items/<id>
```

A skill that shows how the product is operated takes the steps from this file or from the user. When neither says how something works, ask.

## shared/assets.json

```json
{
  "schema": 1,
  "assets": [
    {
      "file": "shared/screenshots/dashboard.png",
      "kind": "screenshot",
      "by": "design-product-overview-builder",
      "source": "https://app.example.com/dashboard",
      "width": 1440,
      "height": 900,
      "text": true,
      "background": "opaque",
      "rights": "user-product",
      "note": "Logged-in view, demo data"
    }
  ]
}
```

| Field | Values |
|---|---|
| `file` | Path to a file in `shared/` |
| `kind` | `screenshot`, `generated`, `frame` (a still from a rendered output), `photo`, `logo`, `recording` |
| `by` | The skill that added it |
| `source` | URL captured, image prompt, or the path or person it came from |
| `width`, `height` | Pixels |
| `text` | `true` when the image shows readable words |
| `background` | `opaque`, `transparent`, or `green` (chroma key still to remove) |
| `rights` | `user-product`, `generated`, `user-supplied`, or `third-party` (confirm before publishing) |
| `note` | Free text: what it shows, known issues |

Add one entry for each file you put in `shared/images/` or `shared/screenshots/`. Name files `<subject>-<detail>.<ext>` in lowercase with hyphens. Never overwrite a file another skill added; choose a new name. Before you use an asset, check `text`, `background`, and `rights` against your skill's own rules.
