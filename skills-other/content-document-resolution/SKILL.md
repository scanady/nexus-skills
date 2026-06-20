---
name: content-document-resolution
description: 'Document Resolution skill. Use when adjusting the level of detail in a document — reducing verbosity, compressing supporting material, or expanding a summary back toward full detail — while preserving the original document''s intent, key claims, decisions, and audience alignment. Also supports document cropping (focusing on a specific topic region and discarding the rest) and named document filters (transforming how content is presented — e.g., executive, risks, action-items, timeline, neutral, bullets, narrative, technical, business, pro-con, evidence-only, decisions-only, staffing, Q&A). Applies the photography metaphor: resolution sets the detail level, crop sets the frame, filters set the rendering style. Executes at minimum 10 iterative processing loops per resolution adjustment. All crop and filter operations are acknowledged and documented in the output audit trail. Triggers: document resolution, reduce document, compress document, summarize document, expand document, document detail level, document condensing, document abstraction, document simplification, document length reduction, resolution level, zoom level, document zoom, document distance, abstract document, document clarity level, crop document, filter document, document filter, executive filter, risk filter, action items filter, timeline filter, neutral filter, pro con filter, evidence filter, decisions filter, bullets filter, narrative filter, technical filter, business filter, staffing filter, Q&A filter.'
argument-hint: 'Provide the document text (or a file reference), the target resolution (1–10), and optionally: a crop region (topic, section name, or question) and one or more named filters. Examples: "Reduce to resolution 4." | "Crop to timing content, resolution 3." | "Apply executive filter, resolution 5." | "Crop to risk section, apply action-items filter, resolution 2."'
---

# Document Resolution

## Role Purpose

The Document Resolution skill adjusts the level of detail in any document — reducing it toward an abstracted essence or expanding a compressed version back toward full richness — while guaranteeing that the **intent, key claims, decisions, and audience alignment** of the original remain intact after processing.

The controlling metaphor is **photography** — resolution, crop, and filter are three independent controls that can be used together or separately:

- **Resolution** sets the distance from the subject — how much detail the reader receives.
- **Crop** sets the frame — which region of the document stays in the picture.
- **Filters** set the rendering style — how surviving content is presented without changing what it says.

Resolution, crop, and filter are composable. A document can be cropped, filtered, and then compressed — or any subset of those three operations — making the output precisely tailored to the audience and purpose.

---

### Resolution — Viewing Distance Control

The controlling metaphor for resolution is **photographic viewing distance**:

| Resolution | Photo Analogy | Document Analogy |
|---|---|---|
| **10** | Macro / 2 inches away | Every sentence, example, data point, qualifier, caveat, and nuance present |
| **8–9** | Portrait / 2 feet away | Nearly complete — obvious filler cut, minor redundancies removed |
| **6–7** | Standard / 6 feet away | Main structure intact, examples reduced, background context trimmed |
| **4–5** | Landscape / 20 feet away | Key points + most important evidence, examples removed or reduced to one per concept |
| **2–3** | Aerial / 100 feet away | Major topics + takeaway per topic, minimal supporting detail |
| **1** | Satellite / 1,000 feet away | Single coherent essence capturing only the essential intent and primary conclusions |

A resolution adjustment does **not** change what the document says — it changes **how much of the way it says it** the reader receives. A resolution-3 version of a technical spec should still allow a reader to understand what is being built and why, even if they couldn't build it from the document alone.

---

## Phase 0: Pre-Processing Setup

### 0.1 Inputs Required

Before beginning, collect:

1. **Source document**: The full text to be adjusted.
2. **Target resolution**: A number from **1** to **10** (whole or half-step, e.g. 3, 5.5, 7).
3. **Source resolution** (optional): If the user is providing a document that is already compressed, ask them to state the current resolution level — or the skill will estimate it.
4. **Crop** (optional): A description of the region to retain — section name, topic keyword(s), or a question the output should answer. Everything outside the crop boundary is discarded before processing begins.
5. **Filters** (optional): One or more named filters from the Filter Catalog (Section 0.5). Filters are applied after crop and before resolution processing.

If target resolution equals 10 and no crop or filter is specified, return the original document unchanged with a note that no processing is required.

### 0.2 Resolution Direction

Determine operation direction:

- **Source > Target**: **Reduction run** — remove layers of detail
- **Source < Target**: **Expansion run** — request source material or expand from what is present
- **Source = Target**: Report that target is already met; offer to fine-tune. If a crop or filter is specified, apply those before reporting.

> **Expansion note**: Expansion from compressed text without the original source is inherently incomplete — the skill cannot invent facts that were never in the original. When performing an expansion, the skill will identify every slot where more detail *could* exist and flag it with `[EXPANSION SLOT: brief description of what would appear here at full resolution]` so the author can fill it in from source material.

### 0.3 Crop Processing

