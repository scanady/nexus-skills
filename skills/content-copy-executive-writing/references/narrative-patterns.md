# Narrative Patterns

The nine narrative patterns are matched to communication objectives. Use this reference to understand the full structure of each pattern, the critical elements that cannot be omitted, the common failure modes, and a usable skeleton.

The patterns are ordered roughly by how frequently technical leaders encounter them.

## 1. Decision Request

**Objective:** Get the reader to approve, reject, or modify a recommendation.

**Structure:**
1. Recommendation, in one sentence
2. Problem or opportunity the recommendation addresses
3. Alternatives considered and why rejected
4. Risks and mitigations
5. The specific ask (approve, fund, sign, delegate, escalate further)

**Critical elements:**
- The recommendation comes first because the executive's first question is "what are you asking me to approve." Burying the recommendation forces them to read defensively, looking for the ask.
- Alternatives come before risks because executives want to know you considered the obvious objections before they raise them. Skipping alternatives signals that the author has not stress-tested the recommendation.
- The ask must be specific. "Your thoughts welcome" is not an ask. "I am asking for approval to commit $400K from the platform reserve, with a decision by Friday so we can start onboarding Monday" is an ask.

**Common failure mode:** Background-first structure where the recommendation appears in the final paragraph. The executive has formed a defensive posture by the time they reach it.

**Skeleton:**

```
I recommend [decision] to [outcome].

[Two to four sentences on the problem this addresses and why it needs a decision now.]

I considered [alternative A] and [alternative B]. I rejected A because [reason]. B remains viable but [reason for preferring the recommendation].

The primary risks are [risk] and [risk]. We will mitigate by [mitigation].

I am asking for [specific approval / signature / funding / direction] by [date] so we can [next action].
```

## 2. Change Announcement

**Objective:** Get the reader to accept and adopt a change being introduced.

**Structure:**
1. Why this matters now (the urgency or driver)
2. What is changing (specifically and concretely)
3. What stays the same
4. What this means for you specifically (the reader)
5. What we are asking of you
6. Where to get help

**Critical elements:**
- The "why now" is non-negotiable. Change without urgency reads as arbitrary. If the why now is not compelling, the change is at risk regardless of how well-designed it is.
- "What stays the same" is the most-skipped element and the one that most reduces resistance. People over-estimate the scope of change and under-estimate continuity. Name the continuity explicitly.
- "What this means for you specifically" must address the reader's actual situation, not generic impact. If the audience is mixed, segment.
- The ask should be a concrete behavior change, not a feeling. "Accept the change" is not a behavior. "Complete the migration questionnaire by November 15" is.

**Common failure mode:** Leading with what is changing, before establishing why. The reader reads the entire announcement looking for justification and concludes it does not exist.

**Skeleton:**

```
[Why this is happening now. The driver: regulatory, competitive, financial, operational. One or two paragraphs of stakes.]

Starting [date], [the specific change].

[What is not changing: roles, reporting lines, tools, processes that people might assume are at risk.]

What this means for you: [segmented impact if needed].

We are asking you to [specific behavior or action] by [date].

For questions, [channel]. For support, [resource].
```

## 3. Status Update

**Objective:** The reader understands current state, what changed, and where their attention is needed.

**Structure:**
1. Headline assertion (on track / at risk / off track) with a one-sentence rationale
2. Progress against commitments
3. What changed since the last update
4. Risks and what is being done about them
5. Asks (decisions needed, blockers requiring escalation)

**Critical elements:**
- The headline carries the assertion. A scanner should get the answer in three seconds. If the headline is "Q4 platform migration: on track for January cutover, with two risks we are managing," the rest of the update fills in detail for those who want it.
- "What changed since last update" is what makes a recurring update worth reading. Without deltas, the update becomes furniture.
- Asks belong at the end where the reader's attention is highest, having read the context. Do not bury them under "additional notes."

**Common failure mode:** A wall of accomplishments with no headline assertion and no asks. The reader cannot tell from a glance whether the project needs their attention.

**Skeleton:**

