#!/usr/bin/env python3
"""
OKR Cascade Generator

Translates company strategy into aligned OKRs across company, product,
and team levels. Calculates alignment scores and renders a cascade dashboard.

Usage:
    python okr_cascade_generator.py [strategy] [json]

    strategy: growth | retention | revenue | innovation | operational
              Defaults to 'growth' when omitted or unrecognized.
    json:     Include full JSON export in output.

Examples:
    python okr_cascade_generator.py
    python okr_cascade_generator.py retention
    python okr_cascade_generator.py revenue json
"""

import json
import sys
from datetime import datetime
from typing import Optional

# ---------------------------------------------------------------------------
# Strategy templates
# ---------------------------------------------------------------------------

STRATEGY_TEMPLATES: dict[str, dict[str, list[str]]] = {
    "growth": {
        "objectives": [
            "Accelerate user acquisition and market expansion",
            "Achieve product-market fit in new segments",
            "Build sustainable growth engine",
        ],
        "key_results": [
            "Increase MAU from {current} to {target}",
            "Achieve {target}% MoM growth rate",
            "Expand to {target} new markets",
            "Reduce CAC by {target}%",
            "Improve activation rate to {target}%",
        ],
    },
    "retention": {
        "objectives": [
            "Create lasting customer value and loyalty",
            "Build best-in-class user experience",
            "Maximize customer lifetime value",
        ],
        "key_results": [
            "Improve retention from {current}% to {target}%",
            "Increase NPS from {current} to {target}",
            "Reduce churn to below {target}%",
            "Achieve {target}% product stickiness",
            "Increase LTV/CAC ratio to {target}",
        ],
    },
    "revenue": {
        "objectives": [
            "Drive sustainable revenue growth",
            "Optimize monetization strategy",
            "Expand revenue per customer",
        ],
        "key_results": [
            "Grow ARR from ${current}M to ${target}M",
            "Increase ARPU by {target}%",
            "Launch {target} new revenue streams",
            "Achieve {target}% gross margin",
            "Reduce revenue churn to {target}%",
        ],
    },
    "innovation": {
        "objectives": [
            "Pioneer next-generation product capabilities",
            "Establish market leadership through innovation",
            "Build competitive moat",
        ],
        "key_results": [
            "Launch {target} breakthrough features",
            "Achieve {target}% of revenue from new products",
            "File {target} patents",
            "Reduce time-to-market by {target}%",
            "Reach {target} innovation index score",
        ],
    },
    "operational": {
        "objectives": [
            "Build world-class product organization",
            "Achieve operational excellence",
            "Scale team efficiently",
        ],
        "key_results": [
            "Improve delivery velocity by {target}%",
            "Reduce cycle time to {target} days",
            "Achieve {target}% process automation",
            "Improve team NPS to {target}",
            "Reduce production incidents by {target}%",
        ],
    },
}

# Team domain relevance keywords — determines which teams pick up which objectives
TEAM_KEYWORDS: dict[str, list[str]] = {
    "Growth": ["acquisition", "growth", "activation", "viral", "onboarding", "expansion"],
    "Platform": [],  # Platform participates in all cascades (cross-cutting)
    "Mobile": ["mobile", "app", "ios", "android", "experience"],
    "Data": ["analytics", "metrics", "insights", "data", "reporting"],
}

# Company → product objective translation map (longest prefix match)
PRODUCT_TRANSLATIONS: dict[str, str] = {
    "Accelerate user acquisition": "Build viral product features for acquisition",
    "Achieve product-market fit": "Validate product hypotheses through rapid iteration",
    "Build sustainable growth": "Create product-led growth loops",
    "Create lasting customer value": "Design sticky, high-retention user experiences",
    "Build best-in-class user experience": "Elevate product UX to benchmark standard",
    "Maximize customer lifetime value": "Expand in-product monetization touchpoints",
    "Drive sustainable revenue growth": "Optimize product-driven revenue conversion",
    "Optimize monetization strategy": "Implement and test product pricing experiments",
    "Expand revenue per customer": "Surface upsell and expansion flows in-product",
    "Pioneer next-generation product capabilities": "Ship differentiated, category-defining features",
    "Establish market leadership through innovation": "Own defining product capabilities in category",
    "Build competitive moat": "Deepen platform switching costs through integrations",
    "Build world-class product organization": "Elevate product craft and delivery standards",
    "Achieve operational excellence": "Systematize product ops and quality gates",
    "Scale team efficiently": "Build scalable product processes and tooling",
}

# KR term substitutions when translating to product context
PRODUCT_KR_TERM_MAP: dict[str, str] = {
    "MAU": "product MAU",
    "growth rate": "feature adoption rate",
    "CAC": "product onboarding efficiency",
    "retention": "product retention",
    "NPS": "product NPS",
    "ARR": "product-driven revenue",
    "churn": "product churn",
    "activation": "in-product activation",
}

