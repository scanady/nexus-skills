#!/usr/bin/env python3
"""
Data quality validator — checks CSV datasets for null rates, duplicate keys,
schema conformance, value ranges, and minimum row count thresholds.

Outputs a structured quality report with pass / warn / fail per check.
Exit code 0 = all checks pass. Exit code 1 = one or more fail-severity checks.

Usage:
    python data_quality_validator.py --input orders.csv --keys order_id
    python data_quality_validator.py --input customers.csv \\
        --keys customer_id \\
        --expected-columns customer_id email country \\
        --null-threshold 0.02 \\
        --min-rows 500
"""

import sys
import csv
import json
import logging
import argparse
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

NULL_SENTINELS = frozenset({"", "null", "NULL", "none", "None", "N/A", "n/a"})


@dataclass
class CheckResult:
    check: str
    status: str  # pass | warn | fail
    detail: str
    metric: Optional[Any] = None


@dataclass
class QualityReport:
    dataset: str
    run_at: str
    row_count: int
    checks: List[CheckResult] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return all(c.status != "fail" for c in self.checks)

    def to_dict(self) -> Dict:
        counts: Dict[str, int] = {"pass": 0, "warn": 0, "fail": 0}
        for c in self.checks:
            counts[c.status] += 1
        return {
            "dataset": self.dataset,
            "run_at": self.run_at,
            "row_count": self.row_count,
            "overall": "pass" if self.passed else "fail",
            **counts,
            "checks": [asdict(c) for c in self.checks],
        }


class DataQualityValidator:
    """Run configurable quality checks on a list-of-dicts dataset."""

    def __init__(
        self,
        rows: List[Dict[str, str]],
        dataset_name: str,
        key_columns: Optional[List[str]] = None,
        null_threshold: float = 0.05,
        min_rows: int = 1,
    ) -> None:
        self.rows = rows
        self.key_columns = key_columns or []
        self.null_threshold = null_threshold
        self.min_rows = min_rows
        self.report = QualityReport(
            dataset=dataset_name,
            run_at=datetime.now(timezone.utc).isoformat(),
            row_count=len(rows),
        )

    def _is_null(self, value: Optional[str]) -> bool:
        return value is None or str(value).strip() in NULL_SENTINELS

    # ── Checks ──────────────────────────────────────────────────────────────

    def check_row_count(self) -> CheckResult:
        n = len(self.rows)
        status = "pass" if n >= self.min_rows else "fail"
        return CheckResult(
            "row_count",
            status,
            f"{n} rows (minimum required: {self.min_rows})",
            n,
        )

    def check_null_rates(self) -> List[CheckResult]:
        if not self.rows:
            return []
        columns = list(self.rows[0].keys())
        n = len(self.rows)
        results: List[CheckResult] = []

        for col in columns:
            null_count = sum(1 for r in self.rows if self._is_null(r.get(col)))
            rate = null_count / n if n else 0.0

            if rate == 0:
                status, detail = "pass", "0 nulls"
            elif rate <= self.null_threshold:
                status = "warn"
                detail = f"{null_count}/{n} nulls ({rate:.1%}) — within threshold"
            else:
                status = "fail"
                detail = (
                    f"{null_count}/{n} nulls ({rate:.1%})"
                    f" — exceeds threshold {self.null_threshold:.1%}"
                )
            results.append(
                CheckResult(f"null_rate:{col}", status, detail, round(rate, 4))
            )
        return results

    def check_duplicates(self) -> CheckResult:
        if not self.key_columns:
            return CheckResult(
                "duplicate_keys",
                "warn",
                "No key columns specified — duplicate check skipped",
            )
        if not self.rows:
            return CheckResult("duplicate_keys", "pass", "Empty dataset")

        keys = [tuple(r.get(k) for k in self.key_columns) for r in self.rows]
        total = len(keys)
        unique = len(set(keys))
        dup_count = total - unique

        if dup_count == 0:
            return CheckResult(
                "duplicate_keys",
                "pass",
                f"0 duplicates on key column(s): {self.key_columns}",
                0,
            )
        return CheckResult(
            "duplicate_keys",
            "fail",
            f"{dup_count} duplicate row(s) on key {self.key_columns} ({unique} unique / {total} total)",
            dup_count,
        )

    def check_schema(self, expected_columns: List[str]) -> CheckResult:
        if not self.rows:
            return CheckResult("schema", "warn", "Empty dataset — schema check skipped")

        actual = set(self.rows[0].keys())
        expected = set(expected_columns)
        missing = expected - actual
        extra = actual - expected

        if not missing and not extra:
            return CheckResult("schema", "pass", "Schema matches expected contract")

        parts: List[str] = []
        if missing:
            parts.append(f"missing columns: {sorted(missing)}")
        if extra:
            parts.append(f"unexpected columns: {sorted(extra)}")

        # Missing required columns = fail; only extra = warn
        status = "fail" if missing else "warn"
        return CheckResult("schema", status, " | ".join(parts))

    def check_value_range(self, column: str, min_val: float, max_val: float) -> CheckResult:
        if not self.rows:
            return CheckResult(f"range:{column}", "warn", "Empty dataset")

        violations: List[str] = []
        for i, row in enumerate(self.rows):
            raw = row.get(column)
            if self._is_null(raw):
                continue
            try:
                val = float(raw)  # type: ignore[arg-type]
                if not (min_val <= val <= max_val):
                    violations.append(f"row {i + 1}: {val}")
            except (ValueError, TypeError):
                violations.append(f"row {i + 1}: non-numeric '{raw}'")

        if not violations:
            return CheckResult(
                f"range:{column}",
                "pass",
                f"All values in [{min_val}, {max_val}]",
                0,
            )
        summary = violations[:5]
        if len(violations) > 5:
            summary.append(f"...and {len(violations) - 5} more")
        return CheckResult(
            f"range:{column}",
            "fail",
            f"{len(violations)} out-of-range value(s): {summary}",
            len(violations),
        )

    # ── Run all ──────────────────────────────────────────────────────────────

    def run(self, expected_columns: Optional[List[str]] = None) -> QualityReport:
        self.report.checks.append(self.check_row_count())
        self.report.checks.extend(self.check_null_rates())
        self.report.checks.append(self.check_duplicates())
        if expected_columns:
            self.report.checks.append(self.check_schema(expected_columns))
        return self.report


