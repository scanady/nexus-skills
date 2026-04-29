# README Strategy

README is project front door. Lead functionally; reserve technical depth for technical overview.

## Section Order

Use this order. Each section has purpose; resist technical detail outside sections that call for it.

1. **Functional overview** — Project name, one-sentence value, short plain-language paragraph on what it does for user. No install, no architecture, no jargon.
2. **Quick links** — Jumps to: minimal quick start, functional quickstart guides, technical overview, contributing. Order by reader journey, not alphabetically.
3. **Table of contents** — Anchored links to README's own sections. For medium-to-long READMEs.
4. **Deeper functional overview** — Subsections: what is this, what does it do, how does it work (capabilities + flow, not internals), key concepts. Diagrams only for user-facing flow.
5. **Prerequisites** — What reader needs before quick start works. Specific versions and platforms.
6. **Quick start** — Minimal copy-paste install + run to first success. End with explicit links into deeper quickstart guides.
7. **Contributing** — How to propose changes, branch model, contribution standards.
8. **License** — Name and link.
9. **Additional resources** — Technical overview, deeper docs, related projects, community.

Skip sections only when truly not applicable.

## Functional Overview Patterns

Open with sentence non-technical stakeholder could repeat:

> `<Project>` helps `<audience>` `<accomplish goal>` by `<functional capability>`.

Follow with short paragraph on user-facing experience. No stack names, frameworks, or architecture — those belong in technical overview.

## Quick Links Pattern

```markdown
## Quick Links

- [Quick start (5 minutes)](#quick-start)
- [Guide: <user goal>](docs/quickstart-<goal>.md)
- [Guide: <user goal>](docs/quickstart-<goal>.md)
- [Technical overview](docs/technical-overview.md)
- [Contributing](#contributing)
```

Order by what new reader needs first. Add TL;DR or "already familiar?" link when project warrants shortcut for experienced readers.

## Deeper Functional Overview Pattern

```markdown
## What is this

`<Project>` is a `<noun phrase>` that `<functional summary>`.

## What does it do

- `<Capability 1 from a user's point of view>`
- `<Capability 2>`
- `<Capability 3>`

## How does it work

A short, functional description of the experience: what a user does, what the system does for them, and the visible flow. Avoid internal components and code structure here.

## Key concepts

- **`<Concept>`** — `<plain-language definition>` and why it matters.
- **`<Concept>`** — `<definition>`.
```

If concept needs deep explanation, give short version here and link to technical overview.

## Quick Start Pattern

Keep README quick start minimal — install, run, observe. Then hand off. Add optional TL;DR block when stack is familiar enough for experienced readers to skip explanation.

```markdown
## Quick start

### TL;DR (optional)

```bash
<one-liner install>
<one-liner run>
```

### Prerequisites

- `<runtime + version>`
- `<package manager + version>`
- `<other tool>`

### Install

```bash
<one or two install commands>
```

### Run

```bash
<one command to start or invoke the project>
```

You should see `<observable outcome>`.

### What to do next

- New here? Try [Guide: <first user goal>](docs/quickstart-<goal>.md).
- Want to do `<task>`? See [Guide: <task>](docs/quickstart-<task>.md).
- Ready to go deeper? Read the [technical overview](docs/technical-overview.md).
```

If minimal path needs more than ~5 commands, project too complex for inline quick start. Move into `docs/quickstart-getting-started.md` and link from README.

## Update Strategy

When README already exists:

- Preserve project-specific voice, badges, acknowledgments, original phrasing where it works.
- Move technical-leaning sections (architecture, internals, design rationale) into `docs/technical-overview.md` and link.
- Replace stale install or run commands using verified source evidence.
- Reorder sections only when current order leads with technical detail before functional value.

## Style Guidance

- Prefer plain language over jargon.
- Write to reader as "you" when giving instructions.
- Short paragraphs. Break long lists into subsections.
- Keep code blocks minimal in README; deeper examples in quickstart guides.
- Use relative links for files in repo.

## Quality Checks

- First screen explains what project does and why, no install or architecture noise.
- Quick links promote minimal quick start and most valuable functional guide.
- Deeper functional overview explains capabilities, not implementation.
- Quick start fits on screen and ends with links into deeper guides.
- Technical depth lives in technical overview, not README.
