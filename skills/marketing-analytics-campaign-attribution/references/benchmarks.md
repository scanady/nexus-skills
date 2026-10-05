# Metrics and Benchmarks

## Honest status of the benchmarks

The ranges in `assets/benchmarks.json` are rough practitioner ranges. No dataset backs them. They were not checked against a current published source. Ad costs shift by season, auction, and year. Use them only to ask "is this wildly off?" Never use them as a target or as proof.

Print them with `python3 scripts/campaign_roi.py --show-benchmarks`. The JSON is the one copy. Edit it to put your own numbers in. This file does not repeat the table.

## Build a better baseline

In order of value:
1. **Your own history.** Same channel, same offer, last 3 to 6 periods. Use the median and the range.
2. **Your own best and worst campaigns.** They mark what your account can do.
3. **A published report for your vertical**, dated and cited in your deliverable. Add it to the JSON.
4. **The built-in ranges**, labeled "unverified orientation".

Put your values in `assets/benchmarks.json` as `[low, target, high]` per channel. Keep `default` as the fallback. Add a channel key to cover a new channel.

## Metric definitions

| Metric | Formula | Note |
|---|---|---|
| CTR | clicks / impressions | Reported as a percent |
| CPC | media spend / clicks | Media only |
| CPM | 1000 x media spend / impressions | Media only |
| CPL | total cost / leads | Total cost = media spend + `other_costs` |
| CPA, CAC | total cost / customers | The script uses one formula for both. Blended CAC is the portfolio line |
| Click-to-lead | leads / clicks | Landing and form quality |
| Lead-to-customer | customers / leads | Sales and lead quality |
| ROAS | revenue / media spend | Ignores non-media cost |
| Loaded ROAS | revenue / total cost | Closer to truth |
| ROI | (revenue - total cost) / total cost | Percent. Negative means money lost |
| Revenue per customer | revenue / customers | Not lifetime value |

A ratio with a zero denominator prints `n/a`. The script never turns it into 0.

## Bands

Each of CTR, ROAS, CPL, CPA is placed on `[low, target, high]`.
- Higher is better (CTR, ROAS): below low is `underperforming`, low to target is `below_target`, target to high is `good`, at or above high is `excellent`.
- Lower is better (CPL, CPA): at or below low is `excellent`, up to target is `good`, up to high is `below_target`, above high is `underperforming`.

A band is a prompt to look closer. It does not say stop or scale.

## Judging a metric in context

- **Brand versus non-brand** search differ by a wide margin. Split them in the input.
- **Retargeting** shows high ROAS because it targets people already close to buying. Part of that revenue would have happened anyway.
- **Awareness** campaigns look bad on CPA by design. Judge them by reach and assisted conversion.
- **Email** ROAS looks very high because list-building cost is not in the campaign cost.
- **Margin.** ROAS above 1 can still lose money after cost of goods. Break-even ROAS is `1 / gross margin`. Use gross margin if you have it.
- **LTV.** A CPA above first-order margin can still be fine when repeat purchase is strong. The script does not model LTV.

## Always include all costs

Add creative production, tools, agency fees, and labor to `other_costs`. The script warns when a campaign has none.
