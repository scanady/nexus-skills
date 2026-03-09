# UX Design Principles

applyTo: "**/*.tsx,**/*.jsx,**/*.vue,**/*.svelte"

---

## Core Principles

**Prefer inline/contextual controls over separate settings pages:**
- Visibility toggles, edit buttons, and status indicators should appear next to the content they control
- Avoid forcing users to navigate away to change settings
- Example: Eye icon toggle on each profile section, not a "Visibility Settings" modal

**Progressive disclosure:**
- Show essential controls always; reveal advanced options on hover/expand
- Don't overwhelm with all options at once

**Immediate feedback:**
- Changes should be visually reflected immediately (optimistic UI)
- Use inline validation, not form-level error summaries

**Reduce cognitive load:**
- Group related actions together
- Use consistent patterns across similar components

## UX Review Checkpoint

When implementing a new UI feature, BEFORE writing code:
1. Propose 2-3 UX pattern alternatives with trade-offs
2. Recommend the pattern that minimizes user friction
3. Only proceed after confirming the approach (or if the choice is obvious)

## Preferred UI Patterns

| Feature | ✅ Preferred | ❌ Avoid |
|---------|-------------|----------|
| Visibility controls | Inline eye icon toggle per item | Settings modal/page |
| CRUD operations | Inline editing with save/cancel | Separate edit pages |
| Status changes | Dropdown or toggle in place | Confirmation dialogs |
| Bulk actions | Checkbox selection + floating action bar | Individual action buttons |
| Form validation | Inline field-level errors | Form-level error summary |
| Loading states | Skeleton/shimmer in place | Full-page spinner |
