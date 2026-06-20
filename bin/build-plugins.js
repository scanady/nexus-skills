#!/usr/bin/env node
/*
 * build-plugins.js
 *
 * Regenerates the Claude plugin marketplace from packs/*.json and skills/.
 *
 * Outputs:
 *   .claude-plugin/marketplace.json            ← in-repo marketplace (one plugin per pack)
 *   .claude-plugin/plugin.json                 ← single "nexus-all" umbrella plugin (back-compat)
 *   dist/plugins/<pack>/.claude-plugin/plugin.json
 *   dist/plugins/<pack>/skills/<skill>/...     ← self-contained pack bundle (for zip distribution)
 *   dist/plugins/manifest.json                 ← machine-readable map for downstream tooling
 *
 * The in-repo marketplace.json is committed so that users can clone the repo
 * and add it directly as a Claude plugin marketplace. The dist/ tree is the
 * source for the per-pack zips published to GitHub Pages.
 *
 * Usage:
 *   node bin/build-plugins.js
 */

const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const SKILLS_DIR = path.join(ROOT, 'skills');
const PACKS_DIR = path.join(ROOT, 'packs');
const CLAUDE_PLUGIN_DIR = path.join(ROOT, '.claude-plugin');
const DIST_DIR = path.join(ROOT, 'dist', 'plugins');

const PLUGIN_PREFIX = 'nexus';
const MARKETPLACE_NAME = 'nexus-agents';
const MARKETPLACE_DESCRIPTION = 'Agentic skills, prompts, agents, and instructions for AI development platforms.';
const KEYWORDS = ['skills', 'prompts', 'agents', 'instructions', 'ai'];

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

function loadPacks() {
  return fs.readdirSync(PACKS_DIR)
    .filter(f => f.endsWith('.json'))
    .map(f => readJson(path.join(PACKS_DIR, f)))
    .sort((a, b) => a.name.localeCompare(b.name));
}

function resolvePack(pack, availableSkills) {
  const matched = new Set();
  for (const pattern of (pack.skills || [])) {
    if (pattern.endsWith('*')) {
      const prefix = pattern.slice(0, -1);
      availableSkills.filter(s => s.startsWith(prefix)).forEach(s => matched.add(s));
    } else if (availableSkills.includes(pattern)) {
      matched.add(pattern);
    }
  }
  return [...matched].sort();
}

function rootVersion() {
  try {
    return readJson(path.join(ROOT, 'package.json')).version || '0.0.0';
  } catch {
    return '0.0.0';
  }
}

function buildInRepoMarketplace(packs, availableSkills, version) {
  const plugins = [];

  // One plugin per pack
  for (const pack of packs) {
    const skills = resolvePack(pack, availableSkills);
    if (skills.length === 0) continue;
    plugins.push({
      name: `${PLUGIN_PREFIX}-${pack.name}`,
      description: pack.description,
      source: './',
      strict: false,
      version: pack.version || version,
      keywords: [...KEYWORDS, pack.name],
      skills: skills.map(s => `./skills/${s}`)
    });
  }

  // Umbrella plugin with every skill
  plugins.push({
    name: `${PLUGIN_PREFIX}-all`,
    description: 'All nexus skills (umbrella plugin).',
    source: './',
    strict: false,
    version,
    keywords: KEYWORDS,
    skills: availableSkills.map(s => `./skills/${s}`)
  });

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

function buildUmbrellaPluginJson(availableSkills, version) {
  return {
    name: MARKETPLACE_NAME,
    owner: { name: MARKETPLACE_NAME },
    metadata: {
      description: MARKETPLACE_DESCRIPTION,
      version
    },
    plugins: [
      {
        name: `${PLUGIN_PREFIX}-all`,
        description: 'All nexus skills (umbrella plugin).',
        source: './',
        strict: false,
        version,
        keywords: KEYWORDS,
        skills: availableSkills.map(s => `./skills/${s}`)
      }
    ]
  };
}

function buildPackBundle(pack, skills, version) {
  const packDir = path.join(DIST_DIR, pack.name);
  rmDir(packDir);

  // .claude-plugin/plugin.json (self-contained: skills live under ./skills/)
  const pluginManifest = {
    name: `${PLUGIN_PREFIX}-${pack.name}`,
    description: pack.description,
    version: pack.version || version,
    keywords: [...KEYWORDS, pack.name],
    skills: skills.map(s => `./skills/${s}`)
  };
  writeJson(path.join(packDir, '.claude-plugin', 'plugin.json'), pluginManifest);

  // Copy each skill folder into the bundle
  for (const skill of skills) {
    copyDir(path.join(SKILLS_DIR, skill), path.join(packDir, 'skills', skill));
  }

  // README inside the bundle
  const readme = [
    `# ${PLUGIN_PREFIX}-${pack.name}`,
    '',
    pack.description,
    '',
    `## Skills (${skills.length})`,
    '',
    ...skills.map(s => `- \`${s}\``),
    '',
    '## Install',
    '',
    'Drop this folder into your Claude Code plugins directory, or unzip and add it as a local plugin source.',
    ''
  ].join('\n');
  fs.writeFileSync(path.join(packDir, 'README.md'), readme, 'utf8');

  return { name: pack.name, pluginName: pluginManifest.name, skills, path: path.relative(ROOT, packDir) };
}

function main() {
  const version = rootVersion();
  const availableSkills = listSkills();
  const packs = loadPacks();

  console.log(`Building plugins from ${packs.length} packs over ${availableSkills.length} skills…`);

  // 1. In-repo marketplace (committed)
  const marketplace = buildInRepoMarketplace(packs, availableSkills, version);
  writeJson(path.join(CLAUDE_PLUGIN_DIR, 'marketplace.json'), marketplace);

  // 2. Back-compat umbrella plugin.json (committed)
  const umbrella = buildUmbrellaPluginJson(availableSkills, version);
  writeJson(path.join(CLAUDE_PLUGIN_DIR, 'plugin.json'), umbrella);

  // 3. Per-pack self-contained bundles (dist/, gitignored, for site/zip distribution)
  rmDir(DIST_DIR);
  const bundleManifest = [];
  for (const pack of packs) {
    const skills = resolvePack(pack, availableSkills);
    if (skills.length === 0) {
      console.log(`  ⚠️  ${pack.name}: no matching skills, skipped`);
      continue;
    }
    const summary = buildPackBundle(pack, skills, version);
    bundleManifest.push(summary);
    console.log(`  ✅ ${summary.pluginName} (${skills.length} skills)`);
  }

  // 4. Manifest for downstream tooling (site builder, install instructions)
  writeJson(path.join(DIST_DIR, 'manifest.json'), {
    generated_at: new Date().toISOString(),
    version,
    marketplace_name: MARKETPLACE_NAME,
    plugin_prefix: PLUGIN_PREFIX,
    packs: bundleManifest
  });

  console.log(`\nDone. Marketplace: ${marketplace.plugins.length} plugins. Bundles: ${bundleManifest.length} in ${path.relative(ROOT, DIST_DIR)}/`);
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
