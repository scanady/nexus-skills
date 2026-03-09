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

- `adsense-review` - Comprehensive live-site review mimicking Google's AdSense approval process. Crawls the site from a URL, evaluates content quality, navigation, technical compliance, and policies. Produces a detailed pass/fail report with remediation steps. Especially effective for diagnosing "low value content" rejections.
- `customer-segmentation` - Expert-level customer segmentation analysis using hybrid qualitative/quantitative methods. Builds data-driven segment personas, opportunity sizing, journey maps, and operationalization plans.
- `internal-comms-organizational-announcement` - Drafts internal announcements for organizational and role changes.
- `mc-problem-solving-brief` - Creates board-ready strategy briefs using SCQ framing, MECE issue trees, hypothesis-driven diagnostics, pyramid-structured recommendations, and implementation roadmaps.
- `mckinsey-problem-solving-brief` - Creates board-ready strategy briefs using SCQ framing, MECE issue trees, hypothesis-driven diagnostics, pyramid-structured recommendations, and implementation roadmaps.
- `copilot-instructions-writer` - Creates expertly crafted GitHub Copilot custom instructions files (.instructions.md and copilot-instructions.md) tailored to specific domains, languages, frameworks, or repositories.
- `product-engineer` - Performs a thorough review of an existing project and produces a product overview, functional specification, and technical design document — all product-agnostic and suitable for greenfield rebuilding.
- `product-overview-page` - Builds polished product overview pages with screenshot showcases, scroll-triggered animations, and modern SaaS design patterns inspired by Stripe, Linear, and Bestow.

## Contributing

Want to add a new skill? See [SKILL.md](SKILL.md) for development guidelines.

### Skill Structure

```
skills/
└── your-skill/
    ├── SKILL.md        # Main skill definition
    └── references/     # Additional reference materials
```

