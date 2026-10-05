const path = require('path');
const { withSkillSource } = require('../../sources/skill-source');
const { extractFrontmatter } = require('../../core/skills');
const { findEnvFiles, listInstalledSkills } = require('../../core/installed');
const { resolveTargets } = require('./install');

async function listAvailableSkills(options, source) {
  const listMode = options.listMode || 'full';
  const skills = await source.listSkills();

  if (listMode === 'count') {
    console.log(skills.length);
    return;
  }

  if (listMode === 'bare') {
    if (skills.length === 0) {
      console.log('  No skills found.\n');
      return;
    }

    skills.forEach(skill => console.log(skill));
    return;
  }

  console.log(`\n📦 Available skills (${source.label}):\n`);

  if (skills.length === 0) {
    console.log('  No skills found.\n');
    return;
  }

  for (const skill of skills) {
    const metadata = await source.getMetadata(skill);
    const description = metadata.description || 'No description';

    console.log(`  • ${skill}`);
    console.log(`    ${description}\n`);
  }

  console.log('Install all:     npx nxa install');
  console.log('Install one:     npx nxa install --skill ops-process-sop-creator\n');
}

/**
 * Print what is installed in each target. Marks skills the source does not
 * have (upgrade leaves those alone) and, in full mode, skills holding .env files.
 */
async function listInstalled(options, source) {
  const targets = resolveTargets(options);
  const available = new Set(await source.listSkills());
  const listMode = options.listMode || 'bare';

  for (const { labels, dir } of targets) {
    const skills = listInstalledSkills(dir);

    if (listMode === 'count') {
      console.log(targets.length > 1 ? `${skills.length}\t${dir}` : skills.length);
      continue;
    }

    if (listMode === 'bare') {
      if (targets.length > 1) console.log(`# ${dir}`);
      skills.forEach(skill => console.log(skill));
      continue;
    }

    console.log(`\n📂 ${labels.join(', ')} (${dir}): ${skills.length} installed\n`);
    if (skills.length === 0) {
      console.log('  No skills installed.');
      continue;
    }

    for (const skill of skills) {
      const notes = [];
      if (!available.has(skill)) notes.push(`not in ${source.label}`);
      const envFiles = findEnvFiles(path.join(dir, skill));
      if (envFiles.length > 0) notes.push(`has ${envFiles.join(', ')}`);

      const description = extractFrontmatter(path.join(dir, skill, 'SKILL.md')).description || 'No description';
      console.log(`  • ${skill}${notes.length ? `  [${notes.join('; ')}]` : ''}`);
      console.log(`    ${description}\n`);
    }
  }

  if (listMode === 'full') console.log('');
}

async function listSkills(options = {}) {
  await withSkillSource(options, source => (options.installed
    ? listInstalled(options, source)
    : listAvailableSkills(options, source)));
}

module.exports = { listSkills };
