#!/usr/bin/env python3
"""Compute ROI, ROAS, and cost metrics per campaign and flag them against rough benchmarks.

Usage:
    python3 campaign_roi.py campaigns.json
    python3 campaign_roi.py campaigns.json --format json
    python3 campaign_roi.py --show-benchmarks
"""

import argparse
import json
from collections import defaultdict

from campaign_data import ASSETS, InputError, divide, fmt, load_json, main_guard, number, table

FUNNEL_FIELDS = ("impressions", "clicks", "leads", "customers")


def load_benchmarks():
    return load_json(ASSETS / "benchmarks.json")


def band(value, thresholds, higher_is_better):
    """Place a value in a low/target/high band."""
    if value is None:
        return "n/a"
    low, target, high = thresholds
    if higher_is_better:
        return "excellent" if value >= high else "good" if value >= target else "below_target" if value >= low else "underperforming"
    return "excellent" if value <= low else "good" if value <= target else "below_target" if value <= high else "underperforming"


def metrics(spend, other_costs, revenue, impressions, clicks, leads, customers):
    cost = spend + other_costs
    ctr = divide(clicks, impressions)
    return {
        "roi_pct": None if not cost else round(100 * (revenue - cost) / cost, 1),
        "roas": _round(divide(revenue, spend), 2),
        "loaded_roas": _round(divide(revenue, cost), 2),
        "cpa": _round(divide(cost, customers), 2),
        "cpl": _round(divide(cost, leads), 2),
        "cpc": _round(divide(spend, clicks), 2),
        "cpm": _round(None if not impressions else 1000 * spend / impressions, 2),
        "ctr_pct": None if ctr is None else round(100 * ctr, 3),
        "click_to_lead_pct": _pct(divide(leads, clicks)),
        "lead_to_customer_pct": _pct(divide(customers, leads)),
        "revenue_per_customer": _round(divide(revenue, customers), 2),
    }


def _round(value, places):
    return None if value is None else round(value, places)


def _pct(ratio):
    return None if ratio is None else round(100 * ratio, 2)


def read_campaign(item, index):
    where = f"campaigns[{index}]"
    if not isinstance(item, dict):
        raise InputError(f"{where}: expected an object")
    values = {field: number(item.get(field, 0), f"{where}.{field}") for field in ("spend", "revenue", "other_costs", *FUNNEL_FIELDS)}
    if values["clicks"] > values["impressions"] > 0:
        raise InputError(f"{where}: clicks exceed impressions")
    return item.get("name", f"#{index}"), item.get("channel", "default"), values


def assess(row, channel, benchmarks):
    """Return benchmark bands for CTR, ROAS, CPL, and CPA. ROAS uses media spend. CPL and CPA use total cost."""
    out = {}
    for key, spec in benchmarks["metrics"].items():
        table_ = spec["channels"]
        thresholds = table_.get(channel, table_["default"])
        out[key] = band(row[key], thresholds, spec["higher_is_better"])
    return out


def analyze(data, benchmarks):
    items = data.get("campaigns")
    if not isinstance(items, list) or not items:
        raise InputError("'campaigns' must be a non-empty list")

    campaigns, totals, by_channel = [], defaultdict(float), defaultdict(lambda: defaultdict(float))
    warnings = set()
    for index, item in enumerate(items):
        name, channel, v = read_campaign(item, index)
        row = metrics(v["spend"], v["other_costs"], v["revenue"], v["impressions"], v["clicks"], v["leads"], v["customers"])
        known = channel in benchmarks["metrics"]["roas"]["channels"]
        if not known:
            warnings.add(f"Channel '{channel}' has no benchmark. The 'default' range was used.")
        if v["customers"] > v["leads"] > 0:
            warnings.add(f"'{name}': customers exceed leads. Check that both count the same people.")
        if v["spend"] == 0:
            warnings.add(f"'{name}': zero spend. ROAS and CPA are undefined.")
        campaigns.append(
            {
                "name": name,
                "channel": channel,
                **{k: v[k] for k in ("spend", "other_costs", "revenue")},
                **row,
                "benchmark_bands": assess(row, channel if known else "default", benchmarks),
                "loses_money": v["revenue"] < v["spend"] + v["other_costs"],
            }
        )
        for bucket in (totals, by_channel[channel]):
            for key, val in v.items():
                bucket[key] += val

    def rollup(v):
        return {k: v[k] for k in ("spend", "other_costs", "revenue", "customers")} | metrics(
            v["spend"], v["other_costs"], v["revenue"], v["impressions"], v["clicks"], v["leads"], v["customers"]
        )

    if any(c["other_costs"] == 0 for c in campaigns):
        warnings.add("Some campaigns list no 'other_costs'. Their ROI and CPA cover media spend only and overstate returns.")
    warnings.add("Sum of campaign revenue can double count when each platform claims the same sale. Use one attribution view.")
    return {
        "campaigns": campaigns,
        "portfolio": rollup(totals),
        "by_channel": {ch: rollup(v) for ch, v in sorted(by_channel.items())},
        "warnings": sorted(warnings),
    }


