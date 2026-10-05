#!/usr/bin/env python3
"""Size a two-arm posting experiment, check it by simulation, and write the plan before the first post.

A pattern found in past posts is a hypothesis. A planned test can confirm it, but
only if you can afford enough posts. This script answers: how many posts per arm,
how many weeks at your cadence, and what the smallest effect is that your window
can detect.

Sizing runs on the log scale. Engagement and reach are ratio-like and right
skewed, so a "30% lift" is a shift of ln(1.30) between arm means of log values,
with spread sigma_log (from profile_posts.py). The planned analysis is a
permutation test on the difference of medians, so --simulate checks the sample
size against that test directly instead of trusting the normal approximation.

If you plan to compare several things in one run, give --comparisons. The test
level is split across them (Bonferroni), which raises the number of posts. That
is the cost of looking at more than one thing.

Usage:
    python3 size_experiment.py --hypothesis "Video earns a higher engagement rate than text" \\
        --variable "format: video vs text" --sigma-log 0.33 --effect 0.30 \\
        --posts-per-week 3 --max-weeks 12 --simulate --output human
    python3 size_experiment.py --sample --output human

Exit codes: 0 feasible in the window | 2 too long (smallest detectable effect returned) | 3 refused
Stdlib only. No network. Deterministic.
"""
from __future__ import annotations

import argparse
import json
import math
import random
import sys

import social_data as sd

SEED = 20260825
MIN_ACTIONABLE_EFFECT = 0.10
SIM_SHUFFLES = 299
HOLD_CONSTANT = [
    "Randomize arm order in small blocks (the arm order given in the plan does this). Strict A,B,A,B can "
    "line up with weekdays and then you are testing the weekday.",
    "Fix posting time. Hour and weekday often move results more than the variable under test.",
    "Change one thing. Same topic mix, same length range, same call to action in both arms.",
    "Freeze profile, bio, pinned content, and cadence for the whole window.",
    "Record each post's arm before publishing. An arm picked after the numbers are in is "
    "not an experiment.",
]
SAMPLE = {
    "hypothesis": "Short video earns a higher engagement rate than text posts for my audience",
    "variable": "format: video vs text",
    "sigma_log": 0.33, "effect": 0.45, "posts_per_week": 4, "max_weeks": 12,
}


def sigma_from_cv(cv: float) -> float:
    return math.sqrt(math.log(1 + cv * cv))


def n_per_arm(sigma: float, effect: float, alpha: float, power: float) -> int:
    """Two-sample size on the log scale, with a small-sample correction."""
    delta = math.log(1 + effect)
    za, zb = sd.z_two_sided(alpha), sd.z_power(power)
    return math.ceil(2 * (za + zb) ** 2 * sigma ** 2 / delta ** 2 + za ** 2 / 4)


def detectable_effect(sigma: float, n: int, alpha: float, power: float) -> float:
    za, zb = sd.z_two_sided(alpha), sd.z_power(power)
    return math.exp(math.sqrt(2 * (za + zb) ** 2 * sigma ** 2 / max(n, 1))) - 1


def simulated_power(n: int, sigma: float, effect: float, alpha: float,
                    sims: int, rng: random.Random) -> float:
    """Share of simulated experiments where the permutation test finds the effect."""
    shift = math.log(1 + effect)
    hits = 0
    for _ in range(sims):
        a = [math.exp(rng.gauss(0, sigma)) for _ in range(n)]
        b = [math.exp(rng.gauss(shift, sigma)) for _ in range(n)]
        p, _ = sd.permutation_p(b, a, rng, SIM_SHUFFLES, exact_limit=0)
        hits += p <= alpha
    return hits / sims


def assignment(total_per_arm: int, rng: random.Random) -> str:
    order = []
    for _ in range(total_per_arm):
        pair = ["A", "B"]
        rng.shuffle(pair)
        order += pair
    return " ".join(order)