def load_csv(path: Path) -> List[Dict[str, str]]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> None:
    parser = argparse.ArgumentParser(description="Data quality validator for CSV datasets")
    parser.add_argument("--input", "-i", required=True, help="CSV file to validate")
    parser.add_argument("--keys", "-k", nargs="*", help="Key column(s) for duplicate check")
    parser.add_argument(
        "--expected-columns", "-e", nargs="*",
        help="Expected column names for schema conformance check",
    )
    parser.add_argument(
        "--null-threshold", "-n", type=float, default=0.05,
        help="Max allowed null rate per column (default: 0.05 = 5%%)",
    )
    parser.add_argument(
        "--min-rows", "-m", type=int, default=1,
        help="Minimum expected row count (default: 1)",
    )
    parser.add_argument("--output", "-o", help="Write report JSON to file (stdout if omitted)")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    path = Path(args.input)
    if not path.exists():
        log.error("Input file not found: %s", path)
        sys.exit(1)

    rows = load_csv(path)
    log.info("Loaded %d rows from '%s'", len(rows), path.name)

    validator = DataQualityValidator(
        rows=rows,
        dataset_name=path.name,
        key_columns=args.keys,
        null_threshold=args.null_threshold,
        min_rows=args.min_rows,
    )
    report = validator.run(expected_columns=args.expected_columns)
    report_dict = report.to_dict()

    # Log summary to stderr
    for check in report.checks:
        level = {"pass": logging.INFO, "warn": logging.WARNING, "fail": logging.ERROR}.get(
            check.status, logging.INFO
        )
        log.log(level, "[%s] %s — %s", check.status.upper(), check.check, check.detail)

    log.info(
        "Overall: %s | %d pass / %d warn / %d fail",
        report_dict["overall"].upper(),
        report_dict["pass"],
        report_dict["warn"],
        report_dict["fail"],
    )

    report_json = json.dumps(report_dict, indent=2)
    if args.output:
        with open(args.output, "w") as f:
            f.write(report_json)
        log.info("Report written to %s", args.output)
    else:
        print(report_json)

    sys.exit(0 if report.passed else 1)


if __name__ == "__main__":
    main()
