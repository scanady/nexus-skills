# Structured Data Checks

Scope: audit existing JSON-LD and decide what a page should carry. To write or fix markup, use `marketing-seo-structured-data`.

**Rule of the audit.** Valid markup makes a page eligible for a rich result. It never guarantees one. Say "eligible", not "will show".

## Always verify the live status

Google changes which types earn rich results. Before calling a type "missing opportunity", confirm it in Google's current structured data gallery and the Rich Results Test. The notes below were true at writing and have moved before.

## Types worth checking

| Type | Typical page | Note |
|---|---|---|
| Organization | Home | Name, logo, `sameAs` links. Every site |
| WebSite | Home | Site name. The sitelinks search box feature was retired in 2024 |
| BreadcrumbList | Any page below the top level | Must mirror the visible trail |
| Article / NewsArticle / BlogPosting | Posts | Needs author, dates, image |
| Product + Offer | Product pages | Price, availability; Review and AggregateRating only when real |
| LocalBusiness | Location pages | Address and hours match the visible page and the business profile |
| Recipe, Event, JobPosting, VideoObject, Course, SoftwareApplication | Matching pages | Follow the type's required properties |
| ProfilePage / Person | Author pages | Supports the E-E-A-T trail |

## Reduced or retired features

| Type | Status | Action |
|---|---|---|
| FAQPage | Rich result limited since Aug 2023 to well-known government and health sites | Keep only if the FAQ is real page content. Do not promise a SERP gain |
| HowTo | Rich result removed from Google Search in 2023 | Leave or remove. Do not sell it as a win |
| QAPage | Applies to single-question community pages, not FAQs | Check it is not misused |
| SpecialAnnouncement and other retired types | No longer processed | Remove |

## Validation checklist

Per page:
- [ ] JSON-LD, valid JSON (a trailing comma breaks the whole block)
- [ ] Passes the Rich Results Test; no errors in Search Console enhancement reports
- [ ] All required properties for the type are present
- [ ] Markup describes content that is visible on the page
- [ ] `@type` fits the page (no Review markup on a non-review page)
- [ ] Related entities linked by `@id` instead of repeated
- [ ] One Organization entity per site, not one per page

## Policy violations (flag as `high`)

- **Schema spam.** Markup for content users cannot see.
- **Self-serving reviews.** Reviews of your own business or Organization marked up on your own site do not qualify.
- **Fabricated ratings.** AggregateRating with no real review source.
- **Stale data.** Event markup for past dates; Offer prices that differ from the page.
- **Duplicate entities.** Several Organization blocks competing on one page.

## Scorer mapping (category `schema`)

Severity `medium` for missing core types (Organization, BreadcrumbList, the page-type schema). Severity `high` for policy violations. Weight the category higher for e-commerce and local profiles; the scorer's `--profile` does this.
