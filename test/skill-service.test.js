const test = require('node:test');
const assert = require('node:assert/strict');

const { resolveSourceConfig } = require('../src/sources/skill-source');

test('resolveSourceConfig prefers explicit source options over environment variables', () => {
  const previousUrl = process.env.NEXUS_AGENTS_REPO_URL;
  const previousRef = process.env.NEXUS_AGENTS_REPO_REF;

  process.env.NEXUS_AGENTS_REPO_URL = 'https://example.com/env.git';
  process.env.NEXUS_AGENTS_REPO_REF = 'env-ref';

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
      delete process.env.NEXUS_AGENTS_REPO_URL;
    } else {
      process.env.NEXUS_AGENTS_REPO_URL = previousUrl;
    }

    if (previousRef === undefined) {
      delete process.env.NEXUS_AGENTS_REPO_REF;
    } else {
      process.env.NEXUS_AGENTS_REPO_REF = previousRef;
    }
  }
});
