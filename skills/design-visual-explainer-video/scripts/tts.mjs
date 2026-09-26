// Narration: one TTS call per line, cached by content hash so edits only re-voice changed lines.
// Usage: node tts.mjs [--provider openrouter|elevenlabs|edge|silent] [--voice X] [--model Y] [--only 3,5]
//        node tts.mjs --sample "Text to audition" --voice Puck   (writes vo/sample-<voice>.mp3, one paid call)
// Out:   vo/raw/<hash>.<ext>, vo/manifest.json [{i, file, words?}]  → then run timeline.mjs
// Providers:
//   openrouter  POST /audio/speech (default model google/gemini-3.8-flash-tts). No word timings: timeline.mjs estimates them.
//   elevenlabs  /v1/text-to-speech/{voice}/with-timestamps: exact word timings. Needs ELEVENLABS_API_KEY + ELEVENLABS_VOICE_ID.
//   edge        Microsoft Edge read-aloud voices via msedge-tts: free, exact word timings, UNOFFICIAL endpoint (can break).
//   silent      Silent clips with estimated length: free animatic timing before any paid voice.
import fs from "node:fs";
import path from "node:path";
import { args, config, env, ff, hash, jobPath, writeJson, die, done, record, assertBudget } from "./lib/config.mjs";
import { loadLines } from "./lib/lines.mjs";
import { speech } from "./lib/openrouter.mjs";

const a = args();
const { voice: voiceDoc, lines } = loadLines();
const provider = a.provider ?? voiceDoc.provider ?? config.tts.provider;
const model = a.model ?? voiceDoc.model ?? (provider === "elevenlabs" ? config.elevenlabs.model : config.tts.model);
const voice = a.voice ?? voiceDoc.voice ?? (provider === "elevenlabs" ? config.elevenlabs.voiceId : provider === "edge" ? "en-US-AndrewMultilingualNeural" : config.tts.voice);
const style = a.style ?? voiceDoc.style ?? config.tts.style;
const speed = +(a.speed ?? voiceDoc.speed ?? config.tts.speed);
const only = a.only ? new Set(String(a.only).split(",").map(Number)) : null;
fs.mkdirSync(jobPath("vo/raw"), { recursive: true });

