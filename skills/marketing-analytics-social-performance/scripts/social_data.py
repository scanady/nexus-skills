"""Shared loading and statistics helpers for the social performance scripts.

Not run directly. profile_posts.py, test_patterns.py and size_experiment.py import it.
Stdlib only.
"""
from __future__ import annotations

import csv
import datetime
import io
import itertools
import json
import math
import random
import sys
from statistics import NormalDist

MIN_POSTS = 10
MAD_TO_SIGMA = 1.4826  # makes MAD estimate a normal standard deviation

# Column names seen in platform exports. First match wins; --exposure-col overrides.
EXPOSURE_ALIASES = ("impressions", "views", "reach", "plays", "video_views", "viewers", "exposure")
INTERACTION_ALIASES = (
    "reactions", "likes", "comments", "replies", "reposts", "shares", "retweets",
    "quotes", "saves", "bookmarks",
)
DATE_ALIASES = ("date", "published", "published_at", "posted_at", "created_at", "day")
WEEKDAYS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")


class DataError(Exception):
    """Input cannot be used. The message tells the user how to fix it."""


# ---------- loading ----------

def read_text(path: str) -> str:
    return sys.stdin.read() if path == "-" else open(path, encoding="utf-8-sig").read()


def load_rows(path: str) -> list[dict]:
    """Read CSV or JSON (a list of objects, or {"posts": [...]})."""
    raw = read_text(path)
    try:
        if raw.lstrip().startswith(("[", "{")):
            data = json.loads(raw)
            if isinstance(data, dict):
                data = data.get("posts") or data.get("rows") or []
            return [dict(r) for r in data]
        return [dict(r) for r in csv.DictReader(io.StringIO(raw))]
    except (json.JSONDecodeError, csv.Error, TypeError) as exc:
        raise DataError(f"could not parse input: {exc}") from exc


def to_float(value) -> float | None:
    if value is None or str(value).strip() == "":
        return None
    try:
        return float(str(value).replace(",", "").replace("%", "").strip())
    except ValueError:
        return None


def parse_date(value) -> datetime.date | None:
    text = str(value or "").strip()
    for fmt, size in (("%Y-%m-%d", 10), ("%m/%d/%Y", 10), ("%d.%m.%Y", 10)):
        try:
            return datetime.datetime.strptime(text[:size], fmt).date()
        except ValueError:
            continue
    return None


def first_present(columns, candidates) -> str | None:
    lowered = {c.lower(): c for c in columns}
    return next((lowered[a] for a in candidates if a in lowered), None)


# ---------- records ----------

def build_records(rows: list[dict], metric: str = "engagement_rate",
                  exposure_col: str | None = None,
                  interaction_cols: list[str] | None = None) -> tuple[list[dict], dict]:
    """Return (records, info). Each record: value, exposure, date, row.

    metric: "engagement_rate" = sum(interactions) / exposure,
            "exposure"        = the exposure column itself,
            anything else     = a numeric column of that name, used as is.
    """
    if not rows:
        raise DataError("no rows in input")
    columns = list(rows[0].keys())
    exposure = exposure_col or first_present(columns, EXPOSURE_ALIASES)
    if metric in ("engagement_rate", "exposure") and not exposure:
        raise DataError("no exposure column found (looked for: " + ", ".join(EXPOSURE_ALIASES)
                        + "). Name it with --exposure-col.")
    if metric == "engagement_rate":
        interactions = interaction_cols or [c for c in columns if c.lower() in INTERACTION_ALIASES]
        if not interactions:
            raise DataError("no interaction columns found (looked for: "
                            + ", ".join(INTERACTION_ALIASES) + "). Name them with --interaction-cols.")
    else:
        interactions = []
        if metric != "exposure" and metric not in columns:
            raise DataError(f"metric column '{metric}' not in input. Columns: {', '.join(columns)}")
    date_col = first_present(columns, DATE_ALIASES)

    records, dropped = [], 0
    for i, row in enumerate(rows):
        expo = to_float(row.get(exposure)) if exposure else None
        if metric == "engagement_rate":
            parts = [to_float(row.get(c)) or 0.0 for c in interactions]
            value = sum(parts) / expo if expo and expo > 0 else None
        elif metric == "exposure":
            value = expo if expo and expo > 0 else None
        else:
            value = to_float(row.get(metric))
        if value is None or (exposure and (expo is None or expo <= 0)):
            dropped += 1
            continue
        records.append({"i": i, "value": value, "exposure": expo,
                        "date": parse_date(row.get(date_col)) if date_col else None, "row": row})
    info = {"metric": metric, "exposure_col": exposure, "interaction_cols": interactions,
            "date_col": date_col, "rows_read": len(rows), "rows_used": len(records),
            "rows_dropped": dropped}
    return records, info


