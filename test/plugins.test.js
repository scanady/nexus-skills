const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');

const {
  PLUGIN_SCHEMA,
  MCP_SCHEMA,
  MANIFEST_KEYS,
  MANIFEST_REQUIRED,
  NAME_PATTERN,
  validateMcpServer,
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

// plugin.schema.json requires $schema and name; mcp.schema.json requires
// $schema and mcpServers. The build injects neither any more, so the authored
// files have to satisfy both on their own.
test('every authored plugin.json declares the required Agent Plugins fields', () => {
  for (const name of listPluginNames()) {
    const { manifest } = loadPluginPackage(name);
    for (const field of MANIFEST_REQUIRED) {
      assert.ok(manifest[field], `${name} plugin.json is missing "${field}"`);
    }
    assert.equal(manifest.$schema, PLUGIN_SCHEMA, `${name} plugin.json has the wrong $schema`);
    assert.ok(NAME_PATTERN.test(manifest.name), `${name} plugin.json name breaks the spec pattern`);
    assert.ok(manifest.name.length <= 64, `${name} plugin.json name exceeds 64 characters`);
  }
});

test('every authored mcp.json matches the closed Agent Plugins MCP schema', () => {
  for (const name of listPluginNames()) {
    const { mcp } = loadPluginPackage(name);
    assert.ok(mcp, `${name} should carry an mcp.json`);
    assert.equal(mcp.$schema, MCP_SCHEMA, `${name} mcp.json has the wrong $schema`);
    assert.ok(mcp.mcpServers, `${name} mcp.json is missing "mcpServers"`);

    const forbidden = Object.keys(mcp).filter(k => k !== '$schema' && k !== 'mcpServers');
    assert.deepEqual(forbidden, [], `${name} mcp.json has forbidden keys`);

    for (const [server, config] of Object.entries(mcp.mcpServers)) {
      assert.deepEqual(validateMcpServer(server, config), [], `${name} declares an invalid server`);
    }
  }
});

test('validateMcpServer accepts each transport the MCP schema defines', () => {
  assert.deepEqual(validateMcpServer('a', { type: 'stdio', command: 'npx', args: ['x'] }), []);
  assert.deepEqual(validateMcpServer('b', { type: 'streamable-http', url: 'https://example.com' }), []);
  assert.deepEqual(validateMcpServer('c', { type: 'sse', url: 'https://example.com' }), []);
  assert.deepEqual(validateMcpServer('d', { type: 'stdio', command: 'npx', cwd: '${PLUGIN_ROOT}/bin' }), []);
});

test('validateMcpServer rejects what the MCP schema forbids', () => {
  const cases = [
    [{ type: 'stdio' }, 'stdio without a command'],
    [{ type: 'websocket', url: 'wss://x' }, 'an unknown transport'],
    [{ type: 'sse', url: 'https://x', command: 'npx' }, 'a key the transport forbids'],
    [{ type: 'stdio', command: 'npx', env: { PLUGIN_ROOT: '/tmp' } }, 'a reserved env name'],
    [{ type: 'stdio', command: 'npx', cwd: '/etc' }, 'a cwd escaping the plugin root']
  ];
  for (const [server, label] of cases) {
    assert.ok(validateMcpServer('x', server).length > 0, `should reject ${label}`);
  }
});
