// Finish this video's output folder in the project (references/project-folder.md), then publish to shared/.
// Usage (from <project>/<dir>/work, the job folder init.mjs made): node deliver.mjs
// Writes to <project>/<dir>/: <stem>.mp4 (moved from work/video.mp4), index.html (self-contained player),
// <stem>.srt/.vtt, README.md. <stem> is the project name for dir "video", <project>-<suffix> for "video-<suffix>".
// Updates this output's entry in project.json and its section in the project README.
// Publishes to shared/: new facts.md lines → facts.md; the look → brand.json (only when it does not exist yet);
// generated images → images/<stem>-<id>.png with assets.json entries. Sources and caches stay in work/.
// README sections marked TODO are for you to fill (what each scene shows, known limitations).
import fs from "node:fs";
import path from "node:path";
import { JOB, config, jobPath, readJson, ledger, die, SCRIPTS_DIR } from "./lib/config.mjs";
import { SKILL, addSharedImage, appendFacts, factLines, pngSize, readJsonFile, setReadmeSection, stemFor, upsertOutput, writeJsonFile } from "./lib/project.mjs";

const to = path.dirname(JOB), root = path.dirname(to), outDir = path.basename(to);
const project = path.basename(JOB) === "work" ? readJsonFile(path.join(root, "project.json")) : null;
if (!project) die(`run deliver.mjs from <project>/<dir>/work (the job folder init.mjs made), not ${JOB}`);
const own = (project.outputs ?? []).find(o => o.dir === outDir);
if (own?.skill !== SKILL) die(`project.json does not list "${outDir}/" for ${SKILL}: run init.mjs for this project first`);
const slug = stemFor(project.name || path.basename(root), outDir);
const video = path.join(to, `${slug}.mp4`);
// Move, not copy: one copy of the MP4 in the output folder. A re-render writes work/video.mp4 again; deliver again to replace it.
if (fs.existsSync(jobPath("video.mp4"))) fs.renameSync(jobPath("video.mp4"), video);
else if (!fs.existsSync(video)) die("missing work/video.mp4: run render.mjs and verify.mjs first");
const brief = readJson("brief.json", {});

const copy = (from, dest) => { if (fs.existsSync(jobPath(from))) fs.copyFileSync(jobPath(from), path.join(to, dest)); };
copy("out.html", "index.html");
copy("captions.srt", `${slug}.srt`);
copy("captions.vtt", `${slug}.vtt`);

const cues = readJson("cues.json");
const { dur } = readJson("timeline.json");
const mm = readJson("music/manifest.json", {});
const im = readJson("assets/manifest.json", {});
const vo = readJson("vo/manifest.json", []);
const l = ledger(), spent = l.entries.reduce((s, e) => s + (e.cost || 0), 0);
const fmt = s => `${Math.floor(s / 60)}:${(s % 60).toFixed(1).padStart(4, "0")}`;
const models = [...new Set(Object.values(im).map(x => x.model))];
const lines = readJson("lines.json");

