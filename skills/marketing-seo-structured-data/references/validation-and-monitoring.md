# Validation, Testing & Monitoring

How to confirm markup is correct, deploy it, and diagnose "why isn't my rich result showing."

## The tools (what each is for)

| Tool | URL | Use it to |
|------|-----|-----------|
| **Rich Results Test** | https://search.google.com/test/rich-results | Check whether a page/snippet is **eligible for a Google rich result**, per feature. The authoritative eligibility check. Tests live URL or pasted code. |
| **Schema Markup Validator** | https://validator.schema.org/ | Validate **generic schema.org** syntax/vocabulary (no Google-feature opinion). Use for types Google doesn't have a rich result for. |
| **URL Inspection** (Search Console) | search.google.com/search-console | See how Google **actually rendered/indexed** the live page, incl. detected structured data; request indexing. |
| **Rich result status reports** (Search Console) | Search Console → Enhancements | Post-deploy: aggregate **valid / warning / error** counts per feature across the site, with examples. |
| **Performance report** (Search Console) | Search Console → Performance | Measure **impact**: filter by "Search Appearance" = the rich result; compare CTR/impressions before vs. after. |

Note: the legacy "Structured Data Testing Tool" is retired — use the Rich Results Test + Schema Markup Validator.

## Pre-deploy validation checklist

- [ ] **Parses** as valid JSON-LD (no trailing commas, correct quotes, one root object or an `@graph` array).
- [ ] `@context` is `https://schema.org` and `@type` is the most specific correct type.
- [ ] **All required properties** for the feature are present (verify against the type's Google doc).
- [ ] **Types/formats correct:** dates in **ISO 8601** (`2026-07-15` or `2026-07-15T09:00:00-05:00`), URLs **absolute** and crawlable, numbers unquoted where numeric, enums spelled exactly (e.g. `https://schema.org/InStock`, `EmploymentType` values).
- [ ] Every value **matches visible page content**; nothing fabricated or hidden.
- [ ] Referenced **images/URLs are crawlable** (not robots.txt-blocked, not behind auth).
- [ ] Shared entities referenced by `@id`; multi-entity pages nested or in `@graph`.
- [ ] Rich Results Test shows the intended feature **detected with no errors** (warnings on recommended props are OK but worth filling).

## Errors vs. warnings

- **Errors** = the item is **ineligible** for the rich result until fixed (missing required property, wrong type). Must fix.
- **Warnings** = eligible, but a **recommended** property is missing; adding it improves quality/appearance. Should fix where data exists.

## Deploy & monitor sequence

1. Validate in Rich Results Test (code, then live URL after deploy).
2. Deploy to the live, crawlable page (same markup on duplicates).
3. **URL Inspection** → confirm Google renders the markup; **Request indexing**.
4. Watch the **rich result status report** for valid/error counts as Google recrawls (can take days).
5. Track **Performance** (filter by the search appearance) for CTR/impression change. Structured data affects appearance/CTR, not ranking directly.

## "My markup is valid but no rich result shows" — decision tree

Eligibility ≠ display. Walk these in order:

1. **Is the feature still live?** Confirm it isn't deprecated/gated (HowTo removed; FAQ gated to gov/health; sitelinks search box removed). See `structured-data-guidelines.md`.
2. **Does the Rich Results Test detect it with zero errors?** If errors → fix required properties first.
3. **Is the page indexed?** URL Inspection. If not indexed, no rich result. Fix crawl/index/robots/noindex issues.
4. **Is the markup crawlable & rendered?** JS-injected JSON-LD must appear in the rendered DOM; images/URLs not blocked.
5. **Content quality / relevance:** Google withholds rich results on low-quality, thin, or policy-violating pages, and where markup doesn't match visible content.
6. **Manual action?** Search Console → Security & Manual Actions → "Structured data issue." A manual action removes eligibility until you fix and request review.
7. **Duplicate/canonical:** markup must be on the canonical (and ideally all duplicate) URLs.
8. **It's still Google's call + it takes time.** Even with everything correct, Google may choose not to show it, and recrawl/rollout takes days to weeks. Don't conclude failure prematurely.

## Common concrete mistakes

- Relative image/URL values instead of absolute `https://…`.
- Dates as `07/15/2026` instead of ISO 8601.
- Marking up content not visible on the page (e.g. reviews rendered only after login).
- Aggregate `AggregateRating`/`review` on a page that doesn't actually display those reviews.
- Wrong enum casing/URL (`InStock` vs `https://schema.org/InStock`).
- Multiple conflicting `@type` blocks for the same entity instead of one `@graph`.
- `Product` review snippet used to review the *whole site/brand* rather than a specific product (self-serving — disallowed).
- FAQ/HowTo markup added expecting rich results that no longer render.
