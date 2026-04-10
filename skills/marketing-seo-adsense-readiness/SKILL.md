---
name: marketing-seo-adsense-readiness
description: 'Analyze websites and projects for Google AdSense compliance and readiness. Use when asked to check AdSense eligibility, audit a site for Google Ads, verify publisher policy compliance, prepare a site for monetization, or fix AdSense policy violations. Covers content quality, ad placement, privacy requirements, and technical standards.'
---

# AdSense Readiness Analyzer

Analyze projects and websites to ensure compliance with Google AdSense Program Policies before applying for monetization or after receiving policy violation notices.

## Workflow

### 1. Project Discovery

Identify the project type and gather relevant files:

```
Web projects: HTML, templates, layouts, content pages, CSS, JS
Frameworks: Next.js, React, Vue, Angular, static site generators
Content: Blog posts, articles, landing pages, error pages
Configuration: ads.txt, privacy policy, terms of service
```

**Key files to examine:**
- All HTML/template files with potential ad placements
- Error pages (404, 500, etc.)
- Thank you / confirmation pages
- Navigation and alert components
- Privacy policy page
- Cookie consent implementation

**Classify the site type before proceeding.** The site type changes which content quality checks apply:

- **Editorial/Blog** — Article-driven content, news, commentary
- **Tool/Calculator** — Single or multi-function utility (converters, generators, calculators)
- **Database/Directory** — Entity-based pages (recipes, products, companies, places, ingredients)
- **E-commerce** — Product listings and purchases
- **Portfolio/Business** — Services, credentials, case studies
- **Hybrid** — Combination of the above

**If the site is a Database, Directory, or Tool type**, apply this additional check during Step 3:
- Do the entity/detail pages contain **prose blocks** (descriptions, context, editorial content) beyond structured fields (names, ratings, prices, tags)?
  - If **yes**: The site may qualify as informational content — flag as "reposition path" (SEO structure, schema, meta descriptions) rather than defaulting to "add a blog."
  - If **no**: Flag content enrichment as the primary readiness gap.

Record the site type in the report header.

### 2. Policy Compliance Audit

Run through each policy category. See [references/policies.md](references/policies.md) for complete policy details.

#### Content Policies Checklist
- [ ] No prohibited content (illegal, adult, violent, deceptive)
- [ ] Original, substantial content on every monetized page
- [ ] No low-value or "lorem ipsum" placeholder content
- [ ] No scraped or auto-generated thin content
- [ ] Content in a supported language
- [ ] **Restricted/sensitive category check**: If the site is in a sensitive-but-legal niche (alcohol, gambling, pharmaceuticals, dating, firearms), note that approval is possible but ad fill may be near-zero unless the publisher opts in to restricted categories in AdSense Blocking Controls (Brand Safety > Blocking Controls > Sensitive Categories). Flag this as an explicit action item in the readiness report even if content quality is otherwise strong.

#### Inventory Value Checklist
- [ ] No ads on pages under construction
- [ ] No ads on error pages (404, 500)
- [ ] No ads on thank you / exit pages
- [ ] No ads on alert or navigation-only screens
- [ ] More content than ads on every page
- [ ] No ads in background processes or hidden contexts

#### Ad Placement Checklist
- [ ] Ads don't overlay navigation elements
- [ ] Ads don't interfere with content consumption
- [ ] No "dead end" screens forcing ad clicks
- [ ] Clear visual separation between ads and content
- [ ] Ads comply with Better Ads Standards

#### Privacy & Technical Checklist
- [ ] Privacy policy exists and is accessible
- [ ] Privacy policy discloses use of cookies/tracking
- [ ] Privacy policy mentions third-party ad serving
- [ ] Cookie consent mechanism (where required)
- [ ] ads.txt file present and valid (if applicable)
- [ ] No malware or unwanted software

### 3. Content Quality Assessment

Evaluate content against Google's quality guidelines. See [references/quality-guidelines.md](references/quality-guidelines.md).

