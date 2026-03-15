# Plugin Examples

Concrete examples of knowledge-work plugin components modeled after the [Anthropic knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) repository. Use these as reference during plugin generation.

---

## Complete Plugin: Sales

A role-based plugin that turns Claude into a sales specialist with CRM integration, call processing, and deal management.

### Directory Structure

```
sales/
├── .claude-plugin/
│   └── plugin.json
├── .mcp.json
├── CONNECTORS.md
├── README.md
├── commands/
│   ├── call-summary.md
│   ├── deal-review.md
│   └── prospect-research.md
└── skills/
    ├── account-research/
    │   └── SKILL.md
    ├── deal-management/
    │   └── SKILL.md
    └── objection-handling/
        └── SKILL.md
```

### plugin.json

```json
{
  "name": "sales",
  "version": "1.0.0",
  "description": "Turn Claude into a sales specialist with CRM integration, call summaries, and deal management"
}
```

### Skill: account-research/SKILL.md

```markdown
---
name: account-research
description: 'Systematic account and prospect research methodology. Use when researching companies, contacts, or preparing for sales conversations.'
---

# Account Research

## Research Framework

When researching an account or prospect, follow this priority order:

### 1. Internal Intelligence (highest priority)
- Check ~~CRM for account history, past deals, notes, and activity
- Search ~~chat for recent team discussions about the account
- Review ~~knowledge base for any existing account briefs

### 2. Public Intelligence
- Company website: products, leadership, recent news, press releases
- SEC filings (public companies): 10-K, 10-Q for financial health
- Job postings: indicate priorities and tech stack
- Social media: LinkedIn company page, executive profiles

### 3. Competitive Intelligence
- Current vendor relationships (from ~~CRM notes or public info)
- Contract renewal timing if known
- Competitor mentions in ~~chat or ~~CRM

## Research Output Format

| Section | Content |
|---------|---------|
| Company Overview | Size, industry, key products, recent news |
| Key Contacts | Names, roles, engagement history from ~~CRM |
| Pain Points | Identified challenges mapped to our solutions |
| Competitive Landscape | Known vendors, contract status |
| Recommended Approach | Talk tracks, value props, timing |

## Source Prioritization

Always cite sources. Internal data (~~CRM, ~~chat) takes precedence over public information when they conflict.
```

### Skill: objection-handling/SKILL.md

```markdown
---
name: objection-handling
description: 'Sales objection handling frameworks and response strategies. Use when preparing for calls, handling objections in real-time, or coaching on objection responses.'
---

# Objection Handling

## Framework: LAER Model

For every objection, follow the LAER model:

1. **Listen** — Let the prospect fully articulate the concern
2. **Acknowledge** — Validate their concern genuinely
3. **Explore** — Ask questions to understand the root cause
4. **Respond** — Address the real objection with evidence

## Common Objection Patterns

### Price/Budget
- "Too expensive" → Reframe as ROI and total cost of ownership
- "No budget" → Explore timeline, help build internal business case
- "Competitor is cheaper" → Differentiate on value, not price

### Timing
- "Not a priority right now" → Tie to their stated goals, quantify cost of delay
- "Call back next quarter" → Agree to timeline but secure commitment, send value content

### Authority
- "Need to check with my boss" → Offer to present jointly, provide materials for internal selling
- "Committee decision" → Map the buying committee, tailor messaging per stakeholder

### Need
- "We already have a solution" → Explore satisfaction, identify gaps
- "Don't see the need" → Share relevant case studies, quantify the problem

## Response Templates

For each objection type, prepare:
1. **Acknowledgment phrase** — Shows you heard them
2. **Clarifying question** — Gets to the real concern
3. **Proof point** — Case study, metric, or testimonial
4. **Next step** — Clear call to action
```

### Command: commands/call-summary.md

```markdown
---
description: Process sales call notes into structured summaries with action items and CRM updates
---

# /call-summary

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Process sales call notes or transcripts into a structured summary with extracted action items and recommended follow-ups.

## Workflow

1. **Gather input**: Accept call notes, transcript, or recording summary from the user
2. **Account lookup**: Search ~~CRM for the account and contact to add context
3. **Extract insights**:
   - Key discussion points
   - Objections raised and responses given
   - Buying signals
   - Competitor mentions
   - Next steps agreed upon
4. **Generate summary**: Produce a structured call summary
5. **Create action items**: Extract follow-ups with owners and deadlines
6. **Draft follow-up**: Write a follow-up email based on the conversation

## Output Format

### Call Summary
| Field | Value |
|-------|-------|
| Date | [date] |
| Account | [company name] |
| Attendees | [names and roles] |
| Stage | [current deal stage] |

### Key Discussion Points
- [point 1]
- [point 2]

### Objections & Responses
| Objection | Response | Status |
|-----------|----------|--------|
| [objection] | [how it was handled] | Resolved / Open |

### Action Items
| Action | Owner | Due Date |
|--------|-------|----------|
| [task] | [person] | [date] |

### Recommended Follow-Up Email
[Draft email]
```

