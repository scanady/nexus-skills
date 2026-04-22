#!/usr/bin/env python3
"""Customer interview analyzer.

Extracts pain points, delights, feature requests, jobs-to-be-done, sentiment,
key themes, notable quotes, metrics, and competitor mentions from a transcript.

Usage:
    customer_interview_analyzer.py <transcript.txt> [json]

    transcript.txt   Path to plain-text interview transcript.
    json             Optional second argument to output JSON instead of text.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Lexicons
# ---------------------------------------------------------------------------

PAIN_SIGNALS: frozenset[str] = frozenset([
    "frustrat", "annoy", "difficult", "hard", "confus", "slow",
    "problem", "issue", "struggle", "challeng", "pain", "waste",
    "manual", "repetitive", "tedious", "boring", "time-consuming",
    "complicated", "complex", "unclear", "wish", "need", "want",
])

DELIGHT_SIGNALS: frozenset[str] = frozenset([
    "love", "great", "awesome", "amazing", "perfect", "easy",
    "simple", "quick", "fast", "helpful", "useful", "valuable",
    "save", "efficient", "convenient", "intuitive", "clear",
])

REQUEST_SIGNALS: frozenset[str] = frozenset([
    "would be nice", "wish", "hope", "want", "need", "should",
    "could", "would love", "if only", "it would help", "suggest",
    "recommend", "idea", "what if", "have you considered",
])

STOP_WORDS: frozenset[str] = frozenset([
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to",
    "for", "of", "with", "by", "from", "as", "is", "was", "are",
    "were", "been", "be", "have", "has", "had", "do", "does", "did",
    "will", "would", "could", "should", "may", "might", "must",
    "can", "shall", "it", "i", "you", "we", "they", "them", "their",
])

HIGH_SEVERITY_WORDS: frozenset[str] = frozenset([
    "always", "every", "never", "critical", "blocking", "urgent", "major",
])

HIGH_PRIORITY_WORDS: frozenset[str] = frozenset([
    "immediately", "asap", "critical", "urgent", "top priority", "must have",
])

JTBD_PATTERNS: list[re.Pattern] = [
    re.compile(r"when i\s+(.+?),\s+i want to\s+(.+?)\s+so that\s+(.+)", re.IGNORECASE),
    re.compile(r"i need to\s+(.+?)\s+because\s+(.+)", re.IGNORECASE),
    re.compile(r"my goal is to\s+(.+)", re.IGNORECASE),
    re.compile(r"i'?m trying to\s+(.+)", re.IGNORECASE),
    re.compile(r"i use \w+ to\s+(.+)", re.IGNORECASE),
    re.compile(r"helps? me\s+(.+)", re.IGNORECASE),
]

# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------


@dataclass
class Signal:
    quote: str
    indicator: str
    rating: str  # "high" | "medium" | "positive"


@dataclass
class Job:
    description: str


@dataclass
class Sentiment:
    score: float
    label: str  # "positive" | "neutral" | "negative"
    positive_count: int
    negative_count: int


@dataclass
class InterviewReport:
    pain_points: list[Signal] = field(default_factory=list)
    delights: list[Signal] = field(default_factory=list)
    feature_requests: list[Signal] = field(default_factory=list)
    jobs_to_be_done: list[Job] = field(default_factory=list)
    sentiment: Optional[Sentiment] = None
    key_themes: list[str] = field(default_factory=list)
    key_quotes: list[str] = field(default_factory=list)
    metrics_mentioned: list[str] = field(default_factory=list)
    competitors_mentioned: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Analysis functions
# ---------------------------------------------------------------------------


def _split_sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]


def _rate(sentence: str, high_words: frozenset[str]) -> str:
    return "high" if any(w in sentence for w in high_words) else "medium"


def extract_pain_points(sentences: list[str]) -> list[Signal]:
    results: list[Signal] = []
    for sentence in sentences:
        lower = sentence.lower()
        for indicator in PAIN_SIGNALS:
            if indicator in lower:
                results.append(Signal(
                    quote=sentence,
                    indicator=indicator,
                    rating=_rate(lower, HIGH_SEVERITY_WORDS),
                ))
                break
        if len(results) == 10:
            break
    return results


def extract_delights(sentences: list[str]) -> list[Signal]:
    results: list[Signal] = []
    for sentence in sentences:
        lower = sentence.lower()
        for indicator in DELIGHT_SIGNALS:
            if indicator in lower:
                results.append(Signal(quote=sentence, indicator=indicator, rating="positive"))
                break
        if len(results) == 10:
            break
    return results


def extract_requests(sentences: list[str]) -> list[Signal]:
    results: list[Signal] = []
    for sentence in sentences:
        lower = sentence.lower()
        for indicator in REQUEST_SIGNALS:
            if indicator in lower:
                results.append(Signal(
                    quote=sentence,
                    indicator=indicator,
                    rating=_rate(lower, HIGH_PRIORITY_WORDS),
                ))
                break
        if len(results) == 10:
            break
    return results


def extract_jobs(text: str) -> list[Job]:
    jobs: list[Job] = []
    for pattern in JTBD_PATTERNS:
        for match in pattern.findall(text):
            description = " → ".join(match) if isinstance(match, tuple) else match
            jobs.append(Job(description=description))
        if len(jobs) >= 5:
            break
    return jobs[:5]


def compute_sentiment(text: str) -> Sentiment:
    lower = text.lower()
    pos = sum(1 for word in DELIGHT_SIGNALS if word in lower)
    neg = sum(1 for word in PAIN_SIGNALS if word in lower)
    total = pos + neg
    score = round((pos - neg) / total, 2) if total else 0.0
    label = "positive" if score > 0.3 else ("negative" if score < -0.3 else "neutral")
    return Sentiment(score=score, label=label, positive_count=pos, negative_count=neg)


def extract_themes(text: str) -> list[str]:
    words = re.findall(r"\b[a-z]{4,}\b", text.lower())
    meaningful = [w for w in words if w not in STOP_WORDS]
    return [word for word, count in Counter(meaningful).most_common(10) if count >= 3]


def _sentence_signal_score(sentence: str) -> int:
    lower = sentence.lower()
    return (
        sum(1 for w in PAIN_SIGNALS if w in lower)
        + sum(1 for w in DELIGHT_SIGNALS if w in lower)
        + sum(1 for w in REQUEST_SIGNALS if w in lower)
    )


def extract_key_quotes(sentences: list[str]) -> list[str]:
    candidates = [s for s in sentences if 20 <= len(s) <= 200]
    return sorted(candidates, key=_sentence_signal_score, reverse=True)[:5]


def extract_metrics(text: str) -> list[str]:
    patterns = [
        r"\d+%",
        r"\$[\d,]+",
        r"\d+x\b",
        r"\d+ (?:hours?|days?|weeks?|months?|users?|customers?)",
    ]
    found: list[str] = []
    for pat in patterns:
        found.extend(re.findall(pat, text, re.IGNORECASE))
    # Deduplicate while preserving order, cap at 10
    return list(dict.fromkeys(found))[:10]


def extract_competitors(text: str) -> list[str]:
    patterns = [
        r"(?:compared? to|instead of|versus|vs\.?|using|competitor|alternative)\s+([A-Z][a-zA-Z]+)",
    ]
    competitors: list[str] = []
    for pat in patterns:
        competitors.extend(re.findall(pat, text))
    return list(dict.fromkeys(competitors))[:10]


def analyze(text: str) -> InterviewReport:
    sentences = _split_sentences(text)
    return InterviewReport(
        pain_points=extract_pain_points(sentences),
        delights=extract_delights(sentences),
        feature_requests=extract_requests(sentences),
        jobs_to_be_done=extract_jobs(text),
        sentiment=compute_sentiment(text),
        key_themes=extract_themes(text),
        key_quotes=extract_key_quotes(sentences),
        metrics_mentioned=extract_metrics(text),
        competitors_mentioned=extract_competitors(text),
    )


# ---------------------------------------------------------------------------
# Output formatters
# ---------------------------------------------------------------------------

_SEP = "-" * 56


def format_text(report: InterviewReport) -> str:
    lines: list[str] = [_SEP, "CUSTOMER INTERVIEW ANALYSIS", _SEP]

    if report.sentiment:
        s = report.sentiment
        lines += [
            "",
            f"SENTIMENT: {s.label.upper()}  (score: {s.score})",
            f"  positive signals: {s.positive_count}  |  negative signals: {s.negative_count}",
        ]

    def section(title: str, items: list) -> None:
        lines += ["", _SEP, title, _SEP]
        if not items:
            lines.append("  (none detected)")
            return
        for item in items:
            if isinstance(item, Signal):
                lines.append(f"  [{item.rating.upper()}] {item.quote}")
            elif isinstance(item, Job):
                lines.append(f"  {item.description}")
            else:
                lines.append(f"  {item}")

    section("PAIN POINTS", report.pain_points)
    section("DELIGHTS", report.delights)
    section("FEATURE REQUESTS", report.feature_requests)
    section("JOBS TO BE DONE", report.jobs_to_be_done)
    section("KEY THEMES", report.key_themes)
    section("KEY QUOTES", report.key_quotes)
    section("METRICS MENTIONED", report.metrics_mentioned)
    section("COMPETITORS MENTIONED", report.competitors_mentioned)

    return "\n".join(lines)


def format_json(report: InterviewReport) -> str:
    def signal_dict(s: Signal) -> dict:
        return {"quote": s.quote, "indicator": s.indicator, "rating": s.rating}

    result = {
        "sentiment": {
            "score": report.sentiment.score,
            "label": report.sentiment.label,
            "positive_count": report.sentiment.positive_count,
            "negative_count": report.sentiment.negative_count,
        } if report.sentiment else None,
        "pain_points": [signal_dict(s) for s in report.pain_points],
        "delights": [signal_dict(s) for s in report.delights],
        "feature_requests": [signal_dict(s) for s in report.feature_requests],
        "jobs_to_be_done": [{"description": j.description} for j in report.jobs_to_be_done],
        "key_themes": report.key_themes,
        "key_quotes": report.key_quotes,
        "metrics_mentioned": report.metrics_mentioned,
        "competitors_mentioned": report.competitors_mentioned,
    }
    return json.dumps(result, indent=2)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: customer_interview_analyzer.py <transcript.txt> [json]",
            file=sys.stderr,
        )
        sys.exit(1)

    transcript_path = sys.argv[1]
    output_format = sys.argv[2].lower() if len(sys.argv) > 2 else "text"

    text = Path(transcript_path).read_text(encoding="utf-8")
    report = analyze(text)

    if output_format == "json":
        print(format_json(report))
    else:
        print(format_text(report))


if __name__ == "__main__":
    main()
