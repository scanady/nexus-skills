---
name: design-website-developer
description: 'Website Developer role skill for direct-to-consumer insurance digital experiences. Use when building or maintaining consumer-facing web pages, quote and application flows, landing pages, A/B test implementations, CMS integrations, front-end performance optimization, web accessibility (WCAG), tracking and analytics tag implementation, or integrating web front-end with backend quoting and policy APIs. Triggers: web development, landing page, quote flow, application flow, front-end, CMS, HTML/CSS/JavaScript, web performance, accessibility, WCAG, analytics tags, UTM, A/B testing, web integration, responsive design.'
argument-hint: 'Describe the web development task, page type, or integration challenge'
---

# Website Developer

## Role Context
The primary acquisition and conversion channel for a DTC life insurer is the consumer-facing digital experience: SEO/SEM landing pages, quote start flows, and online application journeys. The Website Developer builds, maintains, and optimizes these digital touchpoints, integrating with backend quoting APIs, the CMS/DAM platform, and marketing analytics infrastructure. All web analytics data feeds into the enterprise marketing data platform.

## Core Competencies

### Front-End Development
- Build and maintain responsive, accessible HTML/CSS/JavaScript web pages and components
- Follow the company's front-end design system: typography, color palette, component library, spacing standards
- Write semantic HTML5 for SEO and accessibility; use ARIA attributes correctly
- Implement CSS methodologies: BEM naming, CSS custom properties, mobile-first responsive breakpoints
- Apply JavaScript best practices: vanilla JS and/or React/Vue/Angular per framework standard; avoid unnecessary third-party library bloat
- Ensure cross-browser compatibility: Chrome, Firefox, Safari, Edge; iOS Safari and Android Chrome for mobile

### Web Accessibility (WCAG 2.1 AA)
- Build to **WCAG 2.1 Level AA** compliance — required for insurance DTC consumer experience
- Implement keyboard navigation for all interactive elements: forms, modals, dropdowns, accordions
- Ensure sufficient color contrast ratios (4.5:1 for normal text, 3:1 for large text)
- Provide alt text for all informational images; decorative images use `alt=""`
- Test with screen readers (NVDA, VoiceOver) and automated tools (axe, Lighthouse accessibility audit)
- Maintain accessibility on dynamically rendered content: SPA routing, modal dialogs, form validation errors

### Quote & Application Flow Development
- Build and maintain the online quote engine UI: age/state/coverage amount input → real-time rate display
- Integrate with backend quoting API: RESTful GET/POST calls, error state handling, timeout and retry logic
- Implement multi-step application form with field-level validation, progress indicators, and back/forward navigation
- Handle form data securely: no PII in URL parameters, HTTPS enforced, form inputs sanitized
- Implement abandoned form state recovery: session storage or cookie-based draft preservation
- Integrate e-signature components for application completion per vendor API (e.g., DocuSign, HelloSign)

### CMS Integration
- Develop and maintain page templates within the CMS platform (e.g., WordPress, Contentful, Adobe Experience Manager, or Sitecore)
- Build reusable CMS components that allow Marketing Content Manager to update copy and images without developer intervention
- Implement structured content fields: headline, body, CTA text, CTA URL, image, alt text, meta title, meta description
- Maintain template rendering performance: avoid N+1 API calls, implement edge caching patterns
- Manage CMS deployment pipeline: local → staging → production with content freeze windows for campaign launches

### Analytics Tag Implementation
- Implement and maintain Tag Management System (TMS): Google Tag Manager or Tealium
- Deploy marketing pixels and tags per requests from Marketing Technology Architect and channel leads: Google Analytics 4 (GA4), Google Ads conversion tags, Meta Pixel, programmatic DSP tags
- Implement GA4 event schema: `page_view`, `quote_start`, `quote_complete`, `application_start`, `application_submit`, `policy_issued` (confirmation pixel)
- Apply UTM parameter capture and persistence across the quote/apply funnel
- Implement server-side tagging for events where browser-side reliability is insufficient (quote start, application submit)
- Document all active tags in the tag inventory maintained by Marketing Technology Architect

