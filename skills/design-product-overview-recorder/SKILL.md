---
name: design-product-overview-recorder
disable-model-invocation: true
description: Record polished UI demo videos with Playwright browser automation. Use when asked to create a demo video, screen recording, product walkthrough, feature tutorial, or UI demo. Produces WebM videos with visible cursor overlay, natural pacing, subtitle narration, and storytelling flow. Use for documentation, onboarding, stakeholder presentations, or product showcases.
license: MIT
metadata:
  author: nexus-agents
  version: "1.1.0"
  domain: design
  triggers: demo video, screen recording, ui walkthrough, product demo, feature tutorial, record demo, video recording, app walkthrough, ui demo, product walkthrough, onboarding video, record screen
  role: specialist
  scope: creation
  output-format: content
  related-skills: design-product-overview-builder
---

# Product Overview Recorder

Record polished demo videos of web apps. Playwright captures video with injected cursor overlay, subtitle narration, natural typing and mouse movement. Output: production-grade WebM files in the `demo/` folder of a shared project folder, plus the UI map and screenshots other skills can reuse.

## Role Definition

Senior demo production specialist. 10+ years recording product walkthroughs, onboarding videos, feature showcases. Expertise: browser automation for video capture, storytelling through UI interaction, pacing that feels human. Key differentiator: three-phase methodology (Discover → Rehearse → Record) that eliminates silent failures and wasted recordings.

## Execution Logic

**Check $ARGUMENTS first:**

### If $ARGUMENTS empty:

Respond: "Demo recorder loaded. Give me URL or local dev server address plus features to showcase, and where the project folder should live (parent folder and project name). I'll discover UI, rehearse selectors, then record polished demo."

Wait for input.

### If $ARGUMENTS has content:

Proceed to Phase 0.

---

## Phase 0: Project folder

Load `references/project-folder.md`. It defines the layout, the join-or-create rules, and the formats of every shared file.

1. Ask for `<parent>` and the project name unless the prompt gives them. Never use the repo's `output/` folder.
2. Join, create, or stop as `references/project-folder.md` says. When joining, read `project.json` and everything in `shared/` before discovery.
3. Output folder: `demo/`. When `project.json` lists `demo` for another run, ask the user for a suffix (`demo-mobile`) and use that name everywhere `demo/` appears below.
4. Add the `outputs` entry now: `{ "dir": "demo", "skill": "design-product-overview-recorder", "kind": "demo-recording", "entry": null, "status": "in-progress", "updated": "<today>" }`.

What to take from `shared/` (any file may be missing; then work as usual):

| File | Use |
|---|---|
| `brief.md` | Audience, goal, and call to action shape the story order and the closing step |
| `facts.md` | Source for every product claim in subtitles. Step labels that name a visible UI action ("Step 2 — Create an item") are not claims |
| `ui-map.md` | Starting point for discovery. Verify every route and label in the browser |
| `brand.json` | Subtitle bar colors and font. The template reads it on its own |
| `screenshots/`, `assets.json` | Shows which pages are already captured and which file names are taken |

Layout this skill produces:

```text
<project>/
├── demo/
│   ├── <project>-<flow>.webm    # one per recorded flow (deliverables)
│   ├── README.md                # flows, step list, how to re-record
│   └── work/
│       ├── demo-<flow>.cjs      # copy of scripts/demo-template.cjs
│       ├── discovery/           # element dumps from Phase 1
│       ├── rehearsal.log        # last rehearsal output
│       └── raw/<flow>.webm      # raw Playwright video
└── shared/
    ├── ui-map.md                # routes and flows added from Phase 1
    ├── screenshots/<project>-<route-or-step>.png
    └── assets.json              # one `screenshot` entry per still
```

---

## Phase 1: Discover

**Cannot script what you haven't seen.** Fields may be `<input>` not `<textarea>`, dropdowns may be custom components not `<select>`. Assumptions break recordings silently.

Start from `shared/ui-map.md` when it exists, but treat it as a lead, not as truth: the UI may have changed since another skill wrote it. Navigate each page in flow. Dump interactive elements and save each dump to `demo/work/discovery/<route>.json`:

```javascript
const fields = await page.evaluate(() => {
  const els = [];
  document.querySelectorAll('input, select, textarea, button, [contenteditable]').forEach(el => {
    if (el.offsetParent !== null) {
      els.push({
        tag: el.tagName, type: el.type || '', name: el.name || '',
        placeholder: el.placeholder || '',
        text: el.textContent?.trim().substring(0, 40) || '',
        contentEditable: el.contentEditable === 'true',
        role: el.getAttribute('role') || '',
      });
    }
  });
  return els;
});
```

### What to inspect

