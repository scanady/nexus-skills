# Quality And Pattern Signals

How to read profile statistics. Each signal below is a hypothesis with a measurement attached, not a verdict — a flag means "look here", and several common flags have innocent explanations listed alongside them.

## Completeness

Grade each column by non-null rate, then explain the nulls rather than only counting them:

| Band | Non-null | Reading |
|---|---|---|
| Complete | > 99% | Usable as-is |
| Mostly complete | 95–99% | Find out who the missing rows are |
| Incomplete | 80–95% | Usable with a stated caveat; check whether missingness correlates with the outcome |
| Sparse | < 80% | Not usable without imputation or a narrowed population |

Nulls are only random until proven otherwise. Cross-tabulate the null indicator against a date column and a key dimension: nulls concentrated before a cutoff date mean the column was added later; nulls concentrated in one segment mean the column does not apply to that population. Both change how the column can be used, and neither shows up in the overall rate.

Distinguish the three states a missing value can carry — null, empty string, and a sentinel like `"unknown"` — since a column using all three usually has more than one write path.

## Consistency

**Value format drift.** One concept spelled several ways: `"USA"`, `"US"`, `"United States"`, `"us"`. Measure it as `COUNT(DISTINCT col)` versus `COUNT(DISTINCT LOWER(TRIM(col)))`, and by inspecting the rare tail. Any grouped analysis on the column splits categories until it is resolved.

**Type drift.** Numbers stored as strings, dates in mixed formats, booleans as `"Y"`/`"1"`/`"true"`. Detect by pattern collapse on the string values. A numeric column stored as text also sorts wrong — `"10" < "9"`.

**Referential breaks.** Foreign keys with no parent row. Measure the orphan rate; anything above a fraction of a percent means the join in a downstream analysis will drop rows silently.

**Business rule violations.** Negative quantities, end date before start date, percentage above 100, a lifetime total below its most recent month. Write each rule as a boolean and count violations.

**Cross-column contradiction.** `status = 'completed'` with a null `completed_at`; a churn date on an active account. These usually mark either a broken write path or a status field that changed meaning mid-history.

## Accuracy Red Flags

Each of these is a suspicion that needs an owner's confirmation before being reported as an error:

- **Placeholder values** — `0`, `-1`, `999999`, `"N/A"`, `"TBD"`, `"test"`, `"xxx"`, `1970-01-01`, `9999-12-31`. They masquerade as real values and quietly wreck averages.
- **Default-value spikes** — one value at improbable frequency, often a form default or a backfill constant.
- **Impossible ranges** — ages above 150, negative durations, dates before the company existed, far-future timestamps.
- **Round-number bias** — values clustering on multiples of 5 or 10 suggests estimates entered by hand, not measurements.
- **Truncation at a boundary** — a hard pile-up at exactly the max length or a round ceiling means values were cut, not distributed that way.
- **Stale updates** — `updated_at` with no recent movement in a system that should be active.

Innocent explanations exist for most of them: a `0` can be a genuine zero, a spike can be a dominant real category, round numbers can be contract-priced. Report the measurement and the hypothesis, and name who could confirm it.

## Timeliness

- When was the table last written, and does that match its expected refresh cadence?
- Is the most recent period complete, or still filling? A partial current day makes every trend look like a collapse.
- What is the lag between event time and load time, and does the table expose both?
- Do late-arriving rows or backfills rewrite history after the fact?
- Are there gaps in the time series, and do they align with known incidents or deploys?

## Distribution Shapes

Characterize each metric before anyone averages it:

| Shape | Signature | Consequence |
|---|---|---|
| Normal | Mean ≈ median, symmetric | Mean and standard deviation are meaningful |
| Right-skewed | Mean > median, long high tail | Report median and percentiles; common for revenue and duration |
| Left-skewed | Mean < median, long low tail | Rarer; often a ceiling effect |
| Bimodal | Two peaks | Two populations mixed; split before summarizing |
| Power law | Few enormous values, many tiny | Averages are meaningless; use percentiles and rank |
| Uniform | Flat across the range | Suspect synthetic, random, or evenly bucketed data |
| Spiked | One value dominating an otherwise smooth range | Default or placeholder contamination |

Say which shape a metric has in the profile. It determines whether every downstream summary should use a mean or a median.

## Temporal Patterns

- **Trend** — sustained direction over the full span.
- **Seasonality** — repeating weekly, monthly, quarterly, or annual cycles.
- **Day-of-week effect** — weekday versus weekend levels, which makes any 7-day-misaligned comparison unreliable.
- **Holiday effect** — spikes or drops around known dates.
- **Change points** — sudden level shifts; these more often mean a pipeline or instrumentation change than a business event, so check deploy timing before concluding otherwise.
- **Anomalies** — isolated points breaking the pattern.
- **Edge artifacts** — first and last periods that are partial, which look like a ramp and a cliff.

## Segmentation

Find the dimensions worth slicing by:

1. Keep categorical columns with roughly 3–50 distinct values and low null rates.
2. Compare a key metric's distribution across each segment's values.
3. Keep the dimensions where segments differ substantially; drop the ones where every segment looks the same.
4. Check segment sizes — a dimension where one value holds 98% of rows is not a useful cut.
5. Test whether the interesting segments are homogeneous or hide sub-segments.

Watch for Simpson's paradox during this step: a relationship that holds overall can reverse inside every segment when segment sizes are unbalanced. If an aggregate and its segments disagree, the segments are usually the truer read.

## Correlation

- Compute the correlation matrix across metric columns.
- Flag pairs at |r| > 0.7 for inspection.
- Expect trivially high correlations from derived columns — `total` against `subtotal`, a value against the same value in another currency. These are redundancy findings, not insights.
- Pearson correlation only detects linear relationships; a strong curved relationship can read near zero, so scan a scatter before concluding independence.
- Report correlation as association. Nothing in a profile establishes causation.

## Dataset Documentation Template

When the profile is meant to outlive the session, write it up in this form:

```markdown
## Table: [schema.table_name]

**Description:** [what one row represents in business terms]
**Grain:** one row per [entity/event]
**Primary key:** [column(s)] — [verified unique / N duplicates as of date]
**Row count:** [count] as of [date]
**Update frequency:** [real-time / hourly / daily / weekly]
**Owner:** [team or person]

### Key Columns

| Column | Type | Role | Description | Example values | Notes |
|---|---|---|---|---|---|
| user_id | STRING | Identifier | Unique user identifier | "usr_abc123" | FK to users.id, 0.3% orphaned |
| event_type | STRING | Dimension | Type of event | "click", "view", "purchase" | 15 distinct values |
| revenue | DECIMAL | Metric | Transaction revenue, USD | 29.99, 149.00 | Null for non-purchase events |
| created_at | TIMESTAMP | Temporal | Event time, UTC | 2024-01-15 14:23:01 | Partition column |

### Relationships
- Joins `users` on `user_id`
- Joins `products` on `product_id`
- Parent of `event_details` (1:many on `event_id`)

### Known Issues
- [defect, its measurement, and its date]

### Common Query Patterns
- [typical use, and the filter it requires]
```

The notes column carries the most value over time — it is where a measured defect stops being rediscovered by the next analyst.
