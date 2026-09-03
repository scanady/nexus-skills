#!/usr/bin/env node

const fs = require('fs');

const filePath = process.argv[2];

if (!filePath) {
  console.error('Usage: node scripts/validation/check-pr-template.js <pr-body.md>');
  process.exit(1);
}

let body;
try {
  body = fs.readFileSync(filePath, 'utf8');
} catch (error) {
  console.error(`Could not read PR body file: ${filePath}`);
  console.error(error.message);
  process.exit(1);
}

const forbiddenMarkers = [
  'Brief description of what this PR does and why.',
  'Closes #<!-- issue number, or delete if not applicable -->',
  'Closes #',
  '## Screenshots (if applicable)',
  '<!-- Before/after for UI changes -->',
  '1. \n2. ',
  '- \n- \n- ',
  '- \n- \n-\n'
];

const rawTemplateMarkers = [
  'Brief description of what this PR does and why.',
  'Closes #<!-- issue number, or delete if not applicable -->',
  'Closes #',
  '<!-- Before/after for UI changes -->'
];

const matches = rawTemplateMarkers.filter((marker) => body.includes(marker));

if (matches.length > 0) {
  console.error('PR body still contains the raw template placeholders. Populate the body before creating the PR.');
  console.error(`Matched markers: ${matches.join(', ')}`);
  process.exit(1);
}

if (!body.trim() || body.trim().length < 80) {
  console.error('PR body is empty or too short to be a valid review description.');
  process.exit(1);
}

console.log('PR body looks populated and is not using the raw template placeholders.');
