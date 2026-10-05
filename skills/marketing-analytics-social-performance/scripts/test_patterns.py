#!/usr/bin/env python3
"""Test whether an apparent pattern in your own post history survives a null test.

The usual claim is "videos do 3x better for me", built on four posts. This script
tries to kill every candidate pattern before reporting it.

Each candidate is one group of posts against all the others (a format, a topic,
a weekday, a high/low split on a number, a before/after date). Gates, in order:

  1. Size floor: at least 5 posts in the group and 5 outside it.
  2. Permutation test on the difference of medians. Exact when the number of
     label arrangements is small, otherwise Monte Carlo with a fixed seed.
  3. Multiple-comparisons correction over EVERY candidate that was tested, not
     only the ones that looked promising: Benjamini-Hochberg false discovery
     rate (default), Holm family-wise error, or none.
  4. Effect floor: the median must differ by at least 15% relative. A real 3%
     difference changes no decision.

Reported next to each result: a 90% bootstrap interval for the relative effect,
and a flag when the group is lopsided in time (then "group" and "period" are
mixed up and the comparison is confounded).

Pass the candidates you meant to test, in advance, with --attribute. With none,
every low-cardinality text column is tested, and all of them count toward the
correction.

Usage:
    python3 test_patterns.py --input posts.csv --output human
    python3 test_patterns.py --input posts.csv --attribute format --attribute weekday \\
        --attribute length_words@median --attribute period@2026-05-01
    python3 test_patterns.py --sample --output human

Attribute forms:
    column              one group per value, each against the rest
    column@median       split a numeric column at its median (high vs low)
    weekday             from the date column
    period@YYYY-MM-DD   posts on or after the date vs before it ("did it change?")

Exit codes: 0 something survived | 2 nothing survived | 3 under 10 posts | 4 bad input
Stdlib only. No network. Deterministic: same data, same flags, same verdict.
"""
from __future__ import annotations

import argparse
import json
import math
import random
import sys
from pathlib import Path

import social_data as sd

SAMPLE_PATH = Path(__file__).resolve().parent.parent / "assets" / "example_posts.csv"
SEED = 20260825
EXACT_LIMIT = 20000
TIME_FLAG = 0.4
NON_ATTRIBUTE_NAMES = {"title", "name", "id", "url", "link", "text", "post", "caption", "notes"}
MAX_LEVELS = 8


# ---------- attributes ----------

def label_for(spec: str, records: list[dict]) -> tuple[list[str | None], str]:
    """Return (one label per record, display name). None means missing."""
    if spec == "weekday":
        if not sd.time_ordered(records):
            raise sd.DataError("'weekday' needs a date on every post")
        return [sd.WEEKDAYS[r["date"].weekday()] for r in records], "weekday"
    if spec.startswith("period@"):
        cut = sd.parse_date(spec.split("@", 1)[1])
        if cut is None or not sd.time_ordered(records):
            raise sd.DataError("period@YYYY-MM-DD needs a valid date and a date on every post")
        return [f"on/after {cut}" if r["date"] >= cut else f"before {cut}" for r in records], spec
    if spec.endswith("@median"):
        col = spec[: -len("@median")]
        nums = [sd.to_float(r["row"].get(col)) for r in records]
        known = [x for x in nums if x is not None]
        if len(known) < len(records) / 2:
            raise sd.DataError(f"'{col}' is not numeric on most posts")
        cut = sd.median(known)
        return [None if x is None else ("high" if x > cut else "low") for x in nums], spec
    values = [str(r["row"].get(spec, "")).strip() or None for r in records]
    if all(v is None for v in values):
        raise sd.DataError(f"column '{spec}' not found or empty")
    return values, spec


