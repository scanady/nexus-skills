# Prompt Assembly

One master template, built on the architecture. The four aesthetics are material swaps, not separate templates — the room's geometry, light plan, and grouping rules don't change when the finish does.

## Master template

Fill every bracket. Keep insertions as short phrases. Drop a clause entirely rather than filling it with a placeholder.

```
Editorial environmental portrait of a room, photorealistic, 16:9, [AESTHETIC LINE], shot on 35mm at f/5.6, camera at seated eye height, 2.6 meters back from the back wall, tight enough that the desk edge crosses and crops the bottom of the frame, sharp from the near shelving through to the back wall.

ROOM: a corner — [WALL MATERIAL] back wall square to camera, window wall running away in perspective at frame left, [CEILING FEATURE] crossing the top of the frame.

LIGHT: low late-afternoon sun through the window at frame left, raking shallow across the back wall in long bars with mullion shadows, crossing the shelf line; [PRACTICAL 1] concealed under the shelf, grazing the spines and backlighting the glassware so it glows from within; [PRACTICAL 2] low at the far edge of the desk throwing one small warm pool; no exposed bulb hanging in frame; the far right corner and the ceiling falling two stops into shadow with detail holding; cool daylight left, warm tungsten right.

CENTER: [CENTER ANCHOR SURFACE], a slim-framed board hung flat on the face of the wall with a marker tray, an object on the wall and not a recessed panel, about a third of the frame wide and wider than it is tall, with sunlit wall visible above, below and to either side; [ANCHOR CONTENT] drawn in marker across its upper two thirds, lower third left open — mid-ground objects may overlap that lower corner.

LEFT: black-framed window looking onto [VIEW]; [ETHOS 1] leaning on the sill; [LIFE OBJECT] below it; a stretch of bare [WALL MATERIAL] between the window and the anchor, deliberately empty.

NEAR RIGHT: a narrow [WALL MATERIAL] bump-out projecting forward from the back wall, its face square to camera and much closer to the lens, its return side receding away to the left and catching a rim of light on the corner, [FRAMED PIECE] on the small area of its face; three open [SHELF MATERIAL] planks on slim black steel brackets spanning it, no back panel and no sides so the wall shows between and behind them, cropped by the right edge. Lowest plank, closest to camera and largest in frame, holding only books: [NAMED BOOKS] in one or two horizontal stacks lying flat with covers facing camera, largest at the bottom of each stack, no books standing upright. Middle plank: [IDENTITY OBJECT 2] lit from behind. Top plank: [ETHOS 2], [BRAND 2], a trailing plant spilling over the edge.

FAR LEFT FOREGROUND: [SOFT FOREGROUND ELEMENT] very close to the lens at the left edge, heavily out of focus and cropped by the frame.

DESK: [DESK MATERIAL] desk filling the lower quarter of the picture, running the full width, cropped by the bottom edge and hiding the floor completely, [BRAND 1] mug on a cork coaster hard against the right edge of the picture, handle turned away; [DESK ITEM] in the left quarter of the picture, out at the frame edge; the middle third of the desk completely bare with nothing on it at all. Every named title appears exactly once anywhere in the room.

PALETTE: [STRUCTURAL 1] and [STRUCTURAL 2], black steel, one [ACCENT] accent, plant green. Porous [WALL MATERIAL], cold-rolled steel, cloth bindings. Warm highlights, cool shadows, gentle filmic roll-off, fine grain.
```

**Never drop the camera distance.** It is the one token holding the frame together. Remove it and the generator picks its own, goes wide, and returns an architectural interior — beautiful, and useless as a background: the desk foreground disappears, the anchor shrinks into the wall, and its content collapses to a word list. Say the distance, say the desk crops the bottom edge, and say the anchor fills the middle of the back wall.

## Aesthetic swaps

**Industrial-chic is the default and should be the answer roughly nine times out of ten.** The others are for people who ask or who have stated a preference. Seniority, industry, and client-facing work are not reasons to switch — industrial-chic reads warmer and more personal at the same level of professionalism.

