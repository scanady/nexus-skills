#!/usr/bin/env python3
"""Rank pricing models and acquisition motions by fit before anyone picks tiers or prices.

Usage:
    python3 model_fit_scorer.py --input context.json [--profile api] [--format md|json]
    python3 model_fit_scorer.py --sample

Scores two separate questions, because freemium is an acquisition choice, not a way to bill:
  1. Monetization model: per_seat, usage, outcome, feature_tiers, hybrid.
  2. Acquisition motion: free_tier, free_trial, reverse_trial, sales_led.

Every model starts at 50. Each known fact moves the score and leaves a reason or a
trade-off. Unknown facts move nothing and appear in the report as open questions, so
a thin brief reads as a thin brief. Deterministic. Python 3 stdlib only.

Context spec (see assets/model-fit-sample.json; every field optional):
    profile              saas | api | ai | vertical | enterprise | marketplace
    acv                  average annual contract value, USD
    customers            current paying customer count
    active_user_share    0-1, share of users who create or act (rest only view)
    usage_spread         top-decile usage / median usage, e.g. 12 for 12x
    usage_volatility     low | medium | high  (month-to-month swing per customer)
    marginal_cost        low | variable  (serving cost grows with use: AI, infra, SMS)
    outcome              {measurable: bool, attribution: clean | shared | disputed}
    fixed_budget_buyer   bool, buyer needs a fixed, predictable bill
    distinct_segments    bool, segments want clearly different feature sets
    motion               self-serve | sales-led | mixed
    adoption             bottom-up | top-down
    network_effects      bool, product gets better as more people join
    time_to_value_days   days from signup to first real value
    competitor_models    list of model keys used by named competitors
"""
import argparse
import json
import sys

MODELS = ("per_seat", "usage", "outcome", "feature_tiers", "hybrid")
MOTIONS = ("free_tier", "free_trial", "reverse_trial", "sales_led")
LABELS = {
    "per_seat": "Per seat", "usage": "Usage-based", "outcome": "Outcome-based",
    "feature_tiers": "Feature tiers / flat", "hybrid": "Hybrid (platform fee + seats or usage)",
    "free_tier": "Free tier (freemium)", "free_trial": "Time-limited free trial",
    "reverse_trial": "Reverse trial", "sales_led": "Sales-led demo",
}
# Where each model lands in the Strategy Type table of SKILL.md step 4.
STRATEGY_TYPE = {
    "per_seat": "SaaS Tiered (seat limits per tier)", "usage": "Usage Tiers",
    "outcome": "Hybrid (platform fee + outcome share)", "feature_tiers": "SaaS Tiered or Package",
    "hybrid": "Hybrid",
}
# Market priors. Small on purpose: data about this business beats category habit.
PROFILES = {
    "saas": {"per_seat": 5, "feature_tiers": 5},
    "api": {"usage": 10, "per_seat": -10},
    "ai": {"usage": 5, "hybrid": 10, "per_seat": -5},
    "vertical": {"per_seat": 5, "feature_tiers": 5},
    "enterprise": {"outcome": 5, "hybrid": 5, "feature_tiers": -5},
    "marketplace": {"outcome": 10, "per_seat": -10},
}
# What each input decides; shown when the input is missing.
OPEN_QUESTIONS = {
    "active_user_share": "Do most users act, or do a few create while the rest view? Decides per seat vs creator/viewer.",
    "usage_spread": "Top-decile vs median usage? Over 10x favors usage; under 3x favors seats or tiers.",
    "marginal_cost": "Does serving cost grow with use? Variable cost pushes toward usage or hybrid.",
    "outcome": "Can you measure the customer outcome and attribute it cleanly? Gate for outcome pricing.",
    "acv": "Average annual contract value? Sets sales-led vs self-serve and outcome viability.",
    "fixed_budget_buyer": "Does the buyer need a fixed bill? Penalizes pure usage.",
    "adoption": "Bottom-up or top-down adoption? Decides free tier vs sales-led.",
    "time_to_value_days": "Days to first value? Sets trial length and reverse-trial fit.",
}


