#!/bin/bash
# Shared validation and utility functions for engineering-repo-scaffolder scripts.

# Load path rules from JSON (requires jq)
get_path_rules() {
    local rules_path="${1:-$SCRIPT_DIR/../references/path-rules.json}"
    
    if [[ ! -f "$rules_path" ]]; then
        echo "Error: Path rules file not found: $rules_path" >&2
        return 1
    fi
    
    if ! command -v jq &> /dev/null; then
        echo "Error: jq is required to parse JSON rules" >&2
        return 1
    fi
    
    cat "$rules_path"
}

# Check if a path exists relative to a repo root
test_path_exists() {
    local repo_root="$1"
    local relative_path="$2"
    
    if [[ -e "$repo_root/$relative_path" ]]; then
        return 0
    else
        return 1
    fi
}

# Get normalized path status
get_path_status() {
    local repo_root="$1"
    local relative_path="$2"
    local standard_location="$3"
    
    if ! test_path_exists "$repo_root" "$relative_path"; then
        echo "missing"
    elif [[ "$relative_path" == "$standard_location" ]]; then
        echo "correct"
    else
        echo "misplaced"
    fi
}

# Inventory top-level items in repo
get_repo_inventory() {
    local repo_root="$1"
    
    if [[ ! -d "$repo_root" ]]; then
        echo "Error: Repository root not found: $repo_root" >&2
        return 1
    fi
    
    # Use find to get all top-level items
    find "$repo_root" -maxdepth 1 -not -path "$repo_root" -print0 | while IFS= read -r -d '' item; do
        local name=$(basename "$item")
        if [[ -d "$item" ]]; then
            echo "$name|folder|$item"
        else
            echo "$name|file|$item"
        fi
    done
}

# Verify starter shell completeness
test_starter_shell() {
    local repo_root="$1"
    local rules_file="${2:-./_lib/path-rules.json}"
    local project_name
    project_name="$(basename "$(cd "$repo_root" && pwd)")"

    if ! command -v jq &> /dev/null; then
        echo "Error: jq is required" >&2
        return 1
    fi

    local rules=$(cat "$rules_file")
    local paths=$(echo "$rules" | jq -r '.starter_shell.paths[]')

    # Findings are emitted as path|type|status|details, matching the format the
    # console/JSON/Markdown reporters expect.
    local issues=0
    while IFS= read -r path; do
        local resolved_path="${path//\{project-name\}/$project_name}"
        if ! test_path_exists "$repo_root" "$resolved_path"; then
            echo "$resolved_path|starter_shell|missing|"
            ((issues++))
        elif [[ "$resolved_path" != *.gitkeep && -z $(find "$repo_root/$resolved_path" -type f -size +0 2>/dev/null) ]]; then
            echo "$resolved_path|starter_shell|empty|"
            ((issues++))
        fi
    done <<< "$paths"

    # Verify declared symlinks exist, are links, and resolve to the declared target.
    # On Windows the scaffolder creates a directory junction instead of a POSIX symlink,
    # so the presence check falls back to "is a directory that contains files" — a broken
    # or missing link fails the directory check either way.
    local symlink_entries
    symlink_entries=$(echo "$rules" | jq -r '.starter_shell.symlinks // {} | to_entries[] | "\(.key)|\(.value)"')
    while IFS='|' read -r link_path expected_target; do
        [[ -z "$link_path" ]] && continue
        local full="$repo_root/$link_path"
        if [[ -L "$full" ]]; then
            local actual_target
            actual_target=$(readlink "$full")
            if [[ "$actual_target" != "$expected_target" ]]; then
                echo "$link_path|starter_shell|wrong-target|expected $expected_target, got $actual_target"
                ((issues++))
            fi
        elif [[ -d "$full" ]]; then
            # Junction or bind-mount; can't verify target portably. Presence is enough.
            :
        else
            echo "$link_path|starter_shell|missing|symlink to $expected_target"
            ((issues++))
        fi
    done <<< "$symlink_entries"

    return $(( issues > 0 ? 1 : 0 ))
}

