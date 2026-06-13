# Plugin Reference

Complete technical reference for Cowork/Claude Code knowledge-work plugin components, manifest schema, and directory structure.

## Plugin Manifest Schema

The `.claude-plugin/plugin.json` file defines plugin metadata. This is the only file that goes inside the `.claude-plugin/` directory.

### Fields

| Field | Required | Type | Description | Example |
|---|---|---|---|---|
| `name` | **Yes** | string | Unique identifier (kebab-case, no spaces) | `"sales"` |
| `version` | No | string | Semantic version | `"1.0.0"` |
| `description` | No | string | Brief explanation of plugin purpose | `"Sales workflows and deal management"` |
| `author` | No | string | Author name | `"Anthropic"` |
| `keywords` | No | array | Discovery tags | `["sales", "crm", "deals"]` |

### Example Manifest

```json
{
  "name": "sales",
  "version": "1.0.0",
  "description": "Turn Claude into a sales specialist with CRM integration, call summaries, and deal management"
}
```

The `name` field determines the command namespace. A plugin named `"sales"` has commands like `/sales:call-summary`.

## Standard Directory Layout

```
plugin-name/
├── .claude-plugin/              # Metadata directory
│   └── plugin.json                # Plugin manifest — ONLY file here
├── .mcp.json                    # MCP server connections (connectors)
├── CONNECTORS.md                # Tool category documentation
├── README.md                    # Usage documentation
├── commands/                    # Slash command definitions
│   ├── command-one.md
│   └── command-two.md
└── skills/                      # Domain knowledge
    ├── skill-one/
    │   ├── SKILL.md
    │   └── references/            # Optional: large reference docs
    │       └── detailed-guide.md
    └── skill-two/
        └── SKILL.md
```

**Critical**: All component directories (`commands/`, `skills/`) go at the plugin root, NOT inside `.claude-plugin/`. Only `plugin.json` lives in `.claude-plugin/`.

## Component Reference

### Skills

Skills encode domain expertise that Claude draws on automatically when relevant. Each skill is a directory containing a `SKILL.md` file.

**Location**: `skills/<skill-name>/SKILL.md`

**Frontmatter fields:**

| Field | Required | Constraints |
|---|---|---|
| `name` | Yes | 1-64 chars, lowercase letters/numbers/hyphens, matches folder name |
| `description` | Yes | 1-1024 chars, describes WHAT knowledge it contains and WHEN Claude should use it |

**Structure:**

```markdown
---
name: skill-name
description: 'Domain expertise this skill covers. Claude uses this automatically when [trigger conditions].'
---

# Skill Title

[Domain knowledge, workflows, best practices, templates, frameworks]
```

**Guidelines:**
- Keep SKILL.md under 500 lines; use `references/` subfolder for supplementary docs
- Write actionable workflows, not just descriptions
- Use `~~category` placeholders for tool references (not specific product names)
- Include templates and examples where helpful
- The `description` field is critical — it determines when Claude automatically activates the skill

**Optional subdirectories:**

| Subdirectory | Purpose |
|---|---|
| `references/` | Large reference docs split from main SKILL.md |

### Commands

Commands define explicit slash commands users invoke. Each command is a markdown file in `commands/`.

**Location**: `commands/<command-name>.md`

**Frontmatter fields:**

| Field | Required | Description |
|---|---|---|
| `description` | Yes | One-line summary shown in command listings |

**Structure:**

```markdown
---
description: One-line summary of what this command does
---

# /command-name

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

[Purpose description]

## Workflow

1. [Step one]
2. [Step two]
3. [Step three]

## Output Format

[Expected output structure]

## Examples

[1-2 example interactions]
```

**Guidelines:**
- Command file name becomes the command suffix: `commands/call-summary.md` → `/plugin-name:call-summary`
- Always include the CONNECTORS.md callout at the top
- Define clear input/output expectations
- Use `~~category` placeholders for tool references

### Connectors (MCP Servers)

Connectors wire Claude to external tools via MCP servers. Two files work together:

#### .mcp.json

Pre-configures specific MCP servers for the plugin.

**Location**: `.mcp.json` at plugin root

**Format:**

```json
{
  "mcpServers": {
    "server-name": {
      "type": "http",
      "url": "https://mcp-server-url.example.com/sse"
    }
  }
}
```

**Server configuration fields:**

| Field | Description |
|---|---|
| `type` | Connection type — typically `"http"` for remote servers |
| `url` | MCP server endpoint URL |

#### CONNECTORS.md

Documents every tool category used in the plugin, mapping `~~category` placeholders to actual tools.

**Location**: `CONNECTORS.md` at plugin root

**Format:**

```markdown
# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. For example, `~~CRM` might mean Salesforce, HubSpot, or any other CRM with an MCP server.

Plugins are **tool-agnostic** — they describe workflows in terms of categories (CRM, chat, email, etc.) rather than specific products. The `.mcp.json` pre-configures specific MCP servers, but any MCP server in that category works.

## Connectors for this plugin

| Category | Placeholder | Included servers | Other options |
|----------|-------------|-----------------|---------------|
| CRM | `~~CRM` | HubSpot | Salesforce, Close, Pipedrive |
| Chat | `~~chat` | Slack | Microsoft Teams, Discord |
| Email | `~~email` | Microsoft 365 | Gmail |
```

