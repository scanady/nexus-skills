const fs = require('fs');
const path = require('path');
const { PROJECT_ROOT } = require('./skills');

function resolvePackSkills(packNames, availableSkills) {
  const packsDir = path.join(PROJECT_ROOT, 'packs');
  const resolved = new Set();

  for (const packName of packNames) {
    const packFile = path.join(packsDir, `${packName}.json`);

    if (!fs.existsSync(packFile)) {
      console.log(`  ⚠️  Pack not found: ${packName}`);
      continue;
    }

    let pack;
    try {
      pack = JSON.parse(fs.readFileSync(packFile, 'utf8'));
    } catch (error) {
      console.log(`  ⚠️  Failed to read pack ${packName}: ${error.message}`);
      continue;
    }

    for (const pattern of pack.skills || []) {
      if (pattern.endsWith('*')) {
        const prefix = pattern.slice(0, -1);
        availableSkills
          .filter(skill => skill.startsWith(prefix))
          .forEach(skill => resolved.add(skill));
        continue;
      }

      if (availableSkills.includes(pattern)) {
        resolved.add(pattern);
      }
    }
  }

  return [...resolved];
}

module.exports = { resolvePackSkills };