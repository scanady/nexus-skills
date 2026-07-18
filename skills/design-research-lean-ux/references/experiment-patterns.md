# Experiment Patterns

The right experiment answers the hypothesis with the least effort. Start at the lowest fidelity that can answer the question; climb only when lower fidelity can't give the confidence you need.

## The Fidelity Ladder

```
Paper prototype → Clickable prototype → Concierge MVP / Wizard of Oz → Landing-page smoke test → Coded A/B test → Production
```

| Experiment | What it is | Effort | Confidence | Answers |
|------------|-----------|--------|------------|---------|
| **Paper prototype** | hand-drawn screens, facilitator plays computer | very low (30 min) | low–med | does the flow/concept make sense? |
| **Clickable prototype** | Figma/etc, no backend | med (1–3 days) | med–high | can users complete the task? |
| **Concierge MVP** | deliver the service manually, person-to-person | med (ongoing) | high | does the solution actually solve it? |
| **Wizard of Oz** | real-looking frontend, humans do the "automation" | med | high | will the automated feature feel right? |
| **Landing-page smoke test** | page for a non-existent product + CTA | low (½ day) | med | does anyone want this? |
| **A/B test** | live variants, statistical comparison | high | very high | which version performs better? |

Each has a "when NOT to use": don't clickable-prototype what paper answers; don't A/B a brand-new concept (prototype first); don't smoke-test what you already know is wanted (test usability instead).

## Selection Matrix

| Need to learn | Experiment | Time | Participants |
|---------------|-----------|------|-------------|
| Does anyone want this? | landing-page smoke test | 1–2 days | 200+ visitors |
| Does the flow make sense? | paper prototype | 1 day | 5 users |
| Can users complete the task? | clickable prototype | 3–5 days | 5–8 users |
| Does the solution work / feel right? | concierge / Wizard of Oz | 1–2 weeks | 5–10 users |
| Which design wins? | A/B test | 2–4 weeks | 1,000+ per variant |
| What do users need? | interview | 1 day | 5–8 users |
| How do users organize info? | card sort | 3 hrs | 10–15 users |

## The 5-User Rule

~5 users surface ~85% of usability problems. Use 5 for qualitative tests, 20+ for surveys/preference tests, 1,000+ per variant for statistically significant A/B. Don't over-recruit qualitative tests — five, tested fast, beat fifty tested slowly.

## Experiment Design Template

For every experiment: hypothesis ID · type · audience (persona, sample size, recruitment) · design (what to build, what the participant does, what to measure) · **success criteria pre-set** (primary metric, pass threshold, fail threshold) · time box (build/run/analysis) · results (metric, qualitative notes, surprises, decision: validate / iterate / pivot / kill).

## Minimum Viable Test

The simplest experiment that answers one question — learn *before* you build, not test what you already built. Examples: "do people get our value prop?" → show a landing page to 5 people, have them explain it back (2 hrs); "will users pay?" → pricing page + "buy" → waitlist (1 day); "faster than current?" → time-on-task, 5 old vs 5 new (1 day).

## Cadence & Pitfalls

Mature teams run a weekly loop: Mon review + write hypotheses/design experiment · Tue build artifact · Wed recruit · Thu run sessions · Fri synthesize + update log. Remote: moderated tools (Zoom/Lookback) keep depth; unmoderated (Maze) scale; record with consent.

Common failures: leading questions ("would you click here?" → "what would you do next?"), confirmation bias (assign a devil's advocate; read raw data first), too few participants, no success criteria, testing too late (test early/low-fidelity), wrong audience (real users, not colleagues).
