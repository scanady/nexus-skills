// Final audio mix: narration on top, music ducked under speech, SFX from the engine, loudness-normalised.
// Usage: node mix.mjs [--duck 8] [--under 16] [--sfx 0.8] [--no-sfx] [--no-music] [--loop]
//   --under  dB the music sits under the voice while someone speaks (default EXPLAINER_MUSIC_UNDER_VOICE_DB=16)
//   --duck   extra dB the music drops during speech versus the gaps between lines (default 8)
// In:  narration.wav, cues.json, timeline.json, music/manifest.json (music.mjs), out.html (for SFX + synth bed)
// Out: stems/sfx.wav, stems/music.wav, mix.wav (final, 48 kHz stereo), mix.m4a (for the HTML player)
import fs from "node:fs";
import { args, config, ff, jobPath, readJson, loudnorm, loudness, mediaDuration, die } from "./lib/config.mjs";
import { launch, openPage } from "./lib/browser.mjs";

const a = args();
const { dur } = readJson("timeline.json");
const cues = readJson("cues.json");
const UNDER = +(a.under ?? config.audio.musicUnderVoiceDb), DUCK = +(a.duck ?? 8), SFX_GAIN = +(a.sfx ?? config.audio.sfxGain);
const target = config.audio.lufs;
if (!fs.existsSync(jobPath("narration.wav"))) die("missing narration.wav: run timeline.mjs");
fs.mkdirSync(jobPath("stems"), { recursive: true });

// 1. SFX (and the synth music bed if chosen) come from the engine's OfflineAudioContext.
const mm = readJson("music/manifest.json", { provider: "synth" });
const browser = await launch();
const { page, errors } = await openPage(browser);
const sfxB64 = a["no-sfx"] ? null : await page.evaluate(() => window.__renderAudio("sfx"));
const synthB64 = !a["no-music"] && mm.provider === "synth" ? await page.evaluate(() => window.__renderAudio("music")) : null;
await browser.close();
for (const e of new Set(errors)) console.log("console: " + e);
if (sfxB64) fs.writeFileSync(jobPath("stems/sfx.wav"), Buffer.from(sfxB64, "base64"));
else if (fs.existsSync(jobPath("stems/sfx.wav"))) fs.rmSync(jobPath("stems/sfx.wav"));

// 2. Music bed: loop/trim to length, fades, set its level relative to the voice, then duck under each line.
let musicSrc = null;
if (!a["no-music"]) {
  if (mm.file && fs.existsSync(jobPath(mm.file))) musicSrc = jobPath(mm.file);
  else if (synthB64) { musicSrc = jobPath("stems/synth.wav"); fs.writeFileSync(musicSrc, Buffer.from(synthB64, "base64")); }
}
if (musicSrc) {
  const shaped = jobPath("stems/music_shaped.wav");
  // Drop trailing silence so "the end of the track" means its last note.
  const trimmed = jobPath("stems/music_trimmed.wav");
  ff(["-y", "-i", musicSrc, "-af", "areverse,silenceremove=start_periods=1:start_threshold=-50dB,areverse", "-ar", "48000", "-ac", "2", trimmed]);
  const mdur = mediaDuration(trimmed);
  const E = Math.min(8, dur * 0.35), X = 1.5;
  if (!a.loop && mdur > dur + 4) {
    // Generated tracks rarely match the requested length (Lyria gave 61 s for a 19 s request).
    // Keep the natural start and splice the track's real ending onto the video's end with a crossfade.
    const f = `[0]asplit=2[s0][s1];[s0]atrim=0:${(dur - E + X).toFixed(3)},asetpts=PTS-STARTPTS[a];[s1]atrim=${(mdur - E).toFixed(3)}:${mdur.toFixed(3)},asetpts=PTS-STARTPTS[b];[a][b]acrossfade=d=${X}:c1=tri:c2=tri,afade=t=in:d=0.8,apad=whole_dur=${dur}[o]`;
    ff(["-y", "-i", trimmed, "-filter_complex", f, "-map", "[o]", "-t", String(dur), shaped]);
    console.log(`music: ${mdur.toFixed(1)}s track → first ${(dur - E + X).toFixed(1)}s + its last ${E.toFixed(1)}s ending, ${X}s crossfade`);
  } else {
    // Shorter (or --loop): loop to length and fade out.
    ff(["-y", "-stream_loop", "-1", "-i", trimmed, "-t", String(dur), "-af", `afade=t=in:d=0.8,afade=t=out:st=${Math.max(0, dur - 3).toFixed(2)}:d=3`, shaped]);
  }
  fs.rmSync(trimmed);
  // Between lines the bed plays at (target − UNDER + DUCK); during speech it drops by DUCK → UNDER dB below the voice.
  loudnorm(shaped, jobPath("stems/music_level.wav"), { I: target - UNDER + DUCK, TP: -3, LRA: 11, ac: 2 });
  const depth = (1 - Math.pow(10, -DUCK / 20)).toFixed(4);
  const ramps = cues.map(c => {
    const s = (c.start - 0.35).toFixed(3), e = (c.start + c.dur + 0.45).toFixed(3);
    return `clip((t-${s})/0.3,0,1)*clip((${e}-t)/0.45,0,1)`;
  });
  const env = ramps.reduce((acc, r) => (acc ? `max(${acc},${r})` : r), "");
  fs.writeFileSync(jobPath("stems/duck.txt"), `volume='1-${depth}*(${env})':eval=frame`);
  ff(["-y", "-i", jobPath("stems/music_level.wav"), "-filter_script:a", jobPath("stems/duck.txt"), jobPath("stems/music.wav")]);
  fs.rmSync(shaped); fs.rmSync(jobPath("stems/music_level.wav"));
} else if (fs.existsSync(jobPath("stems/music.wav"))) fs.rmSync(jobPath("stems/music.wav"));

