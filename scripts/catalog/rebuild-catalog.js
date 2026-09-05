#!/usr/bin/env node
/*
 * rebuild-catalog.js
 *
 * Rebuild skill-catalog.json by merging:
 *  - New scan results (skill-catalog-scan.json)
 *  - Old evaluations (skill-catalog.json)
 *  - Manually authored evaluations (skill-catalog-evaluations.json, optional)
 *  - Manually authored evaluations for new skills (evaluations/new-evaluations.json)
 *
 * Usage:
 *   node scripts/catalog/rebuild-catalog.js
 */

const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..', '..');
const SCAN_FILE = path.join(ROOT, 'skill-catalog-scan.json');
const OLD_CATALOG = path.join(ROOT, 'skill-catalog.json');
const OUT_FILE = path.join(ROOT, 'skill-catalog.json');
const EVALUATIONS_FILE = path.join(ROOT, 'skill-catalog-evaluations.json');
const NEW_EVALUATIONS_FILE = path.join(__dirname, 'new-evaluations.json');
const PACKAGES_DIR = path.join(ROOT, 'plugin-packages');

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

// ---------------------------------------------------------------------------
// Complexity and pattern classification helpers
// ---------------------------------------------------------------------------

function classifyComplexity(estimatedTokens) {
  if (estimatedTokens < 700) return 'compact';
  if (estimatedTokens < 2000) return 'detailed';
  return 'comprehensive';
}

function classifyPattern(hasScripts) {
  return hasScripts ? 'B' : 'A';
}

// ---------------------------------------------------------------------------
// Plugin helpers
// ---------------------------------------------------------------------------

/**
 * Load plugin membership from plugin-packages/, keyed by directory name.
 *
 * plugin-packages/ is the single source of truth for plugin packages, so the
 * catalog reads membership from it and copies nothing else. The plugin
 * definitions themselves (description, version, keywords, MCP servers) stay
 * where they are authored; `npm run build:plugins` projects them into
 * dist/plugins/manifest.json for tools that need them.
 */
function loadPlugins() {
  const plugins = {};
  if (!fs.existsSync(PACKAGES_DIR)) return plugins;

  const dirs = fs.readdirSync(PACKAGES_DIR, { withFileTypes: true })
    .filter(entry => entry.isDirectory())
    .map(entry => entry.name)
    .sort();

  for (const dir of dirs) {
    try {
      const membership = readJson(path.join(PACKAGES_DIR, dir, 'skills.json'));
      plugins[dir] = { skills: membership.skills || [] };
    } catch {
      continue;
    }
  }
  return plugins;
}

/** Return the sorted list of plugin names that claim this skill. */
function resolveSkillPlugins(skillName, plugins) {
  const result = [];
  for (const [pluginName, plugin] of Object.entries(plugins)) {
    for (const pattern of plugin.skills || []) {
      if (pattern.endsWith('*')) {
        if (skillName.startsWith(pattern.slice(0, -1))) {
          result.push(pluginName);
          break;
        }
      } else if (skillName === pattern) {
        result.push(pluginName);
        break;
      }
    }
  }
  return result.sort();
}

// ---------------------------------------------------------------------------
// Main rebuild logic
// ---------------------------------------------------------------------------

/**
 * Python's round(x, 2): half-to-even on the *exact* binary value of the double.
 *
 * Neither Math.round (half-up) nor toFixed (half-away-from-zero) matches, and
 * scaling by 100 first reintroduces the float error the rounding is supposed to
 * resolve — round(2.235, 2) is 2.23 in Python, because the stored double is
 * just below 2.235, yet 2.235 * 100 evaluates to 223.50000000000003.
 *
 * So decompose the double into mantissa and exponent and do the comparison in
 * exact integer arithmetic.
 */
