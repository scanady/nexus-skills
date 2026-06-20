#!/usr/bin/env node

const { parseArgs } = require('./cli-args');
const { installSkills } = require('./commands/install');
const { listSkills } = require('./commands/list');
const { showHelp } = require('./help');

async function main(argv = process.argv.slice(2)) {
  const options = parseArgs(argv);

  switch (options.command) {
    case 'install':
      await installSkills(options);
      break;
    case 'list':
      await listSkills(options);
      break;
    case 'audit-overlap':
      require('./skill-overlap-report').run(argv.slice(1));
      break;
    case 'help':
    case '--help':
    case '-h':
      showHelp();
      break;
    default:
      if (!options.command) {
        showHelp();
      } else {
        console.log(`\n❌ Unknown command: ${options.command}\n`);
        showHelp();
      }
  }
}

if (require.main === module) {
  main().catch(error => {
    console.error(`\n❌ ${error.message}\n`);
    process.exit(1);
  });
}

module.exports = { main };