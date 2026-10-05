#!/usr/bin/env python3
"""Confidence interval for one proportion or one mean, from summary numbers.

Standard library only.
  proportion : Wilson score interval. Stays inside 0..1 and holds up at small n
               or rates near 0 or 1, where the textbook p +/- z*se interval fails.
  mean       : t-based interval from n, mean, and sample standard deviation.

Examples:
  confidence_interval.py proportion --n 1200 --x 96
  confidence_interval.py mean --n 800 --mean 42.3 --sd 18.1 --confidence 0.99
"""

import argparse
import json
import math
import sys

from statlib import t_critical, z_critical


def fail(message: str):
    sys.exit(f"error: {message}")


def wilson(n, x, confidence):
    if n <= 0 or not 0 <= x <= n:
        fail("need n > 0 and 0 <= x <= n")
    p = x / n
    z = z_critical(1 - confidence)
    z2 = z * z
    center = (p + z2 / (2 * n)) / (1 + z2 / n)
    margin = z / (1 + z2 / n) * math.sqrt(p * (1 - p) / n + z2 / (4 * n * n))
    return {"metric": "proportion", "method": "Wilson score", "n": n, "x": x,
            "estimate": p, "confidence": confidence,
            "lower": max(0.0, center - margin), "upper": min(1.0, center + margin)}


def mean_ci(n, mean, sd, confidence):
    if n < 2 or sd < 0:
        fail("need n >= 2 and a non-negative --sd")
    se = sd / math.sqrt(n)
    margin = t_critical(1 - confidence, n - 1) * se
    return {"metric": "mean", "method": f"t interval, df={n - 1}", "n": n,
            "estimate": mean, "sd": sd, "standard_error": se, "confidence": confidence,
            "lower": mean - margin, "upper": mean + margin}


def render(r):
    half = (r["upper"] - r["lower"]) / 2
    lines = [f"{r['metric']} ({r['method']})",
             f"  estimate: {r['estimate']:.6g}  (n={r['n']})",
             f"  {r['confidence']:.0%} CI: [{r['lower']:.6g}, {r['upper']:.6g}]  (+/- {half:.6g})"]
    if r["estimate"]:
        rel = half / abs(r["estimate"])
        lines.append(f"  half-width is {rel:.1%} of the estimate" +
                     ("; wide, so state the range, not the point." if rel > 0.2 else "."))
    if r["metric"] == "mean" and r["n"] < 30:
        lines.append("  WARNING: n < 30. The interval assumes a roughly normal metric; check the shape.")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("kind", choices=["proportion", "mean"])
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--x", type=int, help="successes (proportion)")
    parser.add_argument("--mean", type=float)
    parser.add_argument("--sd", type=float, help="sample standard deviation (mean)")
    parser.add_argument("--confidence", type=float, default=0.95)
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()
    if not 0 < args.confidence < 1:
        fail("--confidence must be between 0 and 1")
    if args.kind == "proportion":
        if args.x is None:
            fail("proportion needs --x")
        result = wilson(args.n, args.x, args.confidence)
    else:
        if args.mean is None or args.sd is None:
            fail("mean needs --mean and --sd")
        result = mean_ci(args.n, args.mean, args.sd, args.confidence)
    print(json.dumps(result, indent=2) if args.format == "json" else render(result))


if __name__ == "__main__":
    main()
