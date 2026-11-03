// Build the pack a fresh reviewer reads: what a stranger gets from the video, and nothing about how it was made.
// Usage: node review-pack.mjs   (after verify.mjs; hand review-pack/ to a new agent with references/reviewer-brief.md)
// Writes review-pack/ (replaced on every run):
//   PACK.md              audience, goal, spoken words with times, sound measurements, what each image holds
//   facts.md             the sourced claims, so the reviewer can check truth
//   hook.jpg             first 3 s, one frame every 0.5 s, at phone width
//   phone-NN.jpg         one frame per second at phone width
//   beats-NN.jpg         one frame per narration line, 9 per sheet
//   full-<t>.jpg         every third line's frame at full size
//   strip-<t>.jpg        12 frames across each scene change
//   line-NN.jpg          8 frames across each narration line, for the moves inside a scene
// Never add storyboard.json, scenes.js, the chat, or an earlier review: they anchor the reviewer.
import "./lib/job.mjs";
import fs from "node:fs";
import { ff, jobPath, readJson, die } from "./lib/config.mjs";
import { launch, openPage } from "./lib/browser.mjs";

const verify = readJson("verify.json", null);
if (!verify) die("missing verify.json: run verify.mjs first");
const video = jobPath(verify.file);
if (!fs.existsSync(video)) die(`missing ${verify.file}: render it, or run review-pack.mjs before deliver.mjs moves it`);
const cues = readJson("cues.json"), brief = readJson("brief.json", {});
const { dur, fps } = readJson("timeline.json");
const browser = await launch();
const { meta } = await openPage(browser);
await browser.close();

const pack = jobPath("review-pack");
fs.rmSync(pack, { recursive: true, force: true });
fs.mkdirSync(pack);
const to = f => `review-pack/${f}`;
for (const f of fs.readdirSync(jobPath("shots"))) if (f === "hook.jpg" || /^phone-\d+\.jpg$/.test(f)) fs.copyFileSync(jobPath("shots", f), jobPath(to(f)));
if (fs.existsSync(jobPath("facts.md"))) fs.copyFileSync(jobPath("facts.md"), jobPath(to("facts.md")));

// One frame near the end of each line, when its picture is complete.
const beats = cues.map(c => +Math.min(c.start + c.dur * 0.8, dur - 0.05).toFixed(2));
const pick = beats.map(t => `eq(n\\,${Math.round(t * fps)})`).join("+");
ff(["-y", "-i", video, "-vf", `select='${pick}',scale=640:-2,tile=3x3:padding=4:color=black`, "-vsync", "vfr", "-q:v", "3", jobPath(to("beats-%02d.jpg"))]);
beats.forEach((t, k) => { if (k % 3 === 0) ff(["-y", "-ss", String(t), "-i", video, "-frames:v", "1", "-q:v", "2", jobPath(to(`full-${t}.jpg`))]); });

// 12 frames from just before each scene starts until its transition has finished.
const changes = meta.scenes.slice(1).map(s => +s.start.toFixed(2));
for (const t of changes) ff(["-y", "-ss", String(Math.max(0, t - 0.2)), "-t", "1.2", "-i", video, "-vf", "fps=10,scale=480:-2,tile=4x3:padding=3:color=black", "-frames:v", "1", "-q:v", "3", jobPath(to(`strip-${t}.jpg`))]);

// 8 frames across each line. Read 1/8 longer than the line, so the last tile is never cut.
cues.forEach((c, k) => {
  const len = Math.max(c.dur, 0.5);
  ff(["-y", "-ss", String(c.start), "-t", (len * 9 / 8).toFixed(2), "-i", video, "-vf", `fps=${(8 / len).toFixed(4)},scale=480:-2,tile=4x2:padding=3:color=black`, "-frames:v", "1", "-q:v", "3", jobPath(to(`line-${String(k + 1).padStart(2, "0")}.jpg`))]);
});

const clock = s => `${Math.floor(s / 60)}:${(s % 60).toFixed(1).padStart(4, "0")}`;
const list = rows => rows.map(r => `- ${r}`).join("\n") || "- none";
fs.writeFileSync(jobPath(to("PACK.md")), `# Video under review

Length ${clock(dur)}. ${meta.width}×${meta.height} at ${fps} fps. Language: ${brief.language ?? "?"}.

Audience: ${brief.audience || "not stated"}
What it must do: ${brief.goal || "not stated"}
Call to action: ${brief.cta || "none"}
Words this audience searches for: ${(brief.terms ?? []).join(", ") || "not stated"}

## Words spoken, with times

${cues.map(c => `- ${clock(c.start)}  ${c.text}`).join("\n")}

## Sound, as measured (you cannot hear it)

${list(verify.notes.filter(n => /^(audio|loudness|speech check)/.test(n)))}

## Problems the measurements found

${list([...verify.problems.map(p => `FAIL: ${p}`), ...verify.warnings.map(w => `warning: ${w}`)])}

## Files

A phone shows this video about 360 px wide. \`hook.jpg\` and \`phone-NN.jpg\` use that width, so judge text size from them.

- \`hook.jpg\`: 0–3 s, one frame every 0.5 s, at phone width. Judge it as a muted viewer.
- \`phone-NN.jpg\`: one frame per second at phone width. Each sheet holds 40 s.
- \`line-NN.jpg\`: 8 frames across narration line NN, in the order of the words spoken above. Judge the moves inside a scene from these.
- \`beats-NN.jpg\`: one frame per narration line, 9 per sheet, at these times in order: ${beats.join(", ")}
- \`full-<time>.jpg\`: full-size frames.
- \`strip-<time>.jpg\`: 12 frames, 0.1 s apart, across the scene changes at ${changes.join(", ") || "none"}.
${fs.existsSync(jobPath("facts.md")) ? "- `facts.md`: the sourced claims. Each claim in the video must be in it." : "- There is no `facts.md`: mark truth as unverifiable."}
`);
console.log(`review-pack/: ${fs.readdirSync(pack).length} files. Hand it to a new agent with the brief in references/reviewer-brief.md`);
