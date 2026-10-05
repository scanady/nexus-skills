#!/usr/bin/env python3
"""Plan survey completes so every reported segment meets its own margin of error.

Usage:
    python3 segment_sample_planner.py --input survey.json [--format md|json]
    python3 segment_sample_planner.py --input survey.json --budget 600

Plan mode: n per segment = Cochran n0 = z^2 p(1-p) / e^2, then the finite-population
correction n = n0 / (1 + (n0 - 1) / N_segment), times the design effect.
Quota per segment = max(floor, proportional share of the overall n).
Invites = quota / expected response rate.

Budget mode (--budget N): split N completes by population share and report the
margin of error each segment can actually support.

Survey spec (see assets/survey-sample.json):
    population, confidence, margin_of_error, expected_proportion, response_rate,
    design_effect, segment_margin_of_error,
    segments: [{name, population, margin_of_error?, expected_proportion?}]
"""
import argparse
import json
import math
import sys
from statistics import NormalDist


def z_for(confidence):
    if not 0 < confidence < 1:
        sys.exit("error: confidence must be between 0 and 1, for example 0.95")
    return NormalDist().inv_cdf((1 + confidence) / 2)


def required_n(z, p, e, population, deff):
    n0 = z * z * p * (1 - p) / (e * e)
    n = n0 / (1 + (n0 - 1) / population) if population else n0
    return math.ceil(n * deff)


def achievable_moe(z, p, n, population, deff):
    if n <= 0:
        return None
    effective = n / deff
    fpc = (population - effective) / (population - 1) if population and population > 1 else 1.0
    return z * math.sqrt(p * (1 - p) / effective * max(fpc, 0))


def segment_defaults(spec, seg):
    return (seg.get("expected_proportion", spec.get("expected_proportion", 0.5)),
            seg.get("margin_of_error", spec.get("segment_margin_of_error", spec["margin_of_error"])))


def plan(spec):
    z = z_for(spec.get("confidence", 0.95))
    deff = spec.get("design_effect", 1.0)
    rr = spec.get("response_rate", 1.0)
    p = spec.get("expected_proportion", 0.5)
    total_pop = spec.get("population") or sum(s["population"] for s in spec.get("segments", [])) or None
    overall = required_n(z, p, spec["margin_of_error"], total_pop, deff)
    rows = []
    for seg in spec.get("segments", []):
        sp, se = segment_defaults(spec, seg)
        floor = required_n(z, sp, se, seg["population"], deff)
        proportional = math.ceil(overall * seg["population"] / total_pop)
        quota = min(max(floor, proportional), seg["population"])
        rows.append({"name": seg["name"], "population": seg["population"], "target_moe": se,
                     "floor": floor, "proportional": proportional, "quota": quota,
                     "invites": math.ceil(quota / rr),
                     "census_needed": floor >= seg["population"]})
    total = sum(r["quota"] for r in rows) if rows else overall
    for r in rows:
        share_pop = r["population"] / total_pop
        share_sample = r["quota"] / total
        r["weight"] = round(share_pop / share_sample, 3)  # post-stratification weight
    return {"mode": "plan", "overall_n_for_total_moe": overall, "total_completes": total,
            "total_invites": math.ceil(total / rr), "segments": rows,
            "warnings": warnings(rows, rr, deff)}


def budget(spec, completes):
    z = z_for(spec.get("confidence", 0.95))
    deff = spec.get("design_effect", 1.0)
    segs = spec.get("segments", [])
    total_pop = sum(s["population"] for s in segs)
    rows = []
    for seg in segs:
        sp, se = segment_defaults(spec, seg)
        n = round(completes * seg["population"] / total_pop)
        moe = achievable_moe(z, sp, n, seg["population"], deff)
        rows.append({"name": seg["name"], "completes": n, "target_moe": se,
                     "achievable_moe": None if moe is None else round(moe, 4),
                     "meets_target": moe is not None and moe <= se})
    return {"mode": "budget", "budget_completes": completes, "segments": rows,
            "warnings": [f"{r['name']}: supports +/-{r['achievable_moe']:.1%}, target +/-{r['target_moe']:.1%}. "
                         "Do not report this segment alone, or oversample it." for r in rows
                         if r["achievable_moe"] is not None and not r["meets_target"]]}


def warnings(rows, rr, deff):
    out = []
    for r in rows:
        if r["census_needed"]:
            out.append(f"{r['name']}: the floor equals the whole segment. Survey everyone, or relax its margin of error.")
        if r["weight"] < 0.5:
            out.append(f"{r['name']}: oversampled {1 / r['weight']:.1f}x. Weight it back before any total is reported.")
    if rr < 0.2:
        out.append(f"Response rate {rr:.0%} is low. Non-response bias can exceed sampling error. Plan a non-response check.")
    if deff > 1:
        out.append(f"Design effect {deff} inflates every n. Its source must be stated (pilot data or a prior wave).")
    return out


def render_markdown(r):
    if r["mode"] == "budget":
        lines = [f"# Budget check: {r['budget_completes']} completes", "",
                 "| Segment | Completes | Achievable MoE | Target MoE | Meets |", "|---|---|---|---|---|"]
        for s in r["segments"]:
            moe = "n/a" if s["achievable_moe"] is None else f"+/-{s['achievable_moe']:.1%}"
            lines.append(f"| {s['name']} | {s['completes']} | {moe} | +/-{s['target_moe']:.1%} | {'yes' if s['meets_target'] else 'NO'} |")
    else:
        lines = ["# Survey sample plan", "",
                 f"- n for the total margin of error alone: {r['overall_n_for_total_moe']}",
                 f"- Completes with segment floors: **{r['total_completes']}**",
                 f"- Invites at the stated response rate: {r['total_invites']}", "",
                 "| Segment | Population | Target MoE | Floor | Proportional | Quota | Invites | Weight |",
                 "|---|---|---|---|---|---|---|---|"]
        for s in r["segments"]:
            lines.append(f"| {s['name']} | {s['population']:,} | +/-{s['target_moe']:.1%} | {s['floor']} "
                         f"| {s['proportional']} | {s['quota']} | {s['invites']} | {s['weight']} |")
    if r["warnings"]:
        lines += ["", "## Warnings", ""] + [f"- {w}" for w in r["warnings"]]
    lines += ["", "Margin of error covers sampling error only. Coverage, non-response, and question wording are separate risks."]
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", required=True)
    ap.add_argument("--budget", type=int, help="fixed number of completes; report achievable margin of error per segment")
    ap.add_argument("--format", choices=["md", "json"], default="md")
    args = ap.parse_args()
    with open(args.input, encoding="utf-8") as f:
        spec = json.load(f)
    if args.budget is not None and not spec.get("segments"):
        sys.exit("error: --budget needs segments in the spec")
    result = budget(spec, args.budget) if args.budget is not None else plan(spec)
    sys.stdout.write(json.dumps(result, indent=2) + "\n" if args.format == "json" else render_markdown(result))


if __name__ == "__main__":
    main()
