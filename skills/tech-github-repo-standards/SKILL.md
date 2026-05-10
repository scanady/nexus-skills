---
name: tech-github-repo-standards
description: Apply standardized GitHub repository best practices — branch protection, security features, access controls, and required file artifacts — directly to one or more repos via the `gh` CLI. Use when asked to "standardize a repo", "harden this repository", "set up CODEOWNERS", "apply regulated settings", or "configure GitHub repo settings". Supports four profiles (standard, collaborative, monorepo, regulated) and two context modes (internal, external). File artifacts are delivered via pull request; an audit-trail script is available on request.
license: MIT
compatibility: Requires gh CLI ≥ 2.28 installed and authenticated via `gh auth login`. Admin permissions required on target repo(s).
metadata:
  version: "2.1.1"
  domain: tech
  triggers: standardize repo, apply github repo settings, set up CODEOWNERS, harden repository, apply regulated settings, branch protection at scale, repo compliance settings, squash merge policy, dependabot and secret scanning setup, gh cli repo configuration
  anti-triggers: git commit, git push, PR review, issue triage, github actions debugging, create repo, manage issues, manage pull requests
  role: specialist
  scope: automation
  output-format: applied repo settings + artifact PR (+ optional audit script)
  related-skills: tech-github-ops, tech-arch-architecture-decision-records, tech-security-audit-lead, tech-devops-engineer

---

# GitHub Repository Standards

Apply opinionated, open-source-aligned repository standards to one or more GitHub repos directly via the `gh` CLI. Settings (merge policy, branch protection, security, Actions, access) are applied through the API; file artifacts (CODEOWNERS, SECURITY.md, etc.) are delivered via a single pull request rather than committed straight to the default branch.

## Role

Senior platform engineer and GitHub workflow specialist. Apply repository standards directly — do not produce scripts for the user to run unless they explicitly ask for an audit-trail artifact. Use the command playbooks in `references/` as the canonical source for API endpoints, payloads, and artifact bodies.

## Workflow

### Step 1: Collect Inputs

Ask for any missing required inputs. Apply defaults silently for optional ones.

| Input | Required | Default | Values |
|-------|----------|---------|--------|
| `org` | Yes | — | GitHub org or personal account name |
| `repo` | Yes | — | Single name, comma-separated list, or glob (e.g. `service-*`) |
| `context` | No | `internal` | `internal` \| `external` |
| `profile` | No | `standard` | `standard` \| `collaborative` \| `monorepo` \| `regulated` |
| `cla` | No | `false` | Adds DCO or named CLA bot as a required status check |
| `dry-run` | No | `false` | Print every intended `gh` call without executing it |
| `emit-script` | No | `false` | Also save the executed command sequence as an audit-trail script |

For internal context, also collect `owning_team` (GitHub team slug). For external context with multiple maintainers, collect `maintainers` (list of GitHub usernames). For all contexts, collect `security_email` (used in SECURITY.md), the **CodeQL `language` matrix** (e.g. `javascript-typescript`, `python`, `go`, `java-kotlin`, etc. — detect by scanning the repo for primary language(s); ask if ambiguous), and the **Dependabot ecosystems** to enable (e.g. `npm`, `pip`, `gomod`, `maven`, `bundler`, `cargo`, `nuget`, `docker` — `github-actions` is always enabled). Detect by checking for `package.json`, `requirements.txt`, `go.mod`, etc. in the repo root; ask if ambiguous.

**Context modes:**

`internal` — org-scoped repos, GitHub org membership assumed. CODEOWNERS maps to `@org/team-slug`. All four profiles available.

`external` — personal or side-venture repos, no org structure assumed. CODEOWNERS maps to `@username`. The `regulated` profile is unavailable under external context.

### Step 2: Discover Existing Settings

For each target repo, read current settings and present a `**Current settings found**` summary so the user can confirm before changes are applied.

