# Type Reference — Entity, Local & Jobs

Organization, Local business, **Profile page / Person**, Event, Job posting, Employer aggregate rating, Estimated salary.
Format: what it does · Google doc · required · recommended · JSON-LD · pitfalls. **Verify required properties against the linked Google doc before finalizing.**

---

## Organization (`Organization`)
Establishes your entity for Google (feeds sitename, and merchant/knowledge-panel signals). Put it on the **home page / about page**.
Doc: https://developers.google.com/search/docs/appearance/structured-data/organization
- **Use the most specific subtype** where it fits (`OnlineStore`, `NewsMediaOrganization`, `Corporation`).
- **Required:** `name` (and Google recommends the block live at the site root/home page).
- **Recommended (rich, entity-strengthening):** `url`, `logo` (`ImageObject`; used for logo in Search/knowledge panels — square/standard, crawlable), `image`, `sameAs[]` (official social/Wikipedia/Wikidata URLs — key for entity reconciliation), `contactPoint` (`ContactPoint` with `telephone`, `contactType`), `address` (`PostalAddress`), `email`, `telephone`, `foundingDate`, `founder`, `taxID`/`vatID`/`duns`/`iso6523Code`, `numberOfEmployees`, `brand`.
```html
<script type="application/ld+json">
{ "@context":"https://schema.org","@type":"Organization","@id":"https://example.com/#org",
  "name":"Example Company","url":"https://example.com/",
  "logo":{"@type":"ImageObject","url":"https://example.com/logo.png"},
  "sameAs":["https://www.linkedin.com/company/example","https://x.com/example","https://www.wikidata.org/wiki/Q000"],
  "contactPoint":{"@type":"ContactPoint","telephone":"+1-555-0100","contactType":"customer support"} }
</script>
```
- Give it an `@id` so `Article.publisher`, `Product.brand`, `WebSite.publisher`, and Profile pages can reference it.
- **Pitfalls:** non-crawlable logo; `sameAs` to unofficial profiles; putting it only on inner pages.

---

## Local business (`LocalBusiness`)
Local rich treatment for physical businesses (hours, area, ratings). Best paired with a **Google Business Profile** (the biggest local-visibility lever).
Doc: https://developers.google.com/search/docs/appearance/structured-data/local-business
- **Use the most specific subtype:** `Restaurant`, `Dentist`, `Store`, `Hotel, etc.`
- **Required:** `name`, `address` (`PostalAddress`: `streetAddress`, `addressLocality`, `addressRegion`, `postalCode`, `addressCountry`). For departments/multiple locations, model each.
- **Recommended:** `image`, `telephone`, `priceRange`, `geo` (`GeoCoordinates` `latitude`/`longitude`), `url`, `openingHoursSpecification` (`dayOfWeek`, `opens`, `closes`), `menu`/`hasMenu` (food), `servesCuisine`, `acceptsReservations`, `department`, `sameAs`, `aggregateRating`/`review` (genuine, visible), `areaServed`.
```html
<script type="application/ld+json">
{ "@context":"https://schema.org","@type":"Restaurant",
  "name":"PLACEHOLDER","image":["https://example.com/store.jpg"],
  "address":{"@type":"PostalAddress","streetAddress":"123 Main St","addressLocality":"Austin","addressRegion":"TX","postalCode":"78701","addressCountry":"US"},
  "telephone":"+1-555-0100","priceRange":"$$","servesCuisine":"Mexican",
  "geo":{"@type":"GeoCoordinates","latitude":30.2672,"longitude":-97.7431},
  "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"11:00","closes":"22:00"}],
  "url":"https://example.com" }
</script>
```
- **Pitfalls:** inconsistent NAP (name/address/phone) vs. Google Business Profile & the web; fabricated reviews; missing `addressCountry`.

---

