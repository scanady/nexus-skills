#!/usr/bin/env python3
"""Weighted customer health scorer with segment thresholds and trend priority.

Scores four dimensions (usage, engagement, support, relationship) on 0-100,
blends them with dimension weights, classifies the result green/yellow/red
with segment-specific cutoffs, compares to the previous period, and ranks
accounts with the trend-priority matrix.

Missing metrics are skipped and the remaining weights are renormalised, so a
sparse record never scores as a bad one. `data_coverage` reports how much of
the weight was actually observed.

Usage:
    python health_scorer.py portfolio.json
    python health_scorer.py portfolio.json --format json
    python health_scorer.py portfolio.json --profile profile.json   # calibrated
"""

import json
import sys
from typing import Any, Dict, List, Optional, Tuple

from cs_common import base_parser, clamp, load_json, load_records, money, ratio

SEGMENTS = ("enterprise", "mid-market", "smb")

DEFAULT_WEIGHTS: Dict[str, float] = {
    "usage": 0.30,
    "engagement": 0.25,
    "support": 0.20,
    "relationship": 0.25,
}

# segment -> (green_min, yellow_min). Below yellow_min is red.
DEFAULT_THRESHOLDS: Dict[str, Tuple[float, float]] = {
    "enterprise": (75, 50),
    "mid-market": (70, 45),
    "smb": (65, 40),
}

SENTIMENT_SCORE = {"positive": 100.0, "neutral": 60.0, "negative": 20.0, "unknown": 50.0}

# (field, direction, sub-weight, (enterprise, mid-market, smb) target, hint when weak)
# direction "up": score = value / target. "down": score = 1 - value / limit.
Metric = Tuple[str, str, float, Tuple[float, float, float], str]
METRICS: Dict[str, List[Metric]] = {
    "usage": [
        ("login_frequency", "up", 0.35, (90, 80, 70), "Logins low: book a product engagement session"),
        ("feature_adoption", "up", 0.40, (80, 70, 60), "Adoption low: run a guided feature walkthrough"),
        ("dau_mau_ratio", "up", 0.25, (0.50, 0.40, 0.30), "Usage shallow: find the stickiness barrier"),
    ],
    "engagement": [
        ("support_ticket_volume", "down", 0.20, (5, 8, 10), "Ticket volume high: review root causes with support"),
        ("meeting_attendance", "up", 0.30, (95, 85, 75), "Attendance low: reset cadence and agenda value"),
        ("nps_score", "up", 0.25, (9, 8, 7), "NPS low: run a feedback deep-dive"),
        ("csat_score", "up", 0.25, (4.5, 4.0, 3.8), "CSAT low: escalate to support lead"),
    ],
    "support": [
        ("open_tickets", "down", 0.35, (10, 15, 20), "Open tickets high: clear the queue first"),
        ("escalation_rate", "down", 0.35, (0.25, 0.30, 0.40), "Escalations high: review support process"),
        ("avg_resolution_hours", "down", 0.30, (72, 96, 120), "Resolution slow: engage support leadership"),
    ],
    "relationship": [
        ("executive_sponsor_engagement", "up", 0.35, (90, 75, 60), "Sponsor weak: book an executive alignment call"),
        ("multi_threading_depth", "up", 0.30, (5, 3, 2), "Few contacts: add stakeholders across departments"),
        ("renewal_sentiment", "label", 0.35, (0, 0, 0), "Renewal sentiment negative: start a save plan now"),
    ],
}

# Trend-priority matrix: (band, trend) -> priority. A declining account outranks
# a stable account in the same band. "no_data" is treated as stable.
PRIORITY_MATRIX = {
    ("green", "declining"): "high",
    ("green", "stable"): "low",
    ("green", "improving"): "low",
    ("yellow", "declining"): "critical",
    ("yellow", "stable"): "medium",
    ("yellow", "improving"): "medium",
    ("red", "declining"): "critical",
    ("red", "stable"): "critical",
    ("red", "improving"): "high",
}
PRIORITY_RANK = {"critical": 0, "high": 1, "medium": 2, "low": 3}

TREND_DELTA = 5.0  # points of change that count as a real move
WEAK_METRIC = 40.0  # metric score below this raises a recommendation


def load_profile(path: Optional[str]) -> Tuple[Dict[str, float], Dict[str, Tuple[float, float]]]:
    """Return (weights, thresholds), with calibrated overrides applied."""
    weights = dict(DEFAULT_WEIGHTS)
    thresholds = dict(DEFAULT_THRESHOLDS)
    if not path:
        return weights, thresholds
    profile = load_json(path)
    weights.update(profile.get("dimension_weights", {}))
    if abs(sum(weights.values()) - 1.0) > 0.01:
        sys.exit("error: profile dimension_weights must sum to 1.0")
    for segment, cut in profile.get("thresholds", {}).items():
        if segment not in SEGMENTS:
            sys.exit(f"error: profile has unknown segment '{segment}'")
        if cut["green_min"] <= cut["yellow_min"]:
            sys.exit(f"error: profile {segment}: green_min must exceed yellow_min")
        thresholds[segment] = (cut["green_min"], cut["yellow_min"])
    return weights, thresholds


def metric_score(value: Any, direction: str, target: float) -> float:
    if direction == "label":
        return SENTIMENT_SCORE.get(str(value).lower(), SENTIMENT_SCORE["unknown"])
    if direction == "up":
        return clamp(ratio(value, target) * 100)
    return clamp((1.0 - ratio(value, target)) * 100)


