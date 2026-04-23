# Platform Export Guide

Import instructions and variable syntax for major email service providers.

## Contents
- Variable Syntax Reference
- Resend
- Postmark
- Mailgun
- SendGrid
- Mailchimp
- Customer.io
- Kit (ConvertKit)
- HubSpot

---

## Variable Syntax Reference

| Platform | Basic variable | Fallback / default | Conditional |
|----------|---------------|--------------------|-------------|
| Resend (raw HTML) | `{{variable}}` | `{{variable \| default: "fallback"}}` | n/a (use React Email for logic) |
| Postmark | `{{variable}}` | n/a (set server-side) | `{{#if variable}}...{{/if}}` |
| Mailgun | `{{variable}}` | `{{variable \| default: "fallback"}}` | `{{#if variable}}...{{/if}}` |
| SendGrid | `{{variable}}` | `{{variable \| default: "fallback"}}` | `{{#if variable}}...{{/if}}` |
| Mailchimp | `*\|variable\|*` | `*\|IF:variable\|*...*\|ELSE\|*...*\|END:IF\|*` | `*\|IF:variable\|*` |
| Customer.io | `{{customer.variable}}` | `{{customer.variable \| default: "fallback"}}` | `{% if customer.variable %}...{% endif %}` |
| Kit | `{{ subscriber.variable }}` | `{{ subscriber.variable \| default: "fallback" }}` | `{% if subscriber.variable %}...{% endif %}` |
| HubSpot | `{{ contact.variable }}` | `{{ contact.variable \| default: "fallback" }}` | `{% if contact.variable %}...{% endif %}` |

**Universal safe placeholder** (replace before import): `{{first_name}}`, `{{unsubscribe_url}}`

---

## Resend

**Template type**: Raw HTML or React Email component
**Import method**: Resend Dashboard → Emails → Templates → New Template

