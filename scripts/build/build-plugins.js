#!/usr/bin/env node
/*
 * build-plugins.js
 *
 * Regenerates the Claude plugin marketplace from plugin-packages/ and skills/.
 *
 * Inputs:
 *   plugin-packages/<name>/plugin.json   ← Agent Plugins manifest fields (spec keys only)
 *   plugin-packages/<name>/skills.json   ← build-only membership list, never shipped
 *   plugin-packages/<name>/mcp.json      ← MCP servers, spec-shaped; an empty stub ships nothing
 *
 * Outputs:
 *   .claude-plugin/marketplace.json            ← in-repo marketplace (one plugin per package, Claude Code CLI format)
 *   .claude-plugin/plugin.json                 ← single "nexus-all" umbrella plugin (back-compat, Claude Code CLI format)
 *   dist/plugins/<name>/plugin.json            ← Agent Plugins (agent-plugins.org) v1.0.0 manifest, plugin root
 *   dist/plugins/<name>/mcp.json               ← Agent Plugins MCP config (only when servers are declared)
 *   dist/plugins/<name>/skills/<skill>/...     ← self-contained plugin bundle (for zip distribution)
 *   dist/plugins/manifest.json                 ← machine-readable map for downstream tooling
 *
 * The in-repo marketplace.json is committed so that users can clone the repo
 * and add it directly as a Claude plugin marketplace. That marketplace format
 * (and the back-compat umbrella plugin.json) is a Claude Code CLI mechanism
 * with no equivalent in the Agent Plugins spec, so both stay at their
 * existing `.claude-plugin/` location.
 *
 * The per-plugin bundles in dist/ are standalone, portable packages following
 * the Agent Plugins specification (https://agent-plugins.org/) v1.0.0:
 * plugin.json sits at the plugin root (no .claude-plugin/ wrapper), declares
 * $schema, and skills are discovered from the skills/ directory rather than
 * listed in the manifest. That manifest schema is closed, so membership lives
 * in the build-only skills.json and MCP servers live in mcp.json — the spec
 * location, and the only one this repo writes. Claude Code reads those servers
 * from the inlined mcpServers on the marketplace entry. The dist/ tree is the
 * source for the per-plugin zips published to GitHub Pages.
 *
 * Usage:
 *   node scripts/build/build-plugins.js
 */

const fs = require('fs');
const path = require('path');
const { MANIFEST_KEYS, loadPluginPackages, matchSkills } = require('../../src/core/plugins');

const ROOT = path.join(__dirname, '..', '..');
const SKILLS_DIR = path.join(ROOT, 'skills');
const CLAUDE_PLUGIN_DIR = path.join(ROOT, '.claude-plugin');
const DIST_DIR = path.join(ROOT, 'dist', 'plugins');

const PLUGIN_PREFIX = 'nexus';
const MARKETPLACE_NAME = 'nexus-agents';
const AGENT_PLUGINS_SCHEMA = 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json';
const AGENT_PLUGINS_MCP_SCHEMA = 'https://agent-plugins.org/schemas/1.0.0/mcp.schema.json';
const MARKETPLACE_DESCRIPTION = 'Agentic skills, prompts, agents, and instructions for AI development platforms.';
const KEYWORDS = ['skills', 'prompts', 'agents', 'instructions', 'ai'];

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
  const defaults = { $schema: AGENT_PLUGINS_SCHEMA };
  if (pkg.author) defaults.author = { name: pkg.author };
  if (pkg.homepage) defaults.homepage = pkg.homepage;
  if (pkg.license) defaults.license = pkg.license;
  if (pkg.repository && pkg.repository.url) {
    defaults.repository = pkg.repository.url.replace(/^git\+/, '').replace(/\.git$/, '');
  }
  return defaults;
}

