#!/usr/bin/env python3
"""Retention decomposer: GRR, NRR, logo retention, churn causes, cohort drift.

Splits NRR into its parts so expansion cannot hide churn, bands each metric
against stage thresholds, flags a leaky bucket (NRR at 100% or more with weak
GRR), tallies churn causes in the 7-category taxonomy, and checks whether newer
cohorts retain worse than older ones.

Cohort schema (all ARR in the same currency, measured at the 12-month mark):
  name, starting_arr, churned_arr, contraction_arr, expansion_arr,
  starting_logos, churned_logos, churn_reasons {category: logo count}

Usage:
    python retention_decomposer.py cohorts.json --stage growth
    python retention_decomposer.py cohorts.json --stage scale --format json
"""

import json
import sys
from typing import Any, Dict, List

from cs_common import base_parser, load_records, ratio

# stage -> metric -> (healthy at least, concerning at least). Below concerning is critical.
THRESHOLDS: Dict[str, Dict[str, tuple]] = {
    "seed": {"grr": (0.85, 0.75), "nrr": (1.00, 0.95), "logo": (0.80, 0.70)},
    "growth": {"grr": (0.90, 0.85), "nrr": (1.10, 1.00), "logo": (0.85, 0.80)},
    "scale": {"grr": (0.95, 0.90), "nrr": (1.20, 1.10), "logo": (0.90, 0.85)},
}

CHURN_CATEGORIES = {
    "product_fit": "Product did not solve the real job",
    "competitor_loss": "Lost to a rival on fit or price",
    "no_value_realized": "Never reached first value; onboarding gap",
    "pricing": "Too expensive or low perceived value",
    "champion_left": "Internal champion left or changed role",
    "company_event": "Merger, layoffs, or shutdown at the customer",
    "tactical_failure": "Service or support failure",
}
PREVENTABLE = ("product_fit", "no_value_realized", "tactical_failure")
BAND_RANK = {"healthy": 0, "concerning": 1, "critical": 2}
DRIFT_POINTS = 0.02  # GRR move versus earlier cohorts that counts as drift


def band(value: float, limits: tuple) -> str:
    if value >= limits[0]:
        return "healthy"
    return "concerning" if value >= limits[1] else "critical"


def check_cohort(cohort: Dict[str, Any]) -> None:
    name = cohort.get("name", "?")
    start = cohort.get("starting_arr", 0)
    if start <= 0:
        sys.exit(f"error: cohort {name}: starting_arr must be positive")
    if cohort.get("churned_arr", 0) + cohort.get("contraction_arr", 0) > start:
        sys.exit(f"error: cohort {name}: churned_arr + contraction_arr exceeds starting_arr")


def decompose(cohort: Dict[str, Any], limits: Dict[str, tuple]) -> Dict[str, Any]:
    check_cohort(cohort)
    start = cohort["starting_arr"]
    churn, contraction, expansion = (cohort.get(k, 0) for k in ("churned_arr", "contraction_arr", "expansion_arr"))
    logos = cohort.get("starting_logos", 0)
    churned_logos = cohort.get("churned_logos", 0)

    grr = (start - churn - contraction) / start
    nrr = grr + expansion / start
    logo = 1 - ratio(churned_logos, logos) if logos else None

    bands = {"grr": band(grr, limits["grr"]), "nrr": band(nrr, limits["nrr"])}
    if logo is not None:
        bands["logo"] = band(logo, limits["logo"])

    leaky = nrr >= 1.0 and grr < limits["grr"][1]
    overall = "leaky_bucket" if leaky else max(bands.values(), key=BAND_RANK.__getitem__)
    reasons = cohort.get("churn_reasons", {})
    reason_total = sum(reasons.values())

    return {
        "cohort": cohort.get("name"),
        "grr": round(grr, 4),
        "nrr": round(nrr, 4),
        "logo_retention": round(logo, 4) if logo is not None else None,
        "churn_pct": round(churn / start * 100, 1),
        "contraction_pct": round(contraction / start * 100, 1),
        "expansion_pct": round(expansion / start * 100, 1),
        "bands": bands,
        "overall": overall,
        "note": "Expansion is masking churn. Fix gross retention before scaling acquisition." if leaky else "",
        "reason_gap": churned_logos - reason_total if reasons else None,
        "churn_reasons": reasons,
    }


