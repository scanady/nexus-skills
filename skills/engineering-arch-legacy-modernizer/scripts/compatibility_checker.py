#!/usr/bin/env python3
"""Compare a before and after contract and classify each change.

Usage:
    python3 compatibility_checker.py --before a.json --after b.json --type database|api
                                     [--format json|md] [-o report.json]

Exit code: 0 compatible, 1 potentially breaking only, 2 breaking.
Use the exit code as a CI gate.

Database schema shape (see assets/schema-before.json):
    {"tables": {"users": {"columns": {"id": {"type": "bigint", "nullable": false,
        "primary_key": true, "unique": false, "length": 50, "default": null}},
        "foreign_keys": {"fk_name": {"column": "x", "references": "t.id"}},
        "indexes": {"idx_name": {"columns": ["a"], "unique": false}}}}}

API shape (see assets/api-before.json):
    {"endpoints": {"GET /users/{id}": {"params": {"id": {"type": "string", "required": true}},
        "response": {"id": "string"}}}}

A rename looks like a drop plus an add. The checker cannot see intent, so it
reports the drop as breaking. Treat a matching drop and add as one rename and
use the multi-step recipe in references/zero-downtime-techniques.md.
"""
import argparse
import json
import sys

COMPATIBLE, POTENTIAL, BREAKING = "compatible", "potentially_breaking", "breaking"
EXIT = {COMPATIBLE: 0, POTENTIAL: 1, BREAKING: 2}
INT_ORDER = ["smallint", "int", "integer", "bigint"]
TEXT_TYPES = {"varchar", "char", "text"}


class Report:
    def __init__(self):
        self.issues = []

    def add(self, level, where, what, fix):
        self.issues.append({"level": level, "where": where, "change": what, "mitigation": fix})

    def overall(self):
        levels = {i["level"] for i in self.issues}
        return BREAKING if BREAKING in levels else POTENTIAL if POTENTIAL in levels else COMPATIBLE

    def count(self, level):
        return sum(1 for i in self.issues if i["level"] == level)


def type_change(old, new):
    """Return (level, note) for a column type change."""
    ot, nt = old.get("type", "").lower(), new.get("type", "").lower()
    ol, nl = old.get("length"), new.get("length")
    if ot == nt and ol == nl:
        return COMPATIBLE, ""
    if ot in INT_ORDER and nt in INT_ORDER:
        if INT_ORDER.index(nt) > INT_ORDER.index(ot):
            return POTENTIAL, f"{ot} to {nt} widens. Old clients may overflow or mis-parse larger ids."
        return BREAKING, f"{ot} to {nt} narrows. Existing values can overflow."
    if ot in TEXT_TYPES and nt in TEXT_TYPES:
        if nt == "text" or (ot == nt and (nl or 0) > (ol or 0)):
            return POTENTIAL, f"{ot}({ol}) to {nt}({nl}) widens. Check readers that assume a max length."
        return BREAKING, f"{ot}({ol}) to {nt}({nl}) can truncate or reject existing values."
    return BREAKING, f"{ot} to {nt} changes type family. Existing values need conversion."


def diff_columns(rep, table, before, after):
    for name in before.keys() - after.keys():
        rep.add(BREAKING, f"{table}.{name}", "column removed",
                "Stop reads and writes first. Drop in the contract phase after the retention window.")
    for name in after.keys() - before.keys():
        col = after[name]
        if not col.get("nullable", True) and col.get("default") is None and not col.get("primary_key"):
            rep.add(BREAKING, f"{table}.{name}", "new NOT NULL column without default",
                    "Add as nullable, backfill, then add the constraint in a later release.")
        else:
            rep.add(COMPATIBLE, f"{table}.{name}", "column added", "")
    for name in before.keys() & after.keys():
        old, new = before[name], after[name]
        where = f"{table}.{name}"
        level, note = type_change(old, new)
        if level != COMPATIBLE:
            rep.add(level, where, note, "Add a new column of the target type, dual write, backfill, switch reads, drop old.")
        if old.get("nullable", True) and not new.get("nullable", True):
            rep.add(BREAKING, where, "nullable to NOT NULL",
                    "Backfill every NULL. Add the constraint NOT VALID, then validate it.")
        if not old.get("nullable", True) and new.get("nullable", True):
            rep.add(POTENTIAL, where, "NOT NULL to nullable", "Readers may now see NULL. Update consumers first.")
        if not old.get("unique") and new.get("unique"):
            rep.add(POTENTIAL, where, "unique constraint added",
                    "Find duplicates first. Build the index concurrently.")
        if old.get("unique") and not new.get("unique"):
            rep.add(POTENTIAL, where, "unique constraint removed", "Code that relies on uniqueness can break.")
        if old.get("primary_key") != new.get("primary_key"):
            rep.add(BREAKING, where, "primary key membership changed", "Treat as a table rebuild. Use expand and contract.")
        if old.get("default") != new.get("default"):
            rep.add(POTENTIAL, where, f"default changed {old.get('default')!r} to {new.get('default')!r}",
                    "Writers that omit the column get a different value.")