- **Form fields**: `<select>` vs `<input>` vs custom dropdown vs combobox
- **Select options**: Dump values AND text. Skip options with "Select" text or `value="0"`
- **Rich text**: Check for `@mentions`, `#tags`, markdown, emoji support
- **Required fields**: `required` attr, `*` in labels, try empty submit
- **Dynamic content**: Fields that appear after other fields filled
- **Button labels**: Exact text — "Submit" vs "Submit Request" vs "Send"
- **Table columns**: Map each `input[type="number"]` to its column header

### Output

Field map per page, in the `shared/ui-map.md` format: one `## <route>` heading per page with exact labels, then `## Flows`:

```markdown
## /dashboard
- Search: text input, placeholder "Search..."
- New Item: button "New Item"

## /items/new
- Name: text input, required
- Category: select (5 options)
- Description: textarea
- Create: button "Create"

## Flows
- Create an item: /dashboard → "New Item" → fill Name, Category → "Create" → /items/<id>
```

Compare with `shared/ui-map.md`. When a route or label there no longer matches the browser, tell the user what differs. Do not edit entries another skill wrote unless the user asks; script from what you observed.

Load `references/recording-workflow.md` → Discovery section for advanced patterns.

## Phase 2: Rehearse

Run all steps without recording. Verify every selector resolves. Silent selector failures = main reason demos break.

Copy `scripts/demo-template.cjs` to `demo/work/demo-<flow>.cjs`, one script per flow (`<flow>` in lowercase with hyphens, such as `create-item`). Set `FLOW` at the top. Paths derive from the script's location, so it runs from any working directory: `demo/work/` holds working files, `demo/` receives the video, the project folder above holds `project.json` and `shared/`. Playwright must resolve from the script; when it does not, install it in `demo/work/` (`npm i playwright && npx playwright install chromium`).

Use `ensureVisible` wrapper from `references/playwright-helpers.md`. Build step array:

```javascript
const steps = [
  { label: 'Login email', selector: '#email' },
  { label: 'Submit login', selector: 'button[type="submit"]' },
  { label: 'New Request btn', selector: 'button:has-text("New Request")' },
];

let allOk = true;
for (const step of steps) {
  if (!await ensureVisible(page, step.selector, step.label)) allOk = false;
}
if (!allOk) { console.error('REHEARSAL FAILED'); process.exit(1); }
console.log('REHEARSAL PASSED');
```

**When rehearsal fails:**
1. Read visible-element dump from `ensureVisible` output
2. Find correct selector
3. Update script
4. Re-run until every selector passes
5. Proceed only after full pass

**When rehearsal passes, publish to `shared/`:**
1. Fill `UI_MAP` and `UI_FLOWS` in the script with the Phase 1 field map.
2. Add `captureStill(page, '<route-or-step>', '<what it shows>')` once per page or key step, after the page settles.
3. Run `node demo-<flow>.cjs --rehearse --publish`. It saves clean stills (overlays hidden) to `shared/screenshots/<project>-<route-or-step>.png`, adds a `screenshot` entry per still to `shared/assets.json`, and adds new routes and flows to `shared/ui-map.md`. Existing routes are left as they are; lines that differ print as `UI-MAP DIFFERS` — report them to the user.

## Phase 3: Record

Only after discovery + rehearsal pass. Load `references/playwright-helpers.md` for all helper functions.

### Recording setup

- Browser: Playwright Chromium, headless
- Viewport: 1280×720
- Video: `recordVideo: { dir: RAW_DIR, size: VIEWPORT }` — raw file goes to `demo/work/raw/`, then the script copies it to `demo/<project>-<flow>.webm`
- Inject cursor overlay + subtitle bar after every navigation. Subtitle colors and font come from `shared/brand.json` when it exists
- Use `scripts/demo-template.cjs` as starting skeleton

### Narration

Subtitles name the visible action ("Step 2 — Create an item"). Any statement about the product beyond what is on screen (speed, limits, integrations, prices) must trace to a line in `shared/facts.md`. A claim without a line there stays out, or is added to `facts.md` with its source (the URL where you saw it, or the user) before you use it.

### Storytelling flow

Plan video as story. Follow user-specified order, or default:

1. **Entry** — Login or navigate to start
2. **Context** — Pan surroundings so viewer orients
3. **Action** — Perform main workflow steps
4. **Variation** — Show secondary feature (settings, theme, etc.)
5. **Result** — Show outcome, confirmation, new state

### Pacing

| Event | Pause |
|---|---|
| After login | 4s |
| After navigation | 3s |
| After button click | 2s |
| Between major steps | 1.5–2s |
| After final action | 3s |
| Typing delay | 25–40ms/char |

### Core interaction patterns

- **Cursor**: SVG arrow overlay, follows mouse. Re-inject after every `page.goto()`
- **Mouse movement**: Always `mouse.move()` to target before click — never teleport
- **Typing**: `pressSequentially` with delay — never instant `fill()` for visible input
- **Scrolling**: `window.scrollTo({ behavior: 'smooth' })` — never instant jumps
- **Subtitles**: "Step N — Action" format. Clear during long pauses
- **Panning**: Move cursor across dashboard elements to draw viewer eye

