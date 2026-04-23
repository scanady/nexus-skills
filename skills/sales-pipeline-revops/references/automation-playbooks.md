# Automation Playbooks

Platform-specific workflow recipes for HubSpot, Salesforce, scheduling tools, and cross-tool automation.

---

## HubSpot Workflows

### 1. MQL Assignment + Task Creation

**Trigger:** Contact "Lifecycle Stage" changes to "Marketing Qualified Lead"

**Actions:**
1. Rotate contact owner (round-robin across sales team)
2. Send internal email to new owner with lead context + recent activity
3. Create task: "Follow up with [Contact]" — due in 4 hours
4. Send Slack notification to #sales-alerts
5. Enroll in "MQL Follow-Up" sequence (if using HubSpot Sequences)

**Outcome:** Every MQL assigned instantly with clear SLA
**Note:** Set enrollment criteria to exclude leads already owned by a rep

---

### 2. MQL SLA Breach Alert

**Trigger:** Lifecycle Stage = "MQL" AND Days since last contacted > 0.5 (12 hours)

**Actions:**
1. Send internal email to owner: "SLA warning: [Contact] not contacted"
2. If no activity after 24h → alert sales manager
3. If no activity after 48h → reassign via round-robin rotation
4. Create task for new owner: "Urgent: [Contact] — reassigned due to SLA breach"

**Outcome:** No MQL goes unworked beyond 48 hours
**Note:** Exclude contacts where last activity type = Call or Meeting

---

### 3. Auto-MQL on Score Threshold

**Trigger:** HubSpot Score ≥ 65 (adjust to your threshold)

**Actions:**
1. Set Lifecycle Stage to "Marketing Qualified Lead"
2. Set "MQL Date" property to current date
3. Suppress from all marketing nurture workflows
4. Trigger Recipe #1 (MQL Assignment)

**Outcome:** Leads auto-promote when scoring threshold hit
**Note:** Add suppression list for existing customers and competitor domains

---

### 4. Meeting Booked Alert

**Trigger:** Meeting activity logged for contact (via Calendly / HubSpot Meetings)

**Actions:**
1. Send internal email to contact owner with meeting details
2. Update "Last Meeting Booked" property to current date
3. If Lifecycle Stage = "Lead" → advance to "MQL"
4. Create task: "Prepare for meeting with [Contact]" — due 1 hour before meeting
5. Send Slack notification to #meetings

**Outcome:** AEs prepared for every meeting with full context
**Note:** Include recent page views and content downloads in notification email

---

### 5. Closed-Won CS Handoff

**Trigger:** Deal Stage changes to "Closed Won"

**Actions:**
1. Update associated contact Lifecycle Stage to "Customer"
2. Set "Customer Since" date to current date
3. Assign contact owner to CS rep (by segment or territory)
4. Create task for CS: "Schedule kickoff with [Company]" — due 2 business days
5. Enroll contact in "Customer Onboarding" email sequence
6. Send internal notification to CS manager
7. Remove contact from all sales sequences

**Outcome:** Seamless sales-to-CS handoff on every close
**Note:** Include deal notes, contract value, and key stakeholders in CS notification

---

### 6. Stale Deal Alert

**Trigger:** Deal "Days in current stage" > [2x average for that stage]

**Actions:**
1. Email deal owner: "[Deal] stale — in [Stage] for [X] days"
2. Create task: "Update or close [Deal]" — due 3 business days
3. If no update after 7 days → alert sales manager
4. Add deal to "Stale Deals" dashboard list

**Outcome:** Pipeline stays clean, forecast stays accurate
**Note:** Customize thresholds per stage (e.g., Discovery 14 days, Proposal 10 days, Negotiation 21 days)

---

### 7. Recycled Lead Nurture Re-Entry

**Trigger:** Contact "Sales Rejection Reason" property is known (any value)

**Actions:**
1. Update Lifecycle Stage to "Recycled"
2. Reset engagement score to baseline (preserve fit score)
3. Enroll in "Recycled Lead Nurture" sequence (lower frequency)
4. Set "Recycle Date" to current date
5. Set re-enrollment trigger: if score crosses MQL threshold again, re-trigger Recipe #1

**Outcome:** Rejected leads get second chance without clogging active pipeline

---

### 8. Daily Lead Activity Digest

**Trigger:** Scheduled — daily at 8:00 AM local time

**Actions:**
1. Filter contacts: Lifecycle Stage = SQL or Opportunity AND had web activity in last 24h
2. Send digest email to each contact owner with their leads' activity
3. Include: pages visited, content downloaded, emails opened/clicked

**Outcome:** Sales reps start each day knowing which leads are active
**Note:** Exclude single homepage visits — only meaningful activity

---

## Salesforce Flow Equivalents

### 1. MQL Assignment (Record-Triggered Flow)

**Object:** Lead | **Trigger:** Status changes to "MQL"

**Flow steps:**
1. Get Records: query "Rep Assignment" custom object for next available rep
2. Update Records: set Lead Owner to assigned rep
3. Create Records: Task — "Contact MQL: {Lead.Name}" due = NOW + 4 hours
4. Action: send email alert to new owner
5. Update Records: update "Rep Assignment" last-assigned timestamp

