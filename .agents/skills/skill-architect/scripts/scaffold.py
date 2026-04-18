#!/usr/bin/env python3
"""Scaffold a new skill directory with boilerplate structure.

Creates the directory structure, starter SKILL.md with frontmatter,
and optional resource directories based on the archetype.

Usage:
    python scaffold.py <skill-name> --archetype <type> [--output-dir <path>]
    python scaffold.py <skill-name> --archetype technical-execution --refs api-patterns,testing
    python scaffold.py <skill-name> --archetype content-writing --with-agents --with-scripts

Archetypes: technical-execution, architecture-design, specification-contract,
            workflow-conversational, content-writing, research-analysis
"""

import argparse
import sys
from pathlib import Path


# --- Archetype Defaults ---

ARCHETYPES = {
    "technical-execution": {
        "role": "specialist",
        "scope": "implementation",
        "output-format": "code",
        "workflow": [
            "Analyze requirements and constraints",
            "Design solution architecture",
            "Implement core functionality",
            "Add error handling and edge cases",
            "Validate and test",
        ],
        "ref_topics": ["patterns", "conventions", "testing"],
    },
    "architecture-design": {
        "role": "architect",
        "scope": "design",
        "output-format": "architecture",
        "workflow": [
            "Discover requirements and constraints",
            "Design component architecture",
            "Address security and resilience",
            "Plan scaling and cost strategy",
            "Define deployment approach",
        ],
        "ref_topics": ["platform-services", "security-patterns", "scaling"],
    },
    "specification-contract": {
        "role": "architect",
        "scope": "system-design",
        "output-format": "specification",
        "workflow": [
            "Analyze domain and entities",
            "Model resources and relationships",
            "Design contract interface",
            "Plan versioning and evolution",
            "Document specification",
        ],
        "ref_topics": ["protocol-standards", "versioning", "error-handling"],
    },
    "workflow-conversational": {
        "role": "expert",
        "scope": "analysis",
        "output-format": "document",
        "workflow": [
            "Discover scope and stakeholders",
            "Interview for requirements",
            "Document findings",
            "Validate with stakeholders",
            "Iterate and refine",
        ],
        "ref_topics": ["interview-frameworks", "templates", "checklists"],
    },
    "content-writing": {
        "role": "expert",
        "scope": "creation",
        "output-format": "content",
        "workflow": [
            "Understand the brief and goals",
            "Research audience and context",
            "Draft initial content",
            "Refine tone and structure",
            "Finalize deliverable",
        ],
        "ref_topics": ["tone-guide", "audience-profiles", "format-templates"],
    },
    "research-analysis": {
        "role": "analyst",
        "scope": "analysis",
        "output-format": "report",
        "workflow": [
            "Frame the research question",
            "Gather data and sources",
            "Analyze findings",
            "Synthesize insights",
            "Produce recommendations",
        ],
        "ref_topics": ["analysis-frameworks", "data-sources", "reporting"],
    },
}


def generate_skill_md(name: str, archetype_key: str, ref_names: list[str]) -> str:
    """Generate starter SKILL.md content."""
    arch = ARCHETYPES[archetype_key]

    # Build workflow steps
    workflow_lines = []
    for i, step in enumerate(arch["workflow"], 1):
        workflow_lines.append(f"{i}. **{step}**")

    # Build reference table
    ref_table_lines = []
    for ref in ref_names:
        ref_table_lines.append(
            f"| {ref.replace('-', ' ').title()} "
            f"| `references/{ref}.md` "
            f"| [Describe when to load this reference] |"
        )

    # Build MUST DO / MUST NOT DO
    must_do = [
        "- [Add specific, actionable requirements]",
        "- [Add more requirements as needed]",
    ]
    must_not = [
        "- [Name a specific anti-pattern to avoid]",
        "- [Name another anti-pattern]",
    ]

    return f"""---
name: {name}
description: '[WHAT this skill does]. Use when [WHEN to trigger]. Use this skill whenever the user mentions [keywords], even if they don''t explicitly ask for [{name}].'
license: MIT
metadata:
  version: "1.0.0"
  domain: [domain]
  triggers: [keyword1], [keyword2], [keyword3]
  role: {arch['role']}
  scope: {arch['scope']}
  output-format: {arch['output-format']}
  related-skills: [related-skill-1], [related-skill-2]
---

# {name.replace('-', ' ').title()}

[One-sentence summary of what this skill does and why it exists.]

## Role Definition

You are a senior [title] with [N]+ years of experience in [domain]. You specialize in [primary area], [secondary area], and [tertiary area]. You [key differentiator].

## Workflow

{chr(10).join(workflow_lines)}

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
{chr(10).join(ref_table_lines)}

## Constraints

### MUST DO
{chr(10).join(must_do)}

### MUST NOT DO
{chr(10).join(must_not)}

## Output Templates

[Define the expected output structure tied to `{arch['output-format']}` format]

## Knowledge Reference

[technology1], [technology2], [pattern1], [standard1], [framework1]
"""


