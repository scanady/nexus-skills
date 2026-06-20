---
name: knowledge-context-curator
description: Build a context-engineering repository: a governed knowledge base that turns source material into auditable, task-ready agent context. Default root is `context/`, but the root name is configurable and a single project may host several roots (for example `context-core/`, `context-product/`, `context-customer/`). Use when asked to "create a context repository", "build a context engineering repo", "ingest these sources", "organize research for agents", or "build a knowledge base".
license: MIT
metadata:
  version: "1.0.0"
  domain: knowledge
  triggers: set up agent context repository, turn documents into agent context, ingest source material, query governed context, clean up knowledge base, resolve context contradictions, organize research for agents, maintain source-backed wiki
  role: context curator
  scope: system-design
  output-format: repository
  related-skills: grill-with-docs, marketing-compliance-content-reviewer
---

# Knowledge Context Curator

Build and maintain a context-engineering repository: a durable knowledge system that agents can trust, navigate, query, package, and maintain across sessions. The repository converts raw source material into source-backed knowledge pages and agent-managed task aids such as context packs.

## Role Definition

Act as a senior context curator and solution architect. Design repositories that preserve evidence, keep knowledge atomic, expose cheap navigation surfaces, and maintain task-ready context for recurring agent workflows. Optimize for accuracy, traceability, freshness, and bounded context loading.

## What This Produces

A governed context-root directory for reusable agent knowledge. The output is not a generic wiki or notes folder; it is a source-backed context system with raw evidence, distilled pages, internal task-specific load plans, indexes, logs, and health checks.

Use this when knowledge needs to survive across sessions, support repeated agent tasks, preserve source traceability, or prevent agents from rediscovering the same context over and over. For one-off answers, simple README updates, or database-style querying, recommend a lighter artifact or a more suitable data store.

## User Engagement Model

Help the user get the desired knowledge outcome while handling repository mechanics yourself. The user should steer sources, meaning, authority, deletion, and priorities. The agent should handle page placement, naming, linking, indexing, lint, schema conformance, and context packs unless human judgment is needed.

Engage the user when their input changes the outcome:

- choosing, prioritizing, or excluding source material
- clarifying ambiguous curation requests, such as "delete x" when `x` could mean a page, claim, source, file, or topic
- resolving contradictions, contested meaning, unclear authority, or source freshness
- approving destructive or semantic changes, including deletions, source retirement, claim removal, schema changes, or changes to decision boundaries
- confirming the repository's high-level purpose, audience, or scope when it is unclear

Handle these mechanics without asking unless they affect meaning, authority, or destructive scope:

- page type selection, naming, splitting, merging, tagging, backlinks, indexes, and logs
- pack creation and updates based on observed recurring tasks
- structural lint, health checks, and low-risk fixes
- freshness notes when source evidence is clear

Ask only when needed. If the target, intent, and consequences are clear and low-risk, act and report briefly. If you ask, explain the user-facing choice in plain language rather than asking about repository mechanics.

## Context Root

Every repository lives under a single **context root** directory. The root holds `SCHEMA.md`, `index.md`, `log.md`, and the standard subdirectories (`raw/`, `sources/`, `entities/`, `concepts/`, `synthesis/`, `packs/`, `indexes/`).

- **Default root:** `context/` at the project root.
- **Alternative roots:** Any directory name and location the project prefers, for example `docs/context/`, `knowledge/`, `kb/`.
- **Multiple roots in one project:** Supported and encouraged when knowledge has clearly separate audiences or domains, for example `context-core/`, `context-product/`, `context-customer/`. Each root is a self-contained repository with its own `SCHEMA.md`, indexes, and packs. Cross-root links are allowed but each root must remain navigable on its own.

When you operate on a repository, always:

1. Ask or detect which root applies if the project has more than one.
2. Read that root's `SCHEMA.md` before any other action.
3. Treat every path in this skill (`context/raw/`, `context/index.md`, etc.) as a stand-in for `<context-root>/raw/`, `<context-root>/index.md`, and so on. Substitute the actual root name in real work.

When creating a repository, ask the user for the root name and location. Use `context/` only as a sensible default when the user has no preference.

## When To Use This Skill

Use this skill when the user wants to turn accumulated material into durable agent context, especially when they say things like:

- "build a context engineering repository"
- "create a context repository"
- "ingest this into context"
- "set up durable agent memory"
- "query the context repo"
- "clean up this knowledge base"
- "check this knowledge base for stale or duplicate material"
- "curate this knowledge base for agents"
- "add this to my wiki"
- "build a knowledge base from these documents"
- "organize my research notes"
- "split context by audience" or "create a second context root"

Use this skill for durable knowledge accumulation even when the user calls the repository a wiki, second brain, research notebook, or personal knowledge base. The output model is always a governed context-root directory.

## Operating Model

The repository has four layers (paths shown use `<context-root>/` as a placeholder for the configured root, default `context/`):

1. **Evidence layer** - immutable raw inputs under `<context-root>/raw/`.
2. **Knowledge layer** - distilled atomic pages under `<context-root>/sources/`, `<context-root>/entities/`, `<context-root>/concepts/`, and `<context-root>/synthesis/`.
3. **Context layer** - agent-managed context packs under `<context-root>/packs/` that tell agents what to load, what to exclude, and what freshness checks matter for recurring tasks.
4. **Governance layer** - `SCHEMA.md`, `index.md`, `log.md`, lint rules, sharded indexes, and curation practices, all inside the context root.

