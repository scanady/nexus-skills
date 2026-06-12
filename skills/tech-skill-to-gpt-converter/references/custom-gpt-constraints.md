# Custom GPT Constraints Reference

Use this reference to resolve platform limits and runtime assumptions before finalizing a conversion.

## Current Conversion Assumptions

| GPT area | Limit or behavior | Converter rule |
|---|---|---|
| Instructions | Treat 8000 characters as the hard paste-ready limit | Target 6500-7500 characters to leave editing headroom |
| Knowledge files | Custom GPTs allow up to 20 uploaded files | Build at or below 20; target 12-18 for complex bundles |
| File size | Each uploaded file can be up to 512 MB | Prefer smaller text-forward files because retrieval quality matters more than raw size |
| Knowledge purpose | Uploaded knowledge is reference material | Put behavior, workflow, tone, and rules of operation in Instructions |
| Retrieval | GPT retrieves relevant chunks; it does not guarantee a full-folder read | Build a compact index and scoped files; instruct targeted retrieval |
| Conversation state | Each GPT conversation starts fresh and does not use saved memory or user custom instructions | Include first-turn behavior, intake, and scope in Instructions |
| Capabilities | Web search, image generation, canvas, Code Interpreter/Data Analysis, apps, and actions vary by plan/workspace | Enable only when the source skill needs the capability |
| Apps/actions | A GPT can use apps or actions, but not both at the same time | Choose one integration model only when required; otherwise disable both |

## Deployment Target Rule

Default target is **ChatGPT Custom GPT**. If the user asks for ChatGPT Projects, API assistants, or another runtime, treat that as a separate target. Confirm the cap and label it in the conversion report. Do not apply a Project cap to a Custom GPT bundle.

## Capability Mapping

| Source skill assumption | GPT mapping |
|---|---|
| Reads local files from a workspace | Upload relevant files as Knowledge; remove workspace paths from Instructions |
| Runs local scripts for deterministic processing | Generate a rebuild script for the bundle maintainer, or enable Code Interpreter only if the GPT user must run analysis during chat |
| Fetches current web content | Enable Web Search only if up-to-date public information is required |
| Calls private systems or APIs | Define GPT Actions, or document as non-transferable if no action spec is provided |
| Uses external apps | Use Apps only if the workspace supports them and no Actions are needed |
| Generates images | Enable image generation only if image output is a core source outcome |
| Edits long documents interactively | Consider Canvas when available, but do not make fidelity depend on it |
| Calls sister skills or subagents | Inline the needed behavior or document as non-transferable |

## Instruction Placement Rule

OpenAI guidance distinguishes behavior from reference material. Use this rule:

- Put **behavior** in Instructions: role, scope, goals, tone, workflow, intake, decisions, classifications, output format, safety, citation policy, and escalation rules.
- Put **reference material** in Knowledge: rule texts, examples, policy excerpts, glossaries, templates, accepted-risk libraries, prior decisions, and source documents.

When a reference asset contains behavior-critical content, keep a compact governing rule in Instructions and point to the full asset by filename.

## Testing Implications

Preview tests must prove the GPT uses uploaded knowledge as intended. A passing bundle should:

- Retrieve full rule text before citing a rule ID.
- Ask for missing context when rule applicability depends on it.
- Avoid making claims based on knowledge that was not uploaded.
- Follow Instructions even when a knowledge file contains conflicting prose.