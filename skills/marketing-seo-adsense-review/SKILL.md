---
name: marketing-seo-adsense-review
version: v1.0.0
description: 'Perform a comprehensive live-site review mimicking the Google AdSense approval process. Use when a site has been rejected by AdSense (especially for "low value content"), when preparing to submit/resubmit a site for AdSense approval, or when diagnosing why a site keeps getting flagged. Requires a URL. Crawls the live site and evaluates it against every criterion Google reviewers check: content quality/depth/originality, navigation/UX, technical compliance, privacy policy, ads.txt, Better Ads Standards, and more.'
---

# AdSense Site Review

Perform a comprehensive review of a live website that mimics the Google AdSense human review process. Produces a detailed pass/fail report with specific, actionable remediation steps.

## Purpose

Simulate Google's AdSense site approval review by crawling and analyzing a live website against all known approval criteria — with special emphasis on "low value content" signals, the #1 rejection reason.

---

## Execution Logic

**Check $ARGUMENTS first to determine execution mode:**

### If $ARGUMENTS is empty or not provided:
Respond with:
"marketing-seo-adsense-review loaded. Provide the URL of the site you want reviewed (e.g., https://example.com)"

Then wait for the user to provide the URL in the next message.

### If $ARGUMENTS contains a URL:
Extract the URL and proceed immediately to Task Execution.

### If $ARGUMENTS contains content but no URL:
Ask the user to provide the site URL before proceeding.

---

## Task Execution

When a URL is available (either from initial $ARGUMENTS or follow-up message):

### 1. MANDATORY: Read Reference Files FIRST
**BLOCKING REQUIREMENT — DO NOT SKIP THIS STEP**

Before doing ANYTHING else, you MUST use the Read tool to read every file in `./references/`. This is non-negotiable.

Reference files to read:
- `./references/review-criteria.md` — Complete review criteria checklist
- `./references/low-value-content-signals.md` — Deep-dive on low value content detection
- `./references/common-rejections.md` — Common rejection reasons and fixes
- `./references/sources.md` — Official Google source URLs

**DO NOT PROCEED** to Step 2 until you have read all reference files and have their content in context.

### 2. Gather Site Context

If the user has provided additional context (e.g., rejection emails, error messages, site type, niche), note it. The specific rejection reason guides which areas to prioritize.

Common rejection reasons to watch for:
- **Low value content** (most common — triggers deep content analysis)
- **Insufficient content**
- **Site navigation issues**
- **Content policy violations**
- **Traffic source issues**

### 3. Crawl the Live Site

**This step is critical. You must actually visit and analyze the live site.**

Use browser tools (Playwright MCP `browser_navigate`, `browser_snapshot`, `browser_click`) or `fetch_webpage` to systematically crawl the site. You need to visit and analyze **multiple pages**, not just the homepage.

#### 3a. Homepage Analysis
- Navigate to the provided URL
- Take a snapshot of the full page
- Document: page title, meta description, visible content, navigation structure, footer links
- Note: word count estimate, content depth, visual layout

#### 3b. Discover and Map Site Structure
From the homepage, identify and list ALL navigable pages:
- Main navigation links
- Footer links
- Sidebar links
- Internal content links
- Sitemap (check /sitemap.xml)

**You must visit a minimum of 10 pages** (or all pages if fewer than 10 exist). Prioritize:
1. All main navigation pages
2. Content/blog pages (at least 3-5 if they exist)
3. About page
4. Contact page
5. Privacy policy page
6. Terms of service page
7. Any "thin" looking pages from navigation

#### 3c. Per-Page Deep Analysis
For EACH page visited, document:
- **URL**: Full page URL
- **Title**: Page title tag content
- **Word Count Estimate**: Approximate word count of substantive content (exclude nav, footer, boilerplate)
- **Content Type**: Article, landing page, product page, about page, etc.
- **Content Depth**: Shallow (< 100 words), Thin (100-300 words), Adequate (300-600 words), Rich (600+ words)
- **Originality Assessment**: Does this appear to be original content or templated/generic?
- **Value Assessment**: Would a user find this page genuinely useful?
- **Navigation Working**: Can the user easily navigate to/from this page?
- **Ads Present**: Any existing ad placements visible?
- **Issues Found**: Specific problems detected

#### 3d. Technical Checks
Visit these specific URLs:
- `{domain}/ads.txt` — Check existence and validity
- `{domain}/privacy-policy` or `{domain}/privacy` — Check existence and completeness
- `{domain}/terms` or `{domain}/terms-of-service` — Check existence
- `{domain}/sitemap.xml` — Check existence
- `{domain}/robots.txt` — Check for issues

### 4. Run the Full Review

