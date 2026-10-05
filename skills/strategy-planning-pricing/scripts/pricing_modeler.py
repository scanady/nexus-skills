#!/usr/bin/env python3
"""Model price changes for a subscription business before anyone commits to one.

Usage:
    python3 pricing_modeler.py --input pricing.json [--format md|json]

Reports:
  1. Current state: MRR, ARPU, gross margin, price floor from target margin.
  2. Conversion signal: reads the funnel rate against benchmarks for its funnel type.
  3. Increase scenarios: 12-month MRR per increase level, with the existing base
     handled by the chosen rollout (all, new_only, or grandfather after N months).
  4. Break-even churn: the share of the base you can lose and still keep MRR flat.
  5. Tier anchors: entry floor, middle and top multiples, charm-rounded.
  6. Proactive flags: churn, tier crowding, single plan, stale price.

Spec (see assets/pricing-sample.json):
    plans: [{name, price, customers}], monthly_new_customers, monthly_churn_pct,
    funnel: {type: trial|freemium|demo, conversion_pct}, cogs_per_customer,
    target_gross_margin_pct, competitor_prices[], months_since_last_increase,
    scenarios_pct (default [0, 5, 10, 20, 30]),
    rollout: {mode: all|new_only|grandfather, grandfather_months},
    assumptions: {base_churn_per_10pct, new_customer_loss_per_10pct}

Every number from "assumptions" is a guess until a test replaces it. The report says so.
"""
import argparse
import json
import math
import sys

MONTHS = 12
DEFAULT_ASSUMPTIONS = {
    # One-time extra churn of the existing base for each 10% increase (2 points).
    "base_churn_per_10pct": 0.02,
    # Drop in new-customer volume for each 10% increase on new prices (5%).
    "new_customer_loss_per_10pct": 0.05,
}
# Funnel benchmarks: (upper bound of rate in percent, signal, note).
FUNNEL_BANDS = {
    "trial": [(10, "high-friction", "Below 10%. Check trial onboarding and ICP fit before you cut price."),
              (15, "possible-overpricing", "10-15%. Price may cause friction. Test value messaging first."),
              (30, "healthy", "15-30%. Normal range. Work on packaging and the value metric."),
              (40, "possible-underpricing", "30-40%. Room to test a 10-15% increase on new customers."),
              (101, "strong-underpricing", "Above 40%. Strong sign of underpricing. Test 20-30% on new customers.")],
    "freemium": [(1, "high-friction", "Below 1%. Free tier gives too much, or paid value is unclear."),
                 (2, "weak", "1-2%. Rarely covers the cost of free users at scale."),
                 (5, "healthy", "2-5%. Viable at scale."),
                 (101, "possible-underpricing", "Above 5%. Free tier may be too thin or paid price too low.")],
    "demo": [(15, "high-friction", "Below 15% demo-to-close. Check qualification before price."),
             (30, "healthy", "15-30%. Normal for sales-led deals."),
             (101, "possible-underpricing", "Above 30%. Little price pushback. Raise list price or cut discounts.")],
}


def charm(price):
    """Smallest familiar price (4.99, 49, 129, 299) at or above the input, so a floor is never broken."""
    if price < 2:
        return round(price, 2)
    if price < 10:
        return math.ceil(price + 0.01) - 0.01
    step = 5 if price < 50 else 10 if price < 200 else 50 if price < 1000 else 100
    return math.ceil((price + 1) / step) * step - 1


def current_state(spec):
    plans = spec["plans"]
    customers = sum(p["customers"] for p in plans)
    mrr = sum(p["price"] * p["customers"] for p in plans)
    arpu = mrr / customers if customers else 0
    cogs = spec.get("cogs_per_customer", 0)
    target = spec.get("target_gross_margin_pct", 75) / 100
    return {"customers": customers, "mrr": round(mrr), "arpu": round(arpu, 2),
            "gross_margin_pct": round((arpu - cogs) / arpu * 100, 1) if arpu else None,
            "price_floor": round(cogs / (1 - target), 2)}


