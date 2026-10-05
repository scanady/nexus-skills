#!/usr/bin/env python3
"""Find funnel drop-off, rate uncertainty, and segment gaps.

Usage:
    python3 analyze_funnel.py funnel.json
    python3 analyze_funnel.py funnel.json --value-per-conversion 180 --format json
"""

import argparse
import json
import math

from campaign_data import InputError, divide, fmt, load_json, main_guard, number, table

Z95 = 1.96
ALPHA = 0.05
SMALL_COUNT = 30


def wilson(successes, trials):
    """95% Wilson score interval for a rate, in percent."""
    if trials == 0:
        return None
    p = successes / trials
    denom = 1 + Z95**2 / trials
    centre = (p + Z95**2 / (2 * trials)) / denom
    half = Z95 * math.sqrt(p * (1 - p) / trials + Z95**2 / (4 * trials**2)) / denom
    return [round(100 * (centre - half), 1), round(100 * (centre + half), 1)]


def two_sided_p(x1, n1, x2, n2):
    """Two-proportion z-test p-value. None when a group is empty or the pooled rate is 0 or 1."""
    if n1 == 0 or n2 == 0:
        return None
    pooled = (x1 + x2) / (n1 + n2)
    spread = math.sqrt(pooled * (1 - pooled) * (1 / n1 + 1 / n2))
    if spread == 0:
        return None
    z = (x1 / n1 - x2 / n2) / spread
    return math.erfc(abs(z) / math.sqrt(2))


def check_counts(counts, where):
    for i, count in enumerate(counts):
        number(count, f"{where}[{i}]")
        if i and count > counts[i - 1]:
            raise InputError(f"{where}: stage {i + 1} ({count}) exceeds stage {i} ({counts[i - 1]}); count unique entities per stage")


def stage_table(stages, counts):
    rows = []
    for i, (stage, count) in enumerate(zip(stages, counts)):
        row = {"stage": stage, "count": int(count), "cumulative_pct": round(100 * (divide(count, counts[0]) or 0), 2)}
        if i:
            rate = divide(count, counts[i - 1])
            row.update(
                from_stage=stages[i - 1],
                rate_pct=None if rate is None else round(100 * rate, 2),
                rate_ci95_pct=wilson(count, counts[i - 1]),
                lost=int(counts[i - 1] - count),
                small_sample=counts[i - 1] < SMALL_COUNT,
            )
        rows.append(row)
    return rows


def bottlenecks(rows):
    moves = [r for r in rows if "from_stage" in r]
    if not moves:
        return {}
    by_loss = max(moves, key=lambda r: r["lost"])
    rated = [r for r in moves if r["rate_pct"] is not None]
    by_rate = min(rated, key=lambda r: r["rate_pct"]) if rated else None
    label = lambda r: f"{r['from_stage']} -> {r['stage']}"
    return {
        "largest_absolute_loss": {"transition": label(by_loss), "lost": by_loss["lost"]},
        "lowest_rate": by_rate and {"transition": label(by_rate), "rate_pct": by_rate["rate_pct"]},
    }


def compare_segments(stages, segments, value_per_conversion):
    """Per transition and segment: rate vs the other segments, and the gap-to-best opportunity."""
    names = list(segments)
    transitions = len(stages) - 1
    tests = transitions * len(names)
    alpha = ALPHA / tests if tests else ALPHA
    findings = []
    for i in range(1, len(stages)):
        rates = {n: divide(segments[n][i], segments[n][i - 1]) for n in names}
        best = max((r for r in rates.values() if r is not None), default=None)
        for name in names:
            others_x = sum(segments[n][i] for n in names if n != name)
            others_n = sum(segments[n][i - 1] for n in names if n != name)
            p = two_sided_p(segments[name][i], segments[name][i - 1], others_x, others_n)
            rate = rates[name]
            finding = {
                "segment": name,
                "transition": f"{stages[i - 1]} -> {stages[i]}",
                "rate_pct": None if rate is None else round(100 * rate, 2),
                "other_segments_rate_pct": None if not others_n else round(100 * others_x / others_n, 2),
                "p_value": None if p is None else round(p, 4),
                "differs": p is not None and p < alpha,
            }
            if rate is not None and best is not None and best > rate:
                downstream = divide(segments[name][-1], segments[name][i]) or 0.0
                extra = segments[name][i - 1] * (best - rate) * downstream
                finding["gap_to_best_extra_conversions"] = round(extra, 1)
                if value_per_conversion is not None:
                    finding["gap_to_best_extra_value"] = round(extra * value_per_conversion, 2)
            findings.append(finding)
    findings.sort(key=lambda f: -f.get("gap_to_best_extra_conversions", 0))
    return {"alpha_after_bonferroni": round(alpha, 5), "tests": tests, "findings": findings}


