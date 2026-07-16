# Type Reference — Commerce

Product (merchant listing + product snippet), Review snippet, Software app, Subscription & paywalled content, Vacation rental.
Format: what it does · Google doc · required · recommended · JSON-LD · pitfalls. **Verify required properties against the linked Google doc before finalizing.**

---

## Product (`Product`) — two experiences
Doc (overview): https://developers.google.com/search/docs/appearance/structured-data/product
Google has **two** product experiences with different requirements:
- **Product snippet** — a normal blue result enriched with price/availability/rating/review. Any site with product pages.
- **Merchant listing** — shopping-focused experiences for pages where the product can be **bought directly**; stricter requirements (shipping, returns, etc.).
Docs: product snippet → .../product-snippet · merchant listing → .../merchant-listing

**Common core:**
- **Required:** `name`; and for a rich result at least one of `offers`, `review`, or `aggregateRating` (with the required sub-props below).
- **Recommended:** `image`, `description`, `brand` (`Brand`/`Organization`), `sku`/`gtin`/`mpn`, `aggregateRating`, `review`.

**`offers` (`Offer`):** `price` + `priceCurrency` (ISO 4217), `availability` (e.g. `https://schema.org/InStock`), `url`, `priceValidUntil`, `itemCondition`. Or `AggregateOffer` with `lowPrice`/`highPrice`/`offerCount`.
**Merchant listing extras:** `shippingDetails` (`OfferShippingDetails`) and `hasMerchantReturnPolicy` (`MerchantReturnPolicy`) are needed to avoid warnings and qualify for shopping surfaces.
**`aggregateRating`:** `ratingValue`, `reviewCount` or `ratingCount`, `bestRating`/`worstRating`.
**`review` (`Review`):** `author`, `reviewRating` (`ratingValue`, `bestRating`, `worstRating`).

```html
<script type="application/ld+json">
{ "@context":"https://schema.org","@type":"Product",
  "name":"PLACEHOLDER product","image":["https://example.com/p.jpg"],
  "description":"PLACEHOLDER","brand":{"@type":"Brand","name":"PLACEHOLDER"},
  "sku":"PLACEHOLDER",
  "offers":{"@type":"Offer","price":"19.99","priceCurrency":"USD",
    "availability":"https://schema.org/InStock","url":"https://example.com/product",
    "priceValidUntil":"2026-12-31","itemCondition":"https://schema.org/NewCondition"},
  "aggregateRating":{"@type":"AggregateRating","ratingValue":"4.6","reviewCount":"128"} }
</script>
```
- **Pitfalls:** **ratings/reviews not visible on the page**; using site/brand-wide reviews on a single product (self-serving — disallowed); `price` with currency symbol instead of numeric + `priceCurrency`; wrong `availability` enum URL; merchant-listing warnings for missing shipping/returns.

---

## Review snippet (`Review` / `AggregateRating`)
Star ratings on results. Allowed **only** on a defined set of schema types.
Doc: https://developers.google.com/search/docs/appearance/structured-data/review-snippet
- **Allowed host types include:** `Book`, `Course`, `CreativeWorkSeason`/`CreativeWorkSeries`, `Episode`, `Event`, `Game`, `HowTo` (deprecated), `LocalBusiness`, `MediaObject`, `Movie`, `Product`, `Recipe`, `SoftwareApplication`, `Organization` (limited). **Not** allowed to review an entire website/`Article` generically.
- **Required in a `Review`:** `author` (`Person`/`Organization`, with `name`), `reviewRating` (`ratingValue`; `bestRating`/`worstRating` if scale ≠ 5).
- **`AggregateRating` required:** `ratingValue` + (`ratingCount` or `reviewCount`).
- **Rules:** reviews must be **genuine** and **visible on the page**; no self-serving reviews (a business reviewing itself); don't aggregate reviews you don't host.
- **Pitfalls:** attaching reviews to a disallowed type; invisible/aggregated third-party reviews; single-review pages using `AggregateRating`.

---

## Software app (`SoftwareApplication`)
App info rich result with rating, price, OS.
Doc: https://developers.google.com/search/docs/appearance/structured-data/software-app
- **Required:** `name`, and **`aggregateRating`** (`ratingValue` + `ratingCount`/`reviewCount`), plus **one of** `offers` (with `price`/`priceCurrency`; `0` for free) or an equivalent, and `applicationCategory` and `operatingSystem`.
- **Pitfalls:** missing rating (this feature centers on it); ratings not shown on page.

---

## Subscription & paywalled content (`isAccessibleForFree` + `hasPart`)
Lets Google understand paywalled content without treating it as **cloaking** (serving Googlebot different content than users). Pairs with `Article`/`NewsArticle`/etc.
Doc: https://developers.google.com/search/docs/appearance/structured-data/paywalled-content
- **Add to the CreativeWork:** `isAccessibleForFree: false`, and `hasPart` → `WebPageElement` with `isAccessibleForFree:false` and a `cssSelector` marking the paywalled section(s).
```html
"isAccessibleForFree": false,
"hasPart": { "@type":"WebPageElement","isAccessibleForFree":false,"cssSelector":".paywall" }
```
- **Why it matters:** without it, showing Googlebot full text but users a paywall can look like cloaking. This is the sanctioned way.
- **Pitfalls:** `cssSelector` not matching the actual gated element; marking free content as paid.

---

## Vacation rental (`VacationRental`)
For vacation-rental listing platforms; requires **Google onboarding / partner program**, not just on-page markup.
Doc: https://developers.google.com/search/docs/appearance/structured-data/vacation-rental
- Uses `VacationRental` with `name`, `image`, `latitude`/`longitude`/`address`, `numberOfBedrooms`/`Bathrooms`, `amenityFeature`, `aggregateRating`, `containsPlace`.
- **Flag to the user:** this is a program/feed-based feature — check eligibility before investing.
