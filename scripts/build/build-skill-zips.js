#!/usr/bin/env node
/*
 * build-skill-zips.js
 *
 * Packages every source skill under skills/ into an individual zip archive.
 *
 * Outputs:
 *   dist/skills/<skill>.zip                  -> per-skill downloadable bundles
 *
 * Usage:
 *   node scripts/build/build-skill-zips.js
 */

const childProcess = require('child_process');
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..', '..');
const SKILLS_DIR = path.join(ROOT, 'skills');
const DIST_SKILLS_DIR = path.join(ROOT, 'dist', 'skills');

function rmDir(dir) {
  if (fs.existsSync(dir)) fs.rmSync(dir, { recursive: true, force: true });
}

function listSkills() {
  return fs.readdirSync(SKILLS_DIR)
    .filter(name => {
      const skillPath = path.join(SKILLS_DIR, name);
      return fs.statSync(skillPath).isDirectory() && fs.existsSync(path.join(skillPath, 'SKILL.md'));
    })
    .sort();
}

function zipSkillDirectory(sourceDir, outZip) {
  if (process.platform === 'win32') {
    const psCmd = `Compress-Archive -Path '${sourceDir}\\*' -DestinationPath '${outZip}' -Force`;
    childProcess.execSync(`powershell -NoProfile -Command "${psCmd}"`, { stdio: 'inherit' });
  } else {
    const parent = path.dirname(sourceDir);
    const base = path.basename(sourceDir);
    childProcess.execSync(`cd "${parent}" && zip -rq "${outZip}" "${base}" -x '*/.DS_Store' '*/Thumbs.db' '*/__MACOSX/*'`, { stdio: 'inherit' });
  }
}

function main() {
  const skills = listSkills();

  rmDir(DIST_SKILLS_DIR);
  fs.mkdirSync(DIST_SKILLS_DIR, { recursive: true });

  for (const skill of skills) {
    zipSkillDirectory(path.join(SKILLS_DIR, skill), path.join(DIST_SKILLS_DIR, `${skill}.zip`));
  }

  console.log(`Built ${skills.length} skill zips in ${path.relative(ROOT, DIST_SKILLS_DIR)}/`);
}

if (require.main === module) {
  try {
    main();
  } catch (err) {
    console.error(`ERROR: ${err.message}`);
    process.exit(1);
  }
}

module.exports = { main };