## Profile page / Person (`ProfilePage` + `Person`)  ★ author, about, bio, creator pages
For a page **about a single person or organization** — author bios, "About me", creator profiles, forum user profiles, team/employee pages (e.g. a personal site or portfolio). Enables author/creator attribution and profile treatment.
Doc: https://developers.google.com/search/docs/appearance/structured-data/profile-page
- **Required:** `ProfilePage` with `mainEntity` (`Person` **or** `Organization`) → **`name`** (real name preferred; if unavailable, `alternateName`, e.g. a handle, can satisfy it).
- **Recommended:** `dateCreated`, `dateModified` (ISO 8601), `alternateName` (handle), `description` (byline/credentials), `identifier`, `image` (crawlable, high-res, ≥ ~50k px; multiple aspect ratios help), `interactionStatistic` (`InteractionCounter` — followers etc.), `agentInteractionStatistic` (the person's own activity), `sameAs[]` (their other official profiles/homepage), plus `Person` details: `jobTitle`, `worksFor` (→ `Organization` `@id`), `url`, `knowsAbout`, `award`, `alumniOf`, `address`.
```html
<script type="application/ld+json">
{ "@context":"https://schema.org","@type":"ProfilePage",
  "dateCreated":"2024-01-10T00:00:00+00:00","dateModified":"2026-07-15T00:00:00+00:00",
  "mainEntity":{
    "@type":"Person","name":"PLACEHOLDER Full Name","alternateName":"PLACEHOLDER handle",
    "description":"PLACEHOLDER byline / credentials",
    "image":"https://example.com/photo.jpg","url":"https://example.com/",
    "jobTitle":"PLACEHOLDER","worksFor":{"@type":"Organization","name":"PLACEHOLDER"},
    "sameAs":["https://www.linkedin.com/in/PLACEHOLDER","https://x.com/PLACEHOLDER","https://github.com/PLACEHOLDER"],
    "interactionStatistic":{"@type":"InteractionCounter","interactionType":"https://schema.org/FollowAction","userInteractionCount":1200} } }
</script>
```
- **Valid uses:** author pages on a publication, "About me"/portfolio pages, forum/social user profiles, employee pages. **Invalid:** a store home page with mixed content, or a page about an org not affiliated with the site.
- **Entity tip:** rich `sameAs` links (LinkedIn, Wikidata, Wikipedia, X, GitHub) are the strongest signal to reconcile the person into Google's Knowledge Graph. Reference the employer `Organization` by `@id`.
- **Pitfalls:** the page isn't actually focused on one entity; profile image not crawlable; no `name`/`alternateName`.

---

## Event (`Event`)
Event rich result (date, venue, tickets) in Search and event surfaces.
Doc: https://developers.google.com/search/docs/appearance/structured-data/event
- **Required:** `name`, `startDate` (ISO 8601 with timezone), `location` — a `Place` (with nested `PostalAddress`) for physical events, or a `VirtualLocation` (with `url`) for online events.
- **Recommended:** `endDate`, `eventStatus` (`EventScheduled`/`Cancelled`/`Postponed`/`Rescheduled` — mark changes), `eventAttendanceMode` (`Offline`/`Online`/`Mixed`), `image`, `description`, `offers` (`Offer`: `url`, `price`, `priceCurrency`, `availability`, `validFrom`), `performer`, `organizer`.
```html
<script type="application/ld+json">
{ "@context":"https://schema.org","@type":"Event",
  "name":"PLACEHOLDER Event","startDate":"2026-09-01T19:00:00-05:00","endDate":"2026-09-01T22:00:00-05:00",
  "eventStatus":"https://schema.org/EventScheduled","eventAttendanceMode":"https://schema.org/OfflineEventAttendanceMode",
  "location":{"@type":"Place","name":"PLACEHOLDER Venue","address":{"@type":"PostalAddress","streetAddress":"1 Venue Rd","addressLocality":"Austin","addressRegion":"TX","postalCode":"78701","addressCountry":"US"}},
  "image":["https://example.com/event.jpg"],
  "offers":{"@type":"Offer","url":"https://example.com/tickets","price":"25","priceCurrency":"USD","availability":"https://schema.org/InStock","validFrom":"2026-06-01T00:00:00-05:00"} }
</script>
```
- **Pitfalls:** using `Event` for non-events (broadcasts, coupons, sales — a relevance violation); `startDate` without timezone; not updating `eventStatus` for cancellations.

---

## Job posting (`JobPosting`)
Eligibility for the Google **Jobs** experience. Also submit via a job sitemap / indexing where applicable.
Doc: https://developers.google.com/search/docs/appearance/structured-data/job-posting
- **Required:** `title`, `description` (full HTML description), `datePosted` (ISO 8601), `hiringOrganization` (`Organization` `name`, `sameAs`, `logo`), `jobLocation` (`Place` → `PostalAddress`) — or `jobLocationType: "TELECOMMUTE"` + `applicantLocationRequirements` for remote.
- **Recommended:** `validThrough`, `employmentType` (enum: `FULL_TIME`, `PART_TIME`, `CONTRACTOR`, `TEMPORARY`, `INTERN`, `VOLUNTEER`, `PER_DIEM`, `OTHER`), `baseSalary` (`MonetaryAmount` → `QuantitativeValue` `value`/`minValue`/`maxValue`, `unitText`), `identifier`, `jobBenefits`, `industry`, `directApply`.
- **Rules:** remove or set `validThrough` on expired postings (don't leave stale jobs live); one posting per page.
- **Pitfalls:** missing `datePosted`/`hiringOrganization`; salary not as `MonetaryAmount`; expired jobs still marked up.

---

## Employer aggregate rating (`EmployerAggregateRating`)
Adds an employer rating to the Google Jobs experience (for sites that rate employers).
Doc: https://developers.google.com/search/docs/appearance/structured-data/employer-rating
- **Required:** `EmployerAggregateRating` with `itemReviewed` (`Organization`), `ratingValue`, and `ratingCount` or `reviewCount` (`bestRating`/`worstRating` if scale ≠ 5).
- **Pitfalls:** self-rating your own company; ratings not backed by real reviews on the page.

---

## Estimated salary (`Occupation` / `MonetaryAmountDistribution`)
Salary-estimate rich result for sites that publish salary data by occupation/region.
Doc: https://developers.google.com/search/docs/appearance/structured-data/estimated-salary
- **Required:** `Occupation` (or `OccupationAggregationByEmployer`) with `name`, `occupationLocation`, and `estimatedSalary` → `MonetaryAmountDistribution` (`currency`, `duration`, `percentile10`…`percentile90`, `median`). Verify current shape in the doc.
- **Pitfalls:** applying to a single job (use `JobPosting.baseSalary`); missing distribution/location.
