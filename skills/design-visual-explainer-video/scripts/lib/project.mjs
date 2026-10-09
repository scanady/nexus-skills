// The shared project folder (references/project-folder.md): <parent>/<project>/ with project.json, README.md,
// shared/, and one folder per output. This skill owns one output folder (default "video") and its entry,
// its README section, and what it adds to shared/. JSON is edited read → change → write, keeping unknown keys.
import fs from "node:fs";
import path from "node:path";
import { die } from "./config.mjs";

export const SKILL = "design-visual-explainer-video";
export const KIND = "explainer-video";
export const DEFAULT_DIR = "video";

export const today = () => new Date().toISOString().slice(0, 10);
export const rel = (root, f) => path.relative(root, f).split(path.sep).join("/");

export function readJsonFile(file, fallback) {
  if (!fs.existsSync(file)) return fallback;
  try { return JSON.parse(fs.readFileSync(file, "utf8")); } catch (e) { die(`${file} is not valid JSON: ${e.message}`); }
}
export const writeJsonFile = (file, data) => fs.writeFileSync(file, JSON.stringify(data, null, 2) + "\n");

// Read project.json, let `change` edit it in place, write it back. Returns the edited object.
export function updateProject(root, change) {
  const file = path.join(root, "project.json");
  const p = readJsonFile(file);
  if (!p) die(`missing ${file}`);
  if (!Array.isArray(p.outputs)) p.outputs = [];
  change(p);
  writeJsonFile(file, p);
  return p;
}

// Change only this skill's entry (keyed by dir); add it when missing.
export function upsertOutput(root, dir, fields) {
  return updateProject(root, p => {
    let o = p.outputs.find(x => x.dir === dir);
    if (!o) { o = { dir, skill: SKILL, kind: KIND, entry: null, status: "in-progress" }; p.outputs.push(o); }
    Object.assign(o, fields, { updated: today() });
  });
}

// The video file stem: the project name for "video", <project>-<suffix> for "video-<suffix>" (or <project>-<dir>).
export const stemFor = (project, dir) => dir === DEFAULT_DIR ? project : `${project}-${dir.replace(/^video-/, "")}`;

// Replace the text between <!-- output:<dir> --> markers, or add the section at the end.
export function setReadmeSection(root, dir, body) {
  const file = path.join(root, "README.md");
  const open = `<!-- output:${dir} -->`, close = `<!-- /output:${dir} -->`;
  const block = `${open}\n${body.trim()}\n${close}`;
  let md = fs.existsSync(file) ? fs.readFileSync(file, "utf8") : "";
  const a = md.indexOf(open), b = md.indexOf(close, a);
  if (a >= 0 && b > a) md = md.slice(0, a) + block + md.slice(b + close.length);
  else md = (md.trimEnd() ? md.trimEnd() + "\n\n" : "") + block + "\n";
  fs.writeFileSync(file, md);
}

// "- claim — source" lines (the contract's facts.md form).
export const factLines = text => text.split(/\r?\n/).map(l => l.trim()).filter(l => /^-\s+\S/.test(l));

// Append lines not already in shared/facts.md. Returns how many were added.
export function appendFacts(root, lines) {
  const file = path.join(root, "shared", "facts.md");
  const old = fs.existsSync(file) ? fs.readFileSync(file, "utf8") : "";
  const have = new Set(factLines(old));
  const add = [...new Set(lines)].filter(l => !have.has(l));
  if (add.length) fs.writeFileSync(file, (old.trimEnd() ? old.trimEnd() + "\n" : "") + add.join("\n") + "\n");
  return add.length;
}

// PNG width and height from the IHDR chunk; null for anything else.
export function pngSize(file) {
  const b = Buffer.alloc(24), fd = fs.openSync(file, "r");
  try { fs.readSync(fd, b, 0, 24, 0); } finally { fs.closeSync(fd); }
  return b.readUInt32BE(0) === 0x89504e47 && b.toString("ascii", 12, 16) === "IHDR" ? { width: b.readUInt32BE(16), height: b.readUInt32BE(20) } : null;
}

// Copy a file into shared/images/ under `name`, with an assets.json entry. A name already used by a file this
// skill did not add gets -2, -3, … instead; a file this skill added under that name is replaced.
export function addSharedImage(root, src, name, entry) {
  const dirAbs = path.join(root, "shared", "images");
  fs.mkdirSync(dirAbs, { recursive: true });
  const indexFile = path.join(root, "shared", "assets.json");
  const index = readJsonFile(indexFile, { schema: 1, assets: [] });
  if (!Array.isArray(index.assets)) index.assets = [];
  const ext = path.extname(name), base = name.slice(0, -ext.length);
  let file, own;
  for (let n = 1; ; n++) {
    file = `shared/images/${n === 1 ? base : `${base}-${n}`}${ext}`;
    own = index.assets.find(x => x.file === file);
    if (own ? own.by === SKILL : !fs.existsSync(path.join(root, file))) break;
  }
  fs.copyFileSync(src, path.join(root, file));
  const fields = { file, by: SKILL, ...entry };
  if (own) Object.assign(own, fields); else index.assets.push(fields);
  writeJsonFile(indexFile, index);
  return file;
}