async function synth(text, id) {
  if (provider === "openrouter") {
    // Gemini TTS returns only headerless PCM (16-bit mono; 24 kHz unless the content type says otherwise).
    const r = await speech({ model, text, voice, style, speed, format: /^google\//.test(model) ? "pcm" : "mp3", id });
    const note = `$${r.cost.toFixed(4)} ${r.contentType}`;
    const head = r.buffer.subarray(0, 4).toString("latin1");
    if (head === "RIFF") return { buffer: r.buffer, ext: "wav", note };
    if (r.format !== "pcm") return { buffer: r.buffer, ext: "mp3", note };
    const rate = +(r.contentType.match(/rate=(\d+)/)?.[1] ?? env("EXPLAINER_TTS_PCM_RATE", 24000));
    const raw = jobPath("vo/raw", `${id}.pcm`), wav = jobPath("vo/raw", `${id}.tmp.wav`);
    fs.writeFileSync(raw, r.buffer);
    ff(["-y", "-f", "s16le", "-ar", String(rate), "-ac", "1", "-i", raw, wav]);
    const buffer = fs.readFileSync(wav); fs.rmSync(raw); fs.rmSync(wav);
    // Sanity check: a wrong sample rate makes speech far too slow or too fast.
    const wpm = text.split(/\s+/).filter(Boolean).length / (r.buffer.length / 2 / rate) * 60;
    if (wpm < 80 || wpm > 260) console.log(`warn: clip reads at ${Math.round(wpm)} wpm; the PCM sample rate (${rate}) may be wrong: set EXPLAINER_TTS_PCM_RATE`);
    return { buffer, ext: "wav", note };
  }
  if (provider === "elevenlabs") {
    const { apiKey } = config.elevenlabs;
    if (!apiKey || !voice) die("elevenlabs needs ELEVENLABS_API_KEY and ELEVENLABS_VOICE_ID (or --voice)", 2);
    assertBudget(0.05);
    const res = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${encodeURIComponent(voice)}/with-timestamps?output_format=mp3_44100_128`, {
      method: "POST", headers: { "xi-api-key": apiKey, "Content-Type": "application/json" },
      body: JSON.stringify({ text, model_id: model, voice_settings: { stability: 0.45, similarity_boost: 0.8, style: 0.2, speed, use_speaker_boost: true } }),
    });
    if (!res.ok) throw new Error(`ElevenLabs ${res.status}: ${(await res.text()).slice(0, 400)}`);
    const j = await res.json();
    const al = j.alignment ?? j.normalized_alignment, words = [];
    let cur = null;
    al.characters.forEach((ch, k) => {
      if (/\s/.test(ch)) { if (cur) words.push(cur); cur = null; return; }
      if (!cur) cur = { w: "", t: al.character_start_times_seconds[k] };
      cur.w += ch;
    });
    if (cur) words.push(cur);
    // ElevenLabs bills by character on your plan, not in USD per call: record an estimate so the ledger shows it.
    record({ kind: "tts", model: `elevenlabs/${model}`, id, cost: text.length * 0.00018, estimated: true });
    return { buffer: Buffer.from(j.audio_base64, "base64"), ext: "mp3", words };
  }
  if (provider === "edge") {
    let MsEdgeTTS, OUTPUT_FORMAT;
    try { ({ MsEdgeTTS, OUTPUT_FORMAT } = await import("msedge-tts")); } catch { die("edge provider needs the optional msedge-tts package: npm install msedge-tts (in scripts/)"); }
    const dir = jobPath("vo/edge", id); fs.mkdirSync(dir, { recursive: true });
    for (let attempt = 1; ; attempt++) {
      const tts = new MsEdgeTTS();
      try {
        await tts.setMetadata(voice, OUTPUT_FORMAT.AUDIO_24KHZ_96KBITRATE_MONO_MP3, { wordBoundaryEnabled: true });
        const rate = speed === 1 ? "+0%" : `${speed > 1 ? "+" : ""}${Math.round((speed - 1) * 100)}%`;
        const r = await tts.toFile(dir, text, { rate });
        const meta = JSON.parse(fs.readFileSync(r.metadataFilePath, "utf8"));
        const words = (meta.Metadata ?? []).filter(x => x.Type === "WordBoundary").map(x => ({ w: x.Data.text.Text, t: x.Data.Offset / 1e7 }));
        return { buffer: fs.readFileSync(r.audioFilePath), ext: "mp3", words };
      } catch (e) { if (attempt >= 3) throw new Error(`edge TTS failed (unofficial endpoint): ${e.message}`); }
      finally { try { tts.close(); } catch {} }
    }
  }
  if (provider === "silent") {
    const n = text.split(/\s+/).filter(Boolean).length;
    const dur = n / (2.6 * speed) + 0.25; // ≈156 wpm
    const tmp = jobPath("vo/raw", `${id}.tmp.wav`);
    ff(["-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=mono", "-t", dur.toFixed(2), tmp]);
    const buffer = fs.readFileSync(tmp); fs.rmSync(tmp);
    return { buffer, ext: "wav" };
  }
  die(`unknown TTS provider "${provider}" (openrouter | elevenlabs | edge | silent)`);
}

if (a.sample) {
  const r = await synth(String(a.sample), `sample-${voice}`);
  const f = jobPath("vo", `sample-${String(voice).replace(/[^\w-]/g, "_")}.${r.ext}`);
  fs.writeFileSync(f, r.buffer);
  console.log(`wrote ${path.relative(jobPath(), f)} ${r.note ?? ""}`);
  done();
}

const prevManifest = fs.existsSync(jobPath("vo/manifest.json")) ? JSON.parse(fs.readFileSync(jobPath("vo/manifest.json"), "utf8")) : [];
const manifest = [];
for (const [i, line] of lines.entries()) {
  const spoken = line.say ?? line.text;
  const key = hash(provider, model, voice, style ?? "", speed, spoken);
  const cached = ["mp3", "wav"].map(e => `vo/raw/${key}.${e}`).find(f => fs.existsSync(jobPath(f)));
  const metaFile = jobPath(`vo/raw/${key}.json`);
  if (cached && (!only || !only.has(i))) {
    manifest.push({ i, file: cached, words: fs.existsSync(metaFile) ? JSON.parse(fs.readFileSync(metaFile, "utf8")) : undefined, provider });
    console.log(`line ${i}: cached`);
    continue;
  }
  if (only && !only.has(i) && prevManifest[i]) { manifest.push(prevManifest[i]); continue; }
  const r = await synth(spoken, key);
  const file = `vo/raw/${key}.${r.ext}`;
  fs.writeFileSync(jobPath(file), r.buffer);
  if (r.words) fs.writeFileSync(metaFile, JSON.stringify(r.words));
  manifest.push({ i, file, words: r.words, provider });
  console.log(`line ${i}: ${provider} ${voice} ${r.note ?? ""}`);
}
writeJson("vo/manifest.json", manifest);
console.log(`vo/manifest.json: ${manifest.length} clips. Next: node timeline.mjs`);
