# Calculator Guide

`scripts/cohort_calculator.py`. Python 3.8+, standard library only. Run from the skill folder or give the full path.

## Commands

```bash
# Pooled retention curve, weekly grain
python3 scripts/cohort_calculator.py curve events.csv --grain week

# Cohort x age matrix, monthly, unbounded retention
python3 scripts/cohort_calculator.py matrix events.csv --grain month --unbounded

# Curve shape and cohort trend labels, JSON out
python3 scripts/cohort_calculator.py shape events.csv --format json

# Strict ordered funnel with time window
python3 scripts/cohort_calculator.py funnel steps.csv \
  --stages visit,signup,activate,pay --time-column ts --window-days 7
```

## Options

| Option | Commands | Default | Note |
|---|---|---|---|
| `--grain day\|week\|month` | curve, matrix, shape | week | Weeks start Monday |
| `--max-period N` | curve, matrix, shape | 30 day, 12 week, 12 month | Last age reported |
| `--unbounded` | curve, matrix, shape | off | Retained at N if active at N or later |
| `--as-of YYYY-MM-DD` | curve, matrix, shape | latest activity date | Set to the true data cutoff |
| `--user-column`, `--cohort-column`, `--activity-column` | cohort commands | `user_id`, `cohort_date`, `activity_date` | Rename to fit the file |
| `--min-users N` | shape | 30 | Ignore ages and cohorts below this size |
| `--flat-tol X` | shape | 0.005 | Tail slope per period treated as flat |
| `--floor X` | shape | 0.05 | Tail level treated as near zero |
| `--compare-age N` | shape | 7 day, 4 week, 4 month | Age for the cohort trend. Falls back to a lower age until 3 cohorts are mature |
| `--trend-tol X` | shape | 0.02 | Newer minus older mean treated as real |
| `--stages a,b,c` | funnel | required | Ordered steps |
| `--time-column`, `--window-days` | funnel | off | Step order and deadline checks |
| `--loose` | funnel | off | Skip order checks. Audit use only |
| `--format text\|json` | all | text | |

## What the output means

- **Mature cells only.** A cell shows a rate only when its whole period ended on or before `--as-of`. A `-` is an unfinished period, not zero.
- **Pooled curve denominators** add only the cohorts that reached each age, so rates are not diluted by young cohorts.
- **Shape labels:** `plateau`, `slow-decline`, `decays-to-zero`, `near-zero-floor`, `recovering`, `insufficient-data`.
- **Trend labels:** `improving`, `worsening`, `flat`, `insufficient-cohorts`.
- The pooled tail comes only from older cohorts. Check the matrix before trusting a tail label.

## Limits

- Activity grain is the calendar date. Time of day is ignored in cohort commands.
- Cohort sizes count users present in the file. Users with no rows are invisible. Include the anchor event as a row.
- Labels are thresholds on rates, not statistical tests. For significance on a cohort difference, hand off to a statistics skill.
- Errors go to stderr with exit code 1. Fix the named column or date and re-run.

## Verify before trusting

1. Run `matrix` and check each cohort size against a known signup count.
2. Check that `p0` is near 100%. A low `p0` means anchor rows are missing.
3. Spot-check one cell by hand from the raw file.
