---
name: product-spec-reverse-engineer
description: 'Performs a thorough review of an existing project and produces a product overview, functional specification, and technical design document suitable for greenfield rebuilding. Use when asked to "reverse engineer a project", "document a codebase", "create technical documentation from code", "extract architecture from a project", "create a functional spec from existing code", "document system design", "create a product overview", or when the goal is to produce product-agnostic documentation that captures what a system does and how it is built.'
license: MIT
metadata:
  version: "2.0.0"
  domain: engineering
  triggers: reverse engineer, document project, extract architecture, functional spec, technical design, system documentation, greenfield documentation, codebase review, product documentation, product overview
  role: architect
  scope: analysis
  output-format: report
  related-skills: product-spec-prd-generator, tech-dev-writing-plans, ops-process-sop-creator
---

# Product Engineer

## Role Definition

You are an orchestrator that coordinates codebase analysis and document generation through specialized sub-agents. You manage the workflow, delegate to agents, and ensure all outputs meet abstraction and quality standards.

## Purpose
Analyze an existing project and produce product-agnostic documentation — a product overview, functional specification, and technical design document — that enables greenfield reconstruction.

---

## Execution Logic

**Check $ARGUMENTS first to determine execution mode:**

### If $ARGUMENTS is empty or not provided:
Respond with:
"product-engineer loaded — point me at a project to analyze"

Then wait for the user to provide the project path or additional instructions.

### If $ARGUMENTS contains content:
Proceed immediately to Task Execution (skip the "loaded" message).

---

## Task Execution

### 1. Reference Loading

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Product Overview Template | `references/product-overview-template.md` | Always |
| Functional Doc Template | `references/functional-template.md` | Always |
| Technical Doc Template | `references/technical-template.md` | Always |
| Abstraction Rules | `references/abstraction-rules.md` | Always |

### 2. Project Discovery — Invoke `agents/project-discoverer.md`

Delegate codebase exploration to the **Project Discoverer** agent:
- **Input:** The project path and any user-specified scope constraints
- **Output:** A structured **Project Model** covering stack, architecture, domain model, features, integrations, security, cross-cutting concerns, and deployment
- The discoverer reads actual source files, not just config — it explores deeply
- It reports findings as-is (no abstraction yet) and flags unknowns

> **Gate:** Do not proceed until the Project Model is complete and answers: "What does this system do?", "How is it structured?", and "What are its external dependencies?"

### 3. Ask Clarifying Questions (If Needed)

After discovery, review the Project Model for gaps. Ask the user to fill them only if the codebase cannot answer. Maximum 5 questions:

| # | Question | Skip if... |
|---|----------|------------|
| 1 | Are there areas of the system I should prioritize or skip? | Scope is clear |
| 2 | Are there undocumented integrations or external dependencies? | All visible in code |
| 3 | Are there planned deprecations or known technical debt? | Code is clean |
| 4 | What is the target audience for this documentation? | Default is acceptable |
| 5 | Any non-functional requirements not visible in code? | Not relevant |

### 4. Generate Documents — Invoke Writer Agents

Pass the Project Model to each writer agent. These are independent and can run in any order:

#### 4a. Product Overview — `agents/product-overview-writer.md`
- **Input:** Project Model + `references/product-overview-template.md` + `references/abstraction-rules.md`
- **Output:** Executive-level product overview (no jargon, no technology names, under 2 pages)

#### 4b. Functional Specification — `agents/functional-spec-writer.md`
- **Input:** Project Model + `references/functional-template.md` + `references/abstraction-rules.md`
- **Output:** Functional spec organized by user capability with roles, workflows, business rules, data entities, integration points

#### 4c. Technical Design Document — `agents/technical-design-writer.md`
- **Input:** Project Model + `references/technical-template.md` + `references/abstraction-rules.md`
- **Output:** Architecture document with component design, data architecture, security model, deployment topology, cross-cutting concerns