Crop is applied **first** — before filters, before Intent Capture, and before any resolution loop. It establishes the working document that all subsequent operations act on.

**Crop operation protocol:**

1. **Identify the crop boundary**: Locate all content that falls within the user's stated crop region. Accepted crop boundary types:
   - *Section name*: Retain all content under named section(s), discard everything else.
   - *Topic keywords*: Retain all paragraphs, tables, bullets, and data points that bear on the stated topic(s); discard all content with no bearing on those topics.
   - *Question framing*: Retain all content that contributes to answering the stated question(s); discard all content that does not.
   - *Explicit range*: Retain content between stated markers (e.g., "starting at the risks table through the end of Section 4").

2. **Produce the Crop Audit** — a table logged immediately after crop is applied:

```
## Crop Audit

**Crop Boundary**: <description of what was retained>
**Crop Type**: Section / Topic / Question / Range

| Retained | Discarded |
|---|---|
| <section or topic name> | <section or topic name> |
```

3. **Restate the working document scope**: After crop, update the working document header to note it is a cropped region, not the full source.

4. **Crop does not change the resolution** of the retained content — it only changes the frame. The retained content carries its original resolution until the processing loops act on it.

5. **Crop boundary is immutable** once set. Cropped content is never restored during resolution processing or stability passes.

### 0.3.5 Pre-Filter Snapshot

> **Why this step exists:** Filters — especially stripping filters like `evidence-only`, `action-items`, `risks`, and `decisions-only` — deliberately remove whole categories of content. If intent is captured *after* a stripping filter runs, the Intent Scoreboard never knew the removed content existed. This means the resolution loops can silently lose content that the filter already stripped, and validation cannot distinguish "lost by filter" from "lost by compression." The Pre-Filter Snapshot creates a transparent, auditable record of what existed before filters ran, so the full transformation chain is visible from source → crop → filter → compression.

Before any filter is applied, capture a **Pre-Filter Snapshot** of the working document (post-crop, if crop was applied; original source otherwise). This snapshot is read-only and never modified.

**Pre-Filter Snapshot protocol:**

1. **Record the pre-filter word count** of the working document.

2. **Extract the Pre-Filter Key Claims** — the substantive claims, conclusions, decisions, and critical data points present in the working document before any filter transforms them:

```
## Pre-Filter Snapshot

**Taken at**: Post-crop / Post-source (circle one)
**Pre-filter word count**: <count>
**Estimated pre-filter resolution**: <1–10>

**Pre-Filter Key Claims** (all substantive assertions present before filtering):
1. <claim>
2. <claim>
[continue — capture all]

**Pre-Filter Decisions / Actions**:
- [DECISION] <statement>
- [ACTION] <statement>
- [NONE] if none present

**Pre-Filter Critical Data Points**:
- <number, date, named entity, or evidence anchor>
[continue]
```

3. **Classify each pre-filter item by filter fate** — after all filters complete, return to this snapshot and mark each item with one of:
   - `SURVIVED` — item is still present in the post-filter working document
   - `TRANSFORMED` — item is present but restructured, reworded, or reformatted by a filter
   - `STRIPPED BY FILTER: <filter name>` — item was deliberately removed by a named filter

4. **The Pre-Filter Snapshot is linked in the Filter Audit** (Section 0.4) as the authoritative record of intentional filter removals — distinguishing them from accidental losses that occur during resolution compression.

5. **The Intent Scoreboard** (Phase 1) is still built on the post-filter working document (the deliberate design choice that scopes the loop-validation promise to what the filter left intact). The Pre-Filter Snapshot does *not* change what the scoreboard guards — it provides the audit trail that explains *why* the scoreboard scope is narrower than the original source.

> **In plain terms:** The Intent Scoreboard says "validate that the resolution loops didn't lose this." The Pre-Filter Snapshot says "here is what the filters were explicitly allowed to remove before the loops started." Together they give complete traceability — you can always answer the question "where did this content go?" at every stage of the pipeline.

### 0.4 Filter Application

Filters are applied **after crop and before resolution processing**. Each filter transforms how the retained content is presented without adding facts the document does not contain.

**Filter application protocol:**

1. Identify all named filters from the user's request.
2. Before applying the first filter, execute the **Pre-Filter Snapshot** (Section 0.3.5) to record what exists in the working document at this point.
3. Apply filters in the order listed — if multiple filters are specified, each operates on the output of the previous.
4. Produce a **Filter Audit** entry for each filter applied. The Filter Audit has two parts:

   **Part A — Filter Effect Summary** (one row per filter):

```
## Filter Audit — Part A: Effect Summary

| Filter | Purpose | Structural Effect | Content Stripped (intentional) |
|---|---|---|---|
| <filter name> | <one-line purpose> | restructured / reformatted / reframed / none | <categories deliberately removed, e.g., "All prose background", "All non-risk content", or "None — reformatting only"> |
```

   **Part B — Pre-Filter Snapshot Resolution** (completed after all filters run):

   Return to the Pre-Filter Snapshot and classify each item:

