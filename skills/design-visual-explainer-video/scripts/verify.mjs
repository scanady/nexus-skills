// Check the finished MP4 by measurement and write contact sheets pulled from the file itself.
// Usage: node verify.mjs [video.mp4] [--max-mb 60] [--freeze 2.5]
// Checks: duration vs timeline, video/audio/subtitle streams, loudness and true peak,
// unintended black stretches, long silences, file size, a flat first frame, one-frame flashes and pops,
// frozen stretches, and whether Whisper can understand the narration over the music.
// Sheets: shots/verify.jpg (9 frames), shots/hook.jpg (first 3 s, sound-off test), shots/phone-NN.jpg (1 fps at 360 px wide).
// Writes verify.json (review-pack.mjs reads it). Prints the spend ledger. Exit 6 on any FAIL.
import "./lib/job.mjs";
import fs from "node:fs";
import { spawnSync } from "node:child_process";
import { args, config, ff, ffmpegBin, jobPath, readJson, loudness, mediaDuration, ledger, die, writeJson } from "./lib/config.mjs";
import { loadLines } from "./lib/lines.mjs";
import { alignWords, canCheckSpeech, splitWords } from "./lib/align.mjs";
import { launch, openPage } from "./lib/browser.mjs";

const a = args();
const file = jobPath(a._[0] ?? "video.mp4");
if (!fs.existsSync(file)) die(`missing ${file}`);
const { dur } = readJson("timeline.json");
const cues = readJson("cues.json", []);
const problems = [], warnings = [], notes = [];
const FREEZE_SECS = +(a.freeze ?? 2.5);

