# /// script
# requires-python = ">=3.9"
# ///
"""Aggregate grading.json files from an eval iteration into benchmark.json.

Usage:
    python3 scripts/benchmark.py <iteration-dir>

Example:
    python3 scripts/benchmark.py csv-analyzer-workspace/iteration-1

Scans the iteration directory for eval-* subdirectories, reads grading.json
and timing.json from with_skill/ and without_skill/ (or old_skill/) runs,
and writes benchmark.json to the iteration directory.
"""

import json
import math
import sys
from pathlib import Path


def load_json(path: Path) -> dict | None:
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return None


def mean(values: list[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


def stddev(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    m = mean(values)
    variance = sum((x - m) ** 2 for x in values) / (len(values) - 1)
    return math.sqrt(variance)


def collect_run_stats(
    eval_dirs: list[Path], run_type: str
) -> dict | None:
    pass_rates: list[float] = []
    times: list[float] = []
    tokens: list[float] = []

    for eval_dir in eval_dirs:
        run_dir = eval_dir / run_type
        if not run_dir.is_dir():
            continue

        grading = load_json(run_dir / "grading.json")
        if grading and "summary" in grading:
            pass_rates.append(grading["summary"].get("pass_rate", 0.0))

        timing = load_json(run_dir / "timing.json")
        if timing:
            if "duration_ms" in timing:
                times.append(timing["duration_ms"] / 1000.0)
            if "total_tokens" in timing:
                tokens.append(float(timing["total_tokens"]))

    if not pass_rates:
        return None

    return {
        "pass_rate": {"mean": round(mean(pass_rates), 4), "stddev": round(stddev(pass_rates), 4)},
        "time_seconds": {"mean": round(mean(times), 1), "stddev": round(stddev(times), 1)} if times else None,
        "tokens": {"mean": round(mean(tokens), 0), "stddev": round(stddev(tokens), 0)} if tokens else None,
    }


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 scripts/benchmark.py <iteration-dir>", file=sys.stderr)
        print("Example: python3 scripts/benchmark.py workspace/iteration-1", file=sys.stderr)
        sys.exit(1)

    iteration_dir = Path(sys.argv[1])
    if not iteration_dir.is_dir():
        print(f"Error: '{iteration_dir}' is not a directory.", file=sys.stderr)
        sys.exit(1)

    eval_dirs = sorted(
        p for p in iteration_dir.iterdir()
        if p.is_dir() and p.name.startswith("eval-")
    )

    if not eval_dirs:
        print(f"Error: No eval-* directories found in '{iteration_dir}'.", file=sys.stderr)
        sys.exit(1)

    # Detect baseline type: without_skill or old_skill
    baseline_type = "without_skill"
    for eval_dir in eval_dirs:
        if (eval_dir / "old_skill").is_dir():
            baseline_type = "old_skill"
            break

    with_skill = collect_run_stats(eval_dirs, "with_skill")
    baseline = collect_run_stats(eval_dirs, baseline_type)

    if not with_skill:
        print("Error: No with_skill grading data found.", file=sys.stderr)
        sys.exit(1)

    benchmark: dict = {"run_summary": {"with_skill": with_skill}}

    if baseline:
        benchmark["run_summary"][baseline_type] = baseline
        delta: dict = {}
        delta["pass_rate"] = round(
            with_skill["pass_rate"]["mean"] - baseline["pass_rate"]["mean"], 4
        )
        if with_skill.get("time_seconds") and baseline.get("time_seconds"):
            delta["time_seconds"] = round(
                with_skill["time_seconds"]["mean"] - baseline["time_seconds"]["mean"], 1
            )
        if with_skill.get("tokens") and baseline.get("tokens"):
            delta["tokens"] = round(
                with_skill["tokens"]["mean"] - baseline["tokens"]["mean"], 0
            )
        benchmark["run_summary"]["delta"] = delta

    # Per-eval breakdown
    per_eval: list[dict] = []
    for eval_dir in eval_dirs:
        entry: dict = {"name": eval_dir.name}
        for run_type in ["with_skill", baseline_type]:
            grading = load_json(eval_dir / run_type / "grading.json")
            if grading and "summary" in grading:
                entry[run_type] = {
                    "pass_rate": grading["summary"].get("pass_rate", 0.0),
                    "passed": grading["summary"].get("passed", 0),
                    "failed": grading["summary"].get("failed", 0),
                    "total": grading["summary"].get("total", 0),
                }
        per_eval.append(entry)

    benchmark["per_eval"] = per_eval

    output_path = iteration_dir / "benchmark.json"
    with open(output_path, "w") as f:
        json.dump(benchmark, f, indent=2)

    print(json.dumps(benchmark, indent=2))
    print(f"\nBenchmark written to {output_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
