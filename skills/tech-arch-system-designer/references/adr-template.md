# ADR Template

## Format

```markdown
# ADR-{number}: {Title}

## Status
[Proposed | Accepted | Deprecated | Superseded by ADR-{number}]

## Context
What problem are we solving? What constraints exist? What forces are in play?

## Decision
What are we doing? State it clearly and directly.

## Consequences

### Positive
- benefit

### Negative
- drawback

### Neutral
- side effect (neither good nor bad)

## Alternatives Considered
| Option | Why Rejected |
|---|---|
| Option A | reason |
| Option B | reason |

## References
- link or doc
```

## Example

```markdown
# ADR-001: PostgreSQL as primary database

## Status
Accepted

## Context
E-commerce platform. Needs ACID transactions for orders + payments.
Product catalog has flexible attributes. Team knows PostgreSQL and MySQL.
Managed DB service in budget.

## Decision
PostgreSQL on managed cloud RDS (AWS RDS / Cloud SQL / Azure Database).

## Consequences

### Positive
- Full ACID compliance for financial data
- JSONB for flexible product attributes without schema migration
- Rich index types, CTEs, window functions
- Strong OSS ecosystem, wide tooling support

### Negative
- Vertical scaling ceiling (mitigated: read replicas)
- Needs schema migrations for structural changes
- Managed service cost for HA config

### Neutral
- Team learns PostgreSQL-specific features (JSONB, advisory locks)
- Dev → prod parity requires containerized Postgres locally

## Alternatives Considered
| Option | Why Rejected |
|---|---|
| MySQL | Weaker JSON support; less feature-rich for complex queries |
| MongoDB | Relational model required for orders/inventory; transactions across docs awkward |
| CockroachDB | Higher cost; unfamiliar to team; horizontal scale not yet needed |

## References
- PostgreSQL docs: https://www.postgresql.org/docs/current/
- Internal RFC: Database Selection Q3
```

## ADR File Naming

```
docs/adr/
├── 0001-use-postgresql.md
├── 0002-adopt-event-driven-messaging.md
├── 0003-auth-via-external-provider.md
└── README.md       ← index of all ADRs
```

## Key Questions Per Section

| Section | Ask |
|---|---|
| Context | What forces made this decision necessary? |
| Decision | What exactly are we committing to? |
| Consequences | What gets easier? What gets harder? |
| Alternatives | What did we seriously consider and discard? |