def churn_summary(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    totals = {category: 0 for category in CHURN_CATEGORIES}
    for r in results:
        for category, count in r["churn_reasons"].items():
            if category not in totals:
                sys.exit(f"error: unknown churn category '{category}'")
            totals[category] += count
    total = sum(totals.values())
    if total == 0:
        return {"total_logos_churned": 0, "top_drivers": [], "preventable_pct": None, "leverage": "no churn reasons supplied"}

    ranked = sorted(((c, n) for c, n in totals.items() if n), key=lambda item: -item[1])[:3]
    preventable = round(sum(totals[c] for c in PREVENTABLE) / total * 100, 1)
    leverage = "CS has clear leverage" if preventable > 50 else "mostly structural" if preventable < 30 else "mixed"
    return {
        "total_logos_churned": total,
        "top_drivers": [{"category": c, "meaning": CHURN_CATEGORIES[c], "count": n, "pct": round(n / total * 100, 1)} for c, n in ranked],
        "preventable_pct": preventable,
        "leverage": leverage,
    }


def cohort_drift(results: List[Dict[str, Any]]) -> str:
    """Compare the newest cohort's GRR with the mean of the earlier ones."""
    if len(results) < 2:
        return "needs 2+ cohorts"
    earlier = sum(r["grr"] for r in results[:-1]) / (len(results) - 1)
    delta = results[-1]["grr"] - earlier
    if delta > DRIFT_POINTS:
        return "improving"
    return "degrading" if delta < -DRIFT_POINTS else "flat"


def render_text(report: Dict[str, Any]) -> str:
    lines = [f"RETENTION DECOMPOSITION (stage: {report['stage']})", ""]
    for c in report["cohorts"]:
        logo = f"{c['logo_retention']:.1%}" if c["logo_retention"] is not None else "n/a"
        lines.append(f"{c['cohort']}: {c['overall'].upper()}")
        lines.append(f"  GRR {c['grr']:.1%} [{c['bands']['grr']}]  NRR {c['nrr']:.1%} [{c['bands']['nrr']}]  logo {logo}")
        lines.append(f"  churn {c['churn_pct']}%  contraction {c['contraction_pct']}%  expansion {c['expansion_pct']}%")
        if c["note"]:
            lines.append(f"  ! {c['note']}")
        if c["reason_gap"]:
            lines.append(f"  ! churn reasons miss {c['reason_gap']} churned logos")
    lines.append(f"\nCohort drift: {report['cohort_drift']}")
    s = report["churn_summary"]
    lines.append(f"Churned logos: {s['total_logos_churned']}  preventable: {s['preventable_pct']}%  ({s['leverage']})")
    lines.extend(f"  {d['category']:18} {d['count']:>3} ({d['pct']}%) {d['meaning']}" for d in s["top_drivers"])
    return "\n".join(lines)


def main() -> None:
    parser = base_parser("Decompose retention and tally churn causes.", "JSON file with a 'cohorts' list")
    parser.add_argument("--stage", choices=sorted(THRESHOLDS), default="growth", help="Company stage for thresholds")
    args = parser.parse_args()

    limits = THRESHOLDS[args.stage]
    results = [decompose(c, limits) for c in load_records(args.input_file, "cohorts")]
    report = {"stage": args.stage, "cohorts": results, "cohort_drift": cohort_drift(results), "churn_summary": churn_summary(results)}

    print(json.dumps(report, indent=2) if args.fmt == "json" else render_text(report))


if __name__ == "__main__":
    main()
