# Technical Design Document Template

Use this template to structure the technical design document. Every section is required unless explicitly marked optional.

## Document Structure

### 1. Architecture Overview
Cover in 2-3 paragraphs:
- Architecture style (monolith, microservices, modular monolith, serverless, hybrid)
- High-level component topology (how major pieces relate)
- Key architectural drivers (what requirements shaped the architecture)

Include a text-based architecture diagram if the system has 3+ components:
```
[Component A] --REST--> [Component B] --Events--> [Component C]
       |                      |
       v                      v
  [Data Store]          [Cache Layer]
```

### 2. Technology Summary
Present choices as generic categories with reference implementations:

| Layer | Category | Reference Implementation | Purpose |
|-------|----------|--------------------------|---------|
| Runtime | [e.g., Server-side runtime] | [e.g., Node.js 20] | [Why this layer exists] |
| Framework | [e.g., Web framework] | [e.g., Next.js 14] | [What it handles] |
| Data | [e.g., Relational database] | [e.g., PostgreSQL 15] | [What data it stores] |
| Cache | [e.g., In-memory cache] | [e.g., Redis 7] | [What it accelerates] |

Include ALL layers discovered: runtime, framework, data stores, caches, message brokers, search engines, CDN, reverse proxy, container orchestration, etc.

### 3. Component Architecture
For each major component (service, module, or bounded context):

#### [Component Name — generic, not the project's internal name]
- **Responsibility:** What this component owns (single responsibility statement)
- **Interfaces:**
  - Exposes: [APIs, events, or contracts it provides to others]
  - Consumes: [APIs, events, or contracts it depends on]
- **Internal Structure:** [Layers or patterns used internally — e.g., controller/service/repository, hexagonal ports/adapters]
- **Key Design Decisions:**
  - [Decision: what was chosen and why it matters architecturally]

### 4. Data Architecture

#### Storage Strategy
For each data store:
- **Type:** Category (relational, document, key-value, graph, file/blob, time-series)
- **Purpose:** What data domain it serves
- **Access Pattern:** Read-heavy, write-heavy, mixed — and any optimization patterns (indexing strategy, partitioning, read replicas)

#### Entity Model
For each core entity:
- **Name:** Generic functional name
- **Key Fields:** Listed by function, not column name (e.g., "unique identifier (UUID)", "status enumeration")
- **Relationships:** Cardinality and direction (one-to-many, many-to-many with join entity, etc.)
- **Indexes/Constraints:** Uniqueness rules, foreign key relationships

Present as a text-based ER summary:
```
[User] 1--* [Project] 1--* [Task]
[User] *--* [Team] (via membership)
[Project] 1--1 [Settings]
```

#### Data Flow
Trace how data moves through the system for 2-3 primary workflows:
1. [Workflow name]: Source → Processing steps → Final destination

### 5. Integration Architecture

#### Internal Communication
- **Synchronous:** Protocol, patterns (request/response, RPC), service discovery
- **Asynchronous:** Message broker category, topic/queue patterns, delivery guarantees

#### External Integrations
For each external system:
- **Function:** What it provides (generic — e.g., "identity provider" not "Auth0")
- **Protocol:** HTTP/REST, GraphQL, gRPC, webhook, SDK
- **Pattern:** Polling, push, event-driven, request-on-demand
- **Reference Implementation:** The specific service used in parentheses

#### API Design Patterns
- **Style:** REST, GraphQL, gRPC, or mixed
- **Conventions:** Naming, versioning, pagination, filtering
- **Documentation:** How APIs are specified (OpenAPI, GraphQL introspection, etc.)

### 6. Security Architecture

#### Authentication
- **Method:** Category (token-based, session-based, certificate-based, OAuth2 flow)
- **Token Strategy:** Type, lifetime, refresh pattern
- **Multi-factor:** If present, describe the approach

#### Authorization
- **Model:** RBAC, ABAC, policy-based, or hybrid
- **Enforcement Points:** Where authorization checks occur in the architecture
- **Permission Granularity:** Resource-level, field-level, or action-level

#### Data Protection
- **In Transit:** Encryption protocol and scope
- **At Rest:** What is encrypted and how keys are managed
- **Secrets Management:** How credentials and keys are stored and rotated

### 7. Cross-Cutting Concerns

#### Error Handling
- **Strategy:** Global handler, per-layer, or mixed
- **Error Format:** Structure of error responses
- **Retry/Circuit Breaker:** Patterns for transient failures

#### Logging & Observability
- **Logging:** Structured or unstructured, log levels, what is logged
- **Metrics:** What is measured, aggregation approach
- **Tracing:** Distributed tracing if present, correlation ID strategy
- **Alerting:** Threshold-based, anomaly-based (if observable from code)

#### Configuration Management
- **Strategy:** Environment variables, config files, remote config, feature flags
- **Environment Separation:** How config differs across environments
- **Secrets vs. Config:** How sensitive values are handled differently

#### Testing Strategy
- **Unit Tests:** Framework, coverage approach, mocking strategy
- **Integration Tests:** What boundaries are tested, test database approach
- **E2E Tests:** If present — framework, scope, execution strategy
- **Test Data:** How test fixtures and seeds are managed

### 8. Deployment Architecture

#### Infrastructure
- **Hosting Model:** Category (cloud-managed, self-hosted, hybrid, serverless)
- **Topology:** Single region, multi-region, edge
- **Container Strategy:** Containerized or not, orchestration approach

#### Build & Deploy
- **Build Pipeline:** Steps from source to artifact
- **Deployment Strategy:** Rolling, blue-green, canary, or direct
- **Rollback:** How failed deployments are reverted

#### Scalability
- **Horizontal Scaling:** Which components scale out, trigger conditions
- **Vertical Scaling:** Which components scale up
- **Bottlenecks:** Known scaling constraints visible in the architecture
- **Caching Strategy:** What is cached, invalidation approach, cache layers