def plan(a: argparse.Namespace) -> dict:
    if not a.hypothesis.strip() or not a.variable.strip():
        return refuse("No hypothesis or no named variable.",
                      "State a claim that can be wrong: 'X earns a higher <metric> than Y for my "
                      "audience', and name the one thing that differs between arms.")
    if a.effect < MIN_ACTIONABLE_EFFECT:
        return refuse(f"A {a.effect:.0%} lift is below the {MIN_ACTIONABLE_EFFECT:.0%} floor.",
                      "Test only what you would act on. Detecting a 5% lift takes hundreds of posts "
                      "and changes no decision.")
    sigma = a.sigma_log if a.sigma_log else (sigma_from_cv(a.cv) if a.cv else 0.0)
    if sigma <= 0:
        return refuse("No spread estimate.",
                      "Run profile_posts.py and pass planning_inputs.sigma_log as --sigma-log. "
                      "Under 10 posts you have no usable estimate.")

    alpha = a.alpha / a.comparisons
    n = n_per_arm(sigma, a.effect, alpha, a.power)
    rng = random.Random(SEED)
    sim = None
    if a.simulate:
        power_at_n = first_power = simulated_power(n, sigma, a.effect, alpha, a.sims, rng)
        se = math.sqrt(power_at_n * (1 - power_at_n) / a.sims)
        grown = n
        while power_at_n < a.power - se and grown < 3 * n:
            grown = math.ceil(grown * 1.1)
            power_at_n = simulated_power(grown, sigma, a.effect, alpha, a.sims, rng)
        sim = {"sims": a.sims, "formula_n": n, "power_at_formula_n": round(first_power, 3),
               "n_after_check": grown, "power_at_n_after_check": round(power_at_n, 3),
               "standard_error": round(se, 3)}
        n = grown

    total = 2 * n
    weeks = math.ceil(total / a.posts_per_week) if a.posts_per_week > 0 else 10 ** 6
    out = {
        "hypothesis": a.hypothesis.strip(), "variable": a.variable.strip(),
        "design": {"arms": 2, "alpha": a.alpha, "comparisons": a.comparisons,
                   "alpha_per_comparison": round(alpha, 4), "power": a.power,
                   "sigma_log": round(sigma, 4), "target_lift": a.effect,
                   "posts_per_arm": n, "total_posts": total,
                   "posts_per_week": a.posts_per_week, "weeks_needed": weeks},
        "simulation": sim,
        "hold_constant": HOLD_CONSTANT,
        "analysis_rule": "Primary test: permutation test on the difference of medians between "
                         "arms (test_patterns.py with the arm as the one declared attribute). "
                         "No t-test; one breakout post would decide it.",
        "caveat": "Posts are not independent draws: a news-heavy week moves both arms. Treat the "
                  "size as a planning estimate, not a power guarantee.",
    }
    if weeks > a.max_weeks:
        affordable = max(1, int(a.max_weeks * a.posts_per_week / 2))
        mde = detectable_effect(sigma, affordable, alpha, a.power)
        out.update(
            verdict="TOO_LONG", exit_code=2,
            finding=f"{total} posts at {a.posts_per_week}/week is {weeks} weeks. Your window is "
                    f"{a.max_weeks}.",
            minimum_detectable_lift_in_window=round(mde, 3),
            options=[
                f"Accept a larger target: in {a.max_weeks} weeks you can detect about {mde:.0%}. "
                f"If a {mde:.0%} lift would still change what you do, run that test.",
                "Raise cadence only if you can hold it for the whole window. An abandoned test "
                "is worse than none.",
                "Lower power to 0.70 and call the result directional.",
                "Skip the test and publish what you would rather write. Not every question is "
                "worth a quarter of output.",
            ],
            stop_rule="Changing the plan mid-test ends the test. Restart, or keep the result as "
                      "anecdote.")
        return out
    out.update(
        verdict="FEASIBLE", exit_code=0,
        schedule=f"{n} posts per arm, {a.posts_per_week}/week, about {weeks} weeks.",
        assignment_order=assignment(n, rng),
        falsification=f"If the median of arm B is not at least {a.effect:.0%} above arm A at the "
                      "end, with permutation p below the per-comparison level, the hypothesis "
                      "failed. Write this down before the first post.",
        stop_rule=["Run the full window. Stopping early because it looks good turns a coin flip "
                   "into a strategy.",
                   "Stop only if something outside the test changes (job move, viral hit, "
                   "platform change). Then restart instead of salvaging."])
    return out


