#!/usr/bin/env python3
"""Turn a finished audit check matrix into a weighted 0-100 SEO health score.

Usage:
    python3 seo_health_scorer.py --checks checks.json
    python3 seo_health_scorer.py --checks checks.json --profile saas --json
    python3 seo_health_scorer.py --demo

Input: a JSON array. One object per check:
    {"category": "technical", "check": "robots.txt allows key pages",
     "result": "pass|warn|fail", "severity": "critical|high|medium|low",
     "detail": "optional evidence"}

Categories: technical, architecture, on_page, content, schema, performance,
ai_readiness, images. Inside a category, a check counts by severity weight
(critical 4, high 3, medium 2, low 1) times result (pass 1, warn 0.5, fail 0).
A category with no checks is left out and the other weights are rescaled.
Any failed critical check caps the grade at C. Stdlib only.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WEIGHTS = {
    "technical": 0.20,
    "content": 0.20,
    "on_page": 0.15,
    "performance": 0.14,
    "architecture": 0.10,
    "schema": 0.08,
    "ai_readiness": 0.08,
    "images": 0.05,
}

# Profile deltas. Each profile sums to zero.
PROFILES = {
    "saas": {"technical": 0.04, "architecture": 0.03, "content": 0.02, "schema": -0.04, "images": -0.05},
    "ecommerce": {"schema": 0.05, "images": 0.04, "architecture": 0.03, "content": -0.06, "ai_readiness": -0.06},
    "local": {"on_page": 0.05, "schema": 0.05, "technical": -0.04, "ai_readiness": -0.06},
    "publisher": {"content": 0.06, "ai_readiness": 0.04, "technical": -0.05, "schema": -0.05},
}

RESULT_VALUE = {"pass": 1.0, "warn": 0.5, "fail": 0.0}
SEVERITY_WEIGHT = {"critical": 4, "high": 3, "medium": 2, "low": 1}
SEVERITY_RANK = {s: i for i, s in enumerate(SEVERITY_WEIGHT)}

DEMO = [
    ("technical", "robots.txt allows key pages", "pass", "critical", ""),
    ("technical", "sitemap lists only canonical 200 URLs", "warn", "high", "31 redirected URLs listed"),
    ("technical", "no redirect chains", "fail", "high", "6 chains of 3+ hops"),
    ("technical", "HTTPS with no mixed content", "pass", "critical", ""),
    ("architecture", "key pages within 3 clicks", "warn", "high", "14% of pages at depth 4+"),
    ("architecture", "no orphan pages", "fail", "medium", "22 orphan candidates"),
    ("on_page", "unique titles of 30-60 chars", "warn", "high", "9 pages over 60 chars"),
    ("on_page", "one H1 per page", "pass", "high", ""),
    ("on_page", "meta descriptions present", "fail", "medium", "12 pages missing"),
    ("content", "no thin pages", "fail", "high", "8 pages under 300 words with no search intent match"),
    ("content", "author and sources shown (E-E-A-T)", "warn", "high", "no author bios on blog"),
    ("schema", "Organization + BreadcrumbList present", "warn", "medium", "no breadcrumb markup"),
    ("performance", "LCP p75 <= 2.5s", "pass", "critical", ""),
    ("performance", "INP p75 <= 200ms", "pass", "high", ""),
    ("performance", "CLS p75 <= 0.1", "warn", "high", "CLS 0.14 on mobile"),
    ("ai_readiness", "answer-first openings under H2s", "warn", "low", ""),
    ("images", "modern formats and lazy loading", "pass", "low", ""),
]


def die(msg: str) -> None:
    print(f"[error] {msg}", file=sys.stderr)
    sys.exit(1)


def load_checks(raw: object) -> list[dict]:
    if not isinstance(raw, list) or not raw:
        die("checks must be a non-empty JSON array")
    checks = []
    for i, c in enumerate(raw):
        if not isinstance(c, dict):
            die(f"check #{i} is not an object")
        cat = str(c.get("category", "")).lower().replace("-", "_").replace(" ", "_")
        res = str(c.get("result", "")).lower()
        sev = str(c.get("severity", "medium")).lower()
        if cat not in WEIGHTS:
            die(f"check #{i}: unknown category '{cat}'. Use: {', '.join(WEIGHTS)}")
        if res not in RESULT_VALUE:
            die(f"check #{i}: result must be pass, warn or fail (got '{res}')")
        if sev not in SEVERITY_WEIGHT:
            die(f"check #{i}: severity must be critical, high, medium or low (got '{sev}')")
        checks.append({"category": cat, "check": str(c.get("check", "")), "result": res,
                       "severity": sev, "detail": str(c.get("detail", ""))})
    return checks


def weights_for(profile: str | None) -> dict[str, float]:
    w = dict(WEIGHTS)
    for cat, delta in PROFILES.get(profile or "", {}).items():
        w[cat] = max(0.0, w[cat] + delta)
    return w


def grade(score: float, critical_fail: bool) -> str:
    letter = "A" if score >= 90 else "B" if score >= 75 else "C" if score >= 60 else "D" if score >= 40 else "F"
    return "C" if critical_fail and letter in "AB" else letter


def score(checks: list[dict], profile: str | None = None) -> dict:
    weights = weights_for(profile)
    cats: dict[str, float] = {}
    for cat in weights:
        rows = [c for c in checks if c["category"] == cat]
        if rows:
            earned = sum(SEVERITY_WEIGHT[c["severity"]] * RESULT_VALUE[c["result"]] for c in rows)
            cats[cat] = round(100 * earned / sum(SEVERITY_WEIGHT[c["severity"]] for c in rows), 1)

    used = sum(weights[c] for c in cats)
    overall = round(sum(cats[c] * weights[c] for c in cats) / used, 1) if used else 0.0
    critical_fail = any(c["severity"] == "critical" and c["result"] == "fail" for c in checks)

    issues = sorted(
        (c for c in checks if c["result"] != "pass"),
        key=lambda c: (SEVERITY_RANK[c["severity"]], c["result"] != "fail"),
    )
    return {
        "overall_score": overall,
        "grade": grade(overall, critical_fail),
        "grade_capped_by_critical_fail": critical_fail and overall >= 75,
        "profile": profile or "general",
        "category_scores": cats,
        "unscored_categories": [c for c in weights if c not in cats],
        "counts": {r: sum(1 for c in checks if c["result"] == r) for r in RESULT_VALUE},
        "issues": issues,
        "near_misses": [c for c in issues if c["result"] == "warn" and c["severity"] in ("critical", "high")],
    }


def render(r: dict) -> None:
    n = r["counts"]
    print(f"SEO health: {r['overall_score']}/100, grade {r['grade']} (profile: {r['profile']})")
    if r["grade_capped_by_critical_fail"]:
        print("  Grade capped at C: a critical check failed.")
    print(f"Checks: {n['pass']} pass, {n['warn']} warn, {n['fail']} fail\n")
    for cat, s in sorted(r["category_scores"].items(), key=lambda kv: kv[1]):
        print(f"  {cat:<13} {'#' * int(s / 5):<20} {s:5.1f}")
    if r["unscored_categories"]:
        print(f"  not scored: {', '.join(r['unscored_categories'])}")
    print()
    for sev in SEVERITY_WEIGHT:
        rows = [i for i in r["issues"] if i["severity"] == sev]
        if rows:
            print(f"{sev.upper()} ({len(rows)})")
            for i in rows:
                print(f"  [{i['result'].upper()}] {i['category']}: {i['check']}" + (f" - {i['detail']}" if i["detail"] else ""))
    if r["near_misses"]:
        print("\nNear misses (warn on critical/high; cheapest path to pass):")
        for i in r["near_misses"]:
            print(f"  {i['check']}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Weighted 0-100 SEO health score from a check matrix.")
    ap.add_argument("--checks", help="path to checks JSON")
    ap.add_argument("--profile", choices=sorted(PROFILES), help="site type; shifts category weights")
    ap.add_argument("--json", action="store_true", help="JSON output")
    ap.add_argument("--demo", action="store_true", help="score built-in sample checks")
    args = ap.parse_args()

    if args.demo:
        raw = [dict(zip(("category", "check", "result", "severity", "detail"), row)) for row in DEMO]
    elif args.checks:
        path = Path(args.checks)
        if not path.is_file():
            die(f"{path} not found")
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            die(f"{path} is not valid JSON: {e}")
    else:
        ap.print_help()
        return

    result = score(load_checks(raw), args.profile)
    print(json.dumps(result, indent=2)) if args.json else render(result)


if __name__ == "__main__":
    main()
