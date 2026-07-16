# Type Reference — Content & Publishing

Article, Breadcrumb, Carousel, Q&A, Education Q&A, Discussion forum, FAQ, Course / Course list, Speakable, Fact check.
Format: what it does · Google doc · required · recommended · JSON-LD · pitfalls. **Verify required properties against the linked Google doc before finalizing.**

---

## Article (`Article` / `NewsArticle` / `BlogPosting`)
Makes news, blog, and sports content eligible for enhanced article treatment (headline + image in Top stories / news surfaces).
Doc: https://developers.google.com/search/docs/appearance/structured-data/article
- **Use the most specific type:** `NewsArticle`, `BlogPosting`, or `Article`.
- **Required:** none are strictly required by Google for basic eligibility, but effectively you need `headline`, and Google strongly expects `image`, `datePublished`, `author`.
- **Recommended:** `headline` (≤110 chars), `image` (multiple high-res, 16:9/4:3/1:1), `datePublished` + `dateModified` (ISO 8601), `author` (as `Person`/`Organization` with `name` and `url`/`sameAs`), `publisher` (`Organization` + `logo`), `dateline`, `articleSection`.
- **Author:** use a nested `Person` (link to a Profile page — see `types-entity-jobs.md`) for author authority.
```html
<script type="application/ld+json">
{ "@context":"https://schema.org","@type":"NewsArticle",
  "headline":"PLACEHOLDER headline (<=110 chars)",
  "image":["https://example.com/16x9.jpg","https://example.com/4x3.jpg","https://example.com/1x1.jpg"],
  "datePublished":"2026-07-15T08:00:00-05:00","dateModified":"2026-07-15T09:30:00-05:00",
  "author":[{"@type":"Person","name":"PLACEHOLDER Author","url":"https://example.com/author/name"}],
  "publisher":{"@type":"Organization","name":"Example News","logo":{"@type":"ImageObject","url":"https://example.com/logo.png"}} }
</script>
```
- **Pitfalls:** `headline` too long; author as a plain string (prefer nested `Person`); non-crawlable images; `dateModified` earlier than `datePublished`.

---

## Breadcrumb (`BreadcrumbList`)
Shows a readable hierarchy in the result instead of the raw URL; supports sitelinks quality.
Doc: https://developers.google.com/search/docs/appearance/structured-data/breadcrumb
- **Required:** `itemListElement` → array of `ListItem`, each with `position` (1-based int), `name`, and `item` (absolute URL) — `item` is omitted on the **last** item (current page).
- **Recommended:** provide the full path from home to current page. Multiple breadcrumb trails allowed (multiple `BreadcrumbList` objects).
```html
<script type="application/ld+json">
{ "@context":"https://schema.org","@type":"BreadcrumbList",
  "itemListElement":[
    {"@type":"ListItem","position":1,"name":"Home","item":"https://example.com/"},
    {"@type":"ListItem","position":2,"name":"Guides","item":"https://example.com/guides/"},
    {"@type":"ListItem","position":3,"name":"This Page"}
  ] }
</script>
```
- **Pitfalls:** including `item` on the last element; non-sequential `position`; trail not matching the on-page/URL hierarchy.

---

## Carousel (`ItemList`)
A host carousel (list-style rich result) for eligible types — combine `ItemList` with per-item types (Recipe, Course, Movie, Product, Article-type "list"). All items must be from the **same site**.
Doc: https://developers.google.com/search/docs/appearance/structured-data/carousel
- **Required:** `ItemList` with `itemListElement` → `ListItem`s in order, each `position` + a `url` to a page with the full item markup (summary page) **or** full inline item markup (all-in-one page).
- **Pitfalls:** mixing item types; items pointing off-site; missing per-item detail markup on the target pages.

---

## FAQ (`FAQPage`)  ⚠ gated
Doc: https://developers.google.com/search/docs/appearance/structured-data/faqpage
- **Status:** FAQ rich results are **limited to authoritative government and health sites** (2023). For other sites the markup is valid schema but **won't produce a rich result** — set expectations; only recommend it for gov/health.
- **Required (schema):** `mainEntity` → array of `Question`, each with `name` (the question) and `acceptedAnswer` (`Answer` with `text`).
- **Rules:** Q&A must be visible on the page; only for FAQ content authored by the site (not a user-submitted Q&A forum — use Q&A for that).

---

## Q&A (`QAPage`)
For pages where **users** post one question and community answers (forum/support thread with a single question). Not for FAQ (site-authored) content.
Doc: https://developers.google.com/search/docs/appearance/structured-data/qapage
- **Required:** `QAPage` with `mainEntity` → one `Question` (`name`, `answerCount`, and `acceptedAnswer` and/or `suggestedAnswer`, each an `Answer` with `text` and `url`; `upvoteCount` recommended).
- **Pitfalls:** using it for FAQ or product-description content; multiple questions (use one primary `Question`).

---

## Education Q&A (`Quiz`)
Practice-problem / education quiz rich result for flashcard-style Q&A on education sites.
Doc: https://developers.google.com/search/docs/appearance/structured-data/education-qa
- **Required:** `Quiz` with `about` (concept), `hasPart` → `Question`s (with `eduQuestionType`, `acceptedAnswer`, `suggestedAnswer`). Verify current property set in the doc.

---

## Discussion forum (`DiscussionForumPosting`)
For forum/community platforms where people share perspectives; eligible for forum/profile-attributed treatment.
Doc: https://developers.google.com/search/docs/appearance/structured-data/discussion-forum
- **Required:** `DiscussionForumPosting` with `author`, `datePublished`, and either `text` or `image`/`video`; `comment` (nested `Comment`s), `interactionStatistic` (views/likes) recommended.
- **Related:** pair with **Profile page** (`types-entity-jobs.md`) for the author. Use `ProfilePage` for the user-profile pages themselves.
- **Pitfalls:** using it for site-authored articles (use `Article`) or for a single-question support page (use `QAPage`).

---

## Course (`Course`) & Course list
Course info and course-list carousels for educational providers.
Doc: https://developers.google.com/search/docs/appearance/structured-data/course-info · list: .../course
- **Required (`Course`):** `name`, `description`, and `provider` (`Organization`) / `offers` / `hasCourseInstance` per current doc.
- **Recommended:** `courseCode`, `hasCourseInstance` (`courseMode`, `courseWorkload`, `startDate`), `offers` (price), `aggregateRating`.
- **Course list:** wrap `Course` items in an `ItemList` (see Carousel).

---

## Speakable (`speakable`)  — news, limited
Marks sections suitable for text-to-speech (Google Assistant news). Availability limited (English news; check surface).
Doc: https://developers.google.com/search/docs/appearance/structured-data/speakable
- **Used inside** `Article` via `speakable` → `SpeakableSpecification` with `cssSelector` or `xpath` pointing at the readable headline/summary.
- **Pitfalls:** selecting long or non-summary content; treating it as broadly available.

---

## Fact check (`ClaimReview`)
Fact-check badge for eligible fact-checking publishers (must meet Google's eligibility/authoritativeness criteria).
Doc: https://developers.google.com/search/docs/appearance/structured-data/factcheck
- **Required:** `ClaimReview` with `claimReviewed`, `reviewRating` (`ratingValue`, `bestRating`, `worstRating`, `alternateName`), `itemReviewed`, `url`, `author`.
- **Eligibility:** only for sites that do genuine fact-checking and meet Google News criteria; one claim per markup.
