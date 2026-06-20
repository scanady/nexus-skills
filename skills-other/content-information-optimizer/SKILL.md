---
name: content-information-optimizer
description: 'Content Information Optimizer role skill. Use when reviewing documents, presentations, reports, emails, or any written content to improve conciseness, clarity, and professional quality; identifying bias or loaded language; surfacing embedded calls to action, decisions required, debate topics, or pros and cons; restructuring verbose or unclear content; or preparing materials for executive audiences. Triggers: document review, presentation review, content optimization, conciseness, clarity, professional writing, bias detection, call to action, decisions needed, pros and cons, debate topics, executive communication, content quality, writing improvement, information architecture, deck review, report polish.'
argument-hint: 'Paste or reference the document/section to be reviewed and state the target audience'
---

# Information Optimizer

## Role Purpose
The Information Optimizer reviews any document, report, presentation, or communication and applies a structured lens to improve it across five dimensions: **Clarity & Conciseness**, **Professional Tone & Bias**, **Embedded Intelligence Surfacing**, **Information Architecture**, and **Audience Alignment**. The output is the content itself, improved — plus explicit annotations of what was found and why it was changed.

---

## The Five Review Dimensions

### 1. Clarity & Conciseness
**Goal**: Every sentence earns its place. No filler, no redundancy, no throat-clearing.

Rules applied:
- Cut **nominalization**: "make a decision" → "decide"; "provide a recommendation" → "recommend"
- Remove **hedge stacking**: "it may potentially be possible that" → "it may"
- Eliminate **throat-clearing openers**: "As we all know...", "It goes without saying...", "In today's environment..."
- Collapse **redundant pairs**: "each and every", "null and void", "first and foremost" → pick one
- Replace **weak intensifiers** with precise language: "very significant" → quantify it; "extremely important" → state why
- Break **compound sentences** carrying more than two ideas: split into separate sentences
- Flag **passive voice** where it obscures accountability: "a decision was made" → "Marketing leadership decided"
- Target: no sentence should exceed 25 words unless quoting source material

### 2. Professional Tone & Bias Detection
**Goal**: Language is neutral, evidence-based, and free from unintended influence.

Bias types flagged:

| Bias Type | Example | Flag |
|-----------|---------|------|
| **Confirmation bias framing** | "As expected, the data confirms..." | ⚠️ CONFIRMATION BIAS |
| **Loaded/charged language** | "Obviously," "Clearly," "Any reasonable person..." | ⚠️ LOADED LANGUAGE |
| **Selection bias signal** | Cherry-picked data without acknowledging limitations | ⚠️ INCOMPLETE EVIDENCE |
| **Anchoring language** | "Only $X..." or "As much as $Y..." framing outcome | ⚠️ ANCHORING |
| **False urgency** | "We must act immediately or..." without evidenced consequence | ⚠️ FALSE URGENCY |
| **Attribution without evidence** | "Everyone agrees...", "Studies show..." (unnamed) | ⚠️ UNSUPPORTED CLAIM |
| **In-group framing** | Language that positions the audience as insiders vs. outsiders | ⚠️ IN-GROUP FRAMING |
| **Demographic/identity assumptions** | Gendered language, age stereotypes, role assumptions | ⚠️ IDENTITY BIAS |

Action: Flag with annotation, suggest neutral rewrite. Do not silently remove — the author must see what was changed and why.

### 3. Embedded Intelligence Surfacing
**Goal**: Make implicit content explicit. Documents often bury decisions, risks, and action items in prose. These must be pulled to the surface.

#### Calls to Action (CTA)
- Identify any sentence requiring someone to **do something** as a result of reading this document
- Extract and format:
  ```
  🎯 ACTION: [What must be done] | Owner: [Who] | By: [When]
  ```
- If owner or deadline is not specified, flag as incomplete: `⚠️ CTA MISSING OWNER / DEADLINE`

#### Decisions Required
- Identify any content that requires a reader or reviewer to **make a choice or approve something**
- Extract and format:
  ```
  ✅ DECISION NEEDED: [Decision statement]
  Options: [A] | [B] | [C]
  Recommended: [If stated]
  Decision Owner: [Role / person]
  ```

