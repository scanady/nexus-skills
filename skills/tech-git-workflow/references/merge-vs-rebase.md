# Merge vs Rebase

## Merge (Preserves History)

```bash
# Creates a merge commit
git checkout main
git merge feature/user-auth

# Result:
# *   merge commit
# |\
# | * feature commits
# |/
# * main commits
```

**Use when:**
- Merging feature branches into `main`
- You want to preserve exact history
- Multiple people worked on the branch
- The branch has been pushed and others may have based work on it

## Rebase (Linear History)

```bash
# Rewrites feature commits onto target branch
git checkout feature/user-auth
git rebase main

# Result:
# * feature commits (rewritten)
# * main commits
```

**Use when:**
- Updating your local feature branch with latest `main`
- You want a linear, clean history
- The branch is local-only (not pushed)
- You're the only one working on the branch

## Rebase Workflow

```bash
# Update feature branch with latest main (before PR)
git checkout feature/user-auth
git fetch origin
git rebase origin/main

# Fix any conflicts, then continue
git rebase --continue

# Force push (only when you're the sole contributor)
git push --force-with-lease origin feature/user-auth
```

## When NOT to Rebase

```
# NEVER rebase branches that:
- Have been pushed and others have based work on them
- Are protected branches (main, develop)
- Are already merged

# Why: rebase rewrites history, breaking others' work
# Use git revert instead for public branch corrections
```
