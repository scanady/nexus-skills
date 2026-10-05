#!/usr/bin/env python3
"""Turn rubric scores into one gated decision. A high weighted score cannot buy past a veto.

Usage:
    python3 opportunity_verdict.py --input scores.json [--format md|json]
    python3 opportunity_verdict.py --input - < scores.json
    python3 opportunity_verdict.py --sample

Pipeline:
  1. Weighted score 0-100 from the 9 rubric dimensions and the profile weights
     (venture | bootstrapped | micro). Same weights as references/scoring-rubric.md.
  2. Base decision from the score band, stage, and goal.
  3. Veto gates (non-compensatory). One weak load-bearing dimension caps the decision,
     whatever the average. Gates only lower a decision, never raise it.
  4. Tension detection. Named dimension pairs that pull apart by 4+ points are the real
     argument the verdict must settle in prose.
  5. Confidence = stated evidence level, capped by tension size and gate friction.
  6. Riskiest dimension -> risk category -> cheapest test (scripts/cheapest_test.py).

Spec (see assets/verdict-sample.json):
    opportunity, profile, stage (idea|research|prototype|launched|revenue|active),
    goal (venture|cash-flow|lifestyle|strategic|learning|optionality),
    evidence (high|medium|low), motion (self-serve|sales-led), price (optional),
    scores: {pain, market, distribution, monetization, defensibility, timing, fit, execution, portfolio} 0-10,
    fatal_flaw (optional text: stress-test objection that landed),
    riskiest (optional: {category, assumption}) to override the derived riskiest assumption.

Fixes the call, not the prose. The analyst still writes why. To disagree, change a score
with a stated reason and re-run. Do not hand-edit the decision.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cheapest_test import design as design_test  # noqa: E402

DIMENSIONS = {
    "pain": "Customer pain and urgency",
    "market": "Market structure and upside",
    "distribution": "Distribution advantage",
    "monetization": "Monetization and unit economics",
    "defensibility": "Defensibility and compounding",
    "timing": "Timing and tailwinds",
    "fit": "Founder/opportunity fit",
    "execution": "Execution complexity",
    "portfolio": "Portfolio fit and opportunity cost",
}

# Percent weights per profile. Each row sums to 100. Mirrors references/scoring-rubric.md.
WEIGHTS = {
    "venture":      {"pain": 15, "market": 15, "distribution": 15, "monetization": 15, "defensibility": 10,
                     "timing": 10, "fit": 10, "execution": 5, "portfolio": 5},
    "bootstrapped": {"pain": 15, "market": 10, "distribution": 15, "monetization": 20, "defensibility": 5,
                     "timing": 10, "fit": 15, "execution": 5, "portfolio": 5},
    "micro":        {"pain": 15, "market": 5, "distribution": 20, "monetization": 20, "defensibility": 5,
                     "timing": 10, "fit": 15, "execution": 5, "portfolio": 5},
}

BANDS = [(85, "Exceptional"), (70, "Strong"), (55, "Conditional"), (40, "Weak"), (0, "Poor")]

# Veto gates: (dimension, max score that trips it, name, meaning).
GATES = [
    ("pain", 3, "Demand gate", "No specific, painful job. Upside elsewhere cannot replace a missing buyer."),
    ("monetization", 3, "Payment gate", "Buyer will not pay, or unit economics fail on paper."),
    ("distribution", 2, "Reach gate", "No credible path to the buyer at a cost the model can carry."),
    ("execution", 2, "Capacity gate", "Build, ops, or compliance load exceeds the resources on hand."),
]

# Named tensions: (high dim, low dim, label, question the verdict must answer).
TENSIONS = [
    ("pain", "monetization", "Hurts, but no wallet",
     "Is there a different buyer or budget line that pays for this pain?"),
    ("market", "distribution", "Big market, no road in",
     "Is there one channel the user owns or can afford that reaches a first niche?"),
    ("pain", "distribution", "Real pain, unreachable buyer",
     "Can the offer ride an existing channel, partner, or marketplace?"),
    ("monetization", "pain", "Price logic without pull",
     "Is the buyer paying for a real job, or does the model only work on a spreadsheet?"),
    ("market", "pain", "Big market, nobody hurting",
     "Which narrow segment has the acute version of this problem?"),
    ("timing", "fit", "Right wave, wrong surfer",
     "Does the user have or can they borrow the edge to ride this shift before others?"),
    ("defensibility", "execution", "Moat too costly to dig",
     "Is there a cheaper first wedge that earns the right to build the moat later?"),
    ("fit", "portfolio", "Right founder, wrong slot",
     "Does this beat the current best use of the same hours and capital?"),
]

RANK = {"Grow": 6, "Launch": 5, "Run for Cash": 5, "Validate": 4, "Pivot": 3, "Park": 2, "Kill": 1, "Remove": 1}
EVIDENCE = ["low", "medium", "high"]
REVENUE_STAGES = {"revenue", "active"}
CASH_GOALS = {"cash-flow", "lifestyle"}

# Dimension -> test risk category. Portfolio is a choice, not a testable assumption.
RISK_FOR = {"pain": "demand", "market": "demand", "timing": "demand", "monetization": "price",
            "distribution": "channel", "execution": "feasibility", "fit": "feasibility",
            "defensibility": "differentiation"}

SAMPLE = {
    "opportunity": "Grant-draft assistant for small nonprofits",
    "profile": "bootstrapped", "stage": "idea", "goal": "cash-flow", "evidence": "medium",
    "motion": "self-serve", "price": 99,
    "scores": {"pain": 8, "market": 5, "distribution": 7, "monetization": 3, "defensibility": 3,
               "timing": 7, "fit": 9, "execution": 6, "portfolio": 7},
    "fatal_flaw": "",
}


def load_spec(spec):
    """Validate and normalize the input spec. Raises ValueError with every problem at once."""
    errors = []
    profile = spec.get("profile", "bootstrapped")
    if profile not in WEIGHTS:
        errors.append(f"profile must be one of {', '.join(WEIGHTS)}")
    evidence = spec.get("evidence", "medium")
    if evidence not in EVIDENCE:
        errors.append(f"evidence must be one of {', '.join(EVIDENCE)}")
    raw = spec.get("scores") or {}
    scores = {}
    for dim in DIMENSIONS:
        val = raw.get(dim)
        if not isinstance(val, (int, float)) or not 0 <= val <= 10:
            errors.append(f"scores.{dim} must be a number 0-10 (got {val!r})")
        else:
            scores[dim] = float(val)
    unknown = set(raw) - set(DIMENSIONS)
    if unknown:
        errors.append(f"unknown score keys: {', '.join(sorted(unknown))}")
    if errors:
        raise ValueError("; ".join(errors))
    return {
        "opportunity": spec.get("opportunity", "Unnamed opportunity"),
        "profile": profile, "evidence": evidence, "scores": scores,
        "stage": spec.get("stage", "idea"), "goal": spec.get("goal", "cash-flow"),
        "motion": spec.get("motion", "self-serve"), "price": spec.get("price"),
        "fatal_flaw": (spec.get("fatal_flaw") or "").strip(),
        "riskiest": spec.get("riskiest"),
    }


def base_decision(score, s, stage, goal):
    """Decision from the band alone, before any gate."""
    if score >= 70:
        if stage in REVENUE_STAGES:
            return "Run for Cash" if goal in CASH_GOALS and s["market"] <= 5 else "Grow"
        return "Launch"
    if score >= 55:
        return "Validate"
    if score >= 40:
        return "Pivot" if s["pain"] >= 6 else "Park"
    return "Remove" if s["portfolio"] <= 3 else "Kill"


def apply_gates(decision, score, tripped, evidence):
    """Cap the decision under tripped gates. Returns (decision, note). Never raises the rank."""
    if not tripped:
        return decision, ""
    names = {g["dimension"] for g in tripped}
    money_or_demand = bool(names & {"pain", "monetization"})
    if (money_or_demand and score < 55) or (len(tripped) >= 2 and score < 70):
        capped, why = "Kill", "a demand or payment veto on a sub-55 score, or 2+ vetoes below 70"
    elif evidence == "low":
        capped, why = "Validate", "veto rests on low evidence; test the gated dimension first"
    else:
        capped, why = "Pivot", "veto rests on medium/high evidence; change the gated dimension"
    if RANK[capped] < RANK[decision]:
        return capped, f"Capped from {decision}: {why}."
    return decision, ""


def detect_tensions(s, weights):
    """Named pairs 4+ apart, plus the widest gap among heavy (>=10%) dims if no named pair caught it."""
    found = []
    for hi, lo, label, question in TENSIONS:
        gap = s[hi] - s[lo]
        if gap >= 4:
            found.append({"high": hi, "low": lo, "gap": gap, "label": label, "question": question})
    heavy = [d for d in DIMENSIONS if weights[d] >= 10]
    hi = max(heavy, key=lambda d: s[d])
    lo = min(heavy, key=lambda d: s[d])
    gap = s[hi] - s[lo]
    if gap >= 5 and not any(t["high"] == hi and t["low"] == lo for t in found):
        found.append({"high": hi, "low": lo, "gap": gap, "label": "Unnamed split",
                      "question": f"Why is {DIMENSIONS[hi].lower()} strong while "
                                  f"{DIMENSIONS[lo].lower()} is weak, and which one is wrong?"})
    return sorted(found, key=lambda t: -t["gap"])


def confidence(evidence, tensions, gated_down):
    """Start at stated evidence. Wide splits and vetoed upside lower it. Never raise it."""
    level = EVIDENCE.index(evidence)
    widest = tensions[0]["gap"] if tensions else 0
    if widest >= 6:
        level = min(level, 0)
    elif widest >= 4:
        level = min(level, 1)
    if gated_down:
        level = min(level, 1)
    return EVIDENCE[level]


def riskiest(spec, s, weights, tripped):
    """Override wins; else lowest tripped gate; else largest weighted shortfall."""
    if spec["riskiest"]:
        return spec["riskiest"].get("category"), spec["riskiest"].get("assumption", ""), "override"
    if tripped:
        dim = min(tripped, key=lambda g: g["score"])["dimension"]
        return RISK_FOR[dim], DIMENSIONS[dim], "gate"
    testable = [d for d in RISK_FOR]
    dim = max(testable, key=lambda d: weights[d] * (10 - s[d]))
    return RISK_FOR[dim], DIMENSIONS[dim], "weighted shortfall"


def synthesize(raw_spec):
    spec = load_spec(raw_spec)
    s, weights = spec["scores"], WEIGHTS[spec["profile"]]
    score = round(sum(s[d] * weights[d] for d in DIMENSIONS) / 10, 1)
    tier = next(name for floor, name in BANDS if score >= floor)

    tripped = [{"dimension": d, "score": s[d], "gate": name, "meaning": meaning}
               for d, limit, name, meaning in GATES if s[d] <= limit]
    if spec["fatal_flaw"]:
        tripped.append({"dimension": "stress-test", "score": 0, "gate": "Fatal-flaw gate",
                        "meaning": spec["fatal_flaw"]})
    score_gates = [g for g in tripped if g["dimension"] in DIMENSIONS]

    base = base_decision(score, s, spec["stage"], spec["goal"])
    decision, gate_note = apply_gates(base, score, tripped, spec["evidence"])
    tensions = detect_tensions(s, weights)
    conf = confidence(spec["evidence"], tensions, bool(gate_note))

    category, assumption, source = riskiest(spec, s, weights, score_gates)
    test = None
    if category:
        try:
            test = design_test(category, spec["motion"], spec["price"])
        except ValueError as err:
            test = {"error": str(err)}

    contributions = {d: round(s[d] * weights[d] / 10, 1) for d in DIMENSIONS}
    return {
        "opportunity": spec["opportunity"], "profile": spec["profile"],
        "score": score, "tier": tier, "base_decision": base, "decision": decision,
        "confidence": conf, "gates": tripped, "gate_note": gate_note, "tensions": tensions,
        "riskiest": {"category": category, "assumption": assumption, "source": source},
        "cheapest_test": test, "scores": s, "weights": weights, "contributions": contributions,
        "lift": max(contributions, key=contributions.get),
        "drag": max(DIMENSIONS, key=lambda d: weights[d] * (10 - s[d])),
    }


def to_markdown(r):
    out = [f"## Gated verdict — {r['opportunity']}",
           f"**Decision:** {r['decision']}  (base from band: {r['base_decision']})",
           f"**Score:** {r['score']} ({r['tier']}, {r['profile']} weights)",
           f"**Confidence:** {r['confidence'].title()}",
           f"**Lift:** {DIMENSIONS[r['lift']]} · **Drag:** {DIMENSIONS[r['drag']]}", ""]
    if r["gates"]:
        out.append("**Vetoes tripped:**")
        out += [f"- {g['gate']} ({g['dimension']} {g['score']:g}): {g['meaning']}" for g in r["gates"]]
        if r["gate_note"]:
            out.append(f"- {r['gate_note']}")
    else:
        out.append("**Vetoes tripped:** none")
    out.append("")
    if r["tensions"]:
        out.append("**Tensions to resolve in prose:**")
        out += [f"- {t['label']}: {t['high']} {r['scores'][t['high']]:g} vs {t['low']} "
                f"{r['scores'][t['low']]:g} (gap {t['gap']:g}). {t['question']}" for t in r["tensions"]]
    else:
        out.append("**Tensions to resolve in prose:** none above threshold")
    out.append("")
    rk = r["riskiest"]
    out.append(f"**Riskiest assumption:** {rk['assumption']} -> {rk['category']} risk ({rk['source']})")
    test = r["cheapest_test"]
    if test and "error" not in test:
        out += [f"**Cheapest test:** {test['test']} — {test['do']}",
                f"**Cost / time box:** {test['cost']} / {test['time_box']}",
                f"**Pass:** {test['pass']}", f"**Fail:** {test['fail']}"]
        if test.get("note"):
            out.append(f"**Note:** {test['note']}")
    elif test:
        out.append(f"**Cheapest test:** {test['error']}")
    out += ["", "| Dimension | Score | Weight | Points |", "|---|---:|---:|---:|"]
    out += [f"| {DIMENSIONS[d]} | {r['scores'][d]:g} | {r['weights'][d]}% | {r['contributions'][d]:g} |"
            for d in DIMENSIONS]
    return "\n".join(out)


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--input", help="Path to spec JSON, or '-' for stdin")
    ap.add_argument("--sample", action="store_true", help="Run the embedded sample")
    ap.add_argument("--format", choices=("md", "json"), default="md")
    args = ap.parse_args(argv)

    if args.sample:
        spec = SAMPLE
    elif args.input:
        try:
            spec = json.load(sys.stdin if args.input == "-" else open(args.input, encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as err:
            print(f"error: cannot read spec: {err}", file=sys.stderr)
            return 2
    else:
        ap.error("provide --input <file|-> or --sample")
    try:
        result = synthesize(spec)
    except ValueError as err:
        print(f"error: {err}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2) if args.format == "json" else to_markdown(result))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
