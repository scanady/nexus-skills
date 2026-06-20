const { parseArgs } = require('./args');
const { installSkills } = require('./commands/install');
const { listSkills } = require('./commands/list');
const { runAuditOverlap } = require('./commands/audit-overlap');
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
      runAuditOverlap(argv.slice(1));
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

module.exports = { main };