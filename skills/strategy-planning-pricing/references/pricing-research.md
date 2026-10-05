# Pricing Research

Load when price point needs evidence: no competitor anchor, new category, or user asks "how do we test price?". Output feeds price justification per tier.

## Contents

1. [Value-based ladder](#1-value-based-ladder)
2. [Van Westendorp](#2-van-westendorp)
3. [MaxDiff for packaging](#3-maxdiff-for-packaging)
4. [Competitor benchmark](#4-competitor-benchmark)
5. [Conversion-rate signals](#5-conversion-rate-signals)
6. [Pick method](#6-pick-method)

## 1. Value-based ladder

Price sits between next-best alternative and value delivered.

```
cost of doing nothing < next-best alternative < YOUR PRICE < value delivered
```

1. **Next-best alternative.** What customer does without you: competitor, spreadsheet, manual work, hire. Put cost on it.
2. **Value delivered.** Hours saved × loaded hourly rate. Revenue gained or protected. Errors or risk avoided. Ask best customers: "What breaks if we vanish tomorrow?"
3. **Place price.** Start 10-20% of documented value 🟡. Above ~50% of value → buyer feels squeezed. Below alternative → signals low confidence.

Worked: clinic scheduler saves office manager 20 h/month at $35/h loaded = $700/month value. Alternative: spreadsheet + overtime, ~$60/month. 10-20% of value = $70-140, above alternative. Clinic tier $89 sits inside.

## 2. Van Westendorp

Four questions, asked of target buyers who understand product:

1. At what price is it so cheap you doubt quality?
2. At what price is it a bargain?
3. At what price does it feel expensive but still worth considering?
4. At what price is it too expensive to consider?

Optional Newton-Miller-Smith (NMS) follow-up, asked right after Q2 and Q3: "How likely would you buy at [your bargain price] / [your expensive price]?" (1-5). Adds purchase likelihood → trial and revenue curves. Use for new categories where buyers lack reference price.

Run:

```bash
python3 scripts/van_westendorp.py --input survey.csv --segment-field segment --price 49 --price 89
python3 scripts/van_westendorp.py --sample        # fictional 2-segment survey
```

Input format: `assets/wtp-survey-sample.csv`. Script drops rows with missing answers or out-of-order answers (too_cheap ≤ cheap ≤ expensive ≤ too_expensive), then reports per segment.

Four crossings:

| Point | Curves | Read |
|---|---|---|
| PMC | too cheap × expensive | Range floor. Below → quality doubt. |
| OPP | too cheap × too expensive | Equal resistance both sides. Name misleads: not profit-max. |
| IDP | cheap × expensive | Price most buyers read as normal. |
| PME | cheap × too expensive | Range ceiling. Above → rejection. |

Acceptable range = PMC to PME. Practitioners define PMC/PME with variant curve pairs; state which pairs used when comparing to vendor reports.

Sample size: < 30 per segment → hypothesis only. 30-99 → usable, noisy. 100+ → stable. B2C panels often need 200-400.

Misreads that cost money:
- **"Range = price."** No. Pick point inside range with margin floor, competitor anchor, positioning.
- **"OPP = optimal."** OPP = balance point of rejection. Profit point often sits between IDP and PME when market tolerates it.
- **"Any respondent works."** Survey ICP only. Random panel → range for imaginary buyer.
- **"Blended range is fine."** Segments with different ranges = different tiers. Averaged range fits nobody.
- **"PME = what we can charge."** Stated ≠ revealed. Confirm upper half with live test, sales-priced cohort, or deal data before anchoring near PME.
- **"Works for any product."** Weak when buyers cannot form reference price. Add NMS questions or use conjoint.

Script warnings to respect: N < 30, > 20% rows dropped (survey wording confuses), PMC > PME (no shared range), range < 15% wide (small moves risky).

Limits: stated, not revealed preference. Anchors to whatever price respondents saw last. Use for range. Confirm with live test or deal data.

## 3. MaxDiff for packaging

Show sets of 4-5 features. Respondent picks most and least valuable. Repeat across sets. Score = relative value per feature.

Use:
- Top-scored features for hero tier differentiators.
- Features high-value to one segment only → gate to that segment's tier.
- Low scores everywhere → bundle in all tiers or cut.

Answers packaging, not price. Pair with Van Westendorp or conjoint for price.

## 4. Competitor benchmark

| Step | Do |
|---|---|
| 1 | List direct competitors + alternatives buyers name in calls. |
| 2 | Record plan names, prices, value metric, billing terms. Date it. |
| 3 | Map what each price includes. |
| 4 | Mark where you over- and under-deliver per competitor. |
| 5 | Position: premium 20-40% above market, at-market, or value leader at or below. |

Do not copy competitor prices. Their price reflects their costs and position. Public list price ≠ realized price. Discounting common in B2B. Ask won and lost deals what they paid.

## 5. Conversion-rate signals

Conversion = market's vote on price-to-value. Read by funnel type. Modeler applies same bands.

| Funnel | Rate | Signal | Action |
|---|---|---|---|
| Trial → paid | > 40% | Strong underpricing | Test +20-30% on new customers. |
| | 30-40% | Possible underpricing | Test +10-15% on new customers. |
| | 15-30% | Healthy | Work packaging, metric. |
| | 10-15% | Possible overpricing | Test value messaging before price cut. |
| | < 10% | High friction | Check onboarding and ICP fit first. Price last. |
| Free → paid | > 5% | Free tier thin or paid cheap | Test higher paid price or richer free tier. |
| | 2-5% | Healthy | Hold. |
| | < 2% | Weak | Free tier too generous or paid value unclear. |
| Demo → close | > 30% | Little price pushback | Raise list or cut discounting. |
| | 15-30% | Healthy | Hold. |
| | < 15% | Friction | Check qualification first. |

Other signals:
- Nobody ever asks about price on sales calls → too low.
- Every deal needs discount → list too high, or value story weak.
- All customers on one tier → packaging broken, not price.
- Customers ask for features in higher tier → gates working. Make upgrade easy.
- Price unchanged 2+ years → review.

Rule: one signal = hypothesis. Two agreeing signals = test. Never cut price on conversion alone. Fix friction first.

## 6. Pick method

| Situation | Method |
|---|---|
| Existing customers, price question | Conversion signals + new-customer price test. |
| New product, known category | Competitor benchmark + value ladder. |
| New category, no anchor | Value ladder + Van Westendorp with NMS follow-ups. |
| Different segments, one price list | Van Westendorp per segment (`--segment-field`). |
| Which features in which tier | MaxDiff. |
| Exact trade-off price vs feature | Conjoint (needs vendor or stats help). |
| Enterprise deals | Won/lost deal review, realized price, discount spread. |
