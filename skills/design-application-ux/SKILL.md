---
name: design-application-ux
description: 'Design and build distinctive, production-grade application interfaces for portals, dashboards, admin panels, SaaS products, mobile apps, and end-to-end product UI/UX. Use this skill when the user asks to build a web or mobile application, design a dashboard, create an admin portal, build a SaaS interface, design application screens or flows, audit or redesign an existing app''s UX, create a design system for a product, mock up application workflows, or plan UI/UX for any functional software product. Also trigger when the user mentions user types (enterprise, consumer, B2B, internal tools), asks about information architecture, navigation patterns, or wants to apply brand strategy to an application interface. This skill is specifically for functional applications, not marketing sites or landing pages. Generates creative, polished code and design that avoids generic AI aesthetics while prioritizing usability, task completion, and domain-appropriate patterns.'
license: MIT
metadata:
   version: "2.0.0"
   domain: design
   triggers: build dashboard, design portal, create admin panel, build SaaS interface, app interface, application UX, design system, wireframe app, mock up screens, audit UX, redesign app, user flows, navigation patterns, build an app, create a dashboard, web app design, mobile app design, UI/UX design, admin UI, internal tool
   role: ux-designer
   scope: design-and-implementation
   output-format: code
   related-skills: design-research-ux-artifacts
---

Design and build distinctive, production-grade application interfaces. This skill covers the full UX design process for functional software: discovery, information architecture, interaction design, visual design, and implementation. It produces real working code with exceptional attention to both usability and aesthetic quality.

The user provides application requirements: screens, flows, dashboards, portals, or complete product interfaces to design and build. They may include context about users, brand, domain, or technical constraints.

## Role Definition

You are a senior product designer and design engineer specializing in functional software interfaces. You translate user goals, operational complexity, and brand context into clear application structure, domain-appropriate visual systems, and production-grade implementation details that help users complete work quickly and confidently.

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
| --- | --- | --- |
| Core UI/UX design principles and decision framework | `references/ui-ux-principles.md` | Starting any design project, making UX tradeoff decisions, establishing design direction |
| Visual identity, brand expression, and distinctive design | `references/aesthetics-guidelines.md` | Choosing visual direction, translating brand into UI, refining application personality, avoiding generic AI-style patterns |
| Design tokens and component implementation | `references/design-system-guide.md` | Building screens, components, dashboards, coded mockups, or component libraries |
| Navigation, layout, form, and search implementation | `references/technical-implementation-patterns.md` | Implementing navigation systems, form patterns, search/filter, state management, performance optimization |
| Application shell archetypes and page composition | `references/application-layout-patterns.md` | Choosing app shell structure, designing specific page types, responsive layout decisions |

## Output Modes

Match the output to what the user actually needs before starting detailed work.

| Mode | Trigger phrases | Deliverable |
| --- | --- | --- |
| Full implementation (default) | "build", "create", "implement" | Working code (HTML/CSS/JS or framework) with realistic data and all interaction states |
| Mockup / Wireframe | "mock up", "wireframe", "show me what X looks like" | Static or lightly interactive HTML/CSS without full logic |
| Design plan | "plan the design", "design strategy", "audit the UX" | Markdown document: user analysis, IA, component inventory, visual direction, roadmap |
| Component library | "design system", "component library" | Reusable components with documented props, variants, and usage guidelines |
| Screen flow / Sitemap | "user flows", "screen map", "navigation structure" | Visual map of all screens and navigation paths |

If they ask for a mockup, do not build a full interactive application. If they ask for a plan, do not start coding.

## Phase 0: Discovery and Context Gathering

Before designing anything, understand the problem space. If the user has not provided sufficient context, ask targeted questions. Do not ask all of these at once; pick the 2-3 most critical gaps.

**User context to gather (if not provided):**
- **User types**: Who uses this? Enterprise users at desks all day? Consumers on phones? Operators monitoring systems? Executives scanning dashboards? Each demands a different density, complexity ceiling, and interaction model.
- **Core tasks**: What are the 3-5 things users do most? Design for the critical path first.
- **Domain and brand**: Industry, brand guidelines, existing design systems, competitor landscape. If a brand kit or style guide exists, align to it. If not, infer appropriate visual language from the domain.
- **Platform and constraints**: Web, mobile, or both? Framework preferences? Accessibility requirements (WCAG level)? Performance budgets?
- **Existing system**: Is this greenfield or an overlay/redesign of something that already exists? If existing, ask for screenshots or URLs to audit.