```
## Filter Audit — Part B: Pre-Filter Snapshot Resolution

| Pre-Filter Item | Type | Fate | Filter Responsible |
|---|---|---|---|
| <first 10 words of claim or data point> | Key Claim / Decision / Data Point | SURVIVED / TRANSFORMED / STRIPPED | <filter name or "N/A"> |
```

   > **Reading this table:** STRIPPED items were *intentionally removed by a named filter* as part of the user's request. They are not losses — they are deliberate editorial choices. TRANSFORMED items still exist but in a different form. SURVIVED items are unchanged. Only SURVIVED and TRANSFORMED items enter the Intent Scoreboard.

5. After all filters are applied, update the word count and estimated resolution before entering the resolution processing loops.

See **Section 0.5 — Filter Catalog** for the full list of named filters and their transformation rules.

### 0.5 Filter Catalog

The following named filters are available. Filters can be combined; apply them in the order listed by the user.

---

#### FILTER: executive
**Purpose:** Restructure content for executive consumption — conclusion first, supporting evidence second, technical detail minimized.

Transformation rules:
- Apply **Pyramid Principle**: move the key conclusion or recommendation to the first sentence of each section. If the document builds to a conclusion at the end, invert it.
- Strip technical implementation detail that does not change a decision (note removal in Filter Audit).
- Convert passive voice to active, attribution-named voice: "a decision was made" → "the program team decided".
- Replace unexpanded jargon acronyms with plain-language equivalents on first use.
- Reduce evidence blocks to a single most-compelling data point per claim.
- Output tone: direct, declarative, no hedging.

---

#### FILTER: action-items
**Purpose:** Surface only decisions required and calls to action. Strip all non-actionable content.

Transformation rules:
- Scan the full working document for: decisions embedded in prose, CTAs, named owners, deadlines, and dependencies that gate action.
- Reformat every item as:
  ```
  🎯 ACTION / ✅ DECISION: [What must be done or decided]
  Owner: [Named role or "⚠️ UNASSIGNED"]
  By: [Date / quarter or "⚠️ NO DEADLINE"]
  Depends on: [Prior action or "None"]
  ```
- Remove all prose, background, evidence, and analysis that does not directly support an action item.
- Flag any action item with a missing owner or deadline with ⚠️.

---

#### FILTER: risks
**Purpose:** Surface only risk content. Strip all non-risk material.

Transformation rules:
- Retain: risk statements, probability/impact language, mitigation options, trigger conditions, named risk owners.
- Reformat surviving content into a risk register structure:
  ```
  | Risk | Impact | Likelihood | Mitigation | Owner |
  ```
  Mark missing fields as `⚠️ NOT SPECIFIED`.
- Remove: background, scope, timelines, staffing, and any content with no risk bearing.
- Preserve all risk-related data points (numbers, dates, thresholds) intact at any resolution.

---

#### FILTER: timeline
**Purpose:** Surface only timing, scheduling, sequencing, and deadline content.

Transformation rules:
- Retain: activity timelines, quarter/date references, durations, dependencies that affect timing, milestones, and any statements about when something will or must happen.
- Reformat into chronological order if source is not already ordered by time.
- Remove: rationale for timing choices, resource discussion, background context, and content with no temporal dimension.
- Preserve all date, quarter, and duration data points exactly as stated in the source.

---

#### FILTER: neutral
**Purpose:** Strip loaded language, advocacy framing, and bias markers. Does not remove content — rewrites how it is expressed.

Transformation rules:
- Apply bias detection rules: flag and rewrite confirmation bias, loaded language, anchoring, false urgency, unsupported attribution, and in-group framing.
- Replace charged adjectives with measurable alternatives: "critical failure" → "failure with [specific impact]".
- Remove "obviously", "clearly", "any reasonable person" — reframe as evidence-based claims.
- Remove first-person advocacy ("we believe", "we recommend") unless it is a formal documented recommendation — reframe as "the proposal is..." or "the evidence supports...".
- Neutral is not passive — factual directness is preserved.

---

#### FILTER: pro-con
**Purpose:** Restructure all proposals, recommendations, and options as explicit pros/cons with a stated trade-off.

Transformation rules:
- Identify every proposal, recommendation, or option in the working document.
- For each, produce:
  ```
  ⚖️ [Topic / Option]
  Pros:
  - <bullet>
  Cons:
  - <bullet>
  Open risk: <any unaddressed downside not captured above>
  Recommendation (if stated in source): <verbatim or "Not stated">
  ```
- Do not invent pros or cons — only surface what is evidenced in the source document.
- Remove all prose framing around options that is not a pro, con, or stated recommendation.

---

