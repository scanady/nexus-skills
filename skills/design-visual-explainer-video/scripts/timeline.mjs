// Place narration clips on the timeline.
// In:  lines.json, vo/manifest.json (from tts.mjs)
// Out: vo/line<i>.wav (trimmed, loudness-normalised), narration.wav, cues.json (per-word times),
//      timeline.json {dur}, captions.srt, captions.vtt
// Env/flags: --start 0.8 (first line), --gap 0.55 (default pause between lines), --tail 2.5 (after last word)
// The video length is decided here, once. build.mjs, mix.mjs and render.mjs read it from timeline.json.
import fs from "node:fs";
import { args, config, ff, mediaDuration, loudnorm, readJson, writeJson, jobPath, die } from "./lib/config.mjs";
import { loadLines } from "./lib/lines.mjs";

const a = args();
const START = +(a.start ?? 0.8), GAP = +(a.gap ?? 0.55), TAIL = +(a.tail ?? 2.5);
const { lines } = loadLines();
const manifest = readJson("vo/manifest.json");
if (manifest.length !== lines.length) die(`vo/manifest.json has ${manifest.length} clips but lines.json has ${lines.length} lines: re-run tts.mjs`);

// Spread words over a clip by character weight, with extra weight for punctuation pauses.
function estimateWords(text, dur) {
  const words = text.split(/\s+/).filter(Boolean);
  const weight = w => w.replace(/[^\p{L}\p{N}]/gu, "").length + 2 + (/[,;:]$/.test(w) ? 4 : 0) + (/[.!?…]$/.test(w) ? 7 : 0);
  const total = words.reduce((s, w) => s + weight(w), 0) || 1;
  let acc = 0;
  return words.map(w => { const t = (acc / total) * dur * 0.97; acc += weight(w); return { w, t: +t.toFixed(3) }; });
}

const cues = [];
let t = START;
for (const [i, line] of lines.entries()) {
  const clip = manifest[i];
  const src = jobPath(clip.file);
  if (!fs.existsSync(src)) die(`missing ${clip.file}: re-run tts.mjs`);
  const out = jobPath(`vo/line${i}.wav`);
  if (clip.provider === "silent") { // animatic: keep the silent clip as is
    ff(["-y", "-i", src, "-ar", "48000", "-ac", "1", out]);
    const dur = mediaDuration(out);
    cues.push({ i, start: +t.toFixed(3), dur: +dur.toFixed(3), text: line.text, timing: "silent", words: estimateWords(line.text, dur).map(w => ({ w: w.w, t: +(t + w.t).toFixed(3) })) });
    t += dur + (line.pauseAfter ?? GAP);
    continue;
  }
  // Measure leading silence so provider word times can be shifted after trimming.
  const sd = ff(["-i", src, "-af", "silencedetect=n=-45dB:d=0.04", "-f", "null", "-"]);
  const m = sd.match(/silence_start: (-?[\d.]+)[\s\S]*?silence_end: ([\d.]+)/);
  const lead = m && parseFloat(m[1]) <= 0.02 ? parseFloat(m[2]) : 0;
  const trimmed = jobPath(`vo/trim${i}.wav`);
  ff(["-y", "-i", src, "-af", "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,apad=pad_dur=0.05", "-ar", "48000", "-ac", "1", trimmed]);
  loudnorm(trimmed, out, { LRA: 7, ac: 1 });
  fs.rmSync(trimmed);
  const dur = mediaDuration(out);
  const exact = Array.isArray(clip.words) && clip.words.length && !line.say;
  const words = exact
    ? clip.words.map(w => ({ w: w.w, t: +Math.min(dur, Math.max(0, w.t - lead)).toFixed(3) }))
    : estimateWords(line.text, dur);
  cues.push({
    i, start: +t.toFixed(3), dur: +dur.toFixed(3), text: line.text, timing: exact ? "exact" : "estimated",
    words: words.map(w => ({ w: w.w, t: +(t + w.t).toFixed(3) })),
  });
  t += dur + (line.pauseAfter ?? GAP);
}

const END = cues.at(-1).start + cues.at(-1).dur;
const fps = config.video.fps;
const DUR = Math.ceil((END + TAIL) * fps) / fps;

// Mix the lines at their start times into one mono track padded to DUR.
const inputs = cues.flatMap(c => ["-i", jobPath(`vo/line${c.i}.wav`)]);
const delays = cues.map((c, k) => { const ms = Math.round(c.start * 1000); return `[${k}]adelay=${ms}|${ms}[a${k}]`; }).join(";");
const filter = `${delays};${cues.map((_, k) => `[a${k}]`).join("")}amix=inputs=${cues.length}:normalize=0,apad=whole_dur=${DUR}[o]`;
ff(["-y", ...inputs, "-filter_complex", filter, "-map", "[o]", "-ar", "48000", "-ac", "1", "-t", String(DUR), jobPath("narration.wav")]);

writeJson("cues.json", cues);
writeJson("timeline.json", { dur: +DUR.toFixed(3), end: +END.toFixed(3), start: START, gap: GAP, tail: TAIL, fps });

// Captions: chunks of up to 7 words / 42 characters, each shown until the next chunk starts.
const stamp = (s, sep) => { const ms = Math.round(s * 1000); const h = Math.floor(ms / 3600000), mi = Math.floor(ms / 60000) % 60, se = Math.floor(ms / 1000) % 60; return `${String(h).padStart(2, "0")}:${String(mi).padStart(2, "0")}:${String(se).padStart(2, "0")}${sep}${String(ms % 1000).padStart(3, "0")}`; };
const chunks = [];
for (const c of cues) {
  let cur = [];
  const flush = () => { if (cur.length) chunks.push({ a: cur[0].t, words: cur.map(w => w.w).join(" "), lineEnd: c.start + c.dur }); cur = []; };
  for (const w of c.words) { if (cur.length >= 7 || [...cur, w].map(x => x.w).join(" ").length > 42) flush(); cur.push(w); }
  flush();
}
chunks.forEach((ch, k) => { ch.b = Math.min(ch.lineEnd + 0.3, chunks[k + 1]?.a ?? ch.lineEnd + 0.3); });
fs.writeFileSync(jobPath("captions.srt"), chunks.map((ch, k) => `${k + 1}\n${stamp(ch.a, ",")} --> ${stamp(ch.b, ",")}\n${ch.words}\n`).join("\n"));
fs.writeFileSync(jobPath("captions.vtt"), "WEBVTT\n\n" + chunks.map(ch => `${stamp(ch.a, ".")} --> ${stamp(ch.b, ".")}\n${ch.words}\n`).join("\n"));

for (const c of cues) console.log(`line ${c.i}  ${c.start.toFixed(2)}s +${c.dur.toFixed(2)}s  (${c.timing})  ${c.text.slice(0, 70)}`);
const words = cues.reduce((s, c) => s + c.words.length, 0);
console.log(`speech ends ${END.toFixed(2)}s, video ${DUR.toFixed(2)}s, ${words} words = ${Math.round(words / (END - START) * 60)} wpm`);
console.log("wrote narration.wav cues.json timeline.json captions.srt captions.vtt");
