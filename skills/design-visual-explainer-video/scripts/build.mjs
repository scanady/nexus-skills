// Assemble a self-contained out.html from the skill's player + engine and the job's scenes.js,
// embedding fonts, images, per-word cues and the best available audio (mix.m4a > narration).
// Usage: node build.mjs [--title "..."] [--seed name] [--publish <dir>]   (--publish copies to <dir>/index.html)
import fs from "node:fs";
import path from "node:path";
import { args, config, ff, jobPath, readJson, die } from "./lib/config.mjs";
import { assemblePage, b64, fontFaces, loadImages } from "./lib/page.mjs";

const a = args();
const { dur } = readJson("timeline.json");
const cues = readJson("cues.json").map(c => ({ start: c.start, dur: c.dur, text: c.text, words: c.words }));
if (!fs.existsSync(jobPath("scenes.js"))) die("missing scenes.js (start from assets/example/scenes.js in the skill)");
const brief = readJson("brief.json", {});
const { css, families } = fontFaces();
const images = loadImages();

// Player audio: the final mix when it exists, otherwise narration only (preview before mixing).
let audio = null;
if (fs.existsSync(jobPath("mix.m4a"))) audio = "data:audio/mp4;base64," + b64("mix.m4a");
else if (fs.existsSync(jobPath("narration.wav"))) {
  ff(["-y", "-i", jobPath("narration.wav"), "-c:a", "libmp3lame", "-b:a", "96k", jobPath("narration.mp3")]);
  audio = "data:audio/mpeg;base64," + b64("narration.mp3");
}

const { width, height, fps } = config.video;
const data = {
  title: a.title ?? brief.title ?? "Explainer",
  width, height, fps, dur,
  seed: a.seed ?? brief.seed ?? brief.title ?? cues[0]?.text ?? "explainer",
  language: brief.language ?? config.language,
  cues, images, audio,
  fontFamilies: families,
};
const html = assemblePage({ data, scenesJs: fs.readFileSync(jobPath("scenes.js"), "utf8"), faces: css });
fs.writeFileSync(jobPath("out.html"), html);

const mb = Buffer.byteLength(html) / 1048576;
console.log(`out.html ${mb.toFixed(1)} MB  ${width}x${height}@${fps}  dur ${dur}s  images ${Object.keys(images).length}  fonts ${families.join(", ") || "(none: system sans-serif)"}  audio ${audio ? (audio.includes("audio/mp4") ? "final mix" : "narration only") : "none"}`);
if (mb > 40) console.log("warning: over 40 MB; lower EXPLAINER_IMAGE_RESOLUTION or use fewer images so the HTML stays shareable");
if (a.publish) {
  fs.mkdirSync(a.publish, { recursive: true });
  fs.copyFileSync(jobPath("out.html"), path.join(a.publish, "index.html"));
  console.log(`published ${path.join(a.publish, "index.html")}`);
}