def refuse(finding: str, fix: str) -> dict:
    return {"verdict": "REFUSED", "exit_code": 3, "finding": finding, "fix": fix}


def render(r: dict) -> str:
    if r["verdict"] == "REFUSED":
        return f"Experiment: REFUSED\n{r['finding']}\nfix: {r['fix']}"
    d = r["design"]
    lines = [f"Experiment: {r['verdict']}", "=" * 62,
             f"Hypothesis  {r['hypothesis']}", f"Variable    {r['variable']}",
             f"Design      2 arms, alpha {d['alpha']}"
             + (f" split over {d['comparisons']} comparisons ({d['alpha_per_comparison']} each)"
                if d["comparisons"] > 1 else "")
             + f", power {d['power']}, sigma_log {d['sigma_log']}, target lift {d['target_lift']:.0%}",
             f"Sample      {d['posts_per_arm']} posts per arm, {d['total_posts']} total = "
             f"{d['weeks_needed']} weeks at {d['posts_per_week']}/week"]
    if r["simulation"]:
        s = r["simulation"]
        lines.append(f"Simulation  permutation-test power at n={s['n_after_check']}: "
                     f"{s['power_at_n_after_check']:.0%} over {s['sims']} runs (+/- {s['standard_error']:.0%})")
    lines.append("")
    if r["verdict"] == "TOO_LONG":
        lines += [r["finding"], f"Smallest lift detectable in the window: "
                  f"{r['minimum_detectable_lift_in_window']:.0%}", "", "Options:"]
        lines += [f"  - {o}" for o in r["options"]] + ["", f"Stop rule: {r['stop_rule']}"]
    else:
        lines += [f"Schedule: {r['schedule']}", f"Falsification: {r['falsification']}", "",
                  "Stop rule:", *[f"  - {s}" for s in r["stop_rule"]], "",
                  f"Arm order (A = control, B = variant): {r['assignment_order']}"]
    lines += ["", "Hold constant:", *[f"  - {h}" for h in r["hold_constant"]], "",
              r["analysis_rule"], "", r["caveat"]]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Size a two-arm posting experiment.")
    ap.add_argument("--hypothesis", default="")
    ap.add_argument("--variable", default="")
    ap.add_argument("--sigma-log", type=float, default=0.0,
                    help="spread on the log scale, from profile_posts.py (planning_inputs.sigma_log)")
    ap.add_argument("--cv", type=float, default=0.0, help="coefficient of variation, if no sigma-log")
    ap.add_argument("--effect", type=float, default=0.30, help="relative lift you would act on (0.30 = +30%%)")
    ap.add_argument("--posts-per-week", type=float, default=2.0)
    ap.add_argument("--max-weeks", type=int, default=12)
    ap.add_argument("--alpha", type=float, default=0.10, help="two-sided test level")
    ap.add_argument("--power", type=float, default=0.80)
    ap.add_argument("--comparisons", type=int, default=1, help="comparisons planned in this run")
    ap.add_argument("--simulate", action="store_true", help="verify n against the permutation test")
    ap.add_argument("--sims", type=int, default=300)
    ap.add_argument("--output", choices=["json", "human"], default="json")
    ap.add_argument("--sample", action="store_true", help="size a built-in example")
    a = ap.parse_args()

    if a.sample:
        for key, value in SAMPLE.items():
            setattr(a, key, value)
    if not 0 < a.alpha < 1 or not 0.5 <= a.power < 1 or a.comparisons < 1:
        ap.error("alpha must be in (0,1), power in [0.5,1), comparisons at least 1")
    result = plan(a)
    print(json.dumps(result, indent=2) if a.output == "json" else render(result))
    return result["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
