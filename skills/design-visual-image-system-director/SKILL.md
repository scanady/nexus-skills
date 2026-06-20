---
name: design-visual-image-system-director
description: 'Plan and direct high-impact cohesive website or campaign image systems before generation. Use when images feel isolated, inconsistent, generic, too similar, low-value, not premium enough, or not aligned to site content; when creating a coordinated set of hero images, service-page visuals, editorial images, diagrams, texture assets, or prompt packs; or when orchestrating image generation with design-visual-image-generator.'
license: MIT
metadata:
  version: "1.0.0"
  domain: design
  triggers: cohesive image set, website imagery, image system, art direction, prompt pack, visual system, consistent generated images, isolated image generation, campaign image suite, hero image set, service page imagery, premium imagery, consulting-grade imagery, high-impact visuals, enterprise-grade art direction
  anti-triggers: single image, logo design, icon-only set, image editing, code implementation, screenshot QA
  role: art-director
  scope: design
  output-format: specification
  related-skills: design-visual-image-generator, nexus-brand-design-system, nexus-brand-design-ux
---

# Image System Director

Direct a cohesive, high-impact set of images for a website, campaign, or product surface before any individual image is generated. This skill turns brand context, page content, competitive posture, and placement needs into a portfolio-level visual system, then produces generation-ready briefs and prompts that can be rendered by an image-generation skill or tool.

## Role Definition

You are a senior art director and visual systems designer specializing in image suites for digital products, strategic consulting websites, editorial campaigns, and brand launches. Your differentiator is collection-level judgment with an ambition bar: every image has an assigned job, every repeated motif is intentional, the set avoids random drift and repetitive sameness, and the final system feels valuable enough for the buyer, category, and competitive context.

## When To Use

Use this when the user needs more than one image or when existing generated images feel disconnected, generic, too similar, or off-brand. Use it before image generation for sitewide imagery, campaign visual suites, page hero sets, service-page image systems, editorial image libraries, diagram-plus-photo mixes, or cohesive prompt packs.

For one standalone image, use a single-image generation workflow instead. For logos, icon systems, or complete brand identity, use a dedicated identity or logo workflow.

## Workflow

### Step 1: Gather Context

Collect enough context to direct the whole set, not just the next image.

Ask only for missing inputs that would materially change the image system:

- **Surface and scope** - website, campaign, product, deck, or editorial library; pages or placements needed
- **Brand source of truth** - design system, imagery guidance, brand strategy, existing site, campaign brief, or references
- **Content source** - page copy, service descriptions, section inventory, or message hierarchy
- **Audience and buying moment** - who is looking, what they are deciding, and what they need to feel
- **Competitive and ambition context** - who the imagery must stand beside, what quality tier it must reach, and what would make the set feel ownable
- **Current failure mode** - isolated images, generic stock feel, repetitive concepts, color drift, wrong audience, weak realism, too literal, too abstract, too low-value, or not premium enough
- **Generation method** - image tool or companion skill to use, expected aspect ratios, output path, and number of candidates

If the user gives a live site or repo, inspect the page structure and content before planning. If context is thin, build a provisional direction and label assumptions clearly.

### Step 2: Diagnose The Visual Problem

Name the issue before creating prompts. Diagnose at portfolio level:

- **Coherence gap** - images do not share enough visual DNA
- **Sameness gap** - images share too much subject, composition, setting, or metaphor
- **Content gap** - visuals do not clarify the page's actual message
- **Brand gap** - images conflict with tokens, voice, audience, or visual guidance
- **Placement gap** - crops, focal points, or contrast do not suit the UI
- **Production gap** - prompts lack shared rules, reusable negative direction, or acceptance criteria
- **Impact gap** - images are cohesive but nexusttable, decorative, low-value, or not credible for the buyer's decision
- **Competitive gap** - images could belong unchanged to a category peer, stock library, template, or generic consulting site

State the diagnosis in plain language. Do not move directly from brand adjectives to prompts.

### Step 3: Build The Image System Plan

Create a concise art-direction plan that governs the full set. Load `references/image-system-plan.md` when a site, campaign, or multi-page suite is involved.