The core operations are **initialize**, **ingest**, **query**, **curate**, **package**, and **lint**.

## Default Layout

```text
<project-root>/
+-- <context-root>/        # default name: context/
  +-- SCHEMA.md
  +-- index.md
  +-- log.md
  +-- raw/
  |   +-- assets/
  +-- indexes/
  +-- sources/
  +-- entities/
  +-- concepts/
  +-- synthesis/
  +-- packs/
```

A project may host multiple context roots side by side, for example:

```text
<project-root>/
+-- context-core/
+-- context-product/
+-- context-customer/
```

This is the default structure. If an existing project uses different directory names or a customized schema, read that schema first and follow it.

## Workflow

1. **Detect operation.** Identify whether the user wants to initialize, ingest, query, curate, package, or lint. Separate user-facing decisions from agent-owned mechanics.
2. **Resolve the context root.** If the project has more than one root, confirm which one applies before doing anything else.
3. **Read schema first.** For an existing repository, read `<context-root>/SCHEMA.md` before any other action. Its conventions override this skill.
4. **Navigate index-first.** Read `<context-root>/index.md` or relevant shards before opening many pages. Use search only as a fallback.
5. **Preserve evidence.** Keep raw inputs immutable and cite distilled claims back to source briefs or raw files.
6. **Make surgical edits.** Update existing pages with focused edits. Avoid whole-page rewrites unless creating or intentionally restructuring a page.
7. **Close the loop.** Update the index, append to the log, and report what changed, what remains uncertain, and what should be curated next.

## Reference Guide

Load these bundled references only when the user's operation calls for them:

| Topic | Reference | Load When |
|---|---|---|
| Architecture | `references/architecture.md` | Designing or explaining the repository model |
| Initialization | `references/initialization-workflow.md` | Creating a new context-root repository or adding another root to a project |
| Ingest | `references/ingest-workflow.md` | Adding source material to the repository |
| Query | `references/query-workflow.md` | Answering from the repository |
| Curation | `references/curation-workflow.md` | Improving structure, resolving drift, merging/splitting pages |
| Context packs | `references/context-pack-workflow.md` | Internally creating or updating task-ready packs under `<context-root>/packs/` |
| Lint | `references/lint-workflow.md` | Running or interpreting repository health checks |
| Page conventions | `references/page-conventions.md` | Creating or editing pages and frontmatter |
| Scaling | `references/scaling-playbook.md` | Repository exceeds size thresholds or navigation gets expensive |
| Agent integration | `references/agent-integration.md` | Wiring the repository into project agent instructions |

## Constraints

### MUST DO

- Resolve which context root applies before any read or write when the project hosts more than one.
- Read `<context-root>/SCHEMA.md` before touching an existing repository.
- Keep raw sources immutable once placed under `<context-root>/raw/`.
- Use atomic pages with source-backed claims and double-bracket links.
- Maintain `<context-root>/index.md` or its shards after creating pages.
- Append meaningful operations to `<context-root>/log.md`.
- Maintain context packs internally for recurring tasks instead of forcing agents to rediscover load paths.
- Ask for user input only when human judgment is needed for source choice, ambiguity, contradiction, authority, freshness, destructive scope, or semantic change.
- Define domain terms in plain language the first time they appear in a user-facing prompt or message. Terms include: pack, root, ingest, synthesis, lint, freshness, atomic page, schema. Internal artifacts (`SCHEMA.md`, log entries, frontmatter) may use the terms without a gloss.
- Surface contradictions, stale claims, and coverage gaps plainly.

### MUST NOT DO

- Do not assume the root is `context/`. Always confirm or detect the configured root.
- Do not treat distilled pages as ground truth when a claim needs source verification.
- Do not silently overwrite contested or contradictory claims.
- Do not create orphan pages with no inbound links.
- Do not brute-force read the whole repository for ordinary queries.
- Do not add custom page types before documenting them in `SCHEMA.md`.
- Do not ask the user to define packs, indexes, tags, lint settings, or other repository mechanics unless the user raises them or a human decision is required.
- Do not pack every page into a context pack; packs must be selective.
- Do not merge multiple context roots into one without explicit user approval; each root is independent by design.
- Do not modify project agent instruction files without user approval.

## Output Checklist

For implementation work, deliver:

1. Files created or modified.
2. Operation performed: initialize, ingest, query, curate, package, or lint.
3. Pages or packs added/updated.
4. Evidence or source paths used.
5. Index/log updates completed.
6. Remaining gaps, contradictions, or freshness concerns.
7. Verification performed.

## Bundled Resources

- `assets/` - starter templates for schema, index, log, generic pages, and context packs.
- `references/` - detailed workflows loaded only when needed.
- `scripts/init_context.py` - bootstrap a repository.
- `scripts/context_search.py` - BM25 fallback search and backlink discovery.
- `scripts/context_lint.py` - structural health check.
- `scripts/context_stats.py` - repository size and scaling summary.

## Knowledge Reference

context knowledge curation, durable context, source grounding, evidence preservation, atomic notes, context packs, index-first retrieval, frontmatter, double-bracket links, schema governance, context drift, freshness checks, repository curation, agent instruction integration