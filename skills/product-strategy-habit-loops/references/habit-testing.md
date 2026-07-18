# Habit Testing

Measure whether the product is actually forming habits. The **5% rule**: a habit may be forming when at least 5% of users show unprompted, frequent usage.

## The Three Questions

**1. Who are the habitual users?** Users who engage frequently *without* external prompts. Define a target frequency, filter to it, isolate organic (non-notification) sessions, set a "habitual" threshold. Track DAU/MAU, organic session %, session frequency, return rate, streak length. Cohort by acquisition channel, demographics, onboarding completion, feature adoption.

**2. What are they doing?** Map the **Habit Path** — the sequence habitual users share — and contrast it with casual/churned users to find the **"aha moment"** that correlates with retention (Facebook: 7 friends in 10 days; Slack: 2,000 team messages; Dropbox: 1 file saved). Look for the first action, a key feature used early, a social action, an investment action, a time-of-day pattern.

**3. Why are they doing it?** Find the internal trigger. Interviews ("walk me through the last time you used it / what were you doing right before / how did you feel / what would you have done otherwise"), surveys (which emotion, which situation, how automatic 1–10), and behavioral data (time-of-day, context signals, trigger-to-action time).

## The 5% Test

Define "habitual" for your product type (social: daily, 5+ sessions; productivity: 3+/week unprompted; fitness: 4+ workouts/week), then:

```
Habitual Rate = Habitual Users / Active Users × 100
```

| Rate | Status |
|------|--------|
| <5% | habit not forming |
| 5–15% | emerging |
| 15–30% | strong |
| >30% | highly habitual |

Then analyze what makes the habitual cohort different (acquisition, first-session actions, first-week behavior, top features, investment made, social connections) and **replicate it** — steer onboarding toward those behaviors and test whether guided users form habits faster.

## Metrics & Leading Indicators

Core: habitual rate (>5%), DAU/MAU (>20%), organic session rate (rising), time-to-habit (falling), habit-path completion (rising). Track by signup cohort across weeks 1/4/12.

Early signals that predict habit formation: first-week return >3 visits, core action completed in the first session, an investment made in week 1, a social connection in month 1.

## When Habits Aren't Forming

| Symptom | Likely cause | Investigate |
|---------|--------------|-------------|
| low 5% rate | weak hook | audit each phase |
| churn after week 1 | weak first reward | onboarding experience |
| drop after month 1 | novelty gone | reward variability |
| return only with triggers | no internal trigger | user emotions |
| power users but low mainstream | too complex | simplify core action |

Phase-by-phase audit — **Trigger**: are external triggers effective (CTR/opens)? is there an internal trigger? right timing? **Action**: simple enough? friction points? enough motivation? **Reward**: variable? satisfies the internal trigger? meaningful (not just gamification)? **Investment**: are users putting something in? does it load the next trigger? are switching costs building?

## Testing Interventions

Identify the weakest phase from data → hypothesis → small A/B test with a clear metric → run to significance → ship the winner, iterate. Examples: move the investment prompt earlier (→ 30-day retention), tune trigger timing (→ trigger-to-action rate), raise reward variability (→ session frequency), reduce action steps (→ core-action completion).
