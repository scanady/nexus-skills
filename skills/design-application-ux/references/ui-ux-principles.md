# Core Application UI/UX Principles

This document defines the foundational User Interface and User Experience principles for all web application design. These principles are the decision filter for every design choice — from high-level information architecture down to individual component states.

See also:
- [Application Aesthetics Guidelines](./aesthetics-guidelines.md) — Visual identity, brand expression, and distinctive design
- [Design System Guide](./design-system-guide.md) — Token architecture, component specs, and implementation standards
- [Technical Implementation Patterns](./technical-implementation-patterns.md) — Architecture, state management, performance
- [Application Layout Patterns](./application-layout-patterns.md) — Navigation models, page archetypes, and composition

---

## 1. Design for the Domain, Not the Medium

The most distinctive applications feel purpose-built for their domain. A healthcare scheduling app should not feel like a fintech dashboard with different data. The domain should shape every decision.

*   **Let the domain drive the vocabulary.** Use the terminology and mental models of the user's domain, not generic tech labels. A legal tool should say "Matter" and "Docket," not "Project" and "List."
*   **Match the operational tempo.** A stock trading interface needs sub-second response and extreme information density. A project planning tool can afford more whitespace and deliberation. Design for the pace at which users actually work.
*   **Respect domain conventions.** If the industry has established conventions (e.g., red/green in finance, Gantt charts in project management, SOAP notes in healthcare), use them. Reinventing domain-standard patterns creates friction.
*   **Design for the environment.** Consider where and how users work — bright warehouse floor, quiet office, crowded coffee shop, surgical suite. Lighting, noise, device type, and posture all influence contrast needs, touch target size, and information density.

## 2. Express the Brand Through the Experience

Brand is not a skin applied after the UX is done. It lives in how the application behaves, communicates, and feels in use.

*   **Brand lives in interaction, not just color.** A playful brand might use bouncy easing curves and informal microcopy. A serious financial brand uses linear transitions and precise language. The interaction personality should match the brand personality.
*   **Tone of voice is a design element.** Every piece of UI text — button labels, empty states, error messages, tooltips, confirmation dialogs — carries brand tone. Define whether the application speaks formally, conversationally, technically, or warmly, then apply that voice consistently.
*   **Choose a design posture.** Applications fall on spectrums: dense↔spacious, technical↔approachable, neutral↔expressive, minimal↔rich. Consciously select where on each spectrum the brand lives, then design consistently to that posture.
*   **Brand accent, not brand saturation.** Most of the application surface should be neutral and functional. Brand color and personality should appear at strategic moments: the primary CTA, the logo, the onboarding flow, the success states, the empty-state illustrations. Brand expression that is everywhere is actually nowhere.

## 3. Clarity over Cleverness

The primary measure of a functional application is how quickly a user can complete their task.

*   **Obvious is always better.** Do not hide primary actions behind tooltips or hover states. The user should not need to explore the interface to find the thing they came to do.
*   **Predictable metaphors.** Use standard established icons (gear for settings, magnifying glass for search, plus for create). Do not invent new metaphors for standard actions.
*   **Text over Icons.** If the action is destructive, complex, or unfamiliar, use an icon + label, or just a text label. Icon-only buttons are reserved for universally understood actions (close, search, home).
*   **One primary action per view.** Every screen should have one obviously dominant call-to-action. If two actions compete visually, neither wins the user's attention.

## 4. System Status and Feedback

The user should never have to guess what the system is doing.

*   **Immediate interaction feedback.** Every clickable element needs a visible pressed/active state. Every form field needs a clear focus state. The interface must respond within 100ms to feel instantaneous.
*   **Asynchronous feedback.** If an operation takes longer than 400ms, show a loading indicator (spinner, progress bar, or skeleton). If it takes longer than 4 seconds, provide a progress estimate or status message.
*   **Result confirmation.** Use transient notifications (toasts/snackbars) for success or failure of background operations. Success toasts auto-dismiss (5s); error toasts persist until dismissed.
*   **Optimistic UI.** For common, low-risk actions (starring, favoriting, toggling settings), update the UI immediately and reconcile with the server in the background. Roll back gracefully on failure.