**Guidelines:**
- Every `~~category` used anywhere in skills or commands must appear in CONNECTORS.md
- "Included servers" are pre-configured in `.mcp.json`
- "Other options" lists alternatives the user could swap in
- Keep the standard preamble explaining how placeholders work

## The ~~Placeholder Convention

The `~~category` placeholder system makes plugins tool-agnostic. Instead of hardcoding "Check Salesforce for the deal," plugins say "Check ~~CRM for the deal."

### How It Works

1. Plugin author writes workflows using `~~category` placeholders
2. `.mcp.json` pre-configures default servers for each category
3. `CONNECTORS.md` documents available options per category
4. Users customize by swapping `.mcp.json` entries or replacing `~~` placeholders

### Common Placeholder Categories

| Placeholder | Category | Example tools |
|---|---|---|
| `~~chat` | Team messaging | Slack, Microsoft Teams, Discord |
| `~~email` | Email | Microsoft 365, Gmail |
| `~~CRM` | Customer relationship management | HubSpot, Salesforce, Close, Pipedrive |
| `~~project tracker` | Project/issue tracking | Jira, Linear, Asana, Monday, ClickUp |
| `~~knowledge base` | Documentation/wiki | Notion, Confluence, Guru |
| `~~data warehouse` | Data storage/querying | Snowflake, BigQuery, Databricks, Redshift |
| `~~cloud storage` | File storage | Box, Egnyte, Dropbox, Microsoft 365 |
| `~~analytics` | Analytics/BI | Amplitude, Tableau, Looker, Mixpanel |
| `~~design` | Design tools | Figma, Canva |
| `~~office suite` | Productivity suite | Microsoft 365, Google Workspace |
| `~~code` | Code hosting | GitHub, GitLab, Bitbucket |
| `~~CI/CD` | Build/deploy | GitHub Actions, CircleCI, Jenkins |
| `~~monitoring` | Observability | Datadog, PagerDuty, Sentry |
| `~~calendar` | Calendar/scheduling | Google Calendar, Microsoft Outlook |

### Usage Examples in Plugin Files

In a skill file:
```markdown
## Research Workflow
1. Search ~~CRM for the account and recent activity
2. Check ~~chat for recent mentions and team discussions
3. Pull the latest pipeline data from ~~analytics
```

In a command file:
```markdown
## Workflow
1. Gather call notes from user input or ~~chat transcript
2. Look up the account in ~~CRM
3. Draft follow-up email via ~~email
4. Create action items in ~~project tracker
```

## README.md Convention

Every plugin should have a README.md at the root following this pattern:

```markdown
# Plugin Name

A [role] plugin primarily designed for [Cowork](https://claude.com/product/cowork), Anthropic's agentic desktop application — though it also works in Claude Code. [Brief capability description].

## Installation

\```
claude plugins add marketplace/plugin-name
\```

## What It Does

- **Capability one**: Brief description
- **Capability two**: Brief description
- **Capability three**: Brief description

## Commands

| Command | Description |
|---------|-------------|
| `/plugin:command-one` | What it does |
| `/plugin:command-two` | What it does |

## Skills

| Skill | Description |
|-------|-------------|
| `skill-one` | What domain knowledge it provides |
| `skill-two` | What domain knowledge it provides |

## Example Workflows

### Scenario Name

\```
You: /plugin:command [input]
Claude: [Step-by-step of what Claude does]
\```

## Data Sources / MCP Integration

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](CONNECTORS.md).

[Table or description of what tool categories enhance the plugin]

## Configuration

[Any customization steps — editing .mcp.json, adding API keys, etc.]
```

## Validation Checklist

Use this checklist to verify a plugin before distribution:

- [ ] `.claude-plugin/plugin.json` exists with valid JSON and a `name` field
- [ ] `name` is kebab-case with no spaces
- [ ] No component directories inside `.claude-plugin/` (only `plugin.json`)
- [ ] Each skill folder contains a `SKILL.md` with `name` and `description` frontmatter
- [ ] Skill folder name matches the `name` frontmatter field
- [ ] Each command file has a `description` frontmatter field
- [ ] All tool references use `~~category` placeholders, not hardcoded tool names
- [ ] `CONNECTORS.md` documents every `~~category` placeholder used in the plugin
- [ ] `.mcp.json` pre-configures at least the primary connectors
- [ ] `README.md` covers: Installation, What It Does, Commands, Skills, Example Workflows, Data Sources
- [ ] Skill files are under 500 lines (use `references/` for overflow)
- [ ] Everything is markdown and JSON — no code, no build steps, no executables

## Distribution

### Packaging

Plugins can be distributed as `.plugin` files (zip archives):

```bash
cd plugin-name/
zip -r ../plugin-name.plugin . -x '.*' -x '__MACOSX/*'
```

### Installation Methods

**Claude Code (local testing):**
```bash
claude --plugin-dir ./plugin-name
```

**Claude Code (marketplace):**
```bash
claude plugin marketplace add <marketplace-source>
claude plugin install plugin-name@marketplace-name
```

**Cowork:**
Install from [claude.com/plugins](https://claude.com/plugins/).

### Customization After Install

Teams typically customize plugins by:
1. Editing `.mcp.json` to connect their specific tool instances
2. Replacing `~~category` placeholders with specific tool names (optional)
3. Adding company-specific context to skill files (terminology, processes)
4. Modifying command workflows to match team processes
