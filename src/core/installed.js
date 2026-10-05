const fs = require('fs');
const path = require('path');
const { isEnvFile, listFiles } = require('./file-system');

/** Skill folders (with a SKILL.md) already present in a target directory. */
function listInstalledSkills(dir, fsImpl = fs) {
  try {
    return fsImpl.readdirSync(dir, { withFileTypes: true })
      .filter(entry => entry.isDirectory() && !entry.name.startsWith('.'))
      .map(entry => entry.name)
      .filter(name => fsImpl.existsSync(path.join(dir, name, 'SKILL.md')))
      .sort();
  } catch (error) {
    if (error.code === 'ENOENT') return [];
    throw error;
  }
}

/** Relative paths of the .env and .env.local files inside one installed skill. */
function findEnvFiles(skillDir) {
  return listFiles(skillDir).filter(relative => isEnvFile(path.basename(relative)));
}

module.exports = { findEnvFiles, listInstalledSkills };