```bash
gh repo view {org}/{repo} --json name,isPrivate,defaultBranchRef,hasWikiEnabled,deleteBranchOnMerge,squashMergeAllowed,mergeCommitAllowed,rebaseMergeAllowed
gh api GET /repos/{org}/{repo}/branches/main/protection 2>/dev/null || echo "No main protection"
gh api GET /repos/{org}/{repo}/branches/develop/protection 2>/dev/null || echo "No develop protection"
gh api GET /repos/{org}/{repo}/actions/permissions
gh api GET /repos/{org}/{repo} --jq '.security_and_analysis'
gh api GET /repos/{org}/{repo}/teams 2>/dev/null   # internal context
```

If the repo does not exist, stop and ask the user to create it first — this skill configures existing repos, it does not create them.

### Step 3: Validate Inputs

Reject invalid combinations before applying anything. Run prerequisite checks in order — installation, then auth, then permissions, then logical guards.

| Condition | Error |
|-----------|-------|
| `gh --version` fails or `< 2.28` | `ERROR: gh CLI not installed (or below 2.28). Install: winget install --id GitHub.cli` (Windows) or `brew install gh` (macOS) |
| `gh auth status` fails | `ERROR: gh CLI is not authenticated. Run: gh auth login` |
| Token scopes insufficient for context | See "Required scopes by context" below |
| Caller lacks admin on target repo | `ERROR: Admin permission required on {repo}` |
| `context=external` + `profile=regulated` | `ERROR: The 'regulated' profile is only available for internal context.` |
| Unknown profile | `ERROR: Unknown profile '{value}'. Valid: standard, collaborative, monorepo, regulated` |
| Unknown context | `ERROR: Unknown context '{value}'. Valid: internal, external` |

**Required scopes by context:**

| Context | Minimum scopes | Why |
|---------|----------------|-----|
| `external` | `repo`, `workflow` | Repo-level settings, branch protection, content writes, workflow files. No org operations. |
| `internal` | `repo`, `workflow`, `admin:org`, `write:org` | Adds team grants and org membership reads for `apply_access`. |

If scopes are insufficient, surface the exact `gh auth refresh -s {scope}` command rather than just listing the missing scope.

### Step 4: Confirm Plan

Show the user the plan before any write operation. Required approvals, profile-driven flags, and the artifact PR target are all surfaced here.

| Setting | standard | collaborative | monorepo | regulated |
|---------|:--------:|:-------------:|:--------:|:---------:|
| Required approvals | 1 | 2 | 2 | 2 |
| Dismiss stale reviews | ✓ | ✓ | ✓ | ✓ |
| Require CODEOWNERS review | ✓ | ✓ | ✓ | ✓ |
| Enforce on admins (no bypass) | ✓ | ✓ | ✓ | ✓ |
| Allow force pushes | ✗ | ✗ | ✗ | ✗ |
| Allow deletions | ✗ | ✗ | ✗ | ✗ |
| Require conversation resolution | ✓ | ✓ | ✓ | ✓ |
| Require last push approval | ✗ | ✓ | ✓ | ✓ |
| Required linear history | ✗ | ✗ | ✗ | **✓** |
| Merge queue | ✗ | ✗ | **✓** | ✗ |
| Require signed commits | ✗ | ✗ | ✗ | **✓** |
| Web commit sign-off required | ✗ | ✗ | ✗ | **✓** |

**Repository defaults (all profiles, all contexts):**
Squash merge only, `squash_merge_commit_title=PR_TITLE`, `squash_merge_commit_message=PR_BODY`, `delete_branch_on_merge=true`, `allow_auto_merge=true`, `allow_update_branch=true`, `has_wiki=false`, `has_projects=false`.

**Security baseline (all profiles, all contexts — no exceptions):**
Dependabot alerts, Dependabot security updates, private vulnerability reporting, secret scanning, push protection, CodeQL workflow, Dependabot version-updates config.
GitHub Advanced Security: regulated profile only (requires Enterprise license — skip gracefully with manual step if unavailable).

**Actions permissions (all profiles, all contexts):**
`allowed_actions=selected` (GitHub-owned + verified creator only), `default_workflow_permissions=read`, `can_approve_pull_request_reviews=false`.