**Note:** Use custom "Rep Assignment" object to manage round-robin state

---

### 2. SLA Escalation (Scheduled-Triggered Flow)

**Schedule:** Every 4 hours during business hours

**Flow steps:**
1. Get Records: Leads where Status = "MQL" AND LastActivityDate < TODAY − 1
2. Decision: is lead older than 48h with no activity?
   - YES → reassign to next rep, create urgent task, alert manager
   - NO → send reminder email to current owner

---

### 3. Pipeline Stage Automation (Record-Triggered Flow)

**Object:** Opportunity | **Trigger:** Stage field updated

**Flow steps:**
1. Decision: which stage was it changed to?
2. For each stage:
   - **Discovery** → create task "Complete discovery questionnaire"
   - **Demo** → create task "Prepare demo environment"
   - **Proposal** → create task "Send proposal" + alert deal desk if ACV >$25K
   - **Closed Won** → trigger CS handoff (create Case, assign CS owner, send welcome email)
   - **Closed Lost** → create task "Log loss reason" + add to win/loss report

---

### 4. Stale Deal Detection (Scheduled-Triggered Flow)

**Schedule:** Daily at 7:00 AM

**Flow steps:**
1. Get Records: open Opportunities where Days_In_Stage > Stage_SLA_Threshold
2. Loop through results:
   - Create Task: "Update stale deal: {Opportunity.Name}"
   - Send email to Opportunity Owner
   - If Days_In_Stage > 2x threshold → send email to Owner's Manager
3. Update custom field "Stale Flag" = true for dashboard visibility

---

## Calendly / SavvyCal Integration

### Round-Robin Meeting Setup (Calendly)

1. Create team event type with all eligible reps
2. Distribution: "Optimize for equal distribution"
3. Availability: each rep manages own calendar
4. Buffer: 15 min before and after
5. Minimum notice: 4 hours

**CRM integration:**
1. Calendly webhook fires on booking
2. Match invitee email to CRM contact
3. If contact exists → assign meeting to contact owner (override round-robin)
4. If new contact → create lead, assign via routing rules, log meeting
5. Set lifecycle stage to MQL (meeting = high-intent signal)

---

### SavvyCal Setup

Advantages: priority-based scheduling, overlay calendars, personalized booking links per rep

**Integration pattern:**
1. Create team scheduling link with priority rules
2. Webhook on booking → Zapier/Make → CRM
3. Match or create contact, assign owner, create task
4. Send confirmation with meeting prep materials

---

### Meeting Routing by Criteria

```
Booking form submitted
├─ Company size >500? (form field)
│  ├─ YES → Route to enterprise AE calendar
│  └─ NO ↓
├─ Existing customer? (CRM lookup)
│  ├─ YES → Route to account owner's calendar
│  └─ NO ↓
└─ Round-robin across SDR team
```

---

### No-Show Workflow

**Trigger:** Meeting time passes + no meeting notes logged within 30 minutes

**Actions:**
1. Wait 30 min after scheduled meeting time
2. Check: was a call or meeting logged?
   - YES → no action
   - NO → send "Sorry we missed you" email to prospect
3. Create task: "Reschedule with [Contact]" — due next business day
4. Second no-show → flag contact, alert manager

---

## Zapier Cross-Tool Patterns

### 1. New Lead → CRM + Slack + Task

**Trigger:** New form submission (Typeform, HubSpot form, Webflow)

**Actions:**
1. Create/update contact in CRM
2. Enrich with Clearbit (if available)
3. Post to Slack #new-leads with enriched data
4. Create task in project tool (Asana, Linear)

---

### 2. Meeting Booked → CRM + Prep Email

**Trigger:** New Calendly / SavvyCal booking

**Actions:**
1. Find or create CRM contact
2. Update lifecycle stage to MQL
3. Send prep email to rep (CRM link, LinkedIn, recent activity)
4. Create pre-meeting task

---

### 3. Closed Won → Onboarding Stack

**Trigger:** CRM deal stage → "Closed Won"

**Actions:**
1. Create customer record in CS tool (Vitally, Gainsight, ChurnZero)
2. Add to onboarding project template
3. Send welcome email via email tool
4. Create Slack channel: #customer-[company]
5. Notify CS team in Slack

---

### 4. Score Threshold → Cross-Tool Sync

**Trigger:** CRM lead score crosses MQL threshold

**Actions:**
1. Update marketing automation platform status
2. Add to retargeting audience (Facebook/Google Ads)
3. Trigger SDR outreach sequence
4. Log event in analytics (Mixpanel, Amplitude)

---

### 5. SLA Breach → Multi-Channel Alert

**Trigger:** CRM MQL follow-up task overdue

**Actions:**
1. Slack DM to rep
2. Email to rep
3. If 2h+ overdue → Slack DM to manager
4. If 4h+ overdue → reassign in CRM via webhook

---

### 6. Weekly Pipeline Digest

**Trigger:** Scheduled — every Monday 8:00 AM

**Actions:**
1. Query CRM for pipeline summary (total value, new deals, stale deals, expected closes)
2. Format as summary
3. Post to Slack #sales-team
4. Send email digest to sales leadership
