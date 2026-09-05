const fs = require('fs');
const path = require('path');
const { PROJECT_ROOT } = require('./skills');

const PACKAGES_DIR = path.join(PROJECT_ROOT, 'plugin-packages');

// Agent Plugins 1.0.0 (https://agent-plugins.org/). Both schemas are closed
// (additionalProperties: false) and both require their $schema constant, so
// these values are the contract a package is checked against.
const PLUGIN_SCHEMA = 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json';
const MCP_SCHEMA = 'https://agent-plugins.org/schemas/1.0.0/mcp.schema.json';

// plugin.schema.json properties. $schema and name are the only required ones.
const MANIFEST_KEYS = [
  '$schema', 'name', 'version', 'description',
  'author', 'homepage', 'repository', 'license', 'keywords', 'extensions'
];
const MANIFEST_REQUIRED = ['$schema', 'name'];

// plugin.schema.json name pattern, verbatim.
const NAME_PATTERN = /^(?!.*(?:--|\.\.))[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$/;

// mcp.schema.json: one entry per transport, each closed, `type` always required.
const MCP_SERVER_SHAPES = {
  'stdio': { required: ['type', 'command'], allowed: ['type', 'command', 'args', 'env', 'cwd'] },
  'streamable-http': { required: ['type', 'url'], allowed: ['type', 'url', 'headers'] },
  'sse': { required: ['type', 'url'], allowed: ['type', 'url', 'headers'] }
};

// mcp.schema.json reserves these for the client to inject.
const RESERVED_ENV = ['PLUGIN_ROOT', 'PLUGIN_DATA'];

/**
 * Check one MCP server entry against mcp.schema.json's `server` definition.
 * Returns a list of human-readable problems; empty means valid.
 */
function validateMcpServer(name, server) {
  if (!server || typeof server !== 'object' || Array.isArray(server)) {
    return [`mcpServers."${name}" must be an object`];
  }

  const shape = MCP_SERVER_SHAPES[server.type];
  if (!shape) {
    return [`mcpServers."${name}" has type "${server.type}", not one of ${Object.keys(MCP_SERVER_SHAPES).join(', ')}`];
  }

  const issues = [];
  for (const field of shape.required) {
    if (typeof server[field] !== 'string' || server[field].length === 0) {
      issues.push(`mcpServers."${name}" is missing a non-empty "${field}"`);
    }
  }

  const unknown = Object.keys(server).filter(k => !shape.allowed.includes(k));
  if (unknown.length > 0) {
    issues.push(`mcpServers."${name}" has keys "${server.type}" forbids: ${unknown.join(', ')}`);
  }

  for (const key of Object.keys(server.env || {})) {
    if (RESERVED_ENV.includes(key)) {
      issues.push(`mcpServers."${name}" sets reserved env "${key}"`);
    }
  }

  // Plugin-relative paths must stay inside the package.
  if (server.cwd !== undefined && !/^(?:\.\/|\$\{PLUGIN_ROOT\}(?:\/|$)|\$\{PLUGIN_DATA\}(?:\/|$))/.test(server.cwd)) {
    issues.push(`mcpServers."${name}" cwd must start with ./, \${PLUGIN_ROOT}, or \${PLUGIN_DATA}`);
  }

  return issues;
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function listPluginNames(packagesDir = PACKAGES_DIR) {
  if (!fs.existsSync(packagesDir)) return [];
  return fs.readdirSync(packagesDir, { withFileTypes: true })
    .filter(entry => entry.isDirectory())
    .map(entry => entry.name)
    .sort();
}

/**
 * Load one plugin package: the Agent Plugins manifest, the build-only
 * membership list, and the optional MCP server config.
 * Returns null when the directory is not a readable package.
 */
function loadPluginPackage(name, packagesDir = PACKAGES_DIR) {
  const dir = path.join(packagesDir, name);
  const manifestFile = path.join(dir, 'plugin.json');
  const skillsFile = path.join(dir, 'skills.json');
  const mcpFile = path.join(dir, 'mcp.json');

  if (!fs.existsSync(manifestFile) || !fs.existsSync(skillsFile)) return null;

  try {
    return {
      dir: name,
      path: dir,
      manifest: readJson(manifestFile),
      patterns: readJson(skillsFile).skills || [],
      mcp: fs.existsSync(mcpFile) ? readJson(mcpFile) : null
    };
  } catch {
    return null;
  }
}

function loadPluginPackages(packagesDir = PACKAGES_DIR) {
  return listPluginNames(packagesDir)
    .map(name => loadPluginPackage(name, packagesDir))
    .filter(Boolean);
}

/** Expand a package's membership patterns (exact names, or a trailing `*` prefix). */
function matchSkills(patterns, availableSkills) {
  const matched = new Set();
  for (const pattern of patterns) {
    if (pattern.endsWith('*')) {
      const prefix = pattern.slice(0, -1);
      availableSkills.filter(skill => skill.startsWith(prefix)).forEach(skill => matched.add(skill));
    } else if (availableSkills.includes(pattern)) {
      matched.add(pattern);
    }
  }
  return [...matched].sort();
}

/** Resolve the skills named by one or more plugins, for `nxa install --plugin`. */
function resolvePluginSkills(pluginNames, availableSkills, packagesDir = PACKAGES_DIR) {
  const resolved = new Set();

  for (const name of pluginNames) {
    const pkg = loadPluginPackage(name, packagesDir);
    if (!pkg) {
      console.log(`  ⚠️  Plugin not found: ${name}`);
      continue;
    }
    matchSkills(pkg.patterns, availableSkills).forEach(skill => resolved.add(skill));
  }

  return [...resolved];
}

module.exports = {
  PACKAGES_DIR,
  PLUGIN_SCHEMA,
  MCP_SCHEMA,
  MANIFEST_KEYS,
  MANIFEST_REQUIRED,
  NAME_PATTERN,
  validateMcpServer,
  listPluginNames,
  loadPluginPackage,
  loadPluginPackages,
  matchSkills,
  resolvePluginSkills
};
