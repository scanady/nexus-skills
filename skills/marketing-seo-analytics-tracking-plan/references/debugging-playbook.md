# Debugging Playbook

Analytics bugs fail silent. No error, only missing or wrong numbers. Work bottom layer up. Prove each layer before you touch the next.

## The layer stack

```
5  Report          what you see (GA4 reports, Plausible dashboard)
4  Processing      filters, thresholds, registration, goals, consent modeling
3  Network         the request that left the browser
2  Tag layer       GTM tag fired or not, with what values
1  Source          app code, data layer, DOM
```

Rule: symptom at layer 5 → test layer 1 first.

## Tools

| Tool | Shows | How |
|---|---|---|
| Browser console | Layer 1. `dataLayer` contents. | Type `dataLayer`. Filter: `dataLayer.filter(e => e.event === 'sign_up')`. |
| GTM Preview (Tag Assistant) | Layer 2. Tags fired, not fired, variable values, consent state. | GTM → Preview → enter URL. Left: events. Middle: tags. Right: variables. |
| DevTools Network | Layer 3. | Filter `collect` (GA4) or `event` (Plausible). Check status and payload. |
| GA4 DebugView | Layer 4–5, near real time. | Admin → DebugView. Needs debug mode: GTM Preview sets it, or send `debug_mode: true` on the event or Google tag. Tag Assistant extension also works. |
| GA4 Realtime | Quick sanity. | Report → Realtime. |
| Plausible Realtime | Pageviews and goals now. | Dashboard live view. |
| BigQuery export | Raw events, no sampling. | Only if linked beforehand. Not retroactive. |

`_gl` in a URL is the cross-domain linker. It is not a debug switch.

## Method

1. **State the claim.** Exact event name, params, page, user action, expected result.
2. **Reproduce.** Same browser, same steps, consent granted, no blocker, not logged as internal traffic.
3. **Layer 1.** Is the push or call made? Right name, right keys, right values, right time (after success, once)?
4. **Layer 2.** Did the trigger match? Did the tag fire? Do variables hold values at that event?
5. **Layer 3.** Is the request sent? Status 2xx? Payload carries event name and params?
6. **Layer 4.** Filters, consent, registration, goal config, thresholds, wrong property?
7. **Layer 5.** Check report latency before declaring failure.
8. **Fix one thing. Retest at the layer that failed. Then recheck layer 5.**

## GA4 and GTM issues

### Fires in GTM Preview, not in GA4

| Cause | Check | Fix |
|---|---|---|
| Consent denied | Preview → Consent tab. `analytics_storage` value. | Test with consent granted. Fix CMP wiring or defaults. |
| Wrong Measurement ID | Compare `G-` ID in tag with the data stream you are viewing | Correct the constant variable |
| Filter active | Admin → Data filters. Internal traffic Active? | Fix IP definition. Test from another network. |
| Debug filter | Debug sessions hidden from reports | Look in DebugView, not reports |
| Not debug mode | DebugView empty | Use Preview or `debug_mode` |
| Request blocked | Network shows blocked or cancelled | Disable blocker to test. Consider server-side. |
| Too early | Standard reports lag | Wait. Use DebugView and Realtime first. |

### Event never fires in Preview

1. Does the event appear in the left list? No → layer 1 failure (no push, wrong dataLayer object name, push before GTM loaded is fine, but push in wrong window or iframe is not).
2. Event is listed but tag is under "Not fired" → trigger conditions failed. Open the trigger and the Variables tab at that event. Compare.
3. Custom Event trigger name must match exactly. Case-sensitive. Whitespace counts.
4. Element not present at trigger time → use DOM Ready, Window Loaded, or Element Visibility.
5. SPA route change not seen → History Change trigger or enhanced-measurement history setting.
6. Iframe forms (embedded HubSpot, Typeform, Calendly) → GTM on parent cannot see events inside. Use the vendor's postMessage or callback and push to the data layer.
7. Tag has consent requirement not met → Preview shows "consent not granted".

### Params show `(not set)`, `undefined`, or are missing

