// Copy the finished video and its sources into the user's output folder, with a README.
// Usage: node deliver.mjs --to <output-dir> [--name my-video]
// Writes: <name>.mp4, index.html (self-contained player), captions.srt/.vtt, README.md, source/
// README sections marked TODO are for you to fill (what each scene shows, known limitations).
import fs from "node:fs";
import path from "node:path";
import { args, config, jobPath, readJson, ledger, die, SCRIPTS_DIR } from "./lib/config.mjs";

const a = args();
const to = a.to ?? config.outputDir;
if (!to) die("give --to <output-dir> (or set EXPLAINER_OUTPUT_DIR); ask the user where the video should go");
if (!fs.existsSync(jobPath("video.mp4"))) die("missing video.mp4: run render.mjs and verify.mjs first");
const brief = readJson("brief.json", {});
const slug = (a.name ?? brief.title ?? "explainer").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") || "explainer";
fs.mkdirSync(path.join(to, "source"), { recursive: true });

const copy = (from, dest) => { if (fs.existsSync(jobPath(from))) { fs.copyFileSync(jobPath(from), path.join(to, dest)); return true; } return false; };
copy("video.mp4", `${slug}.mp4`);
copy("out.html", "index.html");
copy("captions.srt", `${slug}.srt`);
copy("captions.vtt", `${slug}.vtt`);
for (const f of ["brief.json", "facts.md", "storyboard.json", "storyboard.html", "REVIEW.md", "lines.json", "cues.json", "timeline.json", "assets.json", "music.json", "fonts.json", "scenes.js"]) copy(f, `source/${f}`);

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
| Language | ${brief.language ?? config.language} |

## Script

| # | Time | Line | Scene |
|---|---|---|---|
${cues.map(c => `| ${c.i} | ${fmt(c.start)} | ${c.text.replace(/\|/g, "\\|")} | TODO |`).join("\n")}

## How it was made

- Narration: ${vo[0]?.provider ?? "?"}${vo[0]?.provider === "openrouter" ? ` \`${(lines.voice && lines.voice.model) || config.tts.model}\`` : ""}, voice \`${(lines.voice && lines.voice.voice) || config.tts.voice}\`; word timings ${cues.some(c => c.timing === "estimated") ? "estimated from line length" : "from the TTS provider"}.
- Images: ${models.length ? models.map(m => `\`${m}\``).join(", ") : "none (all drawn in code)"} (${Object.keys(im).length} generated).
- Music: ${mm.provider === "openrouter" ? `\`${mm.model}\` (generated; carries a SynthID watermark)` : mm.provider === "file" ? "supplied track" : mm.provider === "synth" ? "synthesised in code" : "none"}.
- Animation: code-driven canvas (\`source/scenes.js\`), rendered frame by frame in headless Chromium, encoded with ffmpeg (H.264 + AAC, −16 LUFS).
- API spend: $${spent.toFixed(2)} of a $${l.budgetUsd ?? config.budgetUsd} budget${l.entries.some(e => e.estimated) ? " (some entries estimated)" : ""}.

## Known limitations

TODO: say what you could not verify (for example: audio checked by measurement only, sync of estimated word timings).

## Rebuild

The pipeline scripts live in the \`design-visual-explainer-video\` skill (\`${SCRIPTS_DIR.replace(/\\/g, "/")}\`). Copy \`source/\` into a job folder, then run \`tts.mjs\`, \`timeline.mjs\`, \`fonts.mjs\`, \`images.mjs\`, \`music.mjs\`, \`build.mjs\`, \`mix.mjs\`, \`build.mjs\`, \`render.mjs\` from that folder. Cached voice and image files are not included, so a rebuild regenerates them (and costs again).
`;
fs.writeFileSync(path.join(to, "README.md"), readme);
console.log(`delivered to ${path.resolve(to)}: ${slug}.mp4, index.html, ${slug}.srt, README.md (fill the TODOs), source/`);
