# Metadata Fields Reference

Use this reference when choosing or refining metadata for an existing skill. Metadata must improve discoverability and triggering accuracy, not just make the frontmatter look richer. This skill edits only the `metadata` map; it does not rewrite `description` or any other frontmatter field.

## Field Selection Rule

Add a metadata field only when the skill body supports it clearly. If the evidence is weak, omit the field instead of guessing.

## Standard Metadata Fields

### version

Use when the skill already has a metadata block or when you are materially improving its routing metadata.

- Preferred format: semantic version string such as `"1.0.0"`
- Use `"1.0.0"` when adding a first metadata block to an existing skill unless the skill already declares a version elsewhere
- Do not infer complicated version histories from the repo

### domain

Choose the primary operating domain of the skill.

Common values in this repo include:
- `meta`
- `quality`
- `workflow`
- `marketing`
- `data-ml`
- `api-architecture`
- `infrastructure`
- `backend`

Derive from:
- subject matter of the workflow
- nouns in the description and headings
- output artifact and audience

Avoid:
- overly broad values like `general`
- multiple domains in one field unless the repo already uses that pattern

### triggers

This is one of the most important metadata fields for routing. Use it to reinforce and clarify routing signal without changing the existing `description`.

Use:
- direct user phrases someone would type
- action-oriented keywords
- short noun phrases tied to the task

Good trigger patterns:
- `create skill`
- `review skill`
- `API design`
- `prompt optimization`

Bad trigger patterns:
- abstract categories only
- internal implementation jargon users would never say
- redundant copies of the skill name with no added routing value

Aim for 6 to 12 strong triggers, separated by commas.

### role

Choose the expertise stance the skill represents.

Common values:
- `specialist`
- `expert`
- `architect`
- `analyst`
- `strategist`

Derive from:
- seniority and specialization implied by the workflow
- whether the skill is primarily evaluative, design-oriented, or execution-oriented

### scope

Choose the kind of work the skill primarily performs.

Common values:
- `analysis`
- `design`
- `implementation`
- `creation`
- `review`
- `guidance`
- `system-design`

Pick the single best fit based on the main workflow outcome.

### output-format

Choose the artifact the skill most often produces.

Common values:
- `code`
- `architecture`
- `specification`
- `document`
- `content`
- `report`

Derive from the expected deliverable, not from the domain alone.

### related-skills

Use only for real adjacency.

Add a related skill when:
- users commonly run one skill before or after another
- one skill reviews or extends the output of another
- the pairing improves discoverability without causing ambiguity

Do not add unrelated popular skills just to make the metadata look complete.

### author

Optional. Only retain or add it when there is a clear author attribution pattern already used by the repo or the user has asked for it.

## Extended Routing Fields

These fields are not part of the base spec, but they fit under the spec's optional `metadata` map and help with search, identification, and prioritization.

### aliases

Use for alternate names or natural language variants of the skill.

Examples:
- hyphenated and spaced variants
- singular and plural variants when both are common
- common shorthand used by humans

Do not include:
- generic category words that match many unrelated skills
- every token split from the skill name

### anti-triggers

Use to document phrases or domains that look similar but should not activate the skill.

Examples:
- a writing skill may include `anti-triggers: code generation, debugging`
- a metadata skill may include `anti-triggers: implement skill workflow, rewrite skill body`

Use when the skill is broad enough to be confused with adjacent skills.

### examples

Use for 2 to 4 short prompt examples showing how a user might request the skill.

Examples should:
- look like actual user requests
- cover direct and indirect activation scenarios
- reinforce trigger coverage without bloating frontmatter

### priority

Use only when the skill is clearly narrower or broader than its neighbors and routing benefits from that distinction.

Suggested values:
- `specific`
- `normal`
- `broad`

Guidance:
- `specific` for narrow skills that should win on exact matches
- `broad` for umbrella skills that should not crowd out narrower matches
- `normal` when there is no strong prioritization need

## Derivation Heuristics

When a skill has little or no metadata, derive fields in this order:

1. Determine WHAT the skill does from the opening paragraphs and workflow.
2. Determine WHEN it should activate from verbs, task nouns, examples, and the existing description.
3. Determine output artifact to select `output-format`.
4. Determine expertise stance to select `role`.
5. Determine the main work type to select `scope`.
6. Add extended fields only when ambiguity or undertriggering risk is visible.

## Omission Rules

It is better to omit a field than to fill it with low-signal metadata.

Omit when:
- the skill body does not support the value clearly
- the field would duplicate the description without adding new routing signal
- the field would widen activation in a misleading way
- the field would require guessing user behavior not implied by the skill