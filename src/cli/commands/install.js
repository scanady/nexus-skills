const fs = require('fs');
const path = require('path');
const {
  getSupportedAgents,
  getTargetGroups
} = require('../../core/skills');
const { withSkillSource } = require('../../sources/skill-source');
const { loadPluginPackage, resolvePluginSkills } = require('../../core/plugins');
const { CliError } = require('../errors');
const { carryOverEnvFiles } = require('../../core/file-system');

/** Ask a yes/no question. Enter alone gives `defaultYes`. */
function confirm(question, defaultYes = false) {
  if (!process.stdin.isTTY) {
    throw new CliError('Cannot ask for confirmation because input is not a terminal. Nothing changed.\n   Rerun with --yes (same as --overwrite) to take the default answers without prompting.');
  }

  process.stdout.write(`${question} ${defaultYes ? '[Y/n]' : '[y/N]'} `);
  let input = '';
  const buffer = Buffer.alloc(1);

  while (true) {
    let bytesRead;
    try {
      bytesRead = fs.readSync(0, buffer, 0, 1);
    } catch (error) {
      if (error.code === 'EAGAIN') continue;
      if (error.code === 'EOF') break;
      throw error;
    }
    if (bytesRead === 0) {
      break;
    }

    const character = buffer.toString();
    if (character === '\n') {
      break;
    }

    input += character;
  }

  const answer = input.trim().toLowerCase();
  return answer === '' ? defaultYes : answer === 'y' || answer === 'yes';
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
      if (fsImpl.existsSync(pathImpl.join(dir, skill, 'SKILL.md'))) {
        existingSkills.add(skill);
      }
    }
  }

  return existingSkills;
}

/**
 * Expand --skill and --plugin into one list of skill names.
 * Throws before anything is written if a name is unknown, so a typo never
 * turns into a partial install.
 */
function resolveSelection(options, availableSkills) {
  const plugins = options.plugins || [];
  const unknownPlugins = plugins.filter(name => !loadPluginPackage(name));
  if (unknownPlugins.length > 0) {
    throw new CliError(`Unknown plugin(s): ${unknownPlugins.join(', ')}.`);
  }

  const explicit = options.skills || [];
  const { invalidSkills } = resolveSkillsToInstall(explicit, availableSkills);
  if (invalidSkills.length > 0) {
    throw new CliError(`Unknown skill(s): ${invalidSkills.join(', ')}.\n   Run "nxa list" to see available skills.`);
  }

  const pluginSkills = plugins.length > 0 ? resolvePluginSkills(plugins, availableSkills) : [];
  if (plugins.length > 0 && pluginSkills.length === 0) {
    throw new CliError(`Plugin(s) ${plugins.join(', ')} match no available skills.`);
  }

  return {
    selected: plugins.length > 0 || explicit.length > 0,
    explicit,
    skills: [...new Set([...explicit, ...pluginSkills])].sort()
  };
}

function resolveTargets(options) {
  const { targets, invalid } = getTargetGroups(options.agents, options.global);
  if (invalid.length > 0) {
    throw new CliError(`Unknown agent(s): ${invalid.join(', ')}. Supported: ${getSupportedAgents().join(', ')}.`);
  }
  return targets;
}

/**
 * Write one skill into place. The new copy is built in a hidden sibling folder
 * first, so a failed download or copy leaves any existing install untouched.
 * The user's .env and .env.local files, at any depth, are carried into the new
 * copy; nothing else is. Returns the relative paths of the kept files.
 */
async function placeSkill(source, skill, destination) {
  const staging = path.join(path.dirname(destination), `.${skill}.nxa-staging-${process.pid}`);
  fs.rmSync(staging, { recursive: true, force: true });

  try {
    await source.installSkill(skill, staging);
    if (!fs.existsSync(path.join(staging, 'SKILL.md'))) {
      throw new Error('source copy has no SKILL.md');
    }
    const kept = fs.existsSync(destination) ? carryOverEnvFiles(destination, staging) : [];
    fs.rmSync(destination, { recursive: true, force: true });
    fs.renameSync(staging, destination);
    return kept;
  } catch (error) {
    fs.rmSync(staging, { recursive: true, force: true });
    throw error;
  }
}

/**
 * Write each target's skills and print one line per skill.
 * plan: [{ labels, dir, skills }]. replace: overwrite skills that already exist.
 */
async function writePlan(source, plan, { replace }) {
  const totals = { installed: 0, upgraded: 0, skipped: 0 };
  const failures = [];

  for (const { labels, dir, skills } of plan) {
    fs.mkdirSync(dir, { recursive: true });
    console.log(`${labels.join(', ')} (${dir}):`);

    for (const skill of skills) {
      const destination = path.join(dir, skill);
      // A folder left by `remove` holding only .env files is not an install.
      const exists = fs.existsSync(path.join(destination, 'SKILL.md'));

      if (exists && !replace) {
        console.log(`  ⏭  ${skill} (already installed)`);
        totals.skipped++;
        continue;
      }

      try {
        const kept = await placeSkill(source, skill, destination);
        const note = kept.length > 0 ? ` (kept ${kept.join(', ')})` : '';
        console.log(`  ${exists ? '🔄' : '✅'} ${skill}${note}`);
        totals[exists ? 'upgraded' : 'installed']++;
      } catch (error) {
        console.log(`  ❌ ${skill} - ${error.message}`);
        failures.push(`${skill} (${dir})`);
      }
    }

    console.log('');
  }

  const parts = Object.entries(totals)
    .filter(([, count]) => count > 0)
    .map(([label, count]) => `${count} ${label}`);
  if (failures.length > 0) {
    parts.push(`${failures.length} failed`);
  }
  console.log(`✨ Done. ${parts.join(', ') || 'Nothing to do'}.\n`);

  if (failures.length > 0) {
    throw new CliError(`${failures.length} skill(s) failed: ${failures.join(', ')}. Existing copies of those skills were left unchanged.`);
  }
}

async function installSkills(options = {}) {
  await withSkillSource(options, async source => {
    const availableSkills = await source.listSkills();
    if (availableSkills.length === 0) {
      throw new CliError(`No skills found in ${source.label}.`);
    }

    const selection = resolveSelection(options, availableSkills);
    const skills = selection.selected ? selection.skills : availableSkills;
    const targets = resolveTargets(options);

    if (options.upgrade && !options.overwrite) {
      const existingSkills = collectExistingSkills(targets, skills);

      if (existingSkills.size > 0) {
        console.log('\n⚠️  The following skills will be replaced with the source version.');
        console.log('   Your .env and .env.local files are kept. Every other file is replaced:');
        [...existingSkills].forEach(skill => console.log(`   • ${skill}`));
        if (!confirm('\nProceed with upgrade?')) {
          console.log('\nUpgrade cancelled. Nothing changed.\n');
          return;
        }
      }
    }

    const scope = options.global ? 'global' : 'project';
    console.log(`\n🚀 ${options.upgrade ? 'Installing and upgrading' : 'Installing'} ${skills.length} skill(s) (${scope}, source: ${source.label})...\n`);

    await writePlan(
      source,
      targets.map(target => ({ ...target, skills })),
      { replace: options.upgrade }
    );
  });
}

module.exports = {
  collectExistingSkills,
  confirm,
  installSkills,
  placeSkill,
  resolveSelection,
  resolveSkillsToInstall,
  resolveTargets,
  writePlan
};
