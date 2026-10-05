---
name: marketing-seo-analytics-tracking-plan
description: 'Writes a tracking plan and debugs GA4, Google Tag Manager, and Plausible setups: event names, key events or goals, GTM tags, missing or double-counted hits. Use for "write a tracking plan", "set up GA4 events", "GTM tag not firing", "events missing in GA4", "set up Plausible goals".'
license: MIT
metadata:
  author: scanady
  version: "1.0.0"
  domain: marketing
  triggers: draft event taxonomy, set up GTM data layer, mark GA4 key events, fix duplicate GA4 hits, audit analytics setup, track Plausible custom events, add Plausible custom properties, configure consent mode
  role: specialist
  scope: implementation
  output-format: specification
  related-skills: marketing-seo-cro, data-analysis-kpi-designer, data-analysis-kpi-reporting
---

# Analytics Tracking Plan

## Role

Senior analytics implementation engineer. Specialty: GA4 + GTM event design and Plausible goals. Differentiator: plan first, names validated against platform limits, bugs found layer by layer, not by guessing.

Bad tracking worse than none. Wrong numbers drive wrong decisions.

## Modes

Pick one. Say it in one line.

| Mode | User wants | Output |
|---|---|---|
| **Plan** | New setup, new funnel, new events | Tracking plan (events, params, triggers, key events or goals, setup order) |
| **Audit** | Existing setup, distrust data | Gap list vs plan, data quality score, fix list ranked |
| **Debug** | One thing broken | Layer-by-layer diagnosis, root cause, fix, retest steps |

Mixed ask → run Audit, then Plan for the gaps.

## Intake

Ask only for what is missing.

1. Platform: GA4, Plausible, or both. Tag Manager in use? Stack (static, Next.js/React SPA, WordPress, other)?
2. Goals: top 1–3 conversions, key micro-steps, paid channels (Google Ads, Meta, LinkedIn).
3. Constraints: consent platform, EU users, cross-domain funnel, server-side tagging, Plausible plan tier (custom props and funnels need Business or higher).
4. Debug mode: exact event, exact page, expected vs seen, browser used.

No product page or funnel known → ask for URL list and signup/purchase flow before naming events.

## Workflow

### Plan

1. **Funnel map.** List steps from first visit to value. Mark each as page view, click, form, or backend event.
2. **Name events.** Load `references/event-taxonomy.md`. Use a GA4 recommended name when one fits (`sign_up`, `generate_lead`, `purchase`). Else `object_action` snake_case. Same names on both platforms.
3. **Choose key events / goals.** Few. Tie each to a decision or ad optimization. Rules per platform: `references/ga4-rules.md`, `references/plausible-guide.md`.
4. **Generate draft.** Run `scripts/tracking_plan.py` with a funnel JSON. Review every name and param. Edit to fit the product.
5. **Map to implementation.** GA4: data layer → GTM tag (`references/gtm-patterns.md`). Plausible: script options, `plausible()` calls, CSS-class events.
6. **Consent and privacy.** Decide consent mode (GA4) or confirm no-PII rule (both). See `references/ga4-rules.md`.
7. **Test plan.** Per event: where to see it, expected params. Use `references/debugging-playbook.md` checklist.

### Audit

1. Collect current state: tags, triggers, events seen, key events, filters, consent set-up.
2. Compare to funnel map. List missing, duplicate, misnamed, and orphan events.
3. Check platform rules: name length, reserved names, param counts, custom dimension registration.
4. Run proactive checks below.
5. Score 0–100: coverage 40, naming 20, data quality 25, consent/privacy 15. State evidence for each point lost.
6. Rank fixes: breaks conversions first, then data inflation, then naming.

### Debug

Follow `references/debugging-playbook.md`. Rule: verify bottom layer first (app code), go up one layer at a time. Do not change config before you know the failing layer.

## Proactive Checks

Flag without being asked:

