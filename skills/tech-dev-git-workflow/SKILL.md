---
name: tech-dev-git-workflow
description: Full git lifecycle skill — inspect diff, craft tight conventional commit messages, stage, commit, push. Use when asked to commit changes, write a commit message, push work, commit and push, save to remote, stage changes, or complete a git workflow.
license: MIT
metadata:
  version: "1.0.0"
  domain: tech
  triggers: commit, push, git workflow, write commit message, commit and push, push changes, push to github, push this, stage changes, commit message, git commit, git push, save to remote, push to remote
  role: developer
  scope: workflow
  output-format: command
  related-skills: content-copy-caveman
---

# Git Workflow

Full git cycle: inspect → message → stage → commit → push.

## Role

You = senior dev. Know git deep. Own full commit lifecycle. Commit msgs = caveman full: tight, accurate, ≤50 char subject. Platform-agnostic always. No bash-isms.

## Commit Message Style

Caveman full ON for all commit messages. Compress hard. Keep technical truth.

Format: `type(scope): short desc`

Types:
- `feat` = new capability
- `fix` = broke thing fixed
- `docs` = docs only
- `style` = format, whitespace
- `refactor` = no behavior change
- `test` = tests added or fixed
- `chore` = maintenance, deps
- `perf` = faster
- `ci` = pipeline/build config

Rules:
- Subject ≤50 chars
- Imperative mood — "add" not "added"
- No period at end
- Body optional. If needed: why, not what. Ultra-compressed.
- Breaking change: `!` after type + `BREAKING CHANGE:` in footer

Good: `feat(auth): add jwt login`
Bad: `feat(auth): implement JWT-based authentication system with login endpoint, token generation, and validation middleware`

## Workflow

### 1. Inspect

Run before anything else. See what's staged, what's not.

```
git status
git diff
git diff --staged
```

### 2. Analyze Diff

Identify:
- Change type → pick commit type
- Affected area → scope
- Root cause or intent → body if needed
- Any breaking changes → flag with `!`

### 3. Draft Message

Apply caveman full. Subject ≤50 chars.

Examples:
- `fix(api): null check user profile`
- `feat(ui): add dashboard spinner`
- `refactor(db): extract query helpers`
- `chore(ci): bump node to 20`
- `perf(cache): memoize expensive query`
- `feat(api)!: restructure response format`

With body (when why matters):
```
refactor(auth): split service from controller

controller too fat. auth logic now in service layer.
easier to test. no behavior change.
```

Breaking change footer:
```
feat(api)!: restructure response format

BREAKING CHANGE: responses now follow JSON:API spec.
update clients. old: {data, status}. new: {data, meta}.
```

### 4. Stage

Selective preferred — only stage what belongs to this commit:

```
git add -p              # interactive patch selection
git add path/to/file    # specific file
git add path/to/dir/    # specific directory
```

Stage all only when every change belongs to one logical commit:

```
git add -A
```

Confirm staged before moving on:

```
git diff --staged --stat
```

### 5. Commit

Single-line message:

```
git commit -m "type(scope): desc"
```

With body:

```
git commit -m "type(scope): desc" -m "why it changed. impact."
```

### 6. Push

Get current branch:

```
git rev-parse --abbrev-ref HEAD
```

Push (sets upstream on first push, safe on subsequent):

```
git push -u origin <branch>
```

## Constraints

MUST DO:
- Inspect diff before writing message
- Use conventional commits format every time
- Apply caveman full compression to every commit message
- Confirm staged file list before committing
- Use `git push -u origin <branch>` — cross-platform, sets upstream safely

MUST NOT:
- Force push (`--force`, `-f`) without explicit user request
- Write vague messages ("update", "fix stuff", "changes", "wip")
- Blindly stage all when partial commits are more appropriate
- Add agent-specific footers or log entries to commit messages

## Platform Notes

All git commands above work on Linux, macOS, Windows (PowerShell, Git Bash, cmd).

## Quick Reference

| Scenario | Pattern |
|---|---|
| New feature | `feat(scope): add thing` |
| Bug fix | `fix(scope): fix broken thing` |
| Refactor | `refactor(scope): simplify thing` |
| Docs | `docs(scope): update readme` |
| Tests | `test(scope): add unit tests` |
| Config / CI | `chore(scope): update config` |
| Performance | `perf(scope): cache queries` |
| Breaking | `feat(scope)!: change api shape` |
| Selective amend | `git commit --amend --no-edit` |
