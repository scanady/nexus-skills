# Motion & Animation

Animation as polish for a visual refactor: enough to make an interface feel responsive and oriented, without the sluggishness or chartjunk-in-motion that makes it feel worse. For designing a *specific* interaction's choreography end-to-end (trigger → rules → feedback → loops), defer to the design-ui-microinteractions skill; this file is the timing/easing/performance layer.

## Animate Only With a Reason

Valid: feedback (press confirmed), orientation (where did this come from/go), focus (draw the eye to a change), continuity (keep context across a state change), occasional delight. Invalid: "looks cool," matching competitors, animating every state change, or masking slow performance.

## Duration

The default is **~200ms**. Under ~100ms is imperceptible; over ~400ms feels sluggish.

| Type | Duration |
|------|----------|
| Micro-feedback (hover, press) | 100–150ms |
| Simple transitions (fade, slide) | 150–250ms |
| Complex (modal, nav) | 250–350ms |
| Entrances/reveals | 200–400ms |

Longer travel → slightly longer duration, not proportionally. Loading/progress indicators are the exception — they can run longer because they represent real waiting.

## Easing

Linear looks robotic. Match the curve to direction of travel:

| Easing | Use for |
|--------|---------|
| `ease-out` | entrances (modals, dropdowns, toasts appearing) — fast start, gentle stop |
| `ease-in` | exits (fade/slide out) — gentle start, quick leave |
| `ease-in-out` | on-screen movement (tab indicator, drawer) |
| `linear` | progress bars, opacity — mechanical on purpose |

Custom cubic-bezier adds personality (e.g. a slight overshoot `cubic-bezier(0.34, 1.56, 0.64, 1)`).

## Common Transitions

- **Modal enter**: `opacity 0→1`, `scale(0.95)→1`, 200ms ease-out. Exit faster, 150ms ease-in.
- **Dropdown**: `opacity` + `translateY(-8px)→0`, 150ms ease-out, toggle `pointer-events`.
- **Toast**: slide `translateX(100%)→0`, 300ms ease-out in / 200ms ease-in out.
- **Skeleton**: shimmer via an animated `background-position` gradient, ~1.5s loop.

## Loading States

| Indicator | Use when |
|-----------|----------|
| Spinner | short, unknown duration (button submit) |
| Progress bar | known progress, longer op (upload) — never run it backwards |
| Skeleton | loading structured content (feed) — match the real layout |
| Shimmer/pulse | refreshing existing content |

Delay spinners ~300–400ms so fast operations don't flash one. Hold layout size to prevent shift.

## Performance

Animate only **GPU-friendly** properties — `transform` and `opacity`. Avoid animating `width/height/top/left/margin/padding/font-size` (they trigger layout/reflow). Use `will-change` only on elements about to animate, then clear it. Stagger sequences by 0–50ms for cohesion; 100ms+ feels slow. Test on a low-end device or throttled CPU — smooth on a laptop can stutter on a budget phone.

## Accessibility

Always honor reduced motion:
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: .01ms !important;
    transition-duration: .01ms !important;
  }
}
```
Never convey information by motion alone — the state change must be visible when animation is off. Avoid flashing/strobing (seizure risk), heavy parallax (motion sickness), and autoplaying media.

## Ship Checklist
- Serves a purpose, not decoration
- Duration and easing fit the action
- Honors `prefers-reduced-motion`
- GPU-accelerated (`transform`/`opacity`)
- Interface still works with animation off
