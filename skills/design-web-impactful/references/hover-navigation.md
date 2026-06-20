# Hover Navigation Pattern

Table stakes for any marketing site with a multi-group primary nav. Implement as the default in both conversion-safe and expressive mode. Note: hover-nav is a baseline interaction quality signal, not a differentiator. It prevents a broken experience; it does not create a memorable one. The concept, type, and signature moment do that. Get this right, then focus creative energy on the things that make the site distinct.

## Behavior Contract

- **Mouse:** hover the trigger to open. Move into the panel; it stays open. Move away and it closes after ~140ms so the cursor can cross the gap without losing the menu.
- **Touch:** hover does nothing. Tap to toggle.
- **Keyboard:** focus opens the menu. Tab through items. Escape closes. Click outside closes.
- **Bridge:** an invisible ::before strip (~16px tall) above the panel covers the gap between trigger and panel. The most commonly missed detail and the most common reason hover menus feel broken.
- **State:** controlled via a single data-open="true|false" attribute on the wrapper. Drives both visual state (CSS) and accessibility state (aria-expanded, tabIndex).

## Why Not details/summary?

Native `<details>` has no hover behavior, no transition, no panel positioning, and no touch story distinct from desktop. It is wrong for primary navigation.

## Expressive Mode Navigation Alternatives

In expressive mode, consider whether the standard hover-nav is the right pattern. Alternatives used in award-caliber work:

- **Full-screen overlay nav:** triggered by a minimal icon. The nav becomes a designed moment with large type and a background that matches the brand's world.
- **Sidebar drawer nav:** slides in from the left or right with the primary sections as large typographic elements.
- **Mega-menu editorial layout:** the dropdown panel is full-width with rich content (featured case study, large image, editorial grid of links).

If using an alternative nav pattern in expressive mode, the behavior contract (keyboard, touch, Escape, outside-click) still applies.

## React Implementation (Next.js App Router, React 19)

See `assets/hover-nav.tsx` for the paste-ready component. Key constructs:

```tsx
const HOVER_CLOSE_DELAY_MS = 140;

const closeTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
const navRef = useRef<HTMLElement | null>(null);

const clearCloseTimer = () => { if (closeTimer.current) { clearTimeout(closeTimer.current); closeTimer.current = null; } };
const scheduleClose  = () => { clearCloseTimer(); closeTimer.current = setTimeout(() => setOpenMenu(null), HOVER_CLOSE_DELAY_MS); };
const openNow        = (label: string) => { clearCloseTimer(); setOpenMenu(label); };

<div
  data-open={isOpen ? "true" : "false"}
  onPointerEnter={(e) => { if (e.pointerType !== "touch") openNow(group.label); }}
  onPointerLeave={(e) => { if (e.pointerType !== "touch") scheduleClose(); }}
  onFocus={() => openNow(group.label)}
  onBlur={(e) => { if (!e.currentTarget.contains(e.relatedTarget as Node)) scheduleClose(); }}
>
  <button onClick={() => setOpenMenu(isOpen ? null : group.label)} aria-expanded={isOpen} aria-haspopup="true">
    {group.label}
  </button>
  <div role="menu" aria-hidden={!isOpen}>
    {items.map(item => <Link href={item.href} role="menuitem" tabIndex={isOpen ? 0 : -1}>{item.label}</Link>)}
  </div>
</div>
```

Required effects (paste-ready in the asset file):
- Close on route change (usePathname dependency).
- Document-level pointerdown listener closes on outside click.
- Document-level keydown listener closes on Escape.
- Cleanup closeTimer on unmount.

## CSS

See `assets/hover-nav.css` for the paste-ready stylesheet. Architecture:

- `.nav-menu`: positioning context for the panel.
- `.nav-menu > .nav-summary`: the trigger button (44px min-height for touch).
- `.nav-menu > .nav-summary::after`: chevron that rotates 45deg to 225deg on open.
- `.nav-panel`: dropdown; display: none by default, opacity: 0, transform: translateY(-6px).
- `.nav-panel::before`: the invisible 16px hover bridge.
- `.nav-menu[data-open="true"] > .nav-panel`: display: block, opacity: 1, transform: translateY(0).
- Shared --ease (cubic-bezier(0.2, 0, 0, 1)) and 160ms duration.

## Mobile Drawer

Below ~768px, the same component switches behavior:
- A `.nav-toggle` button (hamburger) toggles a menuOpen boolean.
- The `<nav>` gets `.is-open` when menuOpen.
- `document.body` gets `menu-open` class to lock scroll.
- `.nav-panel` becomes position: static, width 100%, no shadow.
- Hover behavior is suppressed (touch path).

```css
@media (max-width: 768px) {
  .nav-toggle { display: inline-flex; }
  .primary-nav { display: none; }
  .primary-nav.is-open { display: flex; flex-direction: column; }
  .nav-menu > .nav-summary { width: 100%; justify-content: space-between; }
  .nav-panel {
    position: static;
    width: 100%;
    margin: 6px 0 10px;
    box-shadow: none;
    display: block;
    opacity: 1;
    transform: none;
  }
  .nav-menu:not([data-open="true"]) > .nav-panel { display: none; }
}

body.menu-open { overflow: hidden; }
```

## Common Mistakes

1. **Closing on pointerleave without delay**: menu disappears when cursor enters the gap. Always use the ~140ms timer.
2. **Nexustting the ::before bridge**: cursor "falls off" between trigger and panel.
3. **Using :hover only in CSS**: breaks keyboard and touch. State must be in React.
4. **Missing aria-expanded, aria-haspopup, role="menu", tabIndex management**: screen-reader users get nothing.
5. **Not skipping pointer events on pointerType === "touch"**: tapping a trigger opens and fires the click toggle, immediately closing again.
6. **Nexustting outside-click and Escape close**: menus stick open.
7. **Animating display directly**: toggle display and animate opacity plus transform instead.

## Verifying in a Real Browser

Synthetic event tools often do not trigger React's delegated pointerenter. Verify manually:

1. Click a trigger: data-open flips to "true," panel becomes visible, chevron rotates.
2. Tab through with keyboard: focus reaches trigger, opens menu; Tab continues through items; Escape closes.
3. Mouse-hover in a real browser: opens immediately; moving cursor into panel keeps it open; moving away closes after ~140ms.
4. Resize to below 768px and refresh: drawer mode activates, hover suppressed, tap toggles.