```
**Headline:** [On track / At risk / Off track]. [One sentence rationale.]

**Progress:**
[Two to four bullets of substantive progress against named commitments.]

**Deltas since last update:**
[What changed that the reader needs to know about.]

**Risks:**
[Risk, what we are doing about it, when we will know more.]

**Asks:**
[Specific decisions, escalations, or unblocks needed. Name the owner expected to act.]
```

## 4. Escalation

**Objective:** Get the reader to intervene to unblock a problem.

**Structure:**
1. What is broken (plainly)
2. Business impact (in their terms)
3. What you have already tried
4. What you need from the executive specifically
5. By when

**Critical elements:**
- "What you have already tried" is what separates an escalation from a complaint. Skipping it suggests you have not done the work, which damages credibility and makes the executive less likely to act.
- The ask must be specific to the executive. "Help" is not an ask. "I need you to call the GM at the vendor and request a named technical resource by Wednesday" is an ask.
- The "by when" must be tied to a concrete consequence. "Soon" gives the executive permission to delay. "Before the November 15 milestone or we slip three weeks" creates the right urgency.

**Common failure mode:** A long history of what went wrong before the actual problem statement and the actual ask. The executive cannot tell what is being asked of them.

**Skeleton:**

```
[Problem in one or two sentences. What is blocked.]

**Business impact:** [In dollars, time, regulatory exposure, or customer experience. Quantify where possible.]

**What we have tried:** [Two to four sentences. Show the work.]

**What I need from you:** [Specific action only the executive can take.]

**By when:** [Date, tied to a consequence.]
```

## 5. Technical Explanation for Non-Technical Audience

**Objective:** The reader understands a technical topic at the level needed to act on or judge it.

**Structure:**
1. The business outcome or problem the technology addresses
2. An analogy or framing the audience already understands
3. How it works at the level they need (not the level you can explain)
4. What it means for the decision or judgment in front of them
5. The scope of their cognitive responsibility (what they do not need to worry about)

**Critical elements:**
- The closing element is the one most often skipped and most often valued. Executives want to know the scope of what they own. "You do not need to evaluate whether the encryption is correct; that is owned by the security team and has been reviewed by external audit" frees them to focus on what they do own.
- The analogy should be domain-appropriate. A medical analogy lands differently with a CFO than with a clinical executive. Choose the audience's domain, not yours.
- The "how it works" section is where most technical leaders over-explain. The right level is the minimum needed to support the decision or judgment being asked of them.

**Common failure mode:** Starting with how the technology works, because that is what the author finds interesting. The reader does not know why they should care.

**Skeleton:**

```
[The business outcome or problem in one paragraph. Why this matters to you.]

[An analogy from the audience's domain that frames the rest.]

Here is how it works at the level you need: [two to four short paragraphs, not a technical deep dive].

What this means for [the decision or judgment in front of them]: [the connection back to the action].

What you do not need to evaluate: [the scope of their cognitive responsibility, with the owner of the rest named].
```

## 6. Strategic Narrative or Vision

**Objective:** The reader accepts a future direction worth investing in.

**Structure:**
1. Current state and why it is insufficient
2. Future state and why it is worth the cost
3. The gap between them
4. The path across the gap
5. The first move

**Critical elements:**
- This is the only pattern where stakes precede recommendation. The reader must accept that the current state is insufficient before they will engage with a proposed future. Leading with the future state assumes a commitment to change that has not yet been earned.
- The first move must be concrete and proximate. Vision without a first move is aspiration. The first move is what makes the vision actionable.
- The gap analysis is where this pattern fails most often. Authors describe current and future state without honestly characterizing the distance between them, which makes the path feel arbitrary.

**Common failure mode:** Future state painted in inspirational language, with no honest reckoning with what it takes to get there. The reader senses the hand-wave and disengages.

**Skeleton:**

```
[Current state in one or two paragraphs. Concrete. What we have, where it is breaking down, what it is costing us.]

[Future state. What the world looks like when this is done. Concrete enough that the reader can picture it.]

[The gap. Honestly characterized. Capability gaps, capacity gaps, capital gaps, organizational gaps.]

[The path. Phased if needed. Sequenced decisions, not a Gantt chart.]

[The first move. What we do in the next thirty days. What we need from you to make it possible.]
```

## 7. Incident or Post-Mortem

**Objective:** The reader understands what happened and trusts the response.

