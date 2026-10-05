const { DEFAULT_AGENT } = require('../core/skills');
const { usageError } = require('./errors');

// Every flag the CLI knows. `value: true` flags take the next argument (or `--flag=value`).
// `list: true` flags are repeatable and also accept comma-separated values.
const FLAGS = {
  help: { names: ['--help', '-h'] },
  version: { names: ['--version', '-v'] },
  skills: { names: ['--skill', '-s'], value: true, list: true },
  plugins: { names: ['--plugin', '-P', '--pack'], value: true, list: true },
  agents: { names: ['--agent', '-a'], value: true, list: true },
  project: { names: ['--project', '-p'] },
  global: { names: ['--global', '-g'] },
  upgrade: { names: ['--upgrade', '-u'] },
  overwrite: { names: ['--overwrite', '-o', '--yes', '-y'] },
  installed: { names: ['--installed', '-i'] },
  deleteEnv: { names: ['--delete-env'] },
  sourceUrl: { names: ['--source-url', '--repo-url'], value: true },
  sourceRef: { names: ['--source-ref', '--ref'], value: true },
  names: { names: ['--names', '-n'] },
  full: { names: ['--full', '-f'] },
  count: { names: ['--count', '-c'] }
};

const SOURCE_FLAGS = ['sourceUrl', 'sourceRef'];
const SCOPE_FLAGS = ['agents', 'project', 'global'];

// Which flags each command accepts. Anything else is a usage error.
const COMMAND_FLAGS = {
  install: ['skills', 'plugins', ...SCOPE_FLAGS, 'upgrade', 'overwrite', ...SOURCE_FLAGS],
  upgrade: ['skills', 'plugins', ...SCOPE_FLAGS, 'overwrite', ...SOURCE_FLAGS],
  remove: ['skills', 'plugins', ...SCOPE_FLAGS, 'overwrite', 'deleteEnv'],
  list: ['names', 'full', 'count', 'installed', ...SCOPE_FLAGS, ...SOURCE_FLAGS],
  help: []
};

// audit-overlap parses its own options; the CLI only routes to it.
const PASSTHROUGH_COMMANDS = ['audit-overlap'];

const COMMANDS = [...Object.keys(COMMAND_FLAGS), ...PASSTHROUGH_COMMANDS];

function findFlag(name) {
  return Object.keys(FLAGS).find(key => FLAGS[key].names.includes(name)) || null;
}

function emptyOptions() {
  return {
    command: null,
    help: false,
    version: false,
    skills: [],
    plugins: [],
    agents: [],
    global: false,
    listMode: 'bare',
    installed: false,
    deleteEnv: false,
    upgrade: false,
    overwrite: false,
    sourceUrl: '',
    sourceRef: '',
    rest: []
  };
}

function splitList(value) {
  return value.split(',').map(item => item.trim()).filter(Boolean);
}

function parseArgs(args) {
  const result = emptyOptions();
  const given = new Set();
  let index = 0;

  // Leading --help / --version may come before the command.
  while (index < args.length && (findFlag(args[index]) === 'help' || findFlag(args[index]) === 'version')) {
    result[findFlag(args[index])] = true;
    index++;
  }

  if (index < args.length) {
    const first = args[index];
    if (first.startsWith('-')) {
      throw usageError(`Put the command first. Expected one of: ${COMMANDS.join(', ')}. Got "${first}".`);
    }
    if (!COMMANDS.includes(first)) {
      throw usageError(`Unknown command "${first}". Expected one of: ${COMMANDS.join(', ')}.`);
    }
    result.command = first;
    index++;
  }

  if (PASSTHROUGH_COMMANDS.includes(result.command)) {
    const rest = args.slice(index);
    result.help = result.help || rest.some(arg => findFlag(arg) === 'help');
    result.rest = rest;
    return finish(result, given);
  }

  const allowed = result.command ? COMMAND_FLAGS[result.command] : [];

  for (; index < args.length; index++) {
    const arg = args[index];

    if (!arg.startsWith('-') || arg === '-') {
      const hint = result.command === 'install' || result.command === 'upgrade'
        ? ` To select a skill, use --skill ${arg}.`
        : '';
      throw usageError(`Unexpected argument "${arg}".${hint}`);
    }

    const equals = arg.startsWith('--') ? arg.indexOf('=') : -1;
    const flagName = equals === -1 ? arg : arg.slice(0, equals);
    const key = findFlag(flagName);

    if (!key) {
      throw usageError(`Unknown option "${flagName}".`);
    }
    if (key === 'help' || key === 'version') {
      result[key] = true;
      continue;
    }
    if (!allowed.includes(key)) {
      const where = result.command ? `with "${result.command}"` : 'without a command';
      throw usageError(`Option "${flagName}" is not valid ${where}.`);
    }

    given.add(key);
    const spec = FLAGS[key];
    if (!spec.value) {
      if (equals !== -1) {
        throw usageError(`Option "${flagName}" does not take a value.`);
      }
      applySwitch(result, key);
      continue;
    }

    let value;
    if (equals !== -1) {
      value = arg.slice(equals + 1);
    } else {
      value = args[index + 1];
      if (value === undefined || value.startsWith('-')) {
        throw usageError(`Option "${flagName}" needs a value.`);
      }
      index++;
    }

    if (spec.list) {
      const items = splitList(value);
      if (items.length === 0) {
        throw usageError(`Option "${flagName}" needs a value.`);
      }
      result[key].push(...items);
    } else {
      if (!value.trim()) {
        throw usageError(`Option "${flagName}" needs a value.`);
      }
      result[key] = value.trim();
    }
  }

  return finish(result, given);
}

// Later flags win for the two exclusive groups: --project/--global and --names/--full/--count.
function applySwitch(result, key) {
  if (key === 'project') result.global = false;
  else if (key === 'global') result.global = true;
  else if (key === 'names') result.listMode = 'bare';
  else if (key === 'full') result.listMode = 'full';
  else if (key === 'count') result.listMode = 'count';
  else result[key] = true;
}

function finish(result, given) {
  if (result.command === 'install' && result.overwrite && !result.upgrade) {
    throw usageError('"--overwrite" (or "--yes") only applies with "--upgrade". Without --upgrade, installed skills are never replaced.');
  }
  if (result.command === 'remove' && result.skills.length === 0 && result.plugins.length === 0) {
    throw usageError('"remove" needs --skill or --plugin. It never removes every skill.');
  }
  if (result.command === 'list' && !result.installed && SCOPE_FLAGS.some(key => given.has(key))) {
    throw usageError('"--agent", "--global", and "--project" apply to "list" only with "--installed".');
  }
  if (result.sourceRef && !result.sourceUrl) {
    throw usageError('"--source-ref" needs "--source-url". Example: --source-url https://github.com/scanady/nexus-skills.git --source-ref main');
  }

  result.skills = [...new Set(result.skills)];
  result.plugins = [...new Set(result.plugins)];
  if (result.agents.length === 0) {
    result.agents.push(DEFAULT_AGENT);
  }

  return result;
}

module.exports = { COMMANDS, parseArgs };
