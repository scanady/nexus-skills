const { AGENTS, getSupportedAgents } = require('../core/skills');

function showHelp() {
  const agents = getSupportedAgents();
  const width = Math.max('global (--global)'.length, ...agents.map(agent => AGENTS[agent].globalDir.length));
  const supportedAgents = agents
    .map(agent => `  ${agent.padEnd(20)} ${AGENTS[agent].globalDir.padEnd(width)} ${AGENTS[agent].projectDir}`)
    .join('\n');

  console.log(`
nxa - Agentic skills for development teams

Usage:
  npx nxa <command> [options]
  npx nxa --help | --version

Commands:
  install              Add skills. Skips skills that are already installed.
  upgrade              Replace installed skills with the source version. Never adds new skills.
                       Your .env and .env.local files are kept; every other file is replaced.
  remove               Delete installed skills. Needs --skill or --plugin.
                       Keeps .env and .env.local in place unless --delete-env is set.
  list                 List available skills, or installed ones with --installed
  audit-overlap        Find duplicate and overlapping skills (repo checkout only)
  help                 Show this help

Selection (install, upgrade, remove):
  --skill, -s <name>   Skill name. Repeatable, or comma-separated (a,b,c)
  --plugin, -P <name>  Every skill in a plugin. Repeatable, or comma-separated
                       install: no selection means every available skill
                       upgrade: no selection means every installed skill
                       remove: a selection is required

Target (install, upgrade, remove, list --installed):
  --agent, -a <agent>  Target agent. Repeatable (default: agent-skills)
  --project, -p        Current project directory (default)
  --global, -g         User home directory (~)

Install, upgrade, and remove behavior:
  --upgrade, -u        install only: also replace skills that are already installed
  --yes, -y            Take the default answers without prompting (alias: --overwrite, -o)
                       Required when input is not a terminal. With remove, keeps .env files
  --delete-env         remove only: also delete .env and .env.local files

Source (install, upgrade, list):
  --source-url <url>   Clone skills from a git repository instead of the bundled skills
  --source-ref <ref>   Branch, tag, or commit to clone (needs --source-url)

List output (list):
  --installed, -i      List what is installed in the target, not what is available
  --names, -n          Skill names only (default)
  --full, -f           Names and descriptions (with --installed: also flags
                       skills not in the source and skills holding .env files)
  --count, -c          Count only

Audit options (audit-overlap):
  --threshold, -t <n>  Minimum overlap score, 0 to 1 (default: 0.20)
  --top <n>            Limit to top N pairs
  --json-only          Write JSON report only
  --md-only            Write Markdown report only
  --output, -o <dir>   Output directory (default: output/)

Rules:
  Unknown commands, options, skills, plugins, and agents are errors.
  Nothing is written when any of them is wrong.
  --help anywhere shows this text and runs nothing.
  An option that does not apply to the command is an error.

Supported Agents:
  ${'agent'.padEnd(20)} ${'global (--global)'.padEnd(width)} project (default)
${supportedAgents}

Examples:
  npx nxa list --full
  npx nxa install --skill ops-process-sop-creator
  npx nxa install --skill content-copy-humanizer,research-analyst --global
  npx nxa install --plugin engineering --plugin data
  npx nxa install -a claude-code -a github-copilot --skill content-copy-humanizer
  npx nxa upgrade --global
  npx nxa upgrade --global --overwrite
  npx nxa upgrade --skill content-copy-humanizer -a claude-code
  npx nxa list --installed --global --full
  npx nxa remove --skill impeccable --global
  npx nxa install --source-url https://github.com/scanady/nexus-skills.git --source-ref main
  node bin/nxa.js audit-overlap --threshold 0.30 --top 25
`);
}

module.exports = { showHelp };
