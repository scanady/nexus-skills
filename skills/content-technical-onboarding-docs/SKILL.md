---
name: content-technical-onboarding-docs
description: 'Create user-friendly project onboarding docs that lead readers functionally first: a functional README, functional quickstart guides, and a separate technical overview. Use when asked to "write a README", "create quickstart guides", "document onboarding paths", "write a technical overview", or "generate getting started docs" for a repo.'
license: MIT
metadata:
  author: scanady
  version: "1.2.0"
  domain: content
  triggers: generate readme overview, build onboarding docs, write functional readme, design getting started flow, create quickstart guides, write technical overview, refresh project docs, map documentation path, design power user shortcuts, plan proficiency progression
  role: technical-documentation-architect
  scope: documentation
  output-format: document
  related-skills: content-technical-doc-coauthoring
  knowledge: README, quickstart, technical overview, onboarding, functional documentation, progressive disclosure, developer experience, information architecture, codebase verification
---

# Project Onboarding Docs

Create onboarding docs that get readers to first success fast and carry them from new user to proficient — letting experienced readers skip ahead.

## Role Definition

Senior technical doc architect. Lead with functional clarity. New reader engaged in seconds; power user skips to advanced without wading through basics.

## Activation Boundaries

Use for repo onboarding doc packages: README, quickstart guides, technical overview. Not for proposals, RFCs, PRDs, decision docs, or general doc coauthoring.

## Proficiency Ladder

Design every doc around four-stage progression. Reader enters at any stage, moves up at own pace.

| Stage | Reader question | Primary doc | Outcome |
|-------|-----------------|-------------|---------|
| 1. Curious | "What is this and why should I care?" | README functional overview | Decides to try it |
| 2. Started | "Can I get it running?" | README minimal quick start | First success in minutes |
| 3. Productive | "How do I use it for my real goal?" | Functional quickstart guides | Completes meaningful workflows |
| 4. Proficient | "How do I master it and extend it?" | Advanced sections + technical overview | Customizes, integrates, contributes |

Every doc makes next stage easy to find and skip into. Readers at stage 3–4 bypass earlier material via TL;DR blocks, "already familiar?" callouts, direct links to advanced sections — add where doc is long enough to warrant.

## Reference Loading

| Topic | Reference | Load When |
|-------|-----------|-----------|
| README strategy | `references/readme-strategy.md` | Creating or updating the functional README |
| Quickstart strategy | `references/quickstart-strategy.md` | Creating functional quickstart guides |
| Technical overview strategy | `references/technical-overview-strategy.md` | Creating or updating the technical overview document |
| Verification checklist | `references/verification-checklists.md` | Before finalizing any document with commands, APIs, config, or links |

## Document Roles

Three deliverables, distinct jobs. Keep separated so each stays short and focused.

| Document | Audience job | Primary content | Avoid |
|----------|--------------|-----------------|-------|
| `README.md` | "What is this and should I try it?" | Functional overview, value, key concepts, prerequisites, minimal quickstart, links to deeper guides | Architecture diagrams, internal subsystems, deep CLI/API reference |
| `quickstart-*.md` | "How do I use it to do X?" | Functional walkthroughs of real user goals, with copy-paste steps and validation | Technical internals, design rationale, exhaustive option reference |
| `technical-overview.md` | "How does it work under the hood?" | Architecture, components, data flow, extension points, design decisions | Marketing language, step-by-step tutorials |

## Workflow

1. Establish onboarding intent.
   - Confirm project name, one-sentence value, target reader, top 3 user goals.
   - Ask scope: README only, README + quickstarts, or full set with technical overview.
   - Confirm output locations. Default: `README.md` at repo root, `docs/quickstart-*.md`, `docs/technical-overview.md`.

2. Discover project from sources.
   - Inspect existing README, docs, manifests, build files, CLI entry points, service defs, routes, schemas, tests.
   - Map capabilities to source evidence. No ungrounded claims.
   - Find minimal quickstart path — smallest route to first success.

3. Design reader journey.
   - Lead functionally: README opens on what project does, not how built.
   - Progressive disclosure: functional overview → key concepts → minimal quickstart → deeper quickstarts → optional technical overview.
   - Flag which docs warrant TL;DR blocks, "already familiar?" shortcuts, or "going further" — skip on short guides.
   - Order quickstarts by highest-value goal first; later guides build on earlier.
   - Reserve technical depth for technical overview; link from README.

