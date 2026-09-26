// Deterministic frame-by-frame render: window.__render(t) for every frame, JPEG frames piped to ffmpeg.
// Frames are split across parallel browser pages, encoded as segments, then joined without re-encoding.
// Usage: node render.mjs [--out video.mp4] [--workers 4] [--draft] [--from 10 --to 20] [--no-subs]
//   --draft   half resolution, 15 fps, fast preset: a quick full-length check before the final render
// Audio: mix.wav (from mix.mjs); falls back to narration.wav with a warning. Captions: captions.srt as a soft track.
import fs from "node:fs";
import os from "node:os";
import { spawn } from "node:child_process";
import { args, config, ff, ffmpegBin, jobPath, readJson, mediaDuration } from "./lib/config.mjs";
import { launch, openPage } from "./lib/browser.mjs";

const a = args();
const { dur } = readJson("timeline.json");
const draft = !!a.draft;
const fps = draft ? 15 : config.video.fps;
const scale = draft ? 0.5 : 1;
const out = jobPath(a.out ?? (draft ? "draft.mp4" : "video.mp4"));
const from = Math.max(0, +(a.from ?? 0)), to = Math.min(dur, +(a.to ?? dur));
const first = Math.round(from * fps), last = Math.round(to * fps); // [first, last)
const total = last - first;
const workers = Math.max(1, Math.min(+(a.workers ?? (config.video.workers || Math.min(4, Math.max(1, Math.floor(os.cpus().length / 2))))), Math.ceil(total / (fps * 2))));
fs.mkdirSync(jobPath("render"), { recursive: true });

const enc = draft
  ? ["-c:v", "libx264", "-preset", "veryfast", "-crf", "28"]
  : ["-c:v", "libx264", "-preset", "medium", "-crf", String(config.video.crf), "-maxrate", config.video.maxrate, "-bufsize", `${parseInt(config.video.maxrate) * 2}M`];
const W = Math.round(config.video.width * scale / 2) * 2, H = Math.round(config.video.height * scale / 2) * 2;

const browser = await launch();
const t0 = Date.now();
let doneFrames = 0, lastLog = 0;
const chunk = Math.ceil(total / workers);
const segs = [];
await Promise.all([...Array(workers)].map(async (_, k) => {
  const a0 = first + k * chunk, a1 = Math.min(last, a0 + chunk);
  if (a1 <= a0) return;
  const seg = jobPath(`render/seg${String(k).padStart(2, "0")}.mp4`);
  segs[k] = seg;
  const { page, errors } = await openPage(browser);
  const proc = spawn(ffmpegBin(), ["-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", String(fps), "-c:v", "mjpeg", "-i", "-",
    "-vf", `scale=${W}:${H}:flags=lanczos,format=yuv420p`, ...enc, "-g", String(fps * 2), "-r", String(fps), seg], { stdio: ["pipe", "inherit", "inherit"] });
  const closed = new Promise((res, rej) => proc.on("close", c => (c === 0 ? res() : rej(new Error(`ffmpeg segment ${k} exited ${c}`)))));
  for (let i = a0; i < a1; i++) {
    const d = await page.evaluate(t => { window.__render(t); return window.__canvas.toDataURL("image/jpeg", 0.93); }, i / fps);
    if (!proc.stdin.write(Buffer.from(d.slice(d.indexOf(",") + 1), "base64"))) await new Promise(r => proc.stdin.once("drain", r));
    doneFrames++;
    if (Date.now() - lastLog > 5000) { lastLog = Date.now(); const s = (Date.now() - t0) / 1000; console.log(`frames ${doneFrames}/${total}  ${s.toFixed(0)}s elapsed, ~${((total - doneFrames) * s / doneFrames).toFixed(0)}s left`); }
  }
  proc.stdin.end();
  await closed;
  if (errors.length) console.log(`worker ${k} console errors:\n  ${[...new Set(errors)].slice(0, 10).join("\n  ")}`);
  await page.close();
}));
await browser.close();

// Join segments (same encoder settings, so stream copy is safe).
const list = jobPath("render/segments.txt");
fs.writeFileSync(list, segs.filter(Boolean).map(s => `file '${s.replace(/\\/g, "/").replace(/'/g, "'\\''")}'`).join("\n"));
const silent = jobPath("render/video_noaudio.mp4");
ff(["-y", "-f", "concat", "-safe", "0", "-i", list, "-c", "copy", silent]);

// Mux audio (+ soft captions).
let audio = jobPath("mix.wav");
if (!fs.existsSync(audio)) { audio = jobPath("narration.wav"); console.log("warn: mix.wav missing, muxing narration only (run mix.mjs for music + sfx)"); }
const subs = !a["no-subs"] && fs.existsSync(jobPath("captions.srt")) && from === 0;
const lang = { en: "eng", es: "spa", fr: "fra", de: "deu", nl: "nld", pt: "por", it: "ita", ja: "jpn", zh: "zho", ko: "kor" }[config.language.slice(0, 2)] ?? "und";
ff(["-y", "-i", silent, "-ss", String(from), "-t", String(to - from), "-i", audio, ...(subs ? ["-i", jobPath("captions.srt")] : []),
  "-map", "0:v", "-map", "1:a", ...(subs ? ["-map", "2:s", "-c:s", "mov_text", "-metadata:s:s:0", `language=${lang}`] : []),
  // explicit -t, not -shortest: the caption track ends at the last caption and would cut the video short
  "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-t", String(total / fps), "-movflags", "+faststart", out]);
for (const s of segs.filter(Boolean)) fs.rmSync(s);
fs.rmSync(silent);

const mb = fs.statSync(out).size / 1048576;
console.log(`done ${out}  ${mediaDuration(out).toFixed(2)}s  ${W}x${H}@${fps}  ${mb.toFixed(1)} MB  in ${((Date.now() - t0) / 1000).toFixed(0)}s with ${workers} worker(s)`);
