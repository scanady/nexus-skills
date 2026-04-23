# New Customers Series (Post-Conversion)

**Trigger**: User converts from free/trial to paid
**Goal**: Reinforce purchase decision, drive adoption of paid features, reduce early churn
**Length**: 3–5 emails over 14 days
**Exit conditions**: Completes setup · reaches first renewal · requests downgrade/cancel → hand off to respective flow

---

## Sequence Blueprint

```
Sequence Name:
Trigger: Paid conversion confirmed
Goal: [first paid feature adoption / early churn reduction]
Length: 3–5 emails
Timing: Immediate → Day 2 → Day 5 → Day 7 → Day 14
Exit conditions: Completes setup milestone, reaches first renewal
Segmentation rules: [by plan tier if features differ significantly]
```

---

## Email-by-Email Template

**Email 1: Thank You + What's Next (Immediate)**
- Express genuine thanks — confirm purchase clearly
- Explain what happens now (setup steps, access instructions)
- Set expectations — don't make them wonder if it worked

**Email 2: Getting Full Value (Day 2)**
- Setup checklist specific to their plan/tier
- Link directly to each step in the product
- Offer help if anything is unclear (support link, chat, CSM intro)

**Email 3: Pro Tips (Day 5)**
- Features or workflows exclusive or enhanced in their paid plan
- One specific "wow" tip — not a feature dump
- Practical use case, not marketing language

**Email 4: Success Story (Day 7)**
- Customer at a similar company size / use case
- Specific result and relatable journey
- Reinforces that they made the right decision

**Email 5: Check-In + Support (Day 14)**
- Genuine check-in — how's it going?
- Introduce ongoing support channels
- Offer call, demo, or CSM meeting if relevant to plan tier

---

## Segmentation

- **By plan tier**: Pro vs. Enterprise → different feature highlights in Email 3, different support offers in Email 5
- **By activation status**: If setup checklist (Email 2) completed → skip reminder nudge in Email 3 and go deeper
- **B2B teams**: Admin received Email 1 → individual users may need a separate invite/activation flow

---

## Copy Rules

- This is NOT a welcome sequence — they've already committed. Reinforce the decision, don't re-sell.
- Focus: adoption, value realization, relationship building
- Avoid: trial conversion messaging, urgency, "don't miss out" framing — they're already in
- Tone: warm, confident, partner — like a CSM intro email

---

## Key Metrics

| Metric | Target |
|--------|--------|
| Setup completion rate | track step 2 checklist CTA clicks |
| Early churn (first 30 days) | benchmark vs. pre-sequence baseline |
| Feature adoption rate | track paid feature usage from email CTA |
| Support ticket rate | lower is better — sequence should preempt issues |

---

## Audit Checklist

- [ ] Sequence is triggered only on paid conversion (not free signup)
- [ ] Email 1 confirms payment clearly and sets expectations
- [ ] Email 2 setup checklist is specific to the user's actual plan tier
- [ ] Email 3 highlights paid-only or enhanced features (not free tier features)
- [ ] Success story (Email 4) matches audience profile
- [ ] Email 5 CSM/support offer is appropriate for plan tier (not offered to low-value plans if cost is a concern)
- [ ] No "upgrade to paid" messaging — they're already paid
- [ ] Sequence handoff to renewal flow is configured at day 14+
