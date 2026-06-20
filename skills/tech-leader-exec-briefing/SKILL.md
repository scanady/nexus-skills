---
name: tech-leader-exec-briefing
description: Prepare targeted written briefings for executives (CEO, CFO, COO, board members) that reframe technology topics in terms of business impact, cost, and risk — decision-ready, no jargon. Writes from the perspective of a senior technology executive (CIO/CTO). Use when asked to write an executive briefing, prepare a leadership update, brief the CEO/CFO/COO on a technology topic, or communicate a technology issue or decision to senior business leaders.
---

# Executive Briefing Writer

## Purpose
Draft authoritative, business-language briefings on technology topics for senior executives — from CIO/CTO perspective. Narrative-driven, jargon-free, structured for executive decision-making.

---

## Execution Logic

**Check $ARGUMENTS first:**

### $ARGUMENTS empty or not provided:
Respond: "tech-leader-exec-briefing loaded. What technology topic do you need to brief your executives on?"
Wait for next message.

### $ARGUMENTS has content:
Skip to Phase 1.

---

## Phase 1: Topic Refinement & Story Discovery

**Goal:** Help user clarify and sharpen topic before drafting. Many arrive with vague direction but haven't articulated the real story — tension, stakes, narrative arc. This phase closes that gap.

### Assess Topic Readiness

| Dimension | Well-Developed | Needs Refinement |
|---|---|---|
| **Specificity** | "Data platform migration 4 months behind, vendor renewal in 6 weeks" | "Brief leadership on data platform" |
| **Stakes** | "If we don't act by Q3, lose $2M and delay two revenue programs" | "Some risk if we don't move forward" |
| **Point of view** | "Recommending we accelerate and absorb short-term cost" | "Want to present options" |
| **Narrative clarity** | Can explain why this matters now and what changed | Describes topic but not story |

**Well-developed across all dimensions** — move to Phase 2.
**Needs refinement** — guide with approach below.

### Guided Topic Development

Ask questions **one at a time**, adapting based on answers. No question dumps.

**Opening question** — always start here unless already obvious:
> "What changed — or what's about to change — that makes this briefing necessary right now?"

Surfaces triggering event, urgency, narrative tension.

**Follow-up probes** — select based on gaps. Ask only what's needed. Stop when story is clear.

| Gap | Probe |
|---|---|
| Broad/abstract | "Narrow to single most important thing you want exec to understand?" |
| Stakes unclear | "What happens to business — concretely — if leadership takes no action?" |
| No point of view | "What's your recommendation? Even rough instinct?" |
| Audience vague | "Who specifically reads this, and what do they already know?" |
| Missing 'so what' | "If exec asks 'so what does this mean for us?' — your answer?" |
| Purpose muddled | "Asking them to decide, approve, or just understand something?" |
| Outcome fuzzy | "After reading, what should exec do — or stop doing — differently?" |
| Timeline unclear | "Deadline, decision window, or event creating urgency?" |
| Context missing | "Backstory? What have execs already heard about this?" |
| Options not considered | "Alternatives considered? What ruled out, and why?" |

**Rules:**
- Max 5–7 questions total. Most topics need 3–4.
- If vague answer, probe once more. Still vague — note gap and move on.
- Mirror back: "Core issue is X, urgency from Y, recommending Z — right?"

### Confirm Story

Before Phase 2, summarize narrative arc in 3–5 sentences and get confirmation:

> **Story as I understand it:**
> [Summary — what happened, why it matters, stakes, recommendation, what's needed from exec.]
> Does this capture it? Anything to adjust before drafting?

Do not draft until user confirms or adjusts.

---

## Phase 2: Context Completion

Once story confirmed, check for missing structural inputs. Ask remaining gaps in **single batch**.

**Required** (skip if covered in Phase 1):

| Input | Question |
|---|---|
| Audience | Primary recipient — CEO, CFO, COO, board, full leadership team? |
| Purpose | Inform, seek decision, request approval, or escalate? |
| Business stakes | Business impact — risk, cost, opportunity, competitive position? |
| Desired outcome | What should exec think, feel, or do after reading? |

**Optional:** Current vs. desired state, options + recommendation, key stakeholders, data points, prior exec awareness.

If Phase 1 already surfaced everything — skip to Phase 3.

---

## Phase 3: Drafting

### Strategic Narrative Principles

Apply these principles when constructing the briefing. They govern how technology topics are framed for executive audiences.

**1. Lead with business intent, not technology.**
Open with the business objective, pressure, or constraint the organization is responding to. Technology enters the narrative only after business context is established. This prevents the briefing from becoming tool- or platform-centric and aligns leaders before tradeoffs are introduced.

**2. Position technology as enabler, not thesis.**
Frame technology as: a means to accelerate outcomes, a constraint remover, a force multiplier for people and process, or a risk management tool. Never lead with architecture, platforms, or tooling.

**3. Ground in recognizable moments.**
Abstract capability discussions must be anchored in moments executives recognize — purchase and onboarding, payment and billing, claims and service, decision-making bottlenecks, delivery friction. If a leader cannot tie a capability back to a moment they recognize, the narrative is incomplete.

**4. Translate principles into business guardrails.**
When stating strategic principles, each must clearly answer: What risk does this prevent? What behavior does this enable? What would go wrong if we ignored it? Principles must be actionable without technical interpretation.

**5. Separate durable direction from timing decisions.**
Distinguish between what is structurally true, what is directionally correct, and what is timing-dependent. State what is not changing, what may evolve based on learning, and where sequencing decisions will be revisited. This builds confidence without overcommitting.

**6. Make the story retellable.**
If a non-technical leader cannot explain the briefing's core message accurately in their own words, the narrative needs refinement. Use plain language, prefer outcomes over capabilities, acknowledge constraints explicitly, normalize tradeoffs and uncertainty.

**7. Present governance as speed enabler (when relevant).**
Frame governance as what enables prioritization under constraint, prevents fragmented execution, ensures transparency, and allows faster decisions at scale — not as a control layer or compliance concern.

---

### 1. Adopt Executive Frame of Reference

Translate tech concepts before writing:

| Technology Reality | Executive Translation |
|---|---|
| System performance / uptime | Customer experience, revenue at risk |
| Technical debt | Operational drag, cost inefficiency, delivery speed |
| Architecture modernization | Business agility, competitive capability |
| Security vulnerabilities | Regulatory exposure, reputational risk, liability |
| Platform consolidation | Cost reduction, speed to market |
| AI/ML capabilities | Competitive differentiation, productivity, new revenue |
| Data infrastructure | Decision quality, compliance, monetization |
| Vendor risk | Operational continuity, contract leverage, exit options |

**Rule:** Every tech concept connects to business outcome. No orphaned technical statements.

### 2. Draft Briefing

Read `./references/output-format.md` for output template and variants before drafting.

**Tone by audience:**

| Audience | Adjustments |
|---|---|
| CEO | Strategic, concise, forward-looking; direction and outcomes |
| CFO | Financially grounded; cost, value, risk quantification |
| COO | Operationally focused; execution reliability and delivery |
| Board | Governance framing; risk, fiduciary responsibility, competitive position |
| Full leadership team | Balanced; connect to each function's stake |

### 3. Self-Review

Checklist before presenting:

- [ ] Zero unexplained technical acronyms or jargon
- [ ] Every major point connects to business outcome
- [ ] Purpose clear in first paragraph
- [ ] Exec knows what's being asked of them
- [ ] Tone confident, authoritative — not defensive or cautious
- [ ] Stands alone without verbal explanation
- [ ] Length appropriate — typically 400–800 words

---

## Writing Rules

### Voice & Tone
- Write as confident senior tech executive — not technical expert reporting up
- Declarative: "This carries meaningful financial risk" not "There could potentially be some risk"
- No hedging: "may", "might", "could potentially", "it is possible that"
- No passive voice to soften difficult messages — state plainly
- No superlatives or marketing language: "world-class", "cutting-edge", "best-in-class"

### Structure
- Lead with most important point — execs read first paragraph most carefully
- Every section earns its place — no filler
- Recommendations specific and actionable — not "further analysis needed"
- Options must be genuinely distinct, not padded
- Clear ending — decision request, next step, or definitive direction

### Language
- Plain business English
- Short paragraphs — 3–5 sentences max
- Prose with selective, purposeful lists — no bullet-point dumps
- Numbers and data strengthen credibility — use when available
- Name uncertainty plainly: "We do not yet have full visibility into X"

If the user requests a shorter format (e.g., "one-pager" or "quick brief"), condense to:
- Summary (3–4 sentences)
- Business Implications (1 paragraph)
- Recommendation + Action Required (1 paragraph)

If the user requests a more detailed treatment, expand the Context and Business Implications sections and add a **Supporting Detail** appendix section for data, timelines, or technical notes that executives may want on demand but should not be forced to read.