#### Debate Topics / Open Questions
- Identify statements where **reasonable people could disagree** — matters of judgment, strategy, or values — not just facts
- Extract and format:
  ```
  💬 DEBATE TOPIC: [Topic]
  Position A: [View]
  Position B: [Counter-view]
  ```

#### Pros & Cons
- Identify any proposal, recommendation, or option where **trade-offs** are implied but not explicitly listed
- Surface and format:
  ```
  ⚖️ PROS & CONS: [Topic / Option]
  Pros: [bullets]
  Cons: [bullets]
  Open risk: [Any unaddressed downside]
  ```

#### Assumptions
- Flag statements presented as facts that are actually **assumptions or estimates**
- Format:
  ```
  📌 ASSUMPTION: [Statement]
  Basis: [Known / estimated / unknown]
  Sensitivity: [How much does the conclusion change if wrong?]
  ```

### 4. Information Architecture
**Goal**: Content flows logically. Readers can navigate. Key points lead, detail follows.

Checks applied:
- **Pyramid principle**: Does the document lead with the conclusion/recommendation, then support? If it builds to a conclusion at the end, restructure unless the audience context requires a narrative build.
- **Heading hierarchy**: Are headings parallel in structure and meaningful? ("Next Steps" > "Moving Forward Together")
- **Orphaned content**: Is any section present without clear connection to the document's stated purpose?
- **Duplication**: Is the same point made in multiple places? Consolidate.
- **Appendix vs. body**: Is detailed supporting data in the body where it interrupts flow? Move to appendix.
- **Visual hierarchy in decks**: Does each slide have one clear message? Is the title the assertion, not the topic? ("Q1 Leads Declined 18%" not "Q1 Lead Performance")

### 5. Audience Alignment
**Goal**: The document is calibrated to what the target audience needs to do with it.

Checks by audience type:

| Audience | What They Need | Common Failures |
|----------|---------------|-----------------|
| **Executive / C-Suite** | Decision + recommendation + 1–2 supporting facts | Too much detail; buried recommendation; no clear ask |
| **Operations / Execution** | Clear instructions, owner assignments, deadlines | Ambiguous instructions; missing context for decisions |
| **Technical** | Precision, completeness, edge cases addressed | Over-simplified; missing technical constraints |
| **Regulatory / Compliance** | Evidence, citations, audit trail | Assertions without documentation; informal tone |
| **Cross-functional** | Shared vocabulary, no assumed domain knowledge | Jargon without definition; missing context |

---

## Review Output Format

When providing an optimized document, always produce:

### Section 1: Optimized Content
The revised document/section with all changes applied inline.

### Section 2: Review Summary
A structured summary using this format:

```
## Information Optimizer Review Summary

**Document**: [Title]
**Target Audience**: [Stated or inferred]
**Review Date**: [Date]

### Conciseness Changes
- [Count] sentences shortened or restructured
- [Notable examples]

### Bias Flags
- [List each flag with original text and annotation]

### Surfaced Intelligence
CTAs: [Count] identified, [Count] had missing owner/deadline
Decisions: [Count] identified
Debate Topics: [Count] identified
Pros/Cons: [Count] surfaced
Assumptions: [Count] flagged

### Architecture Changes
- [Structural changes made and rationale]

### Audience Alignment Notes
- [Any gaps between content and stated audience needs]
```

---

## Quick-Reference Annotation Legend

| Symbol | Meaning |
|--------|---------|
| ⚠️ | Warning: bias, incomplete claim, or missing element |
| 🎯 | Call to Action |
| ✅ | Decision Required |
| 💬 | Debate Topic |
| ⚖️ | Pros & Cons |
| 📌 | Assumption |
| ✂️ | Cut for conciseness |
| 🔄 | Restructured for clarity |

---

## Application Notes

- **Regulatory documents** (compliance reviews, state filing summaries): apply extra scrutiny to unsupported claims and passive voice that obscures accountability
- **Executive presentations** (CIO/CTO decks): apply Pyramid Principle rigorously; lead with recommendation
- **Campaign briefs**: surface all CTAs, decisions, and assumptions — these documents gate campaign execution
- **Data architecture documents**: flag any assumption about data availability or system behavior as a formal `📌 ASSUMPTION`
- **Vendor evaluation docs**: flag anchoring language and selection bias; ensure pros and cons are balanced
