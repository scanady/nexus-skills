#!/usr/bin/env node
/*
 * validate-skills.js
 *
 * Validates every skill in skills/ against the Agent Skills spec
 * (frontmatter, naming, description length, required files).
 * Exits non-zero if any errors are found. Warnings do not fail the build.
 *
 * Usage:
 *   node bin/validate-skills.js                  ← validate all skills
 *   node bin/validate-skills.js <skill-name>...  ← validate specific skills
 *   node bin/validate-skills.js --strict         ← treat warnings as errors
 */

const fs = require('fs');
const path = require('path');
const { SKILLS_DIR, getAvailableSkills, validateSkillStructure } = require('./skills-core');

function parseArgs(argv) {
  const args = { strict: false, skills: [] };
  for (const a of argv) {
    if (a === '--strict') args.strict = true;
    else if (!a.startsWith('-')) args.skills.push(a);
  }
  return args;
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

  if (errors > 0 || (args.strict && warnings > 0)) {
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}