def default_attributes(records: list[dict], info: dict) -> list[str]:
    skip = {c.lower() for c in info["interaction_cols"]} | NON_ATTRIBUTE_NAMES
    skip |= {str(info["exposure_col"]).lower(), str(info["date_col"]).lower(), info["metric"].lower()}
    found = []
    for col in records[0]["row"]:
        if col.lower() in skip:
            continue
        values = [str(r["row"].get(col, "")).strip() for r in records]
        if sum(sd.to_float(v) is not None for v in values) > len(values) / 2:
            continue  # numeric column: declare a split explicitly
        if 2 <= len({v for v in values if v}) <= MAX_LEVELS:
            found.append(col)
    if sd.time_ordered(records):
        found.append("weekday")
    return found


# ---------- inference ----------

def bootstrap_interval(group: list[float], rest: list[float], rng: random.Random,
                       resamples: int = 2000) -> tuple[float, float] | None:
    effects = []
    for _ in range(resamples):
        g = sd.median(rng.choices(group, k=len(group)))
        o = sd.median(rng.choices(rest, k=len(rest)))
        if o > 0:
            effects.append((g - o) / o)
    if len(effects) < resamples // 2:
        return None
    return sd.percentile(effects, 5), sd.percentile(effects, 95)


def adjust(pvalues: list[float], method: str) -> list[float]:
    m = len(pvalues)
    if method == "none" or m == 0:
        return list(pvalues)
    order = sorted(range(m), key=lambda i: pvalues[i])
    adjusted = [0.0] * m
    if method == "holm":
        running = 0.0
        for rank, i in enumerate(order):
            running = max(running, (m - rank) * pvalues[i])
            adjusted[i] = min(1.0, running)
    else:  # Benjamini-Hochberg
        running = 1.0
        for rank in range(m - 1, -1, -1):
            i = order[rank]
            running = min(running, pvalues[i] * m / (rank + 1))
            adjusted[i] = min(1.0, running)
    return adjusted


