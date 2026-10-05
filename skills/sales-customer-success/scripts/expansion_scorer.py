#!/usr/bin/env python3
"""Expansion scorer: seats, tier upgrades, module cross-sell, new departments.

Estimates revenue per opportunity, ranks by impact x ease (0-100), and lists
under-used modules as enablement work, not sales work. Run it only on accounts
that are green or yellow in health_scorer.py and low or medium in
churn_risk_scorer.py; selling to a failing account speeds up churn.

Usage:
    python expansion_scorer.py portfolio.json
    python expansion_scorer.py portfolio.json --format json
"""

import json
from typing import Any, Dict, List, Optional, Tuple

from cs_common import base_parser, clamp, load_records, money, ratio

# Price multiplier of each plan tier relative to the entry tier.
TIER_MULTIPLIER: Dict[str, float] = {"starter": 1.0, "professional": 1.8, "enterprise": 3.0, "enterprise_plus": 4.5}

# Module price as a share of current ARR. Unknown modules use DEFAULT_MODULE_SHARE.
MODULE_SHARE: Dict[str, float] = {
    "core_platform": 0.0,
    "analytics_module": 0.15,
    "integrations_module": 0.12,
    "api_access": 0.10,
    "advanced_reporting": 0.18,
    "security_module": 0.20,
    "automation_module": 0.15,
    "collaboration_module": 0.10,
    "data_export": 0.08,
    "custom_workflows": 0.22,
    "sso_module": 0.08,
    "audit_module": 0.10,
}
DEFAULT_MODULE_SHARE = 0.10

SEAT_GROWTH = {"enterprise": 0.25, "mid-market": 0.20, "smb": 0.15}
SEAT_READY_UTILISATION = 0.90  # seats this full signal a seat upsell
LOW_USAGE_PCT = 30  # adopted module below this needs enablement
NEW_DEPARTMENT_DISCOUNT = 0.8  # a new department lands below the average one

EASE = {"low": 1.0, "medium": 0.7, "high": 0.4}
IMPACT_FULL_AT = 0.5  # an opportunity worth 50% of ARR scores impact 100

Opportunity = Dict[str, Any]


def opportunity(category: str, kind: str, revenue: float, effort: str, why: str, arr: float, **extra: Any) -> Opportunity:
    impact = clamp(ratio(revenue, IMPACT_FULL_AT * arr) * 100)
    return {
        "category": category,
        "type": kind,
        "estimated_revenue": round(revenue),
        "effort": effort,
        "priority_score": round(impact * EASE[effort], 1),
        "rationale": why,
        **extra,
    }


def seat_opportunity(arr: float, segment: str, contract: Dict[str, Any]) -> Optional[Opportunity]:
    licensed, active = contract.get("licensed_seats", 0), contract.get("active_seats", 0)
    utilisation = ratio(active, licensed)
    if utilisation < SEAT_READY_UTILISATION:
        return None
    growth = SEAT_GROWTH[segment]
    return opportunity(
        "seat_expansion", "expansion", arr * growth, "low",
        f"Seats {utilisation:.0%} used; plan for about {int(licensed * growth)} more", arr,
    )


def tier_opportunity(arr: float, contract: Dict[str, Any]) -> Optional[Opportunity]:
    current = str(contract.get("plan_tier", "")).lower()
    if current not in TIER_MULTIPLIER:
        return None
    higher = sorted(
        (TIER_MULTIPLIER[t.lower()], t) for t in contract.get("available_tiers", [])
        if t.lower() in TIER_MULTIPLIER and TIER_MULTIPLIER[t.lower()] > TIER_MULTIPLIER[current]
    )
    if not higher:
        return None
    multiplier, target = higher[0]  # next tier up, never skip
    uplift = arr / TIER_MULTIPLIER[current] * multiplier - arr
    return opportunity(
        "tier_upgrade", "upsell", uplift, "medium",
        f"Move {current} to {target}: +{money(uplift)} ARR", arr, target_tier=target,
    )


