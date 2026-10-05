# Event Taxonomy

Names, parameters, catalog, and change control. Applies to GA4 and Plausible. One name per action on every platform.

## Naming procedure

1. Is there a GA4 recommended event for this action? Use its exact name and its parameter names.
2. No match → `object_action`. Lowercase, underscores, noun first, verb last.
3. Check length ≤ 40, starts with a letter, no reserved prefix (`ga4-rules.md`).
4. Write the name once in the plan. Never rename later without the change protocol below.

| Good | Bad | Why |
|---|---|---|
| `sign_up` | `signup_completed`, `SignUp` | GA4 recommended name exists |
| `generate_lead` | `demo_form_done` | GA4 recommended name exists |
| `purchase` | `checkout_completed` | GA4 recommended name exists |
| `plan_selected` | `selectedPlan`, `plan-selected` | Case and hyphen |
| `onboarding_step_completed` | `step` | Too vague |

## Verb list

Use these. Do not add synonyms.

| Verb | Use for |
|---|---|
| `_started` | Multi-step process begins |
| `_completed` | Process ends well |
| `_failed` | Attempt ends in error |
| `_submitted` | Form or data sent |
| `_viewed` | Passive view of modal, section, content |
| `_clicked` | Click on one named element |
| `_selected` | Choice from options |
| `_opened` / `_closed` | Modal, drawer, chat |
| `_downloaded` | File download |
| `_activated` | Feature used first time |
| `_cancelled` | User ends on purpose |

Page views are not custom events. GA4 and Plausible collect them.

## Parameters

Rules:
- snake_case, ≤ 40 chars, ≤ 25 per event.
- Scalar values only. Stable value sets (`monthly`, not "Monthly plan!").
- Reuse one param name across events. `plan_name` everywhere, not `plan`, `tier`, `planName`.
- GA4 recommended params keep their official names (`value`, `currency`, `transaction_id`, `items`, `method`).
- No PII.

Common params:

| Param | Type | Use |
|---|---|---|
| `method` | string | Sign-up or login method |
| `plan_name` | string | Segment by plan |
| `billing_period` | string | `monthly`, `annual` |
| `value`, `currency` | number, string | Money. `currency` is required with `value`. |
| `transaction_id` | string | Dedup purchases |
| `form_name`, `form_location` | string | Which form, where |
| `content_name`, `content_type` | string | Downloads, gated content |
| `feature_name` | string | Feature events |
| `step_name`, `step_number` | string, int | Onboarding or wizard |
| `error_type` | string | Failed events |

`user_id`: set through the Google tag config or `set` command, not as a per-event param, when you use GA4 User-ID. Value = opaque internal id.

## Catalog

Recommended name in first column when it exists.

### SaaS

| Event | Trigger | Key params |
|---|---|---|
| `pricing_viewed` | Pricing page or section visible | `referrer_page` |
| `generate_lead` | Demo or contact form accepted | `form_name`, `source` |
| `sign_up` | Account created | `method`, `plan_name` |
| `login` | Login success | `method` |
| `trial_started` | Trial begins | `plan_name`, `trial_length_days` |
| `onboarding_step_completed` | Each step done | `step_name`, `step_number` |
| `onboarding_completed` | Last step done | `steps_total` |
| `feature_activated` | First use of key feature | `feature_name` |
| `plan_selected` | Plan chosen | `plan_name`, `billing_period`, `value` |
| `begin_checkout` | Checkout opened | `value`, `currency`, `plan_name` |
| `purchase` | Payment confirmed (server or confirmation page) | `value`, `currency`, `transaction_id` |
| `subscription_cancelled` | Cancel confirmed | `cancel_reason`, `plan_name` |

### Ecommerce

Use GA4 ecommerce events with the `items` array: `view_item_list`, `select_item`, `view_item`, `add_to_cart`, `remove_from_cart`, `view_cart`, `begin_checkout`, `add_shipping_info`, `add_payment_info`, `purchase`, `refund`. Required on purchase: `transaction_id`, `value`, `currency`, `items`.

### Lead gen / content

| Event | Trigger | Key params |
|---|---|---|
| `generate_lead` | Form accepted | `form_name`, `form_location` |
| `content_downloaded` | Gated file delivered | `content_name`, `content_type` |
| `newsletter_subscribed` | Double opt-in done or form accepted | `source` |
| `cta_clicked` | Click on named CTA | `cta_name`, `cta_location` |
| `video_started`, `video_completed` | Player events | `video_title` |
| `search` | Site search | `search_term` |

### Engagement and support

`chat_opened`, `help_article_viewed` (`article_name`), `error_encountered` (`error_type`), `share` (`method`, `content_type`).

## What to fire from where

| Fire from | When |
|---|---|
| App code → data layer (or `plausible()`) | Success states: account created, payment done, form accepted. Most reliable. |
| Backend / Measurement Protocol | Money events and anything that must survive ad blockers and closed tabs. Send `client_id` and `session_id` from the browser. |
| GTM click or form trigger | Static sites, no dev access. Weaker. Breaks on markup change. |
| Thank-you page view | Fallback for forms. Guard against reload and bookmark double-count. |

Fire success, not intent, for conversions. Click on "Buy" is not a purchase.

## Custom dimension plan (GA4)

Register only what you will filter or report on.

| Scope | Candidate params |
|---|---|
| User | `plan_name`, `billing_period`, `company_size` |
| Event | `form_name`, `cancel_reason`, `feature_name`, `content_name`, `error_type`, `step_name` |
| Item | `item_brand`, `item_variant` if used in reports |

Count slots before you add. See limits in `ga4-rules.md`.

## Tracking plan document

Keep one shared doc or sheet. One row per event:

| Column | Content |
|---|---|
| Event | Final name |
| Description | When it fires, in plain words |
| Trigger / source | Data layer push, click selector, backend |
| Params | Name, type, example, required? |
| GA4 key event | yes/no, count method |
| Plausible goal | yes/no, props |
| Owner | Person or team |
| Status | planned, in test, live, retired |
| Added / changed | Date and release |

## Change protocol

1. Propose change in the doc. State what reports it affects.
2. Rename = new event + parallel run + retire old. GA4 cannot rename history.
3. Dev and analytics sign off.
4. Test in a GTM workspace or staging data stream.
5. Publish with version note. Update doc.
6. Retire dead events: remove tags, mark `retired`.

Version the plan: major = renamed or removed event, minor = new event, patch = param tweak.
