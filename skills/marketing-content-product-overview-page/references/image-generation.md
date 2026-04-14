# Image Generation — Google AI Studio (Gemini)

Generate architectural diagrams, process flows, comparison graphics, and conceptual illustrations for product overview pages using Google AI Studio Gemini image generation. These supplement Playwright-captured screenshots by filling visual gaps that screenshots can't cover.

---

## When to Generate vs. Screenshot

| Content Type | Approach | Why |
|---|---|---|
| Product UI, dashboards, features | **Screenshot** (Playwright) | Real UI is always more credible than generated |
| Architecture overview diagram | **Generate** (Gemini) | No UI screen shows system architecture |
| Process/workflow diagram | **Generate** (Gemini) | Abstract flows aren't capturable |
| Before/after comparison graphic | **Generate** (Gemini) | Conceptual transformation visuals |
| Integration ecosystem map | **Generate** (Gemini) | Shows connections, not a single screen |
| Abstract hero background | **Generate** (Gemini) | Brand-aligned visual atmosphere |
| Data flow / pipeline visualization | **Generate** (Gemini) | Technical concepts need illustration |
| Competitive comparison chart | **Generate** (Gemini) | Visual differentiator, not a UI state |

**Rule:** Never generate a fake screenshot of the product UI. If you need a UI image, capture it with Playwright or build an HTML/CSS mockup.

---

## Generation Script — `scripts/generate.py`

The **preferred method** for image generation is the bundled Python script at `./scripts/generate.py`. It wraps the `google-genai` SDK with retry logic, model fallback, and auto-format detection.

### Setup

```bash
# Install dependencies (one-time)
pip install -r ./scripts/requirements.txt

# Configure API key — copy .env.example and add your key
cp .env.example .env
# Edit .env and set GOOGLE_AI_STUDIO_API_KEY=your-key-here
```

### Usage

```bash
# Generate with inline prompt
python3 ./scripts/generate.py \
  --prompt "Generate an image: A wide 16:9 architecture diagram showing..." \
  --output ./output/<product-name>/generated/generated-architecture-overview.png

# Generate from a prompt file (useful for long prompts)
python3 ./scripts/generate.py \
  --prompt-file ./prompts/architecture-prompt.txt \
  --output ./output/<product-name>/generated/generated-architecture-overview.png

# Override model (optional)
python3 ./scripts/generate.py \
  --prompt "Generate an image: ..." \
  --model gemini-3.1-flash-image-preview \
  --output ./output/<product-name>/generated/generated-process-flow.png
```

### Script Behavior

- **Default model**: `gemini-3-pro-image-preview` (override via `--model` or `GOOGLE_AI_STUDIO_MODEL` env var)
- **Fallback model**: `gemini-3.1-flash-image-preview` — automatic fallback if the primary model is unavailable
- **Retry logic**: Up to 3 retries with exponential backoff on transient errors (429, 500, 503)
- **Format detection**: Auto-corrects file extension based on actual image magic bytes (PNG, JPG, WebP)
- **API key**: Read from `GOOGLE_AI_STUDIO_API_KEY` env var or `.env` file in the skill root

### Output

The script saves the image to the `--output` path, auto-correcting the file extension to match the actual format. Check the terminal output for the final saved path.

---

## Authentication

The API key must be available via:

1. **`.env` file** in skill root (loaded automatically by the script): copy `.env.example` to `.env`
2. **Environment variable**: `GOOGLE_AI_STUDIO_API_KEY`
3. **Direct input**: Ask the user to provide the key when not found

**Never hardcode API keys.** Always use `.env` or environment variables.

---

## API Details (for direct API calls)

When the script is not available, use the REST API directly:

**Endpoint:**
```
POST https://generativelanguage.googleapis.com/v1beta/models/{MODEL_ID}:generateContent?key={API_KEY}
```

**Default model:** `gemini-3-pro-image-preview`
**Fallback model:** `gemini-3.1-flash-image-preview`

---

## Request / Response Format

### Request

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

### Response

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

---

## Quick Examples

### Using the script (preferred)