**Structure:**
1. What happened in plain language
2. Impact in business terms
3. Root cause
4. What we did to resolve
5. What we are doing to prevent recurrence
6. What we learned

**Critical elements:**
- Resist the urge to lead with root cause. Executives want to know the impact before the mechanism. Root cause is interesting; impact is what they need to assess.
- "What we learned" is distinct from "what we did to prevent recurrence." The former is reflective and may include things that cannot be engineered away. The latter is concrete. Both belong.
- The tone matters. Defensive post-mortems erode trust. Honest post-mortems build it. Do not hedge the root cause to soften blame; name it cleanly and name the response cleanly.

**Common failure mode:** A timeline-driven structure that walks through the incident chronologically before naming the impact. The executive reads three paragraphs of "at 2:47 AM the on-call engineer was paged" before learning that customers lost service for six hours.

**Skeleton:**

```
On [date], [plain-language description of what happened]. The incident lasted [duration] and was resolved at [time].

**Impact:** [Business terms. Customer impact, financial impact, regulatory exposure, reputational exposure. Numbers where available.]

**Root cause:** [Plainly named, no hedging.]

**Resolution:** [What we did. Sequence if relevant.]

**Prevention:** [Specific actions, owners, dates.]

**Lessons:** [Reflective. What this revealed about our systems, our processes, or our assumptions.]
```

## 8. Reassurance or Risk Response

**Objective:** The reader remains confident in the face of a concern.

**Structure:**
1. Acknowledge the concern directly
2. State the current reality
3. Evidence
4. What we are doing about it
5. What would change our approach

**Critical elements:**
- Hedging or evasion in this pattern destroys trust faster than bad news. If the concern is legitimate and the situation is concerning, say so. Reassurance built on minimization is a confidence trap.
- "What would change our approach" signals that the response is not defensive. It says we have thought about the conditions under which our current path is wrong, and we will act when we see them. This element is rarely included and is the most credibility-building piece of the pattern.
- Evidence should be specific and verifiable, not directional. "Our metrics are strong" is not evidence. "Tier-1 latency has been under 80ms p99 for the last 30 days; here is the dashboard" is evidence.

**Common failure mode:** Reassurance that sounds like a press release. The reader can feel the spin and trusts the author less than they did before reading.

**Skeleton:**

```
You raised concern about [the concern]. That is the right question to be asking.

[Current reality, plainly stated. No spin.]

The evidence: [specific, verifiable. Numbers, observations, third-party confirmations.]

What we are doing: [concrete actions, owners, dates.]

What would change our approach: [the conditions under which our current path is wrong, and what we would do if we saw them.]
```

## 9. Capability or Roadmap Brief

**Objective:** The reader understands what a team or platform does, why it exists, and where it is going.

**Structure:**
1. What this team or platform does (in one sentence)
2. Why it exists (the business problem or opportunity)
3. Current state (what we deliver today, scale, scope)
4. Where we are going (the roadmap, not the backlog)
5. What we need (investment, decisions, alignment, support)

**Critical elements:**
- The one-sentence definition is harder than it looks and is the most important sentence in the brief. If it requires a paragraph, the team's purpose is unclear and the rest of the brief will not save it. Write it last if needed.
- "Where we are going" is a roadmap, not a backlog. The audience does not need the Jira items; they need the three to five strategic moves and the order. Backlog detail signals that the author does not know what matters.
- "What we need" should be specific. "Continued support" is not an ask. "A decision on the platform consolidation question by Q1, headcount for two senior engineers in the FY26 plan, and sponsorship for the regulatory review we have requested twice" is an ask.

**Common failure mode:** A capability inventory presented as accomplishment, with no strategic direction and no ask. The reader leaves the briefing impressed by the work and unsure what they were supposed to do with the information.

**Skeleton:**

```
[Team or platform name] is the [one-sentence definition].

**Why we exist:** [The business problem or opportunity. Why this function is structured the way it is.]

**Current state:** [What we deliver, at what scale, for whom. Numbers where they convey scope.]

**Where we are going:** [The three to five strategic moves, sequenced. Not the backlog.]

**What we need:** [Specific asks. Decisions, investment, alignment, support.]
```
