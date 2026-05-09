---
name: tech-dev-git-start-branch
description: Start a new GitHub Flow branch from an up-to-date base — infers branch type, derives a kebab-case name, pulls latest main, creates the branch, and sets up upstream tracking. Use when "start a branch", "create a feature branch", "new fix branch", "begin work on", "checkout a new branch", "spin up a branch", or "start working on a new task".
license: MIT
metadata:
  version: "1.0.0"
  domain: tech
  triggers: start a branch, create a branch, new feature branch, new fix branch, begin work, spin up branch, start working on, checkout new branch, create branch from main, start github flow, new branch
  anti-triggers: commit changes, push work, merge branch, open PR, finish branch, rebase, conflict resolution, branching strategy
  role: developer
  scope: workflow
  output-format: commands
  priority: specific
  related-skills: tech-dev-git-commit, tech-dev-git-finish-branch, tech-dev-git-workflow-design
---

# Start a Development Branch

## Overview

Start a properly named GitHub Flow branch from an up-to-date base.

**Core principle:** Name it → Update base → Create → Confirm.

**Announce at start:** "I'm using the tech-dev-git-start-branch skill to set up your branch."

## The Process

### Step 1: Identify Work Type

If not clear from context, ask: "What are you working on — is it a feature, fix, chore, docs, or test?"

Map to prefix:

| Prefix | Use for |
|--------|---------|
| `feature/` | New capability |
| `fix/` | Bug fix |
| `chore/` | Maintenance, deps, config |
| `docs/` | Documentation only |
| `test/` | Test-only changes |
| `perf/` | Performance improvement |
| `refactor/` | Restructuring, no behavior change |

### Step 2: Derive Branch Name

Generate a name from the description:
- Lowercase, kebab-case only
- Max 50 chars total (including prefix)
- Drop articles, prepositions, filler words
- Prepend ticket/issue number if provided

Examples:
- "Add user authentication" → `feature/add-user-auth`
- "Fix null pointer on login" → `fix/null-pointer-login`
- "Update dependencies" → `chore/update-deps`
- "JIRA-123 Payment flow" → `feature/JIRA-123-payment-flow`

**Propose before executing:**

```
Branch: feature/add-user-auth
Base:   main

Proceed?
```

### Step 3: Update Base Branch

Detect the base branch:

```bash
git remote show origin | grep 'HEAD branch' | awk '{print $NF}'
```

Pull it fast-forward only:

```bash
git checkout main
git pull --ff-only
```

**If fast-forward fails (base has diverged):** Stop and report:

```
main has diverged from origin/main.
Run: git pull --rebase origin main
Then retry.
```

Do not proceed past this step until the base is clean.

### Step 4: Create and Checkout

```bash
git checkout -b <branch-name>
```

### Step 5: Push and Set Upstream

Establish remote tracking immediately:

```bash
git push -u origin <branch-name>
```

If the remote rejects an empty push (branch protection policy), skip this — the upstream will be set on the first real commit with `git push -u origin <branch-name>`.

### Step 6: Confirm

Report state and next steps:

```
Branch ready: feature/add-user-auth
Base: main (up to date)
Tracking: origin/feature/add-user-auth

Next:
- Make changes, then commit: /tech-dev-git-commit
- When work is complete:   /tech-dev-git-finish-branch
```

## Constraints

### MUST DO
- Always pull the base before creating the branch
- Always propose the branch name before executing
- Use `--ff-only` to detect a diverged base rather than silently creating a merge commit

### MUST NOT DO
- Don't create from a stale local base
- Don't skip the name proposal step
- Don't use spaces, uppercase, or special characters in branch names
- Don't `--force` push at branch creation
