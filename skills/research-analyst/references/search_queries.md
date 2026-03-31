# Search Query Templates

Pre-defined search query templates organized by subject type. Adapt these to the specific research target.

## Date Placeholders

Use dynamic date insertion based on current date:
- **Today**: `[current_date]` (e.g., 2026-03-29)
- **30 days ago**: `[current_date - 30 days]` (e.g., 2026-02-27)
- **7 days ago**: `[current_date - 7 days]` (e.g., 2026-03-22)

---

## Company-Focused Queries

### General Company News
```
"[Company Name]" news OR announcement OR update after:[30_days_ago]
```

### Product & Launches
```
"[Company Name]" launch OR release OR "new product" OR "new feature" after:[30_days_ago]
```

### Funding & Financial
```
"[Company Name]" funding OR investment OR revenue OR IPO OR acquisition after:[30_days_ago]
```

### Leadership & Organizational
```
"[Company Name]" CEO OR hire OR layoff OR restructuring OR appointment after:[30_days_ago]
```

### Press Releases
```
"[Company Name]" press release OR "announces" OR "announced" after:[30_days_ago]
```

### Partnerships
```
"[Company Name]" partnership OR collaboration OR "partners with" OR integration after:[30_days_ago]
```

---

## Industry / Sector Queries

### General Industry News
```
"[Industry]" news OR trends OR market OR developments after:[30_days_ago]
```

### Regulation & Policy
```
"[Industry]" regulation OR policy OR legislation OR compliance OR "new rules" after:[30_days_ago]
```

### Market Movements
```
"[Industry]" market share OR growth OR decline OR forecast OR report after:[30_days_ago]
```

### Innovation & Technology
```
"[Industry]" innovation OR breakthrough OR technology OR "new approach" after:[30_days_ago]
```

### Major Players
```
"[Industry]" leading companies OR "market leader" OR competitive landscape after:[30_days_ago]
```

### Events & Conferences
```
"[Industry]" conference OR summit OR expo OR event OR keynote after:[30_days_ago]
```

---

## Topic / Technology Queries

### General Topic Coverage
```
"[Topic]" news OR update OR development OR announcement after:[30_days_ago]
```

### Adoption & Use Cases
```
"[Topic]" adoption OR "use case" OR implementation OR deployment after:[30_days_ago]
```

### Research & Breakthroughs
```
"[Topic]" research OR breakthrough OR study OR paper OR discovery after:[30_days_ago]
```

### Controversy & Debate
```
"[Topic]" controversy OR debate OR criticism OR concern OR risk after:[30_days_ago]
```

### Funding & Investment
```
"[Topic]" investment OR funding OR startup OR venture capital after:[30_days_ago]
```

---

## Competitor Set Queries

### Head-to-Head Comparison
```
"[Company A]" vs "[Company B]" OR "[Company A]" "[Company B]" comparison after:[30_days_ago]
```

### Competitive Landscape
```
"[Company A]" OR "[Company B]" OR "[Company C]" market OR competition after:[30_days_ago]
```

### Individual Competitor News (repeat per competitor)
```
"[Competitor Name]" news OR announcement OR launch after:[30_days_ago]
```

### Market Share & Positioning
```
"[Industry]" market share "[Company A]" OR "[Company B]" after:[30_days_ago]
```

---

## Advanced Techniques

### Boolean Operators

#### AND (Both terms must be present)
```
"[Topic]" AND "breakthrough" AND "2026"
```

#### OR (At least one term must be present)
```
"[Term A]" OR "[Term B]" OR "[Term C]"
```

#### NOT (Exclude terms)
```
"[Topic]" AND "news" NOT "[irrelevant term]"
```

### Source-Specific Filters

#### News Sites Only
```
site:reuters.com "[Topic]" OR site:bloomberg.com "[Topic]"
```

#### Trade Publications
```
site:[industry-pub].com "[Topic]" after:[30_days_ago]
```

#### Company Blog / Newsroom
```
site:[company].com/blog OR site:[company].com/newsroom after:[30_days_ago]
```

### Date Filters

| Range | Filter |
|-------|--------|
| Last 24 hours | `after:[yesterday]` |
| Last 7 days | `after:[7_days_ago]` |
| Last 30 days (default) | `after:[30_days_ago]` |
| Last 90 days | `after:[90_days_ago]` |
| Custom range | `after:[start_date] before:[end_date]` |
