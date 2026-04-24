# Form Controls and Input Selection Guide

This reference covers how to choose the right input control for the data being collected. Picking the wrong control is one of the most common causes of slow, error-prone, and frustrating forms. The right control makes answers obvious, effortless, and hard to get wrong.

See also:
- [Technical Implementation Patterns](./technical-implementation-patterns.md) — Form layout, multi-step wizards, autosave, validation
- [UI/UX Principles](./ui-ux-principles.md) — Strategic design principles
- [Design System Guide](./design-system-guide.md) — Input tokens, sizing, states

## 1. Control Selection Framework

Before choosing a specific control, answer these questions in order:

1. **What is the data type?** (string, number, date, boolean, enumeration, file, range, etc.)
2. **Is it single-value or multi-value?** (one answer or many)
3. **Is the domain known and finite, or open-ended?** (fixed list vs free text vs large searchable set)
4. **How many options are there?** (the single biggest driver of control choice)
5. **What is the user's familiarity with the options?** (recognition vs recall)
6. **How often is this field filled?** (one-time signup vs daily workflow)
7. **What device is primary?** (touch targets and on-screen keyboards matter)

The number of options and whether choice is single or multi determines the control more than anything else.

## 2. Choice Controls — The "How Many Options?" Matrix

Use this matrix as your default. Deviate only when accessibility, density, or domain conventions demand it.

| Options | Single select | Multi-select |
| --- | --- | --- |
| 2 (binary) | Toggle / switch (setting), or two radios (form field) | Checkbox |
| 3–5 | Radio group or segmented control | Checkbox group |
| 6–10 | Radio group (if space) or dropdown | Checkbox group or multi-select dropdown (§3.6) |
| 11–50 | Dropdown (select) | Multi-select dropdown / checkbox dropdown (§3.6) |
| 51–200 | Combobox / autocomplete with search (§3.7) | Multi-select combobox or tag input (§3.7 / §3.8) |
| 50+ | Autocomplete with async search | Transfer list, tag input with async search, or faceted picker |
| Hierarchical (any size) | Tree select / cascader | Tree select with multi-select |
| Unknown / user-created | Tag input (free-text chips) | Tag input with suggestions |

**Key thresholds:**
- **5 options** is the point where radios/checkboxes start to hurt scanability. Above 5, prefer a dropdown unless comparison between options matters.
- **20 options** is the point where a plain dropdown becomes painful to scroll. Above 20, always add search (combobox).
- **50+ single-select options** must use search; a scrolling dropdown is a usability failure.

## 3. Control Reference

### 3.1 Toggle / Switch
**Use for:** Binary on/off settings that take effect immediately or on the next save (e.g., "Enable notifications", "Dark mode").
**Avoid for:** Form questions that require submission. Use radios instead so the user understands the value is staged, not applied.
**Accessibility:** `role="switch"` with `aria-checked`. Pair with a visible label; do not rely on color alone to show state.

### 3.2 Checkbox
**Use for:** Single independent boolean ("I agree to terms"), or multi-select from a small list (3–7 items).
**Avoid for:** Mutually exclusive choices — use radios. Long lists (10+) — use a multi-select dropdown or transfer list.
**Layout:** Stack vertically. Horizontal checkbox rows are hard to scan and fail on narrow screens.

### 3.3 Radio Group
**Use for:** Single-select from 2–5 mutually exclusive, visible-at-a-glance options where comparison matters (e.g., plan tier, shipping speed, payment method).
**Avoid for:** Lists over 5–7 items. Visual clutter grows and scanning becomes linear.
**Variant — Radio cards:** For plan selection, method selection, or anywhere options need rich descriptions, use card-style radios with titles, descriptions, and optional pricing/metadata. Still cap at ~5 cards.

### 3.4 Segmented Control / Button Group
**Use for:** 2–4 short, parallel options that act like a view switch or quick filter (e.g., "List / Grid / Table", "Day / Week / Month").
**Avoid for:** Destructive choices, options with different weights, or labels longer than 1–2 words.
**Typical width:** All segments equal width when labels are similar length; content-sized when labels vary.

