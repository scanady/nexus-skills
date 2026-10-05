#!/usr/bin/env python3
"""Map the riskiest assumption to the cheapest falsifiable test, with pass and fail lines.

Usage:
    python3 cheapest_test.py --risk price [--price 99] [--motion self-serve|sales-led] [--format md|json]
    python3 cheapest_test.py --list

Risk categories (one assumption usually owns the risk):
    demand          will the target customer want this at all?
    price           will they pay, and at the intended number?
    channel         can the buyer be reached at a cost the economics allow?
    feasibility     can the outcome be delivered with the resources at hand?
    differentiation why this over the incumbent or doing nothing?
    retention       will they come back or keep paying?

Aliases (wtp, moat, churn, distribution, ...) resolve to a category.
Each test has a time box of one week or less. A longer test is a mini-build: split it.
Pure lookup, no network, no LLM. Stdlib only.
"""
import argparse
import json
import sys

# Each entry: per-motion variants. "self-serve" = product-led or consumer buyer.
# "sales-led" = named accounts, demos, contracts. Thresholds are defaults, not law.
TESTS = {
    "demand": {
        "self-serve": {
            "test": "Smoke-test page + small paid push",
            "do": "One page: promise, who it is for, one email or waitlist CTA. "
                  "Drive $50-150 of targeted traffic, or one post where the buyer already gathers.",
            "cost": "$50-150 + 3 hours",
            "time_box": "48 hours",
            "pass": "Visitor-to-signup at or above 10% from cold traffic, at a cost per signup under target CAC.",
            "fail": "Under 5% signup, or signups cost more than a customer is worth.",
        },
        "sales-led": {
            "test": "Named-buyer outreach batch",
            "do": "Send 30 short, specific notes to named buyers in the target role. "
                  "Ask for a 20-minute call about the problem, not the product.",
            "cost": "$0 + 4 hours",
            "time_box": "5 days",
            "pass": "At least 3 calls booked, and 2 or more describe the pain unprompted.",
            "fail": "Under 2 replies, or replies say the problem is minor or already solved.",
        },
    },
    "price": {
        "self-serve": {
            "test": "Pre-sale with a real charge",
            "do": "Put a live payment link or paid early-access offer in front of target strangers. "
                  "A 'Buy' click on a fake page is the weak version. A real charge is the strong one.",
            "cost": "$0-50",
            "time_box": "48 hours of outreach",
            "pass": "At least 1 real prepayment from a stranger, not a friend or colleague.",
            "fail": "Praise and 'I would use this', zero payments. Interest is not demand.",
        },
        "sales-led": {
            "test": "Paid pilot or priced LOI",
            "do": "Offer 3-5 qualified buyers a paid pilot or a letter of intent with the price written in.",
            "cost": "$0 + 1-2 days",
            "time_box": "1 week",
            "pass": "At least 1 signed paid pilot or priced LOI.",
            "fail": "Buyers ask for a free pilot, or stall at procurement with no budget owner.",
        },
    },
    "channel": {
        "self-serve": {
            "test": "One-channel reach spike",
            "do": "Pick one channel (community post, creator DM, SEO page, small ad set). Run it once. "
                  "Measure response from the exact buyer, not general traffic.",
            "cost": "$0-100",
            "time_box": "48 hours",
            "pass": "Response rate that implies CAC under one-third of first-year customer value.",
            "fail": "No response, or the only working channel costs more than the margin can repeat.",
        },
        "sales-led": {
            "test": "50-account outbound batch",
            "do": "One sequence to 50 accounts that fit the profile. Track reply and meeting rates.",
            "cost": "$0-100 for data",
            "time_box": "1 week",
            "pass": "Reply rate at or above 8% and at least 3 meetings booked.",
            "fail": "Reply rate under 3%, or replies come from the wrong role.",
        },
    },
    "feasibility": {
        "self-serve": {
            "test": "Concierge delivery (Wizard of Oz)",
            "do": "Deliver the promised outcome by hand to 1-3 real users. No product. You are the system.",
            "cost": "Time only",
            "time_box": "1-2 days per user",
            "pass": "Outcome delivered by hand, user calls it worth paying for, hours per user fit the price.",
            "fail": "Outcome weak even by hand, or hours per user break the unit economics.",
        },
        "sales-led": {
            "test": "Manual proof on one account",
            "do": "Produce the promised result for one design-partner account with scripts and spreadsheets.",
            "cost": "Time only",
            "time_box": "1 week",
            "pass": "Buyer confirms the result is real and names who would sign for it.",
            "fail": "Result needs data, access, or integration you cannot get.",
        },
    },
    "differentiation": {
        "self-serve": {
            "test": "5 switch interviews",
            "do": "Talk to 5 people who use the incumbent or do nothing. Ask what they use, what they hate, "
                  "what last made them switch. Show the wedge last, watch the reaction.",
            "cost": "$0-50 incentives",
            "time_box": "2-3 days",
            "pass": "A repeated, specific switch reason that the incumbent cannot copy in one release.",
            "fail": "Shrugs, or 'good enough' wins. A feature is not a wedge.",
        },
        "sales-led": {
            "test": "Head-to-head displacement test",
            "do": "Ask 3-5 buyers on the incumbent what it would take to replace it this year, "
                  "and who would block the change.",
            "cost": "$0",
            "time_box": "1 week",
            "pass": "At least 2 name a concrete trigger and a budget window for switching.",
            "fail": "Switching cost or contract lock-in beats the wedge for every buyer.",
        },
    },
    "retention": {
        "self-serve": {
            "test": "One-week repeat-use probe",
            "do": "Give the value to 5-10 users for a week, by hand if needed. Do not nudge. Count returns.",
            "cost": "Time only",
            "time_box": "5-7 days",
            "pass": "At least half return unprompted, or ask for the next session.",
            "fail": "One-and-done use. Novelty, not habit.",
        },
        "sales-led": {
            "test": "Second-use commitment",
            "do": "After the first delivered result, ask each account to book the next cycle now.",
            "cost": "Time only",
            "time_box": "1 week",
            "pass": "At least half book or pay for a second cycle.",
            "fail": "Accounts say 'we will reach out' and go quiet.",
        },
    },
}

