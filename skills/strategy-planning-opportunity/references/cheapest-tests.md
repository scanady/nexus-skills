# Cheapest Tests

Map riskiest assumption to smallest test that can prove it wrong. One week max. Real behavior, not opinion. Script: `scripts/cheapest_test.py` (also called by `opportunity_verdict.py`).

## Rules

- **Test one assumption.** Many assumptions, one or two load-bearing AND unproven. Hit those only. (Blank, *Four Steps to the Epiphany*, 2005.)
- **MVP per assumption, not mini product.** Least effort that yields validated learning. (Ries, *The Lean Startup*, 2011.)
- **Falsifiable.** Result must be able to say no. "Users liked it" can't. "10% of cold traffic signed up" can. (Popper, 1959.)
- **Pass AND fail line written before run.** Else soft result reads as yes. People lie to be nice. (Fitzpatrick, *The Mom Test*, 2013.)
- **Money > words. Stranger > friend. Behavior > survey.**
- **Time box ≤1 week.** Longer = build in disguise. Split it. Answer must arrive before money commits.

## Pick motion

| Motion | When |
|---|---|
| `self-serve` | Product-led, consumer, prosumer, low-ticket SMB. Buyer acts alone. |
| `sales-led` | Named accounts, demos, contracts, procurement, ticket > ~$5k/yr. |

Smoke page useless for enterprise buyer. Outbound batch wasteful for $9 app. Motion picks variant.

## Risk → test map

| Risk | Question | Self-serve test | Sales-led test | Canon |
|---|---|---|---|---|
| demand | Anyone want it? | Smoke page + $50–150 traffic. Pass ≥10% signup under target CAC. | 30 named-buyer notes. Pass ≥3 calls, ≥2 name pain unprompted. | Ries smoke test; Dropbox video |
| price | Pay, at this number? | Live payment link / paid early access. Pass ≥1 stranger prepays. | Paid pilot or priced LOI to 3–5 buyers. Pass ≥1 signed. | Blank; Hoy, *Stacking the Bricks* |
| channel | Reach buyer affordably? | One channel, one run. Pass CAC < ⅓ first-year value. | 50-account sequence. Pass ≥8% reply, ≥3 meetings. | Weinberg & Mares, *Traction* (bullseye) |
| feasibility | Deliverable? | Concierge for 1–3 users by hand. Pass outcome real, hours fit price. | Manual proof, one design partner. Pass buyer confirms + names signer. | Ries concierge MVP; Wizard of Oz |
| differentiation | Why you over incumbent/nothing? | 5 switch interviews, wedge shown last. Pass repeated switch reason incumbent can't copy fast. | 3–5 incumbent users: what forces replacement this year. Pass ≥2 name trigger + budget window. | Christensen, *Competing Against Luck*; Mom Test |
| retention | Come back? | 1-week probe, 5–10 users, no nudges. Pass ≥half return unprompted. | Ask each account to book cycle 2 now. Pass ≥half book/pay. | Ellis PMF retention; cohort over vanity |

Thresholds = defaults. Tighten for venture profile. Loosen only with stated reason (tiny niche, high ticket).

## Output shape

```
**Cheapest test:** [name] — [what to do]
**Cost / time box:** [$] / [≤1 week]
**Pass:** [number that keeps the thesis alive]
**Fail:** [number that kills or forces pivot]
```

Add decision rule in "Decision checkpoint": pass → next step; fail → Pivot/Kill per gate.

## Reject

- "Go talk to users." No count, no threshold.
- Friends-and-family sample.
- Survey asking "would you pay".
- Test needing build first.
- Two assumptions in one test. Ambiguous fail.
