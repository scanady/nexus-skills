# Recording Workflow Patterns

Storytelling structure, discovery techniques, pacing calibration, and pitfall avoidance for demo recordings.

---

## Discovery Techniques

### Element Dump

Core discovery pattern. Run on every page before scripting any interaction:

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
console.log(JSON.stringify(fields, null, 2));
```

### Select Option Dump

Dropdowns need extra inspection. Placeholder options look non-empty but are useless:

```javascript
const options = await page.evaluate(() => {
  return Array.from(document.querySelectorAll('select')).map(sel => ({
    name: sel.name,
    options: Array.from(sel.options).map(o => ({ value: o.value, text: o.text }))
  }));
});
```

Skip options where text includes "Select" or value is `"0"` or `""`.

### Table Column Mapping

Table-driven forms: map each input to its column header. Do not assume all numeric inputs serve same purpose.

### Field Map Template

```text
/<route>:
  - Field Name: <tag> (additional details)
  - Button: <button> text="Exact Label"
  - Table: describe inline-editable pattern
```

---

## Storytelling Flow

### Default Story Arc

| Phase | Purpose | Example |
|---|---|---|
| **Entry** | Login or navigate to start | Land on login, authenticate |
| **Context** | Orient viewer | Pan dashboard, show navigation |
| **Action** | Main workflow | Create item, fill form, submit |
| **Variation** | Secondary capability | Toggle theme, change settings |
| **Result** | Show outcome | Confirmation, new data in list |

Follow user-specified order when provided. Default arc when no preference given.

### Planning Tips

- Map each step to specific URL + UI state before scripting
- Group by navigation path — minimize back-and-forth
- Show populated states, never empty screens
- End on positive outcome (success, completed item)

---

## Pacing Calibration

| Event | Pause | Reason |
|---|---|---|
| After login | 4s | Viewer reads dashboard |
| After navigation | 3s | Orient to new page |
| After button click | 2s | See result of action |
| Between major steps | 1.5–2s | Mental transition |
| After final action | 3s | Absorb outcome |
| Typing delay | 25–40ms/char | Looks natural |
| After scroll | 1.5s | Scan new content |
| Before modal dismiss | 1.5s | Read modal content |

These timings tested across demo audiences. Faster = rushed. Slower = boring.

---

## Common Pitfalls

| # | Problem | Cause | Fix |
|---|---|---|---|
| 1 | Cursor disappears after nav | Overlay destroyed on `page.goto()` | Re-inject `injectOverlays(page)` after every navigation |
| 2 | Video too fast | Missing pauses | Add `waitForTimeout` per pacing guide |
| 3 | Cursor is dot, not arrow | Using browser default cursor | Use SVG overlay from `playwright-helpers.md` |
| 4 | Cursor teleports | Clicking without `mouse.move` | Always use `moveAndClick` |
| 5 | Select looks wrong | Instant value set without visual | Move to dropdown, click open, pick option |
| 6 | Modal feels abrupt | No read pause before confirm | Add 1.5s pause before dismissing |
| 7 | Video file path is random | Playwright uses temp dir | Copy to stable output name in `finally` block |
| 8 | Selector failure swallowed | Empty catch block | Use helpers that log warnings — never silent catch |
| 9 | Wrong field type assumed | Skipped discovery | Always complete Phase 1 before scripting |
| 10 | Placeholder value selected | `value="0"` or "Select..." chosen | Dump options, skip placeholders |
| 11 | Popup creates separate video | New browser context for popup | Capture popup pages explicitly, merge if needed |
| 12 | Features assumed incorrectly | Scripted without seeing UI | Inspect actual page before any script changes |
