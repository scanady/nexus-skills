const { withSkillSource } = require('../../sources/skill-source');
const { CliError } = require('../errors');
const { listInstalledSkills } = require('../../core/installed');
const {
  confirm,
  resolveSelection,
  resolveTargets,
  writePlan
} = require('./install');

/**
 * Decide what to upgrade in each target. Only skills already installed there
 * are touched; nothing new is added. Installed skills the source does not have
 * are reported and left alone.
 */
function planUpgrade(targets, installedByDir, availableSkills, selection) {
  const plan = [];
  const notInSource = new Set();
  const notInstalled = new Set(selection.explicit);

  for (const target of targets) {
    const installed = installedByDir.get(target.dir) || [];
    installed.filter(skill => !availableSkills.includes(skill)).forEach(skill => notInSource.add(skill));

    const candidates = installed.filter(skill => availableSkills.includes(skill));
    const skills = selection.selected
      ? candidates.filter(skill => selection.skills.includes(skill))
      : candidates;

    skills.forEach(skill => notInstalled.delete(skill));
    plan.push({ ...target, skills });
  }

  return { plan, notInSource: [...notInSource].sort(), notInstalled: [...notInstalled].sort() };
}

async function upgradeSkills(options = {}) {
  await withSkillSource(options, async source => {
    const availableSkills = await source.listSkills();
    if (availableSkills.length === 0) {
      throw new CliError(`No skills found in ${source.label}.`);
    }

    const selection = resolveSelection(options, availableSkills);
    const targets = resolveTargets(options);
    const installedByDir = new Map(targets.map(target => [target.dir, listInstalledSkills(target.dir)]));
    const { plan, notInSource, notInstalled } = planUpgrade(targets, installedByDir, availableSkills, selection);

    if (notInstalled.length > 0) {
      throw new CliError(`Not installed in ${targets.map(t => t.dir).join(', ')}: ${notInstalled.join(', ')}.\n   Use "nxa install --skill <name>" to add a skill.`);
    }

    const scope = options.global ? 'global' : 'project';
    const total = plan.reduce((sum, target) => sum + target.skills.length, 0);

    if (notInSource.length > 0) {
      console.log(`\nℹ️  Left unchanged, not in ${source.label}: ${notInSource.join(', ')}`);
    }

    if (total === 0) {
      console.log(`\nNothing to upgrade in ${targets.map(t => t.dir).join(', ')} (${scope}).\n`);
      return;
    }

    if (!options.overwrite) {
      console.log('\n⚠️  The following installed skills will be replaced with the source version.');
      console.log('   Your .env and .env.local files are kept. Every other file is replaced:');
      for (const { dir, skills } of plan) {
        if (skills.length === 0) continue;
        console.log(`   ${dir}`);
        skills.forEach(skill => console.log(`     • ${skill}`));
      }
      if (!confirm('\nProceed with upgrade?')) {
        console.log('\nUpgrade cancelled. Nothing changed.\n');
        return;
      }
    }

    console.log(`\n🚀 Upgrading ${total} installed skill(s) (${scope}, source: ${source.label})...\n`);
    await writePlan(source, plan.filter(target => target.skills.length > 0), { replace: true });
  });
}

module.exports = { planUpgrade, upgradeSkills };
