#!/usr/bin/env python3
"""
Design UI System Advisor — CLI search interface.

Usage:
    # Generate a complete design system (always run first)
    python3 search.py "<query>" --design-system [-p "Project Name"] [-f markdown]

    # Search a specific knowledge domain
    python3 search.py "<query>" --domain <domain> [-n <count>]

    # Search stack-specific guidelines
    python3 search.py "<query>" --stack <stack>

Domains: style, prompt, color, chart, landing, product, ux,
         typography, icons, react, web

Stacks: html-tailwind, react, nextjs, vue, nuxtjs, nuxt-ui,
        svelte, swiftui, react-native, flutter, shadcn
"""

import argparse
import json
import sys

from core import AVAILABLE_STACKS, DOMAIN_CONFIG, MAX_RESULTS, search, search_stack
from design_system import generate_design_system


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

def _fmt_result(result: dict) -> str:
    if "error" in result:
        return f"Error: {result['error']}"

    lines: list[str] = []

    if result.get("stack"):
        lines.append("## Design UI System Advisor — Stack Guidelines")
        lines.append(f"**Stack:** {result['stack']} | **Query:** {result['query']}")
    else:
        lines.append("## Design UI System Advisor — Search Results")
        lines.append(f"**Domain:** {result['domain']} | **Query:** {result['query']}")

    lines.append(f"**Source:** {result['file']} | **Found:** {result['count']} results\n")

    for i, row in enumerate(result["results"], 1):
        lines.append(f"### Result {i}")
        for key, value in row.items():
            v = str(value)
            if len(v) > 300:
                v = v[:300] + "..."
            lines.append(f"- **{key}:** {v}")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="search.py",
        description="Design UI System Advisor — searchable UI/UX knowledge base",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("query", help="Search query or product description")

    # Search mode (mutually exclusive)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--domain", "-d",
        choices=list(DOMAIN_CONFIG.keys()),
        metavar="DOMAIN",
        help=f"Domain to search: {', '.join(DOMAIN_CONFIG.keys())}",
    )
    mode.add_argument(
        "--stack", "-s",
        choices=AVAILABLE_STACKS,
        metavar="STACK",
        help=f"Stack guidelines: {', '.join(AVAILABLE_STACKS)}",
    )
    mode.add_argument(
        "--design-system", "-ds",
        action="store_true",
        help="Generate full design system recommendation (run first)",
    )

    # Options
    parser.add_argument(
        "--max-results", "-n",
        type=int,
        default=MAX_RESULTS,
        help=f"Max results returned (default: {MAX_RESULTS})",
    )
    parser.add_argument(
        "--project-name", "-p",
        metavar="NAME",
        help="Project name for design system output header",
    )
    parser.add_argument(
        "--format", "-f",
        choices=["ascii", "markdown"],
        default="ascii",
        help="Output format for design system (default: ascii)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw JSON (domain/stack search only)",
    )
    return parser


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    if args.design_system:
        print(generate_design_system(args.query, args.project_name, args.format))
        return

    if args.stack:
        result = search_stack(args.query, args.stack, args.max_results)
    else:
        result = search(args.query, args.domain, args.max_results)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(_fmt_result(result))


if __name__ == "__main__":
    main()
