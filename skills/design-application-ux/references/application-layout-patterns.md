# Application Layout Patterns

This reference catalogs proven layout archetypes and page composition patterns for web applications. Use this when choosing the overall application structure, designing specific page types, or composing screens from components.

See also:
- [Core UI/UX Principles](./ui-ux-principles.md) — Strategic design principles
- [Application Aesthetics Guidelines](./aesthetics-guidelines.md) — Visual identity and brand expression
- [Design System Guide](./design-system-guide.md) — Token architecture and component specs
- [Technical Implementation Patterns](./technical-implementation-patterns.md) — Navigation, form, and search implementation

---

## 1. Application Shell Archetypes

The shell is the persistent frame around the content — the sidebar, top bar, and navigation chrome. Choose one shell archetype and use it consistently across the application.

### Sidebar + Top Bar (Enterprise Standard)

```
┌──────────────────────────────────────────────┐
│ Top Bar (logo, search, notifications, avatar) │
├────────┬─────────────────────────────────────┤
│        │                                     │
│ Side-  │         Content Area                │
│  bar   │                                     │
│ (nav)  │                                     │
│        │                                     │
└────────┴─────────────────────────────────────┘
```

**Best for:** Enterprise SaaS, admin panels, internal tools, B2B products, analytics platforms.
**Navigation capacity:** 8-25+ sections (grouped with expandable categories).
**Characteristics:** Sidebar is collapsible. Top bar holds global actions (search, notifications, user menu). Content area is the primary workspace.
**Used by:** Stripe Dashboard, AWS Console, Jira, Notion, Linear, Datadog, Salesforce.

**Implementation notes:**
- Sidebar width: 240-280px expanded, 64px collapsed.
- Top bar height: 48-56px. Fixed position.
- Content area: fills remaining width. Apply internal max-width per page type (e.g., 1200px for forms, full width for tables).
- Mobile: sidebar becomes a full-screen drawer triggered by a hamburger menu.

### Top Bar Only (Consumer / Simple SaaS)

```
┌──────────────────────────────────────────────┐
│ Top Bar (logo, nav links, avatar/CTA)         │
├──────────────────────────────────────────────┤
│                                              │
│               Content Area                   │
│                                              │
│                                              │
└──────────────────────────────────────────────┘
```

**Best for:** Consumer products, marketing sites with app sections, simple SaaS with 3-5 top-level pages.
**Navigation capacity:** 3-7 top-level items.
**Characteristics:** Clean and open. Content gets full viewport width. Less chrome overhead.
**Used by:** Vercel, GitHub (before sidebar era), Twitch, Twitter/X.

**Implementation notes:**
- Top bar: 56-64px. Contains logo, primary nav links, and utility actions (search, notifications, avatar).
- Responsive: nav links collapse to a hamburger menu at < md breakpoint.
- Content max-width: typically constrained to 1200-1440px with auto margins.

### Bottom Tab Bar (Mobile / PWA)

```
┌──────────────────────────────────────────────┐
│ Status Bar / Header                          │
├──────────────────────────────────────────────┤
│                                              │
│               Content Area                   │
│                                              │
│                                              │
├──────────────────────────────────────────────┤
│   Home   Search   Create   Inbox   Profile   │
└──────────────────────────────────────────────┘
```

**Best for:** Mobile-first applications, PWAs, consumer apps optimized for phone usage.
**Navigation capacity:** 3-5 top-level items (maximum — do not exceed 5).
**Characteristics:** Thumb-friendly. Persistent access to core functions. Active state is visually prominent.
**Used by:** Instagram, Spotify, banking apps, ride-sharing apps.

**Implementation notes:**
- Tab bar height: 56-72px including safe area.
- Icons: 24px with a text label below (never icon-only for primary nav).
- Active state: filled icon + brand color or bold weight label.
- Hide the tab bar on full-screen immersive content (video players, editors).

### Split Panel / Master-Detail (Email / File Manager Style)

```
┌────────┬───────────┬─────────────────────────┐
│        │           │                         │
│ Side-  │   List    │    Detail / Preview     │
│  bar   │  (master) │                         │
│        │           │                         │
│        │           │                         │
└────────┴───────────┴─────────────────────────┘
```

**Best for:** Email clients, file managers, CRM record views, support ticket systems, messaging apps, documentation browsers.
**Characteristics:** Three-panel layout with persistent navigation, a scrollable item list, and a detail view that updates based on selection.
**Used by:** Gmail, Outlook, Apple Mail, Slack, Zendesk, VS Code (file tree + editor).

