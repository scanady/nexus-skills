#!/usr/bin/env python3
"""Generate a phased migration plan from a JSON spec.

Usage:
    python3 migration_planner.py --input spec.json [--format json|md] [-o plan.json]

Spec fields (see assets/sample-database-migration.json):
    name, type (database|service|infrastructure), pattern (optional),
    constraints.{max_downtime_minutes, data_volume_gb, dependencies,
    compliance, backfill_gb_per_hour}, tables[], schema_changes[]

The plan JSON feeds rollback_generator.py.
"""
import argparse
import json
import sys

# Phase fields: name, objective, steps, exit_criteria, rollback_trigger,
# rollback_action, hours, reversible, downtime, writes_to_new, scales_with_data
EXPAND_CONTRACT = [
    dict(name="prepare", objective="Prove backups restore and record baselines.",
         steps=["Take a backup and restore it into a scratch environment",
                "Record baseline p95 latency, error rate, and row counts",
                "Rehearse every step on a production-sized copy",
                "Name the rollback owner and the on-call channel"],
         exit_criteria=["Restore test passes", "Baselines recorded", "Rehearsal timings recorded"],
         rollback_trigger="Restore test or rehearsal fails.",
         rollback_action="Stop. Production is unchanged.",
         hours=8, reversible=True, downtime=False, writes_to_new=False),
    dict(name="expand", objective="Add new schema objects beside the old ones. Nothing reads them yet.",
         steps=["Apply additive DDL with an online tool (nullable columns, new tables, concurrent indexes)",
                "Set lock_timeout and statement_timeout on every DDL session",
                "Confirm the legacy application runs unchanged"],
         exit_criteria=["DDL applied", "Legacy error rate equals baseline", "Replication lag at baseline"],
         rollback_trigger="Lock waits, replication lag, or legacy errors above threshold.",
         rollback_action="Drop the added objects. The change is additive, so the drop is safe.",
         hours=4, reversible=True, downtime=False, writes_to_new=False),
    dict(name="dual_write", objective="Write to old and new schema. Old stays the source of truth.",
         steps=["Deploy dual-write code behind a flag, default off",
                "Enable for internal users, then 10%, 50%, 100% of writes",
                "Log every failed secondary write with the row key",
                "Soak at 100% for the soak window"],
         exit_criteria=["Secondary write failure rate below 0.01%", "No drift in sampled reconciliation"],
         rollback_trigger="Primary write latency regresses or secondary failures exceed threshold.",
         rollback_action="Turn the dual-write flag off. Reconcile rows written during the phase before any retry.",
         hours=24, reversible=True, downtime=False, writes_to_new=True),
    dict(name="backfill", objective="Copy historic rows into the new schema in idempotent batches.",
         steps=["Run batches keyed by primary key range, 1k-10k rows each",
                "Throttle on replica lag and primary CPU",
                "Make every batch idempotent (upsert, never blind insert)",
                "Checkpoint progress so the job resumes after a crash"],
         exit_criteria=["Every key range processed", "Job checkpoint at end of table"],
         rollback_trigger="Replica lag or primary CPU stays above limit after throttling.",
         rollback_action="Pause the job. Old schema is still the source of truth, so truncating new columns is safe.",
         hours=4, reversible=True, downtime=False, writes_to_new=True, scales_with_data=True),
    dict(name="verify", objective="Prove old and new data agree before any reader moves.",
         steps=["Compare row counts and per-range checksums",
                "Run the business-query comparison set on both sides",
                "Resolve every difference or record it as accepted",
                "Repeat daily until the verify window ends"],
         exit_criteria=["Zero unexplained differences for the full verify window"],
         rollback_trigger="Unexplained differences persist after repair.",
         rollback_action="Hold. Do not move readers. Fix the dual-write or backfill defect and re-run backfill.",
         hours=24, reversible=True, downtime=False, writes_to_new=True),
    dict(name="cutover_reads", objective="Move reads to the new schema in steps. Dual-write stays on.",
         steps=["Enable new reads for internal users, then 1%, 10%, 50%, 100%",
                "Compare response bodies for a sampled shadow read",
                "Watch p95 latency and error rate at each step"],
         exit_criteria=["100% of reads on new schema for the soak window", "SLOs at baseline"],
         rollback_trigger="Error rate or p95 latency regresses past the guardrail.",
         rollback_action="Flip the read flag back. Dual-write kept the old schema current, so no data repair is needed.",
         hours=12, reversible=True, downtime=False, writes_to_new=True),
    dict(name="contract", objective="Stop writing to the old schema and remove it after the retention window.",
         steps=["Turn off writes to old objects",
                "Keep a final snapshot for the retention window",
                "Drop old columns, tables, and dead code in separate releases",
                "Remove the flags"],
         exit_criteria=["Retention window passed", "No consumer reads old objects (query log check)"],
         rollback_trigger="A consumer breaks after old objects are dropped.",
         rollback_action="Roll forward. Restore only the dropped object from the final snapshot.",
         hours=8, reversible=False, downtime=False, writes_to_new=True),
]