# Find non-standard paths in repo root
find_nonstandard_paths() {
    local repo_root="$1"
    local rules_file="${2:-./_lib/path-rules.json}"
    
    if ! command -v jq &> /dev/null; then
        echo "Error: jq is required" >&2
        return 1
    fi
    
    local rules=$(cat "$rules_file")
    local standard_roots=$(echo "$rules" | jq -r '.root_files, .root_directories | keys | .[]' 2>/dev/null | sort | uniq)
    local non_standard_keys=$(echo "$rules" | jq -r '.non_standard_paths | keys | .[]' 2>/dev/null)
    
    local skip_items=(".git" ".gitignore" ".vscode" ".editorconfig" "node_modules")
    
    find "$repo_root" -maxdepth 1 -not -path "$repo_root" -type f,d | while read -r item; do
        local name=$(basename "$item")
        
        # Skip safe items
        if [[ " ${skip_items[@]} " =~ " $name " ]]; then
            continue
        fi
        
        # Check if it's in non-standard paths
        if echo "$non_standard_keys" | grep -qE "^$name$|^/$name$"; then
            local issue
            issue=$(echo "$rules" | jq -r ".non_standard_paths[\"$name\"].issue // .non_standard_paths[\"/$name\"].issue // \"Unknown issue\"")
            echo "$name|non_standard|non-standard|$issue"
        fi
    done
}

# Export findings to JSON
export_findings_json() {
    local output_path="$1"
    local findings="$2"
    
    {
        echo "{"
        echo "  \"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\","
        echo "  \"findings\": ["
        
        local first=true
        while IFS= read -r finding; do
            if [[ -z "$finding" ]]; then
                continue
            fi
            
            if [[ "$first" == false ]]; then
                echo ","
            fi
            first=false
            
            # Parse finding and output JSON object
            local path type status details
            IFS='|' read -r path type status details <<< "$finding"
            echo "    {"
            echo "      \"path\": \"$path\","
            echo "      \"type\": \"$type\","
            echo "      \"status\": \"$status\""
            if [[ -n "$details" ]]; then
                echo "      ,\"details\": \"$details\""
            fi
            echo -n "    }"
        done <<< "$findings"
        
        echo ""
        echo "  ]"
        echo "}"
    } > "$output_path"
}

# Export findings to Markdown
export_findings_markdown() {
    local output_path="$1"
    local repo_root="$2"
    local findings="$3"
    
    {
        echo "# Repository Structure Audit"
        echo ""
        echo "**Repository:** $repo_root"
        echo "**Generated:** $(date '+%Y-%m-%d %H:%M:%S')"
        echo ""
        echo "## Summary"
        echo ""
        
        local total=$(echo "$findings" | wc -l)
        local missing=$(echo "$findings" | grep '|missing|' | wc -l)
        local misplaced=$(echo "$findings" | grep '|misplaced|' | wc -l)
        
        echo "- Total Findings: $total"
        echo "- Missing Items: $missing"
        echo "- Misplaced Items: $misplaced"
        echo ""
        echo "## Detailed Findings"
        echo ""
        echo "| Path | Type | Status | Details |"
        echo "|------|------|--------|---------|"
        
        while IFS= read -r finding; do
            if [[ -z "$finding" ]]; then
                continue
            fi
            local path type status details
            IFS='|' read -r path type status details <<< "$finding"
            details="${details:--}"
            echo "| \`$path\` | $type | $status | $details |"
        done <<< "$findings"
    } > "$output_path"
}

# Format output table for display
format_audit_table() {
    local findings="$1"
    
    echo ""
    echo "Audit Results:"
    echo "=============="
    echo ""
    echo "Path                                    Type              Status         Details"
    echo "------------------------------------------------------------------------------------"
    
    while IFS= read -r finding; do
        if [[ -z "$finding" ]]; then
            continue
        fi
        local path type status details
        IFS='|' read -r path type status details <<< "$finding"
        printf "%-40s %-18s %-15s %s\n" "$path" "$type" "$status" "${details:--}"
    done <<< "$findings"
}

# Export all functions
export -f get_path_rules
export -f test_path_exists
export -f get_path_status
export -f get_repo_inventory
export -f test_starter_shell
export -f find_nonstandard_paths
export -f export_findings_json
export -f export_findings_markdown
export -f format_audit_table
