// Speech check and measured word times: Whisper listens to each voice clip, locally and for free.
// Usage: node align.mjs   (after tts.mjs, before timeline.mjs)
// Out:   vo/raw/<hash>.align.json for each clip: spoken-word times, match rate, and the words it did not hear.
//        Results are cached per clip. tts.mjs deletes a clip's result when it voices the clip again.
// timeline.mjs uses these times unless the provider gave exact ones.
// Exit 0, also when a line needs a look (printed as "check"); 8 = could not run, so times stay estimated.
import "./lib/job.mjs";
import fs from "node:fs";
import { config, die, jobPath, mediaDuration, readJson, writeJson } from "./lib/config.mjs";
import { loadLines } from "./lib/lines.mjs";
import { alignFile, alignWords, canCheckSpeech, splitWords } from "./lib/align.mjs";

const CHECK_BELOW = 0.8;
const { lines } = loadLines();
const manifest = readJson("vo/manifest.json");
if (manifest.length !== lines.length) die(`vo/manifest.json has ${manifest.length} clips but lines.json has ${lines.length} lines: re-run tts.mjs`);
const language = readJson("brief.json", {}).language ?? config.language;
if (!canCheckSpeech(language)) die(`align.mjs matches words by spaces, so it cannot check "${language}". Word times stay estimated. Run timeline.mjs.`, 8);

let listen = null;
for (const [i, line] of lines.entries()) {
  const clip = manifest[i];
  if (clip.provider === "silent") { console.log(`line ${i}: silent clip, nothing to hear`); continue; }
  const side = alignFile(clip.file);
  if (!fs.existsSync(jobPath(side))) {
    if (!listen) {
      try { const { loadWhisper } = await import("./lib/whisper.mjs"); listen = await loadWhisper(language); }
      catch (e) { die(`speech check unavailable (${e.message.split("\n")[0]}). Word times stay estimated. Install with \`npm install\` in the skill's scripts/ folder, allow huggingface.co for the first run, then run align.mjs again. Otherwise run timeline.mjs.`, 8); }
    }
    const file = jobPath(clip.file);
    const heard = await listen(file);
    const words = splitWords(line.say ?? line.text);
    const r = alignWords(words, heard, mediaDuration(file), language);
    writeJson(side, { words: r.words, matchRate: +r.matchRate.toFixed(3), missed: r.words.filter(w => !w.heard).map(w => w.w), heard: heard.map(h => h.text).join(" ") });
  }
  const { matchRate, missed, heard } = readJson(side);
  const pct = `${Math.round(matchRate * 100)}% heard`;
  if (matchRate < CHECK_BELOW) console.log(`check line ${i}: ${pct}; not heard: ${missed.map(w => `"${w}"`).join(", ")}; it heard: "${heard}"`);
  else console.log(`line ${i}: ${pct}${missed.length ? `; not heard: ${missed.map(w => `"${w}"`).join(", ")}` : ""}`);
}
console.log("Next: node timeline.mjs");
