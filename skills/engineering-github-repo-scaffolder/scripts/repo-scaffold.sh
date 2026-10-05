#!/usr/bin/env bash
# repo-scaffold.sh — Create the starter shell for a new repository.
#
# Usage: ./repo-scaffold.sh [OPTIONS]
# See ./repo-scaffold.sh --help for full options.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_DIR="$SCRIPT_DIR/../assets/starter"
COMMON_SKILLS_FILE="$SCRIPT_DIR/../assets/common-skills.txt"

# shellcheck source=_lib/validators.sh
source "$SCRIPT_DIR/_lib/validators.sh"

# ── Defaults ──────────────────────────────────────────────────────────────────
target_path="$(pwd)"
project_name=""
dry_run=false
force=false
install_common_skills=true
skills_source_url="https://github.com/scanady/nexus-skills.git"
skills_source_ref="main"
apply_shared_standards=true
standards_source_url="https://github.com/scanady/ifoundry-development.git"
standards_source_ref="main"

# ── Usage ─────────────────────────────────────────────────────────────────────
usage() {
    cat <<EOF
Usage: $(basename "$0") [OPTIONS]

Scaffold the starter shell for a new repository.

OPTIONS:
  -t, --target-path <path>    Target directory (default: current directory)
  -n, --project-name <name>   Project name for stubs (default: directory name)
  -d, --dry-run               Show what would be created without writing files
  -f, --force                 Overwrite files that already exist
      --update-existing       Update existing scaffold artifacts and common skills
      --skip-common-skills    Do not install common skills into .agents/skills
      --skills-source-url <url>  Git repository for common skills
      --skills-source-ref <ref>  Git branch, tag, or commit for common skills
      --skip-shared-standards    Do not apply shared standards (instructions files, CLAUDE.md)
      --standards-source-url <url>  Git repository holding the shared standards
      --standards-source-ref <ref>  Git branch, tag, or commit for the shared standards
  -h, --help                  Show this help message

EXAMPLES:
  $(basename "$0") -t /path/to/new-repo -n "my-project"
  $(basename "$0") --dry-run
EOF
}

# ── Argument parsing ──────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
    case "$1" in
        -t|--target-path)   target_path="$2"; shift 2 ;;
        -n|--project-name)  project_name="$2"; shift 2 ;;
        -d|--dry-run)       dry_run=true; shift ;;
        -f|--force)         force=true; shift ;;
        --update-existing)  force=true; shift ;;
        --skip-common-skills) install_common_skills=false; shift ;;
        --skills-source-url) skills_source_url="$2"; shift 2 ;;
        --skills-source-ref) skills_source_ref="$2"; shift 2 ;;
        --skip-shared-standards) apply_shared_standards=false; shift ;;
        --standards-source-url) standards_source_url="$2"; shift 2 ;;
        --standards-source-ref) standards_source_ref="$2"; shift 2 ;;
        -h|--help)          usage; exit 0 ;;
        *) echo "Unknown option: $1" >&2; usage; exit 1 ;;
    esac
done

if [[ -z "$project_name" ]]; then
    if [[ -d "$target_path" ]]; then
        project_name="$(basename "$(cd "$target_path" && pwd)")"
    else
        project_name="$(basename "$target_path")"
    fi
fi

# ── Header ────────────────────────────────────────────────────────────────────
echo "Repository Scaffold"
echo "==================="
echo "Target  : $target_path"
echo "Project : $project_name"
if [[ "$dry_run" == true ]]; then echo "[DRY RUN]"; fi
echo ""

# ── Write template helper ────────────────────────────────────────────────────
created=0
skipped=0
warnings=0

write_template() {
    local template_rel_path="$1"
    local rel_path="${template_rel_path//\{project-name\}/$project_name}"
    local full_path="$target_path/$rel_path"
    local template_path="$TEMPLATE_DIR/$template_rel_path"
    local was_existing=false

    [[ -f "$full_path" ]] && was_existing=true

    local content
    if [[ ! -f "$template_path" ]]; then
        echo "  X  Missing template: $template_rel_path" >&2
        return 1
    fi

    content="$(cat "$template_path")"
    content="${content//\{Project Name\}/$project_name}"
    content="${content//\{project-name\}/$project_name}"

    if [[ "$was_existing" == true && "$force" == false ]]; then
        echo "  -- Skip (exists) : $rel_path"
        skipped=$((skipped + 1))
        return 0
    fi

    if [[ "$dry_run" == true ]]; then
        if [[ "$was_existing" == true ]]; then
            echo "  >> Overwrite     : $rel_path"
        else
            echo "  >> Create        : $rel_path"
        fi
        created=$((created + 1))
        return 0
    fi

    local dir
    dir="$(dirname "$full_path")"
    mkdir -p "$dir"

    printf '%s\n' "$content" > "$full_path"

    if [[ "$was_existing" == true ]]; then
        echo "  OK Overwrote     : $rel_path"
    else
        echo "  OK Created       : $rel_path"
    fi
    created=$((created + 1))
}

