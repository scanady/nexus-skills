# Technical Implementation Patterns

This document outlines standard architectural approaches, tools, and technical strategies for implementing UI and UX features in modern web applications. Adhere to these principles to maintain scalability, performance, and accessibility.

See also:
- [Core UI/UX Principles](./ui-ux-principles.md) — Strategic design principles
- [Application Aesthetics Guidelines](./aesthetics-guidelines.md) — Visual identity and brand expression
- [Design System Guide](./design-system-guide.md) — Token architecture and component specs
- [Application Layout Patterns](./application-layout-patterns.md) — Navigation models and page archetypes
- [Form Controls Guide](./form-controls-guide.md) — Input type selection and form control patterns

## 1. Component Architecture
A robust component architecture separates presentation from logic.

*   **Smart vs. Dumb Components:** Smart (container) components fetch data, manage complex state, and handle side effects. Dumb (presentational) components receive data via props and emit events via callbacks. Dumb components should represent 80-90% of the application's components.
*   **Composition over Configuration:** Avoid passing endless conditional flags (`isPrimary`, `isLarge`, `hasIcon`) down into a single massive component. Instead, compose small, tailored components (e.g., `<PrimaryButton>`, `<IconTextButton>`) or use compound components.
*   **Polymorphic Components:** When building complex UI pieces like Accordions or Select Menus, use a compound format so the user has control over the child elements: `<Accordion.Root><Accordion.Item><Accordion.Header/></Accordion.Item></Accordion.Root>`.

## 2. State Management
Choosing where state lives impacts complexity and performance.

*   **Server State (e.g., SWR, React Query, Apollo):** Manage asynchronous data fetching, caching, synchronization, and optimistic UI updates through dedicated data-fetching libraries. Server state does not belong in global application state.
*   **Local UI State (e.g., useState, useReducer):** State that only affects a specific component (e.g., "is this modal open?", "is this dropdown expanded?") should live locally in that component.
*   **Global Application State (e.g., Zustand, Redux, React Context):** State that must be accessed across deeply nested components (like the authenticated user session, shopping cart, or a dark mode toggle) should live globally, but global state should be kept as thin as possible.

## 3. Styling Strategy
Styling should be maintainable, scalable, and highly cohesive.

*   **Utility-First (Tailwind CSS):** Use for rapid iteration and managing a robust design system natively. Avoid extracting CSS classes from Tailwind utilities unless the component logic forces it, as it breaks the benefit of seeing the styles where the component is rendered.
*   **CSS Variables (Custom Properties):** Always define design tokens (colors, fonts, spacing) as CSS variables in a central file (`theme.css` or `globals.css`). This dramatically simplifies theming (like dark mode). See `design-system-guide.md` for specific token architecture.
*   **Scoped Styling (CSS Modules or CSS-in-JS):** If not using a utility-first framework, enforce scoping to ensure a style change in one component cannot subtly break another.

## 4. Performance Optimization
Do not build applications that are slow to run on an average machine.

*   **Code Splitting and Lazy Loading:** Routes and large third-party dependencies should be dynamically imported or code-split. Never load a 5MB graphing library on the initial page load if the user is on the login screen.
*   **Virtualization:** Long lists (over 100-200 items, or complex row structures) should use windowing/virtualization (e.g., `react-virtual`) to render only the DOM nodes currently visible.
*   **Debouncing and Throttling:** Rapid, continuous user input like typing in a real-time search box, resizing windows, or scrolling must be debounced or throttled to prevent blocking the main thread.
*   **Image Optimization:** Use modern formats (`WebP`, `AVIF`), enforce `loading="lazy"` for below-the-fold assets, and properly size `srcset` values for responsive sizing. Provide `width` and `height` attributes to prevent Cumulative Layout Shift (CLS).

## 5. Accessibility Implementation Toolkit
Accessibility (a11y) is not optional. It must be built into the foundation.

*   **Semantic HTML:** Use native elements (`<button>`, `<a>`, `<dialog>`, `<form>`, `<main>`, `<nav>`) before applying custom ARIA attributes to generic `div`s.
*   **Focus Management:** When opening a modal, focus should be trapped inside the modal until it is closed. Upon closing, focus should be returned to the element that triggered the modal. Use libraries like `react-aria` to handle focus scope and trap accurately.
*   **Hidden Actionable Content:** Text for screen readers that shouldn't be visible to sighted users (e.g., specifying an icon button's function) should utilize a visually hidden (but screen-reader accessible) utility class, such as `.sr-only`. 
*   **Announcements (`aria-live`):** When dynamic content successfully changes without a page reload (e.g., form submissions, loading completions), use `aria-live` regions to announce the result to assistive technologies.

## 6. API and Error Handling Architecture
*   **Centralized Error Handling:** Catch HTTP errors in one central place (e.g., an Axios interceptor) rather than rewriting `try/catch` logic 100 times. If a request returns a `401 Unauthorized`, automatically redirect to the login page.
*   **Idempotent Retries:** For critical paths (like saving data), ensure API operations are retryable without side effects, and build fallback UI logic for offline states.
*   **Graceful Degradation:** The application should not completely break if a non-critical third-party service (like an analytics script or an avatar loading service) goes down.

## 7. Testing
*   **End-to-End (E2E) (e.g., Playwright, Cypress):** Focus E2E tests on critical user journeys (the "happy path"): logging in, creating an enterprise project, sending a payment.
*   **Integration Tests (e.g., React Testing Library):** Ensure data is correctly passed from parent to children, that APIs are properly mocked, and that user interaction updates the DOM correctly.
*   **Component Tests:** Use tools like Storybook to handle visual regression testing and ensure components look identically responsive across updates.

