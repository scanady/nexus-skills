const { DEFAULT_AGENT } = require('./skills-core');

function parseArgs(args) {
  const result = {
    command: null,
    skills: [],
    packs: [],
    agents: [],
    global: false,
    listMode: 'bare',
    upgrade: false,
    overwrite: false,
    sourceUrl: '',
    sourceRef: ''
  };

  let index = 0;
  while (index < args.length) {
    const arg = args[index];

    if (arg === 'install' || arg === 'list' || arg === 'audit-overlap') {
      result.command = arg;
    } else if (arg === '--skill' || arg === '-s') {
      index++;
      if (index < args.length) {
        result.skills.push(args[index]);
      }
    } else if (arg === '--pack' || arg === '-P') {
      index++;
      if (index < args.length) {
        result.packs.push(args[index]);
      }
    } else if (arg === '--agent' || arg === '-a') {
      index++;
      if (index < args.length) {
        result.agents.push(args[index]);
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
      index++;
      if (index < args.length) {
        result.sourceUrl = args[index];
      }
    } else if (arg === '--source-ref' || arg === '--ref') {
      index++;
      if (index < args.length) {
        result.sourceRef = args[index];
      }
    } else if (!arg.startsWith('-') && !result.command) {
      result.command = arg;
    }

    index++;
  }

  if (result.agents.length === 0) {
    result.agents.push(DEFAULT_AGENT);
  }

  return result;
}

module.exports = { parseArgs };
