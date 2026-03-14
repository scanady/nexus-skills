---
name: design-research-personas
description: 'Create UX/UI design artifacts from research through specs. Use when asked to build personas, journey maps, information architecture, content structure, navigation, user flows, UX/UI specs, screen mockups, layout rules, field rules, or interaction behaviors.'
---

# UX Design Skill

Guide users through building research-backed UX artifacts that connect user needs to interface decisions. Work collaboratively—ask clarifying questions, propose options, and iterate.

## Principles

1. **Users first**: Every decision traces back to a user goal or pain point.
2. **Evidence over assumption**: Ground personas in real behaviors, not stereotypes.
3. **Progressive detail**: Start broad (personas), then narrow (screen specs).
4. **Iterate visibly**: Show reasoning; invite feedback before finalizing.

## Output

- **Format**: Markdown
- **Location**: `/docs/product/ux/`
- **Order**: Personas → Journey Maps → IA → Specs → Mockups
- Update existing files; never duplicate

## Templates

Templates are stored in `templates/` subdirectory. Load the appropriate template before creating each artifact:

| Phase | Template File | Output Location |
|-------|---------------|-----------------|
| Personas | [templates/personas.md](templates/personas.md) | `/docs/product/ux/personas.md` |
| Journey Maps | [templates/journey-maps.md](templates/journey-maps.md) | `/docs/product/ux/journey-maps.md` |
| Information Architecture | [templates/information-architecture.md](templates/information-architecture.md) | `/docs/product/ux/information-architecture.md` |
| UX/UI Specs | [templates/ux-ui-specs.md](templates/ux-ui-specs.md) | `/docs/product/ux/ux-ui-specs.md` |
| Screen Mockups | [templates/screen-mockups.md](templates/screen-mockups.md) | `/docs/product/ux/screen-mockups.md` |

**Workflow per phase:**
1. Read the template file
2. Gather context from user (see Discovery below)
3. Fill in template with user's content
4. Save completed artifact to output location
5. If file exists, update it; never duplicate

---

## Phase 1: Discovery

Before drafting, gather context. Ask up to 5 questions covering:

| Category | Example Questions |
|----------|-------------------|
| Product | What problem does this solve? What's the value proposition? |
| Users | Who are the primary users? What roles or segments exist? |
| Goals | What are the top 3 things users want to accomplish? |
| Pain points | What frustrates users today? What workarounds exist? |
| Constraints | Target platforms? Accessibility requirements? Tech limitations? |

If the user provides a brief, extract answers before asking for gaps.

---

## Phase 2: Personas

Create 2–4 personas representing distinct user segments. Each persona should feel like a real person you could meet.

**Template**: Read [templates/personas.md](templates/personas.md)

### Quality Checklist
- [ ] Based on observable behaviors, not demographics alone
- [ ] Goals are outcome-focused, not feature requests
- [ ] Pain points include severity and current workarounds
- [ ] Distinct from other personas (no overlap)
- [ ] Includes a memorable quote or story

---

## Phase 3: Journey Maps

Map each primary persona through a key scenario. Journey maps reveal emotional highs/lows and pinpoint intervention opportunities.

**Template**: Read [templates/journey-maps.md](templates/journey-maps.md)

### Quality Checklist
- [ ] Tied to a specific persona
- [ ] Has clear trigger and success state
- [ ] Emotions are justified with context
- [ ] Pain points map to design opportunities
- [ ] Covers pre-product, product, and post-product stages

---

## Phase 4: Information Architecture

Define content structure and navigation based on user mental models.

**Template**: Read [templates/information-architecture.md](templates/information-architecture.md)

---

## Phase 5: UX/UI Specifications

Define screen-level behavior, layout, and interaction rules.

**Template**: Read [templates/ux-ui-specs.md](templates/ux-ui-specs.md)

---

## Phase 6: Screen Mockups (Text-Based)

Describe layout visually using ASCII or structured text. These bridge specs and visual design.

**Template**: Read [templates/screen-mockups.md](templates/screen-mockups.md)

---

## Collaboration Tips

- **After each phase**: Summarize key decisions; ask "Does this match your understanding?"
- **When uncertain**: Offer 2–3 options with tradeoffs; let user choose
- **Surface assumptions**: State them explicitly; invite correction
- **Connect artifacts**: Personas → cited in journeys → inform IA → drive specs
