#!/usr/bin/env bash
# repo-reorganize.sh — Generate and optionally execute a reorganization plan.
#
# Usage: ./repo-reorganize.sh [OPTIONS]
# See ./repo-reorganize.sh --help for full options.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# shellcheck source=_lib/validators.sh
source "$SCRIPT_DIR/_lib/validators.sh"

# ── Defaults ──────────────────────────────────────────────────────────────────
repo_root="$(pwd)"
execute=false
approve_all=false
rules_path="$SCRIPT_DIR/../references/path-rules.json"

# ── Usage ─────────────────────────────────────────────────────────────────────
usage() {
    cat <<EOF
Usage: $(basename "$0") [OPTIONS]

Generate and optionally execute a reorganization plan for an existing repository.

OPTIONS:
  -r, --repo-root <path>    Repository root (default: current directory)
  -e, --execute             Execute the plan (default: plan only)
  -a, --approve-all         Skip per-step confirmations (requires --execute)
  -h, --help                Show this help message

EXAMPLES:
  $(basename "$0") -r /path/to/repo          # Plan only (safe)
  $(basename "$0") --execute                 # Execute with confirmation
  $(basename "$0") --execute --approve-all   # Execute unattended
EOF
}

# ── Argument parsing ──────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
    case "$1" in
        -r|--repo-root)   repo_root="$2"; shift 2 ;;
        -e|--execute)     execute=true; shift ;;
        -a|--approve-all) approve_all=true; shift ;;
        -h|--help)        usage; exit 0 ;;
        *) echo "Unknown option: $1" >&2; usage; exit 1 ;;
    esac
done

# ── Header ────────────────────────────────────────────────────────────────────
echo "Repository Reorganizer"
echo "======================"
echo "Root : $repo_root"
if [[ "$execute" == false ]]; then
    echo "[PLAN ONLY — pass --execute to make changes]"
fi
echo ""

# ── Check jq ──────────────────────────────────────────────────────────────────
if ! command -v jq &>/dev/null; then
    echo "Error: jq is required but not installed." >&2
    echo "  macOS:         brew install jq" >&2
    echo "  Ubuntu/Debian: sudo apt-get install jq" >&2
    echo "  Alpine:        apk add jq" >&2
    exit 1
fi

# ── Known rename mappings ─────────────────────────────────────────────────────
# Returns the standard name for a known non-standard name, or empty string.
get_standard_name() {
    case "$1" in
        infra) echo "infrastructure" ;;
        doc)   echo "docs" ;;
        *)     echo "" ;;
    esac
}

# ── Collect findings ──────────────────────────────────────────────────────────
# Indexed arrays for automated steps
auto_types=()
auto_descs=()
auto_sources=()
auto_targets=()

# Manual steps (plain strings)
manual_steps=()

# Check for missing starter-shell files
project_name="$(basename "$(cd "$repo_root" && pwd)")"
while IFS= read -r rel_path; do
    rel_path="${rel_path//\{project-name\}/$project_name}"
    full_path="$repo_root/$rel_path"
    if [[ ! -f "$full_path" ]]; then
        auto_types+=("scaffold")
        auto_descs+=("Create missing starter-shell file: $rel_path")
        auto_sources+=("")
        auto_targets+=("$rel_path")
    fi
done < <(jq -r '.starter_shell.paths[]' "$rules_path")

# Check top-level directories for non-standard names
while IFS= read -r item_path; do
    dir_name="$(basename "$item_path")"
    standard_name="$(get_standard_name "$dir_name")"

    if [[ -n "$standard_name" ]]; then
        auto_types+=("rename")
        auto_descs+=("Rename '$dir_name' to '$standard_name'")
        auto_sources+=("$dir_name")
        auto_targets+=("$standard_name")
    elif jq -e ".non_standard_paths[\"/\"] // empty" "$rules_path" &>/dev/null; then
        # Check if the slash-prefixed name is in non_standard_paths
        if action="$(jq -r --arg k "/$dir_name" '.non_standard_paths[$k].action // empty' "$rules_path")" && [[ -n "$action" ]]; then
            manual_steps+=("/$dir_name [non_standard]: $action")
        fi
    fi
done < <(find "$repo_root" -maxdepth 1 -mindepth 1 -type d -not -name '.*' | sort)

# ── Print plan ────────────────────────────────────────────────────────────────
echo "Automated steps (${#auto_types[@]}):"
if [[ ${#auto_types[@]} -eq 0 ]]; then
    echo "  (none)"
else
    for i in "${!auto_types[@]}"; do
        type_upper="$(echo "${auto_types[$i]}" | tr '[:lower:]' '[:upper:]')"
        echo "  [$((i+1))] [$type_upper] ${auto_descs[$i]}"
    done
fi

echo ""
echo "Manual steps (${#manual_steps[@]}):"
if [[ ${#manual_steps[@]} -eq 0 ]]; then
    echo "  (none)"
else
    for step in "${manual_steps[@]}"; do
        echo "  - $step"
    done
fi

if [[ "$execute" == false ]]; then
    echo ""
    echo "Plan complete. Pass --execute to apply automated steps."
    exit 0
fi

# ── Execute automated steps ───────────────────────────────────────────────────
echo ""
echo "Executing automated steps..."

succeeded=0
failed=0

for i in "${!auto_types[@]}"; do
    step_num=$((i + 1))
    total=${#auto_types[@]}
    echo ""
    echo "Step [$step_num/$total]: ${auto_descs[$i]}"

    if [[ "$approve_all" == false ]]; then
        read -r -p "  Apply this step? [y/N] " confirm
        if [[ ! "$confirm" =~ ^[Yy] ]]; then
            echo "  Skipped."
            continue
        fi
    fi

    if [[ "${auto_types[$i]}" == "scaffold" ]]; then
        if bash "$SCRIPT_DIR/repo-scaffold.sh" -t "$repo_root"; then
            succeeded=$((succeeded + 1))
        else
            echo "  X  scaffold failed"
            failed=$((failed + 1))
        fi
    elif [[ "${auto_types[$i]}" == "rename" ]]; then
        source_dir="$repo_root/${auto_sources[$i]}"
        target_dir="$repo_root/${auto_targets[$i]}"
        if [[ -d "$source_dir" ]]; then
            if mv "$source_dir" "$target_dir"; then
                echo "  OK Moved: ${auto_sources[$i]} -> ${auto_targets[$i]}"
                succeeded=$((succeeded + 1))
            else
                echo "  X  mv failed"
                failed=$((failed + 1))
            fi
        else
            echo "  -- Source not found: ${auto_sources[$i]}"
        fi
    fi
done

echo ""
echo "Completed: $succeeded succeeded, $failed failed"

if [[ ${#manual_steps[@]} -gt 0 ]]; then
    echo ""
    echo "Manual steps still require attention (${#manual_steps[@]} items above)."
fi

if [[ $failed -gt 0 ]]; then exit 1; fi
exit 0
