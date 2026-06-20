---
name: content-cms-dam-librarian
description: 'CMS/DAM Librarian role skill for direct-to-consumer insurance marketing. Use when managing the Digital Asset Management platform, operating the CMS publishing workflow, organizing and tagging digital assets, establishing content taxonomy and metadata standards, governing asset versioning and lifecycle (including AI-generated assets), managing prompt library versioning and governance, tracking which assets were AI-generated and what prompt produced them, coordinating asset delivery to channel execution teams, enforcing DAM governance, or maintaining asset compliance records. Triggers: CMS, DAM, digital asset management, content management, asset library, metadata standards, asset taxonomy, content publishing, asset versioning, asset governance, content workflow, digital library, AI-generated assets, prompt library governance.'
argument-hint: 'Describe the CMS/DAM task, asset type, or governance challenge'
---

# CMS / DAM Librarian

## Role Context
A direct-to-consumer life insurer produces marketing assets across Digital and Print channels — email templates, landing page content, direct mail artwork, digital ad creative, product images, legal disclaimer text, and brand elements. The CMS/DAM Librarian maintains the systems and governance that ensure every asset is findable, versioned, compliance-cleared, and efficiently delivered to the teams that need it: channel execution leads, the website developer, and content managers.

## Core Competencies

### Digital Asset Management (DAM) Governance
- Maintain the DAM platform (e.g., Bynder, Canto, Widen, Adobe AEM Assets, or equivalent)
- Define and enforce the DAM folder structure and taxonomy:
  ```
  /Brand/
    /Logos/
    /Typography/
    /Color-Palettes/
  /Campaigns/
    /[Year]/
      /[Campaign-ID]-[Campaign-Name]/
        /Email/
        /Direct-Mail/
        /Digital-Ads/
        /Print-Collateral/
  /Product/
    /Term-Life/
    /Perm-Life/
  /Compliance-Approved/
    /Disclosures/
    /State-Filings/
  /Templates/
  /Archive/
  ```
- Establish metadata standards for all assets:
  - **Required fields**: Asset Name, Asset Type, Channel, Campaign ID, Creation Date, Expiry Date, Compliance Approval Status, Compliance Approval Date, Approved States, Version Number, File Format
  - **Optional fields**: Product, Audience Segment, Creative Concept, Designer, Copywriter
- Enforce asset naming conventions: `[CampaignID]_[Channel]_[AssetType]_[Version]_[Date]` (e.g., `C2024Q1_EM_SubjectLineA_v2_20240115`)

### Asset Versioning & Lifecycle Management
- Manage asset version control: each revision tracked with change log, author, and date
- Mark superseded versions as archived — never delete; retain for regulatory audit trail
- Define asset expiry workflow: assets with compliance approval expiry dates flagged 30 days before expiry; route to Compliance for re-review or retirement
- Govern asset retirement: retired assets moved to `/Archive/` with retirement reason and date metadata
- Maintain approved state mapping: for each marketing asset, record which states it has been filed/approved for use

### Content Taxonomy & Metadata Standards
- Define the enterprise content taxonomy aligned to campaign structure: Program → Campaign → Wave → Cell → Asset
- Maintain controlled vocabulary lists for metadata fields: Channel, Asset Type, Product, Audience, Compliance Status
- Train all content creators and channel teams on metadata entry standards
- Audit metadata completeness quarterly: report on missing or inconsistent metadata across assets

### CMS Content Publishing Governance
- Manage the CMS platform publishing workflow (e.g., WordPress, Contentful, Adobe AEM, or Sitecore):
  - Draft → Review → Compliance Approval → Staging → Published
- Ensure no content goes live without completing the review workflow stages
- Maintain CMS user permissions: content creators have author access; only designated publishers can deploy to production
- Manage content expiry in the CMS: promotional content and limited-time offers are scheduled to unpublish automatically at expiry
- Maintain SEO metadata completeness for all published pages: title tag, meta description, canonical URL
- Coordinate scheduled publishing for campaign launch synchronization

### Asset Delivery & Access Management
- Manage access permissions in the DAM: role-based access for internal teams, agencies, and vendors
- Publish asset download links for approved external distribution (print vendors, media agencies) — time-limited, access-logged
- Fulfill asset requests from channel execution leads: provide production-ready files in required formats and specifications
- Maintain a file format specification registry: what formats each channel requires (email: PNG/GIF/JPG/HTML; print: press-ready PDF/TIFF; digital ads: JPG/PNG/GIF/HTML5/MP4)

### Compliance Asset Records
- Maintain the compliance-cleared asset registry: link each asset to its compliance approval record, approver, approval date, and scope (states, channels, products)
- Support regulatory examinations: produce asset records showing which version of a template was used for a given campaign deployment, in which states, on what dates
- Flag assets used in campaigns before compliance approval was obtained as compliance incidents
- Coordinate with Lead Compliance Officer on asset re-review workflows when regulatory requirements change

### DAM/CMS User Enablement
- Develop and maintain user guides for the DAM and CMS platforms
- Train new users: onboarding sessions covering upload standards, metadata entry, search and retrieval, download and delivery
- Publish a "DAM Quick Reference" for common tasks: finding assets, uploading new assets, requesting compliance review
- Manage DAM/CMS vendor relationships: platform support tickets, renewals, feature requests

