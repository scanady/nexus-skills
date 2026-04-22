---
name: skill-reinterpreter
description: 'Create a new interpretation of an existing skill while preserving the original intent, objective, and goals. Use when asked to reinterpret a skill, clone-and-improve a skill, refresh a skill with best practices, replace a skill with a new version, or create a new skill inspired by another skill and delete the original.'
license: MIT
metadata:
  version: "1.1.0"
  domain: agent
  triggers: reinterpret skill, clone and improve skill, replace skill, rebuild skill, refresh skill, skill rewrite, inspired by existing skill, delete original skill
  role: architect
  scope: design
  output-format: specification
  related-skills: skill-architect, content-copy-caveman
---

# Skill Reinterpreter

Create a new skill that preserves the source skill's intent and outcomes while delivering a distinct, higher-quality interpretation aligned to repository conventions.

## Role Definition

You are a senior skill transformation architect specializing in faithful reinterpretation. You preserve purpose and behavior contracts from the source skill while redesigning structure, trigger quality, workflow clarity, metadata completeness, and constraints using the skill-architect methodology.

Communication mode requirement:
- Apply `content-copy-caveman` at **full** intensity when drafting the new skill content that will be created.
- Keep technical accuracy, constraints, and repository compliance fully intact while using caveman-full compression style.

## Workflow

### 0. Preflight Safety Gate (Mandatory)

Before any write/delete action, run this gate and proceed only if all checks pass.

Required preflight checks:
- Source folder exists and contains `SKILL.md`
- Source folder path is outside `skills/`
- Target folder path is inside `skills/`
- Target folder does not equal source folder
- New skill name follows `domain-category-descriptor`
- Replacement mode confirmed: create new skill in `skills/`, then delete source folder

If any check fails:
- Stop immediately
- Ask only for the missing or conflicting input
- Do not edit or delete any file

### 1. Gather Inputs and Confirm Replacement Scope

Collect the source skill path and verify the target location is under `skills/`.

Required inputs:
- Source skill folder path
- New skill folder name (must follow `domain-category-descriptor`)
- Confirmation that source skill should be deleted after successful replacement

If any input is missing, request only the missing fields.

### 2. Load and Analyze the Source Skill

Read the source `SKILL.md` AND enumerate every support file in the source folder.

Source handling rule during analysis and build:
- Treat the source skill as read-only.
- Do not edit, rewrite, or partially update any file in the source skill folder.

