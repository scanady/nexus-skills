# Analysis Review Playbook

Load only the sections that match the artifact and its decision risks. A validation review is an attempt to falsify important claims, not a ritual pass through every possible check.

## Select Checks By Risk

| Signal | Raise review depth when | Useful response |
|---|---|---|
| Decision impact | Result drives money, policy, launch, staffing, or external communication | Recompute key metrics and reconcile to an independent source |
| Surprise | Magnitude or direction conflicts with history or domain expectations | Trace records and test alternate query paths |
| Method sensitivity | Result changes with population, period, model, or outlier treatment | Run explicit sensitivity checks |
| Causal language | Artifact claims an intervention caused an outcome | Review assignment, timing, confounding, and identification |
| Presentation exposure | Executives, customers, regulators, or the public will see it | Inspect final rendering and likely quick-reader interpretation |
| Reproducibility | Source logic or intermediate calculations are unavailable | Lower confidence and record a handoff blocker |

## Question And Method

### Framing

- Does the analysis answer the actual decision question?
- Is the outcome measured at the right level: user, account, order, event, day, or cohort?
- Are population, eligibility, exclusions, and sampling explicit?
- Do metric definitions match the stakeholder's operational definition?
- Are units, timezone, and cutoff rules consistent?
- Are comparison groups and periods genuinely comparable?

### Causal Claims

Treat language such as *caused*, *drove*, *impact*, *lift*, and *because of* as causal claims.

Look for:

- randomized assignment or a defensible quasi-experimental design
- pre-treatment group definitions
- comparable observation windows
- interference, attrition, and noncompliance
- concurrent launches, seasonality, and selection effects
- uncertainty intervals and multiple-testing controls where relevant

If identification is weak, preserve the observed association and remove the causal conclusion.

## Source And Data Integrity

### Freshness And Completeness

- Recover the source's `as of` date.
- Confirm expected date partitions and refresh completion.
- Compare observed coverage with expected populations, segments, and categories.
- Check whether late-arriving data or backfills affect the period.
- Distinguish a zero from missing, not yet reported, or not applicable.

### Filters And Populations

- Translate every filter into plain language.
- Identify who is removed by each filter and whether removal depends on the outcome.
- Check boundary operators, null behavior, timezone conversion, and status-history logic.
- Compare counts before and after high-impact filters.

### Joins

For each material join, record the intended relationship: one-to-one, many-to-one, or one-to-many.

Check:

1. left-side rows and distinct primary entities before the join
2. right-side key uniqueness at the intended grain
3. matched, unmatched, and multiplied rows after the join
4. whether inner joins silently remove relevant entities
5. whether slowly changing dimensions use the correct effective date

A matching final row count does not prove a join is correct; dropped and multiplied rows can offset each other.

## Calculations And Aggregations

### Recompute From Components

Prefer these independent checks:

- derive a rate from raw numerator and denominator
- reconcile a total to a trusted source maintained through a different path
- trace representative records through filters, joins, and output
- reverse engineer a headline total from component metrics
- rerun one boundary day, segment, or entity
- calculate a surprising claim through an alternate query path

### Calculation Checklist

- Grain matches the entity named in the claim.
- Distinct counts survive joins without duplication.
- Denominators represent the eligible population and are non-zero.
- Compared periods contain equal elapsed time or disclose partial periods.
- Group averages use raw totals or appropriate weights.
- Mutually exclusive parts reconcile to totals within rounding tolerance.
- Currency, quantity, rate, and time units remain consistent.
- Rounding occurs for presentation, not before aggregation.
- Timezones and daily cutoffs align across sources.

## High-Frequency Failure Patterns

### Join Explosion

**Signal:** totals inflate after enrichment or dimension joins.

**Test:** compare rows and distinct primary keys before and after; test right-side key uniqueness.

**Repair:** aggregate or deduplicate the right side to intended grain before joining. Do not use `DISTINCT` merely to hide unexplained multiplication.

