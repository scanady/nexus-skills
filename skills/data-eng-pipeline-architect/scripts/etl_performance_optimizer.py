#!/usr/bin/env python3
"""
ETL performance optimizer — profiles pipeline stage timings from a run report,
identifies bottlenecks, and emits ranked optimization recommendations.

Accepts a JSON run report produced by pipeline_orchestrator.py.
Recommendations are ranked by severity (critical → warn → info) and
target the specific stage type using keyword-based heuristics.

Usage:
    # First produce a run report:
    python pipeline_orchestrator.py --demo --output run_report.json

    # Then analyze it:
    python etl_performance_optimizer.py --report run_report.json
    python etl_performance_optimizer.py --report run_report.json --slow-threshold 30
"""

import sys
import json
import logging
import argparse
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

# Default thresholds (seconds). Override via CLI flags.
DEFAULT_SLOW_S = 60.0
DEFAULT_CRITICAL_S = 300.0


@dataclass
class Recommendation:
    stage: str
    severity: str  # info | warn | critical
    finding: str
    suggestion: str


@dataclass
class OptimizationReport:
    source: str
    stages_analyzed: int
    total_duration_s: float
    bottleneck_stage: Optional[str]
    recommendations: List[Recommendation]

    def to_dict(self) -> Dict:
        by_severity: Dict[str, int] = {"critical": 0, "warn": 0, "info": 0}
        for r in self.recommendations:
            by_severity[r.severity] = by_severity.get(r.severity, 0) + 1
        return {
            "source": self.source,
            "stages_analyzed": self.stages_analyzed,
            "total_duration_s": round(self.total_duration_s, 3),
            "bottleneck_stage": self.bottleneck_stage,
            "recommendation_counts": by_severity,
            "recommendations": [asdict(r) for r in self.recommendations],
        }