Using the data gathered in Step 3, systematically evaluate the site against EVERY criterion in `references/review-criteria.md`. Score each category.

#### Phase 1: Content Quality Assessment (HIGHEST PRIORITY)
This is the #1 reason sites get rejected. Be brutally honest.

**Minimum Content Requirements:**
- Does the site have enough pages with substantive content?
- Google typically wants to see **at least 15-30 pages of quality content** for a new site
- Each content page should have **at least 300-500+ words of original, useful text**
- Content must be in complete sentences and paragraphs, not just headlines or bullet points

**Content Value Signals (what Google reviewers look for):**
- Is there a clear niche/topic focus?
- Does the content demonstrate expertise, experience, authoritativeness, or trustworthiness (E-E-A-T)?
- Would a user bookmark or share this content?
- Does the site offer something competitors don't?
- Is there a reason for users to return?
- Is content regularly updated (check dates if visible)?

**Low Value Content Red Flags (what triggers rejection):**
- Pages with mostly images/video and little text
- Pages with only a few sentences
- Template/boilerplate content that looks auto-generated
- Content that exists solely to host ads
- Duplicate or near-duplicate content across pages
- Thin affiliate content without original value-add
- "Coming soon" or placeholder pages
- Pages behind login walls inaccessible to Google
- Content scraped or copied from other sites
- Pages optimized for keywords rather than users
- AI-generated content without human editorial value-add

**Content Depth Scoring:**
- Score each page: PASS (sufficient), WARN (borderline), FAIL (insufficient)
- Calculate overall site content score

#### Phase 2: User Experience & Navigation
- Is the site navigation clear, intuitive, and functional?
- Can users find content within 2-3 clicks?
- Is the menu/navigation bar well-organized?
- Are there broken links?
- Is the site mobile-responsive?
- Does the page load quickly?
- Is the layout clean and readable?
- Are there excessive pop-ups or interstitials?

#### Phase 3: Site Identity & Trust
- Is there a clear About page explaining who runs the site?
- Is there a Contact page with real contact information?
- Is the site purpose/niche immediately obvious?
- Does the site look professional and trustworthy?
- Is there an author/publisher identity established?

#### Phase 4: Technical Compliance
- **ads.txt**: Present, valid format, correct publisher ID?
- **Privacy Policy**: Exists, accessible, discloses cookies/tracking/third-party ads, mentions Google, opt-out info?
- **Terms of Service**: Present?
- **Cookie Consent**: Present for EU visitors?
- **HTTPS**: Is the site served over HTTPS?
- **Sitemap**: Does sitemap.xml exist?
- **Robots.txt**: Is it blocking important content?

#### Phase 5: Policy Compliance
- No prohibited content categories
- No ads on error pages, under-construction pages, or low-content pages
- Ad-to-content ratio (if ads already placed)
- Better Ads Standards compliance
- No deceptive/misleading content
- Content in a supported language

#### Phase 6: Search Engine Presence
- Does the site appear to be indexed by Google?
- Is there evidence of organic traffic potential?
- Are pages structured for discoverability (proper titles, meta descriptions, headings)?

### 5. Generate the Review Report

Produce a comprehensive, structured report:

```markdown
# AdSense Site Review Report

**Site:** [URL]
**Review Date:** [Date]
**Overall Verdict:** [APPROVE / LIKELY REJECT / REJECT]
**Confidence:** [High / Medium / Low]

---

## Executive Summary

[2-3 sentence summary of the site's AdSense readiness and the primary blocker(s)]

---

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

---

## Critical Issues (Must Fix Before Resubmitting)

[Numbered list of blocking issues with specific details and remediation steps]

1. **[Issue Title]**
   - **Where:** [Specific page(s) or site-wide]
   - **What Google Sees:** [Describe the problem from Google reviewer perspective]
   - **Why It Causes Rejection:** [Link to specific policy]
   - **How to Fix:** [Specific, actionable steps]
   - **Priority:** Critical

---

## Warnings (Should Fix)

[Issues that may contribute to rejection but aren't necessarily blocking alone]

---

## Passes (What's Working)

[Positive findings — important for morale and to avoid breaking what works]

---

## Page-by-Page Analysis

| Page | URL | Word Count | Content Depth | Status | Notes |
|------|-----|------------|---------------|--------|-------|
| [Page name] | [URL] | [count] | [Shallow/Thin/Adequate/Rich] | [PASS/WARN/FAIL] | [Key issues] |

---

## Technical Checks

| Check | Status | Details |
|-------|--------|---------|
| HTTPS | ✅/❌ | [details] |
| ads.txt | ✅/❌ | [details] |
| Privacy Policy | ✅/❌ | [details] |
| Terms of Service | ✅/❌ | [details] |
| Cookie Consent | ✅/❌ | [details] |
| Sitemap | ✅/❌ | [details] |
| Robots.txt | ✅/❌ | [details] |
| Mobile Responsive | ✅/❌ | [details] |

---

## Remediation Roadmap

### Priority 1: Critical (Do These First)
[Ordered list of critical fixes with estimated effort]

### Priority 2: Important (Do Before Resubmitting)
[Ordered list of important fixes]

### Priority 3: Recommended (Improves Chances)
[Ordered list of recommended improvements]

---

## Content Strategy Recommendations

[If content is the primary issue, provide specific guidance:]
- Recommended number of additional pages/posts needed
- Target word count per page
- Topic/niche focus recommendations
- Content structure recommendations (headings, paragraphs, images)
- Publishing frequency recommendations

---

## When to Resubmit

[Specific milestones that should be met before resubmitting to AdSense]

1. [ ] [Milestone 1]
2. [ ] [Milestone 2]
3. [ ] [Milestone 3]

**Estimated time to readiness:** [Based on scope of changes needed]
```

