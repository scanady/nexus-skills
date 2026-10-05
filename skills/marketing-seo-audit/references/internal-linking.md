# Internal Linking

Internal links are free, fully in your control, and shape which pages get crawled, how much weight they get, and what topic they are tied to.

## Three jobs

1. **Reach.** Every page is reachable from the homepage in 3 clicks or fewer.
2. **Weight.** Strong pages (many external links) pass weight to the pages you want to rank.
3. **Meaning.** Anchor text and surrounding copy tell search engines what the target is about.

## Link strength, strongest first

1. In-body links inside a relevant page
2. Hub page links to its spokes
3. Navigation links (sitewide, so each carries less)
4. Footer links
5. Sidebar and auto "related posts" widgets

Widgets supplement manual links. They do not replace them, because they follow tags, not your ranking goals.

## Patterns

| Pattern | Best for | Rules |
|---|---|---|
| Hub and spoke | Topic clusters, SaaS feature groups | Hub links to every spoke; each spoke links back with a fitting anchor; deep pages link to their spoke and the hub; adjacent spokes link only where useful |
| Linear | Courses, multi-part guides, docs | Previous and next links; an index page lists all parts |
| Funnel | SaaS, lead gen | Blog posts link to feature pages; case studies link to features and pricing; pricing links to FAQ and demo. Money pages need contextual links, not nav links alone |
| Star | Homepage and top hubs | Homepage links to 5-8 priority sections, not to every post; each hub distributes downward |

## Anchor text

Heuristic mix across a site's internal links. These are working ranges, not Google rules:

| Type | Share | Example |
|---|---|---|
| Descriptive partial match | 50-60% | "cold email writing guide" |
| Exact match | 10-15% | "cold email templates" |
| Title or branded | 20-25% | "our guide to cold outreach" |
| Generic | under 5% | "learn more" |
| Naked URL | 0% | `https://example.com/guide` |

Write anchors that read as part of the sentence. Vary them: 15 links to one page should not carry one phrase 15 times. If every link to a key page says "our guide", the page gets reach but no topic signal.

## Find link opportunities

1. **Keyword overlap.** `site:example.com "cold email"` lists pages that mention the topic. Those without a link to the new page are candidates.
2. **Crawl export.** In a crawler's internal-links export: zero inbound links = orphan (fix first); one or two = at risk; heavy outbound with weak inbound = over-giver.
3. **Cluster gaps.** A hub that does not link to a key spoke means the cluster is broken.
4. **Old posts.** After publishing, update older posts to link to the new piece. High return, rarely done.

## Orphan recovery

1. **Find.** Sitemap or indexed URL list minus the crawl's linked-URL list.
2. **Classify.**

| Type | Action |
|---|---|
| Valuable page with no home | Add contextual links from related pages and its hub |
| Landing page meant to stay unlinked (ads, events) | Confirm it is not accidentally indexed; noindex if so |
| Duplicate or thin | Merge, canonicalize, or noindex |
| Outdated | 301 to the updated page, or 410 |

3. **Order.** Orphans with external links first, then orphans with search potential, then thin ones (fix the content before linking).

## Quarterly audit checklist

- [ ] Every key page within 3 clicks of the homepage
- [ ] Each hub links to all its spokes; each spoke links back
- [ ] No orphans
- [ ] Homepage links to 5-8 priority sections
- [ ] Footer holds key sections and legal pages only (about 10-15 links)
- [ ] Content published in the last 30 days has 3 or more contextual inbound links
- [ ] No broken internal links
- [ ] No internal link goes through a redirect
- [ ] Anchors are descriptive
- [ ] Pages with the most external links point onward to money pages

## Patterns that fail

- **Footer dump.** Dozens of links in the footer. Footer links carry little weight and add noise.
- **Widgets only.** Auto "related posts" with no hand-placed links.
- **Nav-only money pages.** Pricing and feature pages linked only from the menu. Add contextual links from posts.
- **Wrong anchors.** Strong flow of links, generic anchors, no topic signal.
- **Frozen archive.** Old posts that never link out to newer work.