function pyRound2(value) {
  if (!Number.isFinite(value) || value === 0) return value;

  const sign = value < 0 ? -1n : 1n;
  const buffer = new DataView(new ArrayBuffer(8));
  buffer.setFloat64(0, Math.abs(value));
  const bits = buffer.getBigUint64(0);
  const rawExponent = Number((bits >> 52n) & 0x7ffn);
  const rawMantissa = bits & 0xfffffffffffffn;

  // value = mantissa * 2**exponent, exactly.
  const mantissa = rawExponent === 0 ? rawMantissa : rawMantissa | 0x10000000000000n;
  const exponent = BigInt((rawExponent === 0 ? 1 : rawExponent) - 1075);

  // Round mantissa * 2**exponent * 100 to the nearest integer, ties to even.
  let numerator = mantissa * 100n;
  let denominator = 1n;
  if (exponent >= 0n) numerator <<= exponent;
  else denominator = 1n << -exponent;

  let quotient = numerator / denominator;
  const remainder = numerator % denominator;
  const twice = remainder * 2n;
  if (twice > denominator || (twice === denominator && quotient % 2n !== 0n)) quotient += 1n;

  return Number(sign * quotient) / 100;
}

/** Compute the average of a nested score field across all skills. */
function computeAvg(skills, keyPath) {
  const values = [];
  for (const skill of skills) {
    let node = skill.evaluation || {};
    for (const key of keyPath) {
      if (node && typeof node === 'object' && !Array.isArray(node)) node = node[key];
      else {
        node = undefined;
        break;
      }
    }
    if (typeof node === 'number' && Number.isFinite(node)) values.push(node);
  }
  if (values.length === 0) return 0.0;
  return pyRound2(values.reduce((a, b) => a + b, 0) / values.length);
}

function withoutGeneratedAt(catalog) {
  const comparable = { ...catalog };
  delete comparable.generated_at;
  return comparable;
}

/** Derive a mechanical security-risk summary from scan indicators. */
function deriveSecurityRisk(scanEntry, existingSecurity) {
  const indicators = scanEntry.external_indicators || {};
  const findings = [];
  if (indicators.credential_refs) findings.push('References credentials/secrets');
  if (indicators.network_calls) findings.push('Makes outbound network calls');
  if (indicators.exec_patterns) findings.push('Uses execution patterns');
  if (indicators.install_commands) findings.push('Uses install commands');

  let rating = 'low';
  if (findings.length > 0) rating = findings.length <= 2 ? 'medium' : 'high';

  const updated = { ...(existingSecurity || {}) };
  updated.rating = rating;
  updated.findings = findings;
  updated.rationale = findings.length > 0
    ? 'Evaluated from scanner signals.'
    : 'No obvious credential handling or risky execution patterns detected.';
  return updated;
}

const PLACEHOLDER_CAPABILITIES = new Set([
  '', 'Not evaluated', '>-.', '>.', 'Auto-generated from scan-only fallback.'
]);
const FILLER_CHARS = new Set(['>', '-', '.', ' ', '\t', '\n']);

/** Use the frontmatter description when evaluation text is missing or placeholder-like. */
function deriveCoreCapabilities(frontmatter, existingValue) {
  const description = (frontmatter || {}).description;
  if (!description) return existingValue || '';

  const normalized = (existingValue || '').trim();
  if (!normalized || PLACEHOLDER_CAPABILITIES.has(normalized)) return description;
  if ([...normalized].every(ch => FILLER_CHARS.has(ch))) return description;
  return existingValue || description;
}

