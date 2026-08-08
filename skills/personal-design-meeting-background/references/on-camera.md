# On Camera

How the room behaves once a person and a platform get in front of it. Everything else in this skill designs a picture; this file designs a *composite*.

## Four viewing states, not one

The same background is seen at wildly different sizes in the same meeting, and each state rewards something different.

| State | Rough width | What survives | What's wasted |
|---|---|---|---|
| Picture-in-picture, screen sharing | 120–200 px | large shapes, value blocks, one strong colour | everything else |
| Participant tile, gallery view | 200–350 px | silhouettes, bright rectangles, glowing objects | all text, all small props |
| Speaker / spotlight | 700–1400 px | book titles, letterboards, the framework, materials | nothing |
| Full screen | 1900 px+ | fine texture, grain, the clay on the tyres | nothing |

Gallery view is where people spend most of a meeting. Speaker view is where they look closely at *you*. A room designed only for one of the two fails badly in the other — and the common failure is designing for speaker view, where the density is rewarding, and ending up with grey mush in the tile.

## Two-tier casting

**Every anchor needs an expression at both scales.** Each personal fact should be carried by one large shape *and* one fine detail, so it exists in gallery view and pays off in speaker view.

| Anchor | Tier 1 — silhouette, reads at 200px | Tier 2 — detail, reads at 1000px |
|---|---|---|
| A sport or craft | the whole object: a bike, a cello case, a board | dried clay on the tyres, rosin dust, worn grip tape |
| Brewing or making | a big glowing vessel, lit from behind | hydrometer, grain jar, crock, labels |
| The framework | a bright rectangle against a dark wall | the boxes, arrows and labels on it |
| Books | a warm block of stacked colour | the titles and author names |
| A place | a bright window shape | the trail, the moss, the water |
| Brand | *(none)* | a small wordmark |

Two things fall out of that table.

**A slot with no tier-1 expression is invisible most of the time.** Brand has no silhouette, which is the honest answer to how much a logo is worth here: it only exists when someone is looking closely at you anyway. Don't over-invest in it.

**Tier 1 is built from light, not from objects.** The things that survive at 200px are the bright rectangle, the glowing carboy, the sunlit window, the warm bands under the shelves, and the one saturated accent. That is a lighting job, which is why the light plan is not decoration.

Test it: shrink the finished image to 250 px wide and look. If you can still tell there is a bike, a bright board, and something glowing amber, it works. If it is a brown smear, rebuild tier 1.

## The frame map

Two constraints bite at once — the person covers the middle, and platforms crop the edges. Gallery tiles and phone clients crop hardest, so the outer margin is unreliable.

```
        0%    10%      28%   38%          62%   72%      90%   100%
        │ crop │ second │ ▸PRIORITY│  head zone  │PRIORITY◂│ second │ crop │
 0%  ───┼──────┴────────┴──────────┴─────────────┴─────────┴────────┴──────
        │            ceiling register — texture and structure only
 20% ───┤      ┌────────────────────────────────────────────┐
        │      │        THE READABLE BAND                   │
        │      │   the portrait happens between these lines │
 60% ───┤      └────────────────────────────────────────────┘
        │            desk register — torso covers the middle
 88% ───┼──────────────────────────────────────────────────────────────
        │ ▓▓ UI chrome: name badge bottom-left, controls bottom-centre ▓▓
100% ───┴──────────────────────────────────────────────────────────────
```

| Band | Width | Put here |
|---|---|---|
| **Crop margin** | outer 0–10% each side | falloff, texture, nothing named — assume it can be cut |
| **Second read** | 10–28% and 72–90% | the window and view, the shelving mass, secondary clusters |
| **Priority ring** | 28–38% and 62–72% | the strongest objects. This is the only real estate visible in *every* view, including phone clients that crop to portrait |
| **Head zone** | 38–62% | the calm anchor surface and nothing else |

The priority ring is the correction to "push everything outward". Flanking the head is the most-seen ground in the frame; the extreme edges are the least reliable. Put the hero where it brackets the person, not where it hugs the border.

Vertically, keep named objects out of the **bottom 12%** — the platform prints the name badge over the bottom-left and meeting controls across the bottom-centre. A stack of legible book titles in the bottom-left corner will have a name label sitting on it.

Asking for the stack to be "raised clear of the corner" does not work; generators put a desk stack on the desk, at the bottom edge, whatever you say. **Move it instead of raising it — put the named books at the desk's right and the notebook at the left.** The badge only occupies the bottom-left, so the right-hand corner is free. Losing the bottom title of a left-hand stack is the alternative, and it is always the title you can least afford, because the largest book sits at the bottom.

## Segmentation

Platforms cut the person out with a matte, and the matte fails in predictable places. This is what actually makes a background look cheap on a call.

- **Low frequency behind the head.** Hair against brick joints, book spines, or foliage produces chewed edges and haloing. The area behind the head must be smooth: a plain board, a bare wall, a soft gradient. This is the strongest argument for the bright centre anchor — stronger than the compositional one.
- **Foliage is the worst case.** Never put a plant directly behind where the head sits.
- **Value-distinct from hair.** Dark hair wants a lighter surface behind it; light, grey, or no hair wants a mid-to-dark surface. Ask, and set the anchor's brightness accordingly.
- **No hard vertical edge in the head zone.** Mattes tear along them, and the tear is visible whenever the person leans.
- **Assume movement.** People lean, gesture, and turn. Every edge failure above becomes twice as visible in motion, which is another reason the calm zone has to be genuinely calm rather than merely dim.

## Matching the person, not just the room

A composite reads as fake when the two halves disagree about physics.

- **Light direction.** Ask which side their real key light comes from and put the window on that side. This skill defaults to frame left; that default is a guess, and a mismatch — face lit from the right, background sun from the left — is one of the few tells a viewer notices without knowing why.
- **Colour temperature.** Keep the global grade close to neutral and carry the warmth in the raking beam, the practicals, and the accent. A blanket golden wash fights whatever white balance their real room has.
- **Skin-tone separation.** The surface immediately behind and beside the head should sit away from skin hues or be clearly separated in value and saturation. Warm orange brick directly behind a face is the worst common case; desaturated and cooler surfaces flatter every skin tone.
- **Depth cues.** The person is sharp. A heavily blurred background makes them look pasted on, which is why this skill shoots f/4 rather than wide open.

## Tell them about the mirror

Most platforms mirror the user's own self-view and show everyone else the correct image. Their letterboards and book titles will look backwards *to them* and read correctly to the meeting. Say so when handing over — otherwise the first reaction is that the image is broken, and the instinct is to flip it, which breaks it for everybody else.

## The on-camera check

1. Shrink to 250 px. Can you still see a hero shape, a bright rectangle, and one strong colour?
2. Is every anchor expressed as both a silhouette and a detail?
3. Is the head zone smooth, low-frequency, and value-distinct from their hair?
4. Any foliage or hard vertical edge behind the head?
5. Are the strongest objects in the priority ring rather than jammed against the edges?
6. Is anything named sitting in the bottom 12%, where the name badge lands?
7. Does the light come from the same side as their real key?
8. Is the surface beside the head away from skin hues?
