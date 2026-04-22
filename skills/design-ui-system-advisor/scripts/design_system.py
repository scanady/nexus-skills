#!/usr/bin/env python3
"""
Design System Generator — aggregates multi-domain search results and applies
reasoning rules to produce a complete, opinionated design system recommendation.

Entry point:
    generate_design_system(query, project_name, output_format) -> str
"""

import csv
import json
from pathlib import Path
from typing import Any

from core import DATA_DIR, search

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

REASONING_FILE = "ui-reasoning.csv"

_SEARCH_CONFIG = {
    "product":    {"max_results": 1},
    "style":      {"max_results": 3},
    "color":      {"max_results": 2},
    "landing":    {"max_results": 2},
    "typography": {"max_results": 2},
}

_BOX_WIDTH = 90

_DELIVERY_CHECKLIST = [
    "[ ] No emoji icons — use SVG (Heroicons / Lucide)",
    "[ ] cursor-pointer on all interactive elements",
    "[ ] Hover transitions 150–300ms",
    "[ ] Text contrast ≥ 4.5:1 (light mode)",
    "[ ] Visible focus states for keyboard navigation",
    "[ ] prefers-reduced-motion respected",
    "[ ] Responsive: 375px / 768px / 1024px / 1440px",
]


# ---------------------------------------------------------------------------
# Reasoning loader
# ---------------------------------------------------------------------------

def _load_reasoning() -> list[dict[str, str]]:
    path = DATA_DIR / REASONING_FILE
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


# ---------------------------------------------------------------------------
# Rule matching
# ---------------------------------------------------------------------------

def _find_rule(rules: list[dict], category: str) -> dict[str, str]:
    """Return the best matching reasoning rule for a product category."""
    cat = category.lower()

    for rule in rules:
        if rule.get("ui_category", "").lower() == cat:
            return rule

    for rule in rules:
        stored = rule.get("ui_category", "").lower()
        if stored in cat or cat in stored:
            return rule

    keywords = cat.replace("/", " ").replace("-", " ").split()
    for rule in rules:
        stored = rule.get("ui_category", "").lower()
        if any(kw in stored for kw in keywords):
            return rule

    return {}


_DEFAULT_REASONING = {
    "pattern": "Hero + Features + CTA",
    "style_priority": ["Minimalism", "Flat Design"],
    "color_mood": "Professional",
    "typography_mood": "Clean",
    "effects": "Subtle hover transitions",
    "anti_patterns": "",
    "decision_rules": {},
    "severity": "MEDIUM",
}


def _apply_rule(rule: dict[str, str]) -> dict[str, Any]:
    if not rule:
        return _DEFAULT_REASONING.copy()
    try:
        decision_rules = json.loads(rule.get("decision_rules", "{}"))
    except (json.JSONDecodeError, TypeError):
        decision_rules = {}
    return {
        "pattern":        rule.get("pattern", ""),
        "style_priority": [s.strip() for s in rule.get("style_priority", "").split("+")],
        "color_mood":     rule.get("color_mood", ""),
        "typography_mood": rule.get("typography_mood", ""),
        "effects":        rule.get("effects", ""),
        "anti_patterns":  rule.get("anti_patterns", ""),
        "decision_rules": decision_rules,
        "severity":       rule.get("severity", "MEDIUM"),
    }


# ---------------------------------------------------------------------------
# Result selection helpers
# ---------------------------------------------------------------------------

def _get_results(search_result: dict) -> list[dict]:
    return search_result.get("results", [])


def _best_match(candidates: list[dict], priorities: list[str], name_col: str = "style_name") -> dict:
    if not candidates:
        return {}
    if not priorities:
        return candidates[0]

    for priority in priorities:
        p = priority.lower().strip()
        for c in candidates:
            name = c.get(name_col, "").lower()
            if p in name or name in p:
                return c

    scored = []
    for c in candidates:
        c_str = str(c).lower()
        score = sum(
            10 if kw.lower() in c.get(name_col, "").lower()
            else 3 if kw.lower() in c.get("keywords", "").lower()
            else 1 if kw.lower() in c_str
            else 0
            for kw in priorities
        )
        scored.append((score, c))
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[0][1] if scored and scored[0][0] > 0 else candidates[0]


