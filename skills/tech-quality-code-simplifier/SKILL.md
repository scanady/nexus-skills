---
name: tech-quality-code-simplifier
description: 'Simplifies and refines code for clarity, consistency, and maintainability while preserving all functionality. Use when asked to simplify code, clean up code, refactor for readability, reduce complexity, apply coding standards, or improve code elegance. Focuses on recently modified code unless instructed otherwise.'
---

# Code Simplifier

Simplify and refine code for clarity, consistency, and maintainability while preserving exact functionality. Apply project-specific best practices from documentation, custom instructions, or equivalent project standards.

## Principles

1. **Preserve functionality** — Never change what the code does, only how it does it.
2. **Clarity over brevity** — Explicit, readable code beats clever one-liners. Avoid nested ternaries; prefer switch/if-else for multiple conditions.
3. **Balanced simplification** — Don't over-simplify. Keep helpful abstractions, avoid dense logic that's hard to debug or extend.
4. **Scoped changes** — Only refine recently modified code unless explicitly told to review broader scope.

## Workflow

1. Identify recently modified code sections (check git diff, session changes, or user-indicated files)
2. Analyze for complexity reduction, redundancy, and standards alignment
3. Apply refinements:
   - Reduce unnecessary nesting and complexity
   - Eliminate redundant code and abstractions
   - Improve variable/function naming
   - Consolidate related logic
   - Remove obvious-code comments
   - Sort imports, fix extensions, align with project conventions
4. Verify all original behavior is preserved
5. Document only significant changes that affect understanding

## Project Standards to Enforce

When a project has a custom instructions or equivalent standards file, follow it. Common standards to check for:

- **Imports**: ES modules, proper sorting, file extensions
- **Functions**: `function` keyword over arrow functions for top-level declarations
- **Types**: Explicit return type annotations on top-level functions
- **React**: Explicit Props types, proper component patterns
- **Error handling**: Prefer Result patterns over try/catch when possible
- **Naming**: Consistent conventions throughout

## Anti-Patterns to Fix

| Problem | Fix |
|---------|-----|
| Nested ternaries | Switch statement or if/else chain |
| Deep nesting (3+ levels) | Early returns, extract functions |
| Redundant abstractions | Inline if used once, simplify if trivial |
| Obvious comments (`// increment i`) | Remove |
| Inconsistent naming | Align with project conventions |
| Overly clever code | Rewrite for clarity |

## Anti-Patterns to Avoid Introducing

- Dense one-liners that sacrifice readability
- Combining too many concerns into single functions
- Removing abstractions that improve organization
- Over-engineering simple logic
- Prioritizing "fewer lines" over maintainability
```
