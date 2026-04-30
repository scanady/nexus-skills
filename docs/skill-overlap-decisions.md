# Skill Overlap Decisions

Running log of decisions made during catalog overlap audits. Update this file after each audit to prevent re-litigating the same questions.

---

## How to Use This File

After running `node bin/cli.js audit-overlap`, record your decision for each reviewed cluster here. Future audits should check existing entries before flagging a pair as a new issue.

**Status values:** `pending` | `keep-as-is` | `keep-with-routing` | `merge` | `archive` | `rename`

---

## Active Decisions

<!--
Template — copy and fill in for each cluster:

### [cluster name or pair]
- **Skills:** `skill-a`, `skill-b`
- **Overlap type:** routing-collision | duplicate | umbrella-plus-specialist | adjacent-distinct
- **Score:** 0.xx
- **Status:** pending
- **Decision:** [keep-as-is | keep-with-routing | merge | archive | rename]
- **Rationale:** One sentence.
- **Action taken:** What was actually changed, or "none".
- **Last reviewed:** YYYY-MM-DD
-->

### tech-git-workflow ↔ tech-dev-commit-push
- **Skills:** `tech-git-workflow`, `tech-dev-commit-push`
- **Overlap type:** routing-collision (suspected)
- **Status:** keep-with-routing
- **Decision:** keep-with-routing
- **Rationale:** `tech-dev-commit-push` now owns commit/stage/push execution in the current repo, while `tech-git-workflow` owns branching, PR, release, and collaboration policy.
- **Action taken:** Tightened descriptions, narrowed triggers, added `anti-triggers`, cross-linked the pair, and renamed the execution skill to match its concrete output.
- **Last reviewed:** 2026-04-29

### tech-security-audit-lead ↔ tech-security-vulnerability-analyst
- **Skills:** `tech-security-audit-lead`, `tech-security-vulnerability-analyst`
- **Overlap type:** routing-collision (suspected)
- **Status:** keep-with-routing
- **Decision:** keep-with-routing
- **Rationale:** Reviewer now owns broad audit engagements across code, infra, and DevSecOps; vulnerability-analyst owns exploitability-first OWASP code analysis.
- **Action taken:** Tightened descriptions, narrowed triggers, added `anti-triggers`, and cross-linked the pair.
- **Last reviewed:** 2026-04-29

### research cluster
- **Skills:** `research-ai-landscape-brief`, `research-dtc-insurance-market-intelligence`, `research-analyst`, `research-weekly-ai-news`, `strategy-research-analyst`, `strategy-market-researcher`
- **Overlap type:** duplicate + routing-collision
- **Status:** keep-with-routing
- **Decision:** keep-with-routing
- **Rationale:** The skills split cleanly by domain specificity, cadence, and output type once the generic news, deep landscape, and strategy functions are stated explicitly.
- **Action taken:** Tightened descriptions and triggers, added `anti-triggers`, added routing priority, expanded related-skill links across the research cluster, and renamed the insurance skill to avoid duplicate naming with the AI landscape brief.
- **Last reviewed:** 2026-04-29

### strategy-market-researcher ↔ strategy-research-analyst
- **Skills:** `strategy-market-researcher`, `strategy-research-analyst`
- **Overlap type:** routing-collision
- **Score:** 0.33
- **Status:** keep-with-routing
- **Decision:** keep-with-routing
- **Rationale:** One skill owns decision-grade market sizing and diligence; the other owns signal scoring, threat assessment, and strategic intelligence.
- **Action taken:** Updated descriptions and triggers to separate sizing and diligence from scored intelligence products.
- **Last reviewed:** 2026-04-29

### marketing-seo-adsense-readiness ↔ marketing-seo-adsense-review
- **Skills:** `marketing-seo-adsense-readiness`, `marketing-seo-adsense-review`
- **Overlap type:** routing-collision or duplicate (suspected)
- **Status:** pending
- **Notes:** Both cover Google AdSense approval/readiness. Confirm whether one is pre-submission self-assessment and the other is a live-site rejection diagnosis — if so, sharpen descriptions to make that distinction explicit.
- **Last reviewed:** —

### social content writer cluster
- **Skills:** `marketing-content-engine`, `marketing-content-linkedin-writer`, `marketing-content-x-thread-builder`, `marketing-content-viral-hook`, `marketing-content-lead-magnet`
- **Overlap type:** umbrella-plus-specialist (expected)
- **Status:** keep-with-routing
- **Decision:** keep-with-routing
- **Rationale:** LinkedIn and X are valid specialists, but they needed platform-specific naming and wording so they no longer look like interchangeable writer templates.
- **Action taken:** Rewrote both descriptions around platform-native outputs, added metadata triggers and `anti-triggers`, linked them to adjacent social specialists, and renamed the X skill to remove the shared `...-writer` pattern.
- **Last reviewed:** 2026-04-29

### legal-compliance-creative-review ↔ legal-compliance-regulatory-monitor
- **Skills:** `legal-compliance-creative-review`, `legal-compliance-regulatory-monitor`
- **Overlap type:** merge-candidate
- **Status:** keep-with-routing
- **Decision:** keep-with-routing
- **Rationale:** Creative review is asset-specific pre-publication approval work; research analyst owns upstream monitoring, standards-register maintenance, and evidence-library creation.
- **Action taken:** Tightened descriptions, narrowed triggers, and added explicit `anti-triggers` separating review from research.
- **Last reviewed:** 2026-04-29

### agent-design-visual-identity ↔ agent-design-persona-creator
- **Skills:** `agent-design-visual-identity`, `agent-design-persona-creator`
- **Overlap type:** merge-candidate
- **Status:** keep-with-routing
- **Decision:** keep-with-routing
- **Rationale:** Icon creator owns visual identity assets; persona creator owns behavioral identity bundles and persona architecture.
- **Action taken:** Tightened descriptions, narrowed triggers, added `anti-triggers`, and cross-linked the pair.
- **Last reviewed:** 2026-04-29

### design-research-ux-researcher ↔ design-research-ux-artifacts
- **Skills:** `design-research-ux-researcher`, `design-research-ux-artifacts`
- **Overlap type:** umbrella-plus-specialist (suspected)
- **Status:** pending
- **Notes:** Researcher appears to cover process (interviews, synthesis, study planning); artifacts covers deliverables (personas, journey maps, IA, specs). Likely a valid split — confirm and add related-skills cross-links.
- **Last reviewed:** —

### data-eng-database-architect ↔ tech-database-optimizer
- **Skills:** `data-eng-database-architect`, `tech-database-optimizer`
- **Overlap type:** adjacent-distinct (expected)
- **Status:** pending
- **Notes:** Architect = greenfield schema/tech selection/HA design; optimizer = slow query diagnosis/index tuning/EXPLAIN ANALYZE. Different job. Expected to keep both — confirm trigger phrases don't compete.
- **Last reviewed:** —

---

## Archived Decisions

<!-- Move resolved decisions here once acted upon. -->

---

*Updated by: `node bin/cli.js audit-overlap`. See [skill-catalog-overlap-audit.md](skill-catalog-overlap-audit.md) for the full process.*