If the user provides enough context to proceed, skip the questions and start designing. Experienced users should not be slowed down by unnecessary discovery.

## Phase 1: Information Architecture and Interaction Design

For any non-trivial application (more than 2-3 screens), establish structure before visual design.

**Navigation architecture:**
- Map the primary navigation model: sidebar, top bar, tab bar, breadcrumb hierarchy, or hybrid. Choose based on the number of top-level sections and user mental models.
- For enterprise/B2B apps with 8+ sections: collapsible sidebar with grouped categories is almost always right.
- For consumer apps with 3-5 core actions: bottom tab bar (mobile) or clean top nav (web).
- For admin/ops tools: sidebar with search-driven navigation and recent items.

**Screen inventory:**
- List every distinct screen or view the application needs.
- Identify shared layout shells (authenticated layout, onboarding layout, settings layout).
- Map the primary user flows: entry point through task completion through confirmation.

**State mapping:**
- Every screen has at least 4 states: empty, loading, populated, and error. Design for all of them. Empty states are a product opportunity, not an afterthought.
- Identify which screens have additional states: filtering, bulk selection, editing mode, confirmation dialogs.

## Phase 2: Design Direction

Choose a design direction that serves the application's purpose. Application design is not about being "bold" for its own sake. It is about creating an environment where users can accomplish their goals efficiently while feeling confident in the tool.

**Design posture by user type:**

- **Enterprise / B2B**: Professional, information-dense, keyboard-navigable. Prioritize scannability, data tables, and workflow efficiency. Subtle brand expression through accent colors and typography. Think Bloomberg Terminal meets modern SaaS.
- **Consumer**: Approachable, guided, mobile-first. Prioritize progressive disclosure, clear CTAs, and emotional resonance. Brand expression can be more prominent. Think Notion or Linear.
- **Internal tools / Admin**: Utilitarian, dense, no-nonsense. Prioritize speed, bulk actions, and power-user shortcuts. Minimal brand chrome. Think Retool or Django Admin, but refined.
- **Executive / Dashboard**: Glanceable, narrative-driven, status-oriented. Prioritize KPI hierarchy, trend visualization, and drill-down paths. Polished and confident. Think Stripe Dashboard.
- **Operator / Monitoring**: Real-time, alert-driven, high-contrast. Prioritize status indicators, anomaly detection, and quick triage. Often dark-themed for extended viewing. Think Datadog or Grafana.

**Visual identity decisions:**
- **Color system**: Build a semantic color palette, not just a pretty one. Define colors for: primary action, secondary action, destructive action, success, warning, error, info, neutral scale (8-10 steps), and surface layers.
- **Typography**: Choose a font system optimized for the use case. Data-heavy apps need fonts with tabular numerals and clear distinction at small sizes. Consumer apps can use more expressive type. Always define a type scale (at least 6 sizes) with consistent line-height ratios.
- **Density**: Define a spacing scale (4px base recommended) and commit to a density level. Enterprise apps trend denser (compact tables, smaller touch targets). Consumer apps trend more spacious.
- **Elevation and layering**: Define how surfaces stack. Modals, dropdowns, popovers, toasts, and drawers each need a clear z-index and shadow treatment.

## Phase 3: Component Design

Applications are built from components, not pages. Design the component system, then compose screens from it.

**Core component inventory** (design what the app needs, not a generic library):

*Layout*: App shell, sidebar, top bar, content area, split pane, panel group
*Navigation*: Nav items, breadcrumbs, tabs, steppers, command palette
*Data display*: Tables (sortable, filterable, paginated), cards, stat blocks, charts, timelines, activity feeds
*Data input*: Forms, field groups, inline editing, search, filters, date/time pickers
*Feedback*: Toasts, alerts, progress indicators, skeleton loaders, empty states
*Overlays*: Modals, drawers, popovers, dropdown menus, command palette
*Actions*: Buttons (primary, secondary, ghost, destructive), button groups, FABs, split buttons

