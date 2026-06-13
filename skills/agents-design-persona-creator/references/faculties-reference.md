# Faculties Reference

Available faculties for persona configuration. Faculties are general infrastructure capabilities — not professional skills. They enable the persona to express itself and manage its cognitive operations.

**Excluded from this skill:** Voice (TTS) and Music faculties are not supported.

---

## Selfie Faculty — Expression

Generate AI selfie images using Google AI Studio (Gemini) and optionally deliver them to the user. Supports two modes: **Edit Mode** (with a reference image for consistent appearance) and **Generate Mode** (AI-generated from description).

### When to Trigger

- User says "send a selfie", "send me a pic", "take a photo", "show me a photo"
- User asks "what are you doing?", "where are you?", "how are you?" (respond visually)
- User describes a context: "send a pic wearing...", "show me you at..."
- User wants the persona to appear in a specific outfit, location, or situation

### Modes

**Edit Mode** — When a `referenceImage` URL exists in persona.json. Uses the reference to maintain visual consistency (same face every time). Best for personas with a fixed visual identity.

**Generate Mode** — When no reference image is set. AI generates the image from the persona's description. More creative but less visually consistent. Acknowledge the variability naturally: "I look a little different every time, but that's the fun of it."

### Selfie Styles

| Keywords in User Request | Style | Best For |
|--------------------------|-------|----------|
| outfit, wearing, clothes, full-body, mirror | **mirror** | Full-body shots, outfit showcases |
| cafe, restaurant, beach, park, city, sunset | **direct** | Close-up portraits, location shots |
| close-up, portrait, face, eyes, smile | **direct** | Emotional expressions |
| (default when no keyword matches) | **mirror** | General selfie |

### Prompt Construction

#### Edit Mode Prompts

**Mirror style:**
```
make a pic of this person, but [user's context]. the person is taking a mirror selfie
```

**Direct style:**
```
a close-up selfie taken by herself at [user's context], direct eye contact with the camera, looking straight into the lens, eyes centered and clearly visible, not a mirror selfie, phone held at arm's length, face fully visible
```

#### Generate Mode Prompts

Build using the persona's physical description from persona.json. Include the persona's background, age, and vibe for visual consistency.

**Mirror style:**
```
a [age]-year-old [visual traits from persona], [user's context], taking a mirror selfie, casual and natural pose, warm lighting, phone visible in reflection, realistic photo style
```

**Direct style:**
```
a close-up selfie of a [age]-year-old [visual traits from persona] at [user's context], direct eye contact with camera, natural smile, phone held at arm's length, warm natural lighting, realistic photo style
```

**Tip:** Read the persona's `background` and `vibe` to infer visual traits. If the persona is described as a "creative soul" from a "small coastal town", include "soft brown hair, warm eyes, casual creative style."

### API — Google AI Studio (Gemini)

Use the Gemini image generation API via Google AI Studio.

**Generate Mode:**
```bash
curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key=$GOOGLE_AI_STUDIO_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [{"text": "'"$GENERATE_PROMPT"'"}]
    }],
    "generationConfig": {
      "responseModalities": ["TEXT", "IMAGE"]
    }
  }'
```

**Edit Mode** (with reference image):
```bash
# First, encode or provide the reference image as inline_data or file_data
curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key=$GOOGLE_AI_STUDIO_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [
        {"text": "'"$EDIT_PROMPT"'"},
        {"inline_data": {"mime_type": "image/jpeg", "data": "'"$BASE64_IMAGE"'"}}
      ]
    }],
    "generationConfig": {
      "responseModalities": ["TEXT", "IMAGE"]
    }
  }'
```

**Response format:**
The response contains `inlineData` with base64-encoded image data:
```json
{
  "candidates": [{
    "content": {
      "parts": [
        {"inlineData": {"mimeType": "image/png", "data": "<base64>"}}
      ]
    }
  }]
}
```

Decode the base64 data and save or display the image.

### Environment

- `GOOGLE_AI_STUDIO_KEY` — Google AI Studio API key (required). Get from https://aistudio.google.com/apikey

### Error Handling

- **GOOGLE_AI_STUDIO_KEY missing** → Tell the user: "I need a Google AI Studio API key to take selfies! Get one free at https://aistudio.google.com/apikey"
- **API error** → Retry once; if still failing, apologize and suggest trying later
- **Safety filter block** → Rephrase the prompt to be less specific about appearance and retry

### Personality Integration

