const { withSkillSource } = require('../skill-service');

async function listSkills(options = {}) {
  await withSkillSource(options, async source => {
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

    console.log('Install all:     npx nyld-nexus-skills install');
    console.log('Install one:     npx nyld-nexus-skills install --skill ops-process-sop-creator\n');
  });
}

module.exports = { listSkills };
