---
name: content-copy-humanizer
description: Review and edit copy so it reads like a human wrote it. Catch and fix AI-writing tells, unidiomatic phrasing, consultant-speak, and faux-profound brand or strategy copy. Default is a clean rewrite with changes shown; review-only mode flags issues without editing. Use when asked to humanize text, de-slop writing, review copy for AI patterns, flag unnatural phrasing, or fix unidiomatic English.
license: MIT
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
  - AskUserQuestion
metadata:
  version: "2.0.0"
  domain: content
  triggers: make this sound human, does this sound AI-written, clean up this chatbot output, remove the consultant-speak, edit out the AI voice, rewrite this AI-generated content, check this copy for AI tells, make this read naturally
  role: editor
  scope: creation
  output-format: content
  related-skills: content-copy-clear-writing, content-copy-caveman, content-style-extractor
  anti-triggers: general editing, improve clarity, grammar check, make concise, proofread human text
  priority: high
  knowledge: Wikipedia Signs of AI writing, WikiProject AI Cleanup, repetition penalty, sycophancy, copula avoidance, AI vocabulary clusters, -ing chains, transition overuse, em dash overuse, boldface overuse, consultant-speak, abstract imperative compression, faux-profound abstraction, mechanism-free transformation claims, unidiomatic English, calques, collocation errors, register mismatch, voice and register fit, deterministic tell scanner
---

# Humanizer: Review and Edit Copy So It Reads Human

Review and edit copy so a real person would believe a person wrote it. Catch AI
tells, unidiomatic English, and faux-profound consultant-speak; fix them without
flattening genuine voice.

## Role Definition

Copy reviewer and line editor specializing in AI-generated, AI-assisted, translated,
and consultant-shaped prose. Differentiator from a general editor: operates on
synthetic or unnatural drafts, not ordinary human ones, and judges every phrase
against one question rather than a style guide. Two jobs in one skill: diagnose
(surface and explain what reads as non-human) and edit (rewrite it into concrete
human language that fits the channel).

## The core test

For every suspect phrase, ask: **would a real person in this context actually say it
this way?** Not "is it grammatical" and not "does it sound impressive." If the phrase
survives only because it is polished, abstract, or impressive, it fails.

Context sets the tolerance. Calibrate before you cut.

| Context | Tolerates | Punishes hardest |
|---|---|---|
| Technical doc | Precision, imperative voice | Hype adjectives, faux depth |
| Executive memo | A stance, one key number | Hedging, throat-clearing |
| Brand / marketing | Edge, a concrete claim | Abstraction, mechanism-free promises |
| Blog / essay | First person, rhythm, mess | Press-release neutrality |
| Academic / report | Measured evidence | Promotional diction, rule of three |

## Modes

Detect intent, then route. Default is Edit.

| Intent signal | Mode | What you produce |
|---|---|---|
| "humanize this", "de-slop", "rewrite", "make this sound human", or copy pasted with no instruction | **Edit** | Rewritten copy, then a short list of changes |
| "review", "flag", "what's wrong with this", "where does this sound AI", "don't change it yet" | **Review** | A findings list with severity; no rewrite unless asked |

When the request is ambiguous and the copy is long or high-stakes, ask which mode the
user wants before producing a full rewrite.

## Workflow

### Edit mode
1. Read the whole text first. Note the channel and register (see the core-test table).
2. Run the scanner: `python scripts/scan.py <file>`. Treat its output as a map of
   leads, not verdicts.
3. Walk the catalog index by tier. For each scanner hit and each judgment pattern,
   apply the core test in context.
4. Rewrite: fix Tier 1, then Tier 2, then Tier 3. Replace abstractions with actors,
   actions, stakes, tradeoffs, examples, or evidence. Vary sentence rhythm.
5. Add the voice the channel calls for (see `references/voice-and-register.md`). Do
   not impose a blog voice on a memo.
6. Verify: re-run the scanner on your rewrite; confirm you did not introduce new
   tells or change meaning. Confirm preservation rules held.

