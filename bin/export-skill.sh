#!/usr/bin/env bash
# export-skill.sh — Packages a skill directory into a zip file for manual import.
#
# The archive layout follows the Agent Skills convention:
#   <skill-name>.zip
#   └── <skill-name>/
#       ├── SKILL.md
#       └── optional files/directories (scripts/, references/, assets/, ...)
#
# Usage:
#   ./export-skill.sh <skill-name>
#   ./export-skill.sh research-deep-reading-analyst
#
# Output: ./output/<skill-name>.zip
#
# Zip structure (as required by Claude):
#   <skill-name>.zip
#   └── <skill-name>/
#       ├── SKILL.md
#       └── (any other files/folders in the skill directory)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
SKILLS_DIR="$PROJECT_ROOT/skills"
OUTPUT_DIR="$PROJECT_ROOT/output"

trim_wrapping_quotes() {
    local value="$1"
    value="${value#\"}"
    value="${value%\"}"
    value="${value#\'}"
    value="${value%\'}"
    printf '%s' "$value"
}

extract_frontmatter_field() {
    local field="$1"

    awk -v field="$field" '
        BEGIN { in_frontmatter = 0 }
        /^---[[:space:]]*$/ {
            if (in_frontmatter == 0) {
                in_frontmatter = 1
                next
            }
            exit
        }
        in_frontmatter && $0 ~ ("^" field ":[[:space:]]*") {
            sub("^" field ":[[:space:]]*", "", $0)
            print
            exit
        }
    ' "$SKILL_PATH/SKILL.md"
}

get_available_skills() {
    find "$SKILLS_DIR" -maxdepth 1 -mindepth 1 -type d | while IFS= read -r dir; do
        if [ -f "$dir/SKILL.md" ]; then
            basename "$dir"
        fi
    done | sort
}

show_usage() {
    echo ""
    echo "Usage: export-skill.sh <skill-name>"
    echo ""
    echo "Available skills:"
    get_available_skills | while IFS= read -r skill; do
        echo "  * $skill"
    done
    echo ""
}

SKILL_NAME="${1:-}"

# Show usage when no skill name is provided
if [ -z "$SKILL_NAME" ]; then
    show_usage
    exit 1
fi

if ! command -v zip >/dev/null 2>&1; then
    echo ""
    echo "ERROR: 'zip' is required to export skills."
    echo ""
    exit 1
fi

SKILL_PATH="$SKILLS_DIR/$SKILL_NAME"

# Validate skill directory exists
if [ ! -d "$SKILL_PATH" ]; then
    echo ""
    echo "ERROR: Skill '$SKILL_NAME' not found in $SKILLS_DIR"
    echo ""
    echo "Available skills:"
    get_available_skills | while IFS= read -r skill; do
        echo "  * $skill"
    done
    echo ""
    exit 1
fi

# Validate SKILL.md exists
if [ ! -f "$SKILL_PATH/SKILL.md" ]; then
    echo ""
    echo "ERROR: '$SKILL_NAME' is missing a SKILL.md file."
    echo ""
    exit 1
fi

if [[ ! "$SKILL_NAME" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]] || [ "${#SKILL_NAME}" -gt 64 ]; then
    echo ""
    echo "ERROR: '$SKILL_NAME' does not satisfy the Agent Skills naming rules."
    echo ""
    exit 1
fi

FRONTMATTER_NAME="$(trim_wrapping_quotes "$(extract_frontmatter_field name)")"
FRONTMATTER_DESCRIPTION="$(trim_wrapping_quotes "$(extract_frontmatter_field description)")"

if [ -z "$FRONTMATTER_NAME" ]; then
    echo ""
    echo "ERROR: '$SKILL_NAME/SKILL.md' is missing the required frontmatter name field."
    echo ""
    exit 1
fi

if [ "$FRONTMATTER_NAME" != "$SKILL_NAME" ]; then
    echo ""
    echo "ERROR: Frontmatter name '$FRONTMATTER_NAME' must match the folder name '$SKILL_NAME'."
    echo ""
    exit 1
fi

if [ -z "$FRONTMATTER_DESCRIPTION" ]; then
    echo ""
    echo "ERROR: '$SKILL_NAME/SKILL.md' is missing the required frontmatter description field."
    echo ""
    exit 1
fi

# Ensure output directory exists
mkdir -p "$OUTPUT_DIR"

ZIP_PATH="$OUTPUT_DIR/$SKILL_NAME.zip"

# Remove any existing zip with the same name
[ -f "$ZIP_PATH" ] && rm "$ZIP_PATH"

# Run zip from the skills directory so the skill folder itself becomes the zip root.
(cd "$SKILLS_DIR" && zip -rq "$ZIP_PATH" "$SKILL_NAME/" -x '*/.DS_Store' '*/Thumbs.db' '*/__MACOSX/*')

# Print summary
echo ""
echo "Exported '$SKILL_NAME'"
echo "  $ZIP_PATH"
echo "  Standard: Agent Skills directory layout"
echo ""
echo "Zip contents:"
echo "  $SKILL_NAME.zip"
echo "  +-- $SKILL_NAME/"
find "$SKILL_PATH" -mindepth 1 -maxdepth 1 -printf '%f\n' | sort | while IFS= read -r item; do
    echo "      +-- $item"
done
echo ""
