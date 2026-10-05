#!/usr/bin/env python3
"""Generate a draft tracking plan for GA4 and/or Plausible and check event names.

Usage:
    python3 tracking_plan.py                     sample SaaS funnel, markdown
    python3 tracking_plan.py funnel.json         your funnel
    python3 tracking_plan.py funnel.json --json  machine-readable output

Exit code 1 when any event name or parameter breaks a GA4 rule.
"""

import argparse
import json
import re
import sys

NAME_RE = re.compile(r"^[a-z][a-z0-9_]*$")
RESERVED_PREFIXES = ("google_", "ga_", "firebase_")
RESERVED_NAMES = {
    "app_remove", "click", "error", "file_download", "first_open", "first_visit",
    "form_start", "form_submit", "in_app_purchase", "page_view", "scroll",
    "session_start", "user_engagement", "video_complete", "video_progress", "video_start",
    "view_search_results",
}
MAX_NAME = 40
MAX_PARAMS = 25
MAX_KEY_EVENTS = 30

SAMPLE = {
    "business_type": "saas",
    "platforms": ["ga4", "plausible"],
    "paid_channels": ["google_ads"],
    "consent_required": True,
}

# (event, trigger, parameters, priority, is_key_event)
TEMPLATES = {
    "saas": [
        ("pricing_viewed", "Pricing page or section visible", ["referrer_page"], "medium", False),
        ("generate_lead", "Demo or contact form accepted by server", ["form_name", "source"], "high", True),
        ("sign_up", "Account created", ["method", "plan_name"], "critical", True),
        ("login", "Login succeeds", ["method"], "medium", False),
        ("trial_started", "Free trial begins", ["plan_name", "trial_length_days"], "critical", True),
        ("onboarding_step_completed", "Each onboarding step done", ["step_name", "step_number"], "high", False),
        ("onboarding_completed", "Last onboarding step done", ["steps_total"], "high", False),
        ("feature_activated", "First use of a key feature", ["feature_name"], "medium", False),
        ("plan_selected", "User picks a plan", ["plan_name", "billing_period", "value", "currency"], "critical", False),
        ("begin_checkout", "Checkout opens", ["plan_name", "value", "currency"], "critical", False),
        ("purchase", "Payment confirmed", ["transaction_id", "value", "currency", "plan_name"], "critical", True),
        ("subscription_cancelled", "Cancel confirmed", ["cancel_reason", "plan_name"], "high", False),
    ],
    "ecommerce": [
        ("view_item_list", "Category or list shown", ["item_list_name", "items"], "medium", False),
        ("select_item", "Item picked from list", ["item_list_name", "items"], "medium", False),
        ("view_item", "Product page shown", ["value", "currency", "items"], "high", False),
        ("add_to_cart", "Item added to cart", ["value", "currency", "items"], "critical", False),
        ("view_cart", "Cart opened", ["value", "currency", "items"], "medium", False),
        ("begin_checkout", "Checkout opens", ["value", "currency", "items"], "critical", False),
        ("add_shipping_info", "Shipping step done", ["value", "currency", "shipping_tier", "items"], "medium", False),
        ("add_payment_info", "Payment step done", ["value", "currency", "payment_type", "items"], "medium", False),
        ("purchase", "Order confirmed", ["transaction_id", "value", "currency", "items"], "critical", True),
        ("refund", "Refund issued", ["transaction_id", "value", "currency"], "high", False),
        ("sign_up", "Account created", ["method"], "medium", False),
    ],
    "lead_gen": [
        ("cta_clicked", "Named CTA clicked", ["cta_name", "cta_location"], "medium", False),
        ("generate_lead", "Form accepted by server", ["form_name", "form_location"], "critical", True),
        ("content_downloaded", "Gated file delivered", ["content_name", "content_type"], "high", False),
        ("newsletter_subscribed", "Newsletter signup done", ["source"], "medium", False),
        ("video_started", "Video plays", ["video_title"], "low", False),
        ("video_completed", "Video ends", ["video_title"], "low", False),
        ("search", "Site search used", ["search_term"], "low", False),
    ],
}

DIMENSION_CANDIDATES = [
    "plan_name", "billing_period", "form_name", "cancel_reason", "feature_name",
    "content_name", "error_type", "step_name", "cta_name",
]


def check_event(event, params):
    """Return a list of rule violations for one event."""
    problems = []
    if len(event) > MAX_NAME:
        problems.append(f"name longer than {MAX_NAME} chars")
    if not NAME_RE.match(event):
        problems.append("name must be lowercase snake_case and start with a letter")
    if event.startswith(RESERVED_PREFIXES):
        problems.append("name uses a reserved prefix")
    if event in RESERVED_NAMES:
        problems.append("name is reserved by GA4")
    if len(params) > MAX_PARAMS:
        problems.append(f"{len(params)} params, limit is {MAX_PARAMS}")
    for p in params:
        if len(p) > MAX_NAME or not NAME_RE.match(p):
            problems.append(f"param '{p}' breaks name rules")
    return problems