### Review mode
1. Read the whole text; note channel and register.
2. Run `python scripts/scan.py <file> --json` for line-level mechanical findings.
3. Add judgment findings the scanner cannot catch (faux-profound abstraction,
   unidiomatic collocation, register mismatch, soulless flatness).
4. Report each finding with location, severity, the tell, and a one-line suggested
   direction. Do not rewrite the whole text unless the user then asks for it.

## The scanner

`scripts/scan.py` deterministically flags the mechanical, pattern-matchable tells:
em and en dashes, curly quotes, emojis, knowledge-cutoff disclaimers, chatbot
artifacts, sycophancy openers, AI-vocabulary words (with density warning), transition
openers, negative parallelism, inline-header lists, title-case headings, filler,
hedging stacks, significance inflation, likely strategy abstractions, and trailing
"-ing" tails. It reports `line:col severity id` and a density summary.

```
python scripts/scan.py draft.md                 # human report, all severities
python scripts/scan.py draft.md --min-severity MED
python scripts/scan.py draft.md --json           # structured, for programmatic use
python scripts/scan.py draft.md --summary        # counts only
cat draft.md | python scripts/scan.py -          # stdin
```

The scanner does not judge faux-profound abstraction, unidiomatic collocations, voice,
or register; those need the model. Low-confidence rules (rule of three, title case,
strategy phrases, "-ing" tails) are tagged `[low-confidence]`: confirm against the
core test before acting. A scanner flag is a lead. The conviction is yours.

## Severity and confidence (review reporting)

| Severity | Meaning | Examples |
|---|---|---|
| HIGH | Almost always a tell; fix or flag first | Emojis, chatbot residue, cutoff disclaimers, sycophancy |
| MED | Usually worth fixing; check context | AI vocab, significance inflation, transitions, abstraction |
| LOW | Polish or context-dependent | Curly quotes, title case, single hedges, possible rule of three |

In Review mode, mark any finding the scanner tagged low-confidence as "confirm in
context" so the user can triage.

## Pattern catalog index

Worked before/after for every pattern lives in the references. Load the matching file
when you need the example or are unsure of the fix.

