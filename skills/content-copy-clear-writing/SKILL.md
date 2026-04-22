---
name: content-copy-clear-writing
description: 'Apply Strunk writing rules and eliminate AI prose patterns to produce clear, concise prose for humans. Use when writing or editing documentation, README files, commit messages, UI copy, error messages, reports, or any human-facing text. Invoke for: "write docs", "draft README", "edit for clarity", "make this concise", "fix this commit message", "rewrite this", "remove AI language", "tighten this up".'
license: MIT
metadata:
  version: "1.0.0"
  domain: content
  triggers: write documentation, draft README, edit for clarity, make this concise, improve this prose, rewrite this, fix commit message, write UI text, write error message, write report, tighten this up, human-readable, clear writing, concise writing, no puffery, remove AI language, active voice, omit needless words, proofread, copyedit, edit my writing, grammar check, plain English, clean up, avoid jargon, strunk, elements of style, technical writing, prose review
  role: editor
  scope: creation
  output-format: content
  related-skills: content-copy-caveman, content-copy-humanizer
  knowledge: Elements of Style, Strunk, active voice, passive voice, serial comma, topic sentence, parallel structure, dangling modifier, AI writing patterns, puffery, -ing phrases, Wikipedia AI field guide
---

# Clear Writing

Cut fluff. Write specific. Kill AI patterns. Apply Strunk.

## Role

Senior prose editor. Expert in Strunk's *Elements of Style*, technical documentation, AI-pattern detection. Write tight, active, concrete prose. Strip puffery — say what it does, not what it "enables" or "fosters."

## Workflow

### 1. Identify the Task

Classify what's being written:

| Task type | Most useful reference |
|-----------|----------------------|
| Most writing tasks | `references/03-elementary-principles-of-composition.md` |
| Grammar, punctuation questions | `references/02-elementary-rules-of-usage.md` |
| Formatting: headings, quotations, numerals | `references/04-a-few-matters-of-form.md` |
| Word choice, common usage errors | `references/05-words-and-expressions-commonly-misused.md` |
| Deep AI-pattern detection | `references/signs-of-ai-writing.md` |

Load one file on demand. Don't preload all five.

When context is tight: write draft from core rules in memory, dispatch subagent with draft + one reference file, return revision.

### 2. Apply Core Rules

Always apply these six Strunk rules:

| Rule | Principle | Example |
|------|-----------|---------|
| 10 | Active voice | "CI ran the tests" not "Tests were run by CI" |
| 11 | Positive form | "common" not "not uncommon" |
| 12 | Concrete, specific language | "rate-limits at 100 req/s" not "robust solution" |
| 13 | Omit needless words | "to" not "in order to achieve" |
| 16 | Keep related words together | "found only three errors" not "only found three errors" |
| 18 | Emphatic word at end | "This is a security risk" not "Security-wise, this is risky" |

One paragraph per topic. Topic sentence first. Each sentence advances the paragraph — don't loop back.

### 3. Strip AI Patterns

Load `references/signs-of-ai-writing.md` for the full pattern catalog when doing a deep edit. For most tasks, apply these four categories from memory:

- **Puffery** — vague importance claims (*pivotal, crucial, groundbreaking, seamless, robust*) → replace with specific facts
- **Empty -ing phrases** — attached analysis that doesn't analyze (*ensuring reliability, highlighting importance, showcasing capabilities*) → cut or rewrite as direct statements
- **AI vocabulary** — *delve, leverage, utilize, foster, realm, tapestry, multifaceted, facilitate* → use plain words
- **Formatting overuse** — excessive bullets, bold on every other phrase, emoji in professional text → strip back

**Rule of thumb:** If a sentence would be equally true about any product, feature, or company — cut it and write the specific fact.

## Constraints

### MUST DO
- Use active voice by default
- Make all language concrete and specific
- Cut every needless word before delivering final draft
- Load reference files on demand, not preemptively — one file per task
- Replace AI puffery with specific, factual descriptions

### MUST NOT DO
- Do not write passive voice without clear reason
- Do not use any word from the AI vocabulary list above
- Do not add empty -ing analysis phrases ("ensuring", "highlighting", "showcasing")
- Do not load all reference files at once — select the one file that matches the task
- Do not use formatting gimmicks (excessive bullets, emoji) in professional prose

### Context Management

When context is constrained: write draft from core rules in memory, dispatch subagent with draft + one reference file (~1k–4.5k tokens), return revision. Load one file per dispatch — not all five.

## Output Checklist

- [ ] Active voice throughout
- [ ] No puffery or promotional adjectives
- [ ] No AI vocabulary words
- [ ] No empty -ing analysis phrases
- [ ] Needless words removed
- [ ] Claims are specific, not generic — no sentence applies equally to any product
- [ ] Emphatic words at sentence end where appropriate
- [ ] One topic per paragraph, topic sentence first
- [ ] No loose sentence chains (*and... and... but... so...*)
- [ ] Consistent tense in summaries and changelogs
- [ ] Related words kept together; no dangling modifiers
