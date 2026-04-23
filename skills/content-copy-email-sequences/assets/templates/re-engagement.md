# Re-Engagement Sequence

**Trigger**: 30–60 days of subscriber inactivity (no opens or clicks)
**Goal**: Win back active engagement or cleanly suppress inactive contacts
**Length**: 3–4 emails over 10–14 days
**Exit conditions**: Re-engages (opens/clicks) · explicitly opts out · no response → suppress

---

## Sequence Blueprint

```
Sequence Name:
Trigger: [X] days of inactivity
Goal: Re-engagement or clean list suppression
Length: 4 emails
Timing: Day 0 → Day 2–3 → Day 5–7 → Day 10–14
Exit conditions: Opens/clicks → remove from sequence. No response to Email 4 → suppress.
Segmentation rules: [define inactivity threshold — 30 days for active programs, 60+ for longer cycles]
```

---

## Email-by-Email Template

**Email 1: Check-In (Day 0)**
- Subject: "Is everything okay, [Name]?"
- Genuine concern — not a promo
- Ask what happened / what changed
- Offer an easy, low-friction win to re-engage

**Email 2: Value Reminder (Day 2–3)**
- Subject: "Remember when you [achieved X]?"
- Remind them of past value or what drew them in
- Share what's new since they went quiet
- Quick, low-friction CTA

**Email 3: Incentive (Day 5–7)**
- Subject: "We miss you — here's something special"
- Offer if appropriate (discount, bonus content, free upgrade)
- Limited time, clear CTA
- Don't make this the default — earn it with Emails 1–2 first

**Email 4: Last Chance (Day 10–14)**
- Subject: "Should we stop emailing you?"
- Honest and direct — no guilt, no pressure
- One-click to stay subscribed or unsubscribe
- No response after this = suppress from list

---

## Segmentation

- **By original engagement level**: Once-active vs. never-really-engaged → different tone and incentive
- **By time since last open**: 30 days vs. 90+ days → adjust how much "catching up" to include
- **Post-sequence**: Re-engaged contacts rejoin normal flow. Non-responders suppressed, not deleted.

---

## Copy Rules

- Never use guilt or shame ("You've been ignoring us...")
- Email 4 must be honest — ask plainly if they want to stay. Respect the answer.
- Incentive in Email 3 is optional — value reminder (Email 2) may be enough
- List hygiene is the goal if re-engagement fails — suppression improves deliverability

---

## Key Metrics

| Metric | Target |
|--------|--------|
| Re-engagement rate | 5–15% of inactive list |
| Unsubscribe rate (Email 4) | expected to be higher — this is intentional |
| List hygiene improvement | suppressed contacts should improve overall open rate |

---

## Audit Checklist

- [ ] Inactivity threshold defined (days of no opens/clicks)
- [ ] Email 1 tone is genuinely concerned, not promotional
- [ ] Email 4 includes explicit one-click opt-out
- [ ] Non-responders to Email 4 are suppressed (not just unsubscribed)
- [ ] Re-engaged contacts exit sequence and re-enter normal flow
- [ ] Incentive (Email 3) is appropriate for audience — not overused
- [ ] Sequence runs separately from main program — no overlapping sends
