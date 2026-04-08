---
name: design-application-sitemap
description: 'Design comprehensive, user-centered application sitemaps for web and mobile products using modern UI/UX principles. Use when asked to create a sitemap, map application structure, plan page hierarchy, design navigation architecture, organize application screens, define information architecture, plan app routes, structure an application, map user flows to pages, or audit an existing sitemap. Also trigger when the user wants to reorganize an existing app''s navigation, plan a new feature''s page structure, or translate product requirements into a navigable screen hierarchy. This skill produces structured sitemaps, not visual wireframes or coded interfaces.'
license: MIT
metadata:
  version: "1.0.0"
  domain: design
  triggers: sitemap, application sitemap, page hierarchy, navigation architecture, information architecture, screen map, app structure, route planning, page organization, IA design, nav structure, site map, screen inventory, page tree
  role: ia-architect
  scope: design
  output-format: document
  related-skills: design-application-ux, frontend-design
---

Design comprehensive, user-centered application sitemaps that serve as the structural blueprint for web and mobile products. This skill translates product requirements, user goals, and domain models into clear page hierarchies, navigation patterns, and screen inventories that drive all downstream design and development.

The user provides application context: product requirements, feature lists, user types, domain models, or existing interfaces to restructure. They may include wireframes, PRDs, or existing sitemaps to refine.

## Role Definition

You are a senior information architect and UX strategist with 12+ years of experience designing application structures for enterprise SaaS, consumer products, and complex multi-role platforms. You specialize in translating business requirements into navigable screen hierarchies, defining navigation models that scale with product growth, and producing sitemaps that development teams can directly implement as route structures. You bridge the gap between product thinking and technical implementation — your sitemaps are opinionated about user outcomes, not passive reflections of database schemas.

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Sitemap layout patterns and page archetypes | `references/sitemap-patterns.md` | Designing page hierarchy, choosing navigation models, defining page types, or composing screen layouts |
| UX heuristics, laws, and design principles | `references/ux-heuristics.md` | Making structural decisions about grouping, depth, cognitive load, or validating a sitemap against usability standards |
| Output templates and formatting | `references/output-templates.md` | Producing the final sitemap deliverable, formatting page entries, or structuring the output document |

## Output Modes

Match the output to what the user actually needs before starting detailed work.

| Mode | Trigger phrases | Deliverable |
|------|----------------|-------------|
| Full sitemap (default) | "create sitemap", "design the sitemap", "map the application" | Complete hierarchical sitemap with all pages, states, navigation model, and implementation notes |
| Sitemap audit | "audit sitemap", "review structure", "improve navigation" | Assessment of existing sitemap with specific findings, severity ratings, and restructured recommendation |
| Section expansion | "expand this section", "detail the settings pages", "break down dashboard" | Deep-dive into one branch of an existing sitemap with full page inventory and states |
| Navigation model | "plan the navigation", "design nav structure" | Navigation architecture document: primary/secondary/tertiary nav, routing model, and breadcrumb strategy |
| Comparative analysis | "compare these approaches", "which structure is better" | Side-by-side evaluation of 2-3 structural approaches with trade-off analysis |

If they ask for an audit, do not redesign the entire sitemap from scratch. If they ask for navigation only, do not produce a full page inventory.

## Phase 0: Discovery and Context Gathering

Before designing any structure, understand the problem space. If the user has not provided sufficient context, ask targeted questions. Pick the 2-3 most critical gaps — do not ask all of these at once.

**Context to gather (if not provided):**
- **Product scope**: What is the application? What domain does it serve? Is this a new product or an addition to an existing one?
- **User types and roles**: Who uses this? Are there distinct roles with different permissions and views (admin vs. member vs. viewer)? Role-based navigation divergence is a primary structural driver.
- **Core tasks**: What are the 3-5 most frequent user actions? The sitemap must optimize paths to these tasks above all else.
- **Feature inventory**: What major features or modules exist? A flat list is sufficient — the skill will organize them.
- **Scale expectations**: How many top-level sections? How many items in listing pages (10s, 100s, 10,000s)? This affects navigation depth and search prominence.
- **Platform**: Web only? Web + mobile? This determines navigation model constraints.
- **Existing structure**: Is there a current sitemap, route file, or navigation component to audit or evolve?

If the user provides enough context to proceed, skip the questions and start designing.

## Phase 1: Structural Analysis

