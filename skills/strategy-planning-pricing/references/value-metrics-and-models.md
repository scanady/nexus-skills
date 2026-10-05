# Value Metrics and Pricing Models

Load before picking strategy type (step 3) or when user asks "per seat or usage?". Metric first. Packaging second. Price point last.

## Contents

1. [Three axes, fixed order](#1-three-axes-fixed-order)
2. [Pick value metric](#2-pick-value-metric)
3. [Value-metric red flags](#3-value-metric-red-flags)
4. [Model catalog](#4-model-catalog)
5. [Free, trial, freemium](#5-free-trial-freemium)
6. [Selection path](#6-selection-path)
7. [Benchmarks](#7-benchmarks)

## 1. Three axes, fixed order

| Order | Axis | Question | Wrong-first symptom |
|---|---|---|---|
| 1 | Value metric | What unit does bill scale with? | Tiers fine, revenue flat as customers grow. |
| 2 | Packaging | What sits in each tier? | All customers crowd one tier. |
| 3 | Price point | How much per unit or tier? | Endless price A/B tests, no lift. |

Teams jump to price point. Backwards. Wrong metric caps revenue no matter number.

## 2. Pick value metric

Metric passes all five tests or gets cut.

| Test | Question | Fail example |
|---|---|---|
| Tracks value | Customer gets more value → metric rises? | Seats in tool where one analyst does all work. |
| Grows with customer | Customer success → metric rises without upsell call? | Flat fee for customer that 10x'd. |
| Easy to predict | Buyer can forecast next bill? | API calls swing 5x week to week. |
| Hard to game | Customer cannot dodge it cheaply? | Shared logins on per-seat plan. |
| Easy to measure | You can meter and invoice it cleanly? | "Outcomes" nobody agrees on. |

Common metrics:

| Metric | Fits | Watch |
|---|---|---|
| Per seat | Collaboration, CRM, tools where every user acts. | Viewers, contractors, credential sharing. |
| Per active user | Seat tools with uneven usage. | Billing disputes over "active". |
| Creator / viewer split | One team builds, many consume. | Viewer abuse if viewers can edit. |
| Per usage unit | API, infra, AI, messaging. | Bill shock → customers self-cap. |
| Per record / entity | Contacts, locations, assets, projects. | Customers prune data to save money. |
| Per outcome | Payments, recovered revenue, leads won. | Attribution fights. |
| Flat fee | Small tools, uniform usage. | Heavy users subsidized. |

## 3. Value-metric red flags

Check current pricing against each. Any hit → metric review before price change.

| Red flag | What it looks like | Why it hurts | Fix |
|---|---|---|---|
| Seats without seat value | One power user, team only views output. | Customer pays for headcount, not value. Buys one seat, shares login. | Creator/viewer split, or bill on output (reports, projects). |
| Flat fee, uneven value | Top 10% of customers use 10x median. | Light users churn, heavy users stay cheap. Adverse selection. | Add usage tiers or usage cap per plan. |
| Volatile usage unit | Usage swings week to week. | Surprise bills → churn, or customers throttle use. | Prepaid credits, committed use + overage, or monthly cap. |
| Metric customer controls cheaply | Contacts, seats, projects easy to delete or merge. | Customers game metric. Revenue leaks. | Pick metric tied to activity, not inventory. |
| Metric customer cannot see | Compute units, "credits" with no mapping. | No trust, no forecast, sales cycle slows. | Show usage live. Translate unit to customer term. |
| Metric punishes adoption | More use → bigger bill before more value lands. | Customers limit rollout. You cap own growth. | Generous included usage, bill on value event. |
| Metric differs from competitors with no story | You bill per seat, market bills per location. | Buyers cannot compare. Procurement stalls. | Match market metric, or lead with why yours is fairer. |
| Every tier same metric limit | Tiers differ only by features. | No natural upgrade from growth. Expansion needs sales push. | Tie tier limits to metric (seats, usage bands). |

## 4. Model catalog

| Model | How it bills | Expansion | Best fit | Main failure |
|---|---|---|---|---|
| Per seat | Price × users. | Auto with hiring. | B2B collab, deal > $200/mo. | Single-power-user tools. |
| Usage-based | Pay per unit consumed. | Auto with usage. | Dev tools, infra, AI. | Unpredictable bills, downturn exposure. |
| Feature tiers | Flat price per bundle. | Upsell motion needed. | Clear segment differences, CFO wants fixed spend. | Customers cluster in one tier. |
| Flat fee | One price, all in. | None. | Simplicity as positioning, uniform cost to serve. | No expansion, subsidized heavy users. |
| Hybrid | Platform fee + seats or usage. | Floor + upside. | Mature products, mixed cost base. | Complexity kills self-serve conversion. |

Variants worth knowing:
- **Seat:** named, concurrent, creator/viewer, minimum seat count on enterprise.
- **Usage:** pure consumption, prepaid credits, committed use + overage, volume bands (lower unit price at scale).
- **Hybrid:** platform fee + seats, platform fee + usage, tiers with included usage + overage, seats + usage for heavy users.

Platform fee rule: usage model with many low-use months → add small platform fee. Gives revenue floor, cuts churn from idle months.

## 5. Free, trial, freemium

Freemium = acquisition strategy, not pricing model. Sits on top of any model.

| Option | Shape | Fits |
|---|---|---|
| Free forever tier | Permanent limited plan. | PLG, viral, network effects. |
| Time-limited trial | Full access 14-30 days. | Complex or sales-assisted product. |
| Usage-limited trial | Full access until cap. | Dev tools, AI. |
| Reverse trial | Full access, drops to free tier after trial. | PLG with clear premium value. |

Freemium math: free users cost money. Free-to-paid 2-5% viable at scale. 1-2% rarely covers free cost. Free tier must be useful alone. Paid tier must be obviously better. Crippled free tier worse than none.

## 6. Selection path

1. Value rises with users, every user acts → per seat. Some users only view → creator/viewer.
2. Value rises with measurable usage → usage-based. Usage hard to measure → feature tiers with usage caps.
3. Buyer = small business wanting simple bill → flat fee or 2-3 feature tiers.
4. Enterprise buyers need SSO, audit, SLA → enterprise tier, even if "Contact sales".
5. Developer product → usage + free tier is market norm.
6. Fixed and variable serving cost both large → hybrid (platform fee + usage).

Map result to existing Strategy Type table in SKILL.md.

## 7. Benchmarks

Directional. Vary by segment and ACV. Tag 🟡 estimated when quoted.

| Metric | Early | Growth | Scale |
|---|---|---|---|
| Trial-to-paid | 15-25% | 20-35% | 25-40% |
| Annual share of customers | 30-50% | 40-60% | 50-70% |
| Expansion share of new MRR | 0-10% | 10-20% | 20-40% |
| Monthly logo churn (SMB) | 2-8% | 1-4% | 0.5-2% |
| Price review cadence | Ad hoc | Yearly | Yearly |

LTV:CAC under 3:1 → pricing, retention, or both broken.
