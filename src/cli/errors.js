/**
 * An error the CLI reports to the user and exits on.
 * exitCode 2 marks a usage mistake (bad flag, missing value); 1 marks a failure.
 */
class CliError extends Error {
  constructor(message, exitCode = 1) {
    super(message);
    this.name = 'CliError';
    this.exitCode = exitCode;
  }
}

function usageError(message) {
  return new CliError(`${message}\n   Run "nxa --help" for usage.`, 2);
}

module.exports = { CliError, usageError };