**Implementation notes:**
- List panel: 280-360px wide. Scrollable independently.
- Detail panel: fills remaining width. Scrollable independently.
- Resizable: allow drag-to-resize between panels. Store preference.
- Mobile: collapse to list-only view with tap-to-open detail as a pushed screen.
- Selection: highlight the active item in the list. Support arrow key navigation.

### Canvas + Toolbars (Creative / Editor)

```
┌──────────────────────────────────────────────┐
│ Toolbar (tools, undo/redo, zoom, settings)    │
├──────┬───────────────────────────────┬───────┤
│      │                               │       │
│ Left │        Canvas / Editor        │ Right │
│ Panel│         (main workspace)      │ Panel │
│      │                               │       │
│      │                               │       │
└──────┴───────────────────────────────┴───────┘
```

**Best for:** Design tools, code editors, diagram editors, video editors, map-based applications, page builders.
**Characteristics:** The canvas is the primary workspace. Toolbars and panels are secondary chrome that should minimize visual weight.
**Used by:** Figma, VS Code, Adobe apps, Google Maps, Miro.

**Implementation notes:**
- Canvas: fills all available space. Supports zoom and pan (scroll + drag or pinch).
- Side panels: collapsible. Typical widths 240-320px.
- Top toolbar: 40-48px. Compact controls, grouped by function.
- All chrome should be as low-contrast as possible — the canvas content is the focus.

## 2. Page Composition Archetypes

Within the application shell, individual pages follow common composition patterns. Choose the right archetype for the content type.

### Dashboard Page

**Purpose:** Overview, monitoring, key metrics at a glance.
**Structure:**
```
┌─────────────────────────────────────────────┐
│ Page Header: Title  |  Date Picker  | Export │
├─────────┬──────────┬──────────┬─────────────┤
│ KPI Card│ KPI Card │ KPI Card │  KPI Card   │
├─────────┴──────────┴──────────┴─────────────┤
│ Primary Chart (full width or 2/3)  │ Table  │
│                                    │ or List│
├─────────────────────────────┬───────────────┤
│ Secondary Chart             │ Activity Feed │
└─────────────────────────────┴───────────────┘
```

**Design rules:**
- KPI cards above the fold. Lead with the most important metric.
- Each KPI: current value, comparison (vs. previous period, vs. target), and a trend indicator (arrow or sparkline).
- Chart selection: bar for comparison, line for trend, pie only if showing parts-of-whole with ≤ 5 slices.
- Filters (date range, segment) affect all charts on the page — show applied filters prominently.
- Drill-down: clicking a chart element or KPI navigates to a detail view.

### List / Table Page

**Purpose:** Browse, search, filter, and manage a collection of records.
**Structure:**
```
┌─────────────────────────────────────────────┐
│ Page Header: Title  |  Search  |  + Create  │
├─────────────────────────────────────────────┤
│ Filter Bar: Status ▾  | Role ▾  | Clear All │
├─────────────────────────────────────────────┤
│ ☐ │ Name          │ Status  │ Date   │ ⋮   │
│ ☐ │ Record Alpha  │ Active  │ Mar 12 │ ⋮   │
│ ☐ │ Record Beta   │ Pending │ Mar 10 │ ⋮   │
│ ...                                         │
├─────────────────────────────────────────────┤
│ Showing 1-25 of 142  |  ◄ 1 2 3 ... 6 ►    │
└─────────────────────────────────────────────┘
```

**Design rules:**
- Primary action ("+ Create") is the most visually prominent element in the header.
- Search should be instantly accessible (not hidden behind a toggle).
- Active filters displayed as removable chips/tags above the table.
- Sortable columns: click header to toggle asc/desc. Show sort indicator.
- Row actions: overflow menu (⋮) for per-row actions, or inline icon buttons for 1-2 frequent actions.
- Bulk actions: checkbox column. When items are selected, a bulk action bar replaces or overlays the filter bar.
- Empty state: when no records exist or all are filtered out, show guidance and a CTA.
- Pagination: show total count, page size selector, and navigation. Or use infinite scroll for feeds.

### Detail / Record Page

**Purpose:** View and edit a single entity (user, project, order, etc.).
**Structure:**
```
┌─────────────────────────────────────────────┐
│ Breadcrumb: Projects > Alpha                │
│ Page Header: Entity Name  | Status | Edit ✎ │
├─────────────────────┬───────────────────────┤
│                     │                       │
│ Primary Content     │ Sidebar / Meta        │
│ (tabs or sections)  │ (properties, actions, │
│                     │  related items, notes)│
│                     │                       │
└─────────────────────┴───────────────────────┘
```

