'use strict';

const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

// ---------------------------------------------------------------------------
// Configuration — customize per recording
// ---------------------------------------------------------------------------

const BASE_URL = process.env.DEMO_BASE_URL || 'http://localhost:3000';
const VIDEO_DIR = path.join(process.cwd(), 'output', 'demo');
const OUTPUT_NAME = 'demo.webm';
const REHEARSAL = process.argv.includes('--rehearse');

// ---------------------------------------------------------------------------
// Helpers — cursor overlay, subtitle bar, interaction utilities
// See references/playwright-helpers.md for full documentation
// ---------------------------------------------------------------------------

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

async function injectOverlays(page) {
  await injectCursor(page);
  await injectSubtitleBar(page);
}

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

// ---------------------------------------------------------------------------
// Recording Script — customize the sections below
// ---------------------------------------------------------------------------

(async () => {
  fs.mkdirSync(VIDEO_DIR, { recursive: true });
  const browser = await chromium.launch({ headless: true });

  // --- Rehearsal mode ---
  if (REHEARSAL) {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 720 } });
    const page = await ctx.newPage();

    // Add rehearsal selectors here:
    // await page.goto(`${BASE_URL}/login`);
    // await ensureVisible(page, '#email', 'Login email');
    // await ensureVisible(page, 'button[type="submit"]', 'Login submit');

    console.log('Add selectors above, then run: node demo-template.cjs --rehearse');
    await browser.close();
    return;
  }

  // --- Recording mode ---
  const ctx = await browser.newContext({
    recordVideo: { dir: VIDEO_DIR, size: { width: 1280, height: 720 } },
    viewport: { width: 1280, height: 720 },
  });
  const page = await ctx.newPage();

  try {
    // Step 1 — Entry
    await page.goto(`${BASE_URL}/`);
    await page.waitForLoadState('networkidle');
    await injectOverlays(page);
    await showSubtitle(page, 'Step 1 — Getting started');
    await page.waitForTimeout(4000);

    // Add recording steps here:
    // await moveAndClick(page, '#login-btn', 'Login button');
    // await typeSlowly(page, '#email', 'demo@example.com', 'Email field');

    // Final pause
    await showSubtitle(page, '');
    await page.waitForTimeout(3000);
  } catch (err) {
    console.error('DEMO ERROR:', err.message);
  } finally {
    await ctx.close();
    const video = page.video();
    if (video) {
      const src = await video.path();
      const dest = path.join(VIDEO_DIR, OUTPUT_NAME);
      try {
        fs.copyFileSync(src, dest);
        console.log(`Video saved: ${dest}`);
      } catch (e) {
        console.error(`Failed to copy video: ${e.message}`);
        console.error(`  Source: ${src}`);
        console.error(`  Dest: ${dest}`);
      }
    }
    await browser.close();
  }
})();
