---
name: marketing-seo-adsense-readiness
disable-model-invocation: false
description: Analyze websites and projects for Google AdSense compliance and readiness, in two modes - a source-code audit of a project, or a live-site review of a URL that mimics Google's approval process. Use when asked to check AdSense eligibility, audit a site for Google Ads, verify publisher policy compliance, prepare a site for monetization, fix AdSense policy violations, diagnose an AdSense rejection (especially "low value content"), or prepare a resubmission. Covers content quality, ad placement, privacy requirements, and technical standards.
---

# AdSense Readiness Analyzer

Analyze projects and websites to ensure compliance with Google AdSense Program Policies before applying for monetization or after receiving policy violation notices.

## Choose a Mode

| Mode | Use when | Input | Output |
|------|----------|-------|--------|
| **Project audit** | You have the site source and want to find and fix issues in code | Project files | Readiness report and code fixes (Steps 1-5) |
| **Live-site review** | The site is deployed, was rejected, or is about to be submitted or resubmitted | A URL | Pass/fail review report with scores and a remediation roadmap (see Live-Site Review) |

If the user gives a URL, run the live-site review. If the user gives a project, run the project audit. If the site is deployed and the source is available, run both: audit first, then review.

If the user asks for AdSense help and gives neither a URL nor a project, ask for the site URL or project path before proceeding.

## Project Audit Workflow

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

---

## Live-Site Review

Simulate Google's AdSense site approval review by crawling a live website against all known approval criteria. Put special emphasis on "low value content" signals, the most common rejection reason. Produce a detailed pass/fail report with specific, actionable remediation steps.

### L1. Read the references first

Before anything else, read every file below with the Read tool. Do not proceed until their content is in context.

- [references/review-criteria.md](references/review-criteria.md) — complete scored review criteria
- [references/low-value-content-signals.md](references/low-value-content-signals.md) — how to detect and fix low value content
- [references/common-rejections.md](references/common-rejections.md) — common rejection reasons and fixes
- [references/sources.md](references/sources.md) — official Google source URLs

### L2. Gather context

Note any rejection email, error message, site type, or niche the user supplies. The stated rejection reason sets which area to prioritize, but still run the full review. If no rejection reason is given, assume "low value content" and run the full review.

Common rejection reasons: low value content (most common, triggers deep content analysis), insufficient content, site navigation issues, content policy violations, traffic source issues.

Classify the site type (see Step 1). Apply the Database/Directory/Tool prose-block branch from Step 1 during Phase 1.

### L3. Crawl the live site

You must visit and analyze the live site. Use browser tools (Playwright MCP `browser_navigate`, `browser_snapshot`, `browser_click`) or `fetch_webpage`. Visit **at least 10 pages**, or all pages if fewer exist.

1. **Homepage.** Record title, meta description, visible content, navigation, footer links, estimated word count, and layout.
2. **Site map.** List all navigable pages from main navigation, footer, sidebar, internal links, and `/sitemap.xml`. Prioritize main navigation pages, 3-5 content or blog pages, About, Contact, Privacy Policy, Terms of Service, and any thin-looking pages.
3. **Per-page analysis.** For each page record: URL, title tag, word count of substantive content (exclude nav, footer, boilerplate), content type, depth (Shallow under 100 words, Thin 100-300, Adequate 300-600, Rich 600+), originality, value to a user, navigation, ads present, and issues.
4. **Blog content pattern check** (sites with blog or article sections). Across all posts check: publication dates (flag if most fall in a 2-week window), bylines (flag if all generic or missing), length consistency (flag if all within ±15%), and voice (flag if none show personal experience or opinion). If 2 or more flags trigger, report `WARN: AI Batch Content Pattern Detected` and list each signal.
5. **Technical URLs.** Check `{domain}/ads.txt`, `/privacy-policy` or `/privacy`, `/terms` or `/terms-of-service`, `/sitemap.xml`, and `/robots.txt`.

### L4. Run the review

Evaluate the site against every criterion in `references/review-criteria.md`.

**Phase 1: Content quality (highest priority).** Be brutally honest.
- A new site needs about 15-30 pages of substantive content, each with 300-500+ words of original text in complete sentences.
- Look for: clear niche focus, E-E-A-T signals, a reason to return, regular updates, something competitors lack.
- Red flags: mostly images or video with little text, a few sentences per page, auto-generated boilerplate, content that exists only to host ads, duplicate or near-duplicate pages, thin affiliate content, "coming soon" or placeholder pages, login-walled content, scraped content, keyword-stuffed pages, AI-generated content without editorial value.
- Score each page PASS, WARN, or FAIL, then calculate an overall content score.

