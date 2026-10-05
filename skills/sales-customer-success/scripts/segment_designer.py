#!/usr/bin/env python3
"""Segment designer: ARR tiers, ICP fit score, kill list, tier migration.

Assigns each customer a CS tier by ARR, scores ICP fit 0-10 from seven weighted
signals, flags accounts that cost more than they earn, and checks whether an
account that carries a `current_tier` should move. Each tier names the health
segment (enterprise, mid-market, smb) whose thresholds health_scorer.py uses.

Customer fields: customer_id, name, arr, tenure_months, icp_fit_signals {...},
annual_support_cost, escalations_12mo, multi_year_contract, acquired_by_conflicting,
declining_industry, current_tier (optional).

Usage:
    python segment_designer.py customers.json
    python segment_designer.py customers.json --format json
"""

import json
from typing import Any, Dict, List, Optional

from cs_common import base_parser, load_records, money, ratio

# Highest tier first: (tier, ARR floor, coverage, yearly investment range, health segment)
TIERS = [
    ("strategic", 100_000, "Named CSM + executive sponsor", (20_000, 50_000), "enterprise"),
    ("enterprise", 20_000, "Named CSM", (5_000, 15_000), "enterprise"),
    ("mid-market", 5_000, "Pooled CSM + automation", (1_000, 3_000), "mid-market"),
    ("smb", 0, "Tech-touch + self-serve", (50, 500), "smb"),
]
TIER_ORDER = [t[0] for t in TIERS][::-1]  # lowest first

ICP_WEIGHTS = {
    "in_target_industry": 2.0,
    "in_target_size_range": 1.5,
    "uses_target_workflow": 2.0,
    "has_executive_sponsor": 1.5,
    "advocates_publicly": 1.0,
    "expansion_potential_high": 1.0,
    "competitor_concentration_low": 1.0,
}
POOR_FIT = 5.0
STRONG_FIT = 8.0
COST_TO_ARR_LIMIT = 0.5


def tier_for_arr(arr: float) -> str:
    return next(name for name, floor, *_ in TIERS if arr >= floor)


def icp_score(signals: Dict[str, bool]) -> float:
    return round(sum(w for s, w in ICP_WEIGHTS.items() if signals.get(s)), 1)


def kill_flags(customer: Dict[str, Any], fit: float) -> List[str]:
    arr = customer.get("arr", 0)
    checks = [
        (fit < POOR_FIT, f"ICP fit {fit} below {POOR_FIT:g}"),
        (arr > 0 and customer.get("annual_support_cost", 0) / arr > COST_TO_ARR_LIMIT, "Serving cost above 50% of ARR"),
        (customer.get("tenure_months", 99) < 12 and customer.get("escalations_12mo", 0) >= 2, "Under 12 months old with 2+ escalations"),
        (bool(customer.get("acquired_by_conflicting")), "Acquired by a conflicting company"),
        (bool(customer.get("declining_industry")), "In a declining or closing industry"),
    ]
    return [reason for hit, reason in checks if hit]


def migration(customer: Dict[str, Any], target: str, fit: float) -> Optional[str]:
    """Compare the supplied current tier with the ARR tier; apply promotion gates."""
    current = customer.get("current_tier")
    if current is None or current == target:
        return None
    if TIER_ORDER.index(target) < TIER_ORDER.index(current):
        return "demote: ARR below tier floor"
    signals = customer.get("icp_fit_signals", {})
    gates = {
        "mid-market": (customer.get("tenure_months", 0) >= 12 and fit >= 6, "needs 12+ months tenure and ICP fit 6+"),
        "enterprise": (bool(signals.get("has_executive_sponsor")), "needs an executive contact"),
        "strategic": (
            bool(customer.get("multi_year_contract")) and bool(signals.get("has_executive_sponsor"))
            and bool(signals.get("expansion_potential_high")),
            "needs multi-year deal, executive sponsor, and expansion potential",
        ),
    }
    passed, reason = gates[target]
    return "promote" if passed else f"hold: {reason}"


def design(customer: Dict[str, Any]) -> Dict[str, Any]:
    arr = customer.get("arr", 0)
    tier = tier_for_arr(arr)
    _, _, coverage, (low, high), health_segment = next(t for t in TIERS if t[0] == tier)
    fit = icp_score(customer.get("icp_fit_signals", {}))
    flags = kill_flags(customer, fit)
    status = "kill_candidate" if len(flags) >= 2 else "watch" if flags else "keep"
    return {
        "customer_id": customer.get("customer_id", "unknown"),
        "name": customer.get("name", "Unknown"),
        "arr": arr,
        "tier": tier,
        "health_segment": health_segment,
        "coverage": coverage,
        "investment_range_per_year": [low, high],
        "icp_fit": fit,
        "invest_aggressively": fit >= STRONG_FIT,
        "serving_cost_pct_of_arr": round(ratio(customer.get("annual_support_cost", 0), arr) * 100, 1) if arr else None,
        "status": status,
        "flags": flags,
        "migration": migration(customer, tier, fit),
    }


def tier_summary(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    total_arr = sum(r["arr"] for r in results)
    rows = []
    for name, _, coverage, _, _ in TIERS:
        members = [r for r in results if r["tier"] == name]
        arr = sum(r["arr"] for r in members)
        rows.append({
            "tier": name,
            "customers": len(members),
            "customers_pct": round(ratio(len(members), len(results)) * 100, 1),
            "arr": arr,
            "arr_pct": round(ratio(arr, total_arr) * 100, 1),
            "coverage": coverage,
        })
    return rows


def render_text(results: List[Dict[str, Any]], tiers: List[Dict[str, Any]]) -> str:
    lines = ["SEGMENT DESIGN", ""]
    lines += [f"{t['tier']:11} {t['customers']:>4} customers ({t['customers_pct']}%)  {money(t['arr'])} ({t['arr_pct']}% of ARR)  {t['coverage']}" for t in tiers]
    strategic = next(t for t in tiers if t["tier"] == "strategic")
    if strategic["customers_pct"] > 30:
        lines.append("! Over 30% of customers are strategic: the segmentation is not choosing.")
    lines.append("")
    for r in results:
        mark = {"kill_candidate": "KILL", "watch": "WATCH", "keep": ""}[r["status"]]
        move = f"  [{r['migration']}]" if r["migration"] else ""
        lines.append(f"{r['name']:24} {money(r['arr']):>10}  {r['tier']:11} fit {r['icp_fit']:>4}  {mark}{move}")
        lines.extend(f"    - {flag}" for flag in r["flags"])
    return "\n".join(lines)


def main() -> None:
    parser = base_parser("Tier customers by ARR and ICP fit; flag the kill list.", "JSON file with a 'customers' list")
    args = parser.parse_args()

    results = [design(c) for c in load_records(args.input_file, "customers")]
    tiers = tier_summary(results)

    if args.fmt == "json":
        print(json.dumps({"report": "segment_design", "tiers": tiers, "customers": results}, indent=2))
    else:
        print(render_text(results, tiers))


if __name__ == "__main__":
    main()
