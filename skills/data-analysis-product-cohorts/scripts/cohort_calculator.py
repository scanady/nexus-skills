#!/usr/bin/env python3
"""Cohort retention, curve-shape, and funnel calculator for product event data.

Subcommands:
  curve   Pooled retention curve across all cohorts.
  matrix  Cohort x age retention matrix.
  shape   Label the pooled curve shape and the cohort-over-cohort trend.
  funnel  Ordered step conversion with optional time window.

Standard library only. Input is CSV. Run with --help for options.
"""

import argparse
import calendar
import csv
import datetime as dt
import json
import sys
from collections import Counter, defaultdict

DEFAULT_MAX_PERIOD = {"day": 30, "week": 12, "month": 12}
DEFAULT_COMPARE_AGE = {"day": 7, "week": 4, "month": 4}


class InputError(Exception):
    """Bad input the user can fix."""


# --------------------------------------------------------------------------
# Dates and grain buckets
# --------------------------------------------------------------------------

def parse_date(value: str) -> dt.date:
    try:
        return dt.date.fromisoformat(value.strip()[:10])
    except ValueError:
        raise InputError(f"not an ISO date (YYYY-MM-DD): {value!r}")


def parse_datetime(value: str) -> dt.datetime:
    text = value.strip().replace("Z", "+00:00")
    try:
        parsed = dt.datetime.fromisoformat(text)
    except ValueError:
        raise InputError(f"not an ISO timestamp: {value!r}")
    return parsed.replace(tzinfo=None) if parsed.tzinfo else parsed


def bucket(date: dt.date, grain: str) -> int:
    """Integer index of the calendar period holding the date."""
    if grain == "day":
        return date.toordinal()
    if grain == "week":
        return (date.toordinal() - 1) // 7  # weeks start on Monday
    return date.year * 12 + date.month - 1


def bucket_start(index: int, grain: str) -> dt.date:
    if grain == "day":
        return dt.date.fromordinal(index)
    if grain == "week":
        return dt.date.fromordinal(index * 7 + 1)
    year, month = divmod(index, 12)
    return dt.date(year, month + 1, 1)


def bucket_end(index: int, grain: str) -> dt.date:
    if grain == "day":
        return bucket_start(index, grain)
    if grain == "week":
        return bucket_start(index, grain) + dt.timedelta(days=6)
    year, month = divmod(index, 12)
    return dt.date(year, month + 1, calendar.monthrange(year, month + 1)[1])


def bucket_label(index: int, grain: str) -> str:
    start = bucket_start(index, grain)
    return start.strftime("%Y-%m") if grain == "month" else start.isoformat()


# --------------------------------------------------------------------------
# Loading
# --------------------------------------------------------------------------

def read_rows(path: str, required: list):
    try:
        handle = open(path, "r", encoding="utf-8-sig", newline="")
    except FileNotFoundError:
        raise InputError(f"file not found: {path}")
    with handle:
        reader = csv.DictReader(handle)
        missing = [c for c in required if c not in (reader.fieldnames or [])]
        if missing:
            raise InputError(
                f"column(s) not in CSV: {', '.join(missing)}. "
                f"Found: {', '.join(reader.fieldnames or [])}"
            )
        return list(reader)


def build_cohorts(args):
    """Return (cohorts, as_of). cohorts: {bucket_index: {size, ages: Counter}}."""
    rows = read_rows(args.input, [args.user_column, args.cohort_column, args.activity_column])
    if not rows:
        raise InputError("CSV has no rows")

    cohort_date = {}
    activity = defaultdict(set)
    latest = None
    for row in rows:
        user = row[args.user_column].strip()
        c_date = parse_date(row[args.cohort_column])
        a_date = parse_date(row[args.activity_column])
        cohort_date[user] = min(cohort_date.get(user, c_date), c_date)
        activity[user].add(a_date)
        latest = a_date if latest is None else max(latest, a_date)

    as_of = parse_date(args.as_of) if args.as_of else latest

    cohorts = {}
    for user, c_date in cohort_date.items():
        c_idx = bucket(c_date, args.grain)
        slot = cohorts.setdefault(c_idx, {"size": 0, "ages": Counter()})
        slot["size"] += 1
        ages = {
            bucket(a, args.grain) - c_idx
            for a in activity[user]
            if a >= c_date
        }
        if args.unbounded and ages:
            ages = set(range(0, max(ages) + 1))
        for age in ages:
            slot["ages"][age] += 1
    return cohorts, as_of