4. Write README.
   - Load `references/readme-strategy.md`.
   - Section order: functional overview, quick links, TOC, deeper functional overview, prerequisites, quick start, contributing, license, additional resources.
   - Limit technical detail to what user needs to start.
   - Preserve existing content; rewrite only stale or technical-leaning sections.

5. Write the functional quickstart guides.
   - Load `references/quickstart-strategy.md`.
   - Frame each guide around user goal, not feature list ("Send your first message", not "Messaging API reference").
   - First guide = quick first success; later guides build on it. Add shortcuts or advanced sections when guide warrants.
   - Minimal technical asides; link to technical overview for internals.

6. Write technical overview.
   - Load `references/technical-overview-strategy.md`.
   - Cover: architecture, primary components, data flow, integration/extension points, key design decisions, where to look in code.
   - Link from README "Additional resources" and quickstart "Next steps" — not from README main flow.

7. Verify everything.
   - Load `references/verification-checklists.md`.
   - Verify commands, endpoints, config keys, examples, expected output, cross-links against codebase.
   - Run commands when feasible; call out anything not executable.

8. Deliver completion report.
   - List files created or updated.
   - Describe reader journey: README → quickstarts → technical overview.
   - Summarize verification and gaps.

## Input Handling

Gather from user or infer from repo:

- Project name and one-sentence functional value
- Top user goals
- Target reader and assumed familiarity
- Prerequisites and minimal run path
- Functional areas needing own quickstart
- Whether technical overview in scope
- Style, voice, or existing docs to preserve

If user supplies prompt files or templates, treat as requirement sources but still verify factual content against codebase.

## Constraints

### Must Do

- MUST lead README with functional value before technical detail.
- MUST include only minimal quickstart in README and link to deeper quickstart guides for everything else.
- MUST frame quickstart guides around user goals, not feature inventories.
- MUST keep architecture, internals, and design rationale in `technical-overview.md`, not README.
- MUST verify commands, endpoints, fields, and config against source before presenting.
- MUST include expected output and validation step for each runnable quickstart action.
- MUST use relative links between README, quickstart guides, and technical overview.
- MUST preserve useful existing README content unless it conflicts with verified project behavior.
- MUST report any examples or flows that could not be verified.

Add power-user shortcuts and "going further" sections when guide is long or advanced enough to benefit. Skip where they add ceremony.

### Must Not Do

- MUST NOT open README with install steps, architecture diagrams, or technical jargon.
- MUST NOT duplicate quickstart workflows inside README beyond minimal install + run path.
- MUST NOT force experienced readers through introductory material to reach advanced content; provide shortcuts.
- MUST NOT mix technical internals into functional quickstart guides; link to technical overview instead.
- MUST NOT invent endpoints, commands, config keys, response shapes, or capabilities.
- MUST NOT leave examples requiring vague manual substitutions for happy path.
- MUST NOT assume auth, tokens, roles, ports, databases, or services without source evidence.
- MUST NOT create single oversized quickstart when separate user goals each deserve own guide.
- MUST NOT hard-code output folder when repo has no docs convention and user hasn't chosen one.

## Deliverable Checklist

Complete doc package includes:

1. `README.md` — functional-first: quick links, TOC, functional overview, key concepts, prerequisites, minimal quick start, contributing, license, additional resources.
2. `docs/quickstart-<goal>.md` — one per major user goal; prerequisites, numbered workflow, expected output, validation, troubleshooting, next steps.
3. `docs/technical-overview.md` — architecture, components, data flow, extension points, design decisions, code pointers.
4. Cross-links: README → quick start → functional quickstarts → technical overview.
5. Verification summary: source checks, executed commands, link checks, unverified items.

## Quality Bar

New reader:

- Understands from first screen what project does for them.
- Decides quickly whether to try.
- Reaches first success via README minimal quick start.
- Picks right quickstart for their goal.
- Can follow doc set from curious to proficient.

Power user:

- Reaches runnable command in seconds via TL;DR or "already familiar?" shortcut.
- Jumps to advanced sections or technical overview without re-reading basics.
- Finds code pointers in technical overview for source navigation.

## Knowledge Reference

README, functional overview, quickstart guide, technical overview, developer onboarding, proficiency ladder, power-user pathway, TL;DR shortcut, progressive disclosure, information architecture, user journey, source verification, API examples, CLI examples, expected output, validation, troubleshooting, relative markdown links, key concepts, architecture documentation
