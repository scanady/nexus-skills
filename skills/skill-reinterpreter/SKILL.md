---
name: skill-reinterpreter
disable-model-invocation: true
description: Reinterpret a local or remote skill into this repo, either by merging the ideas that fit into an existing skill or by creating a new skill inspired by it. Use when asked to "reinterpret a skill", "merge this skill into my existing one", "port ideas from this skill", or "create a skill inspired by this GitHub skill". Not skill-architect (edits one skill in place) or skill-evaluator (tests).
license: MIT
metadata:
  version: "1.4.0"
  domain: agent
  triggers: reinterpret skill, merge skill into existing skill, port skill from GitHub, create skill inspired by another skill, rebuild skill from scratch, clone and improve skill, refresh skill with best practices
  role: architect
  scope: design
  output-format: specification
  related-skills: skill-architect, content-copy-clear-writing
---

# Skill Reinterpreter

Take a reference skill. Keep its intent and outcomes. Deliver a distinct, higher-quality interpretation, inspired by the reference, never a copy.

The reference skill is **read-only input**. This skill never edits it and never deletes it.

## Role Definition

Senior skill transformation architect. Preserve purpose and behavior contract of the reference. Redesign structure, trigger quality, workflow clarity, metadata, constraints using the `skill-architect` methodology.

Style: draft new skill prose with `content-copy-clear-writing`. Active voice, specific words, no needless words. `description` and `triggers` stay plain user language. Code and quoted strings stay verbatim. Technical accuracy and constraints stay intact.

## Modes

Two modes. Both take a local or remote reference. Pick one. State pick in one line before any write.

| Mode | Result |
|---|---|
| **Create** | New skill folder in this repo's `skills/` library, inspired by the reference |
| **Merge** | Reference ideas that fit, rewritten into an existing skill in the library |

How to pick:
- Request names an existing skill to improve or extend → Merge.
- Request names a new skill, or says "new skill" / "save in `skills/`" → Create.
- Unclear → ask once. Never improvise a hybrid silently.

Reference types:
- Local folder, any location. A skill already in `skills/` counts, as long as it is not the Merge target.
- Remote (GitHub URL or similar): fetch raw files, not summaries, to a scratch dir. Read them there.

## Scope

User names what to port ("only the review method and the word list") → that is the scope. Scope narrows file coverage. Every in-scope file gets reinterpreted. Out-of-scope files are listed in the report as "excluded by scope", with one-line reason. Not silently dropped.

No scope stated → everything in scope.

## Integrity Rule

Never skip or bend a step silently. Deviation needed → say what, why, before acting. Deviation touches a gate → get user confirmation first. Final report lists every deviation.

## Workflow

### 0. Preflight Gate (Mandatory)

Run before any write. All checks for chosen mode must pass.

