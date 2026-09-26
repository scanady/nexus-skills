// The reviewable plan: brief, script, storyboard, assets, timing, checks and estimates.
// Shared by storyboard.mjs (storyboard.html + REVIEW.md).
import fs from "node:fs";
import { config, jobPath, readJson } from "./config.mjs";
import { loadLines } from "./lines.mjs";

const words = s => s.split(/\s+/).filter(Boolean).length;

export function loadPlan() {
  const brief = readJson("brief.json", {});
  const { voice, lines } = loadLines();
  const sb = readJson("storyboard.json");
  const assets = readJson("assets.json", { images: [] });
  const music = readJson("music.json", null);
  const cues = readJson("cues.json", null);
  const manifest = readJson("assets/manifest.json", {});
  const facts = fs.existsSync(jobPath("facts.md")) ? fs.readFileSync(jobPath("facts.md"), "utf8") : "";
  const extra = fs.existsSync(jobPath("assets/extra")) ? fs.readdirSync(jobPath("assets/extra")).map(f => f.replace(/\.[^.]+$/, "")) : [];

  // Timing: measured length for lines already voiced (matched by text), 150 wpm estimate for new ones.
  const voiced = new Map((Array.isArray(cues) ? cues : []).filter(c => c.timing !== "silent").map(c => [c.text, c]));
  const times = [];
  let measured = 0;
  { let t = 0.8; for (const [i, l] of lines.entries()) {
    const c = voiced.get(l.text);
    const dur = c ? c.dur : words(l.text) / 2.5 + 0.3;
    if (c) measured++;
    times.push({ i, a: t, b: t + dur, dur, estimated: !c, cue: c?.i, pauseAfter: l.pauseAfter ?? 0.55 });
    t += dur + (l.pauseAfter ?? 0.55);
  } }
  const end = times.at(-1).b + 2.5;
  const totalWords = lines.reduce((s, l) => s + words(l.text), 0);
  const wpm = totalWords / ((times.at(-1).b - times[0].a) / 60);

  // Checks
  const errors = [], notes = [];
  const seen = new Map();
  let last = -1;
  const assetStatus = id => (manifest[id] ? "made" : extra.includes(id) ? "supplied" : (assets.images ?? []).some(x => x.id === id) ? "new" : "missing");
  for (const sc of sb.scenes ?? []) {
    for (const i of sc.lines ?? []) {
      if (i < 0 || i >= lines.length) errors.push(`scene "${sc.name}" lists line ${i}, but the script has lines 0–${lines.length - 1}`);
      if (seen.has(i)) errors.push(`line ${i} is in two scenes ("${seen.get(i)}" and "${sc.name}")`);
      if (i < last) errors.push(`scene "${sc.name}" is out of order (line ${i} after line ${last})`);
      seen.set(i, sc.name); last = Math.max(last, i);
    }
    const ids = new Set([...(sc.assets ?? []), ...(sc.frame?.image ? [sc.frame.image] : [])]);
    for (const id of ids) if (assetStatus(id) === "missing") errors.push(`scene "${sc.name}" uses image "${id}", which is not in assets.json or assets/extra/`);
    if (!sc.frame) notes.push(`scene "${sc.name}" has no frame spec, so its storyboard panel is a text card`);
  }
  for (let i = 0; i < lines.length; i++) if (!seen.has(i)) errors.push(`line ${i} is in no scene: "${lines[i].text.slice(0, 60)}"`);
  const target = brief.lengthSec;
  if (target && Math.abs(end - target) / target > 0.15) notes.push(`estimated length ${fmt(end)} is more than 15% off the ${fmt(target)} target`);
  if (wpm > 170) notes.push(`pace ${Math.round(wpm)} wpm is fast; aim for 140–160`);

  // Scenes with times
  const scenes = (sb.scenes ?? []).map((sc, n) => {
    const ls = (sc.lines ?? []).filter(i => times[i]);
    const a = ls.length ? times[ls[0]].a : 0, b = ls.length ? times[ls.at(-1)].b : a;
    return { ...sc, n: n + 1, a, b, changed: !!sc.changed || ls.some(i => measured && times[i].estimated) };
  });
  // Scene spans for the animatic: each scene runs from its first line to the next scene's first line.
  scenes.forEach((s, k) => { s.a0 = k === 0 ? 0 : s.a - 0.3; s.b0 = k === scenes.length - 1 ? end : scenes[k + 1].a - 0.3; });

  // Estimates
  const toMake = (assets.images ?? []).filter(x => !manifest[x.id]);
  const cost = { image: toMake.length * 0.07, tts: (lines.length - measured) * 0.005, music: config.music.provider === "openrouter" ? 0.08 : 0 };
  const sources = [...new Set((facts.match(/https?:\/\/\S+/g) ?? []).map(u => u.replace(/[).,]+$/, "")))];
  const factCount = (facts.match(/^\s*-\s/gm) ?? []).length;

  return {
    brief, voice, lines, sb, assets, music, manifest, extra, times, measured, allMeasured: measured === lines.length,
    end, totalWords, wpm, errors, notes, scenes, toMake, cost, costTotal: cost.image + cost.tts + cost.music,
    sources, factCount, assetStatus,
  };
}

export const fmt = s => `${Math.floor(s / 60)}:${(s % 60).toFixed(0).padStart(2, "0")}`;