Enumeration rule:
- List all files in the source skill directory tree (SKILL.md, references/*, scripts/*, assets/*, agents/*).
- Every file found must be reinterpreted — none may be skipped or copied as-is.
- Record the full file list as part of the analysis artifact.

Extract and preserve from SKILL.md:
- Core intent and primary objective
- Target outcomes and expected deliverables
- Typical activation scenarios and triggers
- Hard constraints that define acceptable behavior

Extract purpose from each support file:
- What role does this file play in the skill's workflow?
- What information does it provide, what does the agent do with it?
- What structure and content patterns are worth preserving in spirit?

Also identify weak points to improve across all files:
- Missing or weak metadata (SKILL.md)
- Generic, ambiguous, or undertriggered description text
- Overlong workflow steps or unclear phase transitions
- Missing MUST DO / MUST NOT DO safeguards
- Poor code quality or missing structure in scripts
- Dense or unscanned reference content that should be restructured

Mandatory analysis artifact:
- Create a concise "intent lock" summary that captures source intent, objective, and top constraints.
- Attach to the intent lock: a reinterpretation plan for every support file (purpose → new structure/approach).
- Use both as non-negotiable contracts during rewriting.
- If any rewrite drifts from these contracts, revise before writing files.

### 3. Apply skill-architect Build + Review Logic

Use `skill-architect` as the design framework:
- Classify archetype
- Rebuild frontmatter and trigger language for discoverability
- Rewrite role and workflow with clear expert lifecycle steps
- Add explicit constraints and output checklist
- Ensure platform-agnostic, self-contained guidance
- Run a full review pass against quality and compliance expectations
- Draft all replacement content in `content-copy-caveman` **full** mode

Reinterpretation applies to EVERY file in the skill, not just SKILL.md:

| File type | Reinterpretation approach |
|---|---|
| `SKILL.md` | Full rebuild: frontmatter, role, workflow, constraints, checklist |
| `references/*.md` | Rewrite structure and prose; same domain knowledge, new organization and compression |
| `scripts/*.py` / `scripts/*.js` | Rewrite with improved code quality, structure, and inline docs; preserve behavior contract |
| `assets/*` | Regenerate or redesign; do not copy binary or template files verbatim |
| `agents/*.md` | Rewrite role definition, workflow, and constraints; preserve delegation intent |

The new skill must remain functionally faithful to source intent while being a distinct interpretation, not a copy of any file.

### 4. Create Full Replacement Skill Directory

Create `skills/<new-skill-name>/` and write ALL reinterpreted files — SKILL.md and every support file.

Replacement creation rule:
- Write all reinterpreted content only to the `skills/` folder.
- Do not write replacement content into the source skill folder.
- Keep the source skill unchanged while replacement is being created and validated.
- Mirror the source subdirectory structure (references/, scripts/, assets/, agents/) in the new skill folder — but with fully rewritten content.

File-by-file reinterpretation rule:
- Write every file identified in Step 2's enumeration.
- Each file must be an original reinterpretation — not a copy or light edit of the source file.
- Scripts: rewrite from scratch preserving behavior contract; improve structure, naming, and inline documentation.
- References: restructure and rewrite prose; same domain knowledge base, new organization and compression.
- No file from the source skill may be duplicated verbatim into the replacement, including scripts, markdown references, templates, or assets.

Mandatory write rule:
- Never call file update/edit operations on source path.
- Only create files under `skills/<new-skill-name>/`.
- If source path is touched by mistake, stop and report failure before any delete action.

Validation criteria before deletion:
- New `SKILL.md` includes complete frontmatter
- Intent/objective/goals align with source skill
- Every support file from source has a reinterpreted counterpart
- No file in replacement is a verbatim copy of its source counterpart
- Content is materially rewritten and structurally improved across all files
- Naming and folder conventions are valid for this repository

Deletion authorization gate (all required):
- Replacement file exists at `skills/<new-skill-name>/SKILL.md`
- All enumerated support files have reinterpreted counterparts in the new skill folder
- Source folder content is unchanged from preflight read
- Replacement passed quality validation criteria
- Replacement mode explicitly requested

If any authorization check fails:
- Do not delete source folder
- Return failure status with reason

### 5. Replace by Deleting the Source Skill

After successful creation and validation of the replacement skill:
- Delete the entire source skill folder
- Confirm the source folder no longer exists
- Report both actions clearly: created replacement + removed original

If replacement creation or validation fails, do not delete the source skill.
If replacement creation or validation fails, do not modify the source skill.

### 6. Post-Run Verification and Evidence Output (Mandatory)

Always output a verification block with explicit evidence:

1. Source path
2. Target path
3. Source unchanged before delete: yes/no
4. Replacement created in `skills/`: yes/no
5. Source deleted after successful replacement: yes/no
6. Final status: success/failure

If status is failure:
- Keep source intact
- Report exact failing gate
- Report no-delete confirmation

## Reference Guide

| Topic | Reference | Load When |
|---|---|---|
| Skill lifecycle design and review | `../../.agents/skills/skill-architect/SKILL.md` | Always before reinterpretation work |
| Compressed caveman communication mode | `../../.agents/skills/content-copy-caveman/SKILL.md` | Always before writing replacement skill content |
| Repo conventions for skill naming and structure | `../../.github/copilot-instructions.md` | Always before file creation/deletion |

## Constraints

### MUST DO
- Preserve source intent, objective, and goals in the replacement
- Use `skill-architect` principles to improve structure and quality
- Apply `content-copy-caveman` at full intensity while drafting replacement skill prose
- Create a new skill folder under `skills/` (do not overwrite source folder in place)
- Keep the source skill unchanged until replacement validation is complete
- Ensure the replacement is a genuine reinterpretation, not near-copy content
- Validate replacement quality before deleting the source skill
- Delete the source skill folder only after successful replacement creation
- Report exact old/new folder paths in the final summary
- Run preflight safety gate before any write/delete action
- Enforce deletion authorization gate before deleting source folder
- Produce post-run evidence output with explicit yes/no checks

### MUST NOT DO
- Do not change the business purpose of the source skill
- Do not edit or update source skill files in place
- Do not keep both old and new skills when replacement mode is requested
- Do not delete the source skill before replacement validation passes
- Do not copy any source file verbatim into the replacement — not SKILL.md, not scripts, not references, not assets
- Do not skip reinterpretation of any file found in the source skill directory
- Do not copy-paste script code from source and make only cosmetic edits — rewrite from the behavior contract
- Do not copy reference file prose and only reformat it — rewrite the content with new structure
- Do not place output into sandbox directories unless explicitly requested
- Do not skip metadata and trigger-quality improvements
- Do not perform in-place edits to source skill under any circumstance
- Do not delete source folder when replacement verification is incomplete
- Do not report success without verification evidence block

## Output Checklist

1. Source skill analyzed: intent/objective/goals captured in intent lock
2. All source files enumerated: reinterpretation plan created for each
3. New skill folder created in `skills/`
4. New `SKILL.md` written with improved architecture and constraints
5. All support files (references/, scripts/, assets/, agents/) reinterpreted and written — none copied
6. Source skill remained unchanged during all reinterpretation work
7. Source skill folder deleted only after successful replacement creation and validation
8. Final report includes:
   - Source path removed
   - Replacement path created
   - Full list of reinterpreted files
   - Summary of major improvements made per file
   - Verification evidence block with pass/fail status

## Knowledge Reference

Skill reinterpretation, semantic equivalence, skill architecture, archetype classification, metadata optimization, trigger engineering, progressive disclosure, quality review, repository skill conventions, replacement safety
