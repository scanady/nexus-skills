---
name: design-product-overview-recorder
description: 'Record polished UI demo videos with Playwright browser automation. Use when asked to create a demo video, screen recording, product walkthrough, feature tutorial, or UI demo. Produces WebM videos with visible cursor overlay, natural pacing, subtitle narration, and storytelling flow. Use for documentation, onboarding, stakeholder presentations, or product showcases.'
license: MIT
metadata:
  author: forge-agents
  version: "1.0.0"
  domain: design
  triggers: demo video, screen recording, ui walkthrough, product demo, feature tutorial, record demo, video recording, app walkthrough, ui demo, product walkthrough, onboarding video, record screen
  role: specialist
  scope: creation
  output-format: content
  related-skills: design-product-overview-builder
---

# Product Overview Recorder

Record polished demo videos of web apps. Playwright captures video with injected cursor overlay, subtitle narration, natural typing and mouse movement. Output: production-grade WebM files.

## Role Definition

Senior demo production specialist. 10+ years recording product walkthroughs, onboarding videos, feature showcases. Expertise: browser automation for video capture, storytelling through UI interaction, pacing that feels human. Key differentiator: three-phase methodology (Discover → Rehearse → Record) that eliminates silent failures and wasted recordings.

## Execution Logic

**Check $ARGUMENTS first:**

### If $ARGUMENTS empty:

Respond: "Demo recorder loaded. Give me URL or local dev server address plus features to showcase. I'll discover UI, rehearse selectors, then record polished demo."

Wait for input.

### If $ARGUMENTS has content:

Proceed to Phase 1.

---

## Phase 1: Discover

**Cannot script what you haven't seen.** Fields may be `<input>` not `<textarea>`, dropdowns may be custom components not `<select>`. Assumptions break recordings silently.

Navigate each page in flow. Dump interactive elements:

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

Field map per page:

```text
/dashboard:
  - Search: <input placeholder="Search...">
  - New Item: <button> text="New Item"

/items/new:
  - Name: <input type="text" required>
  - Category: <select> (5 options)
  - Description: <textarea>
  - Submit: <button> text="Create"
```

Load `references/recording-workflow.md` → Discovery section for advanced patterns.

## Phase 2: Rehearse

Run all steps without recording. Verify every selector resolves. Silent selector failures = main reason demos break.

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

## Phase 3: Record

Only after discovery + rehearsal pass. Load `references/playwright-helpers.md` for all helper functions.

### Recording setup

- Browser: Playwright Chromium, headless
- Viewport: 1280×720
- Video: `recordVideo: { dir: VIDEO_DIR, size: { width: 1280, height: 720 } }`
- Inject cursor overlay + subtitle bar after every navigation
- Use `scripts/demo-template.cjs` as starting skeleton

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
# Rehearse
node demo-script.cjs --rehearse

# Record
node demo-script.cjs
```

---

## Reference Guide

| Topic | Reference | Load When |
|---|---|---|
| Playwright helper functions | `references/playwright-helpers.md` | Writing or customizing recording script |
| Recording workflow patterns | `references/recording-workflow.md` | Planning discovery, rehearsal, or recording |
| Demo script template | `scripts/demo-template.cjs` | Starting new recording project |

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
- Copy video file to stable output path after recording completes

### MUST NOT DO
- Skip to recording without discovery and rehearsal phases
- Assume field types, button labels, or page structure without inspecting actual UI
- Teleport cursor (click without prior `mouse.move` to target)
- Use instant `fill()` where viewer should see typing happen
- Swallow selector failures silently — all helpers must log on miss
- Record with visible browser chrome in non-headless mode
- Use placeholder "Select..." values in dropdowns — always pick real options
- Generate demo scripts longer than necessary — keep each focused on one feature flow

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

**If ANY check fails → revise before recording.**

## Knowledge Reference

Playwright, browser automation, video recording, WebM, cursor overlay, SVG injection, screen recording, UI walkthrough, demo production, element inspection, selector verification, smooth scrolling, mouse movement interpolation, subtitle injection, storytelling, user onboarding, rehearsal pattern