const info = ff(["-i", file, "-f", "null", "-t", "0", "-"]);
const vid = info.match(/Stream #\S+.*Video: (\w+).*?, (\d+)x(\d+).*?, ([\d.]+) fps/);
const aud = info.match(/Stream #\S+.*Audio: (\w+).*?(\d+) Hz, (\w+)/);
const sub = /Stream #\S+.*Subtitle: mov_text/.test(info);
const d = mediaDuration(file);
if (!vid) problems.push("no video stream"); else notes.push(`video ${vid[1]} ${vid[2]}x${vid[3]} @ ${vid[4]} fps`);
if (!aud) problems.push("no audio stream"); else notes.push(`audio ${aud[1]} ${aud[2]} Hz ${aud[3]}`);
notes.push(sub ? "captions: soft subtitle track present" : "captions: none embedded");
if (Math.abs(d - dur) > 0.25) problems.push(`duration ${d.toFixed(2)}s, timeline says ${dur}s`); else notes.push(`duration ${d.toFixed(2)}s`);

if (aud) {
  const L = loudness(file);
  notes.push(`loudness ${L.I} LUFS, true peak ${L.TP} dBTP, LRA ${L.LRA} LU`);
  if (Math.abs(L.I - config.audio.lufs) > 1.5) problems.push(`loudness ${L.I} LUFS, target ${config.audio.lufs}`);
  if (L.TP > config.audio.truePeak + 0.7) problems.push(`true peak ${L.TP} dBTP above ${config.audio.truePeak}`);
  const sil = [...ff(["-i", file, "-af", "silencedetect=n=-45dB:d=2.5", "-vn", "-f", "null", "-"]).matchAll(/silence_start: ([\d.]+)[\s\S]*?silence_end: ([\d.]+)/g)];
  for (const [, s, e] of sil) if (+s > 0.5 && +e < d - 1) problems.push(`audio silent ${(+s).toFixed(1)}–${(+e).toFixed(1)}s`);
}
const black = [...ff(["-i", file, "-vf", "blackdetect=d=0.4:pix_th=0.08", "-an", "-f", "null", "-"]).matchAll(/black_start:([\d.]+) black_end:([\d.]+)/g)];
for (const [, s, e] of black) if (+s > 0.6 && +e < d - 1.0) problems.push(`black frames ${(+s).toFixed(2)}–${(+e).toFixed(2)}s`);

const mb = fs.statSync(file).size / 1048576, maxMb = +(a["max-mb"] ?? 60);
notes.push(`size ${mb.toFixed(1)} MB`);
if (mb > maxMb) problems.push(`file is ${mb.toFixed(1)} MB (> ${maxMb} MB): lower EXPLAINER_MAXRATE`);

// Picture checks on tiny greyscale frames from the encoded file.
if (vid) {
  const fps = +vid[4], aw = 192, ah = Math.max(2, Math.round(aw * +vid[3] / +vid[2] / 2) * 2), size = aw * ah;
  const raw = spawnSync(ffmpegBin(), ["-v", "error", "-i", file, "-vf", `scale=${aw}:${ah}:flags=area,format=gray`, "-f", "rawvideo", "-"], { maxBuffer: 1 << 30 }).stdout;
  const n = Math.floor(raw.length / size), frame = i => raw.subarray(i * size, (i + 1) * size);
  const meanDiff = (p, q) => { let s = 0; for (let k = 0; k < size; k++) s += Math.abs(p[k] - q[k]); return s / size; };
  const at = i => (i / fps).toFixed(2);
  const f0 = frame(0), mean = f0.reduce((s, v) => s + v, 0) / size;
  const std = Math.sqrt(f0.reduce((s, v) => s + (v - mean) ** 2, 0) / size);
  if (std < 6 || mean < 8) problems.push(`first frame is flat or black (mean ${mean.toFixed(0)}, spread ${std.toFixed(0)}): it is the thumbnail, so draw a finished picture at t = 0`);
  const diff = new Float64Array(n);
  for (let i = 1; i < n; i++) diff[i] = meanDiff(frame(i), frame(i - 1));
  const median = [...diff.subarray(1)].sort((p, q) => p - q)[Math.floor((n - 1) / 2)] ?? 0;
  // A planned shake() jitters frame to frame, which looks like a flash or a pop. Skip those frames.
  const browser = await launch();
  const { meta } = await openPage(browser);
  await browser.close();
  const shaking = i => (meta.shakes ?? []).some(s => i / fps >= s.t - 0.05 && i / fps <= s.t + s.len + 0.05);
  // Flash: one frame differs from both neighbours, but the neighbours match each other.
  const flashLevel = Math.max(2, 4 * median), flashes = [];
  for (let i = 1; i < n - 1; i++) if (!shaking(i) && diff[i] > flashLevel && diff[i + 1] > flashLevel && meanDiff(frame(i + 1), frame(i - 1)) < 0.35 * Math.min(diff[i], diff[i + 1])) flashes.push(i);
  if (flashes.length) problems.push(`one-frame flashes at ${flashes.map(at).join(", ")}s`);
  // Pop: a small jump, far above its neighbours. A hard cut is larger than this.
  // A caption changing looks the same and is expected: at a line start, on a spoken word, or as it leaves 0.25 s after the line.
  const flashed = new Set(flashes.flatMap(i => [i, i + 1])), pops = [];
  const expected = i => cues.some(c => Math.abs(i / fps - c.start) < 0.15 || Math.abs(i / fps - (c.start + c.dur + 0.25)) < 0.05 || (c.words ?? []).some(w => Math.abs(i / fps - w.t) < 0.05));
  for (let i = 1; i < n - 1; i++) if (!flashed.has(i) && !shaking(i) && !expected(i) && diff[i] > 2 && diff[i] <= 6 && diff[i] > 3 * Math.max(diff[i - 1], diff[i + 1])) pops.push(i);
  if (pops.length) warnings.push(`small jumps at ${pops.map(at).join(", ")}s: a planned hit, or a glitch?`);
  // Frozen: nothing moves for a long time. The hold at the very end is expected.
  const stillLevel = 0.25;
  for (let i = 1, start = null; i <= n; i++) {
    if (i < n && diff[i] < stillLevel) { start ??= i - 1; continue; }
    if (start !== null && (i - 1 - start) / fps >= FREEZE_SECS && i < n) warnings.push(`nothing moves from ${at(start)} to ${at(i - 1)}s: a planned hold, or dead air?`);
    start = null;
  }
  notes.push(`picture: ${n} frames, median change ${median.toFixed(2)}/255 per frame`);
}

// Sheets from the encoded file: what a viewer gets, not what the canvas drew.
fs.mkdirSync(jobPath("shots"), { recursive: true });
ff(["-y", "-i", file, "-vf", `fps=9/${d.toFixed(2)},scale=640:-2,tile=3x3:padding=4:color=black`, "-frames:v", "1", "-q:v", "3", jobPath("shots/verify.jpg")]);
ff(["-y", "-t", "3.5", "-i", file, "-vf", "fps=2,scale=360:-2,tile=7x1:padding=4:color=black", "-frames:v", "1", "-q:v", "3", jobPath("shots/hook.jpg")]);
for (const f of fs.readdirSync(jobPath("shots"))) if (/^phone-\d+\.jpg$/.test(f)) fs.rmSync(jobPath("shots", f));
for (let s = 0, k = 1; s < d; s += 40, k++) ff(["-y", "-ss", String(s), "-t", "40", "-i", file, "-vf", "fps=1,scale=360:-2,tile=8x5:padding=4:color=black", "-frames:v", "1", "-q:v", "3", jobPath(`shots/phone-${String(k).padStart(2, "0")}.jpg`)]);
notes.push("sheets: shots/verify.jpg, shots/hook.jpg (sound off: what is this?), shots/phone-*.jpg (readable at 360 px?). Look at them");

// Speech check: can the narration be understood over the music and effects?
const { lines } = loadLines();
const language = readJson("brief.json", {}).language ?? config.language;
let speech = null;
if (cues.every(c => c.timing === "silent")) notes.push("speech check: silent narration, nothing to hear");
else if (!canCheckSpeech(language)) warnings.push(`speech check: not available for "${language}"`);
else {
  try {
    const { loadWhisper } = await import("./lib/whisper.mjs");
    const listen = await loadWhisper(language);
    const spoken = lines.map(l => splitWords(l.say ?? l.text));
    const r = alignWords(spoken.flat(), await listen(file), d, language);
    const pct = v => `${Math.round(v * 100)}%`;
    let k = 0;
    const perLine = spoken.map(ws => { const part = r.words.slice(k, k += ws.length); return part.filter(w => w.heard).length / Math.max(1, part.length); });
    // Compare measured times with the cues that drive the animation (lines where the caption words are the spoken words).
    k = 0;
    const offsets = lines.flatMap((l, i) => {
      const part = r.words.slice(k, k += spoken[i].length);
      return l.say ? [] : part.flatMap((w, q) => (w.heard && cues[i]?.words[q] ? [Math.abs(w.t - cues[i].words[q].t)] : []));
    }).sort((p, q) => p - q);
    const offset = offsets[Math.floor(offsets.length / 2)] ?? 0;
    speech = { matchRate: +r.matchRate.toFixed(3), medianOffset: +offset.toFixed(3), perLine: perLine.map(v => +v.toFixed(3)) };
    notes.push(`speech check: ${pct(r.matchRate)} of the script understood in the final mix; word times off by ${offset.toFixed(2)}s (median)`);
    if (r.matchRate < 0.7) problems.push(`only ${pct(r.matchRate)} of the script is understood in the final mix: raise mix.mjs --under or check the voice`);
    else if (r.matchRate < 0.85) warnings.push(`${pct(r.matchRate)} of the script is understood in the final mix (aim for 85%): raise mix.mjs --under, or use fewer effects under speech`);
    perLine.forEach((v, i) => { if (v < 0.8) warnings.push(`line ${i}: only ${pct(v)} understood in the final mix: "${lines[i].text.slice(0, 60)}"`); });
    if (offset > 0.25) warnings.push(`word times are off by ${offset.toFixed(2)}s (median): run align.mjs and timeline.mjs, then rebuild`);
  } catch (e) { warnings.push(`speech check skipped: ${e.message.split("\n")[0]}`); }
}

const l = ledger(), spentUsd = l.entries.reduce((s, e) => s + (e.cost || 0), 0);
const byKind = {};
for (const e of l.entries) byKind[e.kind] = (byKind[e.kind] ?? 0) + (e.cost || 0);
notes.push(`spend $${spentUsd.toFixed(3)} of $${config.budgetUsd}: ${Object.entries(byKind).map(([k, v]) => `${k} $${v.toFixed(3)}`).join(", ") || "none"}${l.entries.some(e => e.estimated) ? " (some entries estimated)" : ""}`);

writeJson("verify.json", { file: a._[0] ?? "video.mp4", notes, warnings, problems, speech });
notes.forEach(n => console.log("ok    " + n));
warnings.forEach(w => console.log("warn  " + w));
problems.forEach(p => console.log("FAIL  " + p));
process.exitCode = problems.length ? 6 : 0;