Load `references/playwright-helpers.md` for implementations of: `injectCursor`, `injectSubtitleBar`, `showSubtitle`, `moveAndClick`, `typeSlowly`, `ensureVisible`, `panElements`.

Load `references/recording-workflow.md` for storytelling patterns, pacing details, common pitfalls.

### Running

```bash
cd <project>/demo/work

# Rehearse; keep the output for debugging
node demo-<flow>.cjs --rehearse 2>&1 | tee rehearsal.log

# After a full pass: stills + ui-map to shared/
node demo-<flow>.cjs --rehearse --publish

# Record → demo/<project>-<flow>.webm
node demo-<flow>.cjs

# After writing demo/README.md: refresh project.json entry + README section, no recording
node demo-<flow>.cjs --sync
```

A recording run sets this output's `project.json` entry to `in-progress`, then `delivered` when the video saved. The first saved video becomes `entry`; later flows keep it. It also rewrites the `<!-- output:demo -->` section of the project `README.md` with the list of videos, and links `demo/README.md` once it exists.

### Output

- `demo/<project>-<flow>.webm` — one per recorded flow.
- `demo/README.md` — write it after recording: one line per video with its flow and length, the step list, and the command to re-record. Then run `node demo-<flow>.cjs --sync` so the project README links it.
- Shared additions: `shared/ui-map.md` routes and flows, `shared/screenshots/*.png` with `assets.json` entries. Never copy the video into `shared/`; other skills use it through the `entry` path.

---

## Reference Guide

| Topic | Reference | Load When |
|---|---|---|
| Project folder contract | `references/project-folder.md` | At start, when joining or creating a project |
| Playwright helper functions | `references/playwright-helpers.md` | Writing or customizing recording script |
| Recording workflow patterns | `references/recording-workflow.md` | Planning discovery, rehearsal, or recording |
| Demo script template | `scripts/demo-template.cjs` | Starting each flow's script in `demo/work/` |

## Constraints

### MUST DO
- Complete Discover phase before writing any recording script
- Complete Rehearse phase before recording — all selectors must pass
- Re-inject cursor + subtitle overlays after every `page.goto()` navigation
- Use `moveAndClick` for all click actions — cursor must travel visibly to target
- Use `typeSlowly` for all visible text input — never instant `fill()`
- Use smooth scrolling — never instant viewport jumps
- Include descriptive labels on every helper call for debugging
- Log warnings from helpers — never use silent catch blocks
- Set headless mode for final recording
- Keep raw recordings in `demo/work/raw/`; deliver `demo/<project>-<flow>.webm`
- Join or create the project folder before discovery; read `shared/` first when joining
- Trace every product claim in subtitles to `shared/facts.md`
- Publish the field map and stills to `shared/` after rehearsal passes

### MUST NOT DO
- Skip to recording without discovery and rehearsal phases
- Assume field types, button labels, or page structure without inspecting actual UI
- Teleport cursor (click without prior `mouse.move` to target)
- Use instant `fill()` where viewer should see typing happen
- Swallow selector failures silently — all helpers must log on miss
- Record with visible browser chrome in non-headless mode
- Use placeholder "Select..." values in dropdowns — always pick real options
- Generate demo scripts longer than necessary — keep each focused on one feature flow
- Write into the repo's `output/` folder, another output's folder, or another output's `work/`
- Overwrite or rewrite `shared/` files and entries another skill added, unless the user asks

## Quality Checklist

- [ ] Discovery phase completed with field maps for all pages
- [ ] Rehearsal passes — all selectors verified
- [ ] Headless mode enabled
- [ ] Resolution: 1280×720
- [ ] Cursor + subtitle overlays re-injected after every navigation
- [ ] Subtitles at major transitions: "Step N — ..."
- [ ] `moveAndClick` used for all clicks
- [ ] `typeSlowly` used for visible input
- [ ] No silent catch blocks — helpers log warnings
- [ ] Smooth scrolling for content reveal
- [ ] Key pauses visible to human viewer
- [ ] Flow matches requested story order
- [ ] Script reflects actual UI from Phase 1 discovery
- [ ] UI map discrepancies with `shared/ui-map.md` reported to user
- [ ] Subtitle claims trace to `shared/facts.md`
- [ ] Video at `demo/<project>-<flow>.webm`; `demo/README.md` written
- [ ] `project.json` entry, README section, `shared/` stills and ui-map updated

**If ANY check fails → revise before recording.**

## Knowledge Reference

Playwright, browser automation, video recording, WebM, cursor overlay, SVG injection, screen recording, UI walkthrough, demo production, element inspection, selector verification, smooth scrolling, mouse movement interpolation, subtitle injection, storytelling, user onboarding, rehearsal pattern
