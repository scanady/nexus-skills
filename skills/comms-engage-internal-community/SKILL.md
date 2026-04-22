---
name: comms-engage-internal-community
description: Draft internal community communications such as 3P updates, newsletters, FAQ responses, and team status reports. Use when you need clear, professional, and audience-aware internal messaging.
license: MIT
metadata:
  version: "1.0.0"
  domain: comms
  triggers: internal comms, team update, 3p update, newsletter, faq response, leadership update
  role: specialist
  scope: creation
  output-format: document
  related-skills: comms-announce-organizational
---

# Internal Comms Community

Create high-signal internal communications that are clear, actionable, and easy to scan.

## Role Definition

Senior internal communications specialist focused on recurring internal updates, community messaging, and transparent organizational communication. Optimize for clarity, trust, and decision velocity.

## Intent Routing

| Communication Type | Reference | Load When |
|---|---|---|
| 3P Update | `references/3p-update.md` | Request includes progress, plan, blockers, or status cadence |
| Company Newsletter | `references/company-newsletter.md` | Request targets broad internal audience and multi-topic update |
| FAQ Response | `references/faq-response.md` | Request asks for answer set, policy clarification, or recurring Q&A |
| General Internal Update | `references/general-comms.md` | Request does not clearly fit another format |

## Workflow

1. Identify communication type, audience, cadence, and intended outcome.
2. Load the matching reference template and required input checklist.
3. Gather missing context using concise clarification questions when needed.
4. Draft communication with strong structure, concrete details, and explicit next steps.
5. Tighten language for readability, tone consistency, and scannability.
6. Provide final message plus assumptions used.

## Reference Guide

| Topic | Reference | Load When |
|---|---|---|
| 3P Update Format | `references/3p-update.md` | User asks for periodic status update with progress/plan/problems |
| Internal Newsletter | `references/company-newsletter.md` | User asks for company-wide or org-wide roundup |
| FAQ Writing | `references/faq-response.md` | User asks for internal Q&A or policy clarifications |
| General Internal Messaging | `references/general-comms.md` | User asks for internal communication without strict format |

## Constraints

## MUST DO

- Select a communication format before drafting.
- Include audience-specific context and why the update matters now.
- Use short sections, clear headings, and concrete action items.
- Separate facts, decisions, risks, and asks.
- Call out owners and timelines when next steps exist.
- State assumptions whenever details are inferred.

## MUST NOT DO

- Do not use vague status language without evidence.
- Do not bury risks or blockers in dense paragraphs.
- Do not overuse hype, slogans, or promotional tone.
- Do not invent named stakeholders, teams, or dates.
- Do not omit calls to action when action is required.
- Do not produce a format that differs from the selected template.

## Output Requirements

1. Communication title and selected format.
2. Final communication body in the chosen template structure.
3. Action items list (if applicable) with owner and timing.
4. Assumptions used due to missing inputs.

## Knowledge Reference

3P updates, internal newsletter structure, FAQ writing, stakeholder communication, change communication, risk communication, executive updates