// 3. Sum, limit, normalise.
const inputs = ["-i", jobPath("narration.wav")];
const parts = ["[0:a]aformat=channel_layouts=stereo,aresample=48000[v]"];
let n = 1; const labels = ["[v]"];
if (fs.existsSync(jobPath("stems/music.wav"))) { inputs.push("-i", jobPath("stems/music.wav")); parts.push(`[${n}:a]aresample=48000[m]`); labels.push("[m]"); n++; }
if (fs.existsSync(jobPath("stems/sfx.wav"))) { inputs.push("-i", jobPath("stems/sfx.wav")); parts.push(`[${n}:a]volume=${SFX_GAIN},aresample=48000[s]`); labels.push("[s]"); n++; }
const sum = labels.length > 1 ? `amix=inputs=${labels.length}:normalize=0:duration=first,` : "";
parts.push(`${labels.join("")}${sum}alimiter=limit=0.89:level=false[o]`);
ff(["-y", ...inputs, "-filter_complex", parts.join(";"), "-map", "[o]", "-t", String(dur), "-ar", "48000", "-ac", "2", jobPath("stems/premix.wav")]);
// 0.5 dB of extra headroom: AAC encoding in render.mjs raises true peak by a few tenths
loudnorm(jobPath("stems/premix.wav"), jobPath("mix.wav"), { ac: 2, TP: config.audio.truePeak - 0.5 });
fs.rmSync(jobPath("stems/premix.wav"));
ff(["-y", "-i", jobPath("mix.wav"), "-c:a", "aac", "-b:a", "160k", jobPath("mix.m4a")]);

// 4. Report by measurement (you cannot listen, so numbers are the check).
const v = loudness(jobPath("narration.wav")), f = loudness(jobPath("mix.wav"));
const m = fs.existsSync(jobPath("stems/music.wav")) ? loudness(jobPath("stems/music.wav")) : null;
const s = fs.existsSync(jobPath("stems/sfx.wav")) ? loudness(jobPath("stems/sfx.wav")) : null;
console.log(`voice   ${v.I} LUFS (mono, reads ~3 LU lower than in the stereo mix)`);
if (m) console.log(`music   ${m.I} LUFS integrated after ducking (${mm.provider}${mm.model ? " " + mm.model : ""})`);
if (s) console.log(`sfx     ${s.I} LUFS integrated, gain ${SFX_GAIN}`);
console.log(`mix     ${f.I} LUFS, true peak ${f.TP} dBTP, LRA ${f.LRA} LU  → mix.wav, mix.m4a`);
if (Math.abs(f.I - target) > 1) console.log(`warn: mix is ${f.I} LUFS, target ${target}`);
if (f.TP > config.audio.truePeak + 0.5) console.log(`warn: true peak ${f.TP} dBTP above ${config.audio.truePeak}`);
console.log("next: node build.mjs (embeds the mix in the HTML player), then node render.mjs");
