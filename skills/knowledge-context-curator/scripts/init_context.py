#!/usr/bin/env python3
"""
init_context.py - Bootstrap a context repository in a project.

Creates the directory layout, drops in templates for SCHEMA.md, index.md, log.md,
a starter page template, and a context-pack template. Idempotent: re-running will
not clobber existing files.

The context root directory name is configurable via --context-dir. The default is
`context`, but a project may host several roots side by side (for example
`context-core`, `context-product`, `context-customer`). Run this script once per
root you want to create.

Usage:
    python init_context.py <project-root> [--context-dir <name>]

Examples:
    python init_context.py .
    python init_context.py . --context-dir context-core
    python init_context.py C:\\work\\project --context-dir knowledge
"""

import argparse
import sys
from datetime import date
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = SKILL_ROOT / "assets"

SUBDIRS = ["raw", "raw/assets", "indexes", "sources", "entities", "concepts", "synthesis", "packs"]


def copy_template(src: Path, dst: Path, substitutions: dict | None = None) -> bool:
    """Copy a template file to dst. Returns True if file was created."""
    if dst.exists():
        return False
    text = src.read_text(encoding="utf-8")
    if substitutions:
        for key, value in substitutions.items():
            text = text.replace(key, value)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(text, encoding="utf-8")
    return True


def init_context(project_root: Path, context_dir: str) -> None:
    project_root = project_root.resolve()
    if not project_root.exists():
        print(f"Error: project root does not exist: {project_root}", file=sys.stderr)
        sys.exit(1)

    context_root = project_root / context_dir

    print(f"Initializing context repository in: {project_root}")
    print(f"  Context directory: {context_root}")
    print()

    created: list[str] = []
    skipped: list[str] = []

    for subdir in SUBDIRS:
        directory = context_root / subdir
        label = f"{context_dir}/{subdir}/"
        if not directory.exists():
            directory.mkdir(parents=True)
            created.append(label)
        else:
            skipped.append(label)

    today = date.today().isoformat()
    substitutions = {"YYYY-MM-DD": today, "{{CONTEXT_ROOT}}": context_dir}
    template_map = [
        ("SCHEMA.template.md", context_root / "SCHEMA.md"),
        ("index.template.md", context_root / "index.md"),
        ("log.template.md", context_root / "log.md"),
        ("page.template.md", context_root / ".page-template.md"),
        ("context-pack.template.md", context_root / ".context-pack-template.md"),
    ]

    for src_name, dst in template_map:
        src = TEMPLATES / src_name
        if not src.exists():
            print(f"Warning: template missing: {src}", file=sys.stderr)
            continue
        if copy_template(src, dst, substitutions):
            created.append(str(dst.relative_to(project_root)))
        else:
            skipped.append(str(dst.relative_to(project_root)))

    log_path = context_root / "log.md"
    if log_path.exists():
        text = log_path.read_text(encoding="utf-8")
        init_line = f"## [{today}] initialize | Created context repository"
        if init_line not in text:
            with log_path.open("a", encoding="utf-8") as handle:
                handle.write(f"\n{init_line}\n")

    if created:
        print("Created:")
        for path in created:
            print(f"  + {path}")
    if skipped:
        print("Already existed (skipped):")
        for path in skipped:
            print(f"  = {path}")

    print()
    print("Next steps:")
    print(f"  1. Read {context_dir}/SCHEMA.md and keep the defaults unless the domain needs a different rule.")
    print(f"  2. Place the first source under {context_dir}/raw/.")
    print("  3. Ingest the source; agent-managed indexes and task context can evolve as patterns appear.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("project_root", type=Path, help="Project root directory.")
    parser.add_argument("--context-dir", default="context", help="Context root directory name (default: context). Use any name; run once per root for multi-root projects.")
    args = parser.parse_args()
    init_context(args.project_root, args.context_dir)


if __name__ == "__main__":
    main()