**Design rules:**
- Identity bar: entity name, key status, and primary actions are always visible at the top.
- Content area: use tabs for distinct content categories (Overview / Activity / Settings) or a single scrollable page with section headings for shorter content.
- Sidebar meta: structured properties (owner, created date, tags, linked records). Edit inline or via a modal.
- Activity / Timeline: show chronological history of changes, comments, and events.
- Related records: link to associated entities with quick-add capability.

### Settings / Configuration Page

**Purpose:** Manage application or entity preferences.
**Structure:**
```
┌──────────┬──────────────────────────────────┐
│          │ Section Title                     │
│ Settings │ Description of what this controls │
│  Nav     │                                   │
│          │ [Form fields]                     │
│ General  │                                   │
│ Profile  │ ───────────────────────────       │
│ Billing  │                                   │
│ Team     │ Another Section                   │
│ API      │ [More form fields]                │
│          │                                   │
│          │               [Save Changes]      │
└──────────┴──────────────────────────────────┘
```

**Design rules:**
- Left sidebar navigation for settings categories. Highlight the active section.
- Each section: heading, descriptive subtext explaining what the setting controls, then form fields.
- Destructive settings (delete account, revoke access): visually separated at the bottom with red-zone styling.
- Save behavior: either per-section save buttons or auto-save with status indicator.
- Mobile: settings nav becomes a top-level list; tapping a category pushes to the settings detail screen.

### Creation / Editing Flow (Wizard / Multi-Step Form)

**Purpose:** Guide the user through a multi-step creation or editing process.
**Structure:**
```
┌─────────────────────────────────────────────┐
│ Step Indicator: ● Step 1 ─ ○ Step 2 ─ ○ 3  │
├─────────────────────────────────────────────┤
│                                             │
│ Step Title                                  │
│ Instructions / context                      │
│                                             │
│ [Form fields for this step]                 │
│                                             │
│                                             │
├─────────────────────────────────────────────┤
│ [← Back]                    [Continue →]    │
└─────────────────────────────────────────────┘
```

**Design rules:**
- Progress indicator at the top: numbered steps with labels showing completion status.
- One concern per step. Do not dump all fields on one page.
- Validate each step before allowing "Continue."
- "Back" button always available (except step 1). Preserve entered data when navigating back.
- Final step: show a summary review of all entered data before the primary submit action.
- Success: redirect to the created entity's detail page, or show a success confirmation with next-step guidance.
- Max-width the form content to 640-720px for readability, centered in the content area.

### Feed / Activity Stream Page

**Purpose:** Chronological stream of events, posts, or updates.
**Structure:**
```
┌─────────────────────────────────────────────┐
│ [Compose / Create new post]                 │
├─────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────┐ │
│ │ Avatar  User Name  ·  3 hours ago       │ │
│ │ Content text / media / attachment        │ │
│ │ [Actions: Like · Comment · Share]        │ │
│ └─────────────────────────────────────────┘ │
│ ┌─────────────────────────────────────────┐ │
│ │ Avatar  User Name  ·  5 hours ago       │ │
│ │ Content text / media / attachment        │ │
│ │ [Actions: Like · Comment · Share]        │ │
│ └─────────────────────────────────────────┘ │
│              [Load more]                    │
└─────────────────────────────────────────────┘
```

**Design rules:**
- Compose/create is at the top of the feed — this is the primary action.
- Max-width the feed column (600-680px) for readability. Center with optional side columns for trending/suggestions.
- Infinite scroll or paginated "Load more" — not traditional page numbers.
- Timestamps: relative ("3 hours ago") for recent items, absolute ("Mar 12, 2025") for older items.
- Real-time: show a "New posts available" banner when new content arrives, rather than auto-inserting (which shifts the reading position).

### Kanban / Board Page

**Purpose:** Visual workflow management with items in stages/columns.
**Structure:**
```
┌─────────────────────────────────────────────┐
│ Header: Board Name  |  Filters  | + Add     │
├──────────┬──────────┬──────────┬────────────┤
│ To Do    │ In Prog  │ Review   │ Done       │
│ (5)      │ (3)      │ (2)      │ (12)       │
│┌────────┐│┌────────┐│┌────────┐│┌──────────┐│
││ Card 1 │││ Card 4 │││ Card 7 │││ Card 9   ││
│└────────┘│└────────┘│└────────┘│└──────────┘│
│┌────────┐│┌────────┐│┌────────┐│            │
││ Card 2 │││ Card 5 │││ Card 8 ││            │
│└────────┘│└────────┘│└────────┘│            │
│+ Add     │+ Add     │          │            │
└──────────┴──────────┴──────────┴────────────┘
```

