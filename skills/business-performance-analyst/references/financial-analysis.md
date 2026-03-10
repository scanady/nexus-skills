# Financial Analysis Reference

## Table of Contents
- [P&L Analysis Framework](#pl-analysis-framework)
- [Margin Analysis](#margin-analysis)
- [Cash Flow Analysis](#cash-flow-analysis)
- [Financial Ratio Toolkit](#financial-ratio-toolkit)
- [Variance Analysis Methods](#variance-analysis-methods)
- [Unit Economics](#unit-economics)
- [Valuation Fundamentals](#valuation-fundamentals)

---

## P&L Analysis Framework

### Revenue Decomposition
Break revenue changes into orthogonal drivers:
- **Volume effect:** Change in units sold × prior period price
- **Price effect:** Change in average price × current period volume
- **Mix effect:** Shift in proportion of high/low-margin products at constant total volume
- **Currency effect:** (if multi-currency) Impact of FX rate changes on reported revenue

Always decompose before diagnosing. A flat revenue line can mask offsetting volume declines and price increases — which require opposite interventions.

### Cost Structure Analysis
- **Fixed vs. Variable:** Classify every cost line. Fixed costs create operating leverage (amplify both gains and losses as revenue scales). Variable costs track revenue and are the primary lever for gross margin improvement.
- **Direct vs. Indirect:** Direct costs trace to a product/service; indirect require allocation. Allocation method choices materially affect segment profitability — state the method.
- **Controllable vs. Uncontrollable:** In the analysis time horizon, which costs can management actually influence? Focus recommendations on controllable costs.

### Waterfall / Bridge Analysis
Walk from one period to the next by quantifying each driver:
```
Prior Period EBITDA
  + Revenue volume impact
  + Revenue price impact
  +/- Revenue mix impact
  - COGS increase (volume-driven)
  - COGS increase (input cost-driven)
  +/- OpEx changes (itemized)
  +/- One-time items
= Current Period EBITDA
```

## Margin Analysis

### Margin Stack
| Margin | Formula | What It Reveals |
|--------|---------|----------------|
| Gross Margin | (Revenue - COGS) / Revenue | Pricing power and production efficiency |
| Contribution Margin | (Revenue - Variable Costs) / Revenue | Per-unit profitability and scalability |
| Operating Margin | EBIT / Revenue | Core business profitability after overhead |
| EBITDA Margin | EBITDA / Revenue | Cash-generating efficiency (capital-structure-neutral) |
| Net Margin | Net Income / Revenue | Bottom-line profitability after all charges |

### Margin Expansion Levers
1. **Price increases** — Test elasticity before assuming revenue-neutral
2. **COGS reduction** — Procurement, process efficiency, supplier renegotiation
3. **Mix shift** — Grow high-margin products faster than low-margin
4. **Operating leverage** — Grow revenue faster than fixed costs
5. **SG&A efficiency** — Automation, span-of-control, zero-based budgeting

### DuPont Decomposition
Break ROE into component drivers to isolate the source of returns:
```
ROE = Net Margin × Asset Turnover × Equity Multiplier
    = (Net Income/Revenue) × (Revenue/Total Assets) × (Total Assets/Equity)
```
This reveals whether returns come from profitability, asset efficiency, or financial leverage.

## Cash Flow Analysis

### Free Cash Flow
```
Operating Cash Flow
  - Capital Expenditures
  - Capitalized Software / R&D (if applicable)
= Free Cash Flow (FCF)
```

### Cash Conversion Cycle
```
CCC = Days Sales Outstanding + Days Inventory Outstanding - Days Payable Outstanding
```
Lower CCC = faster cash generation. Compare to industry benchmarks and track trend.

### Working Capital Analysis
Focus areas:
- **AR aging:** Deteriorating collections signal customer health or process issues
- **Inventory turns:** Declining turns = capital trapped in unsold goods
- **AP management:** Extending payment terms improves cash but risks supplier relationships

## Financial Ratio Toolkit

### Profitability
| Ratio | Formula | Benchmark Use |
|-------|---------|--------------|
| Gross Margin % | Gross Profit / Revenue | Industry comparison, trend |
| Operating Margin % | EBIT / Revenue | Operational efficiency |
| ROIC | NOPAT / Invested Capital | Capital allocation effectiveness |
| ROA | Net Income / Total Assets | Asset productivity |

### Liquidity
| Ratio | Formula | Threshold |
|-------|---------|-----------|
| Current Ratio | Current Assets / Current Liabilities | >1.5 generally healthy |
| Quick Ratio | (Current Assets - Inventory) / Current Liabilities | >1.0 |
| Cash Ratio | Cash / Current Liabilities | Context-dependent |

### Leverage
| Ratio | Formula | Watch For |
|-------|---------|-----------|
| Debt-to-Equity | Total Debt / Equity | Rising trend, covenant thresholds |
| Interest Coverage | EBIT / Interest Expense | <2x is warning zone |
| Net Debt / EBITDA | (Total Debt - Cash) / EBITDA | >3x raises risk flags |

### Efficiency
| Ratio | Formula | Interpretation |
|-------|---------|---------------|
| Asset Turnover | Revenue / Total Assets | Higher = more revenue per asset dollar |
| Inventory Turnover | COGS / Average Inventory | Higher = faster inventory movement |
| Receivables Turnover | Revenue / Average AR | Higher = faster collections |

## Variance Analysis Methods

### Flexible Budget Variance
Split total variance into:
1. **Volume variance:** (Actual volume - Budgeted volume) × Budgeted rate
2. **Rate/Price variance:** (Actual rate - Budgeted rate) × Actual volume
3. **Mix variance:** Effect of selling a different product mix than planned
4. **Efficiency variance:** More/fewer inputs consumed per unit of output

### Materiality Thresholds
Focus analysis effort proportionally:
- Variances <5% of line item and <1% of revenue: note but don't investigate
- Variances 5-15% or >1% of revenue: brief root cause
- Variances >15% or >5% of revenue: full decomposition required

### Trend vs. Point-in-Time
Always compare variances against both budget AND prior period. A metric that meets budget but is deteriorating quarter-over-quarter signals a different problem than one that misses budget but is improving.

## Unit Economics

### SaaS / Subscription
| Metric | Formula | Health Check |
|--------|---------|-------------|
| LTV | ARPU × Gross Margin % × (1 / Churn Rate) | LTV/CAC > 3 |
| CAC | Total S&M Spend / New Customers Acquired | Payback < 12 months |
| CAC Payback | CAC / (ARPU × Gross Margin %) | Months to recover |
| Net Revenue Retention | (Starting MRR + Expansion - Contraction - Churn) / Starting MRR | >110% is strong |
| Magic Number | Net New ARR / Prior Quarter S&M Spend | >0.75 is efficient |

### E-commerce / Transaction
| Metric | Formula | Focus |
|--------|---------|-------|
| AOV | Revenue / Orders | Upsell/cross-sell effectiveness |
| Contribution per Order | AOV × Gross Margin - Variable Cost per Order | Must be positive |
| Repeat Purchase Rate | Returning Customers / Total Customers | Retention health |
| Customer Payback | CAC / (Annual Revenue per Customer × Margin) | < 1 year ideal |

### Marketplace / Platform
| Metric | Formula | Focus |
|--------|---------|-------|
| Take Rate | Platform Revenue / GMV | Pricing power |
| GMV per Active User | Total GMV / Active Users | Engagement depth |
| Supply/Demand Ratio | Active Suppliers / Active Buyers | Marketplace balance |
| Liquidity | % of Listings that Transact | Marketplace health |

## Valuation Fundamentals

### DCF Essentials
```
Enterprise Value = Σ (FCF_t / (1 + WACC)^t) + Terminal Value / (1 + WACC)^n
```
- Use unlevered FCF for enterprise value
- Terminal value typically 60-80% of total — test sensitivity aggressively
- WACC components: cost of equity (CAPM), cost of debt (after-tax), capital structure weights

### Comparable Multiples
| Multiple | When to Use |
|----------|-------------|
| EV/Revenue | Pre-profit companies, high-growth |
| EV/EBITDA | Profitable companies, capital-structure-neutral comparison |
| P/E | Mature companies with stable earnings |
| EV/FCF | Capital-intensive businesses |

Always adjust for: growth rate differences, margin differences, risk profile, and one-time items before concluding a company is "cheap" or "expensive" relative to comps.
