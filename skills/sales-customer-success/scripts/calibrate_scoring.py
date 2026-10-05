#!/usr/bin/env python3
"""Calibrate health weights and segment thresholds against churn history.

Input is a history of past accounts with their dimension scores at fixed lead
times before the outcome (churn date for lost accounts, renewal date for kept
ones). The tool:

  1. Splits accounts into train and holdout (every 4th account, stratified).
  2. Fits dimension weights from how well each dimension separates churned
     from retained accounts (effect size, shrunk toward the defaults).
  3. Fits each segment's green and yellow cutoffs on train data: green_min is
     the lowest cutoff that still flags `--target-recall` of churned accounts
     at the evaluation lead; yellow_min is the highest cutoff whose red zone
     is at least `--red-precision` churn.
  4. Scores the defaults and the fit on the holdout, and warns on overfit.
  5. Measures how many days before churn the calibrated score first warns.

Cutoffs never move more than 10 points from the defaults, and a segment or
weight set with too few churn events keeps its defaults.

History schema:
  {"customers": [{"customer_id": "H-001", "segment": "enterprise",
                  "outcome": "churned" | "retained",
                  "snapshots": {"90": {"usage": 70, "engagement": 65, "support": 80, "relationship": 55},
                                "60": {...}, "30": {...}}}]}

Usage:
    python calibrate_scoring.py history.json
    python calibrate_scoring.py history.json --lead 60 --write-profile profile.json
"""

import json
import statistics
import sys
from collections import Counter
from datetime import date
from typing import Any, Dict, List, Optional, Tuple

from cs_common import base_parser, load_records
from health_scorer import DEFAULT_THRESHOLDS, DEFAULT_WEIGHTS, SEGMENTS

DIMENSIONS = tuple(DEFAULT_WEIGHTS)
MIN_EVENTS_WEIGHTS = 20  # churned and retained accounts needed to refit weights
MIN_EVENTS_SEGMENT = 10  # churned and retained accounts needed to refit a segment
MIN_RED_ACCOUNTS = 3  # smallest red zone worth judging by precision
SHIFT_LIMIT = 10  # cutoffs stay within this many points of the defaults
SHRINK = 0.5  # share of the data-driven weight blended with the default weight
WEIGHT_FLOOR = 0.10
OVERFIT_GAP = 0.15  # holdout recall this far below train recall is overfit

Cut = Tuple[float, float]
Row = Dict[str, Any]


def rate(part: float, whole: float) -> Optional[float]:
    return round(part / whole, 3) if whole else None


def overall(dims: Dict[str, float], weights: Dict[str, float]) -> float:
    return sum(weights[d] * dims[d] for d in DIMENSIONS) / sum(weights.values())


def prepare(raw: List[Dict[str, Any]], lead: int) -> Tuple[List[Row], int]:
    """Keep accounts with a complete snapshot at the evaluation lead."""
    rows: List[Row] = []
    for c in raw:
        snapshots = {
            int(days): dims for days, dims in c.get("snapshots", {}).items()
            if all(isinstance(dims.get(d), (int, float)) for d in DIMENSIONS)
        }
        if c.get("outcome") in ("churned", "retained") and c.get("segment") in SEGMENTS and lead in snapshots:
            rows.append({"id": c["customer_id"], "segment": c["segment"], "churned": c["outcome"] == "churned", "snapshots": snapshots})
    return rows, len(raw) - len(rows)


def split(rows: List[Row]) -> Tuple[List[Row], List[Row]]:
    ordered = sorted(rows, key=lambda r: (r["churned"], r["id"]))
    holdout = [r for i, r in enumerate(ordered) if i % 4 == 3]
    train = [r for i, r in enumerate(ordered) if i % 4 != 3]
    return train, holdout


def counts(rows: List[Row]) -> Tuple[int, int]:
    churned = sum(r["churned"] for r in rows)
    return churned, len(rows) - churned


