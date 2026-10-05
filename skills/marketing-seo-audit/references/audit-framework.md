# Audit Framework

Layers run in this order. A failure in an earlier layer makes later layers moot: a noindexed page needs no title polish.

| # | Layer | Question | Scorer category |
|---|---|---|---|
| 1 | Crawl and indexation | Can search engines find and keep the page? | `technical` |
| 2 | Technical foundations | Is the site fast, secure, mobile-ready? | `technical`, `performance` |
| 3 | Structure | Can users and crawlers reach pages in few steps? | `architecture` |
| 4 | On-page | Does each page say what it is about? | `on_page`, `images` |
| 5 | Content quality | Does the page deserve to rank? | `content` |
| 6 | Structured data and AI readiness | Can machines read it cleanly? | `schema`, `ai_readiness` |

Authority and backlinks: audit only with a backlink tool. Without one, mark the layer "not assessed". Never guess link profiles.

## 1. Crawl and indexation

**robots.txt**
- No rule blocks pages that should rank, or the CSS/JS needed to render them.
- Sitemap line present.
- Remember: robots.txt blocks crawling, not indexing. A blocked URL can stay indexed. To remove a page, use `noindex` and leave it crawlable.

**XML sitemap**
- Reachable, submitted in Search Console.
- Lists only canonical, indexable URLs that return 200. No redirects, no noindex, no parameter URLs.
- `lastmod` is true. A sitemap that stamps every URL with today's date teaches crawlers to ignore it.
- Under 50,000 URLs and 50 MB per file; use a sitemap index above that.

**Index status**
- Compare indexed count (Search Console Pages report) against expected count. Large gaps are the top finding.
- Read the reasons: "Crawled, currently not indexed" points at quality; "Discovered, not indexed" points at crawl budget or weak internal links; "Duplicate, Google chose different canonical" points at canonical conflicts.

**Indexation faults to hunt**
- `noindex` on pages that should rank (check meta tag and `X-Robots-Tag` header).
- Canonical points to a different page, to a redirect, or to a 404.
- Redirect chains or loops. One hop is the limit.
- Soft 404s: thin or empty pages that return 200.
- Duplicates without a canonical: http/https, www/non-www, trailing slash, parameters.

**Crawl budget** (only matters above roughly 10,000 URLs or with heavy faceting)
- Parameter and faceted URLs controlled.
- No session IDs in URLs.
- Infinite scroll has paginated, linked fallbacks.

## 2. Technical foundations

- **HTTPS everywhere.** Valid certificate, no mixed content, http redirects to https in one hop. HSTS is a bonus.
- **Mobile.** Responsive layout, viewport tag, readable tap targets, same content as desktop. Google indexes the mobile version.
- **Speed.** Triage with `core-web-vitals-triage.md`.
- **Status codes.** Real 404/410 for gone pages; 301 for permanent moves. See `url-patterns.md`.
- **JavaScript rendering.** Compare raw HTML with rendered DOM. If titles, links, or body copy exist only after JS runs, flag the render dependency.

## 3. Structure

Run `site-structure.md` and `internal-linking.md`. Feed `scripts/sitemap_structure.py` output into the `architecture` category.

## 4. On-page

Run `scripts/seo_page_checker.py` on each key template, not on every page. Sample at least one page per template (home, category, product or article, landing).

| Element | Pass | Frequent fault |
|---|---|---|
| Title | Unique, 30-60 chars, main topic first, brand last | Duplicates, truncation, stuffing, missing |
| Meta description | Unique, ~70-160 chars, states the benefit | Duplicates, auto-generated filler. Google may rewrite it anyway |
| H1 | One per page, matches the topic | Several, none, or used for styling |
| Heading order | H1 > H2 > H3, no skips | Headings used as font sizes |
| Images | Descriptive file name, accurate alt text, modern format, lazy loading below the fold, explicit width and height | Missing alt, 3 MB hero images. Decorative images use `alt=""` on purpose |
| Internal links | Descriptive anchors, working targets | Orphans, "click here", broken links |
| Keyword targeting | One primary intent per page; title, H1, and URL agree | Two pages fighting for one query (cannibalization) |

**Cannibalization test.** Search Console, Performance, filter by query: two or more URLs sharing impressions for one query means a conflict. Fix by merging, re-targeting one page, or canonicalizing.

## 5. Content quality

- Page matches the search intent behind its target query (informational, commercial, transactional, navigational). Check the live results: what formats rank?
- Depth matches the topic. Word count is a symptom, not a target; a 120-word page can satisfy "what time zone is Denver".
- Thin or duplicate pages: tag archives, empty categories, doorway pages, near-identical location pages.
- Freshness: visible dates are true; stale pages are refreshed or removed.
- E-E-A-T: `eeat-checklist.md`.
- Engagement data (time on page, bounce) is context for diagnosis, never a pass/fail test.

## 6. Structured data and AI readiness

- Structured data: `structured-data-checks.md`. To generate or fix markup, hand off to `marketing-seo-structured-data`.
- AI readiness (light-touch): answer-first openings under each H2, clear entity names, quotable facts with sources, author and date visible. Score only as `low` or `medium` severity.

## Typical faults by site type

| Site type | Look first for |
|---|---|
| SaaS | Thin feature pages; no comparison or alternative pages; blog not linked to product pages |
| E-commerce | Thin category pages; duplicate manufacturer descriptions; faceted URL duplicates; out-of-stock handling; missing Product markup |
| Publisher or blog | Stale posts; cannibalization; no topic clusters; missing author pages; tag archive bloat |
| Local | Inconsistent name, address, phone; copy-pasted city pages; no LocalBusiness markup; unclaimed business profile |

## Severity scale

| Severity | Meaning | Example |
|---|---|---|
| critical | Blocks indexing or causes a penalty | Site-wide noindex, robots block, hacked content |
| high | Clearly limits rankings | Redirect chains, thin pages at scale, failing CWV, canonical conflicts |
| medium | Real but local gain | Missing meta descriptions, orphan pages |
| low | Polish | Image format, heading order |
