#!/usr/bin/env node
/*
 * scan-skills.js
 *
 * Scan a directory tree for Agent Skills (SKILL.md files) and extract
 * structural metadata without LLM involvement.
 *
 * Usage:
 *   node scripts/catalog/scan-skills.js <skills-directory> [--output results.json]
 *
 * Produces a JSON file with mechanical extraction results per skill:
 * frontmatter, directory structure, script languages, external service
 * indicators, and SKILL.md body excerpt.
 */

const fs = require('fs');
const path = require('path');

// ---------------------------------------------------------------------------
// Python-compatible primitives
//
// This file is a direct port of scan-skills.py. The catalog it feeds is a
// committed artifact, so these helpers reproduce the Python semantics the
// original relied on rather than the closest JavaScript idiom.
// ---------------------------------------------------------------------------

/** Python str.strip(chars): drop any leading/trailing character in the set. */
function pyStrip(value, chars) {
  let start = 0;
  let end = value.length;
  while (start < end && chars.includes(value[start])) start++;
  while (end > start && chars.includes(value[end - 1])) end--;
  return value.slice(start, end);
}

/** Python str.strip(): whitespace only, both ends. */
const pyStripWs = value => value.replace(/^\s+|\s+$/g, '');

/** Split a path into segments on either separator, dropping empties. */
const splitPath = p => p.split(path.sep === '\\' ? /[\\/]/ : /\//).filter(Boolean);

/**
 * Line count as Python text-mode iteration reports it: \r\n, \r, and \n all
 * terminate a line, and a final line without a terminator still counts.
 */
function countLines(text) {
  if (text.length === 0) return 0;
  const terminators = text.match(/\r\n|\r|\n/g);
  const count = terminators ? terminators.length : 0;
  return /(?:\r\n|\r|\n)$/.test(text) ? count : count + 1;
}

/**
 * Read a file as UTF-8 with Python's universal-newline translation: \r\n and a
 * lone \r both become \n. Python opens text files this way, so the catalog was
 * generated from translated text. Returns '' when the file cannot be read.
 */
function readText(file, maxChars) {
  let text;
  try {
    text = fs.readFileSync(file, 'utf8');
  } catch {
    return '';
  }
  text = text.replace(/\r\n|\r/g, '\n');
  // Python caps the read after translation, so slice second.
  return maxChars === undefined ? text : text.slice(0, maxChars);
}

// ---------------------------------------------------------------------------
// Frontmatter
// ---------------------------------------------------------------------------

const NESTED_KEY_RE = /^(\w[\w-]*):\s*([\s\S]*)$/;

/**
 * Extract YAML frontmatter from markdown text (between --- delimiters).
 *
 * Manual parsing, to avoid a YAML dependency. Handles simple key-value pairs,
 * nested maps (one level), and multi-line quoted strings.
 */
function parseYamlFrontmatter(text) {
  const lines = text.split('\n');
  if (lines.length === 0 || pyStripWs(lines[0]) !== '---') return null;

  let endIdx = null;
  for (let i = 1; i < lines.length; i++) {
    if (pyStripWs(lines[i]) === '---') {
      endIdx = i;
      break;
    }
  }
  if (endIdx === null) return null;

  const frontmatter = {};
  let currentNested = null;

  for (const line of lines.slice(1, endIdx)) {
    const stripped = pyStripWs(line);
    if (!stripped || stripped.startsWith('#')) continue;

    const indent = line.length - line.replace(/^\s+/, '').length;

    // Nested key under a parent (indented with 2+ spaces)
    if (indent >= 2 && currentNested !== null) {
      const nested = NESTED_KEY_RE.exec(stripped);
      if (nested) {
        frontmatter[currentNested][nested[1]] = pyStrip(pyStripWs(nested[2]), '\'"');
        continue;
      }
    }

    // Top-level key. Matched against the raw line, so an indented line that
    // failed the nested branch above cannot match here either.
    const top = NESTED_KEY_RE.exec(line);
    if (top) {
      const key = top[1];
      const value = pyStripWs(top[2]);
      currentNested = null;

      if (value === '' || value === '|') {
        // Could be a nested map or a multi-line value
        frontmatter[key] = {};
        currentNested = key;
      } else {
        frontmatter[key] = pyStrip(value, '\'"');
      }
    }
  }

  return frontmatter;
}

/** Return a frontmatter boolean value from the repository's simple parser. */
function frontmatterBool(frontmatter, key) {
  if (!frontmatter || !(key in frontmatter)) return false;

  const value = frontmatter[key];
  if (typeof value === 'boolean') return value;
  if (typeof value === 'string') return value.trim().toLowerCase() === 'true';
  // Python bool(): an empty dict is falsy, a populated one is truthy.
  if (value && typeof value === 'object') return Object.keys(value).length > 0;
  return Boolean(value);
}

// ---------------------------------------------------------------------------
// Directory walking
// ---------------------------------------------------------------------------

// Directories that are runtime/generated and should be excluded from file counts
const RUNTIME_DIRS = new Set([
  '.venv', 'venv', 'env', '.env',
  '__pycache__', '.pytest_cache', '.mypy_cache', '.ruff_cache',
  'node_modules', '.npm', '.yarn', '.pnpm-store',
  '.git', '.svn', '.hg',
  'dist', 'build', '.next', '.nuxt', '.output',
  '.tox', '.nox',
  'target',  // Rust/Java
  '.gradle', '.mvn'
]);

/**
 * Recursively list files, skipping runtime/generated directories.
 *
 * The Python original tested every segment of the absolute path, not just the
 * segments below the scan root, so this does the same.
 */
function iterFiles(directory) {
  const found = [];
  const rootParts = splitPath(path.resolve(directory));
  if (rootParts.some(part => RUNTIME_DIRS.has(part))) return found;

  const walk = dir => {
    let entries;
    try {
      entries = fs.readdirSync(dir, { withFileTypes: true });
    } catch {
      return;
    }
    for (const entry of entries) {
      if (RUNTIME_DIRS.has(entry.name)) continue;
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) walk(full);
      else if (entry.isFile()) found.push(full);
    }
  };

  walk(directory);
  return found;
}

