#!/usr/bin/env node

const { spawnSync } = require('child_process');

const candidates = process.platform === 'win32'
  ? [
      { command: 'py', args: ['-3'] },
      { command: 'python', args: [] },
      { command: 'python3', args: [] },
    ]
  : [
      { command: 'python3', args: [] },
      { command: 'python', args: [] },
    ];

function findPython() {
  for (const candidate of candidates) {
    const result = spawnSync(candidate.command, [...candidate.args, '--version'], { stdio: 'ignore' });
    if (result.status === 0) {
      return candidate;
    }
  }
  return null;
}

function main() {
  const python = findPython();
  if (!python) {
    console.error('Unable to find Python. Install Python 3 and rerun the command.');
    process.exit(1);
  }

  const result = spawnSync(python.command, [...python.args, ...process.argv.slice(2)], {
    stdio: 'inherit',
  });

  if (result.error) {
    console.error(result.error.message);
    process.exit(1);
  }

  process.exit(result.status ?? 1);
}

main();