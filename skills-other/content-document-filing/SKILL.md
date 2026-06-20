---
name: content-document-filing
description: 'Document filing skill for project repositories. Use when saving, creating, moving, or reviewing the placement of any document in the Documents/ directory. Ensures every file is placed in the correct topic folder, has valid YAML frontmatter, and that superseded revisions are moved to _versions/ subfolders. Triggers: save document, new document, where does this go, file this document, move document, create document, wrong folder, add frontmatter, document location, document organization, filing rules, organize document, place file, document index, update index.'
argument-hint: 'Provide the document filename, a one-line description of its content, and (optionally) the workstream it belongs to (WS2, WS3, All, IBM, or Governance). The skill will determine the target folder, generate the required YAML frontmatter, and specify whether any existing file must be moved to _versions/.'
---

# Document Filing

## Role Purpose

The Document Filing skill enforces a project repository's document organization rules. Any file created or moved into `Documents/` must be placed in the correct topic folder, carry valid YAML frontmatter, and — when it supersedes an existing version — trigger relocation of the prior file into `_versions/`.

The controlling principle is **topic-first organization**: files are organized by *what they are about*, not by who created them or what format they use. The master catalog at `Documents/INDEX.md` must be kept current after every filing operation.

---

## Phase 0: Pre-Processing Checklist

Before filing any document, collect:

1. **Filename** — exact name the file will have on disk
2. **Content description** — one sentence describing what the document covers
3. **Workstream** — `WS2`, `WS3`, `All`, `IBM`, or `Governance`
4. **Document type** — see the type vocabulary below
5. **Status** — `current`, `superseded`, or `draft`
6. **Version tag** (if applicable) — e.g. `R10`, `v1`, `EJM`, `R5`
7. **Supersedes** (if applicable) — filename of the file this new version replaces

If any of these are unclear, ask before proceeding.

---

## Phase 1: Folder Routing Rules

Apply the **first matching rule** from this list.

### Rule 1 — Governance
**Route to:** `Documents/Governance/`

File belongs here if it is any of:
- An enterprise-wide standard, principle, or policy document
- An API or technical specification that applies across workstreams
- A constitution, charter template, or rules-of-engagement document

Examples: `Architecture_Principles.md`, `constitution.md`, `NYLD_STANDARDS_DATA_VAULT_2_0.MD`, `NYLD_Customer_Experience_API_Layer_Spec_v1.md`

Frontmatter `workstream: All`, `doc_type: standard | spec | policy`

---

### Rule 2 — WS2 Data Foundation
**Route to:** `Documents/Workstreams/WS2_Data_Foundation/`  
**Superseded versions route to:** `Documents/Workstreams/WS2_Data_Foundation/_versions/`

File belongs here if it is any of:
- A WS2 assessment, analysis, or evaluation document
- A signal data source mapping document
- A WS2 roadmap or workstream-specific roadmap
- A WS2 slide summary or slide deck source
- Any document whose primary subject is: event hub, data governance, Initiative G, Initiative I, signal inventory, or the WS2 use case backlog

Scope markers in filename: `W2_`, `WS2_`, `Signal_Data_Source_Mapping`

Frontmatter `workstream: WS2`

---

### Rule 3 — WS3 Foundational Platforms
**Route to:** `Documents/Workstreams/WS3_Platforms/`  
**Superseded versions route to:** `Documents/Workstreams/WS3_Platforms/_versions/`

File belongs here if it is any of:
- A WS3 assessment, analysis, or evaluation document
- A WS3 timing and staffing document
- A WS3 roadmap or workstream-specific roadmap
- A WS3 slide summary or slide deck source
- A WS3 hypothesis testing separation analysis
- Any document whose primary subject is: Sitecore Content Hub, Sitecore XM Cloud, Compliance AI (Initiative D), GenAI content (Initiative C), CMS portal upgrade, web portal, A/B testing platform, email delivery, direct mail, or the WS3 operating model

Scope markers in filename: `W3_`, `WS3_`

Frontmatter `workstream: WS3`

---

### Rule 4 — POV and Gap Analysis
**Route to:** `Documents/POV_and_Gap_Analysis/`  
**Superseded versions route to:** `Documents/POV_and_Gap_Analysis/_versions/`

