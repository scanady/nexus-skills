// Generate the image assets listed in assets.json through OpenRouter's Image API.
// Usage: node images.mjs [--only id1,id2] [--force] [--model slug]
// assets.json:
// { "style": "shared art direction appended to every prompt",
//   "images": [ { "id": "robot", "prompt": "...", "aspect": "1:1", "background": "green" | "transparent" | "scene",
//                 "ref": ["robot"], "seed": 7 } ] }
//  - background "green": the model paints on flat #00FF00, then ffmpeg keys it out → PNG with alpha (cut-out sprites).
//  - background "transparent": asks the provider for real alpha (not every provider supports it).
//  - background "scene": full-frame image, no keying.
//  - ref: ids of already-generated images sent as input references to keep a character or style consistent.
// Out: assets/<id>.png, assets/manifest.json. Existing files are kept unless --force or the prompt changed.
import fs from "node:fs";
import { args, config, ff, hash, jobPath, readJson, writeJson, pool, spent, die, isStop } from "./lib/config.mjs";
import { generateImage } from "./lib/openrouter.mjs";

const a = args();
const doc = readJson("assets.json");
const only = a.only ? new Set(String(a.only).split(",")) : null;
const model = a.model ?? config.image.model;
fs.mkdirSync(jobPath("assets/raw"), { recursive: true });
const manifestPath = "assets/manifest.json";
const manifest = readJson(manifestPath, {});

const GREEN = " Isolated on a perfectly flat, uniform pure chroma-key green background (#00FF00) that fills the whole frame edge to edge. No shadow, gradient, floor or texture on the background, and no green anywhere in the subject.";
const TRANSPARENT = " Isolated subject on a transparent background.";
const NO_TEXT = " Do not render any words, letters, numbers, captions, labels or watermarks unless the prompt quotes them exactly.";

function fullPrompt(img) {
  const bgText = img.background === "green" ? GREEN : img.background === "transparent" ? TRANSPARENT : "";
  return [doc.style, img.prompt].filter(Boolean).join("\n\n") + bgText + (img.allowText ? "" : NO_TEXT);
}

const ids = new Set();
for (const img of doc.images ?? []) {
  if (!/^[a-z0-9][a-z0-9_-]*$/i.test(img.id ?? "")) die(`image id "${img.id}" must be letters, digits, - or _`);
  if (ids.has(img.id)) die(`duplicate image id "${img.id}"`);
  ids.add(img.id);
}

// Images with refs must wait for their references, so run in dependency waves.
const todo = (doc.images ?? []).filter(img => !only || only.has(img.id));
const done = new Set(Object.keys(manifest).filter(id => fs.existsSync(jobPath(`assets/${id}.png`))));
let failures = 0;
while (todo.length) {
  const wave = todo.filter(img => (img.ref ?? []).every(r => done.has(r) || !todo.some(x => x.id === r)));
  if (!wave.length) die(`circular refs among: ${todo.map(x => x.id).join(", ")}`);
  await pool(wave, config.image.concurrency, async img => {
    const prompt = fullPrompt(img);
    const key = hash(model, prompt, img.aspect ?? "1:1", img.seed ?? "", img.ref ?? [], config.image.resolution);
    const out = jobPath(`assets/${img.id}.png`);
    if (!a.force && manifest[img.id]?.key === key && fs.existsSync(out)) { console.log(`${img.id}: cached`); done.add(img.id); return; }
    const references = (img.ref ?? []).map(r => {
      const f = jobPath(`assets/raw/${r}.png`);
      if (!fs.existsSync(f)) die(`${img.id}: ref "${r}" has no generated image yet`);
      return "data:image/png;base64," + fs.readFileSync(f).toString("base64");
    });
    let r, used = model;
    try { r = await generateImage({ id: img.id, model, prompt, aspect: img.aspect, seed: img.seed, references, background: img.background }); }
    catch (e) {
      if (isStop(e)) throw e;
      if (!config.image.fallbackModel || config.image.fallbackModel === model || e.status === 401 || e.status === 403) { console.error(`${img.id}: FAILED ${e.message}`); failures++; return; }
      console.error(`${img.id}: ${model} failed (${e.message.slice(0, 160)}), trying ${config.image.fallbackModel}`);
      used = config.image.fallbackModel;
      try { r = await generateImage({ id: img.id, model: used, prompt, aspect: img.aspect, seed: img.seed, references, background: img.background }); }
      catch (e2) { if (isStop(e2)) throw e2; console.error(`${img.id}: FAILED ${e2.message}`); failures++; return; }
    }
    const raw = jobPath(`assets/raw/${img.id}.png`);
    // normalise whatever came back (png/jpeg/webp) to PNG
    const tmp = jobPath(`assets/raw/${img.id}.src`);
    fs.writeFileSync(tmp, r.buffer);
    ff(["-y", "-i", tmp, raw]); fs.rmSync(tmp);
    if (img.background === "green") {
      // key the green, remove green spill on the edges, and soften the matte by a pixel
      ff(["-y", "-i", raw, "-vf", "format=rgba,colorkey=0x00FF00:0.32:0.08,despill=type=green:mix=0.6:expand=0.1", out]);
    } else fs.copyFileSync(raw, out);
    manifest[img.id] = { key, model: used, cost: r.cost, background: img.background ?? "scene" };
    writeJson(manifestPath, manifest);
    done.add(img.id);
    console.log(`${img.id}: ${used} $${r.cost.toFixed(4)} (job total $${r.total.toFixed(3)})`);
  });
  for (const img of wave) todo.splice(todo.indexOf(img), 1);
}
console.log(`images done. spent so far: $${spent().toFixed(3)} of $${config.budgetUsd}`);
if (failures) die(`${failures} image(s) failed`, 4);
