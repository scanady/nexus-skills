#!/usr/bin/env python3
"""Inspect image assets for a layered scroll scene. Read-only: never edits a file.

Usage:
    python scripts/inspect-assets.py hero.png bg.jpg
    python scripts/inspect-assets.py assets/ --json

For each image it reports:
    * format, mode, pixel size, file weight
    * edge background class (see STATUS below)
    * hint: does the background probably need removing?
    * suggested depth level (0-5), advisory only
    * overrun against the per-depth edge and weight budget

STATUS values
    CLEAN          real transparent pixels along the edge
    OPAQUE_ALPHA   has an alpha channel, but every pixel is opaque
    SOLID_DARK     flat dark colour along the edge
    SOLID_LIGHT    flat light colour along the edge
    SOLID_MID      flat mid-tone colour along the edge
    COMPLEX        edge colour varies: scene, photo, or screenshot
    ERROR          file could not be read

The script finds the background. A person (or the agent, with the user)
judges whether it matters. See references/asset-preparation.md.

Exit codes: 0 ok, 1 no images found or any ERROR, 2 Pillow missing.
Requires Pillow for analysis (pip install Pillow). --help works without it.
"""

import argparse
import json
import os
import sys

IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".webp", ".avif", ".gif")

# depth level -> (max longest edge px, max weight KB). Mirrors scroll-performance.md.
BUDGET = {
    0: (1920, 150),
    1: (1000, 60),
    2: (400, 50),
    3: (1200, 120),
    4: (800, 40),
    5: (128, 10),
}

EDGE_SAMPLES = 96          # points walked around the image border
SOLID_SHARE = 0.9          # share of edge points near the median colour to call it "solid"
SOLID_TOLERANCE = 28       # max per-channel distance from the median colour
TRANSPARENT_SHARE = 0.9    # share of transparent edge points to call it "clean"
DARK_MAX, LIGHT_MIN = 45, 210

STATUS_ICON = {
    "CLEAN": "OK ", "OPAQUE_ALPHA": "!! ", "SOLID_DARK": "!! ", "SOLID_LIGHT": "!! ",
    "SOLID_MID": "?? ", "COMPLEX": "-- ", "ERROR": "XX ",
}


def edge_points(w, h, n=EDGE_SAMPLES):
    """Evenly spaced points walking the border clockwise."""
    perimeter = 2 * (w + h) - 4
    step = max(perimeter / n, 1)
    pts = []
    for i in range(n):
        d = int(i * step) % max(perimeter, 1)
        if d < w:
            pts.append((d, 0))
        elif d < w + h - 1:
            pts.append((w - 1, d - w + 1))
        elif d < 2 * w + h - 2:
            pts.append((w - 1 - (d - (w + h - 2)), h - 1))
        else:
            pts.append((0, h - 1 - (d - (2 * w + h - 3))))
    return [(min(max(x, 0), w - 1), min(max(y, 0), h - 1)) for x, y in pts]


def median(values):
    s = sorted(values)
    return s[len(s) // 2]


def luminance(rgb):
    r, g, b = rgb
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def classify_edge(img):
    """Return (status, edge_rgb or None, notes)."""
    w, h = img.size
    pts = edge_points(w, h)
    notes = []

    has_alpha = img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info)
    if has_alpha:
        rgba = img.convert("RGBA")
        px = rgba.load()
        transparent = sum(1 for x, y in pts if px[x, y][3] < 16)
        if transparent / len(pts) >= TRANSPARENT_SHARE:
            return "CLEAN", None, ["Edge is transparent. Cutout is ready."]
        lo = rgba.getchannel("A").getextrema()[0]
        if lo == 255:
            notes.append("Alpha channel exists but every pixel is opaque. Cutout was never done.")
            status_if_flat = "OPAQUE_ALPHA"
        else:
            notes.append("Some transparency exists, but not along the edge. Check for halos or holes.")
            status_if_flat = None
        img = rgba.convert("RGB")
    else:
        status_if_flat = None
        img = img.convert("RGB")

    px = img.load()
    samples = [px[x, y] for x, y in pts]
    mid = tuple(median([s[c] for s in samples]) for c in range(3))
    near = sum(1 for s in samples if max(abs(s[c] - mid[c]) for c in range(3)) <= SOLID_TOLERANCE)

    if near / len(samples) < SOLID_SHARE:
        notes.append("Edge colour varies. Likely a scene, photo, artwork, or screenshot: the image IS the content.")
        return ("OPAQUE_ALPHA" if status_if_flat else "COMPLEX"), mid, notes

    lum = luminance(mid)
    if lum <= DARK_MAX:
        status, label = "SOLID_DARK", "flat dark"
    elif lum >= LIGHT_MIN:
        status, label = "SOLID_LIGHT", "flat light"
    else:
        status, label = "SOLID_MID", "flat mid-tone"
    notes.append(f"Edge is {label} (rgb{mid}). On a product shot this reads as a box on the page.")
    return (status_if_flat or status), mid, notes


