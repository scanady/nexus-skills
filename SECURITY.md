# Security Policy

## Supported Versions

| Version | Supported |
| ------- | --------- |
| latest  | YES       |
| < 1.0   | NO        |

## Reporting a Vulnerability

**Do not open a public GitHub issue for security vulnerabilities.**

Please report via one of the following channels:

- **GitHub private security advisory**: use the [Report a Vulnerability](../../security/advisories/new) link in the Security tab
- **Email**: security@ifoundry.com

### What to include

- Description of the vulnerability and affected component
- Steps to reproduce
- Potential impact assessment
- Suggested remediation (if known)

### Response timeline

- **Acknowledgement**: within 48 hours
- **Initial assessment**: within 5 business days
- **Resolution target**: within 90 days for critical issues

## Security Standards

This repository enforces:
- OWASP Top 10 guidelines
- Dependency scanning via Dependabot (automated PRs)
- Secret scanning with push protection enabled