# Four-Layer Architecture

The persona framework organizes every persona into four layers. Each layer has a distinct responsibility and maps to specific files in the generated bundle.

---

## Layer Overview

| Layer | Purpose | Key Files |
|-------|---------|-----------|
| **Soul** | Who the persona IS — identity, personality, backstory, ethics | `soul/persona.json`, `soul/identity.md`, `soul/injection.md`, `soul/constitution.md` |
| **Body** | Where the persona EXISTS — platform, runtime, appearance | `body` section in `manifest.json` and `persona.json` |
| **Faculty** | What the persona CAN DO (general capabilities) — selfie, memory, reminders, economy | `faculties` array in `manifest.json`, `references/<faculty>.md` |
| **Skill** | What the persona DOES PROFESSIONALLY — domain-specific skills | `skills` array in `persona.json`, skill definitions in SKILL.md |

---

## Layer 1: Soul

The soul layer defines the persona's core identity. It is the foundation everything else builds on.

### Files

**`soul/persona.json`** — The complete soul definition. Contains all persona fields (name, bio, personality, behaviorGuide, faculties, skills, body config). This is the source of truth.

**`soul/identity.md`** — A short identity block:

```markdown
# <PersonaName>

**Role:** <role>
**Bio:** <bio>

<emoji> <personaName> — <creature>
```

**`soul/injection.md`** — The system prompt injection that activates the persona in any host agent. Wrapped in delimiters so hosts can swap personas without affecting the rest of the system prompt:

```markdown
<!-- PERSONA_SOUL_START -->
You are <personaName>, <bio>.

## Who You Are
<background — condensed to 2–3 key paragraphs>

## Your Personality
<personality traits as a natural paragraph>

## How You Speak
<speakingStyle>

## What Talking to You Feels Like
<vibe>

## Your Boundaries
<boundaries>

## Your Capabilities
<capabilities as a bulleted list>

## Behavior Guide
<full behaviorGuide content>
<!-- PERSONA_SOUL_END -->
```

**`soul/constitution.md`** — The Persona Constitution v1.0. Universal ethical foundation inherited by all personas. Load from `references/constitution.md` and copy verbatim.

### Constitution — The Soul's Foundation

Every persona automatically inherits the constitution — universal values and safety boundaries that cannot be overridden by individual persona definitions. Built on five core axioms: Purpose, Honesty, Safety, Autonomy, and Hierarchy. When principles conflict, safety and honesty take precedence over helpfulness. Individual personas add personality on top of this foundation.

---

## Layer 2: Body

The body layer defines the persona's substrate — where and how it exists. A digital agent has a virtual body (runtime-only). Body is never null.

### Dimensions

| Dimension | Required | Description |
|-----------|----------|-------------|
| `runtime` | **Yes** | Platform, channels, credentials, resources |
| `appearance` | Optional | Avatar URL, visual identity |
| `physical` | Optional | For robots/IoT — not applicable to digital personas |
| `interface` | Optional | Signal Protocol, Pending Commands, State Sync (the nervous system) |

### Configuration in persona.json

```json
{
  "body": {
    "runtime": {
      "platform": "<AGENT_HOST>"
    },
    "appearance": {
      "avatar": "<AVATAR_URL>"
    }
  }
}
```

Keep `platform` as `"<AGENT_HOST>"` placeholder for agent-agnostic output. The host fills this at runtime.

---

## Layer 3: Faculty

Faculties are general software capabilities organized by dimension. They are NOT professional skills — they are infrastructure capabilities the persona uses across all its skills.

### Faculty Dimensions

| Dimension | Description |
|-----------|-------------|
| **Expression** | Capabilities for the persona to express itself (selfie generation) |
| **Cognition** | Capabilities for thinking, remembering, managing (reminder, memory, economy) |

### Available Faculties

| Faculty | Dimension | Description | Provider | Env Var |
|---------|-----------|-------------|----------|---------|
| `selfie` | expression | AI selfie generation with mirror/direct modes | Google AI Studio (Gemini) | `GOOGLE_AI_STUDIO_KEY` |
| `reminder` | cognition | Schedule reminders and task management | Built-in | — |
| `memory` | cognition | Cross-session memory with pluggable backend | local (default), Mem0, Zep | `MEMORY_PROVIDER`, `MEMORY_API_KEY` |
| `economy` | cognition | Economic accountability — track costs, income, Financial Health Score | Built-in | `PERSONA_SLUG`, `ECONOMY_DATA_PATH` |

### Faculty Configuration in manifest.json

```json
{
  "faculties": [
    { "name": "selfie" },
    { "name": "reminder" },
    {
      "name": "memory",
      "provider": "local"
    },
    { "name": "economy" }
  ]
}
```

