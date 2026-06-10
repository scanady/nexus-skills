# Sizing Guide — Icons, Avatars, and Logos

## Core Principle

All assets are **1:1 aspect ratio** (square). Generate at the largest target size and downscale — never upscale.

## Size Specifications by Asset Type

### Icons

Icons are used in app UIs, system trays, favicons, and navigation. Must remain legible at the smallest sizes.

| Size | Use Case | Notes |
|------|----------|-------|
| 512×512 px | App store, high-DPI displays | Primary generation size |
| 256×256 px | Desktop app icons, documentation | Standard display |
| 128×128 px | Web app icons, toolbars | Common web size |
| 64×64 px | Navigation, sidebar icons | Detail reduction needed |
| 32×32 px | Favicon, status bar | Must be recognizable as silhouette |
| 16×16 px | Browser tab favicon | Optional — very few details survive |

**Generation target:** 512×512 px

### Avatars

Avatars represent the agent in chat interfaces, profile cards, and team directories.

| Size | Use Case | Notes |
|------|----------|-------|
| 512×512 px | Profile page, hero display | Primary generation size |
| 256×256 px | Chat interface, profile card | Standard display |
| 128×128 px | Comment sections, mentions | Common compact view |
| 64×64 px | Chat list, notification | Must show character clearly |
| 48×48 px | Inline mentions, small lists | Minimum recommended |

**Generation target:** 512×512 px

### Logos

Logos are used for branding, documentation headers, social media, and marketing materials.

| Size | Use Case | Notes |
|------|----------|-------|
| 1024×1024 px | Print, high-res marketing | Primary generation size |
| 512×512 px | Social media profile, documentation | Standard digital |
| 256×256 px | Email signatures, footers | Compact branding |
| 128×128 px | Watermarks, small placements | Minimum for logos |

**Generation target:** 1024×1024 px

## Resizing Strategy

1. **Generate** at the primary size listed above
2. **Downscale** using nearest-neighbor (pixel art) or bilinear (everything else) interpolation
3. **Verify** that the smallest target size is still recognizable
4. **Save** each size as a separate file: `{name}-{type}-{width}x{height}.png`

### File Naming Convention

```
{agent-name}-icon-512x512.png
{agent-name}-icon-256x256.png
{agent-name}-icon-128x128.png
{agent-name}-icon-64x64.png
{agent-name}-icon-32x32.png
{agent-name}-avatar-512x512.png
{agent-name}-avatar-256x256.png
{agent-name}-avatar-128x128.png
{agent-name}-logo-1024x1024.png
{agent-name}-logo-512x512.png
{agent-name}-logo-256x256.png
```

Use lowercase, hyphens for spaces. No special characters.

## Platform-Specific Guidance

| Platform | Recommended Icon Size | Format |
|----------|----------------------|--------|
| GitHub | 256×256 or 512×512 | PNG |
| Slack | 512×512 | PNG, JPG |
| Discord | 128×128 minimum | PNG, JPG, GIF |
| VS Code Extension | 128×128 | PNG |
| Web Favicon | 32×32, 16×16 | PNG, ICO |
| Apple Touch Icon | 180×180 | PNG |
| Android | 512×512 (adaptive) | PNG |
| Social Media (general) | 512×512 or 1024×1024 | PNG, JPG |