def mine(records: list[dict], info: dict, attributes: list[str], alpha: float,
         correction: str, min_group: int, min_effect: float, shuffles: int) -> dict:
    n = len(records)
    if n < sd.MIN_POSTS:
        return {"verdict": "INSUFFICIENT_DATA", "exit_code": 3, "posts": n, "floor": sd.MIN_POSTS,
                "finding": f"{n} usable posts. Under {sd.MIN_POSTS}, between-post variation is "
                           "larger than any group difference the sample could show.",
                "instead": "Keep posting to the plan, log outcomes by hand, and re-run after "
                           "more posts."}

    rng = random.Random(SEED)
    values = [r["value"] for r in records]
    time_rank = list(range(n))
    if sd.time_ordered(records):
        order = sorted(range(n), key=lambda i: records[i]["date"])
        time_rank = [0] * n
        for pos, i in enumerate(order):
            time_rank[i] = pos
    has_time = sd.time_ordered(records)

    candidates, mirrored = [], []
    for spec in attributes:
        labels, name = label_for(spec, records)
        levels = sorted({lab for lab in labels if lab is not None})
        if len(levels) < 2:
            candidates.append({"attribute": name, "value": "-", "verdict": "NOT_TESTED",
                               "reason": "fewer than two levels"})
            continue
        if len(levels) == 2:
            mirrored.append(f"{name}: tested '{levels[0]}' only; '{levels[1]}' is the same "
                            "comparison with the sign flipped")
            levels = levels[:1]
        for level in levels:
            idx_g = [i for i, lab in enumerate(labels) if lab == level]
            idx_o = [i for i, lab in enumerate(labels) if lab is not None and lab != level]
            c = {"attribute": name, "value": level, "n_group": len(idx_g), "n_rest": len(idx_o)}
            if len(idx_g) < min_group or len(idx_o) < min_group:
                c.update(verdict="NOT_TESTED",
                         reason=f"needs {min_group} in and {min_group} out; has "
                                f"{len(idx_g)} and {len(idx_o)}")
                candidates.append(c)
                continue
            g, o = [values[i] for i in idx_g], [values[i] for i in idx_o]
            m_g, m_o = sd.median(g), sd.median(o)
            rel = (m_g - m_o) / m_o if m_o else math.inf
            p, method = sd.permutation_p(g, o, rng, shuffles, EXACT_LIMIT)
            ci = bootstrap_interval(g, o, rng)
            c.update(median_group=round(m_g, 6), median_rest=round(m_o, 6),
                     relative_effect=None if math.isinf(rel) else round(rel, 3),
                     p_raw=round(p, 4), p_method=method,
                     interval_90=None if ci is None else [round(ci[0], 3), round(ci[1], 3)])
            if has_time and not name.startswith("period@"):
                flags = [1.0 if lab == level else 0.0 for lab in labels]
                pairs = [(time_rank[i], flags[i]) for i in idx_g + idx_o]
                rho = sd.spearman([a for a, _ in pairs], [b for _, b in pairs])
                c["time_rho"] = None if rho is None else round(rho, 2)
                c["time_confounded"] = rho is not None and abs(rho) >= TIME_FLAG
            candidates.append(c)

    family = [c for c in candidates if "p_raw" in c]
    for c, q in zip(family, adjust([c["p_raw"] for c in family], correction)):
        c["p_adjusted"] = round(q, 4)
        big = c["relative_effect"] is None or abs(c["relative_effect"]) >= min_effect
        if q > alpha:
            c.update(verdict="NOT_SUPPORTED",
                     reason=f"adjusted p {q:.3f} is above {alpha}: this gap is within what "
                            "random labelling produces across this many tests")
        elif not big:
            c.update(verdict="TOO_SMALL",
                     reason=f"{c['relative_effect']:+.1%} is under the {min_effect:.0%} floor: "
                            "not worth changing anything over")
        else:
            c.update(verdict="SUPPORTED",
                     reason=f"{c['relative_effect']:+.1%} median difference, adjusted p {q:.3f}")

    supported = [c for c in candidates if c.get("verdict") == "SUPPORTED"]
    raw_pass = [c for c in family if c["p_raw"] <= alpha
                and (c["relative_effect"] is None or abs(c["relative_effect"]) >= min_effect)]
    m = len(family)
    drift = sd.spearman(time_rank, values) if has_time else None
    result = {
        "verdict": "PATTERNS_FOUND" if supported else "NOTHING_SURVIVED",
        "exit_code": 0 if supported else 2,
        "posts": n,
        "inputs": info,
        "method": {"statistic": "difference of medians, two-sided permutation test",
                   "correction": correction, "alpha": alpha, "min_group": min_group,
                   "min_relative_effect": min_effect, "seed": SEED},
        "attributes_declared": attributes,
        "family_size": m,
        "accounting": {
            "tested": m,
            "expected_false_passes_without_correction": round(m * alpha, 1),
            "passed_without_correction": len(raw_pass),
            "passed_after_correction": len(supported),
        },
        "supported": supported,
        "all_candidates": candidates,
        "mirrored_skipped": mirrored,
        "caveats": [
            "Levels of one attribute are tested against the same posts, so they are not "
            "independent. Read them as one question about that attribute.",
            "A pattern in past posts is a hypothesis. You chose formats, topics, and days for "
            "reasons that also affect results. No statistic on this data removes that.",
        ],
        "next_step": "Send a supported candidate to size_experiment.py and run it as a planned, "
                     "alternating test. Until then it is a lead, not a finding.",
    }
    warnings = []
    if drift is not None and abs(drift) >= TIME_FLAG:
        warnings.append(f"The metric trends with time (rho {drift:+.2f}). The permutation null "
                        "assumes posts are interchangeable; treat every p-value here as optimistic.")
    flagged = [f"{c['attribute']}={c['value']}" for c in candidates if c.get("time_confounded")]
    if flagged:
        warnings.append("Group is lopsided in time, so it is confounded with period: "
                        + ", ".join(flagged) + ".")
    if warnings:
        result["warnings"] = warnings
    return result