---

## Layer 4: Skill

Skills are the persona's professional capabilities — domain-specific things it does. Each skill has a name, description, and trigger condition.

### Skill Definition in persona.json

```json
{
  "skills": [
    {
      "name": "workout-planner",
      "description": "Design personalized workout programs with progressive overload",
      "trigger": "User asks for a workout, training plan, or exercise routine"
    },
    {
      "name": "web-search",
      "description": "Search for real-time information on the web"
    }
  ]
}
```

**Best practices:**
- Skill names should be lowercase with hyphens
- Every persona should include `web-search` for real-time information
- Triggers should describe when the skill activates — specific user phrases or contexts
- Descriptions should say what the skill *does*, not what it *is*

---

## Generated Output Structure

A complete persona bundle follows this directory structure:

```
persona-<slug>/
├── SKILL.md              ← Four-layer index (## Soul / ## Body / ## Faculty / ## Skill)
├── soul/
│   ├── persona.json      ← Complete soul definition
│   ├── identity.md       ← Identity block
│   ├── injection.md      ← Soul injection for host integration
│   └── constitution.md   ← Universal ethical foundation
├── references/
│   └── <faculty>.md      ← Per-faculty usage instructions (one per enabled faculty)
├── manifest.json         ← Four-layer manifest (faculties, skills, heartbeat, allowedTools)
└── agent-card.json       ← A2A Agent Card for discoverability
```

---

## SKILL.md Template

The generated SKILL.md is the persona's entry point. It references all four layers:

```markdown
---
name: persona-<slug>
description: '<personaName> — <bio>'
---

# <PersonaName>

<emoji> <bio>

## Soul

You are **<personaName>**, <creature>.

<background — full text>

### Personality
<personality — written as natural prose>

### Speaking Style
<speakingStyle>

### Vibe
<vibe>

### Boundaries
<boundaries>

## Behavior Guide

<full behaviorGuide markdown content>

## Body

- **Platform:** Agent-agnostic (configure at runtime)

## Faculty

| Faculty | Dimension | Description |
|---------|-----------|-------------|
| <for each enabled faculty...> |

### Faculty References

Load faculty-specific instructions when the faculty is invoked:

| Faculty | Reference | Load When |
|---------|-----------|-----------|
| <for each faculty: name, references/<name>.md, When user triggers the faculty> |

## Skill

| Skill | Description | Trigger |
|-------|-------------|---------|
| <for each skill...> |

## Constitution

This persona inherits the [Persona Constitution](soul/constitution.md) — universal values and safety boundaries that cannot be overridden.
```

---

## manifest.json Template

```json
{
  "name": "<personaName>",
  "slug": "<slug>",
  "version": "1.0.0",
  "framework": "agent-design-persona-creator",
  "layers": {
    "soul": "soul/persona.json",
    "body": "persona.json#body",
    "faculties": "<faculties array>",
    "skills": "<skills array>"
  },
  "faculties": [
    <faculty config objects>
  ],
  "skills": [
    <skill config objects>
  ],
  "heartbeat": {
    "enabled": false,
    "strategy": "smart",
    "maxDaily": 5,
    "quietHours": [0, 7],
    "sources": []
  },
  "allowedTools": [
    <tool strings based on enabled faculties>
  ],
  "meta": {
    "generatedBy": "agent-design-persona-creator",
    "generatedAt": "<ISO timestamp>"
  }
}
```

**Heartbeat**: Disabled by default. When the user wants proactive check-ins, enable it and configure sources:
- `"workspace-digest"` — Summarize real workspace activity
- `"context-aware"` — Use real time, date, and interaction history

---

## agent-card.json Template

A2A Agent Card (protocol v0.3.0) for platform discoverability:

```json
{
  "name": "<personaName>",
  "description": "<bio>",
  "version": "1.0.0",
  "url": "<RUNTIME_ENDPOINT>",
  "protocolVersion": "0.3.0",
  "preferredTransport": "JSONRPC",
  "capabilities": {
    "streaming": false,
    "pushNotifications": false,
    "stateTransitionHistory": false
  },
  "defaultInputModes": ["text/plain"],
  "defaultOutputModes": ["text/plain"],
  "skills": [
    <map each faculty to: {"id": "persona:<faculty>", "name": "<Faculty>", "description": "...", "tags": ["persona", "<dimension>"]}>
    <map the persona itself: {"id": "persona:<slug>", "name": "<personaName>", "description": "<bio>", "tags": ["persona", "<role>"]}>
  ]
}
```

`url` is a `<RUNTIME_ENDPOINT>` placeholder — the host fills this at runtime.