CDC_CUTOVER = [
    EXPAND_CONTRACT[0],
    dict(name="replicate", objective="Copy a snapshot to the target and stream changes continuously.",
         steps=["Create the target and load the initial snapshot",
                "Start change data capture from the snapshot position",
                "Alert on replication lag"],
         exit_criteria=["Lag below 5 seconds for the soak window"],
         rollback_trigger="Lag grows without bound or CDC stops.",
         rollback_action="Stop replication and discard the target. Production is unchanged.",
         hours=4, reversible=True, downtime=False, writes_to_new=False, scales_with_data=True),
    dict(name="verify", objective="Prove target data matches source while replication runs.",
         steps=["Compare counts and checksums on a lag-adjusted snapshot",
                "Run application smoke tests against the target",
                "Replay a production-like load on the target"],
         exit_criteria=["Zero unexplained differences", "Load test meets SLOs"],
         rollback_trigger="Differences or SLO misses persist.",
         rollback_action="Hold the cutover. Fix and re-verify.",
         hours=24, reversible=True, downtime=False, writes_to_new=False),
    dict(name="cutover", objective="Freeze writes, drain lag, and repoint the application.",
         steps=["Announce the window and set read-only mode on the source",
                "Wait for lag to reach zero and compare final checksums",
                "Repoint connection strings and sequences, then lift read-only",
                "Start reverse replication to the old source"],
         exit_criteria=["Writes accepted on target", "Reverse replication lag below 5 seconds"],
         rollback_trigger="Target errors or data check fails inside the rollback window.",
         rollback_action="Freeze writes on target, drain reverse replication, repoint to the old source.",
         hours=2, reversible=True, downtime=True, writes_to_new=True),
    dict(name="soak", objective="Run on the target with a live way back.",
         steps=["Keep reverse replication running", "Watch SLOs and reconciliation daily"],
         exit_criteria=["Soak window passed with SLOs at baseline"],
         rollback_trigger="SLO breach or data defect found.",
         rollback_action="Run the cutover rollback while reverse replication is current.",
         hours=72, reversible=True, downtime=False, writes_to_new=True),
    dict(name="decommission", objective="Retire the old source.",
         steps=["Stop reverse replication", "Keep a final snapshot for the retention window", "Delete the source"],
         exit_criteria=["Retention window passed"],
         rollback_trigger="A consumer still needs the old source.",
         rollback_action="Roll forward. Restore from the final snapshot.",
         hours=4, reversible=False, downtime=False, writes_to_new=True),
]

STRANGLER_FIG = [
    dict(name="prepare", objective="Pin legacy behavior and place a routing facade.",
         steps=["Write characterization tests for the slice being replaced",
                "Record baseline latency, error rate, and business KPIs for the slice",
                "Define the slice boundary and its data owner"],
         exit_criteria=["Characterization tests pass on legacy", "Baselines recorded"],
         rollback_trigger="Tests cannot pin legacy behavior.",
         rollback_action="Stop. Production is unchanged.",
         hours=16, reversible=True, downtime=False, writes_to_new=False),
    dict(name="facade", objective="Route all traffic through the facade to legacy.",
         steps=["Deploy the proxy or gateway with a pass-through route",
                "Confirm latency overhead is within budget",
                "Add a per-route flag that selects legacy or new"],
         exit_criteria=["100% of slice traffic through facade", "Overhead within budget"],
         rollback_trigger="Facade adds errors or latency over budget.",
         rollback_action="Route clients back around the facade to legacy.",
         hours=8, reversible=True, downtime=False, writes_to_new=False),
    dict(name="shadow", objective="Send a copy of traffic to the new service and compare results.",
         steps=["Mirror requests to the new service. Discard its responses.",
                "Compare status, body, and side effects with legacy",
                "Make shadow calls free of side effects (stubbed writes)"],
         exit_criteria=["Mismatch rate below target, every mismatch explained"],
         rollback_trigger="Shadow load degrades legacy.",
         rollback_action="Turn mirroring off.",
         hours=24, reversible=True, downtime=False, writes_to_new=False),
    dict(name="canary", objective="Serve a small, sticky cohort from the new service.",
         steps=["Route 1%, then 5%, then 25% by stable user hash",
                "Hold each step for one full traffic cycle",
                "Check guardrail metrics before each step"],
         exit_criteria=["25% on new for the soak window with SLOs at baseline"],
         rollback_trigger="Error rate, latency, or business KPI crosses the guardrail.",
         rollback_action="Set the route flag to legacy. Reconcile writes made by the new service.",
         hours=24, reversible=True, downtime=False, writes_to_new=True),
    dict(name="ramp", objective="Move the remaining traffic.",
         steps=["Route 50%, then 100%", "Keep legacy warm and receiving writes or replication"],
         exit_criteria=["100% on new for the soak window"],
         rollback_trigger="Guardrail breach.",
         rollback_action="Set the route flag to legacy. Legacy must hold current data (dual-write or reverse sync).",
         hours=24, reversible=True, downtime=False, writes_to_new=True),
    dict(name="decommission", objective="Delete the legacy slice.",
         steps=["Confirm no traffic reaches legacy for the retention window",
                "Archive code and data", "Remove routes, flags, and legacy code"],
         exit_criteria=["Retention window passed with zero legacy traffic"],
         rollback_trigger="A hidden consumer reaches the removed slice.",
         rollback_action="Roll forward. Redeploy the archived slice only if no other fix exists.",
         hours=8, reversible=False, downtime=False, writes_to_new=True),
]

