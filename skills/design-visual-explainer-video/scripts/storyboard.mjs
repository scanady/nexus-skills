// Review gate: build storyboard.html (filmstrip + animatic + feedback) and REVIEW.md (text record)
// from brief.json, lines.json, storyboard.json, assets.json. Run it BEFORE any paid generation.
// Usage: node storyboard.mjs [--sketch-all] [--no-audio]
//   Key frames: scenes unchanged since the last build reuse a frame from out.html; new or changed
//   scenes are drawn from their `frame` spec with assets/layouts.js (--sketch-all forces sketches).
//   Animatic audio: lines already voiced play their real clip; new lines use the browser's speech voice.
// Exit 0 = written; 7 = the plan has errors (also shown at the top of the page).
import fs from "node:fs";
import path from "node:path";
import { args, config, ASSETS_DIR, ff, jobPath } from "./lib/config.mjs";
import { loadPlan, fmt } from "./lib/plan.mjs";
import { assemblePage, fontFaces, loadImages, safeJson, esc } from "./lib/page.mjs";
import { reviewMarkdown } from "./lib/review-md.mjs";
import { launch, openPage } from "./lib/browser.mjs";

const a = args();
const P = loadPlan();
const { css, families } = fontFaces();
const THUMB_W = 960;

// ---------- key frames ----------
const frames = new Array(P.scenes.length).fill(null), kinds = new Array(P.scenes.length).fill("text");
const browser = await launch();
const grab = async (page, t) => page.evaluate(({ t, w }) => {
  window.__render(t);
  const src = window.__canvas, c = document.createElement("canvas");
  c.width = w; c.height = Math.round(w * src.height / src.width);
  c.getContext("2d").drawImage(src, 0, 0, c.width, c.height);
  return c.toDataURL("image/jpeg", 0.86);
}, { t, w: THUMB_W });

// 1) reuse frames from the last build for unchanged scenes
if (!a["sketch-all"] && fs.existsSync(jobPath("out.html"))) {
  const { page, meta } = await openPage(browser, { file: "out.html" });
  const old = new Map(meta.scenes.map(s => [s.name, s]));
  for (const [k, s] of P.scenes.entries()) {
    const o = old.get(s.name);
    if (!o || s.changed) continue;
    const len = o.end - o.start;
    frames[k] = await grab(page, Math.max(o.start + 0.3, Math.min(o.start + len * 0.85, o.end - 0.5)));
    kinds[k] = "render";
  }
  await page.close();
}
// 2) sketch frames for the rest
const todo = P.scenes.map((s, k) => (!frames[k] && s.frame ? k : -1)).filter(k => k >= 0);
if (todo.length) {
  const used = new Set(todo.map(k => P.scenes[k].frame.image).filter(Boolean));
  const prompts = Object.fromEntries((P.assets.images ?? []).map(x => [x.id, x.prompt]));
  const SB = { theme: P.sb.design?.theme ?? {}, frames: P.scenes.map((s, k) => (todo.includes(k) ? s.frame : null)), prompts };
  const { width, height, fps } = config.video;
  const data = { title: "storyboard", width, height, fps, dur: P.scenes.length, seed: "storyboard", cues: [], images: loadImages(used), audio: null, fontFamilies: families };
  const scenesJs = `const SB = ${safeJson(SB)};\n` + fs.readFileSync(path.join(ASSETS_DIR, "layouts.js"), "utf8");
  fs.writeFileSync(jobPath("storyboard-frames.html"), assemblePage({ data, scenesJs, faces: css }));
  const { page, errors } = await openPage(browser, { file: "storyboard-frames.html" });
  for (const k of todo) { frames[k] = await grab(page, k + 0.5); kinds[k] = "sketch"; }
  for (const e of new Set(errors)) console.log("frame console: " + e);
  await page.close();
  fs.rmSync(jobPath("storyboard-frames.html"));
}
await browser.close();