def analyze(data, value_per_conversion):
    funnel = data.get("funnel")
    if not isinstance(funnel, dict):
        raise InputError("'funnel' object with 'stages' and 'counts' is required")
    stages, counts = funnel.get("stages"), funnel.get("counts")
    if not isinstance(stages, list) or not isinstance(counts, list) or len(stages) < 2 or len(stages) != len(counts):
        raise InputError("funnel.stages and funnel.counts must be lists of the same length, at least 2")
    check_counts(counts, "funnel.counts")

    rows = stage_table(stages, counts)
    result = {
        "stages": rows,
        "overall_conversion_pct": round(100 * (divide(counts[-1], counts[0]) or 0), 2),
        "bottlenecks": bottlenecks(rows),
        "warnings": [],
    }
    if any(r.get("small_sample") for r in rows):
        result["warnings"].append(f"A stage has fewer than {SMALL_COUNT} entrants. Its rate and interval are unreliable.")

    segments = data.get("segments")
    if segments:
        for name, seg in segments.items():
            if not isinstance(seg, dict) or len(seg.get("counts", [])) != len(stages):
                raise InputError(f"segments.{name}.counts must have {len(stages)} entries")
            check_counts(seg["counts"], f"segments.{name}.counts")
        result["segments"] = compare_segments(stages, {n: s["counts"] for n, s in segments.items()}, value_per_conversion)
        result["warnings"].append(
            "Segment tests are descriptive. Segments are not randomized, so a gap shows a difference, not a cause. "
            "Gap-to-best is an upper bound: it assumes the segment can match the best segment."
        )
    return result


def render(result, value_per_conversion):
    out = ["FUNNEL ANALYSIS", f"  Overall conversion: {result['overall_conversion_pct']}%", ""]
    out.append(
        table(
            ["Stage", "Count", "Step rate", "95% interval", "Lost", "Cumulative"],
            [
                (
                    r["stage"],
                    f"{r['count']:,}",
                    fmt(r.get("rate_pct"), ".1f", suffix="%"),
                    "-" if not r.get("rate_ci95_pct") else f"{r['rate_ci95_pct'][0]}-{r['rate_ci95_pct'][1]}%",
                    f"{r.get('lost', 0):,}",
                    fmt(r["cumulative_pct"], ".1f", suffix="%"),
                )
                for r in result["stages"]
            ],
            [18, 9, 10, 14, 8, 11],
        )
    )
    b = result["bottlenecks"]
    if b:
        out += ["", f"  Largest absolute loss: {b['largest_absolute_loss']['transition']} ({b['largest_absolute_loss']['lost']:,} lost)"]
        if b["lowest_rate"]:
            out.append(f"  Lowest step rate:      {b['lowest_rate']['transition']} ({b['lowest_rate']['rate_pct']}%)")
    seg = result.get("segments")
    if seg:
        out += ["", f"SEGMENT GAPS (Bonferroni alpha {seg['alpha_after_bonferroni']} over {seg['tests']} tests)"]
        shown = [f for f in seg["findings"] if "gap_to_best_extra_conversions" in f][:8]
        headers = ["Segment / step", "Rate", "Others", "p", "Differs", "Extra conv"]
        widths = [34, 8, 8, 8, 8, 11]
        if value_per_conversion is not None:
            headers.append("Extra value")
            widths.append(12)
        rows = []
        for f in shown:
            row = [
                f"{f['segment']}: {f['transition']}",
                fmt(f["rate_pct"], ".1f", suffix="%"),
                fmt(f["other_segments_rate_pct"], ".1f", suffix="%"),
                fmt(f["p_value"], ".4f"),
                "yes" if f["differs"] else "no",
                fmt(f["gap_to_best_extra_conversions"], ",.1f"),
            ]
            if value_per_conversion is not None:
                row.append(fmt(f["gap_to_best_extra_value"], ",.0f", prefix="$"))
            rows.append(row)
        out.append(table(headers, rows, widths))
    if result["warnings"]:
        out += ["", "WARNINGS", *(f"  - {w}" for w in result["warnings"])]
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("input_file", help="JSON file with 'funnel' and optional 'segments'")
    parser.add_argument("--value-per-conversion", type=float, help="value of one final conversion, to price segment gaps")
    parser.add_argument("--format", choices=("text", "json"), default="text", dest="output_format")
    args = parser.parse_args()

    result = analyze(load_json(args.input_file), args.value_per_conversion)
    print(json.dumps(result, indent=2) if args.output_format == "json" else render(result, args.value_per_conversion))


if __name__ == "__main__":
    main_guard(main)