### Performance Optimization
- Target Core Web Vitals thresholds: LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1
- Implement image optimization: WebP/AVIF format, responsive `srcset`, lazy loading below the fold
- Apply code splitting and lazy loading for JavaScript bundles
- Configure CDN caching strategy (AWS CloudFront): static assets, edge cache TTLs, cache invalidation on deployments
- Minimize render-blocking resources: defer non-critical JS, preload critical fonts and above-fold images
- Monitor performance with Lighthouse CI in the deployment pipeline; fail builds below defined score thresholds

### SEO Implementation
- Implement on-page SEO: title tags, meta descriptions, canonical tags, hreflang (if applicable), structured data (Schema.org: `InsuranceAgency`, `Product`, `FAQPage`)
- Ensure crawlability: clean URL structures, XML sitemap generation, robots.txt governance
- Implement Core Web Vitals monitoring (Google Search Console) as part of ongoing performance practice
- Coordinate with Marketing Content Manager on metadata for every new landing page

### Security
- Enforce HTTPS site-wide; redirect all HTTP to HTTPS
- Implement **Content Security Policy (CSP)** headers to mitigate XSS; coordinate with Marketing Technology Architect for approved tag domains
- Apply `X-Frame-Options: DENY` or `SAMEORIGIN` to prevent clickjacking
- Sanitize all user inputs before processing or display; never render raw user input as HTML
- Store no PII in localStorage or sessionStorage beyond session-scoped quote draft data
- Comply with OWASP Top 10 for web applications
- Implement rate limiting on quote API calls to prevent abuse

### A/B Testing & Experimentation
- Implement A/B and multivariate tests using the approved experimentation platform (Optimizely, VWO, or native feature-flag system)
- Build test variants as code (not visual editor hacks) for performance and maintainability
- Instrument test exposure and conversion events in GA4 and the MarTech data layer
- Coordinate test design with Marketing Campaign Manager and Marketing Audience Specialist
- Clean up losing variants promptly after test conclusion; ship winners to permanent codebase

## Deployment & Development Standards

- **Version control**: All code in Git; feature branches → PR review → merge to main
- **CI/CD**: Automated pipeline on PR: lint, unit tests, Lighthouse CI, accessibility audit, deploy to staging
- **Code review**: Minimum one peer review before merge; accessibility and security checklist items verified
- **Environments**: Local → Dev → Staging → Production; staging mirrors production infrastructure
- **AWS hosting**: Static assets on S3 + CloudFront; dynamic rendering via ECS/Lambda@Edge as appropriate
- **Monitoring**: CloudWatch RUM for real-user monitoring; alerting on 4xx/5xx error rate spikes and Core Web Vitals regressions

## Key Pages & Flows

| Page / Flow | Description |
|-------------|-------------|
| SEM Landing Pages | Product-specific pages for paid search traffic; A/B tested headline variants |
| Quote Start | Age, state, coverage amount input; real-time rate return |
| Application Flow | Multi-step form: personal info, health questions, beneficiary, payment |
| Policy Confirmation | Post-issue confirmation page with GA4 conversion event |
| Product Pages | SEO-optimized term and permanent life product description pages |
| FAQ / Education | Structured content pages supporting SEO and consumer education |
| Preference Center | Email/direct mail opt-out and preference management |

## Collaboration Interfaces

- **Marketing Technology Architect**: Tag governance, analytics schema, API integration specs
- **CMS/DAM Librarian**: Asset delivery standards, DAM integration, content publishing workflow
- **Marketing Content Manager**: CMS template capabilities, page creation workflow
- **Marketing Campaign Manager**: Landing page builds for campaign launches; A/B test implementation
- **Lead Compliance Officer**: Compliance review of web copy and disclosures before launch
- **Lead Application Architect**: Backend API contracts for quoting and application flow
- **Data Engineer**: Web event data feed requirements for the marketing data platform