def fit_weights(train: List[Row], lead: int) -> Tuple[Dict[str, float], Dict[str, float], str]:
    """Return (weights, effect sizes, note). Defaults survive thin data."""
    churned, retained = counts(train)
    if churned < MIN_EVENTS_WEIGHTS or retained < MIN_EVENTS_WEIGHTS:
        return dict(DEFAULT_WEIGHTS), {}, f"kept defaults: need {MIN_EVENTS_WEIGHTS}+ churned and retained in train (have {churned}/{retained})"

    effects: Dict[str, float] = {}
    for d in DIMENSIONS:
        lost = [r["snapshots"][lead][d] for r in train if r["churned"]]
        kept = [r["snapshots"][lead][d] for r in train if not r["churned"]]
        pooled = (((len(lost) - 1) * statistics.variance(lost) + (len(kept) - 1) * statistics.variance(kept))
                  / (len(lost) + len(kept) - 2)) ** 0.5
        effects[d] = round((statistics.mean(kept) - statistics.mean(lost)) / pooled, 2) if pooled else 0.0

    positive = {d: max(e, 0.0) for d, e in effects.items()}
    if sum(positive.values()) == 0:
        return dict(DEFAULT_WEIGHTS), effects, "kept defaults: no dimension separates churned from retained"

    total = sum(positive.values())
    blended = {d: SHRINK * positive[d] / total + (1 - SHRINK) * DEFAULT_WEIGHTS[d] for d in DIMENSIONS}
    floored = {d: max(w, WEIGHT_FLOOR) for d, w in blended.items()}
    scale = sum(floored.values())
    weights = {d: round(w / scale, 2) for d, w in floored.items()}
    top = max(weights, key=weights.get)  # absorb rounding drift so weights sum to exactly 1.0
    weights[top] = round(1 - (sum(weights.values()) - weights[top]), 2)
    return weights, effects, "refit from effect sizes, shrunk toward defaults"


def fit_segment(rows: List[Row], weights: Dict[str, float], default: Cut, lead: int,
                target_recall: float, red_precision: float) -> Tuple[Optional[Cut], str]:
    churned, retained = counts(rows)
    if churned < MIN_EVENTS_SEGMENT or retained < MIN_EVENTS_SEGMENT:
        return None, f"kept defaults: need {MIN_EVENTS_SEGMENT}+ churned and retained (have {churned}/{retained})"

    scored = [(overall(r["snapshots"][lead], weights), r["churned"]) for r in rows]
    lost_scores = [s for s, was_lost in scored if was_lost]
    g0, y0 = int(default[0]), int(default[1])

    greens = range(g0 - SHIFT_LIMIT, g0 + SHIFT_LIMIT + 1)
    reached = next((g for g in greens if sum(s < g for s in lost_scores) / len(lost_scores) >= target_recall), None)
    green = reached if reached is not None else greens[-1]

    yellow = min(y0, green - 5)
    for cut in range(min(y0 + SHIFT_LIMIT, green - 5), y0 - SHIFT_LIMIT - 1, -1):
        red = [was_lost for s, was_lost in scored if s < cut]
        if len(red) >= MIN_RED_ACCOUNTS and sum(red) / len(red) >= red_precision:
            yellow = cut
            break

    note = "calibrated" if reached is not None else f"calibrated, but recall {target_recall:.0%} not reachable within +/-{SHIFT_LIMIT} points"
    return (float(green), float(yellow)), note


def evaluate(rows: List[Row], weights: Dict[str, float], cuts: Dict[str, Cut], lead: int) -> Dict[str, Any]:
    tally: Counter = Counter()
    for r in rows:
        green, yellow = cuts[r["segment"]]
        score = overall(r["snapshots"][lead], weights)
        group = "churned" if r["churned"] else "retained"
        tally[group] += 1
        tally[f"{group}_flagged"] += score < green
        if score < yellow:
            tally["red"] += 1
            tally["red_churned"] += r["churned"]
    return {
        "churned": tally["churned"],
        "retained": tally["retained"],
        "recall": rate(tally["churned_flagged"], tally["churned"]),
        "false_alarm_rate": rate(tally["retained_flagged"], tally["retained"]),
        "red_precision": rate(tally["red_churned"], tally["red"]),
        "red_accounts": tally["red"],
    }


