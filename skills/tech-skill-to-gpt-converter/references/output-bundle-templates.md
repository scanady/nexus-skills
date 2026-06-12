# Output Bundle Templates

Use these templates when writing the derived GPT bundle.

## `gpt-profile.md`

```markdown
# GPT Profile

Name: <short GPT name>
Description: <one-sentence user-facing purpose>

## Conversation Starters

- <realistic starter 1>
- <realistic starter 2>
- <realistic starter 3>
- <realistic starter 4>

## Recommended Capabilities

| Capability | Setting | Reason |
|---|---|---|
| Web Search | Off/On | <why> |
| Image Generation | Off/On | <why> |
| Canvas | Off/On | <why> |
| Code Interpreter/Data Analysis | Off/On | <why> |
| Apps | Off/On | <why> |
| Actions | None/<name> | <why> |
```

## `gpt-instructions.md`

Keep the paste-ready body under 8000 characters. Use this skeleton:

```markdown
# Role
<who the GPT is, who it serves, and its decision authority>

# Boundaries
- <non-negotiable rule>
- <human-in-loop or approval boundary>
- <out-of-scope rule>

# First-Turn Behavior
- Ask one consolidated question only when required context is missing.
- Proceed when enough context is present.
- Do not assume saved memory, custom instructions, local files, or unuploaded knowledge.

# Required Context
<compact list or table of intake fields>

# Knowledge Use
- Start with `00-knowledge-index.md` to identify candidate sources.
- Consult full text in the bundled file before citing any ID.
- Cite only exact IDs present in the uploaded knowledge.
- Put concerns without a matching source under <source-specific no-rule section>.

# Workflow
1. <step>
2. <step>
3. <step>

# Classification
<exact labels and compact definitions>

# Output Format
<inline skeleton with required sections and fields>

# Final Rules
- <non-invention rule>
- <formatting rule>
- <uncertainty rule>
```

## `README.md`

```markdown
# <GPT Bundle Name>

Derived from: `<source skill path>`
Generated: <date>

## Files

<tree>

## Setup in ChatGPT

1. Create a new GPT in ChatGPT.
2. Paste `gpt-instructions.md` into Instructions.
3. Upload every file in `knowledge/`.
4. Set capabilities as shown in `gpt-profile.md`.
5. Add conversation starters from `gpt-profile.md`.
6. Test with `verification-prompts.md` before sharing.

## Rebuild

<command or source-edit instructions>

## Trade-Offs

- <trade-off 1>
- <trade-off 2>

## Verification

Run the prompts in `verification-prompts.md` and compare expected behavior.
```

## `conversion-report.md`

```markdown
# Conversion Report

Source skill: `<path>`
Target: ChatGPT Custom GPT
Instruction characters: <count>
Knowledge files: <count>/<cap>

## Source Inventory

| Area | Count | Notes |
|---|---:|---|

## Fidelity Ledger

| Source item | GPT location | Preservation method | Risk | Notes |
|---|---|---|---|---|

## Knowledge Map

| Source group | Bundled file | Items |
|---|---|---:|

## Capability Map

| Source assumption | GPT setting | Notes |
|---|---|---|

## Gaps

> NEEDS INPUT: <gap, if any>

## Verification Results

| Test | Expected | Result | Notes |
|---|---|---|---|
```

## `verification-prompts.md`

```markdown
# Verification Prompts

## Test 1: <happy path>
Prompt: <prompt>
Expected: <observable behavior>

## Test 2: <citation or rule test>
Prompt: <prompt>
Expected: <observable behavior and required source IDs>

## Test 3: <missing context>
Prompt: <prompt>
Expected: <one consolidated question or documented fallback>

## Test 4: <edge case>
Prompt: <prompt>
Expected: <observable behavior>
```