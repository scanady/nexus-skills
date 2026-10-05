const test = require('node:test');
const assert = require('node:assert/strict');

const { parseArgs } = require('../src/cli/args');

const DEFAULTS = {
  command: 'install',
  help: false,
  version: false,
  skills: [],
  plugins: [],
  agents: ['agent-skills'],
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

function usage(args, pattern) {
  assert.throws(() => parseArgs(args), error => error.exitCode === 2 && pattern.test(error.message));
}

test('parseArgs defaults to install target agent skills for project scope', () => {
  assert.deepEqual(parseArgs(['install']), DEFAULTS);
});

test('parseArgs collects repeatable skills, plugins, and agents', () => {
  const args = parseArgs([
    'install',
    '--skill', 'content-copy-humanizer',
    '-s', 'research-analyst',
    '--plugin', 'marketing',
    '-P', 'engineering',
    '--agent', 'github-copilot',
    '-a', 'claude-code',
    '--global',
    '--upgrade',
    '--overwrite',
    '--source-url', 'https://github.com/scanady/nexus-skills.git',
    '--source-ref', 'main'
  ]);

  assert.deepEqual(args, {
    ...DEFAULTS,
    skills: ['content-copy-humanizer', 'research-analyst'],
    plugins: ['marketing', 'engineering'],
    agents: ['github-copilot', 'claude-code'],
    global: true,
    upgrade: true,
    overwrite: true,
    sourceUrl: 'https://github.com/scanady/nexus-skills.git',
    sourceRef: 'main'
  });
});

test('parseArgs accepts comma lists and --flag=value, and drops duplicates', () => {
  const args = parseArgs(['upgrade', '--skill=a,b', '-s', 'b,c', '--agent=claude']);
  assert.deepEqual(args.skills, ['a', 'b', 'c']);
  assert.deepEqual(args.agents, ['claude']);
});

test('parseArgs still accepts the deprecated --pack alias', () => {
  assert.deepEqual(parseArgs(['install', '--pack', 'marketing']).plugins, ['marketing']);
});

test('parseArgs supports list output modes, last one wins', () => {
  assert.equal(parseArgs(['list', '--full']).listMode, 'full');
  assert.equal(parseArgs(['list', '--count']).listMode, 'count');
  assert.equal(parseArgs(['list', '--full', '--names']).listMode, 'bare');
});

test('parseArgs lets the last of --project and --global win', () => {
  assert.equal(parseArgs(['install', '-g', '-p']).global, false);
  assert.equal(parseArgs(['install', '-p', '-g']).global, true);
});

test('parseArgs flags --help and -h anywhere, and --version', () => {
  assert.equal(parseArgs(['install', '--help']).help, true);
  assert.equal(parseArgs(['-h']).help, true);
  assert.equal(parseArgs(['list', '-h']).help, true);
  assert.equal(parseArgs(['install', '--skill', 'x', '--help']).help, true);
  assert.equal(parseArgs(['audit-overlap', '--top', '3', '-h']).help, true);
  assert.equal(parseArgs(['--version']).version, true);
  assert.equal(parseArgs(['install']).help, false);
});

test('parseArgs rejects unknown commands and options', () => {
  usage(['instal'], /Unknown command "instal"/);
  usage(['install', '--globl'], /Unknown option "--globl"/);
  usage(['install', '--skill=x', '--force'], /Unknown option "--force"/);
  usage(['--global', 'install'], /Put the command first/);
});

test('parseArgs rejects a bare word instead of silently installing everything', () => {
  usage(['install', 'content-copy-humanizer'], /Unexpected argument.*--skill content-copy-humanizer/);
  usage(['list', 'extra'], /Unexpected argument "extra"/);
});

test('parseArgs rejects options with a missing value', () => {
  usage(['install', '--skill'], /"--skill" needs a value/);
  usage(['install', '--skill', '--global'], /"--skill" needs a value/);
  usage(['install', '--agent='], /"--agent" needs a value/);
  usage(['install', '--global=yes'], /does not take a value/);
});

test('parseArgs rejects options that do not apply to the command', () => {
  usage(['list', '--global'], /only with "--installed"/);
  usage(['remove', '--upgrade', '-s', 'x'], /not valid with "remove"/);
  usage(['remove', '--source-url', 'u', '-s', 'x'], /not valid with "remove"/);
  usage(['upgrade', '--delete-env'], /not valid with "upgrade"/);
  usage(['install', '--full'], /not valid with "install"/);
  usage(['upgrade', '--upgrade'], /not valid with "upgrade"/);
});

test('parseArgs rejects --overwrite without --upgrade on install', () => {
  usage(['install', '--overwrite'], /only applies with "--upgrade"/);
  assert.equal(parseArgs(['upgrade', '--overwrite']).overwrite, true);
});

test('parseArgs rejects --source-ref without --source-url', () => {
  usage(['list', '--source-ref', 'main'], /needs "--source-url"/);
});

test('parseArgs passes audit-overlap options through untouched', () => {
  assert.deepEqual(parseArgs(['audit-overlap', '-t', '0.3', '-o', 'out']).rest, ['-t', '0.3', '-o', 'out']);
});

test('parseArgs requires a selection for remove', () => {
  usage(['remove'], /needs --skill or --plugin/);
  usage(['remove', '-g', '-y'], /needs --skill or --plugin/);
  const args = parseArgs(['remove', '-s', 'a', '-g', '-y']);
  assert.deepEqual([args.skills, args.global, args.overwrite], [['a'], true, true]);
});

test('parseArgs accepts --yes as the confirmation skip and --installed for list', () => {
  assert.equal(parseArgs(['upgrade', '--yes']).overwrite, true);
  assert.equal(parseArgs(['install', '-u', '-y']).overwrite, true);
  const args = parseArgs(['list', '--installed', '-g', '-a', 'claude']);
  assert.deepEqual([args.installed, args.global, args.agents], [true, true, ['claude']]);
});
