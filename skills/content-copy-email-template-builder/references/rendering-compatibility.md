# Email Client Rendering Compatibility

Known quirks, bugs, and required workarounds for major email clients.

## Contents
- Outlook (Windows)
- Gmail
- Apple Mail
- Yahoo Mail / AOL
- General Rules That Apply Everywhere

---

## Outlook (Windows) — Most Problematic Client

Outlook 2007–2019 and Outlook 365 on Windows use Microsoft Word's rendering engine. This causes the most compatibility issues.

### Layout
- **Use tables for all layout** — no `<div>`-based columns, no Flexbox, no Grid
- Nested tables required for multi-column layouts
- Set `width` on `<td>` attributes, not just CSS: `<td width="300">`
- `margin: 0 auto` for centering works on the wrapper table only — use `align="center"`

### CSS Support
- Inline all CSS — `<link>` stylesheets completely ignored
- `<style>` blocks in `<head>` partially supported (Outlook 2016+ improved this)
- `max-width` ignored on tables — use `width` attribute instead
- `padding` on `<tr>` and `<table>` ignored — only use `padding` on `<td>`
- `border-radius` ignored — all corners square in Outlook
- `background-image` in CSS ignored — use `<td background="url">` attribute or VML

### Buttons (Critical)
Outlook ignores CSS background-color on `<a>` tags. Use VML bullet-proof buttons:

```html
<!--[if mso]>
<v:roundrect xmlns:v="urn:schemas-microsoft-com:vml"
  xmlns:w="urn:schemas-microsoft-com:office:word"
  href="{{action_url}}"
  style="height:44px; v-text-anchor:middle; width:200px;"
  arcsize="10%"
  strokecolor="#[button-border-hex]"
  fillcolor="#[button-bg-hex]">
  <w:anchorlock/>
  <center style="color:#ffffff; font-family:Arial,sans-serif; font-size:16px; font-weight:bold;">
    Button Text
  </center>
</v:roundrect>
<![endif]-->
<!--[if !mso]><!-->
<a href="{{action_url}}"
   style="background-color:#[button-bg-hex]; border-radius:4px; color:#ffffff; display:inline-block; font-family:Arial,sans-serif; font-size:16px; font-weight:bold; line-height:44px; text-align:center; text-decoration:none; width:200px; -webkit-text-size-adjust:none;">
  Button Text
</a>
<!--<![endif]-->
```

### Images
- Always set `width` attribute on `<img>` — not just CSS `width`
- Background images via CSS ignored — use VML for background images if critical:
```html
<!--[if gte mso 9]>
<v:image xmlns:v="urn:schemas-microsoft-com:vml"
  src="image.jpg" style="width:600px; height:200px;"/>
<![endif]-->
```

### Fonts
- Web fonts (`@font-face`, Google Fonts) ignored — fall back to system fonts
- Safe Outlook fonts: Arial, Verdana, Georgia, Times New Roman, Courier New
- Always specify a font-family stack: `font-family: 'Your Font', Arial, sans-serif`

### Spacing
- `line-height` on `<td>` or `<p>`: use both `line-height` CSS and `mso-line-height-rule: exactly`
- Gaps between images: add `display:block` + `font-size:0; line-height:0` to container `<td>`

### MSO Conditional Comments
Use to show/hide content for Outlook specifically:
```html
<!--[if mso]>Outlook only content<![endif]-->
<!--[if !mso]><!-->Non-Outlook content<!--<![endif]-->
<!--[if gte mso 9]>Outlook 2007+<![endif]-->
```

---

## Gmail

Gmail is generally well-behaved but has specific limitations.

### CSS Support
- Strips `<style>` blocks in `<head>` for Gmail in the browser (fixed in 2016 for most cases, but still inconsistent in some webview contexts)
- **Always inline critical CSS** — do not rely solely on `<head>` styles
- `@media` queries ignored in some Gmail mobile app versions
- `@media (prefers-color-scheme: dark)` not supported in Gmail

### Classes and IDs
- Gmail strips class names and IDs in some contexts (promotions tab, external client)
- All critical styles must be inline — classes are a progressive enhancement only

### Images
- Images blocked by default until user clicks "Display images" — alt text critical
- Always set meaningful `alt` text, especially on hero images

### Promotions Tab
- Rich card annotations supported (for promotional emails) via JSON-LD in `<head>`
- Not required but improves visibility in Promotions tab

---

## Apple Mail (macOS and iOS)

Apple Mail is generally the most capable email client for CSS support.

### Dark Mode
Apple Mail has robust dark mode support. Implement carefully:

```css
@media (prefers-color-scheme: dark) {
  body, .body-wrapper { background-color: #1a1a1a !important; }
  .content-card { background-color: #2a2a2a !important; }
  .text-primary { color: #f0f0f0 !important; }
  .text-secondary { color: #a0a0a0 !important; }
  .logo-light { display: none !important; }
  .logo-dark { display: block !important; }
}
```

