# Skills pack

This repository contains skills, prompts, agents, and instructions.

## Installation

### Via npx (recommended)

```bash
npx skills add https://github.com/scanady/forge-agents
```

Install a specific skill:

```bash
npx skills add https://github.com/scanady/forge-agents --skill tech-prd-generator
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
node bin/cli.js install --skill humanizer -a claude-code
```

Install to multiple agents at once:

```bash
node bin/cli.js install -a github-copilot -a claude-code -a codex
```

Install to the current project instead of globally:

```bash
node bin/cli.js install --skill tech-prd-generator -p
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
/mcp-builder build an MCP server for the GitHub API with issues and PR tools
```

## Available Skills

### Marketing
- `marketing-brand-copywriter` - Writes marketing copy using proven copywriting frameworks for ads, landing pages, emails, and social content.
- `marketing-competitor-intel` - Analyzes competitors using web research to provide verified business metrics and actionable leverage strategies.
- `marketing-cro-optimization` - Audits landing pages against proven CRO principles and delivers actionable recommendations to maximize conversions.
- `marketing-go-to-market-plan` - Delivers the 3 best go-to-market strategies tailored to the founder's current stage, product, and market.
- `marketing-ideas` - Produces the best marketing ideas by matching business context against a database of 170+ proven strategies.
- `marketing-lead-magnet-generator` - Creates viral lead magnet posts that drive comments and DMs in quick and detailed formats.
- `marketing-linkedin-writer` - Creates viral LinkedIn posts using proven formats, post templates, and voice matching.
- `marketing-outreach-specialist` - Crafts high-converting outreach messages and email sequences for cold outreach and LinkedIn DMs.
- `marketing-pricing-strategist` - Builds comprehensive pricing strategies, tier structures, and price point recommendations interactively.
- `marketing-product-hunt-launch-plan` - Creates a comprehensive, personalized Product Hunt launch plan to rank #1.
- `marketing-viral-hook-creator` - Creates viral social media hooks using proven psychological patterns and trigger words.
- `marketing-writer-social-x` - Creates viral X (Twitter) posts using proven formats and creator voice matching.

### Technology
- `mcp-builder` - Guides creation of high-quality MCP servers that enable LLMs to interact with external services.
- `tech-code-simplifier` - Simplifies and refines code for clarity, consistency, and maintainability while preserving all functionality.
- `tech-finishing-a-development-branch` - Guides completion of development work by presenting structured options for merge, PR, or cleanup.
- `tech-prd-generator` - Generates professional PRD files optimized for AI coding tools from rough product ideas.
- `tech-receiving-code-review` - Guides rigorous, technical evaluation of incoming code review feedback before implementation.
- `tech-requesting-code-review` - Dispatches a code review subagent to verify work meets requirements before merging.
- `tech-test-driven-development` - Enforces test-first development by writing tests before implementation code on any feature or bugfix.
- `tech-writing-plans` - Creates structured implementation plans from specs or requirements before touching code.

### Design
- `product-overview-page` - Builds polished product overview pages with automated screenshot capture and modern SaaS design patterns.
- `ux-design-personas` - Creates UX/UI design artifacts from research through specs, including personas, journey maps, and interaction behaviors.

### Content
- `doc-coauthoring` - Guides users through a structured workflow for co-authoring documentation, proposals, and technical specs.
- `humanizer` - Removes signs of AI-generated writing by detecting and fixing 26 AI writing patterns.
- `internal-comms-organizational-announcement` - Drafts professional internal announcements for promotions, new hires, restructures, and leadership transitions.
- `meeting-notes` - Creates clear, structured, distribution-ready meeting minutes with decisions, action items, and next steps.

### Strategy
- `brainstorming` - Explores user intent, requirements, and design space before implementation on any creative or technical task.
- `customer-segmentation` - Builds data-driven customer segment personas using hybrid qualitative and quantitative analysis methods.
- `forge-brand-strategist` - Expert brand naming and domain strategy for businesses, products, apps, and ventures.
- `mckinsey-problem-solving-brief` - Builds executive-ready strategic briefs using SCQ, MECE issue trees, and pyramid-structured recommendations.
- `nudge-unit` - Applies nudge theory and choice architecture to design System 1 and System 2 behavioral interventions.
- `startup-strategic-planning` - Delivers the 3 highest-impact next moves for growth by analyzing the founder's business context and bottlenecks.

### Monetization
- `adsense-readiness` - Analyzes websites for Google AdSense policy compliance before applying for monetization.
- `adsense-review` - Performs a comprehensive live-site review mimicking the Google AdSense approval process.

### Tooling
- `github-copilot-instructions-writer` - Creates expertly crafted GitHub Copilot custom instructions files tailored to specific domains and repositories.
- `plugin-builder` - Creates knowledge-work plugins through a guided design process, bundling skills, commands, and connectors.
- `product-reverse-engineer` - Performs a thorough project review and produces product overview, functional specification, and technical design documents for greenfield rebuilding.
- `skill-writer` - Guides creating, editing, verifying, and testing skills before deployment.
- `sop-creator` - Creates detailed Standard Operating Procedures for repeatable business processes.

## Contributing

Want to add a new skill? See [SKILL.md](SKILL.md) for development guidelines.

### Skill Structure

```
skills/
└── your-skill/
    ├── SKILL.md        # Main skill definition
    └── references/     # Additional reference materials
```

