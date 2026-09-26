// Music bed. Run after timeline.mjs (it needs the final duration).
// Usage: node music.mjs [--provider openrouter|file|synth|none] [--force]
// music.json (written by the agent):
// { "prompt": "whimsical pizzicato strings and glockenspiel, light brushed percussion, 100 BPM, D major",
//   "sections": [ { "at": 0, "text": "gentle intro" }, { "at": 18.4, "text": "builds, add percussion" }, { "at": 41, "text": "final chord, ring out" } ] }
// Section times are absolute seconds; use values from cues.json so the music turns with the story.
// Providers:
//   openrouter  Lyria via streamed chat completions (default google/lyria-3-pro-preview, about $0.08 per song)
//   file        EXPLAINER_MUSIC_FILE (a licensed track you supply)
//   synth       no file: mix.mjs renders the engine's built-in bed from music({...}) in scenes.js
//   none        no music
// Out: music/music.<ext>, music/manifest.json
import fs from "node:fs";
import path from "node:path";
import { args, config, ff, hash, jobPath, readJson, writeJson, die, isStop } from "./lib/config.mjs";
import { chatAudio } from "./lib/openrouter.mjs";

const a = args();
const provider = a.provider ?? config.music.provider;
const { dur } = readJson("timeline.json");
fs.mkdirSync(jobPath("music"), { recursive: true });
const mmss = s => `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, "0")}`;

if (provider === "none" || provider === "synth") {
  writeJson("music/manifest.json", { provider });
  console.log(provider === "synth" ? "music: engine synth bed (declare music({...}) in scenes.js)" : "music: none");
  process.exit(0);
}
if (provider === "file") {
  const src = config.music.file;
  if (!src || !fs.existsSync(src)) die("EXPLAINER_MUSIC_FILE is not set or does not exist");
  const dest = `music/music${path.extname(src)}`;
  fs.copyFileSync(src, jobPath(dest));
  writeJson("music/manifest.json", { provider, file: dest, source: src });
  console.log(`music: ${src}`);
  process.exit(0);
}
if (provider !== "openrouter") die(`unknown music provider "${provider}"`);

const spec = readJson("music.json", null);
const base = a.prompt ?? spec?.prompt;
if (!base) die("write music.json with a \"prompt\" (instruments, mood, tempo, key) before running music.mjs");
const sections = (spec?.sections ?? []).slice().sort((x, y) => x.at - y.at);
const timeline = sections.map((s, k) => `[${mmss(s.at)} - ${mmss(sections[k + 1]?.at ?? dur)}] ${s.text}`).join("\n");
const prompt = [
  `Instrumental background score for a narrated explainer video. Instrumental only, no vocals, no lyrics, no spoken words.`,
  base,
  `Total length about ${Math.ceil(dur)} seconds, ending on a clean final chord with a short natural ring-out.`,
  `Keep the mid-range sparse and the dynamics steady so a voice-over sits clearly on top.`,
  timeline && `Structure:\n${timeline}`,
].filter(Boolean).join("\n\n");

const key = hash(config.music.model, prompt);
const prev = readJson("music/manifest.json", {});
if (!a.force && prev.key === key && prev.file && fs.existsSync(jobPath(prev.file))) { console.log(`music: cached ${prev.file}`); process.exit(0); }

let r;
try { r = await chatAudio({ model: config.music.model, prompt, format: "wav", id: "music" }); }
catch (e) {
  if (isStop(e)) throw e;
  die(`music generation failed: ${e.message}
fallback: set EXPLAINER_MUSIC_PROVIDER=synth (engine bed), =file, or =none, then continue`, 4);
}
// The stream may carry WAV, MP3 or headerless PCM depending on the upstream provider.
const b = r.buffer, file = "music/music.wav";
const head = b.subarray(0, 4).toString("latin1");
if (head === "RIFF") fs.writeFileSync(jobPath(file), b);
else if (head.startsWith("ID3") || (b[0] === 0xff && (b[1] & 0xe0) === 0xe0) || head === "OggS" || head === "fLaC") {
  const src = jobPath("music/music.src"); fs.writeFileSync(src, b); ff(["-y", "-i", src, jobPath(file)]); fs.rmSync(src);
} else {
  const src = jobPath("music/music.pcm"); fs.writeFileSync(src, b);
  ff(["-y", "-f", "s16le", "-ar", String(+(a.rate ?? 48000)), "-ac", "2", "-i", src, jobPath(file)]); fs.rmSync(src);
  console.log("music: stream was headerless PCM, decoded as s16le 48 kHz stereo (override with --rate)");
}
fs.writeFileSync(jobPath("music/prompt.txt"), prompt);
writeJson("music/manifest.json", { provider, model: config.music.model, file, key, cost: r.cost });
console.log(`music: ${config.music.model} → ${file} $${r.cost.toFixed(3)} (job total $${r.total.toFixed(3)})`);
