# NFR Checklist

Gather these before designing. Missing NFRs = wrong architecture.

## Scalability

| Question | Tiers |
|---|---|
| Concurrent users | 100 / 1K / 10K / 100K+ |
| Requests per second | 10 / 100 / 1K / 10K+ |
| Data volume now | MB / GB / TB / PB |
| Growth rate (annual) | < 10% / 10–50% / 50–100% / > 100% |
| Peak vs. average load | 2x / 5x / 10x+ |

## Performance

| Metric | Targets |
|---|---|
| API response time (p95) | < 100ms / 200ms / 500ms |
| Page load time | < 1s / 2s / 3s |
| DB query time | < 10ms / 50ms / 100ms |
| Batch throughput | 1K / 10K / 100K records/hr |

## Availability

| SLA | Annual downtime | Typical use |
|---|---|---|
| 99% | 3.65 days | Internal tools |
| 99.9% | 8.76 hours | Business apps |
| 99.95% | 4.38 hours | Consumer / e-commerce |
| 99.99% | 52.6 min | Financial, payments |
| 99.999% | 5.3 min | Life-critical |

## Reliability

| Question | Options |
|---|---|
| Recovery Point Objective (RPO) — max data loss | 0 / 1hr / 4hr / 24hr |
| Recovery Time Objective (RTO) — max downtime | 15min / 1hr / 4hr / 24hr |
| Backup frequency | Real-time / hourly / daily |
| Disaster recovery scope | Single-region / multi-region |

## Security

| Question | Options |
|---|---|
| Authentication | JWT, OAuth 2.0, SAML, MFA, passkeys |
| Authorization model | RBAC, ABAC, ACL |
| Data sensitivity | Public / internal / confidential / PII / PHI |
| Compliance requirements | GDPR, HIPAA, PCI DSS, SOC 2, ISO 27001 |
| Encryption | In transit (TLS 1.2+), at rest, end-to-end |

## Observability

| Concern | Tooling categories |
|---|---|
| Logs | Structured JSON → aggregation platform |
| Metrics | Time-series scrape (Prometheus model) + dashboards |
| Tracing | Distributed trace (OpenTelemetry standard) |
| Alerting | On-call routing, escalation policies |

## Maintainability

| Question | Options |
|---|---|
| Deploy frequency | Hourly / daily / weekly / monthly |
| Deploy strategy | Blue-green / canary / rolling / in-place |
| On-call requirement | 24/7 / business hours / best-effort |

## Cost

| Question | Scope |
|---|---|
| Infrastructure budget | $/month ceiling |
| Cost per unit | $/user, $/request, $/GB |
| Cost optimization | Reserved capacity, spot/preemptible, rightsizing |

## NFR Summary Template

```markdown
## NFRs

**Performance:** API < 200ms p95 | page load < 2s | DB < 50ms
**Scale:** 10K concurrent users | 1K RPS | 1TB data
**Availability:** 99.9% (8.76 hr/yr downtime)
**Reliability:** RPO 1hr | RTO 4hr
**Security:** OAuth 2.0 + RBAC | PII encrypted at rest | GDPR
**Observability:** structured logs | Prometheus metrics | OTel traces | PagerDuty alerts
**Deploy:** daily deploys | blue-green | 24/7 on-call
**Cost:** $X/month infra ceiling
```