const readme = `# ${brief.title || slug}

${brief.goal ? brief.goal + "\n\n" : ""}| | |
|---|---|
| Video | \`${slug}.mp4\` (${fmt(dur)}, ${config.video.width}×${config.video.height} @ ${config.video.fps} fps, captions embedded) |
| Player | \`index.html\`: self-contained, works offline, open it in any browser |
| Captions | \`${slug}.srt\`, \`${slug}.vtt\` |
| Storyboard | \`work/storyboard.html\` (approved plan), \`work/REVIEW.md\` |
| Sources | \`work/\`: script, facts, storyboard, scenes, cached voice and art |
| Project | \`../README.md\`: the other outputs; \`../shared/\`: brief, facts, brand, images |
| Language | ${brief.language ?? config.language} |

## Script

| # | Time | Line | Scene |
|---|---|---|---|
${cues.map(c => `| ${c.i} | ${fmt(c.start)} | ${c.text.replace(/\|/g, "\\|")} | TODO |`).join("\n")}

## How it was made

- Narration: ${vo[0]?.provider ?? "?"}${vo[0]?.provider === "openrouter" ? ` \`${(lines.voice && lines.voice.model) || config.tts.model}\`` : ""}, voice \`${(lines.voice && lines.voice.voice) || config.tts.voice}\`; word timings ${cues.some(c => c.timing === "estimated") ? "estimated from line length" : "from the TTS provider"}.
- Images: ${models.length ? models.map(m => `\`${m}\``).join(", ") : "none (all drawn in code)"} (${Object.keys(im).length} generated).
- Music: ${mm.provider === "openrouter" ? `\`${mm.model}\` (generated; carries a SynthID watermark)` : mm.provider === "file" ? "supplied track" : mm.provider === "synth" ? "synthesised in code" : "none"}.
- Animation: code-driven canvas (\`work/scenes.js\`), rendered frame by frame in headless Chromium, encoded with ffmpeg (H.264 + AAC, −16 LUFS).
- API spend: $${spent.toFixed(2)} of a $${l.budgetUsd ?? config.budgetUsd} budget${l.entries.some(e => e.estimated) ? " (some entries estimated)" : ""}.

## Known limitations

TODO: say what you could not verify (for example: audio checked by measurement only, sync of estimated word timings).

## Rebuild

The pipeline scripts live in the \`design-visual-explainer-video\` skill (\`${SCRIPTS_DIR.replace(/\\/g, "/")}\`). Edit the files in \`work/\`, then run \`tts.mjs\`, \`timeline.mjs\`, \`fonts.mjs\`, \`images.mjs\`, \`music.mjs\`, \`build.mjs\`, \`mix.mjs\`, \`build.mjs\`, \`render.mjs\`, \`verify.mjs\`, \`deliver.mjs\` from inside \`work/\`. Cached voice and image files are kept there, so only changed lines and images cost again.
`;
fs.writeFileSync(path.join(to, "README.md"), readme);

// Project manifest and README section.
const entry = `${outDir}/${slug}.mp4`;
upsertOutput(root, outDir, { entry, status: "delivered" });
const mmss = s => `${Math.floor(Math.round(s) / 60)}:${String(Math.round(s) % 60).padStart(2, "0")}`;
setReadmeSection(root, outDir, `## Explainer video${outDir === "video" ? "" : ` (${outDir})`}
\`${entry}\` (${mmss(dur)}), player \`${outDir}/index.html\`. Details: \`${outDir}/README.md\`.`);

// Publish to shared/. Never secrets, ledgers, or caches.
const shared = path.join(root, "shared");
fs.mkdirSync(shared, { recursive: true });
const published = [];
const newFacts = fs.existsSync(jobPath("facts.md")) ? appendFacts(root, factLines(fs.readFileSync(jobPath("facts.md"), "utf8"))) : 0;
if (newFacts) published.push(`facts.md (+${newFacts} lines)`);

// brand.json: the first output to settle a look writes it; later runs leave it alone.
if (!fs.existsSync(path.join(shared, "brand.json"))) {
  const design = readJson("storyboard.json", {}).design ?? {}, theme = design.theme ?? {};
  const palette = { ...(design.palette ?? {}) };
  for (const [k, v] of [["background", theme.light], ["text", theme.ink], ["accent", theme.accent]]) if (v && !palette[k]) palette[k] = v;
  const fams = new Map();
  for (const f of readJson("fonts.json", [])) {
    const w = Number(f.weight);
    if (!fams.has(f.family)) fams.set(f.family, new Set());
    fams.get(f.family).add(Number.isFinite(w) ? w : f.weight);
  }
  const fonts = [...fams].map(([family, ws]) => ({ family, weights: [...ws].sort((x, y) => (+x || 0) - (+y || 0)), role: family === theme.display ? "heading" : "body" }));
  if (Object.keys(palette).length || fonts.length) {
    writeJsonFile(path.join(shared, "brand.json"), { ...(Object.keys(palette).length ? { palette } : {}), ...(fonts.length ? { fonts } : {}) });
    published.push("brand.json");
  }
}

// Generated images (not assets/extra/, which came from elsewhere). Green-keyed and transparent ones have alpha.
const prompts = new Map((readJson("assets.json", { images: [] }).images ?? []).map(x => [x.id, x]));
for (const [id, m] of Object.entries(im)) {
  const src = jobPath("assets", `${id}.png`);
  if (!fs.existsSync(src)) continue;
  const img = prompts.get(id) ?? {};
  const file = addSharedImage(root, src, `${slug}-${id.toLowerCase().replace(/[^a-z0-9]+/g, "-")}.png`, {
    kind: "generated", source: img.prompt ?? "", ...(pngSize(src) ?? {}), text: Boolean(img.allowText),
    background: ["green", "transparent"].includes(m.background) ? "transparent" : "opaque", rights: "generated",
    note: `Image "${id}" from ${entry}${m.model ? `, ${m.model}` : ""}`,
  });
  published.push(file.replace(/^shared\//, ""));
}

console.log(`delivered to ${to}: ${slug}.mp4, index.html, ${slug}.srt, ${slug}.vtt, README.md (fill the TODOs); sources stay in work/`);
console.log(`project.json: ${outDir} → ${entry}, delivered; README section updated`);
console.log(published.length ? `shared/: ${published.join(", ")}` : "shared/: nothing new");