def is_mature(c_idx: int, age: int, grain: str, as_of: dt.date) -> bool:
    """A cell counts only when its whole period lies on or before as_of."""
    return bucket_end(c_idx + age, grain) <= as_of


def max_period_of(args) -> int:
    return args.max_period if args.max_period is not None else DEFAULT_MAX_PERIOD[args.grain]


# --------------------------------------------------------------------------
# Computations
# --------------------------------------------------------------------------

def compute_matrix(cohorts, grain, max_period, as_of):
    rows = []
    for c_idx in sorted(cohorts):
        size = cohorts[c_idx]["size"]
        cells = []
        for age in range(max_period + 1):
            if is_mature(c_idx, age, grain, as_of):
                active = cohorts[c_idx]["ages"].get(age, 0)
                cells.append({"age": age, "active": active, "rate": round(active / size, 4)})
            else:
                cells.append({"age": age, "active": None, "rate": None})
        rows.append({"cohort": bucket_label(c_idx, grain), "index": c_idx, "size": size, "cells": cells})
    return rows


def compute_curve(cohorts, grain, max_period, as_of):
    curve = []
    for age in range(max_period + 1):
        eligible = active = 0
        for c_idx, data in cohorts.items():
            if is_mature(c_idx, age, grain, as_of):
                eligible += data["size"]
                active += data["ages"].get(age, 0)
        if eligible == 0:
            break
        curve.append({"age": age, "eligible": eligible, "active": active,
                      "rate": round(active / eligible, 4)})
    return curve


def ols_slope(values):
    """Least-squares slope per period; steadier than endpoint difference on noisy tails."""
    n = len(values)
    mean_x = (n - 1) / 2
    mean_y = sum(values) / n
    num = sum((i - mean_x) * (v - mean_y) for i, v in enumerate(values))
    den = sum((i - mean_x) ** 2 for i in range(n))
    return num / den


