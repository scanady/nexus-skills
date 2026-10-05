# GTM Patterns

Container design and tag recipes for GA4. Plausible through GTM: see `plausible-guide.md`.

## Container layout

| Item | Naming | Example |
|---|---|---|
| Tag | `GA4 - Event - <event>` | `GA4 - Event - generate_lead` |
| Trigger | `CE - <event>` (custom event), `Click - <target>`, `PV - <path>` | `CE - sign_up` |
| Variable | `DLV - <key>`, `CONST - <name>`, `JS - <name>` | `DLV - plan_name` |
| Folder | By funnel stage | `Registration` |

Create in this order: variables → triggers → tags.

Base items:
- `CONST - GA4 Measurement ID` (`G-XXXXXXXXXX`).
- One **Google tag** with that ID, trigger **Initialization - All Pages**. Not a second tag per page type.
- Consent defaults come from the CMP template on **Consent Initialization - All Pages**.
- One `DLV` per param you read.

## Pattern 1: data layer push (preferred)

App pushes after success:

```javascript
window.dataLayer = window.dataLayer || [];
window.dataLayer.push({
  event: 'sign_up',
  method: 'email',
  plan_name: 'trial'
});
```

GTM:
- Trigger: Custom Event, event name `sign_up` (exact, case-sensitive).
- Tag: Google Analytics: GA4 Event, Measurement ID `{{CONST - GA4 Measurement ID}}`, Event Name `sign_up`, params `method` = `{{DLV - method}}`, `plan_name` = `{{DLV - plan_name}}`.

Rules:
- Push data in the same object as `event`. Do not push data in one call and the event in the next unless variables use Data Layer Version 2 persistence on purpose.
- Ecommerce: clear before each push so old `items` do not leak:

```javascript
window.dataLayer.push({ ecommerce: null });
window.dataLayer.push({
  event: 'purchase',
  ecommerce: {
    transaction_id: 'T-1042',
    value: 99,
    currency: 'USD',
    items: [{ item_id: 'plan_pro', item_name: 'Pro', price: 99, quantity: 1 }]
  }
});
```

- Push once per real action. Guard against re-render and double click.
- Never push PII.

## Pattern 2: click on a named element

Ask devs to add `data-track="demo-cta"`. Selectors on classes break on redesign.

- Trigger: Click - All Elements (or Just Links). Condition: Click Element matches CSS selector `[data-track="demo-cta"]`.
- Tag: GA4 Event `cta_clicked`, param `cta_name` = `{{Click Element}}` attribute via a `JS` or Auto-Event variable of type Element attribute `data-track`.

## Pattern 3: form submit

Preferred: app pushes `generate_lead` after the server accepts.

Fallback when no dev access:
- Trigger: Form Submission with "Wait for tags" and "Check validation" on. Pairs poorly with AJAX forms.
- Better fallback: Page View trigger on thank-you path, plus once-per-session count method on the key event.
- AJAX forms: listen for a success element with Element Visibility trigger, "Once per page".

## Pattern 4: single page app page views

Pick one source of page views:

| Source | Setup |
|---|---|
| Enhanced measurement history events | Stream setting "Page changes based on browser history events" on. No GTM page_view tag. |
| GTM History Change | Turn that stream setting off. Trigger History Change → GA4 Event `page_view`. Set `page_location` to `{{New History Fragment}}`-aware URL via a JS variable, and `page_referrer` to previous URL. |

Both on = double page views. This is the most common SPA bug.

Update `document.title` before the push, or `page_title` is stale.

## Pattern 5: scroll depth

GA4 enhanced measurement sends `scroll` at 90% only. For 25/50/75/100, use the Scroll Depth trigger → GA4 Event `scroll_depth` with `percent_scrolled`. Turn off nothing: different event name, no clash. Do not mark as key event.

## Pattern 6: consent mode

1. Add a CMP template tag (Cookiebot, OneTrust, Usercentrics, or other). Fire on Consent Initialization - All Pages.
2. Defaults: all four signals `denied` for regions that need consent.
3. On accept, CMP calls update → `granted`.
4. In each tag: Advanced settings → Consent settings. Built-in Google tags check consent themselves. Non-Google tags need "Require additional consent" with the right signal.
5. Test with GTM Preview: Consent tab shows state per event.

## Pattern 7: user_id

Set once after login in the data layer or Google tag config field `user_id`. Opaque id. Clear on logout.

## Pattern 8: server-side tagging

Use when you need first-party endpoint, control over data sent to vendors, or lower ad-blocker loss. Cost: a server container to host and pay for. Start client-side. Move later if loss is measured and matters.

## Workspaces, versions, environments

- One workspace per change set. Name it for the ticket.
- Version name: `YYYY-MM-DD <what changed>`. Notes: events added, removed, reason.
- Use Environments (Dev, Staging, Live) when the site has staging. Preview against staging first.
- Publish only after Preview + DebugView check passes.
- Roll back by publishing the previous version.
- Limit Publish rights. Edit rights for more people is fine.

## Common mistakes

| Mistake | Result |
|---|---|
| Two Google tags, same ID | Duplicate sessions and events |
| Event name typo in trigger | Tag never fires. Preview shows event, tag under "Not fired". |
| Custom Event trigger with regex on, name has `.` | Matches too much |
| Tag on All Pages when it needs a specific event | Fires every load |
| Param typed by hand in tag instead of variable | Drift. Use DLVs. |
| Hard-coded `gtag` plus GTM | Double hits |
| Publish with no Preview | Silent breakage |
| Trigger on class name | Breaks on redesign |
| No version notes | No one knows what changed |
