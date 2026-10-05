#!/usr/bin/env python3
"""Generate a rollback runbook from a migration plan.

Usage:
    python3 rollback_generator.py --input plan.json [--format md|json|both] [-o prefix]

Input is the JSON written by migration_planner.py. For every phase the runbook
gives a trigger, ordered steps, verification, and a data-repair note. Phases
that cannot be undone are marked ROLL FORWARD ONLY.
With --format both, -o is a path prefix: prefix.md and prefix.json.
"""
import argparse
import json
import sys

ENVELOPE_BEFORE = [
    "Incident commander states 'rolling back phase {name}' in the incident channel and records the time",
    "Pause deploys and background jobs for this migration",
]
ENVELOPE_AFTER = [
    "Confirm error rate and p95 latency are back within baseline for 15 minutes",
    "Post the rollback result and the next decision time to stakeholders",
]
REPAIR_NOTE = ("The new side received writes during this phase. Run the reconciliation delta check "
               "before any retry. Do not re-enable the phase until the diff is zero or accepted.")


def runbook_for(phase, guardrails):
    steps = [s.format(name=phase["name"]) for s in ENVELOPE_BEFORE]
    steps.append(phase["rollback_action"])
    steps += ENVELOPE_AFTER
    entry = {
        "phase": phase["name"],
        "index": phase["index"],
        "roll_forward_only": not phase["reversible"],
        "trigger": phase["rollback_trigger"],
        "automatic_triggers": [
            f"Error rate rises more than {guardrails['error_rate_increase_pct']}% over baseline for 5 minutes",
            f"p95 latency rises more than {guardrails['p95_latency_increase_pct']}% over baseline for 5 minutes",
        ] if phase["reversible"] else [],
        "steps": steps,
        "verification": phase["exit_criteria"][:1] + ["Baseline SLOs hold after rollback"],
        "data_repair": REPAIR_NOTE if phase["writes_to_new"] and phase["reversible"] else None,
        "estimated_minutes": 30 if phase["reversible"] else None,
    }
    if not phase["reversible"]:
        entry["steps"] = ["Do not attempt a rollback. Fix forward, or restore only the affected object from the final snapshot:",
                          phase["rollback_action"]]
    return entry


def build(plan):
    entries = [runbook_for(p, plan["guardrails"]) for p in plan["phases"]]
    first_irreversible = next((e["phase"] for e in entries if e["roll_forward_only"]), None)
    return {
        "migration": plan["name"],
        "point_of_no_return": first_irreversible,
        "decision_rights": "Name one rollback owner per phase before start. The owner can roll back without further approval.",
        "phases": entries,
        "rehearsal_required": "Rehearse each rollback on a production-sized copy. Record the measured minutes in this runbook.",
    }


def render_markdown(rb):
    lines = [f"# Rollback runbook: {rb['migration']}", "",
             f"Point of no return: {rb['point_of_no_return'] or 'none'}", "",
             rb["decision_rights"], rb["rehearsal_required"], ""]
    for e in rb["phases"]:
        title = f"## Phase {e['index']}: {e['phase']}" + (" (ROLL FORWARD ONLY)" if e["roll_forward_only"] else "")
        lines += [title, f"Trigger: {e['trigger']}"]
        lines += [f"Automatic: {t}" for t in e["automatic_triggers"]]
        lines += ["", "Steps:"] + [f"{n}. {s}" for n, s in enumerate(e["steps"], 1)]
        lines += ["", "Verify:"] + [f"- {v}" for v in e["verification"]]
        if e["data_repair"]:
            lines += ["", f"Data repair: {e['data_repair']}"]
        lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", required=True)
    ap.add_argument("--format", choices=["md", "json", "both"], default="md")
    ap.add_argument("-o", "--output")
    args = ap.parse_args()
    with open(args.input, encoding="utf-8") as f:
        rb = build(json.load(f))
    outputs = {"md": render_markdown(rb), "json": json.dumps(rb, indent=2) + "\n"}
    wanted = ["md", "json"] if args.format == "both" else [args.format]
    if args.format == "both" and not args.output:
        sys.exit("error: --format both needs -o prefix")
    for fmt in wanted:
        if args.output:
            path = f"{args.output}.{fmt}" if args.format == "both" else args.output
            with open(path, "w", encoding="utf-8") as f:
                f.write(outputs[fmt])
        else:
            sys.stdout.write(outputs[fmt])


if __name__ == "__main__":
    main()
