const test = require('node:test');
const assert = require('node:assert/strict');

const {
  classifyComplexity,
  classifyPattern,
  resolveSkillPlugins,
  computeAvg,
  pyRound2,
  deriveSecurityRisk,
  deriveCoreCapabilities,
  deepEqual
} = require('../scripts/catalog/rebuild-catalog');

const {
  parseYamlFrontmatter,
  frontmatterBool,
  countLines,
  pyStrip
} = require('../scripts/catalog/scan-skills');

// ── rebuild-catalog ─────────────────────────────────────────────────────────

test('deriveCoreCapabilities falls back to the frontmatter description', () => {
  const frontmatter = { description: 'Ultra-compressed communication mode.' };

  assert.equal(deriveCoreCapabilities(frontmatter, '>-.'), frontmatter.description);
  assert.equal(deriveCoreCapabilities(frontmatter, '>.'), frontmatter.description);
  assert.equal(deriveCoreCapabilities(frontmatter, 'Not evaluated'), frontmatter.description);
  assert.equal(deriveCoreCapabilities(frontmatter, 'Real capability text'), 'Real capability text');
});

test('deriveCoreCapabilities keeps the existing value when there is no description', () => {
  assert.equal(deriveCoreCapabilities(null, 'Existing'), 'Existing');
  assert.equal(deriveCoreCapabilities({}, ''), '');
});

test('deriveCoreCapabilities treats an all-filler string as a placeholder', () => {
  const frontmatter = { description: 'Real description.' };
  assert.equal(deriveCoreCapabilities(frontmatter, '  >- . '), frontmatter.description);
});

test('classifyComplexity and classifyPattern bucket on the documented thresholds', () => {
  assert.equal(classifyComplexity(0), 'compact');
  assert.equal(classifyComplexity(699), 'compact');
  assert.equal(classifyComplexity(700), 'detailed');
  assert.equal(classifyComplexity(1999), 'detailed');
  assert.equal(classifyComplexity(2000), 'comprehensive');

  assert.equal(classifyPattern(true), 'B');
  assert.equal(classifyPattern(false), 'A');
});

test('deriveSecurityRisk escalates with the number of findings', () => {
  const none = deriveSecurityRisk({ external_indicators: {} }, null);
  assert.equal(none.rating, 'low');
  assert.deepEqual(none.findings, []);

  const two = deriveSecurityRisk(
    { external_indicators: { credential_refs: true, network_calls: true } }, null);
  assert.equal(two.rating, 'medium');
  assert.equal(two.findings.length, 2);

  const three = deriveSecurityRisk({
    external_indicators: {
      credential_refs: true, network_calls: true, exec_patterns: true, install_commands: true
    }
  }, null);
  assert.equal(three.rating, 'high');
  assert.equal(three.findings.length, 4);
});

test('deriveSecurityRisk keeps unrelated fields from the existing block', () => {
  const updated = deriveSecurityRisk({ external_indicators: {} }, { sub_scores: { bias: 5 } });
  assert.deepEqual(updated.sub_scores, { bias: 5 });
});

test('resolveSkillPlugins matches exact names and prefix globs, sorted', () => {
  const plugins = {
    tech: { skills: ['tech-*'] },
    data: { skills: ['tech-dev-git-commit'] },
    ops: { skills: ['ops-runbook'] }
  };
  assert.deepEqual(resolveSkillPlugins('tech-dev-git-commit', plugins), ['data', 'tech']);
  assert.deepEqual(resolveSkillPlugins('tech-other', plugins), ['tech']);
  assert.deepEqual(resolveSkillPlugins('unclaimed', plugins), []);
});

test('computeAvg ignores skills whose score is missing or not a number', () => {
  const skills = [
    { evaluation: { usage_value: { score: 4 } } },
    { evaluation: { usage_value: { score: 3 } } },
    { evaluation: { usage_value: {} } },
    { evaluation: {} },
    { evaluation: { usage_value: 'nope' } }
  ];
  assert.equal(computeAvg(skills, ['usage_value', 'score']), 3.5);
  assert.equal(computeAvg([], ['usage_value', 'score']), 0.0);
});

