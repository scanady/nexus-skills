const { parseArgs } = require('./args');
const { installSkills } = require('./commands/install');
const { upgradeSkills } = require('./commands/upgrade');
const { removeSkills } = require('./commands/remove');
const { listSkills } = require('./commands/list');
const { runAuditOverlap } = require('./commands/audit-overlap');
const { showHelp } = require('./help');
const { version } = require('../../package.json');

async function main(argv = process.argv.slice(2)) {
  const options = parseArgs(argv);

  if (options.version) {
    console.log(version);
    return;
  }

  // Help never runs a command, wherever --help appears.
  if (options.help || !options.command || options.command === 'help') {
    showHelp();
    return;
  }

  switch (options.command) {
    case 'install':
      await installSkills(options);
      break;
    case 'upgrade':
      await upgradeSkills(options);
      break;
    case 'remove':
      await removeSkills(options);
      break;
    case 'list':
      await listSkills(options);
      break;
    case 'audit-overlap':
      runAuditOverlap(options.rest);
      break;
  }
}

module.exports = { main };
