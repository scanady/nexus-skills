# Measurement Log

Outcome metrics are not in any platform's analytics. They exist only if you write them down when they happen. Five minutes a week. Keep this file beside your positioning brief.

## Tier 1: outcomes (count by hand)

| Date | What happened | Source (post, comment, profile, referral) | Advances the objective? |
|---|---|---|---|
| | Someone started a conversation with you | | |
| | Someone cited a specific post in their first message | | |
| | Invitation: podcast, panel, guest piece, talk | | |
| | Introduction or referral offered unasked | | |
| | Qualified enquiry (named a budget, date, or scoped problem) | | |

Attribution is never clean. Write what the person said, not what you infer.

## Tier 2: behavior proxies (weekly)

| Week | Platform | Posts | Median comments per post | Comment share (comments / interactions) | Saves + shares per post | Note |
|---|---|---|---|---|---|---|
| | | | | | | |

A comment costs a reader time and a little exposure; a like costs a tap. Comment share is the cleanest cheap proxy for content landing with people who care.

## Tier 3: reach (monthly, large shifts only)

| Month | Platform | Posts | Median exposure | Median engagement rate | Followers | What changed |
|---|---|---|---|---|---|---|
| | | | | | | |

Make no weekly decisions from this table. Exposure counts get redefined, and the numbers are easy to move in ways that do not serve the objective.

## Experiment register

Fill the first four columns before the first post of a test. Fill the rest at the end.

| Hypothesis (can be wrong) | Variable | Falsified if | Planned posts per arm | Result | Decision |
|---|---|---|---|---|---|
| | | | | | |

## Quarterly review

Against the success criteria in your brief:

- [ ] Criterion 1: ______ met / not met
- [ ] Criterion 2: ______ met / not met
- [ ] Criterion 3: ______ met / not met

Then:
1. Which topic or format produced outcomes (Tier 1), not only engagement?
2. Did the experimental slot earn promotion, or should it be replaced?
3. Has the audience description grown vaguer? It drifts wider. Pull it back.

## Re-run the scripts

```
python3 scripts/profile_posts.py --input export.csv --output human
python3 scripts/test_patterns.py --input export.csv --attribute format --attribute topic --output human
```

Expect "nothing survived" most times. That is what honest analysis of a small sample looks like. It is a finding, not a reason to slice the data again.