#### FILTER: evidence-only
**Purpose:** Strip claims and conclusions. Retain only supporting data, citations, examples, and named evidence.

Transformation rules:
- Remove: recommendations, conclusions, interpretations, opinions, and generalizations.
- Retain: numbers, dates, named entities, research citations, quoted statements, case studies, and specific examples.
- Where a claim and its evidence appear together, remove the claim; keep the evidence verbatim.
- Output is intentionally conclusion-free — the reader draws their own interpretation from the data.

---

#### FILTER: decisions-only
**Purpose:** Surface only content that frames a decision the reader must make. Strip everything else.

Transformation rules:
- Retain: explicitly framed choices, options stated with trade-offs, decision gates, approval requirements, and binary yes/no questions embedded in the document.
- Reformat as:
  ```
  ✅ DECISION: [Decision statement]
  Options: [A] | [B] | [C if present]
  Recommended (if stated): [Recommendation]
  Decision Owner: [Role or "⚠️ NOT ASSIGNED"]
  ```
- Remove all background, analysis, timeline, and resource content that does not directly frame a choice.

---

#### FILTER: bullets
**Purpose:** Convert prose into structured, hierarchical bullet lists. Preserve information density.

Transformation rules:
- Convert every prose paragraph into a parent bullet (the main assertion) with child bullets (the supporting points).
- Tables are preserved as-is or converted to nested bullets if they gain clarity from that format.
- Numbered lists become ordered bullets when sequence matters; unordered when sequence does not.
- Connective language ("furthermore", "in addition", "as a result") is removed — the hierarchy communicates the relationship.
- Sentences over 20 words are split: the head clause becomes the bullet; the subordinate clause becomes a child bullet.

---

#### FILTER: narrative
**Purpose:** Convert structured bullets, tables, and lists into flowing prose. Apply where content will be read aloud or sent as written communication.

Transformation rules:
- Convert bullet hierarchy to paragraph form: parent bullets become topic sentences; child bullets become supporting sentences in the same paragraph.
- Convert tables to prose: each row becomes a sentence or phrase; related rows group into a paragraph.
- Add minimal transitional connectives to maintain flow: "In addition,", "By contrast,", "As a result,".
- Do not add interpretive language — the prose carries the structure, not additional assertions.
- Retain all numbers, names, dates, and data points from the source structure exactly.

---

#### FILTER: technical
**Purpose:** Strip business framing, executive context, and outcome language. Preserve technical precision, specifications, constraints, and implementation detail.

Transformation rules:
- Remove: business case language, ROI statements, executive-audience context, organizational framing.
- Retain: system names, API references, data formats, integration patterns, technical constraints, configuration parameters, architecture decisions.
- Expand any business-language paraphrase of a technical concept back to its technical form where the source supports it.
- Output tone: precise, neutral, specification-grade.

---

#### FILTER: business
**Purpose:** Strip technical implementation detail. Preserve business capabilities, outcomes, value statements, and strategic framing.

Transformation rules:
- Remove: system-internal names (unless subject of a business decision), API details, data schemas, engineering effort in story points.
- Retain: capability descriptions, business outcomes, value metrics, user-facing features, budget and cost figures, timeline commitments.
- Convert technical jargon to plain-language equivalents where a business equivalent exists.
- Output tone: capability-focused, audience-aligned for non-technical readers.

---

#### FILTER: staffing
**Purpose:** Surface only resource, team, role, and organizational content.

Transformation rules:
- Retain: role names, head count references, named individuals (if present), team assignments, skill requirements, capacity constraints, organizational structure changes, training needs.
- Reformat into a role-indexed structure:
  ```
  | Role | Count Needed | Currently Assigned | Gap |
  ```
  Mark missing fields as `⚠️ NOT SPECIFIED`.
- Remove: timeline, scope, architecture, and risk content with no staffing dimension.
- Flag any work item with no identified owner as `⚠️ UNOWNED WORK ITEM`.

---

#### FILTER: qa
**Purpose:** Restructure document content as explicit question-and-answer pairs.

Transformation rules:
- Identify the questions the document implicitly or explicitly answers. Sources for questions: section headers framed as topics (convert to questions), stated objectives, problem statements, embedded decisions.
- For each question, produce:
  ```
  **Q: [Question]**
  A: [Answer drawn directly from document content — no invention]
  Evidence: [The data point, claim, or section that supports the answer]
  Confidence: [HIGH — stated directly / MEDIUM — strongly implied / LOW — requires inference]
  ```
- Questions for which the document provides no answer are listed at the end:
  ```
  **Q: [Question]** — ⚠️ NOT ANSWERED IN SOURCE
  ```
- Remove all document structure that is not a question or its answer.

---

### 0.6 Processing Order

All pre-processing operations execute in this fixed sequence before any resolution loop begins:

