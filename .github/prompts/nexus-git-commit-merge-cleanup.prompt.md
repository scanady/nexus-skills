---
description: Commit changes, merge current feature branch to default branch, and delete the feature branch
agent: agent
---

# Git Branch Merge and Cleanup

Commit all pending changes, merge the current feature branch into the default branch, and clean up by deleting the feature branch both locally and remotely.

## Inputs

**Commit message:** ${input:commitMessage:Enter the commit message for any uncommitted changes (leave empty to skip commit)}

## Workflow

### 1. Check Current State

Determine:
- Current branch name
- Default branch name (typically `main` or `master`)
- Whether there are uncommitted changes

### 2. Commit Changes (if any)

If there are uncommitted changes and a commit message was provided:
1. Stage all changes: `git add -A`
2. Commit with the provided message
3. Push to remote

If there are uncommitted changes but no commit message was provided:
- Stop and inform the user they have uncommitted changes

### 3. Merge to Default Branch

1. Checkout the default branch
2. Pull latest changes from remote
3. Merge the feature branch (fast-forward if possible)
4. Push the merged default branch to remote

### 4. Delete Feature Branch

1. Delete the local feature branch
2. Delete the remote feature branch

### 5. Confirm Completion

Report:
- ✅ Changes committed (if applicable)
- ✅ Branch merged to [default branch]
- ✅ Local branch deleted
- ✅ Remote branch deleted

## Error Handling

- If merge conflicts occur, stop and report the conflict
- If push fails, report the error and suggest resolution
- If branch deletion fails, report which deletion failed

## Safety Checks

Before proceeding:
- Confirm the current branch is NOT the default branch
- Confirm all tests pass (if test command is known)
- Warn if there are uncommitted changes and no commit message provided