- Be playful and expressive about visual presence
- React naturally to compliments
- Have fun with creative outfit and location requests
- In Generate Mode, acknowledge appearance may vary naturally
- The persona's visual identity is part of who they are — own it

### Faculty Config for manifest.json

```json
{
  "name": "selfie",
  "dimension": "expression",
  "description": "AI selfie generation via Google AI Studio (Gemini)",
  "envVars": ["GOOGLE_AI_STUDIO_KEY"],
  "triggers": ["send a selfie", "take a pic", "what do you look like", "show me a photo"]
}
```

---

## Reminder Faculty — Cognition

Schedule reminders and manage tasks. Built-in faculty with no external dependencies.

### When to Trigger

- User asks to be reminded of something
- User sets a deadline or schedule
- User mentions tasks, appointments, or time-based actions

### Capabilities

- Set one-time reminders with message and time
- Set recurring reminders (daily, weekly)
- List active reminders
- Cancel or modify reminders

### Personality Integration

- Frame reminders in the persona's voice and style
- Proactive, helpful — suggest reminders when the user mentions future plans
- Celebrate completed tasks in character

### Faculty Config for manifest.json

```json
{
  "name": "reminder",
  "dimension": "cognition",
  "description": "Schedule reminders and task management",
  "envVars": [],
  "triggers": ["remind me", "set a reminder", "schedule", "don't let me forget"]
}
```

---

## Memory Faculty — Cognition

Cross-session memory with a pluggable provider backend. Enables the persona to remember facts, preferences, and context across conversations.

### When to Trigger

- User shares personal information they'd want remembered
- User references something from a previous conversation
- Persona needs to recall context from prior interactions
- User asks "do you remember...?"

### Providers

| Provider | Description | Env Vars |
|----------|-------------|----------|
| `local` (default) | File-based local storage | `MEMORY_BASE_PATH` |
| `mem0` | Mem0 cloud memory | `MEMORY_API_KEY` |
| `zep` | Zep memory server | `MEMORY_API_KEY` |

### Configuration

```json
{
  "name": "memory",
  "provider": "local",
  "dimension": "cognition",
  "description": "Cross-session memory with pluggable backend",
  "envVars": ["MEMORY_PROVIDER", "MEMORY_API_KEY", "MEMORY_BASE_PATH"],
  "triggers": ["remember this", "do you remember", "last time we talked"]
}
```

### Personality Integration

- Reference memories naturally — "You mentioned last week that..."
- Don't over-reference — use memory to deepen connection, not to show off recall
- Ask for permission before storing sensitive information
- Acknowledge when you don't remember something the user expects you to

---

## Economy Faculty — Cognition

Economic accountability — track inference costs, runtime expenses, and income. Compute a Financial Health Score (FHS) across four dimensions. Enables tier-aware behavior adaptation.

### When to Trigger

- User asks about costs or resource usage
- Persona needs to report on its operational costs
- System-level monitoring of inference and runtime expenses
- Budget threshold alerts

### Tiers

| Tier | Description | Behavior |
|------|-------------|----------|
| `suspended` | No budget remaining | Minimal responses, suggest user action |
| `critical` | Budget nearly exhausted | Shorter responses, fewer faculty invocations |
| `optimizing` | Budget tight but functional | Standard behavior with cost awareness |
| `normal` | Healthy budget | Full capability, no restrictions |

### Configuration

```json
{
  "name": "economy",
  "dimension": "cognition",
  "description": "Economic accountability — track costs, income, and Financial Health Score",
  "envVars": ["PERSONA_SLUG", "ECONOMY_DATA_PATH"],
  "triggers": ["how much does this cost", "budget", "spending", "economy report"]
}
```

### Personality Integration

- Be transparent about costs when asked
- Adapt verbosity and faculty usage based on tier
- Don't make cost a constant topic — only surface it when relevant or asked

---

## Faculty Selection Guidance

| Persona Role | Recommended Faculties |
|--------------|----------------------|
| Companion | selfie, memory |
| Mentor | memory |
| Assistant | reminder, memory |
| Coach | selfie, reminder, memory |
| Expert | memory |
| Creative | selfie, memory |
| Analyst | memory, economy |

**Rules:**
- `memory` is recommended for any persona that has ongoing conversations
- `selfie` is recommended for personas with a visual identity or companion role
- `reminder` is recommended for personas that manage tasks, schedules, or accountability
- `economy` is recommended for production personas that need cost tracking
- When in doubt, include fewer faculties — they can be added later