```
1. CROP (if specified)              → establishes the working document frame
                                      content outside the frame is permanently discarded
2. PRE-FILTER SNAPSHOT (§0.3.5)    → captures all key claims / decisions / data points
                                      present BEFORE any filter runs
                                      this is the audit baseline for intentional filter removals
3. FILTERS (if specified)           → transform how content is presented
                                      stripping filters deliberately remove content categories
                                      Filter Audit Part B records what each filter removed
4. INTENT CAPTURE (Phase 1)         → scoreboard built on the post-crop, post-filter document
                                      guards only what the filters left intact
                                      does NOT guard content intentionally stripped by filters
                                      (those are documented in the Pre-Filter Snapshot instead)
5. RESOLUTION LOOPS (Phase 2)       → compression or expansion applied to the working document
                                      validated against the Intent Scoreboard each loop
6. VALIDATION (Phase 3)             → final check against the Intent Scoreboard
7. OUTPUT DELIVERY (Phase 4)        → includes Pre-Filter Snapshot, Filter Audit (Parts A+B),
                                      Crop Audit, Content Change Audit, and Resolution Summary
```

> **The separation of concerns:**
> - **Pre-Filter Snapshot** answers: *"What did the filter deliberately remove?"*  
> - **Intent Scoreboard** answers: *"What must survive the resolution compression?"*  
> - **Filter Audit Part B** answers: *"Can I trace every pre-filter item to its final fate?"*  
> - **Content Change Audit** answers: *"What did the resolution loops remove?"*
>
> Together, these four artifacts give complete provenance for every piece of content in the source document. A reader can always explain why any sentence is or is not in the output.

> **Important:** The Intent Scoreboard (Phase 1) is always built on the post-crop, post-filter working document — not the original source. The scoreboard reflects what is being preserved *within the defined frame and rendering*, not what was discarded by crop or intentionally removed by filter. The Pre-Filter Snapshot (§0.3.5) provides the complementary record for filter-stripped content.

---

## Phase 1: Intent Capture

**Intent Capture is performed exactly once**, after crop and all filters have been applied, before any processing loop begins. It produces the **Intent Scoreboard** — the canonical reference used to validate every loop's output.

> **Scope note:** The Intent Scoreboard is built on the *post-crop, post-filter* working document. It deliberately does not include content that was removed by crop (out of frame) or stripped by a filter (intentional editorial transformation). Those removals are fully documented in the Crop Audit and the Pre-Filter Snapshot (§0.3.5). The scoreboard's job is to make a precise, bounded promise: *"within what the user chose to keep, nothing will be accidentally lost during compression."*

### 1.1 Intent Scoreboard Construction

Analyze the source document and produce the following:

```
## Intent Scoreboard

**Document Title / Label**: <title or "[Untitled]">
**Stated Purpose**: <1–2 sentences: what this document is for and what a reader should take away>
**Primary Audience**: <role(s) or description of intended reader>
**Register / Tone**: <e.g., technical / executive / operational / persuasive / neutral informational>

**Key Claims** (the statements that would change the document's meaning if removed or inverted):
1. <claim>
2. <claim>
[continue — capture all, no maximum]

**Decisions / Calls to Action Embedded**:
- [DECISION] <decision statement>
- [ACTION] <action statement with owner if stated>
- [NONE] if none present

**Critical Data Points** (specific numbers, names, dates, or evidence that anchor the claims):
- <data point>
- <data point>
[continue]

**Structural Skeleton** (top-level sections or logical blocks in source order):
1. <section title or descriptor>
2. <section title or descriptor>
[continue]

**Source Word Count**: <count>
**Estimated Source Resolution**: <1–10>
**Target Resolution**: <1–10>
**Resolution Gap**: <difference, direction>
```

The Intent Scoreboard is **immutable** after creation. It is never modified during processing loops.

---

## Phase 2: The Processing Loop

### 2.1 Loop Configuration

Execute a minimum of **10** processing loops regardless of how quickly the target resolution appears to be reached. If the target resolution is reached before loop 10, use remaining loops to **stabilize and refine** — each additional loop after target-achieved is a stability pass that confirms no intent drift introduced by earlier looser passes.

Loop types by resolution direction:

| Direction | Loop Purpose |
|---|---|
| **Reduction** | Apply content removal operations layer by layer |
| **Expansion** | Apply content restoration / enrichment layer by layer |
| **Stability** | After target reached: verify, tighten transitions, remove artifacts |

### 2.2 Content Layers (Reduction)

Reduction removes content in this priority order — lower numbers are removed first (they carry the least information per word). Higher-numbered layers are preserved until resolution demands their removal.

