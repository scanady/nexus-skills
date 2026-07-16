# Type Reference — Media, Recipes & Data

Video, Image metadata, Recipe, Movie, Book, Math solver, Practice problems, Dataset, Learning video.
Format: what it does · Google doc · required · recommended · JSON-LD · pitfalls. **Verify required properties against the linked Google doc before finalizing.**

---

## Video (`VideoObject`)
Makes videos eligible for video rich results, thumbnails, key moments (chapters), live badge, and Video mode.
Doc: https://developers.google.com/search/docs/appearance/structured-data/video
- **Required:** `name`, `description`, `thumbnailUrl` (crawlable; 60×30px min, 16:9 preferred), `uploadDate` (ISO 8601).
- **Recommended:** `contentUrl` and/or `embedUrl`, `duration` (ISO 8601, e.g. `PT2M30S`), `expires` (only if it expires), `hasPart`/`Clip` for **key moments** (with `startOffset`, `url#t=`), `regionsAllowed`, `interactionStatistic` (views), `publication` + `BroadcastEvent` for **LIVE** badge.
```html
<script type="application/ld+json">
{ "@context":"https://schema.org","@type":"VideoObject",
  "name":"PLACEHOLDER title","description":"PLACEHOLDER description",
  "thumbnailUrl":["https://example.com/thumb.jpg"],
  "uploadDate":"2026-07-15T08:00:00-05:00","duration":"PT2M30S",
  "contentUrl":"https://example.com/video.mp4","embedUrl":"https://example.com/embed/123" }
</script>
```
- Also submit a **video sitemap** for large libraries.
- **Pitfalls:** non-crawlable thumbnail; missing `uploadDate`; key-moment offsets not matching the video.

---

## Image metadata / licensable images (`ImageObject` + `license`)
Adds a licensable badge and license details to images in Google Images.
Doc: https://developers.google.com/search/docs/appearance/structured-data/image-license-metadata
- **Required (for the badge):** `contentUrl` (or be the image), plus **either** `license` (URL to license terms) **or** `acquireLicensePage` (URL where a license can be acquired) — Google recommends **both**; the badge needs `acquireLicensePage`.
- Can also be expressed via **IPTC photo metadata** embedded in the image file.
- **Pitfalls:** pointing `license`/`acquireLicensePage` at non-relevant pages; image not crawlable.

---

## Recipe (`Recipe`)
Recipe rich result (image, rating, cook time), plus eligibility for host carousels and guided cooking surfaces.
Doc: https://developers.google.com/search/docs/appearance/structured-data/recipe
- **Required:** `name`, `image` (multiple high-res).
- **Recommended (strongly — needed for the rich features):** `recipeIngredient[]`, `recipeInstructions` (`HowToStep`s), `author`, `datePublished`, `description`, `prepTime`/`cookTime`/`totalTime` (ISO 8601 durations), `recipeYield`, `nutrition` (`calories`), `recipeCategory`, `recipeCuisine`, `keywords`, `video` (`VideoObject`), `aggregateRating` + `review` (genuine only).
- **Carousel:** wrap multiple `Recipe`s in `ItemList`.
- **Pitfalls:** fabricated ratings; instructions not present on page; durations not ISO 8601 (`PT30M`).

---

## Movie (`Movie`)
Movie carousel / movie info panels for film catalog pages.
Doc: https://developers.google.com/search/docs/appearance/structured-data/movie
- **Required:** `name`, `image`.
- **Recommended:** `dateCreated`/`datePublished`, `director` (`Person`), `aggregateRating`, `review`.
- Usually delivered as a **carousel** (`ItemList` of `Movie`).

---

## Book (`Book` actions)
Book knowledge-panel actions (find/buy/borrow). Requires an **onboarding process with Google** and a data feed — not purely on-page markup.
Doc: https://developers.google.com/search/docs/appearance/structured-data/book
- Uses `Book` / `Book` `Volume` with `workExample`, `bookFormat`, `isbn`, `potentialAction` (`ReadAction`).
- **Flag to the user:** this feature needs Google onboarding + feed submission, not just page markup.

---

## Math solver (`MathSolver`)
For sites that solve math problems; shows solvers for supported problem types.
Doc: https://developers.google.com/search/docs/appearance/structured-data/math-solvers
- **Required:** `MathSolver` with `mathExpression`-capable `potentialAction` (`SolveMathAction`) and `usageInfo`. Verify current shape in the doc. **Eligibility is limited** to qualifying math-solver sites.

---

## Practice problems (`Quiz` / `LearningResource`)
Practice-problem rich result for education content (STEM problems with solutions).
Doc: https://developers.google.com/search/docs/appearance/structured-data/practice-problems
- **Required:** `Quiz`/`Question` typed as `LearningResource` with `assesses` (skill), `educationalAlignment`, `acceptedAnswer`, `hasPart` questions. Verify against the doc; overlaps with Education Q&A (`types-content.md`).

---

## Dataset (`Dataset`)
Makes datasets discoverable in **Google Dataset Search** (not a classic web rich result).
Doc: https://developers.google.com/search/docs/appearance/structured-data/dataset
- **Required:** `name`, `description`.
- **Recommended:** `creator`, `citation`, `identifier` (DOI), `license`, `distribution` (`DataDownload` with `contentUrl`, `encodingFormat`), `temporalCoverage`, `spatialCoverage`, `variableMeasured`, `sameAs`.
- **Pitfalls:** treating it as a web rich result — it feeds Dataset Search; thin `description`.

---

## Learning video (`LearningVideo` / `Clip` + educational)
Educational video enrichment (concepts, key moments for learning).
Doc: https://developers.google.com/search/docs/appearance/structured-data/learning-video
- Builds on `VideoObject` (see Video) with education-specific properties (`learningResourceType`, `educationalLevel`, `hasPart` clips for concepts). Verify current requirements in the doc.
