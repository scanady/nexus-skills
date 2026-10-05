#!/usr/bin/env python3
"""Churn-risk scorer: behavioural signals, renewal urgency, risk tiers.

Five signal groups score 0-100 (higher = more risk), blend with fixed weights,
then a renewal-proximity multiplier lifts accounts that renew soon. The tier
decides the intervention. Every warning carries a severity so the worst
evidence prints first.

Usage:
    python churn_risk_scorer.py portfolio.json
    python churn_risk_scorer.py portfolio.json --format json --as-of 2026-03-01
"""

import json
from datetime import date
from typing import Any, Callable, Dict, List, Optional, Tuple

from cs_common import base_parser, clamp, load_records, money, parse_date

SIGNAL_WEIGHTS = {
    "usage_decline": 0.30,
    "engagement_drop": 0.25,
    "support_issues": 0.20,
    "relationship_signals": 0.15,
    "commercial_factors": 0.10,
}

# (tier, minimum score, first action). Checked top-down.
TIERS: List[Tuple[str, int, str]] = [
    ("critical", 80, "Executive escalation within 48 hours"),
    ("high", 60, "CSM intervention within 1 week"),
    ("medium", 40, "Proactive outreach within 2 weeks"),
    ("low", 0, "Standard monitoring"),
]

# Renewal proximity multipliers: (days remaining at most, multiplier).
URGENCY: List[Tuple[int, float]] = [(30, 1.5), (60, 1.35), (90, 1.2), (180, 1.1)]

PLAYBOOKS: Dict[str, List[str]] = {
    "critical": [
        "Executive-to-executive call within 48 hours",
        "Write a save plan with dated value milestones",
        "Pre-approve concessions or contract restructure",
        "Assign a rescue team: CSM, solutions engineer, support lead",
        "Run a daily internal stand-up until stable",
        "Prepare a competitive defence if a rival is involved",
    ],
    "high": [
        "Dedicated CSM call within 1 week (not a routine check-in)",
        "Root-cause the weakest dimensions",
        "Build a 30-day recovery plan with weekly checkpoints",
        "Re-engage the executive sponsor",
        "Fast-track open bugs and feature requests",
        "Touch weekly until the score improves",
    ],
    "medium": [
        "Value check-in within 2 weeks",
        "Share relevant customer wins and best practices",
        "Offer training on under-used features",
        "Compare usage with the success plan goals",
        "Monitor every two weeks",
    ],
    "low": [
        "Keep the standard touch cadence",
        "Share product updates",
        "Review the score trend monthly",
        "Start renewal prep 90 days out",
    ],
}

SEVERITY_RANK = {"critical": 0, "high": 1, "medium": 2}
SATISFACTION_RISK = {"improving": 10.0, "stable": 30.0, "declining": 70.0, "critical": 95.0}

# Numeric warning rules: field -> (comparison, [(limit, severity, message)]), strictest first.
Rule = Tuple[Callable[[float, float], bool], List[Tuple[float, str, str]]]
LE: Callable[[float, float], bool] = lambda v, limit: v <= limit
GE: Callable[[float, float], bool] = lambda v, limit: v >= limit
NUMERIC_RULES: Dict[str, Rule] = {
    "login_trend": (LE, [(-20, "critical", "Logins down {a:g}%"), (-10, "high", "Logins down {a:g}%"), (-5, "medium", "Logins down {a:g}%")]),
    "feature_adoption_change": (LE, [(-15, "high", "Feature adoption down {a:g}%"), (-5, "medium", "Feature adoption down {a:g}%")]),
    "dau_mau_change": (LE, [(-0.10, "high", "DAU/MAU fell {a:.2f}")]),
    "meeting_cancellations": (GE, [(3, "critical", "{a:g} meeting cancellations: customer disengaging"), (2, "high", "{a:g} recent meeting cancellations")]),
    "response_time_days": (GE, [(7, "critical", "Customer silent for {a:g} days"), (4, "high", "Customer reply time up to {a:g} days")]),
    "nps_change": (LE, [(-4, "critical", "NPS down {a:g} points"), (-2, "high", "NPS down {a:g} points")]),
    "unresolved_critical": (GE, [(2, "critical", "{a:g} unresolved critical tickets"), (1, "high", "Unresolved critical ticket")]),
    "open_escalations": (GE, [(2, "high", "{a:g} open escalations"), (1, "medium", "Open escalation")]),
    "competitor_mentions": (GE, [(3, "critical", "Competitor named {a:g} times"), (1, "medium", "Competitor named {a:g} time(s)")]),
}