class ETLPerformanceOptimizer:
    """
    Analyze stage timings from a pipeline run report and emit tuning recommendations.

    Heuristics:
    - Stages > slow_threshold_s are flagged with severity proportional to duration.
    - Stages consuming > 50% of total pipeline time are flagged as dominant bottlenecks.
    - Stage name keywords map to domain-specific optimization hints.
    - Failed stages always emit a critical recommendation to address root cause first.
    """

    # Keyword → optimization hint mapping (checked against lowercase stage name)
    KEYWORD_HINTS: Dict[str, str] = {
        "extract": (
            "Source read bottleneck. "
            "Check: parallelise extraction by partition/date range, increase fetch batch size, "
            "enable server-side pushdown predicates, use connection pooling."
        ),
        "ingest": (
            "Source read bottleneck. "
            "Check: parallelise extraction, increase API page size, use bulk endpoint if available."
        ),
        "transform": (
            "CPU/memory bound. "
            "Check: Spark partition count (aim for 100-200MB/partition), broadcast small lookup tables, "
            "replace Python UDFs with native Spark SQL functions, push filters before joins."
        ),
        "join": (
            "Shuffle / skew risk. "
            "Check: broadcast join hint for tables < 1GB, partition both sides on join key, "
            "inspect data skew on join key, use SKEW JOIN hint in Databricks if skewed."
        ),
        "merge": (
            "MERGE / SCD heavy. "
            "Check: cluster target table on merge key (CLUSTER BY / Z-ORDER), "
            "add `WHERE target.updated_at < source.updated_at` guard, "
            "limit merge to changed rows only with a pre-filter CTE."
        ),
        "load": (
            "Write bottleneck. "
            "Check: use warehouse bulk COPY (COPY INTO / LOAD DATA), "
            "avoid row-by-row INSERT in loops, stage via S3/GCS then COPY, "
            "increase warehouse size temporarily for load window."
        ),
        "write": (
            "Write bottleneck. "
            "Check: bulk insert vs row-by-row, warehouse COPY command, "
            "reduce output file count with coalesce/repartition before write."
        ),
        "aggregate": (
            "Grouping cost. "
            "Check: push aggregation into source query, pre-aggregate at Silver layer, "
            "use approximate aggregates (approx_count_distinct) where exact count not needed."
        ),
        "dedupe": (
            "Sort + compare cost. "
            "Check: window function scoped to partition key vs full-table sort, "
            "add source filter to reduce input volume before dedup step."
        ),
        "validate": (
            "Full-scan quality check. "
            "Check: push validation into dbt tests (schema.yml) rather than a separate pipeline stage, "
            "sample first for volume anomalies, run in parallel with transform not after load."
        ),
        "copy": (
            "Transfer bottleneck. "
            "Check: enable compression on transfer, use region-local staging bucket, "
            "increase parallelism in COPY command (e.g., Snowflake COPY max_file_size)."
        ),
    }

    SEVERITY_ORDER = {"critical": 0, "warn": 1, "info": 2}

    def __init__(
        self,
        stages: List[Dict],
        slow_threshold_s: float = DEFAULT_SLOW_S,
        critical_threshold_s: float = DEFAULT_CRITICAL_S,
    ) -> None:
        # Exclude skipped stages from timing analysis
        self.stages = [s for s in stages if s.get("status") != "skipped"]
        self.slow_threshold_s = slow_threshold_s
        self.critical_threshold_s = critical_threshold_s

    def _keyword_hint(self, stage_name: str) -> Optional[str]:
        lower = stage_name.lower()
        for keyword, hint in self.KEYWORD_HINTS.items():
            if keyword in lower:
                return hint
        return None

    def _severity_by_duration(self, duration_s: float) -> str:
        if duration_s >= self.critical_threshold_s:
            return "critical"
        if duration_s >= self.slow_threshold_s:
            return "warn"
        return "info"

    def analyze(self, source: str = "pipeline_run") -> OptimizationReport:
        if not self.stages:
            return OptimizationReport(source, 0, 0.0, None, [])

        total_s = sum(s.get("duration_s", 0.0) for s in self.stages)
        slowest = max(self.stages, key=lambda s: s.get("duration_s", 0.0))
        recs: List[Recommendation] = []

        for stage in self.stages:
            name = stage.get("name", "unknown")
            dur = stage.get("duration_s", 0.0)
            status = stage.get("status", "success")
            attempts = stage.get("attempts", 1)
            pct = (dur / total_s * 100) if total_s > 0 else 0.0
            hint = self._keyword_hint(name)

            # Failed stages — address before optimizing
            if status == "failed":
                recs.append(
                    Recommendation(
                        stage=name,
                        severity="critical",
                        finding=f"Stage failed after {attempts} attempt(s) — {dur:.1f}s elapsed",
                        suggestion=(
                            "Resolve failure root cause before optimizing. "
                            "Check logs for error details. "
                            + (hint or "Review stage logic for transient vs permanent failures.")
                        ),
                    )
                )
                continue

            # Slow by absolute time
            if dur >= self.slow_threshold_s:
                severity = self._severity_by_duration(dur)
                recs.append(
                    Recommendation(
                        stage=name,
                        severity=severity,
                        finding=f"Slow stage: {dur:.1f}s ({pct:.0f}% of pipeline total)",
                        suggestion=hint or (
                            "Profile execution plan. "
                            "Check I/O throughput, memory pressure, partition count, "
                            "and whether work can be parallelised."
                        ),
                    )
                )

            # Dominates pipeline even if under absolute threshold
            if pct > 50.0 and dur < self.slow_threshold_s:
                recs.append(
                    Recommendation(
                        stage=name,
                        severity="warn",
                        finding=f"Bottleneck: {pct:.0f}% of total pipeline time ({dur:.1f}s)",
                        suggestion=hint or (
                            "Stage dominates pipeline. "
                            "Consider parallelising work or pushing processing closer to source."
                        ),
                    )
                )

        # Sort: critical first, then warn, then info
        recs.sort(key=lambda r: (self.SEVERITY_ORDER.get(r.severity, 99), -self.stages[0].get("duration_s", 0)))

        bottleneck = (
            slowest["name"]
            if slowest.get("duration_s", 0.0) >= self.slow_threshold_s
            else None
        )

        return OptimizationReport(
            source=source,
            stages_analyzed=len(self.stages),
            total_duration_s=total_s,
            bottleneck_stage=bottleneck,
            recommendations=recs,
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="ETL performance optimizer — analyze pipeline run report for bottlenecks"
    )
    parser.add_argument(
        "--report", "-r", required=True,
        help="JSON run report produced by pipeline_orchestrator.py",
    )
    parser.add_argument(
        "--slow-threshold", type=float, default=DEFAULT_SLOW_S,
        help=f"Seconds before a stage is flagged as slow (default: {DEFAULT_SLOW_S})",
    )
    parser.add_argument(
        "--critical-threshold", type=float, default=DEFAULT_CRITICAL_S,
        help=f"Seconds before a stage is flagged critical (default: {DEFAULT_CRITICAL_S})",
    )
    parser.add_argument("--output", "-o", help="Write analysis JSON to file (stdout if omitted)")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    report_path = Path(args.report)
    if not report_path.exists():
        log.error("Run report not found: %s", report_path)
        sys.exit(1)

    with open(report_path) as f:
        run_report = json.load(f)

    stages = run_report.get("results", [])
    if not stages:
        log.error("No stage results found in report. Check report format.")
        sys.exit(1)

    optimizer = ETLPerformanceOptimizer(
        stages=stages,
        slow_threshold_s=args.slow_threshold,
        critical_threshold_s=args.critical_threshold,
    )
    analysis = optimizer.analyze(source=report_path.name)
    analysis_dict = analysis.to_dict()

    # Print summary to stderr
    log.info(
        "Analyzed %d stages — total %.1fs | bottleneck: %s | %d recommendation(s)",
        analysis.stages_analyzed,
        analysis.total_duration_s,
        analysis.bottleneck_stage or "none",
        len(analysis.recommendations),
    )
    for rec in analysis.recommendations:
        level = logging.ERROR if rec.severity == "critical" else logging.WARNING
        log.log(level, "[%s] %s: %s", rec.severity.upper(), rec.stage, rec.finding)

    analysis_json = json.dumps(analysis_dict, indent=2)
    if args.output:
        with open(args.output, "w") as f:
            f.write(analysis_json)
        log.info("Analysis written to %s", args.output)
    else:
        print(analysis_json)

    sys.exit(0)


if __name__ == "__main__":
    main()
