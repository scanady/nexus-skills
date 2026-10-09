#!/usr/bin/env python3
"""Inspect image assets for a layered scroll scene. Read-only: never edits a file.

Usage:
    python scripts/inspect-assets.py hero.png bg.jpg
    python scripts/inspect-assets.py assets/ --json
    python scripts/inspect-assets.py path/to/project            # folder with project.json
    python scripts/inspect-assets.py path/to/project/shared/assets.json

For each image it reports:
    * format, mode, pixel size, file weight
    * edge background class (see STATUS below)
    * hint: does the background probably need removing?
    * suggested depth level (0-5), advisory only
    * overrun against the per-depth edge and weight budget

Project folders: given a folder that holds project.json or shared/assets.json,
or the assets.json file itself, it inspects every image listed in
shared/assets.json, plus any image in shared/images/ or shared/screenshots/
that the list misses. Each result gains a "shared" block (kind, by, source,
text, background, rights, note) and "flags" for the user:
    background transparent  float candidate; flagged if the pixels disagree
    background green        chroma key still to remove: needs keying, flagged
    background opaque       fill, unless the user wants it to float
    text true               readable words: keep it readable, real alt text
    rights third-party      flagged: confirm before publishing
    not in assets.json      flagged: source and rights unknown

STATUS values
    CLEAN          real transparent pixels along the edge
    OPAQUE_ALPHA   has an alpha channel, but every pixel is opaque
    SOLID_DARK     flat dark colour along the edge
    SOLID_LIGHT    flat light colour along the edge
    SOLID_MID      flat mid-tone colour along the edge
    COMPLEX        edge colour varies: scene, photo, or screenshot
    ERROR          file could not be read
    MISSING        listed in shared/assets.json, but the file is not there

The script finds the background. A person (or the agent, with the user)
judges whether it matters. See references/asset-preparation.md.

Exit codes: 0 ok, 1 no images found or any ERROR, 2 Pillow missing.
MISSING does not fail the run: a missing shared file is never an error.
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
    "SOLID_MID": "?? ", "COMPLEX": "-- ", "ERROR": "XX ", "MISSING": "XX ",
}

MANIFEST = ("shared", "assets.json")
SHARED_IMAGE_DIRS = (("shared", "images"), ("shared", "screenshots"))
SHARED_FIELDS = ("kind", "by", "source", "text", "background", "rights", "note")


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


def inspect(path, entry=None):
    """Pixel checks for one image. `entry` is its shared/assets.json entry:
    None outside a project, {} for an image in shared/ that the list misses."""
    try:
        from PIL import Image
    except ImportError:
        print("Pillow is not installed. Run: pip install Pillow", file=sys.stderr)
        sys.exit(2)

    name = entry.get("file") if entry else None
    r = {
        "file": path, "name": name or os.path.basename(path), "status": None, "format": None, "mode": None,
        "width": None, "height": None, "weight_kb": None, "edge_rgb": None,
        "removal": None, "depth_hint": None, "over_budget": [], "notes": [],
    }
    if entry is not None:
        r["shared"], r["flags"] = {k: entry[k] for k in SHARED_FIELDS if k in entry}, []
        if not os.path.isfile(path):
            r["status"] = "MISSING"
            r["notes"].append("Listed in shared/assets.json, but the file is not there. Skip it.")
            return r
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

    if entry is not None:
        apply_shared(r, entry)
    return r


def apply_shared(r, entry):
    """Merge what shared/assets.json says with the pixel checks."""
    if not entry:
        r["flags"].append("In shared/ but not listed in shared/assets.json: source and rights unknown. Ask the user.")
        return
    bg = entry.get("background")
    if bg == "transparent":
        r["notes"].append("assets.json: transparent background. Float candidate.")
        if r["status"] != "CLEAN":
            r["flags"].append(f"assets.json says transparent, but the edge is {r['status']}. Check the file before floating it.")
    elif bg == "green":
        r["removal"] = "needs keying"
        r["flags"].append("assets.json: green chroma-key background still to remove. Needs keying before it can float. Ask the user.")
    elif bg == "opaque":
        if r["removal"] in ("likely", "ambiguous"):
            r["removal"] = "unlikely"
        r["notes"].append("assets.json: opaque background. Use it as a fill unless the user wants it to float.")
    if entry.get("text") is True:
        r["notes"].append("assets.json: shows readable words. Keep it at a readable size, give it real alt text, keep it off fast or blurred layers.")
    if entry.get("rights") == "third-party":
        r["flags"].append("assets.json: third-party rights. Confirm the user may publish it before it ships.")


def project_root(path):
    """Project folder when `path` is one (project.json or shared/assets.json inside) or is an assets.json file."""
    if os.path.isdir(path) and (
        os.path.isfile(os.path.join(path, "project.json")) or os.path.isfile(os.path.join(path, *MANIFEST))
    ):
        return path
    if os.path.isfile(path) and os.path.basename(path) == "assets.json":
        return os.path.normpath(os.path.join(os.path.dirname(path), os.pardir))
    return None


def load_manifest(root):
    """Return (entries, problem). No assets.json is not a problem."""
    path = os.path.join(root, *MANIFEST)
    if not os.path.isfile(path):
        return [], None
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError) as exc:
        return [], f"Could not read {path}: {exc}"
    assets = data.get("assets") if isinstance(data, dict) else None
    if not isinstance(assets, list):
        return [], f"{path} has no \"assets\" list."
    return [a for a in assets if isinstance(a, dict) and isinstance(a.get("file"), str)], None


def collect_project(root):
    """Return ([(path, entry)], warnings): listed images first, then unlisted ones in shared/."""
    entries, problem = load_manifest(root)
    items, warnings, listed = [], [problem] if problem else [], set()
    for e in entries:
        path = os.path.normpath(os.path.join(root, *e["file"].split("/")))
        listed.add(path)
        if e["file"].lower().endswith(IMAGE_EXTS):
            items.append((path, e))
        else:
            warnings.append(f"Skipped (not an image): {e['file']}")
    for parts in SHARED_IMAGE_DIRS:
        folder = os.path.join(root, *parts)
        if not os.path.isdir(folder):
            continue
        for name in sorted(os.listdir(folder)):
            path = os.path.normpath(os.path.join(folder, name))
            if name.lower().endswith(IMAGE_EXTS) and path not in listed:
                items.append((path, {}))
    return items, warnings


def collect(paths):
    """Return ([(path, entry)], warnings) for plain files, folders, and project folders."""
    items, warnings = [], []
    for p in paths:
        root = project_root(p)
        if root is not None:
            found, warns = collect_project(root)
            items.extend(found)
            warnings.extend(warns)
        elif os.path.isdir(p):
            for name in sorted(os.listdir(p)):
                if name.lower().endswith(IMAGE_EXTS):
                    items.append((os.path.join(p, name), None))
        elif os.path.isfile(p):
            items.append((p, None))
        else:
            warnings.append(f"Not found: {p}")
    return items, warnings


def print_report(results):
    line = "-" * 60
    print(f"\nAsset inspection ({len(results)} file{'s' if len(results) != 1 else ''})\n{line}")
    for r in results:
        print(f"\n{STATUS_ICON.get(r['status'], '?? ')}{r['name']}")
        if "shared" in r:
            shared = "  ".join(f"{k}={r['shared'][k]}" for k in SHARED_FIELDS if k in r["shared"] and k != "note")
            print(f"    shared:  {shared or 'not listed in shared/assets.json'}")
            if r["shared"].get("note"):
                print(f"    about:   {r['shared']['note']}")
        if r["status"] in ("ERROR", "MISSING"):
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
        for f in r.get("flags", []):
            print(f"    FLAG:    {f}")
    counts = {}
    for r in results:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    flagged = sum(1 for r in results if r.get("flags"))
    summary = "  ".join(f"{k}: {v}" for k, v in sorted(counts.items()))
    print(f"\n{line}\n{summary}" + (f"  flagged: {flagged}" if flagged else ""))
    print("Next: judge float-or-fill for each flagged image, then tell the user.")
    print("See references/asset-preparation.md.\n")


def main():
    ap = argparse.ArgumentParser(description="Read-only inspection of images for layered scroll scenes.")
    ap.add_argument("paths", nargs="+", help="image files, folders, a project folder, or a shared/assets.json file")
    ap.add_argument("--json", action="store_true", help="print machine-readable JSON")
    args = ap.parse_args()

    items, warnings = collect(args.paths)
    for w in warnings:
        print(w, file=sys.stderr)
    if not items:
        print("No images found.", file=sys.stderr)
        sys.exit(1)

    results = [inspect(path, entry) for path, entry in items]
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print_report(results)
    sys.exit(1 if any(r["status"] == "ERROR" for r in results) else 0)


if __name__ == "__main__":
    main()
