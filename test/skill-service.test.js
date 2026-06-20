const test = require('node:test');
const assert = require('node:assert/strict');

const { resolveSourceConfig } = require('../bin/skill-service');

test('resolveSourceConfig prefers explicit source options over environment variables', () => {
  const previousUrl = process.env.NYLD_NEXUS_SKILLS_SOURCE_URL;
  const previousRef = process.env.NYLD_NEXUS_SKILLS_SOURCE_REF;

  process.env.NYLD_NEXUS_SKILLS_SOURCE_URL = 'https://example.com/env.git';
  process.env.NYLD_NEXUS_SKILLS_SOURCE_REF = 'env-ref';

  try {
    assert.deepEqual(resolveSourceConfig({
      sourceUrl: 'https://example.com/explicit.git',
      sourceRef: 'explicit-ref'
    }), {
      repoUrl: 'https://example.com/explicit.git',
      sourceRef: 'explicit-ref'
    });
  } finally {
    if (previousUrl === undefined) {
      delete process.env.NYLD_NEXUS_SKILLS_SOURCE_URL;
    } else {
      process.env.NYLD_NEXUS_SKILLS_SOURCE_URL = previousUrl;
    }

    if (previousRef === undefined) {
      delete process.env.NYLD_NEXUS_SKILLS_SOURCE_REF;
    } else {
      process.env.NYLD_NEXUS_SKILLS_SOURCE_REF = previousRef;
    }
  }
});
