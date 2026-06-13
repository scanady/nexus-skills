# Search Query Templates

Use dynamic dates based on the current date. Do not hardcode dates in the skill. Replace placeholders at runtime:

- `[today]` — current date in YYYY-MM-DD
- `[yesterday]` — current date minus 1 day
- `[week_ago]` — current date minus 7 days
- `[month_ago]` — current date minus 30 days
- `[quarter_ago]` — current date minus 90 days

## Broad Opportunity Discovery

### Emerging software opportunities
```text
("startup idea" OR "new SaaS" OR "software startup") ("pain point" OR "workflow" OR "automation") after:[month_ago]
```

### New product and launch signals
```text
("launched" OR "new product" OR "beta") ("AI tool" OR "developer tool" OR "workflow automation") after:[week_ago]
```

### Funding category signals
```text
("seed funding" OR "Series A" OR "pre-seed") ("AI" OR "software" OR "vertical SaaS" OR "developer tools") after:[month_ago]
```

### Underserved market language
```text
("still using spreadsheets" OR "manual process" OR "no good tool" OR "wish there was") (software OR SaaS OR app) after:[quarter_ago]
```

## AI and Software Platform Shifts

### AI capability shifts
```text
("open source model" OR "small language model" OR "edge AI" OR "local AI") (release OR benchmark OR deployment) after:[month_ago]
```

### Cost collapse signals
```text
("API pricing" OR "model pricing" OR "inference cost" OR "GPU cost") (lower OR cheaper OR reduced OR efficient) after:[month_ago]
```

### Agent/workflow gaps
```text
("AI agent" OR "workflow automation") ("manual" OR "approval" OR "compliance" OR "back office" OR "operations") after:[month_ago]
```

### Developer workflow pain
```text
(site:news.ycombinator.com OR site:github.com OR site:stackoverflow.com) ("pain" OR "frustrating" OR "workaround" OR "broken") ("developer tool" OR "CI" OR "testing" OR "docs" OR "deployment") after:[quarter_ago]
```

## Embedded, ESP32, and Edge Opportunities

### ESP32 product patterns
```text
("ESP32" OR "ESP32-S3" OR "ESP32-C3" OR "ESP32-C6") ("monitoring" OR "sensor" OR "automation" OR "commercial" OR "fleet") after:[quarter_ago]
```

### ESP32 pain and tooling gaps
```text
("ESP32" OR "ESP-IDF" OR "PlatformIO") ("problem" OR "issue" OR "hard to" OR "OTA" OR "provisioning" OR "fleet management") after:[quarter_ago]
```

### Edge AI and TinyML
```text
("TinyML" OR "edge AI" OR "on-device AI" OR "local inference") ("sensor" OR "industrial" OR "monitoring" OR "predictive maintenance") after:[quarter_ago]
```

### Home Assistant and local-first automation
```text
(site:community.home-assistant.io OR site:home-assistant.io) ("integration" OR "sensor" OR "automation" OR "energy" OR "privacy" OR "offline") after:[quarter_ago]
```

### Industrial IoT gaps
```text
("industrial IoT" OR "remote monitoring" OR "predictive maintenance") ("small business" OR "low cost" OR "retrofit" OR "wireless sensor") after:[quarter_ago]
```

## Underserved Niche Discovery

### Compliance and reporting pain
```text
("new regulation" OR "compliance deadline" OR "reporting requirement") ("software" OR "small business" OR "automation") after:[quarter_ago]
```

### Job posting workflow clues
```text
("operations analyst" OR "compliance analyst" OR "data coordinator") ("spreadsheet" OR "manual" OR "reporting" OR "workflow") after:[quarter_ago]
```

### Review mining
```text
(site:g2.com OR site:capterra.com) ("missing" OR "expensive" OR "hard to use" OR "poor support") ("software" OR "platform") [domain]
```

### Forum pain mining
```text
(site:reddit.com OR site:stackoverflow.com OR site:community.home-assistant.io) ("how do I" OR "is there a tool" OR "can't find" OR "wish") [domain]
```

## Domain-Specific Query Pattern

When the user provides a domain, combine it with these modifiers:

```text
[domain] ("manual process" OR "spreadsheet" OR "compliance" OR "monitoring" OR "alerts" OR "workflow") after:[quarter_ago]
[domain] ("startup" OR "new product" OR "funding" OR "launched") after:[month_ago]
[domain] ("forum" OR "reddit" OR "community") ("problem" OR "pain" OR "workaround") after:[quarter_ago]
[domain] ("sensor" OR "ESP32" OR "IoT" OR "edge AI" OR "automation") after:[quarter_ago]
```

## Query Strategy

1. Start with 2–3 broad signal queries.
2. Add 2–4 domain or technology-specific queries.
3. Add 1–2 pain-mining queries from communities or reviews.
4. For embedded asks, always include at least one ESP32/edge query and one customer/application query.
5. Fetch full pages for high-signal results before using them as evidence.
6. Deduplicate sources and map each source to one or more opportunity hypotheses.