// Python's round() is half-to-even, so a JS Math.round port would drift.
test('pyRound2 rounds half to even, matching Python', () => {
  assert.equal(pyRound2(3.14159), 3.14);
  // 2.235 is stored just *below* 2.235, so Python rounds it down.
  assert.equal(pyRound2(2.235), 2.23);
  assert.equal(pyRound2(0.125), 0.12);   // exact tie, down to even
  assert.equal(pyRound2(0.135), 0.14);   // not a tie: stored just above
  assert.equal(pyRound2(0.375), 0.38);   // exact tie, up to even
  assert.equal(pyRound2(-2.675), -2.67);
  assert.equal(pyRound2(0), 0);
});

test('deepEqual compares nested structures by value', () => {
  assert.ok(deepEqual({ a: [1, { b: null }] }, { a: [1, { b: null }] }));
  assert.ok(!deepEqual({ a: 1 }, { a: 1, b: 2 }));
  assert.ok(!deepEqual({ a: 1 }, { a: '1' }));
  assert.ok(!deepEqual([1, 2], [2, 1]));
});

// ── scan-skills ─────────────────────────────────────────────────────────────

test('parseYamlFrontmatter reads keys, quotes, and one level of nesting', () => {
  const frontmatter = parseYamlFrontmatter([
    '---',
    'name: demo-skill',
    "description: 'Quoted value'",
    '# a comment',
    'metadata:',
    '  version: 1.2.0',
    '  role: "author"',
    '---',
    '# Body'
  ].join('\n'));

  assert.equal(frontmatter.name, 'demo-skill');
  assert.equal(frontmatter.description, 'Quoted value');
  assert.deepEqual(frontmatter.metadata, { version: '1.2.0', role: 'author' });
});

test('parseYamlFrontmatter returns null without a leading delimiter or a closing one', () => {
  assert.equal(parseYamlFrontmatter('# No frontmatter'), null);
  assert.equal(parseYamlFrontmatter('---\nname: x\n'), null);
});

test('frontmatterBool reads the string booleans the parser produces', () => {
  assert.equal(frontmatterBool({ 'disable-model-invocation': 'true' }, 'disable-model-invocation'), true);
  assert.equal(frontmatterBool({ 'disable-model-invocation': 'TRUE' }, 'disable-model-invocation'), true);
  assert.equal(frontmatterBool({ 'disable-model-invocation': 'false' }, 'disable-model-invocation'), false);
  assert.equal(frontmatterBool({}, 'disable-model-invocation'), false);
  assert.equal(frontmatterBool(null, 'disable-model-invocation'), false);
  // An empty nested map is falsy in Python; a populated one is truthy.
  assert.equal(frontmatterBool({ k: {} }, 'k'), false);
  assert.equal(frontmatterBool({ k: { a: 1 } }, 'k'), true);
});

// Python reads text files with universal newlines, so \r\n and a lone \r each
// terminate one line and a final unterminated line still counts.
test('countLines matches Python text-mode line counting', () => {
  assert.equal(countLines(''), 0);
  assert.equal(countLines('a'), 1);
  assert.equal(countLines('a\n'), 1);
  assert.equal(countLines('a\nb'), 2);
  assert.equal(countLines('a\r\nb\r\n'), 2);
  assert.equal(countLines('a\rb'), 2);
});

test('pyStrip removes any of the given characters from both ends', () => {
  assert.equal(pyStrip('"quoted"', '\'"'), 'quoted');
  assert.equal(pyStrip("'mixed\"", '\'"'), 'mixed');
  assert.equal(pyStrip('plain', '\'"'), 'plain');
  assert.equal(pyStrip('""', '\'"'), '');
});
