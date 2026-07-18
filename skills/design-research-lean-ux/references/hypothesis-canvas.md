# Hypothesis Canvas

The central planning artifact. It turns vague ideas into structured, testable predictions. Every initiative starts here, not in a wireframing tool.

## Hypothesis Format

> We believe **[outcome]** will happen if **[persona]** achieves **[action]** with **[feature]**.

| Component | Is | Example |
|-----------|-----|---------|
| Outcome | measurable business/user result | "+15% trial-to-paid conversion" |
| Persona | specific target segment | "first-time PMs on the free tier" |
| Action | expected behavior | "complete guided setup in session one" |
| Feature | the change that enables it | "3-step interactive setup wizard" |

Worked example: *"We believe 7-day retention will increase 25% if new users who sign up via the marketing site achieve their first data import within 10 minutes with an auto-mapping CSV import tool."*

## Assumption Prioritization

Surface assumptions first, then plot on **risk** (damage if wrong) × **uncertainty** (how little we know):

| | High uncertainty | Low uncertainty |
|--|------------------|-----------------|
| **High risk** | Test first — hypothesis + experiment now | Mitigate — safeguards, best practice |
| **Low risk** | Monitor — gather data passively | Ignore — proceed with confidence |

Workshop (45–60 min, PM + designer + tech lead + one stakeholder): generate assumptions on stickies (prompts: "our users are…", "this works because…", "we make money by…", "the biggest risk is…") → cluster → plot on the 2×2 → pick top 3 from Test-First → write as hypotheses with owner + target date.

## Business vs User Assumptions

Both need testing, with different experiments.

- **Business** — revenue model (pricing test), market size (ad response), cost (concierge cost tracking), channel (SEO test), competitive advantage (comparative test).
- **User** — who they are (interviews, analytics), what they need (usage data, diary study), current behavior (contextual inquiry), motivation (time-on-task comparison), barriers (funnel analysis).

Pair them: *business* "users will pay $29/mo" → *user* "users value the time saved enough to justify $29" → *hypothesis* with a measurable signal.

## Sub-Hypotheses

Decompose a big bet when it has multiple unknowns, needs too much to test whole, or the team disagrees on the riskiest part. Each sub-hypothesis isolates one variable (e.g. "users will engage with the flow" / "AI recs feel relevant" / "completers return at 2× the rate"), each with its own cheapest experiment. Decision after testing: all pass → build; some fail → redesign the failing part and retest; all fail → pivot.

## Tracking Log

Keep a living log — ID · hypothesis · status · experiment · metric · target · actual · decision (ship / iterate / pivot / kill). Review weekly (active experiments), at sprint boundary (validated/invalidated count — celebrate invalidations), quarterly (which assumption categories are most often wrong → adjust prioritization).

## Anti-Patterns
- Hypotheses written *after* building → retroactive justification; write them before any design work
- Vague outcomes ("improve UX") → use numeric targets
- Testing the safe assumption first → use the matrix; test high-risk/high-uncertainty first
- One giant quarterly hypothesis → decompose into 1–2 week sub-hypotheses
- No pre-set success criteria → define pass/fail before running
- Hypothesis authored solo → run the assumption workshop with the full team
