const test = require('node:test');
const assert = require('node:assert/strict');

const {
  collectExistingSkills,
  resolveSkillsToInstall
} = require('../src/cli/commands/install');

test('resolveSkillsToInstall installs every available skill when none are selected', () => {
  const result = resolveSkillsToInstall([], ['alpha', 'beta']);

  assert.deepEqual(result, {
    skillsToInstall: ['alpha', 'beta'],
    invalidSkills: []
  });
});

test('resolveSkillsToInstall filters selected skills and reports invalid names', () => {
  const result = resolveSkillsToInstall(['alpha', 'missing'], ['alpha', 'beta']);

  assert.deepEqual(result, {
    skillsToInstall: ['alpha'],
    invalidSkills: ['missing']
  });
});

test('collectExistingSkills returns unique installed skills across targets', () => {
  const existingPaths = new Set([
    'one/alpha',
    'two/alpha',
    'two/beta'
  ]);
  const fsImpl = {
    existsSync(filePath) {
      return existingPaths.has(filePath.replace(/\\/g, '/'));
    }
  };
  const pathImpl = {
    join(...parts) {
      return parts.join('/');
    }
  };

  const result = collectExistingSkills(
    [{ dir: 'one' }, { dir: 'two' }],
    ['alpha', 'beta', 'gamma'],
    fsImpl,
    pathImpl
  );

  assert.deepEqual([...result], ['alpha', 'beta']);
});
