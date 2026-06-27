# Portable Agent Taxonomy

Use this bundled taxonomy when no project-specific taxonomy is supplied. If the user or target project provides a different taxonomy, use that taxonomy instead and record the source in the output.

## Naming Rules

- Reusable catalog skills use `<category-prefix>-<descriptor>`.
- The category prefix must come from the governing taxonomy.
- `metadata.domain` uses the top-level domain prefix, not the category prefix.
- Plugin-local private skills may use shorter names, but record their taxonomy home for future promotion.
- Hero-name exceptions must be explicit and documented.

## Default Prefixes

| Domain | Domain Prefix | Category Prefixes |
|---|---|---|
| Marketing | `marketing` | `marketing-content`, `marketing-brand`, `marketing-campaign`, `marketing-seo`, `marketing-intel` |
| Sales | `sales` | `sales-outreach`, `sales-pipeline`, `sales-call`, `sales-intel`, `sales-cs` |
| Content & Writing | `content` | `content-copy`, `content-technical`, `content-story`, `content-visual`, `content-behavioral`, `content-style` |
| Design | `design` | `design-research`, `design-visual`, `design-delivery`, `design-copy`, `design-app`, `design-web` |
| Engineering | `engineering` | `engineering-arch`, `engineering-dev`, `engineering-quality`, `engineering-api`, `engineering-doc`, `engineering-github` |
| DevOps | `devops` | `devops-infra`, `devops-security`, `devops-incident`, `devops-deploy` |
| Data & Analytics | `data` | `data-analysis`, `data-visual`, `data-eng`, `data-ai` |
| AI | `ai` | `ai-prompt`, `ai-product`, `ai-rag`, `ai-model`, `ai-research` |
| Agents | `agents` | `agents-skill`, `agents-design`, `agents-copilot`, `agents-catalog` |
| Product | `product` | `product-spec`, `product-strategy`, `product-discovery`, `product-roadmap`, `product-stakeholder` |
| Strategy & Business | `strategy` | `strategy-decision`, `strategy-planning`, `strategy-frameworks`, `strategy-change`, `strategy-thought`, `strategy-innovation`, `strategy-tech` |
| Research & Intelligence | `research` | `research-market`, `research-intel`, `research-docs`, `research-general` |
| Knowledge | `knowledge` | `knowledge-ops`, `knowledge-context`, `knowledge-docs` |
| Project Management | `project` | `project-planning`, `project-tracking`, `project-agile`, `project-reporting` |
| People & Talent | `people` | `people-recruiting`, `people-onboarding`, `people-performance`, `people-org`, `people-comms`, `people-culture`, `people-learning` |
| Operations | `ops` | `ops-process`, `ops-capacity`, `ops-risk`, `ops-vendor` |
| Legal | `legal` | `legal-contracts`, `legal-compliance`, `legal-risk`, `legal-comms` |
| Finance | `finance` | `finance-reporting`, `finance-close`, `finance-audit`, `finance-budget` |
| Financial Analysis | `financial-analysis` | `financial-analysis-modeling`, `financial-analysis-performance`, `financial-analysis-market`, `financial-analysis-narrative` |
| Productivity | `productivity` | `productivity-tasks`, `productivity-meetings`, `productivity-personal`, `productivity-daily`, `productivity-ideas`, `productivity-memory` |

## Legacy Prefix Mapping

- `agent-*` -> `agents-*`
- `prompt-*` -> `ai-prompt-*`
- `tech-*` -> `engineering-*` or `devops-*`
- `comms-*` -> `people-comms-*`
- `personal-*` -> `productivity-personal-*`