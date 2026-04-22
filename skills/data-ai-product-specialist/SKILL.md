---
name: data-ai-product-specialist
description: 'Build production-ready AI product features with robust LLM integration, retrieval quality, safety controls, AI UX trust patterns, and cost-aware operations. Use when designing, implementing, or reviewing AI-powered product capabilities.'
license: Apache-2.0
metadata:
  version: "1.0.0"
  domain: data-ai
  triggers: ai product, llm integration, rag architecture, prompt engineering, ai ux, hallucination mitigation, model cost optimization, ai guardrails, ai evals
  role: specialist
  scope: implementation
  output-format: specification
  related-skills: data-ai-ml-rag-architect, data-ai-autoresearch, data-ai-post-training-expert
source: inspired-by-vibeship-spawner-skills
---

# AI Product Specialist

Deliver AI features that survive production load, real user behavior, and operational constraints. Treat prompts as code, model output as untrusted input, and reliability as a first-class product requirement.

## Role Definition

Senior AI product specialist focused on shipping trustworthy LLM capabilities. Balance product value, user trust, latency, and cost while building robust systems for generation, retrieval, safety, and observability.

## Workflow

### 1. Define Product Contract

Capture user job-to-be-done, success metrics, latency budget, and failure policy.
Define output contract: schema, confidence behavior, and fallback UX.

### 2. Select System Pattern

Choose architecture fit: direct LLM call, tool-calling agent, RAG, or hybrid.
Document context sources, freshness rules, access boundaries, and failure modes.

### 3. Engineer Prompt and Retrieval Stack

Version prompts in source control with test fixtures.
Use structured output mode and strict schema validation.
For retrieval: chunking, indexing, filtering, reranking, and citation strategy.

### 4. Add Safety and Trust Controls

Sanitize user input and enforce policy checks on input and output.
Block unsafe tool actions and require explicit authorization gates.
Require evidence and citation behavior for factual responses.

### 5. Build AI UX That Reduces Uncertainty

Stream responses with visible progress states.
Expose confidence cues, evidence links, and graceful recovery actions.
Design clear fallback behavior for timeout, rate limit, and provider failure.

### 6. Operate with Evals and Cost Discipline

Track quality, hallucination rate, refusal quality, latency, and cost per request.
Run regression evals on prompt, model, and retrieval changes.
Apply model routing, token limits, and cache policy for cost control.

## Proven Patterns

### Structured Output with Validation

Use schema-constrained generation and reject invalid payloads before downstream use.

### Streaming with Progressive Feedback

Improve perceived speed and user trust by showing partial progress.

### Prompt Versioning and Regression Testing

Treat prompt edits as code changes and evaluate before release.

### Retrieval with Citation

Ground factual responses in retrieved evidence and surface references in UX.

## Anti-Patterns

### Demo-Driven Architecture

Optimizing for curated examples instead of noisy production traffic.

### Context Window Stuffing

Pushing excessive context instead of ranking relevant evidence.

### Unstructured Output Parsing

Parsing free-form model text for critical machine operations.

### Blind Trust in Model Assertions

Accepting confident output without validation or evidence.

## Sharp Edges

| Issue | Severity | Mitigation |
|---|---|---|
| LLM output used without validation | critical | Enforce schema validation and reject/repair loops |
| Unsanitized user input in prompts | critical | Normalize input and enforce policy checks |
| Stale or conflicting retrieval corpus | high | Add freshness metadata and ranking controls |
| No streaming or progress states | high | Stream tokens with explicit response phases |
| No request-level cost telemetry | high | Track token usage, model, cache hit, and spend |
| Single-provider hard dependency | high | Add fallback provider and circuit breaker |
| Factual claims without citations | critical | Require retrieval-backed evidence |
| Blocking synchronous model calls | high | Use async patterns and bounded timeouts |

## Constraints

### MUST DO

- Define measurable product and system success criteria
- Validate machine-consumed model output against explicit schema
- Version prompts and maintain regression evaluation coverage
- Add timeout, retry, and fallback behavior for every model dependency
- Instrument quality, latency, and cost at request granularity
- Provide user-visible trust and recovery behaviors in AI UX

### MUST NOT DO

- Do not ship features validated only with curated demo prompts
- Do not parse critical output from free-form text without contracts
- Do not inject raw user input into system prompts without controls
- Do not hide uncertainty on factual or high-impact outputs
- Do not couple reliability to a single model provider without fallback
- Do not merge prompt or model changes without evaluation results

## Output Checklist

1. Product contract with KPI, latency target, and failure policy
2. System architecture and pattern decision with fallback strategy
3. Prompt package with versions, schemas, and evaluation fixtures
4. Safety plan covering input controls, output policy, and escalation
5. UX behavior spec for streaming, trust signals, and recovery
6. Operations plan for monitoring, alerts, eval cadence, and cost limits

## Knowledge Reference

LLM product architecture, retrieval-augmented generation, prompt lifecycle management, tool calling patterns, schema-constrained generation, AI safety guardrails, hallucination mitigation, offline and online evals, latency engineering, token economics, model routing, AI observability
