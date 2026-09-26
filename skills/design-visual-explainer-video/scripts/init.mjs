// Create a job folder: the working directory every other script runs in.
// Usage: node <skill>/scripts/init.mjs <job-dir> [--example]
//   --example  copy the three-line "why is the sky blue" example (lines.json, assets.json, scenes.js)
import fs from "node:fs";
import path from "node:path";
import { ASSETS_DIR, SCRIPTS_DIR, args, die } from "./lib/config.mjs";

const a = args();
const dir = a._[0];
if (!dir) die("usage: node init.mjs <job-dir> [--example]");
fs.mkdirSync(dir, { recursive: true });
const put = (name, content) => { const f = path.join(dir, name); if (fs.existsSync(f)) console.log(`keep  ${name}`); else { fs.writeFileSync(f, content); console.log(`wrote ${name}`); } };

if (a.example) for (const f of ["lines.json", "assets.json", "storyboard.json", "scenes.js"]) put(f, fs.readFileSync(path.join(ASSETS_DIR, "example", f), "utf8"));
else {
  put("lines.json", JSON.stringify({ voice: { style: "Warm, clear, curious. Explaining to a smart friend." }, lines: [{ text: "First line of narration." }] }, null, 2) + "\n");
  put("assets.json", JSON.stringify({ style: "", images: [] }, null, 2) + "\n");
  put("storyboard.json", JSON.stringify({
    design: { summary: "", palette: {}, fonts: [], motion: "", voice: "", music: "" },
    scenes: [{ name: "hook", title: "", chapter: "", lines: [0], visual: "", onScreen: [], motion: "", assets: [] }],
    questions: [],
  }, null, 2) + "\n");
}
put("brief.json", JSON.stringify({ title: "", seed: "", audience: "", goal: "", language: "en", lengthSec: 60, style: "", cta: "", sources: [] }, null, 2) + "\n");
put(".gitignore", ["vo/", "assets/raw/", "stems/", "render/", "shots/", "music/", "fonts/", "*.wav", "*.mp3", "*.m4a", "draft.mp4", "narration.*", "storyboard-audio/", "spend.json", ".env", ""].join("\n"));
console.log(`\njob ready: ${path.resolve(dir)}\nrun every script from inside it, e.g.\n  cd "${path.resolve(dir)}"\n  node "${path.join(SCRIPTS_DIR, "doctor.mjs")}"`);
