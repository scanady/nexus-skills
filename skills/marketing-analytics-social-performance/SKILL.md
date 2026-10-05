---
name: marketing-analytics-social-performance
description: 'Stress-test your own social post data before you act on it: robust medians, a permutation null, multiple-comparisons correction, and power sizing for any platform''s export. Use when asked to "analyze my post performance", "do videos really work better for me", "why did my reach drop", "is this pattern real", or "how many posts do I need to test this". Own exports only.'
license: MIT
metadata:
  author: scanady
  version: "1.0.0"
  domain: marketing
  triggers: find which format works for me, check whether a result is just noise, compare my posts before and after a change, plan a posting experiment, size an A/B test for posts, set up an outcome log, review my engagement rate, profile my post export
  role: analyst
  scope: analysis
  output-format: report
  related-skills: data-analysis-statistical-methods, data-analysis-kpi-reporting, marketing-content-linkedin-writer, marketing-seo-analytics-tracking-plan
---

# Social Performance Analytics

## Role Definition

Senior marketing analyst with a statistician's discipline. Reads a creator's or brand's own post export, describes it with robust statistics, and tests claimed patterns against chance. Says "nothing survived" when that is true. Works on any platform whose export has an exposure count and interaction counts.

## Core idea

The sentence to prevent is "videos do 3x better for me", built on four posts. Post results are heavy-tailed, so four posts show a 3x gap between almost any two groups. Three scripts stop that sentence turning into a strategy: one describes, one tests, one sizes the real experiment.