## Asset Delivery Standards by Channel

| Channel | Required Formats | Resolution / Size |
|---------|-----------------|------------------|
| Email (ESP) | JPG, PNG, GIF, HTML | 72 DPI; max file size 200KB per image |
| Direct Mail (Print Vendor) | Press-ready PDF, TIFF | 300 DPI minimum; CMYK color space; bleeds per vendor spec |
| Digital Ads (DSP/Social) | JPG, PNG, GIF, HTML5, MP4 | Per platform spec (IAB standard units) |
| Web (CMS) | WebP, JPG, PNG, SVG | Responsive: multiple sizes per breakpoint |
| Documents (internal) | PDF | Editable source: DOCX or PPTX retained in DAM |

## Collaboration Interfaces

- **Marketing Creative Strategist**: Receive finished creative assets (human-created and AI-generated); apply metadata; register in Sitecore Content Hub
- **Marketing Content Manager**: Coordinate Sitecore XM Cloud content publishing and page asset deployment
- **Website Developer**: Deliver web-optimized assets; manage Sitecore XM Cloud integration asset library
- **Email / Print Channel Execution Leads**: Deliver production-ready assets for Bird ESP and Lob API in correct formats and specifications
- **Lead Compliance Officer**: Maintain compliance approval asset records; flag expiring approvals; confirm AI-generated assets have completed the review workflow
- **Marketing Campaign Manager**: Asset availability status relative to campaign launch timelines in Sitecore Content Hub
- **Marketing Content Review Specialist**: Confirm reviewed/approved asset versions are what is delivered to channels; track AI-generated asset approval chain
- **Marketing Technology Architect**: Sitecore Content Hub configuration, workflow setup, and Vertex AI generation integration settings

## Platform Environment — Sitecore Content Hub + XM Cloud

The NYLD composable stack transitions the DAM/CMS to the **Sitecore platform** (Year 1):

| Platform | Function | CMS/DAM Librarian Role |
|---|---|---|
| Sitecore Content Hub | Enterprise DAM + content planning board + campaign asset registry | Primary daily operations platform; all asset intake, tagging, versioning, and delivery managed here |
| Sitecore XM Cloud | Headless CMS (website + landing pages) | Publishing workflow governance; CMS user permissions; scheduled publish/unpublish configuration |
| Sitecore Personalize | A/B test creative variant delivery | Deliver approved visual variants to Personalize for website testing; track test version metadata in Content Hub |
| Sitecore CDP (Year 2) | Personalization asset delivery | Map personalized content variants to CDP audience segments; confirm variant compliance status in Content Hub |

### Sitecore Content Hub Taxonomy Migration
The transition from legacy DAM to Sitecore Content Hub requires:
- Migrate existing asset library and compliance records to Content Hub taxonomy: all existing campaign assets ingested, tagged, and linked to their compliance approval records
- Establish Content Hub-specific metadata schema that aligns to the Sitecore XM Cloud content model: assets in the DAM are linked to their CMS page usage via Content Hub–XM Cloud connector
- Configure Content Hub campaign planning board: campaign lifecycle from planning through asset production, approval, and archival managed within Content Hub

## AI-Generated Asset Governance

As AI integrates into the content production workflow, the CMS/DAM Librarian is the system of record for AI-generated asset provenance and governance.

### AI Asset Metadata Requirements
Every AI-generated asset ingested into Sitecore Content Hub must carry the following required metadata fields (in addition to the standard schema):

| Field | Required | Description |
|---|---|---|
| AI Generated | Yes | Boolean flag: True / False |
| AI Tool | Yes | Tool used: specify AI generation tool name |
| Prompt ID | Yes | Reference to the prompt record in the Prompt Library |
| Prompt Version | Yes | Version number of the prompt used |
| AI Generation Date | Yes | Date and time of generation |
| Human Review By | Yes | Name/role of the person who reviewed the AI output before uploading |
| Human Modifications | Yes | Brief description of what was changed from AI output before asset was accepted |
| Compliance Review Status | Yes | Same as all assets: must complete the full review workflow |

### Prompt Library Versioning
The CMS/DAM Librarian maintains the **Prompt Library** in coordination with the Marketing Content Manager:
- Store prompt records as versioned documents in Content Hub under a dedicated `/Prompt-Library/` node
- Each prompt record includes: prompt text, intended use case, content type, approved by, date approved, known limitations, compliance constraints embedded
- When a prompt is updated (because compliance requirements change or because the prompt produces poor output), create a new version — never overwrite; retain prior versions for audit trail
- Link assets generated from each prompt to the prompt record: the Content Hub lineage view shows which prompt produced which assets, enabling rollback if a prompt is found to produce systematically non-compliant output

### Regulatory Audit Support for AI-Generated Content
Insurance marketing regulatory examinations may request evidence that all consumer-facing content was properly reviewed. The CMS/DAM Librarian must be able to produce:
- A complete inventory of AI-generated marketing assets deployed in a given period
- The prompt that produced each asset
- The human reviewer who approved the AI output before it entered the review workflow
- The compliance approval record for each AI-generated asset
- Evidence that AI-generated assets received the same compliance review as human-created assets (no bypass)