// ---------- per-line audio for the animatic ----------
fs.mkdirSync(jobPath("storyboard-audio"), { recursive: true });
const lineAudio = P.times.map(t => {
  if (a["no-audio"] || t.estimated || t.cue === undefined) return null;
  const src = jobPath(`vo/line${t.cue}.wav`);
  if (!fs.existsSync(src)) return null;
  const mp3 = jobPath(`storyboard-audio/l${t.cue}.mp3`);
  if (!fs.existsSync(mp3) || fs.statSync(mp3).mtimeMs < fs.statSync(src).mtimeMs) ff(["-y", "-i", src, "-ac", "1", "-b:a", "48k", mp3]);
  return "data:audio/mpeg;base64," + fs.readFileSync(mp3).toString("base64");
});

// ---------- page ----------
const d = P.sb.design ?? {};
const payload = {
  title: P.brief.title || "Explainer video",
  generated: new Date().toLocaleString("sv-SE").slice(0, 16),
  brief: { goal: P.brief.goal, audience: P.brief.audience, cta: P.brief.cta, language: P.brief.language ?? config.language, target: P.brief.lengthSec },
  stats: { end: P.end, words: P.totalWords, wpm: Math.round(P.wpm), lines: P.lines.length, measured: P.measured },
  design: { ...d, imageStyle: d.imageStyle ?? P.assets.style ?? "", voice: d.voice ?? `${P.voice.voice ?? config.tts.voice}: ${P.voice.style ?? ""}`, music: d.music ?? P.music?.prompt ?? config.music.provider, families },
  scenes: P.scenes.map((s, k) => ({
    n: s.n, name: s.name, title: s.title ?? s.name, chapter: s.chapter ?? "", a: s.a0, b: s.b0, changed: s.changed,
    frame: frames[k], frameKind: kinds[k],
    lines: (s.lines ?? []).map(i => ({ i, text: P.lines[i]?.text ?? "", changed: P.measured > 0 && P.times[i]?.estimated, audio: lineAudio[i], dur: P.times[i]?.dur, pauseAfter: P.times[i]?.pauseAfter, at: P.times[i]?.a })),
    onScreen: s.onScreen ?? [], motion: s.motion ?? "", notes: s.notes ?? "", visual: s.visual ?? "",
    assets: [...new Set([...(s.assets ?? []), ...(s.frame?.image ? [s.frame.image] : [])])].map(id => ({ id, status: P.assetStatus(id) })),
  })),
  changes: P.sb.changes ?? [], questions: P.sb.questions ?? [], userFacts: P.sb.userFacts ?? [],
  images: P.toMake.map(x => ({ id: x.id, prompt: x.prompt, background: x.background ?? "scene" })),
  sources: P.sources, factCount: P.factCount, cost: P.cost, costTotal: P.costTotal, budget: config.budgetUsd,
  errors: P.errors, notes: P.notes,
};
let html = fs.readFileSync(path.join(ASSETS_DIR, "storyboard.html"), "utf8");
html = html.split("{{TITLE}}").join(esc(payload.title));
html = html.replace("/*{{FONT_FACES}}*/", () => css);
html = html.replace("/*{{SB}}*/", () => safeJson(payload));
fs.writeFileSync(jobPath("storyboard.html"), html);
fs.writeFileSync(jobPath("REVIEW.md"), reviewMarkdown(P));

const counts = kinds.reduce((m, k) => ((m[k] = (m[k] ?? 0) + 1), m), {});
console.log(`storyboard.html ${(Buffer.byteLength(html) / 1048576).toFixed(1)} MB: ${P.scenes.length} scenes (${Object.entries(counts).map(([k, v]) => `${v} ${k}`).join(", ")}), ${fmt(P.end)}, ${P.lines.length} lines (${lineAudio.filter(Boolean).length} with real voice), build cost about $${P.costTotal.toFixed(2)}`);
console.log("REVIEW.md: text record of the same plan");
P.errors.forEach(e => console.log("ERROR " + e));
P.notes.forEach(n => console.log("note  " + n));
process.exitCode = P.errors.length ? 7 : 0;
