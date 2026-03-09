#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const os = require('os');

const SKILLS_DIR = path.join(__dirname, '..', 'skills');

// Supported agents and their install paths
const AGENTS = {
  'claude-code': {
    name: 'Claude Code',
    projectDir: '.claude/skills',
    globalDir: path.join(os.homedir(), '.claude', 'skills')
  },
  'github-copilot': {
    name: 'GitHub Copilot',
    projectDir: '.agents/skills',
    globalDir: path.join(os.homedir(), '.copilot', 'skills')
  },
  'codex': {
    name: 'Codex',
    projectDir: '.agents/skills',
    globalDir: path.join(os.homedir(), '.codex', 'skills')
  }
};

const DEFAULT_AGENT = 'github-copilot';

// Available skills
function getAvailableSkills() {
  try {
    return fs.readdirSync(SKILLS_DIR).filter(name => {
      const skillPath = path.join(SKILLS_DIR, name);
      return fs.statSync(skillPath).isDirectory() &&
             fs.existsSync(path.join(skillPath, 'SKILL.md'));
    });
  } catch (err) {
    return [];
  }
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
    global: true // default to global install (preserves existing behavior)
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
    } else if (!arg.startsWith('-')) {
      if (!result.command) {
        result.command = arg;
      }
    }
    i++;
  }

  // Default to claude-code if no agents specified
  if (result.agents.length === 0) {
    result.agents.push(DEFAULT_AGENT);
  }

  return result;
}

// List available skills
function listSkills() {
  const skills = getAvailableSkills();

  console.log('\n📦 Available skills:\n');

  if (skills.length === 0) {
    console.log('  No skills found.\n');
    return;
  }

  skills.forEach(skill => {
    const skillPath = path.join(SKILLS_DIR, skill, 'SKILL.md');
    const content = fs.readFileSync(skillPath, 'utf8');

    // Extract description from frontmatter
    const match = content.match(/description:\s*(.+)/);
    const description = match ? match[1].trim() : 'No description';

    console.log(`  • ${skill}`);
    console.log(`    ${description}\n`);
  });

  console.log('Install all:     npx forge-agents install');
  console.log('Install one:     npx forge-agents install --skill sop-creator\n');
}

// Resolve target directories for the given agents and scope
function getTargetDirs(agents, isGlobal) {
  const targets = [];
  const invalid = [];

  for (const agent of agents) {
    const config = AGENTS[agent];
    if (!config) {
      invalid.push(agent);
      continue;
    }
    const dir = isGlobal ? config.globalDir : path.resolve(config.projectDir);
    targets.push({ agent, name: config.name, dir });
  }

  if (invalid.length > 0) {
    console.log(`\n⚠️  Unknown agent(s): ${invalid.join(', ')}`);
    console.log(`   Available: ${Object.keys(AGENTS).join(', ')}\n`);
  }

  return targets;
}

// Install skills
function installSkills(selectedSkills, agents, isGlobal) {
  const availableSkills = getAvailableSkills();

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
    listSkills();
    return;
  }

  const targets = getTargetDirs(agents, isGlobal);
  if (targets.length === 0) {
    console.log('\n❌ No valid agents to install to.\n');
    return;
  }

  const scope = isGlobal ? 'global' : 'project';
  console.log(`\n🚀 Installing forge-agents (${scope})...\n`);

  for (const { agent, name, dir } of targets) {
    fs.mkdirSync(dir, { recursive: true });

    console.log(`${name} (${dir}):`);
    skillsToInstall.forEach(skill => {
      const src = path.join(SKILLS_DIR, skill);
      const dest = path.join(dir, skill);

      try {
        copyDir(src, dest);
        console.log(`  ✅ ${skill}`);
      } catch (err) {
        console.log(`  ❌ ${skill} - ${err.message}`);
      }
    });
    console.log('');
  }

  console.log('✨ Installation complete!\n');
  console.log('Usage:');
  skillsToInstall.forEach(skill => {
    console.log(`  /${skill}`);
  });
  console.log('');
}

// Show help
function showHelp() {
  console.log(`
forge-agents - Agentic skills for founders

Usage:
  npx forge-agents <command> [options]

Commands:
  install              Install skills
  list                 List available skills

Options:
  --skill, -s <name>   Install specific skill(s) (repeatable)
  --agent, -a <agent>  Target agent(s) (repeatable, default: github-copilot)
  --global, -g         Install globally (default)
  --project, -p        Install to current project directory

Supported Agents:
  claude-code          ~/.claude/skills/      .claude/skills/
  github-copilot       ~/.copilot/skills/     .agents/skills/
  codex                ~/.codex/skills/       .agents/skills/

Examples:
  npx forge-agents install
  npx forge-agents install --skill sop-creator
  npx forge-agents install -a github-copilot -a codex
  npx forge-agents install -a github-copilot --skill humanizer -p
  npx forge-agents list
`);
}

// Main
function main() {
  const args = process.argv.slice(2);
  const { command, skills, agents, global: isGlobal } = parseArgs(args);

  switch (command) {
    case 'install':
      installSkills(skills, agents, isGlobal);
      break;
    case 'list':
      listSkills();
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

main();