File belongs here if it is any of:
- An NYLD Point of View document
- A gap analysis comparing IBM deliverables against NYLD's plan or POV
- An analysis of IBM-supplied documents
- An architecture or implementation analysis (analysis_findings, project_implementation_analysis)
- An executive overview or comparison brief that is analytical rather than a roadmap
- A PDF or image that is a binary sibling of any of the above

Scope markers in filename: `POV_`, `GAP_ANALYSIS`, `analysis_findings`, `project_implementation_analysis`, `IBM_SUPPLIED`, `IBM_PLAN_VS`, `IBM_vs_`, `ECL_DIAGRAM_VS`, `Real_Time_Spine_vs`

Frontmatter `workstream: All | IBM`, `doc_type: pov | gap-analysis | analysis`

---

### Rule 5 — Hypothesis Testing
**Route to:** `Documents/Hypothesis_Testing/`  
**Superseded versions route to:** `Documents/Hypothesis_Testing/_versions/`

File belongs here if it is any of:
- An NYLD hypothesis test plan
- A hypothesis test storyboard (HTML or MD)
- A competitive or comparative storyboard used in hypothesis validation
- Any document whose primary subject is: validating IBM's four core hypotheses (Trigger Events Response Value, Audience Granularity Value, Journey Orchestration Value, Cross-Channel Coordination Value)

Scope markers in filename: `Hypothesis_Test`, `Storyboard`

Frontmatter `workstream: All`, `doc_type: hypothesis`

---

### Rule 6 — Roadmaps
**Route to:** `Documents/Roadmaps/`

File belongs here if it is any of:
- The master NYLD PAS transformation roadmap (applies across all workstreams)
- A marketing stack or MarTech platform plan that spans multiple workstreams
- A high-level timeline or phase plan not tied to a single workstream
- A PNG/image rendering of a roadmap or plan diagram

> **Note:** Workstream-specific roadmaps (WS2-only, WS3-only) belong in their respective workstream folders (Rule 2 or Rule 3), not here.

Scope markers in filename: `Roadmap`, `Plan_v`, `Marketing_Stack_Plan`, `NYLD_Plan_`

Frontmatter `workstream: All`, `doc_type: roadmap`

---

### Rule 7 — IBM Supplied
**Route to:** `Documents/IBM_Supplied/`