class Card:
    """Score plus the reasons behind it."""

    def __init__(self, key):
        self.key, self.score, self.fits, self.costs = key, 50, [], []

    def add(self, points, why):
        self.score += points
        (self.fits if points > 0 else self.costs).append(f"{points:+d} {why}")

    def note(self, cost):
        self.costs.append(cost)

    def as_dict(self):
        return {"key": self.key, "label": LABELS[self.key], "score": max(0, min(100, self.score)),
                "fits": self.fits, "costs": self.costs}


def known(ctx, field):
    return ctx.get(field) is not None


def score_models(ctx, profile):
    c = {k: Card(k) for k in MODELS}
    acv = ctx.get("acv")
    users = ctx.get("active_user_share")
    spread = ctx.get("usage_spread")
    volatility = ctx.get("usage_volatility")
    variable = ctx.get("marginal_cost") == "variable"
    fixed = ctx.get("fixed_budget_buyer")
    outcome = ctx.get("outcome") or {}
    customers = ctx.get("customers")

    seat = c["per_seat"]
    if users is not None:
        if users >= 0.7:
            seat.add(20, f"{users:.0%} of users act; every seat carries value.")
        elif users >= 0.4:
            seat.add(5, f"{users:.0%} of users act; seats mostly track value.")
        else:
            seat.add(-15, f"Only {users:.0%} of users act. Viewers pay for nothing; expect shared logins. Consider creator/viewer split.")
    if spread is not None:
        if spread >= 10:
            seat.add(-15, f"{spread:g}x usage spread; seat price leaves heavy-user value uncaptured.")
        elif spread <= 3:
            seat.add(10, f"{spread:g}x usage spread; usage per seat roughly flat.")
    if fixed:
        seat.add(8, "Buyer wants a fixed bill; seat count is easy to budget.")
    if acv is not None and acv >= 2400:
        seat.add(5, "Deal above ~$200/mo; seat math is normal at this size.")
    if variable:
        seat.add(-10, "Serving cost grows with use; heavy seats erode margin.")
    seat.note("Expansion follows hiring, not usage. Seat adds feel like friction.")

    use = c["usage"]
    if spread is not None:
        if spread >= 10:
            use.add(25, f"{spread:g}x usage spread; bill tracks value across a power-law base.")
        elif spread > 3:
            use.add(10, f"{spread:g}x usage spread; moderate case for metering.")
        else:
            use.add(-10, f"{spread:g}x usage spread; metering adds billing work for little upside.")
    if variable:
        use.add(15, "Serving cost grows with use; usage keeps margin per unit.")
    if volatility == "high":
        use.add(-15, "Usage swings month to month. Bill shock risk; use prepaid credits or commit + overage.")
    elif volatility == "medium":
        use.add(-5, "Some month-to-month swing; add a monthly cap or alerts.")
    if fixed:
        use.add(-10, "Buyer wants a fixed bill; pure metering fights procurement.")
    use.note("Revenue tracks usage. Forecasts harder; downturns cut revenue fast.")

    out = c["outcome"]
    if outcome and not outcome.get("measurable"):
        out.add(-25, "No measurable outcome. Outcome pricing collapses into guesswork.")
    elif outcome:
        attribution = outcome.get("attribution", "shared")
        points = {"clean": 25, "shared": 10, "disputed": -10}.get(attribution, 0)
        out.add(points, f"Outcome measurable, attribution {attribution}.")
    if acv is not None:
        if acv >= 50000:
            out.add(10, "Enterprise deal size pays for per-account value proof.")
        elif acv < 5000:
            out.add(-10, "Small deals cannot carry the cost of proving value per account.")
    if customers is not None and customers > 500:
        out.add(-10, f"{customers} customers; per-account value calibration does not scale.")
    out.note("Highest value capture. Needs instrumented proof; revenue lumpy; attribution disputes.")

    tiers = c["feature_tiers"]
    if ctx.get("distinct_segments"):
        tiers.add(15, "Segments want different feature sets; tiers separate them cleanly.")
    if fixed:
        tiers.add(10, "Buyer wants a fixed bill; a flat tier price is the simplest.")
    if spread is not None:
        if spread <= 3:
            tiers.add(10, f"{spread:g}x usage spread; flat tiers do not subsidize heavy users much.")
        elif spread >= 10:
            tiers.add(-15, f"{spread:g}x usage spread; light users subsidize heavy ones.")
    if ctx.get("motion") == "self-serve":
        tiers.add(5, "Self-serve buyers compare 2-4 tiers fast.")
    if variable:
        tiers.add(-10, "Variable serving cost under a flat price; add usage caps per tier.")
    tiers.note("Customers cluster in one tier. Expansion needs an upsell push, not growth.")

    hyb = c["hybrid"]
    if users is not None and spread is not None and users >= 0.4 and spread >= 3:
        hyb.add(15, "Both seat and usage drivers present.")
    if variable and fixed:
        hyb.add(10, "Variable cost plus fixed-bill buyer; platform fee with included usage fits both.")
    if volatility == "high":
        hyb.add(5, "Platform fee gives a revenue floor through idle months.")
    if acv is not None and acv < 1200:
        hyb.add(-15, "Deal under $100/mo; two-part pricing costs more conversion than it earns.")
    elif acv is not None and acv < 5000 and ctx.get("motion") == "self-serve":
        hyb.add(-5, "Small self-serve deal; keep the pricing page simple.")
    hyb.note("Captures more value across segments. Harder pricing page; more billing support.")

    for key in ctx.get("competitor_models") or []:
        if key in c:
            c[key].add(5, "Competitors already bill this way; buyers can compare.")
    for key, bias in PROFILES.get(profile, {}).items():
        c[key].add(bias, f"Profile '{profile}' market prior.")
    return rank(c)