def classify_shape(curve, min_users, flat_tol, floor):
    usable = []
    for point in curve:
        if point["eligible"] < min_users:
            break
        usable.append(point)
    if len(usable) < 5:
        return {"label": "insufficient-data", "points_used": len(usable),
                "note": f"need 5+ ages with {min_users}+ eligible users"}

    rates = [p["rate"] for p in usable]
    tail = rates[-max(3, len(rates) // 3):]
    slope = ols_slope(tail)
    level = sum(tail) / len(tail)
    first_drop = (rates[0] - rates[1]) / rates[0] if rates[0] > 0 else None

    if slope > flat_tol:
        label = "recovering"
    elif level < floor and slope > -flat_tol:
        label = "near-zero-floor"
    elif level < floor:
        label = "decays-to-zero"
    elif abs(slope) <= flat_tol:
        label = "plateau"
    else:
        label = "slow-decline"

    return {
        "label": label,
        "points_used": len(usable),
        "first_period_drop": None if first_drop is None else round(first_drop, 4),
        "tail_level": round(level, 4),
        "tail_slope_per_period": round(slope, 4),
        "thresholds": {"flat_tol": flat_tol, "floor": floor, "min_users": min_users},
    }


def cohort_trend(matrix, grain, min_users, compare_age, trend_tol):
    sized = [r for r in matrix if r["size"] >= min_users]
    age = compare_age if compare_age is not None else DEFAULT_COMPARE_AGE[grain]
    while age >= 1:
        series = [
            (r["cohort"], r["cells"][age]["rate"])
            for r in sized
            if age < len(r["cells"]) and r["cells"][age]["rate"] is not None
        ]
        if len(series) >= 3 or compare_age is not None:
            break
        age -= 1
    if age < 1 or len(series) < 3:
        return {"label": "insufficient-cohorts", "note": f"need 3+ mature cohorts with {min_users}+ users"}

    half = len(series) // 2
    older = sum(v for _, v in series[:half]) / half
    newer = sum(v for _, v in series[-half:]) / half
    delta = newer - older
    label = "improving" if delta >= trend_tol else "worsening" if delta <= -trend_tol else "flat"
    return {"label": label, "compare_age": age, "cohorts_used": len(series),
            "older_mean": round(older, 4), "newer_mean": round(newer, 4),
            "delta": round(delta, 4), "tolerance": trend_tol}


# --------------------------------------------------------------------------
# Funnel
# --------------------------------------------------------------------------

def funnel(args) -> int:
    stages = [s.strip() for s in args.stages.split(",") if s.strip()]
    if len(stages) < 2:
        raise InputError("--stages needs at least two comma-separated steps")
    required = [args.user_column, args.stage_column]
    if args.time_column:
        required.append(args.time_column)
    rows = read_rows(args.input, required)

    events = defaultdict(lambda: defaultdict(list))
    for row in rows:
        stage = row[args.stage_column].strip()
        if stage not in stages:
            continue
        user = row[args.user_column].strip()
        stamp = parse_datetime(row[args.time_column]) if args.time_column else None
        events[user][stage].append(stamp)

    window = dt.timedelta(days=args.window_days) if args.window_days is not None else None
    if window and not args.time_column:
        raise InputError("--window-days needs --time-column")

    counts = [0] * len(stages)
    for per_stage in events.values():
        reached = chain_depth(per_stage, stages, args.loose, window, bool(args.time_column))
        for i in range(reached):
            counts[i] += 1

    results = []
    for i, stage in enumerate(stages):
        prev = counts[i - 1] if i else counts[0]
        results.append({
            "stage": stage,
            "users": counts[i],
            "conversion_from_previous": round(counts[i] / prev, 4) if prev else 0.0,
            "conversion_from_first": round(counts[i] / counts[0], 4) if counts[0] else 0.0,
            "lost_from_previous": (prev - counts[i]) if i else 0,
        })
    leak = max(results[1:], key=lambda r: r["lost_from_previous"])["stage"] if counts[0] else None
    payload = {"mode": "loose" if args.loose else "strict",
               "window_days": args.window_days, "largest_absolute_loss_at": leak, "stages": results}

    if args.format == "json":
        print(json.dumps(payload, indent=2))
    else:
        print(f"funnel mode={payload['mode']} window_days={args.window_days} largest_loss_at={leak}")
        print(f"{'stage':<20}{'users':>8}{'from_prev':>11}{'from_first':>12}{'lost':>8}")
        for r in results:
            print(f"{r['stage']:<20}{r['users']:>8}{r['conversion_from_previous']:>11.1%}"
                  f"{r['conversion_from_first']:>12.1%}{r['lost_from_previous']:>8}")
    return 0


def chain_depth(per_stage, stages, loose, window, timed) -> int:
    """How many leading steps this user completed, honoring order and window."""
    if loose:
        depth = 0
        for stage in stages:
            if stage not in per_stage:
                break
            depth += 1
        return depth
    if not timed:
        return chain_depth(per_stage, stages, True, None, False)

    previous = None
    first = None
    depth = 0
    for stage in stages:
        stamps = sorted(per_stage.get(stage, []))
        pick = next((s for s in stamps if previous is None or s >= previous), None)
        if pick is None or (window and first is not None and pick - first > window):
            break
        first = pick if first is None else first
        previous = pick
        depth += 1
    return depth


# --------------------------------------------------------------------------
# Output for cohort commands
# --------------------------------------------------------------------------

def run_curve(args) -> int:
    cohorts, as_of = build_cohorts(args)
    curve = compute_curve(cohorts, args.grain, max_period_of(args), as_of)
    if args.format == "json":
        print(json.dumps({"grain": args.grain, "as_of": as_of.isoformat(),
                          "unbounded": args.unbounded, "curve": curve}, indent=2))
    else:
        print(f"curve grain={args.grain} as_of={as_of} unbounded={args.unbounded}")
        print(f"{'age':>4}{'eligible':>10}{'active':>8}{'retention':>11}")
        for p in curve:
            print(f"{p['age']:>4}{p['eligible']:>10}{p['active']:>8}{p['rate']:>11.1%}")
    return 0


def run_matrix(args) -> int:
    cohorts, as_of = build_cohorts(args)
    max_period = max_period_of(args)
    matrix = compute_matrix(cohorts, args.grain, max_period, as_of)
    if args.format == "json":
        print(json.dumps({"grain": args.grain, "as_of": as_of.isoformat(),
                          "unbounded": args.unbounded, "cohorts": matrix}, indent=2))
    else:
        print(f"matrix grain={args.grain} as_of={as_of} unbounded={args.unbounded} ('-' = period not finished)")
        print(f"{'cohort':<12}{'size':>7}" + "".join(f"{'p' + str(a):>7}" for a in range(max_period + 1)))
        for row in matrix:
            cells = "".join(
                f"{c['rate']:>7.1%}" if c["rate"] is not None else f"{'-':>7}" for c in row["cells"]
            )
            print(f"{row['cohort']:<12}{row['size']:>7}{cells}")
    return 0


def run_shape(args) -> int:
    cohorts, as_of = build_cohorts(args)
    max_period = max_period_of(args)
    curve = compute_curve(cohorts, args.grain, max_period, as_of)
    matrix = compute_matrix(cohorts, args.grain, max_period, as_of)
    payload = {
        "grain": args.grain,
        "as_of": as_of.isoformat(),
        "unbounded": args.unbounded,
        "curve_shape": classify_shape(curve, args.min_users, args.flat_tol, args.floor),
        "cohort_trend": cohort_trend(matrix, args.grain, args.min_users, args.compare_age, args.trend_tol),
        "note": "Heuristic labels. Read the curve and references/retention-curve-shapes.md before concluding.",
    }
    if args.format == "json":
        print(json.dumps(payload, indent=2))
    else:
        for key in ("curve_shape", "cohort_trend"):
            print(f"{key}:")
            for name, value in payload[key].items():
                print(f"  {name}: {value}")
        print(payload["note"])
    return 0


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def add_cohort_options(p):
    p.add_argument("input", help="CSV with one row per user activity")
    p.add_argument("--user-column", default="user_id")
    p.add_argument("--cohort-column", default="cohort_date", help="anchor event date")
    p.add_argument("--activity-column", default="activity_date", help="retained behavior date")
    p.add_argument("--grain", choices=["day", "week", "month"], default="week")
    p.add_argument("--max-period", type=int, default=None,
                   help="last age to report (default: 30 day, 12 week, 12 month)")
    p.add_argument("--unbounded", action="store_true",
                   help="count a user as retained at age N if active at N or later")
    p.add_argument("--as-of", default=None,
                   help="data cutoff date YYYY-MM-DD (default: latest activity date in file)")
    p.add_argument("--format", choices=["text", "json"], default="text")


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("curve", help="pooled retention curve")
    add_cohort_options(p)
    p.set_defaults(func=run_curve)

    p = sub.add_parser("matrix", help="cohort x age retention matrix")
    add_cohort_options(p)
    p.set_defaults(func=run_matrix)

    p = sub.add_parser("shape", help="classify curve shape and cohort trend")
    add_cohort_options(p)
    p.add_argument("--min-users", type=int, default=30, help="minimum users for a point or cohort to count")
    p.add_argument("--flat-tol", type=float, default=0.005, help="tail slope per period treated as flat")
    p.add_argument("--floor", type=float, default=0.05, help="tail level below which a curve counts as near zero")
    p.add_argument("--compare-age", type=int, default=None, help="age for the cohort-over-cohort comparison")
    p.add_argument("--trend-tol", type=float, default=0.02, help="newer minus older mean treated as a real change")
    p.set_defaults(func=run_shape)

    p = sub.add_parser("funnel", help="ordered step conversion")
    p.add_argument("input", help="CSV with one row per user step event")
    p.add_argument("--stages", required=True, help="ordered, comma-separated step names")
    p.add_argument("--user-column", default="user_id")
    p.add_argument("--stage-column", default="stage")
    p.add_argument("--time-column", default=None, help="enables step-order checks and --window-days")
    p.add_argument("--window-days", type=float, default=None, help="max days from first step to each later step")
    p.add_argument("--loose", action="store_true",
                   help="count a step even if an earlier step has no event (default is strict)")
    p.add_argument("--format", choices=["text", "json"], default="text")
    p.set_defaults(func=funnel)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        return args.func(args)
    except InputError as err:
        print(f"Error: {err}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
