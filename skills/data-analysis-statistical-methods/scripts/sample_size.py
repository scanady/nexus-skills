#!/usr/bin/env python3
"""Sample size, minimum detectable effect, and test duration for two-group tests.

Standard library only. Two directions:
  size  : given baseline and the effect you care about, how many per group?
  mde   : given the n you have, what is the smallest effect you could detect?
          Run this after a null result to say what the test could not see.

Examples:
  sample_size.py size proportion --baseline 0.05 --mde 0.20            # +20% relative
  sample_size.py size proportion --baseline 0.05 --mde-abs 0.01 --daily-traffic 4000
  sample_size.py size mean --baseline-mean 42.3 --baseline-sd 18.1 --mde 0.10
  sample_size.py size proportion --baseline 0.05 --mde 0.20 --tests 4  # Bonferroni
  sample_size.py mde proportion --baseline 0.05 --n 3000
"""

import argparse
import json
import math
import sys

from statlib import normal_ppf, z_critical


def fail(message: str):
    sys.exit(f"error: {message}")


def n_proportion(p1, p2, alpha, power):
    za, zb = z_critical(alpha), normal_ppf(power)
    return math.ceil((za + zb) ** 2 * (p1 * (1 - p1) + p2 * (1 - p2)) / (p2 - p1) ** 2)


def n_mean(sd, delta, alpha, power):
    za, zb = z_critical(alpha), normal_ppf(power)
    return math.ceil(2 * sd ** 2 * (za + zb) ** 2 / delta ** 2)


def mde_proportion(p1, n, alpha, power):
    """Smallest absolute lift detectable with n per group, found by bisection."""
    lo, hi = 1e-9, 1 - p1 - 1e-9
    if hi <= lo or n_proportion(p1, p1 + hi, alpha, power) > n:
        return None
    for _ in range(100):
        mid = (lo + hi) / 2
        if n_proportion(p1, p1 + mid, alpha, power) > n:
            lo = mid
        else:
            hi = mid
    return hi


def mde_mean(sd, n, alpha, power):
    return (z_critical(alpha) + normal_ppf(power)) * sd * math.sqrt(2 / n)


def days_needed(n_per_group, groups, daily_traffic):
    return math.ceil(n_per_group * groups / daily_traffic)


def size_result(args, alpha):
    if args.kind == "proportion":
        if args.baseline is None or not 0 < args.baseline < 1:
            fail("--baseline must be a rate between 0 and 1")
        delta = args.mde_abs if args.mde_abs is not None else args.baseline * args.mde
        p2 = args.baseline + delta
        if not 0 < p2 < 1:
            fail(f"baseline plus effect gives a rate of {p2:.4f}; it must stay between 0 and 1")
        rows = {f"{pw:.0%}": n_proportion(args.baseline, p2, alpha, pw)
                for pw in (0.7, 0.8, 0.9, 0.95)}
        n = n_proportion(args.baseline, p2, alpha, args.power)
        detail = {"baseline": args.baseline, "target": p2, "absolute_effect": delta}
    else:
        if args.baseline_mean is None or args.baseline_sd is None or args.baseline_sd <= 0:
            fail("--baseline-mean and a positive --baseline-sd are required")
        delta = args.mde_abs if args.mde_abs is not None else args.baseline_mean * args.mde
        if delta == 0:
            fail("the effect is zero; set a non-zero --mde or --mde-abs")
        rows = {f"{pw:.0%}": n_mean(args.baseline_sd, abs(delta), alpha, pw)
                for pw in (0.7, 0.8, 0.9, 0.95)}
        n = n_mean(args.baseline_sd, abs(delta), alpha, args.power)
        detail = {"baseline_mean": args.baseline_mean, "baseline_sd": args.baseline_sd,
                  "absolute_effect": delta}
    result = {"mode": "size", "metric": args.kind, **detail, "alpha": alpha,
              "power": args.power, "n_per_group": n, "n_total": n * args.groups,
              "n_per_group_by_power": rows}
    if args.daily_traffic:
        result["days_needed"] = days_needed(n, args.groups, args.daily_traffic)
    return result


