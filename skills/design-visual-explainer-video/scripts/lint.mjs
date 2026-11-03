// Timeline lint: samples the whole video without screenshots and reports the defects viewers notice most.
// Usage: node lint.mjs [--step 0.1] [--margin 0.05] [--wpm 180]
// Checks: console errors (at() misses, unknown images/sfx, Math.random), gaps with no scene,
// on-screen text outside the safe area, overlapping text, text that leaves before it can be read,
// too many words on screen at once, SFX scheduled outside the video, a blank first frame, no hook by 3 s,
// text too small for a phone, brief.json terms that are not said or shown, and drift from storyboard.json.
// Exit code 0 = clean or warnings only; 5 = errors that must be fixed before rendering.
import "./lib/job.mjs";
import { args, config, readJson } from "./lib/config.mjs";
import { launch, openPage } from "./lib/browser.mjs";
import { loadLines, spokenText } from "./lib/lines.mjs";

const a = args();
const STEP = +(a.step ?? 0.1), MARGIN = +(a.margin ?? 0.05), WPM = +(a.wpm ?? 180);
const { width: W, height: H } = config.video;
// Floors: hook 84 px at a 1080 short side, seen by 3 s at 4.5:1. On a 360 px wide phone, text under 8 px is too small.
const HOOK_BY = 3, HOOK_PX = 84 * Math.min(W, H) / 1080, HOOK_CONTRAST = 4.5, PHONE_MIN_PX = 8, PHONE_MIN_SECS = 0.6;
const browser = await launch();
const { page, errors, meta } = await openPage(browser);
const samples = await page.evaluate(({ dur, step }) => {
  const out = [];
  for (let t = 0; t < dur; t += step) { window.__render(t); out.push({ t: +t.toFixed(3), scenes: window.__active(t), text: window.__text() }); }
  return out;
}, { dur: meta.dur, step: STEP });
const sfx = await page.evaluate(() => window.__sfx());
// First frame: mean and spread of its brightness. Hook: the largest solid text by 3 s, and its contrast.
const { frame0, hook } = await page.evaluate(({ by, floor, step }) => {
  const c = window.__canvas, copy = document.createElement("canvas");
  copy.width = c.width; copy.height = c.height;
  // Read a copy: reading the engine's canvas prints a browser warning, and lint counts console output as an error.
  const g = copy.getContext("2d", { willReadFrequently: true });
  const lum = (x, y, w, h) => {
    g.drawImage(c, 0, 0);
    const d = g.getImageData(x, y, w, h).data, out = [];
    for (let i = 0; i < d.length; i += 16) out.push(d[i] * 0.2126 + d[i + 1] * 0.7152 + d[i + 2] * 0.0722);
    return out.sort((p, q) => p - q);
  };
  window.__render(0);
  const all = lum(0, 0, c.width, c.height), mean = all.reduce((s, v) => s + v, 0) / all.length;
  const frame0 = { mean, std: Math.sqrt(all.reduce((s, v) => s + (v - mean) ** 2, 0) / all.length) };
  for (let t = 0; t <= by; t += step) {
    window.__render(t);
    const b = window.__text().filter(x => x.revealed && x.alpha >= 0.9 && x.px >= floor && x.x1 > 0 && x.y1 > 0 && x.x0 < c.width && x.y0 < c.height).sort((p, q) => q.px - p.px)[0];
    if (!b) continue;
    const x = Math.max(0, Math.floor(b.x0)), y = Math.max(0, Math.floor(b.y0));
    const box = lum(x, y, Math.max(1, Math.min(c.width, Math.ceil(b.x1)) - x), Math.max(1, Math.min(c.height, Math.ceil(b.y1)) - y));
    const linear = v => { const s = v / 255; return s <= 0.04045 ? s / 12.92 : ((s + 0.055) / 1.055) ** 2.4; };
    const lo = linear(box[Math.floor(box.length * 0.05)]), hi = linear(box[Math.floor(box.length * 0.95)]);
    return { frame0, hook: { t, str: b.str, px: b.px, contrast: (hi + 0.05) / (lo + 0.05) } };
  }
  return { frame0, hook: null };
}, { by: HOOK_BY, floor: HOOK_PX, step: STEP });
await browser.close();

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
const small = new Map(); // str → seconds on screen below the phone floor
for (const s of samples) {
  const vis = s.text.filter(b => b.alpha >= 0.5);
  for (const b of vis) {
    if (b.px * 360 / W < PHONE_MIN_PX) small.set(b.str, { secs: (small.get(b.str)?.secs ?? 0) + STEP, px: b.px, t: small.get(b.str)?.t ?? s.t });
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
if (cues.some(c => c.timing === "estimated")) warns.push("word times are estimated: run align.mjs, then timeline.mjs. If align.mjs cannot run, key beats to line starts/ends or long words, and state the limit in your report");

// 8. first frame: it is the thumbnail and the first thing a muted feed shows
if (frame0.std < 6 || frame0.mean < 8) warns.push(`first frame is flat or black (mean ${frame0.mean.toFixed(0)}, spread ${frame0.std.toFixed(0)}): draw a finished picture at t = 0`);

// 9. hook: large, solid, and on screen by 3 s, so a muted viewer gets it
if (!hook) warns.push(`no text of at least ${Math.round(HOOK_PX)} px is fully on screen by ${HOOK_BY} s: put the hook there, or state why not`);
else if (hook.contrast < HOOK_CONTRAST) warns.push(`hook "${hook.str.slice(0, 50)}" at ${hook.t.toFixed(1)}s has contrast ${hook.contrast.toFixed(1)}:1; aim for at least ${HOOK_CONTRAST}:1`);

// 10. text too small for a phone
for (const [str, x] of small) if (x.secs >= PHONE_MIN_SECS) warns.push(`${x.t.toFixed(1)}s "${str.slice(0, 50)}" is ${x.px} px: ${(x.px * 360 / W).toFixed(1)} px on a 360 px wide phone; aim for at least ${Math.ceil(PHONE_MIN_PX * W / 360)} px`);

// 11. the words this audience searches for: said and shown
const said = spokenText(loadLines().lines), shown = samples.flatMap(s => s.text.filter(b => b.revealed && b.alpha >= 0.5).map(b => b.str)).join(" ").toLowerCase();
for (const term of readJson("brief.json", {}).terms ?? []) {
  if (!said.includes(term.toLowerCase())) warns.push(`term "${term}" from brief.json is never said`);
  if (!shown.includes(term.toLowerCase())) warns.push(`term "${term}" from brief.json is never shown on screen`);
}

// 12. the approved plan: the scene names and on-screen words in storyboard.json are in the video
const plain = s => s.toLowerCase().replace(/[^\p{L}\p{N}]+/gu, " ").trim();
const shownPlain = plain(shown);
for (const sc of readJson("storyboard.json", {}).scenes ?? []) {
  if (!meta.scenes.some(s => s.name === sc.name)) warns.push(`scene "${sc.name}" from storyboard.json is not in scenes.js: use the same name, or update the storyboard and tell the user`);
  for (const item of sc.onScreen ?? []) if (!shownPlain.includes(plain(item))) warns.push(`scene "${sc.name}": "${item.slice(0, 50)}" from storyboard.json is never shown: show it, or update the storyboard and tell the user`);
}

console.log(`lint: ${meta.scenes.length} scenes, ${sfx.length} sfx, ${samples.length} samples over ${meta.dur}s`);
errs.forEach(e => console.log("ERROR " + e));
warns.forEach(w => console.log("warn  " + w));
if (!errs.length && !warns.length) console.log("clean");
process.exitCode = errs.length ? 5 : 0;