def render(result):
    money = lambda v: fmt(v, ",.0f", prefix="$")
    out = ["CAMPAIGN ROI", ""]
    out.append(
        table(
            ["Campaign", "Spend", "Revenue", "ROI", "ROAS", "CPA", "CTR", "Flag"],
            [
                (
                    c["name"][:26],
                    money(c["spend"] + c["other_costs"]),
                    money(c["revenue"]),
                    fmt(c["roi_pct"], ".0f", suffix="%"),
                    fmt(c["roas"], ".2f", suffix="x"),
                    fmt(c["cpa"], ".2f", prefix="$"),
                    fmt(c["ctr_pct"], ".2f", suffix="%"),
                    "LOSS" if c["loses_money"] else "",
                )
                for c in result["campaigns"]
            ],
            [26, 9, 9, 7, 8, 9, 7, 5],
        )
    )
    out += ["", "BENCHMARK BANDS (CTR, ROAS, CPL, CPA vs rough ranges)"]
    out.append(
        table(
            ["Campaign", "CTR", "ROAS", "CPL", "CPA"],
            [
                (c["name"][:26], *(c["benchmark_bands"][k] for k in ("ctr_pct", "roas", "cpl", "cpa")))
                for c in result["campaigns"]
            ],
            [26, 14, 14, 14, 14],
        )
    )
    out += ["", "BY CHANNEL"]
    out.append(
        table(
            ["Channel", "Cost", "Revenue", "ROI", "ROAS", "CAC"],
            [
                (
                    ch,
                    money(v["spend"] + v["other_costs"]),
                    money(v["revenue"]),
                    fmt(v["roi_pct"], ".0f", suffix="%"),
                    fmt(v["roas"], ".2f", suffix="x"),
                    fmt(v["cpa"], ".2f", prefix="$"),
                )
                for ch, v in result["by_channel"].items()
            ],
            [26, 9, 9, 7, 8, 9],
        )
    )
    p = result["portfolio"]
    out += [
        "",
        f"PORTFOLIO  cost {money(p['spend'] + p['other_costs'])}  revenue {money(p['revenue'])}  "
        f"ROI {fmt(p['roi_pct'], '.0f', suffix='%')}  blended CAC {fmt(p['cpa'], '.2f', prefix='$')}",
        "",
        "WARNINGS",
        *(f"  - {w}" for w in result["warnings"]),
    ]
    return "\n".join(out)


def render_benchmarks(benchmarks):
    out = [benchmarks["_note"], ""]
    for spec in benchmarks["metrics"].values():
        direction = "higher is better" if spec["higher_is_better"] else "lower is better"
        out += [f"{spec['label']} ({direction})"]
        out.append(
            table(
                ["Channel", "Low", "Target", "High"],
                [(ch, *vals) for ch, vals in spec["channels"].items()],
                [18, 8, 8, 8],
            )
        )
        out.append("")
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("input_file", nargs="?", help="JSON file with a 'campaigns' list")
    parser.add_argument("--show-benchmarks", action="store_true", help="print the benchmark ranges and exit")
    parser.add_argument("--format", choices=("text", "json"), default="text", dest="output_format")
    args = parser.parse_args()

    benchmarks = load_benchmarks()
    if args.show_benchmarks:
        print(render_benchmarks(benchmarks))
        return
    if not args.input_file:
        raise InputError("input_file is required unless --show-benchmarks is set")
    result = analyze(load_json(args.input_file), benchmarks)
    print(json.dumps(result, indent=2) if args.output_format == "json" else render(result))


if __name__ == "__main__":
    main_guard(main)