def conversion_signal(funnel):
    if not funnel:
        return None
    kind, rate = funnel.get("type", "trial"), funnel["conversion_pct"]
    if kind not in FUNNEL_BANDS:
        sys.exit(f"error: funnel.type must be one of {', '.join(FUNNEL_BANDS)}")
    signal, note = next((s, n) for upper, s, n in FUNNEL_BANDS[kind] if rate < upper)
    return {"funnel": kind, "conversion_pct": rate, "signal": signal, "note": note}


def project(spec, state, inc_pct, assume):
    """Month-by-month MRR for one increase level. Returns the scenario row."""
    inc = inc_pct / 100
    rollout = spec.get("rollout", {"mode": "new_only"})
    mode = rollout.get("mode", "new_only")
    switch_month = {"all": 1, "new_only": None, "grandfather": rollout.get("grandfather_months", 3) + 1}[mode]
    churn = spec["monthly_churn_pct"] / 100
    arpu = state["arpu"]
    new_per_month = spec["monthly_new_customers"] * (1 - assume["new_customer_loss_per_10pct"] * inc_pct / 10)
    base, new = float(state["customers"]), 0.0
    base_price = arpu
    series = []
    for month in range(1, MONTHS + 1):
        if month == switch_month and inc > 0:
            base *= 1 - assume["base_churn_per_10pct"] * inc_pct / 10
            base_price = arpu * (1 + inc)
        series.append(base * base_price + new * arpu * (1 + inc))
        base *= 1 - churn
        new = new * (1 - churn) + new_per_month
    return {"increase_pct": inc_pct, "month_12_mrr": round(series[-1]), "revenue_12mo": round(sum(series)),
            "break_even_base_loss_pct": round(inc / (1 + inc) * 100, 1)}


def retention_table(state, levels):
    """Immediate MRR if the whole base moves to the new price at each retention level."""
    return [{"increase_pct": inc, **{f"retain_{r}": round(state["mrr"] * (1 + inc / 100) * r / 100) for r in (100, 90, 80, 70)}}
            for inc in levels if inc > 0]


def tier_anchors(spec, state):
    comps = sorted(spec.get("competitor_prices", []))
    entry = max(state["price_floor"], comps[0] * 0.9 if comps else state["arpu"] * 0.5)
    return {"entry": charm(entry), "middle": charm(entry * 2.5), "top": charm(entry * 6),
            "competitor_range": [comps[0], comps[-1]] if comps else None,
            "rule": "Entry >= price floor and near the low end of the market. Middle 2-3x entry. Top 2-3x middle."}


def flags(spec, state, signal):
    out = []
    if spec["monthly_churn_pct"] > 5:
        out.append("Monthly churn above 5%. Fix retention before any increase. An increase speeds up churners.")
    if len(spec["plans"]) == 1:
        out.append("One plan only. No anchor and no upgrade path. Add tiers before you change price.")
    for p in spec["plans"]:
        share = p["customers"] / state["customers"]
        if share > 0.7 and len(spec["plans"]) > 1:
            out.append(f"{share:.0%} of customers sit on {p['name']}. Tiers do not separate segments. Review the value metric and gates.")
    if spec.get("months_since_last_increase", 0) >= 24:
        out.append("No price change in 2+ years. Cost inflation alone supports a review.")
    if state["gross_margin_pct"] is not None and state["gross_margin_pct"] < spec.get("target_gross_margin_pct", 75):
        out.append(f"Gross margin {state['gross_margin_pct']}% is below target. The lowest plan may sit under the price floor.")
    for p in spec["plans"]:
        if p["price"] < state["price_floor"]:
            out.append(f"{p['name']} at {p['price']} is below the price floor {state['price_floor']}.")
    if signal and signal["signal"] in ("possible-underpricing", "strong-underpricing") and spec["monthly_churn_pct"] <= 5:
        out.append("Conversion signal and churn both allow an increase test. Start with new customers only.")
    return out


