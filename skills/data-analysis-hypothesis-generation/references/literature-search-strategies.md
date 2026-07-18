# Literature Search Strategies

Grounding hypotheses in existing evidence. Three-phase approach: **broad exploration** (map the landscape) → **focused searching** (specific mechanisms/theories) → **citation mining** (follow references and "cited by" from key papers). Before searching, clarify: what aspects need evidence, what study types are relevant, what time frame, what level of evidence (mechanistic/correlational/causal).

## PubMed (biomedical / life sciences)

Use for clinical studies, molecular/cellular/physiological mechanisms, disease etiology, drug research. Techniques:
- **Start with reviews** — filter Article Type → Review / Systematic Review / Meta-Analysis; prefer the last 2–5 years for comprehensive reference lists.
- **MeSH terms** — standardized vocabulary captures terminology variants (search "Myocardial Infarction" to also catch "MI", "heart attack").
- **Boolean + syntax** — `AND` narrows, `OR` broadens (`(Alzheimer OR dementia)`), `NOT` excludes, quotes for exact phrases (`"oxidative stress"`), `gene*` wildcards.
- **Filters** — publication type (RCT, meta-analysis) and date (recent for cutting edge, historical for foundations).
- **Similar articles / Cited by** — expand from one highly relevant paper.

## General Web / Preprints

Use for non-biomedical science, interdisciplinary topics, recent preprints, grey literature, cross-domain analogies. Techniques:
- Field-specific terms (chemistry "mechanism/pathway"; physics "model/theory"; ecology "population dynamics").
- Academic source operators — `site:arxiv.org`, `site:biorxiv.org`, `site:edu`, `filetype:pdf`.
- Find authors/labs from a relevant paper; use Google Scholar "Cited by" / "Related articles" with date ranges.
- Combine specific phenomenon + general concept, with Boolean logic (`"spike protein" AND (transmissibility OR virulence) AND mutation`).

## Search by Goal

| Goal | Search components |
|------|-------------------|
| Mechanisms | phenomenon + "mechanism"/"pathway" + suspected molecules |
| Associations | A + B + "association"/"correlation"/"predicts" |
| Interventions | intervention + condition + "efficacy"/"RCT" |
| Methods | method name + application; "how to measure" + phenomenon |
| Analogous systems | mechanism + a different system/organism |

## Judging Source Quality

**Citations (relative to age/field):** 0–3 yr with 100+ = highly influential; 3–7 yr with 500+ = landmark; 7+ yr with 1000+ = foundational. Norms differ by field (biomedical high, math/physics lower with longer half-lives, CS weights conferences).

**Venue tiers:** Tier 1 = Nature/Science/Cell/NEJM/Lancet and field flagships (always prefer); Tier 2 = IF>10 specialized + top ML/AI conferences (NeurIPS/ICML/ICLR); Tier 3 = IF 5–10 society journals; Tier 4 = IF<5 (use sparingly). CS conference ranks: A* (NeurIPS/ICML/ICLR/CVPR/ACL) ≈ Nature/Science; A (AAAI/EMNLP/ECCV) ≈ Tier 2.

**Author track record** — h-index (>40 established, >20 early-career star), Tier-1 publications, leading institution, first/last authorship on cited papers; check Google Scholar / ORCID.

**Red flags** — predatory/low-impact venue, no track record, undisclosed conflicts, unclear methods, extraordinary claims without extraordinary evidence, contradicts a large body of evidence without explanation.

## Workflow & Time Budget

Straightforward hypothesis (30–60 min): 1–2 reviews + 3–5 primary papers + quick web scan. Complex (1–3 hr): multiple reviews, 10–15 primary papers, systematic cross-database search + citation mining. Contentious (3+ hr): systematic-review approach, map competing perspectives, track historical development.

Stop when you keep finding the same papers and multiple independent lines converge; search more if major gaps remain, evidence is single-source, or the hypothesis seems inconsistent with the literature.

## Documentation & Citation Organization

For each paper capture: full citation, key findings relevant to the hypothesis, design/methods, author-noted limitations, and how it relates. Group evidence by hypothesis, by method, by conflicting findings, and by knowledge gap.

For a report: **main text** cites 10–20 key papers (most influential/recent, directly supporting each hypothesis, major reviews); the **literature appendix** carries 40–60+ organized as background/context → current understanding → per-hypothesis evidence (8–15 each) → conflicting findings → gaps. Target 50+ total references.

## Pitfalls

Confirmation bias (search for *contradicting* evidence too) · recency bias (include foundational work) · too narrow (use OR/alternate terms) · too broad (add specific terms/filters) · single database · stopping too soon · cherry-picking (represent the full spectrum, acknowledge contradictions). Balance: hypotheses should be grounded in evidence yet extend it with novel, testable predictions — neither merely restating known mechanisms nor ignoring relevant evidence.
