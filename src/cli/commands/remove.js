const fs = require('fs');
const path = require('path');
const { loadPluginPackage, matchSkills } = require('../../core/plugins');
const { findEnvFiles, listInstalledSkills } = require('../../core/installed');
const { removeExceptEnvFiles } = require('../../core/file-system');
const { CliError } = require('../errors');
const { confirm, resolveTargets } = require('./install');

/**
 * Decide what to remove in each target. Names are matched against what is
 * installed, not against the source, so skills the source no longer has can
 * still be removed. Plugin patterns are matched against installed names.
 */
function planRemoval(targets, installedByDir, skills, pluginPatterns) {
  const notInstalled = new Set(skills);
  const plan = targets.map(target => {
    const installed = installedByDir.get(target.dir) || [];
    const fromPlugins = matchSkills(pluginPatterns, installed);
    const selected = installed.filter(skill => skills.includes(skill) || fromPlugins.includes(skill));
    selected.forEach(skill => notInstalled.delete(skill));
    return { ...target, skills: selected };
  });

  return { plan, notInstalled: [...notInstalled].sort() };
}

async function removeSkills(options = {}) {
  const plugins = options.plugins || [];
  const unknownPlugins = plugins.filter(name => !loadPluginPackage(name));
  if (unknownPlugins.length > 0) {
    throw new CliError(`Unknown plugin(s): ${unknownPlugins.join(', ')}.`);
  }
  const pluginPatterns = plugins.flatMap(name => loadPluginPackage(name).patterns);

  const targets = resolveTargets(options);
  const installedByDir = new Map(targets.map(target => [target.dir, listInstalledSkills(target.dir)]));
  const { plan, notInstalled } = planRemoval(targets, installedByDir, options.skills || [], pluginPatterns);
  const dirs = targets.map(target => target.dir).join(', ');

  if (notInstalled.length > 0) {
    throw new CliError(`Not installed in ${dirs}: ${notInstalled.join(', ')}. Nothing was removed.\n   Run "nxa list --installed" to see what is installed.`);
  }

  const total = plan.reduce((sum, target) => sum + target.skills.length, 0);
  if (total === 0) {
    console.log(`\nNothing to remove in ${dirs}.\n`);
    return;
  }

  console.log('\n⚠️  The following skills will be removed:');
  let hasEnv = false;
  for (const { dir, skills } of plan) {
    if (skills.length === 0) continue;
    console.log(`   ${dir}`);
    for (const skill of skills) {
      const envFiles = findEnvFiles(path.join(dir, skill));
      hasEnv = hasEnv || envFiles.length > 0;
      const note = envFiles.length > 0 ? `  (has ${envFiles.join(', ')})` : '';
      console.log(`     • ${skill}${note}`);
    }
  }

  // Keeping .env files is the default answer, so --yes keeps them; only
  // --delete-env removes them.
  let deleteEnv = options.deleteEnv;
  if (hasEnv && !deleteEnv && !options.overwrite) {
    deleteEnv = !confirm('\nKeep .env and .env.local files?', true);
  }
  if (hasEnv) {
    console.log(deleteEnv
      ? '\n   .env and .env.local files will be deleted.'
      : '\n   .env and .env.local files will be kept in place; everything else is deleted.');
  }

  if (!options.overwrite && !confirm('\nProceed with removal?')) {
    console.log('\nRemoval cancelled. Nothing changed.\n');
    return;
  }

  console.log('');
  const failures = [];
  for (const { labels, dir, skills } of plan) {
    if (skills.length === 0) continue;
    console.log(`${labels.join(', ')} (${dir}):`);
    for (const skill of skills) {
      try {
        const skillDir = path.join(dir, skill);
        if (deleteEnv) {
          fs.rmSync(skillDir, { recursive: true });
          console.log(`  🗑  ${skill}`);
        } else {
          const kept = removeExceptEnvFiles(skillDir);
          console.log(`  🗑  ${skill}${kept.length > 0 ? ` (kept ${kept.join(', ')})` : ''}`);
        }
      } catch (error) {
        console.log(`  ❌ ${skill} - ${error.message}`);
        failures.push(`${skill} (${dir})`);
      }
    }
    console.log('');
  }

  console.log(`✨ Done. ${total - failures.length} removed${failures.length ? `, ${failures.length} failed` : ''}.\n`);
  if (failures.length > 0) {
    throw new CliError(`${failures.length} skill(s) could not be removed: ${failures.join(', ')}.`);
  }
}

module.exports = { planRemoval, removeSkills };
