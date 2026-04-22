#!/usr/bin/env python3
"""RICE feature prioritization with portfolio analysis and quarterly roadmap generation.

Usage:
    rice_prioritizer.py [INPUT] [--capacity MONTHS] [--output FORMAT]

    INPUT     CSV file of features, or "sample" to generate a sample CSV.
              If omitted, runs on built-in demo data.
    --capacity  Team capacity per quarter in person-months (default: 10).
    --output    Output format: text | json | csv (default: text).

CSV format: name,reach,impact,confidence,effort[,description]
  reach       Integer — users affected per quarter
  impact      massive | high | medium | low | minimal
  confidence  high | medium | low
  effort      xl | l | m | s | xs  (person-months: 13 | 8 | 5 | 3 | 1)
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------------------
# Scoring tables
# ---------------------------------------------------------------------------

IMPACT_WEIGHTS: dict[str, float] = {
    "massive": 3.0,
    "high": 2.0,
    "medium": 1.0,
    "low": 0.5,
    "minimal": 0.25,
}

CONFIDENCE_WEIGHTS: dict[str, float] = {
    "high": 1.00,
    "medium": 0.80,
    "low": 0.50,
}

EFFORT_MONTHS: dict[str, int] = {
    "xl": 13,
    "l": 8,
    "m": 5,
    "s": 3,
    "xs": 1,
}

# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------


@dataclass
class Feature:
    name: str
    reach: int
    impact: str
    confidence: str
    effort: str
    description: str = ""
    rice_score: float = field(default=0.0, init=False)

    def __post_init__(self) -> None:
        self.impact = self.impact.strip().lower()
        self.confidence = self.confidence.strip().lower()
        self.effort = self.effort.strip().lower()
        self.rice_score = self._compute()

    def _compute(self) -> float:
        impact = IMPACT_WEIGHTS.get(self.impact, 1.0)
        confidence = CONFIDENCE_WEIGHTS.get(self.confidence, 0.50)
        effort = EFFORT_MONTHS.get(self.effort, 5)
        if effort == 0:
            return 0.0
        return round((self.reach * impact * confidence) / effort, 2)

    def effort_months(self) -> int:
        return EFFORT_MONTHS.get(self.effort, 5)

    @property
    def is_quick_win(self) -> bool:
        return self.impact in ("massive", "high") and self.effort in ("xs", "s")

    @property
    def is_big_bet(self) -> bool:
        return self.impact in ("massive", "high") and self.effort in ("l", "xl")


@dataclass
class Quarter:
    number: int
    capacity: int
    features: list[Feature] = field(default_factory=list)
    used: int = 0

    def fits(self, feature: Feature) -> bool:
        return self.used + feature.effort_months() <= self.capacity

    def add(self, feature: Feature) -> None:
        self.features.append(feature)
        self.used += feature.effort_months()


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------


def prioritize(features: list[Feature]) -> list[Feature]:
    """Return features sorted by RICE score descending."""
    return sorted(features, key=lambda f: f.rice_score, reverse=True)


def portfolio_summary(features: list[Feature]) -> dict:
    """Summarize portfolio balance and key metrics."""
    if not features:
        return {}
    quick_wins = [f for f in features if f.is_quick_win]
    big_bets = [f for f in features if f.is_big_bet]
    return {
        "total_features": len(features),
        "total_effort_months": sum(f.effort_months() for f in features),
        "total_reach": sum(f.reach for f in features),
        "average_rice": round(sum(f.rice_score for f in features) / len(features), 2),
        "quick_wins_count": len(quick_wins),
        "big_bets_count": len(big_bets),
        "quick_wins_top3": quick_wins[:3],
        "big_bets_top3": big_bets[:3],
    }


def build_roadmap(features: list[Feature], capacity: int) -> list[Quarter]:
    """Slot features into quarters by RICE rank within team capacity."""
    quarters: list[Quarter] = []
    current = Quarter(number=1, capacity=capacity)
    for feature in features:
        if current.fits(feature):
            current.add(feature)
        else:
            quarters.append(current)
            current = Quarter(number=len(quarters) + 1, capacity=capacity)
            current.add(feature)
    if current.features:
        quarters.append(current)
    return quarters


# ---------------------------------------------------------------------------
# I/O helpers
# ---------------------------------------------------------------------------

_SAMPLE_ROWS = [
    ("name", "reach", "impact", "confidence", "effort", "description"),
    ("Onboarding Flow", "20000", "massive", "high", "s", "Improve new user onboarding"),
    ("Search Improvements", "15000", "high", "high", "m", "Enhance search functionality"),
    ("Social Login", "12000", "high", "medium", "m", "Add Google/GitHub login"),
    ("Push Notifications", "10000", "massive", "medium", "m", "Mobile push notification support"),
    ("Dark Mode", "8000", "medium", "high", "s", "Dark mode theme"),
    ("Analytics Dashboard", "6000", "high", "medium", "l", "Advanced analytics for users"),
    ("User Dashboard Redesign", "5000", "high", "high", "l", "Redesign main dashboard"),
    ("Team Collaboration", "4000", "massive", "low", "xl", "Real-time collaboration features"),
    ("Export to PDF", "3000", "medium", "low", "s", "Export reports as PDF"),
    ("API Rate Limiting", "2000", "low", "high", "xs", "Add rate limiting to public API"),
]

_DEMO_FEATURES: list[Feature] = [
    Feature("Onboarding Flow", 20000, "massive", "high", "s"),
    Feature("Search Improvements", 15000, "high", "high", "m"),
    Feature("Social Login", 12000, "high", "medium", "m"),
    Feature("Push Notifications", 10000, "massive", "medium", "m"),
    Feature("Dark Mode", 8000, "medium", "high", "s"),
]


def write_sample_csv(path: str = "sample_features.csv") -> None:
    with open(path, "w", newline="", encoding="utf-8") as fh:
        csv.writer(fh).writerows(_SAMPLE_ROWS)
    print(f"Sample CSV written: {path}")


def load_csv(path: str) -> list[Feature]:
    features: list[Feature] = []
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            features.append(
                Feature(
                    name=row.get("name", ""),
                    reach=int(row.get("reach", 0)),
                    impact=row.get("impact", "medium"),
                    confidence=row.get("confidence", "medium"),
                    effort=row.get("effort", "m"),
                    description=row.get("description", ""),
                )
            )
    return features


def _feature_to_dict(f: Feature) -> dict:
    return {
        "name": f.name,
        "reach": f.reach,
        "impact": f.impact,
        "confidence": f.confidence,
        "effort": f.effort,
        "description": f.description,
        "rice_score": f.rice_score,
    }


# ---------------------------------------------------------------------------
# Output formatters
# ---------------------------------------------------------------------------

_SEP = "-" * 56


def format_text(features: list[Feature], summary: dict, roadmap: list[Quarter]) -> str:
    lines: list[str] = [_SEP, "RICE PRIORITIZATION RESULTS", _SEP, ""]

    lines.append("TOP FEATURES  (RICE = reach × impact × confidence / effort)\n")
    for i, f in enumerate(features[:10], 1):
        lines.append(f"  {i:>2}. {f.name}  [RICE: {f.rice_score}]")
        lines.append(
            f"      reach={f.reach}  impact={f.impact}  "
            f"confidence={f.confidence}  effort={f.effort}"
        )

    lines += ["", _SEP, "PORTFOLIO SUMMARY", _SEP]
    lines.append(f"  Features       : {summary.get('total_features', 0)}")
    lines.append(f"  Total effort   : {summary.get('total_effort_months', 0)} person-months")
    lines.append(f"  Total reach    : {summary.get('total_reach', 0):,} users")
    lines.append(f"  Average RICE   : {summary.get('average_rice', 0)}")

    lines += ["", f"  Quick wins ({summary.get('quick_wins_count', 0)}) — high impact, low effort:"]
    for f in summary.get("quick_wins_top3", []):
        lines.append(f"    * {f.name}  (RICE {f.rice_score})")

    lines += ["", f"  Big bets ({summary.get('big_bets_count', 0)}) — high impact, high effort:"]
    for f in summary.get("big_bets_top3", []):
        lines.append(f"    * {f.name}  (RICE {f.rice_score})")

    lines += ["", _SEP, "QUARTERLY ROADMAP", _SEP]
    for q in roadmap:
        lines.append(f"\n  Q{q.number} — {q.used}/{q.capacity} person-months")
        for f in q.features:
            lines.append(f"    * {f.name}  (RICE {f.rice_score})")

    return "\n".join(lines)


def format_json(features: list[Feature], summary: dict, roadmap: list[Quarter]) -> str:
    result = {
        "features": [_feature_to_dict(f) for f in features],
        "summary": {
            k: ([_feature_to_dict(f) for f in v] if isinstance(v, list) else v)
            for k, v in summary.items()
        },
        "roadmap": [
            {
                "quarter": q.number,
                "capacity_used": q.used,
                "capacity_available": q.capacity - q.used,
                "features": [_feature_to_dict(f) for f in q.features],
            }
            for q in roadmap
        ],
    }
    return json.dumps(result, indent=2)


def format_csv(features: list[Feature]) -> str:
    import io
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["name", "reach", "impact", "confidence", "effort", "rice_score"])
    for f in features:
        writer.writerow([f.name, f.reach, f.impact, f.confidence, f.effort, f.rice_score])
    return buf.getvalue()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="RICE feature prioritization with portfolio analysis and roadmap."
    )
    parser.add_argument(
        "input",
        nargs="?",
        help='CSV file of features, or "sample" to generate a sample CSV.',
    )
    parser.add_argument(
        "--capacity",
        type=int,
        default=10,
        metavar="MONTHS",
        help="Team capacity per quarter in person-months (default: 10).",
    )
    parser.add_argument(
        "--output",
        choices=["text", "json", "csv"],
        default="text",
        help="Output format (default: text).",
    )
    args = parser.parse_args()

    if args.input == "sample":
        write_sample_csv()
        return

    features = load_csv(args.input) if args.input else _DEMO_FEATURES
    ranked = prioritize(features)
    summary = portfolio_summary(ranked)
    roadmap = build_roadmap(ranked, args.capacity)

    if args.output == "json":
        print(format_json(ranked, summary, roadmap))
    elif args.output == "csv":
        print(format_csv(ranked), end="")
    else:
        print(format_text(ranked, summary, roadmap))


if __name__ == "__main__":
    main()