### Command: commands/prospect-research.md

```markdown
---
description: Research a prospect or account and produce a comprehensive intelligence brief
---

# /prospect-research

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Research a company or contact and produce an intelligence brief for sales preparation.

## Workflow

1. **Identify target**: Get the company name and/or contact name from the user
2. **Internal search**: Query ~~CRM for existing account data, past interactions, deal history
3. **Team intel**: Search ~~chat for recent mentions or discussions about the account
4. **External research**: Gather public information (website, news, financials, job postings)
5. **Synthesize**: Combine internal and external intelligence into a structured brief
6. **Recommend approach**: Suggest talk tracks, value propositions, and meeting strategy

## Output Format

Produce a research brief following the format defined in the `account-research` skill.

## Examples

```
You: /sales:prospect-research Acme Corp
Claude: I'll research Acme Corp for you. Let me check our internal data first...

[Searches CRM, chat, then external sources]
[Produces structured research brief]
```
```

### CONNECTORS.md

```markdown
# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. For example, `~~CRM` might mean Salesforce, HubSpot, or any other CRM with an MCP server.

Plugins are **tool-agnostic** — they describe workflows in terms of categories (CRM, chat, email, etc.) rather than specific products. The `.mcp.json` pre-configures specific MCP servers, but any MCP server in that category works.

## Connectors for this plugin

| Category | Placeholder | Included servers | Other options |
|----------|-------------|-----------------|---------------|
| CRM | `~~CRM` | HubSpot | Salesforce, Close, Pipedrive |
| Chat | `~~chat` | Slack | Microsoft Teams |
| Email | `~~email` | Microsoft 365 | Gmail |
| Knowledge Base | `~~knowledge base` | Notion | Confluence, Guru |
| Calendar | `~~calendar` | Google Calendar | Microsoft Outlook |
```

### .mcp.json

```json
{
  "mcpServers": {
    "hubspot": {
      "type": "http",
      "url": "https://mcp.hubspot.com/sse"
    },
    "slack": {
      "type": "http",
      "url": "https://mcp.slack.com/sse"
    }
  }
}
```

---

## Complete Plugin: Legal

A plugin for legal professionals focused on contract review and compliance.

### Directory Structure

```
legal/
├── .claude-plugin/
│   └── plugin.json
├── .mcp.json
├── CONNECTORS.md
├── README.md
├── commands/
│   ├── review-contract.md
│   └── summarize-agreement.md
└── skills/
    ├── contract-review/
    │   ├── SKILL.md
    │   └── references/
    │       └── clause-library.md
    └── compliance/
        └── SKILL.md
```

### plugin.json

```json
{
  "name": "legal",
  "version": "1.0.0",
  "description": "Contract review, clause analysis, and legal compliance workflows"
}
```

### Skill: contract-review/SKILL.md

```markdown
---
name: contract-review
description: 'Contract analysis using playbook-based clause review. Use when reviewing, analyzing, or comparing contracts, agreements, or legal documents.'
---

# Contract Review

## Review Methodology

### Step 1: Document Intake
- Identify document type (NDA, MSA, SOW, SaaS Agreement, etc.)
- Note the parties, effective date, and term
- Flag the governing law and jurisdiction

### Step 2: Clause-by-Clause Analysis
For each material clause, evaluate against the playbook:

| Assessment | Meaning |
|-----------|---------|
| ✅ Standard | Matches our preferred position |
| ⚠️ Deviation | Differs from playbook — needs review |
| 🔴 Unacceptable | Violates dealbreakers — must be revised |
| ❓ Missing | Expected clause not found |

### Step 3: Risk Assessment
Rate overall risk: **Low / Medium / High / Critical**

Consider:
- Indemnification scope and caps
- Liability limitations
- IP ownership and assignment
- Termination rights
- Data protection obligations
- Non-compete / non-solicit scope

### Step 4: Redline Generation
For deviations and unacceptable terms:
- Quote the original language
- Propose revised language
- Explain the rationale for the change
- Note negotiation leverage points

## Output Format

Produce a review memo with:
1. **Executive Summary** — 2-3 sentence overview with risk rating
2. **Key Terms Table** — Party names, dates, values, term
3. **Clause Analysis** — Each clause with assessment and notes
4. **Recommended Redlines** — Specific language changes
5. **Negotiation Notes** — Strategy recommendations

For the full clause library reference, see [references/clause-library.md](references/clause-library.md).
```

