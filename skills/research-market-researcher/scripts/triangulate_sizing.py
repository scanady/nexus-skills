#!/usr/bin/env python3
"""Triangulate a top-down and a bottom-up market size and explain any gap.

Usage:
    python3 triangulate_sizing.py --input sizing.json [--format md|json] [--tolerance 1.3]

Each method is three multiplicative chains: tam, sam, som.
    TAM = product(tam factors); SAM = TAM * product(sam factors); SOM = SAM * product(som factors)
A factor is {"name", "value", "source", "low"?, "high"?}. low/high give the band.
See assets/sizing-sample.json.

Divergence is the ratio larger / smaller, so it reads the same in both directions.
The script never averages the two methods. On failure it ranks the inputs that
could close the TAM gap inside their own stated range.

Exit code: 0 triangulated at every level, 1 divergence over tolerance at any level.
"""
import argparse
import json
import math
import sys

LEVELS = ("tam", "sam", "som")
# Ratio larger/smaller allowed before triangulation fails, by market profile.
TOLERANCE = {"b2b-saas": 1.3, "enterprise": 1.25, "consumer": 1.4,
             "marketplace": 1.4, "hardware": 1.3, "services": 1.35}


def product(values):
    return math.prod(values) if values else 1.0


def chain(method):
    """Return point, low, and high values for TAM, SAM, SOM of one method."""
    out, point, low, high = {}, 1.0, 1.0, 1.0
    for level in LEVELS:
        factors = method.get(level, [])
        if level == "tam" and not factors:
            sys.exit("error: every method needs at least one tam factor")
        point *= product([f["value"] for f in factors])
        low *= product([f.get("low", f["value"]) for f in factors])
        high *= product([f.get("high", f["value"]) for f in factors])
        out[level] = {"point": point, "low": low, "high": high}
    return out


def ratio(a, b):
    if a <= 0 or b <= 0:
        return float("inf")
    return max(a, b) / min(a, b)


def levers(spec, td_tam, bu_tam):
    """Inputs that could close the TAM gap alone while staying inside their range."""
    gap = td_tam / bu_tam  # >1 means top-down is larger
    out = []
    for method, needed in (("top_down", 1 / gap), ("bottom_up", gap)):
        for f in spec[method]["tam"]:
            target = f["value"] * needed
            low, high = f.get("low", f["value"]), f.get("high", f["value"])
            beyond = 0.0 if low <= target <= high else (target / high - 1 if target > high else 1 - target / low)
            out.append({"method": method, "input": f["name"], "current": f["value"],
                        "value_to_close_gap": target, "beyond_range_pct": round(beyond * 100),
                        "sourced": bool(f.get("source"))})
    # Inside its range first, then unsourced (weakest evidence), then the smallest stretch.
    return sorted(out, key=lambda x: (x["beyond_range_pct"] > 0, x["sourced"], x["beyond_range_pct"]))


def unsourced(spec):
    return [f"{m}.{lvl}.{f['name']}" for m in ("top_down", "bottom_up")
            for lvl in LEVELS for f in spec[m].get(lvl, []) if not f.get("source")]


def analyze(spec, tolerance):
    td, bu = chain(spec["top_down"]), chain(spec["bottom_up"])
    levels = {}
    for level in LEVELS:
        r = ratio(td[level]["point"], bu[level]["point"])
        overlap = td[level]["low"] <= bu[level]["high"] and bu[level]["low"] <= td[level]["high"]
        levels[level] = {"top_down": td[level], "bottom_up": bu[level], "ratio": round(r, 2),
                         "within_tolerance": r <= tolerance, "bands_overlap": overlap}
    ok = all(v["within_tolerance"] for v in levels.values())
    return {
        "market": spec.get("market", "unnamed market"),
        "currency": spec.get("currency", "USD"),
        "tolerance_ratio": tolerance,
        "verdict": "triangulated" if ok else "failed",
        "levels": levels,
        "levers": [] if levels["tam"]["within_tolerance"] else levers(spec, td["tam"]["point"], bu["tam"]["point"]),
        "unsourced_inputs": unsourced(spec),
    }


def sig2(x):
    """Two significant figures: the inputs do not support more."""
    if x == 0 or math.isinf(x):
        return str(x)
    for unit, size in (("T", 1e12), ("B", 1e9), ("M", 1e6), ("K", 1e3)):
        if abs(x) >= size:
            return f"{float(f'{x / size:.2g}'):g}{unit}"
    return f"{float(f'{x:.2g}'):g}"


def render_markdown(r):
    c = r["currency"]
    lines = [f"# Sizing triangulation: {r['market']}", "",
             f"Verdict: **{r['verdict']}** (tolerance: larger/smaller <= {r['tolerance_ratio']})", "",
             "| Level | Top-down (low-high) | Bottom-up (low-high) | Ratio | Bands overlap |",
             "|---|---|---|---|---|"]
    for level, v in r["levels"].items():
        td, bu = v["top_down"], v["bottom_up"]
        mark = "" if v["within_tolerance"] else " FAIL"
        lines.append(f"| {level.upper()} | {c} {sig2(td['point'])} ({sig2(td['low'])}-{sig2(td['high'])}) "
                     f"| {c} {sig2(bu['point'])} ({sig2(bu['low'])}-{sig2(bu['high'])}) "
                     f"| {v['ratio']}x{mark} | {'yes' if v['bands_overlap'] else 'no'} |")
    tam = r["levels"]["tam"]
    if not tam["within_tolerance"] and tam["bands_overlap"]:
        lines += ["", "The TAM bands overlap, so the gap may sit inside the stated uncertainty. "
                      "Narrow the widest ranges with better sources before you trust either point."]
    if r["levers"]:
        lines += ["", "## Inputs that could explain the TAM gap", "",
                  "Each line is the value that closes the gap alone. Investigate from the top. "
                  "Do not change a value until a source supports the new value.", ""]
        for lv in r["levers"]:
            tag = "inside stated range" if lv["beyond_range_pct"] == 0 else f"{lv['beyond_range_pct']}% beyond stated range"
            src = "" if lv["sourced"] else ", UNSOURCED"
            lines.append(f"- {lv['method']}.{lv['input']}: {sig2(lv['current'])} -> {sig2(lv['value_to_close_gap'])} ({tag}{src})")
    if r["unsourced_inputs"]:
        lines += ["", "## Unsourced inputs", ""] + [f"- {u}" for u in r["unsourced_inputs"]]
    lines += ["", "Quote a range, not a point. State both methods and their inputs with the number."]
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", required=True)
    ap.add_argument("--format", choices=["md", "json"], default="md")
    ap.add_argument("--tolerance", type=float, help="override the profile tolerance ratio (for example 1.3)")
    args = ap.parse_args()
    with open(args.input, encoding="utf-8") as f:
        spec = json.load(f)
    profile = spec.get("profile", "b2b-saas")
    if profile not in TOLERANCE:
        sys.exit(f"error: unknown profile {profile}. Valid: {', '.join(TOLERANCE)}")
    result = analyze(spec, args.tolerance or TOLERANCE[profile])
    sys.stdout.write(json.dumps(result, indent=2) + "\n" if args.format == "json" else render_markdown(result))
    sys.exit(0 if result["verdict"] == "triangulated" else 1)


if __name__ == "__main__":
    main()
