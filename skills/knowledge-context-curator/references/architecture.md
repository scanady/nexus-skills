# Architecture

This reference explains the repository model. Use it when designing, explaining, or revising a context-root repository.

Paths below use `context/` as the default root name for readability. The root is configurable, and a project may host several roots side by side (for example `context-core/`, `context-product/`, `context-customer/`). Substitute the actual root name where it applies.

## Four Layers

### Evidence Layer

The evidence layer is immutable source material under `context/raw/`. It may contain PDFs, markdown captures, transcripts, exported notes, screenshots, or other files the user wants future agents to rely on. Agents may read these files but should not edit them after placement.

The evidence layer is the audit anchor. If a distilled claim becomes questionable, the agent can trace it back to the source brief and then to the raw source.

### Knowledge Layer

The knowledge layer is made of distilled markdown pages:

- `context/sources/` - source briefs, one per ingested source.
- `context/entities/` - people, products, organizations, systems, documents, locations, or other specific things.
- `context/concepts/` - rules, methods, ideas, frameworks, terms, and domain abstractions.
- `context/synthesis/` - cross-source analyses, comparisons, durable query answers, and open-question summaries.

These pages are atomic. Each page should be about one thing, stay small enough to load confidently, and cite the sources it draws from.

### Context Layer

The context layer is what makes the repository task-ready. Pages under `context/packs/` define load plans for recurring agent work. A pack tells an agent what to read first, what can be skipped, what is stale or risky, and what boundaries apply.

Use packs for repeated workflows such as compliance review, PRD drafting, customer-call synthesis, architecture review, research briefing, or support-answer generation.

### Governance Layer

The governance layer keeps the repository maintainable:

- `SCHEMA.md` defines conventions and overrides defaults.
- `index.md` gives cheap navigation.
- `indexes/` holds shards when the top-level index grows.
- `log.md` records operations.
- lint scripts and curation workflows catch drift before it compounds.

## Core Operations

### Initialize

Create the default directory structure, seed templates, document conventions, and optionally wire the repository into project-level agent instructions with user approval.

### Ingest

Add a source to `context/raw/`, distill it into a source brief, update related pages, create new pages when warranted, update indexes, and append to the log.

### Query

Answer a user question by navigating index-first, reading only relevant pages, surfacing uncertainty, and optionally filing substantive synthesis back into `context/synthesis/`.

### Curate

Maintain quality: split oversized pages, merge duplicates, resolve contradictions, tighten summaries, prune tags, update schema conventions, and improve links.

### Package

Create or update task-specific context packs. Packs are selective load plans, not dumps of everything known.

### Lint

Run structural checks and perform semantic review for drift, contradictions, stale pages, missing source links, and pack freshness issues.

## Why Markdown

Markdown is portable, reviewable in git, easy for humans to inspect, and cheap for agents to read. This model is best for curated knowledge and reusable context, not for high-volume transactional data or complex relational queries. If the user's primary need is database-style querying, recommend a database or graph store rather than forcing markdown to do the wrong job.