### Command: commands/review-contract.md

```markdown
---
description: Review a contract against the playbook, flag deviations, and generate redlines
---

# /review-contract

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Perform a comprehensive contract review using the playbook-based methodology.

## Workflow

1. **Intake**: User provides the contract (file, text, or link to ~~cloud storage)
2. **Classification**: Identify document type and applicable playbook
3. **Analysis**: Review clause-by-clause against the playbook
4. **Risk rating**: Assess overall risk level
5. **Redlines**: Generate proposed language changes for deviations
6. **Memo**: Produce the review memo in standard format

## Output Format

See the contract-review skill for the standard review memo format.

## Examples

```
You: /legal:review-contract [paste contract or attach file]
Claude: I'll review this agreement. Let me identify the document type first...

Document Type: Master Services Agreement
Parties: Acme Corp (Client) ↔ Vendor Inc (Provider)

[Proceeds with clause-by-clause analysis]
[Produces review memo with risk rating and redlines]
```
```

---

## Complete Plugin: Data

A plugin for data analysts and engineers focused on SQL, analysis, and data pipeline workflows.

### Directory Structure

```
data/
├── .claude-plugin/
│   └── plugin.json
├── .mcp.json
├── CONNECTORS.md
├── README.md
├── commands/
│   ├── analyze.md
│   └── build-dashboard.md
└── skills/
    ├── sql-queries/
    │   └── SKILL.md
    └── data-modeling/
        └── SKILL.md
```

### Skill: sql-queries/SKILL.md

```markdown
---
name: sql-queries
description: 'SQL best practices, query patterns, and optimization. Use when writing, reviewing, or debugging SQL queries across any dialect.'
---

# SQL Queries

## Query Development Workflow

1. **Understand the question**: Clarify what data is needed and how it will be used
2. **Explore the schema**: Query ~~data warehouse metadata tables to understand available tables and columns
3. **Write incrementally**: Build queries step by step, validating each stage
4. **Optimize**: Review for performance before running on large datasets

## SQL Best Practices

### Readability
- Use CTEs over nested subqueries
- Meaningful alias names (not `a`, `b`, `c`)
- Consistent formatting: uppercase keywords, lowercase identifiers
- Comment complex logic

### Performance
- Filter early with WHERE clauses
- Avoid SELECT * in production queries
- Use appropriate JOIN types (prefer INNER over OUTER when possible)
- Check for index usage on large tables
- Limit result sets during development

### Safety
- Always include WHERE on UPDATE/DELETE
- Use transactions for multi-step modifications
- Test on development data first
- Add LIMIT during exploratory queries

## Common Patterns

### Time Series Analysis
```sql
SELECT
    DATE_TRUNC('month', created_at) AS month,
    COUNT(*) AS total,
    COUNT(DISTINCT user_id) AS unique_users
FROM events
WHERE created_at >= DATEADD('month', -12, CURRENT_DATE)
GROUP BY 1
ORDER BY 1
```

### Funnel Analysis
```sql
WITH steps AS (
    SELECT
        user_id,
        MAX(CASE WHEN event = 'page_view' THEN 1 END) AS step_1,
        MAX(CASE WHEN event = 'signup' THEN 1 END) AS step_2,
        MAX(CASE WHEN event = 'purchase' THEN 1 END) AS step_3
    FROM events
    GROUP BY user_id
)
SELECT
    COUNT(*) AS total_users,
    SUM(step_1) AS viewed,
    SUM(step_2) AS signed_up,
    SUM(step_3) AS purchased
FROM steps
```
```

### Command: commands/analyze.md

