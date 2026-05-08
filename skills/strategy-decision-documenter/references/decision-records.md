# Decision Records

ADRs capture durable choices that future maintainers will question. Keep them short. Record reason, not ceremony.

## Offer Gate

Create or offer ADR only when all conditions hold:
- Hard to reverse: later change has meaningful migration, coordination, cost, or lock-in.
- Surprising without context: code alone will make future reader ask why.
- Real tradeoff: credible alternatives existed and chosen path won for specific reason.

If one condition fails, skip ADR and keep interrogating.

## Location

- System-wide choice: `docs/adr/` at repo root.
- Context-specific choice: nearest context `docs/adr/` beside that context's `CONTEXT.md`.
- No ADR directory: create only when first ADR passes gate.

## Numbering

Scan target ADR directory. Use next four-digit number:
- existing `0001-*`, `0002-*` -> next `0003-short-slug.md`
- none -> `0001-short-slug.md`

Slug rules:
- lowercase
- hyphen-separated
- names decision, not meeting topic
- short enough to scan

## Minimal Template

```md
# <Decision Title>

<One to three sentences: context, chosen path, and reason.>
```

## Optional Sections

Use only when they add memory value:

```md
## Considered Options

- <chosen option> - <why>
- <rejected option> - <why rejected>

## Consequences

- <non-obvious downstream effect>
```

Status frontmatter is useful only when repo already tracks ADR lifecycle:

```yaml
---
status: accepted
---
```

## Good ADR Subjects

- Architecture shape: monorepo, event sourcing, modular monolith, service split
- Integration contract: events vs synchronous calls, ownership boundaries, API style
- Platform lock-in: database, message bus, auth provider, deployment substrate
- Data ownership: which context owns customer, invoice, identity, billing, etc.
- Deliberate deviation: manual SQL over ORM, local queue over broker, REST over GraphQL
- Hidden constraint: compliance, latency, partner contract, operational limit

## Bad ADR Subjects

- Easy-to-reverse library choice
- Obvious implementation detail
- Personal preference without tradeoff
- Decision already documented clearly elsewhere
- Work item, task list, or implementation plan