| Bracket | Industrial-Chic | Scandinavian-Minimalist | Nature-Lodge | Modern-Corporate |
|---|---|---|---|---|
| `AESTHETIC LINE` | cozy industrial-chic workroom | calm Scandinavian workroom | warm nature-lodge study | sleek modern office |
| `WALL MATERIAL` | exposed red brick | pale plaster | knotty pine board | warm-toned concrete |
| `CEILING FEATURE` | black iron pipe run | a single slim rail | exposed timber beam | a recessed light channel |
| `SHELF MATERIAL` | wood-and-black-steel | white oak | timber-and-iron | oak-and-brushed-steel |
| `DESK MATERIAL` | reclaimed wood | pale oak | live-edge timber | dark walnut |
| `PRACTICAL 1` — concealed, does the work | warm strip light hidden under the shelf | concealed shelf light | small brass picture light above the shelf | warm strip light hidden under the shelf |
| `PRACTICAL 2` — low pool, optional | small shaded desk lamp at the far edge | slim brass desk lamp | shaded amber table lamp | low warm desk lamp |
| `STRUCTURAL 1 / 2` | burnt-orange brick / warm oak | bone white / pale oak | amber pine / stone grey | warm concrete / dark walnut |

Modern-corporate keeps warm accent lighting under the shelving on purpose. Glass, steel, and cool even light are what make that aesthetic read as a render; the warmth is the antidote.

If someone asks for an aesthetic not listed, keep the geometry, the light plan, and the grouping rules exactly as they are and swap only the material, finish, and practical language.

## The legible-text budget

Text is the reason these rooms work, so budget generously and govern the medium rather than the count.

| Element | Budget |
|---|---|
| Center anchor | up to 20–25 short labels of one to three words, plus arrows and simple shapes |
| Ethos boards | one to three boards, three to eight words each |
| Book titles | up to seven titles plus three or four author surnames — **only if staged large and near camera**, see below |
| Brand marks | wordmark only, two or three placements, never a tagline |
| Desk item | up to four handwritten labels |
| Whole frame | roughly 45 to 60 legible words |

**The medium governs, the count follows.** A hand-drawn marker framework holding twenty-five labels renders cleanly — flow arrows, a labelled Venn, a feedback loop, a hand-drawn chart all survive. The same content described as a *printed diagram*, a *slide*, a *poster*, or a *screenshot* garbles at any count. So the anchor's content can be as formal as you like — Venn, flowchart, loop, chart. Never use the words printed, poster, slide, screenshot, or infographic. Always say marker on a whiteboard, hand-lettered, or handwritten.

**Never name a spine.** Spine text runs sideways and narrow, and it garbles in effectively every render regardless of distance, size, or how carefully the title is spelled out. Face-out text on a flat cover works every time.

So name titles **only** on books lying flat in a horizontal stack with covers to camera, on the nearest plank or the desk. Upright books are unnamed texture — call them "cloth-bound spines in muted blues and greens" and spend no budget on them. Better still, use few enough books that none need to stand up.

Cap it at **two horizontal stacks of three or four**, six or seven titles total. Someone would rather read four titles than squint at nine. If the cast has more books than that, cut to the most distinctive and let the rest go.

**Text needs width, not emphasis.** When a word garbles, adding "spelled correctly" to the prompt does nothing — the letters have too few pixels. Restructure so each word gets more room. A six-box flow in one row gives each box a sliver and returns `SELAUNCH`; the same six as **two rows of three** doubles the width and every word comes out clean. The same applies to a quote: cramped into a portrait frame it becomes a column of fragments; set landscape at full width it reads perfectly.

**A frame on a shelf costs a shelf.** Hang quote frames on wall face — beside the shelving, or below the lowest plank at desk height — rather than standing them on a plank, where they displace the objects the plank was for.

**Keep labels outside small shapes.** Words placed *inside* a small circle or box on the anchor garble reliably — a three-circle Venn labelled inside its circles comes back with one word mangled almost every time, and rerolling doesn't fix it. Put the labels outside, on leader lines or as a short key beside the diagram, and keep the shapes themselves empty or hatched. Boxes in a flow row are large enough to hold one word; circles in a Venn are not.