def render(r: dict) -> str:
    if r["verdict"] == "INSUFFICIENT_DATA":
        return f"Pattern test: INSUFFICIENT_DATA\n{r['finding']}\nInstead: {r['instead']}"
    me, a = r["method"], r["accounting"]
    lines = [f"Pattern test: {r['verdict']} ({r['posts']} posts, metric {r['inputs']['metric']})",
             "=" * 66,
             f"Method   {me['statistic']}; correction {me['correction']}; alpha {me['alpha']}; "
             f"effect floor {me['min_relative_effect']:.0%}; seed {me['seed']}",
             f"Declared {', '.join(r['attributes_declared'])}"]
    lines += [f"  ! {w}" for w in r.get("warnings", [])]
    lines += ["", f"Accounting: {a['tested']} tests. Uncorrected, about "
              f"{a['expected_false_passes_without_correction']} would pass on noise alone; "
              f"{a['passed_without_correction']} did. After correction: {a['passed_after_correction']}.",
              "", "Candidates:"]
    for c in r["all_candidates"]:
        tag = c["verdict"]
        extra = ""
        if "p_adjusted" in c:
            ci = c["interval_90"]
            extra = (f" raw p {c['p_raw']}, adj p {c['p_adjusted']}"
                     + (f", 90% CI {ci[0]:+.0%}..{ci[1]:+.0%}" if ci else "")
                     + (", TIME-CONFOUNDED" if c.get("time_confounded") else ""))
        lines.append(f"  [{tag:<13}] {c['attribute']}={c['value']} "
                     f"(n {c.get('n_group', '?')} vs {c.get('n_rest', '?')}){extra}")
        lines.append(f"                  {c['reason']}")
    for note in r["mirrored_skipped"]:
        lines.append(f"  skipped: {note}")
    lines += ["", *[f"- {c}" for c in r["caveats"]], "", r["next_step"]]
    if r["verdict"] == "NOTHING_SURVIVED":
        lines.append("\nNothing survived. Report that as the finding. Do not re-slice the data.")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Permutation-test candidate patterns with a "
                                             "multiple-comparisons gate.")
    ap.add_argument("--input", help="CSV or JSON file, or - for stdin")
    ap.add_argument("--sample", action="store_true", help="use the bundled synthetic export")
    ap.add_argument("--metric", default="engagement_rate",
                    help="engagement_rate (default), exposure, or any numeric column name")
    ap.add_argument("--exposure-col")
    ap.add_argument("--interaction-cols", help="comma-separated")
    ap.add_argument("--attribute", action="append", default=[],
                    help="candidate to test; repeatable; see the forms in --help text above")
    ap.add_argument("--correction", choices=["bh", "holm", "none"], default="bh")
    ap.add_argument("--alpha", type=float, default=0.10)
    ap.add_argument("--min-group", type=int, default=5)
    ap.add_argument("--min-effect", type=float, default=0.15)
    ap.add_argument("--shuffles", type=int, default=5000)
    ap.add_argument("--output", choices=["json", "human"], default="json")
    args = ap.parse_args()
    if not (args.input or args.sample):
        ap.error("--input or --sample is required")

    try:
        rows = sd.load_rows(str(SAMPLE_PATH) if args.sample else args.input)
        records, info = sd.build_records(
            rows, args.metric, args.exposure_col,
            args.interaction_cols.split(",") if args.interaction_cols else None)
        if not records:
            raise sd.DataError("no row has a usable exposure and metric value")
        attributes = args.attribute or default_attributes(records, info)
        if not attributes:
            raise sd.DataError("no candidate attributes. Pass --attribute <column>.")
        result = mine(records, info, attributes, args.alpha, args.correction,
                      args.min_group, args.min_effect, args.shuffles)
    except sd.DataError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 4
    print(json.dumps(result, indent=2) if args.output == "json" else render(result))
    return result["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