def score_motions(ctx):
    c = {k: Card(k) for k in MOTIONS}
    acv = ctx.get("acv")
    ttv = ctx.get("time_to_value_days")
    adoption = ctx.get("adoption")
    motion = ctx.get("motion")
    variable = ctx.get("marginal_cost") == "variable"

    free = c["free_tier"]
    if adoption == "bottom-up":
        free.add(20, "Bottom-up adoption; free users become the funnel.")
    if ctx.get("network_effects"):
        free.add(15, "Network effects; free users add value for paid ones.")
    if ttv is not None and ttv <= 1:
        free.add(10, "Value in a day; free tier converts on experience.")
    if variable:
        free.add(-15, "Free users cost real money to serve.")
    if acv is not None and acv >= 25000:
        free.add(-15, "Enterprise deal size; free tier rarely pays back.")
    if motion == "sales-led":
        free.add(-15, "Sales-led motion; free tier dilutes the pitch.")
    free.note("Needs 2-5% free-to-paid at scale. Free tier must be useful alone.")

    trial = c["free_trial"]
    if ttv is not None:
        if ttv <= 14:
            trial.add(15, f"Value in {ttv:g} days; fits a 14-30 day trial.")
        elif ttv > 30:
            trial.add(-15, f"Value takes {ttv:g} days; trial ends before the buyer sees it.")
    if motion in ("self-serve", "mixed"):
        trial.add(10, "Self-serve path; trial is the standard entry.")
    if acv is not None and acv >= 25000:
        trial.add(-5, "Large deals usually need a guided pilot, not an open trial.")
    trial.note("Clean conversion signal. Hard cutoff loses slow evaluators.")

    rev = c["reverse_trial"]
    if adoption == "bottom-up":
        rev.add(10, "Bottom-up users feel premium value, then drop to free.")
    if ttv is not None and ttv <= 14:
        rev.add(10, "Fast value; users meet premium features before the trial ends.")
    if ctx.get("distinct_segments"):
        rev.add(10, "Clear premium line; loss of premium features is visible.")
    if variable:
        rev.add(-5, "Premium usage during trial costs money.")
    rev.note("Loss aversion lifts conversion. Needs a free tier worth keeping.")

    sales = c["sales_led"]
    if acv is not None:
        if acv >= 25000:
            sales.add(25, "Deal size pays for a sales cycle.")
        elif acv < 5000:
            sales.add(-20, "Deal size cannot carry sales cost.")
    if adoption == "top-down":
        sales.add(15, "Top-down buying; a person must sell to the committee.")
    if motion == "sales-led":
        sales.add(10, "Team already sells this way.")
    if ttv is not None and ttv > 30:
        sales.add(10, "Long setup; buyers need guided onboarding.")
    sales.note("High CAC. Price discovery happens deal by deal; watch discount spread.")
    return rank(c)