def time_ordered(records: list[dict]) -> bool:
    return bool(records) and all(r["date"] for r in records)


# ---------- statistics ----------

def median(xs) -> float:
    s = sorted(xs)
    n = len(s)
    if not n:
        return 0.0
    mid = n // 2
    return float(s[mid]) if n % 2 else (s[mid - 1] + s[mid]) / 2.0


def mad(xs) -> float:
    m = median(xs)
    return median([abs(x - m) for x in xs])


def percentile(xs, p: float) -> float:
    s = sorted(xs)
    if not s:
        return 0.0
    k = (len(s) - 1) * p / 100.0
    lo = int(k)
    hi = min(lo + 1, len(s) - 1)
    return float(s[lo] + (s[hi] - s[lo]) * (k - lo))


def positive_logs(xs) -> tuple[list[float], int]:
    """Natural logs of the positive values, and how many values were dropped."""
    logs = [math.log(x) for x in xs if x > 0]
    return logs, len(xs) - len(logs)


def robust_sigma_log(xs) -> float | None:
    """Spread on the log scale: the planning input for size_experiment.py."""
    logs, _ = positive_logs(xs)
    return MAD_TO_SIGMA * mad(logs) if len(logs) >= 3 else None


def _avg_ranks(xs) -> list[float]:
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    ranks = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        for k in range(i, j + 1):
            ranks[order[k]] = (i + j) / 2.0 + 1
        i = j + 1
    return ranks


def spearman(xs, ys) -> float | None:
    if len(xs) < 3 or len(xs) != len(ys):
        return None
    rx, ry = _avg_ranks(xs), _avg_ranks(ys)
    mx, my = sum(rx) / len(rx), sum(ry) / len(ry)
    sxx = sum((a - mx) ** 2 for a in rx)
    syy = sum((b - my) ** 2 for b in ry)
    if sxx == 0 or syy == 0:
        return None
    return sum((a - mx) * (b - my) for a, b in zip(rx, ry)) / math.sqrt(sxx * syy)


def z_two_sided(alpha: float) -> float:
    return NormalDist().inv_cdf(1 - alpha / 2)


def z_power(power: float) -> float:
    return NormalDist().inv_cdf(power)


def permutation_p(group: list[float], rest: list[float], rng: random.Random,
                  shuffles: int, exact_limit: int = 20000) -> tuple[float, str]:
    """Two-sided permutation p-value for the difference of medians.

    Exact when the number of ways to pick the group is at most exact_limit,
    otherwise Monte Carlo with the +1 correction so p is never reported as 0.
    """
    pool = group + rest
    n, k = len(pool), len(group)
    tol = abs(median(group) - median(rest)) - 1e-12
    if exact_limit and math.comb(n, k) <= exact_limit:
        extreme = total = 0
        for chosen in itertools.combinations(range(n), k):
            picked = set(chosen)
            a = [pool[i] for i in chosen]
            b = [pool[i] for i in range(n) if i not in picked]
            extreme += abs(median(a) - median(b)) >= tol
            total += 1
        return extreme / total, "exact"
    extreme = 0
    for _ in range(shuffles):
        rng.shuffle(pool)
        extreme += abs(median(pool[:k]) - median(pool[k:])) >= tol
    return (extreme + 1) / (shuffles + 1), f"monte-carlo ({shuffles} shuffles)"
