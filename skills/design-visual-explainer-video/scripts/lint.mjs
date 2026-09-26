// Timeline lint: samples the whole video without screenshots and reports the defects viewers notice most.
// Usage: node lint.mjs [--step 0.1] [--margin 0.05] [--wpm 180]
// Checks: console errors (at() misses, unknown images/sfx, Math.random), gaps with no scene,
// on-screen text outside the safe area, overlapping text, text that leaves before it can be read,
// too many words on screen at once, and SFX scheduled outside the video.
// Exit code 0 = clean or warnings only; 5 = errors that must be fixed before rendering.
import { args, config, readJson } from "./lib/config.mjs";
import { launch, openPage } from "./lib/browser.mjs";

const a = args();
const STEP = +(a.step ?? 0.1), MARGIN = +(a.margin ?? 0.05), WPM = +(a.wpm ?? 180);
const browser = await launch();
const { page, errors, meta } = await openPage(browser);
const samples = await page.evaluate(({ dur, step }) => {
  const out = [];
  for (let t = 0; t < dur; t += step) { window.__render(t); out.push({ t: +t.toFixed(3), scenes: window.__active(t), text: window.__text() }); }
  return out;
}, { dur: meta.dur, step: STEP });
const sfx = await page.evaluate(() => window.__sfx());
await browser.close();

const { width: W, height: H } = config.video;
const errs = [], warns = [];
const once = new Set();
const warnOnce = (key, msg) => { if (!once.has(key)) { once.add(key); warns.push(msg); } };

// 1. console errors
for (const e of new Set(errors)) errs.push(`console: ${e}`);

// 2. gaps with no scene (black frames), outside the fade-in/out
let gapStart = null;
for (const s of samples) {
  const empty = s.scenes.length === 0 && s.t > 0.2 && s.t < meta.dur - 0.3;
  if (empty && gapStart === null) gapStart = s.t;
  if (!empty && gapStart !== null) { errs.push(`no scene from ${gapStart.toFixed(2)}s to ${s.t.toFixed(2)}s (black frames)`); gapStart = null; }
}
if (gapStart !== null) errs.push(`no scene from ${gapStart.toFixed(2)}s to the end`);

// 3–5. per-frame text checks, and visibility spans per string
const spans = new Map(); // str → [{a, b}]
for (const s of samples) {
  const vis = s.text.filter(b => b.alpha >= 0.5);
  for (const b of vis) {
    const mx = W * MARGIN, my = H * MARGIN;
    if (b.x0 < mx - 2 || b.y0 < my - 2 || b.x1 > W - mx + 2 || b.y1 > H - my + 2) {
      const off = b.x1 < 0 || b.x0 > W || b.y1 < 0 || b.y0 > H;
      if (!off) warnOnce(`safe:${b.str}`, `${s.t.toFixed(1)}s text outside the ${Math.round(MARGIN * 100)}% safe area: "${b.str.slice(0, 50)}"`);
    }
    if (b.revealed) {
      const list = spans.get(b.str) ?? [];
      const last = list.at(-1);
      if (last && s.t - last.b <= STEP * 1.5) last.b = s.t; else list.push({ a: s.t, b: s.t });
      spans.set(b.str, list);
    }
  }
  for (let i = 0; i < vis.length; i++) for (let j = i + 1; j < vis.length; j++) {
    const p = vis[i], q = vis[j];
    const ix = Math.min(p.x1, q.x1) - Math.max(p.x0, q.x0), iy = Math.min(p.y1, q.y1) - Math.max(p.y0, q.y0);
    if (ix > 0 && iy > 0) {
      const small = Math.min((p.x1 - p.x0) * (p.y1 - p.y0), (q.x1 - q.x0) * (q.y1 - q.y0));
      if (ix * iy > small * 0.12 && p.str !== q.str) warnOnce(`ov:${p.str}|${q.str}`, `${s.t.toFixed(1)}s overlapping text: "${p.str.slice(0, 40)}" × "${q.str.slice(0, 40)}"`);
    }
  }
  const words = vis.reduce((n, b) => n + b.str.split(/\s+/).filter(Boolean).length, 0);
  if (words > 24) warnOnce(`dense:${Math.floor(s.t)}`, `${s.t.toFixed(1)}s ${words} words on screen at once (aim for ≤ 12; the voice carries the detail)`);
}
for (const [str, list] of spans) {
  const n = str.split(/\s+/).filter(Boolean).length;
  if (n < 3) continue;
  const need = 1 + n * 60 / WPM, longest = Math.max(...list.map(x => x.b - x.a + STEP));
  if (longest < need) warns.push(`"${str.slice(0, 50)}" is readable for ${longest.toFixed(1)}s; ${n} words need ≥ ${need.toFixed(1)}s`);
}

// 6. sfx outside the video
for (const e of sfx) if (e.t < 0 || e.t > meta.dur) warnOnce(`sfx:${e.t}`, `sfx "${e.kind}" at ${e.t.toFixed(2)}s is outside 0–${meta.dur}s`);

// 7. estimated word timings: remind that sync is approximate
const cues = readJson("cues.json", []);
if (cues.some(c => c.timing === "estimated")) warns.push("word times are estimated (TTS gave no timestamps): key beats to words at line starts/ends or long words, and check sync by ear in out.html");

console.log(`lint: ${meta.scenes.length} scenes, ${sfx.length} sfx, ${samples.length} samples over ${meta.dur}s`);
errs.forEach(e => console.log("ERROR " + e));
warns.forEach(w => console.log("warn  " + w));
if (!errs.length && !warns.length) console.log("clean");
process.exitCode = errs.length ? 5 : 0;