## 5. Cognitive Load Reduction

Users should not have to remember information from one part of the interface to another.

*   **Progressive disclosure.** Start with the most common actions visible. Hide power-user features behind "Advanced" sections, secondary menus, or keyboard shortcuts — but make them discoverable.
*   **Sensible defaults.** Pre-fill forms with the most likely choices. A date picker for scheduling should default to tomorrow, not January 1, 1970. A status dropdown should default to "Active."
*   **Chunking.** Break long processes into steps. A 20-field setup form becomes 4 steps of 5 fields. Show progress (step 2 of 4) and allow navigation between completed steps.
*   **Recognition over recall.** Show recent items, favorites, and suggestions. Autopopulate where possible. Never force the user to type something they've already told the system.

## 6. Forgiveness and Error Recovery

Users make mistakes. Good applications make errors easy to catch, understand, and fix without losing work.

*   **Destructive actions need friction.** Require a confirmation step for delete operations. For high-stakes irreversible actions (delete account, drop database), require typed confirmation of the entity name.
*   **Inline validation.** Validate form inputs as the user completes each field (on blur), not only on submit. Show the specific validation rule that failed, not a generic "Invalid input."
*   **Undo > Confirmation prompts.** When possible (archiving, moving, status changes), execute the action immediately and offer a toast with "Undo" for 8 seconds. This is faster and less annoying than "Are you sure?" dialogs.
*   **Constructive error messages.** Frame errors in the user's context with a clear recovery path: "We couldn't save your changes — you've lost your internet connection. Your changes are saved locally and will sync when you reconnect."
*   **Autosave.** For long-form content (editors, form wizards, configuration pages), save drafts automatically at intervals. Indicate save status ("All changes saved" / "Saving..." / "Unsaved changes").

## 7. Information Architecture

The structure of the application determines whether users find things or get lost.

*   **Match the user's mental model, not the database schema.** If users think in terms of "Clients" and "Projects," do not organize navigation around "Records" and "Entities" because that is how the backend works.
*   **Flat over deep.** Shallow navigation structures (2-3 levels max) outperform deep trees. If navigation requires more than 3 clicks to reach any primary function, the IA needs restructuring.
*   **Wayfinding.** Users must always know: where they are (active nav state, breadcrumbs), where they can go (visible navigation), and how to get back (back buttons, breadcrumbs, browser history support).
*   **Search as navigation.** In applications with more than 15-20 distinct destinations, a command palette or global search bar is essential. It should index pages, actions, settings, and recent items.
*   **Group by task, not by object type.** Instead of separate "Users," "Roles," and "Permissions" sections, consider a single "Team Management" area that groups related functions by the task the admin is performing.

## 8. Consistency and Standards

Users spend most of their time on other applications. Treat external conventions as constraints.

*   **Internal consistency.** A primary button must look and behave identically on every screen. A date picker must work the same on the reporting page and the settings page. Establish patterns once and enforce them everywhere.
*   **External consistency.** Follow platform conventions: navigation placement, keyboard shortcuts, dialog behaviors, and gesture patterns that users already know from daily use of other tools.
*   **Pattern library discipline.** If a pattern exists in the design system, use it. If a pattern does not exist, add it to the system — do not create one-off solutions. One-offs become inconsistencies.

## 9. User Control and Freedom

Design for a spectrum of expertise. Power users need speed; new users need guidance.

