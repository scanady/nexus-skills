#!/usr/bin/env python3
"""
Design UI System Advisor — BM25 search engine over UI/UX knowledge base.

Domain search:  search(query, domain, max_results)
Stack search:   search_stack(query, stack, max_results)
"""

import csv
import re
from collections import defaultdict
from math import log
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

DATA_DIR = Path(__file__).parent.parent / "data"
MAX_RESULTS = 3

# ---------------------------------------------------------------------------
# Domain configuration — maps domain name → CSV file + column specs
# ---------------------------------------------------------------------------

DOMAIN_CONFIG: dict[str, dict[str, Any]] = {
    "style": {
        "file": "styles.csv",
        "search_cols": ["style_name", "keywords", "best_for", "type"],
        "output_cols": [
            "style_name", "type", "keywords", "primary_colors",
            "effects", "best_for", "performance", "accessibility",
            "framework_compat", "complexity",
        ],
    },
    "prompt": {
        "file": "prompts.csv",
        "search_cols": ["style_name", "ai_prompt", "css_keywords"],
        "output_cols": ["style_name", "ai_prompt", "css_keywords", "checklist"],
    },
    "color": {
        "file": "colors.csv",
        "search_cols": ["product_type", "keywords", "notes"],
        "output_cols": [
            "product_type", "keywords", "primary", "secondary",
            "cta", "background", "text", "border", "notes",
        ],
    },
    "chart": {
        "file": "charts.csv",
        "search_cols": ["data_type", "keywords", "chart_type", "accessibility"],
        "output_cols": [
            "data_type", "keywords", "chart_type", "secondary_options",
            "color_guidance", "accessibility", "libraries", "interaction",
        ],
    },
    "landing": {
        "file": "landing.csv",
        "search_cols": ["pattern_name", "keywords", "conversion", "sections"],
        "output_cols": [
            "pattern_name", "keywords", "sections",
            "cta_placement", "color_strategy", "conversion",
        ],
    },
    "product": {
        "file": "products.csv",
        "search_cols": ["product_type", "keywords", "primary_style", "considerations"],
        "output_cols": [
            "product_type", "keywords", "primary_style", "secondary_styles",
            "landing_pattern", "dashboard_style", "color_focus",
        ],
    },
    "ux": {
        "file": "ux-guidelines.csv",
        "search_cols": ["category", "issue", "description", "platform"],
        "output_cols": [
            "category", "issue", "platform", "description",
            "do", "dont", "code_good", "code_bad", "severity",
        ],
    },
    "typography": {
        "file": "typography.csv",
        "search_cols": ["pairing_name", "category", "mood_keywords", "best_for", "heading_font", "body_font"],
        "output_cols": [
            "pairing_name", "category", "heading_font", "body_font",
            "mood_keywords", "best_for", "google_fonts_url", "css_import",
            "tailwind_config", "notes",
        ],
    },
    "icons": {
        "file": "icons.csv",
        "search_cols": ["category", "icon_name", "keywords", "best_for"],
        "output_cols": [
            "category", "icon_name", "keywords",
            "library", "import_code", "usage", "best_for", "style",
        ],
    },
    "react": {
        "file": "react-performance.csv",
        "search_cols": ["category", "issue", "keywords", "description"],
        "output_cols": [
            "category", "issue", "platform", "description",
            "do", "dont", "code_good", "code_bad", "severity",
        ],
    },
    "web": {
        "file": "web-interface.csv",
        "search_cols": ["category", "issue", "keywords", "description"],
        "output_cols": [
            "category", "issue", "platform", "description",
            "do", "dont", "code_good", "code_bad", "severity",
        ],
    },
}

# ---------------------------------------------------------------------------
# Stack configuration
# ---------------------------------------------------------------------------

_STACK_COLS = {
    "search_cols": ["category", "guideline", "description", "do", "dont"],
    "output_cols": [
        "category", "guideline", "description",
        "do", "dont", "code_good", "code_bad", "severity", "docs_url",
    ],
}

STACK_CONFIG: dict[str, dict[str, str]] = {
    "html-tailwind": {"file": "stacks/html-tailwind.csv"},
    "react":         {"file": "stacks/react.csv"},
    "nextjs":        {"file": "stacks/nextjs.csv"},
    "vue":           {"file": "stacks/vue.csv"},
    "nuxtjs":        {"file": "stacks/nuxtjs.csv"},
    "nuxt-ui":       {"file": "stacks/nuxt-ui.csv"},
    "svelte":        {"file": "stacks/svelte.csv"},
    "swiftui":       {"file": "stacks/swiftui.csv"},
    "react-native":  {"file": "stacks/react-native.csv"},
    "flutter":       {"file": "stacks/flutter.csv"},
    "shadcn":        {"file": "stacks/shadcn.csv"},
}

AVAILABLE_STACKS = list(STACK_CONFIG.keys())

# ---------------------------------------------------------------------------
# Domain auto-detection keyword map
# ---------------------------------------------------------------------------

