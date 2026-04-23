# Billing Recovery (Failed Payment)

**Trigger**: Payment processing fails (card expired, declined, insufficient funds)
**Goal**: Recover revenue, retain customer, prevent involuntary churn
**Length**: 3–4 emails over 7–14 days
**Exit conditions**: Payment updated successfully · account manually resolved · account suspended after final email

---

## Sequence Blueprint

```
Sequence Name:
Trigger: Payment failure event
Goal: Customer updates payment method before account suspension
Length: 3–4 emails
Timing: Day 0 → Day 3 → Day 7 → Day 10–14
Exit conditions: Payment updated → stop sequence immediately. No update → suspend per policy.
Segmentation rules: [by customer value / tenure — high-LTV customers may get personal outreach]
```

---

## Email-by-Email Template

**Email 1: Friendly Notice (Day 0)**
- Subject: "Quick heads up — your payment didn't go through"
- Assume it's an accident (card expired, bank flagged it)
- Clear, direct — here's what happened, here's the fix
- Single CTA → update payment link (one click to fix)
- No guilt, no alarm

**Email 2: Reminder (Day 3)**
- Subject: "Your [Product] subscription — action needed"
- Reminder that the issue isn't resolved yet
- Note that service may be interrupted if not fixed soon
- Reiterate single CTA → payment update link

**Email 3: Urgent Notice (Day 7)**
- Subject: "Your account will be suspended [date]"
- Specific date — not vague "soon"
- Explain what access they'll lose
- Direct CTA → update payment + offer support if there's an issue

**Email 4: Final Notice (Day 10–14)**
- Subject: "Your account has been suspended"
- Or: "Last chance — restore your access today"
- What they're losing / have lost
- How to restore (clear, no friction)
- Door stays open — no permanent bans in the copy

---

## Segmentation

- **By customer tenure**: Long-term customers → more empathetic tone, consider personal outreach (CSM/support)
- **By plan value**: High-LTV accounts → human follow-up in parallel with email sequence
- **By previous history**: First failure → full sequence. Repeat failures → tighter timeline + proactive outreach

---

## Copy Rules

- Assume accident, never intent — "your card likely expired" not "you failed to pay"
- Single CTA in every email → payment update link. No distractions.
- No guilt, no threats, no late fees language (unless policy requires)
- Escalate tone gradually: friendly → reminder → urgent → final. Don't start urgent.

---

## Key Metrics

| Metric | Target |
|--------|--------|
| Recovery rate (Email 1) | 40–60% of failures resolved on first email |
| Overall sequence recovery rate | 60–80% |
| Time to recovery | track average days to payment update |
| Churn from billing failure | benchmark to identify at-risk cohorts |

---

## Audit Checklist

- [ ] Sequence fires on payment failure event (not delayed)
- [ ] Email 1 sends same day as failure (Day 0)
- [ ] Each email has single CTA → direct payment update link (not homepage login)
- [ ] Exit condition fires immediately on successful payment update
- [ ] No guilt or threatening language in any email
- [ ] Email 3 includes specific suspension date (not vague)
- [ ] High-LTV accounts flagged for human outreach in parallel
- [ ] Post-recovery: customer receives confirmation and sequence ends