# Team focus labels used when translating objectives to team context
TEAM_FOCUS: dict[str, str] = {
    "Growth": "acquisition and activation",
    "Platform": "infrastructure and reliability",
    "Mobile": "mobile experience",
    "Data": "analytics and insights",
}


# ---------------------------------------------------------------------------
# OKR cascade generator
# ---------------------------------------------------------------------------

class OKRCascadeGenerator:
    """
    Cascades company strategy OKRs down through product and team levels.

    Behavior contract:
    - 5 strategy templates: growth, retention, revenue, innovation, operational
    - 3 objectives per level, 3 key results per objective
    - Product KR targets = 30% of corresponding company KR targets
    - Team KR targets = product target / number of active teams
    - Platform team participates in all cascades (cross-cutting concern)
    - Alignment scoring weights: vertical 40%, horizontal 20%, coverage 20%, balance 20%
    """

    PRODUCT_CONTRIBUTION_RATIO: float = 0.30
    MAX_OBJECTIVES: int = 3
    KRS_PER_OBJECTIVE: int = 3
    DEFAULT_TEAMS: list[str] = ["Growth", "Platform", "Mobile", "Data"]

    def __init__(self, teams: Optional[list[str]] = None) -> None:
        self.teams: list[str] = teams if teams is not None else list(self.DEFAULT_TEAMS)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate_full_cascade(
        self, strategy: str, metrics: dict[str, float]
    ) -> dict:
        """
        Build full OKR cascade: company -> product -> teams.

        Args:
            strategy: One of the five strategy types. Defaults to 'growth'
                      when unrecognized.
            metrics:  Dict with 'current' and 'target' keys at minimum.

        Returns:
            Dict with keys 'company', 'product', 'teams'.
        """
        resolved = self._resolve_strategy(strategy)
        company = self._build_company_okrs(resolved, metrics)
        product = self._cascade_to_product(company)
        teams = self._cascade_to_teams(product)
        return {"company": company, "product": product, "teams": teams}

    def render_dashboard(self, cascade: dict) -> str:
        """Render cascade as a plain-text dashboard."""
        quarter = cascade.get("company", {}).get("quarter", "N/A")
        lines: list[str] = [
            "=" * 60,
            "OKR CASCADE DASHBOARD",
            f"Quarter: {quarter}",
            "=" * 60,
        ]

        if company := cascade.get("company"):
            lines.append("\nCOMPANY OKRS\n")
            for obj in company["objectives"]:
                lines.append(f"  {obj['id']}: {obj['title']}")
                for kr in obj["key_results"]:
                    lines.append(f"    - {kr['id']}: {kr['title']}")

        if product := cascade.get("product"):
            lines.append("\nPRODUCT OKRS\n")
            for obj in product["objectives"]:
                lines.append(f"  {obj['id']}: {obj['title']}")
                lines.append(f"    Supports: {obj.get('parent_objective', 'N/A')}")
                for kr in obj["key_results"]:
                    lines.append(f"    - {kr['id']}: {kr['title']}")

        if teams := cascade.get("teams"):
            lines.append("\nTEAM OKRS\n")
            for team_block in teams:
                lines.append(f"\n  {team_block['team']} Team:")
                for obj in team_block["objectives"]:
                    lines.append(f"    {obj['id']}: {obj['title']}")
                    for kr in obj["key_results"]:
                        lines.append(f"      - {kr['id']}: {kr['title']}")

        lines += ["", "ALIGNMENT MATRIX", "-" * 40]
        lines += self._render_alignment_matrix(cascade)
        return "\n".join(lines)

    def calculate_alignment_score(self, cascade: dict) -> dict[str, float]:
        """
        Calculate alignment across four dimensions.

        Dimension weights (must sum to 1.0):
          vertical   40%  — objectives with explicit parent link
          horizontal 20%  — shared parent objectives across teams
          coverage   20%  — company KRs covered by product layer
          balance    20%  — team workload distribution evenness
        """
        vertical = self._score_vertical(cascade)
        horizontal = self._score_horizontal(cascade)
        coverage = self._score_coverage(cascade)
        balance = self._score_balance(cascade)
        overall = round(
            vertical * 0.40
            + horizontal * 0.20
            + coverage * 0.20
            + balance * 0.20,
            1,
        )
        return {
            "vertical_alignment": vertical,
            "horizontal_alignment": horizontal,
            "coverage": coverage,
            "balance": balance,
            "overall": overall,
        }

    # ------------------------------------------------------------------
    # OKR construction
    # ------------------------------------------------------------------

    def _build_company_okrs(self, strategy: str, metrics: dict[str, float]) -> dict:
        template = STRATEGY_TEMPLATES[strategy]
        objectives = []
        for i in range(self.MAX_OBJECTIVES):
            obj_id = f"CO-{i + 1}"
            key_results = [
                {
                    "id": f"{obj_id}-KR{j + 1}",
                    "title": self._fill_metrics(template["key_results"][j], metrics),
                    "current": metrics.get("current", 0),
                    "target": metrics.get("target", 100),
                    "unit": self._infer_unit(template["key_results"][j]),
                    "status": "not_started",
                }
                for j in range(self.KRS_PER_OBJECTIVE)
            ]
            objectives.append(
                {
                    "id": obj_id,
                    "title": template["objectives"][i],
                    "key_results": key_results,
                    "owner": "CEO",
                    "status": "draft",
                }
            )
        return {
            "level": "Company",
            "quarter": self._current_quarter(),
            "strategy": strategy,
            "objectives": objectives,
        }

    def _cascade_to_product(self, company: dict) -> dict:
        objectives = []
        for company_obj in company["objectives"]:
            obj_num = company_obj["id"].split("-")[1]
            obj_id = f"PO-{obj_num}"
            key_results = [
                {
                    "id": f"{obj_id}-KR{kr['id'].split('KR')[1]}",
                    "title": self._translate_kr_to_product(kr["title"]),
                    "contributes_to": kr["id"],
                    "current": kr["current"],
                    "target": round(kr["target"] * self.PRODUCT_CONTRIBUTION_RATIO, 1),
                    "unit": kr["unit"],
                    "status": "not_started",
                }
                for kr in company_obj["key_results"]
            ]
            objectives.append(
                {
                    "id": obj_id,
                    "title": self._translate_to_product(company_obj["title"]),
                    "parent_objective": company_obj["id"],
                    "key_results": key_results,
                    "owner": "Head of Product",
                    "status": "draft",
                }
            )
        return {
            "level": "Product",
            "quarter": company["quarter"],
            "parent": "Company",
            "objectives": objectives,
        }

    def _cascade_to_teams(self, product: dict) -> list[dict]:
        team_count = len(self.teams)
        result = []
        for team in self.teams:
            objectives = [
                self._build_team_objective(product_obj, team, team_count)
                for product_obj in product["objectives"]
                if self._objective_relevant_for_team(product_obj["title"], team)
            ]
            if objectives:
                result.append(
                    {
                        "level": "Team",
                        "team": team,
                        "quarter": product["quarter"],
                        "parent": "Product",
                        "objectives": objectives,
                    }
                )
        return result

    def _build_team_objective(
        self, product_obj: dict, team: str, team_count: int
    ) -> dict:
        obj_num = product_obj["id"].split("-")[1]
        prefix = team[:3].upper()
        obj_id = f"{prefix}-{obj_num}"
        key_results = [
            {
                "id": f"{obj_id}-KR{kr['id'].split('KR')[1]}",
                "title": f"[{team}] {kr['title']}",
                "contributes_to": kr["id"],
                "current": kr["current"],
                "target": round(kr["target"] / team_count, 1),
                "unit": kr["unit"],
                "status": "not_started",
            }
            for kr in product_obj["key_results"][:2]  # Each team owns 2 KRs
        ]
        return {
            "id": obj_id,
            "title": self._translate_to_team(product_obj["title"], team),
            "parent_objective": product_obj["id"],
            "key_results": key_results,
            "owner": f"{team} PM",
            "status": "draft",
        }

    # ------------------------------------------------------------------
    # Alignment scoring
    # ------------------------------------------------------------------

    def _score_vertical(self, cascade: dict) -> float:
        total, linked = 0, 0
        for obj in cascade.get("product", {}).get("objectives", []):
            total += 1
            if obj.get("parent_objective"):
                linked += 1
        for team_block in cascade.get("teams", []):
            for obj in team_block.get("objectives", []):
                total += 1
                if obj.get("parent_objective"):
                    linked += 1
        return round((linked / total) * 100, 1) if total else 0.0

    def _score_horizontal(self, cascade: dict) -> float:
        teams = cascade.get("teams", [])
        if len(teams) < 2:
            return 0.0
        shared_parents: set[str] = {
            obj["parent_objective"]
            for team_block in teams
            for obj in team_block.get("objectives", [])
            if obj.get("parent_objective")
        }
        return min(100.0, round(len(shared_parents) * 25, 1))

    def _score_coverage(self, cascade: dict) -> float:
        company_krs = sum(
            len(obj["key_results"])
            for obj in cascade.get("company", {}).get("objectives", [])
        )
        product_krs = sum(
            len(obj["key_results"])
            for obj in cascade.get("product", {}).get("objectives", [])
        )
        return round((product_krs / company_krs) * 100, 1) if company_krs else 0.0

    def _score_balance(self, cascade: dict) -> float:
        counts = [
            len(team_block.get("objectives", []))
            for team_block in cascade.get("teams", [])
        ]
        if not counts:
            return 0.0
        avg = sum(counts) / len(counts)
        variance = sum((x - avg) ** 2 for x in counts) / len(counts)
        return round(max(0.0, 100.0 - variance * 10), 1)

    # ------------------------------------------------------------------
    # Translation helpers
    # ------------------------------------------------------------------

    def _translate_to_product(self, company_title: str) -> str:
        """Map company objective to product objective using prefix match."""
        for fragment, product_title in PRODUCT_TRANSLATIONS.items():
            if fragment.lower() in company_title.lower():
                return product_title
        return f"Product: {company_title}"

    def _translate_kr_to_product(self, kr: str) -> str:
        """Substitute domain terms to shift KR into product context."""
        for term, replacement in PRODUCT_KR_TERM_MAP.items():
            if term in kr:
                return kr.replace(term, replacement, 1)
        return kr

    def _translate_to_team(self, objective: str, team: str) -> str:
        focus = TEAM_FOCUS.get(team, "delivery")
        return f"{objective} via {focus}"

    def _objective_relevant_for_team(self, objective: str, team: str) -> bool:
        """
        Return True when the objective falls within the team's domain.
        Platform team always returns True — infrastructure is cross-cutting.
        """
        keywords = TEAM_KEYWORDS.get(team, [])
        if not keywords:  # Empty keyword list signals universal relevance (Platform)
            return True
        lower = objective.lower()
        return any(kw in lower for kw in keywords)

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    @staticmethod
    def _resolve_strategy(strategy: str) -> str:
        """Return strategy if valid, else default to 'growth' with a warning."""
        if strategy in STRATEGY_TEMPLATES:
            return strategy
        print(
            f"Warning: unrecognized strategy '{strategy}', defaulting to 'growth'.",
            file=sys.stderr,
        )
        return "growth"

    @staticmethod
    def _fill_metrics(template: str, metrics: dict[str, float]) -> str:
        """Replace {key} placeholders with values from metrics dict."""
        result = template
        for key, value in metrics.items():
            result = result.replace(f"{{{key}}}", str(value))
        return result

    @staticmethod
    def _infer_unit(kr_template: str) -> str:
        """Infer measurement unit from KR template text."""
        lower = kr_template.lower()
        if "%" in kr_template:
            return "%"
        if "$" in kr_template:
            return "$"
        if "days" in lower:
            return "days"
        if any(word in lower for word in ("score", "index", "nps", "ratio")):
            return "points"
        return "count"

    @staticmethod
    def _current_quarter() -> str:
        now = datetime.now()
        quarter = (now.month - 1) // 3 + 1
        return f"Q{quarter} {now.year}"

    def _render_alignment_matrix(self, cascade: dict) -> list[str]:
        lines: list[str] = ["Company -> Product -> Teams"]
        company_objs = cascade.get("company", {}).get("objectives", [])
        product_objs = cascade.get("product", {}).get("objectives", [])
        team_blocks = cascade.get("teams", [])
        for c_obj in company_objs:
            lines.append(f"\n{c_obj['id']}")
            for p_obj in product_objs:
                if p_obj.get("parent_objective") == c_obj["id"]:
                    lines.append(f"  +-- {p_obj['id']}")
                    for team_block in team_blocks:
                        for t_obj in team_block.get("objectives", []):
                            if t_obj.get("parent_objective") == p_obj["id"]:
                                lines.append(
                                    f"      +-- {t_obj['id']} ({team_block['team']})"
                                )
        return lines


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    strategy = sys.argv[1] if len(sys.argv) > 1 else "growth"
    export_json = len(sys.argv) > 2 and sys.argv[2].lower() == "json"

    # Sample metrics — replace with real values when invoking programmatically
    metrics: dict[str, float] = {
        "current": 100_000,
        "target": 150_000,
        "current_revenue": 10,
        "target_revenue": 15,
        "current_nps": 40,
        "target_nps": 60,
    }

    generator = OKRCascadeGenerator()
    cascade = generator.generate_full_cascade(strategy, metrics)

    print(generator.render_dashboard(cascade))

    scores = generator.calculate_alignment_score(cascade)
    print("\nALIGNMENT SCORES")
    print("-" * 40)
    for metric, score in scores.items():
        label = metric.replace("_", " ").title()
        print(f"{label}: {score}%")

    if export_json:
        print("\nJSON OUTPUT:")
        print(json.dumps(cascade, indent=2))


if __name__ == "__main__":
    main()