**Solo-maintainer override (external context):** if the user is the only CODEOWNER (single-owner CODEOWNERS) and `external` context, GitHub blocks self-approval — the artifact PR (Step 6) cannot be merged under `standard=1` or any profile that requires approvals + CODEOWNER review + `enforce_admins=true`. Two options:
  1. **Recommended:** set `required_approving_review_count=0` for this run. CODEOWNER review still applies (provides routing/notification), `enforce_admins=true` is preserved.
  2. Add a second collaborator/CODEOWNER who can approve.

Ask the user which they want before applying. If 0 approvals, note it in the plan and the artifact PR description as "solo-maintainer mode".

Wait for explicit confirmation before continuing to Step 5. If `dry-run` is true, run Step 5 in print-only mode.

### Step 5: Apply Settings Directly

For each target repo, execute the API calls in order using `gh` / `gh api` in the terminal. The exact endpoints, payloads, and ordering are documented in `references/script-template.sh` (bash) and `references/script-template.ps1` (PowerShell) — these are the **command playbook**, not user-facing scripts. Read them as needed and issue the corresponding `gh api` calls live.

**Order (per repo):**

1. **Repo general settings** — `PATCH /repos/{org}/{repo}` with merge policy, auto-merge, wiki/projects flags, web commit sign-off.
2. **Branch protection** — for each of `main` and `develop` (skip if missing): `PUT /repos/{org}/{repo}/branches/{branch}/protection` with profile-scaled rules. Then signed-commit requirement (regulated only) and merge-queue ruleset (monorepo, main only).
3. **Security features** — Dependabot alerts, automated fixes, private vulnerability reporting, secret scanning, push protection. GHAS attempt for regulated (skip gracefully on license error).
4. **Actions permissions** — restrict to GitHub-owned + verified, default read-only token, no PR approvals.
5. **Access controls** — internal: grant owning team admin via `PUT /orgs/{org}/teams/{slug}/repos/{org}/{repo}`. External: grant maintainers push via `PUT /repos/{org}/{repo}/collaborators/{username}`. Flag any direct collaborators outside the team model.
6. **Artifact pull request** — see Step 6.

**Tracking:** maintain running counters of succeeded / skipped / failed operations and a list of manual steps. Surface failures inline (with the API error message) but continue the run; do not abort on first failure. Surface the full summary in Step 7.

**Verify-after-apply per phase:** after the repo general-settings PATCH (step 1), re-read with `gh api /repos/{org}/{repo} --jq` and confirm every targeted field. The GitHub API will occasionally **silently drop** fields when too many are batched in one PATCH (observed: `has_projects=false` ignored when bundled with 9+ other fields). For any field that did not take, re-apply it in an isolated PATCH and re-verify. Do this for general-settings, security_and_analysis, and Actions permissions phases.

**Dry-run mode:** print each intended call as `[DRY-RUN] {description}: gh api ...` without executing. No API writes, no branch creation, no PR.

### Step 6: Artifact Pull Request

Commit all required file artifacts as a single PR rather than pushing to the default branch.

**Artifacts (all 8 — none are optional):**

| Path | Purpose |
|------|---------|
| `.github/CODEOWNERS` | Profile- and context-specific owner routing |
| `SECURITY.md` | Vulnerability reporting policy |
| `CONTRIBUTING.md` | Branch / commit / PR conventions |
| `.github/ISSUE_TEMPLATE/bug_report.md` | Bug report form |
| `.github/ISSUE_TEMPLATE/feature_request.md` | Feature request form |
| `.github/pull_request_template.md` | PR template (regulated adds security checklist) |
| `.github/workflows/codeql.yml` | CodeQL analysis (regulated adds SARIF artifact upload) |
| `.github/dependabot.yml` | Dependency update schedule |

**PR procedure:**

1. Resolve the default branch and its head SHA:
   - `gh api GET /repos/{org}/{repo} --jq '.default_branch'`
   - `gh api GET /repos/{org}/{repo}/git/refs/heads/{default_branch} --jq '.object.sha'`
