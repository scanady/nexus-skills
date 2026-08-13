# Plugin Reference

Complete technical reference for Cowork/Claude Code knowledge-work plugin components, manifest schema, and directory structure. The portable parts of this format (`plugin.json`, `mcp.json`, `skills/`) follow the [Agent Plugins specification](https://agent-plugins.org/) v1.0.0. Commands are a Claude-specific extension layered on top via the spec's reverse-domain namespace mechanism.

## Plugin Manifest Schema

`plugin.json` sits at the plugin root and defines plugin metadata. There is no `.claude-plugin/` wrapper directory in the Agent Plugins spec.

### Fields

| Field | Required | Type | Description | Example |
|---|---|---|---|---|
| `$schema` | **Yes** | string (const) | Must be `"https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"` | `"https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"` |
| `name` | **Yes** | string | 1-64 chars; lowercase alphanumeric, hyphens, periods only; no leading/trailing `-`/`.`; no `--` or `..` | `"sales"` |
| `version` | No | string | Semantic version (recommended) | `"1.0.0"` |
| `description` | No | string | Brief explanation of plugin purpose | `"Sales workflows and deal management"` |
| `author` | No | object | `{"name": string, "email": string, "url": string}` — not a plain string | `{"name": "Anthropic"}` |
| `homepage` | No | string | Project homepage URL | `"https://example.com"` |
| `repository` | No | string | Source repository URL | `"https://github.com/org/plugin"` |
| `license` | No | string | License identifier | `"MIT"` |
| `keywords` | No | array of strings | Discovery tags | `["sales", "crm", "deals"]` |
| `extensions` | No | object | Client-specific manifest data keyed by reverse-domain namespace | `{"com.anthropic.claude": {}}` |

The schema is **closed**: `additionalProperties` is `false`. Fields outside this list are invalid — put client-specific configuration under `extensions.<namespace>` instead of adding new top-level fields. A conformant client must report unknown top-level fields but is not required to reject the plugin for them; any other schema violation is fatal.

### Example Manifest

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "sales",
  "version": "1.0.0",
  "description": "Turn Claude into a sales specialist with CRM integration, call summaries, and deal management",
  "extensions": {
    "com.anthropic.claude": {}
  }
}
```

The `name` field determines the command namespace. A plugin named `"sales"` has commands like `/sales:call-summary`.

## Standard Directory Layout

```
plugin-name/
├── plugin.json                  # Plugin manifest — plugin root, spec-defined
├── mcp.json                     # MCP server connections (connectors) — plugin root, spec-defined
├── com.anthropic.claude/        # Client extension namespace (reverse-domain)
│   └── commands/                  # Slash command definitions
│       ├── command-one.md
│       └── command-two.md
├── skills/                      # Domain knowledge — plugin root, spec-defined
│   ├── skill-one/
│   │   ├── SKILL.md
│   │   └── references/            # Optional: large reference docs
│   │       └── detailed-guide.md
│   └── skill-two/
│       └── SKILL.md
├── CONNECTORS.md                # Tool category documentation (not spec-defined, informational)
└── README.md                    # Usage documentation (not spec-defined, informational)
```

**Critical**: `plugin.json`, `mcp.json`, and `skills/` are the three spec-defined locations and all live at the plugin root — no wrapper directory. Commands are not part of the portable spec; they live under the reverse-domain client namespace `com.anthropic.claude/`, per the spec's client-extension mechanism. All resolved paths (including symlink targets) must stay inside the plugin root.

## Component Reference

### Skills

Skills encode domain expertise that Claude draws on automatically when relevant. Each skill is a directory containing a `SKILL.md` file.

**Location**: `skills/<skill-name>/SKILL.md`

**Discovery rule**: a client treats each immediate child directory of `skills/` that contains a file named exactly `SKILL.md` as one skill. Clients do not recursively search deeper descendants — do not nest a skill inside a subdirectory of `skills/`. Invalid skills are skipped without failing the rest of the plugin.

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
| `scripts/` | Executable helper scripts for the skill |
| `references/` | Large reference docs split from main SKILL.md |

### Commands

Commands define explicit slash commands users invoke. The Agent Plugins spec defines no portable command component, so commands live under the `com.anthropic.claude` client extension namespace. Each command is a markdown file.

**Location**: `com.anthropic.claude/commands/<command-name>.md`

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

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../../CONNECTORS.md).

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
- Command file name becomes the command suffix: `com.anthropic.claude/commands/call-summary.md` → `/plugin-name:call-summary`
- Always include the CONNECTORS.md callout at the top, with a relative path back to the plugin root (`../../CONNECTORS.md` from inside `com.anthropic.claude/commands/`)
- Define clear input/output expectations
- Use `~~category` placeholders for tool references

### Connectors (MCP Servers)

Connectors wire Claude to external tools via MCP servers. Two files work together: `mcp.json` (spec-defined, machine-readable) and `CONNECTORS.md` (informational).

#### mcp.json

Pre-configures specific MCP servers for the plugin.

**Location**: `mcp.json` at the plugin root.

**Top-level fields:**

| Field | Required | Description |
|---|---|---|
| `$schema` | Yes | Must be `"https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"` |
| `mcpServers` | Yes | Object mapping server name → server config |

**Server config, by `type`:**

| Type | Purpose | Required fields | Optional fields |
|---|---|---|---|
| `streamable-http` | Remote server, current transport (preferred) | `type`, `url` | `headers` |
| `sse` | Remote server, legacy transport | `type`, `url` | `headers` |
| `stdio` | Local subprocess | `type`, `command` | `args`, `env`, `cwd` |

`url` must be an absolute HTTP/HTTPS URL with no fragment; non-loopback hosts must use HTTPS. `command` must resolve as a single executable token or a `./`-relative path inside the plugin. For `stdio` servers, `args` items, `env` values, and `cwd` may reference `${PLUGIN_ROOT}` (the plugin's install directory) and `${PLUGIN_DATA}` (a client-managed writable directory persisted across updates) — expansion is single-pass and only applies in those three places, never in `command` or `env` keys. `env` must not define a key literally named `PLUGIN_ROOT` or `PLUGIN_DATA`. `cwd` defaults to the plugin root when omitted, and must itself be plugin-relative (`./...`) or rooted at `${PLUGIN_ROOT}`/`${PLUGIN_DATA}`.

**Example — remote server:**

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
  "mcpServers": {
    "hubspot": {
      "type": "streamable-http",
      "url": "https://mcp.hubspot.com/mcp"
    }
  }
}
```