*   **Keyboard-first for power users.** Provide hotkeys for repetitive actions (`Cmd+K` for command palette, `/` to focus search, `E` to edit). Display shortcut hints in tooltips and menus.
*   **Escape hatches.** Every modal, wizard, drawer, and overlay must be closable via a visible "Cancel"/"Close" button and the `Escape` key. Multi-step processes must allow backward navigation.
*   **Customization.** Allow users to configure density (compact/default/comfortable), default views (list/grid/kanban), sidebar state (expanded/collapsed), and column visibility in tables — and persist those preferences.
*   **Bulk operations.** In list and table contexts, support multi-select with Shift+Click and Ctrl/Cmd+Click, and reveal a contextual bulk-action toolbar when items are selected.

## 10. Onboarding and First-Run Experience

The first 5 minutes determine whether the user adopts or abandons the tool.

*   **Time to value, not time to tour.** Get the user to their first meaningful action as fast as possible. Do not gate the core experience behind a 7-step onboarding wizard that explains features they have not used yet.
*   **Empty states are onboarding.** The very first view the user sees is an empty state. Design it to explain the value of the feature and provide a single obvious CTA to get started: "Create your first project" with a clear button.
*   **Progressive onboarding.** Introduce features contextually as the user encounters them, not all at once. A tooltip explaining bulk export appears the first time the user selects multiple items, not during signup.
*   **Checklists for setup.** If the application requires configuration (connecting integrations, inviting team members, importing data), show a progress checklist that tracks completion and can be dismissed when done.
*   **Sample data.** For complex applications (dashboards, analytics, project management), offer pre-populated demo data so users can see the interface in its fully populated state before investing time in their own setup.

## 11. Content Design Within the Interface

Every word in the UI is a design decision. Interface text is not filler — it is the primary way the application communicates.

*   **Labels should describe the outcome, not the mechanism.** "Save and continue" is better than "Submit." "Invite teammate" is better than "Add user." "Go live" is better than "Publish."
*   **Microcopy reduces support tickets.** Placeholder text in fields, helper text below inputs, tooltip explanations on complex settings — these small text elements prevent confusion before it starts.
*   **Error messages are a product.** Treat error states as opportunities to build trust. Explain what happened, why it happened, and what the user can do next. Never show raw error codes or stack traces to end users.
*   **Consistent terminology.** If it is called a "Workspace" in the sidebar, do not call it a "Space" in the settings page and a "Project" in the API docs. Maintain a content glossary for the product.

## 12. Trust and Credibility

Users must trust the application before they will trust it with their data and workflows.

*   **Visual polish signals competence.** Alignment errors, inconsistent spacing, broken layouts at certain viewport widths, and mismatched component styles all erode trust, especially for financial, healthcare, and security-sensitive applications.
*   **Transparency with data.** Show users what data is collected, where it is stored, and who can access it. Make privacy controls accessible, not buried in a sub-sub-menu.
*   **Predictable behavior.** The application must never do something the user did not ask for. No auto-subscribing to newsletters, no changing settings without consent, no silent data sharing.
*   **Graceful error handling.** An application that shows a blank white screen on error feels broken. An application that shows a descriptive error page with a recovery path feels reliable even when things go wrong.
*   **Performance is trust.** A slow application feels unreliable. Target < 200ms for interaction response, < 1s for navigation, < 3s for initial page load. Show perceived performance improvements (skeleton screens, optimistic updates) for anything that takes longer.

## 13. Aesthetic Integrity

The visual design should support the task and express the brand, not compete with either.

*   **Data density by context.** Enterprise applications need high data density. Consumer applications need more breathing room. The same application might need different densities for its dashboard (dense) and its settings page (spacious).
*   **Visual hierarchy.** Size, weight, color, and position must immediately communicate what is most important. The user's eye should flow naturally from the most critical data to the primary action without scanning.
*   **Restraint is a feature.** The best application interfaces feel calm, even when displaying complex data. Achieve this through consistent spacing, limited color palette usage, and generous whitespace around dense content areas.
*   **Motion with purpose.** Animation should communicate state changes (element entering, transitioning, exiting), not decorate static content. Every animation should answer the question: "What information does this motion convey?"
