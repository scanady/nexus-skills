# Coding Design Principles

applyTo: "**/*"

---
## DON'T BE A QUITTER: aka The Ed Mitchell Principle
**Always complete the task at hand. Never leave code half-done.**
- **No stubs or TODOs:** Do NOT commit code with `// TODO`, `// FIXME`, `throw new NotImplementedException()`, or commented-out sections. Every code path must be fully implemented.
- **No dead ends:** If you start implementing a feature or fix, you must see it through to completion in the same change. This includes updating all callers, tests, and documentation.
- **No partial implementations:** Every public API, endpoint, or component must be fully functional when committed. Incomplete features must be developed in feature branches until done.


## THE PRIME DIRECTIVE: AGGRESSIVE MODERNIZATION

**This repository follows a "No-Legacy" policy. Safety and backward compatibility are secondary to code cleanliness.**

- **Atomic Refactoring:** You are REQUIRED to break existing code and APIs to accommodate better design. If you change a method signature, you must immediately find and refactor all callers in the workspace.
- **Prohibited Patterns:**
  - DO NOT use `@Deprecated`.
  - DO NOT use `v2`, `New`, or `Legacy` designations (including prefixes, suffixes or embedded) in class/method names.
  - DO NOT use `if/else` logic to toggle between old and new behavior.
  - DO NOT keep unused private methods "just in case."
- **Purge on Update:** When modifying a file, your first action is to identify and delete logic rendered obsolete by the new requirement. Refactor over Supplement.

## DRY (Don't Repeat Yourself)

**Every piece of knowledge must have a single, unambiguous, authoritative representation.**

- **Extract shared logic:** If the same logic appears in 2+ places, extract it into a shared utility, hook, or component immediately.
- **Single source of truth:** Constants, configuration, and type definitions must live in one canonical location—never duplicate them across files.
- **Reusable components:** UI patterns appearing multiple times must be abstracted into shared components.
- **No cross-boundary duplication:** Data that exists in the backend must NOT be replicated as static files in the frontend—fetch from the API and cache for performance.
- **No copy-paste coding:** Before duplicating code, extract and reuse. When refactoring duplicates, update ALL call sites in the same change.

## NO STATIC DATA WORKAROUNDS

**This is a frontend application that integrates with a backend API. The backend is the source of truth.**

- **Never hardcode data to bypass API issues:** If a backend endpoint returns 404 or errors, that is a backend bug to be fixed—not a frontend problem to work around with static data.
- **Never replace API calls with constants:** Hooks and services must always fetch from the backend. Replacing `useQuery` with static arrays is forbidden.
- **Never "fix" console errors by eliminating the request:** A 404 error means the backend contract is incomplete. File an issue, coordinate with backend, or implement the endpoint—do not silence the symptom.
- **Never accept failing tests by mocking away the problem:** If tests fail due to missing API endpoints, the fix is implementing those endpoints, not stubbing static responses.
- **Reference data belongs in the backend:** Product lines, target markets, jurisdictions, and other reference data must come from API endpoints, not hardcoded frontend constants.

**When encountering missing backend endpoints:**
1. Identify the missing endpoint and expected contract
2. Create a backend implementation task/issue
3. Implement the backend endpoint OR coordinate with the backend team
4. Only then update the frontend to consume it

**The frontend's job is to render data from the backend, not to manufacture it.**

## Verification Protocol

### When to Run Compilation Checks

Run compilation **after completing a logical unit of work**, not after every single edit:
- After renames/refactors that touch multiple files
- After API contract changes (endpoints, DTOs)
- After adding/removing imports or dependencies
- Before committing

**Skip compilation** for simple, isolated edits where the impact is obvious.

### Rename/Refactor Checklist

When renaming ANY symbol (class, method, field, type, endpoint, hook, component):
1. **Search entire workspace** for the old name: `grep_search` with `isRegexp: false`
2. **Search for related terms** (e.g., if renaming `template` → `blueprint`, also search for `Template`, `TEMPLATE`, `templateId`, etc.)
3. **Check cross-boundary references**: Backend renames often require frontend updates and vice versa
4. **Update ALL references** before running compilation
5. **Run compilation checks** on both backend AND frontend
6. **Delete old files** rather than leaving duplicates

### API Contract Changes

When modifying backend API endpoints or DTOs:
1. Search frontend for the endpoint path (e.g., `/offerings/templates`)
2. Search frontend for the DTO field names being changed
3. Update frontend types, hooks, and components BEFORE declaring the change complete
