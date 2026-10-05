#!/bin/bash
# Audit a repository against the project structure standard.
#
# Usage: ./repo-audit.sh [OPTIONS]
#
# Options:
#   -r, --repo-root DIR          Repository root to audit (default: current directory)
#   -f, --format FORMAT          Output format: console, json, markdown, all (default: console)
#   -o, --output-path PATH       Base path for reports (default: ./audit-report)
#   -d, --dry-run                Show what would be audited without writing files
#   -h, --help                   Show this help message

set -euo pipefail

# Script configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="${REPO_ROOT:-.}"
OUTPUT_FORMAT="console"
OUTPUT_PATH="./audit-report"
DRY_RUN=false

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
GRAY='\033[0;37m'
NC='\033[0m' # No Color

# Parse arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -r|--repo-root)
                REPO_ROOT="$2"
                shift 2
                ;;
            -f|--format)
                OUTPUT_FORMAT="$2"
                shift 2
                ;;
            -o|--output-path)
                OUTPUT_PATH="$2"
                shift 2
                ;;
            -d|--dry-run)
                DRY_RUN=true
                shift
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                echo "Unknown option: $1" >&2
                show_help
                exit 1
                ;;
        esac
    done
}

show_help() {
    cat << 'EOF'
Repository Structure Audit

Usage: ./repo-audit.sh [OPTIONS]

Options:
  -r, --repo-root DIR          Repository root to audit (default: current directory)
  -f, --format FORMAT          Output format: console, json, markdown, all (default: console)
  -o, --output-path PATH       Base path for reports (default: ./audit-report)
  -d, --dry-run                Show what would be audited without writing files
  -h, --help                   Show this help message

Examples:
  ./repo-audit.sh -r /path/to/repo -f all
  ./repo-audit.sh --dry-run
  ./repo-audit.sh -o /tmp/audit-results

EOF
}

# Main audit logic
main() {
    parse_args "$@"
    
    # Validate prerequisites
    if ! command -v jq &> /dev/null; then
        echo -e "${RED}Error: jq is required but not installed${NC}" >&2
        echo "Install jq to proceed: https://stedolan.github.io/jq/" >&2
        exit 1
    fi
    
    # Source validators library
    if [[ ! -f "$SCRIPT_DIR/_lib/validators.sh" ]]; then
        echo -e "${RED}Error: validators library not found${NC}" >&2
        exit 1
    fi
    source "$SCRIPT_DIR/_lib/validators.sh"
    
    # Validate repo root
    if [[ ! -d "$REPO_ROOT" ]]; then
        echo -e "${RED}Error: Repository root not found: $REPO_ROOT${NC}" >&2
        exit 1
    fi
    
    # Resolve to absolute path
    REPO_ROOT=$(cd "$REPO_ROOT" && pwd)
    
    echo -e "${CYAN}Repository Structure Audit${NC}"
    echo -e "${CYAN}===========================${NC}"
    echo -e "${GRAY}Repository: $REPO_ROOT${NC}"
    echo ""
    
    # Load rules
    local rules_path="$SCRIPT_DIR/../references/path-rules.json"
    if [[ ! -f "$rules_path" ]]; then
        echo -e "${RED}Error: Path rules file not found${NC}" >&2
        exit 1
    fi
    
    local rules=$(cat "$rules_path")
    local version=$(echo "$rules" | jq -r '.version')
    echo -e "${GREEN}✓ Loaded path rules (v$version)${NC}"
    
    # Initialize findings
    local findings=""
    
    # Phase 1: Check starter shell
    echo ""
    echo -e "${CYAN}Phase 1: Checking Starter Shell${NC}"
    
    local starter_findings=$(test_starter_shell "$REPO_ROOT" "$rules_path" 2>/dev/null || true)
    if [[ -n "$starter_findings" ]]; then
        local count=$(echo "$starter_findings" | wc -l)
        echo -e "${RED}  ✗ Found $count starter shell issues${NC}"
        findings="$findings$starter_findings"
    else
        echo -e "${GREEN}  ✓ Starter shell complete${NC}"
    fi
    
    # Phase 2: Check root directory
    echo ""
    echo -e "${CYAN}Phase 2: Checking Root Directory${NC}"
    
    local non_std=$(find_nonstandard_paths "$REPO_ROOT" "$rules_path" 2>/dev/null || true)
    if [[ -n "$non_std" ]]; then
        local count=$(echo "$non_std" | grep -c . || true)
        if [[ $count -gt 0 ]]; then
            echo -e "${RED}  ✗ Found $count non-standard items${NC}"
            findings="$findings$non_std"
        fi
    else
        echo -e "${GREEN}  ✓ Root directory conforms to standard${NC}"
    fi
    
    # Phase 3: Check .github structure
    echo ""
    echo -e "${CYAN}Phase 3: Checking .github/ Structure${NC}"
    
    if [[ -d "$REPO_ROOT/.github" ]]; then
        echo -e "${GREEN}  ✓ .github/ exists${NC}"
    else
        echo -e "${YELLOW}  ⚠ .github/ directory missing (required in starter shell)${NC}"
        findings="$findings.github|required|missing|Required in starter shell"
    fi
    
    # Phase 4: Check docs structure
    echo ""
    echo -e "${CYAN}Phase 4: Checking /docs Structure${NC}"
    
    if [[ -d "$REPO_ROOT/docs" ]]; then
        echo -e "${GREEN}  ✓ docs/ exists${NC}"
    else
        echo -e "${YELLOW}  ⚠ docs/ directory missing (required in starter shell)${NC}"
        findings="$findings$([ -n "$findings" ] && echo ''; echo)docs|required|missing|Required in starter shell"
    fi
    
    # Summary
    echo ""
    echo -e "${CYAN}Audit Summary${NC}"
    echo -e "${CYAN}=============${NC}"
    
    local total_findings=$(echo "$findings" | grep -c . || true)
    echo -e "${YELLOW}Total findings: $total_findings${NC}"
    
    if [[ $total_findings -gt 0 ]]; then
        echo ""
        echo -e "${YELLOW}Issues:${NC}"
        format_audit_table "$findings"
    fi
    
    # Generate reports
    if [[ "$DRY_RUN" == false ]]; then
        echo ""
        echo -e "${CYAN}Generating reports...${NC}"
        
        mkdir -p "$(dirname "$OUTPUT_PATH")"
        
        if [[ "$OUTPUT_FORMAT" =~ ^(json|all)$ ]]; then
            local json_path="${OUTPUT_PATH}.json"
            export_findings_json "$json_path" "$findings"
            echo -e "${GREEN}  ✓ JSON report: $json_path${NC}"
        fi
        
        if [[ "$OUTPUT_FORMAT" =~ ^(markdown|all)$ ]]; then
            local md_path="${OUTPUT_PATH}.md"
            export_findings_markdown "$md_path" "$REPO_ROOT" "$findings"
            echo -e "${GREEN}  ✓ Markdown report: $md_path${NC}"
        fi
    else
        echo ""
        echo -e "${YELLOW}DRY RUN: Reports would be generated at:${NC}"
        echo -e "${GRAY}  ${OUTPUT_PATH}.json${NC}"
        echo -e "${GRAY}  ${OUTPUT_PATH}.md${NC}"
    fi
    
    # Exit with appropriate code
    if [[ $total_findings -gt 0 ]]; then
        exit 1
    else
        exit 0
    fi
}

main "$@"
