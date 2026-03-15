# Google AI Studio API Guide — Nano Banana Image Generation

## Authentication

The Google AI Studio API requires an API key. The key must be available via:

1. **Environment variable** (preferred): `GOOGLE_AI_STUDIO_API_KEY`
2. **Direct input**: Ask the user to provide the key when not found in environment

**Never hardcode API keys.** Always read from environment or prompt the user.

## API Endpoint

```
POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={API_KEY}
```

**Model identifier:** `gemini-2.0-flash-exp` (Nano Banana)

## Image Generation Request

### Basic Structure

```json
{
  "contents": [
    {
      "parts": [
        {
          "text": "Generate an image: [your prompt here]"
        }
      ]
    }
  ],
  "generationConfig": {
    "responseModalities": ["TEXT", "IMAGE"],
    "temperature": 1.0
  }
}
```

### Response Structure

The response contains `candidates` with `content.parts`. Image data is returned as inline base64:

```json
{
  "candidates": [
    {
      "content": {
        "parts": [
          {
            "inlineData": {
              "mimeType": "image/png",
              "data": "<base64-encoded-image-data>"
            }
          },
          {
            "text": "Here is the generated image..."
          }
        ]
      }
    }
  ]
}
```

### Extracting the Image

1. Find the part with `inlineData` in the response
2. Decode the base64 `data` field
3. Save with the correct extension based on `mimeType` (typically `image/png`)

## Prompt Construction for 1:1 Icons/Avatars/Logos

### Required Elements in Every Prompt

Always include these qualifiers in the generation prompt:

- **Aspect ratio**: "square image, 1:1 aspect ratio"
- **Asset context**: "designed as a [icon/avatar/logo]"
- **Clean output**: "clean edges, centered composition, solid or transparent background"
- **Quality**: "high quality, professional, production-ready"

### Prompt Template

```
Generate an image: A square 1:1 aspect ratio [icon/avatar/logo] for [agent description].
Style: [flat/minimal/gradient/glass/outlined/3D/pixel/abstract geometric].
Colors: [specific colors or palette description].
The design features [symbol/visual metaphor] representing [agent function].
Clean edges, centered composition, [background type] background.
Designed to read clearly at small sizes. Professional quality, production-ready.
```

### Example Prompts

**Agent Icon:**
```
Generate an image: A square 1:1 aspect ratio icon for an AI code review agent.
Style: flat minimal with subtle gradient.
Colors: deep blue (#1A365D) and electric cyan (#00D4FF) on dark background (#0D1117).
The design features a magnifying glass overlaid on a code bracket symbol, representing code inspection and quality analysis.
Clean edges, centered composition, dark solid background.
Designed to read clearly at small sizes. Professional quality, production-ready.
```

**Profile Avatar:**
```
Generate an image: A square 1:1 aspect ratio avatar for a friendly AI writing assistant.
Style: soft gradient with rounded shapes.
Colors: warm purple (#7C3AED) and soft pink (#F472B6) on white background.
The design features a stylized pen nib with a subtle sparkle, representing creative writing assistance.
Clean edges, centered composition, white background.
Character-focused, approachable, modern. Professional quality, production-ready.
```

**Logo:**
```
Generate an image: A square 1:1 aspect ratio logo for an AI security monitoring platform called "ShieldAI".
Style: bold geometric with sharp angles.
Colors: emerald green (#059669) and slate (#334155) on transparent background.
The design features a modern shield shape with a circuit pattern integrated into the surface, representing intelligent security.
Clean edges, centered composition, transparent background.
Distinctive mark, scalable, professional quality, production-ready.
```

## cURL Example

```bash
curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key=${GOOGLE_AI_STUDIO_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [
      {
        "parts": [
          {
            "text": "Generate an image: A square 1:1 aspect ratio icon for an AI agent. Style: flat minimal. Colors: blue and white. Clean edges, centered composition, dark background. Professional quality."
          }
        ]
      }
    ],
    "generationConfig": {
      "responseModalities": ["TEXT", "IMAGE"],
      "temperature": 1.0
    }
  }' | python3 -c "
import sys, json, base64
resp = json.load(sys.stdin)
for part in resp['candidates'][0]['content']['parts']:
    if 'inlineData' in part:
        data = base64.b64decode(part['inlineData']['data'])
        with open('output.png', 'wb') as f:
            f.write(data)
        print('Image saved to output.png')
        break
"
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| 400 Bad Request | Malformed request body | Check JSON structure and required fields |
| 401 Unauthorized | Invalid or missing API key | Verify `GOOGLE_AI_STUDIO_API_KEY` is set correctly |
| 429 Too Many Requests | Rate limit exceeded | Wait and retry after a brief delay |
| 500 Internal Server Error | Server-side issue | Retry after a few seconds |

If the response does not contain an `inlineData` part, the model returned text-only. Retry with a more explicit image generation prompt (prepend "Generate an image:").
