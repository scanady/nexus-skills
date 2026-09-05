#!/usr/bin/env node

const { spawnSync } = require('child_process');

// plugin-packages/ is authored by hand and the whole plugin distribution is
// rebuilt into dist/ (gitignored), so skill-catalog.json is the only generated
// file this repo commits.
const artifacts = [
  'skill-catalog.json',
];

function git(args) {
  return spawnSync('git', args, { encoding: 'utf8' });
}

const diff = git(['diff', '--quiet', 'HEAD', '--', ...artifacts]);

if (diff.status === 0) {
  console.log('Generated artifacts are up to date.');
  process.exit(0);
}

if (diff.status === 1) {
  console.error('Generated artifacts differ from committed copies. Run `npm run build` and commit the regenerated files.');
  const stat = git(['diff', '--stat', 'HEAD', '--', ...artifacts]);
  if (stat.stdout) {
    console.error(stat.stdout.trim());
  }
  process.exit(1);
}

if (diff.stderr) {
  console.error(diff.stderr.trim());
}
process.exit(diff.status ?? 1);