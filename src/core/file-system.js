const fs = require('fs');
const path = require('path');

// Local build and OS litter that should never ship inside an installed skill.
const SKIPPED_ENTRIES = new Set(['__pycache__', '.DS_Store', 'node_modules', '.pytest_cache']);

function isSkipped(name) {
  return SKIPPED_ENTRIES.has(name) || name.endsWith('.pyc');
}

/** Relative paths of every file under dir, skipping build and OS litter. */
function listFiles(dir, prefix = '') {
  const files = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (isSkipped(entry.name)) continue;
    const relative = prefix ? path.join(prefix, entry.name) : entry.name;
    if (entry.isDirectory()) {
      files.push(...listFiles(path.join(dir, entry.name), relative));
    } else {
      files.push(relative);
    }
  }
  return files;
}

// The user's environment files, kept across upgrades wherever they sit in a skill.
// Everything else, including .env.example, is replaced by the source copy.
const KEPT_ENV_FILES = new Set(['.env', '.env.local']);

function isEnvFile(name) {
  return KEPT_ENV_FILES.has(name);
}

/**
 * Copy the user's .env and .env.local files from an installed copy (`from`) into the new copy
 * (`into`). Nothing else carries over. Never overwrites a file the source
 * provides. Returns the relative paths kept.
 */
function carryOverEnvFiles(from, into) {
  const kept = [];
  for (const relative of listFiles(from)) {
    if (!isEnvFile(path.basename(relative))) continue;
    const target = path.join(into, relative);
    if (fs.existsSync(target)) continue;
    try {
      fs.mkdirSync(path.dirname(target), { recursive: true });
      fs.copyFileSync(path.join(from, relative), target);
      kept.push(relative);
    } catch (error) {
      // The source has a file where this .env's folder would go. Fail this skill
      // so the installed copy stays as it was, rather than drop the .env.
      throw new Error(`cannot keep ${relative}: ${error.message}`);
    }
  }
  return kept;
}

/**
 * Delete a skill folder but leave its .env and .env.local files in place.
 * Folders emptied along the way are removed; the skill folder itself is
 * removed when nothing is kept. Returns the relative paths kept.
 */
function removeExceptEnvFiles(dir, prefix = '') {
  const kept = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    const relative = prefix ? path.join(prefix, entry.name) : entry.name;
    if (entry.isDirectory()) {
      kept.push(...removeExceptEnvFiles(full, relative));
    } else if (isEnvFile(entry.name)) {
      kept.push(relative);
    } else {
      fs.rmSync(full, { force: true });
    }
  }
  if (fs.readdirSync(dir).length === 0) {
    fs.rmdirSync(dir);
  }
  return kept;
}

function copyDir(src, dest) {
  fs.mkdirSync(dest, { recursive: true });
  const entries = fs.readdirSync(src, { withFileTypes: true });

  for (const entry of entries) {
    if (isSkipped(entry.name)) {
      continue;
    }

    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);

    if (entry.isDirectory()) {
      copyDir(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

module.exports = { carryOverEnvFiles, copyDir, isEnvFile, listFiles, removeExceptEnvFiles };
