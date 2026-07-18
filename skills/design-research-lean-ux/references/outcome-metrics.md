# Outcome Metrics

Lean UX redefines success from "did we ship it?" to "did it change behavior?" This is the philosophical core.

## Outcomes vs Outputs

- **Output** — something produced (feature, design, release): "we shipped the new onboarding."
- **Outcome** — a measurable behavior change from it: "7-day retention rose 25% → 38%."

The **output trap**: optimizing velocity (stories/sprint, features/quarter) instead of impact. Symptoms — a long shipped list but flat engagement, "what did we ship?" instead of "what did we learn?", roadmaps counted in features. Shift the questions: "when will this be done?" → "when will we know if it works?"; "how many points?" → "how many hypotheses validated?"; "what's on the Q3 roadmap?" → "what behavior are we changing in Q3?"

## Leading vs Lagging

- **Leading** — predicts future results, moves fast, actionable (onboarding completion rate).
- **Lagging** — confirms past results, moves slowly, hard to influence directly (monthly revenue).

Every lagging metric has leading predictors — focus experiments on the leading one because it changes within the experiment's time box:

| Lagging | Leading |
|---------|---------|
| monthly revenue | trial-to-paid, activation rate |
| annual churn | weekly engagement, feature adoption |
| NPS | task completion, support ticket volume |
| LTV | feature breadth, upgrade completion |

## HEART Framework

Pick 1–2 categories per hypothesis:

| Category | Measures | Example metric |
|----------|----------|----------------|
| Happiness | satisfaction / perceived ease | NPS, CSAT, SUS |
| Engagement | depth/frequency | DAU/MAU, session length |
| Adoption | new-user / feature uptake | activation rate, first-use completion |
| Retention | continued use | D7/D30 retention, churn |
| Task success | complete core tasks | completion rate, time on task, errors |

Metric checklist before committing: measurable (do we instrument it?), attributable (to our experiment, not noise?), timely (within the time box?), actionable (changes what we do next?), leading (predicts, not just confirms?).

## OKRs

Key Results must be outcome-based. Bad: "ship the dashboard," "add 3 chart types." Good: "dashboard users find their top metric in <5s (from 18s)," "daily dashboard visits rise 40% → 65% of actives." Team-level learning OKR: validate 8+ hypotheses/quarter · user tests every sprint (0 missed) · 100% of shipped features reviewed post-launch within 2 weeks.

## Behavior-Change Levels

Awareness (saw it) → Trial (tried once) → Adoption (regular workflow) → Habit (automatic, unprompted). Track by cohort (users grouped by when they first met the change); if trial-to-habit drop-off shrinks across cohorts, iterations are working.

## Vanity Metrics

A metric is vanity if it only goes up, doesn't inform a decision, can't be tied to an action, or just looks good in a deck. Replace them:

| Vanity | Actionable alternative |
|--------|------------------------|
| total registered users | MAU |
| page views | engaged sessions |
| time on site | task completion + time on task |
| app downloads | D7 retention, activation |
| feature count | feature adoption rate |
| story points completed | hypotheses validated/sprint |
| NPS alone | NPS by cohort/segment + qualitative follow-up |

## Anti-Patterns
- Too many metrics → 1 primary per hypothesis, ≤3 OKR key results
- No baseline → establish before any experiment
- Post-hoc metric selection → pre-commit in the hypothesis
- Ignoring qualitative → pair every number with 3–5 interviews ("why")
- Dashboard but no action → weekly review with assigned action items
- Comparing averages → use cohorts and segment breakdowns
