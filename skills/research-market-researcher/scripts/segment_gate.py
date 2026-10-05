#!/usr/bin/env python3
"""Gate candidate target segments on Kotler's criteria, with hard evidence for the two gates.

Usage:
    python3 segment_gate.py --input segments.json [--format md|json]

Substantial (gate): accounts * annual_value * attainable_share >= min_segment_revenue,
                    and accounts >= min_accounts.
Accessible  (gate): at least one channel reaches >= min_channel_reach of the segment
                    at a CAC <= max_cac_to_value * annual_value.
A segment that fails either gate is DROP, whatever its other scores.

Measurable, differentiable, actionable: scored 1-5, each with an evidence note.
A score without evidence counts as 1.

Spec (see assets/segments-sample.json):
    {"profile", "market_accounts"?, "gates"?: {...}, "segments": [{name, basis, accounts,
      annual_value, attainable_share, channels: [{name, reach, cac}],
      scores: {measurable: {score, evidence}, differentiable: {...}, actionable: {...}}}]}

Exit code: 0 if at least one segment is TARGET, 1 otherwise.
"""
import argparse
import json
import sys

# Profile defaults. A spec "gates" block overrides any key.
GATES = {
    "b2b-saas":    dict(min_segment_revenue=2_000_000, min_accounts=500, min_channel_reach=0.30, max_cac_to_value=1.0),
    "enterprise":  dict(min_segment_revenue=5_000_000, min_accounts=50, min_channel_reach=0.20, max_cac_to_value=1.5),
    "consumer":    dict(min_segment_revenue=1_000_000, min_accounts=20_000, min_channel_reach=0.25, max_cac_to_value=0.5),
    "marketplace": dict(min_segment_revenue=1_000_000, min_accounts=5_000, min_channel_reach=0.25, max_cac_to_value=0.5),
    "hardware":    dict(min_segment_revenue=2_000_000, min_accounts=1_000, min_channel_reach=0.25, max_cac_to_value=0.5),
    "services":    dict(min_segment_revenue=500_000, min_accounts=100, min_channel_reach=0.30, max_cac_to_value=0.75),
}
SCORED = ("measurable", "differentiable", "actionable")
TARGET_MIN_SCORE = 3.5


def evidence_score(entry):
    if not entry or not entry.get("evidence"):
        return 1, "no evidence"
    return max(1, min(5, entry.get("score", 1))), entry["evidence"]


def assess(seg, g):
    reasons = []
    potential = seg["accounts"] * seg["annual_value"] * seg["attainable_share"]
    substantial = potential >= g["min_segment_revenue"] and seg["accounts"] >= g["min_accounts"]
    if potential < g["min_segment_revenue"]:
        reasons.append(f"attainable revenue {potential:,.0f} < {g['min_segment_revenue']:,.0f}")
    if seg["accounts"] < g["min_accounts"]:
        reasons.append(f"{seg['accounts']:,} accounts < {g['min_accounts']:,}")

    max_cac = g["max_cac_to_value"] * seg["annual_value"]
    usable = [c for c in seg.get("channels", []) if c["reach"] >= g["min_channel_reach"] and c["cac"] <= max_cac]
    accessible = bool(usable)
    if not accessible:
        reasons.append(f"no channel reaches >= {g['min_channel_reach']:.0%} at CAC <= {max_cac:,.0f}")

    scores = {c: evidence_score(seg.get("scores", {}).get(c)) for c in SCORED}
    mean = sum(s for s, _ in scores.values()) / len(SCORED)
    notes = []
    if seg.get("basis") == "demographic":
        notes.append("Demographic basis only. Show that the slice responds differently (differentiable) before targeting.")
    if not substantial or not accessible:
        verdict = "DROP"
    elif mean >= TARGET_MIN_SCORE:
        verdict = "TARGET"
    else:
        verdict = "WATCH"
    return {"name": seg["name"], "verdict": verdict, "attainable_revenue": round(potential),
            "substantial": substantial, "accessible": accessible,
            "best_channel": min(usable, key=lambda c: c["cac"])["name"] if usable else None,
            "scores": {c: {"score": s, "evidence": e} for c, (s, e) in scores.items()},
            "mean_score": round(mean, 2), "gate_failures": reasons, "notes": notes}


def run(spec):
    profile = spec.get("profile", "b2b-saas")
    if profile not in GATES:
        sys.exit(f"error: unknown profile {profile}. Valid: {', '.join(GATES)}")
    g = {**GATES[profile], **spec.get("gates", {})}
    rows = [assess(s, g) for s in spec["segments"]]
    order = {"TARGET": 0, "WATCH": 1, "DROP": 2}
    rows.sort(key=lambda r: (order[r["verdict"]], -r["attainable_revenue"]))
    warnings = []
    total = sum(s["accounts"] for s in spec["segments"])
    if spec.get("market_accounts") and total > spec["market_accounts"]:
        warnings.append(f"Segments hold {total:,} accounts but the market has {spec['market_accounts']:,}. "
                        "Segments overlap. Make them mutually exclusive before you add their revenue.")
    return {"profile": profile, "gates": g, "segments": rows, "warnings": warnings}


def render_markdown(r):
    g = r["gates"]
    lines = ["# Segment gate", "",
             f"Profile {r['profile']}. Substantial: attainable revenue >= {g['min_segment_revenue']:,} and "
             f">= {g['min_accounts']:,} accounts. Accessible: a channel with reach >= {g['min_channel_reach']:.0%} "
             f"and CAC <= {g['max_cac_to_value']}x annual value.", "",
             "| Segment | Verdict | Attainable revenue | Substantial | Accessible | Best channel | Mean score |",
             "|---|---|---|---|---|---|---|"]
    for s in r["segments"]:
        lines.append(f"| {s['name']} | **{s['verdict']}** | {s['attainable_revenue']:,} | {'pass' if s['substantial'] else 'FAIL'} "
                     f"| {'pass' if s['accessible'] else 'FAIL'} | {s['best_channel'] or '-'} | {s['mean_score']} |")
    for s in r["segments"]:
        detail = s["gate_failures"] + s["notes"] + [f"{c} {v['score']}/5: {v['evidence']}" for c, v in s["scores"].items()]
        lines += ["", f"## {s['name']}"] + [f"- {d}" for d in detail]
    if r["warnings"]:
        lines += ["", "## Warnings"] + [f"- {w}" for w in r["warnings"]]
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", required=True)
    ap.add_argument("--format", choices=["md", "json"], default="md")
    args = ap.parse_args()
    with open(args.input, encoding="utf-8") as f:
        result = run(json.load(f))
    sys.stdout.write(json.dumps(result, indent=2) + "\n" if args.format == "json" else render_markdown(result))
    sys.exit(0 if any(s["verdict"] == "TARGET" for s in result["segments"]) else 1)


if __name__ == "__main__":
    main()
