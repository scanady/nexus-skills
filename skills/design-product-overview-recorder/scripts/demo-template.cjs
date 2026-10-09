'use strict';

// Demo recording script. Copy this file to <project>/<demo-dir>/work/demo-<flow>.cjs,
// where <demo-dir> is `demo` or the suffixed name the user chose (e.g. `demo-mobile`).
// All paths derive from the script's own location, so it runs from any working directory:
//   __dirname    = <project>/<demo-dir>/work   (working files: this script, logs, raw/)
//   OUTPUT_DIR   = <project>/<demo-dir>        (deliverables: <project>-<flow>.webm, README.md)
//   PROJECT_DIR  = <project>                   (project.json, README.md, shared/)
//
// Usage:
//   node demo-<flow>.cjs --rehearse             verify selectors, no video
//   node demo-<flow>.cjs --rehearse --publish   same, then save stills + ui-map to shared/
//   node demo-<flow>.cjs                        record <project>-<flow>.webm
//   node demo-<flow>.cjs --sync                 refresh project.json entry + README section only

const path = require('path');
const fs = require('fs');

// ---------------------------------------------------------------------------
// Configuration — customize per recording
// ---------------------------------------------------------------------------

const BASE_URL = process.env.DEMO_BASE_URL || 'http://localhost:3000';
const FLOW = 'main'; // lowercase-hyphen flow name, e.g. 'create-item'
const SKILL = 'design-product-overview-recorder';
const VIEWPORT = { width: 1280, height: 720 };

const WORK_DIR = __dirname;
const OUTPUT_DIR = path.dirname(WORK_DIR);
const PROJECT_DIR = path.dirname(OUTPUT_DIR);
const SHARED_DIR = path.join(PROJECT_DIR, 'shared');
const RAW_DIR = path.join(WORK_DIR, 'raw');
const OUTPUT_DIR_NAME = path.basename(OUTPUT_DIR);

const REHEARSAL = process.argv.includes('--rehearse');
const PUBLISH = process.argv.includes('--publish');
const SYNC = process.argv.includes('--sync');

// Field map from Phase 1, written to shared/ui-map.md by `--rehearse --publish`.
// Exact labels as observed in the browser. Keys are routes; values are lines without the "- ".
const UI_MAP = {
  // '/items/new': [
  //   'Name: text input, required',
  //   'Category: select (5 options)',
  //   'Create: button "Create"',
  // ],
};
const UI_FLOWS = [
  // 'Create an item: /items → "New Item" → fill Name, Category → "Create" → /items/<id>',
];

// ---------------------------------------------------------------------------
// Project folder helpers — project.json, README.md, shared/
// All paths written to JSON or Markdown are relative to PROJECT_DIR with forward slashes.
// JSON edits are read-modify-write: entries and keys this script does not own are kept.
// ---------------------------------------------------------------------------

function rel(file) {
  return path.relative(PROJECT_DIR, file).split(path.sep).join('/');
}

function today() {
  return new Date().toISOString().slice(0, 10);
}

function readJson(file, fallback) {
  if (!fs.existsSync(file)) return fallback;
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function writeJson(file, data) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, JSON.stringify(data, null, 2) + '\n');
}

function projectName() {
  const project = readJson(path.join(PROJECT_DIR, 'project.json'), null);
  return (project && project.name) || path.basename(PROJECT_DIR);
}

function deliverablePath() {
  return path.join(OUTPUT_DIR, `${projectName()}-${FLOW}.webm`);
}

// Subtitle styling from shared/brand.json when present; built-in look otherwise.
function subtitleStyle() {
  const brand = readJson(path.join(SHARED_DIR, 'brand.json'), {});
  const palette = brand.palette || {};
  const fonts = Array.isArray(brand.fonts) ? brand.fonts : [];
  const font = fonts.find((f) => f.role === 'body') || fonts[0];
  return {
    background: hexToRgba(palette.background, 0.85) || 'rgba(0, 0, 0, 0.75)',
    color: palette.text || 'white',
    fontFamily: font ? `"${font.family}", -apple-system, "Segoe UI", sans-serif` : '-apple-system, "Segoe UI", sans-serif',
  };
}

function hexToRgba(hex, alpha) {
  const m = /^#?([0-9a-f]{6})$/i.exec(hex || '');
  if (!m) return null;
  const n = parseInt(m[1], 16);
  return `rgba(${(n >> 16) & 255}, ${(n >> 8) & 255}, ${n & 255}, ${alpha})`;
}

// Add or update this skill's own entry in shared/assets.json. Never touches other entries.
function upsertAsset(entry) {
  const file = path.join(SHARED_DIR, 'assets.json');
  const data = readJson(file, { schema: 1, assets: [] });
  if (!Array.isArray(data.assets)) data.assets = [];
  const i = data.assets.findIndex((a) => a.file === entry.file);
  if (i >= 0 && data.assets[i].by !== SKILL) {
    throw new Error(`assets.json entry for ${entry.file} belongs to ${data.assets[i].by}`);
  }
  if (i >= 0) data.assets[i] = { ...data.assets[i], ...entry };
  else data.assets.push(entry);
  writeJson(file, data);
}