**Logo handling for dark mode:**
- Include both light and dark logo versions
- Use CSS `display: none` / `display: block` to swap via `prefers-color-scheme`

### Meta tag required:
```html
<meta name="color-scheme" content="light dark">
<meta name="supported-color-schemes" content="light dark">
```

### Retina / HiDPI Images
- Serve `@2x` images and set HTML `width` to half the actual pixel size
- Example: 1200px image → set `width="600"` in HTML

### Auto-detection (blue links)
Apple Mail auto-links phone numbers, addresses, dates. Prevent with:
```html
<meta name="format-detection" content="telephone=no, date=no, address=no, email=no">
```
Or wrap in:
```html
<a href="tel:+1xxxxxxxxxx" style="color: inherit; text-decoration: none;">+1 (xxx) xxx-xxxx</a>
```

---

## Yahoo Mail / AOL

### CSS Support
- Strips `<style>` blocks in some contexts — inline CSS required for critical styles
- Prefixes CSS class names (`.msg-body` → `.yiv0123456789 .msg-body`) — can break `<head>` styles
- Generally follows standard HTML email rules

### Quirks
- Adds padding to `<p>` tags — reset with `margin: 0; padding: 0` inline
- `background-color` on `<body>` sometimes overridden — apply to outer wrapper `<table>` too

---

## General Rules That Apply Everywhere

### Document Structure
```html
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml"
      xmlns:o="urn:schemas-microsoft-com:office:office" lang="en">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="format-detection" content="telephone=no, date=no, address=no, email=no">
  <meta name="color-scheme" content="light dark">
  <meta name="supported-color-schemes" content="light dark">
  <!--[if gte mso 9]>
  <xml><o:OfficeDocumentSettings>
    <o:AllowPNG/>
    <o:PixelsPerInch>96</o:PixelsPerInch>
  </o:OfficeDocumentSettings></xml>
  <![endif]-->
  <title>Email Subject</title>
  <style type="text/css">
    /* Reset */
    body, table, td, a { -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; }
    table, td { mso-table-lspace: 0pt; mso-table-rspace: 0pt; }
    img { -ms-interpolation-mode: bicubic; }
    /* Resets */
    img { border: 0; height: auto; line-height: 100%; outline: none; text-decoration: none; }
    table { border-collapse: collapse !important; }
    body { height: 100% !important; margin: 0 !important; padding: 0 !important; width: 100% !important; }
    /* iOS blue links */
    a[x-apple-data-detectors] { color: inherit !important; text-decoration: none !important; }
    /* Gmail blue links */
    u + #body a { color: inherit; text-decoration: none; font-size: inherit; font-family: inherit; font-weight: inherit; line-height: inherit; }
    /* Mobile responsive */
    @media screen and (max-width: 600px) {
      .mobile-full { width: 100% !important; display: block !important; }
      .mobile-padding { padding: 16px !important; }
      .mobile-text { font-size: 18px !important; line-height: 1.6 !important; }
      .mobile-hide { display: none !important; }
      .mobile-stack { display: block !important; width: 100% !important; }
    }
    /* Dark mode */
    @media (prefers-color-scheme: dark) {
      /* Override here */
    }
  </style>
</head>
```

### Layout Table Pattern
```html
<!-- Outer wrapper: full width, body background -->
<table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%"
       style="background-color: {{color-bg-body}};">
  <tr>
    <td align="center" style="padding: 20px 0;">

      <!-- Inner content: constrained width -->
      <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="600"
             style="background-color: {{color-bg-content}}; max-width: 600px;">
        <tr>
          <td style="padding: 32px;">
            <!-- Content here -->
          </td>
        </tr>
      </table>

    </td>
  </tr>
</table>
```

### Image Tag Pattern
```html
<img src="{{image_url}}" width="600" height="auto" alt="Description"
     style="display: block; width: 100%; max-width: 600px; height: auto;
            border: 0; outline: none; text-decoration: none;">
```

### Paragraph Reset Pattern
```html
<p style="margin: 0 0 16px 0; padding: 0; font-family: Arial, sans-serif;
          font-size: 16px; line-height: 1.6; color: #111827;">
  Content here.
</p>
```

### Testing Tools
- [Litmus](https://litmus.com) — live preview across 90+ clients
- [Email on Acid](https://emailonacid.com) — similar to Litmus
- [Putsmail](https://putsmail.com) — free send-to-inbox test
- [MailTrap](https://mailtrap.io) — safe inbox for dev/staging
- [Can I Email](https://www.caniemail.com) — CSS/HTML feature support checker (like caniuse.com for email)
