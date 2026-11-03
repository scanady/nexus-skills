// The reviewable plan: brief, script, storyboard, assets, timing, checks and estimates.
// Shared by storyboard.mjs (storyboard.html + REVIEW.md).
import fs from "node:fs";
import { config, jobPath, readJson } from "./config.mjs";
import { loadLines, spokenText } from "./lines.mjs";

const words = s => s.split(/\s+/).filter(Boolean).length;
const numbersIn = s => (s.replace(/https?:\/\/\S+/g, "").match(/\d[\d,.]*\d|\d/g) ?? []).map(n => n.replace(/,/g, ""));

// What the sketches cannot show: a hook, short on-screen text, time to read it, and numbers with a source.
// The same floors as lint.mjs: reading time is 1 s + the words at 180 wpm. Digits only: "forty" is not checked.
export function contentNotes({ lines, scenes, facts = "", userFacts = [] }) {
  const notes = [];
  if (scenes.length && !scenes[0].onScreen?.length) notes.push(`first scene "${scenes[0].name}" has no onScreen text: plan the hook as large text by 3 s`);
  for (const s of scenes) {
    const items = s.onScreen ?? [], n = items.reduce((sum, x) => sum + words(x), 0), need = 1 + n * 60 / 180, has = s.b0 - s.a0;
    for (const x of items) if (words(x) > 8) notes.push(`scene "${s.name}": "${x.slice(0, 50)}" has ${words(x)} words; aim for at most 8`);
    if (n >= 3 && has < need) notes.push(`scene "${s.name}" has ${has.toFixed(1)} s; its ${n} on-screen words need at least ${need.toFixed(1)} s`);
  }
  const known = new Set(numbersIn(`${facts} ${userFacts.join(" ")}`));
  const planned = [...lines.map(l => l.text), ...scenes.flatMap(s => s.onScreen ?? [])];
  for (const n of new Set(planned.flatMap(numbersIn))) if (!known.has(n)) notes.push(`number ${n} is in the plan but not in facts.md: add it with a source, or cut it`);
  return notes;
}

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
  if (!brief.terms?.length) notes.push("brief.json lists no terms: add the words this audience searches for");
  const said = spokenText(lines), shown = (sb.scenes ?? []).flatMap(sc => sc.onScreen ?? []).join(" ").toLowerCase();
  for (const term of brief.terms ?? []) {
    if (!said.includes(term.toLowerCase())) notes.push(`term "${term}" is not in the script`);
    if (!shown.includes(term.toLowerCase())) notes.push(`term "${term}" is in no scene's onScreen list`);
  }

  // Scenes with times
  const scenes = (sb.scenes ?? []).map((sc, n) => {
    const ls = (sc.lines ?? []).filter(i => times[i]);
    const a = ls.length ? times[ls[0]].a : 0, b = ls.length ? times[ls.at(-1)].b : a;
    return { ...sc, n: n + 1, a, b, changed: !!sc.changed || ls.some(i => measured && times[i].estimated) };
  });
  // Scene spans for the animatic: each scene runs from its first line to the next scene's first line.
  scenes.forEach((s, k) => { s.a0 = k === 0 ? 0 : s.a - 0.3; s.b0 = k === scenes.length - 1 ? end : scenes[k + 1].a - 0.3; });
  notes.push(...contentNotes({ lines, scenes, facts, userFacts: sb.userFacts }));

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
