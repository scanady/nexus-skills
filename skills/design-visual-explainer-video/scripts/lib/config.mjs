// Shared configuration, .env loading, ffmpeg helpers and the spend ledger.
// Precedence for every setting: real environment variable > <job dir>/.env > <skill dir>/.env > default.
import fs from "node:fs";
import path from "node:path";
import { execFileSync, spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";

export const SCRIPTS_DIR = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
export const SKILL_ROOT = path.resolve(SCRIPTS_DIR, "..");
export const ASSETS_DIR = path.join(SKILL_ROOT, "assets");
export const JOB = process.cwd();
const require = createRequire(path.join(SCRIPTS_DIR, "package.json"));

// One-line errors instead of stack traces, and no forced exit while network handles are open
// (process.exit during an open fetch trips a libuv assertion on Windows).
export class Stop extends Error {}
const fail = e => {
  if (!(e instanceof Stop)) { console.error(`error: ${e?.message ?? e}`); if (process.env.EXPLAINER_DEBUG) console.error(e?.stack); }
  if (process.exitCode === undefined) process.exitCode = 1;
  setTimeout(() => process.exit(), 2000).unref(); // only fires if something (a browser) keeps the process alive
};
process.on("uncaughtException", fail);
process.on("unhandledRejection", fail);

function parseEnvFile(file) {
  const out = {};
  if (!fs.existsSync(file)) return out;
  for (const raw of fs.readFileSync(file, "utf8").split(/\r?\n/)) {
    const line = raw.trim();
    if (!line || line.startsWith("#")) continue;
    const m = line.match(/^(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$/);
    if (!m) continue;
    let v = m[2].trim();
    if ((v.startsWith('"') && v.endsWith('"')) || (v.startsWith("'") && v.endsWith("'"))) v = v.slice(1, -1);
    else v = v.replace(/\s+#.*$/, "");
    out[m[1]] = v;
  }
  return out;
}

export const ENV_FILES = [path.join(JOB, ".env"), path.join(SKILL_ROOT, ".env")].filter((f, i, a) => a.indexOf(f) === i);
const fileEnv = Object.assign({}, ...ENV_FILES.slice().reverse().map(parseEnvFile));
export function env(name, fallback = undefined) {
  const v = process.env[name] ?? fileEnv[name];
  return v === undefined || v === "" ? fallback : v;
}
const num = (name, fallback) => { const v = Number(env(name, fallback)); return Number.isFinite(v) ? v : fallback; };

export const config = {
  openrouter: {
    apiKey: env("OPENROUTER_API_KEY"),
    baseUrl: env("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1").replace(/\/+$/, ""),
    referer: env("OPENROUTER_HTTP_REFERER", "https://github.com/scanady/nexus-skills"),
    title: env("OPENROUTER_APP_TITLE", "nexus explainer video skill"),
  },
  budgetUsd: num("EXPLAINER_BUDGET_USD", 10),
  image: {
    model: env("EXPLAINER_IMAGE_MODEL", "google/gemini-3.1-flash-image"),
    fallbackModel: env("EXPLAINER_IMAGE_FALLBACK_MODEL", "google/gemini-2.5-flash-image"),
    resolution: env("EXPLAINER_IMAGE_RESOLUTION", "1K"),
    concurrency: num("EXPLAINER_IMAGE_CONCURRENCY", 3),
  },
  tts: {
    provider: env("EXPLAINER_TTS_PROVIDER", "openrouter"),
    model: env("EXPLAINER_TTS_MODEL", "google/gemini-3.8-flash-tts"),
    voice: env("EXPLAINER_TTS_VOICE", "Charon"),
    style: env("EXPLAINER_TTS_STYLE"),
    speed: num("EXPLAINER_TTS_SPEED", 1),
  },
  music: {
    provider: env("EXPLAINER_MUSIC_PROVIDER", "openrouter"),
    model: env("EXPLAINER_MUSIC_MODEL", "google/lyria-3-pro-preview"),
    file: env("EXPLAINER_MUSIC_FILE"),
  },
  elevenlabs: { apiKey: env("ELEVENLABS_API_KEY"), voiceId: env("ELEVENLABS_VOICE_ID"), model: env("ELEVENLABS_MODEL", "eleven_multilingual_v2") },
  video: {
    width: num("EXPLAINER_WIDTH", 1920),
    height: num("EXPLAINER_HEIGHT", 1080),
    fps: num("EXPLAINER_FPS", 30),
    crf: num("EXPLAINER_CRF", 20),
    maxrate: env("EXPLAINER_MAXRATE", "8M"),
    workers: num("EXPLAINER_RENDER_WORKERS", 0),
  },
  audio: {
    lufs: num("EXPLAINER_TARGET_LUFS", -16),
    truePeak: num("EXPLAINER_TRUE_PEAK", -1.5),
    musicUnderVoiceDb: num("EXPLAINER_MUSIC_UNDER_VOICE_DB", 16),
    sfxGain: num("EXPLAINER_SFX_GAIN", 0.8),
  },
  language: env("EXPLAINER_LANGUAGE", "en"),
  chromePath: env("EXPLAINER_CHROME_PATH"),
  ffmpegPath: env("EXPLAINER_FFMPEG_PATH"),
  outputDir: env("EXPLAINER_OUTPUT_DIR"),
};

// ---------- files ----------
export const jobPath = (...p) => path.join(JOB, ...p);
export function readJson(file, fallback) {
  const f = path.isAbsolute(file) ? file : jobPath(file);
  if (!fs.existsSync(f)) { if (fallback !== undefined) return fallback; die(`missing ${path.relative(JOB, f) || f}`); }
  try { return JSON.parse(fs.readFileSync(f, "utf8")); } catch (e) { die(`${f} is not valid JSON: ${e.message}`); }
}
export function writeJson(file, data) { fs.writeFileSync(jobPath(file), JSON.stringify(data, null, 2)); }
// Print, set the exit code, and unwind. Catch blocks must rethrow Stop (see isStop).
export function die(msg, code = 1) { if (!quiet) console.error(`error: ${msg}`); process.exitCode = code; throw new Stop(msg); }
// doctor.mjs catches die() to build its table, so it turns off the direct print.
let quiet = false;
export function setQuiet(v) { quiet = v; }
export const isStop = e => e instanceof Stop;
// End a script early with success (keeps the exit code, avoids process.exit).
export function done() { process.exitCode = 0; throw new Stop("done"); }

// ---------- ffmpeg ----------
export function ffmpegBin() {
  if (config.ffmpegPath) return config.ffmpegPath;
  try { const p = require("ffmpeg-static"); if (p && fs.existsSync(p)) return p; } catch {}
  const probe = spawnSync("ffmpeg", ["-version"], { encoding: "utf8" });
  if (probe.status === 0) return "ffmpeg";
  die("ffmpeg not found: run `npm install` in the skill's scripts/ folder, or set EXPLAINER_FFMPEG_PATH");
}
// Run ffmpeg and return stderr (ffmpeg prints analysis there). Throws on failure.
export function ff(args, { quiet = true } = {}) {
  const r = spawnSync(ffmpegBin(), quiet ? ["-hide_banner", ...args] : args, { encoding: "utf8", maxBuffer: 1 << 28 });
  if (r.status !== 0) throw new Error(`ffmpeg ${args.join(" ")}\n${(r.stderr || "").split("\n").slice(-15).join("\n")}`);
  return r.stderr || "";
}
export function mediaDuration(file) {
  const r = spawnSync(ffmpegBin(), ["-hide_banner", "-i", file], { encoding: "utf8" });
  const m = (r.stderr || "").match(/Duration: (\d+):(\d+):([\d.]+)/);
  if (!m) throw new Error(`cannot read duration of ${file}`);
  return +m[1] * 3600 + +m[2] * 60 + +m[3];
}
// Two-pass linear loudnorm: measure, then apply. Single-pass loudnorm pumps on short clips.
export function loudnorm(input, output, { I = config.audio.lufs, TP = config.audio.truePeak, LRA = 11, ar = 48000, ac } = {}) {
  const meas = ff(["-i", input, "-af", `loudnorm=I=${I}:TP=${TP}:LRA=${LRA}:print_format=json`, "-f", "null", "-"]);
  const j = JSON.parse(meas.slice(meas.lastIndexOf("{"), meas.lastIndexOf("}") + 1));
  const f = `loudnorm=I=${I}:TP=${TP}:LRA=${LRA}:measured_I=${j.input_i}:measured_TP=${j.input_tp}:measured_LRA=${j.input_lra}:measured_thresh=${j.input_thresh}:offset=${j.target_offset}:linear=true`;
  ff(["-y", "-i", input, "-af", f, "-ar", String(ar), ...(ac ? ["-ac", String(ac)] : []), output]);
}
export function loudness(file) {
  const out = ff(["-nostats", "-i", file, "-af", "ebur128=peak=true", "-f", "null", "-"]);
  const tail = out.slice(out.lastIndexOf("Summary:"));
  const g = re => { const m = tail.match(re); return m ? +m[1] : NaN; };
  return { I: g(/I:\s+(-?[\d.]+) LUFS/), LRA: g(/LRA:\s+(-?[\d.]+) LU/), TP: g(/Peak:\s+(-?[\d.]+) dBFS/) };
}

// ---------- spend ledger (enforces EXPLAINER_BUDGET_USD across every paid call in this job) ----------
const LEDGER = () => jobPath("spend.json");
export function ledger() { return readJson(LEDGER(), { budgetUsd: config.budgetUsd, entries: [] }); }
export function spent() { return ledger().entries.reduce((s, e) => s + (e.cost || 0), 0); }
export function assertBudget(estimate = 0) {
  const s = spent();
  if (s + estimate > config.budgetUsd) {
    die(`budget stop: spent $${s.toFixed(3)} of $${config.budgetUsd} (EXPLAINER_BUDGET_USD); next call estimated at $${estimate.toFixed(3)}. Raise the budget only if the user agrees.`, 3);
  }
}
export function record(entry) {
  const l = ledger();
  l.budgetUsd = config.budgetUsd;
  l.entries.push({ at: new Date().toISOString(), ...entry });
  fs.writeFileSync(LEDGER(), JSON.stringify(l, null, 2));
  return l.entries.reduce((s, e) => s + (e.cost || 0), 0);
}

// ---------- misc ----------
export function hash(...parts) {
  let h = 2166136261 >>> 0;
  const s = parts.map(p => (typeof p === "string" ? p : JSON.stringify(p))).join("\u0001");
  for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); }
  return (h >>> 0).toString(16).padStart(8, "0");
}
export async function pool(items, n, fn) {
  const out = new Array(items.length); let i = 0;
  await Promise.all([...Array(Math.max(1, Math.min(n, items.length)))].map(async () => {
    while (i < items.length) { const k = i++; out[k] = await fn(items[k], k); }
  }));
  return out;
}
export function args(argv = process.argv.slice(2)) {
  const o = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith("--")) { const [k, v] = a.slice(2).split("="); o[k] = v ?? (argv[i + 1] && !argv[i + 1].startsWith("--") ? argv[++i] : true); }
    else o._.push(a);
  }
  return o;
}
export function which(cmd) { try { execFileSync(process.platform === "win32" ? "where" : "which", [cmd], { stdio: "ignore" }); return true; } catch { return false; } }
