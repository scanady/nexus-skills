# Skill Catalog Taxonomy Migration Plan — v3

## Overview

This document covers the full set of changes needed to migrate the nexus-agents skill catalog from the current taxonomy to the revised structure. It includes domain-level changes, a complete skill rename table, and notes on skills that required judgment calls.

## What changed and why

**`tech` renamed to `engineering`**
Aligns with Anthropic's own Cowork plugin naming convention. `engineering` is more precise than `tech` and matches how practitioners refer to the discipline. All `tech-*` skills rename to `engineering-*`.

**`devops` split from `engineering`**
DevOps, security, and incident response attract meaningfully different user intent from software development and architecture. Splitting `devops` into its own top-level domain reduces `engineering` to a manageable size and gives infrastructure practitioners a clear landing spot.

**`strategy` split: market and research intelligence moved to `research`**
`strategy` had 14 skills spanning decisions, frameworks, planning, market research, and competitor intelligence. Market and competitive research is a research behavior, not a strategy behavior. Moving those skills to `research` tightens `strategy` and gives `research` more catalog weight.

**`ai` and `agents` as separate top-level domains**
`ai` covers the practitioner layer: prompt engineering, ML pipelines, RAG, AI product work. `agents` covers the meta-layer: building skills, designing agent personas, writing copilot instructions, plugin building, spec building. The stray `agent-*` and `prompt-*` prefixes are absorbed accordingly.

**`knowledge` as a standalone domain**
Knowledge management is a distinct user intent that does not fit cleanly into `research` or `productivity`. Starts thin but provides a clear home for `knowledge-ops`, `knowledge-context-curator`, and future skills in this space.

**`comms` collapsed into `people`**
With only two skills, `comms` did not warrant a top-level slot. Internal communications belongs naturally under People & Talent as `people-comms`.

**`legal` restored as standalone top-level domain**
Legal has distinct enough user intent to warrant its own domain regardless of catalog weight.

**`finance` split into `finance` and `financial-analysis`**
`finance` covers operational finance: reporting, accounting, close management, audit, budgeting. `financial-analysis` covers the analytical layer: modeling, forecasting, variance analysis, market and investment research. Mirrors Anthropic's own plugin split between `finance` and `financial-analysis`. Both start thin; the split supports future growth without requiring a taxonomy revision.

**`ops` scoped to core operations**
No longer absorbs legal or finance. Covers process documentation, capacity planning, risk, and vendor management.

**Stray skills reclassified**
See the rename table below for full details on `frontend-design-impactful`, `personal-communication-style`, `knowledge-ops`, and `thinking-get-unstuck`.

**Hero skill note**
`thinking-get-unstuck` retains its name by design. It is a hero skill — memorable, shareable, and intentionally outside the taxonomy convention. It lives under `strategy-decision` in the taxonomy but should be discoverable by its full name as a slash command. If a short alias system is implemented, this is the first candidate.

## Domain summary — before and after

| Before | Prefix | Skills | After | Prefix |
|---|---|---|---|---|
| Technology | `tech` | 22 | Engineering | `engineering` |
| — | — | — | DevOps | `devops` |
| Strategy & Business | `strategy` | 14 | Strategy & Business | `strategy` |
| — | — | — | Research & Intelligence | `research` |
| Marketing | `marketing` | 13 | Marketing | `marketing` |
| Design | `design` | 10 | Design | `design` |
| Data & Analytics | `data` | 8 | Data & Analytics | `data` |
| Content & Writing | `content` | 8 | Content & Writing | `content` |
| Product | `product` | 8 | Product | `product` |
| Research | `research` | 5 | (absorbed into research domain above) | — |
| — | — | — | AI | `ai` |
| — | — | — | Agents | `agents` |
| — | — | — | Knowledge | `knowledge` |
| — | — | — | Finance | `finance` |
| — | — | — | Financial Analysis | `financial-analysis` |
| People & Talent | `people` | 0 | People & Talent | `people` |
| Productivity | `productivity` | 1 | Productivity | `productivity` |
| Sales | `sales` | 2 | Sales | `sales` |
| Operations | `ops` | 1 | Operations | `ops` |
| Project Management | `project` | 0 | Project Management | `project` |
| Legal | `legal` | 1 | Legal | `legal` |

