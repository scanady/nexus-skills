# Source-to-GPT Fidelity Contract

Use this reference during Phase A and Phase C. The goal is outcome fidelity: the GPT should make the same kinds of decisions and produce the same required artifacts as the source skill, within Custom GPT limits.

## Fidelity Ledger

Create a ledger in `conversion-report.md` with these columns:

| Source item | GPT location | Preservation method | Risk | Notes |
|---|---|---|---|---|
| Role and scope | Instructions | Verbatim or compressed | Low/Med/High | Include audience and what the GPT is not |
| Intake requirements | Instructions | Compressed table/list | Low/Med/High | Mark fields that block work |
| Workflow | Instructions | Numbered procedure | Low/Med/High | Remove local tool mechanics |
| Classification system | Instructions | Verbatim labels plus brief definitions | Low/Med/High | Do not bury only in knowledge |
| Output format | Instructions and/or knowledge template | Inline skeleton plus pointer | Low/Med/High | Required section names must stay visible |
| Citation contract | Instructions, index, knowledge headings | Exact IDs preserved | Low/Med/High | Never rename IDs |
| Accepted-risk/pass patterns | Instructions plus knowledge | Inline governing rule plus full reference | Low/Med/High | Common source of over-strict GPT behavior |
| Boundaries | Instructions | Verbatim or compressed | Low/Med/High | Includes human-in-loop and out-of-scope items |
| Capability assumptions | GPT profile/report | Capability mapping or gap marker | Low/Med/High | Includes scripts, URLs, APIs, sister skills |

## Must-Stay Instructions

These items must remain in `gpt-instructions.md` whenever present in the source:

- Role, audience, scope, and what the GPT must never claim to be.
- First-turn behavior and intake fields.
- Required workflow order.
- Decision labels, severity labels, status enums, and when to use each.
- Output section names, mandatory fields, and formatting constraints.
- Citation format and rule for uncited observations.
- Non-invention rule: do not create rules, IDs, facts, or source content.
- Human approval boundary and escalation language.
- Handling of uncertainty, edge cases, placeholders, and missing knowledge.
- Any source requirement for plain ASCII, concise output, or audit trail.

## Good Knowledge Candidates

These can move to uploaded knowledge when the Instructions keep a compact rule that explains how to use them:

- Full policy, regulation, rule, or control texts.
- Long examples and counterexamples.
- Long accepted-risk or prior-decision libraries.
- Glossaries and domain background.
- Full output template when the inline skeleton would exceed the cap.
- Source assets used as reference, not behavior.

## Gap Markers

Use this exact marker in `conversion-report.md` and, when the deployed GPT needs to ask the user, in Instructions:

`> NEEDS INPUT: <short description of missing source, capability, ID, or decision>`

Common gap markers:

- `> NEEDS INPUT: citation anchor` when source files lack stable IDs.
- `> NEEDS INPUT: output contract` when the source has no required output format.
- `> NEEDS INPUT: capability mapping` when the source requires local scripts, URLs, APIs, or sister skills.
- `> NEEDS INPUT: knowledge upload` when required files are missing from the bundle.

## Fidelity Failure Modes

Watch for these during review:

- The GPT can cite IDs but no longer follows the source classification rules.
- The GPT follows the output shape but drops human-in-loop or approval boundaries.
- The GPT applies rules more strictly than the source because accepted-risk patterns were moved to knowledge without an inline reminder.
- The GPT invents a citation for a reasonable observation because the no-rule path was omitted.
- The GPT asks too many intake questions instead of one consolidated blocking question.
- The GPT says it loaded all knowledge files when retrieval is only relevance-based.

## Pass Standard

A conversion passes when:

- All behavior-critical source items are preserved or explicitly marked as gaps.
- All source citation IDs survive exactly in the index and bundled text.
- Preview tests show the GPT makes source-consistent decisions.
- The bundle fits the configured Custom GPT caps.