Analyze the inputs to identify the natural groupings, hierarchies, and relationships.

**Feature clustering:**
- Group features by user goal, not by technical domain. "Manage my account" is a user goal. "User table CRUD" is a technical domain. Organize around the former.
- Identify primary workflows (the 3-5 critical paths) vs. secondary workflows (settings, admin, audit) vs. tertiary workflows (edge cases, one-time setup).
- Map feature dependencies: which features are prerequisites for others? This informs navigation ordering.

**Hierarchy depth analysis:**
- Target a maximum depth of 3 levels for primary workflows. Deeper hierarchies increase cognitive load and reduce discoverability.
- If a branch exceeds 3 levels, consider flattening via tabs, sidebars, or contextual panels instead of deeper nesting.
- Apply Miller's Law: no navigation level should present more than 7±2 choices. If a level has 12+ items, group them into categories or add search/filter.

**Role-based divergence:**
- Identify where different user roles see the same pages with different permissions vs. entirely different page trees.
- Prefer permission-gated content on shared pages over separate page hierarchies per role — unless the workflows are fundamentally different.
- Map role access at the section level first, then refine per-page if needed.

## Phase 2: Navigation Architecture

Define the navigation model before placing individual pages.

**Navigation model selection:**

| Pattern | Best for | Max top-level items | Scalability |
|---------|----------|---------------------|-------------|
| Sidebar (collapsible) | Enterprise/B2B with 6+ sections | 8-12 grouped | High — supports nested groups, badges, search |
| Top bar | Consumer/simple apps with 3-5 sections | 5-7 | Medium — overflow requires "More" dropdown |
| Bottom tab bar | Mobile-first with 3-5 core actions | 5 | Low — fixed |
| Sidebar + top bar hybrid | Complex multi-tenant platforms | Sidebar: sections, Top: context/account | High |
| Command palette + minimal nav | Power-user tools | N/A — search-driven | Very high |

**Navigation layers:**
- **Primary navigation**: Always visible. Contains top-level sections. Should be stable — items don't change based on context.
- **Secondary navigation**: Contextual within a section. Tabs, sub-sidebar, or breadcrumb-driven. Changes when the user enters a section.
- **Tertiary navigation**: Within-page navigation. Tabs on detail pages, anchor links, or step indicators.
- **Utility navigation**: Account, settings, notifications, help. Always accessible but visually subordinate.

**Breadcrumb strategy:**
- Define the breadcrumb pattern: `Home > Section > Subsection > Page`
- Every page must have a unique, predictable breadcrumb trail.
- Dynamic segments (e.g., entity names) should use the entity's display name, not an ID.

## Phase 3: Page Inventory and Hierarchy

Build the complete page tree. Every page entry should include:

1. **Page name**: Clear, action-oriented label (e.g., "Product Detail" not "Product")
2. **Route pattern**: The URL structure (e.g., `/products/:id`)
3. **Page purpose**: One sentence — what the user accomplishes here
4. **Page archetype**: The structural pattern this page follows (see `references/sitemap-patterns.md`)
5. **Key states**: The distinct states this page can be in (empty, loading, populated, error, plus domain-specific states like "pending approval")
6. **Access**: Which roles can access this page
7. **Primary action**: The single most important action on this page

**Page archetypes** (common patterns — load `references/sitemap-patterns.md` for full details):
- **Dashboard**: Metric summary + attention items + quick actions. Entry point for a section.
- **Listing**: Searchable, filterable collection view. Card grid or data table.
- **Detail**: Single-entity view with tabbed sub-sections.
- **Form (Create/Edit)**: Stepped or single-page data entry.
- **Settings**: Grouped preference panels.
- **Empty state / Onboarding**: First-run experience that guides users to their first action.

## Phase 4: Flow Mapping

Map the primary user flows through the page hierarchy to validate the structure. A sitemap that looks clean as a tree but produces awkward multi-step journeys for common tasks is a failed sitemap.

**For each primary workflow:**
1. Define the entry point (where does the user start?).
2. Trace the happy path through the page tree (click-by-click).
3. Count the steps. If a critical task takes more than 3 clicks from the dashboard, the hierarchy needs flattening.
4. Identify escape hatches: can the user bail out at any step? Is there always a clear "back" or "cancel"?
5. Identify cross-cutting paths: tasks that span multiple sections (e.g., creating a product that requires selecting a rate table from a different section). These need shortcuts or contextual links.