| Layer | Name | Content Type | First Removed At Resolution |
|---|---|---|---|
| **L1** | Ceremony | Throat-clearing openers, redundant closers, transitional filler ("As we have seen...", "In summary, what we've covered..."), boilerplate sign-offs | 9–10 → 8 |
| **L2** | Hedge stacking | Compound hedges and weak intensifiers ("may potentially be possible that", "very significant", "extremely important") — replaced with precise language or removed | 9–10 → 8 |
| **L3** | Redundant pairs | "each and every", "null and void", "first and foremost" — reduce to single term | 9–10 → 8 |
| **L4** | Redundant restatement | Points stated more than once without adding meaning — retain first, remove repeats | 8 → 7 |
| **L5** | Illustrative examples | Examples used to illustrate a point that is already clearly stated — remove at lower resolutions; keep the most illustrative one at mid resolutions | 7 → 5 |
| **L6** | Background / setup context | Paragraphs explaining the situation before making a point the reader already has context for | 6 → 4 |
| **L7** | Supporting evidence | Evidence and data that *explains* a claim but does not *establish* it — retain claim, compress or remove explanation | 6 → 3 |
| **L8** | Qualifications and caveats | Edge-case nuance, exceptions to rules, "however" clauses that don't materially change the main claim for the target audience | 5 → 3 |
| **L9** | Structural elaboration | Sub-bullets that expand on a parent bullet, nested detail, second-level explanations | 4 → 2 |
| **L10** | Section-level consolidation | Entire sections merged into a single paragraph or sentence when the section's contribution can be absorbed into an adjacent section | 3 → 1 |

> **Layer removal is never binary.** At resolution 5, L5 examples are reduced (keep one per concept); at resolution 3, all examples are removed. The layer table above shows the *range* across which each layer is progressively reduced.

### 2.3 Per-Loop Protocol

For **each loop** (Loop 1 through Loop 10+), execute this exact sequence:

#### Step A — Loop Header

```
---
### Loop <N> of <Max>
**Type**: <Reduction | Expansion | Stability>
**Layers targeted this loop**: <e.g., L1, L2, L3>
**Word count entering loop**: <count>
**Intent Scoreboard check (pre-loop)**: <CLEAR | FLAG: [specific item at risk]>
```

#### Step B — Layer Operations

Apply each targeted layer operation to the working document. For each operation:

- State which layer is being applied
- State the rule being invoked from the layer definition
- Apply the change to the working text

Do not narrate the changes in prose — make them. The output of this step is the modified document text, not a description of modifications.

However, track removed or modified content in a **Reduction Log**:

```
Reduction Log — Loop <N>
| Operation | Layer | Original Text (first 15 words) | Action Taken |
|---|---|---|---|
| 1 | L1 | "As we all know, the marketing landscape has..." | Removed — ceremony opener |
| 2 | L2 | "It may potentially be possible to..." | Rewritten: "It may be possible to..." |
```

#### Step C — Convergence Scoring

After applying operations, score the working document on three dimensions:

```
### Convergence Score — Loop <N>

| Dimension | Score | Notes |
|---|---|---|
| **Word count reduction** | <word count> (<% of original>) | — |
| **Estimated current resolution** | <1–10 estimate> | Based on compression ratio and layers remaining |
| **Intent preservation** | <0–10> | 10 = all scoreboard items fully intact; see below |

**Intent Preservation Detail**:
- Key Claims: <count intact> / <total> intact
- Decisions/Actions: <count intact> / <total> intact
- Critical Data Points: <count intact> / <total> intact
- Structural Skeleton coverage: <yes/partial/no — note any sections collapsed>
- Tone/Register match: <yes/partial/no>

**Convergence Status**: 
<TARGET REACHED | PROGRESSING | OVERSHOOT RISK: [explain]>

**Next Loop Plan**:
<Which layers will be targeted in the next loop and why>
```

#### Intent Preservation Scoring Rules

| Score | Meaning |
|---|---|
| **10** | Every key claim, decision, data point, and structural marker is present and accurate |
| **8–9** | Minor elaboration lost, all key claims intact, ≤1 data point absorbed into prose |
| **6–7** | All key claims intact, some supporting structure compressed, tone may shift slightly |
| **4–5** | Most key claims intact, 1–2 claims present only by implication, data points reduced |
| **2–3** | Theme intact, individual claims compressed into summary statements, data points mostly absent |
| **1** | Essence only — a reader understands the domain and general purpose, no specifics |

> **Intent preservation must never fall below 7.0** during any intermediate loop. If a loop causes it to drop below 7.0, the loop is immediately marked **ROLLBACK** and the previous loop's output is restored. The next loop then attempts a more conservative operation targeting only L1–L3.

### 2.4 Overshoot Detection and Recovery

If the convergence score indicates the current resolution has gone **below** the target (over-compressed):

1. Mark the loop as **OVERSHOOT**
2. Restore the previous loop's output
3. Execute a **Partial Restoration Pass**: reintroduce the most recently removed content items in reverse removal order until the estimated resolution is within 0.5 of target
4. Document the restoration in the Reduction Log with action `RESTORED — overshoot recovery`

