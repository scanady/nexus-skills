# Playbooks

Actions by situation. Pick by churn tier, lifecycle stage, or trigger.

## Churn tier playbooks

### Critical (80-100). Act within 48 hours

| When | Step | Detail |
|---|---|---|
| Day 0 | Alert leaders | Head of CS and commercial owner. Brief: warnings, ARR at risk, open support issues. Fast-track support |
| Days 1-2 | Executive call | Our executive to theirs. Listen first. Capture real objection. Do not defend product |
| Days 2-3 | Save plan | Value milestones tied to their business outcomes. Dates, owners, measures. Agree concessions inside first (price, roadmap, terms) |
| Days 3-5 | Rescue team | CSM, solutions engineer, support lead. 15-minute daily stand-up. Technical health check |
| Weeks 2-4 | Execute | Weekly customer check-in. Track milestones. Competitive defence if rival involved |
| Week 4 | Judge | Stabilising: drop to high cadence. Not: escalate to CEO or general manager |

Success: score below 60 in 30 days and customer confirms intent to stay.

### High (60-79). Act within 1 week

1. Days 1-3: root cause. Read all dimensions, ticket history, 90-day usage trend
2. Days 3-5: dedicated call, not routine. Open with: "I noticed changes and want to make sure we support you." Find top three concerns
3. Days 5-7: 30-day recovery plan, weekly checkpoints, shared with customer
4. Week 2: re-engage sponsor; confirm sponsorship and business outcomes
5. Ongoing: name a support contact; weekly issue status
6. Weeks 3-4: review. Drops to critical = executive playbook

Success: score below 40 in 30 days, no new warnings.

### Medium (40-59). Act within 2 weeks

1. Days 1-5: find which dimension drags score; read recent support tone; check known product issues
2. Weeks 1-2: value check-in framed as routine. Share peer wins. Offer training on unused features
3. Weeks 2-3: send ROI summary; flag relevant releases; invite to community
4. Weeks 3-4: monitor every two weeks. Still falling = high playbook

Success: score steady above 50, no climb to high.

### Low (0-39)

Keep cadence: enterprise monthly sessions plus QBR; mid-market every two months plus semi-annual review; SMB quarterly automated update plus annual review. Share releases and insight. Watch expansion signals. Start renewal prep 90 days out.

## Onboarding

Use `assets/onboarding-90-day.md`. Four phases: set up (days 0-14), activate (15-30), adopt (31-60), prove (61-90). First value inside 30 days (segment limits in [benchmarks.md](benchmarks.md)). Gate: yellow or better health before hand-off.

## Renewal timeline

| Days out | Do |
|---|---|
| 120 | Read terms and price. Score health and trend. List open issues. Align renewal plan inside |
| 90 | Book renewal conversation. Write value summary (ROI, usage, milestones). Draft proposal. At risk = escalate and start mitigation |
| 60 | Present proposal. Negotiate. Remove blockers; escalate to leaders |
| 30 | Finalise terms. Get signatures. Plan post-renewal moves |
| After | Confirm in systems. Thank-you and refreshed success plan. Book next QBR. List expansion options |

Renewal at 60 days or less and risk high or critical: bring commercial leader in at once.

## Expansion

Only on green or yellow health with low or medium churn tier.

| Signal | Play | Priority |
|---|---|---|
| Seats over 90% used | Seat expansion | High |
| Asks for higher-tier features | Tier upgrade | High |
| Cites rival for missing feature | Module cross-sell | High |
| Heavy use of adopted modules | Module cross-sell | Medium |
| Other department shows interest | Department expansion | Medium |

Conversation order: (1) discover: "Your team gets value from X; where else does Y hurt?" (2) frame value with a peer result; (3) propose from their real usage; (4) bring the budget holder in early, champion cannot sign; (5) hand commercial close to sales owner. Module used under 30% = enable first, never sell more.

## Escalation matrix

| Trigger | Escalate to | Within |
|---|---|---|
| Health turns red | Head of CS | 24 hours |
| Executive sponsor leaves | CS director and commercial owner | 48 hours |
| Critical bug hits customer | Head of engineering and head of CS | 4 hours |
| Customer names competitor evaluation | Head of CS and head of sales | 24 hours |
| Renewal at risk, 60 days or less | Revenue leader | 24 hours |
| Customer threatens legal action | Legal and head of CS | Immediately |

Escalation message: subject `[ESCALATION] {customer}: {issue}`. Body lines: customer, segment, ARR; health score and band; renewal date; 2-3 sentence summary; warning list; recommended next step; urgency.