// Pick shared/screenshots/<project>-<slug>.png. Reuse the name when this skill added it;
// otherwise, if the file exists, add -2, -3, ... so another skill's file is never overwritten.
function stillPath(slug) {
  const dir = path.join(SHARED_DIR, 'screenshots');
  const assets = readJson(path.join(SHARED_DIR, 'assets.json'), { assets: [] }).assets || [];
  const base = `${projectName()}-${slug}`;
  for (let n = 1; ; n++) {
    const file = path.join(dir, n === 1 ? `${base}.png` : `${base}-${n}.png`);
    const owner = assets.find((a) => a.file === rel(file));
    if (!fs.existsSync(file) && !owner) return file;
    if (owner && owner.by === SKILL) return file;
  }
}

// Save a clean still (overlays hidden) of the current viewport to shared/screenshots/
// and record it in shared/assets.json. Runs only with --publish.
async function captureStill(page, slug, note) {
  if (!PUBLISH) return null;
  const file = stillPath(slug);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  const toggle = (show) => page.evaluate((s) => {
    for (const id of ['demo-cursor', 'demo-subtitle']) {
      const el = document.getElementById(id);
      if (el) el.style.visibility = s ? 'visible' : 'hidden';
    }
  }, show);
  await toggle(false);
  await page.screenshot({ path: file });
  await toggle(true);
  const size = page.viewportSize() || VIEWPORT;
  upsertAsset({
    file: rel(file),
    kind: 'screenshot',
    by: SKILL,
    source: page.url(),
    width: size.width,
    height: size.height,
    text: true,
    background: 'opaque',
    rights: 'user-product',
    note,
  });
  console.log(`Still saved: ${rel(file)}`);
  return file;
}

// Add routes and flows to shared/ui-map.md. Existing routes and flows are never rewritten.
// Returns the lines of `routes` that differ from an existing route's section, so they can
// be reported to the user as possible UI changes.
function addToUiMap(routes, flows) {
  const file = path.join(SHARED_DIR, 'ui-map.md');
  const text = fs.existsSync(file) ? fs.readFileSync(file, 'utf8') : '';
  const sections = [];
  let current = null;
  const preamble = [];
  for (const line of text.split('\n')) {
    const m = /^## (.+?)\s*$/.exec(line);
    if (m) { current = { heading: m[1], lines: [] }; sections.push(current); }
    else if (current) current.lines.push(line);
    else preamble.push(line);
  }
  const discrepancies = [];
  let flowsSection = sections.find((s) => s.heading === 'Flows');
  const routeSections = sections.filter((s) => s !== flowsSection);
  for (const [route, items] of Object.entries(routes)) {
    const existing = routeSections.find((s) => s.heading === route);
    if (existing) {
      for (const item of items) {
        if (!existing.lines.includes(`- ${item}`)) discrepancies.push(`${route}: ${item}`);
      }
      continue;
    }
    routeSections.push({ heading: route, lines: items.map((i) => `- ${i}`).concat('') });
  }
  if (flows.length) {
    if (!flowsSection) flowsSection = { heading: 'Flows', lines: [] };
    const names = flowsSection.lines.map((l) => l.replace(/^- /, '').split(':')[0].trim());
    const added = flows.filter((f) => !names.includes(f.split(':')[0].trim())).map((f) => `- ${f}`);
    const last = flowsSection.lines.map((l) => l.trim() !== '').lastIndexOf(true);
    flowsSection.lines.splice(last + 1, 0, ...added);
  }
  const out = preamble.join('\n').trim() ? [preamble.join('\n').trimEnd(), ''] : [];
  for (const s of routeSections.concat(flowsSection ? [flowsSection] : [])) {
    const body = s.lines.join('\n').trimEnd();
    out.push(`## ${s.heading}`, ...(body ? [body] : []), '');
  }
  fs.mkdirSync(SHARED_DIR, { recursive: true });
  fs.writeFileSync(file, out.join('\n').trimEnd() + '\n');
  for (const d of discrepancies) console.warn(`UI-MAP DIFFERS (not changed): ${d}`);
  return discrepancies;
}

