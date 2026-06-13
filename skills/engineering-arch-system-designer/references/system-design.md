# System Design Template

Use this as scaffolding. Fill every section. Leave no blanks — write "TBD + reason" if genuinely unknown.

---

```markdown
# System: {Name}

## 1. Requirements

### Functional
- {what it must do — use cases, not implementation}

### Non-Functional
- Performance: API < Xms p95 | page load < Xs
- Availability: 99.X% | RPO Xhr | RTO Xhr  
- Scale: X concurrent users | X RPS | X GB data
- Security: auth method | authorization model | compliance
- Cost: $X/month infrastructure ceiling

### Constraints
- Budget: $X/month
- Timeline: MVP by {date}
- Team: X backend, X frontend, X infra
- Existing systems: {what must integrate or remain}

---

## 2. Architecture Overview

Pattern chosen: {Monolith | Modular Monolith | Microservices | Serverless | Event-Driven | CQRS}

Why: {1–2 sentences — requirements that drove this}

Key trade-offs accepted:
- {trade-off 1}
- {trade-off 2}

---

## 3. Components

| Component | Responsibility | Technology | Scales How |
|---|---|---|---|
| API layer | request routing, auth, validation | {framework} | horizontal, load-balanced |
| {Service X} | {what it owns} | {tech} | {strategy} |
| Primary DB | source of truth | {database} | read replicas → then sharding |
| Cache | hot data, sessions | {Redis or equivalent} | cluster |
| Storage | files, media | {object storage} | inherently scalable |

### Data Flow
{Narrative or numbered steps describing how a key request flows through the system}

---

## 4. Data Stores

| Store | Type | Use | Rationale |
|---|---|---|---|
| {DB name} | Relational / Document / etc | {what data lives here} | {why this type} |

See: `references/database-selection.md`

---

## 5. Key Decisions

Write a full ADR for each. Summary here:

| Decision | Choice | Why |
|---|---|---|
| Architecture pattern | {choice} | {one-line reason} |
| Primary database | {choice} | {one-line reason} |
| Auth strategy | {choice} | {one-line reason} |
| {other significant choice} | {choice} | {one-line reason} |

See: `references/adr-template.md`

---

## 6. Scaling Plan

### Current (MVP / baseline)
- {instances, regions, DB config}

### 10x Growth
- {what changes: replicas, CDN, autoscaling, sharding, caching strategy}

### 100x Growth
- {what fundamentally changes: multi-region, architecture pattern shift, etc.}

---

## 7. Security Model

- Auth: {mechanism — JWT, OAuth 2.0, SAML, passkeys}
- Authorization: {RBAC / ABAC / ACL — describe roles}
- Encryption: TLS X.X in transit | {algo} at rest
- Rate limiting: {X req/min per user / IP / tenant}
- Compliance: {GDPR / HIPAA / PCI DSS / SOC 2 — applicable controls}

---

## 8. Failure Modes

| Failure | User Impact | Mitigation | Recovery |
|---|---|---|---|
| Primary DB down | {impact} | Multi-AZ / replica failover | Automatic < Xmin |
| Cache down | {impact} | Fallback to DB | Transparent |
| Auth service down | {impact} | Cache valid tokens | {TTL} |
| {external dependency} down | {impact} | {circuit breaker / fallback} | {manual / auto} |

---

## 9. Open Questions

- {question}: blocked on {what}, owned by {who}, needed by {when}
```