def warning_lead(rows: List[Row], weights: Dict[str, float], cuts: Dict[str, Cut], lead: int) -> Dict[str, Any]:
    """Days before churn at which each churned account first scored below green."""
    firsts: List[int] = []
    lost = [r for r in rows if r["churned"]]
    for r in lost:
        green = cuts[r["segment"]][0]
        flagged = [days for days, dims in r["snapshots"].items() if overall(dims, weights) < green]
        if flagged:
            firsts.append(max(flagged))
    return {
        "median_days": statistics.median(firsts) if firsts else None,
        "flagged_at_or_before_lead_pct": rate(sum(d >= lead for d in firsts), len(lost)),
        "never_flagged": len(lost) - len(firsts),
    }


def separation(rows: List[Row], weights: Dict[str, float]) -> Dict[str, Dict[str, Optional[float]]]:
    """Mean overall score of churned vs retained accounts at every lead."""
    out: Dict[str, Dict[str, Optional[float]]] = {}
    for days in sorted({d for r in rows for d in r["snapshots"]}, reverse=True):
        lost = [overall(r["snapshots"][days], weights) for r in rows if r["churned"] and days in r["snapshots"]]
        kept = [overall(r["snapshots"][days], weights) for r in rows if not r["churned"] and days in r["snapshots"]]
        out[str(days)] = {
            "churned_mean": round(statistics.mean(lost), 1) if lost else None,
            "retained_mean": round(statistics.mean(kept), 1) if kept else None,
        }
    return out


def calibrate(rows: List[Row], lead: int, target_recall: float, red_precision: float) -> Dict[str, Any]:
    train, holdout = split(rows)
    weights, effects, weight_note = fit_weights(train, lead)

    defaults = dict(DEFAULT_THRESHOLDS)
    fitted = dict(DEFAULT_THRESHOLDS)
    segments: Dict[str, Any] = {}
    for seg in SEGMENTS:
        seg_train = [r for r in train if r["segment"] == seg]
        cut, note = fit_segment(seg_train, weights, defaults[seg], lead, target_recall, red_precision)
        if cut:
            fitted[seg] = cut
        segments[seg] = {
            "status": note,
            "default": {"green_min": defaults[seg][0], "yellow_min": defaults[seg][1]},
            "calibrated": {"green_min": fitted[seg][0], "yellow_min": fitted[seg][1]} if cut else None,
            "separation": separation([r for r in rows if r["segment"] == seg], weights),
        }

    results = {
        "default": {"train": evaluate(train, DEFAULT_WEIGHTS, defaults, lead), "holdout": evaluate(holdout, DEFAULT_WEIGHTS, defaults, lead)},
        "calibrated": {"train": evaluate(train, weights, fitted, lead), "holdout": evaluate(holdout, weights, fitted, lead)},
    }
    warnings: List[str] = []
    tr, ho = results["calibrated"]["train"]["recall"], results["calibrated"]["holdout"]["recall"]
    if tr is not None and ho is not None and tr - ho > OVERFIT_GAP:
        warnings.append(f"Overfit: holdout recall {ho:.0%} is {tr - ho:.0%} below train recall {tr:.0%}. Collect more history before adopting.")
    if ho is not None and ho < target_recall - OVERFIT_GAP:
        warnings.append(f"Holdout recall {ho:.0%} misses the {target_recall:.0%} target. Add leading signals before trusting the score.")
    if not any(s["calibrated"] for s in segments.values()):
        warnings.append("No segment had enough churn events to calibrate. Defaults stay in force.")

    return {
        "lead_days": lead,
        "accounts": {"train": len(train), "holdout": len(holdout)},
        "weights": {"default": DEFAULT_WEIGHTS, "calibrated": weights, "effect_sizes": effects, "note": weight_note},
        "segments": segments,
        "results": results,
        "warning_lead": {
            "default": warning_lead(rows, DEFAULT_WEIGHTS, defaults, lead),
            "calibrated": warning_lead(rows, weights, fitted, lead),
        },
        "warnings": warnings,
    }


