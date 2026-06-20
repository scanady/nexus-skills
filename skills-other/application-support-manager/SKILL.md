---
name: application-support-manager
description: 'Application Support Manager role skill for direct-to-consumer insurance technology operations. Use when managing production application support for business systems including the Policy Administration System (PAS), MarTech platforms, the data platform, and CRM; triaging and resolving production incidents under defined SLAs; managing the support ticket queue; defining and maintaining runbooks; coordinating escalation to engineering teams; performing root cause analysis; supporting change management and release deployments; managing user access provisioning; or reporting support metrics. Triggers: application support, production incident, incident management, SLA management, runbook, ticket management, user access, access provisioning, change management support, release support, root cause analysis, production issue, system outage, application stability, support queue, escalation management, support metrics, monitoring and alerting, PAS support, MarTech support, data platform support.'
argument-hint: 'Describe the production system, incident type, support process, or operational support challenge'
---

# Application Support Manager

## Role Context
The Application Support Manager leads the production application support function, ensuring that business-critical systems supporting direct-to-consumer life insurance operations are available, performant, and effectively supported. Supported systems span the full technology stack: the Policy Administration System (PAS), Marketing Technology platforms (ESP, CDP, Tag Management), the data platform (ETL pipelines, data warehouse, object storage), CRM, customer-facing digital experiences, and internal operations tooling.

## Supported System Portfolio

| System Category | Examples | Business Criticality |
|----------------|---------|---------------------|
| Policy Administration System (PAS) | Core policy lifecycle system | Tier 1 — Mission Critical |
| Customer Digital Experience | Quote engine, application flow, self-service portal | Tier 1 — Mission Critical |
| Email Service Provider (ESP) | Marketing email delivery platform | Tier 1 — Campaign Critical |
| AWS Data Platform | Redshift, S3, Glue, dbt pipelines | Tier 1 — Reporting Critical |
| CRM | Customer and prospect relationship management | Tier 2 — Business Critical |
| CDP / Audience Platform | Customer data platform for segmentation | Tier 2 — Business Critical |
| Direct Mail Production Systems | Print vendor APIs and file transfer systems | Tier 2 — Campaign Critical |
| Tag Management / Analytics | Web analytics, conversion tracking | Tier 2 — Business Critical |
| Internal Operations Tools | Claims, servicing, document management | Tier 2 — Business Critical |

## Core Competencies

### Incident Management
- Own the end-to-end **incident management lifecycle**: detection, triage, assignment, investigation, resolution, and post-incident review
- Apply ITIL-aligned incident categorization: **Severity 1** (complete system outage or data-loss risk), **Severity 2** (major degradation affecting business operations), **Severity 3** (partial degradation with workaround available), **Severity 4** (minor issue, cosmetic, low impact)
- Define and enforce response SLAs by severity:

| Severity | Response Time | Resolution Target | Stakeholder Notification |
|----------|-------------|-------------------|--------------------------|
| Sev 1 | 15 minutes | 4 hours | Immediate — COO, CTO, affected business leads |
| Sev 2 | 30 minutes | 8 hours | Within 1 hour — affected business leads |
| Sev 3 | 2 hours | 2 business days | Ticket acknowledgment only |
| Sev 4 | 1 business day | 5 business days | Routine ticket update |

- Coordinate incident bridge calls for Sev 1 and Sev 2 incidents: assemble cross-functional response team, document timeline, communicate status updates at defined intervals
- Manage vendor escalation during incidents: engage vendor support organizations at appropriate severity level; track vendor response and escalate to account managers if SLA is breached
- Conduct **Post-Incident Reviews (PIRs)** for all Sev 1 and Sev 2 incidents: blameless root cause analysis, contributing factors, corrective actions, timeline to remediation

### Service Request & Ticket Management
- Manage the application support ticket queue using the enterprise ticketing platform (ServiceNow or equivalent)
- Define ticket routing rules: auto-assign by system, keyword, or business unit; ensure no ticket ages without assignment
- Monitor queue health metrics: open tickets by severity and age, first response time, SLA adherence rate, resolution time by category
- Conduct weekly ticket queue review: prioritize aging tickets, identify patterns suggesting underlying system problems
- Manage ticket escalation: define criteria for escalating service requests to Tier-3 engineering or vendor support; track escalated tickets to closure

### Runbook Development & Maintenance
- Own the **runbook library** for all Tier-1 and Tier-2 supported systems: step-by-step resolution procedures for known, recurring issues
- Define minimum runbook content standard: problem description, diagnostic steps, resolution steps, escalation path, associated monitoring alerts, and last test date
- Review and update runbooks after every incident where existing documentation proved insufficient or incorrect
- Ensure runbooks are version-controlled, accessible to all support team members, and reviewed on a quarterly basis
- Develop **new runbooks proactively** after system releases introducing new functionality or integration dependencies

### Monitoring & Alerting
- Define application monitoring standards in partnership with Engineering and Infrastructure teams: what to monitor, alert thresholds, and notification routing for each Tier-1 system
- Review monitoring coverage gaps: ensure all Tier-1 systems emit sufficient health signals (uptime, latency, error rate, job completion status) to enable proactive detection
- Manage **data pipeline monitoring**: track dbt pipeline success/failure rates, Glue job execution status, S3 data delivery timeliness; alert on SLA breaches before business users notice
- Manage **marketing platform monitoring**: ESP deliverability alerts, CDP audience sync failures, tag management data layer errors
- Maintain on-call rotation for after-hours Sev 1 coverage; define pager escalation matrix and rotatation schedule

