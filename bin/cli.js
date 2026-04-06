#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const {
  AGENTS,
  DEFAULT_AGENT,
  SKILLS_DIR,
  extractFrontmatter,
  getAvailableSkills,
  getSupportedAgents,
  getTargetGroups,
  isLocalMode,
  parseFrontmatter
} = require('./skills-core');
const {
  downloadRemoteSkill,
  fetchRemoteSkillFrontmatter,
  fetchRemoteSkillList
} = require('./github-fetch');

// Synchronous confirmation prompt
function confirm(question) {
  process.stdout.write(`${question} [y/N] `);
  let input = '';
  const buf = Buffer.alloc(1);
  while (true) {
    const n = fs.readSync(0, buf, 0, 1);
    if (n === 0) break;
    const ch = buf.toString();
    if (ch === '\n') break;
    input += ch;
  }
  return input.trim().toLowerCase() === 'y';
}

// Copy directory recursively
function copyDir(src, dest) {
  fs.mkdirSync(dest, { recursive: true });
  const entries = fs.readdirSync(src, { withFileTypes: true });

  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);

    if (entry.isDirectory()) {
      copyDir(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

// Parse command line arguments
function parseArgs(args) {
  const result = {
    command: null,
    skills: [],
    agents: [],
    global: false, // default to project install
    listMode: 'bare', // full | bare | count
    upgrade: false,
    overwrite: false
  };

  let i = 0;
  while (i < args.length) {
    const arg = args[i];

    if (arg === 'install' || arg === 'list') {
      result.command = arg;
    } else if (arg === '--skill' || arg === '-s') {
      i++;
      if (i < args.length) {
        result.skills.push(args[i]);
      }
    } else if (arg === '--agent' || arg === '-a') {
      i++;
      if (i < args.length) {
        result.agents.push(args[i]);
      }
    } else if (arg === '--project' || arg === '-p') {
      result.global = false;
    } else if (arg === '--global' || arg === '-g') {
      result.global = true;
    } else if (arg === '--count' || arg === '-c') {
      result.listMode = 'count';
    } else if (arg === '--names' || arg === '-n') {
      result.listMode = 'bare';
    } else if (arg === '--full' || arg === '-f') {
      result.listMode = 'full';
    } else if (arg === '--upgrade' || arg === '-u') {
      result.upgrade = true;
    } else if (arg === '--overwrite' || arg === '-o') {
      result.overwrite = true;
    } else if (!arg.startsWith('-')) {
      if (!result.command) {
        result.command = arg;
      }
    }
    i++;
  }

  // Default to the Agent Skills standard path if no agents are specified
  if (result.agents.length === 0) {
    result.agents.push(DEFAULT_AGENT);
  }

  return result;
}

async function getSkillList() {
  if (isLocalMode()) {
    return getAvailableSkills();
  }

  return fetchRemoteSkillList();
}

async function getSkillMetadata(skill) {
  if (isLocalMode()) {
    const skillPath = path.join(SKILLS_DIR, skill, 'SKILL.md');
    return extractFrontmatter(skillPath);
  }

  const content = await fetchRemoteSkillFrontmatter(skill);
  return parseFrontmatter(content);
}

async function installSkill(skill, destinationDir) {
  if (isLocalMode()) {
    const src = path.join(SKILLS_DIR, skill);
    copyDir(src, destinationDir);
    return;
  }

  await downloadRemoteSkill(skill, destinationDir);
}

// List available skills
async function listSkills(listMode = 'full') {
  const skills = await getSkillList();

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

  // full (default)
  console.log('\n📦 Available skills:\n');

  if (skills.length === 0) {
    console.log('  No skills found.\n');
    return;
  }

  for (const skill of skills) {
    const metadata = await getSkillMetadata(skill);
    const description = metadata.description || 'No description';

    console.log(`  • ${skill}`);
    console.log(`    ${description}\n`);
  }

  console.log('Install all:     npx forge-agents install');
  console.log('Install one:     npx forge-agents install --skill ops-process-sop-creator\n');
}

// Install skills
async function installSkills(selectedSkills, agents, isGlobal, upgrade, overwrite) {
  const availableSkills = await getSkillList();

  // If no specific skills selected, install all
  const skillsToInstall = selectedSkills.length > 0
    ? selectedSkills.filter(s => availableSkills.includes(s))
    : availableSkills;

  // Check for invalid skill names
  if (selectedSkills.length > 0) {
    const invalid = selectedSkills.filter(s => !availableSkills.includes(s));
    if (invalid.length > 0) {
      console.log(`\n⚠️  Unknown skills: ${invalid.join(', ')}`);
      console.log(`   Available: ${availableSkills.join(', ')}\n`);
    }
  }

  if (skillsToInstall.length === 0) {
    console.log('\n❌ No valid skills to install.\n');
    await listSkills();
    return;
  }

  const { targets, invalid } = getTargetGroups(agents, isGlobal);
  if (invalid.length > 0) {
    console.log(`\n⚠️  Unknown agent(s): ${invalid.join(', ')}`);
    console.log(`   Available: ${getSupportedAgents().join(', ')}\n`);
  }

  if (targets.length === 0) {
    console.log('\n❌ No valid agents to install to.\n');
    return;
  }

  // When upgrading, collect existing skills across all targets and confirm
  if (upgrade && !overwrite) {
    const existingSkills = new Set();
    for (const { dir } of targets) {
      for (const skill of skillsToInstall) {
        if (fs.existsSync(path.join(dir, skill))) {
          existingSkills.add(skill);
        }
      }
    }
    if (existingSkills.size > 0) {
      console.log('\n⚠️  The following skills will be deleted and replaced:');
      [...existingSkills].forEach(s => console.log(`   • ${s}`));
      if (!confirm('\nProceed with upgrade?')) {
        console.log('\n❌ Upgrade cancelled.\n');
        return;
      }
    }
  }

  const scope = isGlobal ? 'global' : 'project';
  const action = upgrade ? 'Upgrading' : 'Installing';
  const source = isLocalMode() ? 'local bundle' : 'GitHub';
  console.log(`\n🚀 ${action} forge-agents (${scope}, source: ${source})...\n`);

  let totalInstalled = 0, totalUpgraded = 0, totalSkipped = 0;

  for (const { labels, dir } of targets) {
    fs.mkdirSync(dir, { recursive: true });
    console.log(`${labels.join(', ')} (${dir}):`);

    for (const skill of skillsToInstall) {
      const dest = path.join(dir, skill);
      const exists = fs.existsSync(dest);

      if (exists && !upgrade) {
        console.log(`  ⏭  ${skill} (already installed)`);
        totalSkipped++;
        continue;
      }

      try {
        if (exists) {
          fs.rmSync(dest, { recursive: true, force: true });
        }
        await installSkill(skill, dest);
        if (exists) {
          console.log(`  🔄 ${skill}`);
          totalUpgraded++;
        } else {
          console.log(`  ✅ ${skill}`);
          totalInstalled++;
        }
      } catch (err) {
        console.log(`  ❌ ${skill} - ${err.message}`);
      }
    }
    console.log('');
  }

  console.log('✨ Done!\n');
  const parts = [];
  if (totalInstalled > 0) parts.push(`${totalInstalled} installed`);
  if (totalUpgraded > 0) parts.push(`${totalUpgraded} upgraded`);
  if (totalSkipped > 0) parts.push(`${totalSkipped} skipped`);
  if (parts.length > 0) console.log(`   ${parts.join(', ')}`);
}

// Show help
function showHelp() {
  const supportedAgents = getSupportedAgents()
    .map(agent => {
      const config = AGENTS[agent];
      return `  ${agent.padEnd(20)} ${config.globalDir.padEnd(22)} ${config.projectDir}`;
    })
    .join('\n');

  console.log(`
forge-agents - Agentic skills for founders

Usage:
  npx forge-agents <command> [options]

Commands:
  install              Install skills
  list                 List available skills

Options:
  --skill, -s <name>   Install specific skill(s) (repeatable)
  --agent, -a <agent>  Target agent(s) (repeatable, default: agent-skills)
  --project, -p        Install to current project directory (default)
  --global, -g         Install globally
  --upgrade, -u        Replace existing skills with latest versions (prompts for confirmation)
  --overwrite, -o      Skip confirmation when upgrading
  --names, -n          List skill names only (default)
  --full, -f           List skills with names and descriptions
  --count, -c          Print only the count of available skills

Supported Agents:
${supportedAgents}

Examples:
  npx forge-agents install
  npx forge-agents install --skill ops-process-sop-creator
  npx forge-agents install -a agent-skills -a claude-code -a github-copilot -a codex
  npx forge-agents install -a github-copilot --skill content-copy-humanizer -p
  npx forge-agents install --upgrade
  npx forge-agents install --upgrade --overwrite
  npx forge-agents list
  npx forge-agents list --names
  npx forge-agents list --count
`);
}

// Main
async function main() {
  const args = process.argv.slice(2);
  const { command, skills, agents, global: isGlobal, listMode, upgrade, overwrite } = parseArgs(args);

  switch (command) {
    case 'install':
      await installSkills(skills, agents, isGlobal, upgrade, overwrite);
      break;
    case 'list':
      await listSkills(listMode);
      break;
    case 'help':
    case '--help':
    case '-h':
      showHelp();
      break;
    default:
      if (!command) {
        showHelp();
      } else {
        console.log(`\n❌ Unknown command: ${command}\n`);
        showHelp();
      }
  }
}

main().catch(error => {
  console.error(`\n❌ ${error.message}\n`);
  process.exit(1);
});