function isDir(p) {
  try {
    return fs.statSync(p).isDirectory();
  } catch {
    return false;
  }
}

function isFile(p) {
  try {
    return fs.statSync(p).isFile();
  } catch {
    return false;
  }
}

// ---------------------------------------------------------------------------
// Script languages
// ---------------------------------------------------------------------------

const EXT_MAP = {
  '.py': 'python',
  '.sh': 'bash',
  '.bash': 'bash',
  '.js': 'javascript',
  '.mjs': 'javascript',
  '.ts': 'typescript',
  '.rb': 'ruby',
  '.ps1': 'powershell',
  '.pl': 'perl',
  '.lua': 'lua',
  '.r': 'r'
};

// Order matters: "bash" is tested before "sh" so #!/bin/bash is not read as sh.
const SHEBANG_MAP = [
  ['python', 'python'],
  ['python3', 'python'],
  ['bash', 'bash'],
  ['sh', 'bash'],
  ['node', 'javascript'],
  ['ruby', 'ruby'],
  ['perl', 'perl']
];

/** Detect programming languages in a scripts/ directory. */
function detectScriptLanguages(scriptsDir) {
  if (!isDir(scriptsDir)) return ['none'];

  const languages = new Set();
  for (const file of iterFiles(scriptsDir)) {
    const ext = path.extname(file).toLowerCase();
    if (EXT_MAP[ext]) languages.add(EXT_MAP[ext]);

    const firstLine = pyStripWs(readText(file).split('\n')[0] || '');
    if (firstLine.startsWith('#!')) {
      for (const [keyword, lang] of SHEBANG_MAP) {
        if (firstLine.includes(keyword)) {
          languages.add(lang);
          break;
        }
      }
    }
  }

  return languages.size > 0 ? [...languages].sort() : ['none'];
}

// ---------------------------------------------------------------------------
// External service indicators
// ---------------------------------------------------------------------------