**Design rules:**
- Columns represent stages of a workflow. Each column has a header with the stage name and item count.
- Drag and drop: cards are draggable between columns. Show a drop zone indicator.
- Horizontal scroll: the board scrolls horizontally when columns exceed the viewport. Columns should have a fixed width (280-320px).
- Card design: show the most critical info (title, assignee, priority, due date) in a compact format. More detail available on click (opens a modal or detail panel).
- Quick-add: a persistent "+" button at the bottom of each column for rapid card creation.
- Column customization: allow users to add, rename, reorder, and hide columns.
- WIP limits: optionally show column limits (e.g., "In Progress: 3 / 5") and visually indicate when a column exceeds its limit.

## 3. Responsive Composition Rules

### Layout Adaptation by Breakpoint

| Page Type | Desktop (xl+) | Tablet (md-lg) | Mobile (<md) |
|-----------|---------------|-----------------|--------------|
| Dashboard | 3-4 column KPI grid, multi-chart layout | 2 column KPI grid, stacked charts | Single column, stacked everything |
| List/Table | Full table with all columns | Table with fewer columns or horizontal scroll | Card-based list replacing the table |
| Detail | Content + sidebar side-by-side | Content full width, sidebar collapsed or below | Single column, all sections stacked |
| Settings | Left nav + content side-by-side | Left nav collapses to top tabs | Settings list with push navigation |
| Kanban | Horizontal scrolling board | Reduced column widths, fewer visible | Single column view or horizontal swipe |
| Form/Wizard | Centered form, max 640px | Same, slightly wider margins | Full-width with padding |

### Table-to-Card Transformation

When a data table must render on mobile, transform each table row into a card:
- Card title: the value from the primary/name column
- Card metadata: key columns shown as label-value pairs
- Card actions: row action menu preserved as a card-level overflow button
- Sorting and filtering controls remain in a toolbar above the card list

### Navigation Adaptation

| Shell Type | Desktop | Tablet | Mobile |
|-----------|---------|--------|--------|
| Sidebar + Top bar | Full sidebar + top bar | Collapsed (icon-only) sidebar + top bar | Hidden sidebar as overlay drawer + top bar with hamburger |
| Top bar only | Full nav links in top bar | Fewer links + "More" overflow | Hamburger menu → full-screen nav |
| Bottom tab bar | N/A (desktop uses sidebar or top bar) | N/A | 3-5 tab items with icons + labels |

## 4. Content Area Sizing Guidelines

Not all content should fill the available width. Constrain content width by type:

| Content Type | Recommended Max Width | Reason |
|-------------|----------------------|--------|
| Prose / long-form text | 680-720px | Optimal reading line length (55-75 characters) |
| Forms (single column) | 560-640px | Prevents input fields from becoming absurdly wide |
| Forms (two column) | 800-960px | Paired fields with adequate spacing |
| Data tables | Full container width | Tables need horizontal space for columns |
| Dashboard grids | Full container width | KPI cards and charts need space to breathe |
| Card grids | Full container with min/max items | Use CSS Grid `auto-fill` with `minmax(280px, 1fr)` |
| Settings pages | 720-800px content area | Prevent wide settings forms from feeling sparse |
| Detail pages (content area) | 800-960px | Balance between readability and detail density |

Center-align constrained content within the available area using `margin: 0 auto` or flexbox/grid centering.

## 5. Whitespace and Density Scales

Different density levels serve different users and contexts. Define density as a system-level token that adjusts spacing globally.

**Compact density** (power users, data-heavy views):
- Table row height: 32-36px
- Card padding: 12px
- Form field height: 32px
- Button height: 28px
- Section gaps: 16-24px

**Default density** (general use, balanced):
- Table row height: 40-44px
- Card padding: 16px
- Form field height: 36px
- Button height: 36px
- Section gaps: 24-32px

**Comfortable density** (new users, simple content, consumer):
- Table row height: 48-52px
- Card padding: 20-24px
- Form field height: 40px
- Button height: 40px
- Section gaps: 32-48px

Allow users to select their preferred density via a settings toggle or view-specific density control. Persist the choice.
