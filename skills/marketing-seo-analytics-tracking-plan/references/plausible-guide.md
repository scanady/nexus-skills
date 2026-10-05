# Plausible Guide

Privacy-first, cookieless, lightweight analytics. Few moving parts. Match it to what it is: pageviews, sources, goals, funnels. It does not do user-level journeys.

Plausible changes its snippet and options over time. **Rule: use the snippet the user's dashboard shows** (Site settings → Site installation). Check current docs at plausible.io/docs when a detail below is marked verify.

## What Plausible does and does not do

| Does | Does not |
|---|---|
| Pageviews, referrers, UTM, device, country | Per-user paths or user ids |
| Custom event goals, pageview goals | Retroactive goals (events before the goal exists are not backfilled) |
| Custom props on events and pageviews | Objects or arrays as prop values |
| Funnels, revenue goals (Business tier or higher, **verify** tier) | Raw event export without the API |
| Cookieless by design | Cross-site user stitching |

Because it is cookieless and stores no personal data by design, many teams run it without a cookie banner. Whether that satisfies your law is a legal call. Say so. Do not assert compliance.

## Install

The dashboard gives a snippet. Current format loads a per-site script and calls `plausible.init()` with options. Options (from current docs):

| Option | Default | Use |
|---|---|---|
| `endpoint` | `https://plausible.io/api/event` | Send through first-party proxy |
| `autoCapturePageviews` | `true` | Set `false` for manual pageviews |
| `hashBasedRouting` | `false` | Hash URLs (`/#/page`) |
| `outboundLinks` | `false` | Track outbound link clicks |
| `fileDownloads` | `false` | Track downloads (`true` or object listing file types) |
| `formSubmissions` | `false` | Track form submits |
| `customProperties` | `{}` | Props added to every event (object or function) |
| `captureOnLocalhost` | `false` | Test on localhost |
| `logging` | `true` | Console log of events |
| `transformRequest` | none | Edit or drop an event before send |

Older installs use `script.js` with `data-domain` and extension files (`script.outbound-links.js`, `script.tagged-events.js`, `script.revenue.js`, and others). Still works for sites that have it (**verify**). Do not mix old and new snippets on one page. When migrating, replace, do not add.

SPAs: pageviews fire on History API changes by default. No extra tag. Hash routers need `hashBasedRouting`.

## Goals

Two kinds:

| Kind | Setup |
|---|---|
| Pageview goal | Settings → Goals → Add goal → Pageview. Path like `/thanks` or `/blog/**`. No code. |
| Custom event goal | Send the event, then Add goal → Custom event with the exact name. |

Rules:
- Name match is exact, including case. Use the same snake_case names as GA4.
- Create the goal first or soon after. Past events are not backfilled.
- Keep goals few. Same discipline as key events.

## Send custom events

JavaScript:

```javascript
plausible('sign_up');
plausible('plan_selected', { props: { plan_name: 'pro', billing_period: 'annual' } });
plausible('download', { props: { method: 'HTTP' }, callback: () => { /* after send */ } });
```

Options on the second argument: `callback`, `props`, `revenue`, `interactive`.

No code: add CSS class to an element. Space becomes `+`:

```html
<a href="/demo" class="plausible-event-name=demo_requested">Book a demo</a>
```

Class-based events work for clicks on links, buttons, and forms. Fire from app code for success states.

## Custom properties

- Send in `props`. Scalars only: string, number, boolean.
- Limits (from current docs): 30 props per event, name up to 300 chars, value up to 2,000 chars.
- Requires Business plan or higher (**verify**).
- Allow a prop in the dashboard before reports show it: Settings → Custom properties.
- Missing or null value shows as `(none)`. Send the same keys every time.
- Values cannot be deleted one by one. A PII mistake means a data reset for the site. Never send names, emails, phone numbers, precise location, or usernames.

Props for every event in the page: `customProperties` init option.

## Revenue

```javascript
plausible('purchase', { revenue: { currency: 'USD', amount: 99.00 }, props: { plan_name: 'pro' } });
```

Revenue shows on custom event goals. Needs plan support (**verify**). Server truth lives in the payment system. Treat Plausible revenue as a trend view.

## Funnels

Dashboard: Funnels → build from existing goals or pages, 2 or more steps. Needs plan support (**verify**). Define steps in order of the plan's funnel map. Steps need goals to exist first.

## UTM and sources

Plausible reads `utm_*` and `ref`. Same UTM rules as `ga4-rules.md`. Never tag internal links. Paid traffic appears under Sources and Campaigns.

## Plausible through GTM

Allowed, but you lose some simplicity. Use only if the site already runs GTM and one team owns tags.

- Tag: Custom HTML with the dashboard snippet, trigger All Pages. (Or the template from the GTM community gallery if one exists, **verify**.)
- Events: Custom HTML tag calling `plausible('<event>', { props: { ... } })`, trigger Custom Event from the data layer.
- Do not also load Plausible in the page source. Double count.
- GTM is itself blocked by many ad blockers. A direct snippet is more reliable.

## Proxy

Many blockers drop requests to `plausible.io`. Route script and `/api/event` via your own domain (reverse proxy on CDN or host). Set `endpoint` to your path. Test with a blocker on. Keep proxy rules from caching event POSTs.

## Excluding yourself

- Dashboard: Settings → Exclusions (IP, path, hostname) (**verify** names).
- Browser: `localStorage.plausible_ignore = 'true'` in the console on your site.
- Localhost is ignored by default. Use `captureOnLocalhost` to test.

## GA4 and Plausible side by side

- Same event names, same params, same funnel map.
- Plausible = quick truth on traffic and goals. GA4 = ad integration, audiences, deep exploration.
- Expect different totals. GA4 uses cookies, consent state, and modeling. Plausible counts visits by a daily-rotating hash and no consent gate. Compare trends, not totals.
- Plan one source of truth per question and write it in the tracking plan.

## Plausible checklist

```
[ ] Snippet from dashboard installed once, in <head>
[ ] Domain in script matches the site in Plausible
[ ] Pageviews appear in Realtime after a test visit
[ ] Each custom event sent from the browser (Network: POST to the endpoint)
[ ] Matching goal exists, same exact name
[ ] Props allowed in dashboard (Business tier)
[ ] No PII in any prop
[ ] Proxy tested with a blocker
[ ] Own traffic excluded
```