# ---------------------------------------------------------------------------
# Core generator
# ---------------------------------------------------------------------------

def _build_design_system(query: str, project_name: str | None) -> dict[str, Any]:
    rules = _load_reasoning()

    # 1. Identify product category
    product_result = search(query, "product", 1)
    product_rows = _get_results(product_result)
    category = product_rows[0].get("product_type", "General") if product_rows else "General"

    # 2. Resolve reasoning rules for category
    reasoning = _apply_rule(_find_rule(rules, category))
    style_priority = reasoning["style_priority"]

    # 3. Multi-domain search
    style_query = f"{query} {' '.join(style_priority[:2])}" if style_priority else query
    domain_results = {
        "product":    product_result,
        "style":      search(style_query, "style",      _SEARCH_CONFIG["style"]["max_results"]),
        "color":      search(query,       "color",      _SEARCH_CONFIG["color"]["max_results"]),
        "landing":    search(query,       "landing",    _SEARCH_CONFIG["landing"]["max_results"]),
        "typography": search(query,       "typography", _SEARCH_CONFIG["typography"]["max_results"]),
    }

    # 4. Select best match per domain
    style_rows      = _get_results(domain_results["style"])
    color_rows      = _get_results(domain_results["color"])
    typography_rows = _get_results(domain_results["typography"])
    landing_rows    = _get_results(domain_results["landing"])

    best_style      = _best_match(style_rows, style_priority)
    best_color      = color_rows[0]      if color_rows      else {}
    best_typography = typography_rows[0] if typography_rows else {}
    best_landing    = landing_rows[0]    if landing_rows    else {}

    # 5. Merge effects from reasoning and style record
    effects = best_style.get("effects") or reasoning["effects"]

    return {
        "project_name": (project_name or query).upper(),
        "category":     category,
        "pattern": {
            "name":           best_landing.get("pattern_name", reasoning["pattern"]),
            "sections":       best_landing.get("sections", "Hero > Features > CTA"),
            "cta_placement":  best_landing.get("cta_placement", "Above fold"),
            "color_strategy": best_landing.get("color_strategy", ""),
            "conversion":     best_landing.get("conversion", ""),
        },
        "style": {
            "name":          best_style.get("style_name", "Minimalism"),
            "type":          best_style.get("type", "General"),
            "effects":       effects,
            "keywords":      best_style.get("keywords", ""),
            "best_for":      best_style.get("best_for", ""),
            "performance":   best_style.get("performance", ""),
            "accessibility": best_style.get("accessibility", ""),
        },
        "colors": {
            "primary":    best_color.get("primary",    "#2563EB"),
            "secondary":  best_color.get("secondary",  "#3B82F6"),
            "cta":        best_color.get("cta",        "#F97316"),
            "background": best_color.get("background", "#F8FAFC"),
            "text":       best_color.get("text",       "#1E293B"),
            "notes":      best_color.get("notes",      ""),
        },
        "typography": {
            "heading":          best_typography.get("heading_font",    "Inter"),
            "body":             best_typography.get("body_font",       "Inter"),
            "mood":             best_typography.get("mood_keywords",   reasoning["typography_mood"]),
            "best_for":         best_typography.get("best_for",        ""),
            "google_fonts_url": best_typography.get("google_fonts_url", ""),
            "css_import":       best_typography.get("css_import",      ""),
        },
        "key_effects":    effects,
        "anti_patterns":  reasoning["anti_patterns"],
        "decision_rules": reasoning["decision_rules"],
        "severity":       reasoning["severity"],
    }


# ---------------------------------------------------------------------------
# Output formatters
# ---------------------------------------------------------------------------

def _wrap(text: str, prefix: str, width: int) -> list[str]:
    if not text:
        return []
    words = text.split()
    lines: list[str] = []
    line = prefix
    for word in words:
        candidate = (line + " " + word) if line != prefix else (prefix + word)
        if len(candidate) <= width - 2:
            line = candidate
        else:
            if line != prefix:
                lines.append(line)
            line = prefix + word
    if line != prefix:
        lines.append(line)
    return lines