def score_dimension(
    name: str, data: Dict[str, Any], seg_idx: int
) -> Tuple[Optional[float], float, List[str]]:
    """Return (score or None, observed weight share, hints for weak metrics)."""
    weighted = observed = 0.0
    hints: List[str] = []
    for field, direction, weight, targets, hint in METRICS[name]:
        if data.get(field) is None:
            continue
        score = metric_score(data[field], direction, targets[seg_idx])
        weighted += score * weight
        observed += weight
        if score < WEAK_METRIC:
            hints.append(hint)
    if observed == 0:
        return None, 0.0, hints
    return round(weighted / observed, 1), observed, hints


def band(score: float, cut: Tuple[float, float]) -> str:
    if score >= cut[0]:
        return "green"
    return "yellow" if score >= cut[1] else "red"


def trend(current: Optional[float], previous: Optional[float]) -> str:
    if current is None or previous is None:
        return "no_data"
    delta = current - previous
    if delta > TREND_DELTA:
        return "improving"
    return "declining" if delta < -TREND_DELTA else "stable"


def score_customer(
    customer: Dict[str, Any],
    weights: Dict[str, float],
    thresholds: Dict[str, Tuple[float, float]],
) -> Dict[str, Any]:
    segment = str(customer.get("segment", "")).lower()
    if segment not in SEGMENTS:
        sys.exit(f"error: {customer.get('customer_id')}: segment must be one of {', '.join(SEGMENTS)}")
    seg_idx = SEGMENTS.index(segment)
    cut = thresholds[segment]

    dims: Dict[str, Dict[str, Any]] = {}
    hints: List[str] = []
    for name in METRICS:
        score, observed, dim_hints = score_dimension(name, customer.get(name, {}), seg_idx)
        hints += dim_hints
        if score is not None:
            dims[name] = {"score": score, "weight": weights[name], "band": band(score, cut)}

    if not dims:
        sys.exit(f"error: {customer.get('customer_id')}: no usable metrics")
    seen_weight = sum(d["weight"] for d in dims.values())
    overall = round(sum(d["score"] * d["weight"] for d in dims.values()) / seen_weight, 1)
    overall_band = band(overall, cut)

    prev = customer.get("previous_period", {})
    trends = {name: trend(d["score"], prev.get(f"{name}_score")) for name, d in dims.items()}
    trends["overall"] = trend(overall, prev.get("overall_score"))

    effective_trend = "stable" if trends["overall"] == "no_data" else trends["overall"]
    priority = PRIORITY_MATRIX[(overall_band, effective_trend)]

    return {
        "customer_id": customer.get("customer_id", "unknown"),
        "name": customer.get("name", "Unknown"),
        "segment": segment,
        "arr": customer.get("arr", 0),
        "overall_score": overall,
        "band": overall_band,
        "thresholds": {"green_min": cut[0], "yellow_min": cut[1]},
        "dimensions": dims,
        "trends": trends,
        "priority": priority,
        "baseline_missing": trends["overall"] == "no_data",
        "data_coverage": round(seen_weight, 2),
        "recommendations": hints,
    }


def summarise(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    counts = {b: sum(1 for r in results if r["band"] == b) for b in ("green", "yellow", "red")}
    return {
        "total_customers": len(results),
        "average_score": round(ratio(sum(r["overall_score"] for r in results), len(results)), 1),
        **{f"{b}_count": n for b, n in counts.items()},
        "arr_in_critical": sum(r["arr"] for r in results if r["priority"] == "critical"),
    }


def render_text(results: List[Dict[str, Any]], summary: Dict[str, Any]) -> str:
    lines = [
        "CUSTOMER HEALTH REPORT",
        f"{summary['total_customers']} accounts | avg {summary['average_score']} | "
        f"green {summary['green_count']} yellow {summary['yellow_count']} red {summary['red_count']} | "
        f"ARR in critical priority {money(summary['arr_in_critical'])}",
        "",
    ]
    for r in results:
        flag = " (no baseline)" if r["baseline_missing"] else ""
        lines.append(
            f"[{r['priority'].upper():8}] {r['name']} ({r['customer_id']}) {r['segment']} "
            f"{money(r['arr'])}  score {r['overall_score']} {r['band']} / {r['trends']['overall']}{flag}"
        )
        dim_text = "  ".join(f"{n} {d['score']}" for n, d in r["dimensions"].items())
        lines.append(f"           {dim_text}  coverage {r['data_coverage']:.0%}")
        lines.extend(f"           - {hint}" for hint in r["recommendations"])
    return "\n".join(lines)


def main() -> None:
    parser = base_parser("Score customer health with trend priority.", "JSON file with a 'customers' list")
    parser.add_argument("--profile", help="Calibrated profile from calibrate_scoring.py")
    args = parser.parse_args()

    weights, thresholds = load_profile(args.profile)
    results = [score_customer(c, weights, thresholds) for c in load_records(args.input_file, "customers")]
    results.sort(key=lambda r: (PRIORITY_RANK[r["priority"]], -r["arr"]))
    summary = summarise(results)

    if args.fmt == "json":
        print(json.dumps({"report": "customer_health", "summary": summary, "customers": results}, indent=2))
    else:
        print(render_text(results, summary))


if __name__ == "__main__":
    main()