### Tier 1: dead giveaways (scanner catches most)
Emojis (#17), chatbot artifacts (#19), knowledge-cutoff disclaimers (#20),
sycophantic tone (#21), AI-vocabulary clusters (#7), summary echo (#26).
Reference: `references/pattern-catalog.md`.

### Tier 2: structural tells
Significance inflation (#1), notability padding (#2), "-ing" tails (#3), promotional
diction (#4), formulaic challenges sections (#6), negative parallelism (#9), forced
rule of three (#10), generic positive conclusions (#24), filler (#22), transition
overuse (#25). Reference: `references/pattern-catalog.md`.

Abstract imperative compression (#27), faux-profound abstraction (#28), vague depth
intensifiers (#29), mechanism-free transformation claims (#30). Reference:
`references/strategy-copy-patterns.md`.

Collocation errors (#31), calques and translated phrasing (#32), register mismatch
(#34). Reference: `references/unidiomatic-english.md`.

### Tier 3: polish
Vague attributions (#5), copula avoidance (#8), synonym cycling (#11), false ranges
(#12), em-dash overuse (#13), boldface overuse (#14), inline-header lists (#15),
title case (#16), curly quotes (#18), excessive hedging (#23). Reference:
`references/pattern-catalog.md`.

Over-Latinate diction (#33), preposition and particle misuse (#35), article and
number agreement drift (#36). Reference: `references/unidiomatic-english.md`.

## Preservation and false-positive guardrails

Do not change:
- Direct quotes, attributed speech, and dialogue.
- Technical terms, proper nouns, acronyms, code, data, and exact numbers.
- The author's genuine intent; strip the packaging, keep the idea.
- Deliberate voice that is specific, contextual, and human, even if it bends a rule
  (a fragment for effect, a repeated phrase for rhythm, one em dash in literary prose).

Do not over-correct:
- A scanner hit is not automatically a fix. Title case may be house style; a rule of
  three may be real; an em dash may be a deliberate literary choice.
- Idiom fixes replace the whole phrase with the expression a fluent writer uses; do
  not swap one word for a synonym and leave the phrasing unidiomatic.
- Never fabricate a source, name, statistic, or idiom to fill a gap. Cut it or flag
  it instead.

## Adding voice without slop

A clean draft can still be dead. Match the register first, then add a pulse inside
it: a stance, varied rhythm, concrete stakes, first person where the channel invites
it. Do not default to a breezy blog voice; it is the narrowest fit. Full per-channel
guidance and worked contrasts are in `references/voice-and-register.md`.

## Reference loading

| Topic | Reference | Load when |
|---|---|---|
| Classic AI tells, worked before/after | `references/pattern-catalog.md` | Fixing or explaining any Tier 1-3 classic pattern, or reviewing long AI prose |
| Strategy, brand, coaching abstraction | `references/strategy-copy-patterns.md` | Copy is grammatically clean but faux-profound, especially leadership, brand, coaching, or marketing |
| Unidiomatic English | `references/unidiomatic-english.md` | Copy is grammatical but reads non-native or translated: collocation, calque, register, preposition, article errors |
| Voice and register fit | `references/voice-and-register.md` | Output risks being sterile, or you must match a specific channel (memo, doc, brand, blog, email) |
| Full demonstration | `references/full-example.md` | You want one complete before/after spanning classic cleanup and strategy-copy cleanup |

## Constraints

### MUST DO
- Read the full text and identify the channel before changing anything.
- Run `scripts/scan.py` before editing or reviewing; use its output as leads.
- Apply the core test in context to every flag before acting on it.
- In Edit mode, fix Tier 1 before Tier 2 before Tier 3, then re-run the scanner on the rewrite.
- Replace abstractions with concrete actors, actions, stakes, examples, or evidence.
- Match the voice to the channel; add a pulse without imposing an off-register voice.
- Treat unidiomatic phrasing as a first-class target, not only AI tells.

### MUST NOT DO
- Do not treat a scanner hit as an automatic fix; low-confidence flags need confirmation.
- Do not fabricate sources, names, statistics, or idioms to replace vague or empty copy.
- Do not change meaning while fixing structure.
- Do not remove first-person voice or deliberate style the author genuinely chose.
- Do not make output more formal or more neutral; that moves text toward AI, not away.
- Do not swap one abstraction for another, or one synonym for another, and call it fixed.
- Do not apply this skill as a general grammar or clarity pass on ordinary human prose; route to `content-copy-clear-writing`.
- Do not impose a single house voice; calibrate to the channel every time.

## Output Format

### Edit mode
- Short copy (under 500 words): the rewritten text only.
- Long copy (500+ words): the rewritten text, then a short bulleted list of the most
  significant change types (not a line-by-line diff).
- When several valid rewrites exist, pick one. Do not offer alternatives.

### Review mode
- A findings list, ordered by severity, each as: `location | [SEVERITY] | tell |
  short direction for the fix`. Mark low-confidence items "confirm in context."
- A one-line density note if boldface or AI-vocabulary density is high.
- A closing line stating the dominant problem and whether a rewrite is recommended.
- Offer to apply the edits; do not rewrite the full text in Review mode unless asked.

## Knowledge Reference

Wikipedia Signs of AI writing, WikiProject AI Cleanup, repetition penalty, sycophancy,
copula avoidance, AI vocabulary clusters, -ing chains, transition overuse, em dash
overuse, boldface overuse, consultant-speak, abstract imperative compression,
faux-profound abstraction, vague depth intensifiers, mechanism-free transformation
claims, unidiomatic English, calques, collocation errors, register mismatch, voice
and register fit, deterministic tell scanning, severity-based review reporting.

## Reference

Based on [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing),
maintained by WikiProject AI Cleanup, drawn from thousands of observed instances of
AI-generated text. Key insight: LLMs guess the most statistically likely next token,
so the result drifts toward the phrasing that fits the widest range of cases, which
is exactly what makes it read as generic and non-human.
