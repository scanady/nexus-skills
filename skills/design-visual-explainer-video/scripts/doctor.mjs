// Preflight: checks Node, dependencies, browser, ffmpeg, .env settings, and the OpenRouter key's credit limit.
// Usage (from the job folder or anywhere): node <skill>/scripts/doctor.mjs [--offline]
// Exit 0 = ready; 2 = blocking problem (the message says what to fix).
import fs from "node:fs";
import path from "node:path";
import { args, config, ENV_FILES, SCRIPTS_DIR, ffmpegBin, ff, setQuiet } from "./lib/config.mjs";

const a = args();
setQuiet(true);
const rows = [], block = [];
const ok = (k, v) => rows.push(["ok  ", k, v]);
const warn = (k, v) => rows.push(["warn", k, v]);
const bad = (k, v) => { rows.push(["FAIL", k, v]); block.push(k); };

const [maj, min] = process.versions.node.split(".").map(Number);
maj > 20 || (maj === 20 && min >= 10) ? ok("node", process.versions.node) : bad("node", `${process.versions.node}: need 20.10+`);

if (!fs.existsSync(path.join(SCRIPTS_DIR, "node_modules"))) bad("npm deps", `run: cd "${SCRIPTS_DIR}" && npm install`);
else ok("npm deps", "installed");

try { const v = ff(["-version"], { quiet: false }).split("\n")[0] || "found"; ok("ffmpeg", ffmpegBin() === "ffmpeg" ? "system ffmpeg" : "ffmpeg-static"); void v; }
catch (e) { bad("ffmpeg", e.message.split("\n")[0]); }

try {
  const { launch } = await import("./lib/browser.mjs");
  const b = await launch(); ok("browser", `${b.browserType().name()} ${b.version()}`); await b.close();
} catch (e) { bad("browser", e.message.split("\n")[0]); }

const found = ENV_FILES.filter(f => fs.existsSync(f));
found.length ? ok(".env", found.join(", ")) : warn(".env", `none found (looked in ${ENV_FILES.join(", ")}); using process env only`);

const needsOR = [config.tts.provider === "openrouter", config.music.provider === "openrouter", true /* images */].some(Boolean);
if (!config.openrouter.apiKey) (needsOR ? bad : warn)("OPENROUTER_API_KEY", "not set (images, default TTS and music use it)");
else {
  ok("OPENROUTER_API_KEY", `set (…${config.openrouter.apiKey.slice(-4)})`);
  if (!a.offline) {
    try {
      const { keyInfo } = await import("./lib/openrouter.mjs");
      const k = await keyInfo();
      if (k.limit === null || k.limit === undefined) warn("key credit limit", `none: set a limit on this key in the OpenRouter dashboard (e.g. $${config.budgetUsd}) as a hard stop`);
      else ok("key credit limit", `$${k.limit} (remaining $${(+k.limit_remaining).toFixed(2)})`);
      if (k.limit_remaining !== null && k.limit_remaining !== undefined && k.limit_remaining < 1) bad("key credit", `only $${k.limit_remaining} left`);
    } catch (e) { (/ 401/.test(e.message) ? bad : warn)("key check", / 401/.test(e.message) ? "OpenRouter rejected the key (401): check OPENROUTER_API_KEY" : e.message.slice(0, 120)); }
  }
}
ok("budget", `$${config.budgetUsd} per job (EXPLAINER_BUDGET_USD)`);
ok("image model", `${config.image.model} (fallback ${config.image.fallbackModel}), ${config.image.resolution}`);
const t = config.tts;
if (t.provider === "elevenlabs" && !(config.elevenlabs.apiKey && config.elevenlabs.voiceId)) bad("tts", "elevenlabs needs ELEVENLABS_API_KEY and ELEVENLABS_VOICE_ID");
else if (t.provider === "edge") {
  try { await import("msedge-tts"); warn("tts", "edge: free but UNOFFICIAL endpoint; may rate-limit or break"); } catch { bad("tts", "edge needs `npm install msedge-tts` in scripts/"); }
} else ok("tts", `${t.provider}${t.provider === "openrouter" ? ` ${t.model} voice ${t.voice}` : ""}`);
const m = config.music;
if (m.provider === "file" && !(m.file && fs.existsSync(m.file))) bad("music", "EXPLAINER_MUSIC_FILE missing");
else ok("music", `${m.provider}${m.provider === "openrouter" ? ` ${m.model}` : ""}`);
ok("video", `${config.video.width}x${config.video.height} @ ${config.video.fps} fps, crf ${config.video.crf}, maxrate ${config.video.maxrate}`);
if (config.outputDir) ok("output dir", `${config.outputDir} (default --in for init.mjs)`); else warn("output dir", "EXPLAINER_OUTPUT_DIR not set: ask the user which parent folder holds the project folder");

const w = Math.max(...rows.map(r => r[1].length));
for (const [s, k, v] of rows) console.log(`${s}  ${k.padEnd(w)}  ${v}`);
if (block.length) { console.log(`\nblocked by: ${block.join(", ")}. See getting-started.md.`); process.exitCode = 2; }
else console.log("\nready");
