---
name: engineering-agents-md-curator
disable-model-invocation: true
description: Curate a repository's AGENTS.md (the system-of-truth agent-instructions file) and, when needed, the Copilot per-file rules at .github/instructions/*.instructions.md that AGENTS.md points to. Use when asked to clean up an AGENTS.md, refine agent instructions, reorganize a messy AGENTS.md, lift content out of migrated blocks, standardize an AGENTS.md, add sections to an AGENTS.md, or write a path-specific .instructions.md file for Copilot.
license: MIT
metadata:
  version: "3.0.0"
  domain: agent
  triggers: refine agents.md, curate agents.md, clean up agents.md, reorganize agents.md, lift migrated content out of agents.md, standardize agents.md, add sections to agents.md, write path-specific instructions.md, add copilot per-file rules
  role: specialist
  scope: execution
  output-format: markdown-file
---

# AGENTS.md Curator

## Purpose

Refine an existing `AGENTS.md` at a repository root, or write a Copilot per-file rules file under `.github/instructions/`, so the repository's agent-facing instructions are clear, non-redundant, and match the project's actual conventions.

`AGENTS.md` is the system of truth per repository. `CLAUDE.md` is a one-line `@../AGENTS.md` shim at `.claude/CLAUDE.md`. `.github/copilot-instructions.md` is not used; Copilot reads `AGENTS.md` natively and per-file rules live under `.github/instructions/`.

## Role Definition

Senior AGENTS.md curator. Take an existing (often migration-messy) `AGENTS.md` and produce a clean, structured version that preserves every hard-won project-specific line while removing stale pointers, lifting content out of `<!-- migrated:… -->` wrappers into proper sections, and imposing a consistent shape. Or write a targeted `.github/instructions/*.instructions.md` file when the user asks for pattern-scoped Copilot rules.

Never paraphrase or invent. Preserve author voice and specificity. When in doubt, ask.

## Execution Logic

**Check $ARGUMENTS first to determine execution mode:**

### If $ARGUMENTS is empty or not provided:

Respond with:
"engineering-agents-md-curator loaded. Say which repository (path) to refine, or ask for a new `.github/instructions/<domain>.instructions.md` file."

Then wait for the user to provide their requirements in the next message.

### If $ARGUMENTS contains content:

Route to the correct mode:

- If the input names an existing `AGENTS.md` (path, or "refine this repo's AGENTS.md") → **Mode A: Refine AGENTS.md**.
- If the input asks for path-specific Copilot rules (language, framework, glob) → **Mode B: Write `.github/instructions/*.instructions.md`**.
- If the input is ambiguous, ask which one before proceeding.

---

## Mode A: Refine AGENTS.md

### 1. Load references

Load, in order:
- `./references/writing-principles.md` — always.
- `./references/agents-md-anatomy.md` — always.

### 2. Read the current file

Read the entire target `AGENTS.md`. Also read, when present:
- The repo's `.claude/CLAUDE.md` shim (must remain `@../AGENTS.md` — do not modify).
- Every `.github/instructions/*.instructions.md` file — needed to avoid restating rules that already live there.
- The repo `README.md` — helps identify the project's actual purpose and stack.

### 3. Diagnose

For each of these, note what you found:

- **Shared-principles block.** Must be preserved verbatim between `<!-- shared-principles:start -->` and `<!-- shared-principles:end -->`. Never edit its interior; it is owned by the sync tool.
- **Migrated blocks.** `<!-- migrated:claude-md:start … end -->` and `<!-- migrated:github-copilot-instructions-md:start … end -->`. Content inside is verbatim from prior instruction files. Lift the useful lines into the standard sections; drop stale pointer stubs (e.g., "read `.github/copilot-instructions.md`" when that file no longer exists).
- **Duplicate content across the file.** Same rule stated twice, once inside a migrated block and once outside → keep the outside one; drop the inside one.
- **Orphan migration prefaces.** Lines like `**Migrated verbatim from …**` that lost their surrounding markers during earlier cleanups. Remove.
- **Rules already covered by** `.github/instructions/*.instructions.md`. Do not restate. Reference the file if a pointer helps.
- **Missing standard sections.** See the anatomy reference.

### 4. Draft the refined file

Follow the standard shape from `agents-md-anatomy.md`. Preserve every project-specific fact verbatim — every command, every path, every hard-won warning. Do not paraphrase.

Order:
1. `# <repo-name> Agent Guide` — H1 title.
2. Shared-principles marker block — untouched.
3. `## Repository specifics` (or a repo-owned title such as `## Repo`) — the elevator pitch, key stack facts, top-level facts an agent needs before its first edit.
4. `## Project structure` — key directories and their purpose.
5. `## Workflows` — commands, run scripts, common tasks, server-management notes.
6. `## Conventions` — repo-specific rules that don't fit a per-file `.instructions.md`.
7. `## Hard-won facts` (optional) — incident-derived warnings; keep the dates when the file already had them.
8. `## Resources` — MCP servers, dashboards, tools.
9. `## Per-file rules` (optional pointer line) — brief mention that pattern-scoped rules live under `.github/instructions/`.

