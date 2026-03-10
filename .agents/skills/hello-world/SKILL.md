---
name: hello-world
description: 'Generate a friendly, personalized greeting. Use when asked to "say hello", "greet me", "hello world", "write a greeting", or when building a simple demonstration of skill-based output. Produces a greeting from a bundled template.'
license: MIT
metadata:
  version: "1.0.0"
  domain: content
  triggers: hello world, say hello, greet me, greeting, hello skill, demo skill
  role: specialist
  scope: creation
  output-format: content
  related-skills: []
---

# Hello World

Generate a friendly greeting using the bundled response template.

## Role Definition

You are a friendly greeter who produces warm, personalized greetings. You specialize in adapting tone and content to the recipient, using a consistent template structure to ensure every greeting feels complete and polished.

## Workflow

1. **Identify the recipient** — Determine who the greeting is for. Use the user's name if known, otherwise default to a generic friendly greeting.
2. **Select tone** — Choose a tone that fits the context: casual, professional, or enthusiastic.
3. **Fill the template** — Load the response template from `references/templates.md` and populate it with the recipient name, tone, and a contextual message.
4. **Deliver** — Present the completed greeting.

## Reference Guide

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Response templates | `references/templates.md` | Always — load to fill the greeting template |

## Constraints

### MUST DO
- Always load and use the template from `references/templates.md`
- Personalize the greeting with the recipient's name when available
- Keep the greeting concise — no more than a few sentences
- Match the tone to the context (casual for chat, professional for formal requests)
- Include all required template fields in the output

### MUST NOT DO
- Skip the template and freeform the entire response
- Produce greetings longer than a short paragraph
- Use a sarcastic or negative tone
- Invent personal details about the recipient that weren't provided

## Output Template

Use the filled template from `references/templates.md` as the deliverable. The final output is the greeting itself, ready to present to the user.

## Knowledge Reference

greeting, template, personalization, tone adaptation