# Boolean warning rules: field -> (severity, message).
FLAG_RULES: Dict[str, Tuple[str, str]] = {
    "champion_left": ("critical", "Internal champion left the customer"),
    "sponsor_change": ("high", "Executive sponsor changed"),
    "pricing_complaints": ("high", "Customer raised pricing complaints"),
    "budget_cuts_mentioned": ("high", "Customer mentioned budget cuts"),
}


def warnings_for(group: Dict[str, Any]) -> List[Dict[str, str]]:
    found: List[Dict[str, str]] = []
    for field, (compare, rules) in NUMERIC_RULES.items():
        value = group.get(field)
        if value is None:
            continue
        for limit, severity, message in rules:
            if compare(value, limit):
                found.append({"severity": severity, "signal": message.format(a=abs(value))})
                break
    for field, (severity, message) in FLAG_RULES.items():
        if group.get(field):
            found.append({"severity": severity, "signal": message})
    contract = str(group.get("contract_type", "annual")).lower()
    if contract == "month-to-month":
        found.append({"severity": "medium", "signal": "Month-to-month contract: low switching cost"})
    sat = str(group.get("satisfaction_trend", "stable")).lower()
    if sat in ("critical", "declining"):
        found.append({"severity": "critical" if sat == "critical" else "high", "signal": f"Support satisfaction {sat}"})
    return found


def decline(value: float, scale: float) -> float:
    """Risk from a decline: only negative values count."""
    return clamp(abs(min(value, 0)) * scale)


def signal_scores(customer: Dict[str, Any]) -> Dict[str, float]:
    usage = customer.get("usage_decline", {})
    engage = customer.get("engagement_drop", {})
    support = customer.get("support_issues", {})
    relation = customer.get("relationship_signals", {})
    commercial = customer.get("commercial_factors", {})

    competitors = relation.get("competitor_mentions", 0)
    contract_points = {"month-to-month": 30.0, "quarterly": 15.0}.get(
        str(commercial.get("contract_type", "annual")).lower(), 0.0
    )
    return {
        "usage_decline": (
            decline(usage.get("login_trend", 0), 3.0) * 0.40
            + decline(usage.get("feature_adoption_change", 0), 4.0) * 0.35
            + decline(usage.get("dau_mau_change", 0), 500.0) * 0.25
        ),
        "engagement_drop": (
            clamp(engage.get("meeting_cancellations", 0) * 25.0) * 0.30
            + clamp((engage.get("response_time_days", 1) - 1) * 15.0) * 0.35
            + decline(engage.get("nps_change", 0), 20.0) * 0.35
        ),
        "support_issues": (
            clamp(support.get("open_escalations", 0) * 35.0) * 0.35
            + clamp(support.get("unresolved_critical", 0) * 50.0) * 0.35
            + SATISFACTION_RISK.get(str(support.get("satisfaction_trend", "stable")).lower(), 30.0) * 0.30
        ),
        "relationship_signals": clamp(
            (45.0 if relation.get("champion_left") else 0.0)
            + (30.0 if relation.get("sponsor_change") else 0.0)
            + (35.0 if competitors >= 3 else competitors * 12.0)
        ),
        "commercial_factors": clamp(
            contract_points
            + (35.0 if commercial.get("pricing_complaints") else 0.0)
            + (40.0 if commercial.get("budget_cuts_mentioned") else 0.0)
        ),
    }