function main() {
  // Load inputs
  const scanData = readJson(SCAN_FILE);
  const oldCatalog = readJson(OLD_CATALOG);

  // Load plugin packages
  const plugins = loadPlugins();

  // Load external evaluations file (highest priority)
  const freshEvals = {};
  if (fs.existsSync(EVALUATIONS_FILE)) {
    for (const entry of readJson(EVALUATIONS_FILE)) {
      freshEvals[entry.name] = entry.evaluation;
    }
  }

  // Manually authored evaluations for skills the old catalog does not cover
  const newEvaluations = fs.existsSync(NEW_EVALUATIONS_FILE) ? readJson(NEW_EVALUATIONS_FILE) : {};

  // Index old evaluations by skill name
  const oldEvals = {};
  for (const skill of oldCatalog.skills) oldEvals[skill.name] = skill;

  const skillsOut = [];
  let parseErrors = 0;

  for (const scanEntry of scanData.skills) {
    if ('error' in scanEntry) {
      parseErrors++;
      continue;
    }

    const name = scanEntry.name;
    const fm = scanEntry.frontmatter || {};
    let metadata = 'metadata' in fm ? fm.metadata : {};
    if (typeof metadata === 'string' || metadata === null || metadata === undefined) metadata = {};

    // Structure block — prefer old catalog values for complexity/pattern
    const rawStructure = scanEntry.structure || {};
    let complexity = rawStructure.complexity_class;
    let pattern = rawStructure.skill_pattern;

    if (name in oldEvals) {
      const oldStruct = oldEvals[name].structure || {};
      if (!complexity) {
        complexity = oldStruct.complexity_class || classifyComplexity(rawStructure.estimated_tokens || 0);
      }
      if (!pattern) {
        pattern = oldStruct.skill_pattern || classifyPattern(rawStructure.has_scripts || false);
      }
    } else {
      // New skill — compute from scan data
      complexity = classifyComplexity(rawStructure.estimated_tokens || 0);
      pattern = classifyPattern(rawStructure.has_scripts || false);
    }

    const structureBlock = {
      has_scripts: rawStructure.has_scripts || false,
      has_references: rawStructure.has_references || false,
      has_agents: rawStructure.has_agents || false,
      has_assets: rawStructure.has_assets || false,
      has_license_file: rawStructure.has_license_file || false,
      file_count: rawStructure.file_count || 0,
      estimated_tokens: rawStructure.estimated_tokens || 0,
      complexity_class: complexity,
      skill_pattern: pattern
    };

    // Evaluation priority: freshEvals > newEvaluations > oldEvals > placeholder
    let evaluation;
    if (name in freshEvals) {
      evaluation = { ...freshEvals[name] };
      // Refresh mechanical fields from scan
      evaluation.script_languages = scanEntry.script_languages || ['none'];
      evaluation.license = scanEntry.license || 'unspecified';
    } else if (name in newEvaluations) {
      evaluation = { ...newEvaluations[name] };
      // Override mechanically-extracted fields from scan
      evaluation.script_languages = scanEntry.script_languages || ['none'];
      evaluation.license = scanEntry.license || 'unspecified';
    } else if (name in oldEvals) {
      // Deliberately the old catalog's own object, not a copy. The Python
      // original aliased it too, and the generated_at comparison below depends
      // on the alias: a refreshed field shows up on both sides and so does not
      // count as a change.
      evaluation = oldEvals[name].evaluation || {};
      // Refresh mechanical fields and security risk from current scan results
      evaluation.script_languages = scanEntry.script_languages || ['none'];
      evaluation.license = scanEntry.license || 'unspecified';
      evaluation.security_risk = deriveSecurityRisk(scanEntry, evaluation.security_risk);
      evaluation.core_capabilities = deriveCoreCapabilities(fm, evaluation.core_capabilities);
    } else {
      evaluation = {
        usage_value: { score: 0, rationale: 'Not evaluated' },
        security_risk: deriveSecurityRisk(scanEntry, null),
        executability: { score: 0, rationale: 'Not evaluated' },
        invocability: { score: 0, rationale: 'Not evaluated' },
        over_specification_risk: { flagged: false, rationale: 'Not evaluated' },
        core_capabilities: deriveCoreCapabilities(fm, 'Not evaluated'),
        external_requirements_indicator: 'unknown',
        external_requirements: ['unknown'],
        script_languages: scanEntry.script_languages || ['none'],
        license: scanEntry.license || 'unspecified'
      };
    }

    skillsOut.push({
      name,
      disable_model_invocation: scanEntry.disable_model_invocation || false,
      source_id: 'source-1',
      path: scanEntry.path || '',
      url: null,
      plugins: resolveSkillPlugins(name, plugins),
      frontmatter: {
        name: nullable(fm.name),
        disable_model_invocation: scanEntry.disable_model_invocation || false,
        description: nullable(fm.description),
        license: nullable(fm.license),
        compatibility: nullable(fm.compatibility),
        allowed_tools: nullable(fm['allowed-tools']),
        metadata: {
          version: nullable(metadata.version),
          triggers: nullable(metadata.triggers),
          role: nullable(metadata.role),
          scope: nullable(metadata.scope),
          output_format: nullable(metadata['output-format'] || metadata.output_format),
          related_skills: nullable(metadata['related-skills'] || metadata.related_skills)
        }
      },
      structure: structureBlock,
      evaluation
    });
  }

  // ---------------------------------------------------------------------------
  // Summary statistics
  // ---------------------------------------------------------------------------
  const total = skillsOut.length;
  const evaluated = skillsOut.filter(s => ((s.evaluation.usage_value || {}).score || 0) > 0).length;
  const avgUsage = computeAvg(skillsOut, ['usage_value', 'score']);
  const avgExec = computeAvg(skillsOut, ['executability', 'score']);
  const avgInvoc = computeAvg(skillsOut, ['invocability', 'score']);

  const secDist = { low: 0, medium: 0, high: 0 };
  for (const skill of skillsOut) {
    const rating = (skill.evaluation.security_risk || {}).rating ?? 'unknown';
    if (rating in secDist) secDist[rating]++;
  }

  const complexityDist = { compact: 0, detailed: 0, comprehensive: 0 };
  for (const skill of skillsOut) {
    const cc = skill.structure.complexity_class ?? '';
    if (cc in complexityDist) complexityDist[cc]++;
  }

  const patternDist = { A: 0, B: 0, C: 0 };
  for (const skill of skillsOut) {
    const p = skill.structure.skill_pattern ?? '';
    if (p in patternDist) patternDist[p]++;
  }

  const overSpecFlagged = skillsOut
    .filter(s => (s.evaluation.over_specification_risk || {}).flagged || false).length;

  const nonEmptyPatternDist = {};
  for (const [k, v] of Object.entries(patternDist)) {
    if (v > 0) nonEmptyPatternDist[k] = v;
  }

  const catalog = {
    catalog_version: '1.0.0',
    generated_at: oldCatalog.generated_at ?? null,
    sources: [
      {
        id: 'source-1',
        type: 'local',
        path: 'skills',
        url: null,
        commit: null
      }
    ],
    summary: {
      total_skills: total,
      evaluated,
      parse_errors: parseErrors,
      avg_usage_value: avgUsage,
      avg_executability: avgExec,
      avg_invocability: avgInvoc,
      security_risk_distribution: secDist,
      complexity_distribution: complexityDist,
      pattern_distribution: nonEmptyPatternDist,
      over_specification_flagged: overSpecFlagged
    },
    skills: skillsOut
  };

  if (!catalog.generated_at || !deepEqual(withoutGeneratedAt(oldCatalog), withoutGeneratedAt(catalog))) {
    catalog.generated_at = new Date().toISOString().replace(/\.\d{3}Z$/, 'Z');
  }

  // No trailing newline: the Python original wrote none, and the catalog is a
  // committed artifact compared byte for byte.
  fs.writeFileSync(OUT_FILE, JSON.stringify(catalog, null, 2), 'utf8');

  console.log(`Catalog written: ${OUT_FILE}`);
  console.log(`  Total skills : ${total}`);
  console.log(`  Evaluated    : ${evaluated}`);
  console.log(`  Fresh evals  : ${Object.keys(freshEvals).length}`);
  console.log(`  Parse errors : ${parseErrors}`);
  console.log(`  Avg usage    : ${avgUsage}`);
  console.log(`  Avg exec     : ${avgExec}`);
  console.log(`  Security     : ${formatDict(secDist)}`);
  console.log(`  Complexity   : ${formatDict(complexityDist)}`);
  console.log(`  Over-spec    : ${overSpecFlagged}`);
}

