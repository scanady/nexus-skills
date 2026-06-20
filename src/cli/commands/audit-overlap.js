const { run } = require('../../audit/skill-overlap-report');

function runAuditOverlap(argv) {
  run(argv);
}

module.exports = { runAuditOverlap };