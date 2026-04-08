# Anti-Patterns & Quick Reference

## Anti-Patterns

```
# BAD: Committing directly to main
git checkout main
git commit -m "fix bug"
# GOOD: Use feature branches and PRs

# BAD: Committing secrets
git add .env  # Contains API keys
# GOOD: Add to .gitignore, use environment variables

# BAD: Giant PRs (1000+ lines)
# GOOD: Break into smaller, focused PRs

# BAD: Vague commit messages
git commit -m "update"
git commit -m "fix"
# GOOD: Descriptive messages
git commit -m "fix(auth): resolve redirect loop after login"

# BAD: Force-pushing to shared branches ⚠
git push --force origin main
# GOOD: Use revert for public branches
git revert HEAD

# BAD: Long-lived feature branches (weeks/months)
# GOOD: Keep branches short (days), rebase onto main frequently

# BAD: Committing generated files
git add dist/
git add node_modules/
# GOOD: Add to .gitignore
```

## Quick Reference

| Task | Command |
|------|---------|
| Create branch | `git checkout -b feature/name` |
| Switch branch | `git checkout branch-name` |
| Delete branch | `git branch -d branch-name` |
| Merge branch | `git merge branch-name` |
| Rebase branch | `git rebase main` |
| View history | `git log --oneline --graph` |
| View changes | `git diff` |
| Stage changes | `git add .` or `git add -p` |
| Commit | `git commit -m "message"` |
| Push | `git push origin branch-name` |
| Pull | `git pull origin branch-name` |
| Stash | `git stash push -m "message"` |
| Undo last commit | `git reset --soft HEAD~1` |
| Revert commit (safe) | `git revert HEAD` |
