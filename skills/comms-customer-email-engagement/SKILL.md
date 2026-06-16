---
name: comms-customer-email-engagement
description: 'Design and write high-engagement email sequences, drip campaigns, and lifecycle programs using hyper-personalization, behavioral triggers, and interactive content. Use when asked for "email sequence", "drip campaign", "welcome emails", "onboarding emails", "nurture sequence", "re-engagement emails", "email automation", "lifecycle emails", "win-back emails", "billing emails", "email engagement", "email personalization", "email segmentation", or "email cadence". Covers full sequence design: behavioral triggers, audience segmentation, hyper-personalization, mobile-first layout, interactive elements, subject line optimization, A/B testing, storytelling, urgency tactics, and performance metrics.'
license: MIT
metadata:
  version: "2.0.0"
  domain: comms
  triggers: email sequence, drip campaign, welcome emails, nurture sequence, onboarding emails, re-engagement emails, email automation, lifecycle emails, win-back emails, billing emails, email copy, email flow, lifecycle campaign, nurture flow, post-purchase emails, email engagement, email personalization, behavioral triggers, email segmentation, email cadence, interactive email, mobile email, email A/B test, email metrics, abandoned cart email, milestone email
  role: specialist
  scope: creation
  output-format: content
  related-skills: comms-customer-email-designer, content-copy-humanizer, content-copy-caveman
---

# Customer Email Engagement Specialist

Senior email engagement strategist + copywriter. Deep expertise in lifecycle automation, behavioral trigger architecture, hyper-personalization, and data-driven engagement optimization. Specialize in crafting sequences that treat every recipient as an individual — using purchase history, browsing behavior, and real-time signals to deliver the right message at the right moment. Produce sequences that build lasting relationships, drive measurable action, and respect the inbox.

## Workflow

### Phase 1: Assess & Segment

Gather context and define audience segments before writing. Segmentation is the foundation — every sequence decision flows from it.

**Sequence type** — which lifecycle stage?
- Welcome / onboarding
- Lead nurture
- Re-engagement / reactivation
- Post-purchase / cross-sell
- Trial / win-back
- Billing recovery
- Campaign / promotional
- Abandoned cart / browse abandonment
- Milestone / loyalty
- Feedback / NPS

**Audience segmentation** — divide before you write:

| Segmentation Layer | Dimensions | Example Segments |
|---|---|---|
| **Behavioral** | Purchase history, browsing patterns, email engagement, product usage, cart activity | Repeat buyers vs. one-time, active openers vs. dormant, feature power users vs. basic |
| **Lifecycle stage** | Relationship maturity with the brand | Prospect → new subscriber → active customer → loyal → at-risk → lapsed |
| **Demographic** | Age, location, job title, industry, company size | Enterprise vs. SMB, US vs. EU (timezone + compliance), decision-maker vs. end-user |
| **Value-based** | Revenue contribution, LTV prediction, engagement score | High-value VIP → standard → low-engagement |
| **Preference** | Stated interests, email frequency preferences, channel preferences | Weekly digest vs. real-time alerts, product category interests |

**Segmentation rules:**
- Never send the same email to all segments — adapt copy, offers, timing, and tone per segment
- Minimum viable segmentation: behavioral (engagement level) + lifecycle stage
- Advanced: layer behavioral + demographic + value-based for highest relevance
- Every sequence blueprint must declare which segments receive which variant

**Context to gather:**
- Who enters the sequence? What action or event triggered them?
- What data is available for personalization? (purchase history, browsing, demographics, preferences)
- Current relationship stage and engagement level?
- Primary conversion target and success definition?

If user provides sequence type + goal → proceed. Infer missing context. Don't stall with excessive questions.

---

### Phase 2: Design the Sequence

Write structure before copy. Define behavioral triggers first — timing is secondary to user actions.