## Complete skill rename table

### Engineering — renamed from `tech`

All `tech-*` skills rename to `engineering-*`. Sub-category mappings are preserved.

| Old name | New name |
|---|---|
| `tech-arch-architecture-decision-records` | `engineering-arch-architecture-decision-records` |
| `tech-arch-principle-engineer` | `engineering-arch-principle-engineer` |
| `tech-arch-system-designer` | `engineering-arch-system-designer` |
| `tech-dev-git-commit` | `engineering-dev-git-commit` |
| `tech-dev-git-finish-branch` | `engineering-dev-git-finish-branch` |
| `tech-dev-git-start-branch` | `engineering-dev-git-start-branch` |
| `tech-dev-git-workflow-design` | `engineering-dev-git-workflow-design` |
| `tech-dev-writing-plans` | `engineering-dev-writing-plans` |
| `tech-quality-code-simplifier` | `engineering-quality-code-simplifier` |
| `tech-quality-receiving-review` | `engineering-quality-receiving-review` |
| `tech-quality-requesting-review` | `engineering-quality-requesting-review` |
| `tech-quality-tdd` | `engineering-quality-tdd` |
| `tech-api-mcp-builder` | `engineering-api-mcp-builder` |
| `tech-api-n8n-workflow-builder` | `engineering-api-n8n-workflow-builder` |
| `tech-doc-markdown-to-pdf` | `engineering-doc-markdown-to-pdf` |
| `tech-github-ops` | `engineering-github-ops` |
| `tech-github-repo-standards` | `engineering-github-repo-standards` |
| `tech-feature-forge` | `engineering-feature-forge` |
| `tech-legacy-modernizer` | `engineering-legacy-modernizer` |
| `tech-data-scraper` | `engineering-data-scraper` |
| `tech-database-optimizer` | `engineering-database-optimizer` |

### DevOps — split from `engineering`

| Old name | New name |
|---|---|
| `tech-devops-engineer` | `devops-infra-engineer` |
| `tech-devops-incident-responder` | `devops-incident-responder` |
| `tech-security-audit-lead` | `devops-security-audit-lead` |
| `tech-security-vulnerability-analyst` | `devops-security-vulnerability-analyst` |

### Research — absorbs strategy market and intel skills

| Old name | New name |
|---|---|
| `strategy-market-competitor-intel` | `research-market-competitor-intel` |
| `strategy-market-researcher` | `research-market-researcher` |
| `strategy-research-analyst` | `research-market-analyst` |
| `strategy-research-opportunity` | `research-market-opportunity` |
| `strategy-persona-builder` | `research-market-persona-builder` |

### Agents — new domain, absorbs stray agent and prompt skills

| Old name | New name |
|---|---|
| `agent-design-persona-creator` | `agents-design-persona-creator` |
| `agent-design-visual-identity` | `agents-design-visual-identity` |
| `agent-skill-copilot-instructions` | `agents-copilot-instructions` |
| `agent-skill-plugin-builder` | `agents-skill-plugin-builder` |
| `agent-skill-spec-builder` | `agents-skill-spec-builder` |
| `prompt-engineer` | `ai-prompt-engineer` |
| `prompt-optimizer` | `ai-prompt-optimizer` |

### People — absorbs comms skills

| Old name | New name |
|---|---|
| `comms-announce-organizational` | `people-comms-announce-organizational` |
| `comms-engage-internal-community` | `people-comms-engage-internal-community` |

### Legal — prefix unchanged, now standalone domain

| Old name | New name |
|---|---|
| `legal-compliance-regulatory-monitor` | `legal-compliance-regulatory-monitor` |

No rename needed. Prefix already correct.

### Design — absorbs stray frontend skill

| Old name | New name |
|---|---|
| `frontend-design-impactful` | `design-web-impactful` |

### Productivity — absorbs personal skills

| Old name | New name |
|---|---|
| `personal-communication-style` | `productivity-personal-communication-style` |

### Knowledge — prefix unchanged, now formal domain

| Old name | New name |
|---|---|
| `knowledge-ops` | `knowledge-ops` |

No rename needed. Note: `knowledge-context-curator` (in development) should publish as `knowledge-context-curator`.

### Hero skill — no rename

