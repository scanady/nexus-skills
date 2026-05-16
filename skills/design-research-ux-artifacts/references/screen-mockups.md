# Screen Mockups

> Text-based wireframes that describe layout structure. These bridge UX specs and visual design.

---

## Inputs

- **Source screen spec**:
- **Viewport priorities**:
- **Responsive constraints**:

---

## <Screen Name>

### Viewport: Desktop (1280 px)

```
+-------------------------------------------------+
| [Logo]          Nav Item | Nav Item    [Avatar] |  <- Header (64 px)
+-------------------------------------------------+
|                                                 |
|  +-----------------------------------------+    |
|  | H1: Page Title                          |    |
|  | Subtitle / breadcrumb                   |    |
|  +-----------------------------------------+    |
|                                                 |
|  +-------------+  +-------------+  +--------+   |
|  | Card 1      |  | Card 2      |  | Card 3 |   |  <- Content grid
|  | [Image]     |  | [Image]     |  | [Image]|   |     (3 col, 24 px gutter)
|  | Label       |  | Label       |  | Label  |   |
|  +-------------+  +-------------+  +--------+   |
|                                                 |
|  [ Primary Button ]  [ Secondary Link ]         |  <- Actions
|                                                 |
+-------------------------------------------------+
| Footer: Links | Copyright                       |
+-------------------------------------------------+
```

### Annotations

Annotations describe the layout, structure, and interaction intent of elements in the wireframe. When a design token file exists for the project, visual properties (color, typography, spacing, radius) should cite token paths using `{path.to.token}` notation.

Examples:
- "Primary button: `backgroundColor: {colors.primary}`, `textColor: {colors.on-primary}`, `rounded: {rounded.md}`"
- "Card background: `{colors.surface}`, padding `{spacing.md}` all sides"
- "Section heading: `{typography.headline-md}`, color `{colors.on-surface}`"

1.
2.
3.

### Viewport: Mobile (375 px)

```
+---------------------+
| [=]  Logo  [Avatar] |  <- Header
+---------------------+
|                     |
| H1: Page Title      |
| Subtitle            |
|                     |
| +-----------------+ |
| | Card 1          | |
| | [Image]         | |
| | Label           | |
| +-----------------+ |
|                     |
| +-----------------+ |
| | Card 2          | |
| | [Image]         | |
| | Label           | |
| +-----------------+ |
|                     |
| [ Primary Button ]  |
|                     |
+---------------------+
| [Home] [Find] [Set] |
+---------------------+
```

---

## Responsive Breakpoints

| Breakpoint | Width | Layout Changes |
|------------|-------|----------------|
| Mobile | < 768 px | Single column, bottom nav, hamburger menu |
| Tablet | 768-1024 px | 2-column grid, collapsible sidebar |
| Desktop | > 1024 px | Full 3-column layout, persistent nav |

---

## <Screen Name>

### Viewport: Desktop

```
+-------------------------------------------------+
|                                                 |
|                                                 |
|                                                 |
+-------------------------------------------------+
```

### Annotations
1.