**Example — local subprocess server:**

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
  "mcpServers": {
    "local-index": {
      "type": "stdio",
      "command": "./scripts/server.sh",
      "args": ["--data-dir", "${PLUGIN_DATA}"],
      "cwd": "${PLUGIN_ROOT}"
    }
  }
}
```

A bare `"type": "http"` is not valid under the spec — remote servers must declare `streamable-http` (or `sse` for legacy servers only).

#### CONNECTORS.md

Documents every tool category used in the plugin, mapping `~~category` placeholders to actual tools. Not part of the Agent Plugins spec — a plain informational file for plugin authors and users.

**Location**: `CONNECTORS.md` at plugin root

**Format:**

```markdown
# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. For example, `~~CRM` might mean Salesforce, HubSpot, or any other CRM with an MCP server.

Plugins are **tool-agnostic** — they describe workflows in terms of categories (CRM, chat, email, etc.) rather than specific products. `mcp.json` pre-configures specific MCP servers, but any MCP server in that category works.

## Connectors for this plugin

| Category | Placeholder | Included servers | Other options |
|----------|-------------|-----------------|---------------|
| CRM | `~~CRM` | HubSpot | Salesforce, Close, Pipedrive |
| Chat | `~~chat` | Slack | Microsoft Teams, Discord |
| Email | `~~email` | Microsoft 365 | Gmail |
```

**Guidelines:**
- Every `~~category` used anywhere in skills or commands must appear in CONNECTORS.md
- "Included servers" are pre-configured in `mcp.json`
- "Other options" lists alternatives the user could swap in
- Keep the standard preamble explaining how placeholders work

## The ~~Placeholder Convention

The `~~category` placeholder system makes plugins tool-agnostic. Instead of hardcoding "Check Salesforce for the deal," plugins say "Check ~~CRM for the deal."

### How It Works

1. Plugin author writes workflows using `~~category` placeholders
2. `mcp.json` pre-configures default servers for each category
3. `CONNECTORS.md` documents available options per category
4. Users customize by swapping `mcp.json` entries or replacing `~~` placeholders

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

[Any customization steps — editing mcp.json, adding API keys, etc.]
```

## Validation Checklist

Use this checklist to verify a plugin before distribution:

- [ ] `plugin.json` exists at the plugin root (no `.claude-plugin/` wrapper) with valid JSON
- [ ] `plugin.json` has `$schema` = `https://agent-plugins.org/schemas/1.0.0/plugin.schema.json` and a `name` field
- [ ] `name` matches the spec pattern (lowercase alphanumeric/hyphen/period, no leading/trailing separator, no `--`/`..`)
- [ ] `plugin.json` has no fields beyond the closed schema's allowed set; `author`, if present, is an object
- [ ] `skills/` sits at the plugin root; each skill folder is an immediate child containing `SKILL.md` with `name` and `description` frontmatter
- [ ] Skill folder name matches the `name` frontmatter field
- [ ] Command files live under `com.anthropic.claude/commands/`, not at the plugin root; each has a `description` frontmatter field
- [ ] All tool references use `~~category` placeholders, not hardcoded tool names
- [ ] `CONNECTORS.md` documents every `~~category` placeholder used in the plugin
- [ ] `mcp.json` exists at the plugin root with `$schema` = `https://agent-plugins.org/schemas/1.0.0/mcp.schema.json` and pre-configures at least the primary connectors
- [ ] Every `mcp.json` server entry declares `type: stdio`, `type: streamable-http`, or `type: sse` — never a bare `"http"`
- [ ] `README.md` covers: Installation, What It Does, Commands, Skills, Example Workflows, Data Sources
- [ ] Skill files are under 500 lines (use `references/` for overflow)
- [ ] Everything is markdown and JSON — no code, no build steps, no executables
- [ ] No resolved path, including symlink targets, escapes the plugin root

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
1. Editing `mcp.json` to connect their specific tool instances
2. Replacing `~~category` placeholders with specific tool names (optional)
3. Adding company-specific context to skill files (terminology, processes)
4. Modifying command workflows to match team processes