def urgency(days_left: Optional[int]) -> float:
    if days_left is None:
        return 1.0
    for limit, multiplier in URGENCY:
        if days_left <= limit:
            return multiplier
    return 1.0


def tier_for(score: float) -> Tuple[str, str]:
    for name, minimum, action in TIERS:
        if score >= minimum:
            return name, action
    raise ValueError("unreachable: lowest tier minimum is 0")


def score_customer(customer: Dict[str, Any], as_of: date) -> Dict[str, Any]:
    scores = signal_scores(customer)
    raw = sum(scores[name] * weight for name, weight in SIGNAL_WEIGHTS.items())

    end = parse_date(customer.get("contract_end_date"))
    days_left = max((end - as_of).days, 0) if end else None
    multiplier = urgency(days_left)
    adjusted = round(clamp(raw * multiplier), 1)
    tier, first_action = tier_for(adjusted)

    groups: Dict[str, Any] = {}
    for key in ("usage_decline", "engagement_drop", "support_issues", "relationship_signals", "commercial_factors"):
        groups.update(customer.get(key, {}))
    warnings = sorted(warnings_for(groups), key=lambda w: SEVERITY_RANK[w["severity"]])

    return {
        "customer_id": customer.get("customer_id", "unknown"),
        "name": customer.get("name", "Unknown"),
        "segment": customer.get("segment", "unknown"),
        "arr": customer.get("arr", 0),
        "risk_score": adjusted,
        "raw_score": round(raw, 1),
        "tier": tier,
        "first_action": first_action,
        "urgency_multiplier": multiplier,
        "days_to_renewal": days_left,
        "signal_scores": {name: round(score, 1) for name, score in scores.items()},
        "warnings": warnings,
        "playbook": PLAYBOOKS[tier],
    }


def summarise(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "total_customers": len(results),
        **{f"{name}_count": sum(1 for r in results if r["tier"] == name) for name, _, _ in TIERS},
        "arr_at_risk": sum(r["arr"] for r in results if r["tier"] in ("critical", "high")),
    }


def render_text(results: List[Dict[str, Any]], summary: Dict[str, Any]) -> str:
    lines = [
        "CHURN RISK REPORT",
        f"{summary['total_customers']} accounts | critical {summary['critical_count']} high {summary['high_count']} "
        f"medium {summary['medium_count']} low {summary['low_count']} | ARR at risk (critical+high) {money(summary['arr_at_risk'])}",
        "",
    ]
    for r in results:
        renewal = f"{r['days_to_renewal']}d" if r["days_to_renewal"] is not None else "n/a"
        boost = f" x{r['urgency_multiplier']}" if r["urgency_multiplier"] > 1 else ""
        lines.append(
            f"[{r['tier'].upper():8}] {r['name']} ({r['customer_id']}) {r['segment']} {money(r['arr'])}  "
            f"risk {r['risk_score']}{boost}  renews {renewal}"
        )
        lines.append(f"           first action: {r['first_action']}")
        lines.extend(f"           [{w['severity']}] {w['signal']}" for w in r["warnings"])
    return "\n".join(lines)


def main() -> None:
    parser = base_parser("Score churn risk from behavioural signals.", "JSON file with a 'customers' list")
    parser.add_argument("--as-of", help="Reference date YYYY-MM-DD for renewal math (default: today)")
    args = parser.parse_args()

    as_of = parse_date(args.as_of) or date.today()
    results = [score_customer(c, as_of) for c in load_records(args.input_file, "customers")]
    results.sort(key=lambda r: r["risk_score"], reverse=True)
    summary = summarise(results)

    if args.fmt == "json":
        print(json.dumps({"report": "churn_risk", "as_of": as_of.isoformat(), "summary": summary, "customers": results}, indent=2))
    else:
        print(render_text(results, summary))


if __name__ == "__main__":
    main()
