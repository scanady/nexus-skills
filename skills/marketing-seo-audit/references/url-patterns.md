# URL Patterns, Redirects, Canonicals

## Rules for every site

1. Lowercase only. `/Blog/Tips` and `/blog/tips` are different URLs.
2. Hyphens between words, never underscores.
3. No special characters, spaces, or encoded junk in the path.
4. One trailing-slash convention, enforced by 301.
5. No dates in the path unless the date is the content. Dates age a URL.
6. Include the main keyword if it reads naturally. Do not stuff. URL keywords are a small signal.
7. Keep under about 75 characters. Short and readable wins.
8. Stop words are fine when they keep the URL readable.

## Patterns by site type

### SaaS and B2B software

```
/features              /features/[feature]
/solutions/[use-case]  /solutions/[industry]
/pricing               /integrations/[tool]
/customers/[name]      /blog/[slug]
/changelog             /docs/[topic]/[subtopic]
```

- Feature, solution, and integration pages must be real landing pages with copy, not nav labels.
- Integration pages capture high-intent searches; build one per integration that has demand.
- Pick one home for articles (`/blog`), not three (`/resources`, `/learn`, `/content`).
- Avoid redundant suffixes: `/pricing`, not `/pricing-plans`.

### Blog and content sites

```
/[category]/[post-slug]     /guides/[slug]
/author/[author-slug]       /tools/[tool]
```

- Under about 500 posts, flat `/[post-slug]` or `/blog/[slug]` is fine. Above that, category folders help.
- Tag archives make thin duplicates at scale: noindex them, or give each real copy.
- Build real author pages; they carry the E-E-A-T trail.

### E-commerce

```
/collections/[category]/[subcategory]     /products/[product-slug]
/brands/[brand]                            /sale   /new-arrivals
```

- Variants (size, color): one canonical URL for the product; variants canonicalize to it unless each variant has its own demand and its own copy.
- Filter and sort URLs: canonicalize to the clean collection URL, or block crawling of parameter combinations.
- Category pages need copy and useful structure, not only a product grid.
- Discontinued products: 301 to the closest alternative, or return 410 with a helpful page.

### Local and service-area

```
Single site:   /services/[service]   /areas-served/[city]   /about   /contact
Multi-site:    /locations/[city]     /locations/[city]/[service]
```

- Each city page needs content specific to that place. Copy-pasted city pages are doorway pages.
- Use subfolders for most multi-location sites; use subdomains only for truly independent franchises.

## Redirect mapping for a restructure

Every old URL that has links or traffic gets one 301 to its new equivalent.

1. Export indexed URLs (Search Console) and the crawl list.
2. Export URLs with inbound links (backlink tool or Search Console Links report) and with organic traffic (analytics).
3. Map old to new, in priority order: Tier 1 externally linked, Tier 2 high organic traffic, Tier 3 the rest.
4. Implement server-side 301s. No JS redirects or meta refresh.
5. Update internal links to the new URLs; do not leave them pointing at redirects.
6. Resubmit the sitemap. Watch Search Console for new 404s and "redirect error" for several weeks.

Never: chain more than one hop; use 302 for a permanent move; leave old URLs live as duplicates.

## Canonicalization

`<link rel="canonical" href="https://example.com/the-page">`

A canonical is a strong hint, not a command. Make signals agree: internal links, sitemap, redirects, and canonical should all name the same URL.

| Situation | Canonical |
|---|---|
| http and https | https |
| www and non-www | One chosen host, plus 301 from the other |
| Trailing slash variants | One form, plus 301 |
| Filtered or sorted lists | Clean list URL |
| Paginated series | Each page canonicalizes to itself. Google no longer uses `rel=prev/next`; do not canonicalize page 2 to page 1 |
| Print versions, tracking-parameter URLs | The main URL |
| Syndicated copies | The original source |

Google retired the Search Console URL Parameters tool in 2022. Control parameters with canonicals, `noindex`, robots.txt, and clean internal links.

## Status codes

| Code | Meaning | Use |
|---|---|---|
| 200 | OK | Live page |
| 301 / 308 | Permanent redirect | Moved for good; passes signals |
| 302 / 307 | Temporary redirect | Real short-term moves only |
| 404 | Not found | Missing page; serve a helpful 404 page |
| 410 | Gone | Removed on purpose; slightly clearer signal than 404 |
| 503 | Unavailable | Maintenance; tells crawlers to retry |
