# Coverage Model

Decision: how do we cover the book, and when do we add CSMs? Tool: `scripts/coverage_sizer.py`.

## Four models

| Model | Fit | ARR per CSM | Accounts per CSM | Trade-off |
|---|---|---|---|---|
| Tech-touch | SMB, ACV under $5K, PLG | $5M-15M+ | 1,000+ (escalations only) | Cheapest. Cannot save high-stakes deals. Silent churn. Needs good in-product onboarding and an escalation path when account grows |
| Pooled CSM | Mid-market, ACV $5K-20K | $2M-5M | 50-150 | Cheaper than named. Less intimacy. Needs CS ops and health-score automation. Burnout if pool too big |
| Named CSM | Enterprise, ACV $20K-100K | $500K-2M | 20-30 | Standard for enterprise. About $180K loaded cost. Ramp 3-6 months. Single point of failure if CSM leaves |
| Named CSM + executive sponsor | Strategic, ACV $100K+ | $300K-1M | 5-10 | Highest cost: CSM plus 4-8 executive hours per quarter per account. Ceremonial sponsorship destroys trust |

Defaults in the sizer: strategic $800K and 8 accounts; enterprise $1.2M and 25; mid-market $3.5M and 150; SMB $10M and 1,000. Loaded yearly cost: $220K, $180K, $140K, $110K.

Model follows segment; segment follows ARR and ICP fit.

| Segment | Default | Override |
|---|---|---|
| Strategic | Named plus executive | Never. Retention and reference value pay for it |
| Enterprise | Named | Pooled if ACV barely qualifies and tenure is stable |
| Mid-market | Pooled | Named if account is on strategic path |
| SMB | Tech-touch | Pooled if expansion potential is exceptional |

## Ratio math

ARR per CSM = revenue under one CSM. Higher = more leverage; lower = more intimacy. Start point, not target.

| Stage | Strategic | Enterprise | Mid-market | SMB |
|---|---|---|---|---|
| Seed | n/a | $300K-800K | $1M-3M | n/a |
| Series A | $500K-1M | $800K-1.5M | $2M-4M | $5M+ |
| Series B / growth | $700K-1.5M | $1M-2M | $3M-5M | $8M+ |
| Late stage | $1M-2M | $1.5M-3M | $4M-8M | $15M+ |

Lower ratios when: product complex, industry regulated, CS drives expansion. Higher ratios when: product simple, UX strong.

## CSMs needed

Per tier: larger of (ARR / ARR-per-CSM) and (accounts / accounts-per-CSM), both rounded up. The binding limit is reported. Do not wait for CSMs at 100% load; hire to a 20% buffer.

Plan: project the book linearly over four quarters at `growth_pct`. Hire to start one quarter before need.

| Tier | 50% productive | Fully productive |
|---|---|---|
| Strategic | 3 months | 6-9 months |
| Enterprise | 2 months | 4-6 months |
| Mid-market | 1 month | 2-3 months |
| SMB | 2 weeks | 1 month |

Rule: hire 90 days before you need the capacity.

## Manager triggers

Add a manager when any is true:
1. 5+ CSMs in one tier (lead can no longer carry book and manage)
2. 8+ CSMs across team
3. CS escalates to CEO or CTO weekly for non-product issues

Prefer internal promotion: knows the playbooks. Needs people skill and has run a book. Train them; best individual contributors often fail as managers.

## CS compensation

Named CSM: 70% base, 30% variable. Variable: 50% gross retention, 30% net retention (expansion), 20% activity (QBRs done, share of green accounts). Never pay on NPS or happiness alone; it gets gamed and renewals do not follow. Pooled CSM: more weight on activity and automation health; account outcomes are statistical at that volume.

## Out of scope

CS tool selection, health-score formula (see [health-scoring-model.md](health-scoring-model.md)), pay negotiation for one person.

## Sizing project (1 week)

1. Build book with current accounts and planned acquisition
2. Run sizer; read gap now and gap in 12 months per tier
3. Compare with current team; agree hire order with finance and people leads
4. Output: 12-month hiring plan with start-by quarters