**Core value questions:**
1. Does the page provide substantial value vs similar sites?
2. Is content original and not duplicated across pages?
3. Is the site well-organized with clear navigation?
4. Does the content match what's promised (no bait-and-switch)?
5. Would a user return to this site?

**E-E-A-T signal checklist (Expertise, Experience, Authoritativeness, Trustworthiness):**
- [ ] Content is attributed to a named author (not "Team," "Admin," or the site name)
- [ ] Author has a bio or linked profile with credentials relevant to the topic
- [ ] About page establishes who runs the site and their expertise
- [ ] Content demonstrates genuine knowledge, personal experience, or original perspective — not just plausible-sounding generalities

**Blog/article content pattern check** (required if the site has a blog or news section):
- [ ] Posts are spread across more than one 2-week window (not all published in a single burst)
- [ ] Post lengths vary naturally by topic — not all approximately the same word count
- [ ] At least some posts include personal voice, first-person detail, or experience-specific content
- [ ] Bylines are not all identical generic team attributions

If **2 or more** of the pattern checks are flagged, note a `WARN: Publication Pattern Risk` in the report. A burst-published, uniformly-sized, anonymously-bylined content set is a high-confidence AI-batch-content signal that will likely trigger rejection even if individual posts read acceptably.

**Site-type–specific content check:**
- For **database/directory/tool** sites: Apply the reposition vs. enrich branch evaluation defined in Step 1 — do not default to "add a blog" without first assessing whether existing entity pages already contain substantive prose.
- For **editorial/blog** sites: Verify minimum 15-20 pages of 300-500+ word original content.
- For **e-commerce** sites: Verify product pages include original descriptions, not manufacturer copy.

### 4. Generate Recommendations Report

Create a structured report with:

```markdown
## AdSense Readiness Report

### Summary
- Overall Status: [Ready / Needs Work / Not Eligible]
- Critical Issues: [count]
- Warnings: [count]

### Critical Issues (Must Fix)
1. [Issue]: [File/Location]
   - Problem: [Description]
   - Fix: [Specific remediation steps]

### Warnings (Should Fix)
1. [Issue]: [File/Location]
   - Problem: [Description]
   - Recommendation: [Suggested improvement]

### Best Practices (Consider)
1. [Recommendation]

### Files Analyzed
- [list of files examined]
```

### 5. Implement Remediations

For each issue, implement fixes:

**Error/Exit Pages:**
- Remove any ad code from 404, 500, thank-you pages
- Ensure these pages still provide navigation back to content

**Under Construction Pages:**
- Either complete the content or remove from sitemap
- Remove ad placements until content is ready

**Low-Value Content:**
- Add substantial, original content
- Remove or consolidate thin pages
- Replace placeholder text with real content

**Privacy Policy:**
- Add/update privacy policy with required disclosures
- Include cookie consent if serving EU users
- Document third-party ad serving

**ads.txt:**
- Create ads.txt in site root if not present
- Validate format and entries

## Common Violations & Fixes

| Violation | Detection | Fix |
|-----------|-----------|-----|
| Ads on 404 page | Check 404.html for ad scripts | Remove ad code from error templates |
| No privacy policy | Missing /privacy or /privacy-policy | Add compliant privacy policy page |
| Lorem ipsum content | Search for "lorem" in content | Replace with real content |
| Under construction | Pages with "coming soon" | Complete or remove pages |
| Too many ads | Ad-to-content ratio check | Reduce ad placements |
| Ads overlay nav | CSS/layout analysis | Adjust ad positioning |

## File Patterns to Search

```
# Ad code patterns
grep -r "googlesyndication\|adsbygoogle\|google_ad" .

# Placeholder content
grep -ri "lorem ipsum\|placeholder\|coming soon\|under construction" .

# Error pages
find . -name "*404*" -o -name "*error*" -o -name "*500*"

# Privacy policy
find . -name "*privacy*" -o -name "*policy*"

# ads.txt
find . -name "ads.txt"
```

## Verification

After implementing fixes:
1. Re-run the audit checklist
2. Test all page types in browser
3. Validate ads.txt format
4. Confirm privacy policy accessibility
5. Check mobile responsiveness (Better Ads Standards)
