# Sitemap Patterns Reference

Page archetypes, navigation models, and layout patterns for application sitemaps. This reference is loaded when designing page hierarchy, choosing navigation models, or defining page types.

## Table of Contents

1. [Page Archetypes](#page-archetypes)
2. [Navigation Models](#navigation-models)
3. [Layout Composition Patterns](#layout-composition-patterns)
4. [Section Organization Patterns](#section-organization-patterns)
5. [Responsive Navigation Adaptation](#responsive-navigation-adaptation)

## Page Archetypes

Every page in an application sitemap maps to one of these structural archetypes. The archetype determines the page's layout skeleton, expected content zones, and interaction model.

### Dashboard

**Purpose:** Entry point for a section or the entire application. Summarizes state and surfaces actionable items.

**Content zones:**
- Metric summary cards (3-5 KPIs)
- Attention/alert section (items needing action)
- Quick actions (shortcut buttons to common tasks)
- Activity feed or recent items
- Optional: charts/trends for the current period

**Key characteristics:**
- Glanceable: users should extract key information within 5 seconds
- Actionable: every metric and alert links to its detail or filtered view
- Personalized: content should reflect the user's role, permissions, and recent activity

**Route patterns:** `/`, `/dashboard`, `/:section/dashboard`

### Listing (Collection View)

**Purpose:** Browse, search, filter, and act on a collection of entities.

**Content zones:**
- Search + filter bar (sticky)
- Active filter chips (dismissible)
- Collection display (card grid or data table)
- Bulk action bar (appears on selection)
- Pagination or infinite scroll controls
- Empty state (when no items exist or filters return zero results)

**Display variants:**
- **Card grid**: Best for visual items, products, templates — scannable with images and metadata
- **Data table**: Best for structured data with sortable columns — filings, transactions, audit logs
- **Compact list**: Best for high-volume items — notifications, search results, log entries

**Route patterns:** `/:section`, `/:section/list`, `/:section?filter=value`

### Detail (Entity View)

**Purpose:** View and manage a single entity with full context.

**Content zones:**
- Entity header (name, status badge, primary action, secondary actions)
- Tabbed sub-sections for entity facets
- Contextual sidebar (optional: related items, metadata, activity timeline)
- Section content area (varies per tab)

**Tab strategy:**
- First tab = overview or most-used facet
- Order tabs by frequency of access, not alphabetically
- Show count badges on tabs with variable item counts
- Keep tab count to 5-7 maximum; use "More" dropdown if needed

**Route patterns:** `/:section/:id`, `/:section/:id/:tab`

### Form (Create / Edit)

**Purpose:** Capture or modify structured data.

**Variants:**
- **Single-page form**: For simple entities with fewer than 10 fields. All fields visible, submit at bottom.
- **Stepped / Wizard form**: For complex creation flows with 10+ fields or logical groupings. Step indicator at top, next/back navigation, summary review before submit.
- **Inline edit**: For modifying individual fields on a detail page without navigating away. Edit icon triggers field-level form state.
- **Drawer/Modal form**: For quick-create flows that don't warrant a full page. Used for adding related entities from within a parent's detail view.

**Content zones:**
- Step indicator (for wizards)
- Field groups with section headers
- Validation messages (inline per field + summary at top)
- Action bar (Save/Cancel, or Next/Back for wizards)
- Unsaved changes warning on navigation away

**Route patterns:** `/:section/create`, `/:section/:id/edit`, `/:section/create?step=2`

### Settings

**Purpose:** Configure application, account, or entity preferences.

**Content zones:**
- Settings category sidebar or vertical tab list
- Settings panel with grouped controls
- Save/discard controls per section (not per field)

**Organization:**
- Group settings by theme (General, Notifications, Security, Integrations, etc.)
- Place most-used settings first
- Use progressive disclosure: advanced settings behind a "Show advanced" toggle
- Each settings category should be independently saveable

**Route patterns:** `/settings`, `/settings/:category`

### Onboarding / Empty State

**Purpose:** Guide first-time users to their initial action. Replace blank screens with contextual guidance.

**Content zones:**
- Welcome message with user's name
- Value proposition (what this section will help them do)
- Primary CTA (the first action they should take)
- Optional: quick-start checklist, sample data option, tutorial link

**Key rule:** Every listing and dashboard page needs a designed empty state. "No items found" is never acceptable as a production empty state.

**Route patterns:** Same as the page it replaces — this is a state, not a separate route.

### Report / Analytics

**Purpose:** Explore data, generate insights, and export findings.

**Content zones:**
- Date range / filter controls
- Chart area (multiple chart types per report)
- Data table below charts (exportable)
- Saved report configurations

**Route patterns:** `/reports`, `/reports/:reportId`, `/analytics`

### Search Results

**Purpose:** Display results from global or section-scoped search.

**Content zones:**
- Search input (pre-filled with query, editable)
- Result count and scope indicator
- Grouped results by type (products, users, settings, etc.)
- Each result: title, excerpt, breadcrumb showing where it lives
- Pagination or load-more

**Route patterns:** `/search?q=query`, `/:section/search?q=query`

## Navigation Models

### Sidebar Navigation (Collapsible)

```
┌──────────┬──────────────────────────────────────────┐
│ ≡ Logo   │  Header / Breadcrumbs                    │
│          │                                          │
│ ○ Home   │                                          │
│ ○ Sec A  │         Content Area                     │
│  ├ Sub 1 │                                          │
│  └ Sub 2 │                                          │
│ ○ Sec B  │                                          │
│ ○ Sec C  │                                          │
│          │                                          │
│ ─────── │                                          │
│ ○ Settings│                                         │
│ ○ Account │                                         │
└──────────┴──────────────────────────────────────────┘
```

**When to use:** Enterprise apps, B2B SaaS, admin panels with 6+ top-level sections.

**Behavior:**
- Collapsible to icon-only mode for more content space
- Grouped sections with optional group headers
- Active state shows current section and page
- Badge counts for attention items (notifications, pending approvals)
- Footer area for account, settings, and collapse toggle

### Top Bar Navigation

```
┌──────────────────────────────────────────────────────┐
│  Logo    Home   Section A   Section B   Section C  🔍 👤 │
├──────────────────────────────────────────────────────┤
│                                                      │
│                   Content Area                       │
│                                                      │
└──────────────────────────────────────────────────────┘
```

**When to use:** Consumer apps, marketing dashboards, apps with 3-5 top-level sections.

**Behavior:**
- Horizontal link list with active underline indicator
- Overflow into "More" dropdown when sections exceed available width
- Search and account controls right-aligned
- Mobile: collapses into hamburger menu

### Bottom Tab Bar (Mobile)

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│                   Content Area                       │
│                                                      │
├──────────────────────────────────────────────────────┤
│   🏠 Home    📋 Items    ➕    🔔 Alerts    👤 Me    │
└──────────────────────────────────────────────────────┘
```

**When to use:** Mobile-first apps with 3-5 core actions.

**Behavior:**
- Maximum 5 items (iOS/Android convention)
- Center item can be elevated for primary creation action
- Badge dots for unread counts
- Active state with filled icon + label

### Sidebar + Top Bar Hybrid

```
┌──────────────────────────────────────────────────────┐
│  Logo    Context Switcher ▾     🔍  🔔  👤           │
├──────────┬───────────────────────────────────────────┤
│ ○ Sec A  │  Breadcrumbs                              │
│ ○ Sec B  │                                           │
│ ○ Sec C  │         Content Area                      │
│ ○ Sec D  │                                           │
└──────────┴───────────────────────────────────────────┘
```

**When to use:** Multi-tenant platforms, apps with both workspace-level and section-level navigation.

**Behavior:**
- Top bar handles workspace/context switching and global actions
- Sidebar handles section navigation within the current context
- Allows two independent navigation dimensions without confusion

## Layout Composition Patterns

### Master-Detail

A listing panel on the left, detail panel on the right. Selecting an item in the list reveals its detail without full page navigation.

**When to use:** Email clients, file managers, entity browsers where rapid switching between items is the primary workflow.

**Route pattern:** `/:section/:id` — but the listing remains visible.

### Split View

Two independent content panels side by side. Each can navigate independently.

**When to use:** Comparison tools, code editors, translation interfaces, side-by-side document review.

### Contextual Drawer

A panel that slides in from the right (or bottom on mobile) to show secondary content without leaving the current page.

**When to use:** Quick-view previews from listing pages, create/edit forms for related entities, help panels, activity logs.

### Stepped Flow (Wizard)

A linear sequence of pages with a progress indicator. Forward/back navigation with final review step.

**When to use:** Complex creation flows (onboarding, multi-step forms, checkout). When the process has a clear start and end with distinct phases.

## Section Organization Patterns

### By User Goal (Recommended)

Group sections by what users are trying to accomplish:
- **Create & Manage** — Products, Templates, Components
- **Monitor & Analyze** — Dashboard, Reports, Analytics
- **Configure** — Settings, Integrations, Team
- **Review & Approve** — Pending Approvals, Audit Log

### By Entity (Use Sparingly)

Group by business object — only when the domain model maps cleanly to user mental models:
- Products, Customers, Orders, Invoices

**Warning:** Entity-based organization often mirrors the database, not the user's workflow. Validate that users think in terms of these entities before committing.

### By Workflow Phase

Group by stages of a process:
- **Design** — Templates, Builders, Preview
- **Review** — Submissions, Approvals, Comments
- **Launch** — Publishing, Distribution, Monitoring

## Responsive Navigation Adaptation

### Desktop → Tablet

- Sidebar: auto-collapse to icon-only mode, expand on hover or click
- Top bar: move lower-priority items into "More" overflow dropdown
- Master-detail: stack vertically (list above, detail below) or use drawer for detail

### Desktop → Mobile

- Sidebar: convert to off-canvas drawer triggered by hamburger menu
- Top bar: collapse to hamburger + logo + key action button
- Bottom tab bar: remains fixed
- Master-detail: convert to full-screen list → full-screen detail with back button
- Tables: convert to card layout or horizontal scroll
- Multi-column layouts: stack to single column

### Navigation Depth on Mobile

On mobile, limit navigation depth to 2 levels:
1. Primary nav (bottom tabs or drawer)
2. Content + contextual back navigation

Avoid nested sub-menus on mobile. Use full-screen list views with back buttons instead of hierarchical menus.