def diff_named(rep, table, kind, before, after):
    for name in before.keys() - after.keys():
        rep.add(POTENTIAL, f"{table}.{name}", f"{kind} removed", "Check query plans and integrity assumptions.")
    for name in after.keys() - before.keys():
        level = POTENTIAL if kind == "foreign key" else COMPATIBLE
        fix = "Validate existing rows first. Add NOT VALID, then VALIDATE." if level == POTENTIAL else ""
        rep.add(level, f"{table}.{name}", f"{kind} added", fix)
    for name in before.keys() & after.keys():
        if before[name] != after[name]:
            rep.add(POTENTIAL, f"{table}.{name}", f"{kind} definition changed", "Rebuild online and compare plans.")


def check_database(before, after):
    rep = Report()
    bt, at = before.get("tables", {}), after.get("tables", {})
    for table in bt.keys() - at.keys():
        rep.add(BREAKING, table, "table removed", "Stop all access, keep a snapshot, drop in the contract phase.")
    for table in at.keys() - bt.keys():
        rep.add(COMPATIBLE, table, "table added", "")
    for table in bt.keys() & at.keys():
        diff_columns(rep, table, bt[table].get("columns", {}), at[table].get("columns", {}))
        diff_named(rep, table, "foreign key", bt[table].get("foreign_keys", {}), at[table].get("foreign_keys", {}))
        diff_named(rep, table, "index", bt[table].get("indexes", {}), at[table].get("indexes", {}))
    return rep


def check_api(before, after):
    rep = Report()
    be, ae = before.get("endpoints", {}), after.get("endpoints", {})
    for ep in be.keys() - ae.keys():
        rep.add(BREAKING, ep, "endpoint removed", "Keep it behind the facade until traffic is zero. Announce a sunset date.")
    for ep in ae.keys() - be.keys():
        rep.add(COMPATIBLE, ep, "endpoint added", "")
    for ep in be.keys() & ae.keys():
        old_p, new_p = be[ep].get("params", {}), ae[ep].get("params", {})
        for name in new_p.keys() - old_p.keys():
            if new_p[name].get("required"):
                rep.add(BREAKING, f"{ep} param {name}", "required parameter added", "Make it optional with a default.")
            else:
                rep.add(COMPATIBLE, f"{ep} param {name}", "optional parameter added", "")
        for name in old_p.keys() - new_p.keys():
            rep.add(POTENTIAL, f"{ep} param {name}", "parameter removed", "Clients that send it may now get a 400. Ignore it instead.")
        for name in old_p.keys() & new_p.keys():
            if old_p[name].get("type") != new_p[name].get("type"):
                rep.add(BREAKING, f"{ep} param {name}", "parameter type changed", "Accept both types during the transition.")
            if not old_p[name].get("required") and new_p[name].get("required"):
                rep.add(BREAKING, f"{ep} param {name}", "parameter became required", "Keep it optional.")
        old_r, new_r = be[ep].get("response", {}), ae[ep].get("response", {})
        for name in old_r.keys() - new_r.keys():
            rep.add(BREAKING, f"{ep} response {name}", "response field removed", "Keep the field until no client reads it.")
        for name in new_r.keys() - old_r.keys():
            rep.add(COMPATIBLE, f"{ep} response {name}", "response field added", "")
        for name in old_r.keys() & new_r.keys():
            if old_r[name] != new_r[name]:
                rep.add(BREAKING, f"{ep} response {name}", f"response type changed {old_r[name]} to {new_r[name]}",
                        "Add a new field with the new type. Retire the old one later.")
    return rep


def render_markdown(rep):
    lines = [f"# Compatibility report: {rep.overall()}", "",
             f"Breaking: {rep.count(BREAKING)}. Potentially breaking: {rep.count(POTENTIAL)}. "
             f"Compatible: {rep.count(COMPATIBLE)}.", ""]
    for level in (BREAKING, POTENTIAL, COMPATIBLE):
        items = [i for i in rep.issues if i["level"] == level]
        if items:
            lines.append(f"## {level}")
            lines += [f"- `{i['where']}`: {i['change']}" + (f" Fix: {i['mitigation']}" if i["mitigation"] else "") for i in items]
            lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--before", required=True)
    ap.add_argument("--after", required=True)
    ap.add_argument("--type", choices=["database", "api"], required=True)
    ap.add_argument("--format", choices=["json", "md"], default="json")
    ap.add_argument("-o", "--output")
    args = ap.parse_args()
    with open(args.before, encoding="utf-8") as f:
        before = json.load(f)
    with open(args.after, encoding="utf-8") as f:
        after = json.load(f)
    rep = (check_database if args.type == "database" else check_api)(before, after)
    if args.format == "json":
        text = json.dumps({"overall_compatibility": rep.overall(),
                           "breaking_changes_count": rep.count(BREAKING),
                           "potentially_breaking_count": rep.count(POTENTIAL),
                           "issues": rep.issues}, indent=2) + "\n"
    else:
        text = render_markdown(rep)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
    else:
        sys.stdout.write(text)
    sys.exit(EXIT[rep.overall()])


if __name__ == "__main__":
    main()
