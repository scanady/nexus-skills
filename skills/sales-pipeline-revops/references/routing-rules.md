# Lead Routing Rules

Decision trees, routing methods, territory models, ABM routing, speed-to-lead benchmarks, and platform setup.

---

## Routing Decision Tree

Base template — customize for your business. Route most specific match first, fall back to general.

```
New Lead Arrives
│
├─ Is this a named / target account?
│  ├─ YES → Route to assigned account owner
│  └─ NO ↓
│
├─ Is ACV likely >$50K? (company size + industry signal)
│  ├─ YES → Route to enterprise AE team
│  └─ NO ↓
│
├─ PLG signup with team usage?
│  ├─ YES → Route to PLG sales specialist
│  └─ NO ↓
│
├─ Matches a territory rule?
│  ├─ YES → Route to territory owner
│  └─ NO ↓
│
└─ Default: Round-robin across available reps
   └─ No rep available → Assign to team queue with 1-hour SLA
```

Key principle: **route most specific match first, fall back to general.** Always include fallback owner — unassigned leads go cold fast.

---

## Round-Robin Routing

### Rules

1. Distribute leads evenly across eligible reps
2. Skip reps on PTO, at capacity, or with full pipeline
3. Weight by quota attainment — reps below quota get slight priority
4. Reset distribution count weekly or monthly
5. Log every assignment for audit and optimization

### HubSpot Setup

**Built-in rotation:**
- Automation → Workflows
- Trigger: Lifecycle Stage = MQL
- Action: Rotate contact owner among selected users
- Options: Even distribution, skip unavailable owners
- Follow with: task creation + SLA deadline

**Custom rotation (for precise control):**
1. Create "Rotation Counter" property (number)
2. Trigger: new MQL
3. Branch by counter value (0, 1, 2… one branch per rep)
4. Set contact owner to rep for that branch
5. Increment counter; reset at max
6. Create follow-up task with SLA

### Salesforce Setup

**Lead Assignment Rules (basic):**
1. Setup → Marketing → Lead Assignment Rules
2. Create rule entries in priority order (most specific first)
3. Round-robin: combine assignment rule with custom logic or third-party app

**Flow (advanced):**
1. Record-Triggered Flow on Lead creation
2. Get Records: query "Rep Queue" custom object for next available rep
3. Decision: check rep availability, capacity, territory
4. Update Records: assign lead owner
5. Create Task: follow-up with SLA
6. Update "Rep Queue" last-assigned timestamp

---

## Territory Routing

### By Geography

| Territory | Regions | Team |
|-----------|---------|------|
| West | CA, WA, OR, NV, AZ, UT, CO, HI | Team West |
| Central | TX, IL, MN, MO, OH, MI, WI, IN | Team Central |
| East | NY, MA, PA, NJ, CT, VA, FL, GA | Team East |
| International | All non-US | International team |

### By Company Size

| Segment | Size | Team |
|---------|------|------|
| SMB | 1–50 | Inside sales |
| Mid-market | 51–500 | Mid-market AEs |
| Enterprise | 501–5000 | Enterprise AEs |
| Strategic | 5000+ | Strategic accounts |

### By Industry

| Vertical | Industries | Specialist |
|----------|-----------|------------|
| Tech | SaaS, IT services, hardware | Tech vertical rep |
| Financial | Banking, insurance, fintech | Financial vertical rep |
| Healthcare | Hospitals, pharma, healthtech | Healthcare vertical rep |
| General | All others | General pool (round-robin) |

### Hybrid Territory Model

Combine dimensions for precision:

```
Lead arrives
├─ Company size >1000?
│  ├─ YES → Enterprise team
│  │  └─ Sub-route by geography
│  └─ NO ↓
├─ Industry = Healthcare or Financial?
│  ├─ YES → Vertical specialist
│  └─ NO ↓
└─ Round-robin across general pool
   └─ Weighted by geography preference
```

---

## ABM / Named Account Routing

### Setup

1. Define target account list (typically 50–500 accounts)
2. Assign account owners in CRM — one rep per account
3. Match logic: any lead from target account domain → routes to account owner
4. Matching rules:
   - Email domain match (primary)
   - Company name fuzzy match (secondary — requires manual review)
   - IP-to-company resolution (tertiary — for anonymous visitors)

### ABM Routing Tiers

| Tier | Account Type | Routing | Response SLA |
|------|-------------|---------|--------------|
| Tier 1 | Top 20 strategic accounts | Named owner, instant alert | 1 hour |
| Tier 2 | Top 100 target accounts | Named owner, standard alert | 4 hours |
| Tier 3 | Target industry/size match | Territory or round-robin | Same business day |

### Multi-Contact Handling

When 3+ contacts from same account engage:
- Route all contacts to same account owner
- Notify owner of each new contact entering
- Track account-level engagement score (sum of all contacts)
- Trigger "buying committee" alert to AE and manager

---

## Speed-to-Lead

### Response Time Impact

| Response Time | Relative Qualification Rate | Notes |
|---------------|----------------------------|-------|
| Under 5 minutes | **21x** more likely to qualify | Gold standard |
| 5–10 minutes | 10x | Still strong |
| 10–30 minutes | 4x | Acceptable |
| 30 min – 1 hour | 2x | Below best practice |
| 1–24 hours | Baseline | Industry average |
| 24+ hours | 60% below baseline | Lead effectively cold |

Source: Lead Connect, InsideSales.com

### Implementing Speed-to-Lead

1. **Instant notification** — Push + email to rep on MQL creation
2. **Auto-task with countdown** — Task with 5-minute SLA target
3. **Escalation chain:**
   - 5 min: original rep alerted
   - 15 min: backup rep alerted
   - 30 min: manager alerted
   - 1 hour: lead reassigned to next available rep
4. **Measure weekly** — Track actual response times; recognize fast responders

### Speed-to-Lead Automation

**Trigger:** New MQL created

**Actions:**
1. Assign rep via routing rules (instant)
2. Push notification + email to rep
3. Create task: "Contact [Lead] — 5 min SLA"
4. Start SLA timer
5. No activity in 15 min → alert backup rep
6. No activity in 30 min → alert manager
7. No activity in 60 min → reassign via round-robin

### Metrics to Track Weekly

- Average time to first contact (MQL → first call/email)
- Median time to first contact (less skewed by outliers)
- % of leads contacted within SLA (target: 90%+)
- Contact rate by time of day (identify coverage gaps)
- Conversion rate by response time bucket (prove ROI of speed)