**Don't let the anchor's layout float.** Say the boxes run in a single horizontal row across the top and the bullets sit beneath them. Left unspecified, the flow rearranges itself into a tangle and the labels degrade with it.

If a cast runs over budget, cut the least distinctive items rather than shrinking everything. Five sharp titles beat nine unreadable ones.

## Negative line

Deliver on its own line after the prompt:

```
Negative: people, faces, hands, printed posters, slides, screenshots, infographic style, watermarks, third-party logos, evenly lit flat ambient lighting, evenly loaded shelves, symmetrical object spacing, plastic CGI surfaces, oversaturation, HDR halos, shallow depth of field on the shelving, fisheye distortion.
```

Where a generator has no separate negative input, phrase the same intent positively inside the prompt: "clusters with gaps between them" rather than "not evenly spaced".

## Generator notes

- **Midjourney** — append `--ar 16:9 --style raw`. Use `--no people, text-heavy posters` rather than the negative line. Lower `--stylize` when it embellishes past the brief.
- **Flux** — takes the full template nearly verbatim and rewards keeping every section. Fold the negatives into positive phrasing.
- **GPT Image / DALL·E** — rewrites what it's given, so the tail drifts. Put the anchor and the light plan early. Negatives are unreliable.
- **Gemini / Imagen** — follows long descriptive prose and camera language closely; strong at dense legible text.
- **Stable Diffusion** — the negative line works as written. Keep guidance moderate so the shadow falloff survives.

Ask for the largest resolution available. Platforms scale down and never up.

## Pre-delivery checklist

1. Is it a corner, with the window wall running away in perspective? Not one flat wall.
2. Are there three furniture planes — a cropped near unit, a mid desk, a far window? Not everything on the back wall.
3. Is every named title on the near unit rather than against the back wall?
4. Is there one heavily defocused element cropped at the opposite edge?
5. Is there exactly one hero, with the rival bright shapes actively demoted?
6. Is the near unit a bump-out with open shelves, not an angled freestanding bookcase?
7. Is the anchor a board hung on the wall rather than a panel recessed into it?
8. Is any floor visible? There should be none.
9. Did the ceiling register survive? It is the first thing to drop out.
2. Are the three registers present — ceiling feature, readable shelf band, cropped desk edge?
3. Is there a large bright center anchor with its lower third left open for the head?
4. Do both flanking verticals exist — window frame one side, tall shelving the other?
5. Are shelves loaded in clusters of three or five with gaps, varied heights, and mixed orientation?
6. Is there one deliberately near-empty area?
7. Does one object break forward past the shelf line?
8. Is the key raking and does it cross the readable band? Is there a named two-stop falloff?
9. Do both practicals say what they pool or graze onto?
10. Is the palette two structural plus black steel plus exactly one accent?
11. Is the aperture f/4 or tighter, with only the desk edge soft?
12. Is the cast at least half life rather than work? Count them.
13. Are there fifteen to twenty-five identifiable objects? Under a dozen is a showroom.
14. Is the identity object near and large in frame, not small on a high shelf?
15. Are named book titles staged flat in the foreground or at the nearest shelf edge? Distant spines get called texture instead.
16. Are the readable desk objects at the outer desk corners with the middle of the desk left clear? The torso covers the centre.
17. Does any named title appear twice? Say each appears exactly once.
18. Is every object staged — leaning, overhanging, turned, catching light?
19. Any third-party trademark that isn't the person's own employer?
20. Any adjective that doesn't correspond to a real chosen detail? Cut it.
21. Are the desk objects placed against the *frame* edges, with the middle third of the desk bare?
22. Are all named titles on flat, face-out stacks, with no spine-out title named?
23. Does any object repeat a message another object already carries?
24. Shrunk to 250 px, is there still a hero shape, a bright rectangle and one strong colour?
22. Does every anchor have both a silhouette and a detail?
23. Is the head zone smooth and low-frequency, with no foliage or hard edge behind it?
24. Are the strongest objects in the priority ring rather than against the frame edges?
25. Is anything named sitting in the bottom eighth where the name badge lands?
26. Does the window sit on the same side as the person's real key light?
