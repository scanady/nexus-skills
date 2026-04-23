# Cancelled Customers Win-Back

**Trigger**: Customer actively cancels paid subscription
**Goal**: Win back churned customers after product improvements or new offers
**Length**: 2–3 emails over 90 days
**Exit conditions**: Re-subscribes · explicitly declines · no response at Day 90 → suppress

---

## Sequence Blueprint

```
Sequence Name:
Trigger: Cancellation confirmed
Goal: Re-subscription
Length: 2–3 emails
Timing: Day 30 → Day 60 → Day 90
Exit conditions: Re-subscribes, explicitly declines, or suppressed after Day 90
Segmentation rules: [by cancellation reason if captured — critical for relevance]
```

---

## Email-by-Email Template

**Email 1: What's New (Day 30 Post-Cancel)**
- Subject: "A lot has changed since you left, [Name]"
- Share genuine updates — new features, improvements, fixes since they left
- No guilt. No ask. Just a "hey, in case you care" update.
- Soft CTA: explore what's new (optional, low pressure)

**Email 2: We Addressed It (Day 60)**
- Subject: "We heard you — [specific improvement]"
- Reference the cancellation reason if known (use data)
- Show specifically how it was addressed
- Soft CTA: "Give us another shot?" with easy re-subscribe path

**Email 3: Special Offer (Day 90)**
- Subject: "We'd love to have you back"
- Make a genuine offer: discount, extended trial at previous tier, or locked-in rate
- Clear CTA to re-subscribe
- Final email — ends the sequence without burning the relationship

---

## Segmentation by Cancellation Reason

**"Too expensive"**
- Email 3: offer discounted plan or annual pricing
- Email 2: emphasize value improvements and ROI

**"Missing features"**
- Email 1: lead with feature releases that address their gap
- Email 2: specific update on the feature they wanted

**"Switching to competitor"**
- Email 1: neutral, no competitor bashing
- Email 2: differentiation angle — what changed that matters to them

**"Not using it enough"**
- Email 1: new guides, improved onboarding resources
- Email 2: offer a fresh-start guided setup
- Email 3: reduced or starter plan option

**Reason unknown**
- Run full 3-email sequence using general value + improvement angle
- Consider adding a brief survey in Email 1 to learn the reason

---

## Copy Rules

- No guilt. No desperation. No "we miss you so much" overwrought tone.
- Genuine updates only — don't claim improvements that didn't happen
- Reference their specific cancellation reason if known — generic win-back is lower ROI
- Leave every email with the relationship intact — they may refer others even if they don't return

---

## Key Metrics

| Metric | Target |
|--------|--------|
| Win-back rate | 5–15% (varies significantly by reason and time gap) |
| Email open rate | lower than active list — 15–25% is reasonable |
| Re-subscription LTV | track whether win-backs retain at same rate as organic |
| Referrals from non-re-subscribers | passive value even when win-back fails |

---

## Audit Checklist

- [ ] Cancellation reason captured (in-app survey or CSM notes) and used in segmentation
- [ ] Sequence starts at Day 30 — not immediately after cancel (give breathing room)
- [ ] Email 1 contains genuine product updates (not recycled marketing claims)
- [ ] Email 2 references specific cancellation reason if known
- [ ] Email 3 includes a concrete, time-limited offer
- [ ] No guilt, pressure, or desperation language in any email
- [ ] Re-subscribers exit sequence immediately and enter new customers series
- [ ] Non-responders at Day 90 suppressed from win-back (can re-enter if significant time passes)
