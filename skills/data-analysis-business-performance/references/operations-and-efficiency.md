# Operations & Efficiency Reference

## Table of Contents
- [Operational Performance Framework](#operational-performance-framework)
- [Cost Structure Analysis](#cost-structure-analysis)
- [Process Efficiency](#process-efficiency)
- [Capacity and Resource Planning](#capacity-and-resource-planning)
- [Marketing Performance Analytics](#marketing-performance-analytics)

---

## Operational Performance Framework

### Core Operational Metrics by Business Type

**SaaS / Software**
| Metric | Formula | Healthy Range |
|--------|---------|--------------|
| Uptime / Availability | (Total Time - Downtime) / Total Time | >99.9% |
| Mean Time to Resolution | Avg time from incident to resolution | <4 hours (critical) |
| Deployment Frequency | Deployments per time period | Multiple per week |
| Feature Adoption Rate | Users using new feature / Total users | >20% within 30 days |
| Support Ticket Volume | Tickets per 1,000 users | Declining trend |

**E-commerce / Retail**
| Metric | Formula | Focus |
|--------|---------|-------|
| Inventory Turnover | COGS / Average Inventory | Higher = less capital trapped |
| Fulfillment Cost per Order | Total fulfillment costs / Orders | Trend and benchmark |
| Return Rate | Returns / Orders | By product, by channel |
| On-Time Delivery Rate | On-time deliveries / Total deliveries | >95% |
| Stockout Rate | Out-of-stock events / Total SKU-days | <2% |

**Services / Professional Services**
| Metric | Formula | Focus |
|--------|---------|-------|
| Utilization Rate | Billable hours / Available hours | 65-80% is typical target |
| Revenue per Employee | Total Revenue / FTE | Productivity measure |
| Project Margin | (Project Revenue - Direct Costs) / Project Revenue | By client, by type |
| Client Retention Rate | Clients retained / Starting clients | >85% annually |
| Backlog | Contracted but undelivered revenue | Forward visibility |

### Operational Health Dashboard
Structure operational reviews around four dimensions:
1. **Quality:** Error rates, defect rates, customer satisfaction scores, NPS
2. **Speed:** Cycle time, lead time, time-to-market, response time
3. **Cost:** Unit cost, cost-to-serve, overhead ratio, cost per transaction
4. **Throughput:** Output volume, capacity utilization, transactions processed

Track each on a trailing 13-week basis to separate signal from noise.

## Cost Structure Analysis

### Activity-Based Costing (ABC)
When overhead allocation distorts product profitability:
1. **Identify activities** that consume resources (order processing, customer support, quality inspection)
2. **Assign costs to activities** based on resource consumption
3. **Identify cost drivers** for each activity (orders processed, support tickets, inspections performed)
4. **Allocate activity costs to products/customers** based on their consumption of each activity

ABC reveals true cost-to-serve by customer and product — often showing that high-volume customers subsidize low-volume ones, or that "profitable" products are actually underwater once overhead is properly allocated.

### Cost Benchmarking
| Cost Category | Benchmark Approach | What Good Looks Like |
|--------------|-------------------|---------------------|
| COGS | % of revenue vs. industry peers | Improving or at/above peer median |
| S&M | % of revenue, CAC efficiency | Declining as % of revenue at scale |
| R&D | % of revenue vs. growth stage | 15-25% for growth SaaS, <10% for mature |
| G&A | % of revenue, cost per employee | <15% of revenue, declining with scale |
| Facilities | Cost per employee, cost per sq ft | At or below market rate |

### Zero-Based Budgeting Approach
For cost structure resets:
1. Start from zero — every expense must justify its existence against current strategy
2. Categorize: **Must-have** (regulatory, contractual) vs. **Should-have** (competitive necessity) vs. **Nice-to-have** (optimization)
3. Rank discretionary spend by ROI or strategic contribution
4. Set category-level envelopes, then allow reallocation within envelopes

## Process Efficiency

### Lean Principles Applied to Business Operations
- **Value stream mapping:** Trace every step from customer request to delivery; classify as value-adding, necessary non-value-adding, or waste
- **Eliminate waste (8 wastes):** Defects, Overproduction, Waiting, Non-utilized talent, Transportation, Inventory excess, Motion, Extra processing
- **Flow:** Remove batching where possible — smaller batch sizes reduce cycle time and WIP
- **Pull:** Produce based on demand signals, not forecasts, where feasible

### Throughput Analysis (Theory of Constraints)
1. **Identify the constraint** — the step with the lowest throughput in the end-to-end process
2. **Exploit the constraint** — ensure it is never idle, never processing defective inputs
3. **Subordinate everything else** — pace other steps to the constraint; excess capacity elsewhere is irrelevant
4. **Elevate the constraint** — invest to increase its capacity only after steps 2-3 are exhausted
5. **Repeat** — identify the new constraint

### Process Metrics
| Metric | Formula | Purpose |
|--------|---------|---------|
| Cycle Time | Time from start to completion of one unit | Speed |
| Lead Time | Time from customer request to delivery | Customer experience |
| Throughput | Units completed per time period | Capacity |
| WIP | Work-in-progress items at any point | Flow health (lower is better) |
| First Pass Yield | Units passing QC on first attempt / Total units | Quality |
| OEE | Availability × Performance × Quality | Equipment/asset effectiveness |

## Capacity and Resource Planning

### Capacity Planning Framework
```
Required Capacity = Demand Forecast / (Efficiency Rate × Utilization Target)
Capacity Gap = Required Capacity - Current Capacity
```

**Planning horizon considerations:**
- **Short-term (0-3 months):** Adjust staffing, overtime, outsourcing — use current demand run-rate
- **Medium-term (3-12 months):** Hire, train, lease equipment — use forecast with scenarios
- **Long-term (1-3 years):** Build facilities, develop capabilities — use strategic plan with wide confidence bands

### Workforce Productivity
| Metric | Formula | Application |
|--------|---------|-------------|
| Revenue per FTE | Total Revenue / Full-time Equivalents | Overall productivity |
| Cost per FTE | Total Compensation + Benefits / FTE | Labor cost management |
| Revenue per $ of Compensation | Revenue / Total Compensation | Return on human capital |
| Span of Control | Direct reports per manager | Organizational efficiency |
| Voluntary Turnover | Voluntary departures / Avg headcount | Talent retention |

### Make vs. Buy Analysis
| Factor | Make (In-house) | Buy (Outsource) |
|--------|----------------|-----------------|
| Control | High | Lower |
| Fixed Cost | Higher | Lower (variable) |
| Scalability | Limited by capacity | Elastic |
| Quality | Direct oversight | SLA-dependent |
| Strategic Value | Builds capability | Frees capacity |

Decision framework: **Make** when the activity is a core differentiator or requires deep institutional knowledge. **Buy** when the activity is commoditized, demand is volatile, or specialized expertise is needed only intermittently.

## Marketing Performance Analytics

### Funnel Analysis
```
Awareness → Interest → Consideration → Intent → Evaluation → Purchase
   ↓           ↓           ↓             ↓          ↓           ↓
[Impressions] [Clicks] [Leads]    [MQLs/SQLs] [Proposals] [Deals Won]
```

Track conversion rates between each stage. The stage with the lowest conversion rate (relative to benchmarks) is the primary optimization target.

### Channel Economics
| Channel | Metrics to Track | Healthy Signals |
|---------|-----------------|----------------|
| Paid Search | CPC, CTR, Conv Rate, ROAS | ROAS > 3x, declining CPC |
| Paid Social | CPM, CTR, CPA, ROAS | CPA below LTV threshold |
| Organic Search | Traffic, Rankings, Conv Rate | Growing traffic, stable/improving conv |
| Email | Open rate, CTR, Revenue per send | Growing list + stable engagement |
| Direct Sales | Pipeline, Win rate, Deal size, Cycle time | Growing pipeline + stable/improving win rate |

### Attribution and ROI
- **First-touch attribution:** Credits the channel that first introduced the customer — overstates top-of-funnel
- **Last-touch attribution:** Credits the channel that closed — overstates bottom-of-funnel
- **Multi-touch attribution:** Distributes credit across touchpoints — more accurate but harder to implement
- **Incrementality testing:** A/B test channels on vs. off to measure true marginal impact — gold standard but expensive

**Marketing ROI:**
```
Marketing ROI = (Revenue Attributable to Marketing - Marketing Spend) / Marketing Spend
```

Always calculate at the channel level, not just in aggregate. Aggregate ROI can mask a highly profitable channel subsidizing a money-losing one.

### Customer Cohort Analysis
Group customers by acquisition month/quarter and track:
- **Retention curve:** % of cohort still active at month 1, 3, 6, 12
- **Revenue curve:** Average revenue per customer over time (expansion vs. contraction)
- **LTV realization:** Cumulative revenue and margin per customer over time

Compare cohorts to identify: improving/deteriorating acquisition quality, impact of product changes, seasonal patterns in customer behavior.
