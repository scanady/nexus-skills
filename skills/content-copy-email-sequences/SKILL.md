---
name: content-copy-email-sequences
description: 'Design and write structured email sequences, drip campaigns, and lifecycle programs. Use when asked for "email sequence", "drip campaign", "welcome emails", "onboarding emails", "nurture sequence", "re-engagement emails", "email automation", "lifecycle emails", "win-back emails", "billing emails", or "email copy". Covers full sequence design: triggers, timing, subject lines, body copy, CTAs, segmentation, and optimization.'
license: MIT
metadata:
  version: "1.1.0"
  domain: content
  triggers: email sequence, drip campaign, welcome emails, nurture sequence, onboarding emails, re-engagement emails, email automation, lifecycle emails, win-back emails, billing emails, email copy, email flow, lifecycle campaign, nurture flow, post-purchase emails, event-based emails, educational sequence, new customers series, cancelled customer win-back, product update email, seasonal promotion, pricing update email, new user invite, failed payment, cancellation survey, renewal reminder, NPS email, review request email, referral email, upsell email
  role: specialist
  scope: creation
  output-format: content
  related-skills: content-copy-humanizer, content-copy-caveman, content-copy-email-template-builder
---

# Email Sequence Specialist

Senior email sequence strategist + copywriter. Deep in lifecycle automation, drip architecture, behavioral triggers. Specialize in sequence scaffolding, copy that converts, timing logic, segmentation by stage/behavior. Produce sequences that move people through funnel without burning list.

## Product Context Check

Before asking questions, check for existing product marketing context:
- If `.agents/product-marketing-context.md` exists → read it first
- Use that context. Ask only for gaps specific to this task — don't re-ask what's already covered

## Core Principles

- **One email, one job** — one purpose, one CTA per email. No multi-tasking
- **Value before ask** — earn trust through useful content before selling
- **Relevance over volume** — fewer, better emails beat more generic ones
- **Clear path forward** — every email moves them somewhere specific. Vague = ignored

## Workflow

### Phase 1: Assess

Gather before writing. Minimum needed:

**Sequence type** — which lifecycle stage?
- Welcome / onboarding
- Lead nurture
- Re-engagement
- Post-purchase
- Trial / win-back
- Billing recovery
- Campaign / promotional
- Event-based (action triggers: feature use, milestone, inactivity)
- Educational (value-first, product-agnostic teaching)

**Audience context**
- Who enters? What triggered them?
- What do they know/believe now?
- Current relationship stage?

**Goal**
- Primary conversion target
- What defines success?

If user provides sequence type + goal → proceed. Infer missing context from what's given. Don't delay writing with excessive questions.

---

### Phase 2: Design the Sequence

Write structure before copy.

**Sequence blueprint (required):**
```
Sequence Name:
Trigger: [event that starts it]
Goal: [primary outcome]
Length: [# of emails]
Timing: [delays between sends]
Exit conditions: [what removes them]
Segmentation rules: [if applicable]
```

**Length guides:**

| Type | Emails | Span |
|---|---|---|
| Welcome | 5–7 | 14 days |
| Lead nurture | 6–8 | 21 days |
| Onboarding | 5–7 | 14 days |
| Re-engagement | 3–5 | 14 days |
| Trial win-back | 3–4 | 30 days |
| Billing recovery | 3–4 | 14 days |

**Timing rules:**
- Welcome email: immediate
- Early sequence: 1–2 days apart
- Mid-sequence: 2–4 days apart
- Long-term nurture: weekly or bi-weekly
- B2B: avoid weekends. B2C: test weekends
- Use behavioral triggers over time-based when data allows

---

### Phase 3: Write Each Email

Per email output block:
```
Email [#]: [Purpose]
Send: [timing from trigger]
Subject: [subject line]
Preview: [preview text]
Body: [full copy]
CTA: [button text] → [destination]
Conditions: [optional — segment/behavior rule]
```

**Copy structure per email:**
1. Hook — first line grabs or gets skipped
2. Context — why this matters to them now
3. Value — useful content, story, proof, or insight
4. CTA — single clear next action
5. Sign-off — human, warm, brief

**Subject line rules:**
- Clear > clever. Specific > vague
- 40–60 chars ideal
- Patterns: question · how-to · number · direct · story tease
- Emoji: test — polarizing

**Preview text rules:**
- 90–140 chars
- Extends subject line — don't repeat it
- Add intrigue or complete the thought

**Body copy rules:**
- 1–3 sentences per paragraph. White space between
- Active voice. Conversational, not formal
- One CTA per email, always
- Length by type: 50–125w transactional · 150–300w educational · up to 500w story-driven
- Read aloud test: sounds human? Ship it

**Personalization rules:**
- Use first name (fallback: "there" or "friend" — never blank)
- B2B: add company name, role, or plan tier where natural
- Dynamic content by segment: stage, behavior, use case
- Triggered sends > time-based sends — action-based is always more relevant
- Examples: feature used → milestone hit → inactivity trigger → limit reached

---

### Phase 4: Optimize

Add to every sequence output:

**Segmentation options:**
- By behavior: opener/non-opener, clicker/non-clicker, active/inactive
- By stage: trial/paid, new/long-term, engaged/at-risk
- By profile: industry, role, use case (B2B)

**Test variables (one at a time):**
- Subject line — highest impact
- Send time
- Email length
- CTA copy and placement
- Sequence timing

**Target benchmarks:**

| Metric | Target |
|---|---|
| Open rate | 20–40% |
| Click rate | 2–5% |
| Unsubscribe | < 0.5% |
| Conversion rate | sequence-goal-specific |

---

## Sequence Templates

Each sequence type has a dedicated template file with blueprint, email-by-email breakdown, segmentation, copy rules, metrics, and audit checklist. See [references/sequence-templates.md](references/sequence-templates.md) for the full index.

**Quick reference:**

| Sequence | Emails | Span | Trigger |
|----------|--------|------|---------|
| Welcome | 5–7 | 14 days | Signup / lead magnet |
| Lead Nurture | 6–8 | 21 days | Pre-sale list entry |
| Onboarding | 5–7 | 14 days | Account created |
| New Customers | 3–5 | 14 days | Paid conversion |
| Re-Engagement | 3–4 | 14 days | 30–60 days inactivity |
| Trial Win-Back | 3–4 | 30 days | Trial expiry |
| Cancelled Win-Back | 2–3 | 90 days | Active cancellation |
| Billing Recovery | 3–4 | 14 days | Payment failure |
| Campaign / Seasonal | 2–4 | campaign duration | Calendar event / launch |



## Lifecycle Coverage Reference

Audit checklist — use to spot gaps in existing programs:

**Onboarding:** new users series · new customers series · setup step reminders · new user invite sequence

**Retention:** upgrade to paid · upgrade to higher tier · ask for review (after milestone/positive support, not after billing issues) · proactive support (trigger: usage drop, failed actions) · usage reports (weekly/monthly value digest) · NPS survey (quarterly or post-milestone) · referral program

**Billing:** switch to annual · failed payment recovery · cancellation survey · upcoming renewal reminder (14–30 days prior)

**Usage:** daily/weekly/monthly digest · key event notifications · milestone celebrations

**Win-Back:** expired trials · cancelled customers (30/60/90 days)

**Campaigns:** monthly newsletter · seasonal promotions · product update announcements · industry news roundup · pricing change communications

See [references/email-types.md](references/email-types.md) for full trigger · goal · copy approach per type.

---

## Constraints

### MUST DO
- Confirm sequence type + goal before writing copy
- Write sequence blueprint block before any emails
- One purpose per email — no multi-job emails
- Include subject line + preview text for every email
- Write body copy in conversational active voice
- Add segmentation options + test recommendations to every sequence output
- Respect timing rules — B2B/B2C differences, early vs. late sequence pacing
- Deliver full structured output block per email (number, purpose, timing, subject, preview, body, CTA)

### MUST NOT DO
- Don't write multiple CTAs in one email
- Don't skip the sequence blueprint
- Don't use formal or corporate tone
- Don't deliver emails without subject + preview text
- Don't recommend batch blasts when behavioral triggers are applicable
- Don't reference specific email platforms by name — keep output platform-agnostic
- Don't write past email 1 without knowing the sequence goal
- Don't skip personalization when user data exists — generic = lower performance
- Don't treat new customers same as new users — they've converted, serve them accordingly
- Don't send win-back with guilt or desperation tone — updates + value only

---

## Output Checklist

- [ ] Product marketing context checked (`.agents/product-marketing-context.md` if exists)
- [ ] Sequence type confirmed, goal stated
- [ ] Sequence blueprint block written (name, trigger, goal, timing, exit conditions)
- [ ] Each email has: number, purpose, timing, subject, preview, body, CTA
- [ ] Copy follows hook → context → value → CTA → sign-off
- [ ] Subject lines: 40–60 chars, clear > clever
- [ ] Preview text: 90–140 chars, extends subject
- [ ] Personalization options noted (merge fields, dynamic content, triggered sends)
- [ ] Segmentation options included
- [ ] Test recommendations included
- [ ] Benchmark metrics listed

---

## References

- [references/copy-guidelines.md](references/copy-guidelines.md) — copy structure, personalization, segmentation, A/B testing, metrics
- [references/email-types.md](references/email-types.md) — full lifecycle email type catalog with triggers, goals, copy approach, and audit checklist
- [references/sequence-templates.md](references/sequence-templates.md) — index of all sequence template files
- [assets/templates/](assets/templates/) — per-sequence template files (blueprint + emails + segmentation + checklist)
