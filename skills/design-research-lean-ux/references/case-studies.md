# Case Studies

Four composite scenarios (not specific companies) showing hypothesis-driven design, collaborative practice, and outcome metrics in different contexts.

## 1. Enterprise Product Team

**Context** — B2B SaaS, 12-person team, shipped 15 features in a year yet net revenue retention flat and NPS 42 → 35. Caught in the output trap: sales requests → specs → wireframes → build, no feedback loop.

**Intervention** — Assumption workshop surfaced 24 assumptions; three were high-risk/high-uncertainty: Gantt charts (sales-driven, no research), churn-from-missing-integrations (12% survey response), "onboarding is fine" (no funnel data).
- **Gantt** — clickable prototype, 8 users: 6 couldn't finish, 5 preferred spreadsheets. **Invalidated → removed, saved 3 months.**
- **Integrations** — concierge MVP (manual Zapier for 15 at-risk accounts): 9 used it, churn-intent down 35%. **Partially validated → built native for top 3.**
- **Onboarding** — instrumented existing flow: only 28% completed; completers retained 2.4×. **Validated → redesigned via Design Studio, tested with 5 before build.**

**Outcome (3 months)** — features/quarter 5 → 3 (all validated), hypotheses tested 0 → 11, NPS 35 → 41, onboarding completion 28% → 52%, 90-day churn 18% → 14%, 4 roadmap items removed. **Lesson:** fewer features, better outcomes; the hardest part was cultural (the Sales VP convinced by user-test videos).

## 2. Startup

**Context** — 6-person personal-finance app for freelancers, $400K/8-month runway, 200 beta users, 30-day retention 15%. Building the wrong next feature could sink the company.

**Intervention** — assumption mapping → test retention, monetization, bank-sync value.
- **Retention** — interviewed 8 churned users: 6 "forgot the app existed." Manual weekly email summaries to 50 users → 30-day retention 32% vs 15% control. **Validated — the problem was triggers, not features.**
- **Monetization** — smoke test for "tax estimation" at $9/mo: 12% clicked, 4% gave email (weak). Interviews revealed they wanted *peace of mind*, not a calculator. **Pivoted** to a "tax set-aside" feature.
- **Bank sync** — Wizard of Oz (manual categorization for 10 users): 8 logged in more, strong feedback. **Validated → used a third-party API.**

**Outcome (2 months)** — 30-day retention 15% → 34%, WAU 30 → 68, 3 validated features built, 5 removed from backlog, 14 hypotheses tested. **Lesson:** the 2-hour email beat the 6-week tax feature; speed of learning was the edge.

## 3. Agency

**Context** — 40-person agency, deliverable-heavy (pixel-perfect decks, 8–12-week projects), frequent post-handoff change requests eroding margins. Pilot: checkout redesign to cut 72% abandonment.

**Intervention** — Lean UX kick-off replaced the creative brief: 2-hour assumption workshop with client + dev team (16 assumptions), hypothesis prioritization (form length / hidden shipping / guest checkout), 90-min Design Studio with client's developer and marketer. Clickable prototype tested with 6 *actual customers*: form length was fine; **hidden shipping cost was the real trigger** (5 of 6). Revised to show shipping estimate on the cart page, retested with 5 new users — all completed.

**Outcome** — project 10 weeks → 4, designer hours 320 → 140, revision rounds 4–5 → 1, user tests before launch 0 → 11 users, abandonment 72% → 58%, margin 18% → 34%. **Lesson:** clients didn't want 60-page decks — they wanted confidence the design works; testing delivered it faster and cheaper. The agency now sells "Lean UX Sprints."

## 4. Internal Tools Team

**Context** — 4-person team for a 200-person logistics company, 9-month backlog, no research ever ("we know our users"). Recent features underused (barcode scanner used by 2 of 15 staff; dispatcher dashboard abandoned in a week).

**Intervention** — assumption audit found every backlog item was department-head assumption with zero validation. **Went to the gemba** — 3 days observing: warehouse staff needed *speed* (scanner 3s vs 0.5s manual); dispatchers abandoned the dashboard over one missing field (driver phone); service agents toggled 4 systems per ticket. Rapid tests:
- Add phone field + call button (30-min change) → dashboard adoption 0% → 73% in a week. **Validated.**
- Paper prototype of a unified service view, 4 agents → faster, strongly preferred. **Validated.**
- Faster barcode library (0.4s) prototype, 5 staff → all preferred. **Validated.**

**Outcome (2 months)** — backlog validated-before-build 0% → 100%, feature adoption 33% → 90%, request-to-validated-solution 3 months → 2 weeks, 7 items removed. **Lesson:** "we know our users" was the most dangerous assumption; direct observation had the highest ROI.

## Cross-Cutting Themes
- Assumptions are invisible until surfaced → start with a workshop
- Observation beats opinion → go to the gemba
- Small experiments prevent big waste → lowest fidelity that answers the question
- Invalidation is valuable → removing features rivals building them
- Shared understanding beats documentation → design and observe research together
- Outcomes reveal the truth → measure behavior change, not delivery