All modes:
- Reference readable, contains `SKILL.md`, every support file enumerated
- Target library located (the folder holding this repo's skills)
- Governing taxonomy chosen (see Step 3)

Create only:
- New folder name free in the library
- Name and domain fit the taxonomy

Merge only:
- Target skill exists in the library, has `SKILL.md`
- Target is not the reference
- Uncommitted changes in target noted. Tell user before editing.

Gate fails → stop. Ask only for missing or conflicting input. Write nothing.

### 1. Gather Inputs

Required:
- Reference: path or URL
- Mode (infer, then state)
- Target: new folder name (Create) or existing skill (Merge)
- Scope (default: all)
- Governing taxonomy: user-supplied, project-supplied, or `references/agent-taxonomy.md`

Ask only for missing fields.

### 2. Load and Analyze Reference

1. Read `SKILL.md`. List every file in the tree (references, scripts, assets, agents).
2. Pull from `SKILL.md`: core intent, objective, deliverables, activation scenarios, hard constraints.
3. Pull from each support file: role in workflow, what the agent does with it, structure worth keeping.
4. Note weak points: thin description, long steps, missing MUST DO / MUST NOT DO, poor script quality, dense unscanned references.
5. **Intent lock** (write it out before any file): reference intent, objective, top constraints. Plus one line per in-scope support file: purpose → new structure.

Draft drifts from intent lock → fix draft, not the lock.

Merge mode, add:
- Read the target skill fully. Note its voice, structure, existing rules.
- List where reference ideas fit, clash, or duplicate target content. Reference rule contradicts target rule → keep target rule, adapt the idea, report the conflict.
- Name the target's nearest neighbor skills for the collision scan.

### 3. Apply skill-architect Design Logic

Use the `skill-architect` skill as framework. Invoke it. Apply its guidance on archetype, structure, and especially its description-and-triggers guidance.

- Classify archetype.
- Select domain and category prefix from the governing taxonomy. Folder name equals frontmatter `name`. `metadata.domain` equals the top-level domain prefix. Map legacy prefixes (`agent-*`, `prompt-*`, `tech-*`, `comms-*`) to current homes. No invented domain or prefix.
- Rebuild `description` and `triggers` from scratch. Never carry the reference's over.
- Collision scan: read the 2–3 nearest neighbor skills. Opening sentences must not be interchangeable.
- Description 150–400 chars, differentiator in sentence one, 3–6 quoted user phrases in WHEN clause. Triggers 6–10, verb-object, user-authored, no duplicates of description, no morphological variants, no category-only words. No PUSH sentence on narrow skills.
- Add explicit MUST DO / MUST NOT DO and an output checklist.
- Self-contained skill: workflow must not depend on project config files or paths outside the skill folder. Reference other skills by name only.

Merge mode: target's description and triggers change only if the merge widens what the skill does. Then re-run the collision scan.

Reinterpretation by file type:

| File type | Approach |
|---|---|
| `SKILL.md` | Rebuild: frontmatter, role, workflow, constraints, checklist |
| `references/*.md` | New organization and prose. Same knowledge. |
| `scripts/*` | Rewrite from the behavior contract. Better structure, naming, docs. |
| `assets/*` | Regenerate or redesign. No verbatim copy. |
| `agents/*.md` | Rewrite role, workflow, constraints. Keep delegation intent. |

### 4. Write

Create mode:
- Create `<library>/<new-name>/`. Mirror the reference's subfolders. Write all in-scope files there.

Merge mode:
- Edit the target skill. Large new material (a method, a long table) goes in a new `references/` file, linked from `SKILL.md`. `SKILL.md` gets the workflow hook and the constraints.
- Match target's existing style, file naming, and reference conventions.
- Update target's description, triggers, reference table, and checklist where the merge changes them.
- Do not touch files the merge does not need.

Both modes:
- Write only into the new or target skill. Never into the reference.
- No file is a verbatim copy of its reference counterpart.

### 5. Validate

Before declaring done:
- Frontmatter complete. Name matches folder.
- Intent, objective, constraints match intent lock.
- Every in-scope support file has a reinterpreted counterpart.
- No verbatim copies. Spot-check by diffing against the reference.
- Collision scan done, result recorded.
- Run the repository's skill validator if one exists. Report output, pass or fail.
- Merge mode: target's original behavior still intact. Nothing it did before is broken.
- Reference unchanged.

Any check fails → fix, then re-run. Cannot fix → report failing check.

### 6. Report (Mandatory)

Always output:

1. Mode
2. Reference (path or URL)
3. Target path (new or merged skill)
4. Reference unchanged: yes/no
5. Files created or edited: list, with one-line improvement per file
6. Files excluded by scope: list with reason
7. Collision scan: neighbors checked, result
8. Validator output: pass/fail
9. Deviations from this workflow: list, or "none"
10. Final status: success/failure. On failure: failing check.

No success claim without this block.

## Reference Guide

| Topic | Source | Load when |
|---|---|---|
| Skill lifecycle design, description and trigger rules | `skill-architect` skill | Always, before Step 3 |
| Prose drafting style | `content-copy-clear-writing` skill | Before drafting new prose |
| Portable taxonomy | `references/agent-taxonomy.md` | Choosing name prefix or `metadata.domain` when no taxonomy supplied |

## Constraints

### MUST DO
- Preserve reference intent, objective, goals
- Pick a mode, state it, and honor it
- Run the preflight gate before any write
- Write the intent lock before any file
- Treat the reference as read-only
- Rebuild `description` and `triggers` from scratch, with a collision scan
- Enforce taxonomy prefix on folder, `name`, and `metadata.domain`
- Honor user scope. List what scope excluded.
- Get raw reference files for remote references
- Validate before declaring done
- Keep produced skill self-contained
- Output the report block with explicit evidence

### MUST NOT DO
- Edit, rewrite, move, or delete any reference file or folder
- Copy any reference file verbatim, or only reformat it
- Carry over the reference `description` or `triggers`
- Interchangeable opening sentence with a neighbor (collision)
- Pad triggers past ~12, or use variants, name echoes, category-only words
- Invent a taxonomy domain or prefix
- Make the produced skill depend on project config files (agent instruction files, CLAUDE.md, copilot instructions) or on paths outside its own folder
- Write content into sandbox folders unless asked
- Skip or bend a step silently
- Report success without the report block

## Output Checklist

1. Mode stated
2. Preflight passed
3. Intent lock written, with per-file plan
4. Reference unchanged
5. New or merged content written, none copied verbatim
6. `description` and `triggers` rebuilt, collision scan recorded
7. Taxonomy compliance checked
8. Validator run, output reported
9. Report block complete, deviations listed

## Knowledge Reference

Skill reinterpretation, merge versus create, semantic equivalence, skill architecture, archetype classification, trigger engineering, collision scanning, progressive disclosure, taxonomy compliance