BLUE_GREEN = [
    STRANGLER_FIG[0],
    dict(name="green_build", objective="Build the full new environment beside the old one.",
         steps=["Provision green from code", "Replicate data to green", "Smoke-test green with synthetic traffic"],
         exit_criteria=["Green passes smoke and load tests"],
         rollback_trigger="Green cannot meet SLOs.",
         rollback_action="Destroy green. Blue is unchanged.",
         hours=16, reversible=True, downtime=False, writes_to_new=False, scales_with_data=True),
    dict(name="switch", objective="Move traffic from blue to green.",
         steps=["Lower DNS TTL ahead of time", "Shift weighted traffic or flip the load balancer",
                "Keep blue running with data sync back from green"],
         exit_criteria=["100% on green", "SLOs at baseline"],
         rollback_trigger="Guardrail breach inside the rollback window.",
         rollback_action="Flip traffic back to blue. Confirm sync back is current first.",
         hours=4, reversible=True, downtime=False, writes_to_new=True),
    dict(name="soak", objective="Run on green with blue ready.",
         steps=["Watch SLOs and business KPIs", "Keep blue warm"],
         exit_criteria=["Soak window passed"],
         rollback_trigger="SLO breach.",
         rollback_action="Flip traffic back to blue.",
         hours=48, reversible=True, downtime=False, writes_to_new=True),
    dict(name="decommission", objective="Retire blue.",
         steps=["Snapshot blue", "Destroy blue", "Remove sync back"],
         exit_criteria=["Retention window passed"],
         rollback_trigger="A consumer still needs blue.",
         rollback_action="Roll forward. Rebuild from the snapshot.",
         hours=4, reversible=False, downtime=False, writes_to_new=True),
]

INFRASTRUCTURE = [
    dict(name="prepare", objective="Inventory workloads and codify the target.",
         steps=["List every workload, dependency, and network path",
                "Write the target as infrastructure as code",
                "Lower DNS TTLs to 60 seconds"],
         exit_criteria=["Inventory signed off", "Target plan applies cleanly in a sandbox"],
         rollback_trigger="Inventory finds an unmapped dependency.",
         rollback_action="Stop. Production is unchanged.",
         hours=24, reversible=True, downtime=False, writes_to_new=False),
    dict(name="pilot", objective="Move one non-critical workload first.",
         steps=["Pick the lowest-risk workload", "Move it end to end", "Record cost and latency"],
         exit_criteria=["Pilot meets SLOs and cost model"],
         rollback_trigger="Pilot misses SLOs.",
         rollback_action="Point the workload back at the old environment.",
         hours=24, reversible=True, downtime=False, writes_to_new=True),
    dict(name="replicate", objective="Replicate data and connect the networks.",
         steps=["Set up site-to-site connectivity", "Start continuous data replication",
                "Verify replicated data with checksums"],
         exit_criteria=["Replication lag below target", "Checksums match"],
         rollback_trigger="Replication cannot keep up.",
         rollback_action="Stop replication. Production is unchanged.",
         hours=8, reversible=True, downtime=False, writes_to_new=False, scales_with_data=True),
    dict(name="cutover", objective="Move production workloads in waves.",
         steps=["Move workloads in dependency order", "Repoint DNS per wave", "Hold each wave for one traffic cycle"],
         exit_criteria=["All waves moved", "SLOs at baseline"],
         rollback_trigger="Wave breaches guardrail.",
         rollback_action="Repoint DNS for the wave to the old environment. Reverse replication must be current.",
         hours=16, reversible=True, downtime=True, writes_to_new=True),
    dict(name="soak", objective="Run on the new environment with the old one intact.",
         steps=["Watch SLOs and cost", "Test disaster recovery in the new environment"],
         exit_criteria=["Soak window passed", "DR test passed"],
         rollback_trigger="SLO breach or failed DR test.",
         rollback_action="Repoint DNS to the old environment.",
         hours=72, reversible=True, downtime=False, writes_to_new=True),
    dict(name="decommission", objective="Retire the old environment.",
         steps=["Take final backups", "Cancel contracts and delete resources after the retention window"],
         exit_criteria=["Retention window passed"],
         rollback_trigger="A consumer still needs the old environment.",
         rollback_action="Roll forward. Restore from final backups.",
         hours=8, reversible=False, downtime=False, writes_to_new=True),
]

