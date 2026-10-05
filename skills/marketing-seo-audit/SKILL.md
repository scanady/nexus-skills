---
name: marketing-seo-audit
description: 'Audit a website''s general search health end to end: crawl, indexation, Core Web Vitals, on-page, E-E-A-T, and URL or internal-link structure, scored 0-100 with a prioritized fix plan. Use when asked to "audit my SEO", "why am I not ranking", "check my site''s technical SEO", "find orphan pages", or "review my URL structure". Not for AdSense approval.'
license: MIT
metadata:
  version: "1.0.0"
  domain: marketing
  triggers: score my site's SEO health, check my sitemap, fix my internal linking, diagnose an organic traffic drop, plan a site restructure, review title tags and meta descriptions, triage Core Web Vitals, run a pre-migration SEO check
  role: analyst
  scope: analysis
  output-format: report
  related-skills: marketing-seo-structured-data, marketing-seo-cro, marketing-seo-adsense-readiness, design-application-sitemap
---

# SEO Audit

## Role Definition

Senior technical SEO analyst. Audits whole sites across crawl, speed, structure, on-page, and content quality. Turns evidence into a scored, ranked fix plan. Separates what the data shows from what is guessed. Fills the general-SEO gap beside the AdSense-specific skills.

## Modes

Pick one from the request. Say which in one line. Two fit → ask once.

| Mode | Use when | Core steps |
|---|---|---|
| **Full audit** (default) | "audit my SEO", ranking or traffic problem, pre-launch or pre-migration check | Workflow below, all layers |
| **Structure audit or plan** | URL, navigation, orphan, restructure questions; or a new site tree | `references/site-structure.md`, `references/url-patterns.md` |
| **Internal linking plan** | Structure fine, weight and topic signals weak | `references/internal-linking.md` |

Structure work with a wider SEO problem → run Full audit; the Structure layer covers it.

## Workflow

### 1. Scope

Ask only what is missing. Never ask for what the user already gave.

- Site type (SaaS, shop, publisher, local), business goal, priority topics
- Pages in scope: whole site or named templates
- Evidence available: Search Console, analytics, crawl export, backlink tool, or public pages only
- Recent changes: migration, redesign, CMS or URL change, traffic drop date
- Top organic competitors

Evidence available sets the confidence ceiling. Public pages only → findings are `inferred` at best for index status and field data.

### 2. Collect evidence

- Fetch `robots.txt`, the sitemap, and the HTML of one page per template.
- Run `scripts/seo_page_checker.py --url <page> --json` on each sampled template.
- Run `scripts/sitemap_structure.py <sitemap> --json` for structure data.
- Pull field data for Core Web Vitals (PageSpeed Insights or CrUX), not lab data alone.
- Record each fact with its source. Tag every finding: **verified** (seen directly), **inferred** (derived from partial data), **assumed** (not checked; say what would confirm it).

### 3. Walk the layers in priority order

1. Crawl and indexation
2. Technical foundations, with Core Web Vitals triage
3. Structure and internal linking
4. On-page
5. Content quality and E-E-A-T
6. Structured data, then AI readiness

Details and checklists: `references/audit-framework.md`. A critical fault in layer 1 outranks every later finding; report it first.

### 4. Score

Write `checks.json`: one object per check with `category`, `check`, `result` (pass/warn/fail), `severity`, `detail` (the evidence). Run:

```
python3 scripts/seo_health_scorer.py --checks checks.json --profile <saas|ecommerce|local|publisher> --json
```

Categories not assessed stay out of the file. The scorer lists them as unscored; repeat that in the report. Never fill a check to make a category look complete.

### 5. Report

Use the structure in the next section. Lead with the verdict, not the method.

## Output Structure

1. **Verdict.** Score, grade, three to five top issues, quick wins. Three to five bullets.
2. **Findings**, grouped by layer. Each finding: Issue / Impact (high-medium-low) / Evidence + confidence tag / Fix / Priority.
3. **Prioritized action plan:** (1) fixes blocking indexation or ranking, (2) high-impact work, (3) quick wins, (4) long-term items. Quick wins stay separate from big work. Every action has an owner role and an order.
4. **Not assessed.** Layers or data skipped, and what access would unlock them.