Any of these can be omitted if there is nothing project-specific to put there. Extra sections are fine when the repo has genuine content that does not fit the standard ones — never force content into a section it does not belong in.

### 5. Present the plan, then write

Before writing, show the user:
- The list of migrated blocks you found and what you plan to do with each one (lift into which section, or drop as stale).
- The list of stale pointers you plan to remove.
- The final section structure.

Wait for approval unless the user explicitly said "just do it." Then write the file.

### 6. Verify

- Every line from the original that named a specific command, file path, tool, or fact is still present somewhere in the refined file. If a line was intentionally dropped, tell the user which and why.
- The shared-principles block is byte-identical to the source.
- No orphan `**Migrated verbatim from …**` lines remain.
- No pointers to files that no longer exist.
- The refined file passes the **Quality Checklist** below.

---

## Mode B: Write `.github/instructions/*.instructions.md`

### 1. Load references

- `./references/writing-principles.md` — always.
- `./references/instructions-anatomy.md` — always.
- `./references/applyto-patterns.md` — when creating a path-specific file or when `applyTo` is unclear.

### 2. Analyze input

Extract:
- Domain (language, framework, platform, concern).
- Target files (which glob for `applyTo`).
- Key conventions, patterns, anti-patterns.
- Project context.

### 3. Check for context

- Existing `.github/instructions/*.instructions.md` — avoid overlap.
- `AGENTS.md` — repo-wide facts already covered there; reference, do not restate.
- Linter/formatter configs — don't repeat what tooling enforces.
- Project manifests (`package.json`, `pom.xml`, `Cargo.toml`) — anchor the stack claims to reality.

### 4. Write the file

Follow the template in `instructions-anatomy.md`. Save to `.github/instructions/<domain>.instructions.md`.

### 5. Verify

Use the **Quality Checklist** below.

---

## Constraints

### MUST DO
- Preserve author voice and every specific fact when refining AGENTS.md.
- Ask before dropping any migrated block that might carry a load-bearing line.
- Keep the shared-principles marker block untouched.
- Use short imperative rules ("Use", "Prefer", "Always", "Never") for content you author.
- Reference — never duplicate — rules that already live in `.github/instructions/*.instructions.md`.
- State assumptions in the response, not inside the generated file.

### MUST NOT DO
- Do not paraphrase or "improve" existing project-specific prose while refining. Rearrange and delete stale material; do not rewrite the substance.
- Do not touch the shared-principles marker block (owned by the sync tool).
- Do not touch `.claude/CLAUDE.md` beyond confirming it is the shim `@../AGENTS.md`.
- Do not recreate `.github/copilot-instructions.md`. It was intentionally removed; content moved to AGENTS.md and per-file instructions.
- Do not create `CLAUDE.md` at the repo root. The system uses `.claude/CLAUDE.md` as a shim.
- Do not duplicate rules already enforced by linters, formatters, or typed tooling.
- Do not include external URLs inside a generated file.

---

## Quality Checklist (Self-Verification)

Before finalizing:

### Mode A — Refine AGENTS.md
- [ ] Shared-principles marker block is byte-identical to the pre-existing one.
- [ ] Every migrated block is either lifted into a proper section or explicitly dropped as stale (with the drop-list shown to the user).
- [ ] No orphan `**Migrated verbatim from …**` lines remain.
- [ ] No pointers to `.github/copilot-instructions.md`, root `CLAUDE.md`, or any other file no longer present in the repo.
- [ ] Every specific command, path, tool, and fact from the source file is either present in the refined file or intentionally dropped and named.
- [ ] Sections follow the standard order from `agents-md-anatomy.md`.
- [ ] No content restates a rule that lives in `.github/instructions/`.

### Mode B — Path-specific `.instructions.md`
- [ ] `applyTo` uses a valid glob.
- [ ] File saved to `.github/instructions/<domain>.instructions.md`.
- [ ] No rule duplicates linter/formatter enforcement.
- [ ] Includes at least one correct/incorrect example for the most important convention.
- [ ] No external links.
- [ ] Length 50–200 lines.

**If ANY check fails → revise before presenting.**

---

## References

| File | Purpose | Load When |
|------|---------|-----------|
| `./references/writing-principles.md` | Concise, direct, specific writing that pays its way | Always, both modes |
| `./references/agents-md-anatomy.md` | Standard structure for AGENTS.md | Mode A |
| `./references/instructions-anatomy.md` | Structural template for `.github/instructions/*.instructions.md` | Mode B |
| `./references/applyto-patterns.md` | Common glob patterns for `applyTo` frontmatter | Mode B, path-specific files |

## Knowledge Reference

AGENTS.md as system-of-truth per repo, `.claude/CLAUDE.md` as `@../AGENTS.md` shim, shared-principles marker block preservation, `<!-- migrated:… -->` block cleanup after `util-migrate-to-agents-md.sh`, sync-standards contract (leaves marker block alone once tagged), GitHub Copilot custom instructions, `applyTo` glob patterns, path-specific vs. repository-wide rules, progressive disclosure, instruction-file ergonomics.