## 8. Navigation Implementation Patterns

Navigation is the skeleton of the application. The wrong navigation model makes every screen harder to use.

**Sidebar navigation:**
- Use for applications with 5+ top-level sections. Implement as a `<nav>` with `<aside>` landmark.
- Collapsible: expand/collapse with a toggle button that persists preference to `localStorage`.
- Grouped sections: use expandable groups with `aria-expanded` for categories with 3+ sub-items.
- Active state: highlight the current page item with a background color and/or left border accent.
- Footer section: place help, settings, and user profile in the sidebar footer (after a divider/spacer) to separate functional nav from administrative items.

**Top navigation bar:**
- Use for applications with 3-5 top-level sections or consumer-facing products with simple IA.
- Left: logo/brand mark + primary nav links. Center: search (optional). Right: notifications, user avatar/menu.
- Responsive: collapse nav links into a hamburger menu on mobile; keep the logo and critical actions visible.
- Mega menus (dropdown with multi-column content) are appropriate for complex enterprise products but must be keyboard accessible.

**Command palette / search-as-navigation:**
- Implement for any application with 15+ distinct destinations or frequent power users.
- Trigger via `Cmd+K` / `Ctrl+K`. Index: pages, actions, settings, recent items, and quick commands.
- Results should include icons, breadcrumb path context, and keyboard-selectable items.
- Recency-weighted: show recently accessed items first when the palette is empty.

**Breadcrumb navigation:**
- Use when content has a hierarchical structure deeper than 2 levels (e.g., Workspace > Project > Task).
- Implement as a `<nav aria-label="Breadcrumb">` with an `<ol>`, using `aria-current="page"` on the last item.
- Truncate middle items with an ellipsis dropdown when the path exceeds 4 segments.

**Tab navigation (within a page):**
- Use for switching between views of the same entity (e.g., a project's Overview / Tasks / Settings tabs).
- Implement with `role="tablist"`, `role="tab"`, and `role="tabpanel"`. Support arrow key navigation between tabs.
- Persist the active tab in the URL hash or query parameter so it survives page reload and sharing.

## 9. Form Design Patterns

Forms are the primary input mechanism for most applications. Poor form design directly causes abandonment and errors. This section covers form **layout and behavior**. For choosing the right **input control** for each field (radio vs dropdown vs combobox vs transfer list, slider vs number input, etc.), see [Form Controls Guide](./form-controls-guide.md).

**Layout principles:**
- Single-column forms outperform multi-column forms for completion rate — use multi-column only when fields are logically paired (first name + last name, city + state + zip).
- Labels above inputs (not inline/floating). Floating labels reduce readability for filled fields and cause accessibility issues with screen readers.
- Group related fields with a section heading and `<fieldset>` / `<legend>` (or visual equivalent).

**Multi-step forms (wizards):**
- Show a progress indicator (step N of M) at the top of the form.
- Allow backward navigation to review/edit previous steps without losing data.
- Validate each step before allowing the user to proceed to the next.
- Save draft state between steps (server-side or `localStorage`) so users can resume.
- Final step: show a summary/review of all entered data before the primary submit action.

**Inline editing:**
- Use for data tables and property panels where users frequently update individual values.
- Enter edit mode: click on the value or an explicit "Edit" button/icon.
- Confirm: Enter key or blur. Cancel: Escape key. Show saving state inline.
- Validate immediately on confirm. Show error inline next to the edited field.

**Autosave:**
- Use for long-form content (text editors, configuration pages, multi-field settings).
- Save automatically 1-2 seconds after the user stops typing (debounced).
- Show save status persistently: "All changes saved" / "Saving..." / "Unsaved changes" / "Save failed — retry."
- Use optimistic save with conflict detection for collaborative editing scenarios.

**Dependent / conditional fields:**
- Show/hide fields based on prior selections (e.g., "Other — please specify" text field appears when "Other" is selected).
- Animate the reveal with a slide-and-fade (150-200ms) to maintain spatial context.
- Clear hidden field values when the condition is no longer met to avoid submitting stale data.

## 10. Search and Filtering Patterns

Search and filtering are critical for any application with more than a few dozen items in a list.

**Global search:**
- Single search input accessible from any page (typically in the top bar or via keyboard shortcut).
- Return results grouped by type (pages, records, people, settings) with type labels and icons.
- Debounce input (300ms) and show results in a dropdown/overlay. Support keyboard navigation of results.

**Faceted filtering:**
- Use for data-heavy list/table views (e.g., filtering a contact list by status, role, and date range simultaneously).
- Filters can live in a side panel (horizontal space available) or a collapsible filter bar above the table (limited width).
- Each active filter should be visible as a removable chip/tag. Show a "Clear all filters" action when any filters are active.
- Persist filter state in the URL query string so filtered views are shareable and bookmarkable.

**Table-specific filtering:**
- Column header filters: small filter icons in the table header that open a dropdown for that column.
- Quick filter: a single text input above the table that searches across all visible columns.
- Saved views: allow users to save filter + sort + column visibility combinations as named views (e.g., "My open tasks," "High priority + unassigned").

**Search result presentation:**
- Highlight matching text in results.
- Show metadata context (category, date, status) alongside the primary match.
- For zero results: suggest corrections ("Did you mean..."), show related items, and offer to broaden the search.