// Update this output's entry in project.json (keyed by dir) and its README.md section.
// Skips quietly when project.json is missing (script used outside a project folder).
// Without `status`, the current status is kept.
function updateProject({ status } = {}) {
  const manifest = path.join(PROJECT_DIR, 'project.json');
  const project = readJson(manifest, null);
  if (!project) {
    console.warn('No project.json next to this output folder; manifest and README not updated.');
    return;
  }
  if (!Array.isArray(project.outputs)) project.outputs = [];
  let out = project.outputs.find((o) => o.dir === OUTPUT_DIR_NAME);
  if (!out) {
    out = { dir: OUTPUT_DIR_NAME, skill: SKILL, kind: 'demo-recording', entry: null };
    project.outputs.push(out);
  }
  const video = rel(deliverablePath());
  const entryMissing = !out.entry || !fs.existsSync(path.join(PROJECT_DIR, out.entry));
  if (entryMissing && fs.existsSync(deliverablePath())) out.entry = video;
  out.status = status || out.status || 'in-progress';
  out.updated = today();
  writeJson(manifest, project);

  const videos = fs.readdirSync(OUTPUT_DIR).filter((f) => f.endsWith('.webm')).sort();
  const lines = videos.map((f) => `- \`${OUTPUT_DIR_NAME}/${f}\``);
  if (fs.existsSync(path.join(OUTPUT_DIR, 'README.md'))) lines.push(`\nDetails: \`${OUTPUT_DIR_NAME}/README.md\`.`);
  writeReadmeSection(`## Demo recording\n${lines.join('\n')}`);
}

function writeReadmeSection(body) {
  const file = path.join(PROJECT_DIR, 'README.md');
  const open = `<!-- output:${OUTPUT_DIR_NAME} -->`;
  const close = `<!-- /output:${OUTPUT_DIR_NAME} -->`;
  const block = `${open}\n${body}\n${close}`;
  const text = fs.existsSync(file) ? fs.readFileSync(file, 'utf8') : '';
  const start = text.indexOf(open);
  const end = text.indexOf(close);
  const next = start >= 0 && end > start
    ? text.slice(0, start) + block + text.slice(end + close.length)
    : `${text.trimEnd()}${text.trim() ? '\n\n' : ''}${block}\n`;
  fs.writeFileSync(file, next);
}

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

async function injectSubtitleBar(page, style = subtitleStyle()) {
  await page.evaluate((s) => {
    if (document.getElementById('demo-subtitle')) return;
    const bar = document.createElement('div');
    bar.id = 'demo-subtitle';
    bar.style.cssText = `
      position: fixed; bottom: 0; left: 0; right: 0; z-index: 999998;
      text-align: center; padding: 12px 24px;
      background: ${s.background};
      color: ${s.color}; font-family: ${s.fontFamily};
      font-size: 16px; font-weight: 500; letter-spacing: 0.3px;
      transition: opacity 0.3s; pointer-events: none;
    `;
    bar.textContent = '';
    bar.style.opacity = '0';
    document.body.appendChild(bar);
  }, style);
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

async function main() {
  if (SYNC) {
    updateProject();
    return;
  }
  const { chromium } = require('playwright');
  const browser = await chromium.launch({ headless: true });

  // --- Rehearsal mode ---
  if (REHEARSAL) {
    const ctx = await browser.newContext({ viewport: VIEWPORT });
    const page = await ctx.newPage();
    let allOk = true;

    // Add rehearsal selectors here, one page at a time:
    // await page.goto(`${BASE_URL}/login`);
    // allOk = (await ensureVisible(page, '#email', 'Login email')) && allOk;
    // allOk = (await ensureVisible(page, 'button[type="submit"]', 'Login submit')) && allOk;
    // await captureStill(page, 'login', 'Login page, empty form');

    await browser.close();
    if (!allOk) {
      console.error('REHEARSAL FAILED');
      process.exitCode = 1;
      return;
    }
    console.log('REHEARSAL PASSED');
    if (PUBLISH) addToUiMap(UI_MAP, UI_FLOWS);
    return;
  }

  // --- Recording mode ---
  fs.mkdirSync(RAW_DIR, { recursive: true });
  updateProject({ status: 'in-progress' });
  const ctx = await browser.newContext({
    recordVideo: { dir: RAW_DIR, size: VIEWPORT },
    viewport: VIEWPORT,
  });
  const page = await ctx.newPage();
  let ok = true;

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
    ok = false;
    console.error('DEMO ERROR:', err.message);
  } finally {
    await ctx.close();
    const video = page.video();
    if (video) {
      // Playwright names raw files randomly; keep one raw file per flow in work/raw/.
      const raw = path.join(RAW_DIR, `${FLOW}.webm`);
      const dest = deliverablePath();
      try {
        fs.renameSync(await video.path(), raw);
        fs.copyFileSync(raw, dest);
        console.log(`Video saved: ${dest}`);
      } catch (e) {
        ok = false;
        console.error(`Failed to copy video: ${e.message}`);
        console.error(`  Dest: ${dest}`);
      }
    }
    await browser.close();
    updateProject({ status: ok ? 'delivered' : 'in-progress' });
    if (!ok) process.exitCode = 1;
  }
}

if (require.main === module) {
  main().catch((err) => {
    console.error(err);
    process.exitCode = 1;
  });
}

module.exports = { addToUiMap, upsertAsset, stillPath, captureStill, updateProject, writeReadmeSection, subtitleStyle };