def build_events(inputs):
    business_type = inputs.get("business_type", "saas")
    if business_type not in TEMPLATES:
        raise SystemExit(f"business_type must be one of {sorted(TEMPLATES)}")

    rows = [
        {"event": e, "trigger": t, "parameters": list(p), "priority": pr, "is_key_event": k}
        for e, t, p, pr, k in TEMPLATES[business_type]
    ]
    for custom in inputs.get("custom_events", []):
        rows.append({
            "event": custom["event"],
            "trigger": custom.get("trigger", "TBD"),
            "parameters": list(custom.get("parameters", [])),
            "priority": custom.get("priority", "medium"),
            "is_key_event": bool(custom.get("is_key_event", False)),
        })
    for row in rows:
        row["problems"] = check_event(row["event"], row["parameters"])
    return rows


def build_plan(inputs):
    platforms = inputs.get("platforms", ["ga4"])
    events = build_events(inputs)
    key_events = [e["event"] for e in events if e["is_key_event"]]
    used_params = {p for e in events for p in e["parameters"]}

    plan = {
        "business_type": inputs.get("business_type", "saas"),
        "platforms": platforms,
        "events": events,
        "key_events": key_events,
        "warnings": [],
        "setup_order": [],
    }
    if len(key_events) > MAX_KEY_EVENTS:
        plan["warnings"].append(f"{len(key_events)} key events, cap is about {MAX_KEY_EVENTS} (verify in Admin)")

    steps = []
    if "ga4" in platforms:
        plan["ga4"] = {
            "custom_dimensions": sorted(used_params & set(DIMENSION_CANDIDATES)),
            "gtm": {
                "tags": len(events),
                "triggers": len(events),
                "variables": len(used_params),
            },
            "key_events": key_events,
        }
        steps += [
            "GA4: create web data stream, set enhanced measurement (turn off what GTM replaces)",
            "GA4: register custom dimensions listed above",
            "GTM: one Google tag, then variables, triggers, event tags",
            "App: add data layer pushes on success states",
            "Test each event in GTM Preview, Network, DebugView",
            "GA4: mark key events, set counting method, set 14-month retention",
            "GA4: define internal traffic and activate the filter",
        ]
        if "google_ads" in inputs.get("paid_channels", []):
            steps.append("Link GA4 to Google Ads, import key events, confirm auto-tagging")
    if "plausible" in platforms:
        plan["plausible"] = {
            "goals": [e["event"] for e in events if e["is_key_event"]],
            "props_allowed": sorted(used_params & set(DIMENSION_CANDIDATES)),
            "note": "Custom props need Business tier or higher (verify). Use the snippet from the dashboard.",
        }
        steps += [
            "Plausible: install dashboard snippet, enable outbound links and file downloads as needed",
            "Plausible: add custom event goals with the exact names above",
            "Plausible: allow custom props in Settings (Business tier)",
            "Test goals in Realtime and Network",
        ]
    if inputs.get("consent_required"):
        plan["consent"] = {
            "ga4": "Consent Mode v2: default denied for analytics_storage, ad_storage, ad_user_data, ad_personalization; CMP updates on accept",
            "plausible": "Cookieless by design. Confirm legal position with counsel.",
        }
        steps.append("Consent: wire CMP before any Google tag fires")
    steps.append("Document plan in a shared sheet with owners and status")
    plan["setup_order"] = [f"{i}. {s}" for i, s in enumerate(steps, 1)]
    return plan


def render_markdown(plan):
    out = [f"# Tracking plan draft ({plan['business_type']}, {' + '.join(plan['platforms'])})", ""]
    out += ["| Event | Trigger | Params | Key event / goal | Priority | Check |",
            "|---|---|---|---|---|---|"]
    for e in plan["events"]:
        check = "ok" if not e["problems"] else "; ".join(e["problems"])
        key = "yes" if e["is_key_event"] else "no"
        out.append(f"| `{e['event']}` | {e['trigger']} | {', '.join(e['parameters']) or '-'} | {key} | {e['priority']} | {check} |")

    out += ["", f"Key events / goals ({len(plan['key_events'])}): " + ", ".join(plan["key_events"])]
    if "ga4" in plan:
        g = plan["ga4"]
        out += ["", "## GA4",
                f"- Custom dimensions to register: {', '.join(g['custom_dimensions']) or 'none'}",
                f"- GTM inventory: {g['gtm']['tags']} event tags, {g['gtm']['triggers']} triggers, {g['gtm']['variables']} variables, plus one Google tag"]
    if "plausible" in plan:
        p = plan["plausible"]
        out += ["", "## Plausible",
                f"- Goals: {', '.join(p['goals'])}",
                f"- Props to allow: {', '.join(p['props_allowed']) or 'none'}",
                f"- {p['note']}"]
    if "consent" in plan:
        out += ["", "## Consent"] + [f"- {k}: {v}" for k, v in plan["consent"].items()]
    if plan["warnings"]:
        out += ["", "## Warnings"] + [f"- {w}" for w in plan["warnings"]]
    out += ["", "## Setup order"] + plan["setup_order"]
    out += ["", "Review every name and param against the product before you implement."]
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(description="Draft a tracking plan and check names against GA4 rules.")
    parser.add_argument("input_file", nargs="?", help="funnel JSON file (default: sample SaaS funnel)")
    parser.add_argument("--json", action="store_true", help="print JSON instead of markdown")
    args = parser.parse_args()

    if args.input_file:
        with open(args.input_file, encoding="utf-8") as f:
            inputs = json.load(f)
    else:
        inputs = SAMPLE

    plan = build_plan(inputs)
    print(json.dumps(plan, indent=2) if args.json else render_markdown(plan))
    return 1 if any(e["problems"] for e in plan["events"]) else 0


if __name__ == "__main__":
    sys.exit(main())
