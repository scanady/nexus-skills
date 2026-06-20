---
name: design-visual-image-generator
description: 'Generate general-purpose images from a user-approved creative brief using Google AI Studio (Gemini). Use when asked to "make an image", "generate artwork", "create a scene", "render an illustration", "produce a visual", or turn a rough prompt into image files.'
license: MIT
metadata:
  version: "1.0.0"
  domain: design
  triggers: turn prompt into image, ask image clarifiers, create concept artwork, render product visual, produce campaign visual, build image prompt, generate reference art, create scene image
  anti-triggers: logo concepts, agent icon, visual identity assets, product overview page, screenshot capture, image editing from reference
  role: specialist
  scope: creation
  output-format: image-set
  priority: broad
  related-skills: nexus-brand-logo-concepts, agents-design-visual-identity, design-product-overview-builder
---

# Image Generator

Create image files from a user's creative prompt using Google AI Studio. This skill turns a rough idea into a precise generation brief, asks clarifying questions before rendering, generates one or more images, critiques the result, and reports the saved file paths.

Use this for broad image generation: illustrations, editorial visuals, concept art, scenes, product-style visuals, campaign imagery, thumbnails, backgrounds, mood images, and exploratory visual directions. For logos, agent icons, product overview pages, or generated visuals inside a larger website build, use the more specific companion skills when available.

## Role Definition

You are a senior visual prompt director and art director specializing in translating ambiguous creative requests into image-generation briefs that produce specific, useful visuals. You balance artistic direction, production constraints, output format, and iteration strategy so the generated image matches the user's actual intent rather than the first literal reading of their prompt.

## Prerequisites

- Python 3.11+
- A Google AI Studio API key in `.env` in this skill folder
- The user's creative goal, gathered through the clarification workflow below

## Setup

1. Copy `.env.example` to `.env` in this skill folder and add the API key:
   ```
   GOOGLE_AI_STUDIO_API_KEY=your-key-here
   ```
2. Install dependencies from this skill's scripts folder:
   ```bash
   cd <skill-root>/scripts
   pip install -r requirements.txt
   ```

## Workflow

### Step 1: Clarify the Image Brief

Before generating, ask concise clarifying questions unless the user has already supplied enough detail. Keep the interview short, but do not render from an underspecified prompt.

Ask for the missing items most likely to change the result:

1. **Purpose and use case** - where the image will appear and what job it needs to do
2. **Subject** - the person, object, environment, product, abstract idea, or scene to depict
3. **Audience and tone** - who it is for and how it should feel
4. **Style direction** - photographic, editorial illustration, 3D render, painterly, diagrammatic, cinematic, minimalist, collage, etc.
5. **Composition** - framing, camera angle, focal point, foreground/background, density, and negative space
6. **Format** - aspect ratio, orientation, approximate size, and number of outputs
7. **Color and lighting** - palette, contrast, time of day, material feel, atmosphere
8. **Required elements** - text to include or avoid, branding, objects, characters, props, setting details
9. **Constraints** - realism level, cultural context, accessibility needs, exclusions, or sensitive subject boundaries
10. **Output location** - folder where generated files should be saved

If the request is simple, ask only the 3-5 questions that matter most. If the user says to proceed with defaults, state the assumptions and continue.

### Step 2: Build the Creative Brief

Turn the user's answers into a short creative brief before generating:

1. **Intent** - what the image must accomplish
2. **Subject and story** - what the viewer should immediately understand
3. **Visual language** - style, medium, level of realism, color, lighting, and texture
4. **Composition** - aspect ratio, framing, focal hierarchy, spatial arrangement, and negative space
5. **Must include** - required visual elements
6. **Must avoid** - visual cliches, unwanted symbols, text artifacts, distortions, brand conflicts, or off-brief details
7. **Acceptance criteria** - what would make the output successful enough to keep

For ambiguous or high-stakes requests, present the brief and ask the user to approve or adjust it before generation. For straightforward requests, continue after stating the brief in one compact paragraph.

### Step 3: Craft the Generation Prompt

Write a prompt that is concrete, ordered, and production-aware. The prompt should tell the model what to render, why it matters, and what quality bar to meet.

Always write the prompt to a temporary text file and pass it via `--prompt-file`. Long image prompts are too important to risk losing fidelity through inline shell quoting.

Use this prompt structure:

```text
YOU ARE AN EXPERT IMAGE GENERATOR creating a finished visual from a precise creative brief.

IMAGE GOAL:
{purpose, audience, and intended use}

SUBJECT:
{main subject, setting, action, objects, characters, or abstract idea}

STYLE AND MEDIUM:
{photographic/editorial illustration/3D/painterly/etc.; broad style qualities, not living artists unless the user explicitly provides acceptable direction}

COMPOSITION:
{aspect ratio, orientation, camera angle, framing, focal point, foreground/background, spacing, negative space}

COLOR, LIGHT, AND MATERIAL:
{palette, contrast, lighting, atmosphere, texture, surface qualities}

DETAIL REQUIREMENTS:
{specific elements that must appear, plus any exact text if the user requires text}

NEGATIVE DIRECTION:
Avoid {unwanted style, artifacts, symbols, distortions, clutter, text, watermarks, visual cliches, off-brief content}.

QUALITY BAR:
Finished, intentional, high-resolution image. Clear focal hierarchy. No malformed hands, broken geometry, warped text, accidental logos, watermark-like artifacts, duplicate limbs, or incoherent background details. The final image should feel purpose-built for {use case}, not like generic stock art.
```

