# Churn Risk Model

Rules behind `scripts/churn_risk_scorer.py`. Health says how account is. Churn risk says what is going wrong now and how soon renewal bites.

## Signal groups

Each group scores 0-100, higher = worse. Blend with weights.

| Group | Weight | Inputs and conversion |
|---|---|---|
| usage_decline | 30% | login_trend (% change) x3 at 40%; feature_adoption_change x4 at 35%; dau_mau_change x500 at 25%. Only declines count |
| engagement_drop | 25% | meeting_cancellations x25 at 30%; (response_time_days - 1) x15 at 35%; nps_change decline x20 at 35% |
| support_issues | 20% | open_escalations x35 at 35%; unresolved_critical x50 at 35%; satisfaction_trend at 30% (improving 10, stable 30, declining 70, critical 95) |
| relationship_signals | 15% | points: champion_left 45, sponsor_change 30, competitor_mentions 3+ gives 35 else 12 each |
| commercial_factors | 10% | points: month-to-month 30, quarterly 15, pricing_complaints 35, budget_cuts_mentioned 40 |

Each conversion saturates at 100. Group scores 0-100 after weighting inside group.

## Renewal urgency

Raw score x multiplier, cap 100. No end date = 1.0.

| Days to renewal | Multiplier |
|---|---|
| 30 or fewer | 1.50 |
| 31-60 | 1.35 |
| 61-90 | 1.20 |
| 91-180 | 1.10 |
| over 180 | 1.00 |

Use `--as-of` to pin the date when comparing runs.

## Tiers

| Tier | Score | First action |
|---|---|---|
| Critical | 80-100 | Executive escalation within 48 hours |
| High | 60-79 | CSM intervention within 1 week |
| Medium | 40-59 | Proactive outreach within 2 weeks |
| Low | 0-39 | Standard monitoring |

Full steps: [playbooks.md](playbooks.md).

## Warning severity

Output lists worst first.

| Severity | Examples |
|---|---|
| critical | logins down 20%+; 3+ meeting cancellations; silent 7+ days; NPS down 4+; 2+ unresolved critical tickets; 3+ competitor mentions; champion left |
| high | logins down 10%+; adoption down 15%+; DAU/MAU down 0.10+; 2 cancellations; reply 4+ days; NPS down 2+; 1 critical ticket; 2+ escalations; sponsor change; pricing complaints; budget cuts |
| medium | logins down 5%+; adoption down 5%+; 1 escalation; 1-2 competitor mentions; month-to-month |

## Read with health

| Health | Churn tier | Meaning |
|---|---|---|
| Green | Low | Healthy. Expansion candidate |
| Green | High or critical | Hidden event: champion left, budget cut. Health lags. Trust churn score |
| Red | Low | Weak adoption, no active exit signal. Fix value realisation before renewal |
| Red | Critical | Save plan now |

Where scores disagree, act on the more urgent one and find out why they differ.
