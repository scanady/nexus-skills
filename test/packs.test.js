const test = require('node:test');
const assert = require('node:assert/strict');

const { resolvePackSkills } = require('../src/core/packs');

test('resolvePackSkills expands exact skills and prefix patterns', () => {
  const result = resolvePackSkills(
    ['content'],
    [
      'content-copy-humanizer',
      'content-technical-doc-coauthoring',
      'marketing-content-engine',
      'research-analyst'
    ]
  );

  assert.deepEqual(result, [
    'content-copy-humanizer',
    'content-technical-doc-coauthoring'
  ]);
});