### 3.5 Dropdown / Select
**Use for:** Single-select from 6–20 known options where saving vertical space matters more than comparison.
**Avoid for:** Fewer than 5 options (prefer radios — they're faster), or more than 20 options without search (prefer combobox).
**Mobile:** Prefer the native `<select>` on mobile — the OS picker is faster and more accessible than a custom dropdown.
**Accessibility:** Use native `<select>` when possible. Custom comboboxes must implement the WAI-ARIA combobox pattern.

### 3.6 Multi-select Dropdown (Checkbox Dropdown)
This is the pattern implemented by components like PrimeReact `MultiSelect`, MUI `Select` with checkboxes, and Ant Design `Select mode="multiple"`. It is the preferred modern multi-select control — do not confuse it with the native HTML `<select multiple>` (which requires Shift/Ctrl-click to multi-select and is nearly unusable at scale).

**Pattern:** A trigger button showing the current selection opens a floating panel containing a checkbox list. Users click checkboxes to toggle items. The panel stays open until the user clicks outside or presses Esc, allowing rapid selection of multiple items.

**Use for:** Multi-select from ~8–50 known options where users browse the list (e.g., selecting roles, regions, tags, features, languages, team members from a known set).

**Key behaviors to implement:**
- **Trigger display:** Show selected items as chips/tokens inside the trigger (up to ~3), then collapse to "N selected" for longer selections. Offer both display modes (chips or comma-separated) based on density.
- **Select all / Deselect all:** Always include a "Select all" checkbox in the panel header. Show a count of selected items ("3 of 12") when items are partially selected.
- **Built-in filter/search:** Add a search input at the top of the panel when options exceed ~15. Filter in real time on keystroke; do not require Enter.
- **Grouped options:** Support `optgroup`-style headers when the domain has natural categories (e.g., "Americas / APAC / EMEA" for regions).
- **Virtual scrolling:** Enable virtualized rendering when the option count exceeds ~100 to avoid a slow, laggy panel.
- **Clear all:** Provide a clear (`×`) button on the trigger when any items are selected.

**Selection feedback:** The trigger button must always reflect the current state — a closed, empty dropdown that shows no visual indication of how many items are selected is a failure state.

**Prefer this over:**
- Checkbox groups: once options exceed ~7, a checkbox group wastes vertical space and requires scrolling the whole page.
- Native `<select multiple>`: the Shift/Ctrl interaction model is hidden, not discoverable, and unfamiliar to most users.

**Prefer alternatives when:**
- Options exceed ~50 and users can't browse — switch to a combobox with async search (§3.7).
- Users need to type new values in addition to selecting existing ones — use tag input (§3.8).
- Seeing selected vs. available side-by-side matters — use a transfer list (§3.10).
- Space allows and seeing all options simultaneously helps — use a listbox (§3.9).

### 3.7 Combobox / Autocomplete
**Use for:** Single or multi-select from 20+ options, or any field where users know the answer and typing is faster than scrolling (country, user, product SKU, GitHub repo).
**Key behaviors:**
- Debounce input (150–300ms) before querying.
- Highlight matched substring in results.
- Show recent selections at the top when the input is empty.
- Support keyboard navigation (↑↓ to move, Enter to select, Esc to close).
- Async search: show loading state, handle empty results with a "No matches — try X" message.

### 3.8 Tag Input (Chips Input)
**Use for:** Open-ended multi-value lists where users add items one at a time — tags on a post, emails in a recipient field, keywords, skills.
**Key behaviors:**
- Comma, Enter, or Tab creates a chip. Backspace on empty input deletes the last chip.
- Each chip has an `×` remove button (keyboard accessible).
- Validate per-chip (e.g., email format) and highlight invalid chips in red with a tooltip reason.
- Pair with autocomplete suggestions when the domain is known but extensible (e.g., existing tags plus new ones).

### 3.9 Listbox (Inline List)
**Use for:** Single or multi-select from 5–25 options where the list should always be visible (e.g., "Select a printer", "Choose a template") and screen real estate allows.
**Preferred over a dropdown when:** Selection is the primary action of the screen, or users need to see all options to decide.

### 3.10 Transfer List (Dual List Box)
**Use for:** Multi-select from a moderate-to-large list (20–500 items) where users need to see what's selected vs available side-by-side (e.g., permissions, team members, report columns).
**Structure:** Two lists — "Available" on the left, "Selected" on the right, with add/remove arrow buttons between. Include search in each pane when counts exceed ~20.
**Avoid for:** Fewer than 20 options (overkill), or highly hierarchical data (use tree select instead).

### 3.11 Tree Select / Cascader
**Use for:** Hierarchical choices — categories, org structure, file paths, geographic regions (country → state → city).
**Cascader variant:** Stepped columns that reveal children when a parent is selected — good for deep, known hierarchies where only the leaf matters.
**Tree variant:** Expandable/collapsible nodes with checkboxes — good when users may select at any level.
**Always include:** Search that filters and auto-expands matching branches.

### 3.12 Picker / Modal Picker
**Use for:** Complex selection that doesn't fit a dropdown — selecting from a large indexed catalog with previews (icons, images, users with avatars and metadata).
**Open pattern:** Button showing current selection opens a modal with search, filters, and a grid or list of selectable items.

## 4. Numeric Input

| Control | When to use |
| --- | --- |
| Number input with stepper | Precise values where users often type (quantity, price, age). Always allow direct keyboard entry. |
| Slider (single thumb) | Imprecise values in a bounded range where feedback is visual (volume, opacity, zoom, rough filters). |
| Range slider (two thumbs) | Bounded min/max ranges (price range, date range filters). |
| Rating (stars / scale) | Subjective evaluation on a fixed scale (1–5, 1–10). Always show numeric label alongside stars for accessibility. |
| NPS / likert scale | Survey-style fixed-point scales. Render as a horizontal button group with clear endpoint labels. |
| Stepper (+ / −) | Small integer adjustments in compact UI (cart quantity, seat count). Always pair with a typable number field. |

**Sliders — critical rules:**
- Always show the current value numerically next to the slider. A slider without a value label is nearly useless.
- Include min/max labels at the track ends.
- Provide a text input alongside for precise entry when precision matters.
- Step size should match the granularity the value actually needs (don't offer 0.01 steps for a volume slider).
- Avoid sliders for values users need to set exactly — typing is faster.

**Number input — critical rules:**
- Use `inputmode="numeric"` or `inputmode="decimal"` for mobile keyboards.
- Disable scroll-to-change by default (accidental changes from page scrolling are a common bug).
- Right-align numeric values in tables and grids; left-align in forms.
- For currency, show the symbol as an input addon, not inside the input.

## 5. Text Input

| Control | When to use |
| --- | --- |
| Single-line text input | Short free-form strings (name, title, search, URL). |
| Multi-line textarea | Free-form text over one sentence (description, comment, message). Auto-grow up to a max height, then scroll. |
| Masked input | Formatted strings with a known pattern (phone, credit card, SSN, license plate). Show the mask as placeholder scaffolding. |
| Password input | Secret strings. Include a reveal/hide toggle. For signup, show a live strength meter and rule checklist. |
| Search input | Any search field. Include a leading search icon, a clear (`×`) button when populated, and `type="search"` on mobile for the right keyboard. |
| Rich text editor | Formatted content (blog posts, descriptions with lists/links/images). Only use when formatting is genuinely needed — otherwise a plain textarea is faster and more predictable. |
| Mention / at-input | Text with inline references to users, pages, or items. Trigger autocomplete on `@`, `#`, `/` etc. |
| Code editor | Code snippets, query editors, template editors. Use a real editor (Monaco, CodeMirror) with syntax highlighting and autocomplete — never a plain textarea. |

**Text input — critical rules:**
- Set `autocomplete` attributes (`name`, `email`, `current-password`, `one-time-code`, etc.) — this is a free usability win.
- Use `inputmode` for mobile keyboards (`email`, `tel`, `url`, `numeric`, `decimal`, `search`).
- Never disable paste — this breaks password managers and is actively user-hostile.
- Show character count when a max length is enforced; warn before the limit, not just at it.

## 6. Date and Time Input

| Control | When to use |
| --- | --- |
| Date picker (calendar popover) | Picking a single date within a reasonable window (typically the next/past year). |
| Date range picker | Selecting start + end dates (trip booking, report range, filter). Use a two-month calendar view. |
| Time picker | Standalone time selection (reminders, scheduling). Offer 15- or 30-minute snap intervals by default. |
| DateTime picker | Combined date + time. Prefer two separate controls (date then time) over one combined one — easier on mobile. |
| Segmented date input | Typing the date directly (MM / DD / YYYY) — faster for power users who know the date (birthdate, expiration). Always pair with an optional calendar. |
| Relative date picker | Business date ranges: "Last 7 days", "This month", "Quarter to date". Essential for dashboards and analytics. |
| Natural language input | Advanced: parse "next Friday", "in 2 weeks", "Q4". Only add when the audience is power users. |

**Date input — critical rules:**
- Always indicate the expected format (placeholder, format hint, or masked input).
- Native `<input type="date">` is acceptable for simple use cases but has limited customization and inconsistent UX across browsers — use a library for anything user-facing at scale.
- Disable obviously invalid dates (past dates for future events, dates before a minimum, blocked days).
- For ranges: highlight the range while the user hovers between dates so they see what they're about to pick.
- Default to the most likely value (today, next business day, start of current month) rather than an empty field.

## 7. File and Media Input

| Control | When to use |
| --- | --- |
| File upload button | Standard file selection, single or multiple. Show file name(s) and size after selection. |
| Drag-and-drop zone | Primary upload affordance on upload-heavy screens (attachments, imports, media libraries). Always include a fallback "browse" button — drag-and-drop is not discoverable. |
| Image cropper | User-uploaded avatars, hero images, or anything with aspect-ratio requirements. Show the resulting frame in real time. |
| Camera capture | Mobile-first flows where photos are the input (receipts, IDs, check deposit). Use `<input type="file" accept="image/*" capture>`. |
| Clipboard paste | Screenshot-heavy tools (bug reports, support tickets). Listen for paste events on the textarea or upload zone. |

**File input — critical rules:**
- Show accepted file types and max size before the user picks a file.
- Show per-file progress for multi-file uploads; allow canceling an in-flight upload.
- Validate on the client (type, size) before upload, and again on the server.
- For images, show a thumbnail preview after selection — not just the file name.

## 8. Specialized Controls

| Control | When to use |
| --- | --- |
| Color picker | Design tools, brand customization. Offer a palette of brand/preset colors first, custom picker second. Never force users to type hex codes for common choices. |
| Address autocomplete | Any address field. Use a geocoding service (Google Places, Mapbox, etc.) rather than free-form city/state/zip fields — dramatically reduces errors. |
| Phone input with country selector | International phone numbers. Detect country from locale; format as the user types. |
| Location / map picker | Selecting a point or area on a map. Include both map interaction and an address search. |
| Signature pad | E-signature flows. Offer "type", "draw", and "upload" modes. |
| OTP / verification code | 2FA and verification. Use separate single-character inputs with auto-advance, `autocomplete="one-time-code"`, and paste support that fills all boxes. |
| Permission / capability grid | Role and permission editors. A table of capabilities × roles with checkboxes is usually clearer than nested dropdowns. |

## 9. Common Anti-Patterns

Avoid these. They show up constantly and they're always worse than the alternative.

| Anti-pattern | Why it's bad | Use instead |
| --- | --- | --- |
| Radio group with 15+ options | Unscannable, wastes vertical space | Dropdown (6–20) or combobox (20+) |
| Dropdown with 3 options | Hides options behind a click; comparison is impossible | Radio group or segmented control |
| Checkboxes for mutually exclusive choices | Users will check multiple, data is invalid | Radio group |
| Radios for independent booleans | Forces an "either/or" mental model that doesn't match | Checkboxes |
| Dropdown with 50+ unsearchable options | Endless scrolling, no way to find items | Combobox with search |
| Slider for precise numeric input | Impossible to hit exact values | Number input (pair with slider if visual feedback helps) |
| Slider with no current-value label | User can't tell what's selected | Always show the numeric value |
| Free-text for known enums (e.g., country) | Data quality destroyed by typos | Combobox with async search |
| Separate city/state/zip text fields | Error-prone, slow | Address autocomplete |
| Disabling paste on password fields | Breaks password managers | Allow paste |
| Auto-submitting on dropdown change | Users can't cancel; accidental commits | Explicit submit, or autosave with undo |
| Placeholder-as-label | Disappears on focus, fails WCAG, poor contrast | Persistent label above the field |
| Toggle for form fields that need submission | Implies immediate effect | Radio or checkbox |
| Tiny touch targets on mobile | Failed taps, user frustration | Minimum 44×44 px hit area |

## 10. Scaling Forms — When Controls Aren't Enough

When a single screen has more than ~10 fields, the control choice matters less than the overall structure. Apply these patterns:

**Progressive disclosure:** Show only the fields needed for the current decision. Reveal conditional fields as prior answers make them relevant (see [Technical Implementation Patterns §9](./technical-implementation-patterns.md) — dependent fields).

**Chunking:** Group fields into logical sections with clear headings. Use `<fieldset>` / `<legend>` or visual section dividers. Seven-fields-per-section is a good upper bound.

**Multi-step wizards:** For 15+ fields or fields that map to distinct stages (account → profile → preferences → confirmation), split across steps. See [Technical Implementation Patterns §9](./technical-implementation-patterns.md) — multi-step forms.

**Defer the rare:** Fields needed by 10% of users belong behind an "Advanced" disclosure, not in the primary flow.

**Smart defaults:** Every field that can have a sensible default should. A defaulted field is ~5× faster than an empty one.

**Review screens:** For high-stakes submissions (orders, legal, irreversible actions), end with a read-only summary before the submit button.

## 11. Mobile-Specific Considerations

Mobile changes the calculus. Controls that work on desktop can be actively hostile on a phone.

- **Prefer native controls** (`<select>`, `<input type="date">`, `<input type="color">`) on mobile — the OS pickers are faster, accessible, and familiar.
- **Long radio/checkbox lists** become a scroll prison on small screens; collapse into a dropdown or picker.
- **Drag-and-drop uploads** don't work on mobile — always provide the tap-to-upload fallback.
- **Sliders** need larger thumbs (minimum 44×44 px hit area) on touch.
- **Multi-column forms** always collapse to single column below ~640 px.
- **Transfer lists** don't fit on mobile — use a picker modal pattern instead.
- **Keyboard types:** set `inputmode` and `type` correctly so users get the numeric pad, email keyboard, URL keyboard, etc.
- **Avoid hover-only affordances** — anything discoverable only via hover is invisible to touch users.

## 12. Accessibility Checklist for Every Control

Every input, regardless of type, must satisfy:

- [ ] A visible, persistent label associated via `for`/`id` or wrapping `<label>`.
- [ ] A visible focus ring (do not set `outline: none` without a replacement).
- [ ] Keyboard operable: Tab to focus, Enter/Space to activate, arrow keys for grouped controls (radios, tabs, sliders).
- [ ] State conveyed by more than color (icons, text, patterns).
- [ ] Error messages associated via `aria-describedby`, announced on submit failure.
- [ ] Required fields marked with both visual indicator (`*`) and `aria-required="true"` or `required`.
- [ ] Supports browser autofill where appropriate (`autocomplete` attribute).
- [ ] Works with screen readers — test with VoiceOver or NVDA, not just visually.
- [ ] Minimum 44×44 px touch target on mobile.
- [ ] Respects `prefers-reduced-motion` for any reveal/collapse animation.