CATALOG = {
    ("database", "expand_contract"): EXPAND_CONTRACT,
    ("database", "cdc_cutover"): CDC_CUTOVER,
    ("service", "strangler_fig"): STRANGLER_FIG,
    ("service", "blue_green"): BLUE_GREEN,
    ("infrastructure", "replicate_cutover"): INFRASTRUCTURE,
}
DEFAULT_PATTERN = {"database": "expand_contract", "service": "strangler_fig",
                   "infrastructure": "replicate_cutover"}
COMPLEXITY = [(0, "low", 1.0), (4, "medium", 1.5), (7, "high", 2.25), (10, "critical", 3.0)]
CDC_DOWNTIME_MINUTES = 10
DEFAULT_BACKFILL_GB_PER_HOUR = 50
# Schema changes that need more than one release.
MULTI_STEP = {"modify_column", "rename_column", "rename_table", "add_constraint"}
CONTRACT_CHANGES = {"drop_column", "drop_table", "drop_constraint"}


def fail(message):
    sys.exit(f"error: {message}")


def score(spec, changes):
    c = spec.get("constraints", {})
    points = 0
    points += 3 if c.get("data_volume_gb", 0) >= 1000 else 1 if c.get("data_volume_gb", 0) >= 100 else 0
    points += 2 if len(c.get("dependencies", [])) >= 5 else 1 if len(c.get("dependencies", [])) >= 2 else 0
    points += min(len(c.get("compliance", [])), 2)
    points += 2 if c.get("max_downtime_minutes") == 0 else 0
    points += 1 if any(t.get("critical") for t in spec.get("tables", [])) else 0
    points += 2 if any(ch["kind"] != "expand" for ch in changes) else 0
    return points


def classify_changes(spec):
    out = []
    for entry in spec.get("schema_changes", []):
        for change in entry.get("changes", []):
            kind = ("contract" if change["type"] in CONTRACT_CHANGES
                    else "multi_step" if change["type"] in MULTI_STEP else "expand")
            out.append({"table": entry["table"], "change": change["type"],
                        "column": change.get("column"), "kind": kind})
    return out


def build_risks(spec, changes, downtime):
    c = spec.get("constraints", {})
    risks = [dict(id="R1", category="technical", likelihood="medium", impact="high",
                  description="Rollback path fails when first used.",
                  mitigation="Rehearse each phase rollback on a production-sized copy before the real run.")]
    if c.get("data_volume_gb", 0) >= 500:
        risks.append(dict(id="R2", category="technical", likelihood="medium", impact="high",
                          description="Bulk copy saturates the primary and slows live traffic.",
                          mitigation="Throttle on replica lag and CPU. Run in the low-traffic window."))
    if len(c.get("dependencies", [])) >= 4:
        risks.append(dict(id="R3", category="operational", likelihood="high", impact="medium",
                          description="An unlisted consumer breaks on a schema or contract change.",
                          mitigation="Check query and access logs for consumers. Notify every owner before contract."))
    if c.get("compliance"):
        risks.append(dict(id="R4", category="business", likelihood="low", impact="high",
                          description=f"Copies of regulated data ({', '.join(c['compliance'])}) outlive their retention rules.",
                          mitigation="Define retention for every copy and delete on schedule. Record the evidence."))
    if c.get("max_downtime_minutes") == 0:
        risks.append(dict(id="R5", category="technical", likelihood="medium", impact="high",
                          description="Zero downtime budget leaves no slack for a freeze step.",
                          mitigation="Use expand and contract with dual write. Avoid any step that needs a write freeze."))
    if downtime is not None and downtime > c.get("max_downtime_minutes", float("inf")):
        risks.append(dict(id="R6", category="business", likelihood="high", impact="high",
                          description=f"Expected downtime ({downtime} min) exceeds the budget ({c['max_downtime_minutes']} min).",
                          mitigation="Switch to expand_contract, or negotiate a larger window."))
    if any(t.get("critical") for t in spec.get("tables", [])):
        risks.append(dict(id="R7", category="technical", likelihood="low", impact="high",
                          description="Silent corruption in a critical table.",
                          mitigation="Checksum critical tables on every verify run. Gate cutover on zero differences."))
    if any(ch["kind"] == "contract" for ch in changes):
        risks.append(dict(id="R8", category="technical", likelihood="medium", impact="high",
                          description="Destructive change cannot be undone after contract.",
                          mitigation="Run destructive changes only in the contract phase, after the retention window, with a final snapshot."))
    return risks