2. Create branch `chore/apply-github-standards` from that SHA via `POST /repos/{org}/{repo}/git/refs`. If the branch already exists from a prior run, fast-forward it to the current default-branch SHA via `PATCH /repos/{org}/{repo}/git/refs/heads/chore/apply-github-standards` with `force=true`.
3. Upsert all 8 artifacts on that branch using `PUT /repos/{org}/{repo}/contents/{path}` with `branch=chore/apply-github-standards`. Render every artifact body from the playbook in `references/script-template.sh` (bash variants) or `.ps1` (PowerShell variants), substituting the user's actual org, team slugs, usernames, security email, **CodeQL language matrix**, and **Dependabot ecosystems** — **no `REPLACE_WITH_*` tokens may appear in the committed files** unless the user explicitly chose to leave a placeholder for later editing.
4. **Check for existing PR first:** `gh pr list --repo {org}/{repo} --head chore/apply-github-standards --state open --json number,url --jq '.[0]'`. If one exists, update it with `gh pr edit {n} --repo {org}/{repo} --title ... --body-file {path}` instead of creating a new one (creating a duplicate fails with `a pull request for branch ... already exists`).
5. Otherwise create the PR: `gh pr create --repo {org}/{repo} --base {default_branch} --head chore/apply-github-standards --title "chore: apply tech-github-repo-standards ({profile})" --body-file {path}`. Always pass `--repo` explicitly (the agent's CWD may not be a clone of the target). The body must list every artifact added/updated and the profile/context. Add the `chore` label if it exists on the repo.
6. After creation, verify with `gh pr view --repo {org}/{repo} {branch}` — terminal output can buffer and hide success/failure. Do not assume success based on stdout alone.
7. The branch protection rules just applied will gate the PR — that is intentional. Do not attempt to bypass `enforce_admins`.

**If branch protection blocks the PR's own creation** (e.g. an existing ruleset blocks branch creation by non-admins), surface this as a manual step rather than retrying.

### Step 7: Verify and Report

After applying:

1. Re-read each setting and confirm it matches the target. For settings that fail to verify, list them under "Settings failed".
2. Output the summary below. If `emit-script=true`, also write the executed command sequence to `apply-github-standards.sh` (Linux/macOS) or `apply-github-standards.ps1` (Windows) for audit/replay — this script is a record of what was done, not a tool the user must run.

**Summary template:**

```
GitHub Repository Standards — applied
Context : {context}
Profile : {profile}
Repos   : {count}

Settings succeeded  : {n}
Settings skipped    : {n}
Settings failed     : {n}
Artifact PRs opened : {n}  ({pr_urls})
Audit script        : {path or "not requested"}

Manual steps required:
  • {step 1}
  • {step 2}
```

For `regulated` profile, also output the compliance checklist defined at the bottom of `references/script-template.sh` (NYDFS scope, GHAS, org 2FA, audit log streaming, evidence retention, quarterly review).

---

## Constraints

**MUST:**
- Apply settings directly via `gh` / `gh api` — do not hand the user a script and ask them to run it (unless `emit-script=true`, and even then the script is an audit artifact, not the deliverable).
- Deliver file artifacts via a single pull request from `chore/apply-github-standards`, not direct commits to the default branch.
- Run prerequisite checks in order in Step 3: installation → auth → scopes → admin → logical guards.
- Discover existing settings (Step 2) and confirm the plan (Step 4) before any write operation.
- Detect (or ask for) the CodeQL `language` matrix and Dependabot ecosystems based on the actual repo contents — do not hardcode `javascript-typescript` + `npm`.
- Offer the solo-maintainer 0-approvals override when `external` context has only one CODEOWNER.
- Re-verify each phase after PATCH; re-apply any field the API silently dropped (esp. `has_projects`).
- Check for an existing artifact PR before creating; update it via `gh pr edit` if present.
- Always pass `--repo {org}/{repo}` to `gh pr ...` commands.
- Use `references/script-template.sh` and `.ps1` as the canonical command and content playbooks — do not invent endpoints or payloads.
- Substitute every `REPLACE_WITH_*` token in artifact bodies with the user's actual values before committing.
- Surface failures inline with their API error message; continue the run and surface a final tally.
- Surface the `external + regulated` guard error immediately, before any API call.
- Produce all 8 file artifacts in the PR — they are not optional.
- Honor `dry-run`: print intended commands, perform no writes (including no branch creation, no PR).

**MUST NOT:**
- Skip `enforce_admins: true` — there is no admin bypass path.
- Push artifacts directly to the default branch.
- Bypass branch protection on the artifact PR after applying it.
- Add the PUSH sentence to the description or over-broaden activation — this is a narrow, purpose-specific skill.
- Use `gh repo edit` for settings that require the REST API — use `gh api` directly.

---

## Implementation Notes

**Windows / PowerShell specifics** (these issues bit during real runs — apply preventatively):

1. **JSON payload files must be UTF-8 without BOM.** `Out-File -Encoding utf8` in Windows PowerShell 5.1 writes a BOM that breaks `gh api --input`. Use `[IO.File]::WriteAllText($path, $json, (New-Object Text.UTF8Encoding $false))` instead.
2. **For multi-line / multi-artifact operations, write a `.ps1` script file and invoke it** rather than typing here-strings into the interactive shell. Long here-strings buffer unpredictably and may appear to hang or silently truncate output.
3. **Use `--body-file` for `gh pr create` / `gh pr edit`.** Piping a here-string via `--body-file -` is unreliable across shell variants; write the body to a temp file and pass the path.
4. **Existence checks: use `$LASTEXITCODE`, not stdout parsing.** `gh api ... --silent 2>$null; if ($LASTEXITCODE -eq 0) { ... }`. Parsing stderr/stdout for "Not Found" mis-detects because gh writes 404 JSON to stderr.
5. **Always pass `--repo {org}/{repo}` to `gh pr ...` commands.** The agent's CWD may not be a clone of the target repo, and gh's repo auto-detection is silently inconsistent.
6. **Don't trust stdout alone for write operations** — terminal output can buffer or be lost. Verify by re-reading state (`gh repo view`, `gh pr view`, `gh api`).

**Linux / macOS bash specifics:**

1. Heredocs work as expected; `--body-file -` over stdin is reliable.
2. `base64 -w 0` (GNU coreutils) vs `base64` (BSD/macOS without `-w`) — use `base64 | tr -d '\n'` for portability.

**Artifact freshness — keep CodeQL pins and Dependabot grouping current:**

1. **CodeQL workflow uses Action majors.** The templates pin `actions/checkout` and `github/codeql-action/*` to the **current upstream major** at the time the skill is run (today: `actions/checkout@v6`, `github/codeql-action/{init,autobuild,analyze}@v4`). Pinning to stale majors causes Dependabot to fire one PR per action within minutes of the artifact PR merging. When a new major ships upstream, update both `references/script-template.sh` and `references/script-template.ps1`.
2. **Dependabot `github-actions` ecosystem must use `groups:`.** The templates batch all action bumps into a single weekly PR via a wildcard group. Without grouping, a fresh repo with several behind-by-a-major actions immediately spawns N separate PRs after hardening.

---

## Knowledge Reference

`gh` CLI, GitHub REST API v3, branch protection rules, CODEOWNERS syntax, GitHub Actions permissions model, Dependabot, secret scanning, push protection, GitHub Advanced Security (GHAS), CodeQL, merge queue, rulesets API, DCO, CLA, NYDFS 23 NYCRR 500, squash merge, OWASP Top 10, conventional commits, semantic versioning

---

## Reference Guide

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Bash command playbook (Linux/macOS) — `gh api` calls and artifact bodies | `references/script-template.sh` | Steps 5 + 6 — issuing API calls or rendering artifact bodies |
| PowerShell command playbook (Windows) — `gh api` calls and artifact bodies | `references/script-template.ps1` | Steps 5 + 6 — issuing API calls or rendering artifact bodies |

The `references/` files are full executable scripts; treat them as the source of truth for the exact endpoint, payload, ordering, and content of every operation. When `emit-script=true`, save the executed command sequence as an audit artifact based on these playbooks.
