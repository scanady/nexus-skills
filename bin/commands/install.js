const fs = require('fs');
const path = require('path');
const {
  getSupportedAgents,
  getTargetGroups
} = require('../skills-core');
const { withSkillSource } = require('../skill-service');
const { resolvePackSkills } = require('../packs');
const { listSkills } = require('./list');

function confirm(question) {
  process.stdout.write(`${question} [y/N] `);
  let input = '';
  const buffer = Buffer.alloc(1);

  while (true) {
    const bytesRead = fs.readSync(0, buffer, 0, 1);
    if (bytesRead === 0) {
      break;
    }

    const character = buffer.toString();
    if (character === '\n') {
      break;
    }

    input += character;
  }

  return input.trim().toLowerCase() === 'y';
}

function resolveSkillsToInstall(selectedSkills, availableSkills) {
  return {
    skillsToInstall: selectedSkills.length > 0
      ? selectedSkills.filter(skill => availableSkills.includes(skill))
      : availableSkills,
    invalidSkills: selectedSkills.filter(skill => !availableSkills.includes(skill))
  };
}

function collectExistingSkills(targets, skillsToInstall, fsImpl = fs, pathImpl = path) {
  const existingSkills = new Set();

  for (const { dir } of targets) {
    for (const skill of skillsToInstall) {
      if (fsImpl.existsSync(pathImpl.join(dir, skill))) {
        existingSkills.add(skill);
      }
    }
  }

  return existingSkills;
}

async function installSkills(options = {}) {
  await withSkillSource(options, async source => {
    const availableSkills = await source.listSkills();

    if (options.packs && options.packs.length > 0) {
      const packSkills = resolvePackSkills(options.packs, availableSkills);
      options.skills = [...new Set([...(options.skills || []), ...packSkills])];
    }

    const selectedSkills = options.skills || [];
    const { skillsToInstall, invalidSkills } = resolveSkillsToInstall(selectedSkills, availableSkills);

    if (invalidSkills.length > 0) {
      console.log(`\n⚠️  Unknown skills: ${invalidSkills.join(', ')}`);
      console.log(`   Available: ${availableSkills.join(', ')}\n`);
    }

    if (skillsToInstall.length === 0) {
      console.log('\n❌ No valid skills to install.\n');
      await listSkills({ ...options, listMode: 'full' });
      return;
    }

    const { targets, invalid } = getTargetGroups(options.agents, options.global);
    if (invalid.length > 0) {
      console.log(`\n⚠️  Unknown agent(s): ${invalid.join(', ')}`);
      console.log(`   Available: ${getSupportedAgents().join(', ')}\n`);
    }

    if (targets.length === 0) {
      console.log('\n❌ No valid agents to install to.\n');
      return;
    }

    if (options.upgrade && !options.overwrite) {
      const existingSkills = collectExistingSkills(targets, skillsToInstall);

      if (existingSkills.size > 0) {
        console.log('\n⚠️  The following skills will be deleted and replaced:');
        [...existingSkills].forEach(skill => console.log(`   • ${skill}`));
        if (!confirm('\nProceed with upgrade?')) {
          console.log('\n❌ Upgrade cancelled.\n');
          return;
        }
      }
    }

    const scope = options.global ? 'global' : 'project';
    const action = options.upgrade ? 'Upgrading' : 'Installing';
    console.log(`\n🚀 ${action} nexus-agents (${scope}, source: ${source.label})...\n`);

    let totalInstalled = 0;
    let totalUpgraded = 0;
    let totalSkipped = 0;

    for (const { labels, dir } of targets) {
      fs.mkdirSync(dir, { recursive: true });
      console.log(`${labels.join(', ')} (${dir}):`);

      for (const skill of skillsToInstall) {
        const destination = path.join(dir, skill);
        const exists = fs.existsSync(destination);

        if (exists && !options.upgrade) {
          console.log(`  ⏭  ${skill} (already installed)`);
          totalSkipped++;
          continue;
        }

        try {
          if (exists) {
            fs.rmSync(destination, { recursive: true, force: true });
          }

          await source.installSkill(skill, destination);
          if (exists) {
            console.log(`  🔄 ${skill}`);
            totalUpgraded++;
          } else {
            console.log(`  ✅ ${skill}`);
            totalInstalled++;
          }
        } catch (error) {
          console.log(`  ❌ ${skill} - ${error.message}`);
        }
      }

      console.log('');
    }

    console.log('✨ Done!\n');
    const parts = [];
    if (totalInstalled > 0) {
      parts.push(`${totalInstalled} installed`);
    }
    if (totalUpgraded > 0) {
      parts.push(`${totalUpgraded} upgraded`);
    }
    if (totalSkipped > 0) {
      parts.push(`${totalSkipped} skipped`);
    }
    if (parts.length > 0) {
      console.log(`   ${parts.join(', ')}`);
    }
  });
}

module.exports = {
  collectExistingSkills,
  installSkills,
  resolveSkillsToInstall
};