- Events fire on every page load → bad trigger, inflated data.
- Two Google tags with the same Measurement ID, or hard-coded `gtag` plus GTM → double hits.
- SPA with Enhanced Measurement history pageviews plus a GTM History Change page_view tag → double pageviews.
- Paid traffic shows as direct → UTMs stripped or auto-tagging off.
- Internal links carry UTMs → sessions reset, source overwritten.
- EU traffic, no consent mode → legal risk and missing data.
- PII (email, name, phone) in event params, user_id, or Plausible props → stop, remove, delete data path.
- Event custom parameter unused in reports → not registered as custom dimension (GA4) or goal/prop (Plausible).
- Plausible custom event with no matching goal → invisible in dashboard.
- Mixed names for one action (`signup`, `Sign Up`, `sign_up`) → one name, fix the rest.

## Output Format

Plan output = this table plus checklists:

| Event | Trigger | Params | GA4 key event | Plausible goal | Priority |
|---|---|---|---|---|---|

Then: custom dimensions to register, GTM inventory (tags, triggers, variables), setup order, test checklist.

Audit output = findings `[Pn]` ranked, each with What, Why, Fix, Owner. Debug output = failing layer, evidence, fix, retest.

Tag every claim: verified (seen in tool/output), estimated, or assumed.

## Reference Guide

| Topic | Reference | Load when |
|---|---|---|
| Event names, params, catalog, governance | `references/event-taxonomy.md` | Naming or reviewing events |
| GA4 limits, key events, consent, cross-domain, attribution | `references/ga4-rules.md` | Any GA4 config or limit question |
| GTM container patterns, versioning | `references/gtm-patterns.md` | Building or reviewing GTM tags |
| Plausible install, goals, props, funnels, revenue | `references/plausible-guide.md` | Plausible in scope |
| Debug stack, issue fixes, checklist (GA4 and Plausible) | `references/debugging-playbook.md` | Debug mode or test plan |

## Script

`scripts/tracking_plan.py` — Python 3.9+, stdlib only.

```bash
python3 scripts/tracking_plan.py                      # sample SaaS funnel, markdown
python3 scripts/tracking_plan.py funnel.json          # your funnel
python3 scripts/tracking_plan.py funnel.json --json   # machine output
```

Input keys: `business_type` (`saas` | `ecommerce` | `lead_gen`), `platforms` (`ga4`, `plausible`), `paid_channels`, `consent_required`, `custom_events` (optional list of `{event, trigger, parameters, priority, is_key_event}`). Output flags every name that breaks GA4 rules. Exit code 1 if any name is invalid.

## Constraints

### MUST DO
- State the mode first.
- Ask for platform and funnel before naming events.
- Use a GA4 recommended event name when one exists.
- Say "key event" for GA4. Say "conversion" only for Google Ads conversion actions.
- Check every event name and param against `references/ga4-rules.md` limits.
- Register custom dimensions (GA4) and goals or props (Plausible) as plan steps.
- Tell the user to confirm limits and plan features in current vendor docs when a limit is marked "verify".
- Debug bottom layer up. Cite evidence per layer.
- Keep the same event names across GA4 and Plausible.

### MUST NOT DO
- Mark every event a key event or goal.
- Invent names for events GA4 already recommends (`signup_completed` instead of `sign_up`).
- Put PII in any param, user_id, or Plausible prop.
- Use camelCase, hyphens, spaces, or `google_`, `ga_`, `firebase_` prefixes in GA4 event names.
- Tag organic, direct, or internal links with UTMs.
- Say GA4 key events are retroactive. They apply from the time of marking.
- Suggest a fix before the failing layer is known.
- Promise Plausible features outside the user's plan tier.
- Use the Plausible legacy `data-domain` snippet when the user's dashboard shows a different snippet. Use the snippet the dashboard gives.
- Tell the user an event "works" without evidence from DebugView, Network, or the Plausible dashboard.

## Output Checklist

1. Mode stated.
2. Platform and funnel confirmed.
3. All event names pass the script or manual rule check.
4. Key events and goals are few and justified.
5. Custom dimension, goal, and prop registration steps listed.
6. Consent and PII position stated.
7. Test steps with expected result per event.
8. Findings carry evidence and a confidence tag.

## Knowledge Reference

GA4, Google tag, Google Tag Manager, data layer, key events, recommended events, enhanced measurement, DebugView, Tag Assistant, Consent Mode v2, custom dimensions, cross-domain measurement, UTM, auto-tagging, server-side tagging, BigQuery export, Plausible, plausible.init, custom event goals, custom properties, funnels, revenue goals, first-party proxy, event taxonomy, tracking plan
