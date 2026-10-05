#!/usr/bin/env python3
"""Van Westendorp Price Sensitivity Meter: turn WTP survey answers into a price range.

Usage:
    python3 van_westendorp.py --input survey.csv [--format md|json] [--price 49 --price 89]
    python3 van_westendorp.py --input survey.json --segment-field segment
    python3 van_westendorp.py --sample

Input rows (CSV header or JSON objects; JSON may be a list or {"respondents": [...]}):
    too_cheap       price so low the respondent doubts quality
    cheap           price that feels like a bargain        (alias: bargain)
    expensive       price that feels expensive but still OK (alias: getting_expensive)
    too_expensive   price so high the respondent will not buy
    segment         optional; any label (ICP, SMB, role...)
    buy_cheap       optional Newton-Miller-Smith follow-up: purchase likelihood at "cheap"
    buy_expensive   optional NMS follow-up: purchase likelihood at "expensive"
                    Likelihood is 1-5 Likert or a 0-1 probability.

Reports per segment and overall:
  1. Screening: rows dropped for missing values or answers out of order.
  2. Four crossings: PMC, OPP, IDP, PME. Range of acceptable prices = [PMC, PME].
  3. Test prices: share who call each candidate price too cheap or too expensive.
  4. NMS (only when buy_* columns exist): trial-maximizing and revenue-maximizing price.

Stated preference, not revealed. The output is a range to test, never the price.
Python 3 stdlib only.
"""
import argparse
import csv
import json
import random
import statistics
import sys

FIELDS = ("too_cheap", "cheap", "expensive", "too_expensive")
ALIASES = {"bargain": "cheap", "getting_expensive": "expensive"}
MIN_N, GOOD_N = 30, 100
# Standard NMS calibration: stated Likert intent overstates real purchase.
LIKERT_TO_PROB = {1: 0.0, 2: 0.1, 3: 0.3, 4: 0.5, 5: 0.7}


# ---------------------------------------------------------------- input


def load_rows(path):
    """Read CSV or JSON into a list of dicts with canonical field names."""
    with open(path, newline="", encoding="utf-8") as fh:
        if path.lower().endswith(".csv"):
            rows = list(csv.DictReader(fh))
        else:
            data = json.load(fh)
            rows = data.get("respondents", []) if isinstance(data, dict) else data
    return [{ALIASES.get(k.strip(), k.strip()): v for k, v in row.items()} for row in rows]


def to_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def to_prob(value):
    """Map a 1-5 Likert answer or a 0-1 probability to a calibrated purchase probability."""
    v = to_float(value)
    if v is None:
        return None
    if 0 <= v <= 1:
        return v
    return LIKERT_TO_PROB.get(int(round(v)))


def screen(rows):
    """Keep rows with four numeric answers in order. Return (kept, dropped_missing, dropped_order)."""
    kept, missing, disorder = [], 0, 0
    for row in rows:
        prices = [to_float(row.get(f)) for f in FIELDS]
        if any(p is None or p < 0 for p in prices):
            missing += 1
            continue
        if not prices[0] <= prices[1] <= prices[2] <= prices[3]:
            disorder += 1
            continue
        clean = dict(zip(FIELDS, prices))
        clean["segment"] = str(row.get("segment") or "").strip()
        clean["buy_cheap"] = to_prob(row.get("buy_cheap"))
        clean["buy_expensive"] = to_prob(row.get("buy_expensive"))
        kept.append(clean)
    return kept, missing, disorder


# ---------------------------------------------------------------- analysis


def curves(rows, grid):
    """Cumulative shares at each grid price.

    too_cheap and cheap fall with price (share whose threshold is at or above p).
    expensive and too_expensive rise with price (share whose threshold is at or below p).
    """
    n = len(rows)
    out = {f: [] for f in FIELDS}
    for p in grid:
        out["too_cheap"].append(sum(r["too_cheap"] >= p for r in rows) / n)
        out["cheap"].append(sum(r["cheap"] >= p for r in rows) / n)
        out["expensive"].append(sum(r["expensive"] <= p for r in rows) / n)
        out["too_expensive"].append(sum(r["too_expensive"] <= p for r in rows) / n)
    return out


def crossing(grid, falling, rising):
    """Price where a falling curve meets a rising one.

    The gap (falling - rising) never increases, so there is one crossing at most.
    An exact tie over several grid points returns the middle of that flat run.
    A sign change between two points is linearly interpolated.
    """
    gaps = [f - r for f, r in zip(falling, rising)]
    for i, gap in enumerate(gaps):
        if gap > 0:
            continue
        if gap == 0:
            j = i
            while j + 1 < len(gaps) and gaps[j + 1] == 0:
                j += 1
            return (grid[i] + grid[j]) / 2
        if i == 0:
            return None  # curves already crossed below the lowest answer
        prev = gaps[i - 1]
        return grid[i - 1] + prev / (prev - gap) * (grid[i] - grid[i - 1])
    return None


