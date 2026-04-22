#!/usr/bin/env python3
"""
Pipeline stage orchestrator — run DAG-ordered pipeline stages with retry and timing.

Define stages as Python callables or shell commands. Stages execute in topological
(dependency) order. Tracks per-stage timing, retry attempts, and exit status.
Outputs a structured JSON run report compatible with etl_performance_optimizer.py.

Usage:
    python pipeline_orchestrator.py --demo
    python pipeline_orchestrator.py --config stages.json
"""

import sys
import json
import logging
import argparse
import subprocess
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Callable, Dict, List, Optional, Union

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)


@dataclass
class Stage:
    name: str
    command: Union[str, Callable]
    depends_on: List[str] = field(default_factory=list)
    max_retries: int = 2
    retry_delay_s: int = 5


@dataclass
class StageResult:
    name: str
    status: str  # success | failed | skipped
    attempts: int
    duration_s: float
    error: Optional[str] = None


class PipelineOrchestrator:
    """Execute pipeline stages in dependency order with retry logic."""

    def __init__(self, stages: List[Stage]) -> None:
        self.stages: Dict[str, Stage] = {s.name: s for s in stages}
        self._validate_dag()

    def _validate_dag(self) -> None:
        known = set(self.stages)
        for stage in self.stages.values():
            unknown_deps = [d for d in stage.depends_on if d not in known]
            if unknown_deps:
                raise ValueError(
                    f"Stage '{stage.name}' depends on unknown stage(s): {unknown_deps}"
                )

    def _topo_order(self) -> List[str]:
        in_degree: Dict[str, int] = defaultdict(int)
        for stage in self.stages.values():
            in_degree.setdefault(stage.name, 0)
            for dep in stage.depends_on:
                in_degree[stage.name] += 1

        queue: deque = deque(name for name, deg in in_degree.items() if deg == 0)
        order: List[str] = []
        remaining = dict(in_degree)

        while queue:
            name = queue.popleft()
            order.append(name)
            for stage in self.stages.values():
                if name in stage.depends_on:
                    remaining[stage.name] -= 1
                    if remaining[stage.name] == 0:
                        queue.append(stage.name)

        if len(order) != len(self.stages):
            raise ValueError("Cycle detected in pipeline stage dependencies")
        return order

    def _run_stage(self, stage: Stage) -> StageResult:
        attempts = 0
        last_err: Optional[str] = None
        start = time.monotonic()

        while attempts <= stage.max_retries:
            attempts += 1
            try:
                if callable(stage.command):
                    stage.command()
                else:
                    proc = subprocess.run(
                        stage.command,
                        shell=True,
                        capture_output=True,
                        text=True,
                        timeout=3600,
                    )
                    if proc.returncode != 0:
                        raise RuntimeError(
                            proc.stderr.strip() or f"exit code {proc.returncode}"
                        )
                duration = time.monotonic() - start
                return StageResult(stage.name, "success", attempts, round(duration, 3))
            except Exception as exc:
                last_err = str(exc)
                log.warning("Stage '%s' attempt %d failed: %s", stage.name, attempts, last_err)
                if attempts <= stage.max_retries:
                    log.info("Retrying '%s' in %ds...", stage.name, stage.retry_delay_s)
                    time.sleep(stage.retry_delay_s)

        duration = time.monotonic() - start
        return StageResult(stage.name, "failed", attempts, round(duration, 3), last_err)

    def run(self) -> Dict:
        order = self._topo_order()
        log.info("Execution order: %s", " → ".join(order))
        failed: set = set()

        for name in order:
            stage = self.stages[name]
            blocked_by = [d for d in stage.depends_on if d in failed]

            if blocked_by:
                result = StageResult(name, "skipped", 0, 0.0, f"blocked by failed deps {blocked_by}")
                log.warning("Skipping '%s' — blocked by %s", name, blocked_by)
            else:
                log.info("Starting stage: %s", name)
                result = self._run_stage(stage)
                if result.status == "failed":
                    failed.add(name)
                    log.error(
                        "Stage '%s' failed after %d attempt(s): %s",
                        name, result.attempts, result.error,
                    )
                else:
                    log.info("Stage '%s' completed in %.2fs", name, result.duration_s)

            # Store results keyed by stage name so optimizer can consume by name
            self.stages[name].__dict__["_result"] = result

        results = [self.stages[n].__dict__["_result"] for n in order]
        succeeded = sum(1 for r in results if r.status == "success")

        return {
            "status": "success" if not failed else "partial_failure",
            "run_at": datetime.now(timezone.utc).isoformat(),
            "stages_total": len(order),
            "stages_succeeded": succeeded,
            "stages_failed": len(failed),
            "results": [asdict(r) for r in results],
        }


def _demo_stages() -> List[Stage]:
    """Three-stage extract → transform → load demo pipeline."""
    return [
        Stage(
            name="extract",
            command=lambda: (log.info("Extracting source data..."), time.sleep(0.1)),
            max_retries=1,
        ),
        Stage(
            name="transform",
            command=lambda: (log.info("Applying transforms..."), time.sleep(0.05)),
            depends_on=["extract"],
        ),
        Stage(
            name="load",
            command=lambda: (log.info("Loading to warehouse..."), time.sleep(0.05)),
            depends_on=["transform"],
        ),
    ]


def _load_stages_from_config(path: str) -> List[Stage]:
    """
    Load stage definitions from a JSON config file.

    Expected format:
        {
          "stages": [
            {"name": "extract", "command": "python extract.py", "depends_on": [], "max_retries": 2},
            {"name": "transform", "command": "dbt run --select silver", "depends_on": ["extract"]}
          ]
        }
    """
    with open(path) as f:
        raw = json.load(f)
    stages = []
    for s in raw["stages"]:
        stages.append(
            Stage(
                name=s["name"],
                command=s["command"],
                depends_on=s.get("depends_on", []),
                max_retries=s.get("max_retries", 2),
                retry_delay_s=s.get("retry_delay_s", 5),
            )
        )
    return stages


def main() -> None:
    parser = argparse.ArgumentParser(description="Pipeline stage orchestrator")
    parser.add_argument("--config", "-c", help="JSON stage config file")
    parser.add_argument("--demo", action="store_true", help="Run demo extract→transform→load pipeline")
    parser.add_argument("--output", "-o", help="Write run report JSON to file (stdout if omitted)")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if args.demo:
        stages = _demo_stages()
    elif args.config:
        stages = _load_stages_from_config(args.config)
    else:
        parser.error("Provide --config <file> or --demo")

    orchestrator = PipelineOrchestrator(stages)
    report = orchestrator.run()

    report_json = json.dumps(report, indent=2)
    if args.output:
        with open(args.output, "w") as f:
            f.write(report_json)
        log.info("Run report written to %s", args.output)
    else:
        print(report_json)

    sys.exit(0 if report["status"] == "success" else 1)


if __name__ == "__main__":
    main()
