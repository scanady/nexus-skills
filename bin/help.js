const { AGENTS, getSupportedAgents } = require('./skills-core');

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
  npx nyld-nexus-skills <command> [options]

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
  npx nyld-nexus-skills install
  npx nyld-nexus-skills install --skill ops-process-sop-creator
  npx nyld-nexus-skills install -a agent-skills -a claude-code -a github-copilot -a codex
  npx nyld-nexus-skills install -a github-copilot --skill content-copy-humanizer -p
  npx nyld-nexus-skills install --upgrade
  npx nyld-nexus-skills install --upgrade --overwrite
  npx nyld-nexus-skills install --pack marketing
  npx nyld-nexus-skills install --pack tech --pack data
  npx nyld-nexus-skills install --source-url https://github.com/scanady/nexus-skills.git --source-ref main
  npx nyld-nexus-skills list
  npx nyld-nexus-skills list --names
  npx nyld-nexus-skills list --count
  node bin/cli.js audit-overlap
  node bin/cli.js audit-overlap --threshold 0.30 --top 25
`);
}

module.exports = { showHelp };
