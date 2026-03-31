# GitHub Copilot Agent Tools Reference (Doc Co-Authoring)

This file translates the **portable, capability-based** instructions in the content-technical-doc-coauthoring skill into **GitHub Copilot agent tool** operations.

Scope:
- This is a reference for *how to do the mechanics* in GitHub Copilot.
- The primary workflow remains tool-agnostic in [../SKILL.md](../SKILL.md).

## Capability → Tool Mapping

### Read an existing doc or template

**Capability:** Open/read a file that already exists.

**Copilot tool:** `read_file`
- Use when: you need the current wording before patching, or to ingest a template.
- Tip: If the file is large, read it in chunks via `offset` + `limit`.

### Create a new doc scaffold

**Capability:** Create a new Markdown document with section placeholders.

**Copilot tool:** `create_file`
- Use when: starting a doc from scratch.
- Tip: Put the doc somewhere easy to find (e.g., `docs/` or a project folder). If you’re not sure, ask the user where they want it.

### Make a small, surgical edit (diff/patch style)

**Capability:** Replace or tweak specific paragraphs/sections without rewriting the whole doc.

**Copilot tool:** `apply_patch`
- Use when: iterating on a section, incorporating feedback, fixing wording.
- Best practice: Patch the smallest possible region; preserve unrelated formatting.

### Find where to edit (search)

**Capability:** Locate phrases/sections across files.

**Copilot tools:**
- `grep_search` for exact text or regex (fast, predictable)
- `semantic_search` when you don’t know exact wording
- `file_search` to find candidate files by name/pattern

### Reader testing with a “fresh eyes” agent

**Capability:** Ask a clean-room reviewer (no authoring context) to answer questions from only the doc.

**Copilot tool:** `runSubagent`
- Use when: Stage 3 Reader Testing.
- Critical: Provide ONLY the document content + the question(s). Do not include authoring chat context.
- Output: Summarize what the reader got right/wrong and what was ambiguous.

### Fetch content from the web (optional)

**Capability:** Pull in content from a URL the user provides.

**Copilot tool:** `fetch_webpage`
- Use when: user shares a public URL and you can access it.
- Fallback: Ask the user to paste the relevant excerpt if access fails.

### Run commands (optional)

**Capability:** Run formatting, linting, spellcheck, or build/test commands.

**Copilot tool:** `run_in_terminal`
- Use when: repo has tooling (e.g., `markdownlint`, `prettier`, `pytest`) and the user wants validation.
- Tip: Prefer targeted commands and keep output small.

## Practical Recipes

### Recipe: Start a new doc scaffold

1. Ask for:
   - doc type (decision/spec/proposal)
   - audience
   - desired impact
   - template (if any)
2. Create the file scaffold with `create_file`.
3. Iterate section-by-section with `apply_patch`.

### Recipe: Draft a section from bullets

1. Brainstorm bullets in chat.
2. User selects keep/remove/combine.
3. Patch only that section using `apply_patch`.
4. If you need to confirm current wording first, use `read_file` on a small range.

### Recipe: Iterative refinement loop

For each feedback round:
1. Restate the requested change in one sentence.
2. Patch with `apply_patch`.
3. (Optional) `grep_search` to ensure no duplicate phrasing remains.

### Recipe: Reader testing with `runSubagent`

1. Generate 5–10 “reader questions”.
2. For each question:
   - Call `runSubagent` with:
     - the doc content
     - the single question
3. Summarize failures as actionable edits.
4. Patch the doc with `apply_patch`.

## Notes / Pitfalls

- Avoid instructions that depend on features not present in Copilot agent sessions (e.g., `str_replace`, special “artifact links”).
- Prefer patch-based editing (`apply_patch`) to reduce accidental regressions.
- When reader-testing, keep the subagent prompt minimal to prevent “helpful guessing” from hidden context.
