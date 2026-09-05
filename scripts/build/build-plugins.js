#!/usr/bin/env node
/*
 * build-plugins.js
 *
 * Builds the plugin distribution from plugin-packages/ and skills/.
 *
 * plugin-packages/ is the single source of truth for plugin packages. Nothing
 * about a plugin is authored anywhere else, and nothing generated from it is
 * committed — the whole distribution is rebuilt into dist/.
 *
 * Inputs:
 *   plugin-packages/<name>/plugin.json   ← Agent Plugins manifest fields (spec keys only)
 *   plugin-packages/<name>/skills.json   ← build-only membership list, never shipped
 *   plugin-packages/<name>/mcp.json      ← MCP servers, spec-shaped; an empty stub ships nothing
 *
 * Outputs:
 *   dist/plugins/<name>/plugin.json            ← Agent Plugins (agent-plugins.org) v1.0.0 manifest, plugin root
 *   dist/plugins/<name>/mcp.json               ← Agent Plugins MCP config (only when servers are declared)
 *   dist/plugins/<name>/skills/<skill>/...     ← self-contained plugin bundle (for zip distribution)
 *   dist/plugins/<name>/README.md              ← per-bundle install notes
 *   dist/plugins/manifest.json                 ← machine-readable index of every package
 *
 * The per-plugin bundles are standalone, portable packages following the Agent
 * Plugins specification (https://agent-plugins.org/) v1.0.0: plugin.json sits
 * at the plugin root (no .claude-plugin/ wrapper), declares $schema, and skills
 * are discovered from the skills/ directory rather than listed in the manifest.
 * That manifest schema is closed, so membership lives in the build-only
 * skills.json and MCP servers live in mcp.json — the spec location, and the
 * only one this repo writes. The dist/ tree is the source for the per-plugin
 * zips published to GitHub Pages.
 *
 * dist/plugins/manifest.json is the machine-readable projection of
 * plugin-packages/. It carries every authored field — description, version,
 * keywords, membership patterns, resolved skills, and MCP servers — so
 * downstream tools (the site builder, plugin-manager.html) never have to read
 * a lossy copy of the plugin definitions from somewhere else.
 *
 * Usage:
 *   node scripts/build/build-plugins.js
 */

const fs = require('fs');
const path = require('path');
const {
  PLUGIN_SCHEMA,
  MCP_SCHEMA,
  MANIFEST_KEYS,
  loadPluginPackages,
  matchSkills
} = require('../../src/core/plugins');

const ROOT = path.join(__dirname, '..', '..');
const SKILLS_DIR = path.join(ROOT, 'skills');
const DIST_DIR = path.join(ROOT, 'dist', 'plugins');


/** True when a package declares at least one MCP server (an empty stub does not). */
function hasServers(pkg) {
  return Boolean(pkg.mcp && pkg.mcp.mcpServers && Object.keys(pkg.mcp.mcpServers).length > 0);
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function writeJson(file, data) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, JSON.stringify(data, null, 2) + '\n', 'utf8');
}

function copyDir(src, dest) {
  fs.mkdirSync(dest, { recursive: true });
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const s = path.join(src, entry.name);
    const d = path.join(dest, entry.name);
    if (entry.isDirectory()) {
      copyDir(s, d);
    } else if (entry.isFile()) {
      fs.copyFileSync(s, d);
    }
  }
}

function rmDir(dir) {
  if (fs.existsSync(dir)) fs.rmSync(dir, { recursive: true, force: true });
}

function listSkills() {
  return fs.readdirSync(SKILLS_DIR)
    .filter(name => {
      const p = path.join(SKILLS_DIR, name);
      return fs.statSync(p).isDirectory() && fs.existsSync(path.join(p, 'SKILL.md'));
    })
    .sort();
}

function loadPackages() {
  const packages = loadPluginPackages();
  for (const pkg of packages) {
    const unknown = Object.keys(pkg.manifest).filter(k => !MANIFEST_KEYS.includes(k));
    if (unknown.length > 0) {
      throw new Error(`${pkg.dir}: plugin.json has keys the Agent Plugins schema forbids: ${unknown.join(', ')}`);
    }
  }
  return packages;
}

function rootPackage() {
  try {
    return readJson(path.join(ROOT, 'package.json'));
  } catch {
    return {};
  }
}

