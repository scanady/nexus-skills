# Experimental Design Patterns

Patterns for testing hypotheses across domains. In a report, name only the key approach in the main text (e.g. "in vivo knockout" / "prospective cohort") and put full protocols — methods, controls, sample size, statistics, feasibility — in the experimental-design appendix.

## Choose the Design

- **Can you manipulate the variable?** Yes → experimental (RCT, lab). No → observational (cohort, case-control, cross-sectional).
- **What system?** cells/molecules → in vitro; whole organisms → in vivo; humans → clinical/observational; complex systems → computational.
- **Primary goal?** mechanism → gain/loss-of-function, dose-response; causation → RCT or well-controlled cohort; association → cross-sectional/case-control; prediction → modeling; temporal dynamics → time-course/longitudinal.
- **Constraints?** time-limited → cross-sectional/in vitro; budget-limited → computational/observational; ethics → observational/in vitro; rare outcome → case-control/meta-analysis.

## Laboratory

| Design | Purpose | Key elements |
|--------|---------|--------------|
| **Dose-response** | quantitative input→effect | negative + positive controls, 5–8 dose levels, ≥3 technical replicates, curve fit (IC50/EC50) |
| **Gain/loss of function** | causal role of a component | WT control, overexpression, knockout/knockdown, **rescue**, measure downstream effects |
| **Time-course** | temporal dynamics | t=0 baseline + early/intermediate/late points, replication per point |
| **Between-subjects (in vivo)** | compare treated groups | random assignment, power-based n, control (vehicle/sham), blinding, standardized conditions |
| **Within-subjects (repeated measures)** | subject as own control | baseline, counterbalancing, washout, repeated-measures stats |
| **Factorial** | multiple factors + interactions | e.g. 2×2 genotype×treatment; power for interaction terms |

## Computational

- **In silico simulation** — explicit model + assumptions, parameter sensitivity analysis, validation against known data, predictions for experimental test.
- **Bioinformatics / meta-analysis** — test on existing datasets; multiple-testing correction, independent-dataset validation, control confounds/batch effects, clear inclusion criteria.

## Observational

| Design | Strengths | Limits | Key elements |
|--------|-----------|--------|--------------|
| **Cross-sectional** | fast, cheap, prevalence | no temporality/causation | representative sampling, standardized measures, confound control |
| **Cohort (prospective)** | temporality, incidence | slow, costly, attrition | baseline exposure, defined follow-up, handle time-varying confounders |
| **Case-control** | efficient for rare outcomes | recall/selection bias | clear case definition, matched controls, retrospective exposure |

## Clinical Trials

- **RCT** (gold standard) — randomization (simple/block/stratified), allocation concealment, blinding, intention-to-treat, pre-registered protocol/analysis.
- **Crossover** — each participant gets all treatments in randomized order with adequate washout; fewer participants but watch order/carryover effects.

## Design Fundamentals

- **Controls** — negative (baseline), positive (validates system), vehicle, sham; avoid historical controls.
- **Blinding** — open-label / single / double / triple (strongest).
- **Replication** — technical (2–3, measurement error), biological (≥3, prefer 5–10, generalization), experimental (repeat whole study, gold standard for confirmation).
- **Confound control** — randomization, matching, blocking, statistical adjustment, standardization.
- **Power** — formal power analysis before running; aim ≥80% power; account for attrition; pilots ≥10/group.

## Triangulation

Strong testing combines designs (observational association → animal-model manipulation → in vitro mechanism → clinical trial → computational prediction). Convergent evidence across approaches strengthens causal claims; each design covers another's limitation.

## Common Pitfalls

Underpowered n · missing/inappropriate controls · unaccounted confounds · wrong statistical test · p-hacking / uncorrected multiple testing · no blinding on subjective measures · no replication · unregistered analysis plans.

## Applying to Hypotheses

Match design to the claim (causal → manipulation; association → observational). Start simple, then elaborate. Plan controls to isolate the specific effect. Balance ideal design against feasibility. Expect multiple experiments — one rarely settles a hypothesis. Pre-specify the analysis before collecting data. Build in validation (replication, orthogonal methods, convergent evidence).