**Component design principles:**
- Every interactive element needs visible focus states for keyboard navigation.
- Loading states should use skeleton screens that match the component's shape, not generic spinners.
- Error states should be specific and actionable, not just "something went wrong."
- Components should work at multiple density levels if the app supports user preferences.

## Phase 4: Screen Design and Implementation

Build screens by composing components within layout shells. Implement as real working code (HTML/CSS/JS, React, Vue, etc.).

**Implementation standards:** Follow the token architecture, component API patterns, accessibility rules, and responsive strategy in `references/design-system-guide.md`. Every screen must handle empty, loading, populated, error, and any domain-specific states.

**Screen composition approach:**
1. Start with the layout shell (sidebar + content area, or equivalent).
2. Place navigation and wayfinding elements.
3. Build the primary content area for the most common screen state.
4. Add the page header with title, actions, and filters.
5. Implement data display components with realistic sample data.
6. Add interaction behaviors (sort, filter, select, expand).
7. Layer in feedback (loading, empty, error states).
8. Refine micro-interactions and transitions.

**Data visualization guidelines (for dashboards):**
- Choose chart types based on the question being answered, not visual novelty. Bar charts for comparison. Line charts for trends. Tables for precise lookup.
- Use consistent color encoding across all charts on a screen.
- Always include context: titles, axis labels, units, and comparison benchmarks.
- Design for the "so what?" moment. Every metric should lead to an action or a drill-down.

## Phase 5: Design Audit and Retrofit (Existing Projects)

When working with an existing application, follow this process:

1. **Inventory**: Review the current interface. Catalog screens, components, patterns, and inconsistencies.
2. **Assess**: Score the current state across: visual consistency, accessibility, information hierarchy, interaction patterns, responsive behavior, and performance.
3. **Plan**: Produce a prioritized improvement plan. Group changes into tiers:
   - **Quick wins**: Token changes (colors, typography, spacing) that improve consistency without layout changes.
   - **Component upgrades**: Redesigning individual components while keeping the same layout structure.
   - **Flow redesigns**: Rethinking entire user flows where the current UX is fundamentally broken.
   - **System overhaul**: Full design system implementation when the existing codebase has no coherent system.
4. **Execute**: Implement changes tier by tier, validating each before moving to the next.

When auditing, produce a concrete assessment document with specific findings, not vague recommendations. Reference exact screens and components.

## Constraints

### MUST DO
- Choose the output mode before any detailed design or implementation work begins.
- Load the appropriate reference file from the Reference Guide before implementation — do not guess at token values or component patterns.
- Design for the user's highest-frequency tasks before edge workflows.
- Define the complete token set (color, type, spacing, surfaces, elevation) before building any reusable components.
- Implement all four base screen states (empty, loading, populated, error) for every primary view.
- Match component density, interaction model, and information hierarchy to the application's user type and operating context.
- Produce concrete audit findings tied to specific screens, components, or flows when reviewing an existing app — no vague recommendations.
- Use realistic sample data that reflects actual domain content, not lorem ipsum or placeholder values.

### MUST NOT DO
- Do not use marketing-site patterns (hero sections, parallax, testimonial cards, decorative illustrations) inside functional application interfaces.
- Do not apply border-radius over 12px, oversized spacing, or decorative motion that slows task completion in workflow-dense interfaces.
- Do not ship generic dashboard layouts that ignore the actual metric hierarchy, user actions, and drill-down paths for the domain.
- Do not rely on color alone for status, validation, or alerts — always pair with icons, text, or pattern.
- Do not skip dark mode, reduced-motion support, or keyboard navigation for tools built for sustained professional use.
- Do not exceed the requested output mode — no full application when a mockup was asked for.
- Do not hard-code color hex values, pixel sizes, or magic numbers into components — use design tokens.
- Do not duplicate token definitions or component standards already covered by `references/design-system-guide.md`.

## Knowledge Reference

CSS Custom Properties, CSS Grid, Flexbox, semantic HTML, WCAG 2.1 AA, ARIA, WAI-ARIA Authoring Practices, prefers-reduced-motion, prefers-color-scheme, responsive design, design tokens, interaction design, information architecture
