#!/usr/bin/env python3
"""Coverage sizer: CSMs needed per tier, manager triggers, 12-month hiring plan.

Required CSMs for a tier = the larger of ARR-per-CSM and accounts-per-CSM
limits. The plan projects the book linearly over four quarters and schedules
each hire one quarter before the capacity is needed, because a new CSM takes
months to ramp.

Book schema:
  {"book": {"strategic": {"customers": 8, "arr": 3200000, "csms": 1}, "enterprise": {...},
            "mid_market": {...}, "smb": {...}}, "growth_pct": 0.40}

Usage:
    python coverage_sizer.py book.json
    python coverage_sizer.py book.json --format json
"""

import json
import math
import sys
from typing import Any, Dict, List

from cs_common import base_parser, load_json, money

# tier -> model, ARR per CSM, accounts per CSM, fully loaded yearly cost per CSM
MODELS: Dict[str, Dict[str, Any]] = {
    "strategic": {"model": "Named CSM + executive sponsor", "arr_per_csm": 800_000, "accounts_per_csm": 8, "cost": 220_000},
    "enterprise": {"model": "Named CSM", "arr_per_csm": 1_200_000, "accounts_per_csm": 25, "cost": 180_000},
    "mid_market": {"model": "Pooled CSM + automation", "arr_per_csm": 3_500_000, "accounts_per_csm": 150, "cost": 140_000},
    "smb": {"model": "Tech-touch + self-serve", "arr_per_csm": 10_000_000, "accounts_per_csm": 1_000, "cost": 110_000},
}
TIER_MANAGER_AT = 5  # CSMs in one tier that need their own manager
TEAM_MANAGER_AT = 8  # CSMs in the whole team that need a manager


def csms_needed(customers: float, arr: float, model: Dict[str, Any]) -> Dict[str, Any]:
    by_arr = math.ceil(arr / model["arr_per_csm"])
    by_accounts = math.ceil(customers / model["accounts_per_csm"])
    return {"needed": max(by_arr, by_accounts), "binding": "arr" if by_arr >= by_accounts else "accounts"}


def grown(book: Dict[str, Any], factor: float) -> Dict[str, float]:
    return {"customers": math.ceil(book.get("customers", 0) * factor), "arr": book.get("arr", 0) * factor}


def size_tier(name: str, book: Dict[str, Any], growth: float) -> Dict[str, Any]:
    model = MODELS[name]
    now = csms_needed(book.get("customers", 0), book.get("arr", 0), model)
    have = book.get("csms", 0)

    plan: List[Dict[str, Any]] = []
    capacity = have  # CSMs in seat plus hires already scheduled
    for quarter in range(5):  # 0 = today, 1-4 = quarter ends
        projected = grown(book, 1 + growth * quarter / 4)
        need = csms_needed(projected["customers"], projected["arr"], model)["needed"]
        for _ in range(max(need - capacity, 0)):
            plan.append({
                "start_by": "now" if quarter <= 1 else f"Q{quarter - 1}",
                "needed_in": "now" if quarter == 0 else f"Q{quarter}",
                "tier": name,
                "role": f"CSM ({model['model']})",
            })
        capacity = max(capacity, need)

    year_end = need  # the loop's last pass is the 12-month projection
    return {
        "tier": name,
        "model": model["model"],
        "customers": book.get("customers", 0),
        "arr": book.get("arr", 0),
        "csms_now": have,
        "csms_needed_now": now["needed"],
        "binding_constraint": now["binding"],
        "gap_now": now["needed"] - have,
        "csms_needed_12mo": year_end,
        "gap_12mo": year_end - have,
        "yearly_cost_12mo": year_end * model["cost"],
        "hires": plan,
    }


def manager_triggers(tiers: List[Dict[str, Any]]) -> List[str]:
    out = [f"{t['tier']}: {t['csms_needed_12mo']} CSMs in one tier; add a tier manager" for t in tiers if t["csms_needed_12mo"] >= TIER_MANAGER_AT]
    total = sum(t["csms_needed_12mo"] for t in tiers)
    if total >= TEAM_MANAGER_AT:
        out.append(f"team: {total} CSMs in 12 months; add a CS manager or head of CS")
    return out


def render_text(report: Dict[str, Any]) -> str:
    lines = [f"CS COVERAGE (book growth {report['growth_pct']:.0%} over 12 months)", ""]
    for t in report["tiers"]:
        lines.append(f"{t['tier']:11} {t['model']}")
        lines.append(f"  book {t['customers']} customers / {money(t['arr'])}  binding: {t['binding_constraint']}")
        lines.append(f"  CSMs have {t['csms_now']}  need {t['csms_needed_now']} now ({t['gap_now']:+d})  need {t['csms_needed_12mo']} in 12mo ({t['gap_12mo']:+d})")
    lines.append("")
    lines.extend(f"Manager trigger - {m}" for m in report["manager_triggers"])
    lines.extend(f"Hire: start by {h['start_by']} for {h['needed_in']}: {h['role']}" for t in report["tiers"] for h in t["hires"])
    lines.append(f"\nCSM cost in 12 months: {money(sum(t['yearly_cost_12mo'] for t in report['tiers']))}")
    lines.append("Ratios are starting points. Re-run each quarter with fresh book data.")
    return "\n".join(lines)


def main() -> None:
    parser = base_parser("Size the CS team per coverage model.", "JSON file with a 'book' object")
    args = parser.parse_args()

    payload = load_json(args.input_file)
    book = payload.get("book")
    if not book:
        sys.exit("error: input needs a 'book' object")
    unknown = set(book) - set(MODELS)
    if unknown:
        sys.exit(f"error: unknown tiers {sorted(unknown)}; use {sorted(MODELS)}")

    growth = payload.get("growth_pct", 0)
    tiers = [size_tier(name, book[name], growth) for name in MODELS if name in book]
    report = {"growth_pct": growth, "tiers": tiers, "manager_triggers": manager_triggers(tiers)}
    print(json.dumps(report, indent=2) if args.fmt == "json" else render_text(report))


if __name__ == "__main__":
    main()
