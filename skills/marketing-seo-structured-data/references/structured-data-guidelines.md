# Structured Data — General Guidelines, Formats & Policies

The rules that apply to **every** type. Read this before generating or auditing any markup.
Canonical sources:
- Intro: https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data
- General guidelines & policies: https://developers.google.com/search/docs/appearance/structured-data/sd-policies
- Feature gallery (all types): https://developers.google.com/search/docs/appearance/structured-data/search-gallery

## How it works (and what it does NOT do)

Google reads structured data to understand a page and to become *eligible* to show a **rich result** (a richer SERP appearance than a plain blue link — stars, images, price, breadcrumbs, etc.).

- Correct markup = **eligibility only.** Google never guarantees a rich result will show, even for perfect markup.
- Structured data is **not a ranking boost** in itself. It can improve *click-through* by making the listing richer, but "add schema to rank higher" is a myth — say so.
- Google may show, change, or withhold rich results at its discretion, and features get added/removed over time.

## Formats

Google supports three, equally:
1. **JSON-LD — recommended.** A `<script type="application/ld+json">` block, usually in `<head>` (also valid in `<body>`; Google can read dynamically-injected JSON-LD). Easiest to maintain, least error-prone. **Default to this.**
2. **Microdata** — inline HTML attributes (`itemscope`, `itemtype`, `itemprop`).
3. **RDFa** — inline HTML5 attributes.

Vocabulary is **schema.org**. Where Google's per-feature doc and schema.org disagree on what's required, **Google's doc wins** for rich-result eligibility.

## General guidelines (technical)

- **Crawlable & indexable.** Don't block structured-data pages via `robots.txt`, `noindex`, or login/paywall gates that hide the markup from Googlebot. Images referenced in markup must be crawlable and indexable too.
- **Place markup on the page it describes.** Put the same markup on all duplicate pages, not only the canonical URL.
- **Render considerations.** If JSON-LD is injected by JavaScript, ensure it's present in the rendered DOM Google sees. Prefer server-side or static output when possible.
- **Use the most specific type** available (e.g. `Restaurant`, not just `LocalBusiness`; `NewsArticle`, not just `Article`).
- **Multiple entities:** one page can carry several items. Use nesting or an `@graph` array. Reference shared entities (Organization, Person) by `@id` instead of duplicating them.

## General guidelines (quality) & spam policies

Violations can trigger a **manual action** that removes rich-result eligibility (regular ranking is unaffected, but you lose the rich appearance). Rules:

- **Only mark up visible content.** Never mark up information that isn't present and visible to users. No hidden text created just to hold markup.
- **Be accurate & relevant.** Markup must represent the page truthfully. Don't miscategorize (a woodworking guide is not a `Recipe`; a broadcast is not an `Event`).
- **No deceptive/irrelevant markup:** no fake or self-serving reviews, no impersonation, no false affiliations, no ratings the page doesn't actually contain.
- **Completeness matters.** Include every **required** property; add **recommended** ones — richer, accurate data (real ratings, salary ranges, prices) both qualifies more features and reads better.
- **Follow Google's [spam policies](https://developers.google.com/search/docs/essentials/spam-policies)** for web search generally.
- **Reviews:** must be genuine, from real users or editorial; don't gate, fabricate, or aggregate reviews you don't host. Google restricts `review` snippets to a defined list of schema types (see `types-commerce.md`).

## Deprecated / gated features — do NOT recommend as live rich results

| Feature | Status | What to do instead |
|---------|--------|--------------------|
| **HowTo** (`HowTo`) | **Removed** from Search (2023). No longer a rich result on any surface. | Don't add HowTo markup for rich results. Structure the content well with headings/steps. |
| **FAQ** (`FAQPage`) | **Gated** (2023): FAQ rich results show only for **authoritative government and health** sites. | Only recommend FAQ markup for rich results if the site is gov/health. Otherwise the markup is valid schema but won't yield a rich result — set expectations. |
| **Sitelinks search box** (`WebSite` `SearchAction`) | Rich result **removed** (2024). | `WebSite` markup can still help establish the **sitename**; the search box itself no longer renders. |
| **Guided recipes / some voice surfaces** | Availability varies by surface/region. | Verify against the current Google doc before promising. |

Because features change, when a user is investing effort in a feature, **fetch the canonical Google doc** (linked per-type) to confirm it's still live before recommending it.

## Choosing what to implement (priority heuristic)

1. **Foundational for every site:** favicon, a stable sitename signal (`WebSite`/`Organization`), correct titles/meta, `BreadcrumbList` on nested pages. (See `search-appearance-features.md`.)
2. **The page's primary entity:** Article, Product, LocalBusiness, Event, JobPosting, Recipe, Profile page, etc. — pick the single best-fit type.
3. **Supporting enrichers:** review snippets, images/video, Organization details, ratings — where the data is genuine.
4. Skip deprecated/gated features unless the site qualifies.

Sequence by **impact ÷ effort**: sitewide foundations first, then the highest-value primary entity, then enrichers.
