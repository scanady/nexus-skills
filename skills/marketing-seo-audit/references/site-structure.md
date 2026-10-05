# Site Structure

How a site is organized: URL depth, navigation, topic clusters. Use it to audit an existing structure, to plan a new one, or to plan a restructure. Linking tactics are in `internal-linking.md`; URL patterns per site type are in `url-patterns.md`.

## Intake for structure work

Collect before judging:
- Site URL, CMS, `sitemap.xml`, rough page count by section
- Business goal (leads, sales, authority, local) and the topics that must rank
- Known problems: orphans, duplicates, ranking drops
- Constraints: can the CMS change URLs? Can the team run bulk 301s? Dev time available?

## Mode A: audit existing structure

1. Run `scripts/sitemap_structure.py` on the sitemap. Read depth spread, top sections, hygiene problems, same-slug pairs.
2. Walk the live navigation: primary nav, breadcrumbs, footer, one deep page.
3. Compare the sitemap URL list to a crawl's internal-link list. URLs with no inbound internal links are orphans.
4. Rank the structural faults by SEO impact and by cost of fix.
5. Report as scorecard: depth spread, orphan count, URL hygiene counts, navigation gaps, then a prioritized list.

## Mode B: plan a new structure

1. Map business goals to sections.
2. Choose URL depth per content type (table below).
3. Define clusters: one pillar page per core topic, spokes beneath.
4. Specify navigation zones.
5. Deliver a text tree and a URL spec table (section, URL pattern, page purpose, indexable yes/no).

## Mode C: restructure an existing site

Treat as Mode A plus Mode B plus a redirect map from `url-patterns.md`. Never ship the new tree without the map. Every URL with links or traffic needs a 301 target.

## URL depth

Depth = number of path segments. `/` is 0, `/blog` is 1, `/blog/post` is 2.

| Depth | Example | Use when |
|---|---|---|
| 1 | `/pricing` | Core pages |
| 2 | `/blog/cold-email-tips` | Posts, product pages, standard sections |
| 3 | `/solutions/marketing/email-automation` | Real product families or nested services, where the middle level is a page worth ranking |
| 4+ | `/a/b/c/d/page` | Avoid. Flatten, or add shortcut links |

Test for a directory: is `/blog/email-marketing/` a real page you want to rank? If not, do not create the folder.

Targets for a healthy site: under 5% of URLs at depth 4+ (5-15% is acceptable, above 15% is poor). Every key page within 3 clicks of the homepage. Click depth and URL depth differ; check both.

## Navigation zones

| Zone | Job | Rules |
|---|---|---|
| Primary nav | Core sections | 5-8 items. Each item is a page worth ranking. A "Resources" label needs a real landing page |
| Secondary nav | Pages inside a section | Keeps equity inside the section |
| Breadcrumbs | Location, upward links | On every non-home page; each segment is a crawlable link; mark up with BreadcrumbList |
| Footer | Utility and key service links | Short. Not a dump of every post |
| Contextual links | In-body links | The strongest signal; see `internal-linking.md` |

Dropdowns: crawlers may follow them, but the parent item must itself be a clickable link to a real page.

## Topic clusters

A cluster is one pillar page plus the spokes that answer its sub-questions, all linked together. This is common practice and supports topical relevance. Google has not published it as a rule, so present it as a method, not a guarantee.

1. Pick 3-7 core topics for a focused site.
2. One pillar per topic, covering the topic broadly.
3. One spoke per major sub-question.
4. Pillar links to every spoke; each spoke links back to the pillar; adjacent spokes link only where relevant.
5. Build the content first. A cluster of empty or thin pages gains nothing from links.

## Frequent structural faults

| Fault | Harm | Fix |
|---|---|---|
| Orphan pages | No internal path in; weak discovery | Add contextual links, or retire the page |
| URL changes with no 301 | Lost links and traffic | Redirect map; fix internal links at the source |
| Same topic under two paths (`/blog/seo`, `/resources/seo`) | Competing duplicates | Merge, redirect, or canonicalize |
| Nesting at depth 4+ | Weak crawl priority, user confusion | Flatten |
| Footer links to every post | Diluted, noisy | Footer holds key sections and legal pages only |
| Nav built for the org chart, not the user | Users leave | Card-sort or tree-test labels |
| Homepage links to little | Strongest page wastes its equity | Link to the key hubs |
| Hub or category pages with no copy | Thin pages do not rank | Add a real intro and guidance |
| Parameter URLs (`?sort=&filter=`) indexable | Duplicate sprawl | Canonical to the clean URL, or block crawling |
| Nav links to contact and privacy as top items | Equity to low-value pages | Put money and content pages first |

## Deliverables by request

| Request | Deliver |
|---|---|
| Structure audit | Scorecard plus prioritized fix list |
| New structure | Text tree plus URL spec table |
| Internal linking plan | Cluster map, anchor guidance, orphan fix list |
| URL redesign | Before/after table, 301 map, rollout checklist |
| Cluster strategy | Cluster map per goal, content gaps, pillar brief |

Content questions (what to write) are out of scope here. Say what the structure needs; leave the editorial plan to a content strategy skill.