Optional artifacts on request: keyword cannibalization map (query, competing URLs, canonical or merge action), site tree plus URL spec table, 301 redirect map, cluster map.

Write for a technically aware reader who is not an SEO specialist. Explain a term the first time it appears.

## Reference Guide

| Topic | Reference | Load when |
|---|---|---|
| Layers, checks, severity scale, faults by site type | `references/audit-framework.md` | Always, at step 3 |
| LCP, INP, CLS thresholds and fixes | `references/core-web-vitals-triage.md` | Speed or vitals appear in scope |
| Experience, expertise, authority, trust checks | `references/eeat-checklist.md` | Content layer; any YMYL site |
| JSON-LD review, retired features, policy faults | `references/structured-data-checks.md` | Schema appears in scope |
| Depth, navigation, clusters, modes A-C | `references/site-structure.md` | Structure audit or plan |
| URL patterns, redirects, canonicals, status codes | `references/url-patterns.md` | URL redesign, migration, duplicate problems |
| Link patterns, anchors, orphan recovery | `references/internal-linking.md` | Linking plan, orphan findings |

## Scripts

| Script | Run | Output |
|---|---|---|
| `scripts/seo_page_checker.py` | `--file page.html` or `--url <url>`, `--domain`, `--json` | One page, 0-100, 13 checks |
| `scripts/seo_health_scorer.py` | `--checks checks.json`, `--profile`, `--json`, `--demo` | Weighted site score, grade, ranked issues |
| `scripts/sitemap_structure.py` | file, URL, or `-` for stdin, `--json` | Depth spread, URL hygiene, same-slug pairs |

Python 3.8+, stdlib only. Page checker and sitemap tool fetch URLs when given one; the scorer is offline.

## Constraints

### MUST DO
- State the mode before work. Ask for missing scope once.
- Work through layers in priority order; report indexation faults first.
- Tag every finding verified, inferred, or assumed, with its evidence.
- Use field data (CrUX, real users) as the Core Web Vitals verdict; use lab data only to diagnose.
- Score through `seo_health_scorer.py`; show the unscored categories.
- Give every finding an issue, impact, evidence, fix, and priority.
- Say "eligible" for rich results, never "guaranteed".
- Check Google's current docs before claiming a feature or markup type still earns a rich result.
- Sample by template, not by page, on large sites.
- Hand structured data writing to `marketing-seo-structured-data`.

### MUST NOT DO
- Claim a ranking effect with no evidence or reasoning.
- Publish an "E-E-A-T score" as if Google issues one.
- Judge thin content by word count alone; compare against search intent.
- Treat robots.txt as a way to deindex a page.
- Recommend a redirect plan without a map and a check for chains.
- Guess backlink or authority data without a tool; mark it not assessed.
- Treat AdSense approval criteria as general SEO rules, or the reverse; use `marketing-seo-adsense-readiness` for AdSense.
- Mix content strategy (what to write) into a structure finding; note the gap and stop.
- Pad the plan: every action ties to a finding.
- Rank "quick wins" ahead of critical indexation faults.

## Output Checklist

1. Mode stated, scope confirmed
2. Evidence listed with sources; confidence tags on every finding
3. Layers walked in order; indexation first
4. Field data used for vitals, or the gap stated
5. `checks.json` scored; unscored categories named
6. Each finding has issue, impact, evidence, fix, priority
7. Action plan split into critical, high-impact, quick wins, long-term
8. "Not assessed" section present

## Knowledge Reference

Technical SEO, crawlability, indexation, robots.txt, XML sitemaps, canonicalization, redirects, status codes, Core Web Vitals (LCP, INP, CLS), CrUX, Lighthouse, Search Console, on-page optimization, E-E-A-T, YMYL, search intent, keyword cannibalization, schema.org JSON-LD, rich results eligibility, information architecture, topic clusters, hub and spoke, internal linking, anchor text, orphan pages, crawl depth, faceted navigation, site migration, 301 mapping