---

## Writing Rules

### Core Rules
- Be brutally honest — false passes waste the user's time and another rejection cycle
- Every finding must reference the specific Google policy it relates to
- Every issue must have a specific, actionable fix — not vague advice
- Score conservatively — if in doubt, flag it as a warning
- The #1 goal is to prevent another "low value content" rejection

### Assessment Rules
- Judge content as a Google reviewer would, not as a friend
- A page with 50 words of text and a large image is THIN content, period
- Template/framework boilerplate does NOT count as content
- Navigation text, footer text, and sidebar text do NOT count toward content word count
- "Coming soon", placeholder, and under-construction pages are automatic FAILs
- A site with fewer than 10 substantive content pages is almost certainly going to be rejected

### Report Rules
- Always include the page-by-page analysis table — this is the most actionable section
- Always include the remediation roadmap with priorities
- Always include specific "when to resubmit" criteria
- Never recommend resubmitting immediately unless the site genuinely passes all checks

---

## Output Format

The output should be the complete Review Report as specified in Step 5 above. The report uses markdown formatting with tables, headers, and checklists.

---

## References

**These files MUST be read using the Read tool before task execution (see Step 1):**

| File | Purpose |
|------|---------|
| `./references/review-criteria.md` | Complete scored review criteria matching Google's evaluation |
| `./references/low-value-content-signals.md` | Deep-dive on detecting and fixing "low value content" — the #1 rejection reason |
| `./references/common-rejections.md` | All common AdSense rejection reasons with specific fixes |
| `./references/sources.md` | Official Google documentation URLs for policy references |

**Why these matter:** The reference files encode the actual Google AdSense review criteria derived from official documentation, rejection patterns, and Google's own guidance. They ensure the review covers exactly what Google checks and that recommendations map directly to policy requirements.

---

## Quality Checklist (Self-Verification)

Before finalizing the review report, verify ALL of the following:

### Pre-Execution Check
- [ ] I read all reference files before starting
- [ ] I have the reference content in context

### Crawling Check
- [ ] I visited the homepage and took a snapshot
- [ ] I visited at least 10 pages (or all pages if fewer than 10)
- [ ] I checked ads.txt, privacy policy, sitemap.xml, robots.txt
- [ ] I documented word count and content depth for every page visited

### Assessment Check
- [ ] Content quality scored honestly, not generously
- [ ] Every score justified with specific evidence
- [ ] Low value content signals checked thoroughly
- [ ] Technical compliance fully verified
- [ ] Policy compliance checked against all categories

### Report Check
- [ ] Report follows the Output Format template exactly
- [ ] Every critical issue has a specific fix
- [ ] Page-by-page analysis table is complete
- [ ] Remediation roadmap is prioritized
- [ ] "When to resubmit" criteria are specific and measurable
- [ ] Overall verdict is justified by the scores

**If ANY check fails → revise before presenting.**

---

## Defaults & Assumptions

- **Target standard:** New site applying for AdSense (stricter review than established site)
- **Content minimum:** At least 15-30 pages of substantive (300+ word) original content
- **Privacy policy:** Must exist, be accessible, and mention third-party advertising/cookies
- **ads.txt:** Must exist at domain root with valid Google publisher entry
- **Navigation:** Must have clear, working navigation accessible from every page
- **Mobile:** Site must be mobile-responsive (Google reviews from mobile too)
- **Language:** Content must be primarily in an AdSense-supported language
- **Age of site:** Newer sites face stricter scrutiny — flag if domain appears very new
- **If no rejection reason provided:** Assume "low value content" and run full review
- **If specific rejection reason provided:** Prioritize that area but still run full review