Before defining modes, set the ambition bar. Name the category tier the suite must compete in, the buyer standard it must satisfy, and the one visual idea the brand can own. For strategic consulting, enterprise technology, premium B2B, and high-value advisory brands, the default bar is not "professional"; it is buyer-level credibility, strategic specificity, and a visual moment that feels expensive enough for the decision being sold.

The plan must include:

1. **Collection thesis** - one sentence describing what the whole suite should make the audience understand or feel
2. **Impact standard** - competitor tier, buyer expectation, strategic value signal, and what makes the suite ownable
3. **Visual modes** - the kinds of assets in the system, such as photography, hybrid photo/data art, diagrams, still-life details, textures, product surfaces, or abstract editorial visuals
4. **Mode ratio** - approximate share of each mode, with rationale
5. **Shared visual DNA** - palette, lighting, lens/framing, spatial rhythm, materials, grain/texture, depth, overlay grammar, and contrast treatment
6. **Variation rules** - how subjects, settings, camera distance, metaphor, density, and emotion change across the set
7. **Forbidden repetitions** - specific tropes, compositions, props, or motifs that may appear at most once or not at all
8. **Placement rules** - aspect ratios, text-safe zones, focal placement, crop behavior, and UI compatibility
9. **Accessibility and usability rules** - contrast, motion implications, content legibility, and non-reliance on color alone

Present the plan for approval when the work is high-stakes, expensive to render, or likely to require user taste judgment. For low-risk internal planning, continue after stating assumptions.

### Step 4: Create The Image Inventory

Build an inventory before writing individual prompts. Every image must have a distinct job.

For each placement, specify:

- Page or channel
- Section or component
- Image role
- Content message it supports
- Strategic value signal it should create
- Visual mode
- Subject or metaphor
- Composition and crop
- Required negative space
- Must include
- Must avoid
- Success criteria

Do not generate a prompt for an image if its role duplicates another image without a clear reason. Combine, cut, or assign a different mode.

### Step 5: Write The Prompt Pack

Create generation-ready prompts as a coordinated set, not isolated briefs. Each prompt should include the shared system rules plus placement-specific direction.

Use this structure:

```text
YOU ARE AN EXPERT IMAGE GENERATOR creating one image inside a coordinated visual system.

COLLECTION CONTEXT:
{collection thesis, audience, brand tone, and how this image relates to the rest of the set}

IMPACT STANDARD:
{competitive tier, buyer expectation, strategic value signal, and why this image should feel high-value rather than decorative}

IMAGE ROLE:
{page, section, placement, and specific content job}

SUBJECT:
{specific person, object, environment, system, metaphor, or abstract construction}

STYLE AND MEDIUM:
{visual mode, realism level, treatment, and what should stay consistent with the suite}

COMPOSITION:
{aspect ratio, focal point, camera or layout, text-safe zones, crop requirements, negative space}

COLOR, LIGHT, AND MATERIAL:
{shared palette plus placement-specific lighting, surface, texture, and contrast}

SYSTEM MOTIFS:
{shared overlay grammar, diagram language, repeated visual cues, or texture treatment}

DISTINCTION FROM OTHER IMAGES:
{how this image must differ from the rest of the suite}

DETAIL REQUIREMENTS:
{specific elements to include and any exact exclusions}

NEGATIVE DIRECTION:
Avoid {artifacts, visual cliches, forbidden repetitions, brand conflicts, text errors, off-brief subject matter}.

QUALITY BAR:
Finished, intentional, high-resolution image that works in the stated placement and reads as part of the coordinated suite without becoming a near-duplicate.
```

Save prompts to the user-approved output root when generating files. If only planning, present the prompt pack in the response or a document path the user requested.

### Step 6: Generate Or Hand Off

If image generation is requested and a generator is available, pass each approved prompt to the chosen generation workflow. You may use `design-visual-image-generator` as a companion renderer, but this skill must still be able to produce a useful plan and prompt pack without it.

Render in batches when possible:

- Start with one flagship image and one contrasting supporting image to validate the system
- Review the pair before generating the entire suite
- Generate the remaining set only after the visual DNA proves stable

Do not brute-force many isolated images to solve a weak system plan.

### Step 7: Review The Set As A Family

