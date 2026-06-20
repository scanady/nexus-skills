#!/usr/bin/env node

const childProcess = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');
const {
  AGENTS,
  DEFAULT_AGENT,
  PROJECT_ROOT,
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

function getEnvValue(...names) {
  for (const name of names) {
    const value = process.env[name];
    if (value && value.trim()) {
      return value.trim();
    }
  }

  return '';
}

// Resolve a list of pack names to the skills they contain
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
    } catch (err) {
      console.log(`  ⚠️  Failed to read pack ${packName}: ${err.message}`);
      continue;
    }
    for (const pattern of (pack.skills || [])) {
      if (pattern.endsWith('*')) {
        const prefix = pattern.slice(0, -1);
        availableSkills.filter(s => s.startsWith(prefix)).forEach(s => resolved.add(s));
      } else {
        if (availableSkills.includes(pattern)) resolved.add(pattern);
      }
    }
  }

  return [...resolved];
}

function getSkillsFromDir(skillsDir) {
  try {
    return fs.readdirSync(skillsDir)
      .filter(name => {
        const skillPath = path.join(skillsDir, name);
        return fs.statSync(skillPath).isDirectory() &&
          fs.existsSync(path.join(skillPath, 'SKILL.md'));
      })
      .sort((left, right) => left.localeCompare(right));
  } catch (error) {
    return [];
  }
}

function cloneRepoToTempDir(repoUrl, ref) {
  const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'nyld-nexus-skills-'));
  const args = ['clone', '--depth', '1'];

  if (ref) {
    args.push('--branch', ref);
  }

  args.push(repoUrl, tempDir);

  const result = childProcess.spawnSync('git', args, {
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe']
  });

  if (result.error) {
    fs.rmSync(tempDir, { recursive: true, force: true });
    throw new Error(`Failed to run git clone for ${repoUrl}: ${result.error.message}`);
  }

  if (result.status !== 0) {
    fs.rmSync(tempDir, { recursive: true, force: true });
    const stderr = (result.stderr || '').trim();
    throw new Error(stderr || `git clone failed for ${repoUrl}`);
  }

  return tempDir;
}

async function withClonedRepo(sourceConfig, work) {
  const repoDir = cloneRepoToTempDir(sourceConfig.repoUrl, sourceConfig.sourceRef);

  try {
    const skillsDir = path.join(repoDir, 'skills');
    if (!fs.existsSync(skillsDir) || !fs.statSync(skillsDir).isDirectory()) {
      throw new Error(`Repository ${sourceConfig.repoUrl} does not contain a skills/ directory.`);
    }

    return await work(skillsDir);
  } finally {
    fs.rmSync(repoDir, { recursive: true, force: true });
  }
}

function resolveSourceConfig(options = {}) {
  const repoUrl = options.sourceUrl || getEnvValue('NYLD_NEXUS_SKILLS_SOURCE_URL', 'NEXUS_AGENTS_REPO_URL');
  const sourceRef = options.sourceRef || getEnvValue('NYLD_NEXUS_SKILLS_SOURCE_REF', 'NEXUS_AGENTS_REPO_REF');

  return {
    repoUrl,
    sourceRef
  };
}

async function withSkillSource(options, work) {
  const sourceConfig = resolveSourceConfig(options);

  if (sourceConfig.repoUrl) {
    return withClonedRepo(sourceConfig, skillsDir => work({
      type: 'repo',
      label: `repository ${sourceConfig.repoUrl}${sourceConfig.sourceRef ? `#${sourceConfig.sourceRef}` : ''}`,
      listSkills: () => getSkillsFromDir(skillsDir),
      getMetadata: skill => extractFrontmatter(path.join(skillsDir, skill, 'SKILL.md')),
      installSkill: (skill, destinationDir) => copyDir(path.join(skillsDir, skill), destinationDir)
    }));
  }

  if (isLocalMode()) {
    return work({
      type: 'local',
      label: 'local bundle',
      listSkills: () => getAvailableSkills(),
      getMetadata: skill => extractFrontmatter(path.join(SKILLS_DIR, skill, 'SKILL.md')),
      installSkill: (skill, destinationDir) => copyDir(path.join(SKILLS_DIR, skill), destinationDir)
    });
  }

  return work({
    type: 'github',
    label: 'GitHub fallback',
    listSkills: () => fetchRemoteSkillList(),
    getMetadata: async skill => parseFrontmatter(await fetchRemoteSkillFrontmatter(skill)),
    installSkill: (skill, destinationDir) => downloadRemoteSkill(skill, destinationDir)
  });
}

