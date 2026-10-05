"""Shared helpers for the campaign attribution scripts. Not run directly."""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"


class InputError(Exception):
    """Bad input data. The message names the field and the fix."""


def divide(numerator, denominator):
    """Return numerator / denominator, or None when the ratio is undefined."""
    return numerator / denominator if denominator else None


def load_json(path):
    try:
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError:
        raise InputError(f"file not found: {path}")
    except json.JSONDecodeError as err:
        raise InputError(f"invalid JSON in {path}: {err}")


def number(value, where, minimum=0.0):
    """Return value as a float, or raise when it is not a number >= minimum."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise InputError(f"{where}: expected a number, got {value!r}")
    if value < minimum:
        raise InputError(f"{where}: must be >= {minimum}, got {value}")
    return float(value)


def parse_time(text, where):
    """Parse an ISO 8601 date or datetime into a naive UTC datetime."""
    if not isinstance(text, str):
        raise InputError(f"{where}: expected an ISO timestamp string, got {text!r}")
    try:
        moment = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        raise InputError(f"{where}: cannot parse timestamp {text!r}")
    if moment.tzinfo is not None:
        moment = moment.astimezone(timezone.utc).replace(tzinfo=None)
    return moment


def fmt(value, spec=",.2f", prefix="", suffix=""):
    """Format a number, or n/a when it is undefined."""
    return "n/a" if value is None else f"{prefix}{value:{spec}}{suffix}"


def table(headers, rows, widths):
    """Render a left-aligned first column and right-aligned other columns."""
    def line(cells):
        first, *rest = [str(c) for c in cells]
        return f"  {first:<{widths[0]}}" + "".join(
            f" {c:>{w}}" for c, w in zip(rest, widths[1:])
        )

    rule = "  " + " ".join("-" * w for w in widths)
    return "\n".join([line(headers), rule, *(line(r) for r in rows)])


def main_guard(run):
    """Run a script entry point. Print input errors to stderr and exit 2."""
    try:
        run()
    except InputError as err:
        print(f"error: {err}", file=sys.stderr)
        sys.exit(2)