```markdown
---
description: Answer data questions — from quick lookups to full analyses with visualizations
---

# /analyze

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Answer data questions by querying ~~data warehouse, analyzing results, and presenting insights.

## Workflow

1. **Understand**: Clarify the question and what decisions the answer will inform
2. **Explore**: Query ~~data warehouse metadata to find relevant tables and columns
3. **Query**: Write and execute SQL to get the data
4. **Analyze**: Identify patterns, trends, anomalies
5. **Present**: Format results with context and recommendations

## Scope Levels

| Level | Description | Example |
|-------|-------------|---------|
| Quick lookup | Single query, direct answer | "How many users signed up last week?" |
| Analysis | Multiple queries, synthesis | "What's our conversion funnel by channel?" |
| Deep dive | Full investigation with visuals | "Why did revenue drop in Q3?" |

## Examples

```
You: /data:analyze How many active users did we have last month?
Claude: Let me check the data warehouse...

[Queries user_activity table]

Last month: 45,230 active users
- Up 12% from previous month (40,384)
- DAU averaged 8,420
```
```

---

## Minimal Plugin: Single Skill

The simplest useful plugin — just a skill with no commands or connectors.

### Directory Structure

```
code-standards/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── style-guide/
        └── SKILL.md
```

### plugin.json

```json
{
  "name": "code-standards",
  "version": "1.0.0",
  "description": "Team coding standards and conventions"
}
```

### skills/style-guide/SKILL.md

```markdown
---
name: style-guide
description: 'Team coding standards, naming conventions, and project structure rules. Use when writing new code, reviewing code, or asked about coding style.'
---

# Style Guide

## Naming Conventions

- **Variables/functions**: camelCase
- **Classes/types**: PascalCase
- **Constants**: SCREAMING_SNAKE_CASE
- **Files**: kebab-case

## Code Organization

- One component per file
- Group imports: stdlib → third-party → local
- Maximum function length: 50 lines
- Maximum file length: 300 lines

## Error Handling

- Use typed errors, not generic Error
- Log with context: operation, input, timestamp
- Return errors, don't throw (except in entry points)
```

---

## Minimal Plugin: Single Command

A plugin with just one command and no skills or connectors.

### Directory Structure

```
standup/
├── .claude-plugin/
│   └── plugin.json
└── commands/
    └── generate.md
```

### plugin.json

```json
{
  "name": "standup",
  "version": "1.0.0",
  "description": "Generate daily standup updates from recent work"
}
```

### commands/generate.md

```markdown
---
description: Generate a standup update from recent git activity and notes
---

# /generate

Generate a daily standup update based on recent work.

## Workflow

1. Review recent git commits (last 24 hours)
2. Check for any open/in-progress items
3. Format as: Yesterday / Today / Blockers

## Output Format

**Yesterday:**
- [completed items from git history]

**Today:**
- [planned items based on open work]

**Blockers:**
- [any identified blockers, or "None"]
```

---

## Plugin Pattern: Multi-Role with Shared Connectors

Some plugins serve multiple related roles. Here's the pattern for a customer-support plugin that combines ticket triage, response drafting, and escalation.

### CONNECTORS.md (shared across all skills and commands)

```markdown
# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. For example, `~~CRM` might mean Salesforce, HubSpot, or any other CRM with an MCP server.

Plugins are **tool-agnostic** — they describe workflows in terms of categories (CRM, chat, email, etc.) rather than specific products. The `.mcp.json` pre-configures specific MCP servers, but any MCP server in that category works.

## Connectors for this plugin

| Category | Placeholder | Included servers | Other options |
|----------|-------------|-----------------|---------------|
| Helpdesk | `~~helpdesk` | Zendesk | Freshdesk, Intercom, Help Scout |
| CRM | `~~CRM` | HubSpot | Salesforce |
| Chat | `~~chat` | Slack | Microsoft Teams |
| Knowledge Base | `~~knowledge base` | Notion | Confluence, Guru |
```

### Skills working together

- `ticket-triage/SKILL.md` — Category taxonomy, priority framework, routing rules. References `~~helpdesk` for ticket data and `~~CRM` for customer context.
- `response-drafting/SKILL.md` — Tone guidelines, template library, personalization rules. References `~~knowledge base` for solution articles.
- `escalation/SKILL.md` — Escalation criteria, handoff procedures, SLA tracking. References `~~chat` for team notifications and `~~helpdesk` for ticket updates.

### Commands orchestrating skills

- `/support:triage` — Pulls new tickets from `~~helpdesk`, categorizes using `ticket-triage` skill, routes based on rules
- `/support:respond` — Drafts responses using `response-drafting` skill, checks `~~knowledge base` for relevant articles
- `/support:escalate` — Evaluates escalation criteria from `escalation` skill, notifies team via `~~chat`

This pattern shows how skills provide the domain knowledge while commands provide the workflows, all connected through shared `~~category` placeholders documented in CONNECTORS.md.