def profile_from(report: Dict[str, Any]) -> Dict[str, Any]:
    ho = report["results"]["calibrated"]["holdout"]
    return {
        "dimension_weights": report["weights"]["calibrated"],
        "thresholds": {s: seg["calibrated"] for s, seg in report["segments"].items() if seg["calibrated"]},
        "provenance": {
            "calibrated_on": date.today().isoformat(),
            "lead_days": report["lead_days"],
            "accounts": report["accounts"],
            "holdout_recall": ho["recall"],
            "holdout_false_alarm_rate": ho["false_alarm_rate"],
            "recalibrate_by": "next quarter, or after a product, pricing, or ICP change",
        },
    }


def fmt(value: Optional[float]) -> str:
    return "n/a" if value is None else f"{value:.0%}"


def render_text(report: Dict[str, Any]) -> str:
    lines = [f"CALIBRATION (evaluation lead {report['lead_days']} days; train {report['accounts']['train']}, holdout {report['accounts']['holdout']})", ""]
    lines.append(f"Weights: {report['weights']['calibrated']}  ({report['weights']['note']})")
    for seg, info in report["segments"].items():
        cal = info["calibrated"] or info["default"]
        lines.append(f"{seg:11} green>={cal['green_min']:g} yellow>={cal['yellow_min']:g}  [{info['status']}]")
    lines.append("")
    for label in ("default", "calibrated"):
        for part in ("train", "holdout"):
            m = report["results"][label][part]
            lines.append(f"{label:10} {part:7} recall {fmt(m['recall'])}  false alarms {fmt(m['false_alarm_rate'])}  red precision {fmt(m['red_precision'])} ({m['red_accounts']} red)")
    wl = report["warning_lead"]["calibrated"]
    lines.append(f"\nMedian first warning: {wl['median_days']} days before churn; flagged at lead or earlier: {fmt(wl['flagged_at_or_before_lead_pct'])}; never flagged: {wl['never_flagged']}")
    lines.extend(f"! {w}" for w in report["warnings"])
    return "\n".join(lines)


def main() -> None:
    parser = base_parser("Calibrate health weights and thresholds on churn history.", "JSON file with a 'customers' history list")
    parser.add_argument("--lead", type=int, default=60, help="Evaluation lead in days before outcome (default 60)")
    parser.add_argument("--target-recall", type=float, default=0.80, help="Share of churned accounts to flag (default 0.80)")
    parser.add_argument("--red-precision", type=float, default=0.50, help="Minimum churn share inside red (default 0.50)")
    parser.add_argument("--write-profile", help="Write the calibrated profile JSON here for health_scorer.py --profile")
    args = parser.parse_args()

    rows, dropped = prepare(load_records(args.input_file, "customers"), args.lead)
    churned, retained = counts(rows)
    if churned == 0 or retained == 0:
        sys.exit(f"error: need churned and retained accounts with a {args.lead}-day snapshot (usable: {churned} churned, {retained} retained)")

    report = calibrate(rows, args.lead, args.target_recall, args.red_precision)
    report["dropped_records"] = dropped

    if args.write_profile:
        with open(args.write_profile, "w", encoding="utf-8") as handle:
            json.dump(profile_from(report), handle, indent=2)
    print(json.dumps(report, indent=2) if args.fmt == "json" else render_text(report))


if __name__ == "__main__":
    main()
