# Skills pack

This repository contains skills, prompts, agents, and instructions.

## Installation

### Via npx (recommended)

Use `npx nexus-agents` when consuming this package externally.

```bash
npx nexus-agents install
```

Install a specific skill:

```bash
npx nexus-agents install --skill product-spec-prd-generator
```

### Via GitHub (no npm publish required)

Run the CLI directly from the GitHub repository:

```bash
npx github:scanady/nexus-agents install
```

Install a specific skill from GitHub:

```bash
npx github:scanady/nexus-agents install --skill data-ai-autoresearch
```

Install globally from GitHub:

```bash
npm install -g github:scanady/nexus-agents
```

### Local install (from cloned repo)

```bash
git clone https://github.com/scanady/nexus-agents
cd nexus-agents
```

Install all skills into the current project (default target: Agent Skills standard):

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

Install globally instead of to the current project:

```bash
node bin/cli.js install --skill product-spec-prd-generator -g
```

The CLI defaults to project installs. Use `-g` or `--global` when you want the skill available across repos.

List available skills:

```bash
node bin/cli.js list
```

**Supported agents:**

| Agent | Global path | Project path |
|-------|------------|--------------|
| `agent-skills` (default) | `~/.agents/skills/` | `.agents/skills/` |
| `github-copilot` | `~/.copilot/skills/` | `.agents/skills/` |
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

## Contributing

Want to add a new skill? See [SKILL.md](SKILL.md) for development guidelines.

### Skill Structure

```
skills/
└── your-skill/
    ├── SKILL.md        # Main skill definition
    └── references/     # Additional reference materials
```

