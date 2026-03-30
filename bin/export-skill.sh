#!/usr/bin/env bash
# export-skill.sh — Packages a skill into a zip file for import into Claude and other platforms.
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

# Ensure output directory exists
mkdir -p "$OUTPUT_DIR"

ZIP_PATH="$OUTPUT_DIR/$SKILL_NAME.zip"

# Remove any existing zip with the same name
[ -f "$ZIP_PATH" ] && rm "$ZIP_PATH"

# Run zip from the skills directory so the skill folder itself becomes the zip root.
# Result: <skill-name>.zip → <skill-name>/ → SKILL.md, ...
(cd "$SKILLS_DIR" && zip -r "$ZIP_PATH" "$SKILL_NAME/")

# Print summary
echo ""
echo "Exported '$SKILL_NAME'"
echo "  $ZIP_PATH"
echo ""
echo "Zip contents:"
echo "  $SKILL_NAME.zip"
echo "  +-- $SKILL_NAME/"
ls "$SKILL_PATH" | while IFS= read -r item; do
    echo "      +-- $item"
done
echo ""
