# Playwright Demo Helpers

Reusable functions for demo video recording. Paste into recording scripts or import from shared module.

---

## Cursor Overlay

SVG arrow cursor. Follows mouse. Destroyed on navigation — must re-inject after every `page.goto()`.

```javascript
async function injectCursor(page) {
  await page.evaluate(() => {
    if (document.getElementById('demo-cursor')) return;
    const cursor = document.createElement('div');
    cursor.id = 'demo-cursor';
    cursor.innerHTML = `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M5 3L19 12L12 13L9 20L5 3Z" fill="white" stroke="black" stroke-width="1.5" stroke-linejoin="round"/>
    </svg>`;
    cursor.style.cssText = `
      position: fixed; z-index: 999999; pointer-events: none;
      width: 24px; height: 24px;
      transition: left 0.1s, top 0.1s;
      filter: drop-shadow(1px 1px 2px rgba(0,0,0,0.3));
    `;
    cursor.style.left = '0px';
    cursor.style.top = '0px';
    document.body.appendChild(cursor);
    document.addEventListener('mousemove', (e) => {
      cursor.style.left = e.clientX + 'px';
      cursor.style.top = e.clientY + 'px';
    });
  });
}
```

---

## Subtitle Bar

Fixed bar at viewport bottom. Shows step narration over semi-transparent background.

```javascript
async function injectSubtitleBar(page) {
  await page.evaluate(() => {
    if (document.getElementById('demo-subtitle')) return;
    const bar = document.createElement('div');
    bar.id = 'demo-subtitle';
    bar.style.cssText = `
      position: fixed; bottom: 0; left: 0; right: 0; z-index: 999998;
      text-align: center; padding: 12px 24px;
      background: rgba(0, 0, 0, 0.75);
      color: white; font-family: -apple-system, "Segoe UI", sans-serif;
      font-size: 16px; font-weight: 500; letter-spacing: 0.3px;
      transition: opacity 0.3s; pointer-events: none;
    `;
    bar.textContent = '';
    bar.style.opacity = '0';
    document.body.appendChild(bar);
  });
}

async function showSubtitle(page, text) {
  await page.evaluate((t) => {
    const bar = document.getElementById('demo-subtitle');
    if (!bar) return;
    if (t) { bar.textContent = t; bar.style.opacity = '1'; }
    else { bar.style.opacity = '0'; }
  }, text);
  if (text) await page.waitForTimeout(800);
}
```

Usage:
- `showSubtitle(page, 'Step 1 — Logging in')` — display
- `showSubtitle(page, '')` — hide
- Keep text under 60 chars
- "Step N — Action" format for consistency
- Clear during long pauses where UI speaks for itself

Inject alongside cursor after every navigation.

---

## Overlay Composition

Convenience wrapper — injects both cursor and subtitle bar in one call.

```javascript
async function injectOverlays(page) {
  await injectCursor(page);
  await injectSubtitleBar(page);
}
```

Call after every `page.goto()` or navigation event.

---

## Move and Click

Moves cursor visibly to target element, then clicks. Never teleports.

```javascript
async function moveAndClick(page, locator, label, opts = {}) {
  const { postClickDelay = 800, ...clickOpts } = opts;
  const el = typeof locator === 'string' ? page.locator(locator).first() : locator;
  const visible = await el.isVisible().catch(() => false);
  if (!visible) {
    console.error(`WARNING: moveAndClick skipped — "${label}" not visible`);
    return false;
  }
  try {
    await el.scrollIntoViewIfNeeded();
    await page.waitForTimeout(300);
    const box = await el.boundingBox();
    if (box) {
      await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2, { steps: 10 });
      await page.waitForTimeout(400);
    }
    await el.click(clickOpts);
  } catch (e) {
    console.error(`WARNING: moveAndClick failed on "${label}": ${e.message}`);
    return false;
  }
  await page.waitForTimeout(postClickDelay);
  return true;
}
```

Every call needs descriptive `label` for debugging. Returns `false` on miss — never silently swallows errors.

---

## Type Slowly

Visible per-character typing with delay. Moves cursor to field first via `moveAndClick`.

```javascript
async function typeSlowly(page, locator, text, label, charDelay = 35) {
  const el = typeof locator === 'string' ? page.locator(locator).first() : locator;
  const visible = await el.isVisible().catch(() => false);
  if (!visible) {
    console.error(`WARNING: typeSlowly skipped — "${label}" not visible`);
    return false;
  }
  await moveAndClick(page, el, label);
  await el.fill('');
  await el.pressSequentially(text, { delay: charDelay });
  await page.waitForTimeout(500);
  return true;
}
```

Uses `pressSequentially` so viewer sees each keystroke appear. Never use bare `fill()` for visible typing.

---

## Ensure Visible (Rehearsal)

Verification wrapper for Phase 2. Logs all visible interactive elements when selector fails — essential for fast debugging.

```javascript
async function ensureVisible(page, locator, label) {
  const el = typeof locator === 'string' ? page.locator(locator).first() : locator;
  const visible = await el.isVisible().catch(() => false);
  if (!visible) {
    console.error(`REHEARSAL FAIL: "${label}" — selector: ${typeof locator === 'string' ? locator : '(locator)'}`);
    const found = await page.evaluate(() => {
      return Array.from(document.querySelectorAll('button, input, select, textarea, a'))
        .filter(el => el.offsetParent !== null)
        .map(el => `${el.tagName}[${el.type || ''}] "${el.textContent?.trim().substring(0, 30)}"`)
        .join('\n  ');
    });
    console.error('  Visible elements:\n  ' + found);
    return false;
  }
  console.log(`REHEARSAL OK: "${label}"`);
  return true;
}
```

On failure: dumps all visible interactive elements so correct selector can be found immediately without manual inspection.

---

## Pan Elements

Move cursor across key elements on dashboard or overview pages. Draws viewer attention to layout and data.

```javascript
async function panElements(page, selector, maxCount = 6) {
  const elements = await page.locator(selector).all();
  for (let i = 0; i < Math.min(elements.length, maxCount); i++) {
    try {
      const box = await elements[i].boundingBox();
      if (box && box.y < 700) {
        await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2, { steps: 8 });
        await page.waitForTimeout(600);
      }
    } catch (e) {
      console.warn(`WARNING: panElements skipped element ${i}: ${e.message}`);
    }
  }
}
```

Use on dashboards, card grids, data tables. Limit `maxCount` to avoid tedious panning.

---

## Smooth Scroll

Scroll viewport smoothly. Never instant jumps — viewer needs time to track content movement.

```javascript
await page.evaluate((y) => window.scrollTo({ top: y, behavior: 'smooth' }), 400);
await page.waitForTimeout(1500);
```

Wait 1.5s after scroll for viewer to orient to new content position.