**Raw HTML import:**
1. Go to [resend.com/emails](https://resend.com/emails) → Templates
2. Click "New Template" → paste HTML
3. Variables use `{{variable}}` — set defaults in your API send call
4. Test: Dashboard → send preview to your email

**React Email (preferred for Resend):**
- Install: `npm install @react-email/components`
- Convert HTML structure to JSX components (`<Html>`, `<Body>`, `<Section>`, `<Text>`, `<Button>`, etc.)
- Props replace `{{variables}}`
- Render to HTML string with `render(<Template {...props} />)` from `@react-email/render`

**API send example:**
```javascript
await resend.emails.send({
  from: 'onboarding@yourdomain.com',
  to: user.email,
  subject: 'Welcome!',
  html: render(<WelcomeEmail firstName={user.firstName} />),
});
```

**Required variables in every template:**
- `{{first_name}}` — personalization
- Unsubscribe: Resend handles via `X-List-Unsubscribe` header or include manual link

---

## Postmark

**Template type**: HTML + Text (both required)
**Import method**: Postmark Dashboard → Templates → New Template

**Import steps:**
1. Log in → select Server → Templates → New Template
2. Paste HTML into HTML body field
3. Paste plain-text version into Text body field (required by Postmark)
4. Set Template Alias (used in API calls)
5. Variables: `{{variable}}` — Postmark uses Handlebars

**Postmark-specific syntax:**
```handlebars
{{#if product_name}}Welcome to {{product_name}}!{{/if}}
{{first_name}} <!-- standard variable -->
{{{html_content}}} <!-- unescaped HTML — use sparingly -->
```

**API call:**
```javascript
await postmarkClient.sendEmailWithTemplate({
  From: 'sender@domain.com',
  To: 'recipient@domain.com',
  TemplateAlias: 'welcome',
  TemplateModel: {
    first_name: 'Alex',
    product_name: 'Acme',
    action_url: 'https://...',
  },
});
```

**Required variables:**
- `{{first_name}}`
- `{{action_url}}` (for CTA buttons)
- `{{unsubscribe_url}}` or use Postmark's built-in unsubscribe

---

## Mailgun

**Template type**: HTML (Handlebars)
**Import method**: Mailgun Dashboard → Sending → Templates → Create Template

**Import steps:**
1. Dashboard → Sending → Templates → Create Template
2. Set template name and description
3. Paste HTML — Mailgun uses Handlebars `{{variable}}`
4. Variables passed via API `h:X-Mailgun-Variables` header or `template.variables` in send call

**Mailgun-specific syntax:**
```handlebars
{{first_name}}                          <!-- basic variable -->
{{first_name | default: "there"}}       <!-- with fallback -->
{{#if is_paid}}Upgrade offer{{/if}}     <!-- conditional -->
%recipient.variable%                    <!-- batch/recipient variable -->
```

**API call (Node.js):**
```javascript
mg.messages.create(domain, {
  from: 'hello@domain.com',
  to: ['recipient@domain.com'],
  subject: 'Welcome!',
  template: 'welcome-template',
  'h:X-Mailgun-Variables': JSON.stringify({ first_name: 'Alex' }),
});
```

---

## SendGrid

**Template type**: HTML (Dynamic Templates, Handlebars)
**Import method**: SendGrid Dashboard → Email API → Dynamic Templates → Create Template

**Import steps:**
1. Dashboard → Email API → Dynamic Templates → Create Template
2. Add a version → Code Editor
3. Paste HTML — use `{{variable}}` Handlebars syntax
4. Save version, note the Template ID

**SendGrid-specific syntax:**
```handlebars
{{first_name}}                      <!-- basic variable -->
{{first_name | default: "there"}}   <!-- with fallback -->
{{{html_content}}}                  <!-- unescaped HTML -->
{{#if show_cta}}<a href="{{url}}">Click here</a>{{/if}}
```

**Unsubscribe:** Insert SendGrid's unsubscribe tag `<%asm_group_unsubscribe_url%>` or `{{{asm_group_unsubscribe_raw_url}}}` in footer.

**API call:**
```javascript
await sgMail.send({
  to: 'recipient@domain.com',
  from: 'sender@domain.com',
  templateId: 'd-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
  dynamicTemplateData: {
    first_name: 'Alex',
    action_url: 'https://...',
  },
});
```

---

## Mailchimp

**Template type**: HTML (Merge Tags)
**Import method**: Mailchimp → Campaigns → Email Templates → Create Template → Paste your code

**Import steps:**
1. Audience → Email Templates → Create Template
2. Select "Code your own" → Paste in HTML
3. Merge tags use `*|VARIABLE|*` syntax

**Mailchimp-specific syntax:**
```
*|FNAME|*                             <!-- built-in first name merge tag -->
*|EMAIL|*                             <!-- subscriber email -->
*|UNSUB|*                             <!-- unsubscribe URL (required) -->
*|LIST:ADDRESS|*                      <!-- physical address (required) -->
*|IF:FNAME|* Hello *|FNAME|*! *|ELSE|* Hello! *|END:IF|*
*|DATE:d/m/Y|*                        <!-- dynamic date -->
```

**Custom merge tags:** Define in Audience → Manage contacts → Settings → Merge tags.

**Note:** Mailchimp's editor may rewrite or strip custom HTML. Use "Code your own" option and test thoroughly with Inbox Preview.

---

## Customer.io

**Template type**: HTML (Liquid templating)
**Import method**: Customer.io → Journeys → Messages → New Email Message → Code Editor

**Import steps:**
1. Create a new email message in a Campaign or Broadcast
2. Select "Code Editor" (not drag-and-drop)
3. Paste HTML — use Liquid `{{ }}` syntax

**Customer.io Liquid syntax:**
```liquid
{{ customer.first_name | default: "there" }}     <!-- attribute with fallback -->
{{ customer.email }}
{% if customer.plan == "pro" %}
  You have Pro access.
{% endif %}
{% for item in event.items %}
  {{ item.name }} — ${{ item.price }}
{% endfor %}
{{ unsubscribe_url }}                             <!-- built-in unsubscribe -->
```

**Unsubscribe:** Customer.io injects `{{ unsubscribe_url }}` automatically if included. Required for compliance.

---

## Kit (formerly ConvertKit)

**Template type**: HTML (Liquid)
**Import method**: Kit → Broadcasts or Sequences → Create Email → Custom HTML

**Kit Liquid syntax:**
```liquid
{{ subscriber.first_name | default: "there" }}
{{ subscriber.email_address }}
{{ unsubscribe_url }}              <!-- required -->
{% if subscriber.tag_names contains "pro" %}Pro content{% endif %}
```

**Note:** Kit strips some HTML tags in their default editor. Use the custom HTML option for full control. Test thoroughly — Kit has a restrictive email parser.

---

## HubSpot

**Template type**: HTML (HubL — HubSpot Expression Language)
**Import method**: HubSpot → Marketing → Files and Templates → Design Tools → New File → HTML + HubL

**HubSpot HubL syntax:**
```
{{ contact.firstname | default: "there" }}
{{ contact.email }}
{{ unsubscribe_link }}              <!-- built-in macro -->
{{ office_location_html }}         <!-- built-in address block (CAN-SPAM) -->

{% if contact.lifecyclestage == "customer" %}
  Customer-specific content
{% endif %}
```

**Import via Design Tools:**
1. Marketing → Files and Templates → Design Tools
2. New File → Email Template → choose "Custom HTML"
3. Paste template, save, use in Marketing Email campaigns