### Change Management Support
- Participate in the **Change Advisory Board (CAB)**: review upcoming changes for production risk; provide support readiness sign-off for major releases
- Define support pre-requisites for production deployments: updated runbooks, monitoring configured, rollback plan documented, support team briefed
- Coordinate **hypercare support** for major releases: elevated monitoring and faster response SLAs during the first 72 hours post-deployment
- Manage emergency change process: expedited approval for urgent production fixes; ensure proper documentation post-deployment
- Maintain the **change calendar**: visible schedule of upcoming changes, maintenance windows, and blackout periods (e.g., no changes during major marketing campaign drops or month-end reporting periods)

### Root Cause Analysis & Problem Management
- Apply ITIL Problem Management to recurring incidents: distinguish symptoms (incidents) from underlying causes (problems)
- Maintain the **known error database**: documented known issues with workarounds, enabling faster incident resolution while permanent fix is implemented
- Identify repeat incident trends: use ticket data to surface top recurring issues by system, user group, or root cause category
- Commission and track **root cause action items**: engineering fixes, configuration changes, vendor patches, or process changes to eliminate repeat incidents
- Report problem management metrics to COO and CTO: open known errors, top recurring incident categories, MTTR trend

### User Access Management
- Own the **access provisioning and de-provisioning** process for supported applications: ensure new hires receive access within SLA; terminated employees are de-provisioned same day
- Maintain the **access matrix**: role-based access control (RBAC) definitions for each supported system; document who has what access and why
- Conduct quarterly **access certification reviews**: business owners certify that all active user accounts are still appropriate; remediate over-privileged accounts
- Partner with Lead Compliance Officer on access control compliance for insurance-regulated systems: ensure PAS and customer data systems comply with minimum-necessary access principles
- Manage service account inventory: document all system-to-system accounts; ensure shared or embedded credentials are eliminated and replaced with managed service accounts

### Vendor Support Coordination
- Manage support relationships with SaaS vendor support organizations for all Tier-1 and Tier-2 platforms
- Maintain **vendor support contact matrix**: escalation contacts, account managers, emergency hotlines, vendor SLA terms
- Track open vendor tickets: ensure vendor cases are progressing; escalate to account managers when vendor response is inadequate
- Coordinate vendor-initiated changes: maintenance windows, platform upgrades, deprecation notices; assess impact and communicate to affected business users
- Participate in vendor quarterly business reviews (QBRs): report support experience, open issues, and improvement requests

### Support Metrics & Reporting
- Define and report the **Application Support Scorecard** to COO and CTO on a monthly basis:

| Metric | Definition |
|--------|-----------|
| Sev 1/2 Incident Count | Number of high-severity incidents per period |
| SLA Adherence Rate | % of tickets resolved within target SLA |
| Mean Time to Acknowledge (MTTA) | Avg time from ticket creation to first response |
| Mean Time to Resolve (MTTR) | Avg time from ticket creation to resolution |
| Recurring Incident Rate | % of incidents attributable to known recurring problems |
| Access Provisioning SLA | % of new access requests completed within SLA |
| Runbook Coverage | % of Tier-1 and Tier-2 issues with documented runbooks |
| Change-Related Incident Rate | % of incidents caused by recent changes |

## DTC Insurance Application Support Considerations

- **Campaign-driven volume spikes**: Large direct mail drops and digital campaign launches dramatically increase application and quote volume; application support must ensure Tier-1 systems are at full capacity and monitoring is heightened during major campaign windows
- **Data pipeline criticality**: Marketing reporting and audience selection depend on daily AWS data pipeline execution; a failed pipeline that goes undetected can silently corrupt campaign targeting or stop reporting cold — proactive pipeline monitoring is essential
- **Regulatory data systems**: PAS and claims systems are regulated; access controls, audit trails, and change documentation for these systems must meet insurance regulatory examination standards
- **Multi-vendor MarTech stack**: A composable MarTech operation runs multiple SaaS platforms from different vendors; support coordination across vendors is complex — a data flow failure may span three vendors before reaching the root cause
- **PCI and PII data handling in incidents**: Incident investigation often requires accessing logs or records containing PII or payment data; the Application Support Manager must enforce data handling procedures during incident response to comply with CCPA, NYDFS 500, and PCI DSS

## Collaboration Interfaces

- **COO**: Primary business stakeholder for operational system reliability; escalation path for Sev 1 incidents; recipient of support scorecard
- **CTO/CIO**: Engineering escalation for Tier-3 issues; change advisory board; monitoring and alerting standards
- **Data Engineer**: Escalation path for data pipeline failures; runbook collaboration for data platform incidents
- **Marketing Technology Architect**: ESP, CDP, and MarTech platform issue triage; vendor support coordination for MarTech SaaS
- **Lead Compliance Officer**: Access control compliance, audit trail requirements, regulated system support standards
- **CRO**: Application availability contributes to operational risk profile; incident data feeds operational risk register
- **Print Channel Execution Lead / Email Channel Execution Lead**: Support contacts for channel execution system failures impacting campaign delivery
