# Architecture Patterns

## Pattern Decision Table

| Pattern | Use When | Team Size | Key Trade-off |
|---|---|---|---|
| Monolith | Simple domain, fast iteration | 1–10 | Easy to run; hard to scale parts independently |
| Modular Monolith | Growing complexity, team splitting soon | 5–20 | Enforced boundaries; single deploy still |
| Microservices | Large org, distinct scaling needs per domain | 20+ | Independent deploy + scale; major operational overhead |
| Serverless | Variable/spiky load, event-driven processing | Any | Auto-scale, zero idle cost; cold starts, vendor dependency |
| Event-Driven | Async workflows, loose service coupling | 10+ | Decoupled; eventual consistency, hard to trace |
| CQRS | Read/write ratio skewed, complex query needs | Any | Optimized reads + writes; data sync complexity |

## Monolith

**Pick when:** new project, small team, unclear domain boundaries, speed matters more than scale.

Pros: simple deploy, trivial debugging, no distributed system problems.
Cons: scales as a unit, tech stack locked, full deploy on every change.

**Avoid when:** multiple teams need independent deploy, services have wildly different load profiles.

## Modular Monolith

**Pick when:** monolith getting messy, teams emerging, microservices overhead not yet justified.

Enforce hard module boundaries — shared database is the one exception to manage carefully.
Migration path: extract bounded contexts to services when team and load demand it.

## Microservices

**Pick when:** multiple large teams, distinct domain boundaries, genuinely different scaling requirements.

Don't pick microservices to "be ready to scale." Pick when current scale or team structure demands it.

Requires: service discovery, distributed tracing, centralized logging, API gateway, circuit breakers. Budget for operational complexity before committing.

## Event-Driven

**Pick when:** producers shouldn't wait for consumers, high throughput async processing, need audit trail.

Message bus options by scale and need:
- Low volume, simple routing → RabbitMQ / cloud-native queues (SQS, Cloud Pub/Sub)
- High volume, replay needed → Kafka / Kinesis

Cons: debugging cross-service flows is hard, message ordering requires care, eventual consistency everywhere.

## CQRS (Command Query Responsibility Segregation)

**Pick when:** reads far outnumber writes, read model needs different shape than write model, or event sourcing is in scope.

Reads and writes use separate models, often separate stores. Events sync write → read side.

Don't add CQRS for standard CRUD. Complexity cost is real.

## Quick Selector

| Requirement Signal | Pattern |
|---|---|
| Small team, simple domain | Monolith |
| Growing but not yet large | Modular Monolith |
| Large org, clear domain splits | Microservices |
| Spiky or event-triggered load | Serverless |
| Fire-and-forget async workflows | Event-Driven |
| Read-heavy, complex queries | CQRS |