def share_at(rows, price):
    """How respondents read one candidate price."""
    n = len(rows)
    return {
        "price": price,
        "too_cheap_pct": 100 * sum(r["too_cheap"] >= price for r in rows) / n,
        "bargain_pct": 100 * sum(r["cheap"] >= price for r in rows) / n,
        "expensive_pct": 100 * sum(r["expensive"] <= price for r in rows) / n,
        "too_expensive_pct": 100 * sum(r["too_expensive"] <= price for r in rows) / n,
    }


def purchase_prob(r, price):
    """NMS convention: zero outside [too_cheap, too_expensive]; flat at buy_cheap up to "cheap";
    linear from buy_cheap to buy_expensive between "cheap" and "expensive"; linear to zero at
    "too_expensive"."""
    if price < r["too_cheap"] or price > r["too_expensive"]:
        return 0.0
    if price <= r["cheap"]:
        return r["buy_cheap"]
    if price <= r["expensive"]:
        span = r["expensive"] - r["cheap"]
        t = (price - r["cheap"]) / span if span else 1.0
        return r["buy_cheap"] + t * (r["buy_expensive"] - r["buy_cheap"])
    span = r["too_expensive"] - r["expensive"]
    t = (price - r["expensive"]) / span if span else 1.0
    return r["buy_expensive"] * (1 - t)


def nms(rows, grid):
    """Trial and revenue index per price, for rows that answered both follow-ups."""
    usable = [r for r in rows if r["buy_cheap"] is not None and r["buy_expensive"] is not None]
    if not usable:
        return None
    points = []
    for p in grid:
        trial = statistics.fmean(purchase_prob(r, p) for r in usable)
        points.append({"price": p, "trial_pct": 100 * trial, "revenue_index": p * trial})
    top_trial = max(points, key=lambda x: x["trial_pct"])
    top_revenue = max(points, key=lambda x: x["revenue_index"])
    return {
        "n": len(usable),
        "trial_max_price": top_trial["price"],
        "trial_max_pct": top_trial["trial_pct"],
        "revenue_max_price": top_revenue["price"],
        "revenue_max_trial_pct": top_revenue["trial_pct"],
    }


def analyze(rows, label, test_prices, raw_n):
    """Full PSM for one group of screened rows."""
    result = {"segment": label, "n_raw": raw_n, "n": len(rows), "warnings": []}
    if len(rows) < 2:
        result["warnings"].append("Fewer than 2 usable respondents. No analysis.")
        return result
    if len(rows) < MIN_N:
        result["warnings"].append(
            f"N={len(rows)} is below {MIN_N}. Treat the range as a hypothesis only.")
    elif len(rows) < GOOD_N:
        result["warnings"].append(f"N={len(rows)}. Usable; {GOOD_N}+ gives stable crossings.")

    grid = sorted({r[f] for r in rows for f in FIELDS})
    c = curves(rows, grid)
    points = {
        "pmc": crossing(grid, c["too_cheap"], c["expensive"]),
        "opp": crossing(grid, c["too_cheap"], c["too_expensive"]),
        "idp": crossing(grid, c["cheap"], c["expensive"]),
        "pme": crossing(grid, c["cheap"], c["too_expensive"]),
    }
    result.update(points)
    if None in points.values():
        result["warnings"].append("A crossing falls outside the answer range. Check the data.")
    elif points["pmc"] > points["pme"]:
        result["warnings"].append("PMC above PME: no acceptable range. Buyers disagree on value.")
    elif points["pme"] > 0 and (points["pme"] - points["pmc"]) / points["pme"] < 0.15:
        result["warnings"].append("Range is under 15% wide. Small price moves carry high risk.")

    result["medians"] = {f: statistics.median(r[f] for r in rows) for f in FIELDS}
    result["tests"] = []
    for price in test_prices:
        t = share_at(rows, price)
        low, high = points["pmc"], points["pme"]
        if low is None or high is None:
            t["verdict"] = "unknown"
        else:
            t["verdict"] = "below range" if price < low else "above range" if price > high else "in range"
        result["tests"].append(t)
    result["nms"] = nms(rows, grid)
    return result


def run(rows, segment_field, test_prices):
    """Screen, then analyze overall and per segment."""
    for row in rows:
        row["segment"] = str(row.get(segment_field) or "").strip() if segment_field else ""
    kept, missing, disorder = screen(rows)
    screening = {"rows": len(rows), "kept": len(kept), "missing": missing, "out_of_order": disorder}
    report = {"screening": screening, "groups": [analyze(kept, "All respondents", test_prices, len(rows))]}
    if rows and (missing + disorder) / len(rows) > 0.2:
        report["groups"][0]["warnings"].append(
            "Over 20% of rows dropped. Question wording or survey logic may confuse respondents.")
    labels = sorted({r["segment"] for r in kept if r["segment"]})
    if segment_field and len(labels) > 1:
        for label in labels:
            group = [r for r in kept if r["segment"] == label]
            raw = sum(1 for r in rows if r["segment"] == label)
            report["groups"].append(analyze(group, label, test_prices, raw))
    return report


# ---------------------------------------------------------------- output


def money(v):
    return "n/a" if v is None else f"${v:,.2f}"