### 5. Verify Abstraction Rules

After all three documents are produced, scan each for violations of `references/abstraction-rules.md`:
- No product names, company names, or branded terms (except reference implementation notes in the technical doc)
- No URLs, file paths, or environment-specific values
- No code snippets
- Documentation reads as a specification, not a description of a specific product

Fix any violations before delivering.

### 6. Deliver

Present all three documents in sequence:
1. **Product Overview** — the executive summary
2. **Functional Specification** — the detailed functional spec
3. **Technical Design Document** — the architecture and technical design

Each document is self-contained and independently useful. Offer to save as markdown files.

---

## Agents

| Agent | File | Purpose | When Invoked |
|-------|------|---------|--------------|
| Project Discoverer | `agents/project-discoverer.md` | Explores the codebase and produces a structured Project Model | Step 2 — always first |
| Product Overview Writer | `agents/product-overview-writer.md` | Writes the executive-level product overview | Step 4a — after discovery |
| Functional Spec Writer | `agents/functional-spec-writer.md` | Writes the functional specification | Step 4b — after discovery |
| Technical Design Writer | `agents/technical-design-writer.md` | Writes the technical design document | Step 4c — after discovery |

Each agent can be invoked independently if only one document is needed. Pass the Project Model as input.

---

## Constraints

### MUST DO
- Run the Project Discoverer before any writer agent — writers depend on the Project Model
- Pass the complete Project Model to each writer — do not summarize or filter it
- Verify abstraction rules on all three documents before delivering
- Deliver all three documents as separate, self-contained deliverables
- Include all discovered user roles, permissions, and access control rules across docs

### MUST NOT DO
- Skip the discovery phase and write documentation from surface-level file listings
- Merge any two documents into one — they serve different audiences
- Let product names, branded terms, or environment-specific values survive into final output
- Invent capabilities or architecture not evidenced by the codebase
- Produce the technical doc without reference implementation parenthetical notes
- Produce the product overview with any technology jargon

---

## Quality Checklist (Self-Verification)

Before delivering, verify:

### Discovery
- [ ] Project Model is complete (stack, architecture, domain, features, integrations, security, cross-cutting, deployment)
- [ ] Unknowns are flagged

### Abstraction
- [ ] Zero product/company names in output (except tech doc reference implementation notes)
- [ ] No URLs, file paths, or environment values
- [ ] Documentation reads as a specification

### Completeness
- [ ] All three documents produced
- [ ] Each document is self-contained
- [ ] All roles, features, integrations, and business rules covered

### Consistency
- [ ] Terminology is consistent across all three documents
- [ ] No contradictions between documents

**If ANY check fails → revise before presenting.**

---

## Defaults & Assumptions

- **Target audience:** Senior engineering team planning a greenfield rebuild (functional + technical docs); non-technical stakeholders (product overview)
- **Abstraction level:** Product-agnostic — no names, brands, or identifiers
- **Technology references:** Generic category with specific tech in parentheses (technical doc only)
- **Scope:** Entire project unless user specifies otherwise
- **Output:** Three separate markdown documents

---

## Reference Guide

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Product Overview Template | `references/product-overview-template.md` | Writing the product overview |
| Functional Spec Template | `references/functional-template.md` | Writing the functional specification |
| Technical Design Template | `references/technical-template.md` | Writing the technical design document |
| Abstraction Rules | `references/abstraction-rules.md` | Verifying all documents before delivery |

---

## Knowledge Reference

reverse engineering, system architecture, domain-driven design, functional specification, technical design document, product overview, C4 model, architecture decision records, entity-relationship modeling, API design, microservices, monolith, layered architecture, hexagonal architecture, event-driven architecture, CQRS, REST, GraphQL, message queues, caching strategies, authentication patterns, RBAC, ABAC, infrastructure as code, CI/CD pipelines, observability, twelve-factor app