def module_opportunities(arr: float, usage: Dict[str, Dict[str, Any]]) -> Tuple[List[Opportunity], List[Dict[str, Any]]]:
    sells: List[Opportunity] = []
    enablement: List[Dict[str, Any]] = []
    for module, state in usage.items():
        share = MODULE_SHARE.get(module.lower(), DEFAULT_MODULE_SHARE)
        if share == 0:
            continue
        if not state.get("adopted"):
            sells.append(opportunity(
                "module_cross_sell", "cross_sell", arr * share, "low",
                f"{module} not adopted: {money(arr * share)} potential", arr, module=module,
            ))
        elif state.get("usage_pct", 0) < LOW_USAGE_PCT:
            enablement.append({"module": module, "usage_pct": state.get("usage_pct", 0),
                               "action": "Train and enable first; do not sell more here"})
    return sells, enablement


def department_opportunities(arr: float, departments: Dict[str, List[str]]) -> List[Opportunity]:
    current = departments.get("current", [])
    held = {d.lower() for d in current}
    per_department = ratio(arr, max(len(current), 1)) * NEW_DEPARTMENT_DISCOUNT
    return [
        opportunity(
            "department_expansion", "expansion", per_department, "high",
            f"Extend to {dept}: about {money(per_department)} ARR", arr, department=dept,
        )
        for dept in departments.get("potential", []) if dept.lower() not in held
    ]


def score_customer(customer: Dict[str, Any]) -> Dict[str, Any]:
    arr = customer.get("arr", 0)
    segment = str(customer.get("segment", "mid-market")).lower()
    if segment not in SEAT_GROWTH:
        raise SystemExit(f"error: {customer.get('customer_id')}: unknown segment '{segment}'")
    contract = customer.get("contract", {})
    usage = customer.get("product_usage", {})

    sells, enablement = module_opportunities(arr, usage)
    found = [o for o in (seat_opportunity(arr, segment, contract), tier_opportunity(arr, contract)) if o]
    found += sells + department_opportunities(arr, customer.get("departments", {}))
    found.sort(key=lambda o: o["priority_score"], reverse=True)

    adopted = [m for m in usage.values() if m.get("adopted")]
    return {
        "customer_id": customer.get("customer_id", "unknown"),
        "name": customer.get("name", "Unknown"),
        "segment": segment,
        "arr": arr,
        "adoption": {
            "modules_adopted": len(adopted),
            "modules_total": len(usage),
            "avg_adopted_usage_pct": round(ratio(sum(m.get("usage_pct", 0) for m in adopted), len(adopted)), 1),
            "seat_utilisation_pct": round(ratio(contract.get("active_seats", 0), contract.get("licensed_seats", 0)) * 100, 1),
        },
        "total_estimated_revenue": sum(o["estimated_revenue"] for o in found),
        "opportunities": found,
        "enablement_needs": enablement,
    }


def render_text(results: List[Dict[str, Any]], total: int) -> str:
    lines = ["EXPANSION REPORT", f"{len(results)} accounts | potential {money(total)}", ""]
    for r in results:
        a = r["adoption"]
        lines.append(
            f"{r['name']} ({r['customer_id']}) {r['segment']} {money(r['arr'])}  potential {money(r['total_estimated_revenue'])}  "
            f"modules {a['modules_adopted']}/{a['modules_total']}  seats {a['seat_utilisation_pct']}%"
        )
        for i, o in enumerate(r["opportunities"], 1):
            lines.append(f"  {i}. [{o['type']}] {o['category']}  {money(o['estimated_revenue'])}  effort {o['effort']}  priority {o['priority_score']}")
            lines.append(f"     {o['rationale']}")
        lines.extend(f"  enable: {e['module']} at {e['usage_pct']}%" for e in r["enablement_needs"])
    return "\n".join(lines)


def main() -> None:
    parser = base_parser("Rank expansion opportunities by impact and ease.", "JSON file with a 'customers' list")
    args = parser.parse_args()

    results = [score_customer(c) for c in load_records(args.input_file, "customers")]
    results.sort(key=lambda r: r["total_estimated_revenue"], reverse=True)
    total = sum(r["total_estimated_revenue"] for r in results)

    if args.fmt == "json":
        print(json.dumps({"report": "expansion", "total_estimated_revenue": total, "customers": results}, indent=2))
    else:
        print(render_text(results, total))


if __name__ == "__main__":
    main()