ALIASES = {
    "want": "demand", "pull": "demand", "pain": "demand", "market": "demand", "timing": "demand",
    "wtp": "price", "willingness-to-pay": "price", "pricing": "price", "monetization": "price",
    "distribution": "channel", "reach": "channel", "acquisition": "channel", "gtm": "channel",
    "build": "feasibility", "delivery": "feasibility", "execution": "feasibility", "technical": "feasibility",
    "moat": "differentiation", "competition": "differentiation", "defensibility": "differentiation",
    "churn": "retention", "repeat": "retention", "habit": "retention",
}

MOTIONS = ("self-serve", "sales-led")


def resolve(risk):
    """Return the canonical category for a risk name or alias, or None."""
    key = (risk or "").strip().lower().replace("_", "-")
    key = ALIASES.get(key, key)
    return key if key in TESTS else None


def design(risk, motion="self-serve", price=None):
    """Return the test card for a risk. Raises ValueError for an unknown risk or motion."""
    category = resolve(risk)
    if category is None:
        raise ValueError(f"unknown risk '{risk}'. Valid: {', '.join(TESTS)}; aliases: {', '.join(sorted(ALIASES))}")
    if motion not in MOTIONS:
        raise ValueError(f"unknown motion '{motion}'. Valid: {', '.join(MOTIONS)}")
    card = dict(TESTS[category][motion], risk=category, motion=motion)
    if category == "price" and price:
        card["note"] = (f"Charge the real number: ${price:g}. A stranger who will not pay ${price:g} now "
                        "will not be saved by a later discount. Fix the value, not the price.")
    return card


def to_markdown(card):
    lines = [
        f"### Cheapest test — {card['risk']} risk ({card['motion']})",
        f"**Test:** {card['test']}",
        f"**Do:** {card['do']}",
        f"**Cost / time box:** {card['cost']} / {card['time_box']}",
        f"**Pass:** {card['pass']}",
        f"**Fail:** {card['fail']}",
    ]
    if card.get("note"):
        lines.append(f"**Note:** {card['note']}")
    return "\n".join(lines)


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--risk", help="Risk category or alias")
    ap.add_argument("--motion", choices=MOTIONS, default="self-serve")
    ap.add_argument("--price", type=float, help="Intended price; sharpens the price test")
    ap.add_argument("--format", choices=("md", "json"), default="md")
    ap.add_argument("--list", action="store_true", help="List categories and aliases")
    args = ap.parse_args(argv)

    if args.list:
        for cat in TESTS:
            aliases = sorted(a for a, c in ALIASES.items() if c == cat)
            print(f"{cat}: {', '.join(aliases)}")
        return 0
    if not args.risk:
        ap.error("provide --risk <category> or --list")
    try:
        card = design(args.risk, args.motion, args.price)
    except ValueError as err:
        print(f"error: {err}", file=sys.stderr)
        return 1
    print(json.dumps(card, indent=2) if args.format == "json" else to_markdown(card))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