def run(spec):
    assume = {**DEFAULT_ASSUMPTIONS, **spec.get("assumptions", {})}
    state = current_state(spec)
    signal = conversion_signal(spec.get("funnel"))
    levels = spec.get("scenarios_pct", [0, 5, 10, 20, 30])
    scenarios = [project(spec, state, inc, assume) for inc in levels]
    baseline = next((s for s in scenarios if s["increase_pct"] == 0), None) or project(spec, state, 0, assume)
    for s in scenarios:
        s["delta_vs_current_12mo"] = s["revenue_12mo"] - baseline["revenue_12mo"]
    return {"current": state, "conversion_signal": signal, "rollout": spec.get("rollout", {"mode": "new_only"}),
            "assumptions": assume, "scenarios": scenarios, "retention_table": retention_table(state, levels),
            "tier_anchors": tier_anchors(spec, state), "flags": flags(spec, state, signal)}


def money(x):
    return f"{x:,.0f}"


def render_markdown(r):
    c = r["current"]
    lines = ["# Pricing model", "",
             f"- Customers {c['customers']:,}. MRR {money(c['mrr'])}. ARPU {c['arpu']}.",
             f"- Gross margin {c['gross_margin_pct']}%. Price floor at target margin: {c['price_floor']}."]
    if r["conversion_signal"]:
        s = r["conversion_signal"]
        lines += [f"- Conversion ({s['funnel']}) {s['conversion_pct']}%: **{s['signal']}**. {s['note']}"]
    ro = r["rollout"]
    lines += ["", f"## Increase scenarios (rollout: {ro.get('mode')}"
              + (f", {ro.get('grandfather_months', 3)} months" if ro.get("mode") == "grandfather" else "") + ")", "",
              "| Increase | Month-12 MRR | 12-mo revenue | Delta vs current | Break-even base loss |",
              "|---|---|---|---|---|"]
    for s in r["scenarios"]:
        lines.append(f"| {s['increase_pct']}% | {money(s['month_12_mrr'])} | {money(s['revenue_12mo'])} "
                     f"| {s['delta_vs_current_12mo']:+,} | {s['break_even_base_loss_pct']}% |")
    if r["retention_table"]:
        lines += ["", "## Immediate MRR if the whole base moves", "",
                  "| Increase | 100% retained | 90% | 80% | 70% |", "|---|---|---|---|---|"]
        for t in r["retention_table"]:
            lines.append(f"| {t['increase_pct']}% | {money(t['retain_100'])} | {money(t['retain_90'])} "
                         f"| {money(t['retain_80'])} | {money(t['retain_70'])} |")
        lines.append(f"\nCurrent MRR is {money(c['mrr'])}. Any cell below it loses money.")
    a = r["tier_anchors"]
    lines += ["", "## Tier anchors", "", f"Entry {a['entry']}, middle {a['middle']}, top {a['top']}. "
              f"Competitor range {a['competitor_range']}. {a['rule']}"]
    if r["flags"]:
        lines += ["", "## Flags", ""] + [f"- {f}" for f in r["flags"]]
    a = r["assumptions"]
    lines += ["", "## Assumptions (replace with test data)", "",
              f"- Each 10% increase removes {a['base_churn_per_10pct']:.0%} of the existing base once, when it moves.",
              f"- Each 10% increase cuts new-customer volume by {a['new_customer_loss_per_10pct']:.0%}.",
              "- Churn rate and lead volume otherwise hold constant."]
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", required=True)
    ap.add_argument("--format", choices=["md", "json"], default="md")
    args = ap.parse_args()
    with open(args.input, encoding="utf-8") as f:
        spec = json.load(f)
    if not spec.get("plans"):
        sys.exit("error: spec needs at least one plan")
    result = run(spec)
    sys.stdout.write(json.dumps(result, indent=2) + "\n" if args.format == "json" else render_markdown(result))


if __name__ == "__main__":
    main()