// Parse command line arguments
function parseArgs(args) {
  const result = {
    command: null,
    skills: [],
    packs: [],
    agents: [],
    global: false, // default to project install
    listMode: 'bare', // full | bare | count
    upgrade: false,
    overwrite: false,
    sourceUrl: '',
    sourceRef: ''
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
    } else if (arg === '--pack' || arg === '-P') {
      i++;
      if (i < args.length) {
        result.packs.push(args[i]);
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
    } else if (arg === '--source-url' || arg === '--repo-url') {
      i++;
      if (i < args.length) {
        result.sourceUrl = args[i];
      }
    } else if (arg === '--source-ref' || arg === '--ref') {
      i++;
      if (i < args.length) {
        result.sourceRef = args[i];
      }
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

// List available skills
async function listSkills(options = {}) {
  await withSkillSource(options, async source => {
    const skills = await source.listSkills();

    if (options.listMode === 'count') {
      console.log(skills.length);
      return;
    }

    if (options.listMode === 'bare') {
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

    console.log('Install all:     nyld-nexus-skills install');
    console.log('Install one:     nyld-nexus-skills install --skill ops-process-sop-creator\n');
  });
}

// Install skills
async function installSkills(options = {}) {
  await withSkillSource(options, async source => {
    const availableSkills = await source.listSkills();

    // Expand any --pack flags into the skills list before filtering
    if (options.packs && options.packs.length > 0) {
      const packSkills = resolvePackSkills(options.packs, availableSkills);
      options.skills = [...new Set([...(options.skills || []), ...packSkills])];
    }

    const selectedSkills = options.skills || [];

    const skillsToInstall = selectedSkills.length > 0
      ? selectedSkills.filter(s => availableSkills.includes(s))
      : availableSkills;

    if (selectedSkills.length > 0) {
      const invalidSkills = selectedSkills.filter(s => !availableSkills.includes(s));
      if (invalidSkills.length > 0) {
        console.log(`\n⚠️  Unknown skills: ${invalidSkills.join(', ')}`);
        console.log(`   Available: ${availableSkills.join(', ')}\n`);
      }
    }

    if (skillsToInstall.length === 0) {
      console.log('\n❌ No valid skills to install.\n');
      await listSkills({
        ...options,
        listMode: 'full'
      });
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

    const scope = options.global ? 'global' : 'project';
    const action = options.upgrade ? 'Upgrading' : 'Installing';
    console.log(`\n🚀 ${action} nyld-nexus-skills (${scope}, source: ${source.label})...\n`);

    let totalInstalled = 0, totalUpgraded = 0, totalSkipped = 0;

    for (const { labels, dir } of targets) {
      fs.mkdirSync(dir, { recursive: true });
      console.log(`${labels.join(', ')} (${dir}):`);

      for (const skill of skillsToInstall) {
        const dest = path.join(dir, skill);
        const exists = fs.existsSync(dest);

        if (exists && !options.upgrade) {
          console.log(`  ⏭  ${skill} (already installed)`);
          totalSkipped++;
          continue;
        }

        try {
          if (exists) {
            fs.rmSync(dest, { recursive: true, force: true });
          }
          await source.installSkill(skill, dest);
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
  });
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
nyld-nexus-skills - Agentic skills for development teams

Usage:
  nyld-nexus-skills <command> [options]

Commands:
  install              Install skills
  list                 List available skills
  audit-overlap        Find duplicate and overlapping skills

Options:
  --skill, -s <name>   Install specific skill(s) (repeatable)
  --pack, -P <name>    Install all skills in a named pack (repeatable)
  --agent, -a <agent>  Target agent(s) (repeatable, default: agent-skills)
  --project, -p        Install to current project directory (default)
  --global, -g         Install globally
  --upgrade, -u        Replace existing skills with latest versions (prompts for confirmation)
  --overwrite, -o      Skip confirmation when upgrading
  --source-url <url>   Clone skills from a git repository instead of the bundled skills
  --source-ref <ref>   Git branch, tag, or commit to clone with --source-url
  --names, -n          List skill names only (default)
  --full, -f           List skills with names and descriptions
  --count, -c          Print only the count of available skills

Supported Agents:
${supportedAgents}

Audit options (audit-overlap):
  --threshold, -t <n>  Minimum overlap score to report (default: 0.20)
  --top <n>            Limit to top N pairs
  --json-only          Write JSON report only
  --md-only            Write Markdown report only
  --output, -o <dir>   Output directory (default: output/)

Examples:
  nyld-nexus-skills install
  nyld-nexus-skills install --skill ops-process-sop-creator
  nyld-nexus-skills install -a agent-skills -a claude-code -a github-copilot -a codex
  nyld-nexus-skills install -a github-copilot --skill content-copy-humanizer -p
  nyld-nexus-skills install --source-url https://git.nylcloud.com/Direct/nyld-nexus-skills.git --source-ref main
  nyld-nexus-skills install --upgrade
  nyld-nexus-skills install --upgrade --overwrite
  nyld-nexus-skills install --pack marketing
  nyld-nexus-skills install --pack tech --pack data
  nyld-nexus-skills install --pack strategy --skill thinking-get-unstuck
  nyld-nexus-skills list
  nyld-nexus-skills list --names
  nyld-nexus-skills list --count
  node bin/cli.js audit-overlap
  node bin/cli.js audit-overlap --threshold 0.30 --top 25
`);
}

// Main
async function main() {
  const args = process.argv.slice(2);
  const options = parseArgs(args);
  const { command } = options;

  switch (command) {
    case 'install':
      await installSkills(options);
      break;
    case 'list':
      await listSkills(options);
      break;
    case 'audit-overlap':
      require('./skill-overlap-report').run(process.argv.slice(3));
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