function marketplaceEntry(pkg, skills, version) {
  const entry = {
    name: pkg.manifest.name,
    description: pkg.manifest.description,
    source: './',
    strict: false,
    version: pkg.manifest.version || version,
    keywords: pkg.manifest.keywords || KEYWORDS,
    skills: skills.map(s => `./skills/${s}`)
  };
  // Claude Code accepts mcpServers inline on a marketplace entry, which is the
  // only way to attach servers to an entry whose source is the repo root.
  if (hasServers(pkg)) entry.mcpServers = pkg.mcp.mcpServers;
  return entry;
}

function umbrellaEntry(availableSkills, version) {
  return {
    name: `${PLUGIN_PREFIX}-all`,
    description: 'All nexus skills (umbrella plugin).',
    source: './',
    strict: false,
    version,
    keywords: KEYWORDS,
    skills: availableSkills.map(s => `./skills/${s}`)
  };
}

function marketplaceDocument(plugins, version) {
  return {
    name: MARKETPLACE_NAME,
    owner: { name: MARKETPLACE_NAME },
    metadata: {
      description: MARKETPLACE_DESCRIPTION,
      version
    },
    plugins
  };
}

function buildBundle(pkg, skills, defaults, version) {
  const bundleDir = path.join(DIST_DIR, pkg.dir);
  rmDir(bundleDir);

  // plugin.json at the plugin root (Agent Plugins spec, agent-plugins.org v1.0.0).
  // Skills are discovered from the skills/ directory below, not listed here —
  // the spec's plugin.schema.json is closed and has no "skills" field.
  const manifest = { ...defaults, ...pkg.manifest, version: pkg.manifest.version || version };
  writeJson(path.join(bundleDir, 'plugin.json'), manifest);

  // MCP servers live in mcp.json, the Agent Plugins location. Claude Code picks
  // them up from the inlined mcpServers on the marketplace entry instead.
  // Empty stubs are templates for the author, so they are not shipped.
  if (hasServers(pkg)) {
    writeJson(path.join(bundleDir, 'mcp.json'), { $schema: AGENT_PLUGINS_MCP_SCHEMA, ...pkg.mcp });
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

  return {
    name: pkg.dir,
    pluginName: manifest.name,
    skills,
    mcpServers: hasServers(pkg) ? Object.keys(pkg.mcp.mcpServers) : [],
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

  const entries = [];
  rmDir(DIST_DIR);
  const bundleManifest = [];

  for (const pkg of packages) {
    const skills = matchSkills(pkg.patterns, availableSkills);
    if (skills.length === 0) {
      console.log(`  ⚠️  ${pkg.dir}: no matching skills, skipped`);
      continue;
    }
    entries.push(marketplaceEntry(pkg, skills, version));
    const summary = buildBundle(pkg, skills, defaults, version);
    bundleManifest.push(summary);
    const mcpNote = summary.mcpServers.length > 0 ? `, ${summary.mcpServers.length} MCP server(s)` : '';
    console.log(`  ✅ ${summary.pluginName} (${skills.length} skills${mcpNote})`);
  }

  entries.push(umbrellaEntry(availableSkills, version));

  // 1. In-repo marketplace (committed)
  writeJson(path.join(CLAUDE_PLUGIN_DIR, 'marketplace.json'), marketplaceDocument(entries, version));

  // 2. Back-compat umbrella plugin.json (committed)
  writeJson(
    path.join(CLAUDE_PLUGIN_DIR, 'plugin.json'),
    marketplaceDocument([umbrellaEntry(availableSkills, version)], version)
  );

  // 3. Manifest for downstream tooling (site builder, install instructions)
  writeJson(path.join(DIST_DIR, 'manifest.json'), {
    generated_at: new Date().toISOString(),
    version,
    marketplace_name: MARKETPLACE_NAME,
    plugin_prefix: PLUGIN_PREFIX,
    plugins: bundleManifest
  });

  console.log(`\nDone. Marketplace: ${entries.length} plugins. Bundles: ${bundleManifest.length} in ${path.relative(ROOT, DIST_DIR)}/`);
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