const EXTERNAL_URL_RE = /https?:\/\/(?!agentskills\.io|modelcontextprotocol\.io|example\.com)[^\s)"'>]+/gi;
const CREDENTIAL_RE = /(API[_-]?KEY|API[_-]?TOKEN|SECRET|CREDENTIALS?|AUTH[_-]?TOKEN|PASSWORD|BEARER|oauth|\.env\b)/i;
const NEGATED_CREDENTIAL_RE = /\b(?:do not|don't|never|must not|should not|cannot|can't|avoid|forbidden|forbid|hardcode|not use|not store|not expose|without storing|without exposing|exclude|omit)\b/i;
const NETWORK_CALL_RE = /(requests\.(get|post|put|delete|patch)|fetch\(|urllib|httpx|aiohttp|axios\.|http\.request|curl\s|wget\s|subprocess.*curl)/i;
const EXEC_RE = /(os\.system|subprocess\.run.*shell\s*=\s*True|exec\(|eval\(|__import__|child_process\.exec|new\s+Function\()/i;
const INSTALL_RE = /(pip\s+install|npm\s+install|cargo\s+install|apt-get\s+install|brew\s+install)/i;

function findUrls(text) {
  return text.match(EXTERNAL_URL_RE) || [];
}

/** Detect credential references while ignoring negated safety instructions. */
function containsCredentialReference(text) {
  if (!text) return false;

  for (const raw of text.split(/\r\n|\r|\n/)) {
    const line = pyStripWs(raw);
    if (!line) continue;
    if (CREDENTIAL_RE.test(line) && !NEGATED_CREDENTIAL_RE.test(line)) return true;
  }

  return false;
}

/** Scan skill content and scripts for external service indicators. */
function detectExternalIndicators(skillDir, skillText) {
  const indicators = {
    urls: [],
    credential_refs: false,
    network_calls: false,
    exec_patterns: false,
    install_commands: false
  };

  // Scan SKILL.md text.
  // The intermediate cap at 20 is the Python original's; the final sort and cap
  // below re-derive the list, so it only bites a skill with >20 unique URLs in
  // SKILL.md alone. None currently do.
  indicators.urls = [...new Set(findUrls(skillText))].slice(0, 20);
  indicators.credential_refs = containsCredentialReference(skillText);
  indicators.network_calls = NETWORK_CALL_RE.test(skillText);
  indicators.exec_patterns = EXEC_RE.test(skillText);
  indicators.install_commands = INSTALL_RE.test(skillText);

  // Scan scripts/ if present
  const scriptsDir = path.join(skillDir, 'scripts');
  if (isDir(scriptsDir)) {
    for (const file of iterFiles(scriptsDir)) {
      const content = readText(file, 50000);  // Cap at 50KB per file
      indicators.urls.push(...findUrls(content));
      if (containsCredentialReference(content)) indicators.credential_refs = true;
      if (NETWORK_CALL_RE.test(content)) indicators.network_calls = true;
      if (EXEC_RE.test(content)) indicators.exec_patterns = true;
      if (INSTALL_RE.test(content)) indicators.install_commands = true;
    }
  }

  indicators.urls = [...new Set(indicators.urls)].sort().slice(0, 20);
  return indicators;
}

// ---------------------------------------------------------------------------
// License, size
// ---------------------------------------------------------------------------

const LICENSE_FILES = ['LICENSE.txt', 'LICENSE.md', 'LICENSE'];

/** Detect the license for a skill. */
function detectLicense(skillDir, frontmatter) {
  // 1. Frontmatter
  if (frontmatter && 'license' in frontmatter) {
    const value = frontmatter.license;
    if (typeof value === 'string' && value.trim()) return value.trim();
  }

  // 2. LICENSE files in skill dir
  for (const name of LICENSE_FILES) {
    const licenseFile = path.join(skillDir, name);
    if (!isFile(licenseFile)) continue;

    const text = readText(licenseFile, 2000);
    if (text.includes('MIT')) return 'MIT';
    if (text.includes('Apache') && text.includes('2.0')) return 'Apache-2.0';
    if (text.includes('GPL')) {
      if (text.includes('3.0')) return 'GPL-3.0';
      if (text.includes('2.0')) return 'GPL-2.0';
      return 'GPL';
    }
    if (text.includes('BSD')) return 'BSD';
    if (text.includes('ISC')) return 'ISC';
    return 'custom';
  }

  return 'unspecified';
}

/** Count total files in a skill directory, excluding runtime/generated folders. */
function countFiles(skillDir) {
  return iterFiles(skillDir).length;
}

const TEXT_EXTS = new Set([
  '.md', '.txt', '.py', '.js', '.ts', '.sh', '.bash',
  '.yaml', '.yml', '.json', '.rb', '.lua', '.r', '.ps1', '.pl'
]);

/** Estimate token count from total lines across all text files. */
function estimateTokens(skillDir) {
  let totalLines = 0;
  for (const file of iterFiles(skillDir)) {
    if (TEXT_EXTS.has(path.extname(file).toLowerCase())) {
      totalLines += countLines(readText(file));
    }
  }
  return Math.trunc(totalLines * 1.3);
}

// ---------------------------------------------------------------------------
// Scanning
// ---------------------------------------------------------------------------

/** Scan a single SKILL.md and its parent directory. */
function scanSkill(skillMdPath, baseDir) {
  const skillDir = path.dirname(skillMdPath);
  const relPath = path.relative(baseDir, skillMdPath).split(path.sep).join('/');
  const dirName = path.basename(skillDir);

  let text;
  try {
    // Same universal-newline translation readText() applies.
    text = fs.readFileSync(skillMdPath, 'utf8').replace(/\r\n|\r/g, '\n');
  } catch (err) {
    return { path: relPath, error: `Could not read: ${err.message}` };
  }

  const frontmatter = parseYamlFrontmatter(text);

  // Extract body (after frontmatter)
  const bodyLines = text.split('\n');
  let inFrontmatter = false;
  let bodyStart = 0;
  for (let i = 0; i < bodyLines.length; i++) {
    if (pyStripWs(bodyLines[i]) === '---') {
      if (!inFrontmatter) {
        inFrontmatter = true;
      } else {
        bodyStart = i + 1;
        break;
      }
    }
  }

  const bodyExcerpt = bodyLines.slice(bodyStart, bodyStart + 200).join('\n');

  // Structure detection
  const hasScripts = isDir(path.join(skillDir, 'scripts'));
  const hasReferences = isDir(path.join(skillDir, 'references'));
  const hasAgents = isDir(path.join(skillDir, 'agents'));
  const hasAssets = isDir(path.join(skillDir, 'assets'));
  const hasLicenseFile = LICENSE_FILES.some(n => isFile(path.join(skillDir, n)));

  const scriptLanguages = hasScripts
    ? detectScriptLanguages(path.join(skillDir, 'scripts'))
    : ['none'];

  return {
    path: relPath,
    name: frontmatter ? (frontmatter.name ?? dirName) : dirName,
    disable_model_invocation: frontmatterBool(frontmatter, 'disable-model-invocation'),
    frontmatter,
    structure: {
      has_scripts: hasScripts,
      has_references: hasReferences,
      has_agents: hasAgents,
      has_assets: hasAssets,
      has_license_file: hasLicenseFile,
      file_count: countFiles(skillDir),
      estimated_tokens: estimateTokens(skillDir)
    },
    script_languages: scriptLanguages,
    external_indicators: detectExternalIndicators(skillDir, text),
    license: detectLicense(skillDir, frontmatter),
    body_excerpt: bodyExcerpt
  };
}

/**
 * Find every SKILL.md under baseDir, ordered the way Python's
 * `sorted(base_dir.rglob("SKILL.md"))` orders them.
 *
 * pathlib compares paths segment by segment (case-folded on Windows), not by
 * the joined string. The two disagree: as segments, "skill-evaluator" sorts
 * before "skill-evaluator-catalog-builder", but joined with a separator the
 * order flips, because "-" is below "\\" and "/".
 */
function findSkillFiles(baseDir) {
  const found = [];
  const walk = dir => {
    let entries;
    try {
      entries = fs.readdirSync(dir, { withFileTypes: true });
    } catch {
      return;
    }
    for (const entry of entries) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) walk(full);
      else if (entry.isFile() && entry.name === 'SKILL.md') found.push(full);
    }
  };
  walk(baseDir);

  const segments = p => {
    const parts = splitPath(path.resolve(p));
    return process.platform === 'win32' ? parts.map(s => s.toLowerCase()) : parts;
  };

  return found.sort((a, b) => {
    const sa = segments(a);
    const sb = segments(b);
    for (let i = 0; i < Math.min(sa.length, sb.length); i++) {
      if (sa[i] !== sb[i]) return sa[i] < sb[i] ? -1 : 1;
    }
    return sa.length - sb.length;
  });
}

/** Find all SKILL.md files and scan each one. */
function scanDirectory(baseDir) {
  const results = [];
  for (const skillMd of findSkillFiles(baseDir)) {
    results.push(scanSkill(skillMd, baseDir));
    // Progress indicator for large collections
    if (results.length % 25 === 0) {
      process.stderr.write(`  Scanned ${results.length} skills...\n`);
    }
  }
  return results;
}

// ---------------------------------------------------------------------------
// CLI
// ---------------------------------------------------------------------------

function parseArgs(argv) {
  const args = { directory: null, output: 'skill-scan-results.json' };
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === '--output' || arg === '-o') {
      args.output = argv[++i];
    } else if (arg.startsWith('--output=')) {
      args.output = arg.slice('--output='.length);
    } else if (!arg.startsWith('-') && args.directory === null) {
      args.directory = arg;
    }
  }
  return args;
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  if (!args.directory) {
    process.stderr.write('Usage: node scripts/catalog/scan-skills.js <skills-directory> [--output results.json]\n');
    process.exit(1);
  }

  const baseDir = path.resolve(args.directory);
  if (!isDir(baseDir)) {
    process.stderr.write(`Error: ${baseDir} is not a directory\n`);
    process.exit(1);
  }

  process.stderr.write(`Scanning ${baseDir} for SKILL.md files...\n`);
  const results = scanDirectory(baseDir);
  process.stderr.write(`Found ${results.length} skills\n`);

  const output = {
    source_directory: baseDir.split(path.sep).join('/'),
    total_skills: results.length,
    skills: results
  };

  // No trailing newline: the Python original wrote none, and the catalog is a
  // committed artifact compared byte for byte.
  fs.writeFileSync(args.output, JSON.stringify(output, null, 2), 'utf8');
  process.stderr.write(`Results written to ${args.output}\n`);
}

if (require.main === module) {
  main();
}

module.exports = {
  parseYamlFrontmatter,
  frontmatterBool,
  detectScriptLanguages,
  detectExternalIndicators,
  detectLicense,
  countFiles,
  estimateTokens,
  countLines,
  pyStrip,
  scanSkill,
  scanDirectory
};
