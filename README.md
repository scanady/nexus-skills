# Skills pack

This repository contains skills, prompts, agents, and instructions.

## Installation

### Via npx (recommended)

```bash
npx skills add https://github.com/scanady/forge-agents
```

Install a specific skill:

```bash
npx skills add https://github.com/scanady/forge-agents --skill product-spec-prd-generator
```

### Local install (from cloned repo)

```bash
git clone https://github.com/scanady/forge-agents
cd forge-agents
```

Install all skills globally (default agent: GitHub Copilot):

```bash
node bin/cli.js install
```

Install a specific skill to a specific agent:

```bash
node bin/cli.js install --skill content-copy-humanizer -a claude-code
```

Install to multiple agents at once:

```bash
node bin/cli.js install -a github-copilot -a claude-code -a codex
```

Install to the current project instead of globally:

```bash
node bin/cli.js install --skill product-spec-prd-generator -p
```

List available skills:

```bash
node bin/cli.js list
```

**Supported agents:**

| Agent | Global path | Project path |
|-------|------------|--------------|
| `github-copilot` (default) | `~/.copilot/skills/` | `.agents/skills/` |
| `claude-code` | `~/.claude/skills/` | `.claude/skills/` |
| `codex` | `~/.codex/skills/` | `.agents/skills/` |

## Usage

After installation, use skills by typing:

```
/skill-builder create a new skill for drafting weekly status updates
```

```
/tech-api-mcp-builder build an MCP server for the GitHub API with issues and PR tools
```

## Available Skills

### Marketing
- `marketing-content-brand-copywriter` - Writes marketing copy using proven copywriting frameworks for ads, landing pages, emails, and social content.
- `marketing-intel-competitor` - Analyzes competitors using web research to provide verified business metrics and actionable leverage strategies.
- `marketing-seo-cro` - Audits landing pages against proven CRO principles and delivers actionable recommendations to maximize conversions.
- `marketing-campaign-go-to-market` - Delivers the 3 best go-to-market strategies tailored to the founder's current stage, product, and market.
- `marketing-campaign-ideas` - Produces the best marketing ideas by matching business context against a database of 170+ proven strategies.
- `marketing-content-lead-magnet` - Creates viral lead magnet posts that drive comments and DMs in quick and detailed formats.
- `marketing-content-linkedin-writer` - Creates viral LinkedIn posts using proven formats, post templates, and voice matching.
- `sales-outreach-specialist` - Crafts high-converting outreach messages and email sequences for cold outreach and LinkedIn DMs.
- `strategy-planning-pricing` - Builds comprehensive pricing strategies, tier structures, and price point recommendations interactively.
- `marketing-campaign-product-hunt-launch` - Creates a comprehensive, personalized Product Hunt launch plan to rank #1.
- `marketing-content-viral-hook` - Creates viral social media hooks using proven psychological patterns and trigger words.
- `marketing-content-x-writer` - Creates viral X (Twitter) posts using proven formats and creator voice matching.

### Technology
- `tech-api-mcp-builder` - Guides creation of high-quality MCP servers that enable LLMs to interact with external services.
- `tech-quality-code-simplifier` - Simplifies and refines code for clarity, consistency, and maintainability while preserving all functionality.
- `tech-dev-finishing-branch` - Guides completion of development work by presenting structured options for merge, PR, or cleanup.
- `product-spec-prd-generator` - Generates professional PRD files optimized for AI coding tools from rough product ideas.
- `tech-quality-receiving-review` - Guides rigorous, technical evaluation of incoming code review feedback before implementation.
- `tech-quality-requesting-review` - Dispatches a code review subagent to verify work meets requirements before merging.
- `tech-quality-tdd` - Enforces test-first development by writing tests before implementation code on any feature or bugfix.
- `tech-dev-writing-plans` - Creates structured implementation plans from specs or requirements before touching code.

### Design
- `marketing-content-product-overview-page` - Builds polished product overview pages with automated screenshot capture and modern SaaS design patterns.
- `design-research-personas` - Creates UX/UI design artifacts from research through specs, including personas, journey maps, and interaction behaviors.

### Content
- `content-technical-doc-coauthoring` - Guides users through a structured workflow for co-authoring documentation, proposals, and technical specs.
- `content-copy-humanizer` - Removes signs of AI-generated writing by detecting and fixing 26 AI writing patterns.
- `comms-announce-organizational` - Drafts professional internal announcements for promotions, new hires, restructures, and leadership transitions.
- `productivity-daily-meeting-notes` - Creates clear, structured, distribution-ready meeting minutes with decisions, action items, and next steps.

### Strategy
- `product-spec-brainstorming` - Explores user intent, requirements, and design space before implementation on any creative or technical task.
- `marketing-intel-customer-segmentation` - Builds data-driven customer segment personas using hybrid qualitative and quantitative analysis methods.
- `marketing-brand-strategist` - Expert brand naming and domain strategy for businesses, products, apps, and ventures.
- `strategy-frameworks-mckinsey-brief` - Builds executive-ready strategic briefs using SCQ, MECE issue trees, and pyramid-structured recommendations.
- `content-behavioral-nudge-unit` - Applies nudge theory and choice architecture to design System 1 and System 2 behavioral interventions.
- `strategy-planning-startup` - Delivers the 3 highest-impact next moves for growth by analyzing the founder's business context and bottlenecks.

### Monetization
- `marketing-seo-adsense-readiness` - Analyzes websites for Google AdSense policy compliance before applying for monetization.
- `marketing-seo-adsense-review` - Performs a comprehensive live-site review mimicking the Google AdSense approval process.

### Tooling
- `agent-skill-copilot-instructions` - Creates expertly crafted GitHub Copilot custom instructions files tailored to specific domains and repositories.
- `agent-skill-plugin-builder` - Creates knowledge-work plugins through a guided design process, bundling skills, commands, and connectors.
- `product-spec-reverse-engineer` - Performs a thorough project review and produces product overview, functional specification, and technical design documents for greenfield rebuilding.
- `agent-skill-writer` - Guides creating, editing, verifying, and testing skills before deployment.
- `ops-process-sop-creator` - Creates detailed Standard Operating Procedures for repeatable business processes.

## Contributing

Want to add a new skill? See [SKILL.md](SKILL.md) for development guidelines.

### Skill Structure

```
skills/
└── your-skill/
    ├── SKILL.md        # Main skill definition
    └── references/     # Additional reference materials
```

