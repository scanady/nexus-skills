# Skill Archetypes

Each archetype has distinct structural patterns. Identify the archetype before designing any section of a skill.

---

## Technical Execution

**When to use**: The skill produces working code, implements features, configures systems, or performs technical setup.

**Frontmatter:**
- `role`: specialist or expert
- `scope`: implementation
- `output-format`: code

**Workflow pattern** (5 steps):
1. Analyze requirements — identify endpoints, models, auth needs
2. Design schemas — define types, data models, validation
3. Implement — write async/typed code with correct patterns
4. Secure — add auth, input validation, rate limiting
5. Test — write unit and integration tests

**Reference file topics** (load conditionally by sub-domain):
- Core framework patterns (routing, dependency injection, async)
- Data layer patterns (ORM, migrations, queries)
- Authentication/security patterns
- Testing patterns and utilities
- Migration guides (from older frameworks or patterns)

**Output template deliverables** (numbered):
1. Schema or model file (types, validation, data contracts)
2. Implementation file (endpoints, services, components)
3. Config, CRUD, or test file
4. Brief rationale for key design decisions

**Constraints style**: Highly specific syntax rules and exact API names.
Good: "Use `X | None` instead of `Optional[X]`", "Use `Annotated` pattern for dependency injection", "Never use Pydantic V1 syntax (`@validator`, `class Config`)"
Bad: "Follow best practices", "Avoid deprecated patterns"

**Example skills**: fastapi-expert, mcp-developer, django-expert, react-component-builder, typescript-pro

---

## Architecture / Design

**When to use**: The skill designs systems, selects components, and plans infrastructure — it produces blueprints and decision documents, not implementation code.

**Frontmatter:**
- `role`: architect
- `scope`: system-design or infrastructure
- `output-format`: architecture

**Workflow pattern** (follows the real domain lifecycle, 5–6 steps):
1. Discovery — assess current state, requirements, constraints, compliance
2. Design — select services/components, define topology, model data architecture
3. Security / Resilience — zero-trust, encryption, circuit breakers, bulkheads
4. Cost / Scale — right-sizing, reserved capacity, auto-scaling, FinOps
5. Migration / Deployment — migration strategy, rollout waves, failover testing
6. Operate — monitoring, automation, continuous optimization

**Reference file topics** (load by platform or sub-domain):
- Platform-specific services (aws.md, azure.md, gcp.md)
- Cross-cutting concerns: cost.md, multi-cloud.md, observability.md
- Pattern libraries: resilience.md, data.md, communication.md

**Output template deliverables** (numbered):
1. Architecture diagram / service topology with data flow
2. Component selection rationale (compute, storage, networking, database)
3. Security architecture (IAM, network segmentation, encryption)
4. Cost estimation and optimization strategy
5. Deployment approach and rollback plan

**Constraints style**: Principle-based with measurable targets.
Good: "Design for high availability (99.9%+)", "Use infrastructure as code (Terraform, CloudFormation)", "Never create single points of failure"
Bad: "Be secure", "Consider availability"

**Example skills**: cloud-architect, microservices-architect, kubernetes-specialist, database-optimizer, terraform-engineer

---

## Specification / Contract

**When to use**: The skill designs formal contracts — APIs, schemas, protocols, event formats — that other teams or systems implement against.

**Frontmatter:**
- `role`: architect or specialist
- `scope`: design
- `output-format`: specification

**Workflow pattern** (5 steps):
1. Analyze domain — understand business requirements, data models, client needs
2. Model resources — identify entities, relationships, operations
3. Design contract — define schemas, protocols, error models, auth flows
4. Plan evolution — versioning, deprecation, backward compatibility
5. Document — create complete formal specification with examples and edge cases

**Reference file topics**:
- Core specification format (OpenAPI 3.1, AsyncAPI, GraphQL SDL, JSON Schema)
- Specific concern patterns: versioning.md, pagination.md, error-handling.md, rest-patterns.md

**Output template deliverables** (numbered):
1. Resource or entity model with relationships
2. Full formal specification (YAML/JSON or SDL)
3. Authentication and authorization model
4. Versioning and deprecation strategy
5. Error catalog with status codes and examples

**Constraints style**: Standard-specific and semantics-precise.
Good: "Never use verbs in resource URIs (`/users/{id}`, not `/getUser/{id}`)", "Use RFC 7807 Problem Details for error responses", "Never design APIs without a versioning strategy"
Bad: "Follow REST principles", "Handle errors properly"

**Example skills**: api-designer, graphql-architect, asyncapi-designer, event-schema-designer

---

## Workflow / Conversational

**When to use**: The skill's primary value is structured interaction — it interviews, elicits, or facilitates to produce a document, rather than directly generating an artifact from a brief.

**Frontmatter:**
- `role`: specialist or facilitator
- `scope`: design or analysis
- `output-format`: document

**Workflow pattern** (5 steps):
1. Discover — initial open questions to understand scope, goals, and user value
2. Interview — systematic elicitation from multiple perspectives (e.g., user value + technical feasibility)
3. Document — write formal output using a structured format (EARS, Given/When/Then, etc.)
4. Validate — present output for stakeholder review; surface key trade-offs as structured choices
5. Plan — create implementation or next-steps checklist

**Special requirements for this archetype**:
- Explicitly name the structured questioning mechanism in workflow steps (e.g., use `AskUserQuestions` for structured option elicitation)
- Include multi-perspective framing in the interview step (e.g., "PM Hat: user value / Dev Hat: technical feasibility")
- Specify where to save the output artifact: `Save as: path/{name}.ext`
- Use structured question tools for choices that can be predetermined; reserve open-ended questions for when options can't be anticipated

**Reference file topics**:
- The formal syntax or format being used (ears-syntax.md, acceptance-criteria.md, specification-template.md)
- Question banks for systematic elicitation (interview-questions.md)
- Multi-agent pre-discovery patterns for complex cross-domain features

**Output template deliverables** (numbered):
1. Overview and user value statement
2. Functional requirements (formal format)
3. Non-functional requirements (performance, security, scale)
4. Acceptance criteria (Given/When/Then)
5. Error handling table
6. Implementation checklist
7. Save path for the produced artifact

**Constraints style**: Process discipline and rigor.
Good: "Conduct the full interview before writing the spec", "Never accept vague requirements ('make it fast' — push for measurable targets)", "Use structured question tools for choices that can be predetermined"
Bad: "Be thorough", "Ask good questions"

**Example skills**: feature-forge, design-research-ux-artifacts, ops-process-sop-creator, product-requirements, product-spec-prd-generator

---

## Content / Writing

**When to use**: The skill produces human-readable content — copy, articles, social posts, internal communications, proposals, or any text intended for human audiences.

**Frontmatter:**
- `role`: specialist or expert
- `scope`: creation
- `output-format`: content

**Workflow pattern** (5 steps):
1. Understand brief — audience, channel, goal, tone, length constraints, brand context
2. Contextualize — surface relevant audience insights, voice guidelines, competitive context
3. Draft — apply channel-appropriate structure (hook, body, CTA for social; opening/context/ask for comms)
4. Refine — check against brand/tone rules, optimize for channel format and constraints
5. Finalize — deliver with usage notes; provide variations if requested

**Reference file topics** (load by channel or content type):
- Brand voice and tone guidelines (brand-voice.md)
- Channel-specific format rules (linkedin.md, x-twitter.md, email.md, blog.md)
- Audience or persona data
- Example library for few-shot grounding

**Output template deliverables** (numbered):
1. Final copy (ready to publish or send)
2. Usage notes (channel, format, character count, optimal posting context if relevant)
3. Optional: 3–5 variations or A/B alternatives

**Constraints style**: Brand and audience precision with channel-specific rules.
Good: "Match brand voice (see references/brand-voice.md)", "Never use passive voice in CTAs", "Include one specific data point per claim", "LinkedIn posts: 150–300 words, no hashtag spam"
Bad: "Write engagingly", "Be on-brand"

**Example skills**: marketing-content-brand-copywriter, marketing-content-linkedin-writer, marketing-content-x-writer, comms-announce-organizational, content-copy-humanizer

---

## Research / Analysis

**When to use**: The skill investigates a domain, synthesizes findings across sources, and produces insights or ranked recommendations — it works with data, not just generates from a brief.

**Frontmatter:**
- `role`: analyst or expert
- `scope`: analysis
- `output-format`: report

**Workflow pattern** (5 steps):
1. Frame — define the research question, scope, and what "a good answer" looks like
2. Gather — identify sources, load domain reference data, research the landscape
3. Analyze — compare options, surface trade-offs, identify patterns and anomalies
4. Synthesize — extract insights, prioritize findings by importance
5. Recommend — produce actionable conclusions with supporting rationale; acknowledge limitations

**Reference file topics**:
- Domain-specific data or benchmarks (market data, technical benchmarks)
- Evaluation frameworks or scoring rubrics
- Competitor or landscape context

**Output template deliverables** (numbered):
1. Executive summary (1 paragraph, key findings and recommendation)
2. Key findings (bulleted, each with supporting evidence)
3. Trade-off analysis or comparison table
4. Ranked recommendations (most to least impactful or urgent)
5. Assumptions and known limitations

**Constraints style**: Evidence rigor and reasoning transparency.
Good: "Every recommendation must cite evidence from the research", "Distinguish between findings (observable) and recommendations (interpretive)", "Never recommend without addressing the strongest counterargument"
Bad: "Be objective", "Support your claims"

**Example skills**: marketing-intel-customer-segmentation, marketing-intel-competitor, strategy-planning-pricing, marketing-seo-adsense-readiness