**Phase 2: User experience and navigation.** Clear navigation, content within 2-3 clicks, no broken links, mobile-responsive, fast load, readable layout, no excessive pop-ups or interstitials.

**Phase 3: Site identity and trust.** About page that says who runs the site, Contact page with real details, obvious purpose and niche, professional look, established author or publisher identity.

**Phase 4: Technical compliance.** `ads.txt` present and valid, privacy policy that discloses cookies, tracking, third-party ads, and Google with opt-out information, Terms of Service, cookie consent for EU visitors, HTTPS, `sitemap.xml`, `robots.txt` not blocking important content.

**Phase 5: Policy compliance.** No prohibited content, no ads on error, under-construction, or low-content pages, ad-to-content ratio, Better Ads Standards, no deceptive content, supported language, and the restricted-category check from Step 2.

**Phase 6: Search engine presence.** Indexed by Google, organic traffic potential, proper titles, meta descriptions, and headings.

### L5. Generate the review report

```markdown
# AdSense Site Review Report

**Site:** [URL]
**Review Date:** [Date]
**Site Type:** [type]
**Overall Verdict:** [APPROVE / LIKELY REJECT / REJECT]
**Confidence:** [High / Medium / Low]

## Executive Summary
[2-3 sentences: readiness and primary blocker(s)]

## Overall Scores
| Category | Score | Status |
|----------|-------|--------|
| Content Quality & Depth | X/10 | PASS/WARN/FAIL |
| Content Originality | X/10 | PASS/WARN/FAIL |
| Content Volume | X/10 | PASS/WARN/FAIL |
| User Experience & Navigation | X/10 | PASS/WARN/FAIL |
| Site Identity & Trust | X/10 | PASS/WARN/FAIL |
| Technical Compliance | X/10 | PASS/WARN/FAIL |
| Policy Compliance | X/10 | PASS/WARN/FAIL |
| Search Engine Readiness | X/10 | PASS/WARN/FAIL |

**Overall Score: X/80**

## Critical Issues (Must Fix Before Resubmitting)
1. **[Issue]**
   - **Where:** [page(s) or site-wide]
   - **What Google Sees:** [reviewer perspective]
   - **Why It Causes Rejection:** [specific policy]
   - **How to Fix:** [actionable steps]

## Warnings (Should Fix)
## Passes (What's Working)

## Page-by-Page Analysis
| Page | URL | Word Count | Content Depth | Status | Notes |
|------|-----|------------|---------------|--------|-------|

## Technical Checks
| Check | Status | Details |
|-------|--------|---------|
| HTTPS / ads.txt / Privacy Policy / Terms / Cookie Consent / Sitemap / Robots.txt / Mobile | ✅/❌ | [details] |

## Remediation Roadmap
### Priority 1: Critical
### Priority 2: Important (before resubmitting)
### Priority 3: Recommended

## Content Strategy Recommendations
[If content is the primary issue: pages needed, word count, niche focus, structure, publishing frequency]

## When to Resubmit
1. [ ] [Specific, measurable milestone]
**Estimated time to readiness:** [estimate]
```

### Review rules

- Be brutally honest. A false pass wastes a rejection cycle.
- Cite the specific Google policy for every finding, and give every issue a specific fix.
- Score conservatively. If in doubt, flag a warning.
- Judge as a Google reviewer, not as a friend. A page with 50 words and a large image is thin content.
- Template boilerplate, navigation, footer, and sidebar text do not count as content.
- "Coming soon", placeholder, and under-construction pages are automatic FAILs.
- Fewer than 10 substantive content pages almost always means rejection.
- Always include the page-by-page table, the remediation roadmap, and the resubmission criteria.
- Never recommend resubmitting at once unless the site passes every check.
- Assume a new site applying for AdSense (stricter review than an established site). Flag a very new domain.

### Review self-check

Before presenting the report, confirm: all four reference files were read; the homepage and at least 10 pages were visited; `ads.txt`, privacy policy, sitemap, and `robots.txt` were checked; every score has evidence; every critical issue has a fix; the verdict follows from the scores. If any check fails, revise first.