1. Network payload: is the param name there (`ep.plan_name` for string params, `epn.` for numbers)?
2. No → Preview Variables tab: what does the DLV hold at that event? `undefined` → key missing or misspelled in the push.
3. Variable holds a value but tag lacks the param → add param row in the tag.
4. In payload but not in reports → register the custom dimension. Not backfilled.
5. Values truncated or dropped → over length limits. See `ga4-rules.md`.
6. 25 param limit reached → drop params.

### Duplicate events

Count tags that fired in Preview and requests in Network for one action.

| Cause | Fix |
|---|---|
| Enhanced measurement and GTM tag for same thing | Turn off one |
| Two Google tags, same ID | Delete one |
| Hard-coded `gtag` plus GTM | Remove one source |
| SPA: history pageviews plus GTM History Change | Choose one |
| Two triggers match one tag | Tighten triggers, add exclusion |
| Data layer push runs twice (re-render, retry, double click) | Guard in app code |
| Thank-you page reload counts again | Once-per-session count method, dedup key (`transaction_id`) |

### Sessions or users look wrong

| Symptom | Likely cause |
|---|---|
| Sessions too high | Duplicate Google tags, history double fire, client id not kept (cookie blocked) |
| Sessions reset on domain change | Cross-domain not set. Use "Configure your domains". |
| Self-referrals (own domain as source) | Missing domain list, or payment/auth domain needs unwanted referral entry |
| Paid shows as direct | UTMs stripped by redirect, or auto-tagging off, or consent denied on landing |
| Users too low | Consent denied share, blockers, filters too wide, tags on some pages only |
| Source overwritten mid-funnel | UTMs on internal links |
| Landing page `(not set)` | Page view missing on first load, or tag fired late |

### GA4 and Google Ads disagree

1. Model and window: compare on equal settings.
2. Count method: once per event vs once per session.
3. Event name in Ads import matches the key event name.
4. Property linked to the right Ads account. Sync delay up to about a day.
5. Auto-tagging on. No competing manual conversion tags double counting.
6. Consent mode v2 signals set for EEA.
7. Enhanced conversions: user-provided data, hashed, only with consent and a lawful basis.

### Key event not counted

Event name differs in case. Event marked after the data arrived. Count method hides repeats. Event filtered by a data filter. Event is a reserved or auto event with different meaning.

## Plausible issues

| Symptom | Check | Fix |
|---|---|---|
| No pageviews | Network: request to endpoint after load. Status usually 202. | Snippet in `<head>`. Domain matches site. Not on localhost without `captureOnLocalhost`. |
| Pageviews drop sharply on some browsers | Ad blockers | First-party proxy, set `endpoint` |
| Custom event not in goals | Goal exists? Exact same name? Sent after goal created? | Create goal. Fix name casing. Resend. Past data not backfilled. |
| Event sent, no goal data | Network POST body has your event name? | Fix call. Check `props` shape. |
| Props missing | Plan tier. Prop allowed in Settings → Custom properties. | Allow prop. Send same keys every time. `(none)` means missing. |
| Props rejected | Value is object or array | Scalars only |
| SPA shows one page | Router uses hash | `hashBasedRouting` |
| Pageview counted twice | Old and new snippet both loaded, or GTM plus source | Keep one |
| Own visits count | No exclusion | IP exclusion or `localStorage.plausible_ignore = 'true'` |
| Totals differ from GA4 | Different counting and consent | Compare trends. Document the difference. |
| Class event does nothing | Class syntax wrong, tagged-events not enabled on old install | Check `plausible-event-name=Name` and snippet type |

## Debug checklist

```
[ ] Expected event name, params, trigger written down
[ ] Layer 1: push or call exists in console, right keys, fires once
[ ] Layer 2: trigger matched, tag fired, variables resolved (GTM Preview)
[ ] Layer 3: request sent, 2xx, payload correct (Network)
[ ] Consent granted in test, blocker off, not internal traffic
[ ] GA4: DebugView shows event with params
[ ] GA4: custom dimension registered (params you report on)
[ ] GA4: key event marked, name exact
[ ] Plausible: goal exists, exact name, props allowed
[ ] No duplicate tags, sources, or triggers
[ ] Report layer rechecked after latency window
[ ] Result written with evidence per layer
```

## Report template

```
Symptom:
Failing layer:
Evidence:
Root cause:
Fix:
Retest steps and result:
Confidence: verified / estimated / assumed
```
