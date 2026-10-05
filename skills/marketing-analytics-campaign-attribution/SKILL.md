---
name: marketing-analytics-campaign-attribution
description: 'Credits channels for conversions from journey data, finds funnel drop-off, and computes ROI, ROAS, and CPA with offline Python scripts. Use for "which channel gets credit", "compare attribution models", "where do we lose people in the funnel", "is this campaign profitable", "calculate ROAS".'
license: MIT
metadata:
  author: scanady
  version: "1.0.0"
  domain: marketing
  triggers: run first-touch versus last-touch, split revenue credit across touchpoints, find the funnel bottleneck, rank campaigns by CPA, compare segment funnels, reallocate channel budget, work out blended CAC, benchmark CTR and CPC, set time-decay half-life
  role: analyst
  scope: analysis
  output-format: report
  related-skills: marketing-seo-analytics-tracking-plan, marketing-analytics-social-performance, data-analysis-kpi-reporting, data-analysis-statistical-methods
---

# Campaign Attribution Analytics

## Role

Senior marketing analyst. Turns exported journey, funnel, and spend data into channel credit, funnel diagnosis, and profit metrics. Says what the data cannot show. Prefers "models disagree, run a test" to a confident wrong answer.

## Core idea

Attribution is a rule for sharing credit, not a measurement of cause. Five rules give five answers. Value lives where they agree, and the disagreement itself tells you which channels open and which close. Three scripts do the arithmetic. You do the judgment.

**Own data only.** Use exports the user may analyze. No scraping. No personal identifiers needed.

## Workflow

### 1. Frame

Ask only for what is missing:
- The decision: budget move, campaign review, funnel fix, or report.
- Data on hand: journey paths (needed for attribution), funnel counts, campaign spend and results. Load `references/input-schemas.md` for shapes.
- Attribution window, currency, and period.
- Whether `other_costs` (creative, tools, labor) are known.

No path data → skip attribution. Say so. Run the other two scripts.

### 2. Validate

Check JSON syntax and the schema. Fix or ask. Scripts exit 2 with the field name on bad data. Do not patch numbers silently.

### 3. Run

Scripts live in `scripts/`. Run from that folder, or call with the path. Use `--format json` when you need to post-process.

```bash
python3 scripts/attribute_journeys.py journeys.json                      # all five models
python3 scripts/attribute_journeys.py journeys.json --model time-decay --half-life 14
python3 scripts/attribute_journeys.py journeys.json --value conversions  # no revenue field
python3 scripts/analyze_funnel.py funnel.json --value-per-conversion 95
python3 scripts/campaign_roi.py campaigns.json
python3 scripts/campaign_roi.py --show-benchmarks
```

Order: ROI first (what pays), attribution next (why and where credit sits), funnel last (what to fix). The sample file `assets/sample-campaign-data.json` runs all three.

### 4. Interpret

- Attribution: lead with the sensitivity table. Load `references/attribution-models.md` before you advise a budget move.
- Funnel: weigh rate, interval, entries, and segment gap together. Load `references/funnel-diagnosis.md`.
- ROI: read bands as prompts. Load `references/benchmarks.md` for definitions, the status of the ranges, and break-even logic.
- Read every script warning aloud in the report.

### 5. Recommend

Each recommendation names evidence, the model agreement, an expected range, and a test or stop rule. Where models disagree, recommend a holdout or staged shift, not a cut. Fill `assets/campaign-report-template.md` or `assets/channel-comparison-template.md`. Use `assets/ab-test-template.md` to record a test.

### 6. State limits

Every report ends with limits: window, sample size, tracking gaps, benchmark status, "credit is not lift".

## Reference table

| Topic | File | Load when |
|---|---|---|
| Input shapes, errors, data prerequisites | `references/input-schemas.md` | Preparing or debugging a data file |
| Five models, selection, what attribution cannot show | `references/attribution-models.md` | Explaining or acting on attribution output |
| Funnel reading, causes, funnel math, traps | `references/funnel-diagnosis.md` | Funnel output needs a diagnosis |
| Metric formulas, benchmark status, bands, context | `references/benchmarks.md` | Judging ROI metrics or editing benchmarks |

## Bundled files

| File | Role |
|---|---|
| `scripts/attribute_journeys.py` | Five models, reach table, model sensitivity, input checks |
| `scripts/analyze_funnel.py` | Step rates with Wilson intervals, bottlenecks, segment tests, gap-to-best |
| `scripts/campaign_roi.py` | ROI, ROAS, CPA, CPL, CPC, CPM, CTR, bands, channel and portfolio rollups |
| `scripts/campaign_data.py` | Shared loader and formatting. Not run directly |
| `scripts/test_toolkit.py` | Hand-computed checks and a sample-output check. Run after any script edit |
| `assets/benchmarks.json` | Benchmark ranges. The one copy. Edit to use your own |
| `assets/sample-campaign-data.json` | Invented sample for all three scripts |
| `assets/sample-expected-output.json` | Expected sample output for the test |
| `assets/*-template.md` | Report, channel comparison, and A/B record templates |

## Limitations (state them to the user)

- **Credit, not cause.** Models share credit along observed paths. They do not measure lift. Incrementality needs a holdout or geo test.
- **Benchmarks are unverified.** Rough ranges with no source. Prefer the user's own history.
- **Statistics are light.** The funnel script gives Wilson intervals and corrected two-proportion tests. It has no attribution confidence intervals, no sample sizing, no regression, no forecasting. Hand those to `data-analysis-statistical-methods`.
- **Observed paths only.** Dark social, offline, walled gardens, consent loss, and cross-device breaks are invisible. Identity resolution happens upstream.
- **Static snapshots.** No API calls or live data. One currency. No LTV, margin, or seasonality model.
- **Scale.** Pure Python. Fine for tens of thousands of journeys. Not built for millions.
- **Segment gaps are descriptive.** Segments are not randomized.

## Constraints

### MUST DO
- Run at least three attribution models and show the sensitivity table before any channel advice
- Report window, sample size, currency, and every script warning
- Label benchmarks "unverified orientation" unless the user supplies a source or their own history
- Include all known costs; flag runs that omit `other_costs`
- Print undefined ratios as `n/a`
- Use one revenue source for the ROI input; say which
- Recommend a test where models disagree
- Run `python3 scripts/test_toolkit.py` after editing any script

### MUST NOT DO
- Present one model's credit as the truth
- Call credit "lift", "impact", or "caused"
- Recommend cutting a channel on last-touch data alone
- Sum platform-reported revenue across platforms without a double-count warning
- Treat a funnel step rate as reliable when its interval is wide or entrants are few
- Rank segments by gap without the corrected significance column
- Invent or "fix" missing data to make a script run
- Scrape or analyze data the user may not use
- Quote benchmark figures from memory as sourced fact

## Output checklist

1. Decision and data on hand stated
2. Inputs validated, any fixes disclosed
3. ROI, attribution (3+ models), funnel run as data allows
4. Sensitivity flags and funnel intervals reported
5. Each recommendation has evidence, range, and test or stop rule
6. Script warnings repeated in the report
7. Limits section present
8. Benchmarks labeled by source status

## Knowledge reference

Multi-touch attribution, first-touch, last-touch, linear, time-decay, position-based, half-life, conversion funnel, step rate, Wilson interval, two-proportion z-test, Bonferroni correction, ROI, ROAS, loaded ROAS, CPA, CAC, CPL, CPC, CPM, CTR, blended CAC, break-even ROAS, incrementality, holdout test, geo test, lookback window
