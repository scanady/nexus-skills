# Prompt Patterns — Image Generation for Icons, Avatars, and Logos

## Structure

Every generation prompt follows this pattern:

```
Generate an image: [format] [subject] [style] [colors] [composition] [quality]
```

Each section should be explicit — don't rely on the model to infer defaults.

## Format Qualifiers

Always start with the format to anchor the output:

| Asset Type | Format Qualifier |
|-----------|-----------------|
| Icon | "A square 1:1 aspect ratio icon" |
| Avatar | "A square 1:1 aspect ratio profile avatar" |
| Logo | "A square 1:1 aspect ratio logo mark" |

## Style Keywords

### Flat / Minimal
Best for: icons that need to read at very small sizes.
```
flat design, minimal detail, solid colors, no gradients, clean shapes, bold silhouette
```

### Gradient / Glass
Best for: modern avatars and logos with depth.
```
subtle gradient, glassmorphism, soft glow, translucent layers, modern depth
```

### Outlined / Line Art
Best for: technical or developer-focused agents.
```
line art, thin strokes, outlined shapes, monochrome or duotone, technical drawing style
```

### 3D / Isometric
Best for: playful or product-focused branding.
```
3D rendered, isometric perspective, soft shadows, rounded surfaces, clay-like material
```

### Abstract Geometric
Best for: logos and brand marks.
```
abstract geometric, sharp angles, interlocking shapes, mathematical precision, bold composition
```

### Pixel Art
Best for: retro or gaming-adjacent agents.
```
pixel art, 8-bit style, crisp pixels, limited palette, retro gaming aesthetic
```

## Subject Patterns by Agent Type

Map the agent's function to a visual metaphor:

| Agent Domain | Symbol Ideas |
|-------------|-------------|
| Code / Development | Brackets `</>`, terminal cursor, gear + code |
| Security | Shield, lock, key, eye |
| Data / Analytics | Chart, graph, magnifying glass, database cylinder |
| AI / ML | Brain, neural network nodes, sparkle/star |
| Writing / Content | Pen, quill, speech bubble, document |
| Design / Creative | Palette, brush, eye, diamond |
| DevOps / Infra | Cloud, container, pipeline arrows, server stack |
| Communication | Speech bubbles, envelope, antenna, wave |
| Search / Research | Magnifying glass, compass, binoculars, telescope |
| Automation / Bot | Robot face, lightning bolt, loop arrows, cog |

## Color Strategy

### Two-Color Rule
For maximum icon readability, use exactly two colors plus optional background:
- **Primary**: The dominant brand or function color
- **Accent**: A contrasting highlight for key detail
- **Background**: Solid dark, light, or transparent

### Contrast Pairs That Work Well

| Primary | Accent | Mood |
|---------|--------|------|
| Deep blue (#1E3A5F) | Cyan (#00D4FF) | Professional, tech |
| Purple (#7C3AED) | Pink (#F472B6) | Creative, AI |
| Emerald (#059669) | Lime (#84CC16) | Growth, security |
| Orange (#EA580C) | Yellow (#FBBF24) | Energy, speed |
| Slate (#334155) | White (#FFFFFF) | Minimal, clean |
| Red (#DC2626) | Dark (#1F2937) | Alert, power |

### Background Recommendations

| Background Type | When to Use | Prompt Keyword |
|----------------|-------------|----------------|
| Transparent | Logos, icons for light+dark themes | "transparent background" |
| Dark solid (#0D1117 or #1A1A2E) | Dev tools, dark-mode-first products | "dark solid background" |
| White (#FFFFFF) | Documentation, light interfaces | "white background" |
| Gradient | Avatars, social media | "soft gradient background" |

## Refinement Prompts

When the first generation isn't right, use these targeted refinements:

### Simplify
```
Simplify the design: reduce to 2-3 main shapes, remove fine detail, make it bolder and more iconic. Keep the 1:1 square ratio.
```

### Change Style
```
Regenerate in [new style] style while keeping the same subject and colors. Square 1:1 aspect ratio.
```

### Adjust Colors
```
Keep the same composition but change colors to [new palette]. Maintain 1:1 square ratio.
```

### Improve Readability
```
Make the design read more clearly at small sizes: thicken lines, increase contrast between foreground and background, simplify shapes. 1:1 square ratio.
```

### Change Symbol
```
Replace the [current symbol] with [new symbol] while keeping the same style, colors, and composition. 1:1 square ratio.
```

## Anti-Patterns to Avoid in Prompts

- **Too many subjects**: "a brain AND a shield AND a lightning bolt AND gears" — pick one or two
- **Photorealistic for icons**: photorealism loses detail at small sizes — use flat or stylized
- **Text in icons**: text becomes unreadable below 128px — avoid unless it's a logo
- **Complex scenes**: icons are single objects, not landscapes or multi-character scenes
- **Vague style**: "make it cool" — always specify a concrete style keyword
- **Missing ratio**: forgetting "1:1 square" can produce landscape or portrait outputs
