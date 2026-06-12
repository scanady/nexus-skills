# Context Pack Workflow

Use this workflow when creating or updating a task-specific context pack as an internal repository optimization. Do not ask the user to define packs unless the task boundary, audience, authority, or risk level needs human judgment.

Paths below use `context/` as the default root name. The root is configurable and a project may host several roots; create the pack inside the root that owns the relevant knowledge.

## What A Pack Is

A context pack is a load plan for a recurring agent task. It tells the agent:

- what to read before acting
- what to read only when relevant
- what to exclude
- which claims are stale or source-critical
- where the task boundary begins and ends

A pack is not a dump of every page on a topic.

## Step 1: Identify The Task Pattern

Infer the task from repeated user requests, recurring ingests, repository maintenance patterns, or an explicit user goal. Write it as a concrete workflow, for example:

- review marketing content for compliance risk
- draft a product requirements document
- answer support questions about a product
- prepare an architecture review brief

If the workflow is one-off, do not create a pack. If the task is recurring but the boundary is vague, ask one or two outcome-focused questions. Do not ask the user whether they want a pack.

## Step 2: Read Candidate Pages

Use `context/index.md`, relevant shards, and existing packs to identify pages. Read candidate pages before adding them.

Separate:

- required context: needed for nearly every execution
- optional context: useful only for certain variants
- excluded context: stale, misleading, irrelevant, or outside the task boundary

## Step 3: Create Or Update The Pack

Create `context/packs/<task-slug>.md` from `assets/context-pack.template.md`.

Frontmatter example:

```yaml
---
type: context-pack
title: "Marketing Content Compliance Review"
task: "Review marketing content for compliance, brand, and editorial risk"
tags: [compliance, review-boundary]
required_pages: [compliance-review-boundaries, life-insurance-disclosure-rules]
optional_pages: [common-review-patterns]
exclusions: [outdated-product-language]
freshness: "Review policy and product pages before reuse if older than 30 days."
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

## Step 4: Write Load Guidance

The body should include:

- purpose
- load order
- required context with reasons
- optional context with conditions
- exclusions
- freshness and risk checks
- known gaps
- maintenance notes

## Step 5: Link Back

Add a link to the pack from relevant concept, synthesis, or entity pages when appropriate. Add the pack to the index.

## Step 6: Test The Pack Mentally

Before finishing, ask:

- Could an agent perform the task after loading only required pages?
- Are optional pages genuinely optional?
- Are stale or high-risk claims visible?
- Does the pack prevent scope creep?
- Is the pack smaller than loading the whole topic area?

## Step 7: Log The Package Operation

Append:

```markdown
## [YYYY-MM-DD] package | Created or updated <pack title>
```

Report pack maintenance only when useful to the user, and describe the outcome rather than the mechanism. Example: "I also optimized the repository for repeated compliance review tasks." Explain pack details only if the user asks.

## Pack Anti-Patterns

- Adding every related page to `required_pages`.
- Omitting exclusions for a task with known boundaries.
- Hiding freshness concerns in body text while frontmatter says the pack is current.
- Creating packs for one-off questions.
- Making a pack topic-shaped when the user needs a task-shaped workflow.