# Output Templates Reference

Formatting templates and structural patterns for sitemap deliverables. This reference is loaded when producing the final sitemap document, formatting page entries, or structuring the output.

## Table of Contents

1. [Sitemap Document Template](#sitemap-document-template)
2. [Page Entry Format](#page-entry-format)
3. [Page Detail Card Format](#page-detail-card-format)
4. [Tree Notation](#tree-notation)
5. [Flow Map Format](#flow-map-format)
6. [Navigation Architecture Format](#navigation-architecture-format)

## Sitemap Document Template

Use this structure for the full sitemap deliverable:

```markdown
# [Application Name] — Application UX Sitemap

**Version**: [X.Y]
**Date**: [Date]
**Status**: [Draft | Review | Approved]
**Source**: [PRD reference or requirements source]

## Purpose

[1-2 sentences: what this sitemap defines and what it drives downstream]

## User Roles

| Role | Description | Primary Goals |
|------|-------------|---------------|
| [Role Name] | [Who they are] | [What they need to accomplish] |

## Navigation Architecture

[Navigation model, layers, breadcrumb strategy — see Navigation Architecture Format below]

## Page Hierarchy

[Full tree — see Tree Notation below]

## Page Details

[Expanded cards for complex pages — see Page Detail Card Format below]

## Primary User Flows

[Flow maps for top 3-5 workflows — see Flow Map Format below]

## Scalability & Future Considerations

[Growth notes, known limitations, expansion points]
```

## Page Entry Format

Each page in the hierarchy tree uses this compact format:

### Compact (In-Tree) Format

For the tree view, each page entry is a single line with key metadata inline:

```
○ Page Name — [purpose] (Archetype: [type]) [/route/pattern]
```

Example:
```
○ Product Catalog — Browse and search all products (Archetype: Listing) [/products]
```

### Expanded (Below-Tree) Format

For pages that need more detail, use a structured block:

```markdown
### Page Name
- **Route**: `/route/pattern`
- **Purpose**: [What the user accomplishes here]
- **Archetype**: [Dashboard | Listing | Detail | Form | Settings | Onboarding | Report | Search Results]
- **Access**: [Roles that can access this page]
- **Primary Action**: [The single most important action]
- **States**: [empty, loading, populated, error, + domain-specific]
```

## Page Detail Card Format

For high-traffic or complex pages, provide a visual layout description:

```markdown
### [Page Name] — Detail Card

**Route**: `/route/pattern`
**Archetype**: [Type]
**Access**: [Roles]

**Layout:**
┌──────────────────────────────────────────────────────────────┐
│  Breadcrumbs: Home > Section > Page                          │
│                                                              │
│  Page Title                        [Secondary] [+ Primary]  │
│  Subtitle — what this page helps the user do                 │
├──────────────────────────────────────────────────────────────┤
│  [Content Zone 1 — describe what goes here]                  │
│                                                              │
│  [Content Zone 2 — describe what goes here]                  │
│                                                              │
│  [Content Zone 3 — describe what goes here]                  │
└──────────────────────────────────────────────────────────────┘

**States:**
- **Empty**: [Description of empty state — what message, what CTA]
- **Loading**: [Skeleton pattern — which zones show skeletons]
- **Populated**: [Default view with data]
- **Error**: [Error state — what message, what recovery action]
- **[Domain-specific]**: [Any additional states]

**Key Interactions:**
- [Interaction 1]: [What happens]
- [Interaction 2]: [What happens]
```

## Tree Notation

Use indented tree notation for the full page hierarchy. Consistent symbols maintain visual clarity:

### Symbols

| Symbol | Meaning |
|--------|---------|
| `○` | Page (navigable endpoint) |
| `├` | Branch connector (non-terminal child) |
| `└` | Branch connector (terminal child) |
| `│` | Vertical line (continuing branch) |
| `◆` | Section header (navigation group, not a page itself) |
| `🔒` | Restricted access (role-gated) |
| `⟳` | Modal/Drawer (overlay, not a full page route) |

### Tree Example

```
◆ Primary Navigation
│
├── ○ Dashboard — Application overview (Archetype: Dashboard) [/]
│
├── ◆ Products
│   ├── ○ Product Catalog — Browse all products (Archetype: Listing) [/products]
│   ├── ○ Product Detail — View single product (Archetype: Detail) [/products/:id]
│   │   ├── Tab: Overview
│   │   ├── Tab: Coverage & Benefits
│   │   ├── Tab: Riders
│   │   ├── Tab: Rate Tables
│   │   └── Tab: Filing History
│   ├── ○ Create Product — New product wizard (Archetype: Form) [/products/create]
│   └── ⟳ Quick View — Product preview drawer
│
├── ◆ Administration 🔒
│   ├── ○ User Management — Manage team members (Archetype: Listing) [/admin/users]
│   └── ○ Audit Log — System activity history (Archetype: Listing) [/admin/audit]
│
└── ◆ Utility Navigation
    ├── ○ Settings — Application preferences (Archetype: Settings) [/settings]
    ├── ○ Account — User profile and security (Archetype: Settings) [/account]
    └── ○ Help & Docs — Documentation and support [/help]
```

### Notation Rules
- Indent each level by 4 spaces
- Use `◆` for navigation group headers that aren't pages themselves
- Use `○` for every navigable page
- Include archetype and route inline for the tree view
- Append `🔒` to sections or pages with restricted access
- Use `⟳` for modals/drawers that overlay rather than navigate
- Tabs within a detail page are listed as `Tab:` entries (not full pages)

## Flow Map Format

Map user workflows step-by-step through the page tree:

```markdown
### Flow: [Flow Name]

**Goal**: [What the user is trying to accomplish]
**Starting point**: [Where the user begins]
**Roles**: [Which roles perform this flow]

| Step | Page | Action | Next |
|------|------|--------|------|
| 1 | Dashboard [/] | Click "Create Product" quick action | Product Creation |
| 2 | Create Product [/products/create] | Fill product basics (Step 1 of 3) | Step 2 |
| 3 | Create Product [/products/create?step=2] | Configure coverage | Step 3 |
| 4 | Create Product [/products/create?step=3] | Review and submit | Product Detail |
| 5 | Product Detail [/products/:id] | View created product | — (Flow complete) |

**Click depth**: 5 steps from dashboard to completion
**Shortcuts**: Dashboard quick action saves 1 click vs. navigating through Product Catalog
**Cross-links**: Step 2 allows selecting existing rate tables via inline search (no navigation away)
```

### Flow Validation Criteria
- Primary workflows should complete in ≤5 steps
- The first meaningful action should be reachable in ≤3 clicks from the entry point
- Every step should have a clear "back" or "cancel" path
- Cross-cutting references (e.g., selecting an item from another section) should use inline search or drawers, not full navigation away

## Navigation Architecture Format

Document the navigation model with this structure:

```markdown
## Navigation Architecture

### Model: [Sidebar | Top Bar | Hybrid | Tab Bar]

**Rationale**: [Why this model was chosen for this application]

### Primary Navigation (Sidebar / Top Bar)
- [Section 1] → [/route]
- [Section 2] → [/route]
  - [Subsection A] → [/route]
  - [Subsection B] → [/route]
- [Section 3] → [/route]

### Utility Navigation (Top-Right / Sidebar Footer)
- Search (Cmd+K)
- Notifications
- Account / Profile
- Settings
- Help

### Secondary Navigation
[How sub-navigation works within each section: tabs, sub-sidebar, breadcrumb-driven]

### Breadcrumb Strategy
- Pattern: `Home > Section > Subsection > Page`
- Dynamic segments use entity display names
- Always visible except on root dashboard

### Mobile Adaptation
[How the navigation transforms on mobile: drawer, bottom tabs, etc.]
```

## Formatting Conventions

### General Rules
- Use Markdown headers (##, ###) for document structure
- Use tables for structured data (roles, flows, page inventories)
- Use ASCII art boxes for layout diagrams — keep them simple and legible
- Use consistent indentation (4 spaces) for tree notation
- Bold key terms on first use
- One blank line between sections, no horizontal rules

### Naming Conventions
- Page names: Title Case, action-oriented when possible ("Create Product" not "Product Creation Form")
- Route patterns: lowercase, kebab-case, with `:param` for dynamic segments
- Section headers: Title Case, noun-based ("Products" not "Manage Products")
- Tab labels: Title Case, short (1-2 words)

### Status and State Labels
Use consistent terminology for page and entity states:

| Term | Meaning |
|------|---------|
| Empty | No data exists yet — show onboarding guidance |
| Loading | Data is being fetched — show skeleton |
| Populated | Data exists and is displayed — default view |
| Error | Data fetch or action failed — show error message with recovery action |
| Filtered (zero results) | Data exists but filters return nothing — show "clear filters" suggestion |
