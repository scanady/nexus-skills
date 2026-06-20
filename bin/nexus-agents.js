#!/usr/bin/env node

const { main } = require('../src/cli/main');

if (require.main === module) {
  main().catch(error => {
    console.error(`\n❌ ${error.message}\n`);
    process.exit(1);
  });
}

module.exports = { main };