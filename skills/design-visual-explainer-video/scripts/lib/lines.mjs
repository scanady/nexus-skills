// lines.json accepts either an array of strings or
// { "voice": { "style": "...", "voice": "...", "model": "..." }, "lines": [ { "text", "say"?, "pauseAfter"? } | "text" ] }
// "text" is what appears in captions and drives at(); "say" (optional) is a phonetic respelling sent to TTS.
import { readJson, die } from "./config.mjs";

export function loadLines(file = "lines.json") {
  const raw = readJson(file);
  const doc = Array.isArray(raw) ? { lines: raw } : raw;
  if (!Array.isArray(doc.lines) || !doc.lines.length) die(`${file} has no lines`);
  const lines = doc.lines.map((l, i) => {
    const o = typeof l === "string" ? { text: l } : l;
    if (!o.text || typeof o.text !== "string") die(`${file} line ${i} has no text`);
    return o;
  });
  return { voice: doc.voice ?? {}, lines };
}

// Everything the narration says, lowercased, to look up brief.json terms.
export const spokenText = lines => lines.map(l => `${l.text} ${l.say ?? ""}`).join(" ").toLowerCase();