_DOMAIN_SIGNALS: dict[str, list[str]] = {
    "color":      ["color", "palette", "hex", "#", "rgb"],
    "chart":      ["chart", "graph", "visualization", "trend", "bar", "pie", "scatter", "funnel"],
    "landing":    ["landing", "page", "cta", "conversion", "hero", "testimonial", "pricing"],
    "product":    ["saas", "ecommerce", "e-commerce", "fintech", "healthcare", "gaming", "dashboard"],
    "prompt":     ["prompt", "css", "checklist", "variable", "tailwind"],
    "style":      ["style", "ui", "minimalism", "glassmorphism", "neumorphism", "brutalism", "dark mode"],
    "ux":         ["ux", "accessibility", "wcag", "touch", "scroll", "animation", "keyboard", "mobile"],
    "typography": ["font", "typography", "heading", "serif", "sans"],
    "icons":      ["icon", "lucide", "heroicons", "svg", "pictogram"],
    "react":      ["react", "nextjs", "suspense", "memo", "waterfall", "bundle", "rerender"],
    "web":        ["aria", "focus", "semantic", "virtualize", "autocomplete", "preconnect"],
}


# ---------------------------------------------------------------------------
# BM25 ranking engine
# ---------------------------------------------------------------------------

class BM25:
    """Okapi BM25 ranking for in-memory document corpus."""

    def __init__(self, k1: float = 1.5, b: float = 0.75) -> None:
        self.k1 = k1
        self.b = b
        self._corpus: list[list[str]] = []
        self._doc_lengths: list[int] = []
        self._avgdl: float = 0.0
        self._idf: dict[str, float] = {}
        self._df: dict[str, int] = defaultdict(int)
        self._n: int = 0

    def _tokenize(self, text: str) -> list[str]:
        cleaned = re.sub(r"[^\w\s]", " ", str(text).lower())
        return [w for w in cleaned.split() if len(w) > 2]

    def fit(self, documents: list[str]) -> None:
        self._corpus = [self._tokenize(doc) for doc in documents]
        self._n = len(self._corpus)
        if self._n == 0:
            return
        self._doc_lengths = [len(doc) for doc in self._corpus]
        self._avgdl = sum(self._doc_lengths) / self._n
        for doc in self._corpus:
            for word in set(doc):
                self._df[word] += 1
        for word, df in self._df.items():
            self._idf[word] = log((self._n - df + 0.5) / (df + 0.5) + 1)

    def rank(self, query: str) -> list[tuple[int, float]]:
        tokens = self._tokenize(query)
        scores: list[tuple[int, float]] = []
        for idx, doc in enumerate(self._corpus):
            score = 0.0
            dl = self._doc_lengths[idx]
            tf_map: dict[str, int] = defaultdict(int)
            for w in doc:
                tf_map[w] += 1
            for token in tokens:
                if token not in self._idf:
                    continue
                tf = tf_map[token]
                idf = self._idf[token]
                denom = tf + self.k1 * (1 - self.b + self.b * dl / self._avgdl)
                score += idf * (tf * (self.k1 + 1)) / denom
            scores.append((idx, score))
        return sorted(scores, key=lambda x: x[1], reverse=True)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _load_csv(path: Path) -> list[dict[str, str]]:
    with open(path, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _run_bm25(path: Path, search_cols: list[str], output_cols: list[str],
              query: str, max_results: int) -> list[dict[str, str]]:
    if not path.exists():
        return []
    rows = _load_csv(path)
    docs = [" ".join(str(row.get(c, "")) for c in search_cols) for row in rows]
    engine = BM25()
    engine.fit(docs)
    ranked = engine.rank(query)
    results = []
    for idx, score in ranked[:max_results]:
        if score <= 0:
            continue
        row = rows[idx]
        results.append({c: row.get(c, "") for c in output_cols if c in row})
    return results


def _detect_domain(query: str) -> str:
    q = query.lower()
    scores = {d: sum(1 for kw in kws if kw in q) for d, kws in _DOMAIN_SIGNALS.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "style"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def search(query: str, domain: str | None = None, max_results: int = MAX_RESULTS) -> dict:
    """Search a design knowledge domain. Auto-detects domain when not specified."""
    if domain is None:
        domain = _detect_domain(query)
    config = DOMAIN_CONFIG.get(domain, DOMAIN_CONFIG["style"])
    path = DATA_DIR / config["file"]
    if not path.exists():
        return {"error": f"Data file not found: {path}", "domain": domain}
    results = _run_bm25(path, config["search_cols"], config["output_cols"], query, max_results)
    return {
        "domain": domain,
        "query": query,
        "file": config["file"],
        "count": len(results),
        "results": results,
    }


def search_stack(query: str, stack: str, max_results: int = MAX_RESULTS) -> dict:
    """Search stack-specific implementation guidelines."""
    if stack not in STACK_CONFIG:
        return {"error": f"Unknown stack '{stack}'. Available: {', '.join(AVAILABLE_STACKS)}"}
    path = DATA_DIR / STACK_CONFIG[stack]["file"]
    if not path.exists():
        return {"error": f"Stack file not found: {path}", "stack": stack}
    results = _run_bm25(path, _STACK_COLS["search_cols"], _STACK_COLS["output_cols"], query, max_results)
    return {
        "domain": "stack",
        "stack": stack,
        "query": query,
        "file": STACK_CONFIG[stack]["file"],
        "count": len(results),
        "results": results,
    }
