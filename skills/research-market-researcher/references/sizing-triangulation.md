# Sizing Triangulation

Load in Market Sizing mode, before any TAM, SAM, or SOM leaves the draft. Pairs with `scripts/triangulate_sizing.py`.

## Contents

1. [Definitions](#1-definitions)
2. [Build each method as a chain](#2-build-each-method-as-a-chain)
3. [Read the divergence](#3-read-the-divergence)
4. [Reconcile a failed triangulation](#4-reconcile-a-failed-triangulation)
5. [Fallacies](#5-fallacies)
6. [What to quote](#6-what-to-quote)

## 1. Definitions

| Term | Meaning | Test |
|---|---|---|
| TAM | Annual revenue if every possible buyer bought the category at today's price. | Would a buyer outside your geography and segment still count? Yes. |
| SAM | The part of TAM your product, geography, and channels can serve now. | Could you sell to this buyer next quarter with no new product? Yes. |
| SOM | The part of SAM you can win in the planning window, limited by sales capacity and competition. | Does the number fit your hiring plan and win rate? Yes. |

Use one unit for all three: annual revenue in one currency for one year. Do not mix lifetime value, gross merchandise value, and revenue.

## 2. Build each method as a chain

Both methods are products of factors. Write each factor with a value, a source, and a low/high range.

**Top-down** starts from a published total and narrows it.

```
TAM = category spend (report) x share that is your sub-category (report table)
SAM = TAM x share in your serviceable segment (census or survey)
SOM = SAM x attainable share (capacity model)
```

**Bottom-up** starts from countable units and a price.

```
TAM = number of buyers (registry, census) x units per buyer x annual price per unit (price pages, deals)
SAM = TAM x serviceable share (same filter as top-down, from unit data)
SOM = SAM x attainable share (pipeline x win rate x ramp)
```

Rules for factors:
- **Source every factor.** A factor without a source is an assumption. Label it, and expect it to be the first lever in reconciliation.
- **Give a range.** The range is your honest uncertainty, not a sensitivity toy. A range that is too narrow hides the gap. A range that is too wide makes every check pass.
- **Keep the methods independent.** If both chains use the same report for the same factor, they are one method twice. Triangulation then proves nothing.
- **Use the same filter at SAM.** If top-down SAM means "regional carriers" and bottom-up SAM means "carriers with 10-200 trucks", the SAM ratio compares two different markets.

## 3. Read the divergence

The script reports `ratio = larger / smaller` at each level. The ratio reads the same whichever method is larger.

| Result | Meaning | Action |
|---|---|---|
| Ratio within tolerance at all levels | The methods agree. | Quote the range. Name both methods. |
| Ratio over tolerance, bands overlap | The gap may sit inside your stated uncertainty. | Narrow the widest ranges with better sources. Do not quote a point. |
| Ratio over tolerance, bands do not overlap | At least one chain has a wrong factor or a wrong structure. | Reconcile (section 4). Do not quote either number. |
| TAM agrees, SOM does not | The attainable shares differ. | Reconcile the capacity model. SOM is the number the decision uses. |

Default tolerance by profile is a ratio of 1.25 to 1.4. Tighten it when the decision is close to its threshold. A market that is clearly 10x larger than the go/no-go line does not need a tight match.

Never average the two methods. An average hides the disagreement and looks more certain than either input.

## 4. Reconcile a failed triangulation

The script lists, for every TAM factor, the value that closes the gap alone and how far that value sits outside the factor's range. Work from the top.

1. **Inside-range levers.** The gap is explained by a factor inside its own uncertainty. Find a better source for that factor and narrow its range.
2. **Unsourced factors.** These have the weakest evidence. Source them before you question sourced ones.
3. **Structural errors.** If every lever is far outside its range, a chain is built wrong. Check:
   - Unit mismatch: per seat vs per account, monthly vs annual, list vs realized price.
   - Scope mismatch: the report covers a broader category, more countries, or services as well as software.
   - Double counting: the same spend counted at two levels of the value chain (for example, platform plus reseller margin).
   - Buyer count: registry counts include dormant entities. Apply an active filter.
4. **Re-run.** Change a value only when a source supports it. Record each change in the assumptions table with the old value, the new value, and the source.

Do not tune factors until the ratio passes. That produces agreement, not evidence.

## 5. Fallacies

- **One percent of a big number.** "If we get 1% of a $50B market" skips the bottom-up check and the attainable-share logic.
- **Spurious precision.** The script rounds to two significant figures because the inputs rarely support more. "$3.7142B" claims a precision the chain does not have.
- **Category growth as company growth.** A market growing 20% a year does not give you 20% a year.
- **Price drift.** Bottom-up uses today's realized price. Analyst totals can use list price or a forecast year. Align the year and the price basis.
- **Overlapping segments summed.** Segments must be mutually exclusive before their revenue adds up. `segment_gate.py` warns when segment accounts exceed market accounts.
- **Stale totals.** A report figure two years old in a fast category is an estimate, not a fact. Date it.

## 6. What to quote

Quote a range with both methods and the factor that most limits confidence.

> SAM is USD 170-270M a year (bottom-up 170M from 41K registered carriers x 38 trucks x USD 240 per truck x 45% regional; top-down 270M from Analyst report A). The methods differ by 1.6x. The maintenance-module share (10-30%) explains most of the gap and needs a better source before this number supports a pricing decision.

Put both chains in the Market Sizing template's Assumptions table, with sources and ranges.
