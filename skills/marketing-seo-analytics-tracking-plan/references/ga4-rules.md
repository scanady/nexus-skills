# GA4 Rules and Limits

Current facts for GA4 plus Google tag in GTM. Items marked **verify** were not confirmed against live Google docs when this skill was written. Check Admin or Google help before you promise them.

## Terms that changed

| Old | Now |
|---|---|
| Conversions (GA4 events) | **Key events** (renamed March 2024) |
| "Conversion" | Only a Google Ads conversion action, or a key event imported to Ads |
| GA4 Configuration tag (GTM) | **Google tag** (one per Measurement ID) |
| Universal Analytics goals | Gone. Do not mention as an option. |

Say "key event" in all GA4 output. Admin path: Admin → Data display → Key events (menu labels move; search "Key events").

## Key events

- Mark an event as key event in Key events, or toggle on the event in the Events list.
- Cap per property: 30 standard, 50 on 360 (**verify**). Curate.
- Marking is not retroactive. Count starts at marking time. Mark before launch.
- Mark micro-steps only if you optimize ads for them or report them to leadership.
- Counting method per key event: once per event or once per session. Use once per session for leads and signups where duplicate submits are likely.
- Import key events to Google Ads from linked property. Ads then calls them conversions.

## Event name rules

| Rule | Limit |
|---|---|
| Length | 40 chars max |
| Characters | Letters, numbers, underscores. Start with a letter. No spaces, no hyphens. |
| Case | Case-sensitive. `Sign_Up` and `sign_up` are two events. Use lowercase. |
| Reserved prefixes | `google_`, `ga_`, `firebase_` |
| Reserved names | Auto-collected and system events, e.g. `first_visit`, `session_start`, `click`, `scroll`, `page_view`, `user_engagement`, `app_remove`. Do not reuse for custom meaning. |
| Recommended names | Prefer when they fit: `sign_up`, `login`, `generate_lead`, `purchase`, `begin_checkout`, `add_to_cart`, `view_item`, `select_item`, `search`, `share`. They feed built-in reports and Ads. |

## Parameter and property limits

| Item | Limit |
|---|---|
| Params per event | 25 |
| Param name | 40 chars |
| Param value | 100 chars. `page_title` 300, `page_referrer` 420, `page_location` 1000. |
| User properties | 25 per property; name 24 chars; value 36 chars |
| User ID value | 256 chars |
| Custom dimensions (standard) | 50 event-scoped, 25 user-scoped, 10 item-scoped (**verify** item count) |
| Custom metrics (standard) | 50 |
| Events per user per day | 100,000 |

Over limit → GA4 drops the item. No error shown. Check names in the plan before launch.

## Custom dimensions

- A param is in raw data and in DebugView right away. It is in Explore and standard reports only after you register it: Admin → Custom definitions.
- Registration applies going forward. Not backfilled. Takes up to about a day.
- Register only params you will report on. Slots are scarce.
- Do not put high-cardinality values in a dimension (raw URLs, IDs per row). Report shows `(other)` row.

## Data collection settings

- **Enhanced measurement:** page views, scrolls, outbound clicks, site search, video engagement, file downloads, form interactions. Turn off any you replace with GTM tags to avoid double counting. Form interaction events are noisy. Prefer a data layer event for real submit success.
- **Data retention:** event-level data default 2 months. Set 14 months in Admin → Data settings → Data retention for Explorations.
- **Internal traffic:** define IPs in Data stream → Configure tag settings → Define internal traffic. Then Admin → Data settings → Data filters. New filter starts in Testing state. Move to Active.
- **Debug traffic filter:** leave on so debug sessions do not pollute reports.
- **Unwanted referrals:** payment gateways and auth domains that bounce users back. Not the same list as cross-domain.

## Cross-domain

Funnel crosses `www.acme.com` → `app.acme.com` or `checkout.other.com`:

1. Data stream → Configure tag settings → **Configure your domains**. Add all domains in the funnel.
2. Test: click link to domain B. URL gets `_gl=` param. DebugView session does not restart.
3. Subdomains of one site share a cookie. They need no cross-domain setup, but still list them under unwanted referrals only if they cause self-referrals.

`_gl` is a linker param. It is not a debug flag.

## Consent Mode v2

Four signals: `ad_storage`, `analytics_storage`, `ad_user_data`, `ad_personalization`. EEA/UK traffic using ads features needs `ad_user_data` and `ad_personalization` set.

- Default state set to `denied` before any Google tag loads. Update to `granted` when user accepts.
- In GTM: use a CMP template that sets defaults on "Consent Initialization – All Pages". Do not set defaults from a normal page-load tag.
- **Basic mode:** Google tags blocked until consent. No data from decliners.
- **Advanced mode:** tags load, send cookieless pings when denied. Google may model gaps when volume thresholds are met (**verify** thresholds).
- Consent rates differ by region and banner design. Do not promise a number.
- Consent Mode is not legal advice. Send legal questions to counsel or the DPO.

## UTM and auto-tagging

| Param | Rule | Example |
|---|---|---|
| `utm_source` | Platform, lowercase | `linkedin`, `newsletter` |
| `utm_medium` | Channel type | `cpc`, `email`, `social` |
| `utm_campaign` | Stable id or slug | `2026q1_trial_push` |
| `utm_content` | Creative variant | `hero_blue` |
| `utm_term` | Paid keyword | `saas_analytics` |

- Only tag links you place on other sites, in email, in ads, in QR codes.
- Never tag internal links.
- Google Ads: use auto-tagging (`gclid`). Do not add manual UTMs unless the account is set to override.
- Keep a shared sheet of allowed values. Lowercase only.

## Attribution

GA4 defaults to data-driven attribution for key events. Lookback windows: Admin → Attribution settings (**verify** current options). GA4 and Google Ads counts differ because of model, window, and count method. Compare on the same model and window before calling it a bug.

## PII

Google terms forbid sending PII. Do not send email, name, phone, street address in params, user properties, `user_id`, page URLs, or titles. Use an internal opaque id. Watch for `?email=` in URLs. Strip it in GTM before the tag.

## Reporting latency

- DebugView and Realtime: seconds.
- Standard reports: hours to a day or more.
- Data thresholds and sampling can hide small groups in Explore. Not a tracking bug.