read_common_skills() {
    while IFS= read -r skill || [[ -n "$skill" ]]; do
        skill="${skill%%#*}"
        skill="$(printf '%s' "$skill" | xargs)"
        [[ -z "$skill" ]] && continue
        printf '%s\n' "$skill"
    done < "$COMMON_SKILLS_FILE"
}

install_common_skill_set() {
    if [[ "$install_common_skills" == false ]]; then
        echo "  -- Skip common skills"
        return 0
    fi

    if [[ ! -f "$COMMON_SKILLS_FILE" ]]; then
        echo "  !! Common skills list missing: $COMMON_SKILLS_FILE" >&2
        warnings=$((warnings + 1))
        return 0
    fi

    local skills=()
    while IFS= read -r skill; do
        skills+=("$skill")
    done < <(read_common_skills)

    if [[ ${#skills[@]} -eq 0 ]]; then
        echo "  -- No common skills configured"
        return 0
    fi

    if [[ "$dry_run" == true ]]; then
        echo "  >> Install common skills from $skills_source_url#$skills_source_ref"
        for skill in "${skills[@]}"; do
            echo "     - .agents/skills/$skill"
        done
        return 0
    fi

    if ! command -v git >/dev/null 2>&1; then
        echo "  !! git is required to install common skills" >&2
        warnings=$((warnings + 1))
        return 0
    fi

    local temp_dir
    temp_dir="$(mktemp -d)"
    if ! git clone --depth 1 --branch "$skills_source_ref" "$skills_source_url" "$temp_dir" >/dev/null 2>&1; then
        echo "  !! Failed to clone common skills source: $skills_source_url#$skills_source_ref" >&2
        rm -rf "$temp_dir"
        warnings=$((warnings + 1))
        return 0
    fi

    mkdir -p "$target_path/.agents/skills"

    local skill source_dir destination
    for skill in "${skills[@]}"; do
        source_dir="$temp_dir/skills/$skill"
        if [[ ! -d "$source_dir" ]]; then
            source_dir="$temp_dir/.agents/skills/$skill"
        fi

        if [[ ! -d "$source_dir" ]]; then
            echo "  !! Missing common skill in source: $skill" >&2
            warnings=$((warnings + 1))
            continue
        fi

        destination="$target_path/.agents/skills/$skill"
        if [[ -e "$destination" && "$force" == false ]]; then
            echo "  -- Skip (exists) : .agents/skills/$skill"
            skipped=$((skipped + 1))
            continue
        fi

        rm -rf "$destination"
        cp -R "$source_dir" "$destination"
        echo "  OK Installed     : .agents/skills/$skill"
        created=$((created + 1))
    done

    rm -rf "$temp_dir"
}

# Create .claude/skills -> ../.agents/skills so Claude Code discovers reusable skills.
create_claude_skills_link() {
    local link_path="$target_path/.claude/skills"
    local link_dir="$target_path/.claude"
    local target_rel="../.agents/skills"
    local link_display=".claude/skills"

    if [[ "$dry_run" == true ]]; then
        if [[ -L "$link_path" ]]; then
            echo "  -- Link exists   : $link_display -> $(readlink "$link_path")"
        else
            echo "  >> Symlink       : $link_display -> $target_rel"
        fi
        return 0
    fi

    mkdir -p "$link_dir"

    if [[ -L "$link_path" ]]; then
        local current_target
        current_target="$(readlink "$link_path")"
        if [[ "$current_target" == "$target_rel" ]]; then
            echo "  -- Skip (link)   : $link_display -> $target_rel"
            skipped=$((skipped + 1))
            return 0
        fi
        if [[ "$force" == true ]]; then
            rm -f "$link_path"
        else
            echo "  !! Existing link : $link_display -> $current_target (expected $target_rel); pass --force to replace" >&2
            warnings=$((warnings + 1))
            return 0
        fi
    elif [[ -e "$link_path" ]]; then
        if [[ "$force" == true ]]; then
            rm -rf "$link_path"
        else
            echo "  !! Path exists (not a symlink): $link_display; pass --force to replace" >&2
            warnings=$((warnings + 1))
            return 0
        fi
    fi

    if ln -s "$target_rel" "$link_path" 2>/dev/null; then
        echo "  OK Symlinked     : $link_display -> $target_rel"
        created=$((created + 1))
    else
        echo "  !! Failed to create symlink: $link_display" >&2
        warnings=$((warnings + 1))
    fi
}

apply_shared_standard_set() {
    if [[ "$apply_shared_standards" == false ]]; then
        echo "  -- Skip shared standards"
        return 0
    fi

    if [[ "$dry_run" == true ]]; then
        echo "  >> Apply shared standards from $standards_source_url#$standards_source_ref"
        echo "     - .github/instructions/coding-principles.instructions.md"
        echo "     - .github/instructions/core-principles.instructions.md"
        echo "     - AGENTS.md"
        return 0
    fi

    if ! command -v git >/dev/null 2>&1; then
        echo "  !! git is required to apply shared standards" >&2
        warnings=$((warnings + 1))
        return 0
    fi

    local temp_dir
    temp_dir="$(mktemp -d)"
    if ! git clone --depth 1 --branch "$standards_source_ref" "$standards_source_url" "$temp_dir" >/dev/null 2>&1; then
        echo "  !! Failed to clone shared standards source: $standards_source_url#$standards_source_ref" >&2
        rm -rf "$temp_dir"
        warnings=$((warnings + 1))
        return 0
    fi

    # Prefer the bash port on Linux/macOS; fall back to the PowerShell tool only if the .sh is
    # missing from the standards source and pwsh is on PATH.
    local sh_sync="$temp_dir/scripts/sync-standards.sh"
    local ps_sync="$temp_dir/scripts/sync-standards.ps1"
    local sync_ok=false

    if [[ -f "$sh_sync" ]]; then
        if bash "$sh_sync" --source "$temp_dir" --target-repo "$target_path"; then
            sync_ok=true
        fi
    elif [[ -f "$ps_sync" ]] && command -v pwsh >/dev/null 2>&1; then
        if pwsh -NoProfile -File "$ps_sync" -Source "$temp_dir" -TargetRepo "$target_path"; then
            sync_ok=true
        fi
    else
        echo "  !! No sync-standards script found in standards source (need scripts/sync-standards.sh or scripts/sync-standards.ps1 with pwsh)" >&2
        warnings=$((warnings + 1))
        rm -rf "$temp_dir"
        return 0
    fi

    if [[ "$sync_ok" == true ]]; then
        echo "  OK Applied       : shared standards"
    else
        echo "  !! Shared standards sync reported an error" >&2
        warnings=$((warnings + 1))
    fi

    rm -rf "$temp_dir"
}

# ── Starter templates ────────────────────────────────────────────────────────
write_template "README.md"
write_template "{project-name}.code-workspace"
write_template ".gitignore"
write_template ".agents/.gitkeep"
write_template ".agents/skills/.gitkeep"
write_template ".claude/CLAUDE.md"
write_template ".github/.gitkeep"
write_template "docs/.gitkeep"
write_template "docs/index.md"

# ── Common skills ────────────────────────────────────────────────────────────
install_common_skill_set

# ── Claude Code integration ──────────────────────────────────────────────────
# Runs after common skills so the link points at a populated target folder on first scaffold.
create_claude_skills_link

# ── Shared standards ─────────────────────────────────────────────────────────
# Runs after the starter shell so the sync tool creates AGENTS.md with the shared preamble on
# top of a directory that already has the .claude/CLAUDE.md shim pointing at it.
apply_shared_standard_set

# ── Summary ───────────────────────────────────────────────────────────────────
echo ""
echo "Created : $created"
echo "Skipped : $skipped"
echo "Warnings: $warnings"

if [[ "$dry_run" == false && $created -gt 0 ]]; then
    echo ""
    echo "Starter shell ready. Run repo-audit.sh to verify."
    echo "Add optional artifacts only when adoption triggers are met."
fi

exit 0
