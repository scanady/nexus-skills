const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');

const {
  MANIFEST_KEYS,
  listPluginNames,
  loadPluginPackage,
  matchSkills,
  resolvePluginSkills
} = require('../src/core/plugins');

function writePackage(root, name, manifest, skills, mcp) {
  const dir = path.join(root, name);
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, 'plugin.json'), JSON.stringify(manifest));
  fs.writeFileSync(path.join(dir, 'skills.json'), JSON.stringify({ skills }));
  if (mcp) fs.writeFileSync(path.join(dir, 'mcp.json'), JSON.stringify(mcp));
  return dir;
}

function tempPackagesDir() {
  return fs.mkdtempSync(path.join(os.tmpdir(), 'nexus-plugins-'));
}

test('matchSkills expands exact names and prefix patterns', () => {
  const available = [
    'content-copy-humanizer',
    'content-technical-doc-coauthoring',
    'marketing-content-engine',
    'research-analyst'
  ];

  assert.deepEqual(matchSkills(['content-*'], available), [
    'content-copy-humanizer',
    'content-technical-doc-coauthoring'
  ]);
  assert.deepEqual(matchSkills(['research-analyst'], available), ['research-analyst']);
  assert.deepEqual(matchSkills(['does-not-exist'], available), []);
});

test('matchSkills deduplicates skills claimed by several patterns', () => {
  const available = ['content-copy-humanizer', 'content-meta-design'];
  assert.deepEqual(matchSkills(['content-*', 'content-copy-humanizer'], available), [
    'content-copy-humanizer',
    'content-meta-design'
  ]);
});

test('loadPluginPackage reads the manifest, membership, and optional mcp.json', () => {
  const root = tempPackagesDir();
  writePackage(root, 'demo', { name: 'nexus-demo', version: '1.0.0', description: 'Demo.' }, ['a-skill']);
  writePackage(
    root,
    'served',
    { name: 'nexus-served', version: '1.0.0', description: 'Served.' },
    ['b-skill'],
    { mcpServers: { example: { type: 'stdio', command: 'npx' } } }
  );

  const demo = loadPluginPackage('demo', root);
  assert.equal(demo.manifest.name, 'nexus-demo');
  assert.deepEqual(demo.patterns, ['a-skill']);
  assert.equal(demo.mcp, null);

  const served = loadPluginPackage('served', root);
  assert.deepEqual(Object.keys(served.mcp.mcpServers), ['example']);

  assert.deepEqual(listPluginNames(root), ['demo', 'served']);
});

test('loadPluginPackage returns null for a directory missing either file', () => {
  const root = tempPackagesDir();
  fs.mkdirSync(path.join(root, 'incomplete'));
  fs.writeFileSync(path.join(root, 'incomplete', 'plugin.json'), '{"name":"nexus-incomplete"}');

  assert.equal(loadPluginPackage('incomplete', root), null);
  assert.equal(loadPluginPackage('absent', root), null);
});

test('resolvePluginSkills merges the skills of several plugins', () => {
  const root = tempPackagesDir();
  writePackage(root, 'one', { name: 'nexus-one' }, ['alpha', 'shared']);
  writePackage(root, 'two', { name: 'nexus-two' }, ['beta', 'shared']);

  const resolved = resolvePluginSkills(['one', 'two'], ['alpha', 'beta', 'shared'], root);
  assert.deepEqual(resolved.sort(), ['alpha', 'beta', 'shared']);
});

test('resolvePluginSkills skips unknown plugins without throwing', () => {
  const root = tempPackagesDir();
  writePackage(root, 'one', { name: 'nexus-one' }, ['alpha']);

  assert.deepEqual(resolvePluginSkills(['one', 'nope'], ['alpha'], root), ['alpha']);
});

test('every shipped plugin package matches the closed Agent Plugins schema', () => {
  for (const name of listPluginNames()) {
    const pkg = loadPluginPackage(name);
    assert.ok(pkg, `${name} should be a readable plugin package`);
    assert.equal(pkg.manifest.name, `nexus-${name}`);
    assert.ok(pkg.manifest.description, `${name} should declare a description`);
    assert.ok(pkg.patterns.length > 0, `${name} should claim at least one skill`);

    const unknown = Object.keys(pkg.manifest).filter(key => !MANIFEST_KEYS.includes(key));
    assert.deepEqual(unknown, [], `${name} manifest has forbidden keys`);
  }
});