| Skill | Taxonomy home | Notes |
|---|---|---|
| `thinking-get-unstuck` | `strategy-decision` | Name retained intentionally. Does not follow prefix convention. First candidate for a hero alias system if implemented. |

## Skills with no change required

The following skills require no rename. Their prefixes already match the revised taxonomy.

```
content-behavioral-nudge-unit
content-copy-caveman
content-copy-clear-writing
content-copy-critical-writing
content-copy-email-sequences
content-copy-email-template-builder
content-copy-executive-writing
content-copy-humanizer
content-style-extractor
content-technical-doc-coauthoring
content-technical-onboarding-docs
data-ai-autoresearch
data-ai-ml-pipeline
data-ai-ml-rag-architect
data-ai-post-training-expert
data-ai-product-specialist
data-analysis-business-performance
data-eng-database-architect
data-eng-pandas-specialist
data-eng-pipeline-architect
design-application-sitemap
design-application-ux
design-product-overview-builder
design-product-overview-recorder
design-research-ux-artifacts
design-research-ux-researcher
design-scroll-storytelling
design-system-architect
design-ui-system-advisor
design-visual-image-generator
design-visual-image-system-director
marketing-brand-strategist
marketing-campaign-go-to-market
marketing-campaign-ideas
marketing-campaign-product-hunt-launch
marketing-campaign-psychology
marketing-content-brand-copywriter
marketing-content-engine
marketing-content-lead-magnet
marketing-content-linkedin-writer
marketing-content-viral-hook
marketing-content-x-thread-builder
marketing-customer-segmentation
marketing-seo-adsense-readiness
marketing-seo-adsense-review
marketing-seo-cro
ops-process-sop-creator
product-discovery-spec-toolkit
product-spec-brainstorming
product-spec-game-changing-features
product-spec-prd-generator
product-spec-reverse-engineer
product-strategy-okr-specialist
product-strategy-validator
product-vision-strategy
productivity-daily-meeting-notes
research-ai-landscape-brief
research-analyst
research-deep-reading-analyst
research-dtc-insurance-market-intelligence
research-weekly-ai-news
sales-outreach-specialist
sales-pipeline-revops
strategy-change-management
strategy-critical-reasoning
strategy-decision-council
strategy-decision-documenter
strategy-decision-interrogator
strategy-exec-presentation-designer
strategy-frameworks-mckinsey-brief
strategy-innovation-catalyst
strategy-planning-opportunity
strategy-planning-pricing
strategy-planning-startup
```

## Execution steps

1. Replace `taxonomy.yaml` with `taxonomy-revised.yaml` in the repository root.
2. For each skill in the rename table above, rename the directory to the new skill name.
3. Update the `name` field in each renamed skill's `SKILL.md` frontmatter to match the new directory name.
4. Update any internal cross-references between skills if skills reference each other by name.
5. If the platform registers slash commands from directory names or SKILL.md frontmatter, trigger a full re-index after all renames are complete.
6. Verify `thinking-get-unstuck` surfaces correctly under `strategy` in any browse or filter UI. No rename needed but confirm slash command discoverability.
7. Publish `knowledge-context-curator` under `knowledge-context-curator` when ready.

## Open questions

**Slash command aliases**
If the platform supports aliases, `thinking-get-unstuck` should get `/unstuck` as the first test of a hero skill pattern before building more.

**`design-application-*` and `design-product-*` sub-prefixes**
Skills like `design-application-sitemap`, `design-application-ux`, `design-product-overview-builder`, and `design-product-overview-recorder` use sub-prefixes that predate the `design-app` category. They are functionally correct under the `design` domain. Consider renaming to `design-app-*` in a follow-on pass for consistency, or leave as-is.

**`research-analyst` and `research-deep-reading-analyst`**
These use the `research-` prefix without a sub-category segment. They fit `research-general`. Consider adding the sub-category in a follow-on pass.

**`data-ai-*` skills**
The `data-ai-*` cluster (`data-ai-autoresearch`, `data-ai-ml-pipeline`, `data-ai-ml-rag-architect`, `data-ai-post-training-expert`, `data-ai-product-specialist`) sit under `data` today. As the `ai` domain grows, consider whether these belong under `ai-model` and `ai-rag` instead. Leave as-is for now but watch for user confusion between `data` and `ai` for ML-oriented skills.