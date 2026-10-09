// Join or create a project folder and set up this video's output in it (references/project-folder.md):
//   <parent>/<project>/project.json, README.md, shared/   the project (created when the folder does not exist)
//   <parent>/<project>/<dir>/                            deliverables, written later by deliver.mjs
//   <parent>/<project>/<dir>/work/                       the job folder: every other script runs in it
// Usage: node <skill>/scripts/init.mjs --in <parent-dir> --name <project> [--dir video] [--title "…"] [--example]
//   --in       where the project folder is or goes (default: EXPLAINER_OUTPUT_DIR)
//   --name     the project folder name, chosen by the user; it also names the video file
//   --dir      this video's output folder (default "video"); a second video in the same project needs its own,
//              e.g. video-vertical (file <project>-vertical.mp4)
//   --title    the human title for a new project.json (ignored when joining)
//   --example  copy the three-line "why is the sky blue" example (lines.json, assets.json, scenes.js)
// Joining: seeds work/facts.md from shared/facts.md and brief.json from project.json and shared/brief.md,
// and lists the other shared files to read. It copies no images; pick them yourself.
import fs from "node:fs";
import path from "node:path";
import { ASSETS_DIR, SCRIPTS_DIR, args, config, die } from "./lib/config.mjs";
import { DEFAULT_DIR, SKILL, readJsonFile, setReadmeSection, today, upsertOutput, writeJsonFile } from "./lib/project.mjs";

const a = args();
const parent = typeof a.in === "string" ? a.in : config.outputDir;
const name = typeof a.name === "string" ? a.name.trim() : "";
const outDir = typeof a.dir === "string" ? a.dir.trim() : DEFAULT_DIR;
if (!parent || !name) die("usage: node init.mjs --in <parent-dir> --name <project> [--dir video] [--title \"…\"] [--example]; ask the user where the project goes and what to name it (EXPLAINER_OUTPUT_DIR sets a default --in)");
if (/[\\/]/.test(name) || name === "." || name === "..") die(`--name must be one folder name, not a path: "${name}"`);
if (!/^[a-z0-9][a-z0-9-]*$/.test(outDir) || ["shared", "work"].includes(outDir)) die(`--dir must be one lowercase folder name such as video or video-vertical, not "${outDir}"`);

const root = path.resolve(parent, name);
const manifest = path.join(root, "project.json");

// Join or create the project.
if (fs.existsSync(manifest)) {
  const p = readJsonFile(manifest);
  console.log(`join  project ${root}`);
  if ((p.schema ?? 1) > 1) console.log(`note: project.json has schema ${p.schema}; it was made by a newer version. Unknown fields are kept; tell the user.`);
} else if (fs.existsSync(root) && fs.readdirSync(root).length) {
  die(`${root} exists, is not empty, and has no project.json. Ask the user: pick another --name, or empty the folder. Never adopt a folder this skill did not create.`);
} else {
  const title = typeof a.title === "string" ? a.title.trim() : "";
  fs.mkdirSync(path.join(root, "shared"), { recursive: true });
  writeJsonFile(manifest, { schema: 1, name, title, outputs: [] });
  fs.writeFileSync(path.join(root, "README.md"), `# ${title || name}\n`);
  console.log(`new   project ${root}`);
}
fs.mkdirSync(path.join(root, "shared"), { recursive: true });

// Claim the output folder.
const project = readJsonFile(manifest);
const mine = (project.outputs ?? []).find(o => o.dir === outDir);
if (mine && mine.skill !== SKILL) die(`project.json lists "${outDir}/" for ${mine.skill}. Ask the user for a suffix and pass --dir video-<suffix>.`);
if (!mine && fs.existsSync(path.join(root, outDir))) die(`${path.join(root, outDir)} exists but project.json does not list it. It is not this video's folder: ask the user for a suffix and pass --dir video-<suffix>.`);
if (mine) console.log(`keep  output ${outDir}/ (${mine.status ?? "?"}). A second video in this project needs --dir video-<suffix>.`);
upsertOutput(root, outDir, mine ? {} : { skill: SKILL, kind: "explainer-video", entry: null, status: "in-progress" });
if (!mine) setReadmeSection(root, outDir, `## Explainer video${outDir === DEFAULT_DIR ? "" : ` (${outDir})`}\nIn progress (${today()}).`);

const dir = path.join(root, outDir, "work");
fs.mkdirSync(dir, { recursive: true });
const put = (file, content) => { const f = path.join(dir, file); if (fs.existsSync(f)) console.log(`keep  ${file}`); else { fs.writeFileSync(f, content); console.log(`wrote ${file}`); } };
const shared = f => path.join(root, "shared", f);

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

// brief.json: title and seed from project.json; audience, goal, and call to action from shared/brief.md
// when that section is a single paragraph. Anything longer stays in brief.md for you to read.
const section = (md, h) => { const m = md.match(new RegExp(`^## ${h}\\s*\\n([\\s\\S]*?)(?=^## |(?![\\s\\S]))`, "m")); const t = m?.[1].trim() ?? ""; return t && !t.includes("\n\n") ? t.replace(/\s*\n\s*/g, " ") : ""; };
const briefMd = fs.existsSync(shared("brief.md")) ? fs.readFileSync(shared("brief.md"), "utf8") : "";
put("brief.json", JSON.stringify({
  title: project.title ?? "", seed: name, audience: section(briefMd, "Audience"), goal: section(briefMd, "Goal"),
  language: "en", lengthSec: 60, style: "", cta: section(briefMd, "Call to action"), sources: [],
}, null, 2) + "\n");
// facts.md: start from the project's facts; deliver.mjs adds the new lines back to shared/facts.md.
if (fs.existsSync(shared("facts.md"))) put("facts.md", fs.readFileSync(shared("facts.md"), "utf8"));
put(".gitignore", ["vo/", "assets/raw/", "stems/", "render/", "shots/", "music/", "fonts/", "*.wav", "*.mp3", "*.m4a", "draft.mp4", "narration.*", "storyboard-audio/", "spend.json", ".env", ""].join("\n"));

const found = ["brief.md", "facts.md", "brand.json", "ui-map.md", "assets.json", "images/", "screenshots/"].filter(f => fs.existsSync(shared(f)));
const others = (project.outputs ?? []).filter(o => o.dir !== outDir && o.entry).map(o => `${o.entry} (${o.kind})`);
if (found.length) console.log(`\nshared/ has: ${found.join(", ")}. Read them before you research or generate anything.`);
if (others.length) console.log(`other outputs you may use: ${others.join(", ")}`);
console.log(`\nproject: ${root}\noutput: ${path.join(root, outDir)}\njob folder: ${dir}\nrun every script from the job folder, e.g.\n  cd "${dir}"\n  node "${path.join(SCRIPTS_DIR, "doctor.mjs")}"`);