def plan(spec):
    kind = spec.get("type")
    pattern = spec.get("pattern") or DEFAULT_PATTERN.get(kind)
    if (kind, pattern) not in CATALOG:
        valid = ", ".join(f"{t}/{p}" for t, p in CATALOG)
        fail(f"unsupported type/pattern {kind}/{pattern}. Valid: {valid}")
    c = spec.get("constraints", {})
    changes = classify_changes(spec)
    total_score = score(spec, changes)
    label, factor = next((lbl, f) for floor, lbl, f in reversed(COMPLEXITY) if total_score >= floor)
    rate = c.get("backfill_gb_per_hour", DEFAULT_BACKFILL_GB_PER_HOUR)
    phases = []
    for i, template in enumerate(CATALOG[(kind, pattern)], 1):
        phase = {k: v for k, v in template.items() if k != "scales_with_data"}
        phase["index"] = i
        phase["hours"] = round(template["hours"] * factor
                               + (c.get("data_volume_gb", 0) / rate if template.get("scales_with_data") else 0), 1)
        phases.append(phase)
    downtime = CDC_DOWNTIME_MINUTES if any(p["downtime"] for p in phases) else 0
    return {
        "name": spec.get("name", "unnamed-migration"),
        "type": kind,
        "pattern": pattern,
        "complexity": label,
        "complexity_score": total_score,
        "estimated_duration_hours": round(sum(p["hours"] for p in phases), 1),
        "expected_downtime_minutes": downtime,
        "downtime_budget_minutes": c.get("max_downtime_minutes"),
        "guardrails": {"error_rate_increase_pct": 50, "p95_latency_increase_pct": 25,
                       "note": "Starting values. Replace with the service SLOs."},
        "schema_change_sequence": changes,
        "phases": phases,
        "risks": build_risks(spec, changes, downtime),
        "approval_gate": ["compatibility_checker exits 0, or the owner accepts each flagged item in writing",
                          "Every phase has a rehearsed rollback in the runbook"],
    }


def render_markdown(p):
    lines = [f"# Migration plan: {p['name']}", "",
             f"- Type / pattern: {p['type']} / {p['pattern']}",
             f"- Complexity: {p['complexity']} (score {p['complexity_score']})",
             f"- Estimated duration: {p['estimated_duration_hours']} hours",
             f"- Expected downtime: {p['expected_downtime_minutes']} min (budget: {p['downtime_budget_minutes']})", ""]
    for ph in p["phases"]:
        lines += [f"## Phase {ph['index']}: {ph['name']} ({ph['hours']} h)", ph["objective"], "", "Steps:"]
        lines += [f"{n}. {s}" for n, s in enumerate(ph["steps"], 1)]
        lines += ["", "Exit criteria:"] + [f"- {e}" for e in ph["exit_criteria"]]
        lines += [f"- Rollback trigger: {ph['rollback_trigger']}"]
        lines += [] if ph["reversible"] else ["- POINT OF NO RETURN: roll forward only."]
        lines.append("")
    lines += ["## Risks"] + [f"- {r['id']} [{r['likelihood']}/{r['impact']}] {r['description']} Mitigation: {r['mitigation']}"
                             for r in p["risks"]]
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", required=True)
    ap.add_argument("--format", choices=["json", "md"], default="json")
    ap.add_argument("-o", "--output")
    args = ap.parse_args()
    with open(args.input, encoding="utf-8") as f:
        result = plan(json.load(f))
    text = json.dumps(result, indent=2) + "\n" if args.format == "json" else render_markdown(result)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
    else:
        sys.stdout.write(text)


if __name__ == "__main__":
    main()
