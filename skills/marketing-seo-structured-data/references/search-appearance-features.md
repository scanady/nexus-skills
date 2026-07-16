# Search Appearance Features (non-structured-data)

How Google builds the parts of a result that structured data doesn't control: the **title link**, the **snippet**, the **favicon**, the **sitename**, and **sitelinks**. These are foundational — get them right before or alongside rich-result markup.
Canonical: https://developers.google.com/search/docs/appearance (Appearance section index).

## Title link (the blue clickable headline)

Google generates the title link mostly from your `<title>`, but may rewrite it using on-page `<h1>`/headings, anchor text, or other content if your title is poor.
Give Google a good title:
- One clear, descriptive, unique `<title>` per page. Front-load the primary topic; include the brand where useful.
- Avoid boilerplate ("Home", "Untitled"), keyword stuffing, and identical titles across pages.
- Keep it reasonably concise; long titles get truncated in the SERP.
- Match the visible `<h1>` intent — big mismatches invite a rewrite.
Doc: https://developers.google.com/search/docs/appearance/title-link

## Snippet (the description text under the title)

Google generates snippets dynamically — usually from page content, sometimes from the `<meta name="description">`. You influence but don't fully control it.
- Write a unique, accurate **meta description** per page (~1 concise sentence or two) summarizing that page. It's a *hint*, not a guarantee.
- Ensure the answer/value is in real, crawlable page text — Google often pulls the most relevant passage.
- Control snippet length/preview with robots meta tags if needed: `max-snippet`, `nosnippet`, `data-nosnippet`, `max-image-preview`.
- Don't stuff keywords; don't duplicate the same description sitewide.
Doc: https://developers.google.com/search/docs/appearance/snippet

## Favicon (the little icon next to your result on mobile)

To be eligible to show a favicon in Search:
- Provide a favicon referenced in the `<head>` of your **home page** with `<link rel="icon" href="…">` (or `shortcut icon`, `apple-touch-icon`). Google looks for it at the site root too.
- The favicon file and the home page must be **crawlable** (not robots.txt-blocked).
- Use a **square** image, a multiple of 48px (e.g. 48×48, 96×96, 144×144); it's rescaled to 48×48. Minimum viable is 8×8 but 48px-multiples are recommended.
- Supported formats include ICO, PNG, SVG, etc.
- Keep the icon **stable** and representative of the brand; it must not be inappropriate (e.g. a swastika) or Google won't show it.
- Use a valid `rel` and a `sizes` attribute when providing multiple.
Doc: https://developers.google.com/search/docs/appearance/favicon-in-search

## Sitename (the site's name shown above the title link)

Google chooses a sitename for the whole domain from several signals. To influence it:
- Add **`WebSite` structured data** on the home page with a `name` (and optional `alternateName` for a shorter form):
```html
<script type="application/ld+json">
{ "@context":"https://schema.org", "@type":"WebSite",
  "name":"Example Company", "alternateName":"EC", "url":"https://example.com/" }
</script>
```
- Reinforce with `og:site_name`, a consistent `<title>` suffix, `<h1>`, and the same name used consistently across the site.
- Sitename is chosen at the **domain** level (and for some subdomains). Use a real, consistent name; avoid frequent changes.
Doc: https://developers.google.com/search/docs/appearance/site-names

## Sitelinks (the extra sub-links under a result)

- **Fully automated** — you cannot mark up or request sitelinks. Google generates them from site structure.
- Help Google by using a clear, logical site hierarchy, descriptive internal link/anchor text, unique titles, and a `BreadcrumbList` (see `types-content.md`).
- The old **Sitelinks search box** rich result was removed (2024) — don't promise it.
Doc: https://developers.google.com/search/docs/appearance/sitelinks

## Breadcrumbs (display)

The breadcrumb trail shown in a result is driven by `BreadcrumbList` structured data — see `types-content.md` for the markup. It replaces the URL path in the result with a readable hierarchy.

## Images & videos in Search

- **Images:** serve high-quality, crawlable images; use descriptive `alt`, a stable URL, and a good filename; add an image sitemap for large sites. `ImageObject`/`license` metadata can add licensable badges (see `types-media.md`).
- **Videos:** `VideoObject` markup + a video sitemap make videos eligible for video rich results, key moments, and thumbnails (see `types-media.md`).
Docs: https://developers.google.com/search/docs/appearance/google-images · https://developers.google.com/search/docs/appearance/video

## Other appearance surfaces (context)

- **Knowledge panel / entity:** driven by Google's Knowledge Graph, not directly by your markup. You influence your *entity* via Organization/Person markup, `sameAs` links, Wikidata/Wikipedia presence, and Google Business Profile. You can't "add" a knowledge panel with schema alone.
- **Featured snippet:** algorithmically selected from well-structured, directly-answering page content; not a markup feature.
- **Attribution / authorship:** use clear bylines, `Article` `author`, and a Profile page for the author (see `types-entity-jobs.md`).

## Checklist for the appearance foundation
- [ ] Unique, descriptive `<title>` and `<meta name="description">` per page.
- [ ] Crawlable square favicon (48px multiple) linked from the home page `<head>`.
- [ ] `WebSite` markup + consistent naming for a stable sitename.
- [ ] Logical hierarchy + `BreadcrumbList` for breadcrumbs and better sitelinks.
- [ ] High-quality crawlable images (and video markup where relevant).
- [ ] Nothing blocked by robots.txt / noindex that you want to appear.
