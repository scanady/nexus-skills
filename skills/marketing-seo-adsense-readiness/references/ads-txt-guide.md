# ads.txt Implementation Guide

The ads.txt (Authorized Digital Sellers) file is a text file that publishers place in the root of their web domain to declare who is authorized to sell their ad inventory.

## Why ads.txt Matters

- **Required for authorized inventory**: Google policy prohibits ads on domains using ads.txt where you're not listed as an authorized seller
- **Prevents fraud**: Helps buyers identify legitimate inventory
- **Transparency**: Declares your relationship with ad networks

## File Location

Place `ads.txt` at your domain root:
```
https://example.com/ads.txt
```

Must be accessible via HTTP/HTTPS at the exact path `/ads.txt`.

## File Format

Each line contains one record with comma-separated fields:

```
<domain>, <publisher-id>, <relationship>, [certification-authority-id]
```

### Fields

| Field | Required | Description |
|-------|----------|-------------|
| domain | Yes | Canonical domain of the advertising system |
| publisher-id | Yes | Your publisher account ID |
| relationship | Yes | DIRECT or RESELLER |
| certification-authority-id | No | TAG ID if system is TAG certified |

### Relationship Types

- **DIRECT**: You control the account and directly monetize inventory
- **RESELLER**: Another party controls the account that sells your inventory

## AdSense ads.txt Entry

For Google AdSense, add:

```
google.com, pub-XXXXXXXXXXXXXXXX, DIRECT, f08c47fec0942fa0
```

Replace `pub-XXXXXXXXXXXXXXXX` with your AdSense publisher ID.

**To find your publisher ID:**
1. Sign in to AdSense
2. Go to Account → Account information
3. Copy your Publisher ID (starts with "pub-")

## Complete Example

```
# ads.txt file for example.com
# AdSense
google.com, pub-1234567890123456, DIRECT, f08c47fec0942fa0

# Other ad networks (examples)
# openx.com, 123456789, RESELLER, 6a698e2ec38604c6
# appnexus.com, 9876543, RESELLER, f5ab79cb980f11d1
```

## Validation

### Manual Checks
1. File is at domain root: `https://yourdomain.com/ads.txt`
2. Returns HTTP 200 status
3. Content-Type is text/plain
4. No HTML wrapper around content
5. Publisher ID matches your AdSense account

### Common Validation Errors

| Error | Cause | Fix |
|-------|-------|-----|
| 404 Not Found | File doesn't exist | Create ads.txt in root |
| Wrong location | File in subdirectory | Move to domain root |
| HTML content | File wrapped in HTML | Serve as plain text |
| Wrong pub ID | Typo in publisher ID | Copy ID from AdSense |
| Invalid format | Missing commas or fields | Check syntax |

## Framework-Specific Implementation

### Static Sites
Place `ads.txt` in your public/static folder:
- **Next.js**: `/public/ads.txt`
- **Gatsby**: `/static/ads.txt`
- **Hugo**: `/static/ads.txt`
- **Jekyll**: Root directory (or `/assets/`)

### Dynamic Sites
Configure your web server or framework to serve the file:

**Express.js:**
```javascript
app.get('/ads.txt', (req, res) => {
  res.type('text/plain');
  res.send('google.com, pub-XXXXXXXX, DIRECT, f08c47fec0942fa0');
});
```

**nginx:**
```nginx
location = /ads.txt {
    alias /path/to/ads.txt;
    default_type text/plain;
}
```

## Subdomain Considerations

- ads.txt applies to the exact domain where it's hosted
- Subdomains need their own ads.txt OR can reference parent domain
- For `blog.example.com`, either:
  - Place ads.txt at `blog.example.com/ads.txt`
  - Or redirect to parent domain's ads.txt

## Updating ads.txt

When changing ad networks or account details:
1. Update the ads.txt file
2. Verify file is accessible
3. Allow 24-48 hours for crawlers to pick up changes
4. Check AdSense for any ads.txt warnings

## Troubleshooting in AdSense

AdSense shows ads.txt status in:
- **Sites** → Your site → ads.txt status
- **Policy center** → ads.txt issues

Common warnings:
- "Earnings at risk" - ads.txt missing or incorrect
- "No ads.txt file found" - File not accessible
- "ads.txt not verified" - Processing in progress