def _format_ascii(ds: dict[str, Any]) -> str:
    w = _BOX_WIDTH - 1
    pattern    = ds["pattern"]
    style      = ds["style"]
    colors     = ds["colors"]
    typography = ds["typography"]
    sections   = [s.strip() for s in pattern["sections"].split(">") if s.strip()]

    rows: list[str] = []
    add = rows.append

    add("+" + "-" * w + "+")
    add(f"|  TARGET: {ds['project_name']} — RECOMMENDED DESIGN SYSTEM".ljust(_BOX_WIDTH) + "|")
    add("+" + "-" * w + "+")
    add("|" + " " * _BOX_WIDTH + "|")

    add(f"|  PATTERN: {pattern['name']}".ljust(_BOX_WIDTH) + "|")
    if pattern["conversion"]:
        add(f"|     Conversion: {pattern['conversion']}".ljust(_BOX_WIDTH) + "|")
    if pattern["cta_placement"]:
        add(f"|     CTA: {pattern['cta_placement']}".ljust(_BOX_WIDTH) + "|")
    add("|     Sections:".ljust(_BOX_WIDTH) + "|")
    for i, sec in enumerate(sections, 1):
        add(f"|       {i}. {sec}".ljust(_BOX_WIDTH) + "|")
    add("|" + " " * _BOX_WIDTH + "|")

    add(f"|  STYLE: {style['name']}".ljust(_BOX_WIDTH) + "|")
    for line in _wrap(f"Keywords: {style['keywords']}", "|     ", _BOX_WIDTH):
        add(line.ljust(_BOX_WIDTH) + "|")
    for line in _wrap(f"Best For: {style['best_for']}", "|     ", _BOX_WIDTH):
        add(line.ljust(_BOX_WIDTH) + "|")
    if style["performance"] or style["accessibility"]:
        add(f"|     Performance: {style['performance']} | Accessibility: {style['accessibility']}".ljust(_BOX_WIDTH) + "|")
    add("|" + " " * _BOX_WIDTH + "|")

    add("|  COLORS:".ljust(_BOX_WIDTH) + "|")
    for label, key in [("Primary", "primary"), ("Secondary", "secondary"), ("CTA", "cta"),
                       ("Background", "background"), ("Text", "text")]:
        add(f"|     {label:<12}{colors[key]}".ljust(_BOX_WIDTH) + "|")
    for line in _wrap(f"Notes: {colors['notes']}", "|     ", _BOX_WIDTH):
        add(line.ljust(_BOX_WIDTH) + "|")
    add("|" + " " * _BOX_WIDTH + "|")

    add(f"|  TYPOGRAPHY: {typography['heading']} / {typography['body']}".ljust(_BOX_WIDTH) + "|")
    for line in _wrap(f"Mood: {typography['mood']}", "|     ", _BOX_WIDTH):
        add(line.ljust(_BOX_WIDTH) + "|")
    for line in _wrap(f"Best For: {typography['best_for']}", "|     ", _BOX_WIDTH):
        add(line.ljust(_BOX_WIDTH) + "|")
    if typography["google_fonts_url"]:
        add(f"|     Google Fonts: {typography['google_fonts_url']}".ljust(_BOX_WIDTH) + "|")
    if typography["css_import"]:
        add(f"|     CSS Import: {typography['css_import'][:70]}...".ljust(_BOX_WIDTH) + "|")
    add("|" + " " * _BOX_WIDTH + "|")

    if ds["key_effects"]:
        add("|  KEY EFFECTS:".ljust(_BOX_WIDTH) + "|")
        for line in _wrap(ds["key_effects"], "|     ", _BOX_WIDTH):
            add(line.ljust(_BOX_WIDTH) + "|")
        add("|" + " " * _BOX_WIDTH + "|")

    if ds["anti_patterns"]:
        add("|  AVOID (Anti-patterns):".ljust(_BOX_WIDTH) + "|")
        for line in _wrap(ds["anti_patterns"], "|     ", _BOX_WIDTH):
            add(line.ljust(_BOX_WIDTH) + "|")
        add("|" + " " * _BOX_WIDTH + "|")

    add("|  PRE-DELIVERY CHECKLIST:".ljust(_BOX_WIDTH) + "|")
    for item in _DELIVERY_CHECKLIST:
        add(f"|     {item}".ljust(_BOX_WIDTH) + "|")
    add("|" + " " * _BOX_WIDTH + "|")
    add("+" + "-" * w + "+")

    return "\n".join(rows)