def scaffold_skill(
    name: str,
    archetype_key: str,
    output_dir: Path,
    ref_names: list[str] | None = None,
    with_agents: bool = False,
    with_scripts: bool = False,
) -> Path:
    """Create the skill directory structure."""
    arch = ARCHETYPES[archetype_key]

    if ref_names is None:
        ref_names = arch["ref_topics"]

    skill_dir = output_dir / name
    skill_dir.mkdir(parents=True, exist_ok=True)

    # Create SKILL.md
    skill_md = generate_skill_md(name, archetype_key, ref_names)
    (skill_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")

    # Create references/
    refs_dir = skill_dir / "references"
    refs_dir.mkdir(exist_ok=True)
    for ref in ref_names:
        ref_file = refs_dir / f"{ref}.md"
        ref_file.write_text(
            f"# {ref.replace('-', ' ').title()}\n\n"
            f"[Add {ref.replace('-', ' ')} reference content here]\n",
            encoding="utf-8",
        )

    # Create agents/ if requested
    if with_agents:
        agents_dir = skill_dir / "agents"
        agents_dir.mkdir(exist_ok=True)
        (agents_dir / "example-agent.md").write_text(
            "# Example Agent\n\n"
            "[Define a focused sub-agent role with inputs, process, and output format]\n\n"
            "## Role\n\n[One sentence role description]\n\n"
            "## Inputs\n\n- **input_1**: [description]\n\n"
            "## Process\n\n### Step 1: [First step]\n\n[Details]\n\n"
            "## Output Format\n\n[Expected output structure]\n",
            encoding="utf-8",
        )

    # Create scripts/ if requested
    if with_scripts:
        scripts_dir = skill_dir / "scripts"
        scripts_dir.mkdir(exist_ok=True)
        (scripts_dir / "__init__.py").write_text("", encoding="utf-8")
        (scripts_dir / "example.py").write_text(
            '#!/usr/bin/env python3\n'
            '"""Example script — handle deterministic operations here.\n\n'
            "Scripts handle what must be deterministic (validation, data transformation,\n"
            "aggregation). The SKILL.md body handles what requires judgment.\n"
            '"""\n\n'
            "import sys\n\n\n"
            "def main():\n"
            '    print("Replace with actual implementation")\n\n\n'
            'if __name__ == "__main__":\n'
            "    main()\n",
            encoding="utf-8",
        )

    return skill_dir


def main():
    parser = argparse.ArgumentParser(
        description="Scaffold a new Agent Skill directory"
    )
    parser.add_argument("name", help="Skill name (lowercase-with-hyphens)")
    parser.add_argument(
        "--archetype",
        required=True,
        choices=list(ARCHETYPES.keys()),
        help="Skill archetype",
    )
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Parent directory for the skill folder (default: current directory)",
    )
    parser.add_argument(
        "--refs",
        default=None,
        help="Comma-separated reference file names (default: archetype defaults)",
    )
    parser.add_argument(
        "--with-agents",
        action="store_true",
        help="Include an agents/ directory with a starter template",
    )
    parser.add_argument(
        "--with-scripts",
        action="store_true",
        help="Include a scripts/ directory with a starter template",
    )

    args = parser.parse_args()

    # Validate name
    name = args.name.strip()
    if not name or not all(c.isalnum() or c == "-" for c in name):
        print(f"Error: Invalid skill name '{name}'. Use lowercase-with-hyphens.", file=sys.stderr)
        sys.exit(1)
    if name != name.lower():
        print(f"Error: Skill name must be lowercase. Got '{name}'.", file=sys.stderr)
        sys.exit(1)

    output_dir = Path(args.output_dir).resolve()
    ref_names = [r.strip() for r in args.refs.split(",")] if args.refs else None

    skill_dir = scaffold_skill(
        name=name,
        archetype_key=args.archetype,
        output_dir=output_dir,
        ref_names=ref_names,
        with_agents=args.with_agents,
        with_scripts=args.with_scripts,
    )

    print(f"Scaffolded skill at: {skill_dir}")

    # Print tree
    for p in sorted(skill_dir.rglob("*")):
        rel = p.relative_to(skill_dir)
        indent = "  " * len(rel.parts)
        name_display = f"{rel.name}/" if p.is_dir() else rel.name
        print(f"{indent}{name_display}")


if __name__ == "__main__":
    main()
