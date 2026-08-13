const fs = require('fs');
const path = require('path');
const { PROJECT_ROOT } = require('./skills');

const PACKAGES_DIR = path.join(PROJECT_ROOT, 'plugin-packages');

// agent-plugins.org plugin.schema.json sets additionalProperties: false, so a
// package manifest may only carry these keys.
const MANIFEST_KEYS = [
  '$schema', 'name', 'version', 'description',
  'author', 'homepage', 'repository', 'license', 'keywords', 'extensions'
];

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
  MANIFEST_KEYS,
  listPluginNames,
  loadPluginPackage,
  loadPluginPackages,
  matchSkills,
  resolvePluginSkills
};