/** Missing frontmatter keys become null in the catalog, as Python's .get() did. */
function nullable(value) {
  return value === undefined ? null : value;
}

/** Match the Python original's dict repr in the console summary. */
function formatDict(obj) {
  const body = Object.entries(obj).map(([k, v]) => `'${k}': ${v}`).join(', ');
  return `{${body}}`;
}

/** Structural equality, mirroring Python's == on nested dicts and lists. */
function deepEqual(a, b) {
  if (a === b) return true;
  if (typeof a !== typeof b) return false;
  if (a === null || b === null) return a === b;
  if (Array.isArray(a) || Array.isArray(b)) {
    if (!Array.isArray(a) || !Array.isArray(b) || a.length !== b.length) return false;
    return a.every((item, i) => deepEqual(item, b[i]));
  }
  if (typeof a === 'object') {
    const ka = Object.keys(a);
    const kb = Object.keys(b);
    if (ka.length !== kb.length) return false;
    return ka.every(k => Object.prototype.hasOwnProperty.call(b, k) && deepEqual(a[k], b[k]));
  }
  return false;
}

if (require.main === module) {
  main();
}

module.exports = {
  classifyComplexity,
  classifyPattern,
  loadPlugins,
  resolveSkillPlugins,
  computeAvg,
  pyRound2,
  deriveSecurityRisk,
  deriveCoreCapabilities,
  deepEqual,
  main
};