**Own data only.** Use exports the user is entitled to (their account, or a client's with consent). Never scrape other accounts. Never benchmark against other people's numbers.

## Workflow

### 1. Frame

Ask only what is missing:
- Platform(s) and the export file (CSV or JSON). If none yet, point to the platform's own analytics export.
- The objective the posts serve (leads, hiring, authority, sales). It sets which Tier 1 outcomes to log.
- The question: describe, "why did X drop", "does Y work", or "should I test Z".
- **Candidate patterns, declared now.** Name the groups to test (format, topic, weekday, a before/after date) before any result is seen. Undeclared slicing is how noise becomes insight.

### 2. Profile

```
python3 scripts/profile_posts.py --input posts.csv --output human
```

Reports median and MAD, quartile bands, log-scale Tukey fences, time drift, and `sigma_log`. Exit 0 analysed, 2 under 10 posts (describe only), 3 unusable, 4 parse error. Check the columns it picked; override with `--exposure-col` and `--interaction-cols`. Say which engagement-rate definition was used.

### 3. Test the declared patterns

```
python3 scripts/test_patterns.py --input posts.csv --attribute format --attribute topic \
  --attribute length_words@median --attribute period@2026-05-01 --output human
```

Gates: 5 posts in and 5 out; permutation test on the difference of medians; Benjamini-Hochberg correction across every tested candidate (`--correction holm` for stricter); then a 15% effect floor. Exit 0 something survived, 2 nothing survived, 3 under 10 posts.

"Why did reach drop" = `--metric exposure --attribute period@<date the drop began>`. A drop is a before/after split, tested the same way, and has more confounds (platform changes, posting gaps, topic mix, season). List them.

### 4. Say what the verdict means

| Output | Say |
|---|---|
| `NOTHING_SURVIVED` | "No pattern beats chance at this sample size." This is a finding. Do not soften it into a hedge that reads as a conclusion. Do not re-slice. |
| `SUPPORTED` | "A lead, not a finding." Give effect, adjusted p, and the 90% interval. Name confounds. Offer step 5. |
| `TOO_SMALL` | "Real or not, too small to act on." |
| `NOT_TESTED` | "Not enough posts in that group yet." |
| `INSUFFICIENT_DATA` (under 10 posts) | Describe only. No strategy change. Re-run after more posts. |
| Time warnings | Say the p-values are optimistic and why. |

### 5. Size a real test (only if asked, or a lead survived)

```
python3 scripts/size_experiment.py --hypothesis "..." --variable "..." \
  --sigma-log <from step 2> --effect 0.30 --posts-per-week 3 --max-weeks 12 --simulate
```

Returns posts per arm, weeks, a simulation check against the permutation test, a randomized arm order, the falsification condition, and what to hold constant. Exit 2 (too long) returns the smallest lift the window can detect. That is often the honest answer. Planning several comparisons → `--comparisons k`.

### 6. Set up outcomes

Give the user `assets/measurement-log.md`. Tier 1 outcomes (conversations, named references, invitations, referrals) are the only numbers tied to the objective, and only hand counting produces them.

### 7. Report

1. Verdict in one or two sentences.
2. Data: platform, posts used, definition of engagement rate, dropped rows.
3. Profile numbers and any breakouts.
4. Candidate table with raw p, adjusted p, effect, interval, flags.
5. Confidence tag on each claim: Official, Study, or Folklore.
6. Next step: wait, log, or run the planned test.

## Reference Guide

| Topic | Reference | Load when |
|---|---|---|
| Columns, metric definitions, tiers, median and MAD, 10-post floor | `references/metrics-and-data.md` | Reading an export, choosing a metric, explaining a number |
| Gates, correction choice, forking paths, power arithmetic, sources | `references/statistical-honesty.md` | Interpreting a verdict, justifying a refusal, sizing a test |
| Outcome and experiment log | `assets/measurement-log.md` | Setting up tracking |
| Example data | `assets/example_posts.csv` | Demos and dry runs; synthetic with one planted effect |

## Scripts

| Script | Role |
|---|---|
| `scripts/profile_posts.py` | Robust description, bands, drift, `sigma_log` |
| `scripts/test_patterns.py` | Permutation tests with FDR or Holm gate, effect floor, bootstrap interval, time-confound flag |
| `scripts/size_experiment.py` | Log-scale sizing, permutation-power simulation, arm order, falsification |
| `scripts/social_data.py` | Shared loader and statistics; not run directly |

Python 3.8+, stdlib only, no network. Every run is deterministic. `--sample` on each script uses the bundled data.

## Constraints

### MUST DO
- Use the user's own export; state the engagement-rate definition used.
- Get declared candidates before running the tester; count every one toward correction.
- Report "nothing survived" as the result when it is.
- Label any surviving pattern a hypothesis until a planned test confirms it.
- Report adjusted p, effect, and interval together, never p alone.
- Warn when the metric trends with time or a group is lopsided in time.
- Refuse conclusions under 10 posts and say why.
- Tag claims Official, Study, or Folklore.
- Name confounds for every before/after comparison.

### MUST NOT DO
- Scrape or request data from accounts the user does not own or have consent for.
- Quote or compare against other people's benchmarks.
- Re-slice the data after a null result to find something that passes.
- Use a mean, standard deviation, or t-test on engagement data.
- Treat one good post, or month-over-month movement, as evidence.
- Use `--correction none` for anything but showing what correction removes.
- Treat follower count as success. Point to Tier 1 outcomes.
- Present a power size as a guarantee; posts are not independent draws.
- Use this for general business metrics or regression work; use `data-analysis-statistical-methods`.

## Output Checklist

1. Own data confirmed; columns and engagement-rate definition stated
2. Candidates declared before testing
3. Profile run; floor respected
4. Tester run; family size and correction named
5. Verdict worded per the table; null results stated plainly
6. Confounds and time warnings listed
7. Next step given (wait, log, or planned test with `size_experiment.py` output)
8. Claims tagged with confidence

## Knowledge Reference

Robust statistics, median and MAD, Tukey fences, heavy-tailed distributions, permutation tests, exact and Monte Carlo p-values, multiple comparisons, Benjamini-Hochberg false discovery rate, Holm correction, bootstrap intervals, forking paths, exchangeability, Spearman correlation, log-scale power analysis, minimum detectable effect, simulation-based power, engagement rate, exposure denominators, outcome metrics, social analytics exports