**Sequence blueprint (required):**
```
Sequence Name:
Entry Trigger: [behavioral event that starts it]
Goal: [primary outcome]
Target Segment: [who receives this variant]
Length: [# of emails]
Timing: [delays between sends — behavioral override notes]
Behavioral Branches: [conditional paths based on recipient actions]
Exit Conditions: [what removes them]
Personalization Data Required: [fields/signals needed]
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
| Abandoned cart | 3–4 | 7 days |
| Post-purchase | 4–6 | 30 days |
| Milestone/loyalty | 2–3 | Event-driven |

**Behavioral trigger architecture:**

Prioritize behavioral triggers over time-based sends. Time-based cadence is the fallback, not the default.

| Trigger Type | Event | Sequence Action |
|---|---|---|
| **Cart abandonment** | Item added, checkout not completed within 1hr | Enter abandoned cart sequence |
| **Browse abandonment** | Viewed product/category 2+ times, no purchase | Send personalized product reminder |
| **Purchase completed** | Order confirmed | Enter post-purchase → cross-sell sequence |
| **Feature activation** | User completes key setup step | Send next-step onboarding email |
| **Inactivity** | No login/open/click in 30 days | Enter re-engagement sequence |
| **Milestone reached** | Usage threshold, anniversary, loyalty tier | Trigger celebration + reward email |
| **Payment failure** | Charge declined | Enter billing recovery sequence |
| **Trial expiring** | X days before trial end | Enter trial conversion sequence |
| **Feedback signal** | NPS score submitted, support ticket closed | Branch to appropriate follow-up |
| **Engagement drop** | Open/click rate drops below rolling average | Trigger re-engagement or frequency adjustment |

**Behavioral branching rules:**
- After each email, define at least two paths: engaged (opened/clicked) vs. non-engaged
- Engaged recipients → advance to next value email on schedule
- Non-engaged → wait longer, try different subject line angle, or reduce frequency
- High-engagement signals (multiple clicks, replies) → accelerate sequence or escalate offer
- Negative signals (unsubscribe click without completing, spam report) → immediately suppress

**Timing rules:**
- Welcome email: immediate (within minutes of trigger)
- Abandoned cart: 1hr → 24hr → 72hr (three-touch max)
- Early sequence: 1–2 days apart
- Mid-sequence: 2–4 days apart
- Long-term nurture: weekly or bi-weekly
- B2B: Tuesday–Thursday, 8–10am recipient timezone. B2C: test evenings + weekends
- Behavioral triggers always override scheduled timing — if user acts, respond to the action

**Sending cadence & consistency:**
- Establish a predictable schedule — recipients should expect your emails, not be surprised by them
- Maximum frequency: 1 email/day during active sequences, 2–3/week for ongoing engagement
- Respect stated preferences — if they chose weekly digest, don't send daily
- Seasonal/promotional surges: max 1.5x normal frequency, return to baseline within 1 week
- Monitor unsubscribe rate per cadence change — any spike above 0.5% signals over-sending

---

### Phase 3: Hyper-Personalize

Go far beyond `[First Name]`. Personalization drives engagement when it reflects real behavior and genuine relevance.

**Personalization hierarchy** — use the deepest available layer:

| Level | Data Source | Example | Impact |
|---|---|---|---|
| **L1: Identity** | Name, company, location | "Hi [Name]" | Baseline — expected, not impressive |
| **L2: Behavioral** | Purchase history, browsing, cart contents | "The [Product] you viewed is back in stock" | High — feels relevant and timely |
| **L3: Contextual** | Time of day, weather, device, location | "Perfect for your weekend in [City]" | Medium — adds delight when authentic |
| **L4: Predictive** | ML-driven recommendations, next-best-action | "Based on your last 3 orders, you'll love [Product]" | Highest — feels like a personal shopper |
| **L5: Progressive** | Accumulated interaction history across touchpoints | "Since you joined 6 months ago, you've [achievement]" | High — builds relationship narrative |

**Personalization rules:**
- Every email must use at least L2 (behavioral) personalization when data is available
- Product recommendations: show 2–4 items max, based on actual browsing/purchase data — never random
- Dynamic content blocks: swap sections (hero image, product grid, copy angle) per segment
- Personalization tokens must have fallback defaults — broken merge tags destroy trust
- Reference specific actions: "Your recent order of [Product]" not "Your recent activity"
- Time-sensitive personalization: "Your trial ends in 3 days" with live countdown, not static text
- Never personalize in ways that feel surveillance-like — "We noticed you browsed at 2am" is creepy, "Still thinking about [Product]?" is helpful

**Dynamic content blocks by segment:**

| Block | High-Value Customer | New Subscriber | At-Risk Customer |
|---|---|---|---|
| Hero | Loyalty reward / exclusive preview | Welcome + quick start | "We miss you" + incentive |
| Product grid | Curated premium picks based on history | Popular / best-rated items | Items from abandoned browsing |
| Social proof | VIP community stats | Broad customer count | Similar customer success story |
| CTA | "Shop Your Exclusives" | "Start Exploring" | "Come Back & Save 15%" |

---

### Phase 4: Write Each Email

Per email output block:
```
Email [#]: [Purpose]
Send: [timing from trigger]
Segment: [which audience segment(s)]
Subject: [subject line]
Preview: [preview text]
Personalization: [dynamic elements used — L1/L2/L3/L4/L5]
Body: [full copy with personalization tokens marked]
CTA: [button text] → [destination]
Interactive Element: [poll/quiz/countdown/none — describe if included]
Conditions: [behavioral branch rules]
Mobile Notes: [any mobile-specific layout considerations]
```

**Copy structure per email:**
1. Hook — personalized first line using behavioral data; grabs or gets skipped
2. Context — why this matters to them now, referencing their specific situation
3. Value — useful content, story, proof, or insight (never filler)
4. Social proof — brief, relevant proof point (customer result, usage stat, review)
5. CTA — single clear next action with outcome-focused button text
6. Sign-off — human, warm, brief

#### Subject Line Optimization

Subject lines determine everything. Optimize aggressively.

**Rules:**
- Short wins: aim for under 5 words when possible, max 40 characters for mobile
- Personalized: include recipient's name, company, or referenced product when data is reliable
- Specific > generic: "Your [Product] ships tomorrow" beats "Order Update"
- One technique per subject line — don't stack curiosity + urgency + personalization
- No ALL CAPS words. Max 1 exclamation mark. One emoji max, brand-appropriate only
- Test relentlessly — subject lines are the #1 A/B testing priority

**Subject line formulas by engagement goal:**

| Goal | Formula | Example |
|---|---|---|
| Open (curiosity) | Incomplete thought | "About your [Product]…" |
| Open (personal) | Name + specific reference | "[Name], your style picks are ready" |
| Open (urgency) | Time constraint + stake | "24 hrs left on your [Offer]" |
| Open (value) | Clear benefit, no fluff | "3 ways to get more from [Feature]" |
| Open (social) | Peer reference | "What [X] customers do differently" |
| Re-engage | Direct + empathetic | "We haven't heard from you, [Name]" |

**Preview text rules:**
- 40–90 characters
- Extends subject line — adds context the subject couldn't fit
- Never repeats the subject
- Strong preview text can lift open rates 10–15%

#### Body Copy Rules

- 1–3 sentences per paragraph. Generous white space between paragraphs
- Active voice throughout. Conversational — not corporate, not sloppy
- One primary CTA per email, always
- Length by type: 50–100w transactional · 100–200w educational · up to 400w story-driven
- Read aloud test: if it sounds like a robot or a press release, rewrite
- Lead with value — earn attention before asking for action
- Use bold for key phrases and benefits — support scanners
- Bullet lists for 3+ items — never inline comma-separated lists of features

#### Storytelling & Visual Direction

Don't just list features. Tell stories that create connection.

**Storytelling patterns:**

| Pattern | Structure | Best For |
|---|---|---|
| Customer spotlight | "[Customer] had [problem] → tried [product] → achieved [result]" | Social proof, case studies |
| Before/after | Paint the pain → show the transformation | Onboarding, feature adoption |
| Behind the scenes | Share the why/how behind a feature or decision | Brand building, launches |
| Milestone narrative | "When you started → what you've done → what's next" | Retention, anniversary |

**Visual direction notes** (include in output for design team):
- Recommend hero image concept and placement
- Suggest where GIFs or short video thumbnails add value (product demos, how-tos)
- Note when a visual should be personalized (e.g., product image from browse history)
- Keep image-to-text ratio under 40:60 for deliverability
- All visuals must have alt text — emails must work with images off

---

### Phase 5: Engagement Tactics

Apply these selectively per sequence. Not every email needs every tactic — match to goal.

#### Interactive Content

Interactive elements increase click rates 2–3x. Use when gathering feedback or deepening engagement.

| Element | Use Case | Implementation Note |
|---|---|---|
| **Poll** (1-click) | Quick preference check, content direction | Single-question, 2–4 options, results shown on click-through |
| **Survey link** | NPS, CSAT, product feedback | Short (3–5 questions max), incentivize completion |
| **Quiz** | Product recommendation, knowledge check | 3–5 questions → personalized result page |
| **Countdown timer** | Sale ending, trial expiring, event approaching | Live timer (not static image) — falls back to text deadline |
| **Scratch/reveal** | Discount reveal, gamified engagement | Use sparingly — once per quarter max |
| **Image carousel** | Product showcase, feature tour | Fallback to stacked images for non-supporting clients |
| **Add to calendar** | Event, webinar, renewal date | .ics file or calendar link |

**Interactive content rules:**
- Always provide a non-interactive fallback — not all email clients support interactive elements
- One interactive element per email maximum
- Interactive elements complement the CTA, never replace it
- Gather data from interactions to fuel future personalization

#### Urgency & Scarcity

Drives immediate action when used authentically. Destroys trust when manufactured.

**Legitimate urgency tactics:**

| Tactic | When to Use | Example |
|---|---|---|
| Deadline-based | Real expiration (sale, trial, offer) | "This offer expires Friday at midnight" |
| Quantity-based | Genuine low stock or limited seats | "Only 12 spots left for the workshop" |
| Early access | Reward for fast action | "First 50 subscribers get early access" |
| Price increase | Planned pricing change | "Current pricing ends [Date] — lock in now" |

**Urgency rules:**
- Only use urgency when the constraint is real — fake urgency trains recipients to ignore you
- Maximum 1 urgency-driven email per sequence (2 for cart abandonment)
- Never combine multiple urgency types in one email
- Always state the specific deadline or quantity — "limited time" without a date is meaningless
- Countdown timers: use live timers, not static images that show wrong times on re-open
- Follow through — if you say the offer ends Friday, it ends Friday

---

### Phase 6: Mobile-First Design

Over 60% of emails are opened on mobile. Design for the small screen first, then enhance for desktop.

**Layout rules:**
- Single-column layout — no multi-column grids that break on mobile
- Minimum font size: 16px body, 22px headlines
- CTA buttons: minimum 44x44px tap target, full-width on mobile
- Padding: 20px minimum on all sides
- Line length: 35–45 characters per line on mobile
- Stack content vertically — hero image → headline → body → CTA → footer

**Mobile-specific guidance:**

| Element | Mobile Rule |
|---|---|
| Subject line | Under 35 characters visible — front-load key words |
| Preview text | First 40 chars must work standalone — mobile truncates |
| Images | Max 600px wide, compress for fast load (<100KB per image) |
| CTA button | Full-width, high contrast, thumb-friendly placement |
| Body text | 16px minimum, high contrast (4.5:1), generous line-height (1.5) |
| Links | Space links 10px+ apart — prevent mis-taps |
| Video | Thumbnail + play button linking to hosted video — never embed |
| Dark mode | Test in dark mode — use transparent PNGs, avoid white backgrounds on images |

**Responsive design notes (include in output):**
- Specify which elements stack, hide, or resize between mobile and desktop
- Note where progressive disclosure helps — expandable sections for detailed content
- Indicate when a mobile-specific CTA placement differs from desktop

---

### Phase 7: Optimize & Measure

Add to every sequence output. Optimization is not optional.

**A/B testing framework:**

Test one variable at a time. Run each test to statistical significance before deciding.

| Priority | Variable | Sample Size Needed | Duration |
|---|---|---|---|
| 1 (highest) | Subject line | 1,000+ per variant | 24–48 hrs |
| 2 | CTA text + placement | 1,000+ per variant | 48–72 hrs |
| 3 | Send time | 2,000+ per variant | 1–2 weeks |
| 4 | Email length / format | 1,000+ per variant | 48–72 hrs |
| 5 | Personalization depth | 2,000+ per variant | 1–2 weeks |
| 6 | Interactive vs. static | 1,000+ per variant | 48–72 hrs |

**A/B testing rules:**
- Never test more than one variable simultaneously
- Minimum 95% confidence before declaring a winner
- Document every test result — build an institutional knowledge base
- Winning variants become the new control for subsequent tests
- Test across segments — a winner for new subscribers may lose for loyal customers

**Segmentation-driven optimization:**
- Track metrics per segment, not just aggregate — a 25% open rate that's 40% for VIPs and 10% for dormant users hides the real story
- Adjust copy, offers, and frequency per segment based on performance data
- Suppress segments that consistently underperform — protect sender reputation
- Graduate high-engagement recipients to more personalized, higher-frequency tracks

**Key metrics — monitor per email and per sequence:**

| Metric | What It Measures | Target | Action If Below |
|---|---|---|---|
| **Open rate** | Subject line effectiveness + sender trust | 25–45% | Test new subject lines, check sender name, verify deliverability |
| **Click-through rate (CTR)** | Content relevance + CTA strength | 3–7% | Improve CTA clarity, strengthen value proposition, add personalization |
| **Click-to-open rate (CTOR)** | Content quality for engaged readers | 15–25% | Better body copy, clearer CTA, more relevant content |
| **Conversion rate** | End-to-end sequence effectiveness | Sequence-goal-specific | Review full funnel — landing page, offer, timing |
| **Unsubscribe rate** | Audience tolerance / relevance | < 0.3% per email | Reduce frequency, improve segmentation, check content relevance |
| **Bounce rate** | List hygiene | < 2% | Clean list, verify opt-in process, remove invalid addresses |
| **Spam complaint rate** | Trust + deliverability risk | < 0.05% | Immediate review — check frequency, content, opt-in source |
| **Revenue per email** | Direct monetary impact | Benchmark per segment | Optimize offers, timing, personalization |
| **List growth rate** | Acquisition health | Net positive monthly | Review opt-in sources, incentives |

**Deliverability monitoring:**
- Track inbox placement rate (not just delivery rate) — delivered to spam = not delivered
- Monitor sender reputation score weekly
- Warm up new sending domains/IPs gradually — start with engaged segments
- Authenticate all sends: SPF, DKIM, DMARC configured and passing

---

## Sequence Templates

### Welcome (Post-Signup)

| # | Timing | Purpose | Subject Pattern | Personalization |
|---|---|---|---|---|
| 1 | Immediate | Welcome + single next step | "Welcome to [X] — here's step one" | L1: Name; L2: signup source |
| 2 | Day 1–2 | Quick win based on stated interest | "Get your first [result] in 10 min" | L2: selected category/interest |
| 3 | Day 3–4 | Origin story / why we exist | "Why we built [X]" | L1: Name |
| 4 | Day 5–6 | Social proof matching their segment | "How [Similar Customer] achieved [Result]" | L2: industry/role match |
| 5 | Day 7–8 | Overcome likely objection | "[Common objection]? Here's the fix" | L4: predicted concern |
| 6 | Day 9–11 | Feature highlight relevant to usage | "Have you tried [Feature] yet?" | L2: features not yet used |
| 7 | Day 12–14 | Conversion + interactive element | "Ready to [upgrade/commit]?" | L5: journey summary; quiz/poll |

**Behavioral branches:**
- Opened emails 1–3 + clicked → accelerate to email 5 (skip 4)
- No opens after email 2 → switch subject line angle, extend timing to 3 days
- Clicked CTA on email 5 → exit sequence, enter onboarding or sales track

---

### Lead Nurture (Pre-Sale)

| # | Timing | Purpose | Personalization |
|---|---|---|---|
| 1 | Immediate | Deliver lead magnet + brief intro | L2: content topic downloaded |
| 2 | Day 2–3 | Expand on topic, establish expertise | L2: pages browsed after download |
| 3 | Day 4–5 | Problem deep-dive, show empathy | L3: industry-specific pain points |
| 4 | Day 6–8 | Solution framework — educational, not salesy | L2: features most viewed |
| 5 | Day 9–11 | Case study matching their segment + soft CTA | L2: company size/industry match |
| 6 | Day 12–14 | Differentiation vs. alternatives | L4: predicted comparison interest |
| 7 | Day 15–18 | Objection handler + interactive poll | L2: engagement patterns; poll |
| 8 | Day 19–21 | Direct offer + authentic urgency if available | L2: full engagement summary |

---

### Abandoned Cart

| # | Timing | Purpose | Subject Pattern | Personalization |
|---|---|---|---|---|
| 1 | 1 hour | Gentle reminder with cart contents | "You left something behind" | L2: exact products + images |
| 2 | 24 hours | Address likely objection + social proof | "Still thinking about [Product]?" | L2: product reviews, ratings |
| 3 | 72 hours | Incentive if available, scarcity if real | "[Product] is selling fast" | L2: stock level, discount code |

**Rules:** Max 3 emails. Show actual cart items with images. Include price. If they purchase → immediately exit. Never guilt. Incentive only on email 3, and only if margin allows.

---

### Re-Engagement

| # | Timing | Purpose | Subject Pattern | Personalization |
|---|---|---|---|---|
| 1 | Day 0 | Check-in | "Is everything okay, [Name]?" | L5: last activity date |
| 2 | Day 2–3 | Value reminder with specific history | "Remember when you [achieved X]?" | L2: past purchase/usage data |
| 3 | Day 5–7 | Incentive + interactive feedback | "We miss you — quick question" | L2: inactivity reason poll |
| 4 | Day 10–14 | Last chance — honest + direct | "Should we stop emailing you?" | L1: Name |

Email 4 = list hygiene. No response = suppress. Honest + direct — not guilt. Feedback poll in email 3 informs future re-engagement approach.

---

### Onboarding (Product Users)

Supports in-app flow. Email complements, not duplicates.

| # | Timing | Purpose | Personalization |
|---|---|---|---|
| 1 | Immediate | Confirm signup + single critical action | L1: Name; L2: plan selected |
| 2 | Day 1 | Nudge if step 1 incomplete | L2: setup completion status |
| 3 | Day 2–3 | Feature highlight with specific use case | L2: role/industry; L4: predicted use case |
| 4 | Day 4–5 | Customer success story matching their profile | L2: company size/industry match |
| 5 | Day 7 | Check-in + offer help + feedback poll | L2: feature usage data; poll |
| 6 | Day 10–12 | Advanced tip for engaged users | L2: features used; L4: next-best-action |
| 7 | Day 14+ | Upgrade/trial conversion with journey summary | L5: full activity summary |

**Behavioral branches:**
- Completed setup → skip email 2, advance to feature highlights
- Low engagement → send help-offer email earlier (Day 3), offer live demo
- Power user signals → skip to advanced tips, accelerate upgrade prompt

---

### Post-Purchase / Cross-Sell

| # | Timing | Purpose | Personalization |
|---|---|---|---|
| 1 | Immediate | Order confirmation + what to expect | L2: exact items ordered |
| 2 | Day 3–5 | Usage tips for purchased product | L2: product-specific tips |
| 3 | Day 7–10 | Request review / feedback | L2: product purchased; interactive rating |
| 4 | Day 14–21 | Cross-sell recommendations | L4: ML-driven product recs based on purchase history |
| 5 | Day 25–30 | Replenishment reminder (if applicable) | L2: product lifecycle data |
| 6 | Day 30+ | Loyalty program invitation or referral ask | L5: total purchase history + value tier |

---

### Billing Recovery (Failed Payment)

| # | Timing | Tone | Personalization |
|---|---|---|---|
| 1 | Day 0 | Friendly — card likely expired | L2: plan name, amount; countdown timer |
| 2 | Day 3 | Reminder — service at risk | L2: features they'll lose |
| 3 | Day 7 | Urgent — account suspending soon | L2: usage stats ("You've used X this month") |
| 4 | Day 10–14 | Final — what they'll lose, door stays open | L5: full account history |

Copy rule: assume accident, not intent. Single CTA → update payment link. No guilt. No threats.

---

### Trial Win-Back

| # | Timing | Focus | Personalization |
|---|---|---|---|
| 1 | Day 1 post-expiry | What they're missing | L2: features they used most |
| 2 | Day 7 | Gather feedback — interactive survey | L2: usage level; survey element |
| 3 | Day 14 | Incentive (discount/extended trial) | L4: predicted conversion likelihood → tiered offer |
| 4 | Day 30 | Final reach-out, door still open | L5: journey summary |

Segment by trial engagement:
- High engagement → remove friction to convert, highlight specific value gained
- Low engagement → offer fresh start + more onboarding + personal demo
- Zero engagement → ask what happened, offer demo/call, acknowledge the gap

---

### Milestone / Loyalty

| # | Trigger | Purpose | Personalization |
|---|---|---|---|
| 1 | Usage milestone (100th session, 1yr anniversary) | Celebrate + reflect on journey | L5: full stats + personal narrative |
| 2 | Loyalty tier upgrade | Announce new benefits | L2: tier change; new perks specific to them |
| 3 | Referral prompt | Ask to share (after positive milestone) | L5: specific results to share |

---

## Lifecycle Coverage Reference

Audit checklist — use to spot gaps in existing programs:

**Acquisition:** lead magnet delivery · content upgrade follow-up · webinar registration · free tool signup

**Onboarding:** new users series · new customers series · setup step reminders · invite sequence · first-value celebration

**Engagement:** feature adoption · usage tips · content newsletter · event invitations · community highlights · interactive feedback

**Retention:** upgrade to paid · upgrade tier · ask for review · proactive support · usage reports · NPS · referral program · milestone celebrations · loyalty rewards

**Revenue:** cross-sell · upsell · replenishment · abandoned cart · browse abandonment · price drop alerts

**Billing:** switch to annual · failed payment recovery · cancellation survey · renewal reminder · payment method expiring

**Win-Back:** expired trials · cancelled customers · dormant subscribers · lapsed purchasers

**Campaigns:** monthly newsletter · seasonal promotions · product update announcements · pricing change communications · exclusive previews

---

## Constraints

### MUST DO
- Confirm sequence type + goal before writing copy
- Define target segments before writing — never write for "everyone"
- Write sequence blueprint block (including behavioral triggers and personalization data) before any emails
- One purpose per email — no multi-job emails
- Include subject line + preview text for every email
- Use at least L2 (behavioral) personalization when data is available — never just `[First Name]`
- Write body copy in conversational active voice with value before ask
- Add behavioral branching rules to every sequence (engaged vs. non-engaged paths)
- Include segmentation options + A/B test recommendations + key metrics to every sequence output
- Specify mobile layout considerations per email
- Respect timing rules — behavioral triggers override time-based cadence
- Deliver full structured output block per email (number, purpose, timing, segment, subject, preview, personalization level, body, CTA, interactive element, conditions, mobile notes)
- Include visual/design direction notes for the design team
- Maintain consistent sending cadence — predictability builds trust

### MUST NOT DO
- Write multiple CTAs in one email — split into separate emails
- Skip the sequence blueprint or send without defining segments
- Use formal or corporate tone — conversational always
- Deliver emails without subject + preview text
- Recommend batch blasts when behavioral triggers are applicable
- Reference specific email platforms by name — keep output platform-agnostic
- Write past email 1 without knowing the sequence goal
- Use fake urgency or manufactured scarcity — only cite real constraints
- Personalize in ways that feel invasive — "We saw you at 2am" is surveillance, not personalization
- Send the same copy to all segments — differentiate or don't segment
- Stack multiple engagement tactics (urgency + scarcity + countdown + poll) in one email — pick one
- Ignore mobile rendering — if it doesn't work on a phone, it doesn't work

---

## Output Checklist

- [ ] Sequence type confirmed, goal stated
- [ ] Target segments defined with segmentation rationale
- [ ] Sequence blueprint block written (name, entry trigger, goal, segment, timing, behavioral branches, exit conditions, personalization data)
- [ ] Each email has: number, purpose, timing, segment, subject, preview, personalization level, body, CTA, interactive element (or none), conditions, mobile notes
- [ ] Behavioral branching defined (engaged vs. non-engaged paths per email)
- [ ] Copy follows hook → context → value → social proof → CTA → sign-off
- [ ] Subject lines: under 40 chars, personalized, specific
- [ ] Preview text: 40–90 chars, extends subject
- [ ] Hyper-personalization: L2+ personalization used where data available
- [ ] Interactive elements included where they add value (polls, quizzes, countdowns)
- [ ] Urgency/scarcity used only with real constraints
- [ ] Visual/storytelling direction notes included per email
- [ ] Mobile-first design notes included
- [ ] Segmentation options included
- [ ] A/B test recommendations with priority order included
- [ ] Key metrics listed with targets and action thresholds
- [ ] Sending cadence specified and justified

## Knowledge Reference

Email engagement, lifecycle marketing, customer communications, hyper-personalization, behavioral triggers, audience segmentation, RFM analysis, predictive personalization, dynamic content, merge tags, email automation, drip architecture, abandoned cart recovery, browse abandonment, post-purchase sequences, customer lifecycle, onboarding, retention, churn prevention, win-back campaigns, milestone marketing, loyalty programs, interactive email, AMP for email, polls, surveys, quizzes, countdown timers, gamification, mobile-first design, responsive email, dark mode email, email accessibility, WCAG, A/B testing, multivariate testing, statistical significance, email deliverability, sender reputation, SPF, DKIM, DMARC, inbox placement, spam filters, CAN-SPAM, GDPR, CASL, CCPA, subject line optimization, preview text, CTA design, storytelling, visual email design, urgency tactics, scarcity psychology, social proof, open rate, click-through rate, click-to-open rate, conversion rate, revenue per email, list hygiene, subscriber lifecycle, engagement scoring, send-time optimization, cadence management
