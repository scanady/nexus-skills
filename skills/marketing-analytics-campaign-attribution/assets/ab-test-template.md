# A/B Test Record: [Name]

Write sections 1 to 3 before the test starts. Do not edit them after.

## 1. Hypothesis

If we [change], then [metric] will [direction and size] for [audience], because [reason].

## 2. Design (fixed before launch)

| Item | Value |
|---|---|
| Primary metric | [one metric, one definition] |
| Guardrail metrics | [for example refund rate, unsubscribe rate] |
| Unit of randomization | [user / session / geo] |
| Baseline rate | [from own history] |
| Smallest effect worth acting on | |
| Sample per arm | [from a sizing calculation] |
| Planned run time | [full weekly cycles] |
| Stop rule | [fixed sample or date; no early stop on a good-looking number] |

## 3. Decision rule

Ship if [primary metric clears X and no guardrail breaks]. Otherwise [keep control / iterate].

## 4. Results (fill after the stop date)

| Arm | Entrants | Conversions | Rate | Interval |
|---|---|---|---|---|
| Control | | | | |
| Variant | | | | |

Difference: [absolute, relative] · Test and p-value or interval: [method used]

## 5. Validity checks

- [ ] Arms split as planned (no sample ratio mismatch)
- [ ] Ran full cycles, no launch or holiday distortion
- [ ] Tracking identical in both arms
- [ ] One primary metric. Other cuts labeled exploratory
- [ ] Guardrails reviewed

## 6. Decision and learning

Decision: [ship / hold / iterate]. Next test: [idea]. What we learned about the audience: [one sentence].

Sizing and significance work is out of scope for this skill's scripts. Use the `data-analysis-statistical-methods` skill.