### 2.5 Stability Pass Protocol

Once the target resolution is reached (convergence status: TARGET REACHED), any remaining loops are executed as **Stability Passes**:

**Stability Pass operations** (in order):
1. **Transition repair**: Check that paragraph and section transitions still read naturally after content removal — add bridging language only where a gap creates confusion
2. **Orphan detection**: Identify any sentence or bullet that now lacks a referent (e.g., a pronoun with no antecedent, a "see above" with nothing above) — rewrite or remove
3. **Tone calibration**: Verify that the register matches the Intent Scoreboard's stated tone — reduction sometimes strips the warmth or formality that signals tone
4. **Final structure review**: Confirm the structural skeleton from the Intent Scoreboard is still present at the appropriate resolution level — a section need not survive, but its *contribution* must be absorbed somewhere

---

## Phase 3: Validation

After all loops are complete, perform the **Final Validation** — a structured comparison of the processed output against the Intent Scoreboard.

### 3.1 Validation Protocol

```
## Final Validation

**Source document**: [title or label]
**Target resolution**: <N>
**Loops executed**: <count>
**Final word count**: <count> (<% of source word count>)
**Final estimated resolution**: <N>

### Key Claims Validation
| # | Claim (from Scoreboard) | Status | Notes |
|---|---|---|---|
| 1 | <claim> | ✅ INTACT / ⚠️ COMPRESSED / ❌ LOST | <if not intact: what remains> |

### Decisions / Actions Validation
| # | Item | Status | Notes |
|---|---|---|---|

### Critical Data Points Validation
| # | Data Point | Status | Notes |
|---|---|---|---|

### Structural Skeleton Validation
| # | Section | Status | Notes |
|---|---|---|---|

### Tone / Register Validation
**Expected**: <from scoreboard>
**Actual**: <assessed from output>
**Status**: ✅ MATCH / ⚠️ DRIFT / ❌ MISMATCH

### Overall Validation Result

**Intent Preservation Score: <0–10>**
**Resolution Achieved: <1–10>**
**Target Met: YES / NO**

**Validation Verdict**: 
<PASS — output ready for use>
<CONDITIONAL PASS — output ready with notes>
<FAIL — specific items below minimum — remediation required>
```

### 3.2 Validation Failure Remediation

If the validation result is **FAIL**:

1. Identify each failed item (key claim lost, data point missing, etc.)
2. Execute a **targeted restoration pass**: reintroduce only the specific failed items, finding the most compressed form that restores the item
3. Re-score convergence — a restoration may raise the resolution by 0.5–1.0; this is acceptable if it brings intent score to ≥7.0
4. Re-run validation

A maximum of **3 remediation passes** are allowed. If validation still fails after 3 passes, the skill reports the best achieved state and lists the specific items that could not be preserved at the target resolution — informing the user that those items require a higher resolution floor.

---

## Phase 4: Output Delivery

### 4.1 Output Format

Deliver the final output in three blocks:

#### Block 1 — Processed Document
The full text of the document at the target resolution. This is the usable artifact.

#### Block 2 — Resolution Summary Card
```
## Resolution Summary

| Field | Value |
|---|---|
| **Source document** | <title or label> |
| **Crop applied** | <crop description or "None"> |
| **Filters applied** | <filter name(s) in sequence or "None"> |
| **Original resolution** | <N> |
| **Target resolution** | <N> |
| **Achieved resolution** | <N> |
| **Original word count** | <count> |
| **Post-crop word count** | <count or "N/A — no crop"> |
| **Post-filter word count** | <count or "N/A — no filter"> |
| **Output word count** | <count> |
| **Compression ratio** | <e.g., 62% reduction from post-crop/filter baseline> |
| **Processing loops executed** | <count> |
| **Stability passes** | <count> |
| **Intent preservation score** | <0–10> |
| **Validation result** | PASS / CONDITIONAL PASS / FAIL |
```

#### Block 3 — Crop & Filter Audit
Document all crop and filter operations applied. This block is **always present** when any crop or filter was used, and is omitted when neither was applied. It contains three sub-sections:

```
## Crop & Filter Audit

### Crop
**Applied:** YES / NO
**Crop boundary:** <description or "N/A">
**Crop type:** Section / Topic / Question / Range / N/A

| Retained | Discarded |
|---|---|
| <section or topic> | <section or topic> |

### Pre-Filter Snapshot Summary
**Taken:** YES / NO (always YES when any filter was applied)
**Pre-filter word count:** <count>
**Pre-filter item count:** <number of key claims + decisions + data points captured>

| Pre-Filter Item | Type | Fate | Filter Responsible |
|---|---|---|---|
| <first 10 words> | Key Claim / Decision / Data Point | SURVIVED / TRANSFORMED / STRIPPED | <filter name or "N/A"> |

> Items marked STRIPPED were *deliberately removed by the named filter* — they are intentional editorial choices, not losses. Items marked SURVIVED and TRANSFORMED entered the Intent Scoreboard.

### Filters
**Applied:** YES / NO
**Filter sequence:** <filter 1> → <filter 2> → ... (or "None")

| Filter | Purpose | Structural Effect | Content Stripped |
|---|---|---|---|
| <filter name> | <one-line purpose> | restructured / reformatted / reframed / none | <categories stripped or "None"> |
```