def rank(cards):
    return sorted((card.as_dict() for card in cards.values()), key=lambda d: -d["score"])


def evaluate(ctx, profile):
    models, motions = score_models(ctx, profile), score_motions(ctx)
    warnings = []
    gap = models[0]["score"] - models[1]["score"]
    if gap < 8:
        warnings.append(f"Close call: {models[0]['label']} leads {models[1]['label']} by {gap}. "
                        "Answer the open questions or test both before committing.")
    missing = [f for f in OPEN_QUESTIONS if not known(ctx, f)]
    if len(missing) >= 4:
        warnings.append(f"{len(missing)} key inputs unknown. Scores lean on profile priors; low confidence.")
    if models[0]["key"] in (ctx.get("competitor_models") or []):
        warnings.append("Top model matches competitors. Same model reads as same value claim; state the difference.")
    return {
        "profile": profile,
        "top_model": models[0]["key"],
        "strategy_type": STRATEGY_TYPE[models[0]["key"]],
        "top_motion": motions[0]["key"],
        "models": models,
        "motions": motions,
        "open_questions": [OPEN_QUESTIONS[f] for f in missing],
        "warnings": warnings,
    }


def render_md(r):
    lines = [
        "# Pricing Model Fit",
        "",
        f"Profile: `{r['profile']}` · Top model: **{LABELS[r['top_model']]}** → Strategy Type: "
        f"{r['strategy_type']} · Top motion: **{LABELS[r['top_motion']]}**",
        "",
        "Fit score 0-100 ranks options. It is not a price and not a forecast. 🟡",
        "",
    ]
    lines += [f"> ⚠ {w}" for w in r["warnings"]]
    if r["warnings"]:
        lines.append("")
    for title, rows in (("Monetization model", r["models"]), ("Acquisition motion", r["motions"])):
        lines += [f"## {title}", "", "| Rank | Option | Fit |", "|---|---|---|"]
        lines += [f"| {i} | {row['label']} | {row['score']} |" for i, row in enumerate(rows, 1)]
        lines.append("")
        for row in rows[:3]:
            lines.append(f"### {row['label']} — {row['score']}")
            lines += [f"- ✓ {x}" for x in row["fits"]]
            lines += [f"- ✗ {x}" for x in row["costs"]]
            lines.append("")
    if r["open_questions"]:
        lines += ["## Open questions", ""] + [f"- {q}" for q in r["open_questions"]] + [""]
    lines += [
        "## Next",
        "",
        "1. Run the five value-metric tests and red flags on the top model's metric.",
        "2. Validate price range with `van_westendorp.py` (30+ respondents per segment).",
        "3. Check tier design against `references/packaging-anti-patterns.md`.",
    ]
    return "\n".join(lines)


SAMPLE = {
    "profile": "vertical",
    "acv": 1068,
    "customers": 375,
    "active_user_share": 0.35,
    "usage_spread": 4,
    "usage_volatility": "low",
    "marginal_cost": "low",
    "outcome": {"measurable": True, "attribution": "shared"},
    "fixed_budget_buyer": True,
    "distinct_segments": True,
    "motion": "self-serve",
    "adoption": "bottom-up",
    "network_effects": False,
    "time_to_value_days": 3,
    "competitor_models": ["per_seat", "feature_tiers"],
}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--input", help="Context JSON file.")
    src.add_argument("--sample", action="store_true", help="Run on a built-in fictional context.")
    ap.add_argument("--profile", choices=sorted(PROFILES), help="Override profile in the context.")
    ap.add_argument("--format", choices=["md", "json"], default="md")
    args = ap.parse_args()

    if args.sample:
        ctx = SAMPLE
    else:
        try:
            with open(args.input, encoding="utf-8") as fh:
                ctx = json.load(fh)
        except (OSError, ValueError) as exc:
            sys.exit(f"error: cannot read {args.input}: {exc}")
    profile = args.profile or ctx.get("profile") or "saas"
    if profile not in PROFILES:
        sys.exit(f"error: unknown profile '{profile}'. Use one of: {', '.join(sorted(PROFILES))}")

    result = evaluate(ctx, profile)
    print(json.dumps(result, indent=2) if args.format == "json" else render_md(result))


if __name__ == "__main__":
    main()
