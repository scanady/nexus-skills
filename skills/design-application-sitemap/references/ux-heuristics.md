# UX Heuristics & Design Principles Reference

Usability heuristics, cognitive psychology laws, and design principles for validating application sitemaps. This reference is loaded when making structural decisions about grouping, depth, cognitive load, or validating a sitemap against usability standards.

## Table of Contents

1. [Nielsen's 10 Usability Heuristics (Applied to Sitemaps)](#nielsens-10-usability-heuristics)
2. [Cognitive Psychology Laws](#cognitive-psychology-laws)
3. [Information Architecture Principles](#information-architecture-principles)
4. [Sitemap Validation Checklist](#sitemap-validation-checklist)

## Nielsen's 10 Usability Heuristics

Applied specifically to sitemap and navigation design:

### 1. Visibility of System Status

**Sitemap implication:** Every page must make the user's current location clear.
- Breadcrumbs on every page (except the root dashboard)
- Active state on the current navigation item at every level (primary, secondary, tertiary)
- Page titles that match navigation labels exactly — no surprises

### 2. Match Between System and Real World

**Sitemap implication:** Navigation labels and page names must use the user's vocabulary, not the system's internal terminology.
- Use domain language the target users already know (run a card sort if uncertain)
- Group items the way users mentally group them, not the way the database organizes them
- Name pages with action-oriented labels when possible: "Create Product" not "Product Form"

### 3. User Control and Freedom

**Sitemap implication:** Users must always have a clear exit and undo path.
- Every page has a path back (breadcrumb, back button, or cancel action)
- Destructive actions (delete, archive) are reversible or require confirmation
- Wizard/stepped flows always allow backward navigation and a "cancel" escape hatch
- No page should be a dead end — always provide a next action

### 4. Consistency and Standards

**Sitemap implication:** Parallel sections must follow the same structural patterns.
- If "Products" has a listing → detail → edit flow, then "Templates" should follow the same pattern
- Navigation position, label style, and depth should be consistent across sections
- Page archetypes should be used consistently — dashboards look like dashboards everywhere

### 5. Error Prevention

**Sitemap implication:** The navigation structure should prevent users from getting lost.
- Clear, descriptive navigation labels that distinguish similar sections
- Confirmation steps before irreversible navigation (leaving unsaved forms)
- No ambiguous paths where two navigation items lead to overlapping content

### 6. Recognition Rather Than Recall

**Sitemap implication:** Users should recognize where to go, not remember paths.
- Navigation items should have descriptive labels (not icons-only without tooltips)
- Recent items and frequently visited pages should be easily accessible
- Global search provides a fallback when navigation scanning fails
- Breadcrumbs show the full path so users don't have to remember how they got here

### 7. Flexibility and Efficiency of Use

**Sitemap implication:** Provide shortcuts for power users without burdening novices.
- Command palette (Cmd+K) for keyboard-driven navigation
- Quick actions on dashboard pages for common tasks
- Favorites or pinned items in the sidebar
- Keyboard shortcuts for frequent navigation paths
- Deep links: every meaningful state should have a shareable URL

### 8. Aesthetic and Minimalist Design

**Sitemap implication:** Every page and navigation item must earn its place.
- Remove pages that serve no distinct user goal
- Combine pages that users always visit together
- Hide rarely-used sections behind "More" or advanced settings
- Avoid "junk drawer" sections that accumulate miscellaneous items

### 9. Help Users Recognize, Diagnose, and Recover from Errors

**Sitemap implication:** Error states and 404 pages are part of the sitemap.
- Design a custom 404 page with navigation suggestions
- Design error states for every listing and detail page
- Provide contextual help links or documentation pointers near complex features

### 10. Help and Documentation

**Sitemap implication:** Help and documentation access should be part of the navigation architecture.
- Help accessible from every page (contextual help icon or persistent help button)
- Documentation and onboarding flows mapped as first-class pages
- Tooltip/tour system for complex features

## Cognitive Psychology Laws

### Miller's Law

> The average person can hold 7 ± 2 items in working memory.

**Application to sitemaps:**
- No single navigation level should display more than 7 ungrouped items
- If a sidebar has 12 sections, group them into 3-4 categories with headers
- Listing pages with many columns should default to showing 5-7 and allow column customization
- Wizard steps should be 3-7; more than 7 steps requires grouping into phases

### Hick's Law

> The time it takes to make a decision increases with the number and complexity of choices.

**Application to sitemaps:**
- Reduce choices at each navigation level by grouping and progressive disclosure
- Primary actions should be visually distinct from secondary and tertiary actions
- Don't present all available actions at once — use contextual menus and overflow patterns
- Settings pages with 20+ options should be categorized, not presented as a flat list

### Fitts's Law

> The time to acquire a target is a function of the distance to and size of the target.

**Application to sitemaps:**
- Place frequently-used navigation items in easily accessible positions (top of sidebar, leftmost top bar items)
- Primary CTAs should be prominently placed and sized (not small icons in corners)
- Mobile: place critical actions within thumb reach (bottom of screen, bottom tab bar)
- Avoid placing destructive actions adjacent to primary actions

### Jakob's Law

> Users spend most of their time on other sites. They prefer your site to work the same way as all the other sites they already know.

**Application to sitemaps:**
- Follow platform conventions: sidebar nav for enterprise, tab bar for mobile
- Place settings, account, and search where users expect them (top-right, bottom of sidebar)
- Use standard page patterns: listing → detail → edit flows are universally understood
- Don't invent novel navigation paradigms without strong justification

### Peak-End Rule

> People judge an experience largely based on how they felt at its peak and at its end.

**Application to sitemaps:**
- Design strong entry points (first load experience, dashboard) — this is the "peak"
- Design satisfying completion states (success messages, confirmation pages) — this is the "end"
- Onboarding flow and first-time empty states set the tone for the entire experience
- The "most painful" page in the app disproportionately affects user perception — identify and fix it

### Von Restorff Effect (Isolation Effect)

> When multiple similar items are present, the one that differs from the rest is most likely to be remembered.

**Application to sitemaps:**
- Use visual differentiation for primary CTAs (color, size, position)
- Highlight the "recommended" or "most popular" path when presenting choices
- Attention/alert sections should visually break from the surrounding content pattern
- One primary action per page — if everything is emphasized, nothing is

### Tesler's Law (Law of Conservation of Complexity)

> Every application has an inherent amount of complexity that cannot be removed. It can only be moved — from the user to the system.

**Application to sitemaps:**
- If a workflow is inherently complex, don't try to compress it into fewer pages — instead, guide the user through the complexity with clear steps
- Smart defaults reduce the perceived complexity of forms without hiding options
- Complex features can have "simple" and "advanced" modes, but both must be discoverable

### Doherty Threshold

> Productivity soars when the system response time is under 400ms.

**Application to sitemaps:**
- Client-side navigation (SPA routing) for within-section transitions
- Skeleton loading states for pages that require data fetching
- Optimistic UI updates for actions that are very likely to succeed
- Prefetch adjacent pages on hover or the next step in a wizard

## Information Architecture Principles

### LATCH Framework (Richard Saul Wurman)

All information can be organized by one of five schemes:
- **Location**: Geographic or spatial (store locator, map-based views)
- **Alphabet**: A-Z ordering (glossaries, directories)
- **Time**: Chronological (feeds, timelines, audit logs)
- **Category**: Grouped by similarity (most common for app navigation)
- **Hierarchy**: Ranked by importance or magnitude (leaderboards, priority queues)

Choose the organizing principle that matches the user's mental model for each section. Don't default to alphabetical when categorical or hierarchical would serve better.

### Progressive Disclosure

Show only what is needed at each step. Reveal detail on demand.

**In sitemaps:**
- Top-level navigation shows sections, not subsections
- Subsections reveal when a section is entered or expanded
- Advanced settings hidden behind toggles
- Filters default to "popular" subset with "Show all filters" expansion
- Page detail builds progressively: summary first, then expandable sections

### Object-Oriented IA

Structure the information architecture around the key objects (entities) users interact with, then define the actions available on each object.

**Process:**
1. Identify the core objects (Product, Template, Rate Table, Filing)
2. For each object, define: listing view, detail view, create/edit form
3. Map relationships between objects (a Product has Riders, a Filing references a Product)
4. Cross-link related objects in the detail views

This approach ensures consistency — every object follows the same navigation pattern.

## Sitemap Validation Checklist

Use this checklist to validate a completed sitemap before delivery.

### Structure
- [ ] Maximum navigation depth is 3-4 levels
- [ ] No navigation level has more than 7 ungrouped items
- [ ] Parallel sections follow consistent depth and patterns
- [ ] Every page has a unique, predictable breadcrumb trail
- [ ] No orphan pages (unreachable without direct URL)
- [ ] No dead-end pages (every page offers a next action or path back)

### Navigation
- [ ] Navigation model matches the app type and section count
- [ ] Primary, secondary, tertiary, and utility navigation layers are clearly defined
- [ ] Active states are designed for every navigation level
- [ ] Mobile navigation adaptation is defined
- [ ] Global search can reach any entity or page

### User Flows
- [ ] Top 3-5 workflows complete in ≤3 clicks from the main entry point
- [ ] Cross-cutting paths have explicit shortcuts
- [ ] Every wizard/stepped flow allows backward navigation and cancel
- [ ] Destructive actions have confirmation or undo

### Content
- [ ] Every page has a defined purpose (one sentence)
- [ ] Page names use user vocabulary, not system terminology
- [ ] Every listing page has a designed empty state
- [ ] Error states and 404 handling are accounted for

### Scalability
- [ ] Listing pages can accommodate 1,000+ items via search/filter/pagination
- [ ] Navigation model can accommodate 2-3 new sections without redesign
- [ ] Role-based access is defined at the page level
- [ ] The sitemap notes future expansion points

### Accessibility
- [ ] All navigation is keyboard-accessible
- [ ] Screen reader landmarks are implied (nav, main, aside)
- [ ] Focus management is defined for navigation transitions
- [ ] Color is not the sole means of conveying navigation state
