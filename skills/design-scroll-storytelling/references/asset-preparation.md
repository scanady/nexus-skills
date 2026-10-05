# Asset Preparation

Flat images carry the whole depth illusion. A white box around a "floating" bottle kills it. Inspect, judge, tell the user, then build. Order matters: assets first, markup second.

Agent inspects and advises. Agent never removes a background or edits an image on its own. `scripts/inspect-assets.py` is read-only.

## 1. Inspect

```bash
python scripts/inspect-assets.py path/to/images/ other.png
python scripts/inspect-assets.py hero.jpg --json
```

Needs Pillow (`pip install Pillow`). Per image it reports format, mode, size, file weight, border background class, suggested depth, and size overruns against the budget. Details in the script docstring.

| Status | Meaning |
|---|---|
| `CLEAN` | Real transparency around the edge. Use as is |
| `SOLID_DARK` / `SOLID_LIGHT` / `SOLID_MID` | One flat colour at the edge. Maybe a studio backdrop |
| `COMPLEX` | Edge colours vary. Probably a scene, shot, or screenshot |
| `OPAQUE_ALPHA` | Has an alpha channel but every pixel opaque. Cutout never done |
| `ERROR` | Could not open |

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

## Handoff

Give the user: audit list, depth + size plan per asset, open questions. Then build.