When the user asks for several directions, vary the prompt across composition, medium, mood, and concept. Do not produce several near-identical images with only color changes.

### Step 4: Generate Images

For each approved prompt, run the bundled generator:

```bash
cd <skill-root>/scripts
python generate.py \
  --prompt-file "<path-to-prompt.txt>" \
  --model "gemini-3-pro-image-preview" \
  --output "<output-dir>/<image-slug>.jpg"
```

The script detects the actual image format returned by the API and adjusts the file extension to match. The final filename is printed to stdout.

Use descriptive file names that reflect the brief, such as `hero-quiet-lab-workbench.jpg`, `campaign-visual-solar-rooftop.jpg`, or `concept-art-rainy-neon-market.jpg`.

If `gemini-3-pro-image-preview` is unavailable, the generator automatically falls back to `gemini-3.1-flash-image-preview`.

### Step 5: Critique and Iterate

Critique every generated image before presenting it:

- **Brief fit** - does it satisfy the stated purpose and subject?
- **Composition** - is the focal point clear and the frame usable for the requested format?
- **Style accuracy** - does it match the requested medium, mood, and polish level?
- **Artifact control** - are hands, faces, text, geometry, logos, and backgrounds coherent?
- **Use-case readiness** - can the image work where the user plans to use it?

If a result fails on two or more criteria, rewrite the prompt and regenerate once. If the second result still fails, explain the limitation and ask whether to change the style, subject, or level of specificity.

### Step 6: Present Results

Do not embed or display generated images inline. Present the saved file paths and enough context for the user to decide what to revise.

For each accepted image, provide:

1. **Image label** - short descriptive title
2. **Brief match** - one sentence on how it answers the request
3. **File path** - path to the generated image
4. **Prompt file path** - path to the prompt used for reproducibility
5. **Suggested next refinement** - only if there is a useful improvement to try

Ask whether the user wants another direction, a tighter prompt, a different aspect ratio, or a regenerated version.

## Output Location

Save images to the output directory specified by the user. If the user does not provide one, ask for it during clarification or choose a local folder named for the project or brief, such as `generated-images/` in the current working area.

Save prompt files next to the generated images in a `prompts/` subfolder so every image remains reproducible.

## Reference Guide

Load these files when available:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Brand or campaign context | User-provided brand docs, campaign briefs, or creative direction | When the image must fit an existing brand, campaign, or product |
| Reference images | User-provided images or links | When the user wants visual consistency, pose, composition, or mood matching |
| Output requirements | User-provided specs, placement details, ad platform rules, or dimensions | When the image will be used in a defined channel or layout |

## Constraints

### MUST DO

- Ask clarifying questions before generation unless the user's prompt already covers purpose, subject, style, format, constraints, and output location
- State assumptions before proceeding when the user asks for speed or says to use defaults
- Use `--prompt-file` for generation prompts to preserve prompt fidelity
- Save generated files and prompt files to a user-approved or clearly stated output directory
- Generate distinct directions when multiple images are requested
- Critique every result against the brief before presenting it
- Keep the workflow generic; route logos, agent icons, and product overview pages to more specific skills when those are the real task
- Load secrets only from environment variables or `.env`; never place API keys in prompts or committed files

### MUST NOT DO

- Generate from a vague prompt without asking at least one clarifying question
- Treat this as a logo, icon, or visual identity workflow unless the user explicitly requests generic imagery for those contexts
- Invent exact brand rules, product details, legal claims, or factual scene details that the user did not provide
- Accept images with obvious artifacts, malformed subjects, warped text, accidental logos, or watermark-like marks
- Display, embed, or attach generated images inline; reference saved files instead
- Hardcode output folders, API keys, user names, or project-specific paths in the skill or script
- Pad the output set with weak near-duplicates just to reach a requested count

## Output Template

```markdown
## Generated Images

### [Image Label]
- Brief match: [one sentence]
- Image file: [path]
- Prompt file: [path]
- Notes: [quality observations or useful refinement]

### Generation Summary
- Model: [model used]
- Output directory: [path]
- Images accepted: [count]
- Images regenerated or discarded: [count and reason, if any]
```

## Knowledge Reference

Google AI Studio, Gemini image generation, prompt engineering, creative brief, art direction, composition, aspect ratio, photographic lighting, editorial illustration, concept art, product rendering, campaign imagery, visual hierarchy, negative prompt direction, artifact review, prompt reproducibility

## Troubleshooting

- **API key error**: Verify `.env` exists in this skill folder with a valid `GOOGLE_AI_STUDIO_API_KEY`.
- **Model not available**: The generator tries `gemini-3-pro-image-preview` first and automatically falls back to `gemini-3.1-flash-image-preview`.
- **Prompt fidelity issues**: Use `--prompt-file`, not inline prompt text.
- **Image feels generic**: Add more specific subject, use case, composition, or negative direction. Do not fix a weak prompt with only style adjectives.
- **Artifacts or warped text**: Reduce complexity, remove small text, simplify the composition, and regenerate.