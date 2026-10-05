"""Shared helpers for the customer-success scorers. Standard library only."""

import argparse
import json
import sys
from datetime import date
from typing import Any, Dict, List, Optional


def clamp(value: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, value))


def ratio(numerator: float, denominator: float) -> float:
    """numerator / denominator, or 0.0 when the denominator is zero."""
    return numerator / denominator if denominator else 0.0


def load_json(path: str) -> Any:
    """Read a JSON file. Exit with a one-line error on failure."""
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except OSError as err:
        sys.exit(f"error: cannot read {path}: {err.strerror}")
    except json.JSONDecodeError as err:
        sys.exit(f"error: invalid JSON in {path}: {err}")


def load_records(path: str, key: str) -> List[Dict[str, Any]]:
    """Read `path` and return the non-empty list stored under `key`."""
    records = load_json(path).get(key, [])
    if not records:
        sys.exit(f"error: no '{key}' records in {path}")
    return records


def parse_date(text: Optional[str]) -> Optional[date]:
    """Parse an ISO date (YYYY-MM-DD, extra time text ignored). None if absent or bad."""
    if not text:
        return None
    try:
        return date.fromisoformat(text[:10])
    except ValueError:
        return None


def base_parser(description: str, input_help: str) -> argparse.ArgumentParser:
    """Argument parser with the flags every scorer shares."""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("input_file", help=input_help)
    parser.add_argument("--format", choices=["text", "json"], default="text", dest="fmt")
    return parser


def money(value: float) -> str:
    return f"${value:,.0f}"