def mde_result(args, alpha):
    if args.kind == "proportion":
        if args.baseline is None or not 0 < args.baseline < 1:
            fail("--baseline must be a rate between 0 and 1")
        delta = mde_proportion(args.baseline, args.n, alpha, args.power)
        if delta is None:
            fail("no lift below 100% is detectable with this n")
        detail = {"baseline": args.baseline, "detectable_absolute_lift": delta,
                  "detectable_relative_lift": delta / args.baseline}
    else:
        if args.baseline_mean is None or args.baseline_sd is None or args.baseline_sd <= 0:
            fail("--baseline-mean and a positive --baseline-sd are required")
        delta = mde_mean(args.baseline_sd, args.n, alpha, args.power)
        detail = {"baseline_mean": args.baseline_mean, "baseline_sd": args.baseline_sd,
                  "detectable_absolute_difference": delta,
                  "detectable_relative_difference": delta / abs(args.baseline_mean)
                  if args.baseline_mean else None}
    return {"mode": "mde", "metric": args.kind, **detail, "alpha": alpha,
            "power": args.power, "n_per_group": args.n}


def render(result):
    lines = [f"{result['mode']} / {result['metric']}  (alpha={result['alpha']:.4g}, power={result['power']:.0%})"]
    for key, value in result.items():
        if key in ("mode", "metric", "alpha", "power", "n_per_group_by_power"):
            continue
        lines.append(f"  {key}: {value:.6g}" if isinstance(value, float) else f"  {key}: {value}")
    if "n_per_group_by_power" in result:
        lines.append("  n per group by power: " +
                     ", ".join(f"{k}={v:,}" for k, v in result["n_per_group_by_power"].items()))
    if result["mode"] == "size":
        lines.append("  Lock the stopping rule at this n before launch. Do not stop early on a good-looking p-value.")
    else:
        lines.append("  A null result at this n rules out only effects larger than the value above.")
    return "\n".join(lines)


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="mode", required=True)
    for mode in ("size", "mde"):
        p = sub.add_parser(mode)
        p.add_argument("kind", choices=["proportion", "mean"])
        p.add_argument("--alpha", type=float, default=0.05)
        p.add_argument("--power", type=float, default=0.80)
        p.add_argument("--tests", type=int, default=1,
                       help="number of comparisons; alpha is divided by this (Bonferroni)")
        p.add_argument("--baseline", type=float, help="control rate, e.g. 0.05")
        p.add_argument("--baseline-mean", type=float)
        p.add_argument("--baseline-sd", type=float)
        p.add_argument("--format", choices=["text", "json"], default="text")
        if mode == "size":
            p.add_argument("--mde", type=float, default=None,
                           help="relative effect, e.g. 0.20 for +20%%")
            p.add_argument("--mde-abs", type=float, default=None, help="absolute effect")
            p.add_argument("--groups", type=int, default=2, help="groups including control")
            p.add_argument("--daily-traffic", type=int, help="eligible units per day, all groups")
        else:
            p.add_argument("--n", type=int, required=True, help="observations per group")
    return parser


def main():
    args = build_parser().parse_args()
    if not 0 < args.alpha < 1 or not 0.5 <= args.power < 1:
        fail("--alpha must be in (0,1) and --power in [0.5,1)")
    if args.tests < 1:
        fail("--tests must be at least 1")
    alpha = args.alpha / args.tests
    if args.mode == "size":
        if (args.mde is None) == (args.mde_abs is None):
            fail("give exactly one of --mde or --mde-abs")
        result = size_result(args, alpha)
    else:
        if args.n < 2:
            fail("--n must be at least 2")
        result = mde_result(args, alpha)
    print(json.dumps(result, indent=2) if args.format == "json" else render(result))


if __name__ == "__main__":
    main()
