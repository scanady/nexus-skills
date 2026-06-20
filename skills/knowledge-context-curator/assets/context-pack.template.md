---
type: context-pack
title: ""
task: ""
tags: []
required_pages: []
optional_pages: []
exclusions: []
freshness: "Review before reuse if older than 30 days."
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# Context Pack: Title

## Purpose

Define the recurring task this internal pack supports and the decision boundary it gives an agent.

## Load Order

1. Load required pages.
2. Check freshness notes.
3. Load optional pages only if the user request needs them.
4. Review exclusions before answering or acting.

## Required Context

- [[required-page-1]] - why this page is required.

## Optional Context

- [[optional-page-1]] - when to load this page.

## Exclusions

List pages, topics, tags, or stale assumptions that should not be used for this task.

## Freshness And Risk

State what must be checked before reuse, especially regulatory, product, pricing, policy, or workflow facts.

## Known Gaps

List missing sources, uncertain claims, validation needs, or follow-up research that would improve this pack.

## Maintenance Notes

Record when this pack should be revised and what changes should trigger an agent review. Note user input needed only when boundaries, authority, exclusions, or risk cannot be inferred.