// Fields every bundle shares. A package manifest overrides any of them.
function repoDefaults(pkg) {
  const defaults = { $schema: PLUGIN_SCHEMA };
  if (pkg.author) defaults.author = { name: pkg.author };
  if (pkg.homepage) defaults.homepage = pkg.homepage;
  if (pkg.license) defaults.license = pkg.license;
  if (pkg.repository && pkg.repository.url) {
    defaults.repository = pkg.repository.url.replace(/^git\+/, '').replace(/\.git$/, '');
  }
  return defaults;
}

function buildBundle(pkg, skills, defaults, version) {
  const bundleDir = path.join(DIST_DIR, pkg.dir);
  rmDir(bundleDir);

  // plugin.json at the plugin root (Agent Plugins spec, agent-plugins.org v1.0.0).
  // Skills are discovered from the skills/ directory below, not listed here —
  // the spec's plugin.schema.json is closed and has no "skills" field.
  const manifest = { ...defaults, ...pkg.manifest, version: pkg.manifest.version || version };
  writeJson(path.join(bundleDir, 'plugin.json'), manifest);

  // MCP servers live in mcp.json, the Agent Plugins location and the only one
  // this repo writes. Empty stubs are templates for the author, so they are
  // not shipped — a bundle with no declared servers has no mcp.json.
  if (hasServers(pkg)) {
    writeJson(path.join(bundleDir, 'mcp.json'), {
      $schema: MCP_SCHEMA,
      mcpServers: pkg.mcp.mcpServers
    });
  }

  for (const skill of skills) {
    copyDir(path.join(SKILLS_DIR, skill), path.join(bundleDir, 'skills', skill));
  }

  const readme = [
    `# ${manifest.name}`,
    '',
    manifest.description,
    '',
    `## Skills (${skills.length})`,
    '',
    ...skills.map(s => `- \`${s}\``),
    ...(hasServers(pkg) ? ['', '## MCP servers', '', ...Object.keys(pkg.mcp.mcpServers).map(s => `- \`${s}\``)] : []),
    '',
    '## Install',
    '',
    'Drop this folder into your Claude Code plugins directory, or unzip and add it as a local plugin source.',
    ''
  ].join('\n');
  fs.writeFileSync(path.join(bundleDir, 'README.md'), readme, 'utf8');

  // Everything a downstream tool needs about this package, so none of them has
  // to re-read plugin-packages/ or fall back to a lossier copy elsewhere.
  return {
    name: pkg.dir,
    pluginName: manifest.name,
    description: manifest.description || '',
    version: manifest.version,
    keywords: manifest.keywords || [],
    patterns: pkg.patterns,
    skills,
    mcpServers: hasServers(pkg) ? pkg.mcp.mcpServers : {},
    path: path.relative(ROOT, bundleDir).split(path.sep).join('/')
  };
}

function main() {
  const rootPkg = rootPackage();
  const version = rootPkg.version || '0.0.0';
  const defaults = repoDefaults(rootPkg);
  const availableSkills = listSkills();
  const packages = loadPackages();

  console.log(`Building ${packages.length} plugins over ${availableSkills.length} skills…`);

  rmDir(DIST_DIR);
  const bundleManifest = [];

  for (const pkg of packages) {
    const skills = matchSkills(pkg.patterns, availableSkills);
    if (skills.length === 0) {
      console.log(`  ⚠️  ${pkg.dir}: no matching skills, skipped`);
      continue;
    }
    const summary = buildBundle(pkg, skills, defaults, version);
    bundleManifest.push(summary);
    const serverCount = Object.keys(summary.mcpServers).length;
    const mcpNote = serverCount > 0 ? `, ${serverCount} MCP server(s)` : '';
    console.log(`  ✅ ${summary.pluginName} (${skills.length} skills${mcpNote})`);
  }

  // The machine-readable projection of plugin-packages/, for the site builder
  // and plugin-manager.html.
  writeJson(path.join(DIST_DIR, 'manifest.json'), {
    generated_at: new Date().toISOString(),
    version,
    plugins: bundleManifest
  });

  console.log(`
Done. ${bundleManifest.length} bundle(s) in ${path.relative(ROOT, DIST_DIR)}/`);
}

if (require.main === module) {
  try {
    main();
  } catch (err) {
    console.error(`❌ ${err.message}`);
    process.exit(1);
  }
}

module.exports = { main };
