# Pre-Discovery

For features spanning multiple domains (auth, database, UI, etc.) that need front-loaded technical context before the Feature Forge interview.

## Overview

For features spanning multiple domains, you can accelerate discovery by gathering focused technical context BEFORE starting the Feature Forge interview. This front-loads technical context so the interview focuses on decisions rather than exploration.

## When to Use

- Feature touches 3+ distinct system layers (e.g., auth, database, UI)
- Codebase is unfamiliar or underdocumented
- You need concrete technical facts before asking requirements questions
- Stakeholder time is limited and you want to minimize back-and-forth

## When NOT to Use

- Feature is well-scoped to a single domain
- You already have deep codebase knowledge
- Requirements are purely business/UX (no technical exploration needed)

## Pattern

```
1. Identify domains the feature touches
2. Gather facts in parallel where possible:
  - Existing patterns and constraints
  - Current implementation details
  - Security, privacy, and authorization requirements
  3. Collect findings from all discovery passes
4. Begin Feature Forge interview with technical context loaded
5. Focus interview on decisions, trade-offs, and requirements
```

## Example

For a "user profile with avatar upload" feature:

```
Discovery pass 1:
  "Analyze the current user model, storage patterns, and image handling in this codebase"

Discovery pass 2:
  "What security concerns exist for file upload in this stack?"

Discovery pass 3:
  "How does this project handle API endpoints and file storage?"
```

Results feed into the Feature Forge interview, so questions like "Where should we store avatars?" come with context about existing patterns.

## Integration with Interview Questions

See `interview-questions.md` for the full pre-discovery pattern and how technical findings map to interview categories.
