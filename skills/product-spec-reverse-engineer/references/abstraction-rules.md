# Abstraction Rules

These rules govern how to strip product-specific information from documentation to produce product-agnostic specifications suitable for greenfield rebuilding.

## Core Principle

The output must read as a **specification for a system that could be built**, not as a description of a system that was built. A reader should not be able to identify the original product from the documentation alone.

## Replacement Rules

### Product & Company Names
- Replace ALL product names with "the system" or "the platform"
- Replace ALL company names with "the organization"
- Replace branded feature names with generic functional descriptions
  - e.g., "SmartSync™" → "real-time bidirectional synchronization"
  - e.g., "PowerDash" → "analytics dashboard"

### URLs, Paths, and Identifiers
- Remove all URLs (API endpoints, documentation links, marketing sites)
- Remove all file paths — describe structure by pattern, not by path
  - e.g., "controllers are organized by domain area" not "src/controllers/users/"
- Remove all environment-specific values (hostnames, ports, database names, bucket names)
- Remove all version-specific identifiers unless architecturally relevant

### Technology References
Use the **category (reference implementation)** pattern:
- "relational database (PostgreSQL in reference implementation)"
- "server-side JavaScript runtime (Node.js in reference implementation)"
- "container orchestration platform (Kubernetes in reference implementation)"

This preserves architectural intent while noting what was actually used.

### People and Teams
- Remove developer names, team names, code owners
- Replace with role descriptions: "the data team" → "the team responsible for data infrastructure"

### Dates and Timelines
- Remove specific dates, sprint numbers, release versions
- Replace with relative descriptors if timing matters: "in a subsequent phase" or "as a later enhancement"

## Structural Abstraction

### Organize by Function, Not by File
- The functional spec groups by **user capability**: "User Management", "Report Generation"
- NOT by code structure: "UserController", "ReportService"

### Describe Patterns, Not Implementation
- "The system uses an event-driven pattern for asynchronous processing"
- NOT "The system publishes to the `order-events` SQS queue which triggers `processOrder` Lambda"

### Abstract Data Models
- Describe entities by function: "stores user identity and authentication credentials"
- NOT by schema: "users table with columns: id BIGINT, email VARCHAR(255)..."
- Include field categories and relationships, not column definitions

## Verification Checklist

After drafting, scan both documents for:

1. **Proper nouns** — No product names, company names, or branded terms should remain
2. **URLs** — No `http://`, `https://`, `localhost:`, or domain names
3. **File paths** — No `/src/`, `./config/`, or directory trees from the original project
4. **Environment values** — No port numbers, database names, bucket names, or API keys
5. **Code snippets** — No source code; describe behavior in prose
6. **Internal jargon** — Replace project-specific terminology with standard industry terms
7. **Technology names** — Should only appear in parenthetical reference implementation notes

## Edge Cases

### When abstraction conflicts with clarity
If removing a specific term makes the documentation unclear, use the category-first pattern:
- "a publish-subscribe messaging system (Apache Kafka)" — generic category comes first

### When the architecture IS the product
Some projects are development tools, frameworks, or infrastructure. In these cases:
- Still abstract the product name
- Describe the tool's purpose generically: "a command-line interface for managing cloud infrastructure"
- The target audience should be able to understand the system's purpose without knowing the brand

### When code comments contain useful context
- Extract the intent, not the phrasing
- "The system implements request deduplication to handle network retries" — not "As the TODO in line 42 says, we need to handle dupes"
