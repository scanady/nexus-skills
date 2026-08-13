const test = require('node:test');
const assert = require('node:assert/strict');

const { parseArgs } = require('../src/cli/args');

test('parseArgs defaults to install target agent skills for project scope', () => {
  assert.deepEqual(parseArgs(['install']), {
    command: 'install',
    skills: [],
    plugins: [],
    agents: ['agent-skills'],
    global: false,
    listMode: 'bare',
    upgrade: false,
    overwrite: false,
    sourceUrl: '',
    sourceRef: ''
  });
});

test('parseArgs collects repeatable skills, plugins, and agents', () => {
  const args = parseArgs([
    'install',
    '--skill', 'content-copy-humanizer',
    '-s', 'research-analyst',
    '--plugin', 'marketing',
    '-P', 'tech',
    '--agent', 'github-copilot',
    '-a', 'claude-code',
    '--global',
    '--upgrade',
    '--overwrite',
    '--source-url', 'https://github.com/scanady/nexus-skills.git',
    '--source-ref', 'main'
  ]);

  assert.deepEqual(args, {
    command: 'install',
    skills: ['content-copy-humanizer', 'research-analyst'],
    plugins: ['marketing', 'tech'],
    agents: ['github-copilot', 'claude-code'],
    global: true,
    listMode: 'bare',
    upgrade: true,
    overwrite: true,
    sourceUrl: 'https://github.com/scanady/nexus-skills.git',
    sourceRef: 'main'
  });
});

test('parseArgs still accepts the deprecated --pack alias', () => {
  assert.deepEqual(parseArgs(['install', '--pack', 'marketing']).plugins, ['marketing']);
});

test('parseArgs supports list output modes', () => {
  assert.equal(parseArgs(['list', '--full']).listMode, 'full');
  assert.equal(parseArgs(['list', '--count']).listMode, 'count');
  assert.equal(parseArgs(['list', '--names']).listMode, 'bare');
});
