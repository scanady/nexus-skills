#!/usr/bin/env python3
"""Describe a social post export with robust statistics, and refuse to over-read it.

Works on any platform's own export (CSV or JSON). It finds an exposure column
(impressions, views, reach, plays) and the interaction columns (likes, comments,
shares, ...), computes engagement rate per post, and reports:

  - median and MAD, not mean and standard deviation (the data is heavy-tailed)
  - percentile bands and Tukey fences computed on the log scale, so the lower
    fence can actually fire on skewed data
  - a time-drift check (Spearman rho of the metric against post order)
  - sigma_log, the spread figure that size_experiment.py needs

Below 10 usable posts it describes and draws no conclusions.

Usage:
    python3 profile_posts.py --input posts.csv
    python3 profile_posts.py --input posts.json --metric exposure --output human
    python3 profile_posts.py --sample

Exit codes: 0 analysed | 2 below the 10-post floor, descriptive only | 3 unusable | 4 parse error
Stdlib only. No network.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import social_data as sd

SAMPLE_PATH = Path(__file__).resolve().parent.parent / "assets" / "example_posts.csv"
DRIFT_FLAG = 0.4


def analyse(records: list[dict], info: dict) -> dict:
    values = [r["value"] for r in records]
    n = len(values)
    logs, zeros = sd.positive_logs(values)
    med, spread = sd.median(values), sd.mad(values)
    q1, q3 = sd.percentile(values, 25), sd.percentile(values, 75)

    if len(logs) >= 4:
        lq1, lq3 = sd.percentile(logs, 25), sd.percentile(logs, 75)
        iqr = lq3 - lq1
        hi_fence, lo_fence = math.exp(lq3 + 1.5 * iqr), math.exp(lq1 - 1.5 * iqr)
    else:
        hi_fence, lo_fence = float("inf"), 0.0

    def band(v: float) -> str:
        if v >= hi_fence:
            return "BREAKOUT"
        if v >= q3:
            return "STRONG"
        if v >= q1:
            return "TYPICAL"
        return "WEAK" if v > lo_fence else "DUD"

    posts = sorted(
        ({"date": str(r["date"] or ""), "value": round(r["value"], 6),
          "exposure": r["exposure"], "band": band(r["value"]),
          "label": next((str(v) for k, v in r["row"].items()
                         if k.lower() in ("title", "name", "id", "post", "text") and v), "")[:60]}
         for r in records),
        key=lambda p: -p["value"])

    drift = None
    if sd.time_ordered(records) and n >= 5:
        ordered = sorted(records, key=lambda r: r["date"])
        drift = sd.spearman(list(range(n)), [r["value"] for r in ordered])

    below = n < sd.MIN_POSTS
    result = {
        "verdict": "DESCRIPTIVE_ONLY" if below else "ANALYSED",
        "exit_code": 2 if below else 0,
        "posts_analysed": n,
        "floor": sd.MIN_POSTS,
        "inputs": info,
        "metric_summary": {
            "median": round(med, 6), "mad": round(spread, 6),
            "p10": round(sd.percentile(values, 10), 6), "p25": round(q1, 6),
            "p75": round(q3, 6), "p90": round(sd.percentile(values, 90), 6),
            "breakout_above": None if hi_fence == float("inf") else round(hi_fence, 6),
            "dud_below": round(lo_fence, 6),
        },
        "planning_inputs": {
            "sigma_log": None if sd.robust_sigma_log(values) is None
            else round(sd.robust_sigma_log(values), 4),
            "robust_cv": round(sd.MAD_TO_SIGMA * spread / med, 4) if med else None,
            "zero_values_ignored_for_sigma_log": zeros,
        },
        "bands": {b: sum(1 for p in posts if p["band"] == b)
                  for b in ("BREAKOUT", "STRONG", "TYPICAL", "WEAK", "DUD")},
        "time_drift_rho": None if drift is None else round(drift, 3),
        "posts": posts,
        "notes": [
            "Median and MAD, not mean and standard deviation: one breakout post drags a mean "
            "to a value no post resembles.",
            "Exposure counts differ by platform and change over time. Compare posts from the "
            "same period and the same platform.",
        ],
    }
    if drift is not None and abs(drift) >= DRIFT_FLAG:
        result["warnings"] = [
            f"The metric trends with time (rho {drift:+.2f}). Posts are not interchangeable "
            "across the window, so any later group comparison needs this in mind."]
    if below:
        result["warnings"] = result.get("warnings", []) + [
            f"{n} usable posts is under the {sd.MIN_POSTS}-post floor. This is description, "
            "not evidence. Do not change strategy on it."]
    return result


def render(r: dict) -> str:
    if r["verdict"] == "UNUSABLE":
        return f"Profile: UNUSABLE\n{r['finding']}\nfix: {r['fix']}"
    m, i = r["metric_summary"], r["inputs"]
    lines = [f"Profile: {r['verdict']} ({r['posts_analysed']} posts, metric {i['metric']})", "=" * 62]
    lines += [f"  ! {w}" for w in r.get("warnings", [])]
    cols = f"exposure={i['exposure_col']}"
    if i["interaction_cols"]:
        cols += f", interactions={'+'.join(i['interaction_cols'])}"
    lines += [
        f"Columns   {cols}; used {i['rows_used']} of {i['rows_read']} rows",
        f"Median    {m['median']:.4g}   MAD {m['mad']:.4g}",
        f"Spread    p10 {m['p10']:.4g} | p25 {m['p25']:.4g} | p75 {m['p75']:.4g} | p90 {m['p90']:.4g}",
        f"Fences    breakout above {m['breakout_above']}, dud below {m['dud_below']}",
        "Bands     " + ", ".join(f"{k} {v}" for k, v in r["bands"].items()),
        f"Planning  sigma_log {r['planning_inputs']['sigma_log']} (robust CV "
        f"{r['planning_inputs']['robust_cv']}); pass sigma_log to size_experiment.py",
        "", "Posts, best first:"]
    for p in r["posts"]:
        lines.append(f"  {p['band']:<9} {p['value']:>10.4g}  {p['date']:<11} {p['label']}")
    lines += ["", *[f"- {n}" for n in r["notes"]]]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Describe a social post export honestly.")
    ap.add_argument("--input", help="CSV or JSON file, or - for stdin")
    ap.add_argument("--sample", action="store_true", help="use the bundled synthetic export")
    ap.add_argument("--metric", default="engagement_rate",
                    help="engagement_rate (default), exposure, or any numeric column name")
    ap.add_argument("--exposure-col", help="override the exposure column")
    ap.add_argument("--interaction-cols", help="comma-separated interaction columns")
    ap.add_argument("--output", choices=["json", "human"], default="json")
    args = ap.parse_args()
    if not (args.input or args.sample):
        ap.error("--input or --sample is required")

    try:
        rows = sd.load_rows(str(SAMPLE_PATH) if args.sample else args.input)
        records, info = sd.build_records(
            rows, args.metric, args.exposure_col,
            args.interaction_cols.split(",") if args.interaction_cols else None)
    except sd.DataError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 4
    if not records:
        result = {"verdict": "UNUSABLE", "exit_code": 3,
                  "finding": "No row has a usable exposure and metric value.",
                  "fix": "Check the column names, and that exposure is a positive number."}
    else:
        result = analyse(records, info)
    print(json.dumps(result, indent=2) if args.output == "json" else render(result))
    return result["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