def removal_hint(status):
    if status in ("SOLID_DARK", "SOLID_LIGHT", "OPAQUE_ALPHA"):
        return "likely"       # unless it is a screenshot, artwork, or deliberate panel
    if status == "SOLID_MID":
        return "ambiguous"    # branded panel or studio backdrop: needs context
    if status == "COMPLEX":
        return "unlikely"
    return "no"


def suggest_depth(status, w, h):
    """Rough advice from size and cutout state. The agent decides from the story role."""
    edge = max(w, h)
    if status == "COMPLEX" and edge >= 1400:
        return 0, "Large scene-like image: background fill (depth 0)."
    if edge <= 160:
        return 5, "Tiny asset: particle or accent (depth 5)."
    if edge <= 450:
        return 2, "Small asset: mid decoration or companion (depth 2)."
    if status == "CLEAN" or status in ("SOLID_DARK", "SOLID_LIGHT", "OPAQUE_ALPHA"):
        return 3, "Large object: hero candidate (depth 3)."
    return 3, "Large image: hero or UI visual, confirm role."


def inspect(path):
    try:
        from PIL import Image
    except ImportError:
        print("Pillow is not installed. Run: pip install Pillow", file=sys.stderr)
        sys.exit(2)

    r = {
        "file": path, "name": os.path.basename(path), "status": None, "format": None, "mode": None,
        "width": None, "height": None, "weight_kb": None, "edge_rgb": None,
        "removal": None, "depth_hint": None, "over_budget": [], "notes": [],
    }
    try:
        r["weight_kb"] = round(os.path.getsize(path) / 1024, 1)
        with Image.open(path) as img:
            img.load()
            r["format"], r["mode"] = img.format, img.mode
            r["width"], r["height"] = img.size
            status, edge, notes = classify_edge(img)
    except Exception as exc:  # unreadable, truncated, unsupported codec
        r["status"] = "ERROR"
        r["notes"].append(f"Could not read file: {exc}")
        return r

    r["status"], r["edge_rgb"], r["removal"] = status, edge, removal_hint(status)
    r["notes"].extend(notes)

    if r["format"] == "JPEG" and r["removal"] in ("likely", "ambiguous"):
        r["notes"].append("JPEG cannot hold transparency. A cutout needs a PNG or WebP from the user, or an approved CSS blend.")

    depth, why = suggest_depth(status, r["width"], r["height"])
    r["depth_hint"] = {"level": depth, "why": why}

    max_edge, max_kb = BUDGET[depth]
    if max(r["width"], r["height"]) > max_edge:
        r["over_budget"].append(f"edge {max(r['width'], r['height'])}px > {max_edge}px for depth {depth}")
    if r["weight_kb"] > max_kb:
        r["over_budget"].append(f"weight {r['weight_kb']}KB > {max_kb}KB for depth {depth}")
    return r


def collect(paths):
    found, missing = [], []
    for p in paths:
        if os.path.isdir(p):
            for name in sorted(os.listdir(p)):
                if name.lower().endswith(IMAGE_EXTS):
                    found.append(os.path.join(p, name))
        elif os.path.isfile(p):
            found.append(p)
        else:
            missing.append(p)
    return found, missing


def print_report(results):
    line = "-" * 60
    print(f"\nAsset inspection ({len(results)} file{'s' if len(results) != 1 else ''})\n{line}")
    for r in results:
        print(f"\n{STATUS_ICON.get(r['status'], '?? ')}{r['name']}")
        if r["status"] == "ERROR":
            for n in r["notes"]:
                print(f"    {n}")
            continue
        print(f"    {r['format']} {r['mode']}  {r['width']}x{r['height']}px  {r['weight_kb']}KB")
        print(f"    status:  {r['status']}   background removal: {r['removal']}")
        print(f"    depth:   {r['depth_hint']['level']}  ({r['depth_hint']['why']})")
        for o in r["over_budget"]:
            print(f"    budget:  {o}  -> resize or recompress")
        for n in r["notes"]:
            print(f"    note:    {n}")
    counts = {}
    for r in results:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    print(f"\n{line}\n" + "  ".join(f"{k}: {v}" for k, v in sorted(counts.items())))
    print("Next: judge float-or-fill for each flagged image, then tell the user.")
    print("See references/asset-preparation.md.\n")


def main():
    ap = argparse.ArgumentParser(description="Read-only inspection of images for layered scroll scenes.")
    ap.add_argument("paths", nargs="+", help="image files or folders")
    ap.add_argument("--json", action="store_true", help="print machine-readable JSON")
    args = ap.parse_args()

    files, missing = collect(args.paths)
    for m in missing:
        print(f"Not found: {m}", file=sys.stderr)
    if not files:
        print("No images found.", file=sys.stderr)
        sys.exit(1)

    results = [inspect(f) for f in files]
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print_report(results)
    sys.exit(1 if any(r["status"] == "ERROR" for r in results) else 0)


if __name__ == "__main__":
    main()
