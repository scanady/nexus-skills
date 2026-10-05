#!/usr/bin/env python3
"""Two-group and categorical hypothesis tests from summary numbers.

Standard library only. Reports the estimate, a confidence interval, the p-value,
an effect size, and the validity warnings that apply to the inputs. It does not
decide whether to ship; that stays with the analyst.

  proportions  two-proportion z-test (conversion, click, retention)
  means        Welch two-sample t-test (revenue, latency, session length)
  chi2         chi-squared goodness of fit (--observed/--expected)
               or independence (--table "a,b;c,d")

Examples:
  hypothesis_test.py proportions --n1 5000 --x1 250 --n2 5000 --x2 310
  hypothesis_test.py means --mean1 42.3 --sd1 18.1 --n1 800 --mean2 46.1 --sd2 19.4 --n2 820
  hypothesis_test.py chi2 --observed 4980,5120 --expected 1,1      # sample-ratio check
  hypothesis_test.py chi2 --table "120,80;90,110"
"""

import argparse
import json
import math
import sys

from statlib import (chi2_p, effect_label, normal_cdf, t_critical,
                     t_two_sided_p, z_critical)


def fail(message: str):
    sys.exit(f"error: {message}")


def proportions(n1, x1, n2, x2, alpha):
    if min(n1, n2) <= 0:
        fail("group sizes must be positive")
    if not (0 <= x1 <= n1 and 0 <= x2 <= n2):
        fail("successes must be between 0 and the group size")
    p1, p2 = x1 / n1, x2 / n2
    pooled = (x1 + x2) / (n1 + n2)
    se_pooled = math.sqrt(pooled * (1 - pooled) * (1 / n1 + 1 / n2))
    if se_pooled == 0:
        fail("both groups are all successes or all failures; no variance to test")
    z = (p2 - p1) / se_pooled
    p_value = 2 * (1 - normal_cdf(abs(z)))
    diff = p2 - p1
    se_diff = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    margin = z_critical(alpha) * se_diff
    h = 2 * math.asin(math.sqrt(p2)) - 2 * math.asin(math.sqrt(p1))
    warnings = []
    for label, n, x in (("group 1", n1, x1), ("group 2", n2, x2)):
        if x < 10 or n - x < 10:
            warnings.append(f"{label} has fewer than 10 events or non-events; "
                            "the normal approximation is weak. Use an exact test.")
    return {
        "test": "two-proportion z-test",
        "group1": {"n": n1, "x": x1, "rate": p1},
        "group2": {"n": n2, "x": x2, "rate": p2},
        "difference": diff,
        "relative_lift": diff / p1 if p1 else None,
        "statistic": z,
        "p_value": p_value,
        "ci": [diff - margin, diff + margin],
        "effect": {"name": "Cohen's h", "value": h, "label": effect_label(h, "h")},
        "warnings": warnings,
    }


def means(m1, s1, n1, m2, s2, n2, alpha):
    if min(n1, n2) < 2:
        fail("each group needs at least 2 observations")
    if s1 < 0 or s2 < 0:
        fail("standard deviations must be non-negative")
    v1, v2 = s1 ** 2 / n1, s2 ** 2 / n2
    se = math.sqrt(v1 + v2)
    if se == 0:
        fail("both standard deviations are zero; no variance to test")
    diff = m2 - m1
    t = diff / se
    df = (v1 + v2) ** 2 / (v1 ** 2 / (n1 - 1) + v2 ** 2 / (n2 - 1))
    p_value = t_two_sided_p(t, df)
    margin = t_critical(alpha, df) * se
    pooled_sd = math.sqrt(((n1 - 1) * s1 ** 2 + (n2 - 1) * s2 ** 2) / (n1 + n2 - 2))
    d = diff / pooled_sd if pooled_sd else 0.0
    warnings = []
    if min(n1, n2) < 30:
        warnings.append("a group has fewer than 30 observations; "
                        "check the raw data for skew before trusting the t-test.")
    for label, m, s in (("group 1", m1, s1), ("group 2", m2, s2)):
        if m > 0 and s > 2 * m:
            warnings.append(f"{label} sd is over twice its mean; the metric is likely "
                            "heavy-tailed. Compare medians or log values instead.")
    return {
        "test": "Welch two-sample t-test",
        "group1": {"n": n1, "mean": m1, "sd": s1},
        "group2": {"n": n2, "mean": m2, "sd": s2},
        "difference": diff,
        "relative_lift": diff / m1 if m1 else None,
        "statistic": t,
        "df": df,
        "p_value": p_value,
        "ci": [diff - margin, diff + margin],
        "effect": {"name": "Cohen's d", "value": d, "label": effect_label(d, "d")},
        "warnings": warnings,
    }


def parse_numbers(text: str, name: str):
    try:
        return [float(part) for part in text.split(",")]
    except ValueError:
        fail(f"--{name} must be comma-separated numbers")


def parse_table(text: str):
    try:
        rows = [[float(c) for c in row.split(",")] for row in text.split(";")]
    except ValueError:
        fail("--table must look like \"a,b;c,d\"")
    if len(rows) < 2 or any(len(r) != len(rows[0]) for r in rows) or len(rows[0]) < 2:
        fail("--table needs at least 2 rows and 2 columns, all rows the same length")
    return rows


