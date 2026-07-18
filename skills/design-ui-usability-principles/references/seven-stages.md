# The Seven Stages of Action

Every interaction — flipping a switch or completing a checkout — follows the same seven-stage cycle. Walking it lets you locate exactly where users get stuck. It splits into **execution** (stages 1–4, crossing the Gulf of Execution) and **evaluation** (stages 5–7, crossing the Gulf of Evaluation).

```
        1. GOAL  "what do I want?"
   EXECUTION              EVALUATION
   2. PLAN     "how?"     7. COMPARE  "is this what I wanted?"
   3. SPECIFY  "which?"   6. INTERPRET "what does it mean?"
   4. PERFORM  "do it"    5. PERCEIVE  "what happened?"
           └── THE SYSTEM ──┘
```

## The Stages, Failures, Fixes

| Stage | User asks | Gets stuck when | Fix with |
|-------|-----------|-----------------|----------|
| 1. Goal | what do I want? | goal vague / unsupported / forgotten mid-task | suggest goals, make capabilities visible, NL search, keep goal context |
| 2. Plan | how do I do it? | no obvious path / ambiguous options / needs unknown knowledge | clear signifiers, guided workflows, reduce choices, templates |
| 3. Specify | which control? | can't find/identify it, non-obvious sequence | consistent placement, clear labels, affordances, command palette |
| 4. Perform | is it working? | click doesn't register, hard/accidental, tedious | ≥44pt targets, device-appropriate input, spacing, bulk actions, undo |
| 5. Perceive | what happened? | no/subtle/too-fast/off-screen change | immediate + prominent feedback, sufficient duration, scroll-to-change |
| 6. Interpret | what does it mean? | ambiguous, jargon, misleading, too much at once | plain language, context, accurate status, single focus |
| 7. Compare | did I achieve the goal? | can't confirm, partial success, side effects, no reference | explicit confirmation, complete status, consequence preview, before/after |

## As an Evaluation Tool

For any task, attempt it as a new user and fill a row per stage: *question · current support · gap · severity (H/M/L) · proposed fix*. Then identify the weakest stage and whether the execution or evaluation side has more issues.

## Worked Examples

- **Flight booking** — goal/plan/specify/perform strong (autocomplete, date picker); *interpret* gap: "1 stop" doesn't say where/how long → show layover details; minor *compare* gap → add a "best value" tag.
- **Thermostat** — goal vague, *perform/interpret* fail via a wrong conceptual model (sets 85 expecting faster heat) → show current + target, a "Heating…" indicator, and estimated time; explain the rate is constant.
- **E-commerce checkout** — strong at every stage (prominent button, step indicator, logical field order, explicit order confirmation) — the most optimized seven-stage flow because conversion depends on it.

## Audit Worksheet

Rate each stage 1–5 (1 = users consistently fail, 5 = zero friction), note what works / what fails / priority fix. Summarize: weakest stage, which side has more issues, top-3 fixes by impact. Follow up: prototype the top fixes, test with 3–5 users think-aloud, re-score, and track task-completion-rate and time.