File belongs here if it is:
- A document delivered directly by IBM (raw deliverable, not NYLD's analysis of it)
- Prefixed with `IBM_` and not a gap analysis or NYLD-authored comparison

> IBM-supplied files already have internal prefixed subgrouping (`_arch`, `_biz`, `_ecl`, `_fin`, `_IBM`, `_road`). Maintain that convention for new IBM-supplied files.

---

### Rule 8 — Presentations
**Route to:** `Documents/Presentations/`

File belongs here if it is:
- A self-contained HTML presentation file rendered in the branded template
- A PowerPoint or slide deck export (PDF, PPTX)
- A presentation built with the `html-presentation-maker` or `ted-executive-deck` skills

> If an HTML presentation has a corresponding `.md` source document, the `.md` goes to the appropriate topic folder (Rules 1–6); the rendered `.html` goes here.

---

### Rule 9 — Research
**Route to:** `Documents/Research/`

File belongs here if it is:
- An external research article or industry study
- A Gartner or analyst report
- A MarTech, data platform, or technology market research document
- A document authored entirely by a third party (not IBM, not NYLD)

---

### Rule 10 — Archive
**Route to:** `Documents/Archive/`

Use sparingly. Files in Archive are those that predate the `_versions/` pattern and cannot be clearly mapped to a current canonical document. Do not route new work here — use `_versions/` inside the appropriate topic folder instead.

---

## Phase 2: Frontmatter Generation

Every `.md` file saved into `Documents/` (and its subfolders) **must** have YAML frontmatter as the first content in the file.

### Required Frontmatter Schema

```yaml
---
title: "<Human-readable title>"
date: YYYY-MM-DD
status: current          # current | superseded | draft
workstream: WS2          # WS2 | WS3 | All | IBM | Governance
doc_type: assessment     # see vocabulary below
version: "R10"           # omit if not versioned
related:
  - relative/path/to/related-file.md
---
```

### `doc_type` Vocabulary

| Value | Use for |
|-------|---------|
| `standard` | Enterprise standards, principles, naming conventions |
| `spec` | Technical specifications, API contracts |
| `policy` | Governance policies, rules of engagement |
| `assessment` | WS2 or WS3 full-detail assessment documents |
| `analysis` | Architecture, implementation, or findings analysis |
| `gap-analysis` | IBM vs NYLD comparison documents |
| `pov` | NYLD Point of View documents |
| `hypothesis` | Hypothesis test plans and storyboards |
| `roadmap` | Transformation roadmaps and platform plans |
| `presentation` | Slide deck summaries and slide sources |
| `index` | The INDEX.md catalog itself |

### `status` Values

| Value | Meaning |
|-------|---------|
| `current` | Authoritative version — use this |
| `superseded` | Replaced by a newer file — moved to `_versions/` |
| `draft` | In-progress, not yet authoritative |

### Frontmatter Rules

1. `date` must be the document's authored/published date in `YYYY-MM-DD` format, not today's date unless the document is being created today.
2. `title` must be a human-readable phrase, not a filename.
3. `related` must use paths **relative to the file's own location**, not absolute paths.
4. `version` is omitted if the document has no version tag (not all documents have versions).
5. All frontmatter values that contain colons or special characters must be quoted.

---

## Phase 3: Versioning Protocol

When a new document supersedes an existing one:

### Step 3.1 — Identify the incumbent
Find the existing file that the new document replaces. The incumbent is the file with the same topic coverage and a lower or earlier version/date.

### Step 3.2 — Move the incumbent to `_versions/`
Use `git mv` to relocate the incumbent:
```
git mv Documents/<folder>/<incumbent.md> Documents/<folder>/_versions/<incumbent.md>
```

### Step 3.3 — Update the incumbent's frontmatter
Change `status: current` → `status: superseded` in the moved file.  
Add or update `related` to point to the new current file.

### Step 3.4 — Set the new file's frontmatter
Set `status: current`.  
Add `related` entries pointing to the superseded file(s).

### Step 3.5 — Update INDEX.md
Move the incumbent row in INDEX.md to the `> **Superseded:**` note under the folder section.  
Add the new file as a `current` row in the table.

---

## Phase 4: INDEX.md Maintenance

`Documents/INDEX.md` is the master catalog. It must be updated whenever:
- A new file is added to any topic folder
- A file is moved to `_versions/`
- A file's status changes

### INDEX.md Row Format

```markdown
| [Folder/filename.md](Folder/filename.md) | doc_type | version | **current** | One-line description |
```

Rules:
- Links use paths relative to `Documents/` root
- Spaces in filenames must be URL-encoded (`%20`) in the link target
- Only `current` files appear in the main tables; superseded files appear only in the `> **Superseded:**` note beneath each section
- The index date at the bottom must be updated

---

## Phase 5: Filing Confirmation Output

After completing a filing operation, output a brief confirmation in this format:

```
✅ Filed: <filename>
   Folder:    Documents/<target-folder>/
   Status:    current | superseded | draft
   Frontmatter: added | already present | updated
   Supersedes: <incumbent filename> → moved to _versions/ | N/A
   INDEX.md:  updated | needs manual update
```

If any rule was ambiguous or required judgment, explain the routing decision in one sentence.

---

## Quick-Reference Decision Tree

```
Is it an IBM raw deliverable?           → IBM_Supplied/
Is it external research/article?        → Research/
Is it a branded HTML presentation?      → Presentations/
Is it a standard/spec/policy/constitution → Governance/
Is it WS2-scoped content?              → Workstreams/WS2_Data_Foundation/
Is it WS3-scoped content?              → Workstreams/WS3_Platforms/
Is it a comparison/gap/POV/analysis?    → POV_and_Gap_Analysis/
Is it a hypothesis test plan/storyboard? → Hypothesis_Testing/
Is it a cross-workstream roadmap/plan?  → Roadmaps/
Is it a legacy file pre-dating _versions? → Archive/ (last resort)
```
