// Local speech recognition: Whisper on the CPU through Transformers.js. Free, no API key.
// The first run downloads the model from Hugging Face into ~/.cache/nexus-explainer-video/models.
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { ffmpegBin } from "./config.mjs";

// Returns listen(file) → [{text, start, end}]. Throws when the package or the model is not available.
export async function loadWhisper(language) {
  const { env, pipeline } = await import("@huggingface/transformers");
  env.cacheDir = path.join(os.homedir(), ".cache", "nexus-explainer-video", "models");
  const en = language.toLowerCase().startsWith("en");
  const asr = await pipeline("automatic-speech-recognition", en ? "onnx-community/whisper-base.en_timestamped" : "onnx-community/whisper-small_timestamped", { dtype: "q8" });
  return async file => {
    const r = spawnSync(ffmpegBin(), ["-v", "error", "-i", file, "-map", "0:a:0", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], { maxBuffer: 1 << 30 });
    if (r.status !== 0) throw new Error(`ffmpeg cannot read the audio of ${file}: ${String(r.stderr).slice(-300)}`);
    const pcm = new Float32Array(r.stdout.buffer.slice(r.stdout.byteOffset, r.stdout.byteOffset + r.stdout.length));
    const out = await asr(pcm, { return_timestamps: "word", chunk_length_s: 30, stride_length_s: 5, ...(en ? {} : { language, task: "transcribe" }) });
    return (out.chunks ?? []).map(c => ({ text: c.text.trim(), start: c.timestamp[0] ?? 0, end: c.timestamp[1] ?? c.timestamp[0] ?? 0 }));
  };
}