def _format_markdown(ds: dict[str, Any]) -> str:
    pattern    = ds["pattern"]
    style      = ds["style"]
    colors     = ds["colors"]
    typography = ds["typography"]

    rows: list[str] = [f"## Design System: {ds['project_name']}", ""]

    rows += ["### Pattern",
             f"- **Name:** {pattern['name']}"]
    if pattern["conversion"]:
        rows.append(f"- **Conversion Focus:** {pattern['conversion']}")
    if pattern["cta_placement"]:
        rows.append(f"- **CTA Placement:** {pattern['cta_placement']}")
    if pattern["color_strategy"]:
        rows.append(f"- **Color Strategy:** {pattern['color_strategy']}")
    rows += [f"- **Sections:** {pattern['sections']}", ""]

    rows += ["### Style",
             f"- **Name:** {style['name']}"]
    if style["keywords"]:
        rows.append(f"- **Keywords:** {style['keywords']}")
    if style["best_for"]:
        rows.append(f"- **Best For:** {style['best_for']}")
    if style["performance"] or style["accessibility"]:
        rows.append(f"- **Performance:** {style['performance']} | **Accessibility:** {style['accessibility']}")
    rows.append("")

    rows += ["### Colors",
             "| Role | Hex |",
             "|------|-----|",
             f"| Primary | {colors['primary']} |",
             f"| Secondary | {colors['secondary']} |",
             f"| CTA | {colors['cta']} |",
             f"| Background | {colors['background']} |",
             f"| Text | {colors['text']} |"]
    if colors["notes"]:
        rows.append(f"\n*{colors['notes']}*")
    rows.append("")

    rows += ["### Typography",
             f"- **Heading:** {typography['heading']}",
             f"- **Body:** {typography['body']}"]
    if typography["mood"]:
        rows.append(f"- **Mood:** {typography['mood']}")
    if typography["best_for"]:
        rows.append(f"- **Best For:** {typography['best_for']}")
    if typography["google_fonts_url"]:
        rows.append(f"- **Google Fonts:** {typography['google_fonts_url']}")
    if typography["css_import"]:
        rows += ["- **CSS Import:**", "```css", typography["css_import"], "```"]
    rows.append("")

    if ds["key_effects"]:
        rows += ["### Key Effects", ds["key_effects"], ""]

    if ds["anti_patterns"]:
        avoid = "- " + ds["anti_patterns"].replace(" + ", "\n- ")
        rows += ["### Avoid (Anti-patterns)", avoid, ""]

    rows += ["### Pre-Delivery Checklist"] + _DELIVERY_CHECKLIST + [""]

    return "\n".join(rows)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def generate_design_system(query: str, project_name: str | None = None,
                            output_format: str = "ascii") -> str:
    """
    Generate a complete design system recommendation.

    Args:
        query:         Product description (e.g. "SaaS analytics dashboard")
        project_name:  Optional project name shown in output header
        output_format: "ascii" (default) or "markdown"

    Returns:
        Formatted design system string ready for agent consumption
    """
    ds = _build_design_system(query, project_name)
    return _format_markdown(ds) if output_format == "markdown" else _format_ascii(ds)


# ---------------------------------------------------------------------------
# CLI support (standalone use)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate Design System")
    parser.add_argument("query", help="Product description query")
    parser.add_argument("--project-name", "-p", default=None, help="Project name for header")
    parser.add_argument("--format", "-f", choices=["ascii", "markdown"], default="ascii")
    args = parser.parse_args()

    print(generate_design_system(args.query, args.project_name, args.format))