def chi2_fit(observed, expected, alpha):
    if len(observed) != len(expected) or len(observed) < 2:
        fail("--observed and --expected need the same length, at least 2 categories")
    if min(expected) <= 0 or min(observed) < 0:
        fail("expected values must be positive and observed values non-negative")
    total = sum(observed)
    scale = total / sum(expected)
    expected = [e * scale for e in expected]
    stat = sum((o - e) ** 2 / e for o, e in zip(observed, expected))
    df = len(observed) - 1
    v = math.sqrt(stat / (total * df))
    warnings = []
    if min(expected) < 5:
        warnings.append("an expected count is below 5; merge categories or use an exact test.")
    return {
        "test": "chi-squared goodness of fit",
        "observed": observed,
        "expected": [round(e, 3) for e in expected],
        "statistic": stat,
        "df": df,
        "p_value": chi2_p(stat, df),
        "effect": {"name": "Cramer's V (k-1 scaled)", "value": v, "label": effect_label(v, "v")},
        "warnings": warnings,
    }


def chi2_independence(rows, alpha):
    row_sums = [sum(r) for r in rows]
    col_sums = [sum(c) for c in zip(*rows)]
    total = sum(row_sums)
    if min(row_sums) == 0 or min(col_sums) == 0:
        fail("a row or column of the table sums to zero")
    expected = [[rs * cs / total for cs in col_sums] for rs in row_sums]
    stat = sum((o - e) ** 2 / e for ro, re in zip(rows, expected) for o, e in zip(ro, re))
    df = (len(rows) - 1) * (len(rows[0]) - 1)
    k = min(len(rows), len(rows[0])) - 1
    v = math.sqrt(stat / (total * k))
    warnings = []
    if min(min(r) for r in expected) < 5:
        warnings.append("an expected cell count is below 5; use Fisher's exact test.")
    return {
        "test": "chi-squared test of independence",
        "table": rows,
        "statistic": stat,
        "df": df,
        "p_value": chi2_p(stat, df),
        "effect": {"name": "Cramer's V", "value": v, "label": effect_label(v, "v")},
        "warnings": warnings,
    }


def render(result, alpha):
    p = result["p_value"]
    lines = [result["test"]]
    for key in ("group1", "group2"):
        if key in result:
            lines.append(f"  {key}: " + ", ".join(f"{k}={v:.6g}" if isinstance(v, float) else f"{k}={v}"
                                                  for k, v in result[key].items()))
    if "difference" in result:
        lift = result["relative_lift"]
        lift_text = f" ({lift:+.1%} relative)" if lift is not None else ""
        lines.append(f"  difference (group2 - group1): {result['difference']:+.6g}{lift_text}")
        lo, hi = result["ci"]
        lines.append(f"  {1 - alpha:.0%} CI for difference: [{lo:.6g}, {hi:.6g}]")
    df = f", df={result['df']:.2f}" if "df" in result else ""
    lines.append(f"  statistic={result['statistic']:.4f}{df}")
    lines.append(f"  p-value={p:.6f} (alpha={alpha})")
    eff = result["effect"]
    lines.append(f"  effect: {eff['name']} = {abs(eff['value']):.4f} ({eff['label']})")
    if p < alpha:
        lines.append("  reading: unlikely under no difference. This says nothing about size or cause.")
        if eff["label"] == "negligible":
            lines.append("  note: effect size is negligible. Check practical value before acting.")
    else:
        lines.append("  reading: data cannot separate the difference from zero. "
                     "This is not proof of no effect; read the CI and check power.")
    for warning in result["warnings"]:
        lines.append(f"  WARNING: {warning}")
    return "\n".join(lines)


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--alpha", type=float, default=0.05, help="significance level (default 0.05)")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    sub = parser.add_subparsers(dest="test", required=True)

    prop = sub.add_parser("proportions")
    for name in ("n1", "x1", "n2", "x2"):
        prop.add_argument(f"--{name}", type=int, required=True)

    mean = sub.add_parser("means")
    for name in ("mean1", "sd1", "mean2", "sd2"):
        mean.add_argument(f"--{name}", type=float, required=True)
    for name in ("n1", "n2"):
        mean.add_argument(f"--{name}", type=int, required=True)

    chi = sub.add_parser("chi2")
    chi.add_argument("--observed", help="comma-separated observed counts")
    chi.add_argument("--expected", help="comma-separated expected counts or ratios")
    chi.add_argument("--table", help="contingency table, rows split by ';', cells by ','")
    return parser


def main():
    args = build_parser().parse_args()
    if not 0 < args.alpha < 1:
        fail("--alpha must be between 0 and 1")
    if args.test == "proportions":
        result = proportions(args.n1, args.x1, args.n2, args.x2, args.alpha)
    elif args.test == "means":
        result = means(args.mean1, args.sd1, args.n1, args.mean2, args.sd2, args.n2, args.alpha)
    elif args.table:
        result = chi2_independence(parse_table(args.table), args.alpha)
    elif args.observed and args.expected:
        result = chi2_fit(parse_numbers(args.observed, "observed"),
                          parse_numbers(args.expected, "expected"), args.alpha)
    else:
        fail("chi2 needs --table, or both --observed and --expected")
    result["alpha"] = args.alpha
    result["significant"] = result["p_value"] < args.alpha
    print(json.dumps(result, indent=2) if args.format == "json" else render(result, args.alpha))


if __name__ == "__main__":
    main()
