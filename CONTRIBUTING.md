# Contributing

Thank you for your interest in contributing.

## Getting Started

1. Fork the repository or create a branch from `main` (collaborators).
2. Create a branch following the naming convention below.
3. Make your changes following the conventions in this guide.
4. Open a pull request against `main`.

## Branch Naming

| Type | Pattern | Example |
|------|---------|---------|
| Feature | `feat/<short-description>` | `feat/add-oauth-login` |
| Bug fix | `fix/<short-description>` | `fix/null-pointer-auth` |
| Chore | `chore/<short-description>` | `chore/update-deps` |
| Docs | `docs/<short-description>` | `docs/improve-readme` |
| Hotfix | `hotfix/<short-description>` | `hotfix/cve-patch` |

Lowercase with hyphens only. No underscores, no camelCase.

## Commit Conventions

Format: `type(scope): short description` ([Conventional Commits](https://www.conventionalcommits.org/))

| Type | Use for |
|------|---------|
| `feat` | New features |
| `fix` | Bug fixes |
| `docs` | Documentation only |
| `refactor` | Restructuring, no behavior change |
| `test` | Tests added or updated |
| `chore` | Maintenance, dependency updates |
| `ci` | CI/CD pipeline changes |
| `perf` | Performance improvements |

- Subject line: <= 50 chars, imperative mood, no trailing period
- Body: optional - explain *why*, not *what*; wrap at 72 chars
- Breaking changes: `!` after type + `BREAKING CHANGE:` in footer

## Pull Requests

- One concern per PR
- Reference related issues: `Closes #123`
- Fill in the PR template completely
- PRs must pass all CI checks before merging
- Reviews are encouraged but not blocking (solo-maintainer mode)
- Resolve all review comments before merging
- Squash merge only

## Development Setup

```bash
git clone https://github.com/scanady/nexus-agents.git
cd nexus-agents
npm install
```

## Questions?

Open a [GitHub Discussion](../../discussions) or search existing issues first.