### Survivorship Bias

**Signal:** analysis includes only entities still present today.

**Test:** ask which churned, deleted, failed, or otherwise absent entities cannot enter the extract.

**Repair:** reconstruct the historical eligible population or limit the claim explicitly.

### Partial-Period Comparison

**Signal:** current week, month, or quarter is compared with a complete prior period.

**Test:** compare elapsed days and source completion at the same cutoff.

**Repair:** use complete periods, align elapsed time, forecast with uncertainty, or expose the caveat prominently.

### Denominator Drift

**Signal:** conversion, retention, churn, attach, or activation rates move after eligibility changes.

**Test:** calculate cohort sizes and eligibility composition by period or segment.

**Repair:** hold the definition stable, restate history, or separate definition effects from behavior effects.

### Average Of Averages

**Signal:** segment averages are averaged equally despite different group sizes.

**Test:** compare the reported value with `sum(numerator) / sum(denominator)`.

**Repair:** aggregate components or weight each group by its valid observation count.

### Timezone Mismatch

**Signal:** daily totals disagree near boundaries or across systems.

**Test:** inspect timestamp storage, conversion order, daylight-saving behavior, and reporting cutoff.

**Repair:** standardize timestamps before date truncation and state the reporting timezone.

### Selection On Outcome

**Signal:** segments are defined using behavior that occurs after exposure or during the measured outcome window.

**Test:** reconstruct segment membership using only pre-treatment information.

**Repair:** use pre-treatment groups or describe the result without causal or predictive interpretation.

### Statistical Traps

Investigate when relevant:

- aggregate and segment trends point in opposite directions
- small samples produce unstable rates
- outliers dominate means
- many hypotheses are tested and only favorable results shown
- time windows were selected after seeing outcomes
- future information enters features, filters, or cohort labels
- uncertainty is omitted from noisy estimates

## Reasonableness Tests

Treat these as prompts for investigation, not automatic errors:

- large unexplained jumps or drops
- long flatlines in a normally variable metric
- exact round values in derived measures
- rates at 0% or 100%
- shares that do not approximately sum to 100%
- results that perfectly support the initial hypothesis
- missing or empty segments
- implausible scale relative to finance, operations, or product usage

Record the expected range or comparison source behind any reasonableness judgment.

## Visual Integrity

Review the final rendered artifact when possible.

- Use a chart type that matches the comparison.
- Start ordinary bars at zero; justify focused scales for variance or bridge charts.
- Keep scales consistent across comparison panels unless differences are explicit.
- Label axes, units, legends, date ranges, populations, and filters.
- Match category ordering to the comparison the reader should make.
- Avoid unexplained dual axes, 3D effects, truncated axes, and inconsistent intervals.
- Use precision appropriate to source uncertainty and sample size.
- Put caveats near the claims they qualify.
- Ensure titles state only findings supported by the plotted data.
- Check for clipped text, missing tables, stale placeholders, and broken rendering.

## Evidence And Confidence

### Evidence Strength

| Level | Meaning |
|---|---|
| Direct | Independently reproduced from authoritative source data or logic |
| Corroborated | Agrees with a genuinely separate trusted source or method |
| Traceable | Source and logic are visible but not independently reproduced |
| Asserted | Claim appears in the artifact without sufficient supporting evidence |
| Unavailable | Required artifact, access, execution, or confirmation is missing |

Do not call two dashboards independent if both consume the same derived table or semantic-layer metric.

### Confidence Factors

Raise confidence when high-impact claims are independently reproduced, definitions are stable, source lineage is clear, sensitivity checks agree, and final visuals preserve the evidence.

Lower confidence when access is incomplete, sources are stale or conflicting, calculations cannot be reproduced, methods are sensitive, samples are weak, or the narrative exceeds the evidence.

Confidence describes the strength of the validation, not how strongly the reviewer feels.