def rounded(obj):
    """Two-decimal floats for JSON output."""
    if isinstance(obj, float):
        return round(obj, 2)
    if isinstance(obj, dict):
        return {k: rounded(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [rounded(v) for v in obj]
    return obj


def render_md(report):
    s = report["screening"]
    lines = [
        "# Van Westendorp Price Sensitivity Report",
        "",
        f"Rows: {s['rows']} · kept {s['kept']} · dropped {s['missing']} missing, "
        f"{s['out_of_order']} out of order (expected too_cheap ≤ cheap ≤ expensive ≤ too_expensive).",
        "",
    ]
    for g in report["groups"]:
        lines += [f"## {g['segment']} (N={g['n']})", ""]
        lines += [f"> ⚠ {w}" for w in g["warnings"]]
        if g["warnings"]:
            lines.append("")
        if "pmc" not in g:
            continue
        lines += [
            "| Point | Curves crossing | Price | Read |",
            "|---|---|---|---|",
            f"| PMC | too cheap × expensive | {money(g['pmc'])} | Floor. Below it, quality doubt wins. |",
            f"| OPP | too cheap × too expensive | {money(g['opp'])} | Equal resistance both sides. Not profit-max. |",
            f"| IDP | cheap × expensive | {money(g['idp'])} | Price most buyers read as normal. |",
            f"| PME | cheap × too expensive | {money(g['pme'])} | Ceiling. Above it, rejection wins. |",
            "",
            f"**Range of acceptable prices: {money(g['pmc'])} – {money(g['pme'])}** 🟡 stated preference",
            "",
            "Medians: " + " · ".join(f"{k} {money(v)}" for k, v in g["medians"].items()),
            "",
        ]
        if g["tests"]:
            lines += ["| Test price | Too cheap | Bargain | Expensive | Too expensive | Verdict |",
                      "|---|---|---|---|---|---|"]
            lines += [
                f"| {money(t['price'])} | {t['too_cheap_pct']:.0f}% | {t['bargain_pct']:.0f}% | "
                f"{t['expensive_pct']:.0f}% | {t['too_expensive_pct']:.0f}% | {t['verdict']} |"
                for t in g["tests"]
            ]
            lines.append("")
        if g["nms"]:
            m = g["nms"]
            lines += [
                f"NMS (N={m['n']}): trial peaks at {money(m['trial_max_price'])} "
                f"({m['trial_max_pct']:.0f}% trial). Revenue index peaks at "
                f"{money(m['revenue_max_price'])} ({m['revenue_max_trial_pct']:.0f}% trial). 🟡 calibrated intent",
                "",
            ]
    lines += [
        "## Read before use",
        "",
        "- Range, not price. Pick the point inside it with margin floor, competitors, and positioning.",
        "- Segments with different ranges → different tiers, not one averaged price.",
        "- Confirm the upper half with a live price test or deal data before anchoring near PME.",
    ]
    return "\n".join(lines)


def synthetic(n=80, seed=7):
    """Two-segment fictional survey with NMS follow-ups and a few bad rows."""
    rng = random.Random(seed)
    rows = []
    for i in range(n):
        segment, ref = ("Clinic", rng.gauss(95, 18)) if i % 3 else ("Solo", rng.gauss(45, 10))
        ref = max(15.0, ref)
        rows.append({
            "segment": segment,
            "too_cheap": round(ref * rng.uniform(0.25, 0.45), 2),
            "cheap": round(ref * rng.uniform(0.55, 0.8), 2),
            "expensive": round(ref * rng.uniform(0.95, 1.2), 2),
            "too_expensive": round(ref * rng.uniform(1.35, 1.9), 2),
            "buy_cheap": rng.choice([4, 4, 5, 5, 3]),
            "buy_expensive": rng.choice([2, 2, 3, 3, 4, 1]),
        })
    rows[3]["cheap"], rows[3]["expensive"] = rows[3]["expensive"], rows[3]["cheap"]  # out of order
    rows[11]["too_expensive"] = ""  # missing
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--input", help="CSV or JSON survey file.")
    src.add_argument("--sample", action="store_true", help="Run on a built-in fictional survey.")
    ap.add_argument("--format", choices=["md", "json"], default="md")
    ap.add_argument("--price", type=float, action="append", default=[],
                    help="Candidate price to test. Repeat for several.")
    ap.add_argument("--segment-field", help="Column holding segment labels (sample uses 'segment').")
    args = ap.parse_args()

    if args.sample:
        rows, segment_field = synthetic(), args.segment_field or "segment"
        prices = args.price or [49, 89, 129]
    else:
        try:
            rows = load_rows(args.input)
        except (OSError, ValueError) as exc:
            sys.exit(f"error: cannot read {args.input}: {exc}")
        segment_field, prices = args.segment_field, args.price
    if not rows:
        sys.exit("error: no respondents found")

    report = run(rows, segment_field, prices)
    print(json.dumps(rounded(report), indent=2) if args.format == "json" else render_md(report))


if __name__ == "__main__":
    main()