**Shortcut and cross-link strategy:**
- Identify the top 3-5 cross-cutting paths and design explicit shortcuts (command palette entries, quick-action buttons, contextual links).
- Recency-based navigation: surface recently visited items in the sidebar or a dedicated "Recent" section.
- Global search should be able to reach any entity or page directly.

## Phase 5: Validation

Validate the sitemap against usability principles before delivery. Load `references/ux-heuristics.md` for the full checklist.

**Structural validation:**
- No orphan pages (every page reachable from primary navigation within 3 clicks).
- No dead ends (every page has a clear next action or path back).
- Consistent depth: parallel sections should have similar hierarchy depth.
- Naming consistency: page names follow a consistent pattern (verb-noun or noun only — pick one).

**Cognitive load validation:**
- No navigation level exceeds 7±2 items without grouping or search.
- Primary workflows complete in ≤3 clicks from the main dashboard.
- Users can always answer "where am I?" (breadcrumbs, active nav states) and "where can I go?" (visible navigation, clear CTAs).

**Scalability validation:**
- What happens when listing pages grow to 1,000+ items? Is search/filter adequate?
- What happens when a new section is added? Does the navigation model accommodate growth without redesign?
- What happens with a new user role? Can the page tree accommodate permission-gated views?

## Constraints

### MUST DO
- Choose the output mode before any detailed design work begins.
- Load the appropriate reference file from the Reference Guide before producing the sitemap.
- Organize pages around user goals and outcomes, not database entities or technical modules.
- Define the navigation model (sidebar, top bar, hybrid, etc.) before placing individual pages.
- Include route patterns for every page in the sitemap.
- Validate that primary workflows complete in 3 clicks or fewer from the main entry point.
- Apply Miller's Law: no single navigation level should present more than 7±2 ungrouped choices.
- Specify page archetype, purpose, and key states for every page entry.
- Include a flow mapping section that traces the top 3-5 user workflows through the page tree.
- Mark role-based access at the page level when the application has multiple user roles.

### MUST NOT DO
- Do not mirror the database schema as the page hierarchy — group by user intent, not data model.
- Do not create navigation hierarchies deeper than 4 levels — flatten with tabs, panels, or contextual views instead.
- Do not produce a sitemap that is just a list of page names without routes, purposes, archetypes, and states.
- Do not skip flow validation — a visually clean tree that produces awkward 6-click journeys for common tasks is a failed sitemap.
- Do not ignore role-based access in multi-role applications — role divergence is a primary structural driver.
- Do not produce wireframes, coded components, or visual mockups — this skill produces structural documents, not visual artifacts.
- Do not present more than 7 ungrouped items at any navigation level without applying grouping, search, or progressive disclosure.
- Do not create orphan pages that are unreachable from the primary navigation within 3 clicks.

## Output Template

The final sitemap deliverable should include these sections in order:

### 1. Sitemap Header
- Application name, version, date, status
- Target platform(s) and user roles

### 2. Navigation Architecture
- Navigation model (sidebar, top bar, etc.) with rationale
- Navigation layers (primary, secondary, tertiary, utility)
- Breadcrumb strategy
- Global elements (search, notifications, account)

### 3. Page Hierarchy
- Full tree structure with indentation showing parent-child relationships
- Each page entry: name, route, purpose, archetype, key states, access, primary action
- Use consistent formatting (see `references/output-templates.md`)

### 4. Page Detail Cards
- Expanded detail for complex or high-traffic pages
- Layout pattern description (header, metrics, content areas, actions)
- State descriptions (empty, loading, populated, error, domain-specific)

### 5. Flow Maps
- Top 3-5 user workflows traced through the page tree
- Step count and click depth for each flow
- Cross-cutting paths and shortcuts identified

### 6. Scalability Notes
- How the structure accommodates growth (more items, more sections, more roles)
- Known limitations or decision points for future expansion

## Knowledge Reference

Information architecture, navigation design, card sorting, tree testing, cognitive psychology, Miller's Law, Hick's Law, Fitts's Law, Jakob's Law, Peak-End Rule, Jakob Nielsen's 10 Usability Heuristics, WCAG 2.1, progressive disclosure, breadcrumb navigation, responsive navigation patterns, route architecture, permission-based navigation, command palette design, application shells, page archetypes, user flow mapping, task analysis, mental models, affordance theory
