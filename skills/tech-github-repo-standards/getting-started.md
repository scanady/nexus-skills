# Getting Started

Prerequisites and usage notes for `tech-github-repo-standards`.

This skill applies GitHub repository best practices **directly** to your target repo via the `gh` CLI. The agent runs the API calls; file artifacts (CODEOWNERS, SECURITY.md, etc.) are delivered via a single pull request from the branch `chore/apply-github-standards`. You do not run a script — you confirm the plan and the agent applies it.

---

## Prerequisites

### 1. gh CLI ≥ 2.28

Install the [GitHub CLI](https://cli.github.com):

```bash
# macOS
brew install gh

# Windows (winget)
winget install --id GitHub.cli

# Linux — see https://github.com/cli/cli/blob/trunk/docs/install_linux.md
```

Verify:

```bash
gh --version
# gh version 2.28.0 (or higher)
```

### 2. Authenticate with the right scopes

```bash
gh auth login
# GitHub.com -> HTTPS -> web browser
```

**Scopes by context:**

| Context | Required scopes | Add via |
|---------|-----------------|---------|
| `external` (personal repos) | `repo`, `workflow` | Default `gh auth login` provides these |
| `internal` (org repos) | `repo`, `workflow`, `admin:org`, `write:org` | When prompted for additional scopes, request them; or run `gh auth refresh -s admin:org,write:org` |

Verify:

```bash
gh auth status
```

### 3. Admin permissions on all target repos

The authenticated account must have **Admin** role on every repo being configured. Branch protection and security settings require admin access — write access is not sufficient.

For **internal context**: the account must also have permission to manage team access (`write:org` scope).

---

## What You Provide

When you invoke the skill, the agent will ask for any of these it does not already have:

| Input | Required | Notes |
|-------|----------|-------|
| `org` | Yes | GitHub org or personal account |
| `repo` | Yes | Single name, comma-separated list, or glob (e.g. `service-*`) |
| `context` | No (default `internal`) | `internal` for org repos, `external` for personal/side-venture |
| `profile` | No (default `standard`) | `standard` \| `collaborative` \| `monorepo` \| `regulated` |
| `cla` | No (default `false`) | Adds DCO as a required status check |
| `dry-run` | No (default `false`) | Print every intended call, perform no writes |
| `emit-script` | No (default `false`) | Also save the executed command sequence as an audit-trail script |
| `owning_team` | If `internal` | Team slug only — no `@org/` prefix |
| `maintainers` | If `external` | Space-separated GitHub usernames for collaborator grants |
| `security_email` | Yes | Used in `SECURITY.md` |
| `codeql_languages` | Auto-detected; confirm | CodeQL matrix (e.g. `javascript-typescript`, `python`, `go`). Skill scans repo first, asks if ambiguous |
| `dependabot_ecosystems` | Auto-detected; confirm | npm, pip, gomod, etc. `github-actions` is always added |
| `solo_maintainer_zero_approvals` | If `external` + single CODEOWNER | Set required approvals to 0 so you can self-merge the artifact PR (see Solo-Maintainer Mode below) |

---

## What the Skill Does

1. **Discovers** existing repo settings and shows you a summary.
2. **Validates** inputs (e.g. blocks `external + regulated`).
3. **Confirms the plan** with you before any write.
4. **Applies settings directly** via `gh api`:
   - Repo defaults (squash merge, auto-merge, sign-off)
   - Branch protection on `main` and `develop`
   - Security features (Dependabot, secret scanning, push protection, CodeQL, GHAS for regulated)
   - Actions permissions (read-only default token, GitHub-owned + verified actions only)
   - Access (team grant for internal, collaborator grants for external)
5. **Opens a pull request** from `chore/apply-github-standards` containing all 8 file artifacts:
   - `.github/CODEOWNERS`
   - `SECURITY.md`
   - `CONTRIBUTING.md`
   - `.github/ISSUE_TEMPLATE/bug_report.md`
   - `.github/ISSUE_TEMPLATE/feature_request.md`
   - `.github/pull_request_template.md`
   - `.github/workflows/codeql.yml`
   - `.github/dependabot.yml`
6. **Verifies** every applied setting and outputs a summary with succeeded / skipped / failed counts, the artifact PR URL, and any manual steps.

The artifact PR is reviewed and merged like any other PR. The branch protection rules just applied will gate it — that is intentional.

---

## Multi-Repo Application

Pass a comma-separated list or glob:

```
repo = api-service, worker-service, admin-ui
repo = service-*
```

The skill iterates per repo, applies all settings, and opens one artifact PR per repo. The summary aggregates totals across all repos.

---

## Optional: Audit-Trail Script

Set `emit-script=true` to also save the executed command sequence as `apply-github-standards.sh` (Linux/macOS) or `apply-github-standards.ps1` (Windows). This is a record of what was done — useful for compliance evidence or replay in another environment. It is **not** required: the skill applies the changes itself.

---

## Required API Scopes Summary

| Scope | Used for | Required when |
|-------|----------|---------------|
| `repo` | Branch protection, security settings, artifact PR | always |
| `workflow` | Committing `.github/workflows/codeql.yml` | always |
| `admin:org` | Team permission grants | `internal` only |
| `write:org` | Reading/modifying org team membership | `internal` only |

---

## Solo-Maintainer Mode

If you are the only CODEOWNER on an `external` repo and the profile requires approvals (e.g. `standard`), GitHub will block you from approving your own artifact PR — and `enforce_admins=true` blocks an admin override. The skill will detect this and offer to set `required_approving_review_count=0` for the run.

- CODEOWNER review is still required (provides routing/notification on every PR), but the count is 0.
- `enforce_admins=true` is preserved — no one bypasses protection.
- You can later raise the count to 1 once a second collaborator/CODEOWNER exists.

---

## Troubleshooting

**"Resource not accessible by integration"** — the authenticated token lacks `admin:org`. Re-run `gh auth login` and add the scope.

**"Branch not found — skipping protection"** — create the branch first (`git checkout -b develop && git push -u origin develop`), then re-run.

**"GitHub Advanced Security requires Enterprise license"** — expected on Free/Team plans. The skill skips gracefully and surfaces a manual step. Enable GHAS in org Settings if you have a GHEC or GHES license.

**Artifact PR creation fails** — an existing ruleset may block branch creation. The skill surfaces this as a manual step rather than retrying. Adjust the ruleset or create the branch manually.

**Glob pattern matches zero repos** — verify with `gh repo list YOUR_ORG --limit 500 --json name --jq '.[].name'`.

**A repo setting (e.g. `has_projects`) didn't take effect** — known GitHub API quirk: when many fields are batched into one `PATCH /repos/{org}/{repo}`, some can be silently dropped. The skill re-verifies after each phase and re-applies any missed field individually.

**`gh pr create` says "a pull request for branch ... already exists"** — a previous run already opened it. The skill checks first and updates via `gh pr edit` instead of creating a duplicate.
