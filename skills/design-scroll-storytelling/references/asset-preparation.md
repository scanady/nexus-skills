# Asset Preparation

Flat images carry the whole depth illusion. A white box around a "floating" bottle kills it. Inspect, judge, tell the user, then build. Order matters: assets first, markup second.

Agent inspects and advises. Agent never removes a background or edits an image on its own. `scripts/inspect-assets.py` is read-only. When the user asks for a cut-out and you make one, it is a new file: see section 8.

## 1. Inspect

```bash
python scripts/inspect-assets.py path/to/images/ other.png
python scripts/inspect-assets.py hero.jpg --json
python scripts/inspect-assets.py path/to/project              # has project.json
python scripts/inspect-assets.py path/to/project/shared/assets.json
```

Needs Pillow (`pip install Pillow`). Per image it reports format, mode, size, file weight, border background class, suggested depth, and size overruns against the budget. Details in the script docstring.

Given a project folder or its `shared/assets.json`, it inspects every image the list names, plus any image in `shared/images/` or `shared/screenshots/` the list misses. Each result shows the entry's fields (`shared:` line, `"shared"` in JSON) and `FLAG:` lines (`"flags"`) for what the user must answer:

| `assets.json` says | Script does | You do |
|---|---|---|
| `background: transparent` | Float candidate; flags it when the edge is not `CLEAN` | Check the file when flagged |
| `background: green` | Removal `needs keying`, flagged | Ask the user: key it out (section 8) or use another asset |
| `background: opaque` | Removal `unlikely`: a fill | Float it only when the user says so |
| `text: true` | Note | Keep it readable, give it real alt text, keep it off fast or blurred layers |
| `rights: third-party` | Flagged | Confirm the user may publish it before the page ships |
| Image not listed | Flagged | Ask the user where it came from |

A listed file that is not there shows as `MISSING`. Skip it; it does not fail the run.

| Status | Meaning |
|---|---|
| `CLEAN` | Real transparency around the edge. Use as is |
| `SOLID_DARK` / `SOLID_LIGHT` / `SOLID_MID` | One flat colour at the edge. Maybe a studio backdrop |
| `COMPLEX` | Edge colours vary. Probably a scene, shot, or screenshot |
| `OPAQUE_ALPHA` | Has an alpha channel but every pixel opaque. Cutout never done |
| `ERROR` | Could not open |
| `MISSING` | Listed in `shared/assets.json`, file not there |

Script finds the background. YOU decide if it matters.

## 2. Judge: Float Or Fill?

One question: **does this image need to float freely over other content?**

Yes → background must go.
No, it fills a space or IS the content → keep it.

| Remove background | Keep background |
|---|---|
| Isolated product on studio backdrop | Website, app, dashboard screenshot |
| Character or figure that floats in scene | Photo used as section background |
| Logo or icon placed on any depth | Artwork, poster, illustration seen whole |
| Any level 2–3 element floating over content | Device mockup, image-in-a-card |
| Background colour clashes with page | Anything at level 0 (it IS the background) |

A solid colour edge points to "remove". A complex edge points to "keep". Both are hints only. A dark studio shot with a dark site might just blend. A branded colour panel might be the design.

JPEG and most JPG files never hold transparency. If it must float, user supplies a PNG/WebP cutout.

## 3. Plan Depth, Size, Role

Before code, decide for each asset:

1. Role in the story: float beside hero, BE the hero, fill a section, ride a sidebar, decorate an edge.
2. Depth level (0–5). Product default = 3. Background default = 0.
3. Display size from the hero hierarchy in `depth-system.md`.
4. Resize target from the table.

| Level | Role | Max edge |
|---|---|---|
| 0 | Background fill | 1920px |
| 1 | Glow / atmosphere | 800–1000px |
| 2 | Decoration, companion | 400px |
| 3 | Hero | 1200px |
| 4 | UI image | 600–800px |
| 5 | Particle | 128px |

Never embed a bigger file than the level needs. Also check weight against budgets in `scroll-performance.md`.

## 4. Tell The User, Before HTML

Show an asset audit first. Wait for an answer on any flagged item. In a non-interactive run, state the assumption you took and mark it.

Flagged image:

> ⚠️ **Asset notice: `bottle.jpg`**
> JPEG with a solid white background. On the page it will show as a white box, not a floating bottle.
> Role: hero product, depth 3. I think the background should be **removed**.
>
> Options:
> 1. Send a transparent PNG/WebP. Best quality.
> 2. Use a CSS blend as a stand-in (`multiply`). Quick, approximate.
> 3. Keep the background, if the box is intended.
>
> Which one?

Clean image:

> ✅ **`glow.png`**: transparent PNG, resize to 800px, depth 1 (atmosphere)

Keep image:

> 🔵 **`dashboard.png`**: screenshot, keep its background, depth 3, 1200px

Shared asset with flags:

> ⚠️ **`shared/images/mascot-green.png`**: generated mascot on a green screen, third-party rights.
> Role: companion, depth 2. Before it can float, the green must be keyed out, and you need to confirm it may be published.
> Key it out and use it, or leave it out?

In prototype mode, save the audit to `scroll/work/asset-audit.md`.

## 5. Blend Stand-In (Only If User Picks Option 2)

```css
.on-dark-site  { mix-blend-mode: screen; }    /* black pixels vanish */
.on-light-site { mix-blend-mode: multiply; }  /* white pixels vanish */
```

```html
<!-- CSS approximation: bottle.jpg has a solid background.
     Replace with a transparent cutout for best quality. -->
```

Limits:
- `screen` lightens mid-tones. Needs a very dark page.
- `multiply` darkens mid-tones. Needs a very light page.
- Fails on gradients and complex edges.
- Real cutout always wins.

## 6. CSS For Cutouts

```css
.cutout { filter: drop-shadow(0 30px 60px rgb(0 0 0 / .4)); }   /* follows the pixel shape */
```

Never on a cutout:
- `box-shadow`: draws a rectangle.
- `border-radius` or parent `overflow: hidden` for shaping: clips transparency into a box.
- `object-fit: cover`: stretches the cutout out of shape.
- `background-color`: shows the bounding box.

## 7. Copy Into The Deliverable

The page uses copies, never files in a project's `shared/` folder. Copy each chosen image, resized to its level, into the deliverable's asset folder: `scroll/assets/` in prototype mode, the app's asset folder in-app. Keep the original name, or a shorter one in lowercase with hyphens. The page then works when the folder moves.

## 8. Publish A Cut-Out To `shared/`

Only when the user asked for it. When you make a new image from an asset, such as a background-removed or chroma-keyed cut-out, and a project folder is in use:

1. Save it to `shared/images/` under a new name: `<subject>-<detail>-cutout.png` (or `.webp`). Never overwrite the original or any file another skill added.
2. Add an entry to `shared/assets.json` (read, change, write; keep every entry you did not make):

   ```json
   {
     "file": "shared/images/bottle-cutout.png",
     "kind": "photo",
     "by": "design-scroll-storytelling",
     "source": "shared/images/bottle.jpg",
     "width": 1200,
     "height": 1600,
     "text": false,
     "background": "transparent",
     "rights": "user-supplied",
     "note": "Background removed from shared/images/bottle.jpg"
   }
   ```

   `kind`, `text`, and `rights` come from the original's entry. For an original from outside the project, `source` is the path the user gave and `rights` is `user-supplied` unless the user says otherwise.
3. Copy the cut-out into the deliverable's asset folder as in section 7.

Without a project folder, save the cut-out next to the deliverable's assets under a new name. The original stays untouched either way.

## Handoff

Give the user: audit list, depth + size plan per asset, open questions. Then build.
