// Check the finished MP4 by measurement and write a 3×3 contact sheet pulled from the file itself.
// Usage: node verify.mjs [video.mp4] [--max-mb 60]
// Checks: duration vs timeline, video/audio/subtitle streams, loudness and true peak,
// unintended black stretches, long silences, file size. Prints the spend ledger.
import fs from "node:fs";
import { args, config, ff, jobPath, readJson, loudness, mediaDuration, ledger, die } from "./lib/config.mjs";

const a = args();
const file = jobPath(a._[0] ?? "video.mp4");
if (!fs.existsSync(file)) die(`missing ${file}`);
const { dur } = readJson("timeline.json");
const problems = [], notes = [];

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

// Contact sheet from the encoded file: 9 frames spread across the video.
fs.mkdirSync(jobPath("shots"), { recursive: true });
ff(["-y", "-i", file, "-vf", `fps=9/${d.toFixed(2)},scale=640:-2,tile=3x3:padding=4:color=black`, "-frames:v", "1", "-q:v", "3", jobPath("shots/verify.jpg")]);
notes.push("contact sheet: shots/verify.jpg (look at it)");

const l = ledger(), spentUsd = l.entries.reduce((s, e) => s + (e.cost || 0), 0);
const byKind = {};
for (const e of l.entries) byKind[e.kind] = (byKind[e.kind] ?? 0) + (e.cost || 0);
notes.push(`spend $${spentUsd.toFixed(3)} of $${config.budgetUsd}: ${Object.entries(byKind).map(([k, v]) => `${k} $${v.toFixed(3)}`).join(", ") || "none"}${l.entries.some(e => e.estimated) ? " (some entries estimated)" : ""}`);

notes.forEach(n => console.log("ok    " + n));
problems.forEach(p => console.log("FAIL  " + p));
process.exitCode = problems.length ? 6 : 0;