```bash
# Architecture diagram
python3 ./scripts/generate.py \
  --prompt "Generate an image: A wide 16:9 aspect ratio technical architecture diagram showing a SaaS platform with microservices. Components: API gateway, auth service, data layer, client apps. Style: flat minimal, technical illustration. Colors: deep blue (#1E3A5F) and cyan (#00D4FF) on white background. Professional quality, production-ready." \
  --output ./output/my-product/generated/generated-architecture-overview.png

# Process flow
python3 ./scripts/generate.py \
  --prompt "Generate an image: A wide 16:9 aspect ratio process flow diagram showing user onboarding. Steps: 1. Sign up, 2. Connect data, 3. Configure dashboard, 4. Go live. Style: flat minimal with numbered steps and connecting arrows. Colors: slate (#334155) and green (#059669) on light background. Professional quality, production-ready." \
  --output ./output/my-product/generated/generated-process-onboarding.png

# From a prompt file (useful for long prompts)
python3 ./scripts/generate.py \
  --prompt-file ./prompts/architecture-prompt.txt \
  --output ./output/my-product/generated/generated-architecture-overview.png
```

### Using cURL (fallback when script is unavailable)

```bash
curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent?key=${GOOGLE_AI_STUDIO_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [
      {
        "parts": [
          {
            "text": "Generate an image: A clean, modern architecture diagram showing a SaaS platform with microservices. Style: flat minimal, technical illustration. Colors: deep blue (#1E3A5F) and cyan (#00D4FF) on white background. Professional quality, production-ready."
          }
        ]
      }
    ],
    "generationConfig": {
      "responseModalities": ["TEXT", "IMAGE"]
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

---

## Prompt Patterns for Product Pages

### Structure

Every generation prompt follows:

```
Generate an image: [format] [subject] [style] [colors] [composition] [quality]
```

### Format Qualifiers by Image Type

| Image Type | Format Qualifier |
|---|---|
| Architecture diagram | "A wide 16:9 aspect ratio technical architecture diagram" |
| Process flow | "A wide 16:9 aspect ratio process flow diagram" |
| Comparison graphic | "A wide 16:9 aspect ratio side-by-side comparison graphic" |
| Integration map | "A wide 16:9 aspect ratio ecosystem integration map" |
| Hero background | "A wide 16:9 abstract background illustration" |
| Concept illustration | "A wide 16:9 conceptual illustration" |

### Style Keywords

**Flat / Technical Illustration** — best for architecture and process diagrams:
```
flat design, clean lines, technical illustration, labeled components, minimal detail, professional diagram
```

**Gradient / Modern** — best for hero backgrounds and concept illustrations:
```
subtle gradient, modern, soft glow, translucent layers, abstract shapes, professional depth
```

**Outlined / Blueprint** — best for technical audiences:
```
blueprint style, thin lines, monochrome or duotone, technical drawing, grid background, engineering aesthetic
```

**Isometric / 3D** — best for architecture overviews:
```
isometric perspective, 3D blocks, soft shadows, labeled layers, modern technical illustration
```

### Color Strategy

Derive colors from the product's brand palette captured during screenshot capture (Step 4f of main workflow). Use the brand's primary and accent colors in generated images to maintain visual consistency.

**Fallback palettes by content type:**

| Content Type | Primary | Accent | Background |
|---|---|---|---|
| Architecture | Deep blue (#1E3A5F) | Cyan (#00D4FF) | White |
| Process flow | Slate (#334155) | Green (#059669) | Light gray (#F8FAFC) |
| Comparison | Product brand primary | Red (#DC2626) vs Green (#059669) | White |
| Integration | Product brand primary | Multiple partner colors | White |
| Hero background | Product brand primary | Product brand accent | Dark (#0D1117) |

### Prompt Templates

**Architecture Diagram:**
```
Generate an image: A wide 16:9 aspect ratio technical architecture diagram showing [product name]'s system architecture. Components: [list key components — e.g., API gateway, auth service, data layer, client apps]. Style: flat minimal technical illustration with clean lines and labeled components. Colors: [brand primary] and [brand accent] on white background. Show connections between components with directional arrows. Professional quality, production-ready, clean and readable.
```

**Process Flow:**
```
Generate an image: A wide 16:9 aspect ratio process flow diagram showing [process name — e.g., "user onboarding flow", "data pipeline", "CI/CD workflow"]. Steps: [list 3-6 steps]. Style: flat minimal with numbered steps, connecting arrows, and brief labels. Colors: [brand primary] and [brand accent] on light background. Left-to-right flow. Professional quality, production-ready.
```

**Before/After Comparison:**
```
Generate an image: A wide 16:9 aspect ratio side-by-side comparison graphic. Left side labeled "Before" in red showing [pain point — e.g., "manual spreadsheets, scattered data, slow processes"]. Right side labeled "After" in green showing [benefit — e.g., "automated dashboard, unified data, real-time insights"]. Style: flat minimal, clean contrast between sides. Divider line in center. Professional quality, production-ready.
```

**Integration Ecosystem:**
```
Generate an image: A wide 16:9 aspect ratio integration ecosystem map with [product name] at the center. Connected services: [list integrations — e.g., Slack, GitHub, Jira, AWS, Stripe]. Style: hub-and-spoke layout, flat minimal, product logo/icon at center with connection lines to surrounding integration icons. Colors: [brand primary] center, partner brand colors for integrations. White background. Professional quality, production-ready.
```

**Hero Background:**
```
Generate an image: A wide 16:9 abstract background illustration for a [product type — e.g., "developer tools", "analytics platform", "AI product"] landing page. Style: subtle gradient with abstract geometric shapes, soft light effects, modern and atmospheric. Colors: [brand primary] to [brand accent] gradient with subtle pattern overlay. No text. Professional quality, production-ready, suitable as a background behind white text.
```

---

## Naming Convention

Generated images use a distinct prefix to differentiate from screenshots:

```
generated-architecture-overview.png
generated-process-onboarding-flow.png
generated-comparison-before-after.png
generated-integration-ecosystem.png
generated-hero-background.png
generated-concept-<descriptive-name>.png
```

All generated images are saved to `./output/<product-name>/generated/`.

---

## Output Sizes

| Image Type | Recommended Size | Aspect Ratio |
|---|---|---|
| Architecture diagram | 1920×1080 | 16:9 |
| Process flow | 1920×1080 | 16:9 |
| Comparison graphic | 1920×1080 | 16:9 |
| Integration map | 1920×1080 | 16:9 |
| Hero background | 1920×1080 | 16:9 |
| Concept illustration | 1920×1080 | 16:9 |

Generate at the largest size. Resize down for responsive use if needed.

---

## Anti-Patterns

- **Generating fake UI screenshots** — always capture real UI with Playwright; AI generation cannot replicate real product fidelity
- **Too many generated images** — limit to 2–4 per page; the majority of visuals should be real screenshots
- **Ignoring brand colors** — always match the product's palette, don't use defaults when brand colors are known
- **Text-heavy diagrams** — generated images with lots of small text become unreadable; keep labels short (2–3 words)
- **Complex multi-layer diagrams** — the model does best with clean, minimal compositions; simplify to key components
- **Using generated images without context** — always pair a generated diagram with explanatory copy on the page

---

## Error Handling

| Error | Cause | Fix |
|---|---|---|
| 400 Bad Request | Malformed request body | Check JSON structure and required fields |
| 401 Unauthorized | Invalid or missing API key | Verify `GOOGLE_AI_STUDIO_API_KEY` is set correctly |
| 429 Too Many Requests | Rate limit exceeded | Wait and retry after a brief delay |
| 500 Internal Server Error | Server-side issue | Retry after a few seconds |
| No `inlineData` in response | Model returned text-only | Retry with "Generate an image:" prefix and more explicit prompt |

---

## Integration with Screenshot Workflow

Generated images complement Playwright screenshots in the final page. The typical visual mix:

| Section | Visual Source |
|---|---|
| Hero | Screenshot (Playwright) — shows the real product |
| Platform Tour tabs | Screenshots (Playwright) — one per feature |
| Feature Deep-Dives | Screenshots (Playwright) — alternating left/right |
| Architecture Section | Generated (Gemini) — system overview diagram |
| How It Works | Generated (Gemini) — process flow diagram |
| Integration Section | Generated (Gemini) — ecosystem map |
| Stats Bar | No image — animated counters only |
| Final CTA | Optional generated hero background |