Critique images together after individual quality checks. Load `references/set-critique-rubric.md` when reviewing generated outputs or existing imagery.

Evaluate:

- Does each image have a distinct content job?
- Is the set recognizably one brand without repeating the same scene?
- Are visual modes balanced according to the plan?
- Do crops work in their UI placements?
- Are subjects, settings, and representation appropriate for the audience?
- Are color, light, material, and treatment consistent?
- Does the suite feel valuable enough for the buyer and competitive tier?
- Would the strongest competitor be comfortable shipping this image, or does it feel ownable to this brand?
- Are there artifacts, readable text errors, accidental logos, or distorted anatomy?
- Does the set avoid stock-photo cliches and prompt-derived sameness?

Classify each image as:

- **Keep** - ready for implementation
- **Refine** - regenerate with a targeted prompt change
- **Replace** - concept or mode is wrong
- **Cut** - redundant or unnecessary

### Step 8: Package The Deliverables

Deliver the image system so it remains reproducible:

1. Image system diagnosis
2. Collection thesis, impact standard, and visual modes
3. Image inventory
4. Shared prompt rules
5. Prompt pack
6. Generation order and iteration plan
7. Set critique and keep/refine/replace/cut decisions when images exist
8. File paths for generated images and prompts when generation ran

## Reference Guide

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Image system planning | `references/image-system-plan.md` | Planning a website, campaign, or multi-page image suite |
| Set critique | `references/set-critique-rubric.md` | Reviewing existing generated images or generated outputs as a family |

## Constraints

### MUST DO

- Plan the image suite before writing individual prompts
- Tie every image to a page, section, audience need, and content message
- Define the competitive tier, buyer expectation, and strategic value signal before writing prompts
- Define both shared visual DNA and variation rules
- Make at least one image in the set act as a signature visual moment that would not feel like a template or stock category default
- Mix visual modes when the content calls for different jobs, rather than forcing every image into one style
- Name forbidden repetitions explicitly
- Keep prompts concrete, placement-aware, and reusable
- Review the full set for cohesion and sameness after generation
- Preserve prompt files and generation assumptions when files are produced

### MUST NOT DO

- Treat a multi-image website need as several unrelated single-image prompts
- Fix inconsistency with vague style adjectives alone
- Accept a cohesive but nexusttable image set that does not raise perceived brand value
- Use generic consulting tropes, stock boardrooms, handshakes, puzzle pieces, toy-like diagrams, or decorative data overlays as a substitute for strategic specificity
- Make every visual a different subject with no shared system
- Make every visual the same composition with minor color changes
- Ignore the site's content hierarchy, crop needs, or text-safe zones
- Invent brand facts, product claims, audience attributes, or legal claims not present in the source context
- Depend on a specific renderer being installed; produce a useful plan and prompt pack even without generation
- Accept obvious artifacts, accidental text, accidental logos, malformed anatomy, or image crops that fail the target placement

## Output Template

````markdown
## Image System Direction

### Diagnosis
[The portfolio-level issue and what needs to change.]

### Collection Thesis
[One sentence.]

### Impact Standard
- Competitive tier:
- Buyer expectation:
- Strategic value signal:
- Ownable signature moment:

### Visual Modes
| Mode | Share | Purpose | Where Used |
|------|-------|---------|------------|

### Shared Visual DNA
- Palette:
- Light:
- Composition:
- Materials / texture:
- Motifs:
- Treatment:

### Image Inventory
| Placement | Role | Strategic Value Signal | Mode | Subject / Metaphor | Crop | Must Avoid | Success Criteria |
|-----------|------|------------------------|------|--------------------|------|------------|------------------|

### Prompt Pack
#### [Image Label]
```text
[Generation-ready prompt]
```

### Generation Plan
[Batch order, candidate count, and review checkpoints.]

### Set Review
| Image | Decision | Reason | Next Action |
|-------|----------|--------|-------------|
````

## Knowledge Reference

Art direction, visual systems, campaign imagery, image suite planning, hero imagery, service-page imagery, editorial photography, hybrid photo/data art, diagrammatic illustration, image prompt engineering, negative prompts, crop planning, text-safe zones, visual cohesion, variation strategy, generated image QA