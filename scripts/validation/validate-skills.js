#!/usr/bin/env node
/*
 * validate-skills.js
 *
 * Validates every skill in skills/ against the Agent Skills spec
 * (frontmatter, naming, description length, required files), then validates
 * the plugin packages in plugin-packages/ and their skill membership.
 * Exits non-zero if any errors are found. Warnings do not fail the build.
 *
 * Usage:
 *   node scripts/validation/validate-skills.js                  ← validate all skills
 *   node scripts/validation/validate-skills.js <skill-name>...  ← validate specific skills
 *   node scripts/validation/validate-skills.js --strict         ← treat warnings as errors
 */

const fs = require('fs');
const path = require('path');
const { SKILLS_DIR, getAvailableSkills, validateSkillStructure } = require('../../src/core/skills');
const {
  PACKAGES_DIR,
  PLUGIN_SCHEMA,
  MCP_SCHEMA,
  MANIFEST_KEYS,
  MANIFEST_REQUIRED,
  NAME_PATTERN,
  validateMcpServer,
  listPluginNames,
  loadPluginPackage,
  matchSkills
} = require('../../src/core/plugins');

function parseArgs(argv) {
  const args = { strict: false, skills: [] };
  for (const a of argv) {
    if (a === '--strict') args.strict = true;
    else if (!a.startsWith('-')) args.skills.push(a);
  }
  return args;
}

/*
 * Validates plugin-packages/. Every skill must belong to at least one plugin —
 * a skill in no plugin ships in no bundle at all, which is how membership
 * silently drifted before. Manifests are checked against the closed Agent
 * Plugins schema so a bundle can never be built with a forbidden key.
 */
function validatePluginPackages(availableSkills) {
  const errors = [];
  const report = [];
  const claimed = new Set();

  const names = listPluginNames();
  if (names.length === 0) {
    return { errors: [`no plugin packages found in ${path.relative(process.cwd(), PACKAGES_DIR)}/`], report };
  }

  for (const name of names) {
    const pkg = loadPluginPackage(name);
    if (!pkg) {
      errors.push(`${name}: needs a readable plugin.json and skills.json`);
      report.push(`❌ ${name}`);
      continue;
    }

    const issues = [];
    const { manifest } = pkg;

    // plugin.schema.json requires $schema and name, and closes the key set.
    for (const field of MANIFEST_REQUIRED) {
      if (!manifest[field]) issues.push(`plugin.json is missing "${field}"`);
    }
    if (manifest.$schema && manifest.$schema !== PLUGIN_SCHEMA) {
      issues.push(`plugin.json $schema must be "${PLUGIN_SCHEMA}"`);
    }

    // Not required by the schema, but every package in this repo carries them.
    for (const field of ['version', 'description']) {
      if (!manifest[field]) issues.push(`plugin.json is missing "${field}"`);
    }

    const unknown = Object.keys(manifest).filter(k => !MANIFEST_KEYS.includes(k));
    if (unknown.length > 0) {
      issues.push(`plugin.json has keys the Agent Plugins schema forbids: ${unknown.join(', ')}`);
    }

    if (manifest.name && !NAME_PATTERN.test(manifest.name)) {
      issues.push(`plugin.json name "${manifest.name}" does not match the Agent Plugins name pattern`);
    }
    if (manifest.name && manifest.name.length > 64) {
      issues.push(`plugin.json name "${manifest.name}" exceeds the 64-character limit`);
    }
    if (manifest.name && manifest.name !== `nexus-${name}`) {
      issues.push(`plugin.json name "${manifest.name}" does not match the directory (expected "nexus-${name}")`);
    }

    // mcp.schema.json requires both $schema and mcpServers. Every plugin here
    // carries an mcp.json, empty until it declares a server.
    if (!pkg.mcp) {
      issues.push('missing mcp.json (start from an empty { "mcpServers": {} } stub)');
    } else {
      if (pkg.mcp.$schema !== MCP_SCHEMA) {
        issues.push(`mcp.json $schema must be "${MCP_SCHEMA}"`);
      }
      if (!pkg.mcp.mcpServers) {
        issues.push('mcp.json is missing "mcpServers"');
      } else {
        const forbidden = Object.keys(pkg.mcp).filter(k => k !== '$schema' && k !== 'mcpServers');
        if (forbidden.length > 0) {
          issues.push(`mcp.json has keys the Agent Plugins schema forbids: ${forbidden.join(', ')}`);
        }
        for (const [server, config] of Object.entries(pkg.mcp.mcpServers)) {
          issues.push(...validateMcpServer(server, config));
        }
      }
    }

    if (pkg.patterns.length === 0) {
      issues.push('skills.json lists no skills');
    }

    for (const pattern of pkg.patterns) {
      const matched = matchSkills([pattern], availableSkills);
      if (matched.length === 0) {
        issues.push(`skills.json entry "${pattern}" matches no skill`);
      }
      matched.forEach(skill => claimed.add(skill));
    }

    if (issues.length === 0) {
      report.push(`✅ ${name} (${matchSkills(pkg.patterns, availableSkills).length} skills)`);
    } else {
      errors.push(...issues.map(i => `${name}: ${i}`));
      report.push(`❌ ${name}`);
      issues.forEach(i => report.push(`     · ${i}`));
    }
  }

  const unassigned = availableSkills.filter(skill => !claimed.has(skill));
  if (unassigned.length > 0) {
    report.push(`❌ ${unassigned.length} skill(s) belong to no plugin`);
    unassigned.forEach(skill => report.push(`     · ${skill}`));
    errors.push(...unassigned.map(skill => `${skill}: belongs to no plugin package`));
  }

  return { errors, report };
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const all = getAvailableSkills();
  const target = args.skills.length > 0 ? args.skills : all;

  let errors = 0;
  let warnings = 0;
  const report = [];

  for (const name of target) {
    const skillPath = path.join(SKILLS_DIR, name);
    if (!fs.existsSync(skillPath)) {
      console.log(`❌ ${name}: skill folder not found`);
      errors++;
      continue;
    }
    const result = validateSkillStructure(skillPath);
    if (result.errors.length === 0 && result.warnings.length === 0) {
      report.push(`✅ ${name}`);
      continue;
    }
    if (result.errors.length > 0) {
      errors += result.errors.length;
      report.push(`❌ ${name}`);
      for (const e of result.errors) report.push(`     · ${e}`);
    }
    if (result.warnings.length > 0) {
      warnings += result.warnings.length;
      if (result.errors.length === 0) report.push(`⚠️  ${name}`);
      for (const w of result.warnings) report.push(`     · ${w}`);
    }
  }

  console.log(report.join('\n'));
  console.log(`\nValidated ${target.length} skills — ${errors} error(s), ${warnings} warning(s)`);

  // Membership only makes sense over the whole set, so skip it for a subset run.
  if (args.skills.length === 0) {
    const plugins = validatePluginPackages(all);
    console.log(`\n${plugins.report.join('\n')}`);
    console.log(`\nValidated ${listPluginNames().length} plugin packages — ${plugins.errors.length} error(s)`);
    errors += plugins.errors.length;
  }

  if (errors > 0 || (args.strict && warnings > 0)) {
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}