#### Block 4 — Content Change Audit
A compact Reduction/Expansion Audit listing the most significant content changes made during resolution processing (changes from crop and filters are in Block 3):

```
## Content Change Audit

### Removed (Reduction) / Added (Expansion)
| Type | Description | Layer | Loop |
|---|---|---|---|
| REMOVED | Illustrative example: "For instance, when a customer visits..." | L5 | Loop 3 |
| REMOVED | Background section: "Historical context for campaign types..." | L6 | Loop 5 |
| RESTORED | Key claim about TCPA compliance deadlines — overshoot recovery | — | Loop 7 |
```

#### Block 5 — Resolution Floor Warning (if applicable)
If any key claims, decisions, or critical data points could not be preserved at the target resolution:

```
## ⚠️ Resolution Floor Warning

The following items from the Intent Scoreboard could not be preserved at resolution <N>. 
The minimum resolution that can contain them is noted:

| Item | Type | Minimum Resolution |
|---|---|---|
| <item description> | Key Claim / Decision / Data Point | <minimum resolution> |
```

---

## Reference: Resolution Quick-Reference Card

| Resolution | Viewer Distance | What Survives | What Is Removed |
|---|---|---|---|
| **10** | 2 inches | Everything | Nothing |
| **9** | 6 inches | All content, filler removed | Ceremony, hedge stacks, redundant pairs |
| **8** | 1 foot | All content, tightened | + Redundant restatements |
| **7** | 2 feet | Full structure, condensed examples | + Some examples reduced |
| **6** | 4 feet | Key content, essential examples | + Background context, partial example removal |
| **5** | 8 feet | Main points + key evidence | + Most examples removed, evidence compressed |
| **4** | 15 feet | Key points + essential data only | + Supporting evidence, caveats |
| **3** | 30 feet | Topics + conclusions | + All examples, most qualifications, structural elaboration |
| **2** | 75 feet | Major themes + essential claims | + Section-level consolidation begins |
| **1** | 200 feet | Essence only | All but the irreducible intent |

---

## Invocation Examples

### Resolution Only
- "Reduce this architecture document to resolution 4." → Apply reduction from estimated current resolution (~10) to 4
- "I have an executive summary at resolution 3 and need it at resolution 6 — expand it." → Apply expansion, flag expansion slots
- "Compress this to a one-paragraph satellite view." → Apply resolution 1
- "Take this and make it appropriate for a VP who has 90 seconds." → Infer resolution ~3–4 based on audience signal; confirm with user before processing

### Crop Only
- "Crop this to the risks section." → Apply section crop, retain at resolution 10, no filter
- "Crop to everything about staffing and team assignments." → Apply topic crop, retain at resolution 10
- "Focus this on answering 'what are the open decisions' — remove everything else." → Apply question-framing crop

### Filter Only
- "Apply the executive filter to this document." → Apply executive filter, no resolution change, no crop
- "Give me just the action items from this." → Apply action-items filter
- "Rewrite this to be neutral — strip the advocacy." → Apply neutral filter
- "Convert this to bullet form." → Apply bullets filter

### Crop + Resolution
- "Crop to the timing section, then reduce to resolution 3." → Crop first, then apply 10-loop reduction
- "Crop to content that answers 'how realistic is the timing' and 'would we need to augment staff', resolution 1." → Topic crop across two questions, then full compression

### Filter + Resolution
- "Apply the risks filter and reduce to resolution 4." → Filter first, then resolution loops
- "Give me the timeline content at resolution 5." → Timeline filter, then reduce
- "Make this executive-ready at resolution 3." → Executive filter, then reduce to resolution 3

### Crop + Filter + Resolution
- "Crop to Section 4, apply the action-items filter, resolution 2." → Full pipeline: crop → filter → compress
- "Crop to the architecture section, apply technical filter and bullets filter, resolution 6." → Crop, two filters in sequence, then moderate compression
- "Crop to the staffing discussion, apply the pro-con filter, reduce to resolution 4." → Crop → pro-con filter → reduce

### Combining Multiple Filters
- "Apply executive filter then neutral filter." → Executive restructures (conclusion-first, stripped detail); neutral then removes any advocacy language introduced by the restructuring
- "Apply risks filter then action-items filter." → Risks surfaces all risk content; action-items then reduces that to only the actionable risk mitigations
- Order matters — filters are always applied in